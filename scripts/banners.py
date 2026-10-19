"""Fetch metadata for standalone Markdown links marked with "!banner".

Usage: python3 -m scripts enrich content/posts/2026-10-example.md
Successful requests are cached; failed page/image requests are retried on rerun.
Use --refresh to fetch successful pages and images again. Fenced code is skipped.
Only this explicit command accesses the network; Hugo never does.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 20 * 1024 * 1024
USER_AGENT = "Mozilla/5.0 (compatible; Log4D banner metadata fetcher)"
IMAGE_SUFFIXES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
}
LINK_RE = re.compile(
    r"(?P<before>\[[^\n]+\]\((?P<url>https?://[^\s]+)\s+)"
    r"""(?P<quote>["'])!banner(?P<metadata>(?: (?:(?!(?P=quote)).)*)?)(?P=quote)"""
    r"(?P<after>\)[ \t]*(?:\r?\n)?$)"
)
IMAGE_RE = re.compile(r"^\((/images/[^)]+)\)(?:\s|$)|^(/images/\S+)")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, str] = {}
        self.article_depth = 0
        self.article_image = ""
        self.link_image = ""
        self.oembed_url = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "article":
            self.article_depth += 1
        if tag == "img" and self.article_depth and not self.article_image:
            self.article_image = values.get("src") or ""
        if tag == "link":
            if values.get("rel") == "image_src":
                self.link_image = values.get("href") or ""
            if values.get("type") == "application/json+oembed":
                self.oembed_url = values.get("href") or ""
        if tag != "meta":
            return
        key = (values.get("property") or values.get("name") or "").lower()
        content = (values.get("content") or "").strip()
        if key and content:
            self.meta.setdefault(key, content)

    def handle_endtag(self, tag: str) -> None:
        if tag == "article":
            self.article_depth = max(0, self.article_depth - 1)


def fetch(url: str) -> tuple[bytes, str, str, str]:
    if urlparse(url).scheme not in {"http", "https"}:
        raise ValueError("only HTTP(S) URLs are supported")
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=20) as response:
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError("response exceeds 20 MiB")
        return (
            body,
            response.geturl(),
            response.headers.get_content_type(),
            response.headers.get_content_charset() or "utf-8",
        )


def page_metadata(url: str) -> dict[str, str]:
    body, page_url, content_type, charset = fetch(url)
    if content_type not in {"text/html", "application/xhtml+xml"}:
        raise ValueError(f"link is not an HTML page ({content_type})")
    parser = MetadataParser()
    parser.feed(body.decode(charset, errors="replace"))
    image = (
        parser.meta.get("og:image")
        or parser.meta.get("twitter:image")
        or parser.meta.get("twitter:image:src")
        or parser.link_image
        or parser.article_image
    )
    description = next(
        (
            parser.meta[key]
            for key in ("og:description", "twitter:description", "description")
            if key in parser.meta
        ),
        "",
    )
    metadata = {
        "image_url": urljoin(page_url, image) if image else "",
        "description": " ".join(description.split()),
        "local_image": "",
    }
    if not image:
        is_youtube = urlparse(page_url).hostname in {
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
            "youtu.be",
        }
        endpoint = parser.oembed_url
        if not endpoint and is_youtube:
            endpoint = "https://www.youtube.com/oembed?" + urlencode(
                {"url": url, "format": "json"}
            )
        if endpoint:
            body, _, _, charset = fetch(urljoin(page_url, endpoint))
            embedded = json.loads(body.decode(charset))
            value = embedded.get("thumbnail_url")
            if isinstance(value, str) and value.strip():
                metadata["image_url"] = value
            if is_youtube:
                # YouTube's fallback HTML describes the service, not the video.
                metadata["description"] = ""
    return metadata


def download_image(url: str, month: str) -> str:
    data, _, content_type, _ = fetch(url)
    if content_type not in IMAGE_SUFFIXES:
        raise ValueError(f"unsupported image type ({content_type})")
    filename = (
        "banner-" + hashlib.sha256(data).hexdigest()[:16] + IMAGE_SUFFIXES[content_type]
    )
    target = ROOT / "static" / "images" / month / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_bytes(data)
    return f"/images/{month}/{filename}"


def local_image_exists(path: str) -> bool:
    return (
        path.startswith("/images/") and (ROOT / "static" / path.lstrip("/")).is_file()
    )


def metadata_cache_path(url: str, month: str) -> Path:
    digest = hashlib.sha256((url + "\n" + month).encode()).hexdigest()
    return ROOT / ".cache" / "banner-metadata" / (digest + ".json")


def cached_metadata(url: str, path: Path, refresh: bool) -> dict[str, str]:
    # A normal rerun must reuse metadata, including when only the local image is missing.
    if path.exists() and not refresh:
        try:
            entry = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(entry, dict) and all(
                isinstance(entry.get(key), str)
                for key in ("image_url", "description", "local_image")
            ):
                print(f"cache hit: {url}")
                return entry
        except (ValueError, OSError) as error:
            print(f"ignoring unreadable cache {path}: {error}", file=sys.stderr)
    return page_metadata(url)


def save_json(path: Path, entry: dict) -> None:
    text = json.dumps(entry, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def update_file(path: Path, refresh: bool = False, retry_missing: bool = False) -> bool:
    month_match = re.match(r"(\d{4})-(\d{2})-", path.name)
    if not month_match:
        raise ValueError("Markdown filename must start with YYYY-MM-")
    month = "".join(month_match.groups())
    source = path.read_text(encoding="utf-8")
    lines = []
    fence = ""
    failed = False
    changed = 0
    for line in source.splitlines(keepends=True):
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker, suffix = fence_match.groups()
            if not fence:
                fence = marker
            elif (
                marker[0] == fence[0]
                and len(marker) >= len(fence)
                and not suffix.strip()
            ):
                fence = ""
            lines.append(line)
            continue
        match = None if fence else LINK_RE.fullmatch(line)
        if match:
            url = match.group("url")
            old_metadata = html.unescape(match.group("metadata")).strip()
            old_image_match = IMAGE_RE.match(old_metadata)
            old_image = (
                next(filter(None, old_image_match.groups())) if old_image_match else ""
            )
            refresh_link = refresh or (
                retry_missing and not local_image_exists(old_image)
            )
            cache_path = metadata_cache_path(url, month)
            # Adopt existing complete markers without downloading them again.
            if (
                not refresh_link
                and not cache_path.exists()
                and local_image_exists(old_image)
            ):
                lines.append(line)
                continue
            try:
                entry = cached_metadata(url, cache_path, refresh_link)
                save_json(cache_path, entry)
                local_image = entry["local_image"]
                if (
                    old_metadata
                    and not refresh_link
                    and (
                        not entry["image_url"]
                        or (
                            local_image_exists(local_image)
                            and local_image_exists(old_image)
                        )
                    )
                ):
                    lines.append(line)
                    continue
                if entry["image_url"] and not local_image_exists(local_image):
                    try:
                        local_image = download_image(entry["image_url"], month)
                        entry["local_image"] = local_image
                    except (URLError, OSError, ValueError) as error:
                        print(f"image unavailable {url}: {error}", file=sys.stderr)
                        failed = True
                save_json(cache_path, entry)
                if not local_image_exists(local_image):
                    local_image = old_image if local_image_exists(old_image) else ""
                description = entry["description"]
                metadata = " ".join(
                    part
                    for part in (f"({local_image})" if local_image else "", description)
                    if part
                )
                if metadata:
                    title = html.escape("!banner " + metadata, quote=True)
                    updated = (
                        match.group("before") + '"' + title + '"' + match.group("after")
                    )
                    changed += updated != line
                    line = updated
                print(
                    f"{url}: image {'saved' if local_image else 'empty'}, description {'saved' if description else 'empty'}"
                )
            except (URLError, OSError, ValueError, LookupError) as error:
                print(f"failed {url}: {error}", file=sys.stderr)
                failed = True
        lines.append(line)
    result = "".join(lines)
    if result != source:
        path.write_text(result, encoding="utf-8")
    print(f"{path}: {changed} banner link(s) updated")
    return not failed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh", action="store_true", help="refetch successful pages and images too"
    )
    parser.add_argument(
        "--retry-missing",
        action="store_true",
        help="refetch page metadata for cards without a local image",
    )
    parser.add_argument("files", nargs="+", help="Markdown files to update")
    args = parser.parse_args(argv)
    success = True
    for arg in args.files:
        path = Path(arg)
        if not path.is_absolute():
            path = ROOT / path
        try:
            success = (
                update_file(
                    path, refresh=args.refresh, retry_missing=args.retry_missing
                )
                and success
            )
        except (OSError, ValueError) as error:
            print(f"failed {path}: {error}", file=sys.stderr)
            success = False
    return 0 if success else 1

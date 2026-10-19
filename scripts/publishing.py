"""Build-artifact URL conversion and publication verification."""

from __future__ import annotations

import json
import re
import subprocess
import time
from datetime import datetime, timezone
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def settings(root: Path) -> dict[str, str]:
    values = json.loads((root / "scripts/publishing.json").read_text())
    if not values.get("cdn_url", "").startswith("https://"):
        raise ValueError("scripts/publishing.json: cdn_url 必须为 HTTPS URL。")
    values["cdn_url"] = values["cdn_url"].rstrip("/")
    return values


def site_url(root: Path, hugo: str) -> str:
    output = subprocess.run(
        [hugo, "config", "--environment", "production", "--format", "json"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    # Ask Hugo to resolve its own configuration; do not duplicate baseURL or parse YAML.
    return json.loads(output.stdout)["baseurl"].rstrip("/")


def rewrite_cdn(source: str, site: str, cdn: str) -> str:
    # Keep escaping, whitespace, and code outside URL tokens intact. This handles
    # HTML, feed entities, Markdown links/references, and !banner image markers.
    boundary = r"""(?P<before>["'(<]|&(?:quot|apos|#34|#39|lt);|\]:[ \t]+)"""
    path = cdn.rstrip("/").split("/", 3)[-1]
    public_path = path.split("/")[-1]
    pattern = boundary + r"(?:" + re.escape(site.rstrip("/")) + r")?/images/"
    result = re.sub(pattern, lambda m: m["before"] + cdn.rstrip("/") + "/", source)
    if path.startswith("img"):
        result = re.sub(
            boundary + re.escape(public_path) + "/",
            lambda m: m["before"] + cdn.rstrip("/") + "/",
            result,
        )

    def srcset(match):
        value = re.sub(
            r"(?<![^,\s])(?:" + re.escape(site.rstrip("/")) + r")?/images/",
            cdn.rstrip("/") + "/",
            match[2],
        )
        if path.startswith("img"):
            value = re.sub(
                r"(?<![^,\s])" + re.escape(public_path) + r"/",
                cdn.rstrip("/") + "/",
                value,
            )
        return match[1] + value + match[3]

    return re.sub(r"""(srcset=["'])(.*?)(["'])""", srcset, result, flags=re.DOTALL)


def cdn_artifacts(directory: Path, config: dict[str, str]) -> int:
    changed = 0
    # Search JSON and feeds embed images too; binary assets must remain byte-identical.
    for path in directory.rglob("*"):
        if (
            path.suffix.lower() not in {".html", ".xml", ".md", ".json"}
            or not path.is_file()
        ):
            continue
        source = path.read_text(encoding="utf-8")
        updated = rewrite_cdn(source, config["site_url"], config["cdn_url"])
        if updated != source:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def verify(
    urls: list[str],
    attempts: int = 4,
    interval: float = 15,
) -> bool:
    pending = dict.fromkeys(urls)
    for attempt in range(attempts):
        for url in list(pending):
            stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
            try:
                with urlopen(
                    Request(
                        url,
                        method="HEAD",
                        headers={"User-Agent": "Log4D publication check"},
                    ),
                    timeout=20,
                ) as response:
                    if response.status != 200:
                        raise ValueError(f"HTTP {response.status}")
                print(f"{stamp} OK {url}", flush=True)
                del pending[url]
            except (HTTPError, URLError, OSError, HTTPException, ValueError) as error:
                print(f"{stamp} 等待 {url}: {error}", flush=True)
        if not pending:
            return True
        if attempt + 1 < attempts:
            time.sleep(interval)
    return False

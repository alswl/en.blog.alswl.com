"""Image references and checks shared by local commands and CI."""

from __future__ import annotations

import fnmatch
import html
import re
import subprocess
import tempfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .runtime import imagemagick

RASTER = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
EXTENSIONS = RASTER | {".svg"}
MAX_SIZE = 1000
EXCLUDE_DIRS = (
    "upload_dropbox",
    "2009",
    "2010",
    "2011",
    "2012",
    "2014",
    "201502",
    "201503",
    "201504",
    "2022*",
    "2023*",
)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
IMAGE = re.compile(r"(?<!\\)!\[((?:\\.|[^\]\\])*)\]")
DEFINITION = re.compile(r"^ {0,3}\[([^\]]+)\]:\s*(.*)$", re.MULTILINE)
# Consume whole remote URLs so their /images/ tails cannot hide unused local files.
LOCAL_PATH = re.compile(
    r"(?:https?://[^\s\"'<>]+|(?:\.\./)*static/(?:images|img)/[^\s\"'<>\)\]]+|/(?:images|img)/[^\s\"'<>\)\]]+)"
)


@dataclass(frozen=True)
class Reference:
    url: str
    line: int


def prose(source: str) -> str:
    """Mask code without changing line numbers (also used for unused-image checks)."""
    result = []
    fence = ""
    for line in source.splitlines(keepends=True):
        match = FENCE.match(line.rstrip("\r\n"))
        if match:
            marker, suffix = match.groups()
            if not fence:
                fence = marker
            elif (
                marker[0] == fence[0]
                and len(marker) >= len(fence)
                and not suffix.strip()
            ):
                fence = ""
            result.append("\n" if line.endswith("\n") else "")
        elif fence:
            result.append("\n" if line.endswith("\n") else "")
        else:
            result.append(line)
    text = "".join(result)
    return re.sub(
        r"(`+)(?!`)(.+?)(?<!`)\1(?!`)",
        lambda m: "".join("\n" if c == "\n" else " " for c in m[0]),
        text,
        flags=re.DOTALL,
    )


def destination(text: str) -> str:
    text = text.lstrip()
    if text.startswith("<"):
        return text[1:].split(">", 1)[0]
    depth = 0
    result = []
    escaped = False
    for char in text:
        if escaped:
            result.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char.isspace() or (char == ")" and depth == 0):
            break
        else:
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            result.append(char)
    return html.unescape("".join(result))


def label(value: str) -> str:
    return " ".join(value.split()).casefold()


class HTMLImages(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs: list[Reference] = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "img" and values.get("src"):
            self.refs.append(Reference(values["src"], self.getpos()[0]))
        if tag in {"img", "source"} and values.get("srcset"):
            for entry in values["srcset"].split(","):
                if entry.strip():
                    self.refs.append(Reference(entry.split()[0], self.getpos()[0]))


def references(source: str) -> list[Reference]:
    text = prose(source)
    definitions = {label(m[1]): destination(m[2]) for m in DEFINITION.finditer(text)}
    refs: list[Reference] = []
    for match in IMAGE.finditer(text):
        tail = text[match.end() :]
        if tail.startswith("("):
            url = destination(tail[1:])
        elif tail.startswith("[") and "]" in tail:
            key = tail[1:].split("]", 1)[0] or match[1]
            url = definitions.get(label(key), "")
        else:
            url = definitions.get(label(match[1]), "")
        if url:
            refs.append(Reference(url, text.count("\n", 0, match.start()) + 1))
    parser = HTMLImages()
    parser.feed(text)
    refs.extend(parser.refs)
    if text.startswith("---\n"):
        frontmatter = text.split("\n---", 1)[0]
        for number, line in enumerate(frontmatter.splitlines(), 1):
            if match := re.match(r"\s*image:\s*['\"]?(https?://[^\s'\"]+)", line):
                refs.append(Reference(match[1], number))
    return refs


def local_path(url: str) -> str | None:
    url = html.unescape(url)
    # Explicit local paths only; a remote host with /images/ does not use our files.
    if url.startswith("../../static/images/") or url.startswith("../../static/img/"):
        url = url.removeprefix("../../static")
    elif url.startswith("static/images/") or url.startswith("static/img/"):
        url = url.removeprefix("static")
    if not (url.startswith("/images/") or url.startswith("/img/")):
        return None
    value = unquote(urlsplit(url).path).removeprefix("/images/").removeprefix("/img/")
    return value if Path(value).suffix.lower() in EXTENSIONS else None


def local_references(source: str) -> set[str]:
    refs = {p for ref in references(source) if (p := local_path(ref.url))}
    # Covers, image links, and !banner metadata are references too.
    for match in LOCAL_PATH.finditer(prose(source)):
        if path := local_path(match[0]):
            refs.add(path)
    # Historical copies use two date-directory layouts, not arbitrary basenames.
    for ref in tuple(refs):
        if match := re.fullmatch(r"upload_dropbox/(\d{4})(\d{2})/(.+)", ref):
            year, month, tail = match.groups()
            refs.update((f"{year}{month}/{tail}", f"{year}/{month}/{tail}"))
    return refs


def remote_images(root: Path, files: list[str]) -> list[str]:
    errors = []
    for name in files:
        path = root / name
        for ref in references(path.read_text(encoding="utf-8")):
            if urlsplit(ref.url).scheme.lower() in {"http", "https"}:
                errors.append(
                    f"{name}:{ref.line}: 远端图片 {ref.url}；请下载至 static/images/YYYYMM/。"
                )
    return errors


def unused_images(root: Path) -> list[str]:
    refs: set[str] = set()
    for path in (root / "content").rglob("*"):
        if path.suffix.lower() in {".md", ".html"} and path.is_file():
            refs.update(local_references(path.read_text(encoding="utf-8")))
    errors = []
    images = root / "static/images"
    image_roots = [images, root / "static/img"]
    for image_root in image_roots:
        for path in sorted(image_root.rglob("*")):
            if path.suffix.lower() not in EXTENSIONS or not path.is_file():
                continue
            relative = path.relative_to(image_root).as_posix()
            prefix = "static/images" if image_root == images else "static/img"
            if any(
                fnmatch.fnmatch(relative, p) or fnmatch.fnmatch(relative, f"{p}/*")
                for p in EXCLUDE_DIRS
            ):
                continue
            if image_root == images and relative not in refs:
                errors.append(f"{prefix}/{relative}: 未被文章引用。")
    return errors


def image_sizes(root: Path, files: list[str]) -> list[str]:
    if not files:
        return []
    identify, _ = imagemagick()
    errors = []
    for name in files:
        result = subprocess.run(
            [*identify, "-format", "%w %h\n", str(root / name)],
            capture_output=True,
            text=True,
            check=False,
        )
        try:
            frames = [
                tuple(map(int, line.split())) for line in result.stdout.splitlines()
            ]
            valid = (
                result.returncode == 0
                and frames
                and all(len(frame) == 2 for frame in frames)
            )
        except ValueError:
            valid = False
        if not valid:
            errors.append(f"{name}: 无法读取图片尺寸。{result.stderr.strip()}")
        elif any(max(frame) > MAX_SIZE for frame in frames):
            errors.append(
                f"{name}: 超过 {MAX_SIZE}×{MAX_SIZE}；运行 make resize-images。"
            )
    return errors


def resize(root: Path, files: list[str]) -> None:
    if not files:
        print("没有需要处理的图片。")
        return
    _, convert = imagemagick()
    for name in files:
        path = root / name
        # Write to a sibling file: a failed conversion must not corrupt the original.
        with tempfile.TemporaryDirectory(
            prefix=".blog-resize-", dir=path.parent
        ) as directory:
            target = Path(directory) / path.name
            subprocess.run(
                [
                    *convert,
                    str(path),
                    "-auto-orient",
                    "-strip",
                    "-resize",
                    f"{MAX_SIZE}x{MAX_SIZE}>",
                    str(target),
                ],
                check=True,
            )
            target.replace(path)


def copy_public(root: Path) -> None:
    """Create missing deploy copies under static/img without overwriting author edits."""
    source = root / "static/images"
    target_root = root / "static/img"
    if not source.is_dir():
        return
    _, convert = imagemagick()
    for path in sorted(source.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in RASTER:
            continue
        target = target_root / path.relative_to(source)
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                *convert,
                str(path),
                "-auto-orient",
                "-strip",
                "-resize",
                f"{MAX_SIZE}x{MAX_SIZE}>",
                str(target),
            ],
            check=True,
        )
        print(f"生成 {target.relative_to(root)}")

#!/usr/bin/env python3
"""
查找 static/images 目录下未被 content 引用的图片。
与参考站 blog.alswl.com 一致，英文站可自定义 EXCLUDE_DIRS。

用法:
    python3 hack/find-unused-images.py
"""
from __future__ import annotations

import fnmatch
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
IMAGES_DIR = ROOT_DIR / "static" / "images"
CONTENT_DIR = ROOT_DIR / "content"

EXCLUDE_DIRS: list[str] = []

IMAGE_EXTENSIONS = frozenset({".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"})
IMAGE_REF_PATTERN = re.compile(r"images/([^)]+)")


def _is_excluded(rel_path: str) -> bool:
    for pattern in EXCLUDE_DIRS:
        if not pattern:
            continue
        if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(rel_path, f"{pattern}/*"):
            return True
    return False


def _collect_content_refs() -> set[str]:
    refs: set[str] = set()
    if not CONTENT_DIR.exists():
        return refs
    for path in CONTENT_DIR.rglob("*"):
        if path.suffix not in (".md", ".html"):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in IMAGE_REF_PATTERN.findall(content):
            ref = match.split("?")[0].strip()
            if ref:
                refs.add(ref)
                refs.add(Path(ref).name)
    return refs


def _collect_images() -> list[str]:
    images: list[str] = []
    if not IMAGES_DIR.exists():
        return images
    for path in IMAGES_DIR.rglob("*"):
        if path.name == ".DS_Store":
            continue
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        rel = path.relative_to(IMAGES_DIR).as_posix()
        images.append(rel)
    return sorted(images)


def main() -> int:
    refs = _collect_content_refs()
    all_images = _collect_images()
    scanned = [p for p in all_images if not _is_excluded(p)]
    unused = [
        f"{IMAGES_DIR.relative_to(ROOT_DIR).as_posix()}/{p}"
        for p in scanned
        if p not in refs and Path(p).name not in refs
    ]
    print("扫描 static/images 目录...\n")
    print(f"=== 未被 content 引用的图片 ({len(unused)} / {len(scanned)}) ===\n")
    if unused:
        print("\n".join(sorted(unused)))
        return 1
    print("(无)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

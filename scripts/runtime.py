"""Locate installed tools; installation belongs to the package manager or CI."""

from __future__ import annotations

import os
import shutil
from pathlib import Path


class Tools:
    def __init__(self, root: Path):
        self.root = root

    def resolve(self, name: str) -> str:
        if name == "prettier":
            local = self.root / "node_modules/.bin/prettier"
            if local.is_file() and os.access(local, os.X_OK):
                return str(local)
        if binary := shutil.which(name):
            return binary
        raise ValueError(f"缺少 {name}；请按 docs/dev/README.md 安装依赖。")


def imagemagick() -> tuple[list[str], list[str]]:
    if binary := shutil.which("magick"):
        return [binary, "identify"], [binary]
    identify, convert = shutil.which("identify"), shutil.which("convert")
    if identify and convert:
        return [identify], [convert]
    raise ValueError(
        "缺少 ImageMagick：macOS 运行 brew install imagemagick，Ubuntu 安装 imagemagick。"
    )

"""Git file selection and read-only snapshots; filenames never pass through a shell."""

from __future__ import annotations

import shutil
import subprocess
import tarfile
import tempfile
from contextlib import contextmanager
from pathlib import Path

ZERO = "0" * 40


class Repository:
    def __init__(self, root: Path):
        self.root = root

    def git(self, *args: str, data: bytes | None = None) -> bytes:
        return subprocess.run(
            ["git", "-C", str(self.root), *args],
            input=data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout

    def exists(self, ref: str) -> bool:
        try:
            self.git("rev-parse", "--verify", f"{ref}^{{commit}}")
            return True
        except subprocess.CalledProcessError:
            return False

    def names(self, *args: str) -> set[str]:
        return {
            p.decode("utf-8", "surrogateescape")
            for p in self.git(*args).split(b"\0")
            if p
        }

    def files(
        self, scope: str = "worktree", base: str | None = None, head: str = "HEAD"
    ) -> list[str]:
        if scope == "all":
            names = self.names("ls-files", "-z") | self.names(
                "ls-files", "--others", "--exclude-standard", "-z"
            )
        elif scope == "staged":
            names = self.names(
                "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"
            )
        elif scope == "worktree":
            names = self.names("ls-files", "--others", "--exclude-standard", "-z")
            if self.exists("HEAD"):
                names |= self.names(
                    "diff", "HEAD", "--name-only", "--diff-filter=ACMR", "-z"
                )
            else:
                names |= self.names("ls-files", "-z")
        elif scope == "push":
            if base == ZERO and self.exists("origin/master"):
                base = self.git("merge-base", "origin/master", head).decode().strip()
            if base == ZERO:
                names = self.names("ls-tree", "-r", "--name-only", "-z", head)
            else:
                if not base:
                    if not self.exists("origin/master"):
                        raise ValueError(
                            "没有 origin/master；请传 --base <commit> 或先 git fetch origin。"
                        )
                    base = (
                        self.git("merge-base", "origin/master", head).decode().strip()
                    )
                if not self.exists(base):
                    raise ValueError(
                        f"找不到基线 {base}；请先 git fetch 或传入有效的 --base。"
                    )
                # A push compares the actual remote and local tips, including force pushes.
                names = self.names(
                    "diff", base, head, "--name-only", "--diff-filter=ACMR", "-z"
                )
            return sorted(names)
        else:
            raise ValueError(f"未知范围: {scope}")
        # The index can contain files already deleted from the working tree.
        if scope == "staged":
            return sorted(names)
        return sorted(
            n
            for n in names
            if (self.root / n).is_file() and not (self.root / n).is_symlink()
        )

    @contextmanager
    def snapshot(self, ref: str | None = None, paths: list[str] | None = None):
        """Export only the files needed for checks; never stash or touch the worktree."""
        with tempfile.TemporaryDirectory(prefix="blog-check-") as directory:
            # macOS aliases /var to /private/var; containment checks need one spelling.
            root = Path(directory).resolve()
            if ref is None:
                selected = (
                    sorted(set(paths))
                    if paths is not None
                    else sorted(self.names("ls-files", "-z"))
                )
                data = b"".join(
                    p.encode("utf-8", "surrogateescape") + b"\0" for p in selected
                )
                self.git(
                    "checkout-index", f"--prefix={root}/", "--stdin", "-z", data=data
                )
            else:
                command = ["git", "-C", str(self.root), "archive", ref]
                with subprocess.Popen(command, stdout=subprocess.PIPE) as process:
                    with tarfile.open(fileobj=process.stdout, mode="r|") as archive:
                        for member in archive:
                            target = root / member.name
                            if (
                                not member.isfile()
                                or not target.resolve().is_relative_to(root)
                            ):
                                continue
                            target.parent.mkdir(parents=True, exist_ok=True)
                            with (
                                archive.extractfile(member) as source,
                                target.open("wb") as destination,
                            ):
                                shutil.copyfileobj(source, destination)
                    if process.wait():
                        raise ValueError(f"无法读取提交快照: {ref}")
            yield root

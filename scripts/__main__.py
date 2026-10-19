import sys

if sys.version_info < (3, 10):
    raise SystemExit("Log4D 写作工具需要 Python 3.10 或更新版本。")

from .cli import main

raise SystemExit(main())

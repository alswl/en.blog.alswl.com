# en.blog.alswl.com

- https://en.blog.alswl.com/
- https://blog.alswl.com/
- https://www.zhihu.com/column/alswl
- https://www.jianshu.com/u/90d9cec0f932

This is my blog (English).

## Build & preview

Run `make help` for the available author and maintenance commands. Initialize the theme with `make init-theme`, inspect local dependencies with `make check-tools`, preview drafts with `make preview-site`, and build into `public/` with `make build-site`. For a deployment build that preserves the established `/images/` → `/img/` rewrite, run `make build-production cdn`.

Daily content checks cover changed Markdown and images, plus all unused images. Run `make format-markdown`, `make resize-images`, and `make check-content` before committing. The Python tools use only the standard library; install Hugo, Python 3.10+, Node.js/npm, and ImageMagick with your system package manager. Prettier is needed for formatting and checks.

The build deploys this English site through GitHub Pages. The English site keeps its own image setup: source files in `static/images/`, deployment copies in `static/img/`, and published image URLs under `/img/`. It does not use the Chinese site’s object storage settings. See [docs/dev/README.md](docs/dev/README.md) for toolchain details.

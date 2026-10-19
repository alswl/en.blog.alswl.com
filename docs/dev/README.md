# Site maintenance

Use `make help` as the command index. The Python implementation lives in `scripts/`; regression tests live in `tests/`.

## Setup and daily work

Install Git, Python 3.10 or later, Hugo, Node.js/npm, and ImageMagick using your system package manager. Install Prettier locally with `npm install --no-save --package-lock=false --ignore-scripts --no-audit --no-fund prettier@latest`, then run:

```sh
make init-theme
make check-tools
```

The theme is a Git submodule. Local Hugo and Prettier versions may differ from CI; `make check-tools` reports the selected binaries and versions.

For authoring, use `make new-post name=YYYY-MM-DD-slug.md`, `make preview-site`, and `make fetch-banner-metadata post=content/posts/...`. Before committing, run `make format-markdown`, `make resize-images`, and `make check-content`. These commands operate on changed files and do not stage modifications. The unused image check scans all of `static/images/`.

`make build-site` builds into a temporary directory and replaces `public/` only after Hugo succeeds. The deployment command `make build-production cdn` first creates missing `static/img/` copies from `static/images/`, then rewrites `/images/` references to `https://en.blog.alswl.com/img/` before replacing `public/`. `make clean-build` removes build output and cache. Do not commit `public/`.

## Checks and hooks

`make install-git-hooks` installs optional lefthook checks. The pre-commit hook reads the staged snapshot; pre-push checks commits being pushed. Both use the same Python check implementation as CI. Formatting and resizing are explicit actions, not automatic hook changes.

Useful explicit scopes:

```sh
python3 -B -m scripts check-content --changed-only
python3 -B -m scripts check-content --scope all
python3 -B -m scripts check-content --scope staged
python3 -B -m scripts check-content --scope push --base <commit>
```

## CI and publication

The existing GitHub Pages workflow builds `public/` and deploys it on `master`. CI installs Hugo and Node, runs the regression suite and content checks, then builds and deploys. This English site serves images from `https://en.blog.alswl.com/images`; it does not use the Chinese site's object storage or S3 credentials.

After a deployment, `make warm-cdn-images base=<previous-commit>` issues GET requests for changed images. `make verify-publication base=<previous-commit>` retries checks for changed published pages and images and records UTC observation times. With no changes it checks the homepage. These commands are safe to run manually; they need network access.

`make test-toolchain` runs offline tests. The modules are organized by responsibility: `cli.py` dispatches commands, `git.py` computes changed file sets and snapshots, `runtime.py` locates installed dependencies, `images.py` checks and resizes images, `banners.py` fetches explicit link card metadata, and `publishing.py` rewrites build URLs and verifies deployed URLs.

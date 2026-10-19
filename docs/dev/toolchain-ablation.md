# Toolchain change notes

On 2026-10-19, the English site adopted the shared authoring and image-checking tools from `blog.alswl.com`. The Python implementation provides a single command surface, Git-aware changed-file scopes, staged and push snapshots, image reference and size checks, safe resizing, Markdown formatting, banner metadata fetching, and publication URL verification.

Site-specific behavior remains in this repository: GitHub Pages deploys `public/`; source images live under `static/images/`; resized deployment copies live under `static/img/`; `make build-production cdn` rewrites `/images/` links to `https://en.blog.alswl.com/img/`. The source site's S3 endpoint, bucket, and credentials are not used.

The reference site also changed its Mermaid render hook to pin Mermaid 11.17.2. The English site uses the same pinned client in its existing footer hook. Hugo theme and content are unchanged.

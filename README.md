# en.blog.alswl.com

- https://en.blog.alswl.com/
- https://blog.alswl.com/
- https://www.zhihu.com/column/alswl
- https://www.jianshu.com/u/90d9cec0f932

This is my blog (English).

## Build & preview

- **Hugo**: Use the same version as CI (see [quickstart](specs/001-sync-blog-framework/quickstart.md)), currently **0.148.2**.
- **Theme**: Run `git submodule update --init --recursive` after clone.
- **Local preview**: `hugo serve -D`
- **Production build**: `make build-production` (output in `public/`). This site does **not** use CDN; images use original links.

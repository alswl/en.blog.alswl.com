---
name: publish
description: 发布 en.blog.alswl.com 文章的完整流程：图片双目录拷贝、本地构建校验、push master 触发 GitHub Pages 部署、线上 200 验证。在用户要求发布文章、publish、push master 上线、或排查线上图片 404 时使用。
---

# 发布流程

本仓库是 en.blog.alswl.com（Hugo + hugo-PaperMod），push master 即触发部署：
`.github/workflows/gh-pages.yml` 跑 `make build-production cdn` 后发布到 gh-pages。

## 关键机制（先读懂再动手）

- **图片两个目录，分工不同，靠 make target 同步**：
  - `static/images/YYYYMM/` — 原图，文章里引用的路径（`/images/YYYYMM/x.png`），Typora 引用它；
  - `static/img/YYYYMM/` — 部署副本，由 `make resize-images-to-public` 从原图生成（拷贝 + ImageMagick `mogrify -strip -auto-orient -resize 1000x1000`），`/img/` CDN 重写最终服务的就是它；
  - 提交前可用 `make resize-images-in-git-workdir` 压缩本次改动的原图。
  - 原因：`make cdn` 会把构建产物里所有 `src="/images/` 重写成 `https://en.blog.alswl.com/img/`（见 Makefile `CDN_HOST`）。GitHub Pages 按部署目录找文件，`static/img/` 下没有对应文件就是 404。
  - **不要手工 cp**：手工拷贝会跳过缩放，且脚本对已存在文件会 skip，之后跑 target 也不会修正——先删掉手工拷贝再跑 target。
  - 小于 1000px 的图不会被放大（脚本用 `resize '1000x1000>'`，2026-10-06 修复过一次不带 `>` 导致小图被放大的问题，如 ai-native-information-to-insight.png 保持 640x710 原样）。
- **`CDN_HOST := https://en.blog.alswl.com/img` 是既定参数，不要改**（2026-10-06 线上图片 404 时曾试图改它，结论：改参数不对，正确做法是图片放两份；已按用户要求还原）。
- gh-pages 的 `img/` 目录来自 `static/img/`，自 70e32ba 的部署（2026-02-23）起存在；`/img/*` 由 GitHub Pages 直接服务（无 Cloudflare 代理）。老文章图片能 200 是因为 `static/img/` 里有历史副本（只到 202602）；新文章图片不自动跟进，必须自己拷贝。
- 文章内图片引用保留源站的绝对路径 `/images/YYYYMM/...`（表格内的图片链接用相对路径会挂）。

## 发布步骤

### 1. 准备

- `git status` 干净；文章在 `content/posts/YYYY-MM-DD-slug.md`；frontmatter 的 `slug` / `date` 与源站保持一致（中文站同步场景见 translate skill）。
- 图片拷贝（YYYYMM 为发文年月）：

```bash
make resize-images-to-public   # static/images/ -> static/img/，mogrify 缩放到 1000x1000
```

### 2. 本地构建 + 校验（不过就别 push）

```bash
rm -rf public && make build-production cdn

# 校验脚本：检查页面存在、所有图片/资源 URL 落到 public/ 真实文件、
# 内部链接都有对应页面（把页面路径换成实际的，可传多个）
bash hack/verify-publish.sh \
  public/2026/10/<slug>/index.html \
  public/2026/09/<slug>/index.html
# 输出 VERIFY: OK 才继续；MISSING asset = static/img/ 双目录没拷对；
# MISSING link = 文内内部链接目标不存在
```

脚本细节：

- 重写后页面里 `src` 是 `https://en.blog.alswl.com/img/...`，脚本会落到 `public/img/...` 校验，正好覆盖双目录是否拷对。
- 已知缺失的资源默认跳过（`VERIFY_SKIP`，默认 `safari-pinned-tab.svg apple-touch-icon.png`，两者是 PaperMod 默认引用、中文站也没有）；新发现的可疑缺失先用 curl 对比中文站再决定补文件还是加 skip。
- 脚本自带评测：`bash .agents/skills/publish/evals/run-evals.sh`，用临时 fixture 断言通过/失败行为（缺资源、缺链接、缺页面、外链不误报），改动脚本后跑一下。

### 3. 提交并推送

```bash
git add content/posts/... static/images/... static/img/...
git commit -m "pub: ..." && git push origin master
```

- lefthook pre-commit 会跑 prettier 重排 markdown（表格对齐、引号统一），提交后磁盘文件可能变化，属正常。
- push 时 pre-push 钩子再跑一次格式检查。
- push 后 CI（Build workflow）还会跑 `hack/find-unused-images.py`（无未引用图片）和一次完整构建；lint/格式没有独立工具，prettier 即全部。

### 4. 部署验证（不要跳过）

```bash
gh run list --repo alswl/en.blog.alswl.com --limit 3
gh run watch <run-id> --repo alswl/en.blog.alswl.com --exit-status
```

部署成功后线上验证：

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://en.blog.alswl.com/2026/10/<slug>/        # 期望 200
curl -s -o /dev/null -w "%{http_code}\n" https://en.blog.alswl.com/img/YYYYMM/<某张图>.png  # 期望 200，404 = 图片没拷到 static/img/
```

## 踩坑记录

- **2026-10-06 线上图片 404**：新文章图片只拷了 `static/images/`，`make cdn` 把 URL 重写到 `/img/` 后全部 404（旧图 200 是因为 gh-pages 有 202602 之前的遗留 `img/` 目录，极具迷惑性）。修复：补拷 `static/img/`（commit 1e67be9）。教训：本地 `hugo` 不带 `cdn` target 看到的路径和线上不一致，验证一律用 `make build-production cdn`。
- `make build-production`（不带 cdn）的产物图片路径还是 `/images/`，和线上不一样，别拿它做发布前校验。
- 修复图片 404 并重新部署后，Fastly 边缘可能还缓存着旧的 404 响应（约 10 分钟过期），线上验证遇到「本地 public/ 里明明有文件但 curl 404」时先等几分钟再试。
- 中文站 blog.alswl.com 的 CDN 是七牛（`CDN_HOST = https://e25ba8-log4d-c.dijingchao.com`），机制不同，别照搬。
- **favicon 类资产**：主题按约定路径引用站点根的 `favicon-16x16.png` / `favicon-32x32.png`，英文站一直缺失（线上 404），2026-10-06 从中文站补入 `content/`；`apple-touch-icon.png` 与 `safari-pinned-tab.svg` 两个站点都没有，verify 脚本默认 skip。

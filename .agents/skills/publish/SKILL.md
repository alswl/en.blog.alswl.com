---
name: publish
description: 发布 en.blog.alswl.com 文章的完整流程：图片双目录拷贝、本地构建校验、push master 触发 GitHub Pages 部署、线上 200 验证。在用户要求发布文章、publish、push master 上线、或排查线上图片 404 时使用。
---

# 发布流程

本仓库是 en.blog.alswl.com（Hugo + hugo-PaperMod），push master 即触发部署：
`.github/workflows/gh-pages.yml` 跑 `make build-production cdn` 后发布到 gh-pages。

## 关键机制（先读懂再动手）

- **图片必须放两份**：
  - `static/images/YYYYMM/` — 源文件目录，文章里引用的路径（`/images/YYYYMM/x.png`）；
  - `static/img/YYYYMM/` — 部署副本，**同名同路径**再拷一份。
  - 原因：`make cdn` 会把构建产物里所有 `src="/images/` 重写成 `https://en.blog.alswl.com/img/`（见 Makefile `CDN_HOST`）。GitHub Pages 按部署目录找文件，`static/img/` 下没有对应文件就是 404。
- **`CDN_HOST := https://en.blog.alswl.com/img` 是既定参数，不要改**（2026-10-06 线上图片 404 时曾试图改它，结论：改参数不对，正确做法是图片放两份；已按用户要求还原）。
- gh-pages 的 `img/` 目录来自 `static/img/`，自 70e32ba 的部署（2026-02-23）起存在；`/img/*` 由 GitHub Pages 直接服务（无 Cloudflare 代理）。老文章图片能 200 是因为 `static/img/` 里有历史副本（只到 202602）；新文章图片不自动跟进，必须自己拷贝。
- 文章内图片引用保留源站的绝对路径 `/images/YYYYMM/...`（表格内的图片链接用相对路径会挂）。

## 发布步骤

### 1. 准备

- `git status` 干净；文章在 `content/posts/YYYY-MM-DD-slug.md`；frontmatter 的 `slug` / `date` 与源站保持一致（中文站同步场景见 translate skill）。
- 图片拷贝（YYYYMM 为发文年月）：

```bash
mkdir -p static/img/YYYYMM
cp static/images/YYYYMM/*.png static/img/YYYYMM/   # 按实际扩展名调整
```

### 2. 本地构建 + 校验（不过就别 push）

```bash
rm -rf public && make build-production cdn
```

逐条校验构建产物（把文章路径换成实际的）：

```bash
# 页面生成了吗
ls public/2026/10/<slug>/index.html

# 每个图片 URL 都能在 public/ 下找到真实文件
for u in $(grep -ohE '(src|href)="[^"]*/2[0-9]{4}/[^"]*\.(png|jpg|jpeg|gif|webp)"' \
    public/2026/10/<slug>/index.html | sed -E 's/(src|href)="//;s/"//' | sort -u); do
  p="${u#https://en.blog.alswl.com}"
  [ -f "public$p" ] || echo "MISSING: $u"
done

# 文内内部链接都有对应页面
for p in /2026/02/my-2025/ ...; do [ -f "public${p}index.html" ] || echo "MISSING LINK: $p"; done
```

注意：重写后 `src` 是 `https://en.blog.alswl.com/img/...`，上面的循环会落到 `public/img/...` 校验，正好覆盖双目录是否拷对。

### 3. 提交并推送

```bash
git add content/posts/... static/images/... static/img/...
git commit -m "pub: ..." && git push origin master
```

- lefthook pre-commit 会跑 prettier 重排 markdown（表格对齐、引号统一），提交后磁盘文件可能变化，属正常。
- push 时 pre-push 钩子再跑一次格式检查。

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

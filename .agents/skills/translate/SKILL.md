---
name: translate-blog-to-en
description: 将相同 Hugo 结构的博客文章翻译成英文并写入本仓库，保持路径一致并复制文内引用的图片与附件。在用户要求把博客内容翻译成英文、从中文/源站同步文章或向目标站添加译文时使用。
---

# 博客翻译为英文

将相同结构的 Hugo 博客内容翻译成英文，按相同路径写入本仓库，并复制所有引用的图片与附件。

## 适用范围

- **来源**：相同版式的 Hugo 博客（如 `content/posts/YYYY-MM-DD-slug.md`、frontmatter、`static/images/...`）。
- **目标**：本仓库。文章保持相同相对路径；资源放在 `static/` 下且结构一致。

## 工作流程

### 1. 确定源内容位置

- 用户可能提供：源仓库/目录路径，或直接粘贴整篇文章。
- 若提供路径：源根目录 = 该仓库/目录（内含 `content/`、`static/`）。
- 确定要处理的文章文件（如 `content/posts/YYYY-MM-DD-slug.md`）。

### 2. 提取并翻译

- **Frontmatter**：将 `title` 译为英文。保留 `slug`、`date`、`categories`、`tags`、`draft`、`typora-copy-images-to`；若 `typora-copy-images-to` 指向其他仓库，改为相对文章的路径 `../../static/images/YYYYMM`。
- **正文**：将所有正文译为英文。并保持：
  - Markdown 结构（标题、列表、表格、引用块、代码块、链接）。
  - 图片语法 `![alt](path)`：只翻译 `alt` 文案，本步骤不修改路径。
  - 行内 HTML（如 `<center>`、`<mark>`、`<small>`）。
- 不翻译：代码块、URL、链接目标、图片路径、frontmatter 中的 `slug`（除非用户明确要求）。

### 3. 将译文写入本仓库

- **路径**：与源站相同路径，相对于本仓库根目录。
  - 示例：源站 `content/posts/YYYY-MM-DD-slug.md` → 本仓库 `content/posts/YYYY-MM-DD-slug.md`。
- 若父目录不存在则创建。若为预期目标文件则覆盖已有文件。

### 4. 复制图片与附件

- **从译文中找出引用**：
  - Markdown 图片：`![...](path)`，path 形如 `../../static/images/YYYYMM/...` 或 `/static/images/...`。
  - 其他静态资源（如 `static/` 下的 PDF）若有也一并处理。
- **在本仓库中的路径**：图片放在 `static/images/YYYYMM/`；从 `content/posts/*.md` 引用时为 `../../static/images/YYYYMM/文件名.扩展名`。
- **复制**每个被引用的文件：
  - 从：`{源根目录}/static/images/YYYYMM/{文件名}`（或引用所对应的路径）。
  - 到：`{本仓库}/static/images/YYYYMM/{文件名}`。
- 若本仓库没有 `static/images/YYYYMM/` 则创建。按二进制/原样复制，不翻译文件名。
- 若源站使用不同路径（如 `static/images/upload_dropbox/202006/`），在本仓库的 `static/` 下镜像相同结构，以保证现有引用仍有效。

### 5. 核对

- 新文章中的图片/附件引用均指向本仓库内路径（如 `../../static/images/...`）。
- 每个被引用文件在本仓库的 `static/` 下均存在。
- Frontmatter 为合法 YAML；除非用户另有要求，否则不修改 `date` 与 `slug`。

## 本仓库约定

- 文章文件名：`content/posts/YYYY-MM-DD-slug.md`。
- 图片：`static/images/YYYYMM/` 或 `static/images/upload_dropbox/YYYYMM/`；在文章中以 `../../static/images/...` 引用。
- Frontmatter：`title`、`slug`、`date`、`categories`、`tags`；可选 `typora-copy-images-to`、`draft`。

## 示例

**用户**：“把某源仓库里的一篇文章翻译成英文放到本仓库。”

→ 以用户提供的源根目录为准。翻译该文件，写入本仓库的相同相对路径（如 `content/posts/YYYY-MM-DD-slug.md`）。找出文中所有 `![...](../../static/images/...)`（或类似）引用，将对应文件从源根目录下 `static/images/...` 按相同子路径复制到本仓库的 `static/images/...`。

**用户**：“把这篇博客翻译成英文放到本站，保持路径，图片也拷过来。”并粘贴了内容。

→ 按同一流程：翻译、按相同路径写入本仓库、将文中引用的每张图片从用户提供的源位置复制到本仓库的 `static/`（若仅粘贴内容则询问源根目录）。

## 实践之后的经验

- **仅提供 slug 时**：用户可能只说「把某篇翻译到本仓库」或「@源仓库 里面某 slug 翻译到本仓库」。先在源仓库用 glob 搜索 `**/*{slug}*` 或 grep 搜索 slug，确定文章路径（通常为 `content/posts/YYYY-MM-DD-slug.md`），源根目录为该项目根目录（如相对路径表示当前 workspace 的兄弟目录等）。
- **一次性找出所有图片**：用 grep 搜 `!\[.*\]\(|\.\./.*static/|/static/` 或读全文扫描 `../../static/images/YYYYMM/`，列出所有需复制的文件；图片可能为 `.png`、`.jpg` 等，复制时需包含所有出现的扩展名。
- **目标目录不存在时**：本仓库可能还没有 `static/images/YYYYMM/`，复制前先 `mkdir -p 本仓库/static/images/YYYYMM`，再用 `cp` 将源目录下对应文件按原名复制过去（二进制原样复制，不改文件名）。
- **译文质量**：翻译时若发现原文明显笔误（如 "generted" → "generated"，"unkown" → "unknown"），可在译文中直接修正，不保留错误拼写。
- **外链与专有名词**：原文中的第三方站点链接保留原 URL；书名、产品名等可译，作者名不译。代码、仓库名、工具名保持不译。

## 检查清单

- [ ] 已确定源文章路径及（若有）源根目录。
- [ ] 标题与正文已翻译，结构、链接、代码、路径已保留。
- [ ] 译文已按相同路径写入本仓库。
- [ ] 所有图片/附件引用已列出并复制到本仓库 `static/` 下相同结构。
- [ ] 新文件中无失效的图片链接。

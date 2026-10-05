---
name: blog-writing
description: Write blog posts in the established style of en.blog.alswl.com: English, first person, practical and opinionated, with frontmatter and formatting conventions. Use when the user asks to write a new post, draft a blog article, write a year-in-review, write technical notes, or edit an existing post.
---

# Blog Writing Guide

Writing style and formatting conventions summarized from the existing posts on this site, used to keep tone, structure, and layout consistent.

## Scope and Principles

- **When to use**: when writing or editing new posts, year-in-reviews, technical or reading notes under `content/posts/`.
- **Principles**: English first, first person (I), sincere and opinionated; technical posts are concise and practical; life/reading posts may carry a moderate literary touch; no padding, no hand-waving.

## Frontmatter

Every post must start with YAML frontmatter, with these fields:

```yaml
---
title: "Post Title"
slug: "url-slug"
date: 2025-02-04T12:00:00+08:00
categories: ["coding"]
tags: ["tag1", "tag2"]
typora-copy-images-to: ../../static/images/202502
---
```

- **Required**: `title`, `slug`, `date`, `categories`, `tags`, `typora-copy-images-to`
- **slug**: lowercase hyphenated English, matching the URL, e.g. `architecture-design-the-easy-way`
- **typora-copy-images-to**: by year-month `../../static/images/YYYYMM`, matching the image paths in the body
- **Optional**: `draft: true`, `author: "alswl"`

## Body Structure

### Technical / Methodology Posts

- **Opening**: state the point directly, or open with a sharp one-liner/quote, optionally with an image; when needed, state scope and disclaimers in the first paragraph ("this post only covers…", "it does not cover…").
- **Overview**: use an "Overview" section to briefly state the problem and the shape of the solution (bold the core terms).
- **Body**: use `## ` for major sections and `### ` for subsections; conclusion first, then expansion; make good use of lists and tables.
- **Closing**: wrap up with a "Summary" or "Closing Notes" section; a "Further Reading" list may follow with links and a one-line note each.

### Year-in-Review Posts

- Section by area: `## Life - short subtitle`, `## Work - subtitle`, `## Hobbies`, `## Reading`, etc.
- Each block may carry images, with `<small>caption</small>` under the image.
- For books, list title + link + one or two lines of reflection; a cover image is fine.
- Close with "Last" or "Flag", linking to previous year-in-reviews.

### Reading Notes / Reflections

- Open with a blockquote quote, then move into a personal angle ("At first…", "These days…").
- Use `### ` subheadings to extract dimensions (e.g. "Curiosity as the driving force", "Resilience in adversity"), each paragraph carrying a clear point of view.
- The ending may return to a "north star" or "takeaway" — restrained, not vague.

### Tutorials / Short Posts

- Simple structure: why → preparation → process → summary; or just straight steps.
- The process may use `<center><mark><b>Key step</b></mark></center>` plus images; list tools/materials as bullets.

## Language and Tone

- **Person**: primarily "I", expressing personal judgment and experience ("I think", "I recommend", "in my experience").
- **Stance**: hold clear opinions; it is fine to position things as "practical" or "the Easy Way"; technical posts cut the filler and lead with conclusions.
- **Terminology**: English prose; product and project names stay as-is (REST, GitOps, MVP, OKR).
- **Colloquial**: occasional colloquialisms are fine, but stay restrained and never break readability.

## Formatting Conventions

- **Emphasis**: key concepts in **bold**; a sentence that must stand out gets `<mark>...</mark>`.
- **Images**:
  - Path: `![alt](../../static/images/YYYYMM/xxx.png)` (or `/images/YYYYMM/...` when absolute paths are required, e.g. images inside tables), matching `typora-copy-images-to`.
  - Caption: `<small>caption or source</small>` immediately under the image.
- **Quotes**: opening quotes or others' viewpoints use `> blockquote`.
- **Links**: `[text](url)`; external links may note the source, e.g. "(GitHub)", "(X)".
- **Lists/tables**: use lists or tables for multi-option, comparison, and checklist content; keep hierarchy clear.

## Closing Habits

- Technical/methodology posts: end with a "Summary" section, optionally a "Further Reading" list (title/link + one line).
- Year-in-reviews: close with "Last" or "Flag" plus links to previous years.
- Tutorials/short posts: a one-line summary or a simple call-to-action close.

## Example Fragments

**Technical post opening:**

```markdown
Whenever you join a new system, team, or project, you face a simple yet deep question: does this system have API design guidelines?
This question bothered me for a long time. So I wanted to write down a set of **simple and practical** Web API best practices — this post.
```

**Year-in-review section:**

```markdown
## Work - Infrastructure Builder

Last year I went from being an explorer to someone who drives system evolution in an organized way. ... Pain always makes one think ...
```

**Images and captions:**

```markdown
![arch-easy](../../static/images/202307/arch-easy.png)
<small>image via [Pixabay](https://...)</small>
```

Posts written to this spec stay consistent with the site's existing style and can be dropped straight into `content/posts/`.

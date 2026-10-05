---
title: "Working in the AI Native Era: From Information to Delivery"
author: "alswl"
slug: "ai-native-work"
date: 2026-10-06T00:00:00+08:00
draft: false
categories: ["coding"]
tags: ["AI", "AI Coding", "Knowledge Management", "Toolchain"]
---

In my [2025 year in review](/2026/02/my-2025/) I wrote: code typing will become an inefficient way to do engineering, and AI Native should be the default.

Saying it was easy. Once I actually had to work this way every day, the questions got concrete: AI writes code fast — but where does information come from? Who decides on the design? How is the output verified? What is a human still in charge of? After running this way for a year, my understanding has gone through several rounds of change; my focus slowly shifted from "writing code fast" to the whole chain of information, development, delivery, and toolchain.

<!-- more -->

This post describes how I currently work (as of the end of August): how I process information, how I write code, how I put the toolchain together, and the judgments I've formed after running this way for the better part of a year.

My background is Infra, Kubernetes, and PaaS; my main language lately is Go. Everything below comes from my own practice, not a survey of methodologies. This is not an operations manual for any particular product or team process, and I'm not going to argue that AI can replace the humans who make decisions.

## AI Native × Work

How my understanding evolved:

- February: **Code Typing is unnecessary** — the thrill of writing code fast, typing away until 2 a.m. every day
- May: AI amplifies execution; humans own judgment — from 2–3 agents in parallel to 7–8 agents in parallel
- August: information, development, delivery, toolchain

### What exactly is our work, in form and in substance?

> Problem analysis → Solution design → Product building → Launch & operations → Feedback reinforcement

The core carrier: **the artifact**.

Why is "translation-style" work the easiest to replace? Because an artifact is more static, more structured, and occupies a smaller semantic space. The complexity of software engineering is what makes this chain relatively long.

Documents, code, meetings, reports — these are just different forms of work.

The work itself:

1. Organizing, structuring, refining, and developing information; shaping proposals that others can understand and accept.
2. Turning proposals into products: writing code, verifying, shipping, running.
3. The hidden line: improving the toolchain to raise efficiency.

**Summary**: the forms — documents, code, meetings, reports — will change; the work itself is still these three lines. The rest of this post, on information, AI coding, and toolchain, basically follows these three lines.

## What Does AI Native Add?

We keep talking about AI Native. What is it, really?

My understanding: putting the reasoning power of AIGC into every aspect of work.

- Decision-making
- Content production
- Artifact production
- And the environment and platform that support this way of working

Not a point tool. A way of working.

![Under AI Native, work is a loop](/images/202610/ai-native-overview.png)

Real-world information and task goals enter the AI workspace; after analysis, generation, and checking, they hand over to a human for judgment on priority, boundaries, trade-offs, and responsibility; then shippable, acceptable artifacts come out. Artifacts generate feedback and new goals, and the loop returns to the start.

**Summary**: AI has entered every step of analysis, generation, and checking, so the loop spins faster. But the human judgment in the middle hasn't been removed — precisely because the loop spins faster, it binds tighter. This is exactly the May insight: <mark>AI amplifies execution; humans own judgment.</mark>

## How I Process Information Today

### From Information to Insight

![Data → Information → Knowledge → Insight → Wisdom](/images/202610/ai-native-information-to-insight.png)

<small>Image via the web</small>

Data has no value on its own; connected, it becomes knowledge; connected correctly, it becomes insight. The goal of information processing is not to store material away, but to keep it workable — ready for further processing.

### My Workflow

![My personal knowledge repository workflow](/images/202610/ai-native-information-workflow.png)

Every day I open 10+ PRs against my own knowledge repositories.

Local writing, meetings, all kinds of documents, IM messages — everything flows into the agent. The agent opens a worktree, edits files, commits, pushes a branch, opens a PR. I do exactly one thing: read the diff and decide whether to merge.

I keep two knowledge repositories locally, one new and one old, with two different ways of working:

| Repository | Purpose                                          | AI involvement |
| ---------- | ------------------------------------------------ | -------------- |
| `minds`    | AI collaboration, articles and project material  | 90%+           |
| `my-kms`   | Traditional personal knowledge base, daily notes | 5%             |

### The `minds` Repository

`minds` manages the information produced through AI collaboration: the material is messy and needs repeated processing. Most of my recent posts were finished here. I manage this repository with mind-forge, which I wrote myself.

[GitHub - alswl/mind-forge: Forge minds into articles.](https://github.com/alswl/mind-forge)

![Repository → Project → Docs / Sources / Image assets](/images/202610/ai-native-minds-layout.png)

One repository holds several projects, and each project has four zones:

- `sources/` — the input zone, read-only; raw material is never modified once it lands
- `docs/` — the article zone; long posts are split into section fragments named `NN-title.md`, each iterable on its own
- `outputs/` — build artifacts generated by `mf build`, never hand-edited
- `prompts/` and `thinking/` record goals, constraints, and reasoning

The point of this structure: material, work-in-progress, and published output stay separated. Agents can touch `docs/` without polluting `sources/`; when I review, I read the diff of `docs/`.

At the repository root there are a few more things: a `CLAUDE.md` stating collaboration principles and red lines, a glossary that standardizes proper nouns and dictation corrections, and a set of skills that take over repetitive actions. Conventions live in the repository, not in conversations we re-explain every time.

The repository root also uses `minds.yaml` to register projects; shared information is managed through the glossary and cross-project thinking, while articles, sources, and configuration are maintained inside each project.

![minds repository structure overview (redrawn)](/images/202610/ai-native-minds-overview-v2.png)

### The `my-kms` Knowledge Base

`my-kms` is the personal knowledge base I've kept for years. The product has changed several generations (back in 2010 I wrote [My Knowledge Management System](https://blog.alswl.com/2010/09/my-kms/)); later it settled on Obsidian (task management moved in with it, see [From Toodledo to Obsidian Tasks](/2023/02/gtd/)). Content is still entered mostly by hand — at minimum dictated by me. Only a small number of meeting summaries are handed to AI for entry.

My daily information flow:

> Meeting transcripts → summaries → daily notes → daily report → proposals, posts, and talks

Every meeting produces a transcript and a summary; every day closes into a daily report. Material doesn't stay in chat windows — it lands in a repository where it can be revisited, searched, and processed further.

Both repositories are hosted on a self-hosted Forgejo running on my own machine. The benefit is concrete: private data never leaves the machine, yet I still get branches, PRs, diffs, and history — meaning every change an agent makes is reviewable and revertible.

![my-kms repository structure (redrawn)](/images/202610/ai-native-kms-overview-v2.png)

### How I Keep the Human Touch

| Aspect    | My approach                                                   |
| --------- | ------------------------------------------------------------- |
| Framework | I conceive it myself; I keep control of the structure         |
| Long-form | Voice first; AI transcribes, organizes, polishes, structures  |
| Opinions  | From my own inputs — not a piece of generated text            |
| Diagrams  | I draw them myself whenever possible; screenshots as fallback |

Both quality and efficiency improve. More importantly, my own viewpoints survive in the content.

Here's a conversation with a colleague from operations about my writing output:

> "I can't see any trace of AI in it at all."
>
> "It's all AI-generated."
>
> "Wait, you hand-craft it?"
> "Whoa — man, could you share how?"
> "How can AI write something this alive and this professional?"
> "Forever in your debt."
>
> "I write the framework, AI generates. Plus I leave a lot of annotation feedback — like a professor marking a student's paper. I write the framework, AI generates, then I give plenty of margin notes. The human touch doesn't come from AI imitating a human; it's there because the framework and the opinions were mine to begin with."

### Summary

My information practices boil down to three rules:

1. Material goes into the repository, not chat windows;
2. Agents do the carrying and the processing; changes go through PRs, and I decide by reading the diff;
3. Framework and opinions come from me; AI does the expansion and the polish.

AI involvement is 90%+ in one repository and 5% in the other — a big gap — but in both, the material ends up in a repository that can be revisited and reviewed.

## How I Do AI Coding Today

Compared with before, three changes stand out.

### 1. Spec-Driven: From Personal Choice to Team Requirement

Specification, boundaries, acceptance criteria: the starting point of development.

It's now mandatory: use speckit, superpowers, or any well-known spec framework. What used to be a personal choice became a team requirement — the most visible change this year.

### 2. Line-Level Code: Less and Less Eyes-On, But Not Ignorable

In systems with a stable structure, people genuinely pay less and less attention to detailed code. The code-review experience and knowledge accumulated over the years, ironically, needs to keep being distilled into constraints.

I keep these constraints in a single set of guides, pinning down "what to look at, what to skip, and when you must look":

[GitHub - alswl/guides](https://github.com/alswl/guides)

The public version is `v0.0.1-alpha1`, with these guides so far:

| Guide                     | Stack                               | What it pins down                                                                                              |
| ------------------------- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `go-cli-guides.md`        | cobra · viper · `log/slog`          | Command tree structure, flag and config precedence, output/exit-code/error conventions                         |
| `go-server-guides.md`     | huma v2 · chi · GORM                | Layered `pkg/` layout, declarative API with generated OpenAPI, GORM restricted to table mapping and basic CRUD |
| `python-server-guides.md` | FastAPI · SQLAlchemy Core · Alembic | Layered `src/` layout, Pydantic schemas, Core-only explicit queries                                            |
| `go-tui-guides.md`        | Bubble Tea · Lip Gloss · Bubbles    | Elm architecture applied to a real application; business layering reuses the CLI guide                         |
| `fe-page-guide-antd.md`   | Ant Design v5 · ProComponents       | How to organize high-density information pages                                                                 |

Each guide picks exactly one stack and fixes one project structure; rules are written as imperatives. They are written for both humans and AI coding tools, so every rule must be short and checkable — no "it depends". Usage is simple: reference the corresponding file in the project's `CLAUDE.md` / `AGENTS.md` and let the agent follow it while writing code. I wrote a separate post about the story behind the frontend one: [How to Organize High-Density Pages](/2026/09/high-density-page-organization/).

### 3. Self-Testing Agent Verification

AI coding makes delivery density explode. Testing resources can hardly expand at the same pace.

My answer is a self-testing agent whose core pipeline is:

> Specification → Layered verification → Verdict → Write-back to acceptance

The specification is both the starting point of development and the source of assertions. Verification is layered from cheapest to most expensive, fail-fast:

| Layer | What it answers                               | Engine              |
| ----- | --------------------------------------------- | ------------------- |
| smoke | Does the service start? Do health gates pass? | Combined            |
| API   | Do the REST API contracts hold?               | Hurl                |
| CLI   | Is command-line behavior correct?             | bash + Go (testify) |
| E2E   | Do key frontend interactions still work?      | Playwright          |

The last step is verdict and write-back: instead of dumping a pile of logs, it produces a conclusion backed by run evidence and writes it back into the work item's acceptance criteria.

![Self-testing agent end-to-end pipeline (redrawn)](/images/202610/ai-native-ai-tests-e2e-v2.png)

![Three steps inside the verification engine (redrawn)](/images/202610/ai-native-verify-engine-v2.png)

### Summary

Seen together, the three changes form one line: specifications set the starting point, constraints watch the details on your behalf, and layered verification delivers verdicts. Less and less code needs a human watching line by line; what to build, what to build it by, and what counts as done, on the other hand, need to be written down more clearly than ever.

## My Personal Toolchain

Engineers fundamentally strengthen their management, work efficiency, and output speed through better tools. In this era, tools genuinely matter more than they used to.

I've invested quite a bit of time building my own toolchain. The ones I'm happy with so far:

- mind-forge (knowledge base manager)
- a skills collection
- skm, a manager that keeps SKILLs in sync across machines and deploys them quickly to remote hosts
- a review editor that works for me (I chose Vim)

[GitHub - alswl/skm: a tiny local-first AI Skill Manager](https://github.com/alswl/skm)

The skills I use most, some from the community:

- `speckit` — the spec-based suite
- `grilling` — interrogates me
- `humanizer` — makes me sound human

Some I wrote myself:

- `spec-report-html` — turns the current spec into a one-page report
- `spec-status` / `spec-update` — update spec status
- `session-retro` — reflects on the current session to improve local SKILLs
- `chat` — IRC-based agent collaboration
- `distill-memory` — distills local jsonl memory
- `repo-analyzer` — quick repository analysis, similar to deepwiki
- `mf-cli` — the companion SKILL for mind-forge

Earlier I said work itself has three lines, and the third is the "hidden line": improving the toolchain to raise efficiency. This list is my investment on that line.

## Some Opinions

### Efficiency Gains Will Hit a Bottleneck Soon

- Execution density is rising
- Decision density: the new bottleneck
- Information, judgment, consensus: cannot be skipped

### AI's WoW Time Is Passing

- New concepts: short-lived excitement
- Lasting value: how to land it
- Real business, real systems, real users — you have to fight for real

### Meetings Matter More

- AI accelerates output
- Disagreements surface faster
- Building consensus: higher value than ever
- Decisions, commitments, responsibility: these need humans

### Creation = "Originate" + "Produce"

- AI excels at "producing": generating, expanding, polishing
- Humans own "originating": questions, judgment, expression
- People will tire of purely AI-generated content
- Keep your opinions, experience, and personal edges

## Closing Notes

From February's "Code Typing is unnecessary", to May's "AI amplifies execution; humans own judgment", to August's connecting information, development, delivery, and toolchain into one line — what kept changing over these months was my understanding of where the human stands.

AI excels at "producing": generating, expanding, polishing. The "originating" is still yours: raise the questions, make the calls, and keep your own opinions, experience, and edges.

Update 2026-10-05: due to scheduling conflicts, my internal talk was postponed by a month, so this post came out a month late too. Agentic development moves fast — my latest practice has already moved a step beyond this article, touching the threshold of Stage 8. That said, I still recommend engineers walk through the stages one by one; in times changing this fast, experiencing it hands-on is a completely different feeling.

Wait for my next post.

## Further Reading

- [alswl/mind-forge](https://github.com/alswl/mind-forge): the knowledge-forging CLI behind the `minds` repository
- [alswl/skm](https://github.com/alswl/skm): a tiny tool for managing SKILLs across machines
- [alswl/guides](https://github.com/alswl/guides): development guides written for humans and agents to read together
- [github/spec-kit](https://github.com/github/spec-kit), [obra/superpowers](https://github.com/obra/superpowers): the two spec frameworks mentioned above
- [2025 Year in Review — At the Tipping Point](/2026/02/my-2025/)
- [How to Organize High-Density Pages: A Guide to Presenting Information](/2026/09/high-density-page-organization/)
- [From Toodledo to Obsidian Tasks — My GTD Best Practices](/2023/02/gtd/)
- [My Knowledge Management System](https://blog.alswl.com/2010/09/my-kms/)

---
title: "Continuing AI Native Practice: Moving Toward Stage 8"
author: "alswl"
slug: "ai-native-stage-8"
date: 2026-10-18T00:00:00+08:00
draft: false
categories: ["Technology"]
tags: ["AI", "AI Coding", "Multi-Agent", "Toolchain"]
---

![Cover: AI Native practice moving from multiple terminal windows to a collaborative network organized by a coordinator](/images/202610/ai-native-agent-coordination-cover.png)

I recently took another look at how I work. The biggest change is that I now hand complete tasks to a coordinator. It organizes other agents and moves the work forward, while I gradually step away from watching every window one by one.

This follows [my August article on AI Native practice](https://blog.alswl.com/2026/10/ai-native-work/). I look at the verification questions Stage 7 left open, the coordination experiments I tried as I moved toward Stage 8, and the new problems I ran into when I put them to work.

[How I Work in the AI Native Era, due August 2026](https://blog.alswl.com/2026/10/ai-native-work/ "!banner (/images/202610/banner-e7a22f6096cba86a.png) In my 2025 year-end review, I wrote that code typing would become an inefficient way to build software, and that AI Native should become the default. That is easy to say. Once I started working that way every day, the questions became concrete: where does the information come from, who chooses the approach, how do we verify the output, and what is left for people to do? After a year of practice, my view has changed several times. My focus has shifted from writing code faster to the whole chain of information, development, delivery, and tooling. This article describes how I work today, as of the end of August: how I process information, write code, build my toolchain, and what I have learned after running this setup for more than half a year.")

I use this Stage 1–8 progression diagram to locate my current way of working: from editor assistance, to several Coding Agents working in parallel, and then to a coordinator organizing execution. The sections below focus on the verification questions that came after Stage 7 and on the organizational practices I have tried while moving toward Stage 8.

These are still experiments. I have started handing coordination to an agent, but I need more practice and evidence from real tasks before I can say I have fully reached Stage 8. Being able to run several agents does not mean I can reliably take a task from requirements all the way to production.

![Stages 1 through 8: from editor assistance and parallel Coding Agents to coordinated execution](/images/202610/ai-native-stage-overview.png)

Figure 1: Eight stages of evolution, from editor assistance to multi-agent coordination.

## After Stage 7: Verification Is Not Finished

I group my Stage 7 practice into four parts: Spec Driven, Guides, verification, and the toolchain. As I followed this path, I found that my verification was still incomplete. After tests pass, I still need to ask: can these tests actually detect problems?

Here are the entry points for the spec-driven tool and its conventions repository.

[GitHub - github/spec-kit: 💫 Toolkit to help you get started with SDD or any other process!](https://github.com/github/spec-kit "!banner (/images/202610/banner-09f8bc864d898a1a.png) 💫 Toolkit to help you get started with SDD or any other process! - github/spec-kit")

### Tests Need to Be Tested, Too

Recently, I added another layer of verification to an internal testing tool: testing the tests.

First, finish the implementation and its tests. Then deliberately break the code for one behavior under test and run the relevant tests again. They should fail. If the behavior is broken but every test still passes, I need to go back and ask whether the tests reached the behavior they were supposed to verify.

A failure gives me another kind of evidence: at least this test caught this particular fault. It does not prove that the whole system is correct, but it answers “is this test effective?” better than a green screen alone.

This is related to the idea behind **mutation testing**: deliberately change code and see whether the tests detect the change. Stryker's documentation calls each introduced code variant a _mutant_. If a test fails, the mutant is “killed”; if the tests still pass, it “survives.” Code coverage shows where tests ran. Mutation testing goes further and asks whether the tests can recognize a fault. I have started by breaking the target behavior; that is not the same as a full mutation-testing assessment.

[What is mutation testing? | Stryker Mutator](https://stryker-mutator.io/docs/ "!banner (/images/202610/banner-377646a896425a08.png) TL; DR: Mutation testing introduces changes to your code, then runs your unit tests against the changed code. It is expected that your unit tests will now fail. If they don't fail, it might indicate your tests do not sufficiently cover the code.")

I think about verification in two layers: verify the deliverable, then check whether the verification itself is trustworthy. This step deserves focused effort of its own.

![Testing the tests: break the behavior under test, rerun the tests, and see whether they catch the fault](/images/202610/mutation-testing-demo.png)

Figure 2: How to judge tests of tests. After deliberately introducing a fault, the test should fail; this only shows that it caught this particular fault.

### Ask Agents to Explain Their Choices

Another change is that I ask agents to explain the basis for their decisions: what alternatives they considered, which one they chose, why they chose it, and what evidence supports the choice.

I give them room to make decisions, and ask them to explain those decisions. When I need to step in, I can discuss a specific disagreement instead of reconstructing why the agent went down a particular path from a long execution log.

### A Few New Uses in My Toolchain

Recently, I have also been using these Skills:

| Skill       | How I use it                                        |
| ----------- | --------------------------------------------------- |
| `asr`       | Voice input, which connects to how I record thought |
| `pr-visual` | Visualizing PRs to help inspect changes             |
| `ablation`  | Using ablation to find code that can be removed     |

These Skills live in my Skills repository.

I use skm to manage Skills.

[GitHub - alswl/skm: a tiny local-first AI Skill Manager](https://github.com/alswl/skm "!banner (/images/202610/banner-694646ef30044df5.png) a tiny local-first AI Skill Manager. Contribute to skm development by creating an account on GitHub.")

I use a knowledge-base tool to manage information and articles.

## Moving Toward Stage 8: Handing Coordination to a Captain

### Community Practice: Continuous Operation and Organized Work

I looked at two ways of running `/loop`. One prompt asks an agent to keep watching issues, review PRs, run the software, and handle community feedback. Another filters feedback first, then decides whether it should lead to a fix and release.

![Example loop prompt: monitor issues, review PRs line by line, run the software, and handle community feedback](/images/202610/loop-community-maintenance.png)

Figure 3: An example of continuously handling issues, PRs, and community feedback.

![Example loop prompt: filter relevant feedback before starting implementation or a fix](/images/202610/loop-feedback-triage.png)

Figure 4: First decide whether feedback is relevant, then invest in follow-up work.

[Yetone on X: running three loops in parallel](https://x.com/yetone/status/2109855710444237018 "!banner (/images/202610/banner-yetone-loop.png) Many people have asked me to share my workflow. I haven't known how, because there is no magic in it; it is even pretty crude, and I always feel it would be pointless to share. I just use Claude Code with the official Opus 5.5 model to run loops. I run the three loops in the picture in parallel, then spend a little time each night cleaning up after them, mostly UI/UX issues. Then I'm out of work.")

Another talk was Lauren Tan's “I shipped 2000 PRs last month.” What stayed with me was how to organize the work: run things like a restaurant, arrange the chefs and improve the process, instead of always stepping in to cook every dish myself.

![Screenshot from Lauren Tan's talk: I shipped 2000 PRs last month](/images/202610/lauren-tan-2000-prs-talk.png)

Figure 5: Lauren Tan's talk; 2,000 PRs is the speaker's own account.

[How I Shipped 2000 PRs Last Month — Trusting AI Agents | Grok Bot | Lauren Tan](https://www.youtube.com/watch?v=NjoZoUm85x0 "!banner (/images/202610/banner-ae97ec5fd18858a6.jpg)")

I refer to these community examples while keeping their limits in mind. Practices from device-side and client applications do not automatically apply to every business system. In open-source projects, I can learn from the commit history and see how the work is organized. With my own systems, I still need to check whether permissions, deployment, and acceptance fit together.

### My Practice: A Captain Organizes Execution

I now use a 1+N organization. One coordinator owns the task and starts other agents as needed. I follow the coordinator's progress and results; it manages the agents below it.

![From one Claude Code session and several agents to a coordinator that schedules the work](/images/202610/multi-agent-orchestration.png)

Figure 6: From one agent, to several agents in parallel, to unified coordination.

### The Captain Coordinates Instead of Getting Lost in Implementation

The coordinator organizes tasks, assigns work, handles disagreements, and summarizes results. At the start, it works with me to clarify the request, goal, and boundaries. It can also handle a small, quick task directly. For complex work, I limit how much implementation it does itself; in some cases, I even limit its access to the code.

This protects its context. If it stays deep in implementation details, its context fills quickly, and the original goals and constraints can get lost. Delegating the concrete work also lets execution happen on different machines.

I do not define a fixed Agent Team in advance. The coordinator decides what roles and how many agents it needs for each task. The coordination responsibility stays; the execution team can change.

For now, these limits are mostly expressed through Skills and the logbook framework. They are soft constraints, and an agent may forget them. I give the coordinator a more capable model, limit the details it sees, and persist state to disk. If it loses its way, I can restart it.

### Use Herdr to Manage Sessions and Attention

The version of Herdr I use helps me manage agent sessions, messages, and attention, and supports running across machines. The tool can change. What matters more to me is whether it shows which tasks are moving and where I need to step in.

## Connect the Delivery Process with a Logbook

### Write Down the Goal, Path, and Delivery Contract

The complete path I want to connect is: **request → design → confirmation → development → verification → verification of verification → release**. A 1+N group of agents manages every step. Confirming the goal and boundaries, and checking whether verification is effective, are separate steps in the process too.

I use logbook Kit (lbkit) to organize this process. Logbook handles a different layer: what I want, which path to follow, what constraints apply, and what to deliver at the end.

[GitHub - alswl/lbkit: logbook kit](https://github.com/alswl/lbkit "!banner (/images/202610/banner-03fe3a0c63df7885.png) logbook kit. Contribute to lbkit development by creating an account on GitHub.")

![My end-to-end workflow and tool responsibilities: 1+N agents manage tasks, Herdr manages attention, and logbook manages goals and paths](/images/202610/delivery-workflow-overview.png)

Figure 7: The end-to-end workflow and tool responsibilities. The two verification layers check the deliverable and the tests themselves.

I have specific requirements for logbook: **constrain the runtime, constrain the approach, enforce the process, and make the deliverables explicit**. I write down the budget, execution environment, permissions, available context, required process, and deliverables. The agent should receive the information it needs, and its permissions should be limited where necessary.

![Example of a complete logbook structure: legend, goals and non-goals, skills, links, working directory, and execution conventions](/images/202610/logbook-structure.png)

Figure 8: A logbook structure with goals and non-goals, skills, supporting material, working directory, and execution conventions.

There is one boundary: **a logbook constrains the approach; it does not contain the specific design or code**. Design and implementation stay in their own working locations. The logbook connects the goal, path, and delivery requirements.

The process has some enforcement while leaving room for execution. Each step needs a clear result; the agent responsible for that step decides how to produce it.

### Track Progress with Stages and Human Checkpoints

I divide tasks into stages and record the to-dos, artifact locations, and verification evidence within each stage. I mark places that need human involvement separately. After I merge something or log in, the agent continues with the follow-up verification. When I check progress, I can tell whether work is still underway or has reached a checkpoint that needs me.

![Logbook stages: design, development and testing, review and fixes, human merge and login, and follow-up acceptance](/images/202610/delivery-stage-checkpoints.png)

Figure 9: From design and development through review, human checkpoints, and follow-up acceptance. Checkmarks and numbers show the task state at the time of the screenshot.

I ran into a practical problem: if an agent keeps stopping to ask for confirmation, the task cannot keep moving. I made three main adjustments.

### Make Key Decisions at the Start

First, clarify the goal, boundaries, and delivery requirements, then begin execution. If an open-ended question is still unsettled, I discuss it thoroughly with a capable agent first. Once the direction is clear, I hand it to multiple agents.

Multi-agent work is better suited to delivery tasks that already have a direction. When the design itself is still open, splitting it among a group of agents too early can add communication costs before it adds value.

### Rehearse the Whole Process with Preflight

Logbook's Preflight rehearses the path before execution. It identifies needed resources, possible permission problems, and checkpoints that need human confirmation. I review these points before starting.

This lets me resolve some obstacles before they appear halfway through the work. Preflight cannot prevent every change, but it can reduce interruptions that were predictable.

![Preflight rehearses the path from request to release and checks resources, permissions, and human checkpoints](/images/202610/preflight-workflow.png)

Figure 10: Preflight checks the complete path before execution and surfaces resources, permissions, and human checkpoints early.

### Ask for Confirmation When the Result Is Visible

Some things do not need repeated questions while the work is half-finished. The agent can move forward on the parts that are clear, prepare enough material for a decision, and bring the questions that need my confirmation together. If an issue does not block other work, it can be recorded while the agent continues with what it can do.

Checkpoints that need human permissions or a final decision still need to stay. I still handle merges myself. I want to reduce scattered interruptions along the way so I can decide based on a more complete result.

## Let Delivery and Verify Take Different Positions

The two roles I care about most are Delivery and Verify. Delivery pushes the work forward; Verify checks it. Each has something to protect, so disagreements are normal.

![Multi-agent collaboration: requirements and conventions, development, testing and review loops, human checkpoints, release checks, and to-dos](/images/202610/delivery-verification-collaboration.png)

Figure 11: A multi-agent collaboration example covering inputs, development and verification rounds, human checkpoints, and follow-up acceptance. The rounds, PR count, and completion states apply only to this task.

For this task, I first had the agents align on the requirements and front-end conventions, then had development, testing, and review work through several rounds. When testing found a problem, it went back to development for a fix and another test. When agents disagreed, they talked to each other and worked through the issue.

After the agents reached agreement, I still reviewed screenshots and verification evidence, then handled checkpoints such as merging and logging in. Verification then went back to the agents. The diagram includes both completed work and branches still waiting for human verification, so “delivered” cannot mean only that development has finished.

If every agent treats “finish quickly” as its only goal, they can all skip problems together. I want the verifier to look hard for defects and the delivery agent to provide explanations and evidence. They discuss the issue first and continue if they can resolve it. If they cannot, the coordinator steps in. If it still cannot resolve the disagreement, it comes to me.

I use chatta to support communication among agents. Discussions also need a limit on the number of rounds. The coordinator must drive the discussion toward a decision rather than let it run forever. In the end, I look at evidence such as execution results and screenshots, not just whether the agents say they agree.

[GitHub - alswl/chatta: chatta is chat to agent, tiny CLI and SKILL](https://github.com/alswl/chatta "!banner (/images/202610/banner-42ecbf2dfe02b79a.png) chatta is chat to agent, tiny CLI and SKILL. Contribute to chatta development by creating an account on GitHub.")

### Multi-Agent Work Has a Cost; Choose the Right Tasks

Passing context and communicating both cost time. Starting more agents does not automatically produce a better result.

I am willing to pay the multi-agent cost for two main reasons. One is that a single agent has limited context. Separating work reduces the pressure of fitting every detail into the same context. The other is perspective: even if context windows get larger, it is still useful to preserve different concerns around delivery, quality, and reliability. The first is a current capability limit; the second is an organizational choice.

I make a rough distinction based on task size. By traditional development estimates, a task that takes half an hour or half a day usually needs only one agent. A task closer to a week, with changes likely to come up during execution, is more likely to benefit from this coordination and adversarial review. This is my experience choosing tasks, not a fixed threshold.

Even when the goal is clear, new situations can arise during execution. Keeping agents with different perspectives in the process helps handle those changes; the point is not just to split the task once before work begins.

## Some New Thoughts

### Put Bandwidth into a Complete Workflow

I am paying more attention to my decision density and bandwidth. I need a standard workflow that fits me and covers the complete path, so agents can run longer and I can feel less pressure.

Decision density has been a bottleneck for me. I now try to hand the end-to-end path to a coordinator and organize it with logbook, reducing the time I spend chasing progress in individual windows. The process runs from receiving a request through delivery. If a step lacks resources, evidence, or a human decision, I handle it there.

I have made one agreement with myself: at the end of every complex session, do a Retro and write what I learned back into Skills and documentation so the next run can use it.

Reflection does not need to wait until the whole task is finished. I can record thoughts and lessons while work is still moving and pass them on to the next step. The end of a complex session is a point for recording, not a requirement to wait until the project is over before looking back.

### Adversarial Review May Matter More Than Loops

I think adversarial review may matter more than loops. The more useful questions now are: which role in the loop challenges the result, which test can find an error, and who decides when a disagreement appears?

The different positions of Delivery and Verify, asking an agent to substantiate its decisions, and deliberately breaking target code to check tests all address these questions. With only a mechanism for moving work forward, a system can pass errors along very efficiently. Putting challenges into the process gives problems a chance to surface before delivery.

### Protect a Continuous Block of Attention

I want agents to run longer without interruption. When many tasks run in parallel, switching between windows and answering questions can easily break my train of thought.

As of mid-October, my personal observation is that the coordinator commonly runs for around 30–50 minutes before needing me, with the longest stretch close to two hours. This is not a measured statistic or a promise of capability. Even so, I find it tiring and still want to reduce how often I need to take over.

That is one reason I am willing to spend more on execution so agents can prepare the material and evidence first. Model usage and human attention should not be treated as the same kind of cost. I need to preserve uninterrupted time to think about architecture, judge approaches, and handle the questions that truly need me.

![Agents keep work moving, non-blocking questions wait for an answer, and people retain focused time for key decisions](/images/202610/protect-focus-with-agents.png)

Figure 12: Record non-blocking questions so people can keep focused time; retain the human checkpoints that matter.

### Preserve the Thinking Process

I need to stay in control of my attention, thought process, and decisions. Beyond protecting time, I want to preserve how I reached a conclusion: what options I considered, where disagreements arose, and why I made the final call.

I use voice to pass emerging ideas to an agent, then save the points considered in the discussion to thinking. Alongside the final deliverable and source material, I want this record so I can continue making decisions later.

One inspiration for recording thinking came from DeepSeek-R1. Its paper discusses developing reasoning capabilities through reinforcement learning and shows the model revisiting its solution path and checking its own work. This made me more interested in keeping the options considered and the reasons behind a decision. In my work, I save plans, trade-offs, and verification evidence that I can review later. That differs from the model-training mechanism described in the paper, and I still need to test its effect in my own tasks.

[DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948v1 "!banner (/images/202610/banner-ab77af3fa25e0e90.png) We introduce our first-generation reasoning models, DeepSeek-R1-Zero and DeepSeek-R1. DeepSeek-R1-Zero, a model trained via large-scale reinforcement learning (RL) without supervised fine-tuning (SFT) as a preliminary step, demonstrates remarkable reasoning capabilities. Through RL, DeepSeek-R1-Zero naturally emerges with numerous powerful and intriguing reasoning behaviors. However, it encounters challenges such as poor readability, and language mixing. To address these issues and further enhance reasoning performance, we introduce DeepSeek-R1, which incorporates multi-stage training and cold-start data before RL. DeepSeek-R1 achieves performance comparable to OpenAI-o1-1217 on reasoning tasks. To support the research community, we open-source DeepSeek-R1-Zero, DeepSeek-R1, and six dense models (1.5B, 7B, 8B, 14B, 32B, 70B) distilled from DeepSeek-R1 based on Qwen and Llama.")

In _Thinking, Fast and Slow_, Daniel Kahneman discusses the difference between fast, intuitive thinking and slow, deliberate thinking. This gives me one way to think about the process of making a decision. But what I say below about my experience with voice and text is personal; the two input modes do not map directly to the book's two kinds of thinking.

[Thinking, Fast and Slow](https://www.penguin.co.uk/books/563861/thinking-fast-and-slow-by-kahneman-daniel/9780141033570 "!banner (/images/202610/banner-db774a5a922c7c90.jpg) Why is there more chance we'll believe something if it's in a bold type face? Why are judges more likely to deny parole before lunch? Why do we assume a good-looking person will be more competent? The answer lies in the two ways we make choices: fast, intuitive thinking, and slow, rational thinking. This book reveals how our minds are tripped up by error and prejudice (even when we think we are being logical), and gives you practical techniques for slower, smarter thinking, enabling you to make better decisions at work, at home, and in everything you do.")

For me, voice and text are two different ways of thinking. Some ideas unfold more easily when I speak; when I type, I tend to stop and organize them. The value of voice input is not only speed. It lets me say an idea while it is still taking shape, then organize it into text.

I do not trust agents easily, and I keep asking how I can trust them with better evidence. My approach is to give an agent room to make judgments and decisions, while asking it to substantiate them. Having Delivery and Verify discuss the work from different positions serves the same purpose.

### I Still Need to Engage with Architecture

I still draw architecture diagrams and make architecture decisions myself, and occasionally inspect code. I cannot hand these things off just because execution has been delegated.

The coordination approach gives me a wider scope of execution, and it also requires me to know more clearly where my own judgment is needed. Drawing diagrams and spot-checking code are concrete ways for me to stay connected.

## The Relationship Between People and AI: Where Do People Stand After Delegating Execution?

After letting agents do more, I still need to answer a question: once execution is delegated, what should I do?

![Human-AI collaboration: people provide goals and constraints; agents return work and verification evidence](/images/202610/human-agent-collaboration.png)

Figure 13: People define the problem, make judgments, and accept the work. Agents execute, verify, and deliver; evidence helps build trust.

### Return from Efficiency to Judgment and Consensus

Execution density, decision density, and reaching consensus are the three issues I keep coming back to. Multiple agents can speed up execution, but someone still needs to decide what to do before work starts, what to accept at delivery, and how to resolve disagreements.

This time, I put those decisions in specific places: clarify goals and boundaries at the start, let the coordinator handle scheduling and ordinary disagreements during execution, escalate to me when necessary, and deliver with evidence at the end. After the initial excitement around AI, I care more about whether this process works on real tasks.

### Let Disagreements Surface, and Let People Make Commitments

I do not like meetings, but I increasingly think communication matters. We need more meetings to surface disagreements sooner and make decisions and commitments. Different perspectives need to see the problem; faster execution should not mean skipping disagreement.

Agents can discuss, verify, and converge with each other first. When a question involves trade-offs in goals, human permissions, or a disagreement they cannot resolve, I need to take it on. Letting agents run longer is meant to concentrate my involvement at these checkpoints.

### Keep More of the Human Touch

I divide creation into “create” and “produce”: creating means defining the problem, making judgments, and designing; producing means making, expanding, and polishing. AI can help with production, but I need to accept the work I hand over. **I cannot give someone a document generated by AI that I do not believe in myself.**

Drawing diagrams, spot-checking code, reviewing execution evidence, and reading and accepting the articles I publish are all ways I stay involved in the work. Agents can do more execution, but I still need to know why I accept the result.

“More of the human touch; the human touch is scarce.” What remains should include my own questions, judgments, and expression.

### Hidden Information and the Boundaries of Knowledge

The idea of **tacit knowledge** is useful here. In _The Tacit Dimension_, Michael Polanyi summarizes the problem as “we can know more than we can tell.” It helps me make my concern more specific: the text I give an agent may not include all the experience I rely on when making a judgment. Whether that experience can be expressed, learned, or used to make new discoveries are separate questions.

[The Tacit Dimension](https://press.uchicago.edu/ucp/books/book/chicago/T/bo6035368.html "!banner (/images/202610/banner-6d676977a487fead.jpg) A classic work in the philosophy of science that changed how we think about knowledge itself. “I shall reconsider human knowledge by starting from the fact that we can know more than we can tell,” writes Michael Polanyi, whose work paved the way for the likes of Thomas Kuhn and Karl Popper. The Tacit Dimension argues that tacit knowledge—tradition, inherited practices, implied values, and prejudgments—is a crucial part of scientific knowledge. As relevant today as when it was first published, this volume challenges the assumption that skepticism, rather than established belief, lies at the heart of scientific discovery. “The reissuing of this remarkable book gives us a new opportunity to see how far-reaching—and foundational—Michael Polanyi’s ideas are, on some of the age-old questions in philosophy.” —Amartya Sen, from the Foreword")

I still have a question I cannot answer: some information that affects a judgment is never spoken or included in the available material; other discoveries may go beyond what can be directly derived from existing knowledge. For example, could AI have discovered relativity? I do not have enough evidence to answer, but the question keeps me thinking about the roles of human judgment, tacit knowledge, and new discoveries in this kind of collaboration.

## Closing Thoughts

### A Live Example of Non-Code Delivery

Before the talk, I also gave an agent a task: make an introductory video based on the talk's documents and content. Near the end, I opened and played the generated result live, then reviewed how the coordinator and its agents had worked together. This extended “deliverable” beyond code into content production. The live demo showed that the task produced a playable result; it did not amount to a comprehensive quality review.

I would rather describe my current state as “moving toward Stage 8.” I have started using multi-agent coordination, but there is still plenty to practice and verify before I can say I have fully reached Stage 8.

Next, I need to show the results across more real tasks: whether delivery quality is stable, whether the process can reliably reach production, how it handles changes, and how much human involvement it still needs. The examples here show progress at one point in time; they are not enough to show that the whole approach is mature.

I have three reminders for my next steps:

- **Method: emulate the successful path of traditional software development.** Connect requirements, design, confirmation, development, verification, and release.
- **Idea: create a loop.** Execution returns with evidence; disagreements drive fixes and retesting.
- **Challenge: understand the essence of the engineering process.** I need to understand why each step exists before deciding which work to delegate and which checkpoints to keep for myself.

My challenge to myself is “2,000 PRs in one month, and ship them.” I have not achieved this goal yet, and the second half matters as much as the first. What I need to improve next is whether this way of organizing work can deliver tasks continuously, and how often I need to step in.

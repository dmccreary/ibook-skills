---
title: Token Budgets and Usage Limits
description: Treats tokens as an engineering budget -- cost model, plan limits and usage windows, context management, and the serial-versus-parallel agent tradeoff.
generated_by: claude skill chapter-content-generator
date: 2026-08-22 13:50:00
version: 0.09
---

# Token Budgets and Usage Limits

## Summary

This chapter treats tokens as an engineering budget: the token cost model, input versus output tokens, and the Claude Pro and Max plan limits with their four- and five-hour usage windows. It introduces the tradeoff between serial and parallel sub-agent execution and the roughly 12,000-token startup cost of each additional agent. Students will be able to estimate whether a task is cheaper run serially or in parallel after this chapter.

## Concepts Covered

This chapter covers the following 21 concepts from the learning graph:

1. Token Budget
2. Token Cost Model
3. Context Window Management
4. Sub-Agent Startup Overhead
5. Input Versus Output Tokens
6. Token Frugality Principle
7. Claude Pro Plan Limits
8. Context Compaction
9. Claude Max Plan Limits
10. Four-Hour Usage Window
11. Tokens Per Minute Limit
12. Serial Agent Execution
13. Parallel Agent Execution
14. File Layout as Token Strategy
15. Batch Script Substitution
16. Selective File Reading
17. Token Cost Estimation
18. Five-Hour Usage Window
19. Rate Limit Handling
20. Serial Versus Parallel Tradeoff
21. Separate References Files

## Prerequisites

This chapter builds on concepts from:

- [1. Foundations of AI, Language Models, and Prompting](../01-foundations-ai-language-models/index.md)
- [2. AI Coding Agents and the Five Levels of Textbook Intelligence](../02-ai-agents-textbook-intelligence/index.md)
- [3. Python Fundamentals for Skill Automation](../03-python-fundamentals-automation/index.md)

---

!!! mascot-welcome "Let's talk money — token money."
    ![Kit waves hello with their tool satchel](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    Most teachers building a book on this library aren't paying for a $200/month plan. This chapter is how you make a $20/month plan stretch across an entire textbook. Right tool, right task!

## Tokens as an Engineering Budget

A **token budget** is a planned allowance of tokens for a task or a period, treated as a limited resource to be spent deliberately rather than an afterthought. Spending it well starts with a **token cost model**: an understanding of what drives consumption — content read, content generated, and overhead paid per agent — used to predict expense before work begins. Part of that model is the **input versus output token** distinction: text supplied to a model and text produced by it are metered separately and priced differently, so a task that reads a huge file but writes a short answer costs very differently from one that reads little and writes pages.

All of this adds up to the **token frugality principle**: the design rule that a workflow should produce the required quality at the lowest token cost, so authors on inexpensive plans can complete a book. Every other concept in this chapter is really just one technique in service of that one principle.

## Plan Limits and Usage Windows

Token spending isn't unlimited even if you're willing to spend it. **Claude Pro plan limits** are the usage allowance of the lower-cost subscription tier, constraining how much generation can occur within a given period; **Claude Max plan limits** are the larger allowance of a higher-cost tier. Both are measured over a rolling period rather than a fixed calendar day: a **four-hour usage window** measures consumption against a plan allowance on some plans, after which capacity replenishes, while a **five-hour usage window** does the same on others.

#### Diagram: 4-Hour Token Window Visualization

<iframe src="../../sims/4-hour-token-window-visualization/main.html" width="100%" height="420px" scrolling="no"></iframe>

<details markdown="1">
<summary>4-Hour Token Window Visualization (reused MicroSim)</summary>
Type: timeline
**sim-id:** 4-hour-token-window-visualization<br/>
**Library:** vis-timeline<br/>
**Status:** Reused<br/>
**Source:** docs/sims/4-hour-token-window-visualization

Reused from this book's own MicroSim catalog. Learning objective: Explain how a rolling four-hour usage window replenishes capacity over a working session.
</details>

#### Diagram: 5-Hour Token Window Visualization

<iframe src="../../sims/5-hour-token-window-visualization/main.html" width="100%" height="420px" scrolling="no"></iframe>

<details markdown="1">
<summary>5-Hour Token Window Visualization (reused MicroSim)</summary>
Type: timeline
**sim-id:** 5-hour-token-window-visualization<br/>
**Library:** vis-timeline<br/>
**Status:** Reused<br/>
**Source:** docs/sims/5-hour-token-window-visualization

Reused from this book's own MicroSim catalog. Learning objective: Compare a rolling five-hour usage window against the four-hour window used on other plans.
</details>

A separate cap applies on top of the windowed allowance: the **tokens per minute limit**, a cap on throughput distinct from a total allowance, that governs how quickly work may proceed even if you're nowhere near your total budget for the window. When you hit either cap, the response is **rate limit handling**: responding to a throughput or allowance cap by pacing work rather than failing outright, so a long job completes across periods instead of erroring out.

!!! mascot-warning "Hitting a rate limit mid-task isn't a crash."
    ![Kit holding up a caution paw](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    The first time you hit a usage window limit mid-chapter, it can feel like something broke. It didn't — the work is safely saved, and capacity resumes on a rolling basis. Pace large batch jobs (like generating 31 chapters) with that rolling refresh in mind rather than racing to finish before a wall you don't control.

## Keeping Context Under Control

Tokens spent aren't the only budget in play — so is what fits in working memory at once. **Context window management** is deliberately controlling what enters a model's working memory so the relevant material fits and nothing is wasted, a discipline you first met conceptually in Chapter 1. Over a long session, the harness applies **context compaction**: summarizing earlier parts of a long session so work can continue after the accumulated material would otherwise exceed capacity.

!!! mascot-thinking "Compaction is why long sessions don't just stop."
    ![Kit thinking with a paw on their chin](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    Without compaction, a long working session would eventually hit a hard wall the moment history exceeded the context window. With it, older material gets summarized rather than dropped, so a session generating 31 chapters in sequence can keep going well past what any single context window could hold raw.

## Serial Versus Parallel Agent Execution

Every additional agent you launch costs something before it does any useful work at all: **sub-agent startup overhead**, the fixed token cost of launching an additional agent, incurred before it performs any useful work, because it must receive its own instructions and tool definitions — roughly 12,000 tokens, measured on this project. That overhead is the entire reason **serial agent execution** (running one agent that completes an entire task, paying startup overhead only once) and **parallel agent execution** (running several agents at once on portions of a task, paying startup overhead once per agent) aren't simply "fast" versus "slow" — they're a real cost tradeoff.

#### Diagram: Serial Versus Parallel Cost Calculator

<iframe src="../../sims/serial-versus-parallel-cost-calculator/main.html" width="100%" height="552px" scrolling="no"></iframe>

<details markdown="1">
<summary>Serial Versus Parallel Cost Calculator</summary>
Type: microsim
**sim-id:** serial-versus-parallel-cost-calculator<br/>
**Library:** p5.js<br/>
**Status:** Specified

Bloom Level: Apply (L3)
Bloom Verb: Calculate

Learning objective: Calculate the total token cost of a task run serially versus in parallel, and identify the agent-count threshold where parallel execution stops paying off.

Canvas layout:
- Top: three sliders — "Number of sub-tasks" (1-20), "Tokens of real work per sub-task" (1,000-50,000), "Startup overhead per agent" (default 12,000, adjustable 5,000-20,000)
- Middle: two bar totals side by side, "Serial Total" and "Parallel Total," in tokens
- Bottom: a one-line verdict, e.g. "Parallel costs 84,000 more tokens for this workload" or "Parallel and serial cost about the same here"

Data Visibility Requirements:
  Stage 1: Show each sub-task's work-token cost as an individual small bar
  Stage 2: Show serial total = (work-tokens x sub-tasks) + (1 x startup overhead)
  Stage 3: Show parallel total = (work-tokens x sub-tasks) + (sub-tasks x startup overhead)
  Final: Show the numeric difference and which approach is cheaper at the current slider settings

Interactive controls:
- Three sliders described above
- Toggle: "Show formula" to reveal the two total formulas as live-updating equations

Behavior:
- Moving any slider recomputes both totals instantly and updates the verdict line
- When sub-tasks = 1, both totals are equal (parallel overhead of one agent equals serial overhead of one agent), and the sim highlights this as "no benefit from parallel with only one sub-task"

Instructional Rationale: An Apply-level calculator lets the reader plug in this chapter's own example numbers (a 350-term glossary, a 12-chapter book) and see the real crossover point, rather than trusting the "roughly 38% more" figure on faith.

Implementation notes: Use p5.js; all math is simple arithmetic, no external data needed; responsive layout for slider and bar widths.
</details>

Choosing between them is the **serial versus parallel tradeoff**: the decision between finishing sooner and spending less. Parallelism reduces elapsed time but multiplies fixed overhead, and is only justified when the work per agent is genuinely large enough to dwarf that overhead.

## Token Strategies in File Layout

How you organize files on disk is itself a token strategy. **File layout as token strategy** means organizing content into separate files so a routine update reads only a small file instead of a large one — **separate references files** is the concrete example: storing each chapter's citations in a dedicated file so reference maintenance doesn't require loading chapter prose just to fix one citation. **Batch script substitution** replaces repetitive generated output with a program that produces the same result, so the model performs only the creative portion — the same division of labor from Chapter 3, viewed through a cost lens. **Selective file reading** means loading only the portion of a file relevant to the current task rather than its entire contents, the same technique this very chapter's generation used when it grepped specific glossary terms instead of reading the whole file.

!!! mascot-tip "Grep before you read the whole file."
    ![Kit holding up a tool with a knowing look](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    If you only need three definitions out of a 500-term glossary, search for those three terms instead of loading the entire file. It's a small habit that adds up fast across a whole book's worth of work.

## Estimating Cost Before You Start

Put the cost model, the plan limits, and the file-layout strategies together, and you get **token cost estimation**: predicting the consumption of a planned task from measured rates, so an author knows the price before committing to it — the difference between discovering a book cost too much halfway through and knowing the number going in.

## Key Takeaways

- A **token budget**, guided by a **token cost model** and the **input versus output** distinction, is what the **token frugality principle** actually optimizes.
- **Plan limits**, **usage windows** (four- or five-hour), the **tokens-per-minute** cap, and **rate limit handling** govern how much and how fast you can work.
- **Context window management** and **context compaction** keep a long session running past what raw context alone could hold.
- **Sub-agent startup overhead** (~12,000 tokens) is why the **serial versus parallel tradeoff** favors serial execution unless each sub-task's real work is large.
- **File layout strategies** — **separate references files**, **batch script substitution**, **selective file reading** — reduce cost without reducing quality, and **token cost estimation** tells you the price before you start.

!!! mascot-celebration "You can now price a chapter before you write it."
    ![Kit celebrating with arms raised](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    You just learned to treat tokens the way a careful builder treats materials — measured, budgeted, and never wasted on a cut you didn't need to make. Right tool, right task!

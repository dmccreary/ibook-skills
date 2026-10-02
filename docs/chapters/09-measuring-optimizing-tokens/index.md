---
title: Measuring and Optimizing Token Usage
description: Covers deterministic work offloading, quality-gate short-circuiting, the glossary token benchmark, token waste antipatterns, usage hooks and dashboards, and budgeting a whole book.
generated_by: claude skill chapter-content-generator
date: 2026-08-22 14:05:00
version: 0.09
---

# Measuring and Optimizing Token Usage

## Summary

This chapter covers file-layout token strategies -- separate references and quiz files, batch script substitution -- alongside usage-tracking hooks, JSONL logs, and dashboards for elapsed time and token consumption. It closes with techniques for estimating the token cost of a complete book and avoiding common token-waste antipatterns. Students will be able to install a usage hook and analyze its log output after this chapter.

## Concepts Covered

This chapter covers the following 21 concepts from the learning graph:

1. Separate Quiz Files
2. Deterministic Work Offloading
3. Grep Before Read
4. Marginal Token Cost
5. Skill Usage Hook
6. Token Waste Antipatterns
7. Glossary Token Benchmark
8. Quality Gate Short-Circuit
9. Stop Hook
10. JSONL Usage Log
11. Token Cost Per Term
12. Cached Quality Score
13. Skill Usage Analytics
14. Token Management Strategies
15. Elapsed Time Measurement
16. Chapter Token Budgeting
17. Model Versus Script Division
18. Token Usage Dashboard
19. Cost Per Book Estimate
20. Budget-Constrained Authoring
21. Optimizing Claude Usage

## Prerequisites

This chapter builds on concepts from:

- [1. Foundations of AI, Language Models, and Prompting](../01-foundations-ai-language-models/index.md)
- [2. AI Coding Agents and the Five Levels of Textbook Intelligence](../02-ai-agents-textbook-intelligence/index.md)
- [3. Python Fundamentals for Skill Automation](../03-python-fundamentals-automation/index.md)
- [6. Agent Skill Fundamentals](../06-agent-skill-fundamentals/index.md)
- [7. Progressive Disclosure and Meta-Skill Routing](../07-progressive-disclosure-meta-skills/index.md)
- [8. Token Budgets and Usage Limits](../08-token-budgets-usage-limits/index.md)

---

!!! mascot-welcome "From principle to practice."
    ![Kit waves hello with their tool satchel](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    Chapter 8 gave you the vocabulary for token budgets. This chapter gives you the actual techniques and the tools to measure whether they're working. Right tool, right task!

## Deterministic Work Offloading

The single biggest lever for token frugality is deciding, correctly, who does each step. **Deterministic work offloading** means assigning every step with a single correct answer to a program, reserving the model for judgment and composition — the practice behind the **model versus script division**: the design rule separating work that requires judgment, which the model performs, from work with one correct answer, which a program performs. You already practiced the reading-side version of this in Chapter 8's tip: **grep before read** means searching for a pattern to locate relevant lines before opening a whole file, so only the necessary region gets loaded.

## Skipping Work You Don't Need

Not every check needs to run every time. A **quality gate short-circuit** skips a validation step whose result is already known to pass, avoiding cost without lowering standards — the trick is knowing when a result is *actually* already known, which is what a **cached quality score** provides: a previously computed assessment stored with a document so later runs can read it instead of recomputing it.

!!! mascot-tip "If nothing changed, don't re-check it."
    ![Kit holding up a tool with a knowing look](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    Re-running a full quality validation on a glossary that scored 96 and hasn't been touched since is pure waste. Cache the score, check whether the file changed, and only re-validate when it has.

## Measured Benchmarks: The Glossary Case Study

This project doesn't rely on folklore about what's expensive — it measures. The **glossary token benchmark** is a measured reference point showing that a 350-term glossary can be produced by a single agent for roughly 31,000 tokens. Dividing that total across the terms gives the **token cost per term**: the average consumption attributable to each glossary entry, useful for estimating the cost of a glossary of any size. More generally, the **marginal token cost** is the additional cost of one more unit of output after fixed overhead is excluded, used to predict how expense scales with size — the number that actually matters once you're past the first few entries.

| Measurement | Value | What It Tells You |
|-------------|-------|---------------------|
| Glossary token benchmark | ~31,000 tokens for 350 terms | Whole-task cost, one serial agent |
| Token cost per term | ~54 tokens/term (marginal) | Cost of scaling to a larger glossary |
| Fixed overhead | The remainder of the 31,000 | Paid once, regardless of glossary size |

## Recognizing Token Waste

Some habits burn tokens without buying anything. **Token waste antipatterns** are recurring practices that consume tokens without improving results, such as launching unnecessary parallel agents for small tasks or manually assembling data a script could sort in one pass. Avoiding them in a structured way means applying **token management strategies**: the collected techniques for controlling consumption — file separation, script substitution, gate short-circuiting, and selective reading — as a coherent toolkit rather than one-off tricks.

!!! mascot-warning "Parallel agents for a five-item list is waste, not speed."
    ![Kit holding up a caution paw](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    Remember the ~12,000-token startup overhead per agent from Chapter 8. Spinning up five parallel agents to sort five items pays 60,000 tokens of overhead for work a single script could do for free. Match the tool to the task's real size.

## Watching What You Spend: Hooks, Logs, and Dashboards

Optimization only works if you can measure what's actually happening. A **skill usage hook** is a configured callback that records information each time a skill runs, producing data for later analysis. A **stop hook** is a specific kind of callback that fires when an agent finishes a turn, commonly used to record results or perform cleanup — the same mechanism this project's own auto-commit convention relies on. Each event a hook records lands in a **JSONL usage log**: an append-only file with one structured record per line, used to accumulate usage events without rewriting earlier entries.

#### Diagram: From Hook to Dashboard

<iframe src="../../sims/hook-to-dashboard-pipeline/main.html" width="100%" height="392px" scrolling="no"></iframe>

<details markdown="1">
<summary>From Hook to Dashboard</summary>
Type: workflow
**sim-id:** hook-to-dashboard-pipeline<br/>
**Library:** Mermaid<br/>
**Status:** Specified

Bloom Level: Understand (L2)
Bloom Verb: Summarize

Learning objective: Summarize how a single skill-run event travels from a hook, into a log file, and out as a dashboard metric.

Visual style: Left-to-right Mermaid flowchart

Nodes:
1. "Skill Runs" (rounded rectangle)
2. "Skill Usage Hook" (rounded rectangle)
3. "Stop Hook Fires" (rounded rectangle)
4. "JSONL Usage Log (append one line)" (rectangle, styled as a small file icon)
5. "Skill Usage Analytics (Python script)" (rectangle)
6. "Token Usage Dashboard" (rounded rectangle, book's accent color)

Edges:
- Skill Runs --> Skill Usage Hook
- Skill Usage Hook --> Stop Hook Fires
- Stop Hook Fires --> JSONL Usage Log (append one line)
- JSONL Usage Log (append one line) --> Skill Usage Analytics (Python script)
- Skill Usage Analytics (Python script) --> Token Usage Dashboard

Interactivity requirement: every node MUST have a `click` directive opening an infobox with that stage's one-sentence definition, including a note on the Dashboard node that it also reports **elapsed time measurement** (duration) alongside token counts, since the two are recorded separately.

Color scheme: process nodes in the book's teal accent; the log-file node styled distinctly (e.g., a folded-corner file shape) to signal storage rather than computation.

Implementation: Mermaid flowchart with per-node click handlers rendered inside the MicroSim's main.html, opening a shared infobox panel below the diagram.
</details>

!!! mascot-thinking "A log is just data until something reads it."
    ![Kit thinking with a paw on their chin](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    A JSONL file sitting on disk doesn't optimize anything by itself. The insight only shows up once **skill usage analytics** — a script that processes those recorded events to reveal which skills run most often and what each consumes — turns raw log lines into a **token usage dashboard**: a generated report presenting consumption and duration per skill so the expensive steps become visible instead of hidden in a pile of JSON lines.

## Budgeting a Whole Book

Put every technique in this chapter together across an entire project and you get **chapter token budgeting**: allocating a per-chapter allowance for generation so a long book completes without exhausting a usage period's capacity. Storing each chapter's quiz separately — **separate quiz files** — is one concrete instance of the file-layout strategy applied to assessments instead of prose, so revising a quiz never requires reloading the chapter body. From measured per-stage costs, you can produce a **cost per book estimate**: a projection of total consumption for a complete textbook, which is what turns **budget-constrained authoring** — planning a book's production to fit a fixed monthly allowance, choosing techniques by cost as well as quality — from guesswork into planning. All of it together is what **optimizing Claude usage** actually means: arranging work to fit within plan allowances by sequencing, batching, and offloading deterministic steps.

## Key Takeaways

- **Deterministic work offloading**, guided by the **model versus script division** and habits like **grep before read**, is the single biggest token lever available.
- **Quality gate short-circuiting** with a **cached quality score** avoids re-checking what hasn't changed.
- The **glossary token benchmark** (~31,000 tokens for 350 terms) grounds **token cost per term** and **marginal token cost** in measured reality, not guesswork.
- **Token waste antipatterns** — like unnecessary parallel agents — are avoided with a coherent set of **token management strategies**.
- A **skill usage hook** and **stop hook** feed a **JSONL usage log**, which **skill usage analytics** turns into a **token usage dashboard** reporting both cost and **elapsed time**.
- **Chapter token budgeting**, **separate quiz files**, a **cost per book estimate**, and **budget-constrained authoring** are what **optimizing Claude usage** looks like applied to an entire book.

!!! mascot-celebration "You can now measure, not just guess."
    ![Kit celebrating with arms raised](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    You went from "tokens cost something" to "here's exactly how much, and here's the dashboard that proves it." That's the whole discipline. Right tool, right task!

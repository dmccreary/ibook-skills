---
title: Serial Versus Parallel Cost Calculator
description: Use three sliders to calculate the total token cost of a task run by one agent versus one agent per sub-task, and see how startup overhead drives the difference.
image: /sims/serial-versus-parallel-cost-calculator/serial-versus-parallel-cost-calculator.png
og:image: /sims/serial-versus-parallel-cost-calculator/serial-versus-parallel-cost-calculator.png
twitter:image: /sims/serial-versus-parallel-cost-calculator/serial-versus-parallel-cost-calculator.png
social:
   cards: false
quality_score: 100
---

# Serial Versus Parallel Cost Calculator

<iframe src="main.html" height="552px" width="100%" scrolling="no"></iframe>

[Run the Serial Versus Parallel Cost Calculator MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }
<br/>
[Edit in the p5.js Editor](https://editor.p5js.org/)

## About This MicroSim

Every agent pays a fixed **startup overhead** in tokens before it does any
useful work, because it has to receive its own instructions and tool
definitions. **Serial execution** runs one agent for the whole task and pays
that overhead once. **Parallel execution** runs one agent per sub-task and
pays it once per agent.

This calculator shows both totals as stacked bars on one shared scale. Red
blocks are startup overhead. Blue blocks are real work, one block per
sub-task. The blue blocks are identical in both bars. Only the number of red
blocks changes.

| Total | Formula |
|-------|---------|
| Serial | (work tokens × sub-tasks) + (1 × startup overhead) |
| Parallel | (work tokens × sub-tasks) + (sub-tasks × startup overhead) |
| Difference | (sub-tasks − 1) × startup overhead |

The verdict box under the bars reports the difference in tokens and as a
percentage of the serial total. It reads "about the same" when parallel costs
less than 5% more than serial, and it points out that there is no benefit
from parallel when there is only one sub-task.

!!! note "What the model leaves out"
    The calculator counts tokens only. Parallel execution finishes sooner,
    and that saved time is the reason to consider it. The model also ignores
    rate limits, failed agents, and the context an agent reuses when it works
    serially. The default overhead of 12,000 tokens is the rough figure this
    book reports for its own project. Your overhead will differ.

## How to Use

1. Read the default case: 8 sub-tasks, 10,000 tokens of work each, 12,000
   tokens of startup overhead.
2. Drag **Number of sub-tasks** down to 1. The two bars become identical.
3. Drag it back up one step at a time and watch one more red block appear in
   the parallel bar for each added agent.
4. Raise **Tokens of real work per sub-task**. The extra tokens stay the same,
   but the percentage shrinks because the work now dwarfs the overhead.
5. Check **Show formula** to see both totals as live equations.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/serial-versus-parallel-cost-calculator/main.html"
        height="552px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who run this skill
library on a limited token plan and must decide when to use parallel agents.

### Learning Objective

Calculate the total token cost of a task run serially versus in parallel, and
identify the agent-count threshold where parallel execution stops paying off.
(Bloom's Taxonomy: Apply)

### Duration

10-15 minutes

### Prerequisites

- Knows what a token is and that plans limit token use
- Has read the definitions of *sub-agent startup overhead*, *serial agent
  execution*, and *parallel agent execution* in Chapter 8

### Activities

1. **Exploration** (4 min): Move each slider across its full range, one at a
   time. Note which slider changes the extra tokens and which changes only
   the percentage.
2. **Guided Practice** (6 min): Enter the rough figures from Appendix D of this
   book: 6 sub-tasks, 35,000 tokens of work each, and 17,500 tokens of
   overhead per agent. Compare the percentage with the "roughly 38% more"
   that the appendix reports. Then model a 12-chapter book by setting the
   sub-tasks to 12.
3. **Assessment** (4 min): Suppose you will accept parallel execution only if
   it costs no more than 50% extra. With 10,000 tokens of work per sub-task
   and 12,000 tokens of overhead, find the largest number of sub-tasks that
   meets your rule. Then find how large the work per sub-task must be for 8
   sub-tasks to meet it.

### Assessment

- The learner computes both totals by hand for one setting and matches the
  calculator.
- The learner states that the difference is always (sub-tasks − 1) × startup
  overhead and does not depend on the amount of real work.
- The learner sets a tolerance and identifies the agent count at which
  parallel execution exceeds it.

### Discussion Questions

1. In token terms, parallel never costs less than serial. What is it buying?
2. Why does the same extra cost feel small for large sub-tasks and large for
   small ones?
3. What could you change about a workflow to lower the startup overhead
   itself?

## References

1. [Parallel computing](https://en.wikipedia.org/wiki/Parallel_computing) - Wikipedia - General background on dividing work among workers and the overhead that division adds.
2. [Parallel Execution of Tasks](../../chapters/appendix-d-parallel-execution/index.md) - Appendix D of this book - The author's measurements of the token cost of running agents in parallel.
3. [p5.js Reference](https://p5js.org/reference/) - p5.js - Documentation for the library used to build this MicroSim.

---
title: Token Waste Reinforcing Loop
description: Interactive causal loop diagram that contrasts a reinforcing loop (unchecked token waste) with the balancing loop that counteracts it (chapter token budgeting), with a traced change and a minus-sign count for each loop.
image: /sims/token-waste-reinforcing-loop/token-waste-reinforcing-loop.png
og:image: /sims/token-waste-reinforcing-loop/token-waste-reinforcing-loop.png
twitter:image: /sims/token-waste-reinforcing-loop/token-waste-reinforcing-loop.png
social:
   cards: false
quality_score: 100
---

# Token Waste Reinforcing Loop

<iframe src="main.html" height="562px" width="100%" scrolling="no"></iframe>

[Run the Token Waste Reinforcing Loop MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }

## About This MicroSim

A **causal loop diagram** shows how variables influence one another around
closed paths of cause and effect. This one uses the book's own token-waste
example from Chapter 9 to put the two basic loop types side by side.

**Loop R, Token Waste (reinforcing).** More unnecessary parallel agents pay
more startup overhead. More overhead leaves fewer tokens remaining in the
usage window. Fewer remaining tokens raise the pressure to rush, and rushing
launches even more unnecessary agents. The change comes back amplified.

**Loop B, Chapter Token Budgeting (balancing).** The same overhead, once it
pushes a chapter past its allowance, draws more budgeting attention. Budgeting
raises cost awareness, and cost awareness reduces unnecessary parallel agents.
The change comes back reversed.

The two loops share one link, from *Unnecessary Parallel Agents* to *Startup
Overhead Paid*. That shared link is where the two loops work against each
other.

| Link | Sign | Loop |
|------|:----:|:----:|
| Unnecessary Parallel Agents &rarr; Startup Overhead Paid | + | R and B |
| Startup Overhead Paid &rarr; Tokens Remaining in Window | &minus; | R |
| Tokens Remaining in Window &rarr; Pressure to Rush | &minus; | R |
| Pressure to Rush &rarr; Unnecessary Parallel Agents | + | R |
| Startup Overhead Paid &rarr; Chapter Token Budgeting | + | B |
| Chapter Token Budgeting &rarr; Cost Awareness | + | B |
| Cost Awareness &rarr; Unnecessary Parallel Agents | &minus; | B |

A **+** means the two variables move in the same direction. A **&minus;**
means they move in opposite directions. Loop R has two minus signs (an even
number), so it is reinforcing. Loop B has one (an odd number), so it is
balancing.

!!! note "A model, not a measurement"
    The diagram is a qualitative model of cause and effect. The only number
    in it, roughly 12,000 tokens of startup overhead per agent, is the figure
    measured on this project and reported in Chapter 8.

## How to Use

1. Select **R loop**, or click the red **R** circle. The reinforcing loop
   lights up and each variable shows whether it rises or falls when
   *Unnecessary Parallel Agents* rises.
2. Read the traced change in the panel from left to right. Notice that it
   returns to the starting variable pointing the same way it started.
3. Select **B loop**, or click the blue **B** circle. Trace the same starting
   change and notice that this time it returns pointing the opposite way.
4. Count the minus signs on each loop and check the count against the
   "How to tell" line.
5. Hover any variable to read its definition, or any arrow to read the causal
   claim it makes.
6. Drag the background to pan. Use the **&minus;**, **+**, and **Fit** buttons
   to zoom. Pinch also zooms. A normal scroll is left to the page.
7. Select **Show Both** to return to the full diagram.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/token-waste-reinforcing-loop/main.html"
        height="562px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who build intelligent
textbooks with AI agent skills. No prior systems-thinking background is
needed.

### Learning Objective

Differentiate a reinforcing loop from a balancing loop using this book's own
token-waste example from Chapter 9. (Bloom's Taxonomy: Analyze)

### Duration

15 minutes

### Prerequisites

- Knows that each additional agent pays a fixed startup overhead (Chapter 8)
- Has read the token waste antipatterns and chapter token budgeting sections
  of Chapter 9

### Activities

1. **Exploration** (4 min): Hover all six variables and all seven arrows. For
   each arrow, say the causal claim in a full sentence that starts with "The
   more..." or "The fewer...".
2. **Guided Practice** (6 min): Before selecting either loop, predict which
   one is reinforcing by counting minus signs. Then select **R loop** and
   **B loop** and compare the traced change with your prediction.
3. **Assessment** (5 min): Answer the questions below in writing.

### Assessment

- The learner states that a reinforcing loop amplifies a change and a
  balancing loop counteracts it.
- The learner classifies each loop correctly and justifies the answer with the
  even or odd count of minus signs.
- The learner identifies the shared link and explains that it carries the
  effect of both loops.

### Discussion Questions

1. If the link from *Startup Overhead Paid* to *Chapter Token Budgeting* were
   removed, no author would ever notice an overrun. What would be left, and how
   would the system behave?
2. Which single link in loop R would you weaken first, and what practice from
   Chapter 9 weakens it?
3. Name another pair of loops, from any field, with the same shape: a runaway
   habit and the check that restrains it. A pattern that recurs across domains
   like this is a systems archetype.

## References

1. [Causal loop diagram](https://en.wikipedia.org/wiki/Causal_loop_diagram) - Wikipedia - Explains link polarity, reinforcing and balancing loops, and the rule of counting negative links.
2. [System archetype](https://en.wikipedia.org/wiki/System_archetype) - Wikipedia - Describes the recurring patterns of interacting loops that appear across many domains.
3. [Thinking in Systems: A Primer](https://en.wikipedia.org/wiki/Thinking_In_Systems:_A_Primer) - Donella H. Meadows - A readable introduction to stocks, flows, and feedback loops.
4. [vis-network Documentation](https://visjs.github.io/vis-network/docs/network/) - vis.js - Reference for the network library used to draw this diagram.

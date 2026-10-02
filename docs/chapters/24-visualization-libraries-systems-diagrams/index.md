---
title: Visualization Libraries and Systems Diagrams
description: Surveys vis-network, bubble charts, and clickable matrices, causal loop diagrams and systems archetypes, runnable Python labs, and the batch pipeline that scaffolds a chapter's simulations.
generated_by: claude skill chapter-content-generator
date: 2026-08-22 17:50:00
version: 0.09
---

# Visualization Libraries and Systems Diagrams

## Summary

This chapter surveys the MicroSim generator's other visualization families -- Chart.js, Plotly, vis-network, vis-timeline, Leaflet, Mermaid, Venn diagrams, and comparison tables -- alongside Docker-backed runnable Python labs. It introduces causal loop diagrams, reinforcing and balancing loops, and the batch scripts that generate and report on a chapter's diagram coverage. Students will be able to choose the right visualization library for a given concept after this chapter.

## Concepts Covered

This chapter covers the following 19 concepts from the learning graph:

1. Docker Python Lab
2. Sim Scaffolding Workflow
3. vis-network Library
4. Bubble Chart Matrix
5. Clickable Matrix Table
6. Runnable Code Block
7. generate-sim-scaffold.py
8. Causal Loop Diagram
9. Reinforcing Loop
10. Balancing Loop
11. Diagram Coverage Report
12. Batch Sim Generation
13. extract-sim-specs.py Script
14. Educational Metadata Section
15. Systems Archetype
16. Bloom Level to Interaction
17. Sequential Sim Execution
18. diagram-report.py Script
19. Batch Utility Token Savings

## Prerequisites

This chapter builds on concepts from:

- [3. Python Fundamentals for Skill Automation](../03-python-fundamentals-automation/index.md)
- [7. Progressive Disclosure and Meta-Skill Routing](../07-progressive-disclosure-meta-skills/index.md)
- [8. Token Budgets and Usage Limits](../08-token-budgets-usage-limits/index.md)
- [9. Measuring and Optimizing Token Usage](../09-measuring-optimizing-tokens/index.md)
- [13. Bloom's Taxonomy and Instructional Design](../13-blooms-taxonomy-instructional-design/index.md)
- [16. Learning Graph Quality Validation](../16-learning-graph-quality-validation/index.md)
- [18. Chapter Content Quality and Review](../18-chapter-content-quality-review/index.md)
- [21. MicroSim Anatomy and p5.js Basics](../21-microsim-anatomy-p5js-basics/index.md)
- [22. p5.js Controls and MicroSim Quality](../22-p5js-controls-microsim-quality/index.md)
- [23. The MicroSim Generator and Metadata Schema](../23-microsim-generator-metadata-schema/index.md)

---

!!! mascot-welcome "A few more shapes for a few more ideas."
    ![Kit waves hello with their tool satchel](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    Chapter 23 toured most of the MicroSim generator's libraries. This chapter finishes the tour and shows the batch pipeline that turns a whole chapter's diagram requests into finished files at once. Right tool, right task!

## More Visualization Libraries

You've already used the **vis-network library** — a JavaScript library that renders nodes and connecting arrows as an interactive diagram with physics-based layout — in every learning graph viewer throughout this book. Two more specialized formats round out the generator's routing table. A **bubble chart matrix** positions items on two axes with size encoding a third value, used for priority and trade-off comparisons. A **clickable matrix table** is a grid whose cells expand to reveal detailed explanation, used for framework comparisons too dense for a static table.

## Causal Loop Diagrams: Reinforcing and Balancing Loops

Some ideas aren't a hierarchy or a flow — they're a system that feeds back on itself. A **causal loop diagram** is a systems-thinking illustration showing how variables influence one another around closed paths of cause and effect. Two loop shapes recur constantly: a **reinforcing loop** is a closed path of influence in which a change is amplified as it travels around the loop, producing growth or collapse, while a **balancing loop** is a closed path that counteracts change, driving a system toward a stable value instead.

!!! mascot-thinking "One loop grows, the other stabilizes — real systems mix both."
    ![Kit thinking with a paw on their chin](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    Token waste from Chapter 9 is a reinforcing loop left unchecked — small inefficiencies compound across a whole book. Chapter token budgeting is the balancing loop that catches it. Most real systems, including this one's own production pipeline, are a mix of both loop types working against each other.

When the same loop shape shows up across many unrelated domains, it's worth naming: a **systems archetype** is a recurring pattern of interacting loops that appears across many different domains and produces a characteristic behavior, regardless of the specific subject it's describing.

#### Diagram: Token Waste Reinforcing Loop

<iframe src="../../sims/token-waste-reinforcing-loop/main.html" width="100%" height="562px" scrolling="no"></iframe>

<details markdown="1">
<summary>Token Waste Reinforcing Loop</summary>
Type: graph-model
**sim-id:** token-waste-reinforcing-loop<br/>
**Library:** vis-network<br/>
**Status:** Specified

Bloom Level: Analyze (L4)
Bloom Verb: Differentiate

Learning objective: Differentiate a reinforcing loop from a balancing loop using this book's own token-waste example from Chapter 9.

Purpose: Show a concrete reinforcing loop (unchecked token waste compounding) and the balancing loop that counteracts it (chapter token budgeting), as two linked causal loop diagrams.

Node types:
1. Variable nodes (ellipses): "Unnecessary Parallel Agents", "Startup Overhead Paid", "Tokens Remaining in Window", "Chapter Token Budgeting", "Cost Awareness"

Edge types:
1. Reinforcing loop (solid arrows, labeled "R"): Unnecessary Parallel Agents -> Startup Overhead Paid -> (fewer) Tokens Remaining in Window -> pressure to rush -> more Unnecessary Parallel Agents
2. Balancing loop (solid arrows, labeled "B"): Chapter Token Budgeting -> Cost Awareness -> fewer Unnecessary Parallel Agents

Interactive features:
- Hover any node to see its one-sentence definition
- Click the "R" or "B" loop label to highlight that loop's full path and show its net effect (growth/collapse for R, stabilization for B)
- Zoom and pan enabled

Layout: Force-directed, two visually separated loops
Legend: R (reinforcing, red arrows) vs. B (balancing, blue arrows)

Implementation: vis-network JavaScript library, canvas 800x500px
</details>

## Runnable Labs

Not every interactive element in a textbook is a diagram — some are exercises a reader actively edits and runs. A **Docker Python lab** is an interactive exercise in which a reader edits and runs code inside a contained environment directly from a textbook page, and its content is a **runnable code block**: a code sample a reader can execute in place and modify, rather than only read.

## Matching Interaction to Cognitive Demand

Chapter 13 introduced Bloom's levels as a framework for outcomes; the same framework governs interaction design. **Bloom level to interaction** is the principle of matching interaction style to intended cognitive demand, so an activity exercises the level it claims to — a Remember-level flashcard and a Create-level model editor test fundamentally different things, and using the wrong one undersells (or oversells) what a MicroSim actually teaches.

## From Chapter to Simulations: The Batch Pipeline

Turning a chapter full of diagram specification blocks into real files follows a fixed pipeline. **extract-sim-specs.py** reads a chapter and produces a structured list of every simulation it requests, replacing manual parsing of `<details markdown="1">` blocks by hand. From that list, a **sim scaffolding workflow** creates each simulation's directory and placeholder files automatically so only the behavior file requires authoring, performed by **generate-sim-scaffold.py**: the program that creates the standard directory and placeholder files for a simulation from its specification. Doing this for an entire chapter's requested simulations at once is **batch sim generation**: producing all simulations requested by a chapter in one coordinated pass rather than individually.

!!! mascot-warning "Batch generation still runs sequentially by default."
    ![Kit holding up a caution paw](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    It's tempting to assume "batch" means "parallel." It doesn't, by default: **sequential sim execution** generates simulations one after another, since concurrent generation multiplies the ~12,000-token startup overhead from Chapter 8 without improving the actual result. Reach for parallel generation only when each simulation's specification is genuinely large enough to justify the extra cost.

## Educational Metadata and Coverage Reporting

Chapter 23 covered the search and technical metadata sections; the **educational metadata section** is the third piece — the part of a simulation's descriptive record holding grade level, subject, objectives, and targeted cognitive levels, tying every scaffolded MicroSim back to the Bloom's level it was designed to interact at. Once a batch of simulations is generated, **diagram-report.py** compares requested visuals against existing ones and reports coverage per chapter, producing a **diagram coverage report**: a generated summary showing which requested visuals exist, which are missing, and which chapters lack illustration entirely.

!!! mascot-tip "This whole pipeline exists to save tokens, not just time."
    ![Kit holding up a tool with a knowing look](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    **Batch utility token savings** is the reduction in consumption achieved by having programs perform the repetitive parts of simulation production instead of the model — measured on this project at roughly 430,000 tokens saved per chapter run. Extraction, scaffolding, and coverage reporting are all Chapter 3's model-versus-script division, applied at the scale of an entire book's worth of diagrams.

## Key Takeaways

- **vis-network**, **bubble chart matrices**, and **clickable matrix tables** round out the visualization library survey started in Chapter 23.
- **Causal loop diagrams** — built from **reinforcing** and **balancing loops** — model systems, and recurring loop patterns form a **systems archetype**.
- A **Docker Python lab** delivers a **runnable code block**; **Bloom level to interaction** keeps any activity's interaction style honest about what it actually tests.
- **extract-sim-specs.py**, a **sim scaffolding workflow** via **generate-sim-scaffold.py**, and **batch sim generation** turn a chapter's specs into real files — by default through **sequential**, not parallel, execution.
- The **educational metadata section** ties a simulation to its cognitive target; **diagram-report.py** produces a **coverage report**; all of it adds up to real **batch utility token savings**.

!!! mascot-celebration "You now understand the entire MicroSim pipeline, end to end."
    ![Kit celebrating with arms raised](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    From a diagram specification block in a chapter's prose to a scaffolded, validated, deployed simulation — you've now seen every stage of that journey. Right tool, right task!

---
title: The MicroSim Generator and Metadata Schema
description: Explains how the MicroSim generator routes requests across visualization libraries, seeded randomness, the metadata schema, sim lifecycle status, and batch chapter tools.
generated_by: claude skill chapter-content-generator
date: 2026-08-22 17:35:00
version: 0.09
---

# The MicroSim Generator and Metadata Schema

## Summary

This chapter explains how the MicroSim generator routes a request to the right visualization library and introduces seeded randomness for reproducible simulations. It covers the MicroSim metadata schema's search, educational, and technical sections, and the batch Python utilities that scaffold and validate a chapter's worth of simulations at once. Students will be able to write a complete `metadata.json` file for a MicroSim after this chapter.

## Concepts Covered

This chapter covers the following 19 concepts from the learning graph:

1. update-mkdocs-nav.py Script
2. Concept Classifier Sim
3. Batch Screenshot Capture
4. sync-iframe-heights.py
5. MicroSim Generator
6. Seeded Randomness
7. MicroSim Metadata Schema
8. Visualization Library Routing
9. Sim Lifecycle Status
10. Search Metadata Section
11. Technical Metadata Section
12. Ambiguous Term Clarification
13. Chart.js Library
14. Plotly Library
15. vis-timeline Library
16. Leaflet Map Library
17. Mermaid Diagram Syntax
18. Venn Diagram Generator
19. Comparison Table Sim

## Prerequisites

This chapter builds on concepts from:

- [1. Foundations of AI, Language Models, and Prompting](../01-foundations-ai-language-models/index.md)
- [3. Python Fundamentals for Skill Automation](../03-python-fundamentals-automation/index.md)
- [4. Development Tools: Editor, Terminal, and Git Basics](../04-dev-tools-editor-git-basics/index.md)
- [7. Progressive Disclosure and Meta-Skill Routing](../07-progressive-disclosure-meta-skills/index.md)
- [14. Learning Graphs and Concept Enumeration](../14-learning-graphs-concept-enumeration/index.md)
- [15. Learning Graph Data Formats and Taxonomy](../15-learning-graph-formats-taxonomy/index.md)
- [21. MicroSim Anatomy and p5.js Basics](../21-microsim-anatomy-p5js-basics/index.md)
- [22. p5.js Controls and MicroSim Quality](../22-p5js-controls-microsim-quality/index.md)

---

!!! mascot-welcome "One request in, the right library out."
    ![Kit waves hello with their tool satchel](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    You've met p5.js up close. This chapter shows you how a single request gets routed to p5.js, or Chart.js, or six other libraries — and everything that has to be true about a finished MicroSim before it counts as done. Right tool, right task!

#### Diagram: MicroSim Library Routing Table

<iframe src="../../sims/microsim-library-routing-table/main.html" width="100%" height="502px" scrolling="no"></iframe>

<details markdown="1">
<summary>MicroSim Library Routing Table</summary>
Type: workflow
**sim-id:** microsim-library-routing-table<br/>
**Library:** Mermaid<br/>
**Status:** Specified

Bloom Level: Apply (L3)
Bloom Verb: Demonstrate

Learning objective: Demonstrate how a request's keywords route to one of several visualization libraries.

Visual style: Left-to-right Mermaid flowchart

Nodes:
1. "Incoming Request" (rounded rectangle)
2. "MicroSim Generator (Meta-Skill)" (rounded rectangle, book's accent color)
3. Six library nodes fanning out: "p5.js", "Chart.js", "vis-network", "vis-timeline", "Leaflet", "Mermaid" (rounded rectangles)

Edges:
- Incoming Request --> MicroSim Generator
- MicroSim Generator --> each library node, each edge labeled with a matched keyword (e.g., "dates, chronological" -> vis-timeline; "geographic, coordinates" -> Leaflet)

Interactivity requirement: every node MUST have a `click` directive opening an infobox — the request node shows an example request string, the generator node shows its routing job, each library node shows one example MicroSim it's best suited for.

Color scheme: the generator node in the book's teal accent; library nodes in a consistent lighter shade.

Implementation: Mermaid flowchart with per-node click handlers rendered inside the MicroSim's main.html, opening a shared infobox panel below the diagram.
</details>

## The MicroSim Generator: One Meta-Skill, Many Libraries

The **MicroSim generator** is the meta-skill that routes a simulation request to the appropriate specialized guide and produces a complete package of files — a direct application of the meta-skill pattern from Chapter 7, this time routing by visualization type instead of by task category. That routing decision is **visualization library routing**: selecting the rendering technology best matched to a request, based on the kind of data and interaction described.

!!! mascot-thinking "The same routing table pattern, a different domain."
    ![Kit thinking with a paw on their chin](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    Chapter 7's meta-skill routed a request to a reference guide by keyword. This one routes a request to a *rendering library* by the shape of the data — dated events go to a timeline library, geographic data goes to a map library, and so on. Same architecture, applied one level more specifically.

Some requests genuinely could mean more than one thing. **Ambiguous term clarification** resolves request words that could indicate several visualization types before generation begins — "show the relationship" could mean a Venn diagram, a graph model, or a comparison table, and the generator has to ask rather than guess.

## A Tour of the Routed Libraries

Beyond p5.js, the generator routes to several other libraries depending on what's being visualized. The **Chart.js library** produces bar, line, pie, radar, and related plots from structured values. The **Plotly library** is well suited to mathematical functions and scientific charts with interactive axes. The **vis-timeline library** renders dated events along a navigable horizontal axis. The **Leaflet map library** renders interactive geographic maps with markers and layers. **Mermaid diagram syntax** is a text notation for describing flowcharts, sequence diagrams, and state machines that render as diagrams without manual drawing — the same syntax behind every clickable workflow diagram you've seen in this book. Two more routes produce a specific interaction pattern rather than a general chart type: the **Venn diagram generator** produces overlapping-set illustrations showing shared and exclusive membership between categories, and a **comparison table sim** is an interactive table presenting side-by-side attributes with rated values across several options. One more route builds an assessment activity rather than a chart: a **concept classifier sim** is an interactive sorting activity in which a reader assigns scenarios to categories and receives immediate feedback.

| Library / Route | Best For |
|------------------|----------|
| p5.js | Physics, custom animation, general simulation |
| Chart.js | Bar, line, pie, radar charts |
| Plotly | Mathematical functions, scientific data |
| vis-network | Graphs and concept maps |
| vis-timeline | Dated, sequential events |
| Leaflet | Geographic data |
| Mermaid | Flowcharts, sequence diagrams |
| Venn Diagram Generator | Overlapping-set relationships |
| Comparison Table Sim | Side-by-side rated attributes |
| Concept Classifier Sim | Sorting activities with feedback |

## Seeded Randomness

A simulation that uses randomness for placement or variation still needs to behave predictably for testing and grading. **Seeded randomness** means generating apparently random values from a fixed starting number so a simulation produces identical results each time it runs — the same conceptual pairing as Chapter 3's deterministic computation, applied to a process that looks random on the surface.

!!! mascot-tip "Random-looking is fine. Actually unpredictable is not."
    ![Kit holding up a tool with a knowing look](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    Use `randomSeed(42)` (or an equivalent fixed seed) in any MicroSim where reproducibility matters. Grading, screenshots, and bug reports all get much harder when random output means something different every single time.

## The MicroSim Metadata Schema

Every MicroSim's `metadata.json` conforms to the **MicroSim metadata schema**: the formal description of required descriptive fields for a simulation, enabling automated cataloging and validation. Two of its sections matter for discovery specifically. The **search metadata section** holds tags, visualization type, and keywords that support discovery — exactly the fields the reuse-search catalog you've watched this book search throughout Chapters 4 through 22 is built from. The **technical metadata section** holds framework, dimensions, dependencies, and accessibility information — the `library`, `canvasDimensions`, and related fields a scaffolding script reads to know what to generate.

## Sim Lifecycle Status

A MicroSim doesn't go from idea to finished file in one step. **Sim lifecycle status** is the recorded stage of a simulation's production, progressing from specified through scaffolded, implemented, validated, and deployed. You've seen this field directly, over and over: every `<details markdown="1">` block in this book carries a **Status** field, either `Specified` for a new request awaiting generation, or `Reused` — a terminal state, skipping the rest of the lifecycle entirely, for a MicroSim already deployed somewhere in this book's own catalog and simply embedded again.

## Batch Tools for a Whole Chapter

Finishing a chapter's worth of MicroSims at once relies on the same batch-Python philosophy from Chapter 9. **sync-iframe-heights.py** reads each simulation's recorded `CANVAS_HEIGHT` and updates every embedding frame to match, across an entire chapter in one pass. **Batch screenshot capture** generates preview images for many simulations in one automated pass, instead of one MicroSim-utils invocation at a time. Once new pages exist, **update-mkdocs-nav.py** inserts them into the site menu, ensuring generated content is actually reachable.

!!! mascot-warning "A scaffolded MicroSim with no nav entry is still invisible."
    ![Kit holding up a caution paw](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    This is Chapter 18's navigation-entry warning again, in a new context: a batch of freshly scaffolded MicroSims will build without error and simply never appear in the sidebar if `update-mkdocs-nav.py` isn't run afterward. Batch generation and batch navigation updates go together.

## Key Takeaways

- The **MicroSim generator** performs **visualization library routing**, resolving genuinely **ambiguous terms** before it commits to a library.
- Beyond p5.js, requests route to **Chart.js**, **Plotly**, **vis-timeline**, **Leaflet**, **Mermaid**, a **Venn diagram generator**, a **comparison table sim**, or a **concept classifier sim**, depending on the data and interaction described.
- **Seeded randomness** keeps a simulation reproducible even when it looks random.
- The **MicroSim metadata schema**'s **search** and **technical** sections drive discovery and generation; **sim lifecycle status** tracks a simulation from `Specified` through `Deployed` — or straight to a terminal `Reused`.
- **sync-iframe-heights.py**, **batch screenshot capture**, and **update-mkdocs-nav.py** finish a whole chapter's worth of simulations in three automated passes.

!!! mascot-celebration "You now understand the tool that built half of this book's diagrams."
    ![Kit celebrating with arms raised](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    Every reused MicroSim you've clicked through this book — the graph viewer, the cycle detector, the taxonomy pie chart — passed through exactly this routing, schema, and lifecycle system. Right tool, right task!

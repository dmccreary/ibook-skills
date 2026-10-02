---
title: "Domain-Specific Skill Extension: Electronics Case Study"
description: Covers deciding when a subject needs its own skill, an electronics case study generating circuit schematics and breadboard simulations, and rubric-driven hands-on lab evaluation.
generated_by: claude skill chapter-content-generator
date: 2026-08-22 18:50:00
version: 0.09
---

# Domain-Specific Skill Extension: Electronics Case Study

## Summary

This chapter covers deciding when a subject needs its own skill, using a beginning-electronics case study: generating circuit schematics with Schemdraw, simulating a solderless breadboard with animated current flow, and digital circuit simulation. It closes with rubric-driven lab evaluation, frontmatter quality scores, and automated work-item filing for gaps the rubric finds. Students will be able to evaluate whether a new subject warrants a project-specific skill after this chapter.

## Concepts Covered

This chapter covers the following 23 concepts from the learning graph:

1. Domain-Specific Skill
2. Core Versus Domain Skills
3. Domain Skill Standards
4. Circuit Schematic Generation
5. Solderless Breadboard
6. Domain Vocabulary Gap
7. Schemdraw Library
8. Breadboard Tie Points
9. Hands-On Lab Design
10. Prose to Circuit Translation
11. Component Placement
12. Lab Rubric Scoring
13. Parts Kit Buildability
14. Domain Skill Case Study
15. Project-Local Skill Directory
16. Schematic Verification
17. Jumper Wire Routing
18. Frontmatter Quality Score
19. Automated Work Item Filing
20. Animated Current Flow
21. TODO Backlog Generation
22. Digital Circuit Simulation
23. Voltage and Current Scope

## Prerequisites

This chapter builds on concepts from:

- [1. Foundations of AI, Language Models, and Prompting](../01-foundations-ai-language-models/index.md)
- [2. AI Coding Agents and the Five Levels of Textbook Intelligence](../02-ai-agents-textbook-intelligence/index.md)
- [3. Python Fundamentals for Skill Automation](../03-python-fundamentals-automation/index.md)
- [6. Agent Skill Fundamentals](../06-agent-skill-fundamentals/index.md)
- [7. Progressive Disclosure and Meta-Skill Routing](../07-progressive-disclosure-meta-skills/index.md)
- [11. Distributing Skills and Building Commands](../11-distributing-skills-commands/index.md)
- [12. Writing a Course Description](../12-writing-course-description/index.md)
- [13. Bloom's Taxonomy and Instructional Design](../13-blooms-taxonomy-instructional-design/index.md)
- [21. MicroSim Anatomy and p5.js Basics](../21-microsim-anatomy-p5js-basics/index.md)
- [25. Text-to-Image Models and the Verified Infographic Pipeline](../25-verified-infographic-pipeline/index.md)

---

!!! mascot-welcome "Time to leave the core library behind — on purpose."
    ![Kit waves hello with their tool satchel](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    Everything so far has been subject-neutral. This chapter is a worked example of what happens when a subject needs vocabulary the core library simply doesn't have. Right tool, right task!

## When a Subject Needs Its Own Skill

Most of this library works for any subject; some subjects need more. A **domain-specific skill** is a skill encoding knowledge particular to one subject area, used where general-purpose skills lack the necessary vocabulary or conventions. That's **core versus domain skills**: the distinction between subject-neutral skills usable by any book and specialized skills meaningful only within one field.

!!! mascot-thinking "The gap tells you when it's time."
    ![Kit thinking with a paw on their chin](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    A **domain vocabulary gap** is the shortfall that appears when a general skill lacks the terms, conventions, and correctness rules a specific subject requires — no general MicroSim generator skill knows what a breadboard tie point is. That specific gap is the signal that a domain deserves its own skill, not a vague sense that "electronics feels different."

## Keeping Domain Skills to the Same Standard

A domain skill isn't exempt from the rules the rest of this library follows. **Domain skill standards** require that a specialized skill follow the same structure, description quality, and validation practices as the shared library — everything from Chapter 6's frontmatter contract onward still applies. It lives in a **project-local skill directory**: a folder inside a single book holding skills that apply only to that book, the same project-specific installation scope from Chapter 11.

## Case Study: Circuit Schematics from Prose

This book's own **domain skill case study** — a worked example showing how a general library was extended for one subject, used as a pattern for other fields — is a beginning-electronics textbook. Its first extension is **circuit schematic generation**: producing a standard electrical diagram from a description, as a maintainable program plus a rendered picture, built on the **Schemdraw library**: a Python library that draws electrical schematics from code, so a diagram remains editable and version-controlled rather than a static image nobody can safely modify. Producing one starts with **prose to circuit translation**: interpreting a plain-language description of a circuit and expressing it as an explicit component and connection list, and finishes with **schematic verification**: confirming that the rendered diagram actually matches the circuit that was described.

## Simulating a Breadboard

The second extension simulates hands-on assembly. A **solderless breadboard** is a reusable board with gridded holes that hold components and wires, allowing circuits to be assembled without permanent joins. Those holes are **breadboard tie points**: individual holes internally connected in rows and columns that determine which parts share a connection — get the tie points wrong and two components that look adjacent on the board are actually electrically unrelated. Simulating one requires accurate **component placement**: positioning parts into specific holes so their connections match the intended circuit, and **jumper wire routing**: choosing paths for connecting wires so a circuit is both correct and readable to someone rebuilding it by hand.

!!! mascot-tip "Adjacent on the board doesn't mean connected."
    ![Kit holding up a tool with a knowing look](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    This is the single most common beginner mistake with a real breadboard, and it's exactly what a tie-point-accurate simulation teaches safely before a learner ever touches actual hardware: two holes that look close together can be on entirely different internal rows.

#### Diagram: Breadboard Tie Points and Animated Current Flow

<iframe src="../../sims/breadboard-tie-points-current-flow/main.html" width="100%" height="522px" scrolling="no"></iframe>

<details markdown="1">
<summary>Breadboard Tie Points and Animated Current Flow</summary>
Type: microsim
**sim-id:** breadboard-tie-points-current-flow<br/>
**Library:** p5.js<br/>
**Status:** Specified

Bloom Level: Apply (L3)
Bloom Verb: Demonstrate

Learning objective: Demonstrate which breadboard holes are electrically connected, and how current flows once a simple LED circuit is completed.

Canvas layout:
- A simplified breadboard grid (two power rails top and bottom, a central component area split into two halves by the center gap)
- A battery, an LED, and a resistor pre-placed into example tie points, with jumper wires connecting them

Interactive controls:
- Click any hole to highlight every other hole internally connected to it (its full row or rail)
- Button: "Complete the Circuit" — connects the final jumper wire
- Button: "Reset"

Behavior:
- Clicking a hole highlights its entire internally-connected group in one color, with a label reading "Same tie point group" — clicking an adjacent-but-unconnected hole shows no highlight, reinforcing the tip above
- Clicking "Complete the Circuit" animates small moving dots along the wire path from the battery through the resistor and LED and back, and the LED glows once current reaches it
- If the circuit is left incomplete, no animation plays and an infobox explains which connection is missing

Instructional Rationale: An Apply-level demonstrate objective fits a direct-manipulation simulation where the learner completes the circuit themselves and observes the consequence (the LED lighting), rather than only watching a pre-animated video.

Implementation notes: Use p5.js; model tie points as a simple 2D array grouped by row; animate current as particles moving along a precomputed wire path once the circuit is complete.
</details>

Once components are placed correctly, **animated current flow** makes the circuit's behavior visible: a moving visual indication of charge traveling through a circuit, making an otherwise invisible process observable. For circuits whose signals switch between discrete states rather than varying continuously, **digital circuit simulation** models that switching behavior so a reader can observe it without building hardware, often alongside a **voltage and current scope**: a display panel plotting electrical quantities over time alongside the simulated circuit.

## Designing and Scoring a Hands-On Lab

A domain extension isn't complete without an activity a learner can actually do. **Hands-on lab design** means constructing a practical activity a learner can complete independently with a defined set of parts.

!!! mascot-warning "A lab that needs parts nobody can afford isn't hands-on."
    ![Kit holding up a caution paw](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    **Parts kit buildability** is the requirement that a practical activity be completable with an affordable, specified set of components. A beautifully designed lab that secretly requires a $200 specialty part isn't a hands-on activity — it's a demonstration only the instructor can run.

Assessing the result against explicit criteria, rather than general impression, is **lab rubric scoring**: this project's own electronics extension uses a 103-point rubric covering reader age appropriateness and parts-kit buildability together.

## Closing the Loop: Quality Scores and Work Items

A lab's rubric score doesn't just sit in a report — it gets written directly into the page it describes. A **frontmatter quality score** is an assessment value written into a page's metadata block so its standing is visible to both tooling and authors, the same YAML frontmatter mechanism from Chapter 6 carrying a number instead of a name or license. When that score reveals a gap, **automated work item filing** records each identified shortfall as a tracked task at the moment it's found, rather than relying on memory to come back to it later. Across a whole project, that adds up to **TODO backlog generation**: producing a consolidated list of outstanding work items across a project from automated assessments — a domain skill's own quality gate, generating its own punch list.

## Key Takeaways

- A **domain-specific skill** fills a **domain vocabulary gap** that **core skills** can't; it still follows the same **domain skill standards** and lives in a **project-local skill directory**.
- This book's own **domain skill case study**: **circuit schematic generation** via the **Schemdraw library**, through **prose to circuit translation** and **schematic verification**.
- A simulated **solderless breadboard**, with accurate **tie points**, **component placement**, and **jumper wire routing**, supports **animated current flow**, **digital circuit simulation**, and a **voltage and current scope**.
- **Hands-on lab design** requires **parts kit buildability** and **lab rubric scoring** against explicit criteria.
- A **frontmatter quality score**, backed by **automated work item filing**, feeds a project-wide **TODO backlog**.

!!! mascot-celebration "You now know exactly when to build a new domain skill of your own."
    ![Kit celebrating with arms raised](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    Vocabulary gap identified, standards respected, a rubric-scored lab that's actually buildable — that's the complete pattern for extending this library into any subject it doesn't already know. Right tool, right task!

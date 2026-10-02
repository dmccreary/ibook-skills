---
title: Progressive Disclosure and Meta-Skill Routing
description: Explains the three progressive-disclosure loading budgets, trigger matching, and how meta-skills and routing tables keep a large skill library under the thirty-skill limit.
generated_by: claude skill chapter-content-generator
date: 2026-08-22 13:35:00
version: 0.09
---

# Progressive Disclosure and Meta-Skill Routing

## Summary

This chapter explains progressive disclosure and its three loading budgets -- metadata, body, and reference -- along with how trigger matching selects which skill to load. It introduces meta-skills, routing tables, and skill consolidation as the pattern that keeps a large library under the thirty-skill loading limit. Students will be able to design a meta-skill's routing table for a set of related sub-skills after this chapter.

## Concepts Covered

This chapter covers the following 22 concepts from the learning graph:

1. Skill Trigger Matching
2. Opus Versus Sonnet Routing
3. Skill Naming Conventions
4. Supporting Assets in Skills
5. Template Files in Skills
6. Python Scripts in Skills
7. Metadata Loading Budget
8. Body Loading Budget
9. Reference Loading Budget
10. Trigger Keyword Table
11. False Trigger Misfire
12. Skill Discoverability
13. Meta-Skill
14. Thirty Skill Loading Limit
15. Skill Routing Table
16. On-Demand Guide Loading
17. Skill Consolidation
18. Archived Skill
19. Reference Docs in Skills
20. Skill Library
21. Skill Alias Map
22. Skill Library Maintenance

## Prerequisites

This chapter builds on concepts from:

- [1. Foundations of AI, Language Models, and Prompting](../01-foundations-ai-language-models/index.md)
- [3. Python Fundamentals for Skill Automation](../03-python-fundamentals-automation/index.md)
- [6. Agent Skill Fundamentals](../06-agent-skill-fundamentals/index.md)

---

!!! mascot-welcome "Time to scale up the toolbox."
    ![Kit waves hello with their tool satchel](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    One skill is easy to manage — a library of dozens is not, unless you organize it deliberately. This chapter is how you keep a huge toolbox usable instead of overwhelming. Right tool, right task!

## Three Budgets of Progressive Disclosure

Chapter 6 introduced progressive disclosure as three nested layers. Each layer actually costs tokens at a different point in a session, which is why they're better understood as three separate budgets. The **metadata loading budget** is the cost of the always-resident summary for every installed skill — paid on every single request, which is exactly why a skill's description has to stay short. The **body loading budget** is the cost of reading a skill's full instruction file, paid once that specific skill is triggered. The **reference loading budget** is the cost of opening one specific detailed guide, paid only for the one guide a task actually needs — not the other 98 guides sitting untouched in the library.

| Budget | Paid When | Cost Behavior |
|--------|-----------|-----------------|
| Metadata | Every request, for every installed skill | Must stay small — multiplies by skill count |
| Body | Once, when a skill is triggered | Paid only by requests that use that skill |
| Reference | Once, when a specific guide is opened | Paid only by the one guide a task needs |

## How an Agent Picks a Skill: Trigger Matching

**Skill trigger matching** is the process by which an agent compares an incoming request against every installed skill's description to decide which skill to load. This is entirely a metadata-budget operation — it happens before any skill's body is ever read. That makes **skill discoverability** almost entirely a function of description quality: the degree to which an agent can determine that a relevant skill exists, governed by how well its description anticipates the phrases a real request would use.

!!! mascot-warning "A description that's too broad backfires."
    ![Kit holding up a caution paw](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    A **false trigger misfire** is a routing error in which a skill activates for a request it doesn't actually handle, usually caused by an overly broad description. Writing "handles all documentation tasks" sounds helpful but will misfire on requests that belong to a completely different skill. Be specific about what a skill does and, just as importantly, what it doesn't.

For a meta-skill routing among several guides internally, that matching gets formalized as a **trigger keyword table**: an explicit mapping from request phrases to the action or guide that should handle them, making routing decisions predictable rather than left to guesswork.

## The Thirty-Skill Loading Limit

There's a practical ceiling on how much metadata budget a session can spend before it becomes wasteful: the **thirty skill loading limit**, the practical ceiling on how many skills an agent can keep available at once, which forces related skills to be consolidated rather than installed one by one forever. This book's own library would need dozens of standalone skills without a strategy for staying under that number — which is exactly the problem meta-skills solve.

## Meta-Skills: One Router, Many Guides

A **meta-skill** is a skill whose primary job is to route a request to one of several detailed guides rather than to perform the task itself. Inside it lives a **skill routing table**: the decision table that maps trigger keywords to the guide file responsible for each variant of a task. Once a match is found, the meta-skill performs **on-demand guide loading**: reading that one detailed instruction file only at the moment the matching task begins, rather than keeping every guide resident the whole session.

#### Diagram: Meta-Skill Routing Table

<iframe src="../../sims/meta-skill-routing-table/main.html" width="100%" height="552px" scrolling="no"></iframe>

<details markdown="1">
<summary>Meta-Skill Routing Table</summary>
Type: workflow
**sim-id:** meta-skill-routing-table<br/>
**Library:** Mermaid<br/>
**Status:** Specified

Bloom Level: Apply (L3)
Bloom Verb: Demonstrate

Learning objective: Demonstrate how a meta-skill's routing table matches a request's trigger keywords to exactly one on-demand guide.

Visual style: Left-to-right Mermaid flowchart

Nodes:
1. "Incoming Request" (rounded rectangle)
2. "microsim-generator (Meta-Skill)" (rounded rectangle, book's accent color)
3. "Trigger Keyword Table" (rectangle, styled as a small table)
4. Five guide nodes fanning out: "p5.js Guide", "Chart.js Guide", "vis-network Guide", "Mermaid Guide", "Timeline Guide" (rounded rectangles)

Edges:
- Incoming Request --> microsim-generator (Meta-Skill)
- microsim-generator (Meta-Skill) --> Trigger Keyword Table
- Trigger Keyword Table --> each of the five guide nodes, each edge labeled with the keyword that routes there (e.g., "p5, simulation, interactive canvas" -> p5.js Guide)

Interactivity requirement: every node MUST have a `click` directive opening an infobox — the request node shows an example request string, the meta-skill node shows its one-sentence job description, each guide node shows what kind of MicroSim it produces.

Color scheme: the meta-skill node in the book's teal accent; the five guide nodes in a consistent lighter shade so they read as siblings; matched-edge highlighting on click.

Implementation: Mermaid flowchart with per-node click handlers rendered inside the MicroSim's main.html, opening a shared infobox panel below the diagram.
</details>

Building a meta-skill usually means **skill consolidation**: merging several related skills into one router plus a set of guides, reducing the number of installed skills without losing any capability. The original standalone skill doesn't vanish — it becomes an **archived skill**: retained for reference after its content was folded into the meta-skill, but no longer loaded by the agent. So that old references still resolve, a **skill alias map** records which former skill names now correspond to which route inside the consolidated skill.

!!! mascot-thinking "Consolidation trades skill count for guide count."
    ![Kit thinking with a paw on their chin](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    Here's the shift in mental model: consolidating doesn't shrink your capability, it just moves most of it from "always resident" to "loaded on demand." Forty standalone skills at 40 metadata-budget entries becomes 5 meta-skills at 5 metadata-budget entries — same 40 capabilities, one-eighth the always-on cost.

## Naming, Assets, and Templates Inside a Skill

A few more conventions round out what lives inside a well-formed skill. **Skill naming conventions** are the rules governing skill identifiers: lowercase, hyphen-separated, descriptive, and identical to the containing folder name — a rule that keeps a skill discoverable and unambiguous. **Supporting assets in skills** are non-instruction files bundled with a skill, such as schemas, stylesheets, or starter templates, that its workflow copies or reads. Among those, **template files in skills** are prewritten starter files a skill copies into a project and then customizes, avoiding regeneration of boilerplate the model would otherwise have to write from scratch every time. **Python scripts in skills** are programs bundled with a skill that perform its deterministic steps, keeping that work out of the model's output — exactly the division of labor from Chapter 3. **Reference docs in skills** are detailed instructional documents stored alongside a skill and read selectively, allowing real depth without a permanent loading cost.

## Choosing a Model: Opus Versus Sonnet Routing

Progressive disclosure controls how much a skill costs to load; **Opus versus Sonnet routing** controls how much it costs to *run* — the specific choice between a high-capability model and a faster, cheaper one, traded off against task difficulty and cost. A skill that designs an entire book's chapter structure benefits from a stronger model's reasoning; a skill that reformats a CSV file doesn't need it.

!!! mascot-tip "Match the model to the judgment required, not the file size."
    ![Kit holding up a tool with a knowing look](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    A long but mechanical task (renaming 300 files) doesn't need a stronger model just because it touches a lot of files. A short but ambiguous task (designing a chapter order that respects 1,137 dependency edges) does. Route on judgment required, not on task length.

## The Skill Library and Keeping It Healthy

All of this — skills, meta-skills, guides, archives — together makes up a **skill library**: the complete collection of skills available to an agent, together with the conventions that keep them consistent. A library isn't a one-time deliverable; it needs **skill library maintenance**: the ongoing work of updating, testing, and pruning a collection of skills so they remain accurate as tools and standards change.

## Key Takeaways

- Progressive disclosure has three separate costs: the **metadata**, **body**, and **reference loading budgets**, each paid at a different point in a session.
- **Trigger matching** and **skill discoverability** depend entirely on description quality; an overly broad one causes a **false trigger misfire**.
- The **thirty skill loading limit** forces **skill consolidation** into **meta-skills**, each with its own **routing table** and **on-demand guide loading**.
- Consolidated skills become **archived**, tracked by a **skill alias map** so old references still resolve.
- **Naming conventions**, **supporting assets**, **templates**, **Python scripts**, and **reference docs** round out a skill's contents; **model routing** and ongoing **library maintenance** keep the whole thing efficient and accurate.

!!! mascot-celebration "You could design this library's next meta-skill."
    ![Kit celebrating with arms raised](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    You now understand exactly why this book has 14 skills instead of 40 — and you could sketch the routing table for the next one yourself. Right tool, right task!

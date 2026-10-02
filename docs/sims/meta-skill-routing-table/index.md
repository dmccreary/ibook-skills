---
title: Meta-Skill Routing Table
description: Type a request and watch the microsim-generator meta-skill match its trigger keywords to exactly one on-demand guide.
image: /sims/meta-skill-routing-table/meta-skill-routing-table.png
og:image: /sims/meta-skill-routing-table/meta-skill-routing-table.png
twitter:image: /sims/meta-skill-routing-table/meta-skill-routing-table.png
social:
   cards: false
quality_score: 100
---

# Meta-Skill Routing Table

<iframe src="main.html" height="552px" width="100%" scrolling="no"></iframe>

[Run the Meta-Skill Routing Table MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }

## About This MicroSim

A **meta-skill** does not do the task itself. Its job is to route a request to
one of several detailed guides and load only that guide. This left-to-right
flowchart follows one request through the `microsim-generator` meta-skill:

1. An **Incoming Request** reaches the **microsim-generator (Meta-Skill)**.
2. The meta-skill consults its **Trigger Keyword Table**.
3. The table fans out to five guides. Each edge is labeled with keywords that
   route there.

Type a request in the box and select **Route**. The MicroSim looks for trigger
keywords in your text, highlights the matching route in the diagram, dims the
four guides that are not loaded, and marks the matching row of the table below.

| Guide | Example trigger keywords | Produces |
|-------|--------------------------|----------|
| p5.js Guide | simulation, physics, interactive | Custom simulations and animations |
| Chart.js Guide | chart, bar, pie | Standard data charts |
| vis-network Guide | network, nodes, edges | Network graphs and concept maps |
| Mermaid Guide | flowchart, workflow | Flowcharts and process diagrams |
| Timeline Guide | timeline, dates, events | Chronological displays |

!!! note "A five-guide excerpt with simplified matching"
    The keywords are the real trigger keywords for these five guides in the
    `microsim-generator` skill. The full skill routes among more guides than
    the five shown here. The MicroSim picks the guide with the most keyword
    matches, which is a simplification. The real meta-skill is read by a
    language model, which weighs the whole request rather than counting words.

## How to Use

1. The first example is already routed. Find the highlighted path and the
   highlighted table row.
2. Pick another request from the **Examples** list and compare which keywords
   matched.
3. Pick *Create a graph of our sales data*. Two rows match equally, so the
   request is ambiguous. Read what the real meta-skill does in that case.
4. Type your own request and select **Route** (or press Enter). Try one with
   no trigger keyword at all.
5. Click any box in the diagram for its definition. Clicking a guide
   highlights the edge and table row that lead to it.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/meta-skill-routing-table/main.html"
        height="552px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who use this skill
library and want to understand how one skill can stand in for many.

### Learning Objective

Demonstrate how a meta-skill's routing table matches a request's trigger
keywords to exactly one on-demand guide. (Bloom's Taxonomy: Apply)

### Duration

10 minutes

### Prerequisites

- Knows what a skill is and how an agent chooses one from its description
- Has read the definitions of *meta-skill*, *skill routing table*, and
  *on-demand guide loading* in Chapter 7

### Activities

1. **Exploration** (3 min): Route all six example requests. For each, name the
   guide that loads and the keywords that caused it.
2. **Guided Practice** (4 min): Write one new request for each of the five
   guides without reusing the example wording. Route each one and check that
   it lands where you intended.
3. **Assessment** (3 min): Rewrite the ambiguous request *Create a graph of our
   sales data* two ways: once so it routes to the Chart.js Guide, and once so
   it routes to the vis-network Guide. Explain what you changed.

### Assessment

- The learner predicts the guide a request will load before routing it.
- The learner states that only the matched guide is loaded and the others
  cost nothing for that request.
- The learner resolves an ambiguous request by adding a more specific trigger
  keyword.

### Discussion Questions

1. Why is it cheaper to keep five guides behind one meta-skill than to install
   five separate skills?
2. What goes wrong if two rows of a routing table share the same keyword?
3. How would you choose trigger keywords for a new guide?

## References

1. [Flowcharts Syntax](https://mermaid.js.org/syntax/flowchart.html) - Mermaid - Documentation for the flowchart syntax and the `click` interaction used in this MicroSim.
2. [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) - Anthropic - Vendor documentation on skills and on loading instructions only when they are needed.
3. [Routing table](https://en.wikipedia.org/wiki/Routing_table) - Wikipedia - The networking idea the term borrows from: a lookup table that sends each item to one destination.

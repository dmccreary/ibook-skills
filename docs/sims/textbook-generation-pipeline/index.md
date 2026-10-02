---
title: Textbook Generation Pipeline
description: Step through the ordered stages that turn a course description into a published textbook, and see where the two quality gates send work back.
image: /sims/textbook-generation-pipeline/textbook-generation-pipeline.png
og:image: /sims/textbook-generation-pipeline/textbook-generation-pipeline.png
twitter:image: /sims/textbook-generation-pipeline/textbook-generation-pipeline.png
social:
   cards: false
quality_score: 100
---

# Textbook Generation Pipeline

<iframe src="main.html" height="377px" width="100%" scrolling="no"></iframe>

[Run the Textbook Generation Pipeline MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }

## About This MicroSim

The **textbook generation pipeline** is the ordered sequence of steps that
turns a course description into a published book. This left-to-right flowchart
shows six stages (teal boxes) and two **quality gates** (amber diamonds). A
quality gate is a defined check that output must pass before the next stage
begins. Each gate has a dashed red "No" branch that sends the work back to the
stage before it.

| Step | Box | Performed by |
|-----:|-----|--------------|
| 1 | Course Description | `course-description-analyzer` skill |
| 2 | Learning Graph | `learning-graph-generator` skill |
| 3 | Quality Gate: Graph Valid? | `analyze-graph.py` in the `learning-graph-generator` skill |
| 4 | Chapter Structure | `book-chapter-generator` skill |
| 5 | Chapter Content | `chapter-content-generator` skill |
| 6 | Quality Gate: Concepts Covered? | `chapter-content-generator` skill |
| 7 | Media and MicroSims | `microsim-generator` and `book-media-generator` skills |
| 8 | Deployment | `mkdocs gh-deploy` command |

Clicking a box fills the panel below the diagram with that step's
one-sentence definition and the skill that performs it. Where a person
reviews the output before the pipeline moves on, the panel says so.

This diagram is a simplified view. The full pipeline also produces a
glossary, FAQ, quizzes, and references. The
[Book Build Workflow](../book-build-workflow/index.md) MicroSim shows those
supporting steps.

## How to Use

1. Select **Next** to walk through the eight steps in order. The selected box
   gets a dark outline and the counter shows your position.
2. Select **Previous** to go back one step.
3. Click any box in the diagram to jump straight to it.
4. At each amber diamond, read the **If the check fails** line and trace the
   dashed red arrow back to the stage that has to be redone.
5. Keyboard users can press Tab to move between boxes and Enter to select one.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/textbook-generation-pipeline/main.html"
        height="377px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who are about to build
their first intelligent textbook with this skill library.

### Learning Objective

Summarize the ordered stages of the textbook generation pipeline and where
human review and quality gates sit within it. (Bloom's Taxonomy: Understand)

### Duration

10 minutes

### Prerequisites

- Has read the definitions of *agentic workflow*, *human in the loop*, and
  *quality gate* in Chapter 2
- Knows what a learning graph is at a high level

### Activities

1. **Exploration** (3 min): Use **Next** to step through all eight boxes. Say
   each step's output aloud before reading the panel.
2. **Guided Practice** (4 min): Close the MicroSim and write the six stages in
   order from memory, then mark where the two quality gates go. Reopen the
   MicroSim to check.
3. **Assessment** (3 min): Explain why the "Graph Valid?" gate sits before
   Chapter Structure rather than after Chapter Content.

### Assessment

- The learner lists the six stages in the correct order.
- The learner places both quality gates correctly and names the stage each
  one loops back to.
- The learner explains that a defect caught at a gate is cheaper to fix than
  the same defect found after later stages have been built on it.

### Discussion Questions

1. What would it cost to discover a cycle in the learning graph after every
   chapter had been written?
2. Which steps have a person reviewing the output, and why those steps?

## References

1. [Flowcharts Syntax](https://mermaid.js.org/syntax/flowchart.html) - Mermaid - Documentation for the flowchart syntax and the `click` interaction used in this MicroSim.
2. [Directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph) - Wikipedia - The structure a learning graph must have to pass the first quality gate.
3. [Deploying your docs](https://www.mkdocs.org/user-guide/deploying-your-docs/) - MkDocs - How `mkdocs gh-deploy` publishes a site to GitHub Pages, the last step in the pipeline.

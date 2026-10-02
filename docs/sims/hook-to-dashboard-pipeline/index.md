---
title: From Hook to Dashboard
description: Step-through flowchart that follows one skill-run event from a hook, into an append-only JSONL log, through an analytics script, and out as a row of a token usage dashboard.
image: /sims/hook-to-dashboard-pipeline/hook-to-dashboard-pipeline.png
og:image: /sims/hook-to-dashboard-pipeline/hook-to-dashboard-pipeline.png
twitter:image: /sims/hook-to-dashboard-pipeline/hook-to-dashboard-pipeline.png
social:
   cards: false
quality_score: 100
---

# From Hook to Dashboard

<iframe src="main.html" height="392px" width="100%" scrolling="no"></iframe>

[Run the From Hook to Dashboard MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }

## About This MicroSim

You cannot optimize token use that you cannot see. This left-to-right
flowchart follows **one** skill-run event through the six stages that turn it
from something invisible into a number on a report:

1. **Skill Runs**: an agent runs a skill. Nothing is recorded yet.
2. **Skill Usage Hook**: a configured callback notes which skill started and
   when.
3. **Stop Hook Fires**: when the agent finishes, the result is recorded: how
   long the run took and what it consumed.
4. **JSONL Usage Log**: the event is appended as one line to a log file.
   Earlier lines are never rewritten.
5. **Skill Usage Analytics**: a Python script reads the log and groups the
   lines by skill.
6. **Token Usage Dashboard**: the grouped result becomes one row of a report
   that shows both tokens and elapsed time.

The panel below the diagram shows the glossary definition of the selected
stage and, on the right, what the example event *looks like* at that stage:
a skill name, a start record, an end record, a JSON line, a grouped total,
and finally a dashboard row.

| Box | Shape and color | Meaning |
|-----|-----------------|---------|
| Skill Runs, Skill Usage Hook, Stop Hook Fires, Skill Usage Analytics | Light teal | A process: something runs |
| JSONL Usage Log | Cream sheet with a folded corner | A stored file: nothing is computed here |
| Token Usage Dashboard | Dark teal | The report a person reads |

!!! note "The numbers are examples"
    The skill name, timestamps, 154 seconds, 84,200 tokens, and the five-run
    totals are the example values from this library's skill tracker
    documentation. They are not measurements of your project. The diagram
    follows the chapter's simplified chain; the skill tracker installed by the
    `book-installer` skill registers its hooks on the start and end of each
    skill call.

## How to Use

1. Select **Next** to move the example event one stage to the right. Stages
   the event has not reached yet are dimmed.
2. At each stage, read the right-hand panel and say what changed about the
   event since the previous stage.
3. Stop at stage 4 and notice that the log line holds two separate fields,
   `duration_seconds` and `total_tokens`.
4. Continue to stage 6 and find those same two measurements on the dashboard.
5. You can also click any box to jump straight to it. Keyboard users can press
   Tab to move between boxes and Enter to select one.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/hook-to-dashboard-pipeline/main.html"
        height="392px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who build intelligent
textbooks with AI agent skills. No programming background is needed.

### Learning Objective

Summarize how a single skill-run event travels from a hook, into a log file,
and out as a dashboard metric. (Bloom's Taxonomy: Understand)

### Duration

10 minutes

### Prerequisites

- Knows what a token is and why token use is limited
- Has read the definitions of *skill usage hook*, *stop hook*, and *JSONL
  usage log* in Chapter 9

### Activities

1. **Exploration** (3 min): Step through all six stages with **Next**. For
   each stage, say in one sentence what happens to the event.
2. **Guided Practice** (4 min): Close the MicroSim and write a three-sentence
   summary of the path from "a skill runs" to "a row on the dashboard". Reopen
   the MicroSim and check your summary against the six stages.
3. **Assessment** (3 min): Answer the two questions below without looking.

### Assessment

- The learner names the stages in order and identifies the JSONL log as
  storage rather than computation.
- The learner explains why the log is append-only: new events are added
  without rewriting earlier entries.
- The learner states that the dashboard reports elapsed time as well as token
  counts, and that the two are recorded separately.

### Discussion Questions

1. A JSONL file on disk does not optimize anything by itself. Which stage
   turns the raw lines into something a person can act on?
2. Why is grouping log lines by skill a job for a Python script rather than
   for the language model?
3. Describe a skill run that is slow but cheap, and one that is fast but
   expensive. Why would a dashboard that showed only tokens mislead you?

## References

1. [JSON Lines](https://jsonlines.org/) - JSON Lines - Describes the one-record-per-line text format used for the usage log.
2. [Hooks reference](https://code.claude.com/docs/en/hooks) - Claude Code Docs - Documents the hook events an agent can fire, including the Stop hook and the tool-use hooks.
3. [Flowcharts Syntax](https://mermaid.js.org/syntax/flowchart.html) - Mermaid - Documentation for the flowchart syntax and the `click` interaction used in this MicroSim.

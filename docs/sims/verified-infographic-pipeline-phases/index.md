---
title: The Eight-Phase Verified Infographic Pipeline
description: Step-through flowchart of the eight ordered phases that separate claim verification from image rendering, showing which phases are text only, which single phase calls an image model, and which audit-trail files exist after each phase.
image: /sims/verified-infographic-pipeline-phases/verified-infographic-pipeline-phases.png
og:image: /sims/verified-infographic-pipeline-phases/verified-infographic-pipeline-phases.png
twitter:image: /sims/verified-infographic-pipeline-phases/verified-infographic-pipeline-phases.png
social:
   cards: false
quality_score: 100
---

# The Eight-Phase Verified Infographic Pipeline

<iframe src="main.html" height="537px" width="100%" scrolling="no"></iframe>

[Run the Eight-Phase Verified Infographic Pipeline MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }

## About This MicroSim

A text-to-image model can draw a finished, fully labeled poster in one call.
If the same call also invents the numbers, nobody can check them, and a wrong
number is baked into pixels. The **verified infographic pipeline** fixes this
by changing the order of operations: decide what is true first, draw it
second.

This top-to-bottom flowchart shows the eight phases in order.

| Phase | Name in this book | Name in the skill's guide | Adds to the audit trail |
|:-----:|-------------------|---------------------------|-------------------------|
| 1 | Claim Planning | Intake and Claim Planning | `01-claim-plan.yaml` |
| 2 | Source Discovery | Source Discovery | |
| 3 | Per-Claim Verification | Verification and Classification | `02-verification-report.md` |
| 4 | Verification Report | User Checkpoint (mandatory) | |
| 5 | Layout Specification Lock | Layout Specification | `03-layout-spec.yaml` |
| 6 | Verbatim Text Prompt | Image Prompt Assembly | `04-image-prompt.md` |
| 7 | Image Generation (single call) | Final Rendering | `poster.png` |
| 8 | Rendered Image Audit | Post-Render Audit | `sources.md` |

The colors carry the main idea:

- **Teal, inside the dashed band:** phases 1 to 6 are text only. No image
  model is called.
- **Amber:** phase 5 is the lock. After it, no wording or number is written
  again by hand.
- **Deep orange:** phase 7 is the only image-model call.
- **Green:** phase 8 audits the rendered image against the locked
  specification.
- **Dashed red arrow:** a claim rejected in phase 3 never reaches the image.
  It is removed or replaced, which sends the work back to the claim plan.

The phase details follow the verified infographic guide in the
`microsim-generator` skill. In that skill a poster that passes the audit is
then always wrapped in an interactive overlay, which is the subject of
Chapter 26.

## How to Use

1. Select **Next** to walk through the phases in order. Phases that have not
   been reached yet are dimmed.
2. For each phase, read its one-sentence definition and watch the **Audit
   trail** list grow. The newest file is highlighted.
3. Notice at which phase the first image file appears in the list.
4. Click **3. Per-Claim Verification** and find the dashed arrow that returns
   to phase 1.
5. You can also click any box to jump straight to it. Keyboard users can press
   Tab to move between boxes and Enter to select one.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/verified-infographic-pipeline-phases/main.html"
        height="537px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who want factual
posters and infographics they can defend. No programming background is needed.

### Learning Objective

Summarize the eight ordered phases that separate claim verification from image
rendering. (Bloom's Taxonomy: Understand)

### Duration

10 minutes

### Prerequisites

- Knows that a language model can state false things fluently (Chapter 2)
- Has read the one-shot generation risk and baked-in text problem sections of
  Chapter 25

### Activities

1. **Exploration** (3 min): Step through all eight phases with **Next**. For
   each one, say whether it works on text or on pixels.
2. **Guided Practice** (4 min): Group the eight phases under three headings of
   your own, such as "decide", "draw", and "check". Write one sentence for
   each heading.
3. **Assessment** (3 min): Answer the questions below without looking.

### Assessment

- The learner lists the eight phases in order.
- The learner states that phases 1 to 6 are text only and that phase 7 is the
  only image-model call.
- The learner explains what happens to a claim that fails verification.
- The learner explains why an audit is still needed after the wording has been
  locked.

### Discussion Questions

1. Why is it cheaper to fix a wrong number in phase 3 than in phase 8?
2. The author must approve the verification report before any layout work
   begins. What could go wrong if that checkpoint were skipped?
3. Every phase leaves a file behind. Who benefits from that audit trail after
   the poster is published?

## References

1. [Text-to-image model](https://en.wikipedia.org/wiki/Text-to-image_model) - Wikipedia - Background on the image generators used in the single rendering phase.
2. [Hallucination (artificial intelligence)](https://en.wikipedia.org/wiki/Hallucination_(artificial_intelligence)) - Wikipedia - Describes fabricated output, the risk this pipeline is designed to remove.
3. [Fact-checking](https://en.wikipedia.org/wiki/Fact-checking) - Wikipedia - Overview of verifying claims against sources before and after publication.
4. [Flowcharts Syntax](https://mermaid.js.org/syntax/flowchart.html) - Mermaid - Documentation for the flowchart syntax and the `click` interaction used in this MicroSim.

---
title: Interactive Infographic Overlays
description: Covers overlay engines, marker positioning and leader lines, source discovery and passage-level verification, layout specification locking, and the audit trail behind a published claim.
generated_by: claude skill chapter-content-generator
date: 2026-08-22 18:20:00
version: 0.09
---

# Interactive Infographic Overlays

## Summary

This chapter covers the annotation-free illustration technique paired with a JavaScript overlay layer -- callout and grid engines, leader lines, and editable marker positions. It closes with the claim verification report, source sidecar files, and the audit trail that keeps every rendered number traceable to a source. Students will be able to build an interactive callout overlay on top of a generated illustration after this chapter.

## Concepts Covered

This chapter covers the following 17 concepts from the learning graph:

1. Grid Overlay Engine
2. Source Discovery Phase
3. Callout Marker Coordinates
4. Overlay Explore Mode
5. Passage-Level Verification
6. Leader Line Rendering
7. Editable Marker Positions
8. Claim Verification Report
9. generate-favicon.py Script
10. crop-screenshot.py Script
11. Layout Specification Lock
12. Source Sidecar File
13. Verbatim Text Prompt
14. Asymmetric Content Handling
15. Substitution Prohibition
16. Rendered Image Audit
17. Audit Trail Preservation

## Prerequisites

This chapter builds on concepts from:

- [1. Foundations of AI, Language Models, and Prompting](../01-foundations-ai-language-models/index.md)
- [2. AI Coding Agents and the Five Levels of Textbook Intelligence](../02-ai-agents-textbook-intelligence/index.md)
- [3. Python Fundamentals for Skill Automation](../03-python-fundamentals-automation/index.md)
- [7. Progressive Disclosure and Meta-Skill Routing](../07-progressive-disclosure-meta-skills/index.md)
- [21. MicroSim Anatomy and p5.js Basics](../21-microsim-anatomy-p5js-basics/index.md)
- [25. Text-to-Image Models and the Verified Infographic Pipeline](../25-verified-infographic-pipeline/index.md)

---

!!! mascot-welcome "Finishing the overlay, then proving it's true."
    ![Kit waves hello with their tool satchel](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    Chapter 25 introduced the callout overlay engine. This chapter finishes the overlay toolkit and shows the paper trail that lets every number in it survive a fact-check. Right tool, right task!

## Two Overlay Engines

Chapter 25's callout overlay engine handles point markers on specific features. A **grid overlay engine** handles a different layout entirely: the code layer that draws rectangular interactive regions over columns or sections of a poster-style image, better suited to a comparison table baked into an illustration than to labeled points on a diagram.

## Positioning and Connecting Markers

Wherever a marker sits, its position is data, not a hardcoded pixel value. **Callout marker coordinates** are the stored positions identifying where each marker sits on an illustration, kept in data so they can be adjusted without editing code — which is what makes **editable marker positions** possible: the ability to reposition annotation markers through stored data, allowing correction without regenerating anything.

!!! mascot-tip "Move the number, not the picture."
    ![Kit holding up a tool with a knowing look](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    If a marker sits slightly off from the feature it's labeling, fix its stored coordinate — never regenerate the underlying illustration just to nudge a label. That's the entire point of keeping markers in data instead of pixels.

When a label needs to sit outside the illustration itself, **leader line rendering** draws a connecting line from a marker to its label so the association is unambiguous, rather than leaving a reader to guess which label belongs to which point.

#### Diagram: Callout Marker Anatomy

<iframe src="../../sims/callout-marker-anatomy/main.html" width="100%" height="452px" scrolling="no"></iframe>

<details markdown="1">
<summary>Callout Marker Anatomy</summary>
Type: microsim
**sim-id:** callout-marker-anatomy<br/>
**Library:** p5.js<br/>
**Status:** Specified

Bloom Level: Understand (L2)
Bloom Verb: Explain

Learning objective: Explain how a stored marker coordinate, a leader line, and a label work together on an annotation-free illustration.

Canvas layout:
- Left (500px): a simple annotation-free illustration placeholder (a labeled rectangle standing in for a generated picture)
- Right (200px): a small data table showing the currently selected marker's stored {x, y} coordinate

Interactive controls:
- Drag any of 3 example markers to a new position on the illustration
- Toggle: "Show leader lines" on/off

Data Visibility Requirements:
  Stage 1: Show the illustration with 3 markers placed at default coordinates
  Stage 2: Show each marker's stored {x, y} coordinate in the side table, updating live as a marker is dragged
  Stage 3: Show a leader line drawn from each marker to a label positioned outside the illustration

Behavior:
- Dragging a marker updates its stored coordinate in the side table instantly, demonstrating that position is data, not a pixel baked into the image
- Toggling leader lines off/on shows labels floating disconnected vs. clearly connected to their markers

Instructional Rationale: An Understand-level objective is best served by concrete data visibility (the coordinate table) rather than animation — dragging a marker and watching its stored value change makes "position is data" tangible.

Implementation notes: Use p5.js; the illustration itself is a static placeholder rectangle, not a generated image, since the point is the marker/coordinate/leader-line relationship.
</details>

## Exploring an Overlay

Put those markers together into an interaction and you get **overlay explore mode**: an interaction style in which hovering or selecting a marker reveals explanatory information about that feature — the same minimum interactivity bar every diagram in this book has followed since Chapter 1.

## Finding and Verifying Sources

Back in the verified infographic pipeline's claim planning phase, once every assertion is listed, someone has to find evidence for it. The **source discovery phase** is the stage locating authoritative material that could support each planned assertion. Finding a source isn't enough on its own — **passage-level verification** confirms an assertion by quoting the specific text in a source that supports it, rather than citing a document as a whole and hoping it holds up. The result of that work is recorded in a **claim verification report**: showing each planned assertion, its supporting quotation, and whether it passed, was softened, or was removed.

!!! mascot-thinking "Citing a whole document proves nothing specific."
    ![Kit thinking with a paw on their chin](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    A citation to an entire 40-page report doesn't tell you whether the report actually supports your specific number. Passage-level verification forces the question all the way down to one quoted sentence — either that sentence says what you claimed, or it doesn't.

## Locking the Layout Before Rendering

Once claims are verified, nothing about them should change during rendering. **Layout specification lock** means fixing the exact wording and arrangement of a planned poster before generation, so nothing can drift during rendering. That lock is enforced at the prompt level with a **verbatim text prompt**: an image instruction requiring that supplied wording be reproduced exactly, with no paraphrase or substitution, backed by an explicit **substitution prohibition**: forbidding an image generator from altering figures, names, or labels, or inventing additional ones to fill a gap.

!!! mascot-warning "A model will invent a number to fill empty space if you let it."
    ![Kit holding up a caution paw](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    Left unconstrained, an image generator asked to fill a comparison layout with mismatched amounts of real evidence on each side will often invent something to balance it visually. **Asymmetric content handling** — allowing a comparison layout to show unequal amounts of material on each side, so missing evidence is displayed honestly rather than filled with invention — is the deliberate alternative. An honest gap beats a fabricated fact every time.

## Auditing the Result

Even a locked, verbatim-prompted image needs a final check. A **rendered image audit** checks a finished picture against its locked specification to confirm every element was reproduced correctly — the model can still misplace or slightly alter something, even under a substitution prohibition. Every claim behind that audited image is preserved in a **source sidecar file**: a companion file stored beside the finished image recording every claim, its source address, and its supporting quotation, which is what makes **audit trail preservation** possible: retaining the evidence chain behind published material so any figure can be traced back to where it came from, long after the original generation session is over.

## Two More Image Scripts

Two small Python programs handle the last mile of image production. **generate-favicon.py** produces browser tab icons at required sizes from a source picture. **crop-screenshot.py** trims a captured image to a required aspect ratio for use in posts and previews — the same batch-script-substitution philosophy from Chapter 9, applied to image cropping instead of text generation.

## Key Takeaways

- A **grid overlay engine** complements Chapter 25's callout overlay engine for column- or section-based layouts.
- **Callout marker coordinates** stored as data enable **editable marker positions**; **leader line rendering** connects a marker to its label unambiguously.
- **Overlay explore mode** is the interaction pattern that makes any of this actually usable by a reader.
- **Source discovery** and **passage-level verification** produce a **claim verification report**; a **layout specification lock**, **verbatim text prompt**, **substitution prohibition**, and **asymmetric content handling** keep rendering honest.
- A **rendered image audit**, backed by a **source sidecar file**, gives every published figure **audit trail preservation** — with **generate-favicon.py** and **crop-screenshot.py** handling the smaller image tasks around it.

!!! mascot-celebration "You could trace any number in a poster back to its source."
    ![Kit celebrating with arms raised](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    Overlay, verification, lock, audit — that's a complete chain of custody from a raw claim to a published picture. Right tool, right task!

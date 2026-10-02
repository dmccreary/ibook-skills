---
title: Text-to-Image Models and the Verified Infographic Pipeline
description: Explains the one-shot generation risk and fact fabrication rate, the eight-phase verified infographic pipeline, interactive overlays, book identity assets, and MARP slide decks.
generated_by: claude skill chapter-content-generator
date: 2026-08-22 18:05:00
version: 0.09
---

# Text-to-Image Models and the Verified Infographic Pipeline

## Summary

This chapter explains what modern text-to-image models changed, the one-shot generation risk, and why baked-in text produces a high rate of fabricated facts. It introduces the eight-phase verified infographic pipeline that separates claim planning, source discovery, and passage-level verification from image rendering. Students will be able to explain why a locked layout specification must precede any image call after this chapter.

## Concepts Covered

This chapter covers the following 18 concepts from the learning graph:

1. Text-to-Image Model
2. Text Rendering in Images
3. MARP Slide Deck
4. Image Prompt Engineering
5. Slide Deck Publishing
6. One-Shot Generation Risk
7. Cover Image Generation
8. Fact Fabrication Rate
9. Baked-In Text Problem
10. Site Logo and Favicon
11. Social Media Preview Card
12. Separating Facts From Pixels
13. Open Graph Meta Tags
14. Verified Infographic Pipeline
15. Interactive Infographic Overlay
16. Claim Planning Phase
17. Annotation-Free Illustration
18. Callout Overlay Engine

## Prerequisites

This chapter builds on concepts from:

- [1. Foundations of AI, Language Models, and Prompting](../01-foundations-ai-language-models/index.md)
- [2. AI Coding Agents and the Five Levels of Textbook Intelligence](../02-ai-agents-textbook-intelligence/index.md)
- [4. Development Tools: Editor, Terminal, and Git Basics](../04-dev-tools-editor-git-basics/index.md)
- [21. MicroSim Anatomy and p5.js Basics](../21-microsim-anatomy-p5js-basics/index.md)

---

!!! mascot-welcome "Pixels are the easy part. Facts are the hard part."
    ![Kit waves hello with their tool satchel](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    This chapter is about the moment images stopped being decoration and started being able to lie convincingly. Here's how this book's own pipeline keeps that from happening. Right tool, right task!

## What Text-to-Image Models Changed

A **text-to-image model** is a generative system that produces a picture from a written description, and modern versions can do something earlier ones couldn't: **text rendering in images** — the capability to draw legible, exact wording inside a picture. That single capability is what makes a beautiful, fully-labeled infographic poster achievable in one generation call. It's also what makes a factual error in that poster permanent and unreadable as an error, since the wrong number is now baked into pixels instead of sitting in editable text.

## The One-Shot Generation Risk

Asking a model to invent facts and render them as a finished poster in the same step is the **one-shot generation risk**: the hazard of asking an image generator to invent factual content and render it simultaneously, since neither step is verified. This isn't a theoretical concern. The **fact fabrication rate** — the measured proportion of generated factual claims that no cited source supports — was measured on a real test at eight of ten numeric claims unsupported, with two of five citations entirely fictional.

!!! mascot-warning "A beautiful poster is not evidence the numbers are real."
    ![Kit holding up a caution paw](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    This is Chapter 2's hallucination warning, made visually undeniable. The **baked-in text problem** means wording is permanently fixed into pixels, so any error requires regenerating the whole picture and cannot be audited by a reader the way a wrong number in a paragraph could be quietly fixed. Never trust a one-shot generated infographic's numbers without checking them against a real source first.

#### Diagram: The Eight-Phase Verified Infographic Pipeline

<iframe src="../../sims/verified-infographic-pipeline-phases/main.html" width="100%" height="537px" scrolling="no"></iframe>

<details markdown="1">
<summary>The Eight-Phase Verified Infographic Pipeline</summary>
Type: workflow
**sim-id:** verified-infographic-pipeline-phases<br/>
**Library:** Mermaid<br/>
**Status:** Specified

Bloom Level: Understand (L2)
Bloom Verb: Summarize

Learning objective: Summarize the eight ordered phases that separate claim verification from image rendering.

Visual style: Top-to-bottom Mermaid flowchart, eight numbered stages

Nodes:
1. "1. Claim Planning" (rounded rectangle)
2. "2. Source Discovery" (rounded rectangle)
3. "3. Per-Claim Verification" (rounded rectangle)
4. "4. Verification Report" (rounded rectangle)
5. "5. Layout Specification Lock" (rounded rectangle, amber — the last text-only stage)
6. "6. Verbatim Text Prompt" (rounded rectangle)
7. "7. Image Generation (single call)" (rounded rectangle, book's accent color)
8. "8. Rendered Image Audit" (rounded rectangle)

Edges: sequential 1 --> 2 --> 3 --> 4 --> 5 --> 6 --> 7 --> 8, with a dashed "reject/revise" edge from 3 back to 1 for a claim that fails verification

Interactivity requirement: every node MUST have a `click` directive opening an infobox with that phase's one-sentence definition, and phases 1-6 should be visually grouped (background band) as "text-only," with phase 7 marked as "the only image-model call."

Color scheme: text-only phases in the book's teal accent; phase 7 (image generation) in a distinct warm color to emphasize it happens exactly once; phase 8 in green (audit/verification).

Implementation: Mermaid flowchart with per-node click handlers rendered inside the MicroSim's main.html, opening a shared infobox panel below the diagram.
</details>

## Separating Facts From Pixels: The Verified Infographic Pipeline

The fix isn't to avoid text-to-image models — it's to change the order of operations. **Separating facts from pixels** is the design rule that content is decided and verified in text before any picture is produced, so the image generator never chooses a figure on its own. That rule is implemented as the **verified infographic pipeline**: a staged process producing a factual poster in which claims are planned, sourced, verified, and locked before a single image is generated, and the result is audited afterward. It begins with the **claim planning phase**: the initial stage listing every factual assertion a planned poster will make, before any source is even consulted.

!!! mascot-thinking "Decide what's true first. Draw it second."
    ![Kit thinking with a paw on their chin](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    The whole pipeline is one mental shift, repeated eight times: never let the same step both decide a fact and render it. Planning, sourcing, and verification all happen in plain text, where a claim can be checked and revised cheaply — only once every number is locked does an image call happen at all.

## Prompting for Images

Once content is locked, generating the actual picture is its own discipline: **image prompt engineering** — composing the description supplied to an image generator so the resulting picture matches an intended composition and content, the visual counterpart to Chapter 1's prompt engineering for text.

## Interactive Infographic Overlays

An alternative to baking labels into pixels at all is the **interactive infographic overlay**: a labeled illustration in which a picture carries no printed annotation and a code layer draws numbered markers, labels, and explanations on top. That starts with an **annotation-free illustration**: a generated picture produced deliberately without text, arrows, or labels, so an interactive layer can supply them instead. The code responsible for that layer is a **callout overlay engine**: drawing numbered point markers on specific features of an illustration and connecting them to descriptive labels.

!!! mascot-tip "Labels in code stay editable; labels in pixels don't."
    ![Kit holding up a tool with a knowing look](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    An overlay's labels can be corrected, translated, or made accessible to a screen reader with a code change. A label baked into an image requires regenerating the entire picture for a one-word fix. When in doubt, prefer the overlay.

## Book Identity: Covers, Logos, and Social Cards

Text-to-image generation also produces the smaller visual assets that give a book its identity online. **Cover image generation** produces the principal illustration representing a book, derived from the book's own subject matter. **Site logo and favicon** are the small identifying marks shown in a site header and browser tab, typically derived from a book's cover or character artwork — Kit's own neutral pose serves this role for this book. When a link to a page is shared, a **social media preview card** is the image and text a platform displays, driven by **Open Graph meta tags**: markup in a page header supplying the title, description, and image that platforms use when rendering that shared link.

## Slide Decks

Book content doesn't only live as chapter pages. A **MARP slide deck** is a presentation authored in markdown and rendered as a self-contained web deck that can be published alongside a book, and **slide deck publishing** is adding that rendered presentation to a site so it can be viewed in a browser and linked directly — the same authoring-in-markdown philosophy behind every chapter you've read, applied to a lecture format instead of a chapter format.

## Key Takeaways

- **Text-to-image models** can now render **exact text inside images**, which makes beautiful infographics possible and factual errors permanent.
- The **one-shot generation risk** and a measured **fact fabrication rate** are why the **baked-in text problem** matters — never trust an ungrounded poster's numbers.
- **Separating facts from pixels** is enforced by the **verified infographic pipeline**, starting with a **claim planning phase** before any image call.
- **Image prompt engineering** shapes the picture once content is locked; an **interactive infographic overlay**, built from an **annotation-free illustration** and a **callout overlay engine**, keeps labels editable instead of baked in.
- **Cover images**, **logos and favicons**, **social media preview cards**, and **Open Graph meta tags** give a book its visual identity online; **MARP slide decks** extend that content into a presentation format.

!!! mascot-celebration "You can now tell a trustworthy infographic from a risky one."
    ![Kit celebrating with arms raised](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    Claims planned and verified before a single pixel exists — that's the difference between a poster you can trust and one that just looks trustworthy. Right tool, right task!

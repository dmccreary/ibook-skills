---
title: Slide Decks, Stories, and Audio Media
description: Covers PowerPoint lecture decks with speaker notes, illustrated stories and graphic novels, freely-licensed image sourcing and compression, overlay quiz mode, and text-to-speech narration.
generated_by: claude skill chapter-content-generator
date: 2026-08-22 18:35:00
version: 0.09
---

# Slide Decks, Stories, and Audio Media

## Summary

This chapter covers MARP web decks and downloadable PowerPoint lectures with speaker notes, illustrated stories and graphic novels, and sourcing freely-licensed images from Wikimedia and government archives with proper attribution. It closes with ElevenLabs text-to-speech narration and glossary pronunciation buttons. Students will be able to generate a slide deck and an audio-narrated glossary entry after this chapter.

## Concepts Covered

This chapter covers the following 17 concepts from the learning graph:

1. Illustrated Story Format
2. Text-to-Speech Narration
3. Freely-Licensed Images
4. Graphic Novel Format
5. ElevenLabs Voice Settings
6. Audio Streaming Playback
7. Pronounce Button
8. generate-images.py Script
9. Wikimedia Commons Sourcing
10. Government Archive Images
11. Image Attribution
12. Image Compression
13. trim-padding-from-image.py
14. compress-images.py Script
15. Overlay Quiz Mode
16. PowerPoint Lecture Deck
17. Speaker Notes

## Prerequisites

This chapter builds on concepts from:

- [1. Foundations of AI, Language Models, and Prompting](../01-foundations-ai-language-models/index.md)
- [3. Python Fundamentals for Skill Automation](../03-python-fundamentals-automation/index.md)
- [7. Progressive Disclosure and Meta-Skill Routing](../07-progressive-disclosure-meta-skills/index.md)
- [17. Chapter Structure and Content Elements](../17-chapter-structure-content-elements/index.md)
- [18. Chapter Content Quality and Review](../18-chapter-content-quality-review/index.md)
- [19. FAQs and Curated References](../19-faqs-curated-references/index.md)
- [20. Glossaries and Quizzes](../20-glossaries-and-quizzes/index.md)
- [21. MicroSim Anatomy and p5.js Basics](../21-microsim-anatomy-p5js-basics/index.md)
- [25. Text-to-Image Models and the Verified Infographic Pipeline](../25-verified-infographic-pipeline/index.md)
- [26. Interactive Infographic Overlays](../26-interactive-infographic-overlays/index.md)

---

!!! mascot-welcome "The last stretch of media, then straight into publishing."
    ![Kit waves hello with their tool satchel](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    Decks for the classroom, stories for a first introduction, and a voice for readers who'd rather listen — this chapter rounds out everything a book can be besides plain chapter text. Right tool, right task!

## Downloadable Decks: PowerPoint Lectures

Chapter 25's MARP deck lives in the browser; sometimes a classroom needs a downloadable file instead. A **PowerPoint lecture deck** is a downloadable presentation file intended for classroom use, generated with structured narrative and presenter guidance, carrying **speaker notes**: presenter-facing text attached to a slide describing what to say and which points to emphasize — visible to the presenter, invisible to the audience on screen.

## Telling Stories with Pictures

Some ideas land better as narrative than as definition. The **illustrated story format** is a narrative retelling of course material paired with generated pictures, used to introduce ideas through story rather than through a direct explanation. For material that needs more room to unfold, the **graphic novel format** is a sequential illustrated narrative with panels and dialogue, used for extended storytelling within a book. Both are produced with help from **generate-images.py**: the program that requests illustrations for a narrative and stores them with their descriptions.

!!! mascot-thinking "A story is a scaffold, not a shortcut."
    ![Kit thinking with a paw on their chin](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    An illustrated story works because it gives an abstract concept a concrete situation to attach to before the formal definition arrives — it's instructional scaffolding from Chapter 12, told through character and plot instead of through ordered prose.

## Sourcing Images Responsibly

Not every image in a book needs to be generated. **Freely-licensed images** are pictures whose terms permit reuse in educational material, typically with attribution required. Two reliable sources supply them: **Wikimedia Commons sourcing** obtains reusable illustrations and photographs from a large repository of openly licensed media, and **government archive images** are pictures from public agency collections, often free of copyright restriction and suitable for educational reuse.

!!! mascot-warning "Free to use still means credit is required."
    ![Kit holding up a caution paw](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    "Freely licensed" is not the same as "no obligations." **Image attribution** means crediting the creator and stating the license of a reused picture, exactly as the license terms require. Skipping attribution on a Creative Commons image (the same license family from Chapter 1) is a license violation, not a shortcut.

## Keeping Images Fast to Load

A page full of unoptimized images loads slowly no matter how well-sourced the pictures are. **Image compression** reduces the file size of pictures so pages load quickly, while keeping quality acceptable for reading, handled at scale by **compress-images.py**: reducing picture file sizes across an entire project in one pass. Before compression even happens, **trim-padding-from-image.py** removes surrounding blank space from a picture so it aligns correctly when placed, avoiding a picture that looks fine alone but sits oddly next to text once it's actually embedded.

!!! mascot-tip "Trim first, then compress — the order matters."
    ![Kit holding up a tool with a knowing look](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    Compressing an image with excess blank padding still leaves the padding in the file, just smaller. Trim the padding first, then compress what's left — you'll get a tighter final file either way, and a cleaner layout as a bonus.

## One More Overlay Mode: Quiz

Chapters 25 and 26 covered explore mode for an interactive overlay; there's a second mode built on the same markers. **Overlay quiz mode** is an interaction style in which a reader is asked to identify a named feature by selecting the correct marker, turning the same callout infrastructure from Chapter 26 into a self-check instead of a reference.

## Hearing the Book: Text-to-Speech

For a reader who'd rather listen than read, **text-to-speech narration** generates spoken audio of written material, offering an alternative to reading rather than a replacement for it. The specific voice that reads it is shaped by **ElevenLabs voice settings**: the parameters controlling a synthesized voice's identity, pacing, and expressiveness. Delivered through **audio streaming playback** — sound that begins playing before the whole file has downloaded — narration doesn't force a reader to wait through a long download before hearing the first word. At the smallest scale, a **pronounce button** is a small control beside a defined term that plays its spoken pronunciation, helping readers with unfamiliar vocabulary hear a term like "GraphRAG" or "idempotent" spoken correctly.

#### Diagram: Pronounce Button and Streaming Playback

<iframe src="../../sims/pronounce-button-demo/main.html" width="100%" height="502px" scrolling="no"></iframe>

<details markdown="1">
<summary>Pronounce Button and Streaming Playback</summary>
Type: microsim
**sim-id:** pronounce-button-demo<br/>
**Library:** p5.js<br/>
**Status:** Specified

Bloom Level: Apply (L3)
Bloom Verb: Demonstrate

Learning objective: Demonstrate how clicking a pronounce button begins audio streaming playback before the full narration has loaded.

Canvas layout:
- Top: three example glossary terms with a small speaker-icon pronounce button beside each ("GraphRAG", "idempotent", "Schemdraw")
- Bottom: a horizontal progress bar representing streaming playback, with a "Downloaded" marker and a "Playback Position" marker

Interactive controls:
- Click any pronounce button to start its term's simulated playback
- Button: "Simulate slow connection" (exaggerates the gap between download and playback markers)

Behavior:
- Clicking a pronounce button starts the "Playback Position" marker moving immediately, while the "Downloaded" marker fills in behind it more slowly — demonstrating that playback begins before the full file has downloaded
- Hovering the progress bar shows an infobox explaining streaming playback vs. waiting for a full download

Instructional Rationale: An Apply-level demonstration lets the reader trigger the behavior directly and see the two markers diverge, making "streaming" concrete instead of an abstract claim.

Implementation notes: Use p5.js; no real audio is played, the markers simulate timing only.
</details>

## Key Takeaways

- A **PowerPoint lecture deck** with **speaker notes** serves the classroom; the **illustrated story** and **graphic novel formats**, built via **generate-images.py**, introduce ideas through narrative.
- **Freely-licensed images**, sourced from **Wikimedia Commons** or **government archives**, still require proper **attribution**.
- **Image compression** and **trim-padding-from-image.py**, run via **compress-images.py**, keep a book's pages fast to load.
- **Overlay quiz mode** turns an interactive overlay's markers into a self-check.
- **Text-to-speech narration**, tuned by **ElevenLabs voice settings** and delivered through **streaming playback**, plus a per-term **pronounce button**, make a book listenable as well as readable.

!!! mascot-celebration "You've now met every media format this book's library can generate."
    ![Kit celebrating with arms raised](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    Slides, stories, sourced images, and a spoken voice — that's the complete media toolkit sitting alongside the chapters and MicroSims you've already mastered. Right tool, right task!

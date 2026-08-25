---
name: book-media-generator
description: Generates media for intelligent textbooks - slide decks and presentations (MARP web decks in docs/slides/ or PowerPoint .pptx lecture downloads), illustrated stories and graphic novels, freely-licensed chapter images from Wikimedia and government archives, and audio (text-to-speech voiceovers, glossary pronounce buttons via ElevenLabs). Routes to the appropriate media guide.
license: Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
metadata:
  ibook.version: "1.0"
  ibook.preferred-model: "sonnet"
---

# Book Media Generator

**Version:** 1.0

## Overview

This meta-skill generates static media for intelligent textbooks — slides, illustrations, sourced images, and audio. It consolidates six skills into a single entry point with on-demand loading of specific media guides.

## FIRST: Slides Disambiguation Rule

Two routes make slide decks. Before routing any "make slides / a presentation / a deck" request, decide:

- **Published on the site / embedded / web deck / shareable link** → `references/marp-deck-guide.md` (MARP → self-contained HTML in `docs/slides/`, iframe-embedded, added to the slides gallery and nav)
- **Downloadable file / classroom lecture / "PowerPoint" / .pptx** → `references/pptx-lecture-guide.md` (pptxgenjs → .pptx with 4-act storytelling and speaker notes)
- **Ambiguous** (just "make slides for chapter 3") → ask ONE question: "Published on the site as a web deck, or a downloadable PowerPoint for classroom use?"

## When to Use This Skill

Use this skill when users request:

- A slide deck or presentation from a topic, chapter, or document (see disambiguation rule above)
- An illustrated story / graphic novel about a scientist or historical figure (docs/stories/)
- Adding freely-licensed maps and photos to chapters (Wikimedia Commons, US government archives)
- Text-to-speech audio, voiceovers, or spoken narration (ElevenLabs)
- A "Pronounce" button with an MP3 pronunciation for a glossary term

## Step 1: Identify Media Type

### Routing Table

| Trigger Keywords | Guide File | Purpose |
|------------------|------------|---------|
| slide deck, slides, presentation, web deck, publish slides, MARP, deck on the site | `references/marp-deck-guide.md` | MARP → self-contained HTML deck in docs/slides/ with gallery + nav integration |
| powerpoint, pptx, lecture deck, classroom slides, downloadable deck, lecture presentation | `references/pptx-lecture-guide.md` | pptxgenjs → .pptx lecture with 4-act structure and speaker notes |
| story, graphic novel, illustrated narrative, historical figure story, scientist story, case study story | `references/story-guide.md` | Illustrated graphic-novel narratives in docs/stories/ with generated panel images |
| chapter images, add photos, add maps, wikimedia, image sourcing, freely licensed images, attribution | `references/chapter-images-guide.md` | Source real licensed media from Wikimedia/gov archives with captions + attribution |
| text to speech, tts, voiceover, narration, audio version, speech synthesis, elevenlabs | `references/text-to-speech-guide.md` | ElevenLabs TTS — voiceovers, voice apps, 70+ languages |
| pronounce, pronunciation, pronounce button, glossary audio, say the term | `references/pronounce-button-guide.md` | Generate an MP3 pronunciation and insert a Pronounce button into a glossary entry |

### Decision Tree

```
Slides or a presentation?
  → Apply the Slides Disambiguation Rule (top of this file)

Narrative with illustrated panels about a person or case study?
  → YES: story-guide.md

Poster/infographic containing numeric claims or cited data?
  → NOT this skill: the fact-verified poster route lives in the
    microsim-generator skill (references/verified-infographic-guide.md)
  (purely decorative image with no factual claims → consider
   the cover-image feature in book-installer instead)

Real photos/maps sourced from archives (not AI-generated)?
  → YES: chapter-images-guide.md

Audio from text?
  → Single glossary term pronunciation → pronounce-button-guide.md
  → Anything else (narration, voiceover, app) → text-to-speech-guide.md
```

## Step 2: Load the Matched Guide

Read the corresponding guide file from `references/` and follow its workflow.

## Audio Routes: ElevenLabs API Key

Both audio routes (`text-to-speech-guide.md`, `pronounce-button-guide.md`) call the ElevenLabs API and need `ELEVENLABS_API_KEY` set in the environment. Check for it before starting; if missing, point the user at `references/tts-installation.md`.

## Supporting Files

- `references/marp-mkdocs-integration.md`, `references/marp-authoring-guide.md`, `assets/marp/template.md` — MARP route
- `references/pptx-slide-patterns.md`, `references/pptx-speaker-notes-guide.md` — PowerPoint route
- `references/story-index-template.md`, `scripts/story/` (generate-images.py, verify-images.py, fix-references.py, uncomment-images.sh) — story route
- `references/tts-installation.md`, `references/tts-streaming.md`, `references/tts-voice-settings.md` — TTS route
- `scripts/audio/generate-pronunciation.py` — pronounce-button route

## Examples

### Example 1: Web Deck
**User:** "Turn chapter 4 into a presentation on the site"
**Routing:** "presentation" + "on the site" → `references/marp-deck-guide.md`
**Action:** Read marp-deck-guide.md; produce docs/slides/<deck>/ + gallery entry + nav

### Example 2: Classroom PowerPoint
**User:** "I need a PowerPoint to lecture from for chapter 4"
**Routing:** "PowerPoint" + "lecture" → `references/pptx-lecture-guide.md`
**Action:** Read pptx-lecture-guide.md; generate the .pptx with speaker notes

### Example 3: Ambiguous Slides
**User:** "Make slides for chapter 4"
**Routing:** Ambiguous → ask: web deck or downloadable PowerPoint? Then route accordingly.

### Example 4: Story
**User:** "Add a graphic novel story about Ada Lovelace to the Stories section"
**Routing:** "graphic novel story" → `references/story-guide.md`
**Action:** Read story-guide.md; write index.md with panel prompts; run scripts/story/generate-images.py

### Example 5: Fact-Checked Poster (routes elsewhere)
**User:** "Create an infographic about remote-work productivity statistics"
**Routing:** NOT this skill — fact-verified posters moved to `microsim-generator` → `references/verified-infographic-guide.md`
**Action:** Load the microsim-generator skill instead; it owns claim verification, the poster pipeline, and the gallery thumbnail script

### Example 6: Pronounce Button
**User:** "Create a pronounce button for the term Mitochondria"
**Routing:** "pronounce button" → `references/pronounce-button-guide.md`
**Action:** Read pronounce-button-guide.md; run scripts/audio/generate-pronunciation.py; insert the button into glossary.md

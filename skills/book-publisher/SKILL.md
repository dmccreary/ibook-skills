---
name: book-publisher
description: Publishes and promotes a finished intelligent textbook - GitHub README with badges and site statistics, LinkedIn announcement posts, LinkedIn carousel document posts (PPTX/PDF slideshows), and AP-style press releases. Use when announcing a book milestone or updating repository documentation. Routes to the appropriate guide.
model: sonnet
license: Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
metadata:
  ibook.version: "1.0"
---

# Book Publisher

**Version:** 1.0

## Overview

This meta-skill handles publishing and promotion tasks for finished (or milestone-ready) intelligent textbooks. It consolidates four skills into a single entry point with on-demand loading of specific guides.

All four routes draw their numbers from the same canonical metrics hub — `docs/learning-graph/book-metrics.json`, produced by `bk-generate-book-metrics` (book-installer feature #40) — so the README, posts, carousel, and press release always cite identical statistics. Never recount content by hand or parse the human-readable `book-metrics.md` table.

## When to Use This Skill

Use this skill when users request:

- Creating or updating the GitHub README (badges, overview, site metrics, getting started)
- Announcing a textbook milestone on LinkedIn (post text)
- Building a LinkedIn carousel / document post (13-slide PPTX/PDF with screenshots)
- Writing an AP-style press release for journalists or education trade press

## Step 1: Identify Publishing Task

### Routing Table

| Trigger Keywords | Guide File | Purpose |
|------------------|------------|---------|
| readme, github readme, update the readme, badges, repo documentation | `references/readme-guide.md` | Create/update README.md with badges, overview, metrics table, getting-started |
| linkedin post, linkedin announcement, announce the book, milestone post, social media announcement | `references/linkedin-post-guide.md` | Generate LinkedIn post text with metrics, hashtags, and link strategy |
| linkedin carousel, document post, carousel post, slideshow post, pptx for linkedin | `references/linkedin-carousel-guide.md` | Generate a 13-slide PPTX/PDF carousel with real screenshots and metrics |
| press release, media pitch, journalists, news release, AP style, education press | `references/press-release-guide.md` | Write an AP-style press release with headline, lead, quotes, boilerplate |

### Decision Tree

```
GitHub repository documentation (README, badges)?
  → YES: readme-guide.md

Social announcement as TEXT (a LinkedIn post)?
  → YES: linkedin-post-guide.md

Social announcement as a SLIDESHOW (LinkedIn document post, PPTX/PDF)?
  → YES: linkedin-carousel-guide.md
  (Post caption text for it → linkedin-post-guide.md; the two are often paired)

Formal news announcement for journalists / trade press?
  → YES: press-release-guide.md
```

## Step 2: Ensure the Metrics Hub Is Fresh

Before any route, verify the canonical metrics file exists and is current:

```bash
bk-generate-book-metrics 2>/dev/null \
  || python3 "$BK_HOME/src/book-metrics/book-metrics.py" docs
```

Then read `docs/learning-graph/book-metrics.json` (the `metrics` object). If the script is unavailable, load `$HOME/.claude/skills/book-installer/references/book-metrics.md` (feature #40) for the full setup.

## Step 3: Load the Matched Guide

Read the corresponding guide file from `references/` and follow its workflow.

## Supporting Files

- `references/badges.md` — shields.io badge catalog for the README
- `references/carousel-slide-patterns.md` — nine reusable pptxgenjs slide patterns
- `references/carousel-content-sourcing.md` — which project field feeds which carousel slide
- `scripts/collect-site-metrics.py` — fallback scanner for counts the metrics hub does not provide (image assets, code blocks)
- `scripts/validate-readme.py` — README structure validator
- `scripts/crop-screenshot.py` — crop screenshots to carousel aspect ratio

## Examples

### Example 1: README
**User:** "Update the README for this book"
**Routing:** Keyword "README" → `references/readme-guide.md`
**Action:** Refresh book-metrics.json, read readme-guide.md, generate README.md with badges and metrics table

### Example 2: LinkedIn Post
**User:** "Write a LinkedIn announcement — we just published chapter 12"
**Routing:** Keywords "LinkedIn announcement" → `references/linkedin-post-guide.md`
**Action:** Read linkedin-post-guide.md; pull metrics from book-metrics.json; produce post text + hashtags

### Example 3: Carousel
**User:** "Make a LinkedIn carousel showing off the book's features"
**Routing:** Keyword "carousel" → `references/linkedin-carousel-guide.md`
**Action:** Read linkedin-carousel-guide.md; capture/crop screenshots; build the 13-slide PPTX

### Example 4: Press Release
**User:** "Write a press release for the course launch"
**Routing:** Keywords "press release" → `references/press-release-guide.md`
**Action:** Read press-release-guide.md; verify 2-3 figures from book-metrics.json; write AP-style release

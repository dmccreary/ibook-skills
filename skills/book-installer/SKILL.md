---
name: book-installer
description: Installs and configures intelligent-textbook infrastructure - scaffold a brand-new MkDocs Material textbook (init textbook), install any of 40 features (math, mascot, learning graph viewer, Google Analytics GA4, custom 404, kanban board), and generate book metrics. Routes to the appropriate installation guide.
license: Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
metadata:
  ibook.version: "1.0"
---

# Book Installer

**Version:** 1.0

### Changelog

- **v1.0** — First tracked version number for this skill. Adds
  `references/mascot-placement-rules.md` as the single canonical source for when
  and how often a learning mascot may appear, plus
  `scripts/render-mascot-guide.py` (renders those rules into a book's
  `CONTENT-GENERATION-GUIDE.md` between sentinel comments so the copy is
  regenerated, never hand-edited). The per-chapter ceiling is raised from 6 to 9
  admonitions for longer chapters, and `scripts/validate-chapter-mascots.py` now
  reports the deprecated `-encouraging` spelling of the encourage pose class —
  which `mascot.css` never defined, so it rendered unstyled — and exempts the
  Chapter 1 self-introduction
  from the 1-3 sentence cap it always violated. Version is tracked under
  `metadata:` rather than a bare `version:` key, which strict packaging
  validation rejects.

## Overview

This meta-skill handles installation and setup tasks for intelligent textbook projects. It consolidates five installation skills into a single entry point with on-demand loading of specific installation guides.

## When to Use This Skill

Use this skill when users request:

- Setting up a new MkDocs Material project
- Creating a new intelligent textbook from scratch (feature #0 scaffold)
- Installing a learning graph viewer
- Setting up skill usage tracking with hooks
- Registering the book with Google Analytics (GA4 Measurement ID)
- Bootstrapping project infrastructure

## Step 1: Handle Help Requests

If the user asks for "help", "what can you do", or "list features", display this numbered list directly (do not load a reference file):

```
Book Installer Features (most → least common):

 0. New textbook scaffold - complete mkdocs.yml + docs/ tree + license for an empty directory (run once at project birth)
 1. Simple mkdocs.yml template - Minimal starter config for new projects (see feature 0)
 2. Site logo - Add custom logo to header
 3. Favicon - Browser tab/bookmark icon
 3b. Generate favicon from mascot - Auto-generate favicon.ico from neutral.png mascot image
 4. Cover image & social preview - Home page image + og:image metadata
 4b. Generate cover image prompt - Create a prompt for generating a cover image using text-to-image AI (DALL-E, Midjourney, etc.)
 4c. Social media preview hook - Inject og:* / twitter:* meta tags via MkDocs hook (no Cairo required)
 5. Math equations - KaTeX (recommended) or MathJax
 6. Code syntax highlighting - Language-aware code blocks
 7. Code copy button - One-click copy for code blocks
 8. Mermaid diagrams - Flowcharts, sequence diagrams from text
 9. Content tabs - Tabbed sections for alternatives
10. Image zoom (GLightbox) - Click to enlarge images
11. Custom admonitions - Prompt boxes with copy button
12. Interactive quizzes - Self-assessment questions
13. Abbreviations & tooltips - Glossary hover definitions
14. Task lists - Checkbox lists
15. Simple feedback - Thumbs up/down per page
16. Detailed comments (Giscus) - GitHub Discussions integration
17. Tags & categorization - Page tagging system
18. Search enhancements - Suggestions and highlighting
19. Table of contents config - TOC sidebar options
20. Blog support - Add blog section
21. Announcement bar - Dismissible top banner
22. Privacy & cookie consent - GDPR compliance
23. Learning graph viewer - Interactive concept visualization
24. Skill usage tracker - Claude Code analytics hooks
25. Google Analytics - requires a Google Analytics property ID G-*
26. .gitignore installer - make sure that `site` and `.cache` are not in the main branch
27. extra CSS installer for iframe and customer prompt admonition
28. extra JavaScript installer - for prompt admonition copy button
29. Feature checklist - auto-detect and document which features are implemented
30. Learning mascot - add a pedagogical agent character to guide students
31. Instructor's guide - comprehensive teacher's guide with classroom tips
32. Custom 404 page - friendly error page with mascot image
33. Document status indicators - colored dots in nav showing page lifecycle state
34. Kanban board - GitHub Projects board for tracking textbook development
35. Mascot chapter updater - retrofit existing chapters with mascot admonitions
36. About page - professional about.md with motivation, author bio, and citations
37. Slide generator - install slide-viewer MicroSim and generate slides.md decks for chapters
38. Reading level analysis - Flesch-Kincaid grade level report for all chapters
39. Generate all supplementary content - glossary, FAQ, per-chapter quizzes & references, book metrics, diagram reports, about page, landing page, README
40. Book metrics report - chapters, concepts, glossary/FAQ counts, quiz & reference totals, diagrams, equations, MicroSims, word count & equivalent pages (book-metrics.md + chapter-metrics.md)

Type a number or feature name to install.

Note: If you see `navigation.tabs` in mkdocs.yml, remove it. These books
use side navigation optimized for wide landscape screens.
```

After displaying the list, wait for user to specify which feature they want.

---

## Step 1b: Check for Navigation Tabs (Existing Projects)

When working with an existing mkdocs.yml, always check for and remove navigation tabs:

```yaml
# REMOVE these lines if present in mkdocs.yml:
theme:
  features:
    - navigation.tabs        # DELETE
    - navigation.tabs.sticky # DELETE
```

These books use side navigation optimized for wide landscape screens. Top navigation tabs waste vertical space and are not appropriate for this format.

---

## Step 2: Identify Installation Type

Match the user's request to the appropriate installation guide:

### Routing Table

| Trigger Keywords | Action | Purpose |
|------------------|--------|---------|
| help, what can you do, features, capabilities, list features | Display numbered list (Step 1) | Show quick feature overview |
| init textbook, scaffold textbook, brand new book, empty directory, fresh start, new textbook from scratch, 0 | `references/init-textbook.md` | Bootstrap a brand-new textbook from scratch (mkdocs.yml + docs/ + license + contact + social-override hook) — run this *before* any other feature |
| 1, simple mkdocs, minimal template, starter config | `references/init-textbook.md` | Canonical scaffold (supersedes the old minimal template) |
| google analytics, GA4, measurement id, tracking id, G-, analytics property, register analytics, 25 | `references/google-analytics.md` | Create the GA4 property, write the G-* Measurement ID into mkdocs.yml extra.analytics, verify the tag, deploy |
| enrich, add feature, number 2-24, specific feature name | `references/mkdocs-features.md` | Install specific feature |
| new project, mkdocs, textbook, bootstrap, setup, template, new book | `references/init-textbook.md` | Create new MkDocs Material project (feature 0 scaffold) |
| graph viewer, learning graph, visualization, interactive graph, concept viewer | `references/learning-graph-viewer.md` | Add learning graph viewer to existing project |
| track skills, skill usage, activity tracking, hooks, usage analytics | `references/skill-tracker.md` | Set up skill tracking with hooks |
| generate cover image prompt, generate cover image, auto cover image prompt, create cover image promt, run cover prompt script | `references/cover-image-generator.md` | Generate a high-quality cover image prompt from the book's own content; image auto-generation via API/ChatGPT is optional and only runs if explicitly requested |
| cover image, home page, montage, book cover, index page | `references/home-page-template.md` | Create home page with cover image and social metadata |
| social media preview, social card, social meta, og:image, og:title, og:description, open graph, twitter card, twitter image, linkedin preview, slack unfurl, bk-check-social-cover, social hook, social override | `references/social-media-preview.md` | Install the Cairo-free hook that injects og:* and twitter:* meta tags on every page |
| logo, site logo, branding, upper left, header icon | `references/mkdocs-features.md` | Add custom logo with AI prompt examples |
| favicon, browser tab, bookmark icon, .ico | `references/mkdocs-features.md` | Add favicon with AI prompt examples |
| generate favicon, favicon from mascot, mascot favicon, favicon.ico from png, create favicon | `references/favicon-generator.md` | Generate favicon.ico from neutral.png mascot using Python |
| math, equations, latex, mathjax, katex | `references/mkdocs-features.md` | Add math equation support |
| feature checklist, generate feature checklist, feature status, what features | `references/feature-checklist-generator.md` | Auto-detect and document implemented features |
| quiz, quizzes, assessment, multiple choice | `references/mkdocs-features.md` | Add interactive quizzes |
| feedback, thumbs up, thumbs down, was this helpful | `references/mkdocs-features.md` | Add page feedback widget |
| comments, giscus, discussions | `references/mkdocs-features.md` | Add comment system |
| image zoom, lightbox, glightbox, click to enlarge | `references/mkdocs-features.md` | Add image zoom on click |
| code highlighting, syntax, copy button | `references/mkdocs-features.md` | Add code syntax highlighting |
| mermaid, diagrams, flowchart | `references/mkdocs-features.md` | Add Mermaid diagram support |
| admonition, callout, prompt box, copy prompt | `references/mkdocs-features.md` | Add custom admonitions with copy |
| mascot, learning mascot, pedagogical agent, character, guide character, persona | `references/learning-mascot.md` | Add a learning mascot to guide students |
| instructor guide, teacher guide, teachers guide, instructor's guide, classroom guide | `references/instructors-guide.md` | Generate comprehensive instructor's guide |
| 404, error page, not found, custom 404, page not found | `references/custom-404-page.md` | Add custom 404 page with mascot |
| document status, page status, status indicators, status dots, nav status, page lifecycle, review workflow | `references/document-status.md` | Add colored status dots to nav sidebar |
| kanban, project board, kanban board, project management, github project, task board, milestones, 34 | `references/kanban-board.md` | Create GitHub Projects Kanban board for textbook development |
| mascot chapter, update chapter, retrofit mascot, place mascot, add mascot to chapter, 35 | `references/mascot-chapter-updater.md` | Retrofit an existing chapter with mascot admonitions using placement rules |
| mascot placement rules, mascot rules, how often mascot, mascot frequency, which mascot pose, mascot admonition guidelines | `references/mascot-placement-rules.md` | **Canonical** single-source rules for when/how often each mascot pose is used (read, never restate) |
| about page, about, about.md, about this book, author bio, cite this book, citation, 36 | `references/about-page.md` | Generate professional about page with motivation, bio, and citations |
| slide generator, slides, slide deck, slide viewer, presentation, generate slides, install slide viewer, 37 | `references/slide-generator.md` | Install the slide-viewer MicroSim and generate slides.md decks for chapters |
| reading level, readability, flesch kincaid, grade level, reading analysis, 38 | `references/reading-level-analysis.md` | Analyze chapter reading level consistency |
| generate all supplementary content, supplementary content, complete the book, finish the book, book completion, generate glossary faq quiz, generate all content, all supplementary, 39 | `references/supplementary-content-generator.md` | Generate glossary, FAQ, per-chapter quizzes & references, book metrics, diagram reports, about page, landing page, and README in one coordinated workflow |
| book metrics, generate metrics, book-metrics, chapter metrics, content statistics, word count, page count, equivalent pages, book composition, metrics report, 40 | `references/book-metrics.md` | Generate book-metrics.md, chapter-metrics.md, and the metrics block in book-metadata.json via bk-generate-book-metrics |

### Decision Tree

```
Asking for help or what book-installer can do?
  → YES: Display numbered list directly (Step 1)

Creating a new project/textbook from scratch (empty directory)?
  → YES: init-textbook.md (feature 0 — the canonical scaffold)

Registering the book with Google Analytics (GA4 / G-* Measurement ID)?
  → YES: google-analytics.md

Adding a learning graph viewer to existing project?
  → YES: learning-graph-viewer.md

Setting up skill usage tracking?
  → YES: skill-tracker.md

Want to GENERATE a high-quality cover image prompt from the book's content?
  → YES: cover-image-generator.md (prompt is the default output; auto-generation via API/ChatGPT only runs if explicitly requested)

Creating a cover image MANUALLY or setting up home page with social metadata?
  → YES: home-page-template.md

Installing the social media preview hook (og:* / twitter:* meta tags) or
fixing a failing bk-check-social-cover run?
  → YES: social-media-preview.md (Cairo-free; this is the default approach)

Want to generate a feature checklist showing what's implemented?
  → YES: feature-checklist-generator.md

Want to GENERATE a favicon.ico automatically from the mascot's neutral.png?
  → YES: favicon-generator.md (runs scripts/generate-favicon.py via Python/Pillow)

Want to add branding (logo, favicon, cover image)?
  → YES: mkdocs-features.md (Branding Features section)

Want to add a learning mascot (pedagogical agent) to guide students?
  → YES: learning-mascot.md

Want to generate an instructor's/teacher's guide?
  → YES: instructors-guide.md

Want a custom 404 error page with the mascot?
  → YES: custom-404-page.md

Want to add colored status dots to the nav sidebar for page lifecycle tracking?
  → YES: document-status.md

Want a GitHub Projects Kanban board to track textbook development?
  → YES: kanban-board.md

Want to retrofit an existing chapter with mascot admonitions?
  → YES: mascot-chapter-updater.md

Want to generate a professional about page with author bio and citations?
  → YES: about-page.md

Want to install a slide viewer and generate slide decks for chapters?
  → YES: slide-generator.md

Want to analyze reading level consistency across chapters?
  → YES: reading-level-analysis.md

Want to generate all supplementary content in one pass (glossary, FAQ, per-chapter quizzes & references, book metrics, diagram reports, about page, landing page, README)?
  → YES: supplementary-content-generator.md

Want to generate book metrics only (chapters, concepts, word/page counts,
diagram/MicroSim/quiz totals) into book-metrics.md and chapter-metrics.md?
  → YES: book-metrics.md

Want to add a specific feature (equations, quizzes, feedback, etc.)?
  → YES: mkdocs-features.md (then follow specific feature instructions)
```

## Step 2: Load the Matched Guide

Read the corresponding guide file from `references/` and follow its installation workflow.

## Step 3: Execute Installation

Each guide contains:
1. Prerequisites and requirements
2. Step-by-step installation commands
3. Configuration options
4. Verification steps
5. Troubleshooting tips

## Available Installation Guides

### mkdocs-features.md

**Purpose:** Detailed configuration for all MkDocs feature enhancements

**Contains:** Full configuration snippets for features 2-24 listed in the help output, including:
- YAML for mkdocs.yml
- JavaScript files to create
- CSS files to create
- Usage examples

**Use when:**
- User selects a feature by number or name
- User wants detailed configuration for a specific feature
- User has a minimal mkdocs.yml and wants to enrich it

### init-textbook.md (feature 0)

**Purpose:** The canonical scaffold for a brand-new intelligent textbook in an empty directory

**Creates:**
- mkdocs.yml (side nav, search, admonitions, arithmatex, exclude_docs, schema URI)
- docs/ tree: index, about, course-description, contact, license, chapters/, learning-graph/, sims/, css/extra.css, img/ (cover + license badge)
- CONTENT-GENERATION-GUIDE.md (CIS-driven word-count targets, anti-padding rules, MicroSim and Markdown rules — read by book-chapter-generator and chapter-content-generator)
- plugins/social_override.py hook (per-page og:/twitter: image override)
- .gitignore and VS Code workspace file
- MicroSim status-indicator plumbing (scaffold/built/approved)

**Templates:** single canonical copy in `assets/init-textbook/`

**Prerequisites:**
- Empty (or nearly empty) project directory — refuses to overwrite mkdocs.yml, docs/index.md, or docs/license.md

### google-analytics.md (feature 25)

**Purpose:** Register the book as a Google Analytics 4 property and wire the Measurement ID into mkdocs.yml

**Creates:**
- GA4 property + web data stream (via Claude in Chrome)
- `extra.analytics` block in mkdocs.yml with the G-* Measurement ID
- Build-time tag verification, commit, and gh-deploy

**Prerequisites:**
- Claude in Chrome extension connected; user logged into Google Analytics
- site_url set in mkdocs.yml

### learning-graph-viewer.md

**Purpose:** Add interactive learning graph exploration to existing textbook

**Creates:**
- Interactive vis-network graph viewer
- Search, filtering, and statistics features
- Integration with existing learning-graph.json

**Prerequisites:**
- Existing MkDocs project
- learning-graph.json file present

### skill-tracker.md

**Purpose:** Set up Claude Code skill usage tracking

**Creates:**
- Hook scripts for tracking skill invocations
- Activity log directory structure
- Reporting scripts for usage analysis

**Prerequisites:**
- Claude Code installed
- ~/.claude directory exists

### social-media-preview.md

**Purpose:** Install a Cairo-free MkDocs hook that emits Open Graph and Twitter Card meta tags on every page

**Creates:**
- `plugins/social_override.py` — `on_post_page` hook that injects/replaces `og:title`, `og:description`, `og:image`, `og:type`, `og:url`, and `twitter:*` tags
- `hooks:` block in `mkdocs.yml` referencing the new file

**Features:**
- Reads `image:`, `title:`, `description:` from each page's frontmatter; falls back to `img/cover.png` and the site-wide values
- Emits absolute `og:image` URLs by joining `site_url` with the image path (so crawlers and `bk-check-social-cover` can HEAD-request them)
- Works without `mkdocs-material[imaging]` / Cairo — the common-case default
- Compatible with the full `social` plugin when Cairo is present: replaces its auto-generated `/assets/images/social/...` URLs with the declared `cover.png`
- Verified via `~/.local/bin/bk-check-social-cover` (which enforces `og:image` basename = `cover.png` and image reachability)

**Prerequisites:**
- Existing MkDocs Material project with `site_url:` set
- `docs/img/cover.png` (use `cover-image-generator.md` or `home-page-template.md` first if missing)
- Home page frontmatter with `title:` and `description:` (typically from `home-page-template.md`)

### home-page-template.md

**Purpose:** Create professional home page with cover image and social media optimization

**Creates:**
- docs/index.md with proper frontmatter metadata
- AI image generation prompts for cover with montage background
- Open Graph and Twitter Card configuration

**Features:**
- Cover image design guidance (1.91:1 aspect ratio)
- Montage element suggestions by topic
- Social media preview optimization
- Example prompts for various book themes

**Prerequisites:**
- Existing MkDocs project
- Access to AI image generator (DALL-E, Midjourney, etc.)

### learning-mascot.md

**Purpose:** Design and implement a pedagogical agent (learning mascot) that guides students through the textbook

**Creates:**
- Character design (name, species, appearance, personality, catchphrase)
- AI image generation prompts for consistent mascot poses
- Implementation via inline images, custom CSS admonitions, or JavaScript auto-detection
- A mascot test page with automated transparency/4 px trim checks and all seven admonition previews
- CONTENT-GENERATION-GUIDE.md character guidelines for consistent AI-generated content, with the placement rules rendered from `references/mascot-placement-rules.md`

**Features:**
- Subject-specific mascot suggestions with reasoning
- Seven standard pose variants (neutral, welcome, thinking, tip, warning, encouraging, celebration)
- Three implementation methods at different complexity levels
- Restraint guidelines to prevent overuse

**Prerequisites:**
- Existing MkDocs Material project
- Access to AI image generator (DALL-E, Midjourney, etc.)

### instructors-guide.md

**Purpose:** Generate a comprehensive instructor's/teacher's guide for the textbook

**Creates:**
- `docs/teachers-guide/index.md` (or `docs/instructors-guide/index.md` for college-level)
- Navigation entry in mkdocs.yml

**Features:**
- Five levels of intelligent textbooks explained
- Detailed usage instructions for chapters, MicroSims, glossary, FAQ, quizzes, and references
- Classroom tips (before/during/after class suggestions, pacing)
- MicroSim iframe embedding guide for external LMS pages
- Creative Commons license explained in plain English (what you can/cannot do)
- Step-by-step customization guide (fork, clone, change colors/title/logo, deploy)
- Google Analytics setup instructions
- xAPI/LRS overview with FERPA/COPPA/GDPR regulatory warnings
- Learning graph usage tips for teachers
- Pedagogical agent (mascot) documentation (if mascot exists)
- All technical terms defined before use — no assumed prior knowledge

**Prerequisites:**
- Existing MkDocs Material project
- At least some chapter content written

### custom-404-page.md

**Purpose:** Add a custom 404 error page featuring the project's learning mascot

**Creates:**
- `overrides/404.html` — Jinja2 template extending Material base theme with mascot image, friendly message, and home link
- mkdocs.yml updates for `custom_dir` and `static_templates`

**Features:**
- Uses the mascot's warning pose (or other pose) centered on the page
- Inherits full site navigation (header, sidebar, footer) from the Material theme
- Customizable message matched to the mascot's personality and voice
- Absolute image paths so the 404 works from any URL depth

**Prerequisites:**
- Existing MkDocs Material project
- Learning mascot images in `docs/img/mascot/` (use `learning-mascot.md` first if needed)

### document-status.md

**Purpose:** Add per-page colored status dots to the navigation sidebar for tracking page lifecycle state

**Creates:**
- `extra.status` configuration in mkdocs.yml
- CSS rules for colored status dots in extra.css
- `status:` frontmatter on individual pages

**Features:**
- Three-state workflow (spec-complete → prototype → ready-for-testing)
- Colored dots (red, orange, green) visible in the nav sidebar
- Tooltip text on hover
- Customizable status codes for any workflow

**Prerequisites:**
- Existing MkDocs Material project
- Custom CSS file referenced in `extra_css`

### reading-level-analysis.md

**Purpose:** Analyze Flesch-Kincaid grade level consistency across all chapters

**Creates:**
- `docs/learning-graph/chapter-reading-levels.md` — per-chapter reading level report

**Uses script:** `scripts/analyze-reading-levels.py`

**Features:**
- Strips markdown/HTML formatting to analyze pure prose
- Per-chapter table with FK grade and explanatory notes
- Summary statistics (mean, median, range, standard deviation)
- Interpretation section explaining whether variation is meaningful
- Identifies vocabulary-driven score inflation vs. genuine difficulty differences

**Prerequisites:**
- Existing MkDocs project with chapters in `docs/chapters/`
- Python `textstat` library (`pip install textstat`)

### book-metrics.md

**Purpose:** Generate comprehensive book-wide and per-chapter metrics for an intelligent textbook

**Creates:**
- `docs/learning-graph/book-metrics.md` — Book Composition + Student-Facing Content Metrics tables
- `docs/learning-graph/chapter-metrics.md` — per-chapter breakdown
- merges a `metrics` block of book-wide totals into `docs/learning-graph/book-metadata.json` (author fields preserved)

**Uses script:** `bk-generate-book-metrics` (resolves `$BK_HOME/src/book-metrics/book-metrics.py`); fallback `python3 "$BK_HOME/src/book-metrics/book-metrics.py" docs`

**Features:**
- Tracks all 12 book-composition elements with Required/Recommended/Optional status
- Counts concepts, chapters, MicroSims, stories, glossary terms, FAQs, quiz questions, references, diagrams, equations, words, links, appendices, mascot poses
- Estimates equivalent printed pages and records the development stage
- Produces the totals the intelligent-textbooks case-studies index displays

**Prerequisites:**
- Existing MkDocs project with chapters in `docs/chapters/`
- `$BK_HOME` exported and `bk-generate-book-metrics` on `$PATH`

### favicon-generator.md

**Purpose:** Generate a web-compliant multi-resolution `favicon.ico` from the mascot's `neutral.png`

**Creates:**
- `docs/img/favicon.ico` — multi-resolution icon (16, 32, 48, 64, 128, 256 px) embedded in a single `.ico` file

**Uses script:** `scripts/generate-favicon.py`

**How it works:**
- Detects the bounding box of non-transparent pixels (trims invisible padding)
- Centers the visible content on a square canvas with configurable padding
- Downscales to each favicon size using Lanczos resampling
- Supports transparent or white background canvas

**Prerequisites:**
- Mascot image at `docs/img/mascot/neutral.png` (image need not be square)
- Python `Pillow` library (`pip install Pillow`)

### cover-image-generator.md

**Purpose:** Craft a high-quality cover image prompt at `docs/img/cover-image-prompt.md`, built from the book's title, course description, concept list, mascot, and MicroSim screenshots. Image auto-generation is optional and only runs if the user explicitly asks for it.

**Provides:**
- Guidance for selecting 6-10 montage concepts from the book's own content
- A detailed prompt template covering subject/tone, title typography, montage, mascot, style/color, and things to avoid
- Recommended manual review loop: paste the prompt into a text-to-image tool, compare drafts, iterate on the prompt before finalizing
- Optional automated paths (API, browser automation, or local-prompt) with troubleshooting — only used on explicit request

**Prerequisites:**
- Existing MkDocs project with mkdocs.yml
- docs/course-description.md with book content description
- Only if auto-generation is requested: OpenAI API billing, ChatGPT Pro subscription, or a free AI image generator

### kanban-board.md

**Purpose:** Create a GitHub Projects (v2) Kanban board for tracking textbook development progress

**Creates:**
- GitHub Projects board with Board (Kanban) layout
- Priority field (High / Medium / Low)
- 13 standard textbook milestone draft items
- `docs/project-management.md` with column documentation and workflow guide
- README section about the Kanban board

**Features:**
- Automated setup via `gh project` CLI commands
- Links project to the repository automatically
- Pre-populated milestones matching the 12-step textbook workflow
- Fallback instructions for manual setup if `gh` commands fail

**Prerequisites:**
- `gh` CLI installed and authenticated
- `project` scope on the GitHub token (`gh auth refresh -s project`)
- Existing MkDocs project with mkdocs.yml

### supplementary-content-generator.md

**Purpose:** Generate all standard supplementary content for an intelligent textbook in a single coordinated workflow

**Produces (in execution order):**
- `docs/about.md` — professional about page (via `about-page.md` reference)
- `docs/glossary.md` — ISO 11179-compliant glossary (via `glossary-generator` skill)
- `docs/faq.md` — ≥ 30-question FAQ (via `faq-generator` skill)
- `docs/chapters/*/quiz.md` — per-chapter quizzes (via `quiz-generator` skill)
- `docs/chapters/*/references.md` — per-chapter reference lists (via `reference-generator` skill)
- `docs/img/cover.png` — book cover image + social-preview hook (via `cover-image-generator.md` + `social-media-preview.md`)
- Book metrics report (via `bk-generate-book-metrics` script)
- Diagram reports (via `bk-diagram-reports` script)
- `README.md` — GitHub-facing README after metrics, so it can embed content counts (via the `book-publisher` readme route — skill)
- `docs/index.md` — main landing page last, so it can link to all of the above (via `home-page-template.md`)
- Updated `mkdocs.yml` nav entries for all generated files

**Execution order:** about → glossary → FAQ → quizzes → references → cover image → metrics → diagram reports → README → landing page → nav update → verification

**Model guidance:** All text-generation steps use Sonnet. Any MicroSim created during this workflow must use `claude-opus-4-7` with `high` thinking — Opus is significantly better at the coding and spatial reasoning MicroSims require.

**Prerequisites:**
- Existing MkDocs project with `mkdocs.yml`
- `docs/course-description.md` present
- `docs/learning-graph/learning-graph.json` present
- At least one chapter under `docs/chapters/`

### slide-generator.md

**Purpose:** Install the slide-viewer MicroSim into an intelligent textbook project and generate presentation-style `slides.md` decks for specified chapters

**Creates:**
- `docs/sims/slide-viewer/` — viewer shell (main.html, script.js, local.css, index.md) that fetches any rendered MkDocs page URL, splits its content on `<hr>` elements, and renders one slide at a time with keyboard + button navigation
- `docs/chapters/<slug>/slides.md` — per chapter: title slide, content slides separated by `---`, retrieval check, bridge, celebration close
- Three-button nav bar (`Content`, `Slides`, `Slides in Viewer`) at the top of each chapter's `index.md` and its `slides.md`
- mkdocs.yml nav restructured so each chapter with slides has `Content` / `Slides` sub-entries

**Features:**
- Viewer reads MkDocs' rendered HTML (never raw `.md` — MkDocs doesn't serve `.md` directly)
- Mascot integration: neutral pose on every slide, celebration pose on the last slide (uses `docs/img/mascot/neutral.png` and `celebration.png` if present; silently absent otherwise)
- First/last-slide jump buttons, `Home`/`End` keys, fullscreen, table-of-contents overlay
- Distills chapter `index.md` into 15–28 slides following project voice/style rules

**Prerequisites:**
- Existing MkDocs Material project with `docs/chapters/` populated
- Chapter `index.md` files with real content (not just scaffold) — guide checks line counts before generating
- Optional: mascot installed via `learning-mascot.md`

### mascot-placement-rules.md

**Purpose:** The single source of truth for when a learning mascot may appear, how often, and which pose carries which pedagogical job

**Used by:** `learning-mascot.md`, `mascot-chapter-updater.md`, `instructors-guide.md`, and the `chapter-content-generator` skill — all of which reference this file rather than restating its rules

**Contains:**
- The admonition format and the Markdown-vs-raw-HTML image path rules
- The placement table (context → pose → per-chapter count)
- Hard limits: fewer than 10 admonitions per chapter, no back-to-back placement, one welcome and one celebration, 1-3 sentence bodies
- Per-pose instructional-design rules for all seven poses
- The one-time Chapter 1 self-introduction pattern
- The post-generation validation rule

**Important:** never copy this file's tables or counts into another skill or into a book by hand. Skills reference it by path; books receive a rendered copy via `scripts/render-mascot-guide.py`, spliced between sentinel comments so it can be regenerated. Run `scripts/bk-check-mascot-rules` from the repo root to verify no restatement has crept back in.

### mascot-chapter-updater.md

**Purpose:** Retrofit an existing chapter markdown file with mascot admonitions in the right places, following the canonical `references/mascot-placement-rules.md`

**Creates:**
- In-place edits to the specified chapter file only (no new files)
- A placement plan shown to the user for confirmation before editing

**Features:**
- LLM-driven workflow for semantic placement (no regex auto-insertion)
- Enforces the hard limits defined in `references/mascot-placement-rules.md` (total ceiling, one welcome and one celebration maximum, no back-to-back placements)
- Image-path guidance for directory-URL rendering (counts `../` from rendered page)
- Voice and body-text rules: 1-3 sentences, in-character, specific to chapter content
- Validation via `scripts/validate-chapter-mascots.py` that flags count limits, back-to-backs, missing mascot images, and body-text length

**Prerequisites:**
- Mascot images present in `docs/img/mascot/` or `docs/img/mascots/`
- `docs/css/mascot.css` loaded and the mascot-test page renders correctly
- Specific chapter file identified by absolute path

## Examples

### Example 1: Ask for Help
**User:** "book-installer help"
**Routing:** Keyword "help" → Display numbered list
**Action:** Show the numbered feature list (Step 1), then wait for user to select a feature

### Example 2: Add a Specific Feature
**User:** "Add math equation support to my book"
**Routing:** Keyword "math" → `references/mkdocs-features.md`
**Action:** Load mkdocs-features.md, find the Math Equations section, and apply the configuration

### Example 2b: Select by Number
**User:** "5"
**Routing:** Number selection after help list → `references/mkdocs-features.md`
**Action:** Load mkdocs-features.md, find Math Equations (item 5), and apply the configuration

### Example 2c: Simple Template
**User:** "1"
**Routing:** Number 1 → `references/init-textbook.md` (canonical scaffold)
**Action:** Load init-textbook.md and scaffold the starter config and docs/ tree

### Example 3: New Textbook Project
**User:** "I want to create a new intelligent textbook about machine learning" (empty directory)
**Routing:** Keywords "create", "new", "textbook" → `references/init-textbook.md`
**Action:** Read init-textbook.md, gather SITE_NAME/SITE_DESCRIPTION, confirm the substitution table, scaffold from `assets/init-textbook/`

### Example 3b: Register Google Analytics
**User:** "Add Google Analytics to this book" or "25"
**Routing:** Keywords "google analytics", "GA4", "25" → `references/google-analytics.md`
**Action:** Read google-analytics.md; create the GA4 property, write the G-* ID into mkdocs.yml extra.analytics, verify the tag, deploy

### Example 4: Add Graph Viewer
**User:** "Add an interactive viewer for the learning graph"
**Routing:** Keywords "viewer", "learning graph", "interactive" → `references/learning-graph-viewer.md`
**Action:** Read learning-graph-viewer.md and follow its workflow

### Example 5: Track Skill Usage
**User:** "I want to track which skills I use most often"
**Routing:** Keywords "track", "skills", "usage" → `references/skill-tracker.md`
**Action:** Read skill-tracker.md and follow its workflow

### Example 6: Create Cover Image
**User:** "Help me create a cover image for my textbook"
**Routing:** Keywords "cover image", "textbook" → `references/home-page-template.md`
**Action:** Read home-page-template.md and follow its workflow

### Example 7: Set Up Home Page with Social Sharing
**User:** "I need to add og:image metadata to my home page"
**Routing:** Keywords "og:image", "home page" → `references/home-page-template.md`
**Action:** Read home-page-template.md and follow its workflow

### Example 8: Generate Cover Image Prompt
**User:** "generate cover image" or "book-installer generate cover image"
**Routing:** Keywords "generate cover image" → `references/cover-image-generator.md`
**Action:** Read cover-image-generator.md, gather source material (title, course description, concept list, mascot, MicroSim screenshots), write `docs/img/cover-image-prompt.md`, and recommend the user paste it into a text-to-image tool and review drafts. Only ask about API key/ChatGPT Pro/macOS and run `generate-cover.sh` if the user explicitly requests auto-generation.

### Example 9: Add a Learning Mascot
**User:** "I want to add a mascot character to my math textbook"
**Routing:** Keywords "mascot", "character" → `references/learning-mascot.md`
**Action:** Read learning-mascot.md, guide user through character design, generate AI image prompts, and implement chosen method (inline, CSS admonitions, or JS detection)

### Example 10: Generate Feature Checklist
**User:** "generate a feature checklist" or "what features do I have"
**Routing:** Keywords "feature checklist" → `references/feature-checklist-generator.md`
**Action:** Read feature-checklist-generator.md, run the detection script, generate docs/feature-checklist.md with detected statuses

### Example 11: Generate Instructor's Guide
**User:** "add a teacher's guide" or "create instructor guide"
**Routing:** Keywords "teacher guide", "instructor guide" → `references/instructors-guide.md`
**Action:** Read instructors-guide.md, gather project variables from mkdocs.yml/course-description.md/CLAUDE.md, generate the guide with all variables substituted, add to navigation

### Example 12: Create Kanban Board
**User:** "set up a kanban board for my textbook" or "create a project board"
**Routing:** Keywords "kanban", "project board" → `references/kanban-board.md`
**Action:** Read kanban-board.md, verify gh auth with project scope, create the GitHub Project, link to repo, populate milestones, create docs/project-management.md, update nav and README

### Example 13: Generate About Page
**User:** "create an about page" or "add about.md with author bio and citations"
**Routing:** Keywords "about page", "about", "author bio", "citation" → `references/about-page.md`
**Action:** Read about-page.md, gather project variables from mkdocs.yml/course-description.md, generate docs/about.md with all sections (motivation, author bio, citation formats), add to navigation

### Example 14: Add Mascots to an Existing Chapter
**User:** "add Sparky admonitions to chapter 2" or "place the mascot in docs/chapters/02-ohms-law/index.md"
**Routing:** Keywords "mascot chapter", "place mascot", "add mascot to chapter" → `references/mascot-chapter-updater.md`
**Action:** Read mascot-chapter-updater.md, survey the chapter, propose a placement plan with line numbers, wait for user confirmation, apply edits, run validate-chapter-mascots.py, and address any flags

### Example 15: Generate Favicon from Mascot
**User:** "generate favicon from mascot" or "create favicon.ico from neutral.png"
**Routing:** Keywords "generate favicon", "mascot favicon", "favicon from mascot" → `references/favicon-generator.md`
**Action:** Read favicon-generator.md, verify `docs/img/mascot/neutral.png` exists and Pillow is installed, run `scripts/generate-favicon.py` from the project root, then update `theme.favicon` in mkdocs.yml to `img/favicon.ico`

### Example 15b: Install Social Media Preview Hook
**User:** "add the social media preview mkdocs hook" or "my bk-check-social-cover is failing" or "install og:image meta tags"
**Routing:** Keywords "social media preview", "og:image", "bk-check-social-cover", "social hook" → `references/social-media-preview.md`
**Action:** Read social-media-preview.md, create `plugins/social_override.py` at the project root with the exact code in the reference, add a top-level `hooks: - plugins/social_override.py` block to `mkdocs.yml`, run `mkdocs build`, verify the nine og:* / twitter:* meta tags appear in `site/index.html`, then run `bk-check-social-cover` against either the deployed URL or a local server staging the build under `/<project>/`

### Example 17: Generate All Supplementary Content
**User:** "generate all supplementary content" or "complete the book" or "39"
**Routing:** Keywords "supplementary content", "complete the book", "39" → `references/supplementary-content-generator.md`
**Action:** Read supplementary-content-generator.md. First inventory existing files. Then execute Steps 2–12 in order: generate about page, landing page, README, glossary, FAQ, per-chapter quizzes and references, run `bk-generate-book-metrics` and `bk-diagram-reports`, update mkdocs.yml nav, and run the verification bash check. Report which files were created, skipped, or missing.

### Example 16: Install Slide Viewer and Generate Chapter Slides
**User:** "install the slide viewer and make slides for chapters 1 and 2" or "generate slides for chapter 3"
**Routing:** Keywords "slide", "slides", "slide viewer", "generate slides", "slide deck" → `references/slide-generator.md`
**Action:** Read slide-generator.md, copy the slide-viewer assets into docs/sims/slide-viewer/, ask which chapters to generate decks for, create slides.md for each (title + content slides separated by `---` + retrieval check + bridge + celebration), add the three-button nav bar to each chapter's index.md, restructure the chapter's mkdocs.yml entry into Content/Slides sub-entries, and append deck links to the viewer's index.md

### Example 18: Generate Book Metrics
**User:** "generate book metrics" or "how many words/chapters/MicroSims does this book have" or "40"
**Routing:** Keywords "book metrics", "generate metrics", "metrics report", "40" → `references/book-metrics.md`
**Action:** Read book-metrics.md, run `bk-generate-book-metrics` from the project root (or the `python3 "$BK_HOME/src/book-metrics/book-metrics.py" docs` fallback), confirm `book-metrics.md`, `chapter-metrics.md`, and the `metrics` block in `book-metadata.json` were written, and add the two reports to the Learning Graph nav in `mkdocs.yml` if not already present.

## Common Workflows

### Full Project Setup
For a complete new project, users typically run these installations in order:
1. `init-textbook.md` - Scaffold the project structure (feature 0)
2. `cover-image-generator.md` - Generate a high-quality cover image prompt (auto-generation optional, on request)
3. `home-page-template.md` - Configure home page with cover image metadata
4. `social-media-preview.md` - Install the og:* / twitter:* meta-tag hook (verify with `bk-check-social-cover`)
5. `learning-graph-viewer.md` - Add graph visualization (after learning graph exists)
6. `skill-tracker.md` - Enable usage analytics (optional)
7. `google-analytics.md` - Register the book with GA4 (feature 25, optional)
8. `supplementary-content-generator.md` - Generate all supplementary content once chapters exist (glossary, FAQ, quizzes, references, metrics, about, README)

### Verification Commands

After any installation, verify with:
```bash
# For MkDocs projects
mkdocs serve
# Visit http://127.0.0.1:8000/[project-name]/

# For skill tracker
cat ~/.claude/activity-logs/skill-usage.jsonl | tail -5
```

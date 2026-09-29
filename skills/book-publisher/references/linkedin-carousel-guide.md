
# LinkedIn Carousel (Document Post) Guide

> Formerly the standalone skill `linkedin-carousel-generator`.

Generates a 13-slide LinkedIn carousel — LinkedIn calls this a **"document post"** — that
visually walks a reader through what makes an intelligent textbook worth exploring. Unlike
the `linkedin-post-guide.md` route (which writes the post's caption text), this skill produces
the **artifact itself**: a square, mobile-readable slide deck the reader swipes through in
their feed, built from the project's real metrics, mascot art, and screenshots.

## When to Use This Skill

Use this skill when the user says things like:
- "Make a LinkedIn carousel/slideshow for this textbook"
- "Create a LinkedIn document post"
- "I want a slide deck I can upload to LinkedIn"

Do **not** use this skill when the user wants only the caption/post text — use
the `linkedin-post-guide.md` route for that (the two are often used together: carousel as the
attached document, announcement text as the post copy, with the carousel referenced instead
of a bare link).

Do **not** use the book-media-generator pptx-lecture route for this — that route builds a 25-35 slide
**lecture deck** for live classroom delivery with speaker notes. This skill builds a much
shorter, image-heavy, no-speaker-notes deck meant to be read silently on a phone in a feed.

## Prerequisites

- Node.js installed, with `pptxgenjs` installed locally in the output directory
  (`npm install pptxgenjs`)
- An intelligent textbook project with:
  - `mkdocs.yml` (site name, description, theme palette)
  - `docs/about.md` (the "Why This Book" narrative)
  - `docs/learning-graph/book-metrics.json` (canonical metrics — see
    `book-installer`'s `bk-generate-book-metrics` if missing)
  - `docs/img/mascot/` with the character sheet and pose PNGs (see `book-installer`'s
    `learning-mascot` guide if the project has no mascot yet)
  - `docs/license.md` and `docs/img/license.png`
  - At least one MicroSim under `docs/sims/`, and (ideally) a learning-graph viewer
    MicroSim (commonly `docs/sims/graph-viewer/`)
- `~/.local/bin/bk-capture-screenshot` available (installed by `microsim-utils`) for the two
  screenshots this skill needs
- Python 3 with Pillow (`pip install pillow`) for cropping the learning-graph screenshot

If any prerequisite is missing, tell the user which one and point at the skill that creates
it rather than improvising a substitute (e.g. don't hand-draw a learning graph image if
`book-metrics.json` and a real graph viewer exist).

## The 13 Slides

| # | Slide | Content source | Image source |
|---|-------|-----------------|---------------|
| 1 | Cover | `mkdocs.yml` site_name / site_description | `docs/img/cover.png` (if present) + mascot `welcome.png` |
| 2 | Why This Book | `docs/about.md` → "Why This Intelligent Textbook" section | mascot `thinking.png` or `welcome.png`, floated left |
| 3 | Learning Graph | `docs/learning-graph/book-metrics.json` (concepts, taxonomy categories, edges) + `docs/learning-graph/index.md` | Zoomed crop of the graph-viewer MicroSim screenshot, floated right |
| 4 | Coverage Summary | Chapter count from `book-metrics.json` + 4-6 standout chapter titles from `mkdocs.yml` nav | Big-number treatment, no image needed |
| 5 | Engagement Strategy | The "Read → Run → Modify" Skulpt-lab cycle (or the project's equivalent hands-on loop) from `CLAUDE.md` / `CONTENT-GENERATION-GUIDELINES.md` | 3-icon row, deliberately NOT a wall of text |
| 6 | Mascot Summary | Mascot character sheet (`docs/img/mascot/character-sheet.md`) | Grid of pose PNGs with a 2-4 word role label under each |
| 7 | MicroSim Count | `microsims` count from `book-metrics.json` + one-sentence definition of "MicroSim" | Screenshot of one flagship MicroSim (confirm which one with the user) |
| 8 | Supplementary Content | `glossaryTerms`, `faqs`, `quizQuestions`, `references` counts from `book-metrics.json` | 4-icon stat row |
| 9 | License | `docs/license.md` license type | `docs/img/license.png` + note on customizing colors/logo/mascot for another school |
| 10 | Adaptivity | How Claude Skills add whole new chapters/lessons consistent with the existing book (course-description → learning-graph → chapter generators) | Simple pipeline diagram (3-4 boxes) |
| 11 | Continuous Enrichment | Forward-looking: agents proposing content/MicroSim variants, measured via analytics/A/B testing, phrased as a capability the framework *supports*, not a claim of an existing automated pipeline | Icon-based, light touch |
| 12 | Summary of Benefits | A recap checklist of the strongest points from slides 2-11 — the 5-6 most compelling facts, each condensed to a single bolded phrase (e.g. "450 concepts, 0 dependency violations", "31 interactive MicroSims", "Free & open source") | none — checklist pattern, no image needed |
| 13 | Closing CTA | Site URL, GitHub repo URL, "free & open source" | mascot `celebration.png`, dark background matching slide 1 |

This mapping is a strong default, not a rigid template — if the project lacks one of these
elements (no stories, zero equations, etc.), drop or substitute a slide rather than showing a
zero. See `references/carousel-content-sourcing.md` for the exact extraction commands for every slide.

**Slide 12 exists to close the loop before the CTA:** by slide 11 the reader has seen ten
different facts in ten different visual styles — slide 12 pulls the single strongest claim out
of each of slides 2-11 into one scannable list, so a reader who only skims gets the whole
pitch in five seconds before hitting the ask on slide 13. Pick the *best* fact per slide, not
every fact — this slide fails if it turns back into a wall of text.

## Workflow

### Step 1: Gather Source Material

Read, in parallel:
1. `mkdocs.yml` — `site_name`, `site_description`, `site_url`, `repo_url`, and
   `theme.palette.primary` / `theme.palette.accent` (drives every slide's color scheme)
2. `docs/about.md` — pull the "Why This Book" / "Why This Intelligent Textbook" section
3. `docs/learning-graph/book-metrics.json` — the canonical metrics object (same file
   the `linkedin-post-guide.md` route and the `readme-guide.md` route use — keep numbers consistent
   across all three artifacts)
4. `docs/img/mascot/character-sheet.md` — name, species, and the pose table
5. `docs/learning-graph/color-config.json` (if present) — taxonomy category colors, used as
   a small legend on the learning-graph slide
6. `docs/license.md` — license type and URL
7. `mkdocs.yml` nav — chapter list, to hand-pick 4-6 standout titles for slide 4

If `book-metrics.json` is missing or stale, regenerate it first (`bk-generate-book-metrics`)
rather than estimating numbers.

### Step 2: Capture the Two Required Screenshots

**Learning graph (slide 3):** Run `bk-capture-screenshot` against the graph-viewer MicroSim
(commonly `docs/sims/graph-viewer/`) at a large window size so labels are legible when cropped:

```bash
~/.local/bin/bk-capture-screenshot docs/sims/graph-viewer
```

The full-graph screenshot shows all concepts at once — too dense to read at slide/thumbnail
size. Crop to a readable cluster of 15-25 nodes that shows concept labels and a spread of
taxonomy colors, using `scripts/crop-screenshot.py`:

```bash
python3 scripts/crop-screenshot.py docs/sims/graph-viewer/graph-viewer.png \
  linkedin/slides/learning-graph-zoom.png --box 300,200,1400,1000
```

Adjust the `--box left,top,right,bottom` coordinates by opening the full screenshot first —
don't guess blindly. If no crop region looks clean (e.g. the graph is too sparse or labels
overlap everywhere), fall back to asking the user to manually pan/zoom the live viewer in a
browser and take their own screenshot.

**Flagship MicroSim (slide 7):** Ask the user which MicroSim best represents the book if it
isn't obvious (prefer one with strong visuals — turtle graphics, a chart, a network — over a
plain form-based one), then:

```bash
~/.local/bin/bk-capture-screenshot docs/sims/<chosen-microsim>
```

### Step 3: Confirm the Outline Before Generating

Before writing any slide code, show the user:
- The 13-slide plan with the specific numbers it will display (e.g. "38 chapters, 450
  concepts, 31 MicroSims, 338 glossary terms")
- Which chapters you picked to highlight on slide 4
- Which MicroSim you picked for slide 7
- Which 5-6 facts you picked for the slide 12 benefits recap

This is a quick sanity check, not a full design review — the numbers are objective (pulled
from `book-metrics.json`), but the chapter/MicroSim/recap picks are subjective and worth a
10-second confirmation before building 13 slides around them.

### Step 4: Set Up the pptxgenjs Project

```bash
mkdir -p linkedin
cd linkedin && npm install pptxgenjs
```

Use a **square 10in x 10in slide** (`pptx.defineLayout({name:'SQUARE', width:10, height:10})`)
— LinkedIn document posts render best at 1:1 on mobile feeds. If the user prefers the taller
4:5 format some carousels use, use `width:8, height:10` instead; confirm with the user only if
they express a preference, otherwise default to square.

### Step 5: Build Each Slide

Read `references/carousel-slide-patterns.md` for the nine reusable pptxgenjs slide patterns (title/
cover, mascot-aside, image-aside, big-numbers, icon-row, pose-grid, badge-callout, checklist
recap, closing CTA) and `references/carousel-content-sourcing.md` for exactly which field feeds which
slide. Map the 13 slides in the table above onto these patterns — several slides reuse the
same pattern with different content (e.g. slides 2, 3, 9 are all variants of "image on one
side, text on the other").

**Design rules — LinkedIn carousels are read on a phone, not projected:**
- No more than ~25 words of body text per slide (this is a stricter cap than a lecture deck)
- Minimum 18pt body text, 36pt+ for headlines — small text is illegible in the LinkedIn
  in-feed thumbnail
- One idea per slide, always
- Dark background (primary color) for slides 1 and 13 only — bookends the deck; slides 2-12
  stay light/white for readability and print/PDF friendliness
- Use the project's actual `theme.palette.primary` / `accent` from `mkdocs.yml`, not generic
  blues

### Step 6: Generate and Verify

1. Run the Node.js script to produce the `.pptx`
2. Confirm exactly 13 slides were produced
3. Open each slide (or export slide 1, 3, 6, 7, 12, and 13 as PNGs) and visually check that no
   text overflows its box and that images aren't stretched or pixelated
4. Report slide count and file size to the user

### Step 7: Prepare for LinkedIn Upload

LinkedIn's document-post uploader (the icon in "Start a post" that looks like a page/document,
distinct from the photo icon) accepts `.pptx`, `.ppt`, `.pdf`, `.doc`, and `.docx` directly —
**no PDF conversion is required.** If the user wants a smaller file or to strip editable
metadata before sharing, offer to convert with LibreOffice if it's installed:

```bash
soffice --headless --convert-to pdf --outdir linkedin linkedin/<kebab-title>-carousel.pptx
```

Tell the user LinkedIn will also ask for a **document title** shown above the carousel in the
feed — suggest a short, benefit-led title (e.g. "13 Things That Make This Python Textbook
Different"), not the book's formal title.

Remind the user of the same rule from the `linkedin-post-guide.md` route: the **post caption**
should not contain the external site link (LinkedIn suppresses reach on posts with links in the
body) — but a URL printed as **text on slide 13 of the document itself** is fine, since it's
not a clickable hyperlink in the post body. If they're also posting caption text, hand off to
the `linkedin-post-guide.md` route and tell them to paste the site URL as the first comment,
same as always — with UTM tags (see "UTM tagging" in that guide; use
`utm_content=carousel` to distinguish it from a text-only post). The URL printed on slide 13
is not clickable, so it needs no tags.

## Output

```
{project-root}/linkedin/
├── generate.js                       # pptxgenjs generation script
├── <kebab-title>-carousel.pptx       # the deliverable
└── slides/
    ├── learning-graph-zoom.png       # cropped learning-graph screenshot
    └── microsim-preview.png          # flagship MicroSim screenshot
```

Keep this directory outside `docs/` (sibling to it, like `presentation/` in
the pptx-lecture route) so MkDocs never tries to build it into the site.

## Quality Checklist

- [ ] Exactly 13 slides
- [ ] Every number on every slide traces back to `book-metrics.json` (no invented stats)
- [ ] Learning-graph image is a legible zoomed crop, not the full dense graph
- [ ] Mascot poses shown match the character sheet's actual pose set
- [ ] Colors match the project's `mkdocs.yml` theme palette
- [ ] No slide exceeds ~25 words of body text
- [ ] Body text is 18pt+ everywhere
- [ ] Slide 12's benefits recap pulls one strongest fact per prior slide, not every fact
- [ ] Slide 13 has a clear URL and call to action
- [ ] File opens cleanly in PowerPoint/Keynote/Google Slides with no broken image links

## Troubleshooting

**Issue:** Learning-graph screenshot is blank or shows a loading spinner
**Solution:** The graph-viewer MicroSim needs more render time — see
`microsim-utils`'s `screen-capture` reference for increasing the timeout.

**Issue:** Cropped learning-graph image still looks too dense to read
**Solution:** Increase the screenshot's `--window-size` before cropping (more native pixels
per node), or ask the user to manually zoom the live viewer and screenshot that.

**Issue:** `book-metrics.json` is missing
**Solution:** Run `bk-generate-book-metrics` (via `book-installer`) before proceeding —
don't estimate or recount content by hand.

**Issue:** Project has no mascot yet
**Solution:** Point the user at `book-installer`'s `learning-mascot` guide first; slides 2
and 6 depend on mascot art existing.

## Related Skills

- **linkedin-post-guide.md** (this skill) — writes the post caption text; often paired with this
  skill's carousel as the attached document
- **book-media-generator → pptx-lecture** — the long-form lecture-deck sibling; reuse its
  pptxgenjs setup patterns but not its 25-35 slide scope or speaker-notes step
- **microsim-utils** (screen-capture reference) — the `bk-capture-screenshot` tool this skill
  depends on for slides 3 and 7
- **book-installer** (learning-mascot, book-metrics guides) — creates the mascot art and
  metrics file this skill reads
- **readme-guide.md** (this skill) — another consumer of the same `book-metrics.json`, useful for
  cross-checking that numbers stay consistent across all generated artifacts

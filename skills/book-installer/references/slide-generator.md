---
name: install-slide-generator
description: Installs the slide-viewer MicroSim into an intelligent textbook project and generates presentation-style slide decks (slides.md) for specified chapters from their index.md content. Use this skill when the user wants slide decks for one or more chapters of a textbook.
---
# Install Slide Generator

## Step 0 (REQUIRED): Surface the Known Trade-offs to the User Before Doing Anything

**Before running any command in this guide, Claude MUST paste the following caveat to the user and ask them to confirm they still want to proceed.** Do not skip this step, even if the user's request sounds eager and specific. The trade-offs below are real, and users who invoke this skill often have not thought them through. Presenting them up front is the difference between being a helpful collaborator and being an obedient slide factory.

Paste this block verbatim (it is short on purpose):

> **Before we generate slide decks, a few skeptical notes:**
>
> 1. **Two sources of truth drift silently.** Once a chapter has both `index.md` and `slides.md`, editing the chapter does not update the deck, and MkDocs gives no warning when they diverge. Readers on the Slides view silently consume a stale chapter.
> 2. **Slides are a different medium, not a projection.** Auto-distilled slides tend to be either paragraph-dense (unreadable in a room) or skeletal (useless without a presenter). Neither is actually a presentation.
> 3. **There may be no real audience.** Textbooks are read asynchronously; slide decks imply a synchronous setting that may never happen. If nobody presents from the decks, the authoring and maintenance cost is pure overhead.
> 4. **The pattern can contradict the book's own pedagogy.** If the textbook teaches that retrieval beats re-reading, giving readers a slide summary of each chapter is a form of re-reading that produces a fluency illusion without the encoding benefit.
> 5. **Maintenance cost scales linearly with chapter count, value may not.** Every deck adds nav entries, a three-button bar, a viewer query string with its own path-depth gotchas, and four independent fragility surfaces (viewer JS, `<hr>` separators, directory-URL rewriting, mascot image paths).
>
> **Recommendation:** start with one or two flagship chapters, instrument whether the viewer is actually opened (Google Analytics or similar), and only generalize if the data supports it. Retrieval prompts, flashcards, and MicroSims often give better pedagogical return on the same authoring budget.
>
> **Do you still want to proceed with slide generation? If yes, which chapters — and do you have a specific audience/use case for the decks?**

After presenting this block:

- If the user says "yes, proceed" with a specific chapter list and audience, continue to Step 1.
- If the user says "yes for all chapters," gently push back once — suggest piloting on one or two chapters first — and then defer to their judgment.
- If the user says "no" or "let me think," stop and do not install anything.
- If the user redirects to a different deliverable (retrieval prompts, flashcards, a quiz), route them to the appropriate skill instead.

Full written analysis: see any `logs/slide-tradeoffs.md` the project may have, or regenerate the same reasoning on request.

## Overview

This guide does two things:

1. **Installs the slide-viewer MicroSim** into `docs/sims/slide-viewer/` by copying four template files. The viewer fetches any rendered MkDocs page URL, splits the page's content on `<hr>` elements, and renders each chunk as a slide.
2. **Generates a `slides.md` deck** for each chapter the user specifies, distilling the chapter's `index.md` into a presentation with a title slide, content slides separated by `---`, and a closing celebration slide.

Total install time: under 2 minutes for the viewer. Generating slides for a chapter typically takes one pass per chapter (the content summarization is an LLM task, not a script).

## Viewer Version

Current template version: **v0.01**.

When you ship a behavior change to the viewer templates, bump the version in **three** places:

1. The version in this file (the line above).
2. `references/assets/slide-viewer/main.html` — the `<div id="viewer-version">v0.01</div>` line.
3. The changelog entry below.

### Changelog

- **Guide update (no viewer version bump)** — Moved the chapter-index slide links from the top of `index.md` to the end, under a `## Slides for this chapter` heading separated by a horizontal rule. Slides are a secondary artifact; putting the links at the top re-elevated them to co-equal status with the chapter prose and pushed the opening hook and welcome mascot below the fold. Added Step 0, a required trade-off block the skill must paste to the user before installing anything — slides drift silently from the chapter, are often the wrong medium for asynchronous reading, and may contradict the book's own pedagogy on retrieval vs. re-reading.
- **Guide update (no viewer version bump)** — Fixed the slide-deck and chapter-index button-bar templates to use source-relative paths. Previously the guide instructed authors to write `../../../sims/slide-viewer/main.html` in `slides.md` and `slides/` in the chapter index. MkDocs rewrites source-relative paths to account for directory URLs at render time, so the old templates wrote rendered-URL paths into source — the three-`../` form escaped the site prefix on GitHub Pages (resolved to `/sims/...` instead of `/<repo>/sims/...`) and all of the button-bar links triggered MkDocs link-check WARNINGs or INFOs. The corrected templates use `../index.md`, `../../sims/...`, and `slides.md` and produce a clean build.
- **v0.01** — Initial template. Fetches rendered MkDocs HTML, splits on `<hr>`, keyboard + button navigation, first/last jumps, fullscreen, table of contents, mascot in lower-left corner (neutral on every slide, celebration on the last).

## Step 1: Verify Prerequisites

```bash
ls mkdocs.yml docs/chapters/ 2>&1
```

If either is missing, the project isn't a MkDocs Material textbook yet — run the `init-textbook.md` guide (feature 0) first.

Optional but recommended — if the project has a mascot installed, the viewer will use `neutral.png` and `celebration.png` automatically:

```bash
ls docs/img/mascot/neutral.png docs/img/mascot/celebration.png 2>&1
```

Missing mascot images are harmless: the viewer still works, the mascot img just 404s silently.

## Step 2: Install the Slide Viewer

```bash
SKILL_DIR="$BK_HOME/skills/book-installer/references/assets/slide-viewer"
mkdir -p docs/sims/slide-viewer
cp "$SKILL_DIR/main.html"  docs/sims/slide-viewer/main.html
cp "$SKILL_DIR/script.js"  docs/sims/slide-viewer/script.js
cp "$SKILL_DIR/local.css"  docs/sims/slide-viewer/local.css
cp "$SKILL_DIR/index.md"   docs/sims/slide-viewer/index.md
```

### File Structure Installed

```
docs/sims/slide-viewer/
├── main.html   # Viewer shell with controls and mascot slot
├── script.js   # Fetches rendered HTML, splits on <hr>, handles nav
├── local.css   # 16:9 slide stage, mascot positioning, responsive
└── index.md    # MkDocs page — describes the viewer, lists deck links
```

## Step 3: Add the Viewer to mkdocs.yml

Add this entry under the existing MicroSims section in `mkdocs.yml` (create the section if it doesn't exist):

```yaml
nav:
  # ... existing nav ...
  - MicroSims:
    - Slide Viewer: sims/slide-viewer/index.md
```

## Step 4: Confirm Which Chapters to Generate Slides For

**Ask the user which chapters** to generate slides for. Accept any of:

- A list of chapter numbers: "1, 2, 5"
- A range: "chapters 1 through 4"
- "all" — every chapter directory under `docs/chapters/`

List available chapters first so the user can pick:

```bash
ls docs/chapters/ | grep -v '^index'
```

**Do not generate slides for chapters whose `index.md` does not yet have content.** A chapter that is only a title and summary produces a thin, low-value deck. Check with:

```bash
for d in docs/chapters/*/; do
  lines=$(wc -l < "$d/index.md")
  echo "$lines $d"
done
```

Skip chapters under ~100 lines unless the user insists.

## Step 5: Generate slides.md for Each Selected Chapter

For each selected chapter, create `docs/chapters/<chapter-slug>/slides.md` by summarizing the chapter's `index.md`. This is a **writing task, not a script** — the LLM reads the chapter and drafts the deck.

### Deck Structure (required)

Every generated deck must follow this shape:

1. **Navigation button bar** (before any slide content):

   ```markdown
   [Content](../index.md){ .md-button } [Slides in Viewer](../../sims/slide-viewer/main.html?src=../../chapters/<chapter-slug>/slides/){ .md-button .md-button--primary }
   ```

   **Path-depth note — write SOURCE-relative paths, not rendered-URL paths.** MkDocs validates link targets against the source tree (`docs/chapters/<chapter-slug>/slides.md`) and, for `use_directory_urls: true` (the default), automatically rewrites the output to account for the extra directory level of the rendered URL. So:
   - `../index.md` in source → MkDocs rewrites to `../` at runtime, landing on the chapter index (`/chapters/<chapter-slug>/`). Using bare `../` in source passes the link check with an INFO nag ("Did you mean '../index.md'?") — always include the `.md` suffix.
   - `../../sims/slide-viewer/main.html` in source → MkDocs rewrites to `../../../sims/slide-viewer/main.html` at runtime. Writing `../../../sims/...` directly in source is a **footgun**: it passes at build time with a WARNING (unresolvable target), and at runtime resolves to `<site-root>/../sims/` which escapes the deployment prefix on GitHub Pages (e.g. `/sims/...` instead of `/<repo>/sims/...`). Always count `../` from the source file's directory, not from the rendered URL.
   - The `src=` query parameter is a separate beast — it is resolved by the viewer's own JavaScript relative to `/sims/slide-viewer/`, so that portion stays `../../chapters/<chapter-slug>/slides/` regardless.

   Using `./` for the Content link is another common mistake — `./` resolves to the same slides page, not the chapter.

2. **Title slide** — `# Chapter Title`, one-line subtitle, short tagline or the mascot's catchphrase, author/mascot attribution line. Keep it to 4–6 lines of text.

3. **Content slides**, separated by `---` on its own line. Each slide should:
   - Start with an `## H2` heading that names the idea.
   - Hold 3–7 bullets OR one short paragraph OR one small table — **not all three**.
   - Keep prose spoken-voice, not paragraph-dense. A slide is a signpost; the speaker fills in detail.
   - Use `>` blockquotes for emphasis/quotations, sparingly.

4. **Retrieval check slide** — if the chapter has a retrieval section, preserve 3–5 of its questions on one slide. Mark Bloom levels in parentheses where the source does.

5. **Bridge slide** — one slide that names what the next chapter sets up.

6. **Celebration slide** (always the last slide) — a short, affirming close. The viewer swaps the mascot pose to `celebration.png` on this slide automatically; don't try to embed an image yourself.

### Slide Count Guidance

- Short/framework chapters (~200 lines of `index.md`): aim for **15–20 slides**.
- Deep content chapters (~300+ lines): aim for **22–28 slides**.
- Hard ceiling: **30 slides**. If you exceed that, you're paragraphing the chapter onto slides instead of distilling it.

### Voice and Style Rules

Follow the project's CLAUDE.md style guide if one exists. For Learning Sciences and similar projects, these rules apply to slides too:

- No "obviously", "simply", "just", "clearly".
- No hype adjectives ("game-changing", "revolutionary").
- Term-of-art in **bold** on first use on a slide.
- Present tense, active voice, contractions welcome.
- If the chapter has a mascot voice (like Bloom), the title and celebration slides can carry the mascot's signature line — but body slides stay in chapter prose voice.

### What to Leave Out

- **Skip long tables** that won't fit at a glance. If a table is 7+ rows, compress to the 3–4 rows that matter most.
- **Skip embedded diagrams** (Mermaid, MicroSim blocks, collapsible `<details>` spec blocks). The viewer renders plain HTML from MkDocs; complex interactive blocks will not render as intended. Replace each with a **one-slide textual summary** of what the diagram shows and what the reader takes away.
- **Skip admonitions** (`!!! mascot-*`, `!!! info`, etc.). The mascot slot in the viewer already carries the mascot. Admonition styling is heavy for a slide.

### Required Cross-Links on the Chapter's index.md

After generating `slides.md`, add a button bar at the **END** of the chapter's `index.md`, after the last section of chapter content (typically after the closing bridge / celebration mascot admonition). **Placing the link at the end — not the top — is deliberate: slides are a secondary artifact, and the chapter prose is the canonical reading experience.** A button bar at the top would signal that slides are a co-equal view, which they are not; it would also push the chapter's opening hook and welcome mascot below the fold on small screens.

**Do not include a "Content" button on the chapter page itself — the reader is already on the content, so that button would be redundant.**

Append this block at the bottom of the chapter's `index.md`, separated from the preceding content by a blank line:

```markdown
<!-- ... chapter content above ... -->

---

## Slides for this chapter

If you would prefer the slide-deck view of this chapter, or want to present it in a class or workshop:

[Slides](slides.md){ .md-button } [Slides in Viewer](../../sims/slide-viewer/main.html?src=../../chapters/<chapter-slug>/slides/){ .md-button .md-button--primary }
```

Design notes:

- The `---` rule and `## Slides for this chapter` heading visually separate the slide links from the chapter prose. Readers who scroll to the end see the links; readers who stop at the celebration mascot never do, and that is fine — they are there for the content.
- Write `slides.md` (not `slides/`) in the source — MkDocs will rewrite to the `slides/` directory URL in the rendered output. Using the bare `slides/` form passes the build but triggers an INFO nag from the link checker.
- From the rendered `slides.md` page, readers already see a **Content** button (added in the deck template above) that links back to the chapter. The two pages cross-link each other; neither page shows a button to itself.

**When retrofitting chapters that already have a button bar at the top:** remove the top bar and move the links to the end. Do not leave both — having the links in two places re-elevates the slides to co-equal status, which defeats the purpose of the move.

## Step 6: Update mkdocs.yml Nav for Each Deck

For every chapter that got a `slides.md`, restructure its nav entry from a single link into a `Content`/`Slides` subsection:

```yaml
# Before:
- 1. Chapter Title: chapters/01-slug/index.md

# After:
- 1. Chapter Title:
    - Content: chapters/01-slug/index.md
    - Slides: chapters/01-slug/slides.md
```

Leave chapters without decks as single-link entries.

## Step 7: Update the Slide Viewer's Deck List

The viewer's `index.md` contains an HTML-comment placeholder:

```markdown
<!-- DECK_LIST_START -->
<!-- Deck links are appended here by the slide-generator installer. -->
<!-- DECK_LIST_END -->
```

Replace the inner comment with one line per chapter deck generated:

```markdown
<!-- DECK_LIST_START -->
- [Chapter 1 — <Chapter Title>](main.html?src=../../chapters/01-slug/slides/){target=_blank}
- [Chapter 2 — <Chapter Title>](main.html?src=../../chapters/02-slug/slides/){target=_blank}
<!-- DECK_LIST_END -->
```

When adding a new chapter later, append a line inside the markers; don't recreate the list.

## Step 8: Verify

Tell the user to reload the browser tab running `mkdocs serve` (the user runs this themselves — never start or kill `mkdocs serve` yourself) and test:

1. **Viewer page:** `http://127.0.0.1:8000/<repo-name>/sims/slide-viewer/` — deck links should appear.
2. **Chapter page:** `http://127.0.0.1:8000/<repo-name>/chapters/01-<slug>/` — three-button bar at the top.
3. **Slides page (rendered):** `http://127.0.0.1:8000/<repo-name>/chapters/01-<slug>/slides/` — slides stacked with horizontal rules.
4. **Slides in the viewer:** click **Slides in Viewer** — first slide is the title, arrow keys advance, last slide shows the celebration mascot.

If the viewer shows "Could not load slides from ... HTTP 404": the `src=` query is pointing at a `.md` file. MkDocs does not serve raw `.md`. The `src` must end in `/` (a directory-style URL), not `.md`.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Viewer shows "Could not load slides ... HTTP 404" | `src=` points at a `.md` file | Use the rendered URL: end in `/`, not `.md` |
| Only one slide shows; everything is on it | Source `slides.md` has no `---` horizontal rules | Separator must be `---` on its own line, with blank lines above and below |
| Mascot does not appear | `docs/img/mascot/neutral.png` not installed | Install the mascot via `learning-mascot.md`, or ignore — viewer still works |
| Deck nav buttons break the title slide | Buttons placed after the first `---` | The button bar must be at the very top of `slides.md`, before any slide separator |
| "Content" button on `slides.md` stays on the same page | Link uses `./` (current directory = same slides page) | Use `../index.md` (source-relative). MkDocs rewrites to `../` in the rendered HTML, landing on `/chapters/<slug>/` |
| "Slides in Viewer" button on `slides.md` 404s or escapes site prefix on GitHub Pages | Source contains `../../../sims/...` (rendered-URL path written into source) | Use source-relative `../../sims/slide-viewer/main.html?src=...` — MkDocs rewrites to `../../../sims/...` in the rendered HTML automatically. Writing three `../` in source escapes the deployment prefix at runtime |
| `[Slides](slides/)` on chapter `index.md` triggers INFO "Did you mean 'slides.md'?" | Source uses the rendered directory URL instead of source-relative `.md` | Write `[Slides](slides.md)` in source; MkDocs rewrites to `slides/` in the rendered output |
| Slides in viewer look ugly (raw admonitions, collapsed `<details>`) | Chapter content was copied verbatim instead of distilled | Re-summarize: slides are 3–7 bullets, not full chapter prose |

## Dependencies

- MkDocs Material (the viewer assumes the theme's `article.md-content__inner` container).
- Optional: `docs/img/mascot/neutral.png` and `docs/img/mascot/celebration.png` from the `learning-mascot.md` guide.
- No runtime JS dependencies (marked.js is **not** used — MkDocs already renders the markdown; the viewer walks the DOM).

## Why the Viewer Fetches Rendered HTML (Not Raw `.md`)

MkDocs does not serve raw `.md` files. A file at `docs/chapters/01-foundations/slides.md` becomes a rendered HTML page at `/chapters/01-foundations/slides/`. Fetching the raw `.md` path returns 404. The viewer therefore:

1. Strips any trailing `.md` or `/index.md` from the `src` parameter.
2. Appends `/` if missing.
3. Fetches the rendered page, extracts `article.md-content__inner`, and splits children on `<hr>` elements.

This is why horizontal rules (`---`) are the slide separator — they survive intact as `<hr>` in the rendered HTML.

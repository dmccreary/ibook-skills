# Supplementary Content Generator

## Purpose

Generate all standard supplementary content for an intelligent textbook in one coordinated workflow. This covers every artifact that surrounds the chapter content: navigation, discovery, reference, assessment, and reporting layers.

## Model Guidance

> **Sonnet for all text-generation steps** (glossary, FAQ, quizzes, references, about, README, landing page).
> **Opus with high thinking for MicroSims** — any interactive simulation created as part of this workflow should be generated with `claude-opus-4-7` at the `high` thinking budget. Opus is significantly better at the coding and layout reasoning required for correct, interactive p5.js / Chart.js / vis-network simulations.

## When to Use

Invoke this guide when the user says any of:
- "generate all supplementary content"
- "complete the book"
- "generate glossary, faq, quizzes, references"
- "finish the book"
- "run book completion"
- "supplementary content"
- selects **39** from the help list

## Prerequisites

Before running this workflow, verify the following are in place:

- [ ] `mkdocs.yml` exists and `site_name` is set
- [ ] `docs/course-description.md` exists with a complete course description
- [ ] `docs/learning-graph/learning-graph.json` exists (required for glossary and FAQ quality)
- [ ] At least one chapter exists under `docs/chapters/`
- [ ] The user is in the project root directory

If any prerequisite is missing, tell the user which ones are needed and stop.

---

## Step 1: Inventory What Already Exists

Before generating anything, check which supplementary files are already present so you don't overwrite existing work without asking.

```bash
# Check existing supplementary files
ls docs/glossary.md docs/faq.md docs/about.md docs/index.md docs/img/cover.png README.md 2>/dev/null
ls docs/chapters/*/references.md docs/chapters/*/quiz.md 2>/dev/null | head -20
```

Report findings to the user. For any file that already exists, ask: **"This file already exists — overwrite, skip, or append?"** before proceeding. Default to **skip** if the user does not respond.

---

## Step 2: Generate the About Page

**Target:** `docs/about.md`

If not already present (or user chose overwrite), invoke the `about-page` reference:

```
Read references/about-page.md and execute its workflow for this project.
```

The about page should include:
- Book motivation and intended audience
- Author / contributor bio
- How to cite the book (APA, MLA, BibTeX)
- License statement
- Acknowledgements section (if applicable)

Add to `mkdocs.yml` nav if not already present:
```yaml
- About: about.md
```

---

## Step 3: Generate the Glossary

**Target:** `docs/glossary.md`

Invoke the `glossary-generator` skill:

```
Invoke the glossary-generator skill for this project.
```

The glossary must:
- Cover every concept in `docs/learning-graph/learning-graph.json`
- Follow ISO 11179 definition standards (precise, concise, distinct, non-circular, free of business rules)
- Be sorted alphabetically
- Include a back-link to the chapter where each concept is first introduced (if determinable)

Add to `mkdocs.yml` nav if not already present:
```yaml
- Glossary: glossary.md
```

---

## Step 4: Generate the FAQ

**Target:** `docs/faq.md`

Invoke the `faq-generator` skill:

```
Invoke the faq-generator skill for this project.
```

The FAQ should:
- Have ≥ 30 questions covering the full breadth of the course
- Be organized into thematic sections matching the chapter structure
- Answer questions a typical student would ask before, during, and after the course
- Cross-link answers to the relevant chapter or glossary term

Add to `mkdocs.yml` nav if not already present:
```yaml
- FAQ: faq.md
```

---

## Step 5: Generate Per-Chapter Quizzes

**Target:** `docs/chapters/<chapter-slug>/quiz.md` for each chapter

Invoke the `quiz-generator` skill for each chapter that lacks a `quiz.md`:

```
Invoke the quiz-generator skill for docs/chapters/<chapter-slug>/index.md
```

Each quiz must:
- Contain 10–15 questions aligned to the chapter's learning objectives
- Cover at least three Bloom's Taxonomy levels (Remember, Understand, Apply minimum)
- Include answer keys in a collapsed `<details>` block
- Use MkDocs Material's `???` admonition for each question (collapsed by default)

After creating each `quiz.md`, add a **Quizzes** sub-entry to the chapter's nav in `mkdocs.yml`:
```yaml
- Chapter N - Title:
    - Content: chapters/<slug>/index.md
    - Quiz: chapters/<slug>/quiz.md
```

If the chapter already has a `quiz.md`, skip it (or append if user said "append").

---

## Step 6: Generate Per-Chapter References

**Target:** `docs/chapters/<chapter-slug>/references.md` for each chapter

Invoke the `reference-generator` skill for each chapter that lacks a `references.md`:

```
Invoke the reference-generator skill for docs/chapters/<chapter-slug>/index.md
```

Each references file must:
- List 8–15 curated, verifiable sources (books, papers, websites, videos)
- Be grouped by type: Books, Articles, Online Resources, Videos
- Include a one-sentence annotation for each source explaining why it is relevant
- Prefer freely accessible or open-access sources where possible

After creating each `references.md`, add a **References** sub-entry to the chapter's nav in `mkdocs.yml`:
```yaml
- Chapter N - Title:
    - Content: chapters/<slug>/index.md
    - Quiz: chapters/<slug>/quiz.md      # if quiz exists
    - References: chapters/<slug>/references.md
```

---

## Step 7: Generate the Cover Image Prompt

**Target:** `docs/img/cover-image-prompt.md` (and `docs/img/cover.png` only if the user explicitly requests auto-generation)

A high-quality cover image anchors the landing page, social previews, and README. Generate the prompt now — before the landing page — so the landing page can reference the cover once it exists.

If `docs/img/cover.png` already exists and the user did not choose overwrite, skip this step.

Otherwise, invoke the `cover-image-generator` reference:

```
Read references/cover-image-generator.md and execute its workflow for this project.
```

`cover-image-generator.md` writes `docs/img/cover-image-prompt.md` by default and does **not** call any image generation API or script unless the user explicitly asks for auto-generation as part of this coordinated run. If the user hasn't opted in, report the prompt file as ready, note that the landing page and social preview will reference `docs/img/cover.png` once the user (or an explicit follow-up request) produces it, and continue to Step 8 without blocking on it.

If the image was generated (either because the user opted in during this step, or `docs/img/cover.png` already existed):
1. Confirm it is saved to `docs/img/cover.png` (1200×628 px, 1.91:1 aspect ratio).
2. Install the social-media-preview hook if not already present:
   ```
   Read references/social-media-preview.md and execute its workflow for this project.
   ```
   The hook ensures every page emits correct `og:image` meta tags pointing to `cover.png`.

---

## Step 8: Run Book Metrics

**Script:** `bk-generate-book-metrics`

```bash
bk-generate-book-metrics
```

This script generates a metrics report (typically written to `docs/book-metrics.md` or printed to stdout). If it writes a file, add it to the nav:

```yaml
- Book Metrics: book-metrics.md
```

If the script is not found in PATH, remind the user to install it:
```
bk-generate-book-metrics is not found. Install it from the ibook-skills scripts directory or your local bin path.
```

---

## Step 9: Run Diagram Reports

**Script:** `bk-diagram-reports`

```bash
bk-diagram-reports
```

This script audits all MicroSims and diagrams in the project and generates a report (typically `docs/diagram-reports.md`). If it writes a file, add it to the nav:

```yaml
- Diagram Reports: diagram-reports.md
```

If the script is not found in PATH, remind the user to install it similarly to Step 8.

---

## Step 10: Generate README.md

**Target:** `README.md` (project root)

The README is generated after the metrics scripts so it can incorporate accurate counts: number of chapters, MicroSims, glossary terms, FAQ entries, and any summary statistics produced by `bk-generate-book-metrics` and `bk-diagram-reports`.

Invoke the `book-publisher` skill's readme route to create a GitHub-facing README. This is separate from the MkDocs site and is what visitors see on the GitHub repository page.

```
Invoke the book-publisher skill (readme route) for this project.
```

The README should include:
- Book title and one-paragraph description
- Live site link (from `site_url` in mkdocs.yml)
- Topics / tags (from learning graph taxonomy)
- Content summary stats: chapters, MicroSims, glossary terms, FAQ entries (from metrics output)
- Quick-start instructions (how to run locally, how to contribute)
- License badge and link
- Cover image (`docs/img/cover.png`)

---

## Step 11: Generate the Main Landing Page

**Target:** `docs/index.md`

The landing page is generated last so it can include links and highlights drawn from all the supplementary content produced in earlier steps: glossary term count, FAQ question count, number of MicroSims, cover image, metrics summary, about-page link, and README-aligned stats.

If the home page is a stub (< 30 lines) or the user chose overwrite, generate it using the `home-page-template` reference:

```
Read references/home-page-template.md and execute its workflow for this project.
```

When writing the landing page, incorporate:
- The cover image at `docs/img/cover.png`, following the **Landing Page Title Rule** in `home-page-template.md`: when the cover renders the book title, hide the duplicate h1 with the `<style>` block and start the image's alt text with the book title. If `cover.png` is still the scaffold placeholder, leave the h1 visible.
- A summary stat block: number of chapters, MicroSims, glossary terms, FAQ entries
- Quick-links to Glossary, FAQ, and About in the intro prose or a callout box
- Any course prerequisites or target audience statement from `docs/course-description.md`

If a full landing page already exists and the user chose skip, leave it untouched.

---

## Step 12: Update mkdocs.yml Navigation

After all content is generated, ensure the nav section of `mkdocs.yml` is clean and complete. A typical supplementary nav block looks like:

```yaml
nav:
  # ... existing chapter entries ...
  - Glossary: glossary.md
  - FAQ: faq.md
  - About: about.md
  - Book Metrics: book-metrics.md
  - Diagram Reports: diagram-reports.md
```

Check that no nav entries point to files that don't exist, and no generated files are missing from the nav.

---

## Step 13: Verification

Run a final check to confirm all generated files are present and non-empty:

```bash
echo "=== Supplementary Content Check ===" && \
for f in docs/glossary.md docs/faq.md docs/about.md docs/index.md docs/img/cover.png README.md; do
  if [ -f "$f" ]; then
    lines=$(wc -l < "$f")
    echo "OK  $f ($lines lines)"
  else
    echo "MISSING  $f"
  fi
done && \
echo "" && \
echo "=== Per-Chapter Quiz & References ===" && \
for dir in docs/chapters/*/; do
  chapter=$(basename "$dir")
  quiz="${dir}quiz.md"
  refs="${dir}references.md"
  [ -f "$quiz" ] && echo "OK  $chapter/quiz.md" || echo "MISSING  $chapter/quiz.md"
  [ -f "$refs" ] && echo "OK  $chapter/references.md" || echo "MISSING  $chapter/references.md"
done
```

Report the results to the user. For any MISSING item, offer to generate it now.

---

## Execution Order Summary

| Step | Artifact | Skill / Script | Model |
|------|----------|----------------|-------|
| 2 | `docs/about.md` | `references/about-page.md` | Sonnet |
| 3 | `docs/glossary.md` | `glossary-generator` skill | Sonnet |
| 4 | `docs/faq.md` | `faq-generator` skill | Sonnet |
| 5 | Per-chapter `quiz.md` | `quiz-generator` skill | Sonnet |
| 6 | Per-chapter `references.md` | `reference-generator` skill | Sonnet |
| 7 | `docs/img/cover-image-prompt.md` (`docs/img/cover.png` only if requested) | `references/cover-image-generator.md` | Sonnet (+ AI image tool if auto-generation is requested) |
| 8 | `docs/book-metrics.md` | `bk-generate-book-metrics` script | — |
| 9 | `docs/diagram-reports.md` | `bk-diagram-reports` script | — |
| 10 | `README.md` | `book-publisher` skill (readme route) | Sonnet |
| 11 | `docs/index.md` | `references/home-page-template.md` | Sonnet |
| 12 | `mkdocs.yml` nav | Manual edit | — |
| 13 | Verification | Bash check | — |

**MicroSims:** Any interactive simulation created during this workflow must use `claude-opus-4-7` with `high` thinking. Opus handles the spatial reasoning, canvas math, and interactive JavaScript patterns that MicroSims require far better than Sonnet.

---

## Tips

- **Run in phases**: If the book has many chapters, generate quizzes and references for one or two chapters first to confirm quality, then batch the rest.
- **Glossary before FAQ**: The FAQ generator produces better output when it can reference glossary definitions, so always run Step 3 before Step 4.
- **Metrics before README and landing page**: Steps 8–9 run before Steps 10–11 intentionally — both the README and landing page embed content counts from the metrics output.
- **Cover before landing page**: Step 7 runs before Step 11 so the landing page can reference `docs/img/cover.png` directly if it exists; otherwise the landing page can reference `docs/img/cover-image-prompt.md` and note the image is pending manual or on-request generation.
- **Check bk scripts in PATH**: Both `bk-generate-book-metrics` and `bk-diagram-reports` must be installed in a directory on `$PATH`. If missing, skip and note it in the verification report.
- **Nav ordering**: Place Glossary and FAQ near the end of the nav, after all chapters. About page goes last.

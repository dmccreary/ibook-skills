---
name: arxiv-paper-generator
description: Generates a complete academic paper in arXiv format — modular LaTeX source, a verified BibTeX bibliography, figures, and a build script that produces a polished PDF plus a ready-to-upload arXiv package — in a new folder under the repository's papers/ directory. Interviews the author until there is enough real content (contribution, evidence, prior work, figures), then scores the paper on a 100-point quality rubric. Use this whenever the user wants to write, draft, start, convert, score, or package a research paper, preprint, or white paper for arXiv, EdArXiv, OSF, SSRN or a conference — including turning a book, a course, project docs, or a Markdown draft into a paper — even if they never say "arXiv" or "LaTeX".
license: Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
metadata:
  ibook.version: "0.01"
---

# ArXiv Paper Generator

**Version:** 0.01

Tell the user they are running Version 0.01 of the ArXiv Paper Generator skill.

## Overview

This skill produces an academic paper in arXiv format. The result is modular LaTeX
source, a BibTeX bibliography of verified references, figures, and a `build.sh` that
makes a high-quality PDF and an arXiv upload package. Each paper lives in its own
folder under the repository's `papers/` directory.

A paper is only as good as its content. An LLM can turn out fluent, paper-shaped text
on any topic, so fluency is no evidence of quality. Reviewers look for a specific
contribution, real evidence, and honest positioning against prior work, and those can
only come from the author and their sources. Most of this skill's effort therefore goes
into collecting enough real content before any LaTeX is written. The 100-point rubric in
`references/quality-rubric.md` is used twice. First it decides when the interview has
gathered enough (the **readiness** score). Then it grades the finished paper (the
**quality** score).

## Output layout

```
<repo>/papers/
├── README.md                  # index of this repo's papers (create if missing)
└── <paper-slug>/
    ├── brief.md               # interview answers, assumptions, readiness score
    ├── main.tex               # preamble, title block, \input list
    ├── sections/
    │   ├── 01-abstract.tex    # one file per section, numbered in reading order
    │   ├── 02-introduction.tex
    │   ├── ...
    │   └── references.bib
    ├── figures/               # PNG (300 DPI) or .tikz figures + the scripts that make them
    ├── build.sh               # ./build.sh | clean | arxiv | release
    ├── arxiv-metadata.md      # what to paste into the arXiv submission form
    ├── quality-report.md      # rubric score, gaps, items needing the author
    ├── README.md
    └── main.pdf
```

The pattern (main.tex + numbered section files + `sections/references.bib` + PNG figures
+ Tectonic `build.sh`) matches the author's earlier papers, so keep to it.

## Workflow

### Step 1: Locate the repository and the paper folder

- The repo root is `git rev-parse --show-toplevel` for the current directory, unless the
  user names another repo. Papers go in `<root>/papers/<slug>/`. Use the plural
  `papers`, even if the repo has an older singular `paper/` folder; leave that one alone.
- The slug is short, lowercase and hyphenated, derived from the working title
  (`five-levels`, `self-improving-textbooks`). Confirm it along with the title.
- If `papers/<slug>/` already exists, don't overwrite it. Read its `brief.md` and
  `quality-report.md` and pick up where it left off: continue the interview, revise,
  rebuild or rescore.
- If `papers/README.md` is missing, create it from `assets/papers-README.md`.

### Step 2: Mine the source material before asking anything

Start with what the user attached or pointed to. Then look through the repo: its README,
`docs/` (chapters, course description, "why" or motivation pages, research notes,
per-chapter `references.md` files), Markdown drafts, data files, images, posters,
MicroSims, and earlier papers under `papers/`. In a textbook or MicroSims repo the docs
are the richest source. A book's course description and case-study chapters often hold
the thesis and the evidence.

Note which files feed which section. Every question the repo can answer is one the user
doesn't have to. For a large source such as a whole book, read the overview pages and
skim the chapter headings first, then read in depth only the chapters that carry the
paper's argument.

### Step 3: Interview until the content is sufficient

Read `references/intake-interview.md`. It lists what a high-quality paper needs, maps each
item to the rubric, and gives the questions that fill each gap.

- Ask in small rounds of 2–4 related questions. A wall of 20 questions gets skimmed. Lead
  with what you found in Step 2, so the user confirms rather than authors: "Chapter 10
  frames the researcher as coordinating 20 planning and 10 execution agents. Is that the
  paper's central claim?"
- Record answers in `brief.md` (template: `assets/brief-template.md`) after each round
  and recompute the readiness score.
- Keep asking until readiness is at least 80 and none of the blockers in
  intake-interview.md remain. If the user wants to go ahead sooner, say which rubric
  categories will come out weak and why, and record that decision in brief.md.
- **When no one can answer** (a batch run, a subagent, or a user who said "just write
  it"), make reasonable decisions from the source material. Record each one in brief.md
  under *Assumptions* so the author can check it later. Proceed only if readiness is at
  least 80 without assumptions standing in for blockers. Otherwise write the open
  questions under *Open questions* in brief.md, report the readiness score, and stop
  before drafting. A paper built on invented answers is worse than no paper.

### Step 4: Outline, then get approval

Pick the paper type and section plan from `references/section-guide.md`: framework or
position, system or tool, empirical study, or survey. Write the outline into brief.md:

- the final title
- a 3–5 sentence abstract sketch
- the section list, with a 1–2 line summary of each
- a figure plan of 3–6 figures, saying what each shows and how it will be made
- planned tables
- the target length (usually 10–20 pages)

Check where the paper can be posted before committing to the outline. Since October
2025, arXiv's CS categories reject position and survey papers that haven't already
passed peer review. Research papers on technology's societal impact (cs.CY) are exempt.
`references/arxiv-submission.md` gives the details. A framework supported by case
studies or data is a research paper, so frame it that way. For a pure position piece,
recommend EdArXiv, OSF, or TechRxiv instead. Record the decision in brief.md.

Show the outline to the user and fold in their changes. Changing an outline is cheap;
changing 15 pages of LaTeX is not. When no one is there to approve it, proceed and note
in brief.md that the outline was not reviewed.

### Step 5: Scaffold the paper folder

```bash
cp -R <skill-dir>/assets/template/ <root>/papers/<slug>/
chmod +x <root>/papers/<slug>/build.sh
mkdir -p <root>/papers/<slug>/figures
```

In `main.tex`, fill in the title, authors, `\paperversion` and the `\input` list to match
the outline, replacing every `{{...}}` placeholder. Leave the preamble alone unless the
paper needs something extra, such as `algorithm` for pseudocode. It is set up to compile
both locally with Tectonic (XeTeX) and on arXiv with pdfLaTeX. Don't add `fontspec`,
`\pdfoutput`, or other engine-specific packages.

### Step 6: Write the sections

Write each section to its own file, following section-guide.md.

- **Never fabricate.** Don't invent statistics, study results, quotes, user counts, dates
  or references. Every number comes from the user, the repo, or a cited source. When the
  evidence is thin, narrow the claim, present it as a proposal or hypothesis, or move it
  to Future Work.
- **Every reference must be real and verified.** Before adding an entry to
  `sections/references.bib`, confirm the work exists with a web search, a DOI lookup, or
  the publisher's page, and copy its metadata from there, not from memory. Give it a
  `doi` field, or a `url` for web resources. The book's own `references.md` files are a
  good starting pool, but verify those entries too. Prefer peer-reviewed and seminal
  sources, and include recent work from the last 5 years. Aim for 25–50 references. If a
  source can't be verified, leave it out and list it in quality-report.md for the author.
- **Cite as you write.** Every non-obvious factual claim gets a `\cite{}`, or a pointer to
  the paper's own evidence.
- **Follow LaTeX hygiene for arXiv**, since arXiv compiles with pdfLaTeX. Use `---` for an
  em dash, ``` ``quotes'' ```, `\%` and `$\geq$`. Avoid raw Unicode symbols such as →, ≥,
  ✓, Greek letters, emoji and smart quotes. Tectonic may silently drop them, and pdfLaTeX
  will fail on them. Label everything (`sec:`, `fig:`, `tab:`, `eq:`) and refer to it as
  `Figure~\ref{fig:x}`.
- **Write in an academic register.** Be precise. Use "we" or the third person. Use
  defined terms consistently and expand each acronym on first use. Leave out marketing
  adjectives such as "revolutionary" or "game-changing". The paper argues; a book chapter
  teaches. Don't paste textbook prose; condense it into claims, definitions and evidence.
- **Disclose AI assistance.** arXiv expects authors to report generative-AI use beyond
  basic editing, and AI tools can't be authors. Add a short disclosure in the
  Acknowledgments that says what the tool did and that the authors take responsibility
  for the content.
- **Write the abstract last**, once the content is settled: 150–250 words, at most
  1,920 characters (arXiv's form limit), with no citations, followed by a
  `\textbf{Keywords:}` line.

### Step 7: Make the figures

Follow `references/figures-guide.md`. Every figure is referenced in the text before it
appears, has a self-contained caption, and is legible at print size. Use one of these:

- PNG at 300 DPI from a script kept in `figures/` (matplotlib for charts)
- TikZ in `figures/<name>.tikz` for diagrams
- an existing image or screenshot from the repo

Keep the scripts, so the figures can be regenerated.

### Step 8: Build

Run `./build.sh` from the paper folder. Fix every error, undefined citation or
reference, missing figure, and "Missing character" warning. Overfull boxes wider than
10pt get fixed too: rephrase, break the URL, or adjust the table. The build script prints
these at the end. A paper that doesn't compile cleanly loses the build points, and the
hard gate keeps it from being called ready.

### Step 9: Score and revise

```bash
python3 <skill-dir>/scripts/score_paper.py <root>/papers/<slug> --verify-dois
```

The script scores the mechanical criteria (references, figures, tables, build, package,
metadata) and prints the facts you need for the judgment criteria. It also checks every
DOI against Crossref and doi.org. Score the judgment criteria yourself with the
descriptors in quality-rubric.md, then write `quality-report.md` using the format given
there.

If the total is below 85 or any hard gate fails, revise the lowest-scoring categories,
rebuild, and rescore. After two revision passes, stop and report what only the author
can supply, such as data, figures, or a missing reference.

### Step 10: Package for arXiv

- Run `./build.sh arxiv`. It builds, creates `arxiv-upload.zip` (sources, figures,
  `main.bbl`), and test-compiles the zip in a clean temporary folder to prove it is
  self-contained.
- Fill in `arxiv-metadata.md` from `assets/arxiv-metadata-template.md`: a plain-text
  abstract, the primary and cross-list categories, a comments line ("N pages, M
  figures"), and the license. `references/arxiv-submission.md` explains each field.
- Fill in the paper's `README.md` (from the template), and add the paper to
  `papers/README.md`.
- Rerun the scorer so quality-report.md reflects the packaged state.

### Step 11: Report back

Tell the user:

- the PDF path and page count
- the quality score and tier, and which hard gates fail, if any
- the top gaps
- anything that needs their input: unverified references, missing data, assumptions to
  confirm
- how to rebuild

Then list what's left for submission. They submit to arXiv themselves, and a first-time
submitter to a category may need an endorsement. Commit only if the user asks.

## Resources

- `references/quality-rubric.md`: the 100-point rubric, hard gates, tiers and report
  format. Read it before Steps 3 and 9.
- `references/intake-interview.md`: the content checklist, readiness scoring and question
  bank. Read it before Step 3.
- `references/section-guide.md`: section plans for each paper type, and what each section
  must do. Read it before Steps 4 and 6.
- `references/figures-guide.md`: how to make figures (matplotlib, TikZ, screenshots),
  captions, resolution and color. Read it before Step 7.
- `references/arxiv-submission.md`: arXiv rules, categories, licenses, the metadata
  fields, and other preprint servers (EdArXiv/OSF). Read it before Step 10.
- `assets/template/`: `main.tex`, `build.sh`, `.gitignore`, `README.md`,
  `sections/01-abstract.tex` and `sections/references.bib` to copy into a new paper.
- `assets/brief-template.md`, `assets/arxiv-metadata-template.md` and
  `assets/papers-README.md`: templates for the files with those names.
- `scripts/score_paper.py`: automated rubric checks. Python standard library only.

# Mascot Chapter Updater

## Purpose

Guide the agent through adding mascot admonitions to an existing chapter
markdown file. This is the natural follow-on to `learning-mascot.md`: once
the mascot images, CSS, and test page are in place, this guide walks through
retrofitting real chapter content with the six pose admonitions in the
right places.

This is an LLM-driven workflow — semantic understanding of the chapter is
required to decide *where* the mascot should appear. Do not try to automate
placement with regex. Use the validation script (`scripts/validate-chapter-mascots.py`)
only to check counts and rule violations after editing.

## When to Use

Use this guide when:

- A project already has mascot images in `docs/img/mascot/` (or
  `docs/img/mascots/`) and `mascot.css` with the seven pose classes.
- The user wants to retrofit one or more existing chapters with mascot
  admonitions.
- The mascot-test page renders correctly (all seven poses show with correct
  colors, fonts, and images).

Do **not** use this guide when:

- The mascot character or images don't exist yet — run `learning-mascot.md`
  first.
- The user wants mascots on non-chapter pages (home page, glossary, FAQ) —
  those have their own conventions, usually just `mascot-welcome` on
  the home page and `mascot-neutral` sparingly on reference pages.

## Prerequisites

- Mascot images present in `docs/img/mascot/` or `docs/img/mascots/`
  (confirm which with `ls docs/img/mascot*`).
- `docs/css/mascot.css` loaded via `extra_css:` in `mkdocs.yml`.
- Working `docs/learning-graph/mascot-test.md` page — if this page does
  not render correctly, stop and fix it first. Debugging mascot CSS on a
  real chapter is painful.
- Chapter file to update, identified by absolute path.

## Placement Rules

**Read the canonical placement rules before placing any admonition:**

    $BK_HOME/skills/book-installer/references/mascot-placement-rules.md

That file is the single source of truth for which pose carries which
pedagogical job, how many of each belong in a chapter, and the hard limits on
total count, back-to-back placement, and body length. It is shared by every
skill in this library.

**Do not restate its tables or counts in this guide.** A second copy drifts
out of sync within weeks — that drift is exactly what the single-source rule
exists to prevent. If a rule seems wrong, change it in the canonical file so
every skill picks the change up at once.

## Workflow

### Step 1: Survey the chapter

Read the full chapter file first. As you read, identify candidates for
each admonition type — do not start editing yet. Build a mental list:

- **Welcome candidate**: the first substantive paragraph after the title
  and any frontmatter. Usually right after the opening `#` heading and
  any chapter-overview box.
- **Thinking candidates**: moments where a named law, equation, or
  principle is introduced for the first time (Ohm's Law, Kirchhoff's
  Current Law, etc.). Look for `##` or `###` headings that name a concept.
- **Tip candidates**: sections that describe problem-solving strategy,
  mnemonic devices, or "when you see X, do Y" patterns.
- **Warning candidates**: paragraphs that describe common errors,
  sign-convention gotchas, unit confusion, or places where students
  typically get tripped up.
- **Encouraging candidates**: the hardest derivation or proof in the
  chapter — usually a section that introduces calculus, complex numbers,
  or a new mathematical technique.
- **Celebration candidate**: the end-of-chapter summary or the final
  worked example that ties everything together.

### Step 2: Propose a plan, then confirm

Before editing, present the user with a numbered list:

```
Proposed mascot placements for <chapter-path>:

1. mascot-welcome  → line 12, after the chapter overview
2. mascot-thinking → line 78, introducing Ohm's Law
3. mascot-warning  → line 145, sign-convention pitfall
4. mascot-tip      → line 210, voltage-divider shortcut
5. mascot-celebration → line 340, end-of-chapter summary

Total: 5 admonitions. Any changes before I apply?
```

Wait for user confirmation or adjustments. Users often have strong
opinions about *where* the mascot should speak — they may want to skip
`mascot-tip` entirely, or move `mascot-thinking` to a different concept.
Do not skip this step. Retrofitting a chapter and then having the user
ask you to undo half the changes is worse than one round of review.

### Step 3: Compute the image path

MkDocs renders directory URLs. A chapter at `docs/chapters/01-intro/index.md`
renders at `.../chapters/01-intro/index.html`. Relative image paths in the
rendered HTML are resolved from `.../chapters/01-intro/`.

Standard chapter depths:

| Chapter file path | `src` path to mascot |
|---|---|
| `docs/chapters/NN-name/index.md` | `../../img/mascot/POSE.png` |
| `docs/chapters/NN-name/content.md` | `../../img/mascot/POSE.png` |
| `docs/sections/NN-name/index.md` | `../../img/mascot/POSE.png` |
| `docs/index.md` | `img/mascot/POSE.png` |

**Check which folder the project actually uses** — `img/mascot/` (singular)
is the book-installer default, but some projects use `img/mascots/`
(plural). Look at an existing working admonition on the mascot-test page
and copy that path prefix exactly.

### Step 4: Apply the edits

For each confirmed placement, use Edit to insert the admonition. The
standard form:

```markdown
!!! mascot-welcome "Welcome to Chapter N"
    ![Sparky waving welcome](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    One to three sentences of in-character introduction. Include the
    mascot's voice and catchphrase where it fits naturally.
```

Rules for the body text:

- Write in the mascot's voice as established in
  `docs/img/mascot/character-sheet.md` (the canonical identity document) or
  the book's `CONTENT-GENERATION-GUIDE.md`. Do not invent a new personality.
- Reference the chapter's actual content specifically — "voltage divider"
  not "this topic". Generic mascot text is worse than no mascot text.
- End `mascot-welcome` with a preview of what the reader will learn.
- End `mascot-celebration` with a call-forward to the next chapter or
  the broader payoff.
- `mascot-warning` should name the specific mistake, not just warn
  generically — "watch sign conventions" is useless; "the passive sign
  convention flips when current enters the negative terminal" is useful.

### Step 5: Verify placement rules

Run the validation script against the edited chapter:

```sh
python3 "$BK_HOME/skills/book-installer/scripts/validate-chapter-mascots.py" \
    docs/chapters/01-intro/index.md
```

The script enforces the caps defined in `mascot-placement-rules.md`. It reports:

- Total mascot admonition count (flags anything at or above the ceiling).
- Count by type (flags if more than one `mascot-welcome` or `mascot-celebration`).
- Back-to-back placements (flags with line numbers).
- Admonitions with suspicious body text (too short, too long, or missing
  the mascot image).

Address every flag before considering the chapter complete.

### Step 6: Visual verification

Run `mkdocs serve` (or ask the user to, if the user runs mkdocs in their
own terminal) and visit the chapter page. Confirm:

- All mascot images load (no broken image icons).
- Background colors match the intended pose (welcome = primary, warning =
  red, celebration = purple, etc.).
- Body text sits to the right of the floated image with no awkward
  wrapping.
- At mobile width the image still behaves cleanly (may stack above text).

## Anti-patterns to avoid

- **Mascot at every `##` heading.** This is the most common over-use.
  Pick the 2–3 most important headings, not all of them.
- **Identical voice across all admonitions.** If every mascot admonition
  sounds the same, the poses are doing no work. `mascot-warning` should
  read urgently; `mascot-celebration` should read excitedly;
  `mascot-thinking` should read curiously.
- **Mascot doing the chapter's actual teaching.** The mascot is a *guide*.
  The chapter body still does the explaining. If you find yourself
  putting the definition of a term inside the admonition, move it out.
- **Back-to-back mascots because two concepts are nearby.** Pick one.
  Two mascots in adjacent paragraphs reads as clutter, not guidance.
- **Mascot image path wrong by one `../`.** Always verify against a
  known-working admonition on the mascot-test page. Every project gets
  this wrong at least once.

## Example: Retrofitting a short chapter

Given `docs/chapters/02-ohms-law/index.md` with sections:

```
# Chapter 2: Ohm's Law
## Introduction
## The Three Quantities: V, I, R
## Stating Ohm's Law
## Common Mistakes with Sign Conventions
## Worked Example
## Summary
```

Reasonable placement:

1. `mascot-welcome` — after the `# Chapter 2` title, before `## Introduction`.
2. `mascot-thinking` — inside `## Stating Ohm's Law`, right after the
   first statement of `V = IR`.
3. `mascot-warning` — at the top of `## Common Mistakes with Sign Conventions`.
4. `mascot-celebration` — at the end of `## Summary`.

Total: 4. Comfortably under the ceiling, no back-to-backs, one of each
relevant type. `mascot-tip` and `mascot-encourage` are skipped because this
short chapter has no natural fit for them — forcing them in would be
decorative. A longer chapter with more distinct sections would legitimately
carry more.

## Outputs this guide produces

For each chapter processed:

1. A confirmed placement plan (shown to user before editing).
2. Updated chapter markdown with admonitions inserted.
3. Clean validation script output (zero flags).
4. Brief summary message listing what was added and where.

No new files are created outside the chapter being edited.

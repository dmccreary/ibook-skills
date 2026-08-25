# Content Generation Guide

Read this file **before** generating any student-facing content for
{{SITE_NAME}} — chapters, lesson plans, quizzes, FAQ entries, glossary prose,
or workshop material.

Instructor-facing content (teacher guides, instructor guides, answer keys)
is exempt from any persona/mascot guidance this file may later define.

<!--
  No learning mascot has been added yet. If this book adds one via the
  `book-installer` "learning-mascot" feature, that skill replaces this comment
  with a "## Learning Mascot" section containing the book's character identity
  followed by the placement rules, rendered by:

      python3 "$BK_HOME/skills/book-installer/scripts/render-mascot-guide.py"

  The rules arrive between BEGIN/END "mascot-placement-rules" sentinel comments
  and are regenerated from the single canonical source at
  book-installer/references/mascot-placement-rules.md. Never write mascot
  placement rules here by hand, and never edit inside the sentinels -- the next
  re-render discards those edits.
-->

---

## Concept Depth & Word-Count Targets

Not every concept deserves equal space. A concept that many other concepts
depend on — directly or transitively — needs more careful explanation, since
a shaky foundation cascades into everything built on top of it, while a leaf
concept that nothing depends on can be treated more lightly.

**This is driven by each concept's Concept Impact Score (CIS)**, a
PageRank-style recursive importance measure computed by
`learning-graph-generator` (v1.06+) and written into `learning-graph.json` as
`node.cis`: `CIS(x) = 1 + sum(CIS(d) for d in direct dependents of x)`. CIS
is a strictly better importance signal than a plain dependents count because
it captures *transitive* impact — a concept with only one or two direct
dependents can still be highly foundational if those dependents themselves
have many dependents, which raw in-degree misses entirely.

`book-chapter-generator` (v1.0.0+) writes each concept's CIS into its
chapter's "Concepts Covered" table, and `chapter-content-generator` (v1.09+)
converts CIS into a per-concept word-count and required-element budget in its
**Elaboration Budget** step (Step 2.3b): CIS is normalized globally against
the book's maximum CIS into an Elaboration Score `E(c)`, then assigned a tier:

| Tier | `E(c)` range | Target words | Required elements |
|------|--------------|---------------|--------------------|
| A (full treatment) | `>= 0.5` | 500-750 | worked example + diagram/chart/table/MicroSim |
| B (standard) | `0.2 <= E(c) < 0.5` | 250-400 | worked example |
| C (brief) | `< 0.2` | 120-200 | clear definition; example optional |

A chapter's total word count is the **sum** of its concepts' individual
targets, not an independent flat number — a chapter with several Tier A
concepts will naturally run longer than one of mostly Tier C concepts, and
that variation is intentional, not something to normalize away.

For the exact normalization formula, tier cut-points, and worked table
format, see `skills/chapter-content-generator/SKILL.md`, Step 2.3b
("Compute the Elaboration Budget (CIS-Driven)") — that skill is the
canonical source; this section is a summary so writers know the *why*
without duplicating the math in two places that could drift out of sync.

## Anti-Padding & Writing Style Rules

Models inflate text to hit word-count targets, producing repetitive and
sometimes hallucinated content. All generating agents must follow these rules.

1. **Quality over quantity.** Per-concept Elaboration Budgets (see *Concept
   Depth & Word-Count Targets* above) are guidelines, not requirements. A
   dense, correct chapter beats a padded one at the target length. Never
   inflate length artificially — a Tier A concept should reach its target
   through a worked example or MicroSim walkthrough, never restated prose,
   and a Tier C concept should stop once it is correctly explained even if
   that's well under its target.
2. **Expand by showing, not telling.** If a chapter is genuinely thin, add a
   concrete worked example, another MicroSim, or more technical detail. Never
   expand by restating earlier paragraphs, summarizing what was just said, or
   adding generic filler.
3. **No formulaic templates.** Avoid boilerplate scaffolding like "Let's talk
   about X. The concept of X is fundamental…". Weave concepts into flowing
   narrative prose.
4. **Examples over prose.** When explaining abstract logic, prefer a short
   commented example or a MicroSim to a long descriptive passage.

## MicroSims (Interactive Examples)

This book targets Level 2+ textbook intelligence, so interactivity is a
pedagogical requirement rather than a garnish.

- **Requirement**: whenever a concept can be illustrated with a dynamic,
  interactive example, include a MicroSim rather than describing it in prose.
- **Format**: embed finished MicroSims with an `<iframe>` pointing at the
  simulation's `main.html`, followed by a fullscreen button link.
- **Tools**: p5.js for physics, graphics, and simulation; Chart.js for data;
  vis-network for graphs; Mermaid for flow and sequence diagrams.

## Markdown Formatting Rules

1. **List spacing.** EVERY Markdown list — bulleted or numbered — MUST have a
   blank line before it. MkDocs will not render the list otherwise.
2. **Image paths.** Markdown images `![alt](path)` resolve relative to the
   **source `.md` file's directory**; raw HTML `<img src>` resolves relative
   to the **rendered URL**. These differ for any page not directly under
   `docs/` — get this wrong and the page still displays but `mkdocs build
   --strict` fails with a "target is not found among documentation files"
   warning.
3. **Admonition bodies** are indented four spaces.

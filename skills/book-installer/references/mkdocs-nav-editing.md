<!-- Canonical copy. Do not fork into other skills; reference by path:
     $BK_HOME/skills/book-installer/references/mkdocs-nav-editing.md

     `$BK_HOME` points at the ibook-skills checkout and is agent-neutral.
     Do NOT use a path under `~/.claude/skills/`, `~/.codex/skills/`, or
     `~/.gemini/antigravity/skills/` — each is specific to one agent
     framework, and these skills run on all of them. If `$BK_HOME` is
     unset, the file is at
     `book-installer/references/mkdocs-nav-editing.md` relative to the
     skills root that contains the calling skill. -->

# Editing mkdocs.yml Navigation — Canonical Rules

Every content skill that adds pages to an intelligent textbook (chapters,
glossary, FAQ, quizzes, references, reports) must edit the `nav:` section of
`mkdocs.yml`. These are the shared rules; the invoking skill says *what* to
add, this guide says *how* to add it safely.

## Core Rules

1. **Read before write.** Always read the current `mkdocs.yml` immediately
   before editing. Never edit from a stale copy earlier in the conversation.
2. **Serialize nav edits.** Never let two agents (or two parallel tasks)
   modify `mkdocs.yml` at the same time — concurrent edits cause
   inconsistencies that require manual repair. If a batch workflow generates
   many chapters/quizzes in parallel, collect the nav changes and apply them
   in ONE edit at the end.
3. **Only touch your section.** Add or update the entries the invoking skill
   owns; do not remove, reorder, or "clean up" other navigation entries.
4. **Preserve YAML structure.** Match the existing indentation. A `nav:` block
   is order-sensitive — insert new entries in the conventional position
   (see placement table) rather than appending blindly.
5. **Never add `navigation.tabs`.** These books use side navigation optimized
   for wide landscape screens. If you see `navigation.tabs` in
   `theme.features`, tell the user to remove it.
6. **Verify after editing.** Confirm no nav entry points at a file that does
   not exist (`mkdocs build --strict` catches this).

## Conventional Placement

| Artifact | Where in nav |
|----------|--------------|
| Chapters | Under `Chapters:` after `List of Chapters: chapters/index.md` |
| Per-chapter quiz / references | Nested under that chapter's entry |
| Glossary | Near the end, before License/Contact |
| FAQ | Near the end, adjacent to Glossary |
| Quality reports (quiz, FAQ, diagrams, metrics) | Under `Learning Graph:` |
| About page | Last |

## Chapter Label Convention

The nav sidebar is narrow. Do **not** spell out "Chapter X" in chapter labels —
use the number only, since the `Chapters:` heading sits above the list:

```yaml
nav:
  - Chapters:
    - List of Chapters: chapters/index.md
    - 1. Introduction to AI: chapters/01-intro-ai/index.md
    - 2. Getting Started: chapters/02-getting-started/index.md
```

When a chapter gains sub-pages (quiz, references), nest them and label the
main page `Content:` (again, no "Chapter" prefix in the label):

```yaml
    - 1. Introduction to AI:
      - Content: chapters/01-intro-ai/index.md
      - Quiz: chapters/01-intro-ai/quiz.md
      - Annotated References: chapters/01-intro-ai/references.md
```

## End-of-Nav Artifacts

```yaml
nav:
  # ... chapters, learning graph ...
  - FAQ: faq.md
  - Glossary: glossary.md
  - License: license.md
  - Contact: contact.md
```

## Learning-Graph Reports

```yaml
  - Learning Graph:
    # ... existing learning graph pages ...
    - FAQ Quality Report: learning-graph/faq-quality-report.md
    - FAQ Coverage Gaps: learning-graph/faq-coverage-gaps.md
    - Quiz Generation Report: learning-graph/quiz-generation-report.md
    - Diagrams Table: learning-graph/diagram-table.md
    - Diagrams Details: learning-graph/diagram-details.md
```

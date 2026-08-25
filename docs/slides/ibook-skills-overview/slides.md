---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- _class: lead -->
# Agent Skills for Intelligent Textbooks

## Automating intelligent textbook generation

A ~3,500-hour authoring task, done in ~10 hours

---

# Built for Claude — Portable Everywhere

- Originally written for Anthropic's Claude Code skill system
- Same `SKILL.md` + `CLAUDE.md` pattern now runs in any AI IDE that supports "skills"
- Verified working in OpenAI Codex, Google Gemini, Cursor, Perplexity, and Hermes
- Just copy `CLAUDE.md` → `AGENTS.md`

<!--
Presenter note: one caveat — skills that rely on Claude's image-understanding
(e.g. reviewing a MicroSim screenshot for layout errors) are Claude-specific
and don't port cleanly to IDEs without equivalent vision tooling.
-->

---

# One Pipeline, Start to Finish

- **`init-textbook`** scaffolds a brand-new project — `mkdocs.yml`, `docs/` tree, starter pages
- 12-step pipeline: description → Bloom's outcomes → 200 concepts → dependency DAG → taxonomy → learning graph → chapter structure → content → MicroSims → glossary/FAQ/quiz → QA → deploy
- **`book-installer`** installs supporting infrastructure and runs quality checks along the way
- Ends with `mkdocs gh-deploy`

---

# Learning Graphs: the Backbone

- A **200-concept DAG** with Bloom's-Taxonomy tagging drives sequencing for the whole book
- `learning-graph-generator` builds it in five steps:
  - Enumerate concepts → map dependencies (CSV DAG)
  - Validate with `analyze-graph.py` (no cycles, no orphan nodes)
  - Categorize into 12 taxonomy groups
  - Convert to vis-network JSON with `csv-to-json.py`
- Nothing gets written in a chapter before its prerequisites exist

---

# Token Efficiency: Scripts, Not Re-Derivation

- Repetitive, deterministic work is pushed into bundled **Python utilities**, not redone in-context every time
- Example: `microsim-generator`'s batch utilities (parsing specs, scaffolding files, fixing iframes, updating nav) save **~430K tokens per batch run**
- Frees the model's attention for the part that actually needs judgment — writing the visualization logic itself

---

# Mascots: Part of Book-Installer, Not a Standalone Skill

- Lives inside `book-installer` as the **learning-mascot** capability
- Designs a pedagogical-agent persona (name, appearance, voice, catchphrase)
- Generates AI image prompts for consistent mascot poses
- Implements it via custom CSS admonitions with the image floated in the body
- Goal: engagement, wayfinding, and brand identity — not just decoration

---

# Supplementary Content Tour

- **`glossary-generator`** — ISO 11179-compliant definitions from the concept list *(200 terms in this site)*
- **`faq-generator`** — FAQ set from content + learning graph + glossary, once ~30% of chapters exist *(64 questions)*
- **`quiz-generator`** — Bloom's-aligned multiple-choice questions per chapter *(520 questions)*

---

# Mini Graphic Novels for Historical Context

- **`story-generator`** — illustrated narratives about scientists, mathematicians, and historical figures
- Default: **12 panels + 1 cover** (configurable 4–16 via `--panels N`)
- Each panel: narrative paragraph + a detailed image-generation prompt
- Can auto-generate every panel image (Gemini / gpt-image-1) at **~$0.039/image** — about $0.51 for a full 13-image story

---

# Getting Started

1. Symlink skills into every agent via `scripts/bk-install-skills`
2. Run **`init-textbook`** to scaffold a new project
3. Run **`course-description-analyzer`**, then **`learning-graph-generator`**
4. Follow the 12-step pipeline chapter by chapter

---

<!-- _class: lead -->
# What's Next: 10 Hours → 4 Hours

- This is a roadmap, not a shipped feature
- Push more repetitive work out of model context into scripts — the same shift already made for MicroSims
- Tighten the handoffs between the 12 pipeline steps so less manual re-prompting is needed between stages

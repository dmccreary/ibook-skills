# MicroSim Batch Processing Utilities

Python scripts for extracting, scaffolding, validating, and managing MicroSim
specifications in MkDocs intelligent textbook projects. Standard library only,
Python 3.7+.

## Overview

These utilities eliminate repetitive work when batch-generating MicroSims:

| Script | Purpose | Token Savings |
|--------|---------|---------------|
| `extract-sim-specs.py` | Parse specs from chapter markdown | ~80K |
| `generate-sim-scaffold.py` | Create main.html / index.md / metadata.json | ~150K |
| `update-mkdocs-nav.py` | Regenerate MicroSims nav section | ~100K |
| `generate-sims-index.py` | Build the `docs/sims/index.md` thumbnail gallery | ~40K |
| `add-iframes-to-chapter.py` | Insert missing iframes + fix heights/paths | ~50K |
| `sync-iframe-heights.py` | Set every sim iframe to `CANVAS_HEIGHT + 2` (own page + all embeds) | ~40K |
| `validate-sims.py` | 100-point quality rubric scoring | ~50K |

## Workflow

```
Chapter Markdown
       │
       ▼
  extract-sim-specs.py ──→ specs.json + sim-status.json
       │
       ▼
  generate-sim-scaffold.py ──→ main.html, index.md, metadata.json
       │
       ▼
  [Agent writes .js file]
       │
       ▼
  add-iframes-to-chapter.py ──→ iframes in chapter markdown
       │
       ▼
  update-mkdocs-nav.py ──→ mkdocs.yml nav updated
       │
       ▼
  validate-sims.py ──→ quality scores
```

## Scripts

### extract-sim-specs.py

Parse spec headers from chapter markdown and extract `<details>` block
specifications. A spec header is a level-4 heading whose first word is one of
`Diagram`, `Drawing`, `MicroSim`, `Timeline`, `Chart`, `Infographic`,
`Workflow` or `Map` (for example `#### MicroSim: SIR Simulator`). The list is
`SPEC_HEADING_TYPES` in `shared.py`, shared with `add-iframes-to-chapter.py`;
add a word there if a book uses another one.

```bash
# Extract all specs to JSON
python3 extract-sim-specs.py --project-dir /path/to/project --output specs.json --verbose

# Single chapter
python3 extract-sim-specs.py --project-dir /path/to/project --chapter 03-angles-and-relationships --output ch03-specs.json

# Generate sim-status.json lifecycle tracking
python3 extract-sim-specs.py --project-dir /path/to/project --status-file sim-status.json --verbose
```

**Output fields:** `sim_id`, `title`, `summary`, `heading_type`, `chapter`,
`element_type`, `bloom_level`, `library`, `iframe_src`, `iframe_height`,
`spec_text`, `status`

### generate-sim-scaffold.py

Generate `main.html`, `index.md`, and `metadata.json` scaffold files from the
specs JSON. The agent then only needs to write the `.js` file.

```bash
# Scaffold all unbuilt sims
python3 generate-sim-scaffold.py --spec-file specs.json --project-dir /path/to/project --verbose

# Single sim (dry run)
python3 generate-sim-scaffold.py --spec-file specs.json --sim-id angle-explorer --dry-run

# Force overwrite existing scaffolds
python3 generate-sim-scaffold.py --spec-file specs.json --force

# Set the course values explicitly
python3 generate-sim-scaffold.py --spec-file specs.json \
    --subject "Data Science" --grade-level "11-12" --subject-area "Statistics"
```

**Subject, grade level and subject area:** each value written into `index.md`
(`### Grade Level`) and `metadata.json` (`subject`, `gradeLevel`,
`subjectArea`) comes from the first source that has one:

1. The `--subject`, `--grade-level` and `--subject-area` flags.
2. The project: `site_name` in `mkdocs.yml` for the subject, and the target
   audience in `docs/course-description.md` for the grade level (a
   `**Target Audience:**` line or a `## Target Audience` / `## Audience`
   heading). Explicit grades such as "grades 9–12" are used as written; other
   wording ("college freshmen", "graduate students") is mapped to the
   metadata schema's `gradeLevel` values on a best-effort basis.
3. A `TODO:` placeholder, with a warning naming the flag to pass.

Nothing in a project states its subject area, so pass `--subject-area` (one of
the schema's values, such as `Mathematics`, `Computer Science` or `Health`) to
avoid `TODO: subject area`. Run with `--verbose` to see the resolved values.
`geometry-course` keeps its original built-in values.

**Library-to-CDN mapping:** p5.js 1.11.10, vis-network 9.1.9, Chart.js 4.4.4,
Mermaid 10, Plotly 2.35.0, Leaflet 1.9.4, vis-timeline 7.7.3.

### update-mkdocs-nav.py

Scan `docs/sims/` for directories with `index.md` and regenerate the MicroSims
nav section in `mkdocs.yml`. Alphabetically sorted, idempotent.

```bash
# Preview changes
python3 update-mkdocs-nav.py --project-dir /path/to/project --dry-run --verbose

# Apply
python3 update-mkdocs-nav.py --project-dir /path/to/project
```

### generate-sims-index.py

Build the MicroSims gallery page at `docs/sims/index.md` — a responsive grid of
thumbnail cards, one per sim, each linking to the sim and showing its `.png`
screenshot (sims without a screenshot get a "no preview" placeholder). Titles
come from frontmatter `title` > first `# Heading` > directory name. The
gallery counterpart to `update-mkdocs-nav.py`; run both after a batch.

```bash
# Preview
python3 generate-sims-index.py --project-dir /path/to/project --dry-run --verbose

# Apply
python3 generate-sims-index.py --project-dir /path/to/project
```

### add-iframes-to-chapter.py

Find spec headers (`#### Diagram:`, `#### MicroSim:`, `#### Timeline:` and the
other words `extract-sim-specs.py` accepts) missing iframes and insert them.
Also fixes height typos (`500xp` → `500px`) and path issues.

```bash
# Single chapter, dry run
python3 add-iframes-to-chapter.py --chapter 11-circles --project-dir /path/to/project --dry-run --verbose

# All chapters, fix everything
python3 add-iframes-to-chapter.py --all --project-dir /path/to/project --fix-heights --fix-paths

# Just fix typos and paths
python3 add-iframes-to-chapter.py --all --project-dir /path/to/project --fix-heights --fix-paths --verbose
```

### sync-iframe-heights.py

Set every iframe that shows a sim to `CANVAS_HEIGHT + 2` — the sim's own
`docs/sims/<id>/index.md` **and** every page that embeds it. `CANVAS_HEIGHT`
is resolved per sim from the first source that has it:

1. `// CANVAS_HEIGHT: <n>` in the first ~15 lines of `<id>.js` (primary)
2. `"canvasHeight": <n>` in `metadata.json` — the consistent place for sims
   with **no `.js`** (Mermaid, vis-network, Chart.js, Leaflet, vis-timeline,
   Plotly, custom HTML)
3. `<!-- CANVAS_HEIGHT: <n> -->` in `main.html` (back-compat)
4. computed `drawHeight + controlHeight` (+ `graphHeight`) from `<id>.js`,
   then the `// CANVAS_HEIGHT` comment is inserted on line 2

The embed scan walks every `*.md` under `docs/` and matches iframes by the
`sims/<id>/main.html` path, so it is layout-agnostic — it handles the standard
`docs/chapters/<chapter>/index.md` layout **and** the nested
`docs/bands/<band>/chapters/<chapter>/index.md` layout unique to the
`health-education` textbook. Poster embeds and the learning-graph viewer are
never touched.

```bash
# Preview
python3 sync-iframe-heights.py --project-dir /path/to/project --dry-run --verbose

# Apply
python3 sync-iframe-heights.py --project-dir /path/to/project

# Single sim
python3 sync-iframe-heights.py --project-dir /path/to/project --sim gradient-explorer

# Also backfill metadata.json canvasHeight (migrate no-.js sims to the structured store)
python3 sync-iframe-heights.py --project-dir /path/to/project --write-metadata
```

See the microsim-utils skill's `references/canvas-height-strategy.md` for the
full convention and how the height is communicated to downstream agents.

> `fix-iframe-heights.py` is the older, own-page-only predecessor
> (it does not update chapter embeds). Prefer `sync-iframe-heights.py`.

### validate-sims.py

Score MicroSims against a 100-point quality rubric.

```bash
# Validate single sim
python3 validate-sims.py --project-dir /path/to/project --sim angle-builder --verbose

# Validate all, show only low scores
python3 validate-sims.py --project-dir /path/to/project --min-score 0 --format table

# Export to JSON
python3 validate-sims.py --project-dir /path/to/project --output scores.json
```

**Scoring Rubric (100 points):**

| Category | Points | Checks |
|----------|--------|--------|
| main.html | 10 | exists (5), schema meta tag (3), `<main>` tag (2) |
| metadata.json | 30 | present (10), required fields (10), educational (5), pedagogical (5) |
| index.md structure | 35 | title (2), YAML basic (3), YAML images (5), iframe (10), fullscreen (5), iframe example (5), description (5) |
| image | 5 | screenshot PNG present |
| lesson plan | 10 | Lesson Plan section exists |
| references | 5 | References section exists |
| p5.js conventions | 5 | updateCanvasSize (2), no DOM buttons (2), querySelector parenting (1) |

The metadata.json checks accept both layouts. In the schema layout
(`{"microsim": {...}}`) the required fields are read from `microsim.dublinCore`,
educational from `microsim.educational`, and pedagogical from `microsim.usage`
(the schema has no `pedagogical` object). In the legacy flat layout they are
read from the top level, with pedagogical from a top-level `pedagogical` object.

## sim-status.json Schema

Generated by `extract-sim-specs.py --status-file`. Tracks the lifecycle of
every MicroSim across the project.

**Status lifecycle:** `specified` → `scaffolded` → `implemented` → `validated` → `deployed`

`reused` is a terminal state outside this progression: the chapter embeds an
existing MicroSim from another repo via an absolute iframe URL (`**Status:** Reused`
in the details block). Reused sims are treated as complete — `generate-todo.py`
excludes them from TODO.md and they never get scaffolded.

| Status | Detection |
|--------|-----------|
| `specified` | Has `<details>` spec in chapter but no sim directory |
| `scaffolded` | Directory with main.html/index.md but no substantive JS |
| `implemented` | JS file exists and >50 lines |
| `validated` | quality_score >= 70 |
| `deployed` | iframe in chapter AND validated |
| `reused` | `**Status:** Reused` in the chapter details block (existing sim in another repo) |

**Entry fields:**

```json
{
  "sim_id": "angle-builder",
  "title": "Angle Builder",
  "chapter": "03-angles-and-relationships",
  "bloom_level": "Apply",
  "library": "p5.js",
  "status": "deployed",
  "has_iframe": true,
  "quality_score": 85
}
```

## Shared Utilities (shared.py)

Common module imported by all scripts:

- `find_project_root()` — walk up to find mkdocs.yml
- `load_mkdocs_config()` — parse site_url, site_name (regex, no PyYAML)
- `kebab_case(title)` — title to directory name
- `parse_yaml_frontmatter(content)` — extract YAML block from markdown
- `detect_library(html)` — detect JS library from script tags
- ANSI color constants, unicode symbols
- `LIBRARY_CDNS` / `LIBRARY_CSS` — CDN URL mappings

## Design Constraints

- **Standard library only** — no pip dependencies
- **Python 3.7+** compatible
- All scripts support `--project-dir` (default: auto-detect), `--dry-run`, `--verbose`
- Idempotent operations
- `if __name__ == '__main__':` with argparse

## Batch Generation Workflow

For generating MicroSims across multiple chapters:

```bash
# 1. Extract all specs
python3 extract-sim-specs.py --project-dir $PROJECT \
    --output /tmp/specs.json --status-file /tmp/status.json --verbose

# 2. Scaffold unbuilt sims
python3 generate-sim-scaffold.py --spec-file /tmp/specs.json \
    --project-dir $PROJECT --verbose

# 3. [Agent implements .js files for each sim]

# 4. Insert iframes into chapters
python3 add-iframes-to-chapter.py --all --project-dir $PROJECT \
    --fix-heights --fix-paths --verbose

# 5. Update mkdocs.yml navigation
python3 update-mkdocs-nav.py --project-dir $PROJECT --verbose

# 6. Validate quality
python3 validate-sims.py --project-dir $PROJECT --output /tmp/scores.json
```

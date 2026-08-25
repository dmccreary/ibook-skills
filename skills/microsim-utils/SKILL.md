---
name: microsim-utils
description: Utility tools for MicroSim management including quality validation, screenshot capture, icon management, index page generation, iframe height synchronization, iframe control-visibility testing, visual layout review, and diagram/MicroSim coverage reports across chapters. Routes to the appropriate utility based on the task needed.
metadata:
  ibook.version: "1.0"
---

# MicroSim Utilities

**Version:** 1.0

## Overview

This meta-skill provides utility functions for managing and maintaining MicroSims in intelligent textbook projects. It consolidates five utility skills into a single entry point with on-demand loading of specific utility guides.

## When to Use This Skill

Use this skill when users request:

- Validating MicroSim quality and standards
- Capturing screenshots for preview images
- Adding or managing icons for MicroSims
- Generating index pages for MicroSim directories
- Quality scoring and standardization checks
- Synchronizing iframe heights from JS source files
- Setting up runtime iframe auto-resize via postMessage
- Scaffolding MicroSim directories (main.html, index.md, metadata.json) from TODO JSON specs
- Testing whether interactive controls are fully visible inside the iframe (Playwright)
- Reviewing a MicroSim's visual layout for rendering defects (Claude Vision)
- Auditing diagram/MicroSim coverage across chapters (status, difficulty, Bloom's levels)

## Step 1: Identify Utility Type

Match the user's request to the appropriate utility guide:

### Routing Table

| Trigger Keywords | Guide File | Purpose |
|------------------|------------|---------|
| standardize, quality, validate, score, check, audit | `references/standardization.md` | Quality validation and scoring |
| screenshot, capture, preview, image, thumbnail | `references/screen-capture.md` | Automated screenshot generation |
| icons, add icons, favicon, logo | `references/add-icons.md` | Icon management for MicroSims |
| index page, microsim list, grid, directory, catalog, update the microsim listings, update the list of microsims, create a grid view, generate a listing | `references/index-generator.md` | Generate index page with grid cards |
| TODO, todo json, extract specs, diagram specs, unimplemented, create microsim todo, todo files, extract diagrams, unimplemented microsims | `scripts/create-microsim-todo-json-files.py` | Extract unimplemented diagram specs into TODO JSON files |
| scaffold microsims, scaffold from todo, scaffold sims, create microsim stubs, generate microsim scaffolding, stub out microsims, create scaffold files, generate scaffold from json, microsim stubs from todo | `scripts/scaffold-microsims-from-todo.py` | Generate `main.html`, `index.md`, and `metadata.json` stub files for each TODO JSON spec that does not yet have an implementation |
| fix iframe heights, sync iframe heights, correct iframe heights, iframe height, canvas height, sync heights, update iframe heights | `scripts/sync-iframe-heights.py` | Set every sim iframe to CANVAS_HEIGHT + 2, resolving CANVAS_HEIGHT from the .js comment / metadata.json / main.html / computed vars, across the sim's own index.md and all embeds |
| canvas height strategy, where is the height stored, height convention, how do iframe heights work, store height for mermaid/vis-network, metadata canvasHeight, no js height | `references/canvas-height-strategy.md` | The build-time height convention: resolution order, per-library storage, metadata.json fallback, and downstream hand-off |
| iframe auto height, iframe auto resize, iframe postMessage, runtime iframe resize, microsim auto resize, auto-size iframe, iframe self-resize | `references/iframe-auto-height.md` | Runtime postMessage protocol so embedded MicroSims report their own height to the parent page |
| test iframe, controls clipped, controls cut off, are controls visible, test iframe heights, verify controls fit, check if sims fit, iframe visibility | `references/iframe-tester.md` (runs `scripts/test-iframe-heights.py`) | Playwright check that every interactive control is fully visible inside the iframe at its declared height |
| review layout, layout review, looks off, looks wrong, clipped labels, overlapping controls, residual stroke, draw order, visual QA, review the sim | `references/layout-reviewer.md` | Claude Vision review of a sim's rendered layout — walks a checklist, diagnoses defects, patches source |
| diagram report, diagram reports, visualization coverage, audit diagrams, audit microsims, diagram status, microsim status report | `references/diagram-reports.md` (runs `scripts/diagram-report.py`) | Generate status reports of all diagrams/MicroSims across chapters (type, status, Bloom's levels, UI complexity, difficulty) |

### Decision Tree

```
Need to check MicroSim quality/standards?
  → YES: standardization.md

Need to capture screenshots for previews?
  → YES: screen-capture.md

Need to add or manage icons?
  → YES: add-icons.md

Need to generate/update the MicroSim index page?
  → YES: index-generator.md

Need to extract unimplemented diagram specs into TODO files?
  → YES: Run scripts/create-microsim-todo-json-files.py

Need to scaffold sim directories (main.html, index.md, metadata.json) from those TODO JSON files?
  → YES: Run scripts/scaffold-microsims-from-todo.py

Need to fix, sync, or correct iframe heights?
  → YES: Run scripts/sync-iframe-heights.py

Need iframes to auto-resize at runtime via postMessage?
  → YES: references/iframe-auto-height.md

Need to verify interactive controls are fully visible inside the iframe?
  → YES: references/iframe-tester.md (runs scripts/test-iframe-heights.py)

Need to review whether a sim's rendered layout looks right (not just fits)?
  → YES: references/layout-reviewer.md

Need a status report of all diagrams/MicroSims across chapters?
  → YES: references/diagram-reports.md (runs scripts/diagram-report.py)
```

### Iframe-height utilities at a glance

Three utilities touch iframe height — they are complementary, not redundant:

| Utility | Question it answers | Tool |
|---------|--------------------|------|
| `scripts/sync-iframe-heights.py` | "Do all iframes use the sim's `CANVAS_HEIGHT` + 2?" (build-time) | Python |
| `references/canvas-height-strategy.md` | "Where is `CANVAS_HEIGHT` stored for each library type, and how does it flow?" (convention) | Doc |
| `references/iframe-tester.md` | "Do the controls actually fit at that height?" (geometric) | Playwright |
| `references/layout-reviewer.md` | "Does the rendering *inside* the canvas look right?" (visual) | Claude Vision |

## Step 2: Load the Matched Guide or Run the Script

For reference-based utilities, read the corresponding guide file from `references/` and follow its workflow.

For Python script utilities, run the script directly:

**TODO JSON extractor:**
```bash
python3 /path/to/skills/microsim-utils/scripts/create-microsim-todo-json-files.py --project-dir /path/to/project
```
Report the summary output to the user (chapters scanned, total specs found, already implemented, TODO files written, output directory).

**Scaffold from TODO JSON:**
```bash
python3 /path/to/skills/microsim-utils/scripts/scaffold-microsims-from-todo.py --project-dir /path/to/project
```
Report the summary output to the user (TODO specs processed, scaffolded, skipped). Use `--force` only if the user explicitly asks to regenerate stubs; the script never overwrites an existing `main.html` regardless of `--force`.

**Iframe height sync:**
```bash
python3 /path/to/skills/microsim-utils/scripts/sync-iframe-heights.py --project-dir /path/to/project --verbose
```
Report the summary output to the user (sims synced, CANVAS_HEIGHT comments inserted, iframe heights updated).

## Step 3: Execute Utility

Each guide contains:
1. Purpose and use cases
2. Prerequisites
3. Step-by-step workflow
4. Output format
5. Best practices

## Available Utilities

### standardization.md

**Purpose:** Validate MicroSim quality against standards

**Checks:**
- Required file presence (main.html, index.md)
- Code structure and patterns
- Accessibility features
- Documentation completeness
- Responsive design implementation

**Output:** Quality score (0-100) with recommendations

### screen-capture.md

**Purpose:** Capture high-quality screenshots for social media previews

**Script:** `~/.local/bin/bk-capture-screenshot <microsim-directory-path>`

**Features:**
- Uses Chrome headless mode with localhost server
- Handles JavaScript-heavy visualizations (p5.js, vis-network, Chart.js)
- Waits 3 seconds for proper rendering
- Creates consistent 1200x800 image sizes

**Output:** PNG screenshot named `{microsim-name}.png` in MicroSim directory

### add-icons.md

**Purpose:** Add favicon and icons to MicroSim directories

**Creates:**
- favicon.ico
- apple-touch-icon.png
- Other platform-specific icons

### index-generator.md

**Purpose:** Generate comprehensive MicroSim index page

**Creates:**
- Grid-based card layout
- Screenshots for each MicroSim
- Alphabetically sorted entries
- MkDocs Material card format
- Updates mkdocs.yml navigation

### create-microsim-todo-json-files.py

**Purpose:** Extract unimplemented MicroSim diagram specifications from chapter content and create TODO JSON files

**Script:** `scripts/create-microsim-todo-json-files.py --project-dir /path/to/project`

**How it works:**
- Scans all `docs/chapters/*/index.md` files for `#### Diagram:` headers
- Extracts sim-id, library, Bloom level, learning objective, and full specification from `<details>` blocks
- Skips any sim-id that already has a directory with `main.html` under `docs/sims/`
- Writes one JSON file per unimplemented diagram to `docs/sims/TODO/`

**Output:** Individual JSON files in `docs/sims/TODO/{sim-id}.json` with fields:
- `sim_id`, `diagram_name`, `chapter_number`, `chapter_title`
- `library`, `bloom_level`, `bloom_verb`, `learning_objective`
- `completion_status: "specified"`, `extracted_date`, `specification`

**Important:** Always pass `--project-dir` pointing to the project root (the directory containing `mkdocs.yml`). If omitted, the script walks up from its own location to find `mkdocs.yml`, which may find the wrong project.

### scaffold-microsims-from-todo.py

**Purpose:** Generate scaffold (stub) files for each MicroSim that has a TODO JSON spec but no implementation yet. This is the natural next step after `create-microsim-todo-json-files.py`.

**Script:** `scripts/scaffold-microsims-from-todo.py --project-dir /path/to/project`

**How it works:**
- Reads each `docs/sims/TODO/<sim-id>.json`
- For any sim-id that does NOT already have `docs/sims/<sim-id>/main.html`, creates the directory with three stub files:
  - `main.html` — placeholder canvas with the spec embedded as a comment
  - `index.md` — frontmatter, learning objective, iframe embed, full spec
  - `metadata.json` — mapped from the TODO JSON
- Skips any sim-id whose `main.html` already exists (so real implementations are never clobbered)

**Flags:**
- `--project-dir` — Project root containing `mkdocs.yml` (required or auto-detected)
- `--force` — Overwrite existing `index.md` and `metadata.json` stubs. **Never** overwrites an existing `main.html`, even with `--force`, because that file may contain a real implementation.

**Output:** Summary showing TODO specs processed, scaffolded, and skipped (already implemented).

**Important:** Always pass `--project-dir` pointing to the project root. The script auto-detects by walking up from cwd to find `mkdocs.yml` if omitted.

### sync-iframe-heights.py

**Purpose:** Set every iframe that shows a sim to `CANVAS_HEIGHT + 2`, using
each sim's resolved `CANVAS_HEIGHT` as the single source of truth. See
[`references/canvas-height-strategy.md`](references/canvas-height-strategy.md)
for the full convention (resolution order, per-library storage, downstream
hand-off).

**Script:** `scripts/sync-iframe-heights.py --project-dir /path/to/project`

**How it works:**
- Resolves each sim's `CANVAS_HEIGHT` from the first source that has it:
  1. `// CANVAS_HEIGHT: <int>` in the first ~15 lines of `<id>.js` (primary)
  2. `"canvasHeight": <int>` in `metadata.json` (the consistent place for sims with **no `.js`** — Mermaid, vis-network, Chart.js, Leaflet, vis-timeline, Plotly, custom HTML)
  3. `<!-- CANVAS_HEIGHT: <int> -->` in `main.html` (back-compat)
  4. computed `drawHeight + controlHeight` (+ `graphHeight`) from `<id>.js`, then **inserts** the `// CANVAS_HEIGHT` comment on line 2
- Sets iframe height = `CANVAS_HEIGHT + 2` (2px for iframe border) in:
  - The sim's own `docs/sims/<id>/index.md`
  - **Every** page under `docs/` that embeds the sim, matched by the `sims/<id>/main.html` path. Layout-agnostic: handles the standard `docs/chapters/<chapter>/index.md` **and** the nested `docs/bands/<band>/chapters/<chapter>/index.md` used only by the health-education textbook, plus teacher guides. Poster embeds and the learning-graph viewer are never touched.
- Reports all changes with colored output

**Flags:**
- `--project-dir` — Project root containing `mkdocs.yml` (required or auto-detected)
- `--sim <sim-id>` — Sync a single sim instead of all
- `--dry-run` — Preview changes without writing files
- `--write-metadata` — Backfill each sim's `metadata.json` `canvasHeight` field (off by default; use once to migrate no-`.js` sims into the structured store)
- `--verbose` — Show the resolved height and source for every sim

**Output:** Summary showing sims resolved (by source), iframe heights updated (own-index vs embeds), and any metadata backfilled.

**Important:** Always pass `--project-dir` pointing to the project root. The script auto-detects by walking up from cwd to find `mkdocs.yml` if omitted.

### iframe-auto-height.md

**Purpose:** Runtime alternative to `sync-iframe-heights.py`. Documents the
two-part `postMessage` protocol that lets an embedded MicroSim report its
own measured content height to the parent page, which then resizes the
iframe automatically.

**When to use:** Sims with responsive or content-dependent heights that
are hard to predict at build time (e.g., diagram-overlay sims whose height
depends on the longest callout text). Coexists with `sync-iframe-heights.py`
without conflict.

**What's in the guide:**
- The `'microsim-resize'` message contract (type, height fields)
- Drop-in parent-side listener block for `docs/js/extra.js`
- Child-side reporter snippets for diagram-overlay, p5.js, and Mermaid sims
- Why to match by `event.source === iframe.contentWindow` (not by URL)
- Caveats: one-shot vs. live, target origin, sandbox attributes, fullscreen mode
- Reference implementation paths in the `digital-citizenship` project

**Setup is one-time per project:** add the listener block once to
`docs/js/extra.js`, then any MicroSim that posts the `microsim-resize`
message participates automatically.

### iframe-tester.md

**Purpose:** Verify that every interactive control (button, slider, dropdown,
checkbox) is fully visible inside the iframe at its declared height — a
geometric check using a real headless browser.

**Script:** `scripts/test-iframe-heights.py` (Playwright)

**How it works:**
- Finds all MicroSim directories under `docs/sims/`
- Reads each `index.md` to get the declared iframe height
- Loads `main.html` in a viewport constrained to that height
- Checks every interactive element's bounding box against the iframe boundary
- Reports PASS/FAIL with a suggested height for failures

**Prerequisites:** `pip install playwright && playwright install chromium`

**When to use:** controls appear clipped at the bottom of a sim, or auditing
iframe sizing across all sims after a batch generation. Complements
`sync-iframe-heights.py` (which propagates the height) — run the tester to
confirm the propagated height actually works.

> A legacy Node.js version was retired during consolidation; the Python script
> is the only supported implementation.

### layout-reviewer.md

**Purpose:** Review a sim's *rendered* layout with Claude Vision — catches
defects geometric checks miss: clipped row labels, overlapping controls, text
rendered with residual strokes, panel overflow, low-contrast labels, draw-order
bugs, and library-specific rendering issues.

**Tool:** Claude Vision (reads the screenshot PNG directly) + `bk-capture-screenshot`

**How it works:**
- Reads the iframe height from `index.md`, captures a screenshot at that height
- Walks `references/visual-checklist.md` item by item (PASS / FAIL / N/A)
- For each FAIL, consults `references/common-fixes.md` and applies the smallest
  patch
- Re-captures and re-walks; stops after 3 review-patch cycles

**Reference files:** `references/visual-checklist.md` (every item to inspect),
`references/common-fixes.md` (symptom → root cause → edit).

**When to use:** right after generating a new sim (proactive QA), or when the
iframe height is correct but something *inside* the canvas looks wrong. For
"controls clipped at the edge" only, run `iframe-tester.md` first.

## Examples

### Example 1: Quality Check
**User:** "Check if my bouncing-ball MicroSim meets standards"
**Routing:** Keywords "check", "standards" → `references/standardization.md`
**Action:** Read standardization.md and follow its workflow

### Example 2: Capture Screenshot
**User:** "Create a preview image for the timeline MicroSim"
**Routing:** Keywords "preview", "image" → `references/screen-capture.md`
**Action:** Run `~/.local/bin/bk-capture-screenshot /path/to/docs/sims/timeline`

### Example 3: Update Index
**User:** "Update the MicroSim index page with all new sims"
**Routing:** Keywords "index", "update" → `references/index-generator.md`
**Action:** Read index-generator.md and follow its workflow

### Example 4: Create TODO JSON Files
**User:** "Create MicroSim TODO JSON files"
**Routing:** Keywords "TODO", "create microsim todo" → `scripts/create-microsim-todo-json-files.py`
**Action:** Run `python3 scripts/create-microsim-todo-json-files.py --project-dir /path/to/project` and report results (chapters scanned, specs found, already implemented, TODO files written)

### Example 5: Scaffold MicroSims from TODO JSON
**User:** "scaffold the microsims" or "create the stub files for the TODO sims" or "generate scaffold files from the JSON specs"
**Routing:** Keywords "scaffold microsims", "stub out microsims", "scaffold from todo" → `scripts/scaffold-microsims-from-todo.py`
**Action:** Run `python3 scripts/scaffold-microsims-from-todo.py --project-dir /path/to/project` and report results (TODO specs processed, scaffolded, skipped). Typically follows immediately after `create-microsim-todo-json-files.py`.

### Example 6: Fix Iframe Heights
**User:** "fix the iframe heights" or "sync the iframe heights" or "correct the iframe heights"
**Routing:** Keywords "fix iframe heights", "sync iframe heights", "correct iframe heights" → `scripts/sync-iframe-heights.py`
**Action:** Run `python3 scripts/sync-iframe-heights.py --project-dir /path/to/project --verbose` and report results (sims synced, comments inserted, iframe heights updated)

### Example 7: Set Up Iframe Auto-Resize
**User:** "make the iframes auto-size" or "set up iframe auto height" or "I want microsims to report their own height"
**Routing:** Keywords "iframe auto height", "auto-size iframe", "iframe postMessage" → `references/iframe-auto-height.md`
**Action:** Read `iframe-auto-height.md` and follow the two-part setup: paste the parent-side listener block at the top of `docs/js/extra.js`, then ensure the relevant MicroSims post `{ type: 'microsim-resize', height }` after layout settles. Confirm both sides are in place and report which sims now participate.

### Example 8: Test Iframe Control Visibility
**User:** "check if my sims fit" or "are the controls visible" or "test iframe heights"
**Routing:** Keywords "check if sims fit", "controls visible", "test iframe heights" → `references/iframe-tester.md`
**Action:** Read `iframe-tester.md`, ensure Playwright is installed, then run `python3 scripts/test-iframe-heights.py --sims-dir docs/sims` and present the PASS/FAIL table. Offer to fix failing heights.

### Example 9: Review a Sim's Visual Layout
**User:** "this sim looks off" or "review the layout" or "the labels look clipped"
**Routing:** Keywords "looks off", "review layout", "clipped labels" → `references/layout-reviewer.md`
**Action:** Read `layout-reviewer.md`, capture a screenshot at the sim's iframe height, read the PNG with Claude Vision, walk `visual-checklist.md`, and patch defects per `common-fixes.md` (max 3 cycles).

## Common Workflows

### After Creating New MicroSim
1. Run `standardization.md` to validate quality
2. Run `~/.local/bin/bk-capture-screenshot <microsim-path>` to create preview image
3. Run `references/layout-reviewer.md` (Claude Vision) to catch rendering defects
4. Run `references/iframe-tester.md` (Playwright) to confirm controls fit at the iframe height
5. Run `index-generator.md` to add to index page

### Bulk Quality Audit
Use `standardization.md` to audit all MicroSims in a project and generate a quality report.

## Integration Notes

These utilities work with the standard MicroSim directory structure:
```
docs/sims/<microsim-name>/
├── main.html       # Main visualization
├── index.md        # Documentation
├── *.js            # JavaScript code
├── style.css       # Styles (optional)
└── <name>.png      # Preview screenshot (created by screen-capture)
```

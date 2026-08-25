---
name: microsim-generator
description: Creates interactive educational MicroSims, routing to the best-matched generator - p5.js, Chart.js, Plotly, Mermaid, vis-network, timelines, maps, Venn, causal-loop/feedback-loop diagrams (CLD), concept-classifier sorting quizzes, infographic overlays with callout labels, Docker Python labs (runnable code blocks), and fact-verified statistics posters (every numeric claim checked against a cited source before rendering). Generates complete MicroSim packages with HTML, JavaScript, CSS, documentation, and metadata.
model: opus
metadata:
  ibook.version: "1.0"
---

# MicroSim Generator

**Version:** 1.0

## Overview

This meta-skill routes MicroSim creation requests to the appropriate specialized generator based on visualization requirements. It consolidates 17 individual MicroSim generator skills into a single entry point with on-demand loading of specific implementation guides.

Six Python batch utilities in `src/microsim-utils/` automate the repetitive parts of MicroSim generation (parsing specs, scaffolding files, inserting iframes, fixing iframe heights, validating quality, updating navigation), saving ~430K tokens per batch run. The agent's creative work is focused on writing the `.js` file.

## Default Sequential Execution

When the microsim generator skill us used on all of the #### Diagram elements
of a chapter, always run the microsim generator tasks sequentially unless
the user specifically uses the phrase "execute in parallel".

## When to Use This Skill

Use this skill when users request:

- Interactive educational visualizations
- Data visualizations (charts, graphs, plots)
- Timelines or chronological displays
- Geographic/map visualizations
- Network diagrams or concept maps
- Flowcharts or workflow diagrams
- Mathematical function plots
- Set diagrams (Venn)
- Priority matrices or bubble charts
- Custom simulations or animations
- Comparison tables with ratings
- Matrix comparisons with expandable cell details
- Fact-verified infographic posters where every statistic is traced to a cited source
- Batch generation of MicroSims for a chapter

---

## Step 0: Environment Setup

Before any generation work, establish paths and determine scope.

### 0.1 Set Paths

```bash
# Python utilities live in the ibook-skills repo
UTILS="$HOME/Documents/ws/ibook-skills/src/microsim-utils"

# Detect project root (directory containing mkdocs.yml)
PROJECT=$(python3 -c "
import os, sys
d = os.path.abspath('.')
while d != os.path.dirname(d):
    if os.path.isfile(os.path.join(d, 'mkdocs.yml')): print(d); sys.exit()
    d = os.path.dirname(d)
print('ERROR: mkdocs.yml not found', file=sys.stderr); sys.exit(1)
")
```

If the scripts are not found at `$UTILS`, check for them in the project's own `src/microsim-utils/` directory.

### 0.2 Determine Scope

| User Request | Route |
|-------------|-------|
| "Generate MicroSims for chapter 11" | **Chapter batch** → Step 1 |
| "Create a MicroSim for inscribed angles" | **Single sim** → Step 1B |
| "Build a timeline of Unix history" | **Single sim** → Step 1B |

---

## Step 1: Extract Specs from Chapter (Batch Route)

**MANDATORY for chapter-level generation.** Do NOT manually parse chapter markdown.

```bash
python3 $UTILS/extract-sim-specs.py \
    --project-dir $PROJECT \
    --chapter <chapter-dir-name> \
    --output /tmp/ch-specs.json \
    --status-file /tmp/sim-status.json \
    --verbose
```

**What this does:**

- Parses all `#### Diagram:` and `#### Drawing:` headers from the chapter's `index.md`
- Extracts `<details>` block content, iframe paths, sim IDs, Bloom levels, and library hints
- Produces a JSON array of spec objects (one per sim)
- Generates a `sim-status.json` with lifecycle states: `specified → scaffolded → implemented → validated → deployed`

**Read the output:**

```bash
cat /tmp/ch-specs.json | python3 -m json.tool | head -60
```

Check the status file to see which sims need work:

```bash
python3 -c "
import json
with open('/tmp/sim-status.json') as f:
    for e in json.load(f):
        if e['status'] != 'deployed':
            print(f\"  {e['status']:12s}  {e['sim_id']}\")
"
```

After extracting, proceed to **Step 2**.

---

## Step 1B: Single-Sim Shortcut

For a single MicroSim request (not a full chapter batch):

1. **Write a 1-entry spec JSON** manually:

```bash
cat > /tmp/ch-specs.json << 'EOF'
[{
    "sim_id": "inscribed-angle-theorem",
    "title": "Central vs Inscribed Angles Interactive",
    "summary": "Demonstrates the inscribed angle theorem",
    "heading_type": "Diagram",
    "chapter": "",
    "element_type": "microsim",
    "bloom_level": "Analyze",
    "library": "p5.js",
    "iframe_src": "",
    "iframe_height": "",
    "spec_text": "",
    "status": ""
}]
EOF
```

2. **Run scaffold** for just that sim:

```bash
python3 $UTILS/generate-sim-scaffold.py \
    --spec-file /tmp/ch-specs.json \
    --sim-id inscribed-angle-theorem \
    --project-dir $PROJECT \
    --verbose
```

3. **Jump to Step 3** (Instructional Design Checkpoint), then **Step 4** (Implement .js).

---

## Step 2: Scaffold Sim Directories

**MANDATORY for batch generation.** Do NOT manually create main.html, index.md, or metadata.json.

```bash
python3 $UTILS/generate-sim-scaffold.py \
    --spec-file /tmp/ch-specs.json \
    --project-dir $PROJECT \
    --verbose
```

**What this does:**

- Creates `docs/sims/<sim-id>/` directory for each spec
- Generates `main.html` with correct CDN links, `<main>` tag, and schema meta tag
- Generates `index.md` with frontmatter, iframe embed, fullscreen link, lesson plan skeleton
- Generates `metadata.json` with Dublin Core fields and educational metadata
- **Skips** directories that already exist (unless `--force` is used)

**Using `--force` for partially-built sims:**

When sim directories exist (with main.html + .js) but lack index.md or metadata.json, the scaffold script skips the entire directory by default. Use `--force` to regenerate all scaffold files. This is safe because the creative work lives in the `.js` file, which the scaffold never overwrites.

```bash
python3 $UTILS/generate-sim-scaffold.py \
    --spec-file /tmp/ch-specs.json \
    --project-dir $PROJECT \
    --force \
    --verbose
```

**After scaffolding, the agent ONLY writes .js files from here on.**

---

## Step 3: Instructional Design Checkpoint (MANDATORY)

**Before writing any .js file, you MUST complete this checkpoint.**

### 3.1 Identify Learning Objective Details

Extract from the specification:
- **Bloom Level**: Remember, Understand, Apply, Analyze, Evaluate, or Create
- **Bloom Verb**: The action verb (explain, demonstrate, calculate, etc.)
- **Learning Objective**: The full statement of what learners will be able to do

### 3.2 Match Interaction Pattern to Bloom Level

| Bloom Level | Appropriate Patterns | Inappropriate Patterns |
|-------------|---------------------|------------------------|
| Remember (L1) | Flashcards, matching, labeling | Complex simulations |
| **Understand (L2)** | **Step-through worked examples, concrete data visibility** | **Continuous animation, particle effects** |
| Apply (L3) | Parameter sliders, calculators, practice problems | Passive viewing only |
| Analyze (L4) | Network explorers, comparison tools, pattern finders | Pre-computed results |
| Evaluate (L5) | Sorting/ranking activities, rubric tools | No feedback mechanisms |
| Create (L6) | Builders, editors, canvas tools | Rigid templates |

### 3.3 Answer These Questions

Before proceeding, answer these questions:

1. **What specific data must the learner SEE?**
   - Not "animated particles" but "the tokenized array ['physics', 'ball']"

2. **Does the learner need to PREDICT before observing?**
   - If YES → Use step-through with Next/Previous buttons
   - If YES → Do NOT use continuous animation

3. **What does animation add that static arrows don't?**
   - If you can't answer this clearly → Don't use animation

4. **Is continuous animation appropriate for this Bloom level?**
   - For Understand (L2) with verb "explain" → Almost always NO
   - For Apply (L3) with real-time feedback → Often YES

### 3.4 Modify Specification If Needed

If the specification requests animation/effects for an UNDERSTAND level objective:
- **Flag this as a potential instructional design issue**
- **Recommend step-through pattern instead**
- **Ask user**: "The specification requests animation, but for an 'explain' objective, a step-through approach with concrete data visibility typically supports learning better. Should I proceed with step-through instead?"

### 3.5 Document Your Decision

Add to your response:
```
Instructional Design Check:
- Bloom Level: [level]
- Bloom Verb: [verb]
- Recommended Pattern: [pattern]
- Specification Alignment: [aligned/modified]
- Rationale: [why this pattern supports the learning objective]
```

---

## Step 4: Implement .js Files

This is where the agent's creative work happens. For each sim that needs implementation:

### 4.1 Analyze Request and Match Generator

Scan the spec for trigger keywords and match to the appropriate generator guide.

#### Quick Reference Routing Table

| Trigger Keywords | Guide File | Library |
|------------------|------------|---------|
| timeline, dates, chronological, events, history, schedule, milestones | `references/timeline-guide.md` | vis-timeline |
| map, geographic, coordinates, latitude, longitude, locations, markers | `references/map-guide.md` | Leaflet.js |
| function, f(x), equation, plot, calculus, sine, cosine, polynomial | `references/plotly-guide.md` | Plotly.js |
| network, nodes, edges, graph, dependencies, concept map, knowledge graph | `references/vis-network-guide.md` | vis-network |
| flowchart, workflow, process, state machine, UML, sequence diagram | `references/mermaid-guide.md` | Mermaid.js |
| venn, sets, overlap, intersection, union, categories | `references/venn-guide.md` | Custom |
| chart, bar, line, pie, doughnut, radar, statistics, data | `references/chartjs-guide.md` | Chart.js |
| bubble, priority, matrix, quadrant, impact vs effort, risk vs value | `references/bubble-guide.md` | Chart.js |
| causal, feedback, loop, systems thinking, reinforcing, balancing, CLD, systems archetype | `references/causal-loop-guide.md` | vis-network |
| comparison, table, ratings, stars, side-by-side, features | `references/comparison-table-guide.md` | Custom |
| matrix, framework comparison, clickable cells, detail panel, expandable | `references/html-table.md` | Custom |
| animation, celebration, particles, confetti, effects | `references/celebration-guide.md` | p5.js |
| classify, classifier, categorize, sort scenarios, identify types, recognize patterns | `references/concept-classifier-guide.md` | p5.js |
| diagram overlay, callout labels, anatomy, labeled illustration, infographic overlay, explore/quiz modes | `references/infographic-overlay-guide.md` | Custom (diagram.js) |
| python lab, code runner, runnable code block, interactive python exercise, docker | `references/docker-python-lab-guide.md` | Custom (docker-lab.js) |
| verified infographic, statistics poster, fact-checked poster, cited data, sourced claims, evidence-based comparison | `references/verified-infographic-guide.md` | Custom (text-verify → image) |
| custom, simulation, physics, interactive, bouncing, movement, p5.js | `references/p5-guide.md` | p5.js |

#### Decision Tree

```
Static poster whose numeric claims must be verified against sources?
  → YES: verified-infographic-guide.md  (EXIT ROUTE — see below, this is not a sim)

Has dates/timeline/chronological events?
  → YES: timeline-guide.md

Has geographic coordinates/locations?
  → YES: map-guide.md

Mathematical function f(x) or equation?
  → YES: plotly-guide.md

Nodes and edges/network relationships?
  → YES: vis-network-guide.md (or causal-loop-guide.md if systems thinking)

Flowchart/workflow/process diagram?
  → YES: mermaid-guide.md

Sets with overlaps (2-4 categories)?
  → YES: venn-guide.md

Priority matrix/2x2 quadrant/multi-dimensional?
  → YES: bubble-guide.md

Standard chart (bar/line/pie/radar)?
  → YES: chartjs-guide.md

Comparison table with ratings/stars?
  → YES: comparison-table-guide.md

Matrix comparison with clickable cells/detail panels?
  → YES: html-table.md

Celebration/particles/visual feedback?
  → YES: celebration-guide.md

Students classify scenarios into categories (sorting quiz)?
  → YES: concept-classifier-guide.md

Labeled illustration with interactive callout markers or hover zones?
  → YES: infographic-overlay-guide.md

Runnable Python code block executed in Docker?
  → YES: docker-python-lab-guide.md

Custom simulation/animation/physics?
  → YES: p5-guide.md
```

#### Exit Route: Fact-Verified Poster (not a MicroSim)

`references/verified-infographic-guide.md` is the one route in this skill that does **not** produce a
sim directory. It produces a static poster PNG in `docs/posters/<slug>/` alongside its verification
report and source sidecar. When a request matches it:

- **Skip Steps 0–9 of this file entirely.** No scaffold, no `.js`, no `CANVAS_HEIGHT`, no iframe
  insertion, no quality validator, no `docs/sims/` entry.
- Read the guide and follow **its** 8-phase workflow instead. Phases 1–6 are text-only work by the
  agent; Phase 7 is the single image-model call; Phase 8 audits the render.
- The hard rule that makes this route worth having: **no claim reaches the image until it has a
  verified source.** An unverified claim blocks the pipeline, gets downgraded to qualitative
  language, or is dropped — it is never rendered on a guess.

**Reusing the verification phases for a real MicroSim.** Phases 1–4 (claim plan → source discovery →
per-claim verification → verification report) are output-format agnostic. When a *sim* must carry
sourced facts — a comparison table of real products, a chart of published measurements, a timeline of
dated events — run Phases 1–4 first, then hand the locked claim set to the matched sim guide and carry
each `source_id` into the sim's data file so the citation is visible to the student. Skip Phases 5–8;
those are poster-rendering steps.

### 4.2 Load the Matched Guide

**Read the corresponding guide file** from the `references/` directory and follow its workflow for writing the `.js` file.

### 4.3 Write ONLY the .js File

The scaffold (Step 2) already created `main.html`, `index.md`, and `metadata.json`. You only need to write `docs/sims/<sim-id>/<sim-id>.js`.

Each guide contains:
1. Library-specific requirements
2. Code templates and patterns
3. Best practices for that visualization type

### 4.4 MANDATORY: Add CANVAS_HEIGHT Comment to .js File

**Every .js file MUST include a `// CANVAS_HEIGHT:` comment on its own line near the top of the file (within the first 10 lines).** This is the primary source of truth for iframe height across all library types. The `sync-iframe-heights.py` utility and manual height-fixing rely on it.

> **No-`.js` sims:** if a sim is rendered entirely by `main.html` and ships **no `<id>.js`** (some projects author Mermaid, vis-network, or custom-HTML sims this way), there is no `.js` to hold the comment. Store the height in the sim's `metadata.json` instead, as `"canvasHeight": <integer>` — the consistent structured fallback that downstream tooling reads next after the `.js` comment. See the microsim-utils skill's `references/canvas-height-strategy.md` for the full resolution order. Everything else in this step (how to *calculate* the number, the `+2` iframe rule) is identical.

Format: `// CANVAS_HEIGHT: <integer>`

The value is the **total pixel height** the iframe needs to display the entire MicroSim without clipping — canvas, controls, legends, info panels, titles, and any padding.

#### How to Calculate CANVAS_HEIGHT by Library Type

| Library | Formula | Example |
|---------|---------|---------|
| **p5.js** | `drawHeight + controlHeight + graphHeight` (the `canvasHeight` variable) | `// CANVAS_HEIGHT: 695` |
| **vis-network** | container height + title (~35px) + info panel (~60px) + legend (~30px) + controls (~40px) | `// CANVAS_HEIGHT: 685` |
| **Chart.js** | chart container height + title (~35px) + controls (~40px) + legend (~30px) | `// CANVAS_HEIGHT: 505` |
| **Plotly.js** | plot div height + title (~35px) + controls (~40px) | `// CANVAS_HEIGHT: 475` |
| **vis-timeline** | timeline container height + title (~35px) + controls (~40px) | `// CANVAS_HEIGHT: 475` |
| **Leaflet.js** | map container height + title (~35px) + controls (~40px) + legend (~40px) | `// CANVAS_HEIGHT: 515` |
| **Mermaid.js** | diagram container height + title (~35px) + controls (~40px) | `// CANVAS_HEIGHT: 475` |
| **Custom HTML** (comparison table, html-table, venn) | total rendered height of all DOM elements | `// CANVAS_HEIGHT: 600` |
| **Interactive Infographic Overlay** | image container height + toolbar (~40px) + info panel (~60px) | `// CANVAS_HEIGHT: 620` |

#### Examples for Each Library Type

**p5.js:**
```javascript
// Predator-Prey Population Dynamics Simulator
// CANVAS_HEIGHT: 695
let drawHeight = 400;
let graphHeight = 180;
let controlHeight = 115;
let canvasHeight = drawHeight + graphHeight + controlHeight;
```

**vis-network:**
```javascript
// Climate Feedback Loops - vis-network
// CANVAS_HEIGHT: 685
document.addEventListener('DOMContentLoaded', function() {
```

**Chart.js:**
```javascript
// Air Quality Trends Dashboard - Chart.js
// CANVAS_HEIGHT: 505
document.addEventListener('DOMContentLoaded', function () {
```

**Leaflet.js:**
```javascript
// Watershed Map - Leaflet
// CANVAS_HEIGHT: 515
document.addEventListener('DOMContentLoaded', function() {
```

**Interactive Infographic Overlay:**
```javascript
// Ecosystem Components Overlay
// CANVAS_HEIGHT: 620
document.addEventListener('DOMContentLoaded', function() {
```

#### Rules

1. **The comment MUST appear within the first 10 lines** of the .js file so parsing tools can find it quickly.
2. **The value MUST be an integer** (no `px` suffix, no expressions).
3. **The iframe height = CANVAS_HEIGHT + 2** (2px accounts for the iframe border). The `sync-iframe-heights.py` utility adds this automatically.
4. **For p5.js sims**, the CANVAS_HEIGHT value must equal `drawHeight + controlHeight` (plus `graphHeight` if present). Keep the existing named variables — the comment is a redundant-but-authoritative declaration for tooling.
5. **When updating an existing sim**, always update the CANVAS_HEIGHT comment if you change any height-related values.
6. **If unsure about the height**, render the sim in a browser, measure the total content height, and use that value. Err on the side of being slightly too tall (extra whitespace is better than clipped controls).

### 4.5 Handling Ambiguous Requests

If the request could match multiple generators:

1. **Read `references/routing-criteria.md`** for detailed scoring methodology
2. **Score top 3 candidates** using the 0-100 scale
3. **Present options to user** with reasoning:
   ```
   Based on your request, I recommend:
   1. [Generator A] (Score: 85) - Best for [reason]
   2. [Generator B] (Score: 70) - Alternative if you need [feature]
   3. [Generator C] (Score: 55) - Possible if [condition]

   Which would you prefer?
   ```
4. **Proceed with user's selection**

#### Common Ambiguities

| Ambiguous Term | Clarification Needed |
|----------------|---------------------|
| "graph" | Chart (ChartJS) or Network graph (vis-network)? |
| "diagram" | Structural (Mermaid), Network (vis-network), or Custom (p5)? |
| "map" | Geographic (Leaflet) or Concept map (vis-network)? |
| "table" | Star ratings (comparison-table) or Clickable cells with detail panels (html-table)? |
| "visualization" | What type of data? What interaction needed? |

---

## Step 5: Fix Chapter Iframes

**MANDATORY for batch generation.** Do NOT manually insert or edit iframes in chapter markdown.

```bash
python3 $UTILS/add-iframes-to-chapter.py \
    --chapter <chapter-dir-name> \
    --project-dir $PROJECT \
    --fix-heights \
    --fix-paths \
    --verbose
```

**What this does:**

- Finds `#### Diagram:` / `#### Drawing:` headers that are missing iframe embeds
- Inserts `<iframe>` tags before the `<details>` block with correct relative paths
- `--fix-heights`: Parses `.js` files to detect `createCanvas()` height and sets iframe height to canvas height + 2px
- `--fix-paths`: Converts absolute paths (`/sims/...`) to relative (`../../sims/...`)
- Fixes height typos (`500xp` → `500px`)

**For all chapters at once:**

```bash
python3 $UTILS/add-iframes-to-chapter.py \
    --all \
    --project-dir $PROJECT \
    --fix-heights \
    --fix-paths \
    --verbose
```

**Dry-run first** to preview changes:

```bash
python3 $UTILS/add-iframes-to-chapter.py \
    --chapter <chapter-dir-name> \
    --project-dir $PROJECT \
    --fix-heights --fix-paths \
    --dry-run --verbose
```

---

## Step 6: Validate Quality

**MANDATORY after implementing .js files.** Do NOT rely on a manual checklist.

```bash
python3 $UTILS/validate-sims.py \
    --project-dir $PROJECT \
    --format table \
    --verbose
```

**What this does:**

Scores each MicroSim on a 100-point rubric:

| Category | Points | Checks |
|----------|--------|--------|
| main.html | 10 | Exists (5), schema meta tag (3), `<main>` tag (2) |
| metadata.json | 30 | Present (10), required fields (10), educational (5), pedagogical (5) |
| index.md | 35 | Title (2), YAML (3), images (5), iframe (10), fullscreen (5), example (5), description (5) |
| Screenshot | 5 | PNG file exists |
| Lesson Plan | 10 | Section present in index.md |
| References | 5 | Section present in index.md |
| p5.js conventions | 5 | updateCanvasSize, no DOM buttons, querySelector parenting, no textFont('Segoe UI') |

**Grade scale:** A (85+), B (70-84), C (50-69), D (<50)

**Validate a single sim:**

```bash
python3 $UTILS/validate-sims.py \
    --project-dir $PROJECT \
    --sim <sim-id> \
    --verbose
```

**Fix issues found, then re-validate** to confirm improvements:

```bash
# After fixing issues...
python3 $UTILS/validate-sims.py \
    --project-dir $PROJECT \
    --min-score 0 \
    --format table \
    --verbose
```

---

## Step 6B: Sync Iframe Heights

**MANDATORY after implementing .js files.** Do NOT manually calculate iframe heights.

```bash
python3 $UTILS/sync-iframe-heights.py \
    --project-dir $PROJECT \
    --verbose
```

**What this does:**

- Parses each sim's `.js` file to find the `// CANVAS_HEIGHT: <value>` comment (primary source, see Step 4.4)
- Falls back, in order, to `"canvasHeight"` in `metadata.json` (the place for sims with no `.js`), a `<!-- CANVAS_HEIGHT: -->` comment in `main.html`, then computed `drawHeight + controlHeight` from the `.js`
- Sets the iframe height to `CANVAS_HEIGHT + 2` (2px for border)
- Updates the `<iframe>` height attribute in each sim's `index.md` **and** in every page under `docs/` that embeds the sim — chapters, teacher guides, poster pages
- Skips sims that are already correct

**Use `sync-iframe-heights.py`, not `fix-iframe-heights.py`.** The latter is an own-page-only predecessor: it updates the sim's own `index.md` but silently leaves the chapter embeds inserted by Step 5 at their stale heights, so the sim looks right on its own page and clipped in the chapter.

**Important:** The `// CANVAS_HEIGHT:` comment in the .js file is the single source of truth for ALL library types (p5.js, vis-network, Chart.js, Leaflet, Mermaid, etc.). If the comment is missing, add it to the .js file before running this tool — see Step 4.4 for format and calculation rules.

**Fix a single sim:**

```bash
python3 $UTILS/sync-iframe-heights.py \
    --project-dir $PROJECT \
    --sim <sim-id> \
    --verbose
```

**Dry-run first** to preview changes:

```bash
python3 $UTILS/sync-iframe-heights.py \
    --project-dir $PROJECT \
    --dry-run --verbose
```

---

## Step 6C: Verify Controls Visible in Iframe (Playwright)

**MANDATORY after fixing iframe heights.** This catches controls that extend beyond the iframe boundary — something static height calculation can miss, especially for sims with responsive layouts or narrow viewports.

```bash
TESTER="$HOME/.claude/skills/microsim-utils/scripts"

# Single sim (after generating one MicroSim)
python3 $TESTER/test-iframe-heights.py --sims-dir $PROJECT/docs/sims --sim <sim-id>

# All sims in a batch run
python3 $TESTER/test-iframe-heights.py --sims-dir $PROJECT/docs/sims
```

**What this does:**

- Launches headless Chromium via Playwright
- Loads each MicroSim's `main.html` in a viewport constrained to the iframe height from `index.md`
- Waits for libraries (p5.js, vis-network, Chart.js) to render
- Checks that all interactive controls (buttons, sliders, selects, checkboxes) are fully visible
- Reports PASS/FAIL with a suggested height for any failures

**Prerequisites** (one-time setup):

```bash
pip install playwright
playwright install chromium
```

**If a sim fails:**

1. Update the `// CANVAS_HEIGHT:` comment in the `.js` file to the suggested height minus 10
2. Re-run `sync-iframe-heights.py` for that sim
3. Re-run the Playwright test to confirm it passes

---

## Step 7: Update Navigation

**MANDATORY after creating new sims.** Do NOT manually edit the MicroSims section of mkdocs.yml.

```bash
python3 $UTILS/update-mkdocs-nav.py \
    --project-dir $PROJECT \
    --verbose
```

**What this does:**

- Scans `docs/sims/` for directories containing `index.md`
- Extracts display titles from frontmatter or `# Heading`
- Replaces the entire `- MicroSims:` section in `mkdocs.yml` with an alphabetically sorted list
- Idempotent and safe to run multiple times

**Dry-run first:**

```bash
python3 $UTILS/update-mkdocs-nav.py \
    --project-dir $PROJECT \
    --dry-run --verbose
```

---

## Step 8: Generate a Screen Image of the MicroSim

A screen image of the microsim is needed for the /doc/sims/index.md file which
provides a list of all the MicroSims in the textbook.

A unix shell script is use to get a screen image of the MicroSim.  This
shell script runs Google Chrome headless and creates a 800px wide image
where the height of the screen image is determined by the iframe height.

The screen capture shell scrip is installed in ~/.local/bin/bk-capture-screenshot
as a symbolic link to the $BK_HOME/scripts/bk-capture-screenshot program

bk-capture-screenshot has 3 command line parameters:

$1  MicroSim directory path (default: current directory)
$2  Delay in seconds for JS rendering (default: 3)
$3  Target image height in pixels (default: 600)

Tip: use the iframe height from the MicroSim's index.md file to get the correct height.

Sample Usage:

```sh
bk-capture-screenshot /path/to/microsim 3 700    # 3 second delay, 700px height
```

Output:

Creates <microsim-name>.png in the MicroSim directory that is typically around 50K bytes.

---

## Step 9: Visual Layout Review (MANDATORY)

**MANDATORY after capturing the screenshot.** This is the visual QA
counterpart to the iframe-tester utility (which uses Playwright
bounding-box checks). Layout review catches the defects that geometry
checks miss: clipped row labels, controls overlapping, text rendered
with residual strokes, panel content overflow, low-contrast labels,
draw-order bugs, and library-specific rendering issues.

The screenshot from Step 8 is the input — do not re-capture.

Use the **layout-reviewer** utility in `microsim-utils` on each
newly-generated sim:

```
For each sim that was generated in this batch:
  1. Read references/visual-checklist.md from microsim-utils
  2. Read the sim's screenshot PNG (Read tool — Claude Vision sees it)
  3. Walk every checklist item; mark PASS / FAIL / N/A with quoted
     evidence for any FAIL
  4. For each FAIL, consult references/common-fixes.md and apply the
     smallest patch that resolves it (typically a small edit to the
     .js for p5.js / Chart.js / vis-network / Leaflet sims, or to
     main.html for Mermaid sims)
  5. Re-capture, re-read, re-walk the checklist
  6. Stop after 3 review-patch cycles even if issues remain — surface
     residue rather than over-tweak
```

The utility documents its full workflow at
`~/.claude/skills/microsim-utils/references/layout-reviewer.md`. From this
generator's standpoint, the contract is: "after Step 8, every sim
must have passed layout review or had its remaining defects
explicitly reported."

**What layout review does NOT do:**

- Does not fix iframe-height clipping (content extending past the
  iframe edge) — that's `sync-iframe-heights.py` and the iframe-tester
  utility (`microsim-utils`) from Step 6B / 6C.
- Does not modify approved sims (frontmatter `status: approved`).
  In this generator's flow that's irrelevant — newly-generated sims
  are not yet approved — but the rule still applies.

**Why this is mandatory in the generator:** the value of catching
layout defects at generation time, before the user sees the sim, is
much higher than catching them later. Visual review at the end of
Step 8 means "looks right when embedded" is part of the definition
of done for every new MicroSim, not a separate manual QA pass.

---

## Workflow Summary

### Batch (Chapter-Level) Generation

```
Step 0: Set UTILS and PROJECT paths
  ↓
Step 1: extract-sim-specs.py → /tmp/ch-specs.json
  ↓
Step 2: generate-sim-scaffold.py → creates main.html, index.md, metadata.json
  ↓
Step 3: Instructional Design Checkpoint (per sim)
  ↓
Step 4: Write .js files (creative work — route to guide, implement)
  ↓
Step 5: add-iframes-to-chapter.py → inserts/fixes iframes
  ↓
Step 6: validate-sims.py → scores quality, fix issues
  ↓
Step 6B: sync-iframe-heights.py → syncs iframe heights (own page + chapter embeds)
  ↓
Step 6C: test-iframe-heights.py → Playwright verifies controls visible in iframe
  ↓
Step 7: update-mkdocs-nav.py → regenerates nav
  ↓
Step 8: bk-capture-screenshot /path/to/microsim 3 {height} → creates screen image
  ↓
Step 9: microsim-utils layout-reviewer → Claude Vision walks the checklist,
        diagnoses + patches FAILs, re-captures to verify (max 3 cycles)
```

### Single Sim Generation

```
Step 0:  Set UTILS and PROJECT paths
  ↓
Step 1B: Write 1-entry spec JSON + scaffold
  ↓
Step 3:  Instructional Design Checkpoint
  ↓
Step 4:  Write .js file
  ↓
Step 6:  validate-sims.py --sim <name>
  ↓
Step 6B: sync-iframe-heights.py --sim <name>
  ↓
Step 6C: test-iframe-heights.py --sim <name> → Playwright verifies controls visible
  ↓
Step 7:  update-mkdocs-nav.py
  ↓
Step 8:  bk-capture-screenshot /path/to/microsim 3 {height} → creates screen image
  ↓
Step 9:  microsim-utils layout-reviewer → Claude Vision walks the checklist,
         diagnoses + patches FAILs, re-captures to verify (max 3 cycles)
```

### Resuming After Context Window Fills

When a batch run fills the context window mid-chapter:

1. The new session reads `sim-status.json` to see what's done
2. Sims in `implemented` or later status are skipped
3. Sims in `specified` or `scaffolded` status still need .js files

```bash
# Check where we left off
python3 $UTILS/extract-sim-specs.py \
    --project-dir $PROJECT \
    --chapter <chapter-dir-name> \
    --status-file /tmp/sim-status.json \
    --verbose
```

---

## Available Generators

### Primary Generators

| Generator | Library | Best For |
|-----------|---------|----------|
| p5-guide | p5.js | Custom simulations, physics, animations |
| chartjs-guide | Chart.js | Bar, line, pie, doughnut, radar charts |
| timeline-guide | vis-timeline | Chronological events, history, schedules |
| map-guide | Leaflet.js | Geographic data, locations, routes |
| vis-network-guide | vis-network | Network graphs, dependencies, concept maps |
| mermaid-guide | Mermaid.js | Flowcharts, workflows, UML diagrams |
| plotly-guide | Plotly.js | Mathematical function plots |
| venn-guide | Custom | Set relationships (2-4 sets) |
| bubble-guide | Chart.js | Priority matrices, multi-dimensional data |
| causal-loop-guide | vis-network | Systems thinking, feedback loops, multi-loop CLD articles |
| comparison-table-guide | Custom | Side-by-side comparisons with ratings |
| html-table | Custom | Matrix comparisons with clickable cells, detail panels |
| celebration-guide | p5.js | Particle effects, visual feedback |
| concept-classifier-guide | p5.js | Classification quizzes — sort scenarios into categories |
| infographic-overlay-guide | Custom (diagram.js) | Interactive callout/zone overlays on illustrations |
| docker-python-lab-guide | Custom (docker-lab.js) | Runnable Python labs in Docker containers |
| verified-infographic-guide | Custom (text-verify → image) | Fact-verified statistics posters — claim plan, source verification, locked image prompt (**static poster, not a sim**) |

### Shared Standards

All MicroSims follow these standards regardless of generator:

**Directory Structure:**
```
docs/sims/<microsim-name>/
├── main.html       # Main visualization file
├── index.md        # Documentation page
├── *.js or *.css   # Supporting files
└── metadata.json   # Dublin Core metadata (optional)
```

**URI Scheme for Discoverability:**

All MicroSim HTML files MUST include this schema meta tag for global discoverability:

```html
<meta name="schema" content="https://dmccreary.github.io/intelligent-textbooks/ns/microsim/v1">
```

This enables counting and discovery of MicroSims across GitHub using code search. See the [URI Scheme documentation](https://dmccreary.github.io/intelligent-textbooks/uri-scheme/) for details.

**Integration:**
- Embedded via iframe in MkDocs pages
- Width-responsive design
- Non-scrolling iframe container
- Standard height: `CANVAS_HEIGHT + 2px` (where CANVAS_HEIGHT is declared in a `// CANVAS_HEIGHT: <value>` comment at the top of the .js file — see Step 4.4)
- Prevent scroll hijacking:
  - Keep chapter iframes non-scrolling: `scrolling="no"`
  - Do not consume page wheel-scroll by default inside sims (for example, set Leaflet `scrollWheelZoom: false` unless explicitly requested)
- **Iframe paths MUST always be relative, NEVER absolute:**
  - From a sim's own `index.md`: `<iframe src="main.html" ...>`
  - From chapter files (`docs/chapters/*/index.md`): `<iframe src="../../sims/[sim-name]/main.html" ...>`
  - **NEVER use absolute paths** like `/sims/...` — they break on GitHub Pages where the site is served under a subdirectory (e.g., `/geometry-course/`)

**Quality Checklist:**
- [ ] Runs without errors in modern browsers
- [ ] Responsive to container width
- [ ] Controls respond immediately
- [ ] Does not hijack page scrolling when embedded in an iframe
- [ ] Educational purpose is clear
- [ ] Code is well-commented
- [ ] Does not call `textFont()` unless a specific font is explicitly required by the design — never use `textFont('Segoe UI')`, which is a Windows-only font unavailable on macOS/Linux

## Examples

### Example 1: Timeline Request
**User:** "Create a timeline showing key events in computer history"
**Routing:** Keywords "timeline", "events", "history" → `references/timeline-guide.md`
**Action:** Read timeline-guide.md and follow its workflow

### Example 2: Chart Request
**User:** "Make a bar chart comparing programming language popularity"
**Routing:** Keywords "bar chart", "comparing" → `references/chartjs-guide.md`
**Action:** Read chartjs-guide.md and follow its workflow

### Example 3: Custom Simulation
**User:** "Build an interactive bouncing ball simulation"
**Routing:** Keywords "interactive", "bouncing", "simulation" → `references/p5-guide.md`
**Action:** Read p5-guide.md and follow its workflow

### Example 4: Ambiguous Request
**User:** "Create a graph of our project dependencies"
**Routing:** "graph" + "dependencies" suggests network → `references/vis-network-guide.md`
**Action:** Read vis-network-guide.md (but clarify if user meant a chart)

### Example 5: Chapter Batch
**User:** "Generate MicroSims for chapter 11"
**Action:** Step 0 → Step 1 → Step 2 → Step 3-4 (loop per sim) → Step 5 → Step 6 → Step 6B → Step 6C → Step 7

### Example 6: Classification Quiz
**User:** "Create a quiz where students identify which cognitive bias each scenario shows"
**Routing:** Keywords "identify", "classify scenarios" → `references/concept-classifier-guide.md`
**Action:** Read concept-classifier-guide.md and follow its workflow

### Example 7: Causal Loop Article
**User:** "Show the feedback loops in supply chain bullwhip"
**Routing:** Keywords "feedback loops" → `references/causal-loop-guide.md`
**Action:** Read causal-loop-guide.md; full article if requested, single inline CLD otherwise

### Example 8: Labeled Diagram Overlay
**User:** "Make an interactive anatomy diagram of a moss sporophyte with labeled structures"
**Routing:** Keywords "anatomy", "labeled" → `references/infographic-overlay-guide.md`
**Action:** Read infographic-overlay-guide.md and follow the callout workflow

### Example 9: Python Lab
**User:** "Add a runnable Python lab about list operations to this page"
**Routing:** Keywords "runnable", "Python lab" → `references/docker-python-lab-guide.md`
**Action:** Read docker-python-lab-guide.md and follow its workflow

### Example 10: Fact-Verified Poster
**User:** "Make a poster comparing the energy use of LED vs. incandescent lighting with real numbers"
**Routing:** "poster" + numeric claims needing sources → `references/verified-infographic-guide.md`
**Action:** Exit route — skip Steps 0–9; run the guide's 8 phases; verify every number before the one image call

### Example 11: Sourced Comparison Sim
**User:** "Build a comparison table of these five breadboard power supplies using verified specs"
**Routing:** "comparison table" → `references/comparison-table-guide.md`, but the specs must be sourced
**Action:** Run Phases 1–4 of verified-infographic-guide.md to lock and cite the claims, then build the
sim with comparison-table-guide.md, carrying each `source_id` into the table so citations stay visible

## Reference Files

For detailed information, consult:

- `references/routing-criteria.md` - Complete scoring methodology for all generators
- `references/<generator>-guide.md` - Specific implementation guide for each generator
- `assets/templates/` - Shared templates and patterns
- `references/infographic-claim-plan-template.yaml`, `references/infographic-verification-report-template.md`,
  `references/infographic-layout-spec-template.yaml`, `references/poster-image-prompt.md`,
  `references/infographic-biophilic-case-study.md` - verified-infographic route
- `scripts/posters/generate-poster-thumbnails.py` - poster gallery thumbnails (see verified-infographic-guide.md, "Gallery Thumbnails")

## sim-status.json Lifecycle

The `extract-sim-specs.py --status-file` flag generates a lifecycle tracking file. States progress as:

| Status | Meaning |
|--------|---------|
| **specified** | Has spec in chapter but no sim directory yet |
| **scaffolded** | Directory with main.html/index.md but no substantive JS |
| **implemented** | JS file exists and >50 lines |
| **validated** | quality_score >= 70 |
| **deployed** | Validated + iframe present in chapter |

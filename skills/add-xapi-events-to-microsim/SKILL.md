---
name: add-xapi-events-to-microsim
description: Use when the user wants an existing MicroSim or chapter quiz to record what students do with it. Typical requests are "add xAPI events", "add tracking or analytics", "make this sim feed the LRS or LRS-Lite", "instrument chapter 5's sims", or "what should this sim record?". Use it even if they never say "xAPI". Not for building a new MicroSim (use microsim-generator) or for LRS backend work.
metadata:
  ibook.version: "0.1"
  ibook.preferred-model: "opus"
---

# Add xAPI Events to a MicroSim

**Version:** 0.1 (Phase 1 draft, 2026-09-26)

## What this skill does

This skill takes a MicroSim that already works and makes it report what the student did,
as xAPI statements, **without changing what the sim does**. The per-sim code is a thin
mapping, usually 20 to 60 lines, onto a shared runtime. It is never a copy of the runtime.

The runtime decides Full vs. Compact from config and builds every statement. It also
enforces the producer contract and renders the teaching panel. Your job is to decide
**which interactions are evidence, of what, and for which concept**, and then wire them up.

The canonical runtime and the four reference sims live in the `learning-record-store`
repo. Read them whenever this skill points at one; they are the ground truth.

```
LRS_REPO=~/Documents/ws/learning-record-store
$LRS_REPO/docs/js/lrs-sim.js           the API a sim calls (its header comment is the contract)
$LRS_REPO/docs/js/lrs-config.js        per-book identity + default policy (example)
$LRS_REPO/docs/sims/bouncing-ball/     p5, slider + Start/Pause            (verified)
$LRS_REPO/docs/sims/sine-wave/         p5, three sliders                   (verified)
$LRS_REPO/docs/sims/scientific-method/ Mermaid, hover + pin, page dwell    (verified)
$LRS_REPO/docs/sims/animal-cell/       image overlay, explore + quiz       (verified)
$LRS_REPO/docs/js/quiz-xapi.js         chapter quiz page, answers only     (verified)
$LRS_REPO/docs/specs/xapi-producer-contract-v1.md   the statement rules
```

Scripts are in this skill's `scripts/` directory (`SKILL_DIR` below). The Python scripts
need only the standard library, except the two that drive a browser. Run those with
`uv run --with playwright==1.58.0 python ...`.

## Principles, and why they matter

- **Instrument the act the sim was designed for.** Don't record every act you *can*
  detect. The sim's own instructions tell you which act was designed ("Click a node to
  see details", "Hover over a marker or a label"). Hover is absent on touch devices, so
  hover-only evidence is biased by device, and device correlates with school funding.
  Record hover only when it is the designed act, or when click is simply how a
  touchscreen does the same thing (then they are one act; see animal-cell).
- **Not every interaction is evidence.** Mouse crossings (<600 ms hover), mis-clicks
  (<250 ms runs), glances (<1 s page dwell), and events the program fires on itself
  (autosize, `setView`, `rangechange`) are noise. If you emit them, dashboards will
  believe them.
- **Answers are never folded.** A checked answer (a quiz item, a checked prediction, a
  goal reached) is its own `answered` statement in *both* modes, emitted as it happens.
  Only exposure evidence folds into the Compact summary. BKT reads the order of attempts.
- **Mode and teaching UI come from config, never from the sim.** The book's
  `docs/js/lrs-config.js` sets the default for every sim. A sim's `metadata.json` `xapi`
  block overrides it for that one sim. Production sims show nothing.
- **Never edit the runtime or a vendored library.** `docs/js/lrs-*.js` is identical in
  every book. A vendored file such as `shared-libs/diagram.js` is shared by many sims.
  Wrap functions and add listeners beside the originals instead. If the runtime truly
  lacks something, use `lrs.emit(spec)`, or stop and tell the user.
- **The sim must still run without the runtime.** Teachers paste p5 sketches into the
  p5.js editor. Guard every call site with `if (window.LRSSim)` or a null `lrs`.

## Workflow

Work through these steps in order. Steps 2–4 are the thinking. Show the user the
evidence table from step 3 before you write code whenever there is anything debatable,
for example two input paths to one act, a canvas hit-test, or no matching concept.

### Step 0 — Locate the book and the sim

The book root is the directory containing `mkdocs.yml`. The sim is
`docs/sims/<sim-name>/`, containing `main.html` (the iframe payload), `index.md` (the
lesson page that embeds it), and usually `metadata.json`. For a chapter quiz, the "sim"
is the rendered quiz page; go straight to `references/adapters/quiz-page.md`.

For a batch request ("instrument chapter 5's sims"), handle one sim at a time and keep
a running table of results. Finish and verify each sim before starting the next.

### Step 1 — Detect the library (from script tags, not the catalog)

```bash
python3 $SKILL_DIR/scripts/detect-library.py docs/sims/<sim-name>
```

The catalog's `library` field is empty for about 45% of sims, so trust the `<script>`
tags. The report also lists:

- whether the runtime is already loaded (if so, this is a revision, not a first pass),
- vendored shared files you must wrap rather than edit,
- a first-pass inventory of interaction hooks found in the JS.

Open the matching adapter and read it before going further:

| Library / shape | Adapter | Status |
|---|---|---|
| p5.js with `createSlider`/`createButton`/`createSelect`/… | `references/adapters/p5-dom-controls.md` | verified |
| p5.js with canvas `mousePressed`/`mouseDragged` hit-tests | `references/adapters/p5-canvas.md` | click/predict piloted; drags **unverified** |
| Mermaid flowchart (click-to-pin or hover infobox) | `references/adapters/mermaid-html.md` | verified (hover+pin); click-to-pin template piloted |
| Image with hotspot markers/labels (image-overlay, diagram.js) | `references/adapters/image-overlay.md` | verified |
| Chapter quiz page (`??? question` answers) | `references/adapters/quiz-page.md` | verified |
| vis-network | `references/adapters/vis-network.md` | **unverified** |
| vis-timeline | `references/adapters/vis-timeline.md` | **unverified** |
| Chart.js | `references/adapters/chartjs.md` | piloted |
| Plotly | `references/adapters/plotly.md` | **unverified** |
| Leaflet | `references/adapters/leaflet.md` | **unverified** |
| Plain HTML/SVG controls | `references/adapters/mermaid-html.md` (same DOM-listener pattern) | verified |

Many sims mix shapes, for example p5 DOM controls plus canvas-drawn buttons. Read every
adapter that applies. An **unverified** adapter was drafted from library docs and has
not passed a pilot yet. Follow it, but verify its claims against the real sim and tell
the user which parts you had to correct. A **piloted** adapter passed a pilot in an eval
run, and its corrections are folded in. It becomes **verified** once that pilot sim is
committed to its book.

### Step 2 — Inventory the interactions

Read the sim's JS and HTML completely; the detector's inventory is only a starting
point. List every way the student can change or inspect the sim: each control, each
clickable thing, each hover target, each mode switch, each check of an answer. Also
note the sim's own instruction text, because it names the designed act.

### Step 3 — Classify each interaction into an evidence class

Read `references/evidence-classes.md`. Every interaction becomes exactly one of:

| # | Class | Handle | Typical source |
|---|---|---|---|
| 1 | Continuous parameter | `lrs.slider(key, o).input(v)` / `.settle(v)` | slider, zoom, numeric input |
| 2 | Discrete inspection | `lrs.item(key, o).study(mode, ms)` | click, hover ≥ 600 ms, pin, select, legend toggle |
| 3 | Run/Pause | `lrs.button(key).press(action)` + `lrs.runner(o).start()/.stop(reason)` | Start/Pause, Play/Stop |
| 3a | Discrete press | `lrs.button(key, o).press(action)` | Reset, Randomize, scale toggle |
| 4 | Page dwell | `pageDwell: true` in `LRSSim.create` | any sim with no Run control |
| 5 | Assessment | `lrs.question(key, o).answer({success, response, …})` | quiz item, checked prediction, goal |
| 6 | Focus loss | handled by the runtime | tab hidden, scroll-away, idle, blur |
| — | Not evidence | nothing | sub-threshold hover, programmatic events, pure layout |

Write the result as a table for the user: interaction → class → fragment key →
concept. Name each fragment key for what the thing *is* (`#frequency-slider`,
`#start-pause-control`, `#q-kafka`), never for its position.

### Step 4 — Map each object to a concept id

Read `references/concept-mapping.md`. In short: the concept id is namespaced as
`{conceptPrefix}-{ConceptID}` from the book's `docs/learning-graph/learning-graph.csv`.
Each statement carries **one** concept. To propose candidates, run:

```bash
python3 $SKILL_DIR/scripts/find-concepts.py --book . --sim docs/sims/<sim-name>
python3 $SKILL_DIR/scripts/find-concepts.py --book . "prediction" "data loss"
```

The script only proposes; you choose. If nothing genuinely matches, **leave that object
unmapped and tell the user**. Don't guess the nearest label. A wrong concept id is
worse than none, because it silently credits mastery of the wrong thing. A mapping the
book itself states is not a guess. If the chapter or a sibling sim's spec pairs *Gateway*
with *Kafka Unavailable Failure*, use that pairing and cite it.

While mapping a question, check its **answer key against the chapter**. A key that
contradicts the text makes every student who learned the chapter score `success: false`.
Both chaos-kill eval runs found such a key. Report it; changing it is a content
decision for the user.

In code, write `LRS.conceptId(353)` so the prefix comes from the book's config. Record
the map, with full ids, in `metadata.json` (step 7).

### Step 5 — Confirm the runtime is installed in this book

```bash
python3 $SKILL_DIR/scripts/install-runtime.py --book . --check
```

If files are missing, run it without `--check`. It copies `lrs-xapi.js`,
`lrs-lite-sim.js`, `lrs-sim.js`, `xapi-json-viewer.js` and `lrs-xapi.css` from the
canonical repo. It writes `docs/js/lrs-config.js` from `mkdocs.yml` only if that file is
absent, because the config is the book's identity and is never overwritten. If the
script reports **drift** (the book's copy differs from canonical), stop and tell the
user; don't pass `--force` on your own. Phase 3 will move this job into
`book-installer`.

### Step 6 — Wire the adapter

1. **`main.html`:** add the script block from `assets/main-html-script-block.html`,
   in that order, *before* the sim's own script. Add the CSS link. For layouts where the
   panel should sit below the sim, add `<div id="xapi-slot"></div>` after `<main>`.
2. **The sim's JS:** create one `LRSSim` instance, then one handle per object from
   step 3, then call the handles from the sim's existing event handlers. Follow the
   adapter file for the library. See `references/runtime-api.md` for every option, with a
   worked example of each class.
3. Keep the sim's original behaviour byte-for-byte where you can: add listeners, wrap
   functions, and don't reorder the sim's own logic. For a sim whose main file is a
   vendored library, put the instrumentation in a separate `xapi.js` (animal-cell).
4. Clicks and mouse moves inside the xAPI panel must not reach the sim's own handlers,
   such as "click outside to unpin" or a follow-the-mouse infobox. Check for these.

Read `references/pitfalls.md` before you finish this step; every item on it was
learned by shipping the bug.

### Step 7 — Set the metadata.json `xapi` block

```json
"xapi": {
  "concept": "learning-record-store-353",
  "objects": {
    "service-select": "learning-record-store-353",
    "q-kafka": "learning-record-store-334",
    "q-neo4j": "learning-record-store-336"
  }
}
```

In this example, the page and its generic controls take the sim's concept (353, Chaos Kill
Test). Each question takes the concept it tests (334, Kafka Unavailable Failure).

- `concept` is the page-level concept (runs, page dwell, the Compact summary). `objects`
  maps every fragment key to its concept id. `check-xapi.py` verifies that the emitted
  statements match this map, so the map and the code can't drift apart silently. The
  map also gives the MicroSim catalog exact concept ids, which it lacks today.
- **Production sims** (the normal case) carry no policy keys, so they inherit the book's
  `lrs-config.js` default. If the book's default is ever `teaching: true`, add
  `"teaching": false` to keep this sim silent.
- **Teaching sims** (ones that exist to *teach* xAPI) add
  `"compact": false, "teaching": true`, so they start on Full and show the log.
- Policy keys and their meaning: `compact`, `teaching`, `idleMs`, `offscreenMs`,
  `blurMs`. The precedence, lowest first, is: runtime defaults < book `lrs-config.js`
  `xapi` < page `policy` option < this block.

### Step 8 — Re-measure the iframe height

```bash
uv run --with playwright==1.58.0 python $SKILL_DIR/scripts/measure-iframe.py docs/sims/<sim-name>
```

A teaching sim gains a panel, so its iframe must grow. The script measures a **full**
log at 375, 700 and 900 px and recommends a height. It measures the state after load. If
the sim is taller in another state (quiz mode, an open detail panel), put it there first
with `--eval "sim.setMode('quiz')"`. An empty-log screenshot is not a measurement.

The script also lists **every iframe in the book that embeds this sim**, not just the one
in `index.md`. Chapters embed sims too, and the teaching panel appears wherever the sim
is shown, because the mode comes from the sim's own `metadata.json`. It also reports the
sim's `CANVAS_HEIGHT` source. `microsim-utils`' `sync-iframe-heights.py` sets every
embedding iframe to `CANVAS_HEIGHT + 2`. So if you edit iframe heights by hand, its next
run silently shrinks them back. Instead:

1. Set the sim's `CANVAS_HEIGHT` (its `// CANVAS_HEIGHT:` comment, or `canvasHeight` in
   `metadata.json`, whichever the script reports) to the recommended height − 2.
2. Run `python3 ~/Documents/ws/ibook-skills/src/microsim-utils/sync-iframe-heights.py
   --project-dir . --sim <sim-name>` to update every embed.

A production sim should not change height; if it did, the wiring added something
visible, so find it.

### Step 9 — Verify both modes headless

```bash
uv run --with playwright==1.58.0 python $SKILL_DIR/scripts/check-xapi.py docs/sims/<sim-name> \
    --actions docs/sims/<sim-name>/xapi-actions.json      # optional; see below
```

The script serves `docs/` and embeds the sim in an iframe the way the book does. It
rewrites `metadata.json` in flight to Full, then Compact, then production, drives
interactions, and asserts the contract:

- only the three verbs,
- IRIs from the book's `siteUrl`, with no `main.html` and no localhost,
- grouping present,
- concept ids present and matching the metadata map,
- Compact silent until focus loss, then exactly one summary with
  `statements_represented`,
- answers passing through unfolded,
- no teaching UI in production,
- a clean console.

Generic driving covers DOM sliders, selects, checkboxes and buttons. For canvas clicks,
hovers, chart points or graph nodes, write a small actions file. The format is in
`scripts/check-xapi.py --help` and in each adapter. Keep that file in the scratch space,
not in the book, unless the user wants it. Iterate until every check passes. Report any
warning you decide to accept, and why.

### Step 10 — Lesson text (teaching sims only)

For a sim that teaches xAPI, add a section to `index.md` that lists what it emits in
each mode. Also add `keyQuestions` in `metadata.json` that make the student compare the
two streams. Use `$LRS_REPO/docs/sims/bouncing-ball/index.md` as the model. Production
sims get no lesson text about xAPI.

### Step 11 — Report

Tell the user, briefly:

- the evidence table (interaction → class → key → concept),
- anything left unmapped and why,
- files changed,
- the `check-xapi.py` summary, with the iframe height before and after,
- any unverified-adapter claim you had to correct. That feedback is how an adapter
  becomes verified.

## Reference files

| File | Read it when |
|---|---|
| `references/runtime-api.md` | Writing the wiring (step 6): every `LRSSim` option and handle, with worked examples |
| `references/evidence-classes.md` | Classifying (step 3): thresholds, fragment naming, Full vs. Compact per class |
| `references/concept-mapping.md` | Mapping concepts (step 4) |
| `references/contract-digest.md` | Any doubt about a statement's shape; the rules the runtime enforces |
| `references/pitfalls.md` | Before finishing step 6, and whenever a check fails for no obvious reason |
| `references/adapters/*.md` | Step 1 onward, for the sim's library |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/detect-library.py` | Library from script tags, runtime status, vendored files, interaction inventory |
| `scripts/find-concepts.py` | Candidate learning-graph concepts for a sim or search terms, with namespaced ids |
| `scripts/install-runtime.py` | Check or install the runtime and `lrs-config.js` in a book |
| `scripts/check-xapi.py` | Headless contract check of Full, Compact and production modes |
| `scripts/measure-iframe.py` | Iframe height with a full log at 375/700/900 px |

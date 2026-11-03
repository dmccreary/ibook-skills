# Iframe Height Tester

**Purpose:** Verify that a MicroSim's interactive controls (sliders, buttons,
dropdowns) are fully visible inside its `<iframe>` at the declared height.
This is a *geometric* check using a real headless browser — it complements
the *visual* review in [layout-reviewer.md](layout-reviewer.md) and the
build-time height sync in `scripts/sync-iframe-heights.py`.

## When to Use

- Controls appear clipped at the bottom of an embedded MicroSim
- Auditing iframe sizing across all MicroSims after a batch generation
- As a mandatory gate after `sync-iframe-heights.py` in the MicroSim
  generation pipeline

MicroSims embed in MkDocs via `<iframe>` tags with fixed heights and
`scrolling="no"`. If the iframe is too short, bottom controls get clipped and
students can't interact with them. This utility automates checking that every
MicroSim's controls fit at the declared height.

## How It Works

The Python script (`scripts/test-iframe-heights.py`) uses Playwright to:

1. Find all MicroSim directories under `docs/sims/`
2. Read each `index.md` to extract the declared iframe height
3. Load `main.html` in a browser viewport constrained to that height
4. Wait for p5.js (or other libraries) to finish rendering controls
5. Find all interactive elements (buttons, sliders, selects, inputs, checkboxes)
6. Check whether each element's bounding box fits within the iframe height
7. Measure the actual content height needed
8. Report pass/fail with a recommended height for failures

> **Note:** A legacy Node.js implementation (`test-iframe-heights.js`) was
> retired when this utility was consolidated into `microsim-utils`. The Python
> script is the only supported version — it needs just `pip install playwright`
> and no npm/Node toolchain.

## Prerequisites

```bash
pip install playwright
playwright install chromium
```

## Running the Tests

The script lives at `$BK_HOME/skills/microsim-utils/scripts/test-iframe-heights.py`.

```bash
SCRIPTS="$BK_HOME/skills/microsim-utils/scripts"

# Test all MicroSims
python3 $SCRIPTS/test-iframe-heights.py --sims-dir docs/sims

# Test a single MicroSim
python3 $SCRIPTS/test-iframe-heights.py --sims-dir docs/sims --sim energy-pyramid

# Test with a custom height override (ignores index.md heights)
python3 $SCRIPTS/test-iframe-heights.py --sims-dir docs/sims --height 530

# Generate a markdown report
python3 $SCRIPTS/test-iframe-heights.py --sims-dir docs/sims --report report.md
```

## Reading the Output

```
MicroSim                    | Iframe Height | Content Height | Status | Suggested Height
----------------------------|---------------|----------------|--------|------------------
energy-pyramid              |           532 |            528 | PASS   |              532
predator-prey               |           697 |            720 | FAIL   |              730
greenhouse-effect           |           500 |            498 | PASS   |              500
```

- **PASS**: All controls fit inside the *visible* iframe area (height minus
  the 4px border; 1px rounding tolerance)
- **FAIL**: One or more controls extend below the visible area. Even a 2–4px
  clip counts, because it cuts the bottom border off a button row.
- **SLACK**: Everything fits, but more than 30px of empty iframe sits below the
  content. Shrink the iframe to the suggested height.
- **Suggested Height**: measured content height + 4 (the border). Exact, not
  rounded, so it matches what `sync-iframe-heights.py` writes.
- **`declared CANVAS_HEIGHT N != measured M`**: the `.js` comment is stale.
  Update the comment to the measured value and re-run the sync.

## How the Test Matches the Real Page

- **Width:** the viewport is **684px**, the MkDocs Material content column in a
  1440px window with both sidebars. Pass `--width 746` to check a 1024px
  window too. Width-dependent sims (text wrap, wrapping button rows, Chart.js
  aspect ratio, p5 sims that size themselves) change height with width.
- **Height:** the viewport is the iframe height **minus 4px**. Material's
  `border-box` sizing draws the template's 2px iframe border inside the height
  on both top and bottom. Pass `--border 0` for a site with no iframe border.
- **Content:** measured over all of `<body>`, because p5's `createButton` and
  `createSlider` add controls to `<body>`, not to `<main>`.
- **Empty space inside the canvas** (a sim that sizes itself to its tallest
  view) can't be seen geometrically. The canvas fills the iframe either way.
  Use [layout-reviewer.md](layout-reviewer.md) and the "size to the common
  view" rule in [canvas-height-strategy.md](canvas-height-strategy.md).

## Fixing Failures

For each failing MicroSim, update the iframe height in `index.md`:

```html
<!-- Before -->
<iframe src="main.html" height="500" width="100%" scrolling="no"></iframe>

<!-- After — use the suggested height from the report -->
<iframe src="main.html" height="540" width="100%" scrolling="no"></iframe>
```

Also update the `// CANVAS_HEIGHT:` comment in the JavaScript file if present,
and any chapter markdown files that embed the same sim. The
`scripts/sync-iframe-heights.py` utility automates propagating a corrected
`CANVAS_HEIGHT` to every embed.

## Step-by-Step for Claude

1. Confirm the project root contains `docs/sims/` with MicroSim directories
2. Run `playwright install chromium` if not already installed
3. Run the Python test script from the project root
4. Present the results to the user
5. For failures, offer to update the iframe heights in the affected `index.md`
   files (or run `sync-iframe-heights.py` after setting `CANVAS_HEIGHT`)
6. If chapter markdown files also embed the failing sims, update those too

## Relationship to Other Utilities

| Utility | What it checks | Tool |
|---------|----------------|------|
| `sync-iframe-heights.py` | Propagates `CANVAS_HEIGHT` to every embed (build-time) | Python |
| **iframe-tester** (this guide) | Controls actually fit at the declared height (geometric) | Playwright |
| [layout-reviewer.md](layout-reviewer.md) | The rendering *inside* the canvas looks right (visual) | Claude Vision |

Run the tester first for "controls clipped at the edge" problems; use the
layout reviewer when the height is right but something *inside* the canvas
looks wrong.

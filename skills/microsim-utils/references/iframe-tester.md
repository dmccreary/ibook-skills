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

- **PASS**: All controls fit within the iframe height (with 5px tolerance)
- **FAIL**: One or more controls extend below the iframe boundary
- **Suggested Height**: The actual content height rounded up to the nearest
  10px, plus a 10px safety margin. If the sim's JS file contains a
  `// CANVAS_HEIGHT = N` comment, that declared height is used instead of the
  measured content height (responsive sims can measure taller at the test
  viewport width than they actually render in MkDocs).

## Responsive Sims and CANVAS_HEIGHT

Some p5.js sims dynamically resize their canvas based on viewport width. The
test viewport (700px) may not exactly match the MkDocs content column, causing
measured heights to differ from the actual embedded height. When a sim declares
`// CANVAS_HEIGHT = N` in its JS file, the tester trusts that value as
authoritative. **Always sanity-check suggestions for responsive sims** — if the
suggested height is dramatically larger than the current iframe height, the sim
likely has dynamic sizing and needs a `CANVAS_HEIGHT` declaration rather than a
blind height increase.

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

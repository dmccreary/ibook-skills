---
name: microsim-screen-capture
description: This skill automates the capture of high-quality screenshots for MicroSim visualizations using headless Chromium (Playwright). Use this skill when working with MicroSims that need preview images for social media sharing, documentation, or quality assessment. The skill handles JavaScript-heavy visualizations that require proper rendering time and external CDN resources.
---

# MicroSim Screen Capture

## Overview

This skill automates the process of capturing high-quality screenshots of MicroSim visualizations using headless Chromium driven by Playwright. It properly handles dynamic JavaScript content, external CDN libraries (like vis-network.js, p5.js, Chart.js), and ensures the visualization has time to fully render before capturing.

## When to Use This Skill

Use this skill when:

- Creating preview images for MicroSims that need social media metadata (`og:image`)
- Generating screenshots for MicroSim documentation
- Capturing visualizations for quality assessment or archival purposes
- Working with the microsim-standardization skill to achieve a perfect 100/100 quality score

**Typical user requests:**
- "Create a screenshot of this MicroSim"
- "I need a preview image for the org-chart MicroSim"
- "Generate a social media preview for this visualization"
- "Capture a screenshot of the main.html file"

## Workflow

### Step 1: Validate the MicroSim Directory

Before capturing a screenshot, verify:

1. The MicroSim directory exists at the provided path (typically `docs/sims/{microsim-name}/`)
2. The directory contains a `main.html` file
3. The MicroSim name follows kebab-case convention (lowercase letters and dashes only)

### Step 2: Run the Screenshot Capture Script

Execute the `bk-capture-screenshot` script with the MicroSim directory path, the render delay in seconds, and the iframe height from the MicroSim's `index.md`:

```bash
~/.local/bin/bk-capture-screenshot <microsim-directory-path> [delay-seconds] [height]
```

**Example:**
```bash
~/.local/bin/bk-capture-screenshot /Users/dan/Documents/ws/intro-to-graph/docs/sims/org-chart 3 600
```

The script will:

1. Extract the MicroSim name from the directory path (e.g., `org-chart` from `.../sims/org-chart/`)
2. Locate the `main.html` file in the directory
3. Serve it from a temporary `127.0.0.1` HTTP server and load it in headless Chromium at an exact 800 x height viewport
4. Wait the render delay (default 3 seconds), then capture the viewport
5. Save the screenshot as `{microsim-name}.png` in the MicroSim directory (e.g., `org-chart.png`)
6. Display the output file path and size upon success, plus the first few uncaught JavaScript errors if any

**Why the height argument matters:** the viewport is exactly the height you pass, from the first frame. Layouts that use `height: 100vh` (including the standard vis-network template) and p5 sketches that read `windowHeight` size themselves to it, so passing the iframe height makes the screenshot match what readers see in the page.

### Step 3: Verify the Screenshot

After the script completes:

1. Check that the image file was created: `{microsim-name}.png`
2. Verify the file size is reasonable (typically 20-100KB for rendered visualizations)
3. Use the Read tool to view the screenshot and confirm the visualization rendered properly
4. If the visualization area appears blank/white, the JavaScript may need more time to render - pass a longer delay as the second argument (e.g., `10`)
5. If the bottom of the layout (legend, controls, bottom row of nodes) is cut off or there is empty space, check that the height argument matches the iframe height in `index.md`

### Step 4: Update MicroSim Metadata (Optional)

If capturing the screenshot as part of MicroSim standardization, update the `index.md` YAML frontmatter:

```yaml
---
title: MicroSim Title
description: Brief description
image: microsim-name.png
og:image: microsim-name.png
quality_score: 100
---
```

This adds the social media preview metadata and contributes 10 points toward the quality score (5 points for metadata fields + 5 points for the image file existing).

## Troubleshooting

### Screenshot captures but visualization is blank

**Problem:** The screenshot shows the page header/controls but the main visualization area is white/empty.

**Solutions:**
1. The `bk-capture-screenshot` script waits 3 seconds by default; for complex visualizations, pass a longer delay as the second argument
2. Check the script output for `JS error:` lines — it prints the first few uncaught JavaScript errors from the page
3. Verify the visualization works under `mkdocs serve` in a browser

### Playwright not found error

**Problem:** Script reports "Playwright for Python not found"

**Solutions:**
1. Install it: `pip install playwright && playwright install chromium`
2. Or activate the conda env that already has it (e.g., `conda activate mkdocs`)
3. Or set `BK_PYTHON` to a `python3` that can `import playwright`

If Playwright is installed but its Chromium download is missing, the script falls back to Google Chrome automatically.

### External resources not loading

**Problem:** Visualizations that use CDN libraries (vis-network, p5.js, Chart.js) don't render

**Solution:** If still not working:
1. Verify internet connectivity (CDNs need to be accessible)
2. Check if the library CDN URL is valid in `main.html`
3. Check the script output for `JS error:` lines

### localhost Server

The `bk-capture-screenshot` script serves the MicroSim from a temporary Python HTTP server on `127.0.0.1` instead of opening it as `file://`. Headless Chromium blocks `fetch()` of `file://` URLs, so MicroSims that load `data.json` (like the vis-network template) would otherwise render empty.

The server root is the git repository that contains the MicroSim (or two directories above it outside git), so relative links such as `../../img/logo.png` resolve the same way they do under `mkdocs serve`. The server stops when the capture finishes.

## Technical Details

### Why Playwright?

Playwright drives headless Chromium through the DevTools protocol, which lets the script:
1. **Set an exact viewport:** The viewport is exactly 800 x height before the page loads. Chrome's own `--headless --screenshot --window-size` starts the page about 87px shorter on macOS and resizes only at capture time, so `100vh` layouts and sketches that size once in `setup()` came out wrong
2. **Render WebGL:** SwiftShader software WebGL flags make p5.js `WEBGL` sketches render instead of showing blank rectangles
3. **Report page errors:** Uncaught JavaScript errors are printed with the result
4. **Run without a GUI:** Works on macOS, Linux, and in CI

### Screenshot Naming Convention

The script names screenshots using the MicroSim directory name to maintain consistency:
- MicroSim: `docs/sims/org-chart/` → Screenshot: `org-chart.png`
- MicroSim: `docs/sims/learning-graph-viewer/` → Screenshot: `learning-graph-viewer.png`

This differs from using a generic name like `preview.png` because:
1. Makes the file purpose immediately clear when viewing the directory
2. Easier to identify which screenshot belongs to which MicroSim in bulk operations
3. Follows naming conventions used elsewhere in the project

### Default Screenshot Dimensions

The screenshot is 800 pixels wide by the height argument (default 600):

- **Width (800px):** Close to the MkDocs Material content column, so the layout matches the embedded iframe
- **Height:** Pass the iframe height from `index.md` so the image shows exactly what readers see
- **File Size:** Produces reasonably sized PNG files (typically 20-100KB)

## Resources

### ~/.local/bin/bk-capture-screenshot

User-installed Bash script (a symlink to `scripts/bk-capture-screenshot` in this repo) that automates the entire screenshot capture process. The script:

- Validates input and checks for required files
- Checks that `python3` (or `BK_PYTHON`) can import Playwright
- Starts a temporary local HTTP server rooted at the enclosing git repo
- Loads `main.html` at an exact 800 x height viewport and waits for JavaScript to render
- Saves screenshot as `{microsim-name}.png` in the MicroSim directory
- Reports success/failure with file size information

Requirements: Python 3 with Playwright (`pip install playwright && playwright install chromium`). Google Chrome is used as a fallback if Playwright's Chromium is not installed.

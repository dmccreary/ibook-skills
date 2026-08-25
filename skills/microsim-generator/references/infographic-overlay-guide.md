# Interactive Infographic Overlay Guide

> Formerly the standalone skill `interactive-infographic-overlay`.

## Overview

This guide generates a complete MicroSim directory for interactive diagram overlays used in intelligent textbooks. It produces all files needed for a diagram where:

1. A text-to-image LLM generates an annotation-free scientific illustration
2. The `diagram.js` shared library renders interactive numbered markers, leader lines, and labels over the image
3. Students can explore (hover for info), take quizzes (identify structures), and instructors can edit marker positions

## When to Use This Guide

Use this guide when:

- A chapter content spec includes a `#### Diagram:` details block with type "Interactive Infographic" or "Diagram" that requires a scientific illustration with labeled callouts
- The textbook needs a labeled anatomy diagram, structural diagram, process diagram, or any image with identified regions
- The specification calls for explore mode (hover to learn), quiz mode (identify structures), or both

Do NOT use this guide when:

- The diagram is better served by Mermaid, Chart.js, or p5.js drawing (no background image needed) — route to that generator guide instead
- The content is a pure simulation with dynamic elements (use the p5 guide instead)
- The diagram needs only simple inline markdown images with no interactivity

## Overlay Types: Callout vs. Grid

This guide supports **two distinct overlay engines** depending on the infographic type:

| Engine | Use When | Files |
|--------|----------|-------|
| **Callout** (`diagram.js` + `style.css`) | Scientific illustrations with numbered point markers on specific structures (anatomy, cell diagrams, labeled components) | `main-template.html`, `overlay-data-json-schema.md` |
| **Grid** (`grid-diagram.js` + `grid-overlay.css`) | Comparison infographics or posters with large rectangular column/region zones (side-by-side comparisons, poster sections) | `grid-main-template.html`, `overlay-grid-data-json-schema.md` |

**Key differences:**

- Callout uses `callouts[]` with `x`, `y` point coordinates and draws numbered circle markers with leader lines
- Grid uses `zones[]` with `x1`, `y1`, `x2`, `y2` rectangle coordinates and draws transparent hover rectangles over columns/regions
- Grid supports `showLabels: true/false` to control whether a chip label appears inside each zone (set to `false` when the image already has printed column titles)

## Prerequisites

The project must have the shared overlay libraries installed:

```
docs/sims/shared-libs/
├── diagram.js          (callout overlay engine — point markers)
├── style.css           (callout overlay styles)
├── grid-diagram.js     (grid overlay engine — rectangular zones)
└── grid-overlay.css    (grid overlay styles)
```

To install all four files from this skill's bundled assets:

```bash
mkdir -p docs/sims/shared-libs
cp $BK_HOME/skills/microsim-generator/assets/infographic-overlay/shared-libs/diagram.js docs/sims/shared-libs/
cp $BK_HOME/skills/microsim-generator/assets/infographic-overlay/shared-libs/style.css docs/sims/shared-libs/
cp $BK_HOME/skills/microsim-generator/assets/infographic-overlay/shared-libs/grid-diagram.js docs/sims/shared-libs/
cp $BK_HOME/skills/microsim-generator/assets/infographic-overlay/shared-libs/grid-overlay.css docs/sims/shared-libs/
```

Always check that the project's copy is up to date with the skill's bundled version before creating new diagram MicroSims.

## Workflow

### Choosing the Overlay Type

Before generating files, decide which engine to use:

- **Use Callout** when the diagram is a scientific illustration (anatomy, hardware internals, botanical diagrams, labeled components) where small numbered markers should point to specific structures
- **Use Grid** when the infographic is a comparison poster or section-based layout (3-column technology comparison, side-by-side concept contrasts, poster regions) where large rectangular hover zones make more sense

The two workflows below share the same Steps 1, 2, 6, 7, 8 but differ in Steps 3–5.

---

## Callout Overlay Workflow (diagram.js)

### Step 1: Gather Diagram Requirements

Extract from the chapter content specification or user request:

1. **Subject** — What the diagram depicts (e.g., "animal cell cross-section," "moss sporophyte anatomy," "mossarium layers")
2. **Structures to label** — List of 5-15 structures/regions with:
   - Name/label
   - Brief description (1-2 sentences)
   - Approximate position in the image
   - Suggested color for the marker
3. **Image style** — Scientific illustration style (flat, watercolor, realistic, etc.)
4. **Image dimensions** — Typically 1200×900 (landscape 4:3) or 900×1200 (portrait 3:4)
5. **Layout** — `side-panel` (default, labels on right), `top-bottom`, or `dual-panel`
6. **Context tips** — Optional exam tips, hints, or additional info per structure

### Step 2: Create the MicroSim Directory

Create the directory under `docs/sims/`:

```bash
mkdir -p docs/sims/{sim-id}
```

Where `{sim-id}` is a kebab-case name (e.g., `moss-sporophyte`, `mossarium-layers`, `animal-cell`).

### Step 3: Generate image-prompt.md

Create `docs/sims/{sim-id}/image-prompt.md` with a detailed prompt for the text-to-image LLM. Use the template in [overlay-image-prompt.md](overlay-image-prompt.md).

**Critical rules for all image prompts:**

1. **NO TEXT IN THE IMAGE** — The image must contain absolutely no text, labels, arrows, callout lines, numbers, or annotation marks of any kind — **including the diagram's title or any heading** (the engine renders the title as an `<h1>`; see [Title Rendering](#title-rendering)). All labeling is handled by diagram.js.
2. Specify exact dimensions, background color, and art style
3. Describe each structure with precise position, color, shape, and size
4. Use percentage-based positioning (e.g., "centered at 40% from left, 30% from top")
5. Specify the viewing angle (cross-section, top-down, side view, etc.)

### Step 4: Generate data.json

Create `docs/sims/{sim-id}/data.json` with the overlay data. See [overlay-data-json-schema.md](overlay-data-json-schema.md) for the complete schema and field definitions.

**Position guidelines:**

- `x` and `y` are percentages of the image dimensions (0 = left/top, 100 = right/bottom)
- Place markers at the visual center of each structure
- Space markers at least 5-8% apart to avoid overlap
- Use the `?edit=true` URL parameter to calibrate positions after image generation

**Panel assignment (`top-bottom` and `dual-panel` layouts only):**

For these layouts each callout needs a `panel` field that decides which label
strip it lives in. **Assign it by proximity — send every label to the strip
nearest its marker. Never use an alternating / odd-even (parity) pattern.** The
leader line's length is dominated by the gap between the marker and its label
strip, so a parity pattern scatters labels far from their structures and makes
the lines cross; proximity assignment keeps them short and readable.

- **`top-bottom`** (top strip above the image, bottom strip below): sort the
  callouts by `y` (0 = top of image). Give the upper half (smallest `y`)
  `"panel": "top"` and the lower half `"panel": "bottom"`. With an odd count,
  put the extra label on `top`. Splitting at the median keeps the two strips
  balanced (so neither is overcrowded) while still placing each label on the
  edge closest to its marker. Then, **within each strip, list the callouts
  left-to-right by ascending `x`** so the leader lines don't cross.
- **`dual-panel`** (left strip | image | right strip): the same idea rotated 90°.
  Sort by `x`, give the left half `"panel": "left"` and the right half
  `"panel": "right"`, and order each side top-to-bottom by ascending `y`.
- **`side-panel`**: omit `panel` entirely — there is only one label panel.

Tip: if you also number the callouts (`id`) in the same geometric order you use
for panels — e.g. top-to-bottom for `top-bottom` — the low ids naturally land on
`top` and the labels read in order, so the numbering and the proximity rule agree.

### Step 5: Generate main.html

Create `docs/sims/{sim-id}/main.html` using the template in `assets/infographic-overlay/main-template.html`. Replace `{TITLE}`, `{IMAGE_FILENAME}`, and `{ALT_TEXT}` with the actual values.

### Step 6: Generate index.md

Create `docs/sims/{sim-id}/index.md` with documentation and an embedded iframe. Include:

- A frontmatter `title:` (drives the page `<title>`, nav label, and social cards) plus `hide: toc`. **Do not add a `# Title` H1 in the page body** — `diagram.js` already renders the title as an `<h1>` inside the iframe, so a body H1 would show the title twice. See [Title Rendering](#title-rendering).
- Embedded iframe (`height="640px" width="100%"`)
- Fullscreen link
- Usage instructions for explore, quiz, and edit modes
- Numbered list of all labeled structures

### Step 7: Update mkdocs.yml

Add two entries to `mkdocs.yml`:

1. **Navigation** — Add the MicroSim to the nav section under MicroSims
2. **Exclude image prompt from build** — Add `sims/{sim-id}/image-prompt.md` to the `exclude_docs:` block to prevent mkdocs from rendering it as a page. Create the `exclude_docs:` block if it doesn't exist yet.

### Step 8: Inform the User

Report all files created and provide next steps:

1. Copy image prompt into text-to-image tool
2. Save generated image to the MicroSim directory
3. View at `http://127.0.0.1:8000/{repo}/sims/{sim-id}/main.html`
4. Calibrate positions with `?edit=true`
5. Copy calibrated JSON back into data.json

---

## Grid Overlay Workflow (grid-diagram.js)

Use this workflow when the infographic is a comparison poster or section-based layout.

### Grid Step 1: Gather Zone Requirements

Extract from the chapter content specification or user request:

1. **Subject** — What the infographic compares (e.g., "digital vs. analog signals", "textbook intelligence levels", "three sorting algorithms")
2. **Zones** — List of 2–6 rectangular regions with:
   - `id` (kebab-case, unique)
   - `label` (display name)
   - `color` (hex)
   - Approximate percentage boundaries (`x1`, `y1`, `x2`, `y2`)
   - One-line `summary`
   - 3–6 bullet `facts`
3. **Image style** — Flat infographic, comparison poster, data visualization
4. **Image dimensions** — Typically 900×600 (landscape) or 1200×800
5. **showLabels** — `false` if the image has printed column titles (default); `true` only if the image has no titles

### Grid Step 2: Create the MicroSim Directory

```bash
mkdir -p docs/sims/{sim-id}
```

### Grid Step 3: Generate image-prompt.md

Use [overlay-image-prompt.md](overlay-image-prompt.md) with these extra rules for comparison posters:

1. **Columns/regions must have visible titles** in the image (the chip labels are hidden by default for grid overlays). Each column should have a bold, legible header text built into the illustration.
2. **No interactive callout marks** — no numbers, arrows, or overlaid text annotations (same as callout type)
3. Each region should have a **distinct color scheme** matching the intended zone color
4. Describe exact pixel regions or percentage positions so zone boundaries in data.json can be estimated accurately

### Grid Step 4: Generate data.json

Create `docs/sims/{sim-id}/data.json` using the schema in [overlay-grid-data-json-schema.md](overlay-grid-data-json-schema.md).

Zone position guidelines:

- Start by estimating zone boundaries from the image description (percentage of image width/height)
- Use `?edit=true` to drag corner handles and calibrate after the image is generated
- For a standard 3-column landscape poster, typical zone boundaries are:
  - Column 1: `x1: 2, y1: 12, x2: 32, y2: 90`
  - Column 2: `x1: 35, y1: 12, x2: 65, y2: 90`
  - Column 3: `x1: 68, y1: 12, x2: 98, y2: 90`

### Grid Step 5: Generate main.html

Use `assets/infographic-overlay/grid-main-template.html`. Replace `{TITLE}` and `{PROMPT_TEXT}` (the click-to-explore instruction). The image and zones are injected by `grid-diagram.js` — there is no `<img>` tag in the template.

Link to `grid-overlay.css` and `grid-diagram.js`:

```html
<link rel="stylesheet" href="../shared-libs/grid-overlay.css">
...
<script src="../shared-libs/grid-diagram.js"></script>
```

### Grid Step 6–8

Follow the same steps as the Callout workflow (Step 6: index.md, Step 7: mkdocs.yml, Step 8: Inform user).

### Grid Edit Mode

Same as callout edit mode but uses **draggable corner handles** instead of draggable marker circles:

1. Open `main.html?edit=true`
2. Drag the four corner handles of each zone to calibrate the rectangle
3. Click "Copy JSON" to get updated coordinates
4. Replace the `zones` array in `data.json`

---

## Calibration Workflow

After the image is generated and saved, marker positions will likely need adjustment:

1. Open `main.html?edit=true` in the browser
2. Drag each numbered marker to the correct position on the image
3. Click "Copy JSON" to get the calibrated coordinates
4. Replace the `callouts` array in `data.json` with the copied data
5. Reload the page to verify positions

This edit mode is built into diagram.js and requires no additional code.

## Layout Options

| Layout | Description | Best For |
|--------|-------------|----------|
| `side-panel` | Image left (65%), labels right (35%) | Most diagrams — default choice |
| `top-bottom` | Labels above and below image | Wide panoramic images |
| `dual-panel` | Labels left (22%), image center (56%), labels right (22%) | Diagrams with many callouts (12+) |

## Color Palette for Markers

```
#8E44AD  purple    — nucleus, central structures
#E74C3C  red       — energy-related structures
#3498DB  blue      — membrane structures
#2ECC71  green     — photosynthetic structures
#E67E22  orange    — transport structures
#1ABC9C  teal      — storage structures
#F39C12  gold      — signaling structures
#9B59B6  violet    — genetic structures
#34495E  dark gray — structural elements
#16A085  sea green — fluid/matrix regions
```

## Iframe Auto-Resize via postMessage

Diagram overlay MicroSims have responsive content heights that change with
viewport width. Rather than guessing a fixed `height` for the `<iframe>`,
`diagram.js` automatically reports its actual content height to the parent
page via `postMessage`. The parent page's `extra.js` listens for these
messages and adjusts the iframe height dynamically.

> **Before modifying `reportHeight()` in `diagram.js`, read
> [overlay-iframe-height-pinning.md](overlay-iframe-height-pinning.md)** — it
> documents the non-obvious constraints behind the worst-case-height design.

### How It Works

1. **Sender (diagram.js)** — After init and on every resize, the
   `reportHeight()` method temporarily populates the infobox with the
   **longest** callout's description + tip, measures
   `document.body.scrollHeight + 30px`, then restores the default infobox
   state. This ensures the iframe is sized for the worst-case content height
   from the start — no clipping when users hover over long descriptions.

2. **Receiver (extra.js on parent page)** — A `message` event listener
   matches `event.source` to the correct iframe's `contentWindow` and sets
   `iframe.style.height` to the reported height.

3. **Fallback** — The static `height="NNN"` attribute in the iframe HTML
   remains as a fallback shown while the sim loads. Once the sim renders
   and reports its height, the static value is overridden.

### Requirements

The parent page must include this listener in its JavaScript (already present
in the standard `docs/js/extra.js`):

```javascript
window.addEventListener('message', function (event) {
    if (!event.data || event.data.type !== 'microsim-resize') return;
    var iframes = document.querySelectorAll('iframe');
    for (var i = 0; i < iframes.length; i++) {
        if (iframes[i].contentWindow === event.source) {
            iframes[i].style.height = event.data.height + 'px';
            break;
        }
    }
});
```

If the project's `extra.js` does not have this listener, add it. The
diagram MicroSims will still work without it — they'll just use the static
iframe height as before.

## Controls Placement

The Explore/Quiz `#controls` div must be placed **below** `#layout` and
**above** `#infobox` in `main.html`. This gives the diagram image maximum
vertical space and places mode buttons where users expect them after
viewing the diagram. The `main-template.html` asset already follows this
order.

## Title Rendering

`diagram.js` renders the diagram title for you: `injectTitle()` inserts an
`<h1 class="sim-title">` above the diagram inside `main.html`, using the
`title` field from `data.json`. Because the engine owns the title, it must
appear in exactly one place. Guard against the two ways it gets duplicated:

1. **No title text baked into the generated image.** This is part of the "no
   text in the image" rule, but the title/heading is the single most common
   thing an image generator adds anyway. A baked-in title would sit on the
   illustration *and* be repeated by the engine's `<h1>`. Regenerate if the
   image comes back with a title.
2. **No `# Title` H1 in the `index.md` body.** The standalone page embeds
   `main.html`, which already shows the engine's `<h1>`, so a markdown H1 above
   the iframe would display the title twice. Put the title only in the
   `index.md` frontmatter `title:` — that drives the page `<title>`, nav label,
   and social cards, not a visible body heading.

`data.json.title` stays as the single source of the title: it feeds the engine's
`<h1>` and the image `alt` text, so keep it — it is never the visible duplicate.

## Common Pitfalls

- **Text in generated images** — Always verify the image has NO text, labels, arrows, or **title/heading**. Regenerate if the LLM adds annotations.
- **Duplicate title** — The title must appear exactly once. `diagram.js` injects an `<h1>` from `data.json.title`, so the image must have no baked-in title and `index.md` must have no `# Title` body H1 (use the frontmatter `title:` only). See [Title Rendering](#title-rendering).
- **Marker overlap** — Keep callout positions at least 5-8% apart. Use edit mode to fine-tune.
- **Missing shared-libs** — Verify `docs/sims/shared-libs/diagram.js` and `style.css` exist before testing.
- **Forgetting exclude_docs** — The `image-prompt.md` file will cause mkdocs build warnings if not excluded.
- **Wrong image path** — The `image` field in data.json must match the exact filename (case-sensitive).

## Resources

### references/ (this skill)

- `overlay-data-json-schema.md` — Callout overlay data.json schema (point markers, `callouts[]` array)
- `overlay-grid-data-json-schema.md` — Grid overlay data.json schema (rectangular zones, `zones[]` array)
- `overlay-image-prompt.md` — Template for generating annotation-free image prompts
- `overlay-iframe-height-pinning.md` — Design rationale for `reportHeight()`; read before changing height logic

### assets/infographic-overlay/ (this skill)

- `main-template.html` — HTML template for callout overlay MicroSims (uses `diagram.js`)
- `grid-main-template.html` — HTML template for grid overlay MicroSims (uses `grid-diagram.js`)
- `shared-libs/diagram.js` — Callout overlay engine: numbered point markers, leader lines, explore/quiz/edit modes
- `shared-libs/style.css` — Styles for callout overlay MicroSims
- `shared-libs/grid-diagram.js` — Grid overlay engine: rectangular hover zones, explore/quiz/edit modes
- `shared-libs/grid-overlay.css` — Styles for grid overlay MicroSims

### Test Case

A working grid overlay test is available at `docs/sims/grid-overlay-test/` in the ibook-skills repo:

- `test-image.svg` — SVG comparison infographic (3 columns: Static vs. Interactive vs. Adaptive)
- `data.json` — 3 zones + 3 quiz questions
- `main.html` — Uses `grid-diagram.js` and `grid-overlay.css`
- `index.md` — MkDocs page with embedded iframe

Preview at: `http://127.0.0.1:8000/ibook-skills/sims/grid-overlay-test/`

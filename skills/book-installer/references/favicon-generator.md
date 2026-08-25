---
name: favicon-generator
description: Generates a web-compliant multi-resolution favicon.ico from the project mascot's neutral.png image. Centers non-square mascots on a square canvas and embeds all standard icon sizes (16–256 px) in a single .ico file.
---

# Favicon Generator (from Mascot)

This guide converts the learning mascot's `neutral.png` image into a
browser-compliant `favicon.ico` that works across all browsers, bookmarks,
taskbars, and mobile home screens.

## When to Use This Guide

Use this guide when:
- The project has a mascot at `docs/img/mascot/neutral.png`
- No `docs/img/favicon.ico` exists yet (or you want to replace it)
- You want the browser tab icon to match the mascot branding

## Prerequisites

1. **Pillow** installed in the active Python environment:
   ```bash
   pip install Pillow
   ```

2. **Mascot image** present:
   ```
   docs/img/mascot/neutral.png
   ```
   The image does **not** need to be square — the script handles centering.

3. **Script** available at:
   ```
   $BK_HOME/skills/book-installer/scripts/generate-favicon.py
   ```
   (`$BK_HOME` points at the ibook-skills checkout and is agent-neutral. Do
   not substitute a path under `~/.claude/skills/`, `~/.codex/skills/`, or
   `~/.gemini/antigravity/skills/` — each is specific to one agent framework,
   and this skill runs on all of them.)

## Step 1: Verify the Source Image Exists

```bash
ls -lh docs/img/mascot/neutral.png
```

If the file is missing, ask the user to generate the mascot first using the
`learning-mascot.md` guide before continuing.

## Step 2: Run the Favicon Generator Script

From the **project root** (the directory containing `mkdocs.yml`):

```bash
python3 $BK_HOME/skills/book-installer/scripts/generate-favicon.py
```

This uses all defaults:
- **Source**: `docs/img/mascot/neutral.png`
- **Output**: `docs/img/favicon.ico`
- **Background**: transparent
- **Padding**: 8 % of the content area on each side

### Expected Output

```
source : docs/img/mascot/neutral.png  (400x600)
content: 380x560 px (after transparent trim)
canvas : 620x620 px (square, 8% padding, bg=transparent)
wrote  : docs/img/favicon.ico  (sizes: 16, 32, 48, 64, 128, 256)
```

The script:
1. Opens `neutral.png` and converts to RGBA
2. Detects the bounding box of non-transparent pixels (trims invisible padding)
3. Centers the visible content on a square canvas with 8 % padding
4. Downscales to each favicon size using Lanczos resampling
5. Saves all six sizes into a single multi-resolution `.ico` file

## Step 3: Optional Flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--src PATH` | `docs/img/mascot/neutral.png` | Override source PNG |
| `--out PATH` | `docs/img/favicon.ico` | Override output path |
| `--bg transparent` | ✓ | Transparent square background |
| `--bg white` | | White square background |
| `--padding N` | `8` | % of content size used as padding |

**Examples:**

```bash
# White background (for browsers that don't support transparency in .ico)
python generate-favicon.py --bg white

# Larger breathing room around the mascot
python generate-favicon.py --padding 15

# Different source image
python generate-favicon.py --src docs/img/mascot/celebration.png

# Completely custom paths
python generate-favicon.py \
  --src docs/img/mascot/neutral.png \
  --out docs/img/favicon.ico \
  --bg transparent \
  --padding 8
```

## Step 4: Configure mkdocs.yml

Add the favicon path to the `theme:` section in `mkdocs.yml`:

```yaml
theme:
  name: material
  favicon: img/favicon.ico
```

If a `favicon:` line already exists, update the value to `img/favicon.ico`.

**Full example `theme:` block context:**

```yaml
theme:
  name: material
  logo: img/logo.png
  favicon: img/favicon.ico
  palette:
    primary: indigo
    accent: indigo
```

## Step 5: Verify

Restart `mkdocs serve` (the user runs this in their own terminal) and open
the site at `http://127.0.0.1:8000/{repo-name}/`. Check:

- The browser tab shows the mascot icon
- Bookmarking the page shows the correct icon
- The icon is recognizable even at the small 16×16 tab size

## Troubleshooting

### "Pillow is not installed"

```bash
pip install Pillow
# or, in a conda environment:
conda install pillow
```

### "source file not found"

The script looks for `docs/img/mascot/neutral.png` relative to the current
working directory. Run the script from the project root (where `mkdocs.yml`
lives), or supply `--src` with the full path.

### Icon appears as white square (no mascot visible)

The mascot PNG may have a fully opaque white background rather than
transparency. Options:

1. Use `--bg white` so the canvas matches the image background.
2. Remove the white background from the PNG using an image editor or
   the `trim-padding-from-image.py` script (which handles transparency trimming).

### Icon looks blurry at small sizes

Favicon legibility at 16×16 is inherently limited for detailed images.
Consider:
- Increasing `--padding 0` to use more of the tile area
- Using `--src` with a simpler, higher-contrast mascot pose
- Adding a solid background circle with `--bg white` to improve contrast

### mkdocs.yml not picking up the favicon

Ensure the path in `mkdocs.yml` is relative to `docs/`:
```yaml
favicon: img/favicon.ico   # correct  (docs/img/favicon.ico)
favicon: docs/img/favicon.ico  # wrong
```

## Web Standards Reference

The generated `.ico` embeds six sizes required for full compatibility:

| Size | Used by |
|------|---------|
| 16×16 | Browser tab, bookmarks bar |
| 32×32 | Browser tab (HiDPI / Retina), Windows taskbar |
| 48×48 | Windows site icons, some browser toolbars |
| 64×64 | Windows jump lists, high-res contexts |
| 128×128 | Chrome Web Store, macOS Dock |
| 256×256 | Windows Vista+, macOS Finder |

MkDocs Material also serves the `.ico` as the default favicon, and browsers
automatically pick the best embedded size for their context.

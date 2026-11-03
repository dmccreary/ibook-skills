#!/usr/bin/env python3
"""Fix iframe heights in each MicroSim's index.md to match the actual sim height.

Own-page-only predecessor of `sync-iframe-heights.py` (which also updates chapter
embeds and shares this same resolution order). Prefer `sync-iframe-heights.py`
for full propagation; see `references/canvas-height-strategy.md`.

Height detection (in priority order — CANVAS_HEIGHT, then iframe = it + 4px,
the template's 2px border counted top and bottom):
  1. // CANVAS_HEIGHT: <int> comment in <sim>.js — primary for sims with a .js.
  2. "canvasHeight": <int> in metadata.json — the consistent place for sims with
     NO .js (Mermaid, vis-network, Chart.js, Leaflet, vis-timeline, custom HTML).
  3. <!-- CANVAS_HEIGHT: <int> --> comment in main.html — back-compat.
  4. From <sim>.js: vis-network container + 80px, createCanvas() height, or a
     named height variable.

Usage:
  python3 fix-iframe-heights.py --project-dir /path/to/project --verbose
  python3 fix-iframe-heights.py --project-dir /path/to/project --sim volcano-plot
  python3 fix-iframe-heights.py --project-dir /path/to/project --dry-run
"""
import argparse
import json
import os
import re
import glob
import sys

# MkDocs Material's border-box sizing draws the template's 2px iframe border
# inside the height on top AND bottom, so the iframe needs 4px over the sim.
IFRAME_BORDER = 4


def detect_height(sim_dir, sim_name):
    """Detect the correct iframe height for a MicroSim by parsing its JS and HTML."""
    js_path = os.path.join(sim_dir, f'{sim_name}.js')
    js_content = ''
    if os.path.isfile(js_path):
        with open(js_path) as f:
            js_content = f.read()

    # PRIMARY: the universal `// CANVAS_HEIGHT: <int>` comment in the .js.
    # The iframe height = CANVAS_HEIGHT + IFRAME_BORDER.
    canvas_height_match = re.search(
        r'^\s*//\s*CANVAS_HEIGHT\s*:\s*(\d+)\s*$',
        js_content,
        re.MULTILINE,
    )
    if canvas_height_match:
        return int(canvas_height_match.group(1)) + IFRAME_BORDER, 'CANVAS_HEIGHT comment + border'

    # FALLBACK for sims with no .js comment: the structured metadata.json field.
    meta_path = os.path.join(sim_dir, 'metadata.json')
    if os.path.isfile(meta_path):
        try:
            val = json.load(open(meta_path)).get('canvasHeight')
        except (ValueError, OSError):
            val = None
        if isinstance(val, int) and not isinstance(val, bool):
            return val + IFRAME_BORDER, 'metadata.json canvasHeight + border'
        if isinstance(val, str) and val.strip().isdigit():
            return int(val.strip()) + IFRAME_BORDER, 'metadata.json canvasHeight + border'

    # Detect library type from main.html + read a back-compat HTML comment.
    main_html = os.path.join(sim_dir, 'main.html')
    is_vis = False
    if os.path.isfile(main_html):
        with open(main_html) as f:
            html = f.read()
        html_comment = re.search(
            r'<!--\s*CANVAS_HEIGHT\s*[:=]\s*(\d+)\s*-->', html, re.IGNORECASE
        )
        if html_comment:
            return int(html_comment.group(1)) + IFRAME_BORDER, 'main.html CANVAS_HEIGHT + border'
        if 'vis-network' in html:
            is_vis = True

    if not js_content:
        return None, 'no JS file and no metadata/html height'

    if is_vis:
        # vis-network: look for height in JS
        # Common patterns: height:450px, height:'450px', style="...height:450px..."
        h_match = re.search(r"height['\"]?\s*[:=]\s*['\"]?(\d+)", js_content)
        if h_match:
            container_h = int(h_match.group(1))
            return container_h + 80, 'vis-network container + 80px'
        return 530, 'vis-network default'
    else:
        # p5.js: look for createCanvas(width, height)
        canvas_match = re.search(r'createCanvas\s*\(\s*\w+\s*,\s*(\d+)', js_content)
        if canvas_match:
            return int(canvas_match.group(1)) + IFRAME_BORDER, 'createCanvas height + border'

        # Named height variables
        h_var = re.search(
            r'(?:canvasHeight|drawHeight|cHeight)\s*=\s*(\d+)', js_content
        )
        if h_var:
            return int(h_var.group(1)) + IFRAME_BORDER, 'named height var + border'

        # Generic height variable declaration
        h_var2 = re.search(
            r'(?:let|const|var)\s+(?:h|height)\s*=\s*(\d+)', js_content
        )
        if h_var2:
            return int(h_var2.group(1)) + IFRAME_BORDER, 'generic height var + border'

        return None, 'could not detect height from JS'


def fix_sim_height(sim_dir, sim_name, dry_run=False, verbose=False):
    """Fix the iframe height in a single sim's index.md. Returns (old, new) or None."""
    index_path = os.path.join(sim_dir, 'index.md')
    if not os.path.isfile(index_path):
        if verbose:
            print(f'  SKIP {sim_name}: no index.md')
        return None

    height, reason = detect_height(sim_dir, sim_name)
    if height is None:
        if verbose:
            print(f'  SKIP {sim_name}: {reason}')
        return None

    with open(index_path) as f:
        index_content = f.read()

    # Match iframe with height attribute
    iframe_pattern = r'(<iframe\s[^>]*?)height\s*=\s*["\']?(\d+)[px]*["\']?([^>]*>)'
    match = re.search(iframe_pattern, index_content)
    if not match:
        if verbose:
            print(f'  SKIP {sim_name}: no iframe found in index.md')
        return None

    old_height = int(match.group(2))
    if old_height == height:
        if verbose:
            print(f'  OK   {sim_name}: {old_height}px (already correct, {reason})')
        return None

    if not dry_run:
        new_iframe = f'{match.group(1)}height="{height}"{match.group(3)}'
        new_content = (
            index_content[: match.start()] + new_iframe + index_content[match.end() :]
        )
        with open(index_path, 'w') as f:
            f.write(new_content)

    label = 'WOULD FIX' if dry_run else 'FIXED'
    print(f'  {label} {sim_name}: {old_height} → {height}  ({reason})')
    return (old_height, height)


def main():
    parser = argparse.ArgumentParser(
        description='Fix iframe heights in MicroSim index.md files to match JS dimensions.'
    )
    parser.add_argument(
        '--project-dir',
        default=None,
        help='Project root (auto-detect from cwd if omitted)',
    )
    parser.add_argument(
        '--sim', default=None, help='Fix a single sim by name (default: all sims)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show changes without writing files',
    )
    parser.add_argument('--verbose', action='store_true', help='Show all sims, not just changes')
    args = parser.parse_args()

    # Resolve project dir
    if args.project_dir:
        project_dir = os.path.abspath(args.project_dir)
    else:
        d = os.path.abspath('.')
        while d != os.path.dirname(d):
            if os.path.isfile(os.path.join(d, 'mkdocs.yml')):
                project_dir = d
                break
            d = os.path.dirname(d)
        else:
            print('ERROR: mkdocs.yml not found. Use --project-dir.', file=sys.stderr)
            sys.exit(1)

    sims_dir = os.path.join(project_dir, 'docs', 'sims')
    if not os.path.isdir(sims_dir):
        print(f'ERROR: {sims_dir} not found.', file=sys.stderr)
        sys.exit(1)

    if args.sim:
        sim_dirs = [os.path.join(sims_dir, args.sim)]
        if not os.path.isdir(sim_dirs[0]):
            print(f'ERROR: sim directory {sim_dirs[0]} not found.', file=sys.stderr)
            sys.exit(1)
    else:
        sim_dirs = sorted(glob.glob(os.path.join(sims_dir, '*/')))

    changes = 0
    for sim_dir in sim_dirs:
        sim_name = os.path.basename(sim_dir.rstrip('/'))
        result = fix_sim_height(sim_dir, sim_name, dry_run=args.dry_run, verbose=args.verbose)
        if result is not None:
            changes += 1

    action = 'Would update' if args.dry_run else 'Updated'
    print(f'\n{action} {changes} iframe height{"s" if changes != 1 else ""}')


if __name__ == '__main__':
    main()

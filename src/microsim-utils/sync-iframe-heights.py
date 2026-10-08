#!/usr/bin/env python3
"""Synchronize MicroSim iframe heights from a single per-sim CANVAS_HEIGHT.

CANVAS_HEIGHT is resolved for each sim from the first source that has it, in
priority order (see references/canvas-height-strategy.md for the full rationale):

  1. `// CANVAS_HEIGHT: <n>`      comment in the first ~15 lines of <sim-id>.js
                                  (p5.js and any JS-driven sim — primary)
  2. `"canvasHeight": <n>`        in <sim-id>/metadata.json
                                  (the consistent, structured place for sims that
                                   have NO .js: Mermaid, vis-network, Chart.js,
                                   Leaflet, vis-timeline, Plotly, custom HTML)
  3. `<!-- CANVAS_HEIGHT: <n> -->` comment in main.html
                                  (back-compat: some projects store it here)
  4. computed drawHeight + controlHeight (+ graphHeight) from <sim-id>.js
                                  (last-resort fallback; the // comment is then
                                   inserted on line 2 of the .js so it is cached)

Every iframe that shows the sim is then set to  CANVAS_HEIGHT + 2  (2px border):
  * the sim's own      docs/sims/<id>/index.md      (src="main.html" / "./main.html")
  * every page that embeds it, anywhere under docs/  (src=".../sims/<id>/main.html")

The embed scan walks EVERY markdown file under docs/ and matches iframes by the
`sims/<id>/main.html` path, so it is layout-agnostic:

  * standard layout   docs/chapters/<chapter>/index.md          (used by ~all books)
  * nested layout     docs/bands/<band>/chapters/<chapter>/...  (unique to the
                      health-education textbook — no other book nests this way)
  * teacher guides, poster pages, or any other embedder — all handled uniformly.

Usage:
  python3 sync-iframe-heights.py --project-dir /path/to/project --verbose
  python3 sync-iframe-heights.py --project-dir /path/to/project --sim gradient-explorer
  python3 sync-iframe-heights.py --project-dir /path/to/project --dry-run --verbose
  python3 sync-iframe-heights.py --project-dir /path/to/project --write-metadata
"""

import argparse
import glob
import json
import os
import re
import sys

# ── ANSI helpers ─────────────────────────────────────────────────────
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
CHECK = "✔"
ARROW = "→"

# metadata.json field that stores CANVAS_HEIGHT (the content height, before the
# +2 border). Keep this name stable — downstream agents/tools read it.
METADATA_HEIGHT_KEY = "canvasHeight"


# ── Height detection ─────────────────────────────────────────────────

def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def height_from_js_comment(js_content):
    """`// CANVAS_HEIGHT: <int>` in the first 15 lines. None if absent."""
    for line in js_content.splitlines()[:15]:
        m = re.match(r'^\s*//\s*CANVAS_HEIGHT\s*[:=]\s*(\d+)', line)
        if m:
            return int(m.group(1))
    return None


def height_from_metadata(meta_path):
    """`"canvasHeight": <int>` in metadata.json. None if absent/unparsable."""
    if not os.path.isfile(meta_path):
        return None
    try:
        data = json.loads(_read(meta_path))
    except (ValueError, OSError):
        return None
    val = data.get(METADATA_HEIGHT_KEY)
    if isinstance(val, bool):          # guard: JSON true/false is an int in Python
        return None
    if isinstance(val, int):
        return val
    if isinstance(val, str) and val.strip().isdigit():
        return int(val.strip())
    return None


def height_from_html_comment(html_content):
    """`<!-- CANVAS_HEIGHT: <int> -->` in main.html. None if absent."""
    m = re.search(r'<!--\s*CANVAS_HEIGHT\s*[:=]\s*(\d+)\s*-->',
                  html_content, re.IGNORECASE)
    return int(m.group(1)) if m else None


def compute_from_js_vars(js_content):
    """Compute CANVAS_HEIGHT from named height variables in the JS.

    drawHeight + controlHeight (+ graphHeight if present), or a direct
    canvasHeight/createCanvas() height. Returns (height, explanation) or
    (None, reason).
    """
    draw_h = _extract_var(js_content, r'(?:drawHeight|drawingHeight|draw_height)')
    ctrl_h = _extract_var(js_content,
                          r'(?:controlHeight|controlAreaHeight|control_height)')
    graph_h = _extract_var(js_content, r'(?:graphHeight|graph_height)')

    if draw_h is not None and ctrl_h is not None:
        total = draw_h + ctrl_h + (graph_h or 0)
        parts = f"drawHeight({draw_h})+controlHeight({ctrl_h})"
        if graph_h:
            parts += f"+graphHeight({graph_h})"
        return total, parts

    canvas_h = _extract_var(js_content,
                            r'(?:canvasHeight|canvas_height|containerHeight)')
    if canvas_h is not None:
        return canvas_h, f"canvasHeight({canvas_h})"

    m = re.search(r'createCanvas\s*\(\s*\w+\s*,\s*(\d+)\s*\)', js_content)
    if m:
        return int(m.group(1)), f"createCanvas height({m.group(1)})"

    return None, "no height variables"


def _extract_var(js_content, pattern):
    m = re.search(rf'(?:let|const|var)\s+{pattern}\s*=\s*(\d+)', js_content)
    return int(m.group(1)) if m else None


def resolve_canvas_height(sim_dir, sim_id, dry_run, write_metadata):
    """Resolve CANVAS_HEIGHT for one sim via the 4-tier priority chain.

    May insert the `// CANVAS_HEIGHT` comment into the .js when the height had
    to be computed. When write_metadata is set, backfills metadata.json's
    canvasHeight for any sim whose metadata is missing it.

    Returns (height, source_label) or (None, reason).
    """
    js_path = os.path.join(sim_dir, f"{sim_id}.js")
    html_path = os.path.join(sim_dir, "main.html")
    meta_path = os.path.join(sim_dir, "metadata.json")

    js_content = _read(js_path) if os.path.isfile(js_path) else None
    height, source = None, None

    # 1. // CANVAS_HEIGHT in the .js (primary for JS-driven sims)
    if js_content is not None:
        height = height_from_js_comment(js_content)
        if height is not None:
            source = "js-comment"

    # 2. metadata.json canvasHeight (consistent place for no-.js sims)
    if height is None:
        height = height_from_metadata(meta_path)
        if height is not None:
            source = "metadata.json"

    # 3. <!-- CANVAS_HEIGHT --> in main.html (back-compat)
    if height is None and os.path.isfile(html_path):
        height = height_from_html_comment(_read(html_path))
        if height is not None:
            source = "html-comment"

    # 4. compute from JS height variables (and cache the comment)
    if height is None and js_content is not None:
        height, explanation = compute_from_js_vars(js_content)
        if height is not None:
            source = f"computed:{explanation}"
            insert_canvas_comment(js_path, js_content, height, dry_run)

    if height is None:
        return None, "no CANVAS_HEIGHT (no .js comment, metadata, html comment, or vars)"

    # Optionally backfill the structured metadata field so downstream agents
    # can rely on metadata.json regardless of library type.
    if write_metadata and height_from_metadata(meta_path) != height:
        write_metadata_height(meta_path, height, dry_run)

    return height, source


def insert_canvas_comment(js_path, js_content, height, dry_run):
    """Insert/refresh `// CANVAS_HEIGHT: <height>` on line 2 of the .js."""
    lines = js_content.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    comment = f"// CANVAS_HEIGHT: {height}\n"
    if len(lines) > 1 and re.match(r'^\s*//\s*CANVAS_HEIGHT', lines[1]):
        if lines[1].strip() == comment.strip():
            return
        lines[1] = comment
    else:
        lines.insert(1, comment)
    if not dry_run:
        with open(js_path, "w", encoding="utf-8") as f:
            f.writelines(lines)


def write_metadata_height(meta_path, height, dry_run):
    """Set metadata.json's canvasHeight, preserving key order and formatting."""
    if not os.path.isfile(meta_path):
        return
    try:
        data = json.loads(_read(meta_path))
    except (ValueError, OSError):
        return
    data[METADATA_HEIGHT_KEY] = height
    if not dry_run:
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")


# ── Iframe updating ──────────────────────────────────────────────────

# capture: (prefix up to & incl. height=") (number) (optional px) (rest of tag)
IFRAME_RE = re.compile(
    r'(<iframe\b[^>]*?height\s*=\s*["\']?)(\d+)(px)?(["\']?[^>]*>)',
    re.IGNORECASE,
)
SRC_RE = re.compile(r'src\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)


def sim_id_for_iframe(md_path, iframe_tag):
    """Which sim id does this iframe point at? None if it is not a sim embed
    (e.g. a poster, the learning-graph viewer, or an unrelated iframe)."""
    s = SRC_RE.search(iframe_tag)
    src = s.group(1) if s else ""
    m = re.search(r'sims/([^/"\']+)/main\.html', src)
    if m:
        return m.group(1)
    # a sim's own index.md uses a bare src="main.html" / "./main.html"
    if src.split("?")[0].lstrip("./") == "main.html":
        parent = os.path.dirname(md_path)
        if os.path.basename(os.path.dirname(parent)) == "sims":
            return os.path.basename(parent)
    return None


def update_iframes_in_file(md_path, heights, dry_run):
    """Rewrite every sim iframe in one markdown file to CANVAS_HEIGHT + 2.

    heights: {sim_id: canvas_height}. Returns list of (sim_id, old, new)."""
    content = _read(md_path)
    changes = []

    def repl(m):
        sim = sim_id_for_iframe(md_path, m.group(0))
        if sim is None or sim not in heights:
            return m.group(0)
        target = heights[sim] + 2
        old = int(m.group(2))
        if old == target:
            return m.group(0)
        changes.append((sim, old, target))
        return f"{m.group(1)}{target}px{m.group(4)}"

    new_content = IFRAME_RE.sub(repl, content)
    if changes and not dry_run:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(new_content)
    return changes


# ── Main logic ───────────────────────────────────────────────────────

def build_height_map(sims_dir, only_sim, dry_run, write_metadata, verbose):
    """Resolve CANVAS_HEIGHT for every sim (or just --sim). Returns
    ({sim_id: height}, [(sim_id, reason)] unresolved, stats)."""
    heights, unresolved = {}, []
    stats = {"js-comment": 0, "metadata.json": 0, "html-comment": 0,
             "computed": 0, "metadata_written": 0}

    if only_sim:
        sim_dirs = [os.path.join(sims_dir, only_sim)]
    else:
        sim_dirs = sorted(
            d for d in glob.glob(os.path.join(sims_dir, "*/"))
            if os.path.basename(d.rstrip("/")) not in ("TODO", "shared-libs")
        )

    for sim_dir in sim_dirs:
        sim_id = os.path.basename(sim_dir.rstrip("/"))
        meta_before = height_from_metadata(os.path.join(sim_dir, "metadata.json"))
        height, source = resolve_canvas_height(
            sim_dir, sim_id, dry_run, write_metadata
        )
        if height is None:
            unresolved.append((sim_id, source))
            continue
        heights[sim_id] = height
        key = "computed" if source.startswith("computed") else source
        stats[key] = stats.get(key, 0) + 1
        if write_metadata and meta_before != height:
            stats["metadata_written"] += 1
        if verbose:
            print(f"  {DIM}{sim_id}: CANVAS_HEIGHT={height} "
                  f"(iframe={height + 2}) [{source}]{RESET}")

    return heights, unresolved, stats


def find_project_root(project_dir):
    if project_dir:
        return os.path.abspath(project_dir)
    d = os.path.abspath(".")
    while d != os.path.dirname(d):
        if os.path.isfile(os.path.join(d, "mkdocs.yml")):
            return d
        d = os.path.dirname(d)
    print("ERROR: mkdocs.yml not found. Use --project-dir.", file=sys.stderr)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser(
        description="Synchronize iframe heights from each sim's CANVAS_HEIGHT "
                    "(js comment / metadata.json / html comment / computed) to "
                    "its own index.md and every page that embeds it."
    )
    ap.add_argument("--project-dir", default=None,
                    help="Project root containing mkdocs.yml (auto-detect if omitted)")
    ap.add_argument("--sim", default=None,
                    help="Sync a single sim by id (default: all sims)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Preview changes without writing files")
    ap.add_argument("--write-metadata", action="store_true",
                    help="Backfill each sim's metadata.json canvasHeight field "
                         "(off by default; use to migrate no-.js sims to the "
                         "structured store)")
    ap.add_argument("--verbose", action="store_true",
                    help="Show the resolved height/source for every sim")
    args = ap.parse_args()

    project_dir = find_project_root(args.project_dir)
    sims_dir = os.path.join(project_dir, "docs", "sims")
    docs_dir = os.path.join(project_dir, "docs")
    if not os.path.isdir(sims_dir):
        print(f"ERROR: {sims_dir} not found.", file=sys.stderr)
        sys.exit(1)
    if args.sim and not os.path.isdir(os.path.join(sims_dir, args.sim)):
        print(f"ERROR: sim directory for '{args.sim}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"{BOLD}Project root:{RESET} {project_dir}")

    heights, unresolved, stats = build_height_map(
        sims_dir, args.sim, args.dry_run, args.write_metadata, args.verbose
    )
    print(f"Resolved CANVAS_HEIGHT for {GREEN}{len(heights)}{RESET} sims "
          f"({stats['js-comment']} js-comment, {stats['metadata.json']} metadata, "
          f"{stats['html-comment']} html-comment, {stats['computed']} computed).")
    if unresolved and args.verbose:
        print(f"{YELLOW}Unresolved (skipped — not sims or no height):{RESET}")
        for sid, reason in unresolved:
            print(f"  {DIM}{sid}: {reason}{RESET}")

    # Walk every markdown file under docs/ once; update sim iframes in place.
    own_changes, embed_changes = 0, 0
    for md in sorted(glob.glob(os.path.join(docs_dir, "**", "*.md"), recursive=True)):
        # A glob for "*.md" also matches DIRECTORIES whose name ends in .md.
        # At least one book has docs/archetypes/shifting-the-burden/er-overuse.md
        # as a directory, which made this script die with IsADirectoryError
        # after it had already resolved every height.
        if not os.path.isfile(md):
            continue
        changes = update_iframes_in_file(md, heights, args.dry_run)
        if not changes:
            continue
        rel = os.path.relpath(md, project_dir)
        is_own = rel.startswith(os.path.join("docs", "sims") + os.sep)
        label = "WOULD FIX" if args.dry_run else "FIXED"
        color = CYAN if is_own else GREEN
        for sim, old, new in changes:
            print(f"  {color}{label}{RESET} {rel}: {old} {ARROW} {new}  [{sim}]")
            if is_own:
                own_changes += 1
            else:
                embed_changes += 1

    print()
    verb = "Would update" if args.dry_run else "Updated"
    print(f"{GREEN}{CHECK}{RESET} {verb} {own_changes} own-index + "
          f"{embed_changes} embed iframe(s) = {own_changes + embed_changes} total")
    if stats["metadata_written"]:
        verb2 = "Would write" if args.dry_run else "Wrote"
        print(f"  {verb2} canvasHeight into {stats['metadata_written']} metadata.json file(s)")


if __name__ == "__main__":
    main()

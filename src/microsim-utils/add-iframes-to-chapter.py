#!/usr/bin/env python3
"""
add-iframes-to-chapter.py — Insert missing iframes into chapter markdown.

Finds spec entries (``#### Diagram:``, ``#### Drawing:``, ``#### MicroSim:``,
``#### Timeline:`` and the other ``shared.SPEC_HEADING_TYPES``) that are
missing iframe embeds and inserts them before the ``<details>`` block.  Also
provides ``--fix-heights`` and ``--fix-paths`` options for normalizing
existing iframes.

Usage:
    python3 add-iframes-to-chapter.py --chapter DIR [--all]
        [--project-dir PATH] [--dry-run] [--fix-heights] [--fix-paths]
        [--verbose]
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import (
    find_project_root, kebab_case, SPEC_HEADING_RE, DETAILS_OPEN_RE,
    spec_region_end,
    GREEN, RED, YELLOW, CYAN, BOLD, DIM, RESET, CHECK, CROSS, WARN, ARROW,
)


# Same spec headings extract-sim-specs.py recognizes (group 2 is the title).
HEADING_RE = SPEC_HEADING_RE

# Reused MicroSims (Status: Reused) embed absolute https:// srcs pointing at
# another book's deployed sim. IFRAME_RE must keep matching those so no local
# iframe gets inserted, and ABS_PATH_RE must keep matching ONLY srcs that start
# with "/sims/" so --fix-paths never rewrites an absolute https URL.
IFRAME_RE = re.compile(
    r'<iframe\s[^>]*src=["\']([^"\']+/sims/([^/"\']+)/main\.html)["\']',
    re.IGNORECASE,
)

# How far past a spec heading to look for its iframe and details block.
# The region also ends at the next heading; see shared.spec_region_end.
LOOKAHEAD_LINES = 40

# Fix "500xp" typo pattern
HEIGHT_TYPO_RE = re.compile(r'height=["\'](\d+)xp["\']', re.IGNORECASE)

# Absolute path pattern: /sims/ instead of ../../sims/
ABS_PATH_RE = re.compile(r'src=["\'](/sims/([^/"\']+)/main\.html)["\']', re.IGNORECASE)


def _infer_sim_id(title, details_text=""):
    """Infer sim_id from title or details block content."""
    # Check for explicit "Directory name:" field
    # Capture only id-safe characters so trailing markup like <br/> is excluded
    m = re.search(r"Directory name:\s*([A-Za-z0-9_-]+)", details_text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Check for sim-id field
    m = re.search(r"\*\*sim-id:\*\*\s*([A-Za-z0-9_-]+)", details_text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return kebab_case(title)


def _read_canvas_height(sim_dir):
    """Parse JS files in a sim directory to find canvas height."""
    if not os.path.isdir(sim_dir):
        return None
    for fname in os.listdir(sim_dir):
        if not fname.endswith(".js"):
            continue
        path = os.path.join(sim_dir, fname)
        with open(path, encoding="utf-8", errors="ignore") as f:
            content = f.read()
        # Look for createCanvas(w, h) pattern
        m = re.search(r"createCanvas\(\s*\w+\s*,\s*(\d+)\s*\)", content)
        if m:
            return int(m.group(1))
        # Look for canvasHeight = N pattern
        m = re.search(r"(?:canvasHeight|height)\s*=\s*(\d+)", content)
        if m:
            return int(m.group(1))
    return None


def process_chapter(chapter_path, project_dir, dry_run=False,
                    fix_heights=False, fix_paths=False, verbose=False):
    """Process a single chapter file. Returns (changes_made, report)."""
    with open(chapter_path, encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    changes = []
    new_lines = list(lines)  # work on a copy
    offset = 0  # track line insertions

    sims_dir = os.path.join(project_dir, "docs", "sims")

    # Pass 1: Fix typos and paths throughout the file
    if fix_heights or fix_paths:
        for i in range(len(new_lines)):
            line = new_lines[i]
            original = line

            if fix_heights:
                # Fix "500xp" → "500px"
                line = HEIGHT_TYPO_RE.sub(lambda m: f'height="{m.group(1)}px"', line)

            if fix_paths:
                # Fix absolute /sims/ → relative ../../sims/
                line = ABS_PATH_RE.sub(
                    lambda m: f'src="../../sims/{m.group(2)}/main.html"', line
                )

            if line != original:
                new_lines[i] = line
                changes.append(f"Fixed line {i+1}: typo/path correction")

    # Pass 2: Find headings missing iframes and insert them
    i = 0
    while i < len(new_lines):
        m = HEADING_RE.match(new_lines[i].strip())
        if not m:
            i += 1
            continue

        heading_line = i
        title = m.group(2).strip()

        # Search this spec's own region for its iframe and details block:
        # up to the next heading, so the next spec's iframe is not mistaken
        # for this one's and the next spec's details block is not claimed.
        search_end = spec_region_end(new_lines, i, LOOKAHEAD_LINES)
        has_iframe = False
        details_line = None
        details_text = ""

        for j in range(i + 1, search_end):
            if IFRAME_RE.search(new_lines[j]):
                has_iframe = True
            if DETAILS_OPEN_RE.search(new_lines[j]):
                details_line = j
                # Grab details block text for sim_id inference
                depth = 0
                block = []
                for k in range(j, min(j + 50, len(new_lines))):
                    block.append(new_lines[k])
                    if DETAILS_OPEN_RE.search(new_lines[k]):
                        depth += 1
                    if re.search(r"</details>", new_lines[k], re.IGNORECASE):
                        depth -= 1
                        if depth <= 0:
                            break
                details_text = "\n".join(block)
                break

        if not has_iframe and details_line is not None:
            sim_id = _infer_sim_id(title, details_text)
            sim_path = os.path.join(sims_dir, sim_id)

            # Determine height
            height = "450px"
            if fix_heights:
                canvas_h = _read_canvas_height(sim_path)
                if canvas_h:
                    height = f"{canvas_h + 2}px"

            iframe_line = (
                f'<iframe src="../../sims/{sim_id}/main.html" '
                f'width="100%" height="{height}" scrolling="no"></iframe>'
            )
            fullscreen_line = (
                f'[Run {title} Fullscreen](../../sims/{sim_id}/main.html)'
            )

            # Insert iframe + fullscreen link before the details block
            insert_at = details_line
            insert_lines = ["", iframe_line, fullscreen_line, ""]
            for idx, il in enumerate(insert_lines):
                new_lines.insert(insert_at + idx, il)
            offset += len(insert_lines)
            changes.append(f"Inserted iframe for '{sim_id}' before details at line {details_line + 1}")

            if verbose:
                print(f"  {GREEN}{CHECK}{RESET} Inserted iframe: {sim_id}")

        # Fix height if iframe exists and --fix-heights
        if has_iframe and fix_heights:
            for j in range(i + 1, search_end):
                im = IFRAME_RE.search(new_lines[j])
                if im:
                    sim_id_found = im.group(2)
                    sim_path = os.path.join(sims_dir, sim_id_found)
                    canvas_h = _read_canvas_height(sim_path)
                    if canvas_h:
                        correct_h = f"{canvas_h + 2}px"
                        new_lines[j] = re.sub(
                            r'height=["\'][^"\']*["\']',
                            f'height="{correct_h}"',
                            new_lines[j],
                        )
                        changes.append(f"Updated height for {sim_id_found} to {correct_h}")
                    break

        i += 1

    if not changes:
        if verbose:
            print(f"  {DIM}No changes needed{RESET}")
        return 0, []

    new_content = "\n".join(new_lines) + "\n"

    if dry_run:
        for c in changes:
            print(f"  {DIM}[dry-run]{RESET} {c}")
        return len(changes), changes

    with open(chapter_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return len(changes), changes


def main():
    parser = argparse.ArgumentParser(
        description="Insert missing iframes into chapter markdown."
    )
    parser.add_argument("--chapter", default=None,
                        help="Single chapter directory name to process")
    parser.add_argument("--all", action="store_true",
                        help="Process all chapters")
    parser.add_argument("--project-dir", default=None,
                        help="Project root (auto-detect if omitted)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show changes without writing")
    parser.add_argument("--fix-heights", action="store_true",
                        help="Parse JS files and update iframe heights")
    parser.add_argument("--fix-paths", action="store_true",
                        help="Normalize absolute paths to relative")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if not args.chapter and not args.all:
        parser.error("Specify --chapter DIR or --all")

    project_dir = args.project_dir or find_project_root()
    chapters_dir = os.path.join(project_dir, "docs", "chapters")

    if args.verbose:
        print(f"{BOLD}Project root:{RESET} {project_dir}")

    if args.all:
        chapter_dirs = sorted([
            d for d in os.listdir(chapters_dir)
            if os.path.isfile(os.path.join(chapters_dir, d, "index.md"))
        ])
    else:
        chapter_dirs = [args.chapter]

    total_changes = 0
    for ch in chapter_dirs:
        index_path = os.path.join(chapters_dir, ch, "index.md")
        if not os.path.isfile(index_path):
            print(f"{RED}{CROSS} {ch}/index.md not found{RESET}")
            continue

        if verbose := args.verbose:
            print(f"\n{CYAN}{BOLD}{ch}{RESET}")

        n, _ = process_chapter(
            index_path, project_dir,
            dry_run=args.dry_run,
            fix_heights=args.fix_heights,
            fix_paths=args.fix_paths,
            verbose=args.verbose,
        )
        total_changes += n

    mode = "[dry-run] " if args.dry_run else ""
    print(f"\n{GREEN}{CHECK} {mode}Total changes: {total_changes} across {len(chapter_dirs)} chapter(s){RESET}")


if __name__ == "__main__":
    main()

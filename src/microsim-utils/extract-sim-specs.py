#!/usr/bin/env python3
"""
extract-sim-specs.py — Extract MicroSim specifications from chapter markdown.

Parses spec headers from chapter markdown files — ``#### Diagram:``,
``#### Drawing:``, ``#### MicroSim:``, ``#### Timeline:``, ``#### Chart:``,
``#### Infographic:``, ``#### Workflow:`` and ``#### Map:`` (the list lives in
``shared.SPEC_HEADING_TYPES``) — and extracts ``<details>`` block content,
iframe paths, sim IDs, and structured fields.  Optionally generates a
sim-status.json lifecycle file.

Usage:
    python3 extract-sim-specs.py [--project-dir PATH] [--chapter DIR]
                                 [--output FILE] [--status-file FILE]
                                 [--verbose]
"""

import argparse
import json
import os
import re
import sys

# Allow running from any directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import (
    find_project_root, kebab_case, detect_library, parse_yaml_frontmatter,
    SPEC_HEADING_RE,
    GREEN, RED, YELLOW, CYAN, BOLD, DIM, RESET, CHECK, CROSS, WARN, ARROW,
)


# ── Regex patterns ────────────────────────────────────────────────────

# Spec headings (Diagram, Drawing, MicroSim, Timeline, ...) are shared with
# add-iframes-to-chapter.py; see SPEC_HEADING_TYPES in shared.py.
HEADING_RE = SPEC_HEADING_RE

IFRAME_RE = re.compile(
    r'<iframe\s[^>]*src=["\']([^"\']+/sims/([^/"\']+)/main\.html)["\']'
    r'[^>]*(?:height=["\']([^"\']*)["\'])?[^>]*>',
    re.IGNORECASE,
)

# Also match iframe where height comes before src
IFRAME_HEIGHT_RE = re.compile(
    r'<iframe\s[^>]*height=["\']([^"\']*)["\'][^>]*src=["\']([^"\']+/sims/([^/"\']+)/main\.html)["\']',
    re.IGNORECASE,
)

DETAILS_OPEN_RE  = re.compile(r"<details\s+markdown=[\"']1[\"']\s*>", re.IGNORECASE)
DETAILS_CLOSE_RE = re.compile(r"</details>", re.IGNORECASE)
SUMMARY_RE       = re.compile(r"<summary>(.*?)</summary>", re.IGNORECASE | re.DOTALL)

# Structured fields inside details blocks
FIELD_RES = {
    "type":        re.compile(r"^Type:\s*(.+)$",        re.MULTILINE | re.IGNORECASE),
    "status":      re.compile(r"\*\*Status:\*\*\s*(.+?)(?:<br|$|\n)", re.IGNORECASE),
    # "**Bloom Level:** Analyze<br/>" (chapter-content-generator v1.11+), "Bloom Taxonomy Level: ...",
    # and the inline "(Bloom level: Analyze; verb: ...)" form; the value stops before <br/>, ";" or ")".
    "bloom_level": re.compile(r"Bloom(?:'s)?(?:\s+Taxonomy)?\s+Level:\*?\*?\s*(.+?)(?:\s*<br|\s*[-–—;)(]|$|\n)", re.IGNORECASE),
    "library":     re.compile(r"\*\*Library:\*\*\s*(.+?)(?:<br|$|\n)", re.IGNORECASE),
    "sim_id":      re.compile(r"\*\*sim-id:\*\*\s*(.+?)(?:<br|$|\n)", re.IGNORECASE),
}


def _extract_iframe_info(text):
    """Return (src_path, sim_id, height) from an iframe tag, or (None, None, None)."""
    # Try src-first pattern
    m = IFRAME_RE.search(text)
    if m:
        return m.group(1), m.group(2), m.group(3) or ""
    # Try height-first pattern
    m = IFRAME_HEIGHT_RE.search(text)
    if m:
        return m.group(2), m.group(3), m.group(1) or ""
    return None, None, None


def _extract_details_block(lines, start_idx):
    """Starting from *start_idx*, find the matching ``<details>`` …
    ``</details>`` pair and return the full text (including tags) and
    the index of the line after ``</details>``.
    """
    depth = 0
    block_lines = []
    i = start_idx
    while i < len(lines):
        line = lines[i]
        block_lines.append(line)
        if DETAILS_OPEN_RE.search(line):
            depth += 1
        if DETAILS_CLOSE_RE.search(line):
            depth -= 1
            if depth <= 0:
                return "\n".join(block_lines), i + 1
        i += 1
    # Unclosed details
    return "\n".join(block_lines), i


def _parse_structured_fields(details_text):
    """Extract known structured fields from a details block."""
    fields = {}
    for key, pattern in FIELD_RES.items():
        m = pattern.search(details_text)
        if m:
            fields[key] = m.group(1).strip().strip("*").strip()
    return fields


def _infer_bloom_from_text(text):
    """Best-effort Bloom level inference from learning objective text."""
    lower = text.lower()
    bloom_keywords = [
        ("create",    "Create"),
        ("design",    "Create"),
        ("evaluate",  "Evaluate"),
        ("judge",     "Evaluate"),
        ("analyze",   "Analyze"),
        ("compare",   "Analyze"),
        ("apply",     "Apply"),
        ("calculate", "Apply"),
        ("solve",     "Apply"),
        ("demonstrate", "Apply"),
        ("understand", "Understand"),
        ("explain",   "Understand"),
        ("describe",  "Understand"),
        ("classify",  "Understand"),
        ("identify",  "Remember"),
        ("recall",    "Remember"),
        ("list",      "Remember"),
        ("name",      "Remember"),
        ("remember",  "Remember"),
    ]
    for kw, level in bloom_keywords:
        if kw in lower:
            return level
    return ""


def extract_specs_from_chapter(chapter_path, chapter_dir_name, verbose=False):
    """Parse a single chapter file and return a list of spec dicts."""
    with open(chapter_path, encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    specs = []

    # Find all spec headings (#### Diagram: / #### MicroSim: / #### Timeline: ...)
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line.strip())
        if not m:
            continue

        heading_type = m.group(1)   # one of shared.SPEC_HEADING_TYPES
        title = m.group(2).strip()

        # Search ahead (up to 40 lines) for iframe and details block
        search_start = i + 1
        search_end = min(i + 60, len(lines))
        search_region = "\n".join(lines[search_start:search_end])

        # Find iframe
        iframe_src, iframe_sim_id, iframe_height = _extract_iframe_info(search_region)

        # Find details block
        details_text = ""
        details_start = None
        for j in range(search_start, search_end):
            if DETAILS_OPEN_RE.search(lines[j]):
                details_start = j
                break

        if details_start is not None:
            details_text, _ = _extract_details_block(lines, details_start)

        # Extract summary text
        summary = ""
        sm = SUMMARY_RE.search(details_text)
        if sm:
            summary = sm.group(1).strip()

        # Extract structured fields
        fields = _parse_structured_fields(details_text)

        # Determine sim_id: explicit field > iframe-derived > kebab-case title
        sim_id = fields.get("sim_id") or iframe_sim_id or kebab_case(title)

        # Determine library from explicit field or details text hints
        library = fields.get("library", "")
        if not library:
            impl_match = re.search(r"Implementation:?\s*(.+)", details_text, re.IGNORECASE)
            if impl_match:
                impl_text = impl_match.group(1).lower()
                if "p5" in impl_text or "p5.js" in impl_text:
                    library = "p5.js"
                elif "vis-network" in impl_text:
                    library = "vis-network"
                elif "chart.js" in impl_text or "chartjs" in impl_text:
                    library = "Chart.js"
                elif "mermaid" in impl_text:
                    library = "Mermaid"
                elif "plotly" in impl_text:
                    library = "Plotly"
                elif "leaflet" in impl_text:
                    library = "Leaflet"
                elif "vis-timeline" in impl_text:
                    library = "vis-timeline"
            if not library and ("microsim" in details_text.lower() or
                                "p5.js" in details_text.lower()):
                library = "p5.js"

        # Bloom level
        bloom = fields.get("bloom_level", "")
        if not bloom:
            bloom = _infer_bloom_from_text(details_text)

        # Status
        status = fields.get("status", "")

        # Element type
        elem_type = fields.get("type", "")

        spec = {
            "sim_id":       sim_id,
            "title":        title,
            "summary":      summary,
            "heading_type":  heading_type,  # Diagram, Drawing, MicroSim, ...
            "chapter":      chapter_dir_name,
            "element_type": elem_type,
            "bloom_level":  bloom,
            "library":      library,
            "iframe_src":   iframe_src or "",
            "iframe_height": iframe_height or "",
            "spec_text":    details_text,
            "status":       status,
        }
        specs.append(spec)

        if verbose:
            flag = f"{GREEN}{CHECK}{RESET}" if iframe_src else f"{YELLOW}{WARN}{RESET}"
            print(f"  {flag} {sim_id}  ({heading_type}: {title})")

    return specs


def scan_chapters(project_dir, chapter_filter=None, verbose=False):
    """Scan all chapter directories and extract specs."""
    chapters_dir = os.path.join(project_dir, "docs", "chapters")
    if not os.path.isdir(chapters_dir):
        print(f"{RED}{CROSS} docs/chapters/ not found in {project_dir}{RESET}")
        return []

    all_specs = []
    entries = sorted(os.listdir(chapters_dir))

    for name in entries:
        if chapter_filter and name != chapter_filter:
            continue
        index_path = os.path.join(chapters_dir, name, "index.md")
        if not os.path.isfile(index_path):
            continue

        if verbose:
            print(f"\n{CYAN}{BOLD}{name}{RESET}")

        specs = extract_specs_from_chapter(index_path, name, verbose=verbose)
        all_specs.extend(specs)

    return all_specs


def generate_status_file(specs, project_dir, output_path, verbose=False):
    """Generate sim-status.json by combining specs with filesystem state."""
    sims_dir = os.path.join(project_dir, "docs", "sims")

    status_entries = {}

    # Start with specs from chapters
    for spec in specs:
        sid = spec["sim_id"]
        entry = {
            "sim_id":       sid,
            "title":        spec["title"],
            "chapter":      spec["chapter"],
            "bloom_level":  spec["bloom_level"],
            "library":      spec["library"],
            "status":       "specified",
            "has_iframe":   bool(spec["iframe_src"]),
            "quality_score": None,
        }

        # Reused sims reference an existing MicroSim in another repo via an
        # absolute iframe URL. They have no local docs/sims/ directory, so
        # skip the filesystem checks and treat them as complete (terminal
        # state), not pending.
        if spec.get("status", "").strip().lower() == "reused":
            entry["status"] = "reused"
            status_entries[sid] = entry
            continue

        sim_path = os.path.join(sims_dir, sid)
        if os.path.isdir(sim_path):
            html_path = os.path.join(sim_path, "main.html")
            js_files = [f for f in os.listdir(sim_path) if f.endswith(".js")]
            index_md = os.path.join(sim_path, "index.md")

            if os.path.isfile(html_path):
                entry["status"] = "scaffolded"

                # Check if JS exists and is substantive (>50 lines)
                for jsf in js_files:
                    jspath = os.path.join(sim_path, jsf)
                    with open(jspath, encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    if len(lines) > 50:
                        entry["status"] = "implemented"
                        break

                # Detect actual library from main.html
                if not entry["library"]:
                    with open(html_path, encoding="utf-8", errors="ignore") as f:
                        entry["library"] = detect_library(f.read())

            # Check quality_score from index.md frontmatter
            if os.path.isfile(index_md):
                with open(index_md, encoding="utf-8", errors="ignore") as f:
                    fm, _ = parse_yaml_frontmatter(f.read())
                qs = fm.get("quality_score", "")
                if qs:
                    try:
                        score = int(qs)
                        entry["quality_score"] = score
                        if score >= 70 and entry["status"] == "implemented":
                            entry["status"] = "validated"
                    except ValueError:
                        pass

            # Check if deployed (validated + has iframe in chapter)
            if entry["status"] == "validated" and entry["has_iframe"]:
                entry["status"] = "deployed"

        status_entries[sid] = entry

    # Also scan sims_dir for sims not mentioned in any spec
    if os.path.isdir(sims_dir):
        for name in sorted(os.listdir(sims_dir)):
            sim_path = os.path.join(sims_dir, name)
            if not os.path.isdir(sim_path) or name in status_entries:
                continue
            if name.startswith(".") or name == "__pycache__":
                continue

            html_path = os.path.join(sim_path, "main.html")
            if not os.path.isfile(html_path):
                continue

            entry = {
                "sim_id":       name,
                "title":        name.replace("-", " ").title(),
                "chapter":      "",
                "bloom_level":  "",
                "library":      "",
                "status":       "scaffolded",
                "has_iframe":   False,
                "quality_score": None,
            }

            # Detect library
            with open(html_path, encoding="utf-8", errors="ignore") as f:
                entry["library"] = detect_library(f.read())

            # Check JS
            js_files = [f for f in os.listdir(sim_path) if f.endswith(".js")]
            for jsf in js_files:
                jspath = os.path.join(sim_path, jsf)
                with open(jspath, encoding="utf-8", errors="ignore") as f:
                    if len(f.readlines()) > 50:
                        entry["status"] = "implemented"
                        break

            # Check quality_score
            index_md = os.path.join(sim_path, "index.md")
            if os.path.isfile(index_md):
                with open(index_md, encoding="utf-8", errors="ignore") as f:
                    fm, _ = parse_yaml_frontmatter(f.read())
                qs = fm.get("quality_score", "")
                if qs:
                    try:
                        score = int(qs)
                        entry["quality_score"] = score
                        if score >= 70 and entry["status"] == "implemented":
                            entry["status"] = "validated"
                    except ValueError:
                        pass

            status_entries[name] = entry

    # Write output
    entries_list = sorted(status_entries.values(), key=lambda e: e["sim_id"])
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(entries_list, f, indent=2)

    # Summary
    counts = {}
    for e in entries_list:
        s = e["status"]
        counts[s] = counts.get(s, 0) + 1

    if verbose:
        print(f"\n{BOLD}sim-status.json summary:{RESET}")
        for s in ["specified", "scaffolded", "implemented", "validated", "deployed", "reused"]:
            c = counts.get(s, 0)
            if c:
                print(f"  {s:12s}  {c}")
        print(f"  {'total':12s}  {len(entries_list)}")

    return entries_list


def main():
    parser = argparse.ArgumentParser(
        description="Extract MicroSim specifications from chapter markdown."
    )
    parser.add_argument(
        "--project-dir", default=None,
        help="Project root (auto-detect if omitted)",
    )
    parser.add_argument(
        "--chapter", default=None,
        help="Single chapter directory name to process",
    )
    parser.add_argument(
        "--output", default=None,
        help="Write specs JSON to this file (default: stdout summary)",
    )
    parser.add_argument(
        "--status-file", default=None,
        help="Generate sim-status.json at this path",
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    project_dir = args.project_dir or find_project_root()

    if args.verbose:
        print(f"{BOLD}Project root:{RESET} {project_dir}")

    specs = scan_chapters(project_dir, chapter_filter=args.chapter, verbose=args.verbose)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(specs, f, indent=2)
        print(f"\n{GREEN}{CHECK} Wrote {len(specs)} specs to {args.output}{RESET}")
    else:
        print(f"\n{BOLD}Total specs found:{RESET} {len(specs)}")
        # Per-chapter summary
        chapters = {}
        for s in specs:
            ch = s["chapter"]
            chapters[ch] = chapters.get(ch, 0) + 1
        for ch in sorted(chapters):
            print(f"  {ch}: {chapters[ch]} specs")

    if args.status_file:
        entries = generate_status_file(specs, project_dir, args.status_file, verbose=args.verbose)
        print(f"{GREEN}{CHECK} Wrote {len(entries)} entries to {args.status_file}{RESET}")


if __name__ == "__main__":
    main()

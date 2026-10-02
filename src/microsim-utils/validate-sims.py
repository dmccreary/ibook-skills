#!/usr/bin/env python3
"""
validate-sims.py — Validate MicroSims against a 100-point quality rubric.

Checks required files, schema meta tag, frontmatter fields, JS quality,
and p5.js conventions.  Produces per-sim scores and aggregate summaries.

Scoring Rubric (100 points):
  main.html (10): file exists
  metadata.json (30): present (10) + valid fields (20)
  index.md structure (35): title (2) + YAML basic (3) + YAML images (5) +
                           iframe (10) + fullscreen (5) + iframe example (5) +
                           description (5)
  image (5): screenshot PNG exists
  lesson plan (10): Lesson Plan section present
  references (5): References section present
  p5.js conventions (5): updateCanvasSize, builtin controls (not manually
                         drawn), <main> parenting

Usage:
    python3 validate-sims.py [--project-dir PATH] [--sim NAME]
        [--min-score N] [--output FILE] [--format table|json] [--verbose]
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import (
    find_project_root, parse_yaml_frontmatter, detect_library,
    GREEN, RED, YELLOW, CYAN, BOLD, DIM, RESET, CHECK, CROSS, WARN, ARROW,
)


REQUIRED_METADATA_FIELDS = [
    "title", "description", "creator", "date", "subject",
]


def _check_main_html(sim_dir):
    """Check main.html: exists (5), has schema meta tag (3), has <main> tag (2)."""
    path = os.path.join(sim_dir, "main.html")
    if not os.path.isfile(path):
        return 0, ["main.html missing"]

    with open(path, encoding="utf-8", errors="ignore") as f:
        content = f.read()

    score = 5  # exists
    issues = []

    if 'name="schema"' in content and "intelligent-textbooks" in content:
        score += 3
    else:
        issues.append("main.html: missing schema meta tag")

    if "<main>" in content or "<main " in content:
        score += 2
    else:
        issues.append("main.html: missing <main> tag")

    return score, issues


def _check_metadata_json(sim_dir):
    """Check metadata.json: present (10), valid fields (20).

    Valid fields: required Dublin Core fields (10), educational section (5),
    pedagogical section (5). Accepts both the schema layout, where sections
    live under "microsim" and microsim.usage is the pedagogical section, and
    the legacy flat layout with top-level "educational" and "pedagogical".
    """
    path = os.path.join(sim_dir, "metadata.json")
    if not os.path.isfile(path):
        return 0, ["metadata.json missing"]

    score = 10  # present
    issues = []

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, ValueError):
        issues.append("metadata.json: invalid JSON")
        return score, issues

    # Check for required fields (at top level or nested)
    # Schema layout nests every section under "microsim"; legacy files are flat.
    nested = "microsim" in data
    if nested:
        sim = data["microsim"] if isinstance(data["microsim"], dict) else {}
        dc = sim.get("dublinCore") or {}
    else:
        sim = {}
        dc = data

    missing = [f for f in REQUIRED_METADATA_FIELDS if not dc.get(f)]
    if len(missing) <= 1:
        score += 10  # mostly complete
    elif len(missing) <= 3:
        score += 5

    # Check for educational section
    edu = data.get("educational") or dc.get("educational") or sim.get("educational")
    if edu:
        score += 5
    else:
        issues.append("metadata.json: missing educational section")

    # Check for pedagogical section. The schema has no "pedagogical" object;
    # its equivalent is microsim.usage (recommendedUsage, instructionalStrategies,
    # assessmentQuestions). Legacy flat files use a top-level "pedagogical".
    ped = (data.get("pedagogical") or dc.get("pedagogical")
           or sim.get("usage") or sim.get("pedagogical"))
    if ped:
        score += 5
    elif nested:
        issues.append("metadata.json: missing pedagogical section (microsim.usage)")
    else:
        issues.append("metadata.json: missing pedagogical section")

    if missing:
        issues.append(f"metadata.json: missing fields: {', '.join(missing)}")

    return score, issues


def _check_index_md(sim_dir):
    """Check index.md structure (35 points)."""
    path = os.path.join(sim_dir, "index.md")
    if not os.path.isfile(path):
        return 0, ["index.md missing"]

    with open(path, encoding="utf-8") as f:
        content = f.read()

    score = 0
    issues = []

    # Title (2)
    lines = content.splitlines()
    in_fm = False
    has_title = False
    for line in lines:
        if line.strip() == "---":
            in_fm = not in_fm
            continue
        if not in_fm and line.startswith("# "):
            has_title = True
            break
    if has_title:
        score += 2
    else:
        issues.append("index.md: missing # title header")

    # YAML basic: title + description (3)
    fm, _ = parse_yaml_frontmatter(content)
    if fm.get("title") and fm.get("description"):
        score += 3
    else:
        issues.append("index.md: missing title/description in frontmatter")

    # YAML images (5)
    fm_block = content.split("---")[1] if content.startswith("---") and content.count("---") >= 2 else ""
    if fm.get("image") or "og:image" in fm_block:
        score += 5
    else:
        issues.append("index.md: missing social preview images in frontmatter")

    # iframe embed (10)
    if re.search(r'<iframe[^>]*src=["\']main\.html["\']', content, re.IGNORECASE):
        score += 10
    else:
        issues.append("index.md: missing iframe with src='main.html'")

    # Fullscreen button (5)
    if re.search(r'\[.*(?:[Ff]ull\s*[Ss]creen|[Rr]un).*\]\(.*main\.html', content):
        score += 5
    else:
        issues.append("index.md: missing fullscreen link")

    # iframe example in code block (5)
    code_blocks = re.findall(r'```(?:html)?\s*\n(.*?)\n```', content, re.DOTALL)
    has_example = any("<iframe" in b.lower() and "main.html" in b for b in code_blocks)
    if has_example:
        score += 5
    else:
        issues.append("index.md: missing copy-paste iframe example")

    # Description/About section (5)
    if re.search(r'^##\s+(?:Description|About|Overview|How [Tt]o [Uu]se|Introduction)',
                 content, re.MULTILINE):
        score += 5
    else:
        issues.append("index.md: missing description/about section")

    return score, issues


def _check_image(sim_dir):
    """Check for screenshot PNG (5 points)."""
    for f in os.listdir(sim_dir):
        if f.endswith(".png") and f not in ("favicon.png", "icon.png"):
            return 5, []
    return 0, ["screenshot PNG missing"]


def _check_lesson_plan(sim_dir):
    """Check for Lesson Plan section (10 points)."""
    path = os.path.join(sim_dir, "index.md")
    if not os.path.isfile(path):
        return 0, ["index.md missing"]
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if re.search(r'^##\s+[Ll]esson\s*[Pp]lan', content, re.MULTILINE):
        return 10, []
    return 0, ["index.md: missing Lesson Plan section"]


def _check_references(sim_dir):
    """Check for References section (5 points)."""
    path = os.path.join(sim_dir, "index.md")
    if not os.path.isfile(path):
        return 0, ["index.md missing"]
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if re.search(r'^##\s+[Rr]eferences', content, re.MULTILINE):
        return 5, []
    return 0, ["index.md: missing References section"]


def _check_p5_conventions(sim_dir):
    """Check p5.js-specific conventions (5 points).

    Only applies to p5.js sims. Non-p5 sims get full marks.
    """
    html_path = os.path.join(sim_dir, "main.html")
    if not os.path.isfile(html_path):
        return 5, []  # Can't determine library, give benefit of doubt

    with open(html_path, encoding="utf-8", errors="ignore") as f:
        html = f.read()

    lib = detect_library(html)
    if lib != "p5.js":
        return 5, []  # Not p5.js, full marks

    # Find JS files
    js_content = ""
    for fname in os.listdir(sim_dir):
        if fname.endswith(".js"):
            with open(os.path.join(sim_dir, fname), encoding="utf-8", errors="ignore") as f:
                js_content += f.read() + "\n"

    if not js_content:
        return 0, ["p5.js: no JS file found"]

    score = 0
    issues = []

    # updateCanvasSize in setup (2 pts)
    if "updateCanvasSize" in js_content:
        score += 2
    else:
        issues.append("p5.js: missing updateCanvasSize() call")

    # Builtin controls, not manually drawn ones (2 pts).
    # Project standard: ALWAYS use p5.js builtin controls (createButton,
    # createSlider, etc.); never draw controls with rect() + mouse hit-testing.
    builtin_controls = re.findall(
        r"create(?:Button|Slider|Checkbox|Select|Input|Radio)\s*\(",
        js_content,
    )
    manual_hit_testing = (
        re.search(r"\bfunction\s+mouse(?:Pressed|Clicked|Released)\b", js_content)
        and re.search(r"\bmouseX\s*[<>]", js_content)
        and re.search(r"\bmouseY\s*[<>]", js_content)
    )
    if builtin_controls or not manual_hit_testing:
        score += 2
    else:
        issues.append(
            "p5.js: controls appear manually drawn (mouse hit-testing, no "
            "createButton/createSlider/etc.) — use builtin p5.js controls"
        )

    # Correct canvas parenting: document.querySelector('main') (1 pt)
    if "document.querySelector" in js_content and "'main'" in js_content:
        score += 1
    elif 'canvas.parent("main")' in js_content or "canvas.parent('main')" in js_content:
        issues.append("p5.js: uses string-based canvas.parent('main') instead of querySelector")
    else:
        issues.append("p5.js: missing canvas.parent(document.querySelector('main'))")

    return score, issues


def validate_sim(sim_dir, verbose=False):
    """Validate a single sim and return (total_score, category_scores, issues)."""
    categories = {
        "main_html":    _check_main_html(sim_dir),
        "metadata":     _check_metadata_json(sim_dir),
        "index_md":     _check_index_md(sim_dir),
        "image":        _check_image(sim_dir),
        "lesson_plan":  _check_lesson_plan(sim_dir),
        "references":   _check_references(sim_dir),
        "p5_conventions": _check_p5_conventions(sim_dir),
    }

    total = 0
    all_issues = []
    scores = {}
    for cat, (pts, iss) in categories.items():
        scores[cat] = pts
        total += pts
        all_issues.extend(iss)

    return total, scores, all_issues


def format_table(results, verbose=False):
    """Format results as a text table."""
    lines = []
    hdr = f"{'MicroSim':<40} {'Score':>5} {'Grade':>6}"
    lines.append(hdr)
    lines.append("-" * len(hdr))

    for r in results:
        name = r["sim_id"]
        score = r["score"]
        if score >= 85:
            grade = f"{GREEN}A{RESET}"
            indicator = f"{GREEN}{CHECK}{RESET}"
        elif score >= 70:
            grade = f"{CYAN}B{RESET}"
            indicator = f"{CYAN}{CHECK}{RESET}"
        elif score >= 50:
            grade = f"{YELLOW}C{RESET}"
            indicator = f"{YELLOW}{WARN}{RESET}"
        else:
            grade = f"{RED}D{RESET}"
            indicator = f"{RED}{CROSS}{RESET}"

        lines.append(f"{indicator} {name:<38} {score:>5} {grade:>6}")

        if verbose and r.get("issues"):
            for iss in r["issues"]:
                lines.append(f"      {DIM}{iss}{RESET}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate MicroSims against a 100-point quality rubric."
    )
    parser.add_argument("--project-dir", default=None,
                        help="Project root (auto-detect if omitted)")
    parser.add_argument("--sim", default=None,
                        help="Validate a single sim by name")
    parser.add_argument("--min-score", type=int, default=0,
                        help="Only show sims with score >= N")
    parser.add_argument("--output", default=None,
                        help="Write results to JSON file")
    parser.add_argument("--format", choices=["table", "json"], default="table",
                        help="Output format (default: table)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    project_dir = args.project_dir or find_project_root()
    sims_dir = os.path.join(project_dir, "docs", "sims")

    if not os.path.isdir(sims_dir):
        print(f"{RED}{CROSS} docs/sims/ not found in {project_dir}{RESET}")
        sys.exit(1)

    # Determine which sims to validate
    if args.sim:
        sim_dirs = [args.sim]
    else:
        sim_dirs = sorted([
            d for d in os.listdir(sims_dir)
            if os.path.isdir(os.path.join(sims_dir, d))
            and not d.startswith(".")
        ])

    results = []
    for name in sim_dirs:
        sim_path = os.path.join(sims_dir, name)
        if not os.path.isdir(sim_path):
            continue

        score, cat_scores, issues = validate_sim(sim_path, verbose=args.verbose)

        if score < args.min_score:
            continue

        results.append({
            "sim_id": name,
            "score": score,
            "categories": cat_scores,
            "issues": issues,
        })

    if args.output:
        # Strip ANSI for JSON output
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"{GREEN}{CHECK} Wrote {len(results)} results to {args.output}{RESET}")
        return

    if args.format == "json":
        print(json.dumps(results, indent=2))
        return

    # Table format
    print(format_table(results, verbose=args.verbose))

    # Aggregate summary
    if results:
        scores = [r["score"] for r in results]
        avg = sum(scores) / len(scores)
        high = sum(1 for s in scores if s >= 85)
        med = sum(1 for s in scores if 50 <= s < 85)
        low = sum(1 for s in scores if s < 50)

        print(f"\n{BOLD}Summary:{RESET}")
        print(f"  Validated: {len(results)}  Avg: {avg:.1f}")
        print(f"  {GREEN}A (85+): {high}{RESET}  "
              f"{CYAN}B (70-84): {sum(1 for s in scores if 70 <= s < 85)}{RESET}  "
              f"{YELLOW}C (50-69): {sum(1 for s in scores if 50 <= s < 70)}{RESET}  "
              f"{RED}D (<50): {low}{RESET}")


if __name__ == "__main__":
    main()

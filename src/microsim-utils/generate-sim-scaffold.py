#!/usr/bin/env python3
"""
generate-sim-scaffold.py — Generate MicroSim scaffold files from specs JSON.

Reads the specs JSON produced by extract-sim-specs.py and generates
``main.html``, ``index.md``, and ``metadata.json`` scaffold files.
The agent then only needs to write the ``.js`` file.

The subject, grade level and subject area written into the scaffolds come
from, in order: the ``--subject`` / ``--grade-level`` / ``--subject-area``
flags, the project itself (``site_name`` in mkdocs.yml and the target audience
in docs/course-description.md), then a ``TODO:`` placeholder.

Usage:
    python3 generate-sim-scaffold.py --spec-file SPECS.json
        [--sim-id NAME] [--project-dir PATH]
        [--subject TEXT] [--grade-level TEXT] [--subject-area TEXT]
        [--dry-run] [--force] [--verbose]
"""

import argparse
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import (
    find_project_root, kebab_case, load_mkdocs_config, LIBRARY_CDNS, LIBRARY_CSS,
    GREEN, RED, YELLOW, CYAN, BOLD, DIM, RESET, CHECK, CROSS, WARN, ARROW,
)


# ── Course context (subject / grade level / subject area) ─────────────

TODO_SUBJECT      = "TODO: subject"
TODO_GRADE_LEVEL  = "TODO: grade level"
TODO_SUBJECT_AREA = "TODO: subject area"

# This script was first written for geometry-course with these values
# hard-coded into every scaffold.  Keep them for that project only, so its
# scaffolds do not change; every other project derives its own.
PROJECT_DEFAULTS = {
    "geometry-course": {
        "subject":      "High School Geometry",
        "grade_level":  "9-12",
        "subject_area": "Mathematics",
    },
}

# Labels that introduce the audience in course-description.md, best first.
# Each matches "**Target Audience:** High school students ..." or a
# "## Target Audience" heading; the text may start on the same line or on
# the lines that follow.
AUDIENCE_RES = tuple(
    re.compile(
        rf"^(?:\*\*{label}:?\*\*:?|#{{2,4}}[ \t]+{label}(?=[ \t]*$))[ \t]*(.*)$",
        re.IGNORECASE | re.MULTILINE,
    )
    for label in (
        r"Target\s+Audience", r"Intended\s+Audience", r"Primary\s+Audience",
        r"Audience", r"Grade\s+Levels?", r"Level",
    )
)

# Unedited placeholder from the init-textbook course-description.md template
TEMPLATE_AUDIENCE = "describe the intended reader"

_GRADE = r"(K|\d{1,2})(?:st|nd|rd|th)?"
_RANGE_SEP = r"\s*(?:[-–—]|to|through|and)\s*"
# The lookarounds skip a lone grade that is one end of an open span
# ("through grade 12", "9th grade through adult"), which names no range.
EXPLICIT_GRADE_RES = (
    # "grades 9–12", "Grade 5 and 6", "grades K-5"
    re.compile(rf"(?<!through )(?<!to )\bgrades?\s+{_GRADE}(?:{_RANGE_SEP}{_GRADE})?\b",
               re.IGNORECASE),
    # "5th through 12th grade", "9th grade"
    re.compile(rf"\b(?:{_GRADE}{_RANGE_SEP})?(\d{{1,2}})(?:st|nd|rd|th)[\s-]+grade"
               r"(?!\s+(?:through|to|and\s+(?:up|above)))", re.IGNORECASE),
)

# Audience wording → gradeLevel values from microsim-metadata-schema.json.
# The K-12 stages are only used when the text names no explicit grades.
K12_STAGE_RES = (
    (re.compile(r"elementary|grade[\s-]+school|primary[\s-]+school", re.IGNORECASE), range(0, 6)),
    (re.compile(r"middle[\s-]+school|junior[\s-]+high", re.IGNORECASE),              range(6, 9)),
    # "at least a high school education" describes adults, not grades 9-12
    (re.compile(r"high[\s-]+school(?!\s+(?:education|diploma|degree|graduate))",
                re.IGNORECASE),                                                      range(9, 13)),
)
ADULT_STAGE_RES = (
    (re.compile(r"undergraduate|\bfreshm[ae]n\b|college\s+(?:\w+\s+)?"
                r"(?:students?|sophomores?|juniors?|seniors?)", re.IGNORECASE), "Undergraduate"),
    (re.compile(r"\bgraduate\b", re.IGNORECASE),                                "Graduate"),
    (re.compile(r"\badults?\b|professional|practitioner", re.IGNORECASE),       "Adult"),
)


def read_target_audience(project_dir):
    """Return the target audience from docs/course-description.md as one
    line of plain text, or ``""`` if the file or the label is missing."""
    path = os.path.join(project_dir, "docs", "course-description.md")
    if not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    m = next((m for m in (p.search(text) for p in AUDIENCE_RES) if m), None)
    if not m:
        return ""

    # Collect one paragraph; a lead-in ending in ":" also pulls in its list.
    out = ""
    for line in [m.group(1)] + text[m.end():].splitlines()[1:15]:
        s = line.strip()
        if not s:
            if out and not out.endswith(":"):
                break
            continue
        if s.startswith("#") or (out and re.match(r"\*\*[^*]+\*\*", s)):
            break
        item = re.match(r"(?:[-*+]|\d+\.)\s+(.*)", s)
        s = re.sub(r"<br\s*/?>|\*\*", "", item.group(1) if item else s).strip()
        if not out:
            out = s
        else:
            out += ("; " if item and not out.endswith(":") else " ") + s
    out = re.sub(r"\s+", " ", out).strip()
    return "" if out.rstrip(".").lower() == TEMPLATE_AUDIENCE else out


def _explicit_grades(text):
    """Return ``(low, high)`` for the first explicit grade span in *text*
    (kindergarten is 0), or ``None``."""
    for pattern in EXPLICIT_GRADE_RES:
        m = pattern.search(text)
        if not m:
            continue
        # A single grade ("9th grade") fills only one of the two groups
        low, high = m.group(1) or m.group(2), m.group(2) or m.group(1)
        low, high = (0 if g.upper() == "K" else int(g) for g in (low, high))
        if 0 <= low <= high <= 12:
            return low, high
    return None


def grade_levels_from_text(text):
    """Map free text ("grades 9–12", "college freshmen") to the schema's
    gradeLevel values.  Returns ``[]`` when nothing is recognized."""
    span = _explicit_grades(text)
    grades = set(range(span[0], span[1] + 1)) if span else set()
    if not span:
        for pattern, stage in K12_STAGE_RES:
            if pattern.search(text):
                grades.update(stage)
    levels = ["K" if g == 0 else str(g) for g in sorted(grades)]
    return levels + [name for pattern, name in ADULT_STAGE_RES if pattern.search(text)]


def resolve_course_context(project_dir, mkdocs_cfg,
                           subject=None, grade_level=None, subject_area=None):
    """Work out the subject, grade level and subject area for the scaffolds.

    Each value comes from the first source that has one: the CLI flag, the
    ``PROJECT_DEFAULTS`` entry for this project, the project's own files
    (mkdocs.yml ``site_name``; the target audience in course-description.md),
    then a ``TODO:`` placeholder.

    Returns a dict with ``subject``, ``grade_level`` (display text),
    ``grade_levels`` (list for metadata.json) and ``subject_area``.
    """
    names = {
        os.path.basename(os.path.normpath(project_dir)),
        mkdocs_cfg.get("site_url", "").rstrip("/").rsplit("/", 1)[-1],
    }
    defaults = next((PROJECT_DEFAULTS[n] for n in sorted(names) if n in PROJECT_DEFAULTS), {})

    subject = subject or defaults.get("subject") or mkdocs_cfg.get("site_name") or TODO_SUBJECT
    subject_area = subject_area or defaults.get("subject_area") or TODO_SUBJECT_AREA

    grade_level = grade_level or defaults.get("grade_level")
    if grade_level:
        # A bare "9-12" is a grade span; anything else is read as free text.
        bare = re.fullmatch(r"\s*(?:K|\d{1,2})(?:\s*[-–—]\s*\d{1,2})?\s*", grade_level, re.IGNORECASE)
        grade_levels = grade_levels_from_text(f"grades {grade_level.strip()}" if bare else grade_level)
        grade_levels = grade_levels or [grade_level]
    else:
        # Only the first sentence describes the audience; later ones tend to
        # be prerequisites.  The display text is its first clause.  A period
        # after a short token ("St.", "U.S.", "e.g.") does not end a sentence.
        audience = re.split(r"(?:(?<=[a-z]{3})|(?<=[)\d]))\.(?:\s|;|$)",
                            read_target_audience(project_dir), maxsplit=1)[0]
        span = _explicit_grades(audience)
        if span:
            low, high = ("K" if g == 0 else str(g) for g in span)
            grade_level = low if low == high else f"{low}-{high}"
        else:
            grade_level = re.split(r"\s*;\s*|\s+[-–—]\s+", audience, maxsplit=1)[0].rstrip(" ,:.")
        grade_level = grade_level or TODO_GRADE_LEVEL
        grade_levels = grade_levels_from_text(audience) or [TODO_GRADE_LEVEL]

    return {
        "subject":      subject,
        "grade_level":  grade_level,
        "grade_levels": grade_levels,
        "subject_area": subject_area,
    }


# Used when a template is called without a resolved course context
PLACEHOLDER_COURSE = {
    "subject":      TODO_SUBJECT,
    "grade_level":  TODO_GRADE_LEVEL,
    "grade_levels": [TODO_GRADE_LEVEL],
    "subject_area": TODO_SUBJECT_AREA,
}


def _html_template(sim_id, title, library):
    """Generate the main.html content for a given library."""
    cdn = LIBRARY_CDNS.get(library, LIBRARY_CDNS["p5.js"])
    css_cdn = LIBRARY_CSS.get(library, "")

    css_link = ""
    if css_cdn:
        css_link = f'    <link rel="stylesheet" href="{css_cdn}">\n'

    # Determine script tag
    if library == "p5.js":
        script_src = f'    <script src="{cdn}"></script>\n    <script src="{sim_id}.js"></script>'
    elif library in ("vis-network", "vis-timeline", "Leaflet"):
        script_src = f'    <script src="{cdn}"></script>\n    <script src="{sim_id}.js"></script>'
    elif library == "Chart.js":
        script_src = f'    <script src="{cdn}"></script>\n    <script src="{sim_id}.js"></script>'
    elif library == "Mermaid":
        script_src = f'    <script src="{cdn}"></script>\n    <script src="{sim_id}.js"></script>'
    elif library == "Plotly":
        script_src = f'    <script src="{cdn}"></script>\n    <script src="{sim_id}.js"></script>'
    else:
        # Default to p5.js
        cdn = LIBRARY_CDNS["p5.js"]
        script_src = f'    <script src="{cdn}"></script>\n    <script src="{sim_id}.js"></script>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="schema" content="https://dmccreary.github.io/intelligent-textbooks/ns/microsim/v1">
    <title>{title} using {library}</title>
{css_link}    <style>
        body {{ margin: 0px; padding: 0px; font-family: Arial, Helvetica, sans-serif; }}
    </style>
{script_src}
</head>
<body>
    <main></main>
    <br/>
    <a href=".">Back to Lesson Plan</a>
</body>
</html>
"""


def _index_md_template(sim_id, title, library, bloom_level, chapter, site_url="", course=None):
    """Generate the index.md scaffold."""
    display_title = title.replace("-", " ").title() if title == sim_id else title
    today = date.today().isoformat()
    course = course or PLACEHOLDER_COURSE
    grade_level = course["grade_level"]
    if course["subject"] != TODO_SUBJECT:
        grade_level += f" ({course['subject']})"

    return f"""---
title: {display_title}
description: Interactive {library or 'p5.js'} MicroSim for {display_title.lower()}.
image: /sims/{sim_id}/{sim_id}.png
og:image: /sims/{sim_id}/{sim_id}.png
twitter:image: /sims/{sim_id}/{sim_id}.png
social:
   cards: false
quality_score: 0
---

# {display_title}

<iframe src="main.html" height="450px" width="100%" scrolling="no"></iframe>

[Run the {display_title} MicroSim Fullscreen](./main.html){{ .md-button .md-button--primary }}
<br/>
[Edit in the p5.js Editor](https://editor.p5js.org/)

## About This MicroSim

TODO: Describe what this MicroSim demonstrates.

## How to Use

TODO: Describe how students should interact with this MicroSim.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="{site_url}sims/{sim_id}/main.html"
        height="450px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Grade Level
{grade_level}

### Duration
10-15 minutes

### Prerequisites
TODO: List prerequisites.

### Activities

1. **Exploration** (5 min): TODO
2. **Guided Practice** (5 min): TODO
3. **Assessment** (5 min): TODO

### Assessment
TODO: List assessment criteria.

## References

1. TODO: Add references.
"""


def _metadata_json_template(sim_id, title, library, bloom_level, chapter, course=None):
    """Generate the metadata.json scaffold."""
    display_title = title.replace("-", " ").title() if title == sim_id else title
    today = date.today().isoformat()
    course = course or PLACEHOLDER_COURSE

    return json.dumps({
        "title": display_title,
        "creator": "Dan McCreary",
        "subject": course["subject"],
        "description": f"Interactive MicroSim for {display_title.lower()}",
        "date": today,
        "educational": {
            "gradeLevel": course["grade_levels"],
            "subjectArea": course["subject_area"],
            "topic": display_title,
            "learningObjectives": [
                "TODO: Add learning objectives"
            ],
            "bloomsTaxonomy": bloom_level or "Understand",
            "duration": "10-15 minutes",
            "prerequisites": [],
            "standards": []
        },
        "technical": {
            "framework": library or "p5.js",
            "version": "1.0",
            "canvasDimensions": {"width": "responsive", "height": 450},
            "responsive": True,
            "dependencies": [],
            "accessibility": {
                "hasAltText": False,
                "keyboardNavigable": False
            }
        },
        "pedagogical": {
            "teachingStrategy": "Interactive exploration",
            "keyQuestions": [],
            "commonMisconceptions": [],
            "assessmentOpportunities": []
        },
        "chapter": chapter
    }, indent=2) + "\n"


def scaffold_sim(spec, project_dir, site_url="", dry_run=False, force=False, verbose=False,
                 course=None):
    """Create scaffold files for a single sim spec."""
    sim_id = spec["sim_id"]
    title = spec["title"]
    library = spec.get("library", "") or "p5.js"
    bloom = spec.get("bloom_level", "")
    chapter = spec.get("chapter", "")

    sim_dir = os.path.join(project_dir, "docs", "sims", sim_id)

    if verbose:
        print(f"\n{CYAN}{BOLD}{sim_id}{RESET}")
        print(f"  Library: {library}  Bloom: {bloom or 'unset'}  Chapter: {chapter or 'none'}")

    if os.path.isdir(sim_dir) and not force:
        if verbose:
            print(f"  {YELLOW}{WARN} Directory exists, skipping (use --force to overwrite){RESET}")
        return False

    files = {
        "main.html":     _html_template(sim_id, title, library),
        "index.md":      _index_md_template(sim_id, title, library, bloom, chapter, site_url, course),
        "metadata.json": _metadata_json_template(sim_id, title, library, bloom, chapter, course),
    }

    if dry_run:
        for name in files:
            path = os.path.join(sim_dir, name)
            print(f"  {DIM}[dry-run]{RESET} Would create {path}")
        return True

    os.makedirs(sim_dir, exist_ok=True)
    for name, content in files.items():
        path = os.path.join(sim_dir, name)
        if os.path.exists(path) and not force:
            if verbose:
                print(f"  {YELLOW}{WARN} {name} exists, skipping{RESET}")
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        if verbose:
            print(f"  {GREEN}{CHECK}{RESET} Created {name}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate MicroSim scaffold files from specs JSON."
    )
    parser.add_argument(
        "--spec-file", required=True,
        help="Path to specs JSON from extract-sim-specs.py",
    )
    parser.add_argument(
        "--sim-id", default=None,
        help="Only scaffold this specific sim_id (default: all unscaffolded)",
    )
    parser.add_argument(
        "--project-dir", default=None,
        help="Project root (auto-detect if omitted)",
    )
    parser.add_argument(
        "--subject", default=None,
        help="Subject written into the scaffolds (default: site_name from mkdocs.yml)",
    )
    parser.add_argument(
        "--grade-level", default=None,
        help="Grade level, e.g. '9-12' or 'Undergraduate' "
             "(default: target audience from docs/course-description.md)",
    )
    parser.add_argument(
        "--subject-area", default=None,
        help="Subject area for metadata.json, e.g. 'Mathematics' "
             "(default: a TODO placeholder)",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be created without writing files")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing files")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    project_dir = args.project_dir or find_project_root()

    # Extract site_url from mkdocs.yml for full iframe embed paths
    mkdocs_cfg = load_mkdocs_config(project_dir)
    site_url = mkdocs_cfg.get("site_url", "").rstrip("/")
    if site_url:
        site_url += "/"

    course = resolve_course_context(
        project_dir, mkdocs_cfg,
        subject=args.subject, grade_level=args.grade_level, subject_area=args.subject_area,
    )
    if args.verbose:
        print(f"{BOLD}Subject:{RESET} {course['subject']}")
        print(f"{BOLD}Grade level:{RESET} {course['grade_level']}  {DIM}{course['grade_levels']}{RESET}")
        print(f"{BOLD}Subject area:{RESET} {course['subject_area']}")
    unresolved = [
        flag for flag, value in (
            ("--subject", course["subject"]),
            ("--grade-level", course["grade_levels"][0]),
            ("--subject-area", course["subject_area"]),
        ) if value.startswith("TODO:")
    ]
    if unresolved:
        print(f"{YELLOW}{WARN} No project value for {', '.join(unresolved)}; "
              f"scaffolds will carry TODO placeholders{RESET}")

    with open(args.spec_file, encoding="utf-8") as f:
        specs = json.load(f)

    if args.sim_id:
        specs = [s for s in specs if s["sim_id"] == args.sim_id]
        if not specs:
            print(f"{RED}{CROSS} sim_id '{args.sim_id}' not found in specs file{RESET}")
            sys.exit(1)

    created = 0
    skipped = 0
    for spec in specs:
        if scaffold_sim(spec, project_dir, site_url=site_url,
                        dry_run=args.dry_run,
                        force=args.force, verbose=args.verbose, course=course):
            created += 1
        else:
            skipped += 1

    mode = "[dry-run] " if args.dry_run else ""
    print(f"\n{GREEN}{CHECK} {mode}Scaffolded: {created}  Skipped: {skipped}  Total: {len(specs)}{RESET}")


if __name__ == "__main__":
    main()

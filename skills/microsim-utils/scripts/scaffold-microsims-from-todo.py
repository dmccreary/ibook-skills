#!/usr/bin/env python3
"""
Scaffold MicroSim directories from TODO JSON specification files.

For each docs/sims/TODO/<sim-id>.json that does NOT already have a
docs/sims/<sim-id>/main.html, create a new directory with stub files:
  - main.html       (placeholder canvas + spec embedded as a comment)
  - index.md        (frontmatter, learning objective, iframe embed, spec)
  - metadata.json   (mapped from the TODO JSON)

All project-specific metadata (creator, author, rights/license, language) is
derived from the project's mkdocs.yml so nothing is carried over from whatever
project this skill was last run against. Each can be overridden on the command
line.

Usage:
    python scaffold-microsims-from-todo.py [--project-dir /path/to/project]
        [--force] [--project-name NAME] [--subject TAG ...]
        [--rights LICENSE] [--language CODE]

--force overwrites existing scaffold files (but never main.html if it
already exists, since that may contain a real implementation).
"""

import argparse
import glob
import json
import os
import re
import sys
from datetime import date


def find_project_root(start_path):
    current = os.path.abspath(start_path)
    while True:
        if os.path.isfile(os.path.join(current, "mkdocs.yml")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def _strip_quotes(value):
    """Strip a trailing inline comment and surrounding quotes from a YAML scalar."""
    value = value.strip()
    # If the value is quoted, take only what is inside the quotes (so a '#'
    # inside the quotes is preserved). Otherwise drop any inline comment.
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1].strip()
    if "#" in value:
        value = value.split("#", 1)[0]
    return value.strip()


def _strip_html(text):
    """Remove HTML tags, leaving the visible text."""
    return re.sub(r"<[^>]+>", "", text)


# Matches Creative Commons license identifiers such as:
#   CC BY 4.0, CC BY-NC-SA 4.0, CC BY-SA 4.0, CC0 1.0
CC_LICENSE_RE = re.compile(
    r"\bCC[0-9]?(?:[ -](?:BY|NC|SA|ND))*(?:\s+\d+(?:\.\d+)?)?", re.IGNORECASE
)


def parse_license(copyright_text):
    """Extract a concise license id from a copyright string.

    Falls back to the full HTML-stripped copyright text when no recognizable
    Creative Commons identifier is present. Returns None for empty input.
    """
    if not copyright_text:
        return None
    plain = _strip_html(copyright_text).strip()
    match = CC_LICENSE_RE.search(plain)
    if match:
        return re.sub(r"\s+", " ", match.group(0)).strip()
    return plain or None


def read_mkdocs_config(project_root):
    """Parse selected fields from mkdocs.yml without a PyYAML dependency.

    Returns a dict with keys: site_name, site_author, copyright, language.
    The nested theme.language value is read with a small indentation-aware
    scan. Line-based parsing keeps the script robust against the custom YAML
    tags (e.g. !!python/name:) that Material configs sometimes use and that
    break yaml.safe_load.
    """
    config = {
        "site_name": None,
        "site_author": None,
        "copyright": None,
        "language": None,
    }
    mkdocs_path = os.path.join(project_root, "mkdocs.yml")
    in_theme = False
    try:
        with open(mkdocs_path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.rstrip("\n")
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                indented = line[:1] in (" ", "\t")
                # A new top-level key ends the theme block.
                if not indented:
                    in_theme = stripped.startswith("theme:")
                if line.startswith("site_name:"):
                    config["site_name"] = _strip_quotes(line.split(":", 1)[1])
                elif line.startswith("site_author:"):
                    config["site_author"] = _strip_quotes(line.split(":", 1)[1])
                elif line.startswith("copyright:"):
                    config["copyright"] = _strip_quotes(line.split(":", 1)[1])
                elif in_theme and stripped.startswith("language:"):
                    config["language"] = _strip_quotes(stripped.split(":", 1)[1])
    except OSError:
        pass
    return config


# Sentinel embedded in every generated stub so the scaffolder can later tell
# its own placeholder main.html apart from a real, hand-built implementation.
# A real implementation will not contain this string, so it is never clobbered.
SCAFFOLD_MARKER = "<!-- microsim-scaffold-stub -->"


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {marker}
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8f9fa;
            color: #212529;
        }}
        #container {{
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: white;
        }}
        h1 {{
            font-size: 22px;
            margin-bottom: 10px;
            color: #1a3a6c;
        }}
        .placeholder {{
            border: 2px dashed #adb5bd;
            border-radius: 8px;
            padding: 40px 20px;
            text-align: center;
            color: #6c757d;
            margin: 20px 0;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .placeholder .badge {{
            display: inline-block;
            background: #ffc107;
            color: #212529;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 12px;
        }}
        .placeholder h2 {{
            font-size: 18px;
            color: #495057;
            margin-bottom: 8px;
        }}
        .placeholder p {{
            font-size: 14px;
            max-width: 480px;
        }}
        .meta {{
            margin-top: 20px;
            font-size: 13px;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
            padding-top: 12px;
        }}
        .meta strong {{ color: #495057; }}
    </style>
</head>
<body>
    <div id="container">
        <h1>{title}</h1>
        <div class="placeholder">
            <span class="badge">SCAFFOLD</span>
            <h2>MicroSim Not Yet Implemented</h2>
            <p>This MicroSim has been scaffolded from its specification but the
            interactive content has not been built yet. See the chapter source
            and the <code>index.md</code> in this directory for the full spec.</p>
        </div>
        <div class="meta">
            <p><strong>Sim ID:</strong> {sim_id}</p>
            <p><strong>Library:</strong> {library}</p>
            <p><strong>Bloom Level:</strong> {bloom_level}</p>
            <p><strong>Learning Objective:</strong> {learning_objective}</p>
        </div>
    </div>

    <!--
    SPECIFICATION (from chapter index.md):

{spec_block}
    -->
</body>
</html>
"""


INDEX_MD_TEMPLATE = """---
title: {title_yaml}
description: {description_yaml}
status: scaffold
library: {library_yaml}
bloom_level: {bloom_level_yaml}
---

# {title}



<iframe src="main.html" width="100%" height="600"></iframe>

[Run MicroSim in Fullscreen](main.html){{ .md-button .md-button--primary }}

## Specification

The full specification below is extracted from
[Chapter {chapter_number}: {chapter_title}](../../{chapter_rel_dir}/index.md).

{fence}text
{specification}
{fence}

## Related Resources

- [Chapter {chapter_number}: {chapter_title}](../../{chapter_rel_dir}/index.md)
"""


def make_metadata(
    spec,
    project_name="Intelligent Textbook",
    subject=None,
    rights="All rights reserved",
    language="en",
    author=None,
):
    return {
        "title": spec["diagram_name"],
        "description": (spec.get("learning_objective") or spec["diagram_name"]),
        "creator": project_name,
        "author": author or project_name,
        "date": str(date.today()),
        "subject": subject if subject else [project_name],
        "type": "Interactive Simulation",
        "format": "text/html",
        "language": language,
        "rights": rights,
        "identifier": spec["sim_id"],
        "library": spec.get("library") or "TBD",
        "bloomLevel": spec.get("bloom_level") or "TBD",
        "bloomVerb": spec.get("bloom_verb") or "TBD",
        "completion_status": "scaffold",
        "chapter_number": spec.get("chapter_number"),
        "chapter_title": spec.get("chapter_title"),
        "chapter_dir": spec.get("chapter_dir"),
        "chapter_rel_dir": spec.get("chapter_rel_dir") or f"chapters/{spec.get('chapter_dir') or ''}",
    }


def indent_block(text, indent="    "):
    return "\n".join(indent + line for line in text.splitlines())


def yaml_quote(value):
    """Return value as a double-quoted YAML scalar.

    Frontmatter values are always quoted because an unquoted value that
    contains ": " is invalid YAML, and the page then silently loses its title
    and nav status dot without failing `mkdocs build --strict`. A JSON string
    is a valid YAML double-quoted scalar, so json.dumps does the escaping.
    """
    return json.dumps(str(value), ensure_ascii=False)


# A plain (unquoted) YAML scalar is only safe when it has none of these.
YAML_UNSAFE_RE = re.compile(r""":\s|\s#|^[\s'"&*!|>%@`\[\]{},#?-]|[\s:]$""")


def yaml_scalar(value):
    """Return value unquoted when that is safe YAML, otherwise double-quoted.

    Used for the short machine-readable fields (library, bloom_level) so the
    common case stays `library: p5.js`.
    """
    value = str(value)
    if not value or YAML_UNSAFE_RE.search(value):
        return yaml_quote(value)
    return value


def code_fence_for(text):
    """Return a backtick fence long enough to wrap text.

    A spec that contains its own fenced code block would close a fixed
    three-backtick fence early, so use one backtick more than the longest
    run of backticks in the text, with a minimum of three.
    """
    longest = max((len(run) for run in re.findall(r"`+", text)), default=0)
    return "`" * max(3, longest + 1)


# Stubs generated before SCAFFOLD_MARKER existed are still recognizable by
# this distinctive placeholder text, which no real implementation contains.
LEGACY_STUB_SIGNATURE = "MicroSim Not Yet Implemented"


def is_scaffold_stub(main_html_path):
    """True if main.html is one of our generated placeholder stubs.

    Matches both the current marker and the pre-marker placeholder text so
    stubs created by earlier runs are still recognized. A real, hand-built
    implementation contains neither, so it is reported as implemented and
    never overwritten or refreshed.
    """
    try:
        with open(main_html_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return False
    return SCAFFOLD_MARKER in content or LEGACY_STUB_SIGNATURE in content


def scaffold_one(
    spec,
    sims_dir,
    force=False,
    project_name="Intelligent Textbook",
    subject=None,
    rights="All rights reserved",
    language="en",
    author=None,
):
    sim_id = spec["sim_id"]
    sim_dir = os.path.join(sims_dir, sim_id)
    main_html = os.path.join(sim_dir, "main.html")
    index_md = os.path.join(sim_dir, "index.md")
    meta_json = os.path.join(sim_dir, "metadata.json")

    main_exists = os.path.isfile(main_html)

    # An existing main.html that is NOT one of our stubs is a real
    # implementation: never touch it.
    if main_exists and not is_scaffold_stub(main_html):
        return "skipped-implemented"

    # An existing stub with no --force has nothing to do.
    if main_exists and not force:
        return "skipped-existing"

    os.makedirs(sim_dir, exist_ok=True)

    title = spec["diagram_name"]
    library = spec.get("library") or "TBD"
    bloom_level = spec.get("bloom_level") or "TBD"
    bloom_verb = spec.get("bloom_verb") or "TBD"
    learning_objective = spec.get("learning_objective") or "TBD"
    description = (spec.get("learning_objective") or title).split("\n")[0]
    specification = spec.get("specification") or ""

    html_out = HTML_TEMPLATE.format(
        marker=SCAFFOLD_MARKER,
        title=title,
        sim_id=sim_id,
        library=library,
        bloom_level=bloom_level,
        learning_objective=learning_objective,
        spec_block=indent_block(specification, "    "),
    )

    chapter_rel_dir = spec.get("chapter_rel_dir") or f"chapters/{spec.get('chapter_dir') or ''}"

    md_out = INDEX_MD_TEMPLATE.format(
        title=title,
        title_yaml=yaml_quote(title),
        description_yaml=yaml_quote(description),
        library_yaml=yaml_scalar(library),
        bloom_level_yaml=yaml_scalar(bloom_level),
        fence=code_fence_for(specification),
        bloom_verb=bloom_verb,
        learning_objective=learning_objective,
        chapter_number=spec.get("chapter_number") or "?",
        chapter_title=spec.get("chapter_title") or "",
        chapter_rel_dir=chapter_rel_dir,
        specification=specification,
    )

    # Write main.html. We reach here only when it is absent (fresh scaffold)
    # or it is an existing stub being refreshed with --force; a real
    # implementation was already returned above, so this never clobbers code.
    with open(main_html, "w", encoding="utf-8") as f:
        f.write(html_out)

    # index.md - write if missing or force
    if force or not os.path.isfile(index_md):
        with open(index_md, "w", encoding="utf-8") as f:
            f.write(md_out)

    # metadata.json - write if missing or force
    if force or not os.path.isfile(meta_json):
        with open(meta_json, "w", encoding="utf-8") as f:
            json.dump(
                make_metadata(
                    spec,
                    project_name=project_name,
                    subject=subject,
                    rights=rights,
                    language=language,
                    author=author,
                ),
                f,
                indent=2,
                ensure_ascii=False,
            )

    # main_exists implies we got here via --force on an existing stub.
    return "refreshed" if main_exists else "scaffolded"


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold MicroSim directories from TODO JSON specs."
    )
    parser.add_argument(
        "--project-dir",
        help="Path to the project root (containing mkdocs.yml). Auto-detected if omitted.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing index.md and metadata.json (never overwrites main.html).",
    )
    parser.add_argument(
        "--project-name",
        help="Project/creator name written to metadata.json 'creator' and 'subject'. "
        "Defaults to site_name from mkdocs.yml.",
    )
    parser.add_argument(
        "--subject",
        action="append",
        help="Subject tag for metadata.json (repeatable). "
        "Defaults to a single tag equal to the project name.",
    )
    parser.add_argument(
        "--rights",
        help="License/rights string for metadata.json. "
        "Defaults to the license parsed from the mkdocs.yml 'copyright' field.",
    )
    parser.add_argument(
        "--language",
        help="Language code for metadata.json. "
        "Defaults to theme.language in mkdocs.yml, or 'en'.",
    )
    args = parser.parse_args()

    if args.project_dir:
        project_root = os.path.abspath(args.project_dir)
    else:
        project_root = find_project_root(os.path.dirname(os.path.abspath(__file__)))

    if not project_root or not os.path.isfile(os.path.join(project_root, "mkdocs.yml")):
        print("ERROR: Could not find project root (no mkdocs.yml found).", file=sys.stderr)
        sys.exit(1)

    sims_dir = os.path.join(project_root, "docs", "sims")
    todo_dir = os.path.join(sims_dir, "TODO")

    if not os.path.isdir(todo_dir):
        print(f"ERROR: TODO directory not found: {todo_dir}", file=sys.stderr)
        sys.exit(1)

    todo_files = sorted(glob.glob(os.path.join(todo_dir, "*.json")))

    # All project-specific metadata is derived from mkdocs.yml so nothing is
    # carried over from whatever project this skill was last used on.
    config = read_mkdocs_config(project_root)
    project_name = args.project_name or config["site_name"] or "Intelligent Textbook"
    subject = args.subject  # None falls back to [project_name] in make_metadata
    rights = args.rights or parse_license(config["copyright"]) or "All rights reserved"
    language = args.language or config["language"] or "en"
    author = config["site_author"] or project_name

    counts = {"scaffolded": 0, "refreshed": 0, "skipped-existing": 0, "skipped-implemented": 0}
    labels = {
        "scaffolded": "scaffolded",
        "refreshed": "refreshed (stub updated)",
        "skipped-existing": "skipped (already scaffolded, use --force to refresh)",
        "skipped-implemented": "skipped (real implementation)",
    }
    for todo_path in todo_files:
        with open(todo_path, "r", encoding="utf-8") as f:
            spec = json.load(f)
        result = scaffold_one(
            spec,
            sims_dir,
            force=args.force,
            project_name=project_name,
            subject=subject,
            rights=rights,
            language=language,
            author=author,
        )
        counts[result] = counts.get(result, 0) + 1
        print(f"  {labels.get(result, result)}: {spec['sim_id']}")

    print()
    print(f"Project root: {project_root}")
    print("Metadata derived from mkdocs.yml:")
    print(f"  creator/project name: {project_name}")
    print(f"  author:               {author}")
    print(f"  rights/license:       {rights}")
    print(f"  language:             {language}")
    print(f"TODO specs processed: {len(todo_files)}")
    print(f"Scaffolded (new):                {counts['scaffolded']}")
    print(f"Refreshed (stub updated):        {counts['refreshed']}")
    print(f"Skipped (already scaffolded):    {counts['skipped-existing']}")
    print(f"Skipped (real implementation):   {counts['skipped-implemented']}")


if __name__ == "__main__":
    main()

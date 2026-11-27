#!/usr/bin/env python3
"""Validate (and optionally fix) YAML frontmatter in MkDocs markdown pages.

Why this exists: generated pages (stories, posters, MicroSims) often get a
title like ``The Sultan's Sweet Tooth: Spice, Coffee and Turkish Delight``.
Unquoted, the ``: `` inside the value makes the frontmatter invalid YAML
("mapping values are not allowed here"), and MkDocs silently drops the whole
frontmatter block: the page loses its title, description, social-card image
and status. A `` #`` inside an unquoted value is worse: it parses, but
everything after it is treated as a comment and vanishes.

Checks every ``*.md`` file under the given paths that starts with ``---``:

  * ERROR  - the frontmatter does not parse as YAML, or is not terminated.
  * RISKY  - a single-line ``key: value`` whose value is an unquoted plain
             scalar containing ``: ``, `` #``, a trailing ``:``, or starting
             with a YAML indicator character. Parses today only by luck, or
             parses to something other than what was written.

Usage:
    python3 validate-frontmatter.py docs/                  # report only
    python3 validate-frontmatter.py docs/stories/x/index.md
    python3 validate-frontmatter.py docs/ --fix            # double-quote risky values

``--fix`` rewrites each risky value as a YAML double-quoted string (escaping
backslashes and double quotes), then re-parses the file to confirm it is
valid. Exits 1 if any ERROR or RISKY line remains, 0 when everything is clean.
Requires PyYAML (installed with MkDocs).
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml (it ships with mkdocs)")

FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(\r?\n|\Z)", re.S)
# Single-line "key: value" (keys may contain ':' as in og:image, or '.'/'-').
KEY_VALUE_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<key>[A-Za-z_][\w:.-]*):[ \t]+(?P<value>\S.*?)[ \t]*$")
# Characters that cannot safely begin a plain YAML scalar.
INDICATOR_START = set("@`!&*%?|>,[]{}#")
QUOTE_OR_BLOCK = set("\"'|>[{")


def is_risky(value: str) -> str | None:
    """Return a reason string if an unquoted value is unsafe, else None."""
    if value[0] in QUOTE_OR_BLOCK:
        return None  # already quoted, a block scalar, or a flow collection
    if ": " in value:
        return "contains ': ' (colon-space)"
    if " #" in value:
        return "contains ' #' (rest of the line becomes a comment)"
    if value.endswith(":"):
        return "ends with ':'"
    if value[0] in INDICATOR_START:
        return f"starts with YAML indicator {value[0]!r}"
    if value.startswith("- ") or value == "-":
        return "starts with '- '"
    return None


def quote(value: str) -> str:
    # JSON strings are valid YAML double-quoted scalars.
    return json.dumps(value, ensure_ascii=False)


def check_file(path: Path, fix: bool) -> tuple[list[str], int]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return [], 0
    m = FRONTMATTER_RE.match(text)
    if not m:
        return [f"{path}:1: ERROR frontmatter opened with '---' but never closed"], 0

    fm = m.group(1)
    lines = fm.splitlines()
    problems, fixed = [], 0
    for i, line in enumerate(lines):
        kv = KEY_VALUE_RE.match(line)
        if not kv:
            continue
        reason = is_risky(kv.group("value"))
        if not reason:
            continue
        if fix:
            lines[i] = f'{kv.group("indent")}{kv.group("key")}: {quote(kv.group("value"))}'
            fixed += 1
        else:
            problems.append(f"{path}:{i + 2}: RISKY {kv.group('key')} {reason}: {line.strip()[:100]}")

    if fixed:
        new_fm = "\n".join(lines)
        text = text[: m.start(1)] + new_fm + text[m.end(1):]
        path.write_text(text, encoding="utf-8")
        fm = new_fm

    try:
        yaml.safe_load(fm)
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        line_no = mark.line + 2 if mark else 1
        problem = getattr(e, "problem", None) or str(e).splitlines()[0]
        problems.append(f"{path}:{line_no}: ERROR invalid YAML: {problem}")
    return problems, fixed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("paths", nargs="+", help="markdown files or directories to scan")
    ap.add_argument("--fix", action="store_true", help="double-quote risky unquoted values in place")
    args = ap.parse_args()

    files: list[Path] = []
    for p in map(Path, args.paths):
        if p.is_dir():
            files.extend(sorted(p.rglob("*.md")))
        elif p.is_file():
            files.append(p)
        else:
            print(f"warning: {p} not found", file=sys.stderr)

    all_problems, total_fixed = [], 0
    for f in files:
        problems, fixed = check_file(f, args.fix)
        all_problems.extend(problems)
        if fixed:
            print(f"fixed {fixed} value(s) in {f}")
        total_fixed += fixed

    for p in all_problems:
        print(p)
    print(f"Checked {len(files)} file(s): {len(all_problems)} problem(s)"
          + (f", {total_fixed} value(s) quoted" if args.fix else ""))
    return 1 if all_problems else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Set `status: instrumented` on every MicroSim that carries xAPI event handling.

The nav's status icon (MkDocs Material `status:` frontmatter, the book's `extra.status`)
shows a sim's lifecycle: specified -> scaffolded -> implemented -> **instrumented**.
"Instrumented" means the capability is PRESENT: main.html loads the runtime (lrs-sim.js)
and the sim's code calls LRSSim.create. It says nothing about whether the book or the
sim's metadata.json turns the teaching panel on; `?xapi=teaching` shows it on any
instrumented sim.

Usage:
    sync-status.py --book <book-root>            # report only (dry run)
    sync-status.py --book <book-root> --apply    # edit index.md frontmatter

Rules:
  * An instrumented sim whose status is `implemented`, `built`, missing, or anything
    unregistered becomes `instrumented`.
  * A human sign-off (`approved`) is never overwritten; it is reported instead.
  * A sim marked `instrumented` that no longer loads the runtime is reported, and with
    --apply is set back to `implemented`.
  * Only the `status:` line inside the index.md frontmatter is touched; if the page has no
    frontmatter status, one is inserted before the closing `---`.
  * The icon is ALWAYS the "signal" icon (Material Design Icons access-point, teal) from
    assets/status-instrumented.css (Dan, 2026-09-26). With --apply, a book that lacks it
    gets that CSS appended to docs/css/extra.css, and the tooltip added under an existing
    mkdocs.yml `extra.status` block. Without them Material shows a bare info icon with no
    tooltip.

Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

KEEP = {"approved"}          # human sign-offs this script never overwrites
ASSET_CSS = Path(__file__).resolve().parent.parent / "assets" / "status-instrumented.css"
TOOLTIP = "Instrumented — the MicroSim emits xAPI events; add ?xapi=teaching to the URL to see them"


def find_book_root(start: Path) -> Path:
    d = start.resolve()
    while d != d.parent:
        if (d / "mkdocs.yml").is_file():
            return d
        d = d.parent
    sys.exit(f"no mkdocs.yml above {start}")


def is_instrumented(sim: Path) -> bool:
    html = (sim / "main.html").read_text(errors="replace")
    if not re.search(r"<script[^>]+src=['\"][^'\"]*lrs-sim\.js['\"]", html):
        return False
    code = [html] + [f.read_text(errors="replace") for f in sim.glob("*.js")]
    return any("LRSSim.create" in c for c in code)


FRONT = re.compile(r"\A---\n(.*?\n)---\n", re.DOTALL)


def get_status(text: str) -> str | None:
    m = FRONT.match(text)
    if not m:
        return None
    s = re.search(r"^status:\s*(\S+)\s*$", m.group(1), re.MULTILINE)
    return s.group(1) if s else None


def set_status(text: str, value: str) -> str:
    m = FRONT.match(text)
    if not m:
        return f"---\nstatus: {value}\n---\n" + text
    body = m.group(1)
    if re.search(r"^status:", body, re.MULTILINE):
        body = re.sub(r"^status:.*$", f"status: {value}", body, count=1, flags=re.MULTILINE)
    else:
        body += f"status: {value}\n"
    return f"---\n{body}---\n" + text[m.end():]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", type=Path, default=Path("."))
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    book = find_book_root(a.book)
    sims = sorted(d for d in (book / "docs" / "sims").iterdir() if (d / "main.html").is_file())
    changes, notes = [], []
    for sim in sims:
        idx = sim / "index.md"
        if not idx.is_file():
            continue
        text = idx.read_text(errors="replace")
        cur = get_status(text)
        inst = is_instrumented(sim)
        want = None
        if inst and cur != "instrumented":
            if cur in KEEP:
                notes.append(f"{sim.name}: instrumented, but status '{cur}' is a sign-off — left alone")
            else:
                want = "instrumented"
        elif not inst and cur == "instrumented":
            want = "implemented"
            notes.append(f"{sim.name}: marked instrumented but no longer loads the runtime")
        if want:
            changes.append((sim.name, cur, want))
            if a.apply:
                idx.write_text(set_status(text, want))

    n_inst = sum(is_instrumented(s) for s in sims)
    print(f"book: {book}   sims: {len(sims)}   instrumented: {n_inst}")
    for name, cur, want in changes:
        print(f"  {'SET ' if a.apply else 'WOULD SET'}  {name:<44} {cur or '(none)'} -> {want}")
    for n in notes:
        print(f"  NOTE  {n}")
    if not changes:
        print("  statuses already in sync")

    # The nav icon itself: the standard "signal" (MDI access-point) icon, teal, from this
    # skill's assets/status-instrumented.css. Without the CSS and the extra.status entry,
    # Material shows a bare info icon with no tooltip.
    mk_path = book / "mkdocs.yml"
    mk = mk_path.read_text(errors="replace")
    if not re.search(r"^\s+instrumented\s*:", mk, re.MULTILINE):
        m = re.search(r"^extra:\s*\n(?:(?:[ \t].*)?\n)*?([ \t]+)status:\s*\n", mk, re.MULTILINE)
        if a.apply and m:
            line = f"{m.group(1) * 2}instrumented: {TOOLTIP}\n"
            mk_path.write_text(mk[:m.end()] + line + mk[m.end():])
            print("  ADDED  mkdocs.yml extra.status.instrumented")
        else:
            print("  !! mkdocs.yml extra.status has no `instrumented` entry" +
                  ("" if m else " (and no extra.status block to add it to)") +
                  f". {'Add it by hand' if not m else 'Run with --apply'}:\n"
                  f"       extra:\n         status:\n           instrumented: {TOOLTIP}")
    css_files = sorted((book / "docs").rglob("*.css"))
    if not any(".md-status--instrumented" in p.read_text(errors="replace") for p in css_files):
        target = book / "docs" / "css" / "extra.css"
        if a.apply and target.is_file() and "extra.css" in mk:
            target.write_text(target.read_text() + "\n" + ASSET_CSS.read_text())
            print("  ADDED  docs/css/extra.css: the instrumented (signal icon) status rules")
        else:
            print(f"  !! no CSS styles .md-status--instrumented. "
                  f"{'Run with --apply, or a' if target.is_file() else 'A'}ppend {ASSET_CSS} "
                  "to a stylesheet listed in mkdocs.yml extra_css")
    if not a.apply and changes:
        print("\nDry run. Re-run with --apply to write the index.md files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

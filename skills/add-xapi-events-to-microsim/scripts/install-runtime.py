#!/usr/bin/env python3
"""Check or install the shared xAPI runtime and this book's lrs-config.js.

The runtime is identical in every textbook; only lrs-config.js differs. Until Phase 3
moves this job into book-installer, the canonical runtime is the learning-record-store
repo's docs/js and docs/css.

Usage:
    install-runtime.py --book <book-root> --check      # report only; exit 1 if anything is missing/drifted
    install-runtime.py --book <book-root>              # copy missing files, generate lrs-config.js if absent
    options:
      --source DIR        canonical docs/ dir (default ~/Documents/ws/learning-record-store/docs,
                          or $LRS_RUNTIME_SRC)
      --textbook-id ID    grouping IRI textbook id for a NEW lrs-config.js (default: repo slug; see below)
      --version V         textbook version for a NEW lrs-config.js (default: mkdocs.yml
                          extra.textbook_version with a 'v' prefix, else v1.0.0)
      --force             overwrite drifted runtime files with the canonical copy (ask the user first)

Rules:
  * Runtime files that are missing are copied. Files identical to canonical are left alone.
    Files that DIFFER are reported as drift and never overwritten without --force — a book
    may deliberately pin an older runtime, and the user should decide.
  * lrs-config.js is the book's identity. It is generated from mkdocs.yml `site_url` only
    when absent, and never overwritten.
  * mkdocs.yml is never edited. If site pages need the runtime (chapter quizzes), the
    script prints the extra_javascript / extra_css lines to add.

OPEN DECISION flagged on every new config: textbookId form. learning-record-store uses a
short id ('lrs'); the LRS seeder uses 'tb-{repo-slug}'. The default here is the repo slug.

Standard library only.
"""

from __future__ import annotations

import argparse
import datetime
import filecmp
import os
import re
import shutil
import sys
from pathlib import Path

RUNTIME = [
    ("js", "lrs-xapi.js"),
    ("js", "lrs-lite-sim.js"),
    ("js", "lrs-sim.js"),
    ("js", "xapi-json-viewer.js"),
    ("css", "lrs-xapi.css"),
]
OPTIONAL = [("js", "quiz-xapi.js")]      # only for books whose chapter quizzes should emit
SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "assets" / "lrs-config.template.js"


def slug(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def find_book_root(start: Path) -> Path:
    d = start.resolve()
    while d != d.parent:
        if (d / "mkdocs.yml").is_file():
            return d
        d = d.parent
    sys.exit(f"no mkdocs.yml above {start}")


def site_url(book: Path) -> str | None:
    for line in (book / "mkdocs.yml").read_text(errors="replace").splitlines():
        m = re.match(r"\s*site_url\s*:\s*['\"]?([^'\"#\s]+)", line)
        if m:
            url = m.group(1)
            return url if url.endswith("/") else url + "/"
    return None


def repo_slug(book: Path) -> str:
    """The seeder namespaces concepts by slug(repo name). Prefer mkdocs.yml repo_url's last
    segment, which survives a checkout under another directory name; fall back to the dir."""
    for line in (book / "mkdocs.yml").read_text(errors="replace").splitlines():
        m = re.match(r"\s*repo_url\s*:\s*['\"]?([^'\"#\s]+)", line)
        if m:
            name = m.group(1).rstrip("/").rsplit("/", 1)[-1]
            name = name.removesuffix(".git")
            if name:
                return slug(name)
    return slug(book.name)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", type=Path, default=Path("."))
    ap.add_argument("--source", type=Path,
                    default=Path(os.environ.get("LRS_RUNTIME_SRC",
                                                "~/Documents/ws/learning-record-store/docs")).expanduser())
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--textbook-id")
    ap.add_argument("--version", help="default: mkdocs.yml extra.textbook_version with a 'v' prefix, else v1.0.0")
    ap.add_argument("--with-quiz", action="store_true", help="also install quiz-xapi.js")
    a = ap.parse_args()

    book = find_book_root(a.book)
    docs = book / "docs"
    src = a.source.resolve()
    problems = 0

    print(f"book:    {book}")
    print(f"source:  {src}")
    if not (src / "js" / "lrs-sim.js").is_file():
        print("!! canonical runtime not found at the source. Pass --source or set LRS_RUNTIME_SRC.")
        return 2
    same_repo = src == docs.resolve()

    files = RUNTIME + (OPTIONAL if a.with_quiz else [])
    for sub, name in files:
        s, d = src / sub / name, docs / sub / name
        rel = f"docs/{sub}/{name}"
        if same_repo:
            print(f"  ok       {rel}  (this IS the canonical repo)")
            continue
        if not d.exists():
            if a.check:
                print(f"  MISSING  {rel}")
                problems += 1
            else:
                d.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(s, d)
                print(f"  copied   {rel}")
        elif filecmp.cmp(s, d, shallow=False):
            print(f"  ok       {rel}")
        elif a.force and not a.check:
            shutil.copy2(s, d)
            print(f"  REPLACED {rel}  (was drifted; --force)")
        else:
            print(f"  DRIFT    {rel}  differs from canonical — not overwritten. Ask the user; "
                  f"diff with: diff {s} {d}")
            problems += 1

    cfg = docs / "js" / "lrs-config.js"
    if cfg.exists():
        text = cfg.read_text()
        keys = {k: (re.search(k + r"\s*:\s*['\"]([^'\"]*)['\"]", text) or [None, None])[1]
                for k in ("siteUrl", "textbookId", "version", "conceptPrefix")}
        print(f"  ok       docs/js/lrs-config.js  {keys}")
        su = site_url(book)
        if su and keys["siteUrl"] and keys["siteUrl"] != su:
            print(f"  !! siteUrl {keys['siteUrl']!r} != mkdocs.yml site_url {su!r} — every IRI would be wrong")
            problems += 1
    elif a.check:
        print("  MISSING  docs/js/lrs-config.js  (generated from mkdocs.yml when run without --check)")
        problems += 1
    else:
        su = site_url(book)
        if not su:
            print("  !! mkdocs.yml has no site_url; cannot generate lrs-config.js. Ask the user.")
            return 2
        prefix = repo_slug(book)
        if not a.version:
            m = re.search(r"^\s*textbook_version\s*:\s*['\"]?([^'\"#\s]+)",
                          (book / "mkdocs.yml").read_text(errors="replace"), re.MULTILINE)
            a.version = ("" if m and m.group(1).startswith("v") else "v") + m.group(1) if m else "v1.0.0"
        tid = a.textbook_id or prefix
        body = (TEMPLATE.read_text()
                .replace("{{SITE_URL}}", su)
                .replace("{{TEXTBOOK_ID}}", tid)
                .replace("{{VERSION}}", a.version)
                .replace("{{CONCEPT_PREFIX}}", prefix)
                .replace("{{DATE}}", datetime.date.today().isoformat()))
        cfg.parent.mkdir(parents=True, exist_ok=True)
        cfg.write_text(body)
        print(f"  created  docs/js/lrs-config.js  siteUrl={su} textbookId={tid} version={a.version} "
              f"conceptPrefix={prefix}")
        if not a.textbook_id:
            print("  NOTE     textbookId defaulted to the repo slug. The form is an OPEN decision "
                  "(learning-record-store uses 'lrs', the seeder 'tb-{slug}') — tell the user.")

    print("\nSite pages (chapter quizzes) need the runtime from mkdocs.yml, which this script "
          "never edits. If wanted, add:\n"
          "  extra_javascript: [js/lrs-config.js, js/lrs-xapi.js, js/lrs-lite-sim.js, js/lrs-sim.js,\n"
          "                     js/xapi-json-viewer.js, js/quiz-xapi.js]\n"
          "  extra_css:        [css/lrs-xapi.css]")
    if a.check:
        print(f"\n{'OK' if not problems else f'{problems} problem(s)'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build a book-level docs/references.md from the per-chapter reference files.

The reference-generator skill produces `docs/chapters/NN-name/references.md` for
every chapter and stops there. A reader who wants to know what the whole book
rests on, or who wants to find a source again without remembering which chapter
it was in, has nowhere to go. Several books in this workspace carry a
hand-written `docs/references.md` that drifts out of step with the chapters as
soon as either changes.

This aggregates the chapter files instead: one entry per distinct source,
deduplicated by URL, listing the chapters that cite it. Regenerate it whenever
chapter references change and it cannot drift.

Usage:
    python3 build-book-references.py /path/to/project
    python3 build-book-references.py /path/to/project --title "References"
    python3 build-book-references.py /path/to/project --dry-run
"""
import argparse
import glob
import os
import re
import sys
from collections import defaultdict

ENTRY = re.compile(r"^\s*\d+\.\s+(.*)$")
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
CHAPTER_DIR = re.compile(r"^(\d+)[-_](.+)$")


def chapter_title(path):
    """Prefer the chapter's H1, falling back to its directory name."""
    index = os.path.join(os.path.dirname(path), "index.md")
    if os.path.exists(index):
        for line in open(index, encoding="utf-8"):
            if line.startswith("# "):
                return line[2:].strip()
    name = os.path.basename(os.path.dirname(path))
    m = CHAPTER_DIR.match(name)
    return (m.group(2) if m else name).replace("-", " ").title()


def parse_entries(path):
    """Yield each numbered reference, joining the lines it wraps across."""
    buf = None
    for line in open(path, encoding="utf-8").read().splitlines() + [""]:
        m = ENTRY.match(line)
        if m:
            if buf:
                yield buf
            buf = m.group(1).strip()
        elif buf is not None and line.strip() and not line.lstrip().startswith("#"):
            buf += " " + line.strip()
        elif buf:
            yield buf
            buf = None


def collect(docs_dir):
    refs, per_chapter, chapters = {}, defaultdict(int), {}
    pattern = os.path.join(docs_dir, "chapters", "*", "references.md")
    for path in sorted(glob.glob(pattern)):
        dirname = os.path.basename(os.path.dirname(path))
        m = CHAPTER_DIR.match(dirname)
        if not m:
            continue
        n = int(m.group(1))
        chapters[n] = {"dir": dirname, "title": chapter_title(path)}
        for text in parse_entries(path):
            link = LINK.search(text)
            url = link.group(2) if link else None
            title = link.group(1) if link else text.split(" - ")[0].strip(" *_")
            if not title:
                continue
            # a source is the same source wherever it is cited, so key on the URL
            key = url or title.lower()
            parts = [p.strip() for p in LINK.sub(r"\1", text).split(" - ")]
            publisher = parts[1] if len(parts) > 1 else ""
            blurb = " - ".join(parts[2:]) if len(parts) > 2 else ""
            entry = refs.setdefault(key, {"title": title, "url": url,
                                          "publisher": publisher, "blurb": blurb,
                                          "chapters": set()})
            entry["chapters"].add(n)
            # keep the fullest description any chapter wrote for it
            if len(blurb) > len(entry["blurb"]):
                entry["blurb"] = blurb
            if len(publisher) > len(entry["publisher"]):
                entry["publisher"] = publisher
            per_chapter[n] += 1
    return refs, per_chapter, chapters


def render(refs, per_chapter, chapters, title, min_shared):
    def cite(r):
        head = f"[{r['title']}]({r['url']})" if r["url"] else f"**{r['title']}**"
        pub = f" - {r['publisher']}" if r["publisher"] else ""
        blurb = f" - {r['blurb']}" if r["blurb"] else ""
        cited = ", ".join(
            f"[{n}](chapters/{chapters[n]['dir']}/index.md)"
            for n in sorted(r["chapters"]) if n in chapters)
        plural = "s" if len(r["chapters"]) > 1 else ""
        return (f"- {head}{pub}{blurb}  \n"
                f"  <small>Cited in chapter{plural} {cited}</small>")

    total_citations = sum(per_chapter.values())
    shared = sorted((r for r in refs.values() if len(r["chapters"]) >= min_shared),
                    key=lambda r: (-len(r["chapters"]), r["title"].lower()))
    alpha = sorted(refs.values(), key=lambda r: r["title"].lower())

    out = [f"""---
title: {title}
description: Every source this book cites, and the chapters that cite it.
---

# {title}

**{len(refs)} distinct sources** across **{total_citations} citations** in
**{len(chapters)} chapters**.

Generated from the per-chapter reference lists, so it cannot drift out of step
with them. Each chapter also carries its own list, which is the better place to
start if you have a chapter in mind.
"""]

    if shared:
        out.append(f"\n## Sources used by more than one chapter\n\n"
                   f"The {len(shared)} the book leans on most.\n")
        out.extend(cite(r) for r in shared)

    out.append("\n## Every source, A to Z\n")
    out.extend(cite(r) for r in alpha)
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", nargs="?", default=".",
                    help="project root containing docs/ (default: .)")
    ap.add_argument("--output", default=None,
                    help="output path (default: <project>/docs/references.md)")
    ap.add_argument("--title", default="References", help="page H1 and title")
    ap.add_argument("--min-shared", type=int, default=2,
                    help="cite count for the 'used by more than one chapter' "
                         "section (default: 2)")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would be written without writing it")
    args = ap.parse_args()

    docs = os.path.join(args.project, "docs")
    if not os.path.isdir(docs):
        sys.exit(f"No docs/ directory under {args.project}")

    refs, per_chapter, chapters = collect(docs)
    if not refs:
        sys.exit("No chapter reference files found at "
                 "docs/chapters/*/references.md. Run reference-generator first.")

    body = render(refs, per_chapter, chapters, args.title, args.min_shared)
    out = args.output or os.path.join(docs, "references.md")

    print(f"{len(refs)} distinct sources from {sum(per_chapter.values())} citations "
          f"across {len(chapters)} chapters")
    thin = [n for n, c in sorted(per_chapter.items()) if c < 5]
    if thin:
        print(f"  chapters with fewer than 5 references: "
              f"{', '.join(str(n) for n in thin)}")
    if args.dry_run:
        print(f"  (dry run — would write {out})")
        return 0

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(body)
    print(f"Wrote {out}")
    print("Add it to mkdocs.yml nav as:  - References: references.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Find an existing, already-vetted photo of a part before sourcing a new one.

Dan's workspace holds 100+ sibling textbook repos that have been accumulating
component photography for years. Almost every part in a Moving Rainbow kit has
already been photographed for some other book, and reusing that image is
strictly better than hunting for a new one: it is known to be license-clean,
it matches the house look, and it costs nothing.

So: search here first, Wikimedia second, generate an image-description.md only
as a last resort.

Usage:
    python3 find_part_image.py breadboard
    python3 find_part_image.py momentary push button --limit 15
    python3 find_part_image.py "screw terminal" --deep      # walk all of docs/, not just docs/img/
    python3 find_part_image.py photoresistor --ws ~/Documents/ws --repo .

Ranking favors filename matches on every keyword, then the current repo, then
larger images (a 1200px product shot beats a 200px thumbnail for print).
"""

import argparse
import os
import re
import sys
from pathlib import Path

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
SKIP_DIRS = {".git", "node_modules", "site", "venv", ".venv", "__pycache__",
             "dist", "build", ".cache"}


def tokens(text: str):
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if t]


def loose(a: str, b: str) -> bool:
    """Stem-ish overlap, but only for tokens long enough to mean something.

    Without the length floor, a one-letter token like the "a" in "a-boring-map"
    is a substring of nearly every keyword, and the results fill with noise.
    """
    return len(a) >= 4 and len(b) >= 4 and (a in b or b in a)


def score(path: Path, keys, repo_root: Path):
    """Higher is better; None means 'not a match at all'."""
    name = path.stem.lower()
    name_tokens = set(tokens(name))
    hits = 0
    for k in keys:
        if k in name_tokens:
            hits += 3          # whole-word hit in the filename: strong signal
        elif k in name:
            hits += 2          # substring hit ("buttons" matching "button")
        elif any(loose(k, t) for t in name_tokens):
            hits += 1          # loose stem overlap
    if hits == 0:
        return None
    s = hits * 100
    if len(keys) > 1 and all(
        k in name or any(loose(k, t) for t in name_tokens) for k in keys
    ):
        s += 250               # matched every keyword -- almost always the right file
    try:
        if repo_root in path.parents:
            s += 200           # local images need no cross-repo copy
    except Exception:
        pass
    try:
        s += min(path.stat().st_size // 20000, 60)  # nudge toward higher-res files
    except OSError:
        pass
    return s


def dimensions(path: Path):
    try:
        from PIL import Image  # optional; nice-to-have, not required
        with Image.open(path) as im:
            return f"{im.width}x{im.height}"
    except Exception:
        return "?"


def iter_images(ws: Path, repo: Path, deep: bool):
    roots = []
    # The current repo is always searched in full -- kit-local images live beside
    # their index.md, not in docs/img/.
    if (repo / "docs").is_dir():
        roots.append(repo / "docs")
    for child in sorted(ws.iterdir()):
        if not child.is_dir() or child.resolve() == repo.resolve():
            continue
        docs = child / "docs"
        if not docs.is_dir():
            continue
        roots.append(docs if deep else docs / "img")
    for root in roots:
        if not root.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames
                           if d not in SKIP_DIRS and not d.startswith(".")]
            for fn in filenames:
                if Path(fn).suffix.lower() in IMAGE_EXT:
                    yield Path(dirpath) / fn


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("keywords", nargs="+", help="part keywords, e.g. momentary push button")
    p.add_argument("--ws", default=str(Path.home() / "Documents" / "ws"),
                   help="workspace root holding the sibling repos")
    p.add_argument("--repo", default=".", help="the repo the guide is being written in")
    p.add_argument("--deep", action="store_true",
                   help="walk all of each repo's docs/, not just docs/img/ (slower)")
    p.add_argument("--limit", type=int, default=10)
    args = p.parse_args()

    keys = tokens(" ".join(args.keywords))
    if not keys:
        print("no usable keywords", file=sys.stderr)
        return 1

    ws = Path(args.ws).expanduser()
    repo = Path(args.repo).expanduser().resolve()
    if not ws.is_dir():
        print(f"workspace not found: {ws}", file=sys.stderr)
        return 1

    results = []
    for img in iter_images(ws, repo, args.deep):
        s = score(img, keys, repo)
        if s is not None:
            results.append((s, img))
    results.sort(key=lambda r: (-r[0], str(r[1])))

    # A lone weak hit is worse than no hit: it sends you off to crop a photo of
    # the wrong thing. Treat everything under one solid whole-word match as noise.
    strong = [r for r in results if r[0] >= 300]
    if strong:
        results = strong
    else:
        results = []

    if not results:
        print(f"No local match for {' '.join(keys)!r}.")
        print("Next: try Wikimedia Commons, then fall back to image-description.md.")
        return 0

    print(f"{len(results)} match(es) for {' '.join(keys)!r} -- top {min(args.limit, len(results))}:\n")
    for s, img in results[: args.limit]:
        try:
            kb = img.stat().st_size // 1024
        except OSError:
            kb = 0
        where = "THIS REPO" if repo in img.parents else img.relative_to(ws).parts[0]
        print(f"  [{s:5d}] {img}")
        print(f"          {where}  {dimensions(img)}  {kb} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
generate-poster-thumbnails.py — Generate lightweight thumbnails for the
poster gallery index page (docs/posters/index.md).

Why this script exists
-----------------------
The poster gallery index displays every poster in a 3-column CSS grid
(`.grid.poster-grid`, ~600px columns), one card per poster. Left
unoptimized, each card's `<img>` points straight at the full-size
verified-infographic PNG (typically 1536x1024, 2-3 MB apiece). A gallery
of ~90 posters then ships 200+ MB on a single page load even though the
grid only ever displays each image at ~600px wide.

This script generates a compressed JPEG thumbnail next to each poster's
full-size PNG and rewrites the gallery index.md so the grid cards
reference the thumbnail instead. It does NOT touch each poster's own
detail page (main.html) — the interactive callout/grid overlay keeps
using the full-size PNG, since that page needs full resolution for
zoom/hover accuracy.

Measured result on a 86-poster gallery: 233.5 MB -> 11.9 MB (~95%
reduction), no visible quality loss at gallery-card size.

Usage
-----
    # Run from the project root, or pass --posters-dir explicitly
    python3 $BK_HOME/skills/microsim-generator/scripts/posters/generate-poster-thumbnails.py

    python3 .../generate-poster-thumbnails.py --posters-dir docs/posters --width 900 --quality 82

    # Preview without writing any files
    python3 .../generate-poster-thumbnails.py --dry-run

Requires: Pillow (`pip install Pillow`)

Conventions assumed
--------------------
- Each poster lives in its own directory: <posters-dir>/<slug>/<slug>.png
- The gallery index page is <posters-dir>/index.md and references each
  poster image as a markdown image link:
    [![Alt text](./<slug>/<slug>.png)](./<slug>/index.md)
  (the standard grid-cards layout produced by this skill's poster
  gallery step). Only the image src is rewritten — the link target
  (index.md) is left untouched.

Safe to re-run: thumbnails and the index.md rewrite are idempotent.
"""

import argparse
import re
from pathlib import Path

from PIL import Image

THUMB_SUFFIX = "-thumb.jpg"


def find_posters(posters_dir: Path):
    """Yield (slug, full_png_path) for every poster directory that has a
    full-size PNG matching its directory name."""
    for entry in sorted(posters_dir.iterdir()):
        if not entry.is_dir():
            continue
        slug = entry.name
        full_png = entry / f"{slug}.png"
        if full_png.exists():
            yield slug, full_png


def generate_thumbnail(full_png: Path, width: int, quality: int) -> Path:
    thumb_path = full_png.with_name(full_png.stem + THUMB_SUFFIX)
    with Image.open(full_png) as img:
        img = img.convert("RGB")
        if img.width > width:
            height = round(img.height * (width / img.width))
            img = img.resize((width, height), Image.LANCZOS)
        img.save(thumb_path, "JPEG", quality=quality, optimize=True)
    return thumb_path


def update_index_md(index_md: Path) -> int:
    """Point every poster card image at its -thumb.jpg instead of the
    full-size .png. The link that wraps the image (to index.md) is left
    untouched because it matches a different pattern."""
    text = index_md.read_text()
    pattern = re.compile(r"\(\./([a-zA-Z0-9_-]+)/\1\.png\)")
    new_text, count = pattern.subn(rf"(./\1/\1{THUMB_SUFFIX})", text)
    index_md.write_text(new_text)
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--posters-dir", default="docs/posters", help="Path to the posters directory (default: docs/posters)")
    parser.add_argument("--width", type=int, default=900, help="Thumbnail width in pixels (default: 900)")
    parser.add_argument("--quality", type=int, default=82, help="JPEG quality 1-95 (default: 82)")
    parser.add_argument("--dry-run", action="store_true", help="Report what would happen without writing files")
    parser.add_argument("--skip-index-update", action="store_true", help="Only generate thumbnails, don't rewrite index.md")
    args = parser.parse_args()

    posters_dir = Path(args.posters_dir).resolve()
    index_md = posters_dir / "index.md"

    posters = list(find_posters(posters_dir))
    if not posters:
        print(f"No posters found under {posters_dir}")
        return

    total_before = 0
    total_after = 0
    for slug, full_png in posters:
        before = full_png.stat().st_size
        total_before += before
        if args.dry_run:
            print(f"[dry-run] would generate thumbnail for {slug} ({before / 1024:.0f} KB source)")
            continue
        thumb_path = generate_thumbnail(full_png, args.width, args.quality)
        after = thumb_path.stat().st_size
        total_after += after
        print(f"{slug}: {before / 1024:.0f} KB -> {after / 1024:.0f} KB  ({thumb_path.relative_to(posters_dir.parent)})")

    print(f"\n{len(posters)} posters processed.")
    if not args.dry_run:
        print(f"Full-size total: {total_before / 1024 / 1024:.1f} MB")
        print(f"Thumbnail total: {total_after / 1024 / 1024:.1f} MB")

        if not args.skip_index_update:
            if index_md.exists():
                count = update_index_md(index_md)
                print(f"Updated {count} image reference(s) in {index_md.relative_to(posters_dir.parent)}")
            else:
                print(f"No index.md found at {index_md}; skipped index rewrite.")


if __name__ == "__main__":
    main()

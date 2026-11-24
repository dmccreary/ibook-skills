"""Trim a PNG to its visible content and add an exact transparent border.

Usage:
    trim-padding-from-image.py <png-path> [<png-path> ...]

The visible content is every pixel with alpha > THRESH. The script crops to
that bounding box and then places it on a fully transparent canvas with
exactly PADDING px on all four sides. The result always has 4/4/4/4 px
content margins and fully transparent corners, which is what the mascot test
page (docs/learning-graph/mascot-test.md) checks for.

Padding is added, not just preserved: when the artwork comes within PADDING px
of an edge (common for AI-generated poses), the canvas grows on that side.
An earlier version only cropped and clamped at the image edge, so those
sides kept a 2-3 px margin and the mascot test page still failed after
running the script.

Each argument must be an explicit path to a .png file. The script overwrites
the file in place. The script does NOT walk any directory — passing zero
arguments is an error, not a request to batch-process docs/img/mascot/.

This explicit-argument design exists because an earlier version silently
ignored sys.argv and walked docs/img/mascot/, which was a footgun: the
documented invocation pattern looked like it processed a single named file
but actually overwrote every PNG in the mascot directory.
"""
import sys
from pathlib import Path
from PIL import Image

THRESH = 10   # alpha <= 10 treated as padding
PADDING = 4   # exact transparent border on every side after trimming


def trim(path: Path) -> None:
    img = Image.open(path).convert('RGBA')
    visible = img.getchannel('A').point(lambda a: 255 if a > THRESH else 0)
    bbox = visible.getbbox()   # (left, top, right, bottom), right/bottom exclusive
    if bbox is None:
        print(f'skip {path.name}: image is fully transparent')
        return

    w, h = img.size
    left, top, right, bottom = bbox
    margins = (left, top, w - right, h - bottom)
    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    corners_clear = all(img.getpixel(c)[3] == 0 for c in corners)
    if margins == (PADDING,) * 4 and corners_clear:
        print(f'unchanged {path.name}: already {PADDING}px border ({img.size})')
        return

    content = img.crop(bbox)
    out = Image.new('RGBA',
                    (content.width + 2 * PADDING, content.height + 2 * PADDING),
                    (0, 0, 0, 0))
    out.paste(content, (PADDING, PADDING))
    out.save(path, optimize=True)
    print(f'trimmed {path.name}: {img.size} -> {out.size} '
          f'(margins L/T/R/B were {"/".join(map(str, margins))}px, now '
          f'{PADDING}px each)')


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        sys.stderr.write(
            "usage: trim-padding-from-image.py <png-path> [<png-path> ...]\n"
            "Each argument must be an explicit path to a .png file.\n"
        )
        return 2
    rc = 0
    for arg in argv[1:]:
        path = Path(arg)
        if not path.is_file():
            print(f'skip {arg}: not a file')
            rc = 1
            continue
        if path.suffix.lower() != '.png':
            print(f'skip {arg}: not a .png')
            rc = 1
            continue
        trim(path)
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv))

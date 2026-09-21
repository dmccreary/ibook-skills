"""MkDocs-only hook: warn when this site is previewed with `mkdocs serve`.

This book is built and deployed with Zensical. MkDocs renders it differently --
most visibly it does not rewrite relative <iframe src> paths, so MicroSims
embedded from top-level pages show up as broken frames.

Zensical does not load `hooks:` entries from mkdocs.yml, so this file only ever
runs under MkDocs. The warning is emitted for `serve` only, never for `build`,
so that `mkdocs build --strict` (the authoritative check) still passes cleanly.

Installed by the book-installer skill, feature 41 (mkdocs-serve-warning.md).
Delete this file and its `hooks:` entry when MkDocs is no longer installed.
"""

import logging
import sys

log = logging.getLogger("mkdocs.hooks.serve-warning")

# One logical line per sentence group, no manual padding: in a terminal MkDocs'
# log formatter wraps each line to the window width and indents continuation
# lines itself, so hand-aligned text would end up double-indented.
MESSAGE = (
    "You are running `mkdocs serve`, but this book is built and deployed with "
    "Zensical.\n"
    "MkDocs renders it differently: it does not rewrite relative <iframe src> "
    "paths, so MicroSims embedded from top-level pages appear as broken frames "
    "in this preview.\n"
    "Use `zensical serve` instead (see AGENTS.md)."
)


def _subcommand():
    """The mkdocs subcommand actually typed: the first non-option argument."""
    return next((arg for arg in sys.argv[1:] if not arg.startswith("-")), None)


def on_startup(command, dirty):
    # `mkdocs serve --clean` reports command == "build", so also check argv.
    if command == "serve" or _subcommand() == "serve":
        log.warning(MESSAGE)

#!/usr/bin/env bash
# link-skill.sh <skill> <book>
#
# Enable an optional skill in one book by linking it into that book's
# project-level .claude/skills/ directory:
#
#   <book>/.claude/skills/<skill> -> ../../../ibook-skills/optional-skills/<skill>
#
# Optional skills live in ibook-skills/optional-skills/ and are never linked
# into ~/.claude/skills, so they only load in the books that opt in.
#
# <book> may be a repo name in the workspace (e.g. moving-rainbow) or a path.
# The book must be a sibling checkout of ibook-skills for the relative link to
# resolve. Safe to re-run: an existing correct link is left alone, a wrong
# symlink is replaced, and a real file or directory is never overwritten.
set -euo pipefail

if [ $# -ne 2 ]; then
  echo "usage: $(basename "$0") <skill> <book>" >&2
  exit 2
fi
skill="${1%/}"
book_arg="${2%/}"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
ibook_dir="$(cd "$script_dir/.." && pwd -P)"
ws_dir="$(cd "$ibook_dir/.." && pwd -P)"
skill_src="$ibook_dir/optional-skills/$skill"

if [ ! -f "$skill_src/SKILL.md" ]; then
  echo "error: no optional skill '$skill' (expected $skill_src/SKILL.md)" >&2
  exit 1
fi

if [ -d "$book_arg" ]; then
  book_dir="$(cd "$book_arg" && pwd -P)"
elif [ -d "$ws_dir/$book_arg" ]; then
  book_dir="$(cd "$ws_dir/$book_arg" && pwd -P)"
else
  echo "error: book '$book_arg' not found (as a path or under $ws_dir)" >&2
  exit 1
fi

if [ "$(dirname "$book_dir")" != "$ws_dir" ]; then
  echo "error: $book_dir is not a sibling of ibook-skills ($ws_dir); the relative link would not resolve" >&2
  exit 1
fi

target="../../../ibook-skills/optional-skills/$skill"
link_dir="$book_dir/.claude/skills"
link="$link_dir/$skill"
book_name="$(basename "$book_dir")"

mkdir -p "$link_dir"

if [ -L "$link" ]; then
  current="$(readlink "$link")"
  if [ "$current" = "$target" ]; then
    echo "ok: $book_name/.claude/skills/$skill -> $target (already linked)"
    exit 0
  fi
  echo "replacing symlink $book_name/.claude/skills/$skill (was -> $current)"
  rm "$link"
elif [ -e "$link" ]; then
  echo "error: $link exists and is a real file or directory; refusing to overwrite it" >&2
  echo "       move or delete it yourself, then re-run" >&2
  exit 1
fi

ln -s "$target" "$link"

if [ -f "$link/SKILL.md" ]; then
  echo "linked: $book_name/.claude/skills/$skill -> $target"
else
  echo "error: created $link but it does not resolve to a SKILL.md" >&2
  exit 1
fi

---
name: mkdocs-serve-warning
description: Installs a MkDocs-only hook that logs a clear warning when a Zensical-built intelligent textbook is previewed with `mkdocs serve`. Recommended for every Zensical-designed book during the MkDocs-to-Zensical transition period, while MkDocs is still installed alongside Zensical.
---

# MkDocs-Serve Warning — Feature #41: Zensical Transition Guard

This guide installs a small MkDocs-only hook that prints a warning when someone
runs `mkdocs serve` on a book that is really built and deployed with
**Zensical**. It changes no output and Zensical never loads it.

## Why This Exists

During the transition from MkDocs to Zensical, both tools are usually
installed side by side — sometimes in the same conda environment — and
nothing stops a person from typing `mkdocs serve` out of habit. It starts
without complaint, but it renders the book differently. The most visible
difference: **MkDocs does not rewrite relative `<iframe src>` paths**, so a
MicroSim embedded as `sims/<id>/main.html` from a page at the docs root shows
as a broken frame. `zensical build` and `zensical serve` both rewrite it to
`../sims/<id>/main.html`.

Nothing tells the reader they are looking at the wrong renderer. A bug report
blaming `zensical serve` for exactly this symptom
([zensical/zensical#943](https://github.com/zensical/zensical/issues/943))
was closed as not reproducible — the behavior it described is what
`mkdocs serve` does. The warning turns that silent confusion into one clear
console message.

## When to Use — and When Not To

**Install it when both are true:**

1. The book is built and deployed with Zensical. Signs: `zensical` in
   `.github/workflows/docs.yml`, a Zensical mention in `AGENTS.md`, a
   `zensical.toml`, or the user says so.
2. MkDocs is still installed or still able to build the book (a `mkdocs.yml`
   exists — Zensical reads the same file).

**Do NOT install it when:**

- The book is built and deployed with MkDocs. The message says "this book is
  built and deployed with Zensical", which would be false and confusing. When
  the builder is unclear, ask the user; do not guess.
- The project has no `mkdocs.yml` (native `zensical.toml` only). MkDocs cannot
  build it at all, so there is nothing to warn about.

Remove it when the transition ends (see [Removal](#removal)).

## What This Guide Creates

1. **`hooks/mkdocs_serve_warning.py`** — the hook, copied byte-for-byte from
   `assets/mkdocs-serve-warning/mkdocs_serve_warning.py`
2. **A `hooks:` entry in `mkdocs.yml`** — appended to the existing list if there
   is one
3. **An `AGENTS.md` note** — only if the project's `AGENTS.md` has a rule
   against `hooks:`

## Prerequisites

- An existing MkDocs Material / Zensical project with a `mkdocs.yml`
- MkDocs **1.4 or newer** (the `on_startup` event it relies on was introduced
  in 1.4; on older versions the hook silently never fires)

## Workflow

### Step 1: Confirm the Builder

Check the signs listed under [When to Use](#when-to-use-and-when-not-to). If
the book deploys with MkDocs, stop and tell the user why this feature does not
apply.

### Step 2: Copy the Hook

```bash
mkdir -p hooks
cp "$BK_HOME/skills/book-installer/assets/mkdocs-serve-warning/mkdocs_serve_warning.py" hooks/
```

(`$BK_HOME` points at the ibook-skills checkout, e.g.
`~/Documents/ws/ibook-skills`.) Copy the file verbatim — do not retype it. The
four behaviors described under [Design Rules](#design-rules) are all
load-bearing.

### Step 3: Register It in `mkdocs.yml`

**Check for an existing top-level `hooks:` key first.** MkDocs does not reject
a duplicate key — the second `hooks:` silently replaces the first, so adding a
second block would quietly drop the hooks already registered (verified). A book
scaffolded by `init-textbook` already has one, for the social-preview hook, so
*append* to it:

```yaml
hooks:
  - plugins/social_override.py            # already there (init-textbook scaffold)
  - hooks/mkdocs_serve_warning.py         # add this line
```

If there is no `hooks:` key, add:

```yaml
# MkDocs-only guard: warns when this Zensical-built book is previewed with
# `mkdocs serve`. Zensical never loads `hooks:` entries. Warns on `serve`
# only, so `mkdocs build --strict` is unaffected.
hooks:
  - hooks/mkdocs_serve_warning.py
```

Paths in `hooks:` are relative to `mkdocs.yml`.

### Step 4: Customize the Message (Optional)

The shipped text is deliberately generic. If the book has a page that actually
breaks under MkDocs, name it — find candidates with:

```bash
grep -rln '<iframe src="sims/' docs --include='*.md' | grep -v '^docs/sims/'
```

Keep the message as one logical line per sentence group with **no manual
padding** (see Design Rules).

### Step 5: Update `AGENTS.md` If It Forbids Hooks

Some Zensical projects forbid `hooks:` because Zensical ignores them (a hook
that rewrites page output would silently not run there). If the project's
`AGENTS.md` has such a rule, name this hook as the one sanctioned exception,
and add its file to the "where things live" table:

> The one sanctioned hook is `hooks/mkdocs_serve_warning.py`: a MkDocs-only
> guard that warns on `mkdocs serve`. Zensical never loads it, and it must
> stay silent on `mkdocs build` so `mkdocs build --strict` still passes.

### Step 6: Verify

Never start `mkdocs serve` yourself — the author runs it in their own
terminal. Verify without a server:

```bash
# 1. The authoritative check still passes and prints no warning
mkdocs build --strict -d "$(mktemp -d)" && echo "strict build OK"

# 2. Fire MkDocs' own startup event as `serve` would (no server started)
python3 - <<'EOF'
import logging, sys
from mkdocs.config import load_config
logging.basicConfig(level=logging.INFO, format="%(levelname)s -  %(message)s")
sys.argv = ["mkdocs", "serve"]
load_config(config_file="mkdocs.yml").plugins.on_startup(command="serve", dirty=False)
EOF
```

Expect step 1 to exit 0 with no warning, and step 2 to print the warning.
Then confirm Zensical is unaffected: `zensical build` should exit 0 with
output identical to before. Finally, ask the user to run `mkdocs serve` once
in their own terminal and confirm the warning appears above the build output.

## Design Rules

These are why the shipped file looks the way it does. Do not "simplify" them
away.

- **Zensical never loads it.** `hooks:` entries are ignored by Zensical
  (verified with an import probe on 0.0.62 and 0.0.63), so the file only ever
  runs under MkDocs and the same `mkdocs.yml` stays valid for both builders.
- **Warn on `serve` only, never on `build`.** A warning during `mkdocs build`
  makes `mkdocs build --strict` — the authoritative check — fail.
- **Check `sys.argv` as well as `command`.** MkDocs reports `mkdocs serve
  --clean` as `command == "build"`, which a check on `command` alone would miss.
- **Don't hand-indent the message.** In a real terminal MkDocs wraps each log
  line to the window width and indents continuation lines by 11 columns itself.
  Manual padding stacks on top and misaligns the text.
- **Never put page-output logic in a hook.** Zensical would silently skip it.
  Markup injection belongs in a `theme.custom_dir` template override.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| No warning on `mkdocs serve` | MkDocs older than 1.4, or wrong path in `hooks:` | `mkdocs --version`; check the path is relative to `mkdocs.yml` |
| `mkdocs build --strict` now fails | The hook was edited to warn on `build` | Restore the `serve`-only check |
| Warning text is indented twice | Hand-aligned continuation lines in `MESSAGE` | Remove the manual padding |
| Social-preview meta tags vanished after install (no error) | A second top-level `hooks:` key silently replaced the first list | Merge both entries into a single `hooks:` list (Step 3) |
| Warning appears under `zensical serve` | Should be impossible — Zensical never imports hooks | Confirm which command is really running (`which zensical`, `which mkdocs`) |

## Removal

When the transition ends and MkDocs is no longer installed or used, delete
`hooks/mkdocs_serve_warning.py`, remove its line from the `hooks:` list (and
the whole key if it was the only entry), and drop the `AGENTS.md` exception.

## Reference Implementation

The reference implementation is
[zensical-test](https://github.com/dmccreary/zensical-test) (see its
`hooks/mkdocs_serve_warning.py`). Its migration guide,
[Step 9](https://dmccreary.github.io/zensical-test/migration-steps/), gives
the same recommendation for books migrated from MkDocs.

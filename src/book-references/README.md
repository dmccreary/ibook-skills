# Book-level references

`build-book-references.py` aggregates the per-chapter `references.md` files that
the `reference-generator` skill produces into a single `docs/references.md`.

## Why

The skill generates `docs/chapters/NN-name/references.md` for every chapter and
stops there. That answers "what should I read next about *this*" and leaves two
things unanswered: what the whole book rests on, and where a reader can find a
source again without remembering which chapter cited it. A source cited by six
chapters appears as six unrelated entries and looks like six sources.

Several books in this workspace carry a hand-written `docs/references.md`. It
drifts out of step with the chapters the moment either changes, and nothing
warns anyone. Generating it means it cannot.

## Usage

```bash
python3 "$BK_HOME/src/book-references/build-book-references.py" .

# preview without writing
python3 "$BK_HOME/src/book-references/build-book-references.py" . --dry-run

# elsewhere, or with a different heading
python3 "$BK_HOME/src/book-references/build-book-references.py" . \
    --output docs/bibliography.md --title Bibliography
```

Then add it to `mkdocs.yml`:

```yaml
  - References: references.md
```

## What it does

- Parses every numbered entry in `docs/chapters/*/references.md`, joining entries
  that wrap across lines.
- Deduplicates by URL, so a source cited by several chapters is one entry that
  names them all. Sources without a URL fall back to their title.
- Keeps the fullest description and publisher any chapter wrote for a source.
- Emits a "used by more than one chapter" section ahead of the A-to-Z list.

## Two numbers worth reading

It reports **any chapter with fewer than five references**, which usually means
the per-chapter step was skipped or a chapter was added afterwards.

It also reports distinct sources against total citations. If those are nearly
equal, no source is doing work across chapters — in a book built on a concept
graph that usually means the chapters were researched in isolation rather than
as one book. On the books tested: 90 sources from 150 citations, and 257 from
320, both healthy; one book at 160 from 170, which is the pattern to look at.

## Exit behaviour

Exits non-zero with an explanation if there is no `docs/` directory, or if no
per-chapter reference files exist yet — in which case run `reference-generator`
first.

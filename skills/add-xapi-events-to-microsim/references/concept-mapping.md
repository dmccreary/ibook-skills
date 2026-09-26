# Mapping interactions to concept ids

A statement without a `concept_id` is dropped by the concept rollup's own
`WHERE notEmpty(concept_ids)`. The sim keeps emitting and logging, and quietly
contributes no concept evidence. A statement with the **wrong** `concept_id` is worse:
it credits mastery of something the student never touched. This step is where the
skill earns its keep.

## The id format: namespaced learning-graph ConceptIDs

Every book's learning graph numbers its concepts 1..N, so `42` collides across books.
The LRS seeder (`learning-record-store/src/lrs/catalog.py`, "CONCEPT IDS ARE
NAMESPACED") prefixes each id with the **repo slug**:

```
{conceptPrefix}-{ConceptID}        e.g.  biology-42,  learning-record-store-353
conceptPrefix = slug(repo name)    (lowercase, runs of non [a-z0-9] -> '-')
```

The seeder slugs the repo's directory name. `install-runtime.py` takes the name from
`mkdocs.yml` `repo_url` (which survives a checkout under another directory name) and
falls back to the directory. On 2026-09-26 the two agreed for all 90 workspace books
that have a `repo_url`. The other 2 have none and use the directory name.

The book's `docs/js/lrs-config.js` holds `conceptPrefix`. In code, always write
`LRS.conceptId(353)`, never the literal string, so the id follows the book's config.
In `metadata.json` write the full literal id (`"learning-record-store-353"`), because
that file is read by tools that don't run the runtime.

A statement's `concept_id` then joins straight to the `Concept` vertex the seeder wrote.
That is the whole point.

## The learning graph file

`docs/learning-graph/learning-graph.csv`:

```
ConceptID,ConceptLabel,Dependencies,TaxonomyID
353,Chaos Kill Test,334|335|336,OPS
```

- `Dependencies` are pipe-separated ConceptIDs, numbered per book.
- **Row order is not topological.** Forward references are common. Don't infer anything
  from position.
- `taxonomy-names.json` names the `TaxonomyID` categories, and helps you judge whether
  a candidate is in the right area of the book.
- `metadata.json` in the same folder gives the book's real title.

## Finding candidates

```bash
python3 $SKILL_DIR/scripts/find-concepts.py --book <book-root> --sim docs/sims/<name>
python3 $SKILL_DIR/scripts/find-concepts.py --book <book-root> "data loss" "prediction"
```

With `--sim`, the script builds search terms from the sim's `metadata.json` (`title`,
`description`, `concepts`, `subject`), its `index.md` title, and control labels found in
the JS. It prints ranked candidates with their namespaced ids and taxonomy. It only
proposes. Scores are token overlap plus fuzzy similarity, which is exactly the kind of
match that pairs *Animal Cell* with nothing and *Cell Membrane* with *Membrane Proteins*.

## Choosing: the rules

1. **One concept per statement** (contract §6). Choose the concept the interaction is
   *evidence for*, not everything the sim touches.
   - A slider for amplitude is evidence of *amplitude*, not of *sine wave*.
   - A Start/Pause run is evidence of engaging with the whole simulation, so it takes
     the page-level concept.
   - A diagram node is evidence of the concept that node names.
   - A question is evidence of the concept it tests.
2. **Page-level concept** (`LRSSim.create({concept})`): the one concept the whole sim is
   about. It goes on runs, page dwell, and the Compact summary. Usually it's the concept
   the sim's lesson page teaches. If the sim's chapter lists concepts, it's among them.
3. **Several objects may share a concept.** Scientific-method maps
   Decision1/Accept/Revise all to `hypothesis-testing`. The concept rollup's grain is
   (student, concept), so they compress into one vertex. That's the grain working, not
   a loss.
4. **Same concept for explore and quiz.** `#nucleus` (Control) and `#q-nucleus`
   (Question) both carry the nucleus concept, and reconverge in the concept rollup.
5. **Nothing matches: warn, never guess.** But first check what the book itself says.
   - If the chapter, or a sibling sim's spec, pairs the object with a concept, that is
     **evidence, not a guess**. For example, chapter 19 pairs "Gateway/Kafka: Kafka
     Unavailable Failure". Use the pairing and cite it in the report. Guessing means
     choosing the nearest label with nothing in the book to back it.
   - Otherwise leave that object's `concept` undefined, and **still emit its
     statements**. They land in the log, which is the system of record, but not in the
     concept rollup. (Animal-cell returns early for an unmapped callout and emits
     nothing. That predates this rule; don't copy it.)
   - If the objects come from data (hotspots, nodes), make the adapter
     `console.warn('[<sim>] no concept mapped for "<label>" …')`, so a later upstream
     addition fails loudly instead of silently.
   - Tell the user which objects are unmapped, and suggest the fix: add the concept to the
     learning graph, or accept the gap.
6. **A node that covers several concepts** (vis-network concept maps, compound
   diagram steps): multi-concept statements are not expressible in contract v1 (§12
   item 5). Pick the node's primary concept. For a concept-map node whose id *is* a
   ConceptID, that's the node itself. Record the others in your report. Don't emit two
   statements for one act to smuggle in a second concept; that double-counts engagement.

## Books without a usable learning graph

If `docs/learning-graph/learning-graph.csv` is missing, you can't produce namespaced
ids. Stop and ask the user. Options are to generate the learning graph first
(`learning-graph-generator`), or to use clearly-illustrative slug ids for a demo sim.
The second option is what this repo's physics demos do: `motion` and `amplitude` are
not in the LRS learning graph, and their `index.md` says so. Never mix the two forms
silently in one sim.

## Recording the map

Put the map in the sim's `metadata.json` `xapi` block:

```json
"xapi": {
  "concept": "learning-record-store-15",
  "objects": {
    "actor":   "learning-record-store-9",
    "verb":    "learning-record-store-10",
    "object":  "learning-record-store-11",
    "result":  "learning-record-store-13",
    "context": "learning-record-store-14"
  }
}
```

- `concept` is the page-level concept, and `objects` maps each fragment key to its
  concept. Omit an unmapped key rather than writing `null`, and list it in your report.
- For generated keys (`q-{service}` for eight services), list every key the sim can
  produce.
- `check-xapi.py` compares every emitted statement against this map, and fails on a
  mismatch. So the map and the code can't drift silently, and the MicroSim catalog
  gets exact concept ids rather than inferring them from title matches.
- The runtime ignores these two keys when it resolves policy, so they never change the
  sim's mode.

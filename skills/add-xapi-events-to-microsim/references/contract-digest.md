# Producer contract digest

The normative document is
`~/Documents/ws/learning-record-store/docs/specs/xapi-producer-contract-v1.md`. This is
a digest of the rules an instrumented sim must never break. The runtime enforces most of
them by construction (`lrs-xapi.js` throws or warns). Know them anyway, so you can
recognise a violation in `check-xapi.py`'s output.

| § | Rule | Enforced by |
|---|---|---|
| 1 | `object.id` for a page is `{siteUrl}` + the page's nav path **with a trailing slash**. Never `main.html`, never localhost, never another site. The sim is `…/sims/<name>/`. | `LRS.pageIri()` derives it; `validate()` warns on `main.html`/localhost/non-https |
| 2 | A sub-activity's fragment is its **stable local name**: `#speed-slider`, `#hypothesis`. A fixed-order question is `#q{N}`, one-based. A shuffled or generated question is `#q-{name}`. | You. The runtime can't know if your key is stable. |
| 3 | **Exactly three verbs.** `answered` requires `result.success` (bool). `experienced` requires `result.duration`. `interacted` requires nothing; values go in `result.extensions`. | `LRS.build` throws on other verbs; warns on a missing success/duration |
| 4 | `context.contextActivities.grouping[0].id` = `{siteUrl}textbook/{textbookId}/{version}` on **every** statement. `parent[0]` = the page IRI for `answered` (and Controls). | `LRS.build` from `lrs-config.js` |
| 5 | `object.definition.type`: `lesson` becomes **Page**, `simulation` becomes **MicroSim** (the page, no fragment), `cmi.interaction` becomes **Question**, and `interaction` becomes **Control** (a fragment-qualified sub-activity). One object, one type; the UI mode never changes it. | `LRS.build` throws on other types; warns on a fragment typed MicroSim/Page |
| 6 | `context.extensions["https://w3id.org/lrs/ext/concept_id"]` = **one** concept id string. Absent means no concept evidence. | You, via `concept:` on every handle |
| 7 | Start/Pause = **one** `experienced` per run, emitted on Pause (or a flush), object = the page. Nothing on Start. Under 250 ms emits nothing. | `lrs.runner` |
| 7.1 | Presses may add `interacted` with `action`, carrying no duration, and **never on a flush**. | `lrs.button` |
| 8 | Producers never send `district_id`, `student_key`, `stored_at`, `section_id`, `voided_by` or `provisional`. | `LRS.build` doesn't set them |
| 9 | Transport: a JSON array POST, all-or-nothing. **Nothing POSTs yet**; `LRSLite.record()` is the seam. | n/a |

## The shapes a sim produces

```
interacted  Control   …/sims/x/#speed-slider   result.extensions {value, previous-value}      parent = page
interacted  Control   …/sims/x/#hypothesis     result.duration + extensions {engagement-mode}  parent = page
interacted  Control   …/sims/x/#start-pause-control  result.extensions {action}                parent = page
experienced MicroSim  …/sims/x/                result.duration + extensions {run-ended-by}     (run or page dwell)
answered    Question  …/sims/x/#q-kafka        result {success, score.scaled, response, duration}  parent = page
experienced MicroSim  …/sims/x/                Compact summary: result.duration, result.extensions
                      {xapi_mode:'compact', end_reason, active_ms, session_ms, interaction_count,
                       controls:{key:{n,min,max,last,modes,ms,concept,reversals}}, runs:{count,ms}},
                      context.extensions {statements_represented: N}
```

Every statement carries `grouping[0]` and, where mapped, `concept_id`. Extension keys
are short in code (`value`, `engagement-mode`) and qualified to
`https://w3id.org/lrs/ext/<key>` by the runtime.

## Known open items that affect instrumentation

- **§6 / §12.5: multi-concept statements are not expressible.** Pick one concept.
- **§12.9: a Control's duration reaches no rollup.** Per-node dwell is still worth
  emitting, because the log is the system of record, but no dashboard shows it yet.
- **§12.8: the same sim in two books merges in the rollups.** The IRI is canonical, and
  only `grouping[0]` differs. Low engagement is not evidence of low mastery.
- **The extension IRIs the runtime emits** (`xapi_mode`, `end_reason`, `controls`,
  `statements_represented`, `action`, `engagement-mode`, `attempt-number`,
  `run-ended-by`, …) are not yet listed in the contract's tables. Don't add new
  extension names casually; each one is a future schema entry.
- **Full-mode page dwell over-counts on long pages** (found by an eval baseline,
  2026-09-26). With `pageDwell: true`, `lrs-sim.js` times from iframe load until the tab
  hides. It ignores scroll-away and idle, which Compact mode does watch. A chart halfway
  down a 40-minute chapter can therefore be credited with 40 minutes. This is a runtime fix,
  not a per-sim one: still set `pageDwell: true`, and don't work around it in adapter code.
- **A Compact visit made only of answers emits no summary** (found 2026-09-26 in
  `eight-hour-entrepreneur/docs/sims/symptom-root-cause-drilldown`). `lrs-lite-sim.js` opens a
  session only on a folded interaction (`touch`/`run`), and `question().answer()` folds
  nothing. So a student who answers every question and touches nothing else leaves their
  `answered` statements but no `experienced` summary, and therefore no time on the sim. This
  is a runtime fix (for example, let an answer open the session without counting it in
  `statements_represented`). Don't add a dummy touch in adapter code to force a summary.
- **`textbookId` form is undecided across books.** `lrs-config.js` says `lrs` in the
  LRS book, while the seeder uses `tb-{repo-slug}`. `install-runtime.py` defaults a new
  book's `textbookId` to the repo slug and says so. Flag it; don't resolve it inside a
  sim.

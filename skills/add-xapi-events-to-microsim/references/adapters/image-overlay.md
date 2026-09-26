# Adapter: image with hotspot markers (image-overlay, diagram.js)

**Status: VERIFIED.** Proven by `learning-record-store/docs/sims/animal-cell/`: an explore
mode (inspect hotspots) plus a quiz mode (identify the structure, retry until correct),
instrumented from a separate `xapi.js` without forking the vendored
`shared-libs/diagram.js`.

**Applies when:** `main.html` shows an image with numbered markers and/or a label list,
driven by `data.json` callouts, usually through a shared `diagram.js` (or the
microsim-generator `infographic-overlay` assets). Modes such as Explore / Quiz may exist.

## The shape

| Student act | Class | Object | Call |
|---|---|---|---|
| Hover a marker or its label ≥ 600 ms (explore) | 2 | `#{slug(label)}` Control | `item.study('hover', ms)` |
| Click/tap a marker or label (explore) | 2 | the same object | `item.study('click', ms)`, suppressing that visit's hover |
| Click a marker in answer to "Where is X?" (quiz) | 5 | `#q-{slug(target)}` Question | `question.answer({success, response: slug(clicked), durationMs, extensions: {'attempt-number'}})` |
| Mode switch (Explore ↔ Quiz) | not evidence | — | `lrs.note(...)` for the teaching log; reset quiz clocks |
| Time on the sim | 4 | page | `pageDwell: true` |

**Explore and quiz are two objects** (`#nucleus` vs `#q-nucleus`). The object type
belongs to the object, not the mode. Both carry the same concept.

**Hover and click are one act here.** `diagram.js` calls one `showInfobox()` for both,
and there is no pin. Click is what hover is called on a touchscreen. Emit one inspection
per visit either way.

**Quiz order is shuffled on every load**, so the question key must be the target's name
(`q-nucleus`), never an ordinal. **Emit every attempt**: `handleAnswer` locks only on a
correct click, so wrong, wrong, right on one IRI is the BKT signal. Emitting only the
success would make a brute-forcer look like an expert.

## Wiring without forking the library

The vendored `diagram.js` is byte-identical to upstream (`../biology`) and shared by
many sims. **Never edit it.** Put everything in `xapi.js`, loaded after it:

```html
<script src="../shared-libs/diagram.js"></script>
<!-- runtime block (assets/main-html-script-block.html) -->
<script src="xapi.js"></script>
```

In `xapi.js`, wrap the sim's methods, which are bound synchronously before
DOMContentLoaded calls `sim.init()`:

```js
const origHandleAnswer = sim.handleAnswer.bind(sim);
sim.handleAnswer = function (clicked, target) {
  if (sim.quizLocked) return origHandleAnswer(clicked, target);  // replicate the sim's own guard FIRST
  const correct = clicked.id === target.id;
  origHandleAnswer(clicked, target);
  question(target).answer({ success: correct, response: LRS.slug(clicked.label), … });
};
```

For explore listeners, wrap `sim.initExplore` and attach `pointerenter`/`pointerleave`/
`click` with `addEventListener` to `sim.markers.get(id)` and `sim.labelRows.get(id)`.
Track the interval **per callout**, so marker to label is one visit. The listeners
persist across mode switches (only the sim's `on*` properties are nulled), so each
handler must check `sim.mode === 'explore'` itself.

Keep the concept map in `xapi.js`, not in the vendored `data.json`. A re-sync from
upstream would silently delete a field added there. `console.warn` for any callout
with no mapped concept, so an upstream addition fails loudly.

The full, commented reference is `learning-record-store/docs/sims/animal-cell/xapi.js`.
Copy its structure.

## Traps

- Check how the library binds handlers before planning the wrap. Property assignment
  (`btn.onclick = …`) coexists with `addEventListener`; a library that uses
  `addEventListener` with stored references might remove yours on mode switches.
- The quiz's lock window (after a correct answer, ~1.8 s before advancing) ignores
  clicks. Replicate the guard before calling through, or those clicks answer a finished
  question.
- Reset the per-question clock and attempt counter on `showNextQuestion` and
  `setMode`, or a stale clock attaches to the next question.
- The iframe gets taller at phone widths when the label list wraps under the image.
  Animal-cell measured 958 px at 375 px wide in a 960 px iframe. Measure with a full
  log.

## check-xapi actions

The sim's `sim` object is global, so drive it the way the repo tests do:

```json
[
  {"wait_for_js": "typeof sim !== 'undefined' && sim.markers.size > 0"},
  {"eval": "sim.markers.get(sim.data.callouts[0].id).click()"},
  {"click": "button", "text": "Quiz"},
  {"eval": "(() => { const t = sim.quizQueue[sim.quizIndex]; sim.markers.get(sim.data.callouts.find(c => c.id !== t.id).id).click(); })()"},
  {"eval": "(() => { const t = sim.quizQueue[sim.quizIndex]; sim.markers.get(t.id).click(); })()"}
]
```

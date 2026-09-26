# The runtime API a sim talks to

Canonical source: `~/Documents/ws/learning-record-store/docs/js/lrs-sim.js`. Its header
comment is the contract. If this file and that one disagree, **that one wins**; fix this
file.

## Contents

1. The script block and load order
2. `LRSSim.create(opts)`: every option
3. The handles, one per evidence class, each with a worked example from a verified sim
4. `lrs.emit(spec)`: anything else
5. Instance methods and properties
6. Constants, config, and concept ids
7. The p5.js-editor guard
8. The URL switch: `?xapi=teaching`

## 1. The script block and load order

Every instrumented `main.html` loads these, **in this order, before the sim's own
script**. The paths are relative to `docs/sims/<name>/main.html`:

```html
<link rel="stylesheet" href="../../css/lrs-xapi.css">
<script src="../../js/lrs-config.js"></script>     <!-- this book's identity + default policy -->
<script src="../../js/lrs-xapi.js"></script>       <!-- builds every contract statement -->
<script src="../../js/lrs-lite-sim.js"></script>   <!-- Compact sessions, focus-loss detection -->
<script src="../../js/lrs-sim.js"></script>        <!-- the API below; log + teaching UI -->
<script src="../../js/xapi-json-viewer.js"></script><!-- formatted JSON, in a new tab -->
<script src="your-sim.js"></script>
```

`assets/main-html-script-block.html` has the commented version to paste. A site page
(a chapter quiz) gets the same files from `mkdocs.yml` `extra_javascript` and
`extra_css` instead, because iframe payloads don't inherit those.

If the sim's own script is an ES module or loads late (Mermaid 11's
`<script type="module">`), that's fine. The runtime scripts are classic scripts and
define `window.LRS`, `window.LRSLite` and `window.LRSSim` synchronously.

## 2. `LRSSim.create(opts)` returns `lrs`

Call it **once per sim**, after the runtime has loaded. In a p5 sketch that means in
`setup()`; in an IIFE, at the top level. It returns synchronously. The policy from
`metadata.json` loads asynchronously, and `lrs.ready` resolves when it has. You rarely
need `ready`, because handles called before it are handled correctly: nothing is folded
before the policy is known.

| Option | Type | Meaning |
|---|---|---|
| `name` | string | The MicroSim's display name, `object.definition.name` for runs, dwell and the summary. Defaults to `document.title`. |
| `concept` | string | The **page-level** concept id: runs, page dwell, the Compact summary. Use `LRS.conceptId(n)`. |
| `pageDwell` | bool | `true` for a sim with **no Run control**. Full mode emits one `experienced` for time on the page when it loses focus (only if ≥ 1 s). |
| `source` | string | How the formatted-JSON tab names the sim: `'the Sine Wave MicroSim'`. |
| `mount` | selector or element | Where the teaching panel is appended. Default `<body>`. Use `'#xapi-slot'` (a div after `<main>`) for p5 sims. |
| `title` | string | Log header. Default `'xAPI statements emitted:'`. |
| `modeText(compact, sim)` | function → string | Header explanation, re-rendered on every update. Teaching sims should say what *this* sim emits in each mode. |
| `foldNotes` | bool | `false` hides the "· x folded into the session summary" log lines. |
| `modeControls` | bool | `false` hides the Full/Compact switch and Simulate Done. Only for pages whose every statement is an answer (a quiz), where the switch would change nothing. |
| `metadata` | bool | `false` for a page with no `metadata.json` of its own (a chapter quiz). |
| `policy` | object | Policy keys the page sets itself, above the book config and below `metadata.json`. |

The teaching options (`mount`, `title`, `modeText`, `foldNotes`, `modeControls`) only
take effect when the resolved policy says `teaching: true`. Production sims build no
panel at all, so always pass a sensible `mount` anyway.

## 3. The handles

Every handle takes a **fragment key** (see `evidence-classes.md`, "Fragment naming") and
`{ name, concept }`. `name` is human-readable; it becomes `object.definition.name`.

### Class 1: `lrs.slider(key, o)` for a continuous parameter

```
o = { name, concept, min, max, initial, round, deadband }
.input(v)    every raw input event; reports only past the deadband. Counts direction reversals on EVERY raw value.
.settle(v)   the value let go at (a `change` event); always reported unless it equals the last reported value
```

- `min`/`max` set the default deadband, `(max − min) / 60`. Pass `deadband:` for
  controls with a natural step.
- `initial` is the control's starting value. It is the first move's `previous-value`,
  and where reversal tracking starts. Leave it out and the first move has no previous
  value.
- `round` is the decimal places to report. **Report what the student sees.**

Worked example (sine-wave, three sliders, `$LRS_REPO/docs/sims/sine-wave/sine-wave.js`):

```js
sliderEvidence[key] = x.slider(key + '-slider', {
  name: m.label, concept: m.concept, min: m.min, max: m.max, initial: m.default, round: m.round
});
// (sine-wave routes these through handleSliderInput / handleSliderChanged, which also keep its own stats)
amplitudeSlider.input(() => { if (x) sliderEvidence.amplitude.input(amplitudeSlider.value()); });
amplitudeSlider.changed(() => { if (x) sliderEvidence.amplitude.settle(amplitudeSlider.value()); });
```

Full: `interacted`, object `…/sims/sine-wave/#amplitude-slider` (Control), extensions
`value`, `previous-value`. Compact: `controls["amplitude-slider"] = {n, min, max, last,
concept, reversals}`.

### Class 2: `lrs.item(key, o)` for a discrete inspection

```
o = { name, concept }
.study(mode, ms)   mode: 'hover' | 'click' | 'pinned' | 'select' | 'legend' | …   ms: dwell, or undefined
```

The runtime does **not** apply the hover threshold for you, because only the adapter
knows when a hover started. Gate it yourself with `LRSSim.HOVER_MS`.

Worked example (scientific-method, `$LRS_REPO/docs/sims/scientific-method/script.js`):

```js
steps[key] = lrs.item(key.toLowerCase(), { name: nodeInfo[key].title, concept: NODE_CONCEPT[key] });

node.addEventListener('mouseenter', () => { enteredAt = Date.now(); });
node.addEventListener('mouseleave', () => {
  if (enteredAt === null) return;
  const dwell = Date.now() - enteredAt; enteredAt = null;
  if (dwell >= LRSSim.HOVER_MS) steps[key].study('hover', dwell);
});
node.addEventListener('click', () => {
  if (lockedNode === node) {                 // the sim's own handler ran first and pinned it
    steps[key].study('pinned', Date.now() - (enteredAt || Date.now()));
    enteredAt = null;                        // suppress the hover: ONE engagement, not two
  }
});
```

Full: `interacted`, Control, `result.duration`, extension `engagement-mode`. Compact:
`controls[key] = {n, modes: {pinned: 1}, ms, concept}`.

### Class 3a: `lrs.button(key, o)` for a discrete press

```
o = { name, concept }
.press(action)   action: a short word, e.g. 'start' | 'pause' | 'reset' | 'log' | 'linear'
```

A press never carries a duration, and it **never fires for a flush**. Hiding the tab is
not a Pause click.

### Class 3: `lrs.runner(o)` for a Start/Pause run interval

```
o = { onStop(reason) }   called whenever the run closes, whether by Pause or a flush the sim didn't ask for
.start()                 no statement; starts the clock, marks the session busy (a running sim is engaged without input)
.stop(reason)            one `experienced` for the run (object = the PAGE, typed MicroSim); none if < 250 ms
```

`onStop` is what keeps the sim honest. When a flush (tab hidden, Simulate Done, a mode
switch) closes the run, the sim must actually stop, so no run is left open behind the
student's back.

Worked example (bouncing-ball, `$LRS_REPO/docs/sims/bouncing-ball/bouncing-ball.js`):

```js
startPause = lrs.button('start-pause-control', { name: 'Start/Pause Control', concept: CONCEPT_ID });
run = lrs.runner({ onStop: () => setRunning(false) });

function toggleSimulation() {
  if (isRunning) { if (lrs) { startPause.press('pause'); run.stop('paused'); } setRunning(false); }
  else           { if (lrs) { startPause.press('start'); run.start(); }        setRunning(true); }
}
```

Full: Start gives `interacted {action: start}`. Pause gives `interacted {action: pause}`
followed by `experienced` (PT…S, `run-ended-by: paused`). Compact:
`controls["start-pause-control"] = {n: 2, modes: {start: 1, pause: 1}}` and
`runs = {count, ms}`.

### Class 4: `pageDwell: true` for page dwell

This is an option, not a handle. Use it for sims with no Run control (diagrams,
hotspots, charts). Scientific-method and animal-cell both set it.

### Class 5: `lrs.question(key, o)` for a checked answer

```
o = { name, concept }        key names the QUESTION: 'q3' (fixed order, one-based) or 'q-nucleus' (shuffled/generated)
.answer({ success, response, score, durationMs, extensions })
  success     REQUIRED boolean — without it the concept rollup counts no attempt
  response    what the student chose — the most useful part of a wrong answer
  score       0..1; defaults to 1 for success, 0 otherwise
  durationMs  time for this attempt
  extensions  e.g. { 'attempt-number': n }
```

It is emitted immediately, in both modes, and never folded. Emit every attempt.

Worked example (animal-cell, `$LRS_REPO/docs/sims/animal-cell/xapi.js`): the sim's
`handleAnswer` is wrapped, not edited:

```js
sim.handleAnswer = function (clicked, target) {
  if (sim.quizLocked) return origHandleAnswer(clicked, target);   // replicate the sim's own guard
  const correct = clicked.id === target.id;
  origHandleAnswer(clicked, target);
  question(target).answer({ success: correct, response: LRS.slug(clicked.label),
                            durationMs: since, extensions: { 'attempt-number': attemptNo } });
};
```

A **checked prediction** (predict, then run, then compare) is class 5, emitted at the
moment it's checked. Key it by what is being predicted (`q-kafka` for "what happens when
Kafka dies?"), with `response` the prediction and `success` the comparison.

## 4. `lrs.emit(spec, text)` for anything else

It builds and publishes any contract statement through `LRS.build`. It **bypasses
Compact folding**, so use it only for something that passes through in both modes and
that no handle covers. If you find yourself reaching for it, re-read
`evidence-classes.md` first; almost everything is one of the five classes.

```js
lrs.emit({
  verb: 'interacted',                      // 'answered' | 'experienced' | 'interacted' — nothing else
  object: { iri: LRS.pageIri() + '#key', name: 'Name', type: 'Control' },  // Page|MicroSim|Question|Control
  parent: LRS.pageIri(),
  concept: LRS.conceptId(42),
  result: { durationMs, success, score, response, extensions: { value: 3 } }
}, 'log line text');
```

## 5. Instance methods and properties

| Member | Use |
|---|---|
| `lrs.compact` | `true` in Compact mode (after the policy loads) |
| `lrs.teaching` | `true` when the teaching panel is shown |
| `lrs.ready` | Promise, resolves to `lrs` once the policy has loaded |
| `lrs.note(msg)` | A log line that is **not** a statement: why something was deliberately not emitted. Teaching panel only; a no-op otherwise. |
| `lrs.setCompact(bool)` | Runtime mode switch (the teaching radio calls it). Closes the record being left. |
| `lrs.done()` | What the Simulate Done button does |
| `lrs.interactions`, `lrs.count` | Evidence events reported / statements emitted |

The runtime also records every statement in `LRSLite.statements` (an array; the tests
read it) and dispatches a `lrs-lite:statement` window event. Nothing is POSTed; the
transport attaches at `LRSLite.record()` later, with no sim edits needed.

## 6. Constants, config, and concept ids

- `LRSSim.HOVER_MS` 600, `LRSSim.MISCLICK_MS` 250, `LRSSim.GLANCE_MS` 1000.
- `LRS.conceptId(353)` gives `'{conceptPrefix}-353'`, from the book's `lrs-config.js`.
- `LRS.slug('Cell membrane')` gives `'cell-membrane'`, for fragment keys from labels.
- `LRS.pageIri()` is the canonical page IRI, derived and never supplied. It is
  `{siteUrl}sims/<name>/`, with no `main.html`, even inside the iframe, even on
  localhost.
- `window.LRS_CONFIG` = `{ siteUrl, textbookId, version, conceptPrefix, xapi: {compact,
  teaching}, quizzes: {teaching} }`. There is one per book, generated once, and never
  edited by this skill except at the user's request.

## 7. The p5.js-editor guard

The sim must still run when its JS is pasted into the p5.js editor, where none of the
runtime exists. Use this pattern:

```js
let lrs = null;                     // not `x`: p5 sims often use x for position
...
if (window.LRSSim) { lrs = LRSSim.create({...}); speedEvidence = lrs.slider(...); }
speedSlider.input(() => { if (lrs) speedEvidence.input(speedSlider.value()); });
```

In a non-p5 IIFE (a separate `xapi.js`), use `if (!window.LRSSim) return;` at the top.

## 8. The URL switch: `?xapi=teaching`

A reader's explicit request in the URL overrides every config layer for one visit. It is
read from the sim's own URL **and**, inside an iframe, from the page that embeds it. So
`?xapi=teaching` on a lesson or chapter page turns every instrumented sim on that page
into a teaching aid, with no file edited (`urlPolicy()` in `lrs-lite-sim.js`).

| Token | Effect |
|---|---|
| `teaching` | Shows the teaching panel. It starts on Full, like every teaching sim. |
| `teaching,compact` | The same, starting on Compact. |
| `full` / `compact` | Chooses the stream without the panel (read `LRSLite.statements`). |
| `production` | Hides the panel on a teaching sim. |

The full precedence, lowest first: runtime defaults < book `lrs-config.js` `xapi` < page
`policy` option < sim `metadata.json` `xapi` < the URL switch.

**Consequence for the wiring:** when only the URL turned the panel on
(`policy.teachingFromUrl`), `lrs-sim.js` `_fitFrame()` grows the embedding iframe to fit
the panel. It is same-origin and grow-only, and it follows both the log filling and
content above the panel growing. A layout that fills its frame (100vh, html/body at 100%)
grows with the iframe and would be chased forever. The runtime detects that, stops, and
warns in the console. `check-xapi.py`'s `url` mode then fails with "the switched-on panel
fits its iframe". The fix is teaching-only CSS that pins the container to its production
height:

```css
body:has(> .xapi-panel) #network { height: 480px; }   /* was 100vh */
```

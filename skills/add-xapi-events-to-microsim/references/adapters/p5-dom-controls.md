# Adapter: p5.js with DOM controls

**Status: VERIFIED.** Proven by `learning-record-store/docs/sims/bouncing-ball/` (slider +
Start/Pause) and `docs/sims/sine-wave/` (three sliders). Both are covered by
`tests/test_microsim_compact_xapi.py`. A 20-sim batch in `eight-hour-entrepreneur`
(commit `e2c3b94`) confirmed it and added the free-text input, preset-button and checkbox
rows below: card-sorting quizzes, a decision tree, four-slider and one-slider calculators, a
select-and-type builder, and a checkbox signal checker.

**Applies when:** `main.html` loads `p5.js`, and the sketch creates controls with
`createSlider`, `createButton`, `createSelect`, `createCheckbox`, `createRadio` or
`createInput`. If the sketch also hit-tests the canvas in `mousePressed`, read
`p5-canvas.md` too.

## Where to hook

p5 DOM controls are real HTML elements. Hook them through p5's own registration, next
to the sim's existing callback, or wrap that callback:

| Control | Existing sim hook | Evidence class | Call |
|---|---|---|---|
| `createSlider` | `.input(fn)` fires per move; `.changed(fn)` fires on release | 1 | `ev.input(slider.value())` in `.input`; `ev.settle(slider.value())` in `.changed` |
| `createButton('Start')` toggling Start/Pause | `.mousePressed(toggle)` | 3 | `press('start'|'pause')` + `runner.start()/.stop('paused')` inside the toggle |
| `createButton('Reset')` and other one-shots | `.mousePressed(fn)` | 3a | `btn.press('reset')` |
| `createSelect` | `.changed(fn)` | 2 (a choice to look at) or 1 (an ordered numeric setting) | `item.study('select', undefined)`, with the option in the key if each option is its own object |
| `createCheckbox` | `.changed(fn)` | 3a (a toggle action) | `press(cb.checked() ? 'on' : 'off')` |
| `createRadio` | `.changed(fn)` | 2 or 3a | as select |
| `createInput` (numeric) | `.input(fn)` / `.changed(fn)` | 1 | slider handle with `min`/`max` |
| `createInput` (free text: the student writes their own words) | `.changed(fn)` (Enter or leaving the box) | 3a | `press(box.value().trim() ? 'write' : 'erase')`. **Never record the typed text**; it can be personal. |
| A button that checks the student's choice (Check, a Yes/No at a decision node) | `.mousePressed(fn)` | 5 | `question(key).answer({success, response, …})`, every attempt |
| A preset/Load/Reset button that **moves a slider in code** | `.mousePressed(fn)` | 3a | `press('load'|'reset')`, then re-create that slider's handle (below) |

**A free-text box.** The press says only that the student committed wording, and whether the
box is now empty. Report it only while the box is actually in use (for example, while its
dropdown still says "Write your own"). A Load or Clear that hides a focused box fires
`change` too, and that isn't the student writing. The sim's own `.input(fn)` keeps running
untouched. `.changed` is usually free: check that the sim hasn't registered one.

**A slider moved in code** (`slider.value(40)` from Load Jordan's Numbers, or Reset to 0)
fires no `input` event, so the handle's last value, and with it the next move's
`previous-value`, is stale. Re-create the handle with `initial` = the slider's value now:

```js
function makeSliderEvidence() {       // call once in setup, and again after every preset
  priceEv = lrs.slider('price-per-sale-slider', { name: 'Price per Sale Slider', concept: c,
    min: Number(priceSlider.elt.min), max: Number(priceSlider.elt.max),
    initial: Number(priceSlider.elt.value), round: 0 });
}
```

This is safe: a handle is a plain object holding the last value, with nothing registered, and
Compact folds by **key**, so the new handle keeps counting into the same control. Any
unreported pending reversal on the old handle is dropped, which is acceptable.

**Checkboxes.** A p5 checkbox's `.changed(fn)` handler receives the DOM event, so one shared
handler can tell which box fired from `e.target`. Checking a box in code (`cb.checked(true)`,
when loading a scenario) fires no `change`, so it correctly emits nothing.

**p5 element hooks replace; they don't chain.** `.mousePressed()`, `.input()`,
`.changed()`, `.mouseOver()` and the rest all go through `p5.Element._adjustListener`.
That detaches the previous listener for the event before attaching the new one. A
second `slider.input(telemetryFn)` therefore **silently disconnects the sim's own
handler**. Either call the handle from inside the sim's existing function, or add a
plain DOM listener beside it with `slider.elt.addEventListener('input', …)`. The first
option keeps the event order obvious; use it when you can.

## Skeleton

```js
// ---- xAPI (docs/js/lrs-sim.js). Without it (p5.js editor) the sim still runs, silently. ----
const PAGE_CONCEPT = () => LRS.conceptId(353);      // a function: LRS is undefined in the p5 editor
let lrs = null, speedEv, startPause, run;

function setup() {
  updateCanvasSize();                                // always first
  const canvas = createCanvas(containerWidth, containerHeight);
  canvas.parent(document.querySelector('main'));

  speedSlider = createSlider(0, 20, speed);
  speedSlider.input(() => { if (lrs) speedEv.input(speedSlider.value()); });
  speedSlider.changed(() => { if (lrs) speedEv.settle(speedSlider.value()); });
  startButton = createButton('Start');
  startButton.mousePressed(toggleSimulation);

  if (window.LRSSim) {
    lrs = LRSSim.create({ name: 'Bouncing Ball', concept: PAGE_CONCEPT(), mount: '#xapi-slot',
                          source: 'the Bouncing Ball MicroSim' });
    speedEv = lrs.slider('speed-slider', { name: 'Speed Slider', concept: LRS.conceptId(42),
                                           min: 0, max: 20, initial: speed, deadband: 1 });
    startPause = lrs.button('start-pause-control', { name: 'Start/Pause Control', concept: PAGE_CONCEPT() });
    run = lrs.runner({ onStop: () => setRunning(false) });   // a flush must actually stop the sim
  }
}

function toggleSimulation() {
  if (isRunning) { if (lrs) { startPause.press('pause'); run.stop('paused'); } setRunning(false); }
  else           { if (lrs) { startPause.press('start'); run.start(); }        setRunning(true); }
}
```

Note `LRS.conceptId` must not run at the top level of the sketch, because `LRS` doesn't
exist in the p5 editor. Call it inside the `if (window.LRSSim)` block or inside a
function.

## main.html

- Paste `assets/main-html-script-block.html` before the sketch's `<script>`.
- Add `<div id="xapi-slot"></div>` after `<main></main>`, and mount the panel there.
- Add local CSS for `.xapi-panel { margin: 12px 10px 0 10px; }` and a `.xapi-log`
  max-height that fits the iframe. The look comes from `lrs-xapi.css`; only placement
  is local.
- Keep `<main></main>` without an id (the p5-editor rule).

## Traps specific to p5

- `updateCanvasSize()` must still be the first call in `setup()`. Don't put
  `LRSSim.create` before it.
- p5 sims often use `x`/`y` for positions. Name the instance `lrs`.
- A sim that starts running on load violates the paused-by-default standard, and would
  emit dwell nobody chose. Report it; don't start a runner in `setup()`.
- The canvas height doesn't change: the teaching panel sits **below** the canvas in
  HTML, so a production sim keeps its exact size. Only the iframe in `index.md` grows,
  and only for teaching sims.
- Values: `slider.value()` is already in display units for most sims. Where the sketch
  rescales (pixels, radians shown as degrees), report the displayed value (`round:`).
- **`btn.mousePressed(fn)` calls `fn` with the MouseEvent as its first argument.** If you
  give an existing handler an optional parameter (`nextStep(how)`), a button press passes the
  event, not `undefined`. Normalize it: `typeof how === 'string' ? how : 'step'`.
- When one function serves two purposes (the sim's `resetPath()` is called by the Reset button
  *and* by `changeScenario()`), press inside a wrapper on the button only:
  `resetButton.mousePressed(() => { resetPath(); if (lrs) resetEv.press('reset'); });`. That
  is still one listener. Pressing inside `resetPath()` would report every scenario change as a
  Reset.
- Card-sorting quizzes that reshuffle on Try Again: key each card by a short `id:` added to
  its data item (`q-pay-for-convenience`), never by its position or its full text.

## check-xapi actions

Generic driving already moves every `input[type=range]`, changes every `select`,
toggles every checkbox and clicks every button, which is usually enough. For a
Start/Pause sim, make sure a run lasts longer than 250 ms:

```json
[
  {"slider": "input[type=range]", "nth": 0, "values": [5, 7, 9, 11, 13]},
  {"click": "button", "text": "Start"},
  {"wait": 400},
  {"click": "button", "text": "Pause"}
]
```

For a free-text box, `type` sends real keystrokes and then leaves the box, which fires
`change`:

```json
[
  {"select": "select", "nth": 2, "option": "Write your own"},
  {"type": "input[type=text]", "nth": 2, "value": "my own words"}
]
```

Action selectors skip the teaching panel's own controls. In teaching modes `#xapi-slot`
comes before the p5-created buttons in the DOM, so a bare `"button"` with `nth: 0` would
otherwise hit the panel. Add `"panel": true` only to target the panel on purpose.

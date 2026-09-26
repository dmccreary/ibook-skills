# Adapter: p5.js with DOM controls

**Status: VERIFIED.** Proven by `learning-record-store/docs/sims/bouncing-ball/` (slider +
Start/Pause) and `docs/sims/sine-wave/` (three sliders). Both are covered by
`tests/test_microsim_compact_xapi.py`.

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

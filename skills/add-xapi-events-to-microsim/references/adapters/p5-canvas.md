# Adapter: p5.js canvas interactions (hit-tested clicks and drags)

**Status: PARTLY PILOTED.**
- **Canvas click-to-pick and predict → check** passed in the skill's first eval
  (`learning-record-store/docs/sims/chaos-kill-test-simulator`, 2026-09-26: check-xapi
  49/6/0, with state and pixels identical before and after). That run's corrections are
  below.
- **Drags remain UNVERIFIED.** Their pilot is
  `3d-printing-course/docs/sims/ideation-sketch-canvas` (`mouseDragged` hit-testing).

About 1,750 of the ~3,580 p5 sims use canvas `mousePressed`/`mouseDragged`, so this
adapter matters. Verify each claim against the sim, and report corrections.

**Applies when:** the sketch defines global `mousePressed()`, `mouseReleased()`,
`mouseDragged()`, `mouseClicked()`, `doubleClicked()`, `keyPressed()` or
`touchStarted()`, and decides what was hit by comparing `mouseX`/`mouseY` with drawn
shapes. It also applies to canvas-drawn "buttons" (a `rect` + `text` + a hit-test).
DOM controls in the same sketch follow `p5-dom-controls.md`.

## Find the hit-test, not the event

The global `mousePressed()` fires for **every** click, anywhere on the page. That
includes clicks on DOM controls and clicks inside the xAPI panel below the canvas. Don't
report from the top of `mousePressed()`. Report from **inside the branch where the
sim decided something was hit**:

```js
function mousePressed() {
  preds.forEach(function (p, i) {
    if (mouseIsInside(x, py, w, 34)) {
      prediction = p;
      if (lrs) predictionEv.study('select');     // inside the hit branch, never above it
    }
  });
}
```

Report only when the pick **changes** something. A re-click of the current choice is not
new evidence.

Reporting inside the sim's own hit branch tracks the sim's state exactly, and it was
enough in the pilot. There, the hit area (y 200–234) can't be reached from the DOM
controls or the panel below the canvas. If a drawn target *can* overlap DOM controls or
the panel in canvas coordinates, also check that the event target is the canvas
(`event && event.target && event.target.tagName === 'CANVAS'`). A click on the panel's
Simulate Done button reports `mouseX`/`mouseY` relative to the canvas.

## Classes for canvas acts

| Canvas act | Class | Notes |
|---|---|---|
| Click a drawn button that performs an action | 3a `button.press(action)` | key the button by what it does |
| Click a drawn choice (pick a prediction, choose a mode) | 2 `item.study('select')` for the pick | the pick is not yet an answer |
| The choice is **checked** against a right answer | 5 `question.answer()` | emit at the moment of checking, with `response` = the choice |
| Drag a handle that sets a value (a point on a curve, a vector's head) | 1 `slider` on the value the drag controls | one handle per draggable, feed every `mouseDragged` value, `settle()` on `mouseReleased` |
| Free drawing / free positioning with no single value | 2, once per drag | report on `mouseReleased`, `mode: 'drag'`, `ms` = drag duration. **A drag is one continuous move, never one statement per frame.** |
| Click on empty canvas | not evidence | |

## Predict → check (a common canvas pattern)

For example, the chaos-kill-test simulator: pick a case (a service), pick a prediction,
press Kill, and see whether the prediction was right. That's one class-5 answer, emitted
at Kill:

```js
// Key by WHAT is being predicted (the case run): 'q-kafka'. The concept is the one the
// question TESTS; this book has a failure-mode concept per service (334 for Kafka), and
// the page concept (353) belongs to the page and its generic controls.
const FAILURE_CONCEPT = { Kafka: 334, ClickHouse: 335, Neo4j: 336, Summarizer: 337, Redis: 340 };
questions[svc] = questions[svc] || lrs.question('q-' + LRS.slug(svc), {
  name: 'Predict the effect of killing ' + svc,
  concept: FAILURE_CONCEPT[svc] ? LRS.conceptId(FAILURE_CONCEPT[svc]) : undefined });
const key = svc + '|' + prediction;
if (key !== lastChecked) {                  // a double-click / Restore→Kill re-check is not a new attempt
  lastChecked = key;
  questions[svc].answer({ success: prediction === EFFECT[svc].answer,
                          response: LRS.slug(prediction), extensions: { 'attempt-number': ++attempts[svc] } });
}
// lastChecked resets when a new round starts. Follow the SIM's state machine: here choosing
// the service clears the prediction, so choosing the service starts the round (and Reset ends it).
```

- The pick itself can additionally be a class-2 `item` (`#prediction`, `#service-select`).
  The pilot recorded both. In Compact they cost only a count. Don't emit an answer on the
  pick: the check is the evidence.
- **Check the answer key against the chapter** before shipping. In the pilot, the Identity
  key contradicted chapter 19, so correct students would score `success: false`. Both eval
  runs caught it. Report such a key; don't silently fix or silently ship it.

## Continuous drags

`mouseDragged()` fires once per frame (about 60/s). Feed the value to a `slider` handle,
whose deadband makes it about 60 statements per full-range sweep. There is no natural
quantum for a 2-D position, so pick the value the drag *means* (an angle, a radius, a
coefficient), and set `min`/`max` from its legal range. If the drag means two values,
use two handles. When nothing meaningful is being set (free sketching), emit one
`item.study('drag', ms)` per drag, on release.

## Traps

- `mousePressed()` also fires for touches on mobile (p5 maps touch to mouse). That's
  fine; it's the same act.
- Hit-test coordinates depend on `canvasWidth` from `updateCanvasSize()`. Test at
  several widths (check-xapi drives at 900 px).
- A sketch without `redraw` guards may re-run the hit-test every frame via `mouseIsPressed`
  in `draw()`. If so, report on the transition (a `wasPressed` flag), not per frame.

## check-xapi actions

Canvas clicks need coordinates, taken **relative to the canvas's top-left**. Compute
them the way the sketch does. It's often easiest to evaluate the sketch's own geometry:

```json
[
  {"click_at": [100, 215], "on": "canvas"},
  {"select": "select", "option": "Kafka"},
  {"click": "button", "text": "Kill"},
  {"drag": [[120, 120], [260, 180]], "on": "canvas", "steps": 12}
]
```

`click_at` also accepts a JS expression string that returns `[x, y]`, evaluated in the
frame, e.g.
`"[12 + ((width - 24) / 3) * 1.5, 217]"` for the middle of the second of three buttons.

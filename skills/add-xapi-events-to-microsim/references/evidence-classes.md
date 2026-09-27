# Evidence classes

Every interaction in a MicroSim becomes exactly one evidence class, or "not evidence".
The class decides the statement shape in Full mode and the fold in Compact mode. A
per-library adapter only says *which DOM or library event* is which class. The class
itself is library-independent.

## The table

| # | Class | What counts | Full stream (full LRS) | Compact (LRS-Lite) |
|---|---|---|---|---|
| 1 | Continuous parameter | slider, zoom, numeric input, drag of a value | `interacted` per deadband step (default range/60), `value` + `previous-value` | `touch(ctrl, v, {concept, reversals})`: n/min/max/last/reversals |
| 2 | Discrete inspection | click, hover ≥ 600 ms, pin, legend toggle, select, data-point click | `interacted`, `engagement-mode`, `result.duration` | `touch(ctrl, _, {mode, ms, concept})`: n/modes/ms |
| 3 | Run/Pause | Start/Pause, Play/Stop | a press is an `interacted` (`action`); one `experienced` per run (contract §7/§7.1) | `run(ms)` + a press touch |
| 3a | Discrete press | Reset, Randomize, Step, a scale toggle | `interacted` with `action` | a touch with `modes` |
| 4 | Page dwell | a sim with no Run control | `experienced` on focus loss, only if ≥ 1 s | carried by the session summary's duration |
| 5 | Assessment | quiz item, checked prediction, goal reached | `answered` with `success` (+ `response`, `score`) | **passes through unchanged**; never folded |
| 6 | Focus loss | tab hidden, scroll away, idle, blur, Simulate Done | closes the open run or page interval | `end(reason)` gives one summary |

The runtime implements the right-hand columns. You never build a statement or a fold
yourself; you call the handle for the class.

## Thresholds, and why each exists

| Constant | Value | Where | Why |
|---|---|---|---|
| deadband | `(max − min) / 60` | `lrs.slider` default | ~60 statements per full sweep, whatever the numeric range. A slider fires `input` per pixel; that is not 300 decisions. Override with `deadband:` when the control has a natural step (bouncing-ball's integer speed uses `deadband: 1`). |
| `LRSSim.HOVER_MS` | 600 ms | your hover code | A mouse crossing a tall diagram enters a dozen nodes in a few hundred ms. Below 600 ms it is a crossing, not attention. Sweeping 5 nodes quickly must emit **0** statements. |
| `LRSSim.MISCLICK_MS` | 250 ms | `runner.stop()` | A run shorter than this is a mis-click: no `experienced` (the press touches still count). |
| `LRSSim.GLANCE_MS` | 1000 ms | page dwell | Less than a second on the page is a glance, not engagement. |
| `idleMs` / `offscreenMs` / `blurMs` | 90 s / 10 s / 30 s | policy | When the Compact session ends. Tests shorten them; production leaves them. |

`settle(v)` always reports the value the student let go at (the `change` event), even
inside the deadband, so the last value is never lost.

## Choosing the class: the questions to ask

1. **Does it check an answer against a right one?** Then it's class 5, whatever it looks
   like: a canvas-drawn prediction button, a drag-to-bin sort, a "goal reached" banner.
   Emit *every* attempt, wrong ones included. A student who brute-forces six options
   must not look like one who knew it.

   An attempt is a new, deliberate answer, though. Re-checking the **same** choice is not
   a new attempt: a double-clicked Kill, or Restore-then-Kill on the same service and
   prediction. Neither is a choice made after the answer was revealed. Both chaos-kill
   runs converged on this, following `quiz-xapi.js`'s peek rule. De-duplicate on
   (question, response) within one presentation of the question. Follow the sim's own
   state machine for when a presentation starts: in the chaos-kill sim, choosing the
   service clears the prediction, so choosing the service starts it.
2. **Does it change a numeric parameter continuously?** Class 1.
3. **Does it start or stop time passing in the sim?** Class 3: the press is 3a, and the
   interval is the runner.
4. **Is it a one-shot action?** For example Reset, Randomize, Next step, or switching
   log/linear. That's class 3a, a press with an `action` word.
5. **Is it the student looking at, opening, selecting or pinning something?** Class 2.
   `mode` says how: `'hover'`, `'click'`, `'pinned'`, `'select'`, `'legend'`, or
   `'keyboard'`.
6. **Does the sim have no Run control at all?** Add class 4 (`pageDwell: true`) so time
   on the sim is still recorded.
7. **Did the program fire it rather than the student?** Examples: autosize relayout,
   programmatic `setView`, `rangechange` during an animation, a hover the sim itself
   triggered. Then it's **not evidence**. Filter it out at the adapter.

## Two input paths, one act

The most common modelling error is emitting twice for one engagement.

- **Hover and click on one visit are ONE engagement.** If click is a *separate designed
  act* (scientific-method's click-to-pin), the click reports as `'pinned'` and
  **suppresses** the in-flight hover: set the hover clock to `null`, don't restart it.
  Before the fix, clicking all 12 nodes emitted 24 statements.
- **If click is merely the touch fallback for hover**, they are the same act:
  animal-cell's `diagram.js` wires both to one `showInfobox()`, and there is no pin. Emit
  one inspection either way, with `engagement-mode` recording which path. That field is
  an input-device fact, not an evidence-strength fact. Demoting hover here would count
  tablet users and discard laptop users for the identical act.
- **Marker and label for one thing are one object.** Track the hover interval per
  *thing*, not per element, so moving from a marker to its label doesn't emit twice.
- **Click, Next/Previous and arrow keys onto the same object are one act.** When stepping
  controls select the same objects a click does, report one inspection of the newly shown
  object with mode `'click'`, `'step'` or `'keyboard'`, and no Next/Previous press on top.
  Report only when the selection changes. The sim's load-time selection, and the program
  moving on by itself (a timer entering the next section), are not evidence. The
  eight-hour-entrepreneur batch (2026-09-26) used this in ten explorers across p5, Chart.js
  and vis-timeline. A press-only model would give a student who only ever pressed Next no
  per-object evidence at all.

## Explore vs. quiz on the same objects

If a sim inspects hotspots in one mode and asks "where is the nucleus?" in another, those
are **two objects**: `#nucleus` (Control, `item`) and `#q-nucleus` (Question,
`question`). The object type belongs to the object, never to the UI mode. The tell is
that the two acts need different `result` fields to be honest: an inspection has no
`success`. Both carry the same concept, so they reconverge in the concept rollup.

## Fragment naming (contract §2)

The fragment names the sub-activity by its **most stable local identifier**.

| Thing | Fragment | Rule |
|---|---|---|
| A control | `#speed-slider`, `#start-pause-control`, `#scale-toggle` | name it for what it *is*; one fragment for a button whose label toggles |
| A slider evidencing a concept | `#frequency-slider`, not `#period-slider` tagged frequency | name it for its concept so the stream and the student say the same word |
| A diagram node / hotspot | `#hypothesis`, `#nucleus` | the node's stable key, slugified (`LRS.slug`) — never its position |
| A fixed-order quiz question | `#q1`, `#q2` | ONE-based, the number the student sees |
| A shuffled or generated question | `#q-nucleus`, `#q-kafka` | name it for what it asks; an ordinal that changes on reload is not an identity |

The test for any fragment scheme: *would an edit that doesn't change what the thing IS
change its IRI?* If yes, the scheme is wrong.

## Values and units

Report values in **the units the student sees**, rounded to what the student sees
(`round:` on `lrs.slider`). Sine-wave's amplitude was once pixels ÷ 100, and its phase a
pixel shift; both were wrong.

A select has no value slot in `item.study(mode, ms)`, and `mode` is how the student
engaged, so don't overload it with the chosen option. Pick one of these:

- **Each option is a thing to inspect** (choose a dataset or a case to view): make one
  `item` per option, keyed by the option's slug (`#dataset-2020`), and call
  `study('select')` on it.
- **The choice feeds an answer** (pick a service, then predict what happens): one
  `#service-select` item is enough. The chosen option shows up in the answer's key
  (`#q-kafka`) and `response`.
- **An ordered numeric choice** (1×, 2×, 4× speed): treat it as a class 1 `slider`
  with the numeric value.

## Full vs. Compact, per class, concretely

Take this sequence: drag a slider through 5 steps, press Start, wait, press Pause, then
leave the tab.

- **Full:** 5 `interacted` (slider), 1 `interacted` (start), 1 `interacted` (pause), and
  1 `experienced` (the run). That is 8 statements, and hiding the tab adds nothing.
- **Compact:** nothing until the tab hides, then **one** `experienced` summary with
  `controls: {"speed-slider": {n:5,min,max,last,concept}, "start-pause-control":
  {n:2, modes:{start:1,pause:1}}}`, `runs: {count:1, ms}`, and
  `statements_represented: 8`.

Add a quiz answer anywhere in that sequence. It appears as an `answered` statement at
that moment in **both** modes, and it is **not** counted in `statements_represented`.

## What a statement cannot tell you

Exposure evidence (classes 1–4) contributes `attempts = 0` to mastery, by design. Only
`answered` carries `result.success`. If the user wants the sim to measure
*understanding*, it needs an assessment (class 5): a checked prediction or questions
(`pedagogical.keyQuestions`). Say so rather than implying hover data measures
knowledge.

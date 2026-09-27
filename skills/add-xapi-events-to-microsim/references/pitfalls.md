# Pitfalls learned the hard way

Each of these shipped as a bug at least once in `learning-record-store` (2026-07-16 to
2026-09-26). Read the list before you finish wiring a sim. When a check fails for no
obvious reason, the cause is usually on it.

## Statement shape

**Only three verbs: `answered`, `experienced`, `interacted`.**
"start-simulation" is an `interacted` with `action: start`, never a new verb. The
runtime throws on any other verb, and the gateway would reject it. `completed`,
`launched`, `paused` and `selected` are all out.

**Fragment ids are stable local names.**
Use one `#start-pause-control` for a button whose label toggles Start/Pause; the label
changing doesn't change what the control is. Name a slider for the concept it evidences:
`#frequency-slider`, not `#period-slider` tagged `frequency`. Never use `#node-3` or
`#q{N}` for anything whose order can change. The animal-cell quiz reshuffles every
load, so `#q1` would have meant a different question for each student.

**Values are in the units the student sees.**
Sine-wave reported amplitude as pixels ÷ 100 and phase as a pixel shift. The student
saw 0.75 and π/2. Convert to displayed units and `round:` to displayed precision.

**One concept per statement.**
`concept_id` is a single string (contract §6). If a node covers three concepts, pick
the one the interaction is evidence *for*, and note the others in your report. Don't
invent a `concept_ids` array.

**Unmapped means unmapped.**
Leave `concept` undefined and say so. Don't substitute the nearest label; a wrong
concept credits mastery of the wrong thing. Animal-cell warns in the console for an
unmapped callout, which is the right pattern when the object list comes from data.

## Evidence semantics

**A flush is never a button press.**
Tab hidden, idle, scroll-away and Simulate Done close intervals. They must not emit an
`interacted` "pause". Use `runner.stop(reason)` with a reason like `'tab-hidden'`, and
let `onStop` halt the animation. Never call `button.press('pause')` from a flush path.

**A compact summary has no order, so it must carry `reversals` explicitly.**
This is handled by `lrs.slider`, but only if you feed it **every** raw input. It counts
direction changes on raw values, not reported ones. Don't pre-filter slider events
before `.input(v)`.

**A mode switch closes the record being left.**
`lrs.setCompact()` does this. Don't implement your own mode switch; if a sim needs one,
it comes from the teaching panel. Otherwise dwell is lost or double-counted.

**A hover and a click on one visit are one engagement.**
If click pins (a separate designed act), report `'pinned'` and set the hover clock to
`null` so the pending hover can't fire. Restarting the clock (`Date.now()`) only delays
the duplicate. Clicking 12 nodes once produced 24 statements.

**But click as a touch fallback is not a separate act.**
If hover and click call the same function (no pin), emit one inspection per visit
either way. Demoting hover would count tablet users and discard laptop users.

**Answers pass through in both modes.**
Don't fold a prediction or goal into the Compact summary; there is deliberately no
handle that can. Emit every attempt, wrong ones included.

**Paused by default is load-bearing.**
A sim that auto-runs emits dwell the student never chose to spend. If a sim starts
running on load, flag it to the user rather than wiring a runner that starts at load.
Confirm the detector's flag by reading the code. Until 2026-09-26 it flagged any
`running = true`, including one inside the Start button's handler (a false positive on
two-minute-pitch-structure-timer). It now flags only load-time assignments.

**Clicking, stepping and arrow keys onto the same object are one act.**
When Next/Previous or an arrow key selects the same objects a click does, report one
inspection of the newly shown object (`'click'`/`'step'`/`'keyboard'`), never an
inspection *plus* a Next press. Report only when the selection changes. The sim's
load-time selection, and the program moving on by itself (a timer entering the next
section), are not evidence (p5-canvas.md, "Stepping").

**A worked example's check is not an answer.**
If the sim shows the right reading *before* the student chooses (a "Load Priya's
Evidence" worked example with its verdict on screen), a Check on it is a peek, as in
`quiz-xapi.js`. Emit a press plus an `lrs.note`, not an `answered`. The sim itself usually
leaves it out of its own score, which confirms it (persevere-vs-pivot-signal-checker).

## Runtime and environment

**p5 sims must still run pasted into the p5.js editor.**
Guard every call on the runtime existing (`if (lrs)`, `if (window.LRSSim)`). An unguarded
`lrs.slider(...)` throws `ReferenceError` there and the sketch never draws.
`scripts/check-no-runtime.py` loads each sim with the runtime blocked and fails on exactly
this, so run it rather than trusting a read-through.

**Teaching controls are HTML in the shared panel, never on a p5 canvas.**
They are not MicroSim controls, so the p5 builtin-controls rule doesn't apply. On the
canvas they would leave an empty control row in production. Don't add Full/Compact,
Simulate Done or View JSON yourself; `lrs-sim.js` renders them from config.

**Flex-item panels need `min-width: 0`.**
One unwrapped raw-JSON log line otherwise widens the page to thousands of pixels.
Scientific-method's panel is a flex child and needed `flex: 1 0 100%; min-width: 0;` in
its own `style.css`.

**Clicks and mouse moves inside the xAPI panel must not trigger the sim's handlers.**
Scientific-method had "click anywhere outside a node to unpin" on `document` and a
follow-the-mouse infobox. Pressing Simulate Done unpinned the step being studied.
Check every `document`/`window`/`body` listener the sim registers. Exclude
`.xapi-panel`, for example
`if (e.target.closest && e.target.closest('.xapi-panel')) return;`, in a wrapper, not
by editing a vendored file.

**Keys typed inside the xAPI panel reach global key handlers too.**
p5's global `keyPressed()` and any `document` `keydown` listener fire for keys pressed in
the panel. Its Full/Compact radios take arrow keys, so every sim that steps on arrow keys
stepped when the student switched the xAPI mode. Five sims needed the guard in one
20-sim batch. p5 1.11 passes the KeyboardEvent to `keyPressed(e)`: return early when
`e.target.closest('.xapi-panel')` matches.

**vis-timeline blanks if the frame resizes during its first draw.**
A resize within about 100 ms of `new vis.Timeline(...)` leaves 7.7.3 invisible for the
whole visit. The runtime's iframe growth for the teaching panel causes exactly that
resize. Create `LRSSim` in the timeline's `onInitialDrawComplete` (vis-timeline.md).

**Template handlers that call `stopPropagation()` hide clicks from bubbling listeners.**
The microsim-generator Mermaid template does `e.stopPropagation()` in its node click
handler. A delegated `document.addEventListener('click', …)` in the bubble phase never
sees node clicks. Attach to the node itself, or listen in the capture phase (`true`).

**A production sim can still show the panel.**
`?xapi=teaching` on the embedding page turns it on for that visit, so every instrumented
sim needs a `mount` that works and a layout that tolerates the panel. The runtime grows
the iframe to fit. A layout that fills its frame (100vh, html/body at 100%) grows with
the iframe instead, so the runtime stops and warns. Pin it with teaching-only CSS:
`body:has(> .xapi-panel) <container> { height: <px> }`.

**Re-measure iframe height after adding the panel, with a full log, at 700 px.**
An empty-log screenshot underestimates by the log's max-height. Use
`scripts/measure-iframe.py`, and don't shrink an iframe because an empty log fits.

**Browsers cache the stale shared JS during testing.**
After changing a sim, a reused browser happily runs yesterday's `lrs-sim.js`. The check
scripts use a fresh context; in a manual browser, hard-reload or disable the cache
before trusting a result.

**A background tab clamps `setTimeout` to about 1 s.**
A scripted "40 ms hover sweep" in a background tab dwelled about 1000 ms and emitted 19
statements, which looked exactly like a broken threshold. Timing tests belong in
headless Chromium (as `check-xapi.py` does) or must busy-wait on `Date.now()`.

**Wait for the library to render before wiring.**
Mermaid, vis-network and Chart.js create their DOM asynchronously. Wiring on
`DOMContentLoaded` finds no nodes. Poll for the elements, hook the library's own
ready/render event, or wrap the sim's own "setup interactions" function.
Scientific-method's `setTimeout(1200)` works but is fragile; prefer a render promise or
a poll.

**Vendored libraries are wrapped, never edited.**
If `main.html` loads a shared file (`../shared-libs/diagram.js`), it is byte-identical
to an upstream copy used by many sims. Wrap its methods from your own `xapi.js`, loaded
after it. First check how it binds handlers: property assignment (`el.onclick = …`)
coexists with `addEventListener`, but a later `el.onclick = null` removes only the
property handler, so your listeners must branch on the sim's mode themselves.

**Don't copy the runtime into a sim.**
Every sim links `../../js/…`. A per-sim copy is the "five implementations that
disagree" problem Phase 0 existed to end.

## Verification

**A probe needs its own positive control.**
A check that counts 0 before and 0 after proves nothing if it can't see a write.
`check-xapi.py` asserts that Full mode emitted something before it asserts anything
about the shape. If Full emits nothing, your drive didn't reach the wiring; fix the
drive before trusting any other result.

**Test through the iframe, the way the book embeds it.**
IntersectionObserver inside an iframe sees the *parent* page scrolling, and the page IRI
must strip `main.html`. Only the embedded path tests both.

# Adapter: vis-timeline

**Status: PARTLY VERIFIED (2026-09-26).**
- **Item click/select, hover, and Previous/Next/arrow-key stepping: VERIFIED** on
  vis-timeline 7.7.3 by `eight-hour-entrepreneur/docs/sims/field-discovery-window-rhythm` and
  `thirty-day-launch-roadmap-timeline` (commit `e2c3b94`; check-xapi passes in full, compact,
  production and `?xapi=teaching` modes). That batch's corrections are folded in below.
- **Zoom/pan (`rangechanged`) remains UNVERIFIED.** Both verified sims are fixed diagrams
  (`moveable: false, zoomable: false`). The zoom/pan pilot is still
  `Digital-Transformation-with-AI-Spring-2026/docs/sims/timeline`. There are 96 sims in 42 repos.

**Applies when:** `main.html` loads `vis-timeline` (standalone UMD, `vis.Timeline`).

## Getting the instance

The same as vis-network. Use the bare name if the sim declares `let timeline` at the top
level. Otherwise wrap `vis.Timeline` before the sim's script runs, and push the
instance to `window.__lrsTimelines`.

## Wire from `onInitialDrawComplete`, never right after `new vis.Timeline` (verified trap)

If the iframe resizes within about 100 ms of the timeline being created, vis-timeline 7.7.3
never finishes its first draw. Its root keeps `visibility: hidden`, and the timeline stays
blank for the whole visit. The runtime grows the iframe as soon as it builds a teaching panel,
so an `LRSSim.create` placed right after `new vis.Timeline(...)` blanks the timeline in every
`?xapi=teaching` visit. check-xapi's `url` mode then times out at its first `wait_for`, with no
layout failure to point at the cause. This was reproduced on the **unmodified** sims by resizing
at 0–100 ms, so the bug is vis-timeline's. The instrumentation must just not trigger it.

Create the `LRSSim` instance in the timeline's own `onInitialDrawComplete` option:

```js
const options = { /* the sim's options */, onInitialDrawComplete: xapiSetup };
timeline = new vis.Timeline(container, items, groups, options);

function xapiSetup() {
  if (!window.LRSSim || lrs) return;              // once, and silent without the runtime
  lrs = LRSSim.create({ name: 'The Field Discovery Window Rhythm', concept: LRS.conceptId(18),
                        pageDwell: true, mount: '#xapi-slot', source: 'the … MicroSim' });
  stepEv = STEPS.map(s => lrs.item(s.id, { name: s.title, concept: LRS.conceptId(KIND_CONCEPT[s.kind]) }));
  timeline.on('itemover', p => xapiVisit(p.item));
  timeline.on('itemout',  p => { if (visit && visit.id === p.item) xapiEndVisit(); });
}
```

A reader whose own window resizes at load can still hit the bug, with or without xAPI. Report
it to the author as a sim issue.

## Events

| Student act | Event | Class | Call |
|---|---|---|---|
| Click an item | `select` with a non-empty `p.items` | 2 | `item.study('click')`, only if the selection **changed** |
| Previous/Next buttons, arrow keys stepping through the same items | the sim's own handlers | 2 (same items) | `study('step')` / `study('keyboard')`; one selection = one statement, never also a button press (see p5-canvas.md, "Stepping") |
| Hover an item ≥ 600 ms (only if the design reveals details on hover: a tooltip or preview) | `itemover` / `itemout` | 2 | `study('hover', ms)` on out; a click during the visit wins |
| Zoom or pan the time window (**unverified**) | **`rangechanged`** with `p.byUser === true` | 1 on the visible span (years) | `spanEv.input(years)` |
| Category / group filter | the sim's control handler | 3a | |
| Programmatic `setWindow`, `fit`, `moveTo`, `setSelection`, initial render, the sim's load-time selection | — | not evidence | |

- Use mode `'click'` for a clicked item, the same word the other adapters use. Keep `'select'`
  for choosing from a `<select>` or a list beside the timeline.
- **Re-clicking the already-selected item fires `select` again** (verified on 7.7.3). Gate on
  "the selection actually changed", as the p5 explorers do.
- `select` gives `{items, event}` (event type `tap`). A click on empty space gives
  `items: []`. Filter it: it's a deselect, or the sim re-selects the current item, and either
  way it's not evidence.
- `timeline.setSelection()` does **not** fire `select` (verified). If the sim selects from its
  own buttons or a list, report from that handler.
- `setWindow()` fires `rangechange` and `rangechanged`, both with `byUser: false` (verified).

**Never use `rangechange`** (no *d*). It fires continuously during a drag or zoom
animation. `rangechanged` fires once at the end, and carries `byUser`. That flag is the
whole filter between the student zooming and the sim zooming itself.

The span in the unit the student reads, usually years (**unverified**):

```js
timeline.on('rangechanged', function (p) {
  if (!p.byUser) return;
  const years = (p.end - p.start) / (365.25 * 24 * 3600 * 1000);
  spanEv.input(Math.round(years * 10) / 10);
});
```

Set `min`/`max` on the span handle from the timeline's `zoomMin`/`zoomMax` options, or
from the data's full extent. A **fixed-diagram** timeline (`moveable: false, zoomable: false`,
often with the wheel stopped in the capture phase so the page scrolls) has no zoom/pan
evidence at all. Skip this row.

## Hover: one visit, one engagement (verified)

Track the visit per item, as in chartjs.md. `itemover` starts a visit; `itemout` for that item
ends it and emits `study('hover', ms)` if `ms >= LRSSim.HOVER_MS` and no click happened during
it. A click on the visited item marks `visit.clicked`, so one engagement yields one statement.

- **Gate hover evidence on `(hover: none)`.** Touch emulation fires `itemover` on tap, and never
  a timely `itemout`, which produces long fake hovers. Use
  `const noHover = matchMedia('(hover: none)').matches;` and don't emit hovers when it's true.
  The tap still reports as a `click`.
- Close an open visit before the runtime ends the Compact session. Capture listeners on
  `window` run ahead of the runtime's `document` listener:
  `window.addEventListener('visibilitychange', …, true)` and `window.addEventListener('pagehide', xapiEndVisit, true)`.

## Object keys and concepts

- Items: key by the item's stable `id`. When the id already names the thing (`session-2`,
  `week-3`, `fdw-1`), use it as-is. Use `#event-{id}` only for a bare numeric id. With no id,
  use `slug(content)`.
- An item that names an era or event maps to a concept only when the learning graph has
  that concept. Many timeline items are illustrative facts; leave those on the page
  concept, or unmapped, and say which.

## Traps

- The initial-draw blank-out above. Always create the `LRSSim` instance in `onInitialDrawComplete`.
- `itemover` requires a pointer; there's no hover on touch. Only instrument it when the
  design requires hover, and gate it on `(hover: none)`.
- Keys: if the sim steps with a `document` `keydown` listener, guard it against keys pressed
  inside `.xapi-panel` (see p5-canvas.md, "Keyboard").

## check-xapi actions

```json
[
  {"wait_for": ".vis-item"},
  {"click": ".vis-item", "nth": 2},
  {"hover": ".vis-item", "nth": 3, "ms": 800},
  {"click": "button", "text": "Next"},
  {"key": "ArrowRight"},
  {"wheel": ".vis-timeline", "delta": -400}
]
```

Drop the `wheel` step for a fixed-diagram timeline.

# Adapter: vis-timeline

**Status: UNVERIFIED.** Drafted from the vis-timeline 7.x API. Pilot:
`Digital-Transformation-with-AI-Spring-2026/docs/sims/timeline`. There are 96 sims in
42 repos.

**Applies when:** `main.html` loads `vis-timeline` (standalone UMD, `vis.Timeline`).

## Getting the instance

The same as vis-network. Use the bare name if the sim declares `let timeline` at the top
level. Otherwise wrap `vis.Timeline` before the sim's script runs, and push the
instance to `window.__lrsTimelines`.

## Events

| Student act | Event | Class | Call |
|---|---|---|---|
| Click/select an event item | `select` with `p.items` (and `p.event`) | 2 | `eventItem(p.items[0]).study('select')` |
| Hover an item ≥ 600 ms (only if the design reveals details on hover) | `itemover` / `itemout` | 2 | `study('hover', ms)` on out |
| Zoom or pan the time window | **`rangechanged`** with `p.byUser === true` | 1 on the visible span (years) | `spanEv.input(years)` |
| Category / group filter | the sim's control handler | 3a | |
| Programmatic `setWindow`, `fit`, `moveTo`, initial render | `rangechanged` with `byUser === false` | not evidence | |

**Never use `rangechange`** (no *d*). It fires continuously during a drag or zoom
animation. `rangechanged` fires once at the end, and carries `byUser`. That flag is the
whole filter between the student zooming and the sim zooming itself.

The span in the unit the student reads, usually years:

```js
timeline.on('rangechanged', function (p) {
  if (!p.byUser) return;
  const years = (p.end - p.start) / (365.25 * 24 * 3600 * 1000);
  spanEv.input(Math.round(years * 10) / 10);
});
```

Set `min`/`max` on the span handle from the timeline's `zoomMin`/`zoomMax` options, or
from the data's full extent.

## Object keys and concepts

- Items: key by the item's stable `id` if the data file gives one, else by
  `slug(content)`. Use `#event-{id}`.
- An item that names an era or event maps to a concept only when the learning graph has
  that concept. Many timeline items are illustrative facts; leave those on the page
  concept, or unmapped, and say which.

## Traps

- `select` fires with an **empty** `items` array when the student clicks empty space to
  deselect. Filter it.
- `select` is not fired by `timeline.setSelection()`. If the sim selects from a list
  beside the timeline, hook that list.
- `itemover` requires a pointer; there's no hover on touch. Only instrument it when the
  design requires hover.

## check-xapi actions

```json
[
  {"wait_for": ".vis-item"},
  {"click": ".vis-item", "nth": 2},
  {"wheel": ".vis-timeline", "delta": -400}
]
```

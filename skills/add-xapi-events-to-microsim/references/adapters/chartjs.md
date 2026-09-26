# Adapter: Chart.js

**Status: VERIFIED (2026-09-26).** Proven by `3d-printing-course/docs/sims/fdm-price-history`
(commit `6d31ad6`): a Chart.js 4.4.4 line chart where a click on a point reveals an event,
plus a log/linear toggle. It passes `check-xapi.py` in Full, Compact, production and
`?xapi=teaching` modes. The pilot's corrections are folded in below; read that sim's JS
for the full working code. There are 304 Chart.js sims in 63 repos.

**Applies when:** `main.html` loads `chart.js` (usually `chart.umd.min.js`, v4).

## Getting the chart instance

Sims usually create the chart inside a closure
(`document.addEventListener('DOMContentLoaded', () => { const chart = new Chart(canvas, …) })`),
so there's no global. Use Chart.js's own registry:

```js
const chart = Chart.getChart(canvasElOrId);        // null until the chart exists
```

Your `xapi.js` loads after the sim script, and its own `DOMContentLoaded` listener runs
after the sim's (listeners fire in registration order), so the chart exists by then. If
the sim builds the chart later (after a `fetch`), poll `Chart.getChart` or iterate
`Object.values(Chart.instances)`.

When the sim's JS is its own (not vendored), the pilot shows a simpler option. Append one
guarded block (`if (window.LRSSim) instrumentXapi();`) at the end of the sim's own closure.
There it can use `chart`, `DATA` and the toggle button directly.

## Events

| Student act | Where | Class | Call |
|---|---|---|---|
| Click a data point (designed: "click a point to see…") | wrap `chart.options.onClick` | 2 | `item(point).study('click')` |
| Hover a point long enough to read its tooltip | a local plugin's `afterEvent` + `chart.tooltip.getActiveElements()` (**not** `options.onHover`) | 2, when hover reveals content the design relies on | `study('hover', ms)` ≥ `HOVER_MS`, time on the dot only |
| Toggle a legend item | wrap `chart.options.plugins.legend.onClick`, **calling the default** | 2 (`'legend'`) or 3a | `study('legend')` / `press(hidden ? 'hide' : 'show')` |
| A DOM button/select beside the chart (log/linear, dataset picker) | its own `click`/`change` listener | 3a / 2 | `press('log'|'linear')` |
| Zoom/pan (chartjs-plugin-zoom) | `onZoomComplete` | 1 on the visible range | slider on the range width |
| `chart.update()` / resize / animation | — | not evidence | |

### Wrapping onClick without changing behaviour

```js
const chart = Chart.getChart('priceChart');
const origClick = chart.options.onClick;
chart.options.onClick = function (evt, elements, c) {
  if (origClick) origClick.call(this, evt, elements, c);   // the sim's own behaviour first
  if (!elements.length) return;                             // a click on empty chart area
  const i = elements[0].index;                              // the SAME element the sim used
  pointItem(i).study('click');
};
chart.update('none');
```

Report from the same `elements` the sim acts on. The sim's `interaction` options
(`mode: 'nearest', intersect: false`) decide which point a click means, and your report
must agree with what the student saw revealed. Verified on 4.4.4: assigning to
`chart.options.onClick` and then calling `update('none')` takes effect, so no
`config.options` fallback is needed.

### Hover: one visit, one engagement (verified in the pilot)

`options.onHover` **never fires on mouseout or outside the chart area**, so a hover timed
with it never closes. Use a local plugin instead. `afterEvent` sees every chart event
(moves, mouseout, touches) *after* the tooltip has updated. A "visit" lasts while the
tooltip shows one point. Each visit yields at most one statement, and a click on that
visit wins over the hover.

With `interaction.intersect: false`, the tooltip follows the pointer anywhere in the chart
area. One sweep across the plot therefore shows every point without the student reading
any. Count only the time the pointer is **on the dot**
(`element.inRange(e.x, e.y)`):

```js
let visit = null;                                    // { i, onDotSince, ms, clicked }
function endVisit() {
  if (!visit) return;
  if (visit.onDotSince !== null) visit.ms += Date.now() - visit.onDotSince;
  if (!visit.clicked && visit.ms >= LRSSim.HOVER_MS) points[visit.i].study('hover', visit.ms);
  visit = null;
}
function visitPoint(i) {
  if (visit && visit.i === i) return;
  endVisit();
  if (i !== null) visit = { i, onDotSince: null, ms: 0, clicked: false };
}
chart.config.plugins.push({ id: 'xapiEvidence', afterEvent(c, args) {
  const e = args.event, active = c.tooltip ? c.tooltip.getActiveElements() : [];
  visitPoint(active.length && e.type !== 'mouseout' ? active[0].index : null);
  if (!visit) return;
  const onDot = e.x !== null && active[0].element.inRange(e.x, e.y);
  if (onDot && visit.onDotSince === null) visit.onDotSince = Date.now();
  else if (!onDot && visit.onDotSince !== null) { visit.ms += Date.now() - visit.onDotSince; visit.onDotSince = null; }
}});
chart.update('none');
// In the onClick wrapper: visitPoint(i); if (!visit.clicked) { visit.clicked = true; points[i].study('click'); }
// Close an open visit BEFORE the runtime ends the Compact session. A capture listener on
// window runs ahead of the runtime's document listener:
window.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') endVisit(); }, true);
window.addEventListener('pagehide', endVisit, true);
```

On a touchscreen, a tap fires the tooltip and then the click, so the visit model yields
exactly one `click`. The full code is at the end of
`3d-printing-course/docs/sims/fdm-price-history/fdm-price-history.js`.

**Is hover the designed act?** On-screen text often names only the click ("Click a data
point…"), while the tooltip reveals content too. The pilot counted both, as one engagement
per visit, so that tablet users (tap = click) and laptop users (tooltip readers) are counted
for the same act. That's the image-overlay rule: when click is the touch fallback for
reading, both paths are one act.

### Legend: keep the default handler

```js
const defaultLegendClick = Chart.defaults.plugins.legend.onClick;
const origLegend = chart.options.plugins.legend.onClick;
chart.options.plugins.legend.onClick = function (e, item, legend) {
  (origLegend || defaultLegendClick).call(this, e, item, legend);   // still hides/shows the dataset
  seriesItem(item.text).study('legend');
};
```

Replacing the handler without calling the default silently breaks the toggle. That's
the single most common Chart.js instrumentation bug.

## Object keys and concepts

- **Data points**: key by the point's stable label, not its index, and name the key for
  what the label *is*: `#year-2018` for a time series, `#country-kenya` for a category
  axis. Most points share the page concept. If a point's revealed content *is* a concept
  (the pilot's 2009 point, whose event is "FDM Patent Expiration"), map that point to it.
- **Series (legend)**: `#series-{slug(dataset.label)}`.
- **Scale toggle**: `#scale-toggle`, `press('log'|'linear')`. Report the *resulting*
  scale, which is what the student chose to see.

## Traps

- `onHover` fires on every mouse move over the canvas, and never on mouseout. Don't time
  hovers with it; use the `afterEvent` plugin above.
- A chart with `legend: { display: false }` has no legend to instrument, even though
  `detect-library.py` lists a legend hook for any `legend:` block.
- An idle pointer resting on a dot through the idle timeout inflates that hover. Chart.js
  gets no events from a still pointer. Tab-hide and page-leave are handled by the listeners
  above. Scientific-method's hover has the same gap.
- The canvas is `responsive`. The xAPI panel below it must not be inside the chart's
  sized wrapper (`position: relative; height: 340px`), or the chart resizes as the log
  grows. Mount on `main` or `body`.

## check-xapi actions

Click a point at its real pixel position, computed in the frame:

```json
[
  {"wait_for_js": "Chart.getChart('priceChart')"},
  {"click_at": "(() => { const p = Chart.getChart('priceChart').getDatasetMeta(0).data[8]; return [p.x, p.y]; })()", "on": "#priceChart"},
  {"click": "button", "text": "Switch to Linear Scale"},
  {"click_at": "(() => { const p = Chart.getChart('priceChart').getDatasetMeta(0).data[3]; return [p.x, p.y]; })()", "on": "#priceChart"}
]
```

# Adapter: Plotly

**Status: UNVERIFIED.** Drafted from the plotly.js 2.x event API. Pilot:
`data-science-course/docs/sims/plotly-interactive-features-microsim`. There are only 10
sims in 8 repos, so it's low priority, but the event model differs from the others.

**Applies when:** `main.html` loads `plotly` (`cdn.plot.ly/plotly-*.min.js`).

## Getting the plot

The graph div gains `.on()` after `Plotly.newPlot` resolves. Find it by class:

```js
document.querySelectorAll('.js-plotly-plot').forEach(function (gd) { wire(gd); });
```

Or wrap `Plotly.newPlot` so it runs `wire(gd)` after the original's promise resolves.

## Events

| Student act | Event | Class | Call |
|---|---|---|---|
| Click a point / bar | `plotly_click` with `d.points[0]` | 2 | `pointItem(d.points[0]).study('click')` |
| Hover (only if hover is the designed act) | `plotly_hover` / `plotly_unhover` | 2, ≥ `HOVER_MS` | |
| Toggle a legend trace | `plotly_legendclick` (**return nothing**, so the default still toggles) | 2 (`'legend'`) | |
| Zoom / pan / range slider | `plotly_relayout` with `xaxis.range[0]`/`[1]` (or `xaxis.range`) | 1 on the span | |
| Reset axes / autoscale button | `plotly_relayout` with `xaxis.autorange: true` | 3a `press('autoscale')` | |
| A slider/dropdown built with `sliders`/`updatemenus` | `plotly_sliderchange` / `plotly_buttonclicked` | 1 / 3a | |
| Autosize on load/resize, `Plotly.relayout` from code | `plotly_relayout` with `autosize` or no axis keys | not evidence | |

**`plotly_relayout` also fires on autosize.** Only treat it as evidence when the event
carries user axis keys (`'xaxis.range[0]'`, `'xaxis.range'`, `'xaxis.autorange'`). An
event with only `autosize: true` (or `width`/`height`) is the program resizing itself.
Also ignore relayouts that happen while your own code is calling `Plotly.relayout`.

Returning `false` from a `plotly_legendclick` handler **cancels** the default toggle. Your
handler must return `undefined`.

## Object keys

- Points: `#point-{slug(trace.name)}-{slug(x)}`, using the x value, never `pointIndex`,
  which shifts if data is filtered.
- Traces: `#trace-{slug(trace.name)}`.

## check-xapi actions

Plotly points are SVG paths, so use a real click at the point's position:

```json
[
  {"wait_for": ".js-plotly-plot .point"},
  {"click": ".js-plotly-plot .point", "nth": 3},
  {"click": ".legendtoggle", "nth": 0}
]
```

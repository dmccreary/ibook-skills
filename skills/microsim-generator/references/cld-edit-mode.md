# CLD Edit Mode (`?edit=true`)

**Every causal loop diagram this skill generates must support an `?edit=true`
URL suffix.** Generated coordinates are never the final layout. A CLD only reads
well after a human has dragged the boxes and the R/B markers into place and
bent a few arrows, and the author needs a way to do that without editing JSON
by hand. Edit mode is that way: it unlocks dragging, adds curve tools, and
exports the updated CLD JSON so the author can drop it straight back into the
data file.

Learners never see edit mode. Without the suffix the diagram is locked, so a
stray drag in the textbook cannot scramble the layout.

Reference implementation (standalone CLD MicroSim, vis-network 9.1.9):
`macos-screen-grab/docs/sims/feature-count-causal-loop/` —
`feature-count-causal-loop.js`, `feature-count-cld.json`, `main.html`,
`style.css`, `index.md`. Copy from it rather than starting over.

## Which CLDs this applies to

| CLD form | How `edit=true` is supported |
|---|---|
| **Standalone CLD MicroSim** (`docs/sims/<sim-id>/` with its own `main.html`) | Build the full edit mode described below into the sim's `.js`. |
| **Article diagrams** (`cld-inline.js` + the bundled `cld-viewer`) | The bundled `cld-viewer/main.html` treats `?edit=true` like `?menu=true`: it shows the Save Positions and Copy Positions buttons. Give the author `main.html?file=<id>-cld&edit=true`. Inline diagrams on the article page stay read-only. |

## Requirements checklist

A standalone CLD MicroSim is not done until every item holds:

- [ ] The data lives in a separate `<id>-cld.json` (the schema in
      [cld-json-schema.md](cld-json-schema.md)), fetched at startup, **not**
      hard-coded in the `.js`. That is what makes the export a drop-in
      replacement for the file.
- [ ] `const EDIT = new URLSearchParams(location.search).get('edit') === 'true';`
- [ ] `interaction.dragNodes: EDIT`. Nodes are locked for learners and draggable
      in edit mode. Keep `dragView: true` in both modes so learners can still pan.
- [ ] The R/B loop markers are synthetic nodes with ids `loop_<loopId>`, so they
      drag like any other node and export back to `loops[].position`.
- [ ] An edit toolbar, `hidden` unless `EDIT`, with **Copy JSON**,
      **Download JSON**, and **Reset Layout**, plus the edge tools **Flip Curve**,
      **Curve −**, **Curve +**, and **Straight**. The edge tools stay disabled
      until an edge is selected.
- [ ] A status readout that shows `node_id: (x, y)` while dragging and after
      the drop, and `edge_id: curvedCW 0.15` when an edge is selected.
- [ ] Per-edge curves are stored in `edges[].curve` as `{type, roundness}`,
      where `type` is `curvedCW`, `curvedCCW`, or `straight`. The export omits
      `curve` on edges still at the default curve, so the JSON stays clean.
- [ ] The export reads positions from `network.getPositions()`, never from the
      loaded data ([cld-pitfalls.md](cld-pitfalls.md) footgun #7), and rounds them
      to integers.
- [ ] The in-progress layout autosaves to `localStorage` after each drop and
      curve change, and is restored on reload, so an accidental refresh does not
      lose an hour of dragging. **Reset Layout** clears it and reloads.
- [ ] In edit mode the diagram fills the window (`height: 100vh`), because the
      author works in fullscreen, not in the textbook iframe.
- [ ] The sim's `index.md` has an **Editing the Layout** section with a
      `[Open the Layout Editor](main.html?edit=true){ .md-button }` link and a
      short how-to (drag, select an edge to reshape it, Copy/Download, replace
      the JSON file).
- [ ] When you report the finished sim, give the author the edit URL with the
      repo name in the path:
      `http://127.0.0.1:8000/<repo-name>/sims/<sim-id>/main.html?edit=true`.

## Code patterns

### Network options

```js
const EDIT = new URLSearchParams(window.location.search).get('edit') === 'true';

network = new vis.Network(container, { nodes, edges }, {
    physics: { enabled: false },          // every node has an explicit position
    layout: { improvedLayout: false },
    interaction: {
        dragNodes: EDIT,                  // locked for learners
        dragView: true,
        zoomView: false,                  // custom wheel handler, pitfall #5
        hover: true,
        selectConnectedEdges: false
    }
});
if (EDIT) wireEditMode();
```

### Curves

```js
const DEFAULT_CURVE = { type: 'curvedCW', roundness: 0.15 };
const curves = {};   // edge id -> {type, roundness}

function smoothFor(curve) {
    if (curve.type === 'straight') return { enabled: false };
    return { enabled: true, type: curve.type, roundness: curve.roundness };
}

// When building vis edges:
curves[e.id] = Object.assign({}, DEFAULT_CURVE, e.curve || {});
visEdge.smooth = smoothFor(curves[e.id]);

// Edge tool buttons call this with a small mutator.
function changeCurve(fn) {
    if (!selectedEdge) return;
    const c = curves[selectedEdge];
    fn(c);
    c.roundness = Math.round(Math.max(0, Math.min(1, c.roundness)) * 100) / 100;
    edges.update({ id: selectedEdge, smooth: smoothFor(c) });
    updateEdgeTools();
    saveDraft();
}
```

A roundness of 0.15 is a good default for hub-and-spoke diagrams. The 0.4 used
by the bundled viewer bows long spokes so far that they cross neighbouring
loops.

### Export

```js
function exportCLD() {
    const live = network.getPositions();
    const out = JSON.parse(JSON.stringify(cld));
    out.nodes.forEach(n => {
        const p = live[n.id];
        if (p) n.position = { x: Math.round(p.x), y: Math.round(p.y) };
    });
    out.loops.forEach(l => {
        const p = live['loop_' + l.id];
        if (p) l.position = { x: Math.round(p.x), y: Math.round(p.y) };
    });
    out.edges.forEach(e => {
        const c = curves[e.id];
        if (c.type === DEFAULT_CURVE.type && c.roundness === DEFAULT_CURVE.roundness) delete e.curve;
        else e.curve = c.type === 'straight' ? { type: 'straight' } : { type: c.type, roundness: c.roundness };
    });
    out.metadata.updated_date = new Date().toISOString().slice(0, 10);
    return out;
}
```

**Copy JSON** writes `JSON.stringify(exportCLD(), null, 2)` with
`navigator.clipboard.writeText`. If that throws (an insecure context or a
denied permission), put the JSON in a `<textarea>` in the details panel so it
can still be copied by hand. **Download JSON** saves a Blob under the data
file's own name (`<id>-cld.json`), so the author only has to move it into place.

### Draft autosave: layout only

```js
const DRAFT_KEY = '<id>-cld-draft';

function saveDraft() {
    try { localStorage.setItem(DRAFT_KEY, JSON.stringify(exportCLD())); } catch (err) { /* storage unavailable */ }
}

// On load in edit mode: take ONLY positions and curves from the draft.
function applyDraftLayout(data, draft) {
    const byId = list => Object.fromEntries((list || []).map(item => [item.id, item]));
    const dNodes = byId(draft.nodes), dLoops = byId(draft.loops), dEdges = byId(draft.edges);
    data.nodes.forEach(n => { if (dNodes[n.id]) n.position = dNodes[n.id].position; });
    data.loops.forEach(l => { if (dLoops[l.id]) l.position = dLoops[l.id].position; });
    data.edges.forEach(e => {
        if (!dEdges[e.id]) return;
        if (dEdges[e.id].curve) e.curve = dEdges[e.id].curve; else delete e.curve;
    });
}
```

Never restore the whole draft object. If you do, any wording the author fixes
in the JSON file afterwards is silently hidden behind the stale draft. When a
draft was restored, say so in the status line ("Restored the unsaved layout
from this browser. Reset Layout discards it.") so the author is not confused
when the JSON file and the screen disagree. Wrap every `localStorage` call in
`try/catch`, because storage can be unavailable in private windows.

### Drag readout

```js
const showPosition = params => {
    if (!params.nodes.length) return;
    const id = params.nodes[0];
    const p = network.getPositions([id])[id];
    setStatus(id + ': (' + Math.round(p.x) + ', ' + Math.round(p.y) + ')');
};
network.on('dragging', showPosition);
network.on('dragEnd', params => {
    if (!params.nodes.length) return;
    showPosition(params);   // the last 'dragging' event can lag the drop
    saveDraft();
});
```

## Gotchas found while building the reference sim

1. **Status shows the drag-start position.** `getPositions()` inside the
   `dragging` handler can return a position from before the latest move.
   Update the readout again on `dragEnd`.
2. **Markers turn light blue after a drag.** Without explicit `hover` colors,
   vis-network paints a dragged node in its default hover blue, which is wrong
   for a red R or green B marker. Give every node and marker a `color.hover`
   (and a `color.highlight`) that matches its own colors.
3. **Thin edges are hard to click.** Tell the author to click the edge's
   `+` / `−` label, which selects the edge just as well.
4. **`fetch` fails from `file://`.** The JSON must be served by `mkdocs serve`
   or another web server. Show a clear error in the details panel when the fetch
   fails, instead of an empty canvas.
5. **Perfectly horizontal edges can lose their label** on first draw. Nudge one
   end a few units in `y`, and expect the author's drags to create such edges
   occasionally.
6. **The title overlay covers the top row** after `network.fit()`. Fit, then
   zoom out about 10% and shift the view down a little (`fitBelowTitle()` in
   the reference sim).
7. **Fit to the container, not the window, and size world coordinates to the
   iframe.** With the network fitted to a ~750px-wide iframe, a layout spanning
   1,300 world units renders 16px labels at about 8px. Keep a hub-and-spoke
   CLD within about ±400 world units horizontally and ±300 vertically, or scale
   the coordinates before the author starts editing.

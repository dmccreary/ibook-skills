# Adapter: vis-network

**Status: UNVERIFIED.** Drafted from the vis-network 9.x API. Pilot:
`3d-printing-course/docs/sims/graph-viewer` (a learning-graph viewer with search, legend
filters, and node selection). vis-network is the second-largest library: 531 sims in
93 repos.

**Applies when:** `main.html` loads `vis-network` (standalone UMD).

## Getting the network instance

- `let network` / `var network` at the top level of a classic script is reachable by
  its **bare name** from your later script (not as `window.network` if it's `let`).
- If the network is created inside a closure, capture it by wrapping the constructor.
  To do that, load your capture script **after vis-network and before the sim's
  script**:

  ```js
  (function () {
    const Orig = vis.Network;
    window.__lrsNetworks = [];
    vis.Network = function (container, data, options) {
      const n = new Orig(container, data, options);
      window.__lrsNetworks.push(n);
      return n;
    };
    vis.Network.prototype = Orig.prototype;
  })();
  ```

## Events

| Student act | Event | Class | Call |
|---|---|---|---|
| Click / select a node | `network.on('click', p)` with `p.nodes.length` (or `selectNode`) | 2 | `nodeItem(p.nodes[0]).study('click')` |
| Hover a node ≥ 600 ms (only if hover is the designed act; needs `interaction.hover: true`) | `hoverNode` / `blurNode` | 2 | `study('hover', ms)` on blur |
| Double-click to expand/focus | `doubleClick` | 2 (`'expand'`) or 3a | |
| Zoom | `zoom` with `p.scale` | 1 | `zoomEv.input(round(p.scale, 2))`, `min`/`max` from `interaction.zoomSpeed`/limits or 0.1..3 |
| Drag a node | `dragEnd` with `p.nodes.length` | 2 (`'drag'`), one per drag | |
| Search box picks a node | the sim's search handler | 2 (`'search'`) | |
| Legend / group filter checkbox | its `change` handler | 3a `press(checked ? 'show' : 'hide')` | key `#group-{slug}` |
| Stabilization, `fit()`, programmatic `selectNodes`/`focus` | — | not evidence | |

`network.on` handlers **chain**; adding yours doesn't remove the sim's.

## Node ids are often concept ids

In a learning-graph viewer, the node id **is** the book's ConceptID. Then:

```js
function nodeItem(id) {
  return items[id] || (items[id] = lrs.item('node-' + LRS.slug(String(id)), {
    name: nodes.get(id).label, concept: LRS.conceptId(id)
  }));
}
```

The key is `node-{id}` (stable even if the label is edited). Check that the viewer's ids
really are the CSV's ConceptIDs, and that it isn't loading another book's graph.

For concept maps that **aren't** the learning graph, map node → ConceptID by label with
`find-concepts.py`, and leave unmatched nodes unmapped.

**Multi-concept (contract §12 item 5):** a node or an edge can legitimately touch
several concepts. v1 carries one `concept_id` per statement. For a node, use the node's
own concept. For an **edge** click (prerequisite → dependent), use the dependent
concept, the one whose understanding the relationship explains, and note the choice in
the report. Never emit two statements for one click to carry two concepts.

## Traps

- `click` fires for empty-canvas clicks too (`p.nodes` empty). Filter them.
- Programmatic selection (`network.selectNodes()`) should not fire `selectNode`, so a
  sim's search-to-select path emits nothing through the network events. Hook the search
  handler itself. **Verify in the pilot.**
- The `zoom` event fires per wheel tick; the slider deadband handles it. `fit()` and
  stabilization don't emit `zoom`, but `network.moveTo` with animation might emit
  `animationFinished`. Ignore everything except `zoom`/`dragEnd` from the user.
- Physics keeps moving nodes after load. A `dragEnd` with no nodes is a canvas pan
  (class 1 on the view, usually not worth reporting).
- The panel must sit outside the network container. vis sizes its canvas to the
  container, and a growing log inside it would resize the graph.

## check-xapi actions

Click a node at its DOM position:

```json
[
  {"wait_for_js": "typeof network !== 'undefined' && network && Object.keys(network.getPositions()).length > 0"},
  {"wait": 1500},
  {"click_at": "(() => { const id = network.body.data.nodes.getIds()[0]; const p = network.canvasToDOM(network.getPositions([id])[id]); return [p.x, p.y]; })()", "on": "#network canvas"}
]
```

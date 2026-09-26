# Adapter: Mermaid diagrams, and plain HTML/SVG with DOM listeners

**Status: VERIFIED** for the hover-and-pin pattern:
`learning-record-store/docs/sims/scientific-method/` (Mermaid 10, hover ≥ 600 ms + click
to pin, page dwell). The **click-to-pin-only template** (below), the common
microsim-generator shape, is **VERIFIED** too, by
`learning-record-store/docs/sims/xapi-statement-triple` (Mermaid 11 ESM, teaching sim,
commit `a6c0062`). The skeleton below worked unchanged. The template's full-height layout
needed the recipe under "Layout".

**Applies when:** `main.html` loads `mermaid` (classic `mermaid.min.js` or the ESM
`mermaid.esm.min.mjs` in a `<script type="module">`). The same DOM-listener pattern
covers any plain HTML/SVG sim whose interactive things are DOM elements.

## Know which template you have

Read the sim's script and instruction text first. They name the designed act.

| Shape | Tells | Designed act | Instrument |
|---|---|---|---|
| **Click-to-pin template** (microsim-generator `mermaid`): `script.js` with `showNodeInfo`, `extractNodeId`, `setupNodeInteractions`, `waitForMermaid`; placeholder text "Click a node to see details" | click only, no hover handler; clicking empty space clears | click | `item.study('click', undefined)` per node click |
| **Hover + pin** (scientific-method): `mouseenter`/`mouseleave` + `click` locking a node | "Hover over any step… Click on any node to keep its information displayed" | hover to read, click to keep | hover ≥ 600 ms gives `'hover'`; click-that-pins gives `'pinned'` and suppresses that visit's hover |
| **Hover = click** (one function for both, no pin) | both wired to the same show function | reading the infobox | one inspection per visit, `mode` = `'hover'` or `'click'` (see image-overlay.md) |

Clearing a selection (clicking empty space, clicking a pinned node to unpin) is **not
evidence**; emit nothing.

## Node identity

- Mermaid assigns element ids like `flowchart-Hypothesis-3` (v10) or
  `mermaid-1699-flowchart-Hypothesis-3` (v11). The **author's node id** (`Hypothesis`) is
  stable; the prefix and suffix are not. Use the template's own `extractNodeId(el)` if
  it exists (it's a global function), or strip with
  `el.id.replace(/^.*flowchart-/, '').replace(/-\d+$/, '')`.
- The fragment key is the slugified node id: `LRS.slug('Hypothesis')` gives
  `hypothesis`. Its `name` is the infobox title (`nodeInfo[id].title`).
- Only nodes that have an entry in the sim's info object (`nodeInfo`) are interactive.
  Instrument exactly those.

## Waiting for the render

Mermaid renders asynchronously, and with the ESM build (`type="module"`) even later. No
`.node` exists at `DOMContentLoaded`. In order of preference:

1. **Wrap the template's own setup function.** `setupNodeInteractions` is a top-level
   `function` in a classic script, so it's a property of `window`, and
   `waitForMermaid()` looks it up by name at call time. Replace it from a script loaded
   *after* `script.js`:
   ```js
   const origSetup = window.setupNodeInteractions;
   window.setupNodeInteractions = function () { origSetup(); wireXapi(); };
   ```
   Your wiring then runs exactly once, right after the sim's.
2. **Poll** for `.mermaid svg .node` (every 100 ms), then wire.
3. **Avoid** fixed timeouts (`setTimeout(…, 1200)`). Scientific-method uses one, and it
   is a known follow-up.

## Skeleton: the click-to-pin template

Put this in a new `xapi.js`, loaded after `script.js`. The template's `script.js` is
generic and identical across hundreds of sims, so don't edit it.

```js
(function () {
  'use strict';
  if (!window.LRSSim) return;                       // the diagram works without the runtime

  // node id (the author's, from the Mermaid source) -> learning-graph ConceptID
  const NODE_CONCEPT = { Actor: 9, Verb: 10, Object: 11, Result: 13, Context: 14 };

  const lrs = LRSSim.create({
    name: document.title, concept: LRS.conceptId(15), pageDwell: true,
    source: 'the <Title> MicroSim', mount: 'body'
  });

  const items = {};
  function item(nodeId) {
    if (!items[nodeId]) {
      const n = NODE_CONCEPT[nodeId];
      if (n === undefined) console.warn('[<sim>] no concept mapped for node "' + nodeId + '"');
      items[nodeId] = lrs.item(LRS.slug(nodeId), {
        name: (typeof nodeInfo !== 'undefined' && nodeInfo[nodeId] && nodeInfo[nodeId].title) || nodeId,
        concept: n === undefined ? undefined : LRS.conceptId(n)
      });
    }
    return items[nodeId];
  }

  function wire() {
    document.querySelectorAll('.mermaid .node').forEach(function (node) {
      const id = extractNodeId(node);
      if (typeof nodeInfo === 'undefined' || !nodeInfo[id]) return;   // not an interactive node
      // On the node itself: the template's handler calls stopPropagation(), so a
      // bubbling listener on document would never see this click.
      node.addEventListener('click', function () { item(id).study('click'); });
    });
  }

  const orig = window.setupNodeInteractions;
  window.setupNodeInteractions = function () { orig(); wire(); };
})();
```

For the hover + pin shape, copy the pattern in
`learning-record-store/docs/sims/scientific-method/script.js` (bottom section). It uses
`mouseenter`/`mouseleave` with `LRSSim.HOVER_MS`, and a pin that sets the hover clock to
`null`.

## Layout: where the panel goes

Mermaid sims are usually a flex row (diagram + info panel). Mount the panel on the
container and give it its own full-width row in the sim's `style.css`. Don't touch
`lrs-xapi.css`:

```css
.xapi-panel { flex: 1 0 100%; min-width: 0; }   /* own row; min-width stops JSON lines widening the page */
```

If the container is not a flex row, mount on `body` (animal-cell) and skip the CSS.

### The click-to-pin template fills the iframe, so make room (verified)

The microsim-generator Mermaid template pins `html`, `body` and `.container` to 100% of
the iframe with `overflow: hidden`. That leaves no room below the diagram, and a panel
placed inside the flex row is clipped. For a **teaching** sim:

- Mount the panel on `body`.
- In the sim's `style.css`, scope every rule to `body:has(> .xapi-panel)`. The runtime
  builds the panel only when `teaching: true`, so a production embed keeps its original
  fill-the-iframe layout exactly.

```css
body:has(> .xapi-panel),
body:has(> .xapi-panel) .container,
body:has(> .xapi-panel) .diagram-panel { height: auto; }          /* the row takes the diagram's natural height */
body:has(> .xapi-panel) .info-panel { height: auto; contain: size; } /* a long definition scrolls; the row doesn't grow on click */
body:has(> .xapi-panel) .mermaid svg { max-height: 440px; }       /* the diagram grows with width; cap it so one iframe height fits 700–900 px */
body > .xapi-panel { margin: 10px; }
```

Pick the `max-height` from the measured diagram at 700 px. `:has()` needs Chrome 105+,
Safari 15.4+ or Firefox 121+.

**Add this CSS to production sims too.** A reader can switch any sim's panel on with
`?xapi=teaching`, and this template fills its frame, so without the recipe the panel is
clipped. The runtime detects that it can't grow the frame to fit, and `check-xapi.py`'s
`url` mode fails. Because every rule is scoped to `body:has(> .xapi-panel)`, the CSS does
nothing until the panel exists.

## Traps

- **`const nodeInfo` is not `window.nodeInfo`.** A top-level `const`/`let` in a classic
  script is visible to later scripts by its bare name, but it is *not* a property of
  `window`. Test it with `typeof nodeInfo !== 'undefined'`. Top-level `function`
  declarations *are* window properties, which is what makes wrapping
  `setupNodeInteractions` work.
- **`stopPropagation()` in the template's node handler.** Attach to each node (as
  above) or use a capture-phase listener. A bubbling `document` listener misses every
  node click.
- **"Click empty space to clear"** is on `.diagram-panel` or `document`. Make sure a
  click inside the xAPI panel doesn't reach it. That's usually true when the panel is
  outside `.diagram-panel`; check it if you mount inside.
- **Clicking the already-selected node** re-shows the same info. It's still a deliberate
  click, so emit it. Deduplicating is the rollup's job, not the adapter's.
- **Iframe height**: the panel adds height, so re-measure (`measure-iframe.py`).
  Mermaid diagrams are often tall at narrow widths.

## check-xapi actions

```json
[
  {"wait_for": ".mermaid .node"},
  {"wait": 500},
  {"click": ".mermaid .node", "nth": 0},
  {"click": ".mermaid .node", "nth": 2},
  {"hover": ".mermaid .node", "nth": 3, "ms": 800}
]
```

# Adapter: Leaflet maps

**Status: UNVERIFIED.** Drafted from the Leaflet 1.9 API. Pilot:
`food-science/docs/sims/world-fermented-foods-map`. There are 48 sims.

**Applies when:** `main.html` loads `leaflet.js` (`L.map`).

## Getting the map

Leaflet has an official hook, so no constructor wrapping is needed. Register it
**before** the sim creates its map (a script loaded after `leaflet.js` and before the
sim):

```js
window.__lrsMaps = [];
L.Map.addInitHook(function () { window.__lrsMaps.push(this); });
```

Markers: hook `L.Marker.addInitHook` the same way, or iterate
`map.eachLayer(l => l instanceof L.Marker && …)` after the sim has added them.

## Events

| Student act | Event | Class | Call |
|---|---|---|---|
| Click a marker / feature | `marker.on('click')` or the layer's `click` | 2 | `placeItem(name).study('click')` |
| Open a popup (the usual designed act) | `map.on('popupopen', e)`, `e.popup._source` is the marker | 2 | use either click or popupopen, **not both** (one act) |
| Zoom | `zoomend`, `map.getZoom()` | 1 | `zoomEv.input(map.getZoom())`, `min`/`max` = `map.getMinZoom()`/`getMaxZoom()` |
| Pan | `moveend` | usually not evidence on its own | |
| Layer control toggle | `overlayadd` / `overlayremove` / `baselayerchange` | 3a | `press('show'|'hide')`, key `#layer-{slug(name)}` |

**`zoomend` and `moveend` also fire on programmatic `setView`, `fitBounds` and
`flyTo`**, including the initial view at load and every "fly to this place" button the
sim offers. Filter them with a user-intent flag:

```js
let userGesture = false;
map.getContainer().addEventListener('pointerdown', () => { userGesture = true; }, true);
map.getContainer().addEventListener('wheel',       () => { userGesture = true; }, { capture: true, passive: true });
map.on('zoomend', function () {
  if (!userGesture) return;                // setView / fitBounds / flyTo from code
  userGesture = false;
  zoomEv.input(map.getZoom());
});
```

The zoom +/- control buttons are inside the container, so they count as user gestures.
That's correct.

## Object keys and concepts

- A place: `#place-{slug(name)}`, from the data's name field, never from coordinates or
  marker order.
- Map places are usually examples, not concepts. Most sims map every place to the page
  concept or a small set of category concepts (e.g. by food type). Do that only when the
  learning graph has those categories.

## Traps

- Tile loading generates no events you care about. Ignore `load`/`tileload`.
- A marker click that opens a popup fires both `click` and `popupopen`. Pick one.
- Leaflet needs its container height set explicitly. Put the xAPI panel outside the
  map container.

## check-xapi actions

```json
[
  {"wait_for": ".leaflet-marker-icon"},
  {"click": ".leaflet-marker-icon", "nth": 0},
  {"click": ".leaflet-control-zoom-in"},
  {"wait": 400}
]
```

# Layout Templates

Vis-network has physics disabled in this skill, so every node needs an explicit `(x, y)` position. These templates give you sensible starting points. Coordinates are in vis-network world space — they're abstract; the canvas auto-fits to the bounding box on render. World-space "up" is negative y.

The templates assume a logical center near `(300, 300)` for single-loop CLDs. For the full-system CLD, use `(0, 0)` as center and let things fan out symmetrically — that file gets bigger and benefits from a centered origin.

## Single-loop layouts

### 3-node triangle (recommended for simple loops)

Used by R1, R2 in the reference Winner-Takes-All article.

```
       Top (300, 120)
       /            \
      /              \
  Left (120, 420)  Right (480, 420)
```

```json
{ "id": "node_a", "position": {"x": 300, "y": 120} },
{ "id": "node_b", "position": {"x": 480, "y": 420} },
{ "id": "node_c", "position": {"x": 120, "y": 420} }
```

Loop annotation at center: `{"x": 300, "y": 320}` (slightly below visual center, since the top of the triangle has more visual weight).

### 4-node diamond

Used by R4 (Data Flywheel) and the original AI Flywheel.

```
        Top (300, 150)
       /              \
   Left              Right
  (150,300)         (450,300)
       \              /
       Bottom (300, 450)
```

```json
{ "id": "north", "position": {"x": 300, "y": 150} },
{ "id": "east",  "position": {"x": 450, "y": 300} },
{ "id": "south", "position": {"x": 300, "y": 450} },
{ "id": "west",  "position": {"x": 150, "y": 300} }
```

Loop annotation at center: `{"x": 300, "y": 300}`.

### 5-node pentagon

Used by R3 (Capital → Compute → Capability) which has 5 nodes.

```json
{ "position": {"x": 300, "y": 120} },   // top
{ "position": {"x": 520, "y": 300} },   // upper-right
{ "position": {"x": 420, "y": 500} },   // lower-right
{ "position": {"x": 180, "y": 500} },   // lower-left
{ "position": {"x":  80, "y": 300} }    // upper-left
```

Loop annotation at center: `{"x": 300, "y": 320}`.

### Sizing guidance

The cld-viewer's network area is ~600×600 in world units when the canvas is 600px tall. The templates above use a comfortable margin so labels don't get clipped. For 4-line node labels, give 200–250px of horizontal breathing room.

## Multi-loop hub-and-spoke

Used by the full-system CLD when one variable (e.g. `Model Capability`) sits at the center of multiple loops radiating outward. Center origin at `(0, 0)`; each loop occupies a sector.

```
                  B1
                   |
         R3        +        R2
           \       |       /
            \      |      /
   B3 ------ MODEL_CAPABILITY ------ R1
            /      |      \
           /       |       \
         R4        +        B4
                   |
                  B2
```

Sector angles you can use as a starting grid (with 1 hub, 8 loops):

```
N (0°)        loop pointing up         (0, -y)
NE (45°)      upper-right diagonal     (+x, -y)
E (90°)       right                    (+x, 0)
SE (135°)    lower-right diagonal     (+x, +y)
S (180°)     loop pointing down       (0, +y)
SW (225°)    lower-left diagonal      (-x, +y)
W (270°)     left                     (-x, 0)
NW (315°)    upper-left diagonal      (-x, -y)
```

Each loop occupies a sector with the hub node at its inside edge. Place 2–3 supporting nodes per loop along the sector. Reference: [winner-takes-all-cld.json](../assets/causal-loop/cld-viewer/examples/winner-takes-all-cld.json) — 17 nodes, 8 loops, hub at `(0, 0)`.

A typical sector spans about 250 world units radially and ±150 tangentially. So an "east" sector with one supporting node at `+250` and a deeper one at `+450`:

```json
{ "id": "model_capability", "position": {"x": 0,   "y": 0} },
{ "id": "code_quality",     "position": {"x": 250, "y": -80} },
{ "id": "rd_productivity",  "position": {"x": 450, "y": 60} }
```

Keep 200+ units between adjacent loops so labels don't collide.

## R/B annotation positions

The renderer adds a colored circle (red R for reinforcing, green B for balancing) at `loop.position`. Two strategies for picking it:

1. **Centroid of loop nodes** — average the positions of every node in `path`. Works well for triangle and diamond layouts.
2. **Toward the visual center** — for hub-and-spoke, place each loop's R/B between the hub and the outer ring of the sector, so all the markers sit on a smaller inner circle around the hub. This makes loop counts easy to read at a glance.

The marker is 40px wide, so it needs at least 60px of clear space around it. Don't place it directly on top of an edge crossing.

## When to break the templates

These are starting points, not laws. Real diagrams often need adjustments:

- A loop with one very-long-label node may need that node pulled outward to give the label room.
- Two loops sharing a node (e.g. R3 and B1 both touching `compute_scarcity`) may want that shared node placed on the boundary between their sectors.
- For more than 8 loops, consider splitting into two diagrams rather than crowding one.

Edit mode is your friend. Open any CLD with `?edit=true` (for the bundled cld-viewer, `main.html?file=<id>-cld&edit=true`, which shows its Save Positions button). Drag the nodes and R/B markers into a layout you like and save, and the exported JSON has your hand-placed coordinates frozen in. Use that to iterate fast. See [cld-edit-mode.md](cld-edit-mode.md).

Size the layout to the iframe it will be embedded in. A hub-and-spoke CLD fitted into a ~750px iframe should stay within about ±400 world units horizontally and ±300 vertically. A layout twice that wide renders 16px labels at about 8px.

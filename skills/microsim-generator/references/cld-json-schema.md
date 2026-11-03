# CLD JSON Schema

Every CLD is a JSON file matching the schema below. The `cld-viewer` and `cld-inline.js` renderer both consume this exact format. The schema is the same one used by the systems-thinking course, so files are portable between projects.

Save each CLD as `<id>-cld.json` inside the project's `docs/sims/cld-viewer/examples/` directory. The id should be lowercase, hyphenated, and unique across the project (e.g. `runaway-hypothesis-cld`, `data-flywheel-cld`).

## Top-level structure

```json
{
  "metadata": { ... },
  "nodes":    [ ... ],
  "edges":    [ ... ],
  "loops":    [ ... ],
  "leverage_points":   [ ... ],   // optional
  "scenarios":         [ ... ],   // optional
  "educational_content": { ... }  // optional
}
```

## metadata

```json
"metadata": {
  "id": "runaway-hypothesis-cld",
  "title": "The Runaway Hypothesis (R1)",
  "archetype": "limits-to-growth",
  "description": "One-paragraph summary that appears in the details panel.",
  "version": "1.0.0",
  "created_date": "2026-05-05",
  "author": "Project Name",
  "tags": ["ai", "reinforcing-loop", "self-improvement"]
}
```

The `title` shows in the diagram's title overlay (24px black, top center) and in the details panel header. Keep it short — under ~50 chars renders best. Common archetypes: `limits-to-growth`, `success-to-the-successful`, `tragedy-of-the-commons`, `shifting-the-burden`, `fixes-that-fail`, `accidental-adversaries`, `escalation`, `drifting-goals`.

## nodes

Each node is a system variable.

```json
{
  "id": "model_capability",
  "label": "Model Capability",
  "position": {"x": 300, "y": 120},
  "type": "stock",
  "description": "Aggregate quality of the frontier model — reasoning, code generation, agentic task completion."
}
```

- **id** — snake_case, unique within this CLD, used as edge source/target.
- **label** — display name. Will be word-wrapped to ~18 chars per line.
- **position.x / position.y** — vis-network world coordinates. See `layout-templates.md`.
- **type** — typically `stock` for the central accumulating variable, `variable` for everything else. Purely informational; the renderer doesn't change behavior based on type.
- **description** — shown in the details panel when the node is clicked. One sentence is plenty.

Optional node fields: `examples` (array of strings), `measurement` (string).

## edges

Each edge is a causal link between two nodes.

```json
{
  "id": "mc_to_cq",
  "source": "model_capability",
  "target": "code_quality",
  "polarity": "positive",
  "description": "Better models generate better code.",
  "strength": "strong"
}
```

- **id** — required; any unique string within the file.
- **source / target** — must match a node id.
- **polarity** — `"positive"` (renders as green `+`) or `"negative"` (red `−`). Polarity is causal: "if source goes up, target goes up" = positive; "if source goes up, target goes down" = negative.
- **description** — shown in the details panel.
- **strength** — optional: `"weak"`, `"moderate"`, `"strong"`. Currently informational only.

Optional fields: `delay: { present: true, duration: "weeks", description: "..." }`, `label` (overrides the polarity symbol), `curve: { type: "curvedCW" | "curvedCCW" | "straight", roundness: 0.15 }` (per-edge curve, written by the `?edit=true` curve tools; omit it to use the renderer's default; see [cld-edit-mode.md](cld-edit-mode.md)).

## loops

Each loop is a closed cycle of nodes that produces reinforcing or balancing dynamics. The `loops` array drives the R/B center marker — the colored circle in the middle of each loop.

```json
{
  "id": "R1",
  "type": "reinforcing",
  "label": "R1: Recursive Self-Improvement",
  "description": "Better models build better models.",
  "path": ["model_capability", "code_quality", "rd_productivity", "model_capability"],
  "behavior_pattern": "Compounding capability growth bounded only by external constraints.",
  "position": {"x": 300, "y": 320},
  "is_primary": true
}
```

- **id** — typically `R1`, `R2`, `B1`, `B2` etc. Becomes the synthetic node id `loop_<id>` in the rendered network.
- **type** — `"reinforcing"` (red R marker) or `"balancing"` (green B marker).
- **path** — node ids in traversal order, starting and ending at the same node. Informational; not strictly required for rendering, but used in the details panel.
- **position** — where the R/B circle sits. Put it at the centroid of the loop's node positions, or slightly offset toward the visual center of the diagram.
- **is_primary** — optional; flag the most important loop in a multi-loop diagram for emphasis.

A balancing loop has an *odd* number of negative edges along its path. A reinforcing loop has an *even* number (zero counts). When in doubt, mentally trace the loop: if a perturbation comes back amplified, it's reinforcing (R); if it comes back damped, it's balancing (B).

## Optional sections

These are read by the cld-viewer's details panel but skipped by the inline renderer. Include them when the diagram is meant to be deep-dived in fullscreen mode.

- `leverage_points` — places to intervene, with `target_type` (`"node"`, `"edge"`, `"system"`), `target_id`, `leverage_level` (1–12, Donella Meadows scale), `title`, `description`, `intervention_strategies` array.
- `scenarios` — what-if analyses with `title`, `description`, `changes` array, `predicted_outcomes`.
- `educational_content` — `discussion_questions`, `key_insights`, `common_misconceptions` (each with `misconception` + `correction`), `extension_activities`, `related_concepts`.

See `assets/causal-loop/cld-viewer/examples/winner-takes-all-cld.json` and `ai-flywheel-cld.json` for full examples.

## Validation checklist

Before declaring a CLD complete:

- [ ] Every `edge.source` and `edge.target` matches an existing `node.id`.
- [ ] Every `loop.path` entry matches an existing `node.id`.
- [ ] No duplicate `node.id` or `edge.id` values.
- [ ] Every node has an explicit `position` (the renderer disables physics — no auto-layout).
- [ ] Loop count and polarity match the visual: count negative edges along each `loop.path` — odd → balancing, even → reinforcing.
- [ ] `metadata.id` matches the filename (e.g. `id: "foo-cld"` → `foo-cld.json`).

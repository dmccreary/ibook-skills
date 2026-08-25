---
name: install-learning-graph-viewer
description: This skill installs an interactive learning graph viewer application into an intelligent textbook project. Use this skill when working with a textbook that has a learning-graph.json file and needs a visual, interactive graph exploration tool with search, filtering, and statistics capabilities.
---
# Install Learning Graph Viewer

## Overview

Installs a complete interactive graph viewer into `/docs/sims/graph-viewer/` by copying 4 template files and replacing the TITLE placeholder. Total install time: under 2 minutes.

**Template files are in this skill at:** `references/assets/`

## Viewer Version

Current template version: **v1.04** (CIS-based node sizing, batched DataSet updates, loading-message indicator, version badge in top-right corner).

When you ship a behavior change to the viewer templates, bump this number in **three** places so future debugging can trace which version of the viewer is deployed where:

1. The version in this file (the line above).
2. `references/assets/main.html` — the `<div id="viewer-version">v1.04</div>` line.
3. The changelog entry below.

Remember there are **two copies** of the template files (`references/assets/` and `references/learning-graph-viewer-templates/`) that must be kept byte-identical — Step 2 below copies from `references/assets/`, so that is the one that actually ships, but keep both in sync.

### Changelog

- **v1.04** — **BREAKING:** Node size (font size + margin, `box` shape is auto-sized around its label so this is what actually changes the rendered box dimensions) now scales with each node's **Concept Impact Score** (`node.cis`, added by `learning-graph-generator` v1.06+). Higher-CIS concepts render as slightly larger boxes. Uses `log(cis+1)` normalization, not raw CIS, because CIS is heavy-tailed (roughly half of concepts in a typical graph sit at the minimum value) — linear scaling would make that entire lower half visually indistinguishable. Range is deliberately modest (font 12-22px, margin 4-10px) to stay legible in a 200+ node force-directed graph; see `cisNormalized()`, `CIS_FONT_MIN/MAX`, `CIS_MARGIN_MIN/MAX` in `script.js`. Verified empirically (not just assumed) that: (a) vis-network's native `nodes.scaling`/`value` mechanism has **no visible effect on `box`-shaped nodes** — only `dot`/icon-style shapes respond to it, so per-node `font.size` is the correct mechanism for this project's box-style nodes; (b) per-node `font: {size: N}` correctly **merges** with (does not replace) the group-level `font.color`, so existing group color-coding is unaffected. Graphs generated before `learning-graph-generator` v1.06 have no `cis` field on their nodes — `cisNormalized()` treats a missing/undefined `cis` as `1` (the minimum), so those graphs render at a uniform `CIS_FONT_MIN` size with no error, just no size variation, until `learning-graph.json` is regenerated.
- **v0.04** — Fixed slow check-all/uncheck-all (batched `DataSet.update(array)` instead of per-item calls). Added `Loading concepts and edges…` indicator removed on `stabilizationIterationsDone`. Added version badge in top-right corner. Precomputed `nodesWithDeps` / `groupCounts` at load. Assigned explicit integer IDs to edges so batched updates can target them.
- **v0.03** — Initial template split from inline code into `references/assets/` (commit `89275ae6`).

## Step 1: Verify Prerequisites

```bash
ls docs/learning-graph/learning-graph.json
```

If missing, run the `learning-graph-generator` skill first.

### Validate classifierName Values

```bash
python3 -c "
import json
with open('docs/learning-graph/learning-graph.json') as f:
    data = json.load(f)
issues = []
for gid, ginfo in data['groups'].items():
    name = ginfo.get('classifierName', '')
    if name == gid:
        issues.append(f'  {gid}: classifierName equals ID - needs human-readable name')
    else:
        print(f'  OK: {gid} -> {name}')
if issues:
    print('FIX REQUIRED:')
    for i in issues: print(i)
"
```

If any classifierName equals its ID, fix taxonomy-names.json and regenerate learning-graph.json before proceeding.

## Step 2: Copy Template Files

```bash
SKILL_DIR="$BK_HOME/skills/book-installer/references/assets"
mkdir -p docs/sims/graph-viewer
cp "$SKILL_DIR/local.css"  docs/sims/graph-viewer/local.css
cp "$SKILL_DIR/script.js"  docs/sims/graph-viewer/script.js
cp "$SKILL_DIR/index.md"   docs/sims/graph-viewer/index.md
cp "$SKILL_DIR/main.html"  docs/sims/graph-viewer/main.html
```

## Step 3: Replace TITLE Placeholder

Extract the course title from learning-graph.json and replace TITLE in main.html:

```bash
TITLE=$(python3 -c "import json; print(json.load(open('docs/learning-graph/learning-graph.json'))['metadata']['title'])")
sed -i '' "s/TITLE/$TITLE/g" docs/sims/graph-viewer/main.html
echo "Title set to: $TITLE"
```

Verify the replacement worked:

```bash
grep "<title>" docs/sims/graph-viewer/main.html
```

## Step 4: Reorder Groups to Match Taxonomy (Optional but Recommended)

The legend order in the sidebar matches the groups key order in learning-graph.json. Reorder to match concept-taxonomy.md:

```bash
cd docs/learning-graph
python3 -c "
import json, re
with open('concept-taxonomy.md') as f:
    text = f.read()
ordered_ids = re.findall(r'^#{1,6}[^(]+\(([A-Z]{2,8})\)', text, re.MULTILINE)
with open('learning-graph.json') as f:
    data = json.load(f)
ordered_groups = {}
for key in ordered_ids:
    if key in data['groups']:
        ordered_groups[key] = data['groups'][key]
for key in data['groups']:
    if key not in ordered_groups:
        ordered_groups[key] = data['groups'][key]
data['groups'] = ordered_groups
with open('learning-graph.json', 'w') as f:
    json.dump(data, f, indent=2)
print('Groups reordered to match concept-taxonomy.md')
for k in data['groups']:
    print(f'  {k}: {data[\"groups\"][k][\"classifierName\"]}')
"
cd ../..
```

## Step 5: Add Fullscreen Link to Learning Graph Index

Add this markdown to `docs/learning-graph/index.md` right after the level-1 heading:

```markdown
[Open Learning Graph Viewer Fullscreen](../sims/graph-viewer/main.html){ .md-button .md-button--primary }

<iframe src="../sims/graph-viewer/main.html" width="100%" height="600px" frameborder="0"></iframe>
```

## Step 6: Update mkdocs.yml Navigation

Add the graph viewer to the MicroSims section in `mkdocs.yml`:

```yaml
nav:
  # ... existing nav ...
  - MicroSims:
    - Learning Graph Viewer: sims/graph-viewer/index.md
```

## Step 7: Inform the User

Tell the user to test at:
```
http://127.0.0.1:8000/REPO_NAME/sims/graph-viewer/main.html
```

Where REPO_NAME is the git repository name.

## File Structure Created

```
docs/sims/graph-viewer/
├── main.html      # vis-network viewer (TITLE replaced with course name)
├── script.js      # Graph loading, search, filtering, highlighting
├── local.css      # Sidebar layout, search, legend, stats styling
└── index.md       # MkDocs page with iframe embed + fullscreen link
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Legend shows IDs like "FOUND" | classifierName not set | Fix taxonomy-names.json, regenerate JSON |
| Colors don't match legend | groups not passed to vis-network | Verify script.js builds visGroups from JSON |
| Graph keeps spinning | Physics timeout missing | script.js disables physics after 5s (built-in) |
| Checkbox toggling slow | Per-item DataSet.update() calls | Use batched array update (built-in) |
| Graph not loading | Wrong JSON path | script.js expects `../../learning-graph/learning-graph.json` |
| All nodes render the same size | `learning-graph.json` predates `learning-graph-generator` v1.06 (no `node.cis` field) | Regenerate `learning-graph.json` (re-run `csv-to-json.py` v1.04+) |

## Dependencies

- vis-network.js (CDN: `https://unpkg.com/vis-network/standalone/umd/vis-network.min.js`)
- learning-graph.json at `docs/learning-graph/learning-graph.json`

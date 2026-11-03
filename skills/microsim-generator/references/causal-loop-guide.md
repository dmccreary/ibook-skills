# Causal Loop Diagram (CLD) Generator Guide

> Formerly the standalone skill `causal-loop-diagram-generator`. This guide supersedes
> the earlier single-sim causal-loop guide: it builds complete multi-loop CLD
> **articles**, and scales down to a single inline diagram when that is all the
> user needs.

This guide produces a complete, working multi-CLD article for an MkDocs Material site. The output is a set of files that together render an article where each section discusses one feedback loop and shows it as an interactive draggable diagram, building up to a full-system view at the end.

## What the user gets

When invoked on a topic (say, "make me a CLD article about supply chain bullwhip"), the workflow produces:

1. **One JSON file per loop** (`docs/sims/cld-viewer/examples/<id>-cld.json`) — usually 3–5 nodes each, one per archetype loop in the topic.
2. **One full-system JSON** combining all loops around a shared central node.
3. **The article markdown** (`docs/articles/<slug>.md`) — progressive build-up, one section per loop, with inline interactive diagrams and a fullscreen-button per diagram.
4. **The shared infrastructure** (`docs/articles/cld-inline.js`, `docs/sims/cld-viewer/`) if not already present in the project.
5. **Updated `mkdocs.yml`** nav entries.

Every diagram is a live vis-network instance the reader can drag, zoom, and click to inspect. Not a static image.

**Every CLD also supports an `?edit=true` URL suffix** that lets the author reposition every node and every R/B marker, reshape edge curves, and export the updated JSON. Generated coordinates are a first draft, and the author always finishes the layout by hand. See [cld-edit-mode.md](cld-edit-mode.md).

## When to use this guide

Trigger on requests for any of:

- "Make a causal loop diagram for X"
- "Write an article about [the runaway dynamic in X]"
- "Show the feedback loops in X"
- "Add a CLD article to my site"
- A topic that has one or more reinforcing loops competing with balancing ones (AI race, virality, addiction, supply chain bullwhip, market dynamics, climate, organizational dysfunction)

If the user just wants a single quick diagram — not an article — generate just one CLD JSON and embed it inline; skip the article structure.

If the user wants a single CLD as a **standalone MicroSim** (its own `docs/sims/<sim-id>/` directory, embedded in a chapter by iframe), keep the data in `docs/sims/<sim-id>/<id>-cld.json`, fetch it from the sim's `.js`, and build in the full edit mode from [cld-edit-mode.md](cld-edit-mode.md). The reference implementation is `macos-screen-grab/docs/sims/feature-count-causal-loop/`.

## High-level workflow

1. **Understand the system.** Ask clarifying questions if the topic is ambiguous, but a single sentence is usually enough to draft a plausible loop set. List the candidate reinforcing loops (R1, R2, …) and balancing loops (B1, B2, …) before writing any JSON. Show the list to the user and confirm before generating files.

2. **Verify the project layout.** Determine the project root (look for `mkdocs.yml`). Confirm or create:
   - `docs/articles/` (article location)
   - `docs/sims/cld-viewer/examples/` (CLD JSON location)
   - `docs/articles/cld-inline.js` (inline renderer)
   - `docs/sims/cld-viewer/main.html` + `cld-viewer.js` + the four R/B PNGs (fullscreen viewer)

3. **Port missing assets.** Copy the bundled assets from `assets/causal-loop/` in this skill if any are missing. See the "Bundled assets" section below for the exact file map.

4. **Generate one JSON per loop.** Read [cld-json-schema.md](cld-json-schema.md) and [cld-layout-templates.md](cld-layout-templates.md). Use the 3-node triangle template for simple loops, 4-node diamond for richer ones, hub-and-spoke for the full system.

5. **Write the article.** Follow [cld-article-structure.md](cld-article-structure.md) — frontmatter, lead, anchor example, R-loops, B-loops, status table, full system, leverage point, signals, bottom line. Required `<style>` and `<script src="../cld-inline.js">` block at the bottom.

6. **Update `mkdocs.yml`.** Add a nav entry for the new article. If `cld-viewer/index.md` doesn't exist yet, add it under MicroSims.

6b. **Check edit mode.** Open each CLD with `?edit=true` (for article diagrams, `cld-viewer/main.html?file=<id>-cld&edit=true`). Confirm that nodes and R/B markers drag, that the exported JSON carries the new positions, and, for a standalone sim, that the diagram is locked without the suffix. Follow the checklist in [cld-edit-mode.md](cld-edit-mode.md).

7. **Read [cld-pitfalls.md](cld-pitfalls.md) before changing anything in `cld-inline.js`, `cld-viewer.js`, or the rendering setup.** Nine specific footguns are documented — they each cost real debugging hours to find. The most important one: never use one iframe per inline diagram; both Chrome and Firefox silently fail to render past the 5th–6th iframe on a single page, and there is no client-side workaround.

## Bundled assets

Everything you need to install into a fresh project lives in this skill's `assets/causal-loop/`:

```
assets/causal-loop/
├── cld-inline.js                  # Inline vis-network renderer for article pages.
│                                  # Copy to: docs/articles/cld-inline.js
└── cld-viewer/
    ├── main.html                  # Fullscreen viewer page (used by the iframe
    │                              # buttons in the article). Has menu mode for
    │                              # sample buttons + Save/Copy positions.
    ├── cld-viewer.js              # Fullscreen viewer's JS — loads JSON, renders
    │                              # network, handles drag/zoom/save.
    ├── reinforcing-loop-cw.png    # R/B archetype icons referenced in the
    ├── reinforcing-loop-ccw.png   # systems-thinking schema. Optional but copy
    ├── balancing-loop-cw.png      # them through if the project will use loop
    ├── balancing-loop-ccw.png     # iconography.
    └── examples/
        ├── ai-flywheel-cld.json           # 4-node diamond, single reinforcing loop.
        ├── runaway-hypothesis-cld.json    # 3-node triangle, single reinforcing loop.
        └── winner-takes-all-cld.json      # 17 nodes, 8 loops, hub-and-spoke.
                                           # Use as a model for full-system diagrams.
```

## Reference docs

Loaded as needed, in roughly this order:

- **[cld-json-schema.md](cld-json-schema.md)** — the CLD JSON format. Read first when generating loops.
- **[cld-layout-templates.md](cld-layout-templates.md)** — coordinate templates for 3-, 4-, 5-node loops and for hub-and-spoke. Read when placing nodes.
- **[cld-article-structure.md](cld-article-structure.md)** — section-by-section template for the article markdown, including the required `<style>` + `<script>` boilerplate. Read when writing the article.
- **[cld-pitfalls.md](cld-pitfalls.md)** — nine documented footguns with symptoms, root causes, and solutions. Read before modifying any rendering code or attempting an iframe-based design.
- **[cld-edit-mode.md](cld-edit-mode.md)** — the required `?edit=true` layout editor: requirements checklist, code patterns (drag lock, curve tools, export, layout-only draft autosave), and gotchas. Read before writing any CLD's `.js`.

## Default loop count

When the user gives only a topic and asks for "a CLD article," default to:

- 1 anchor example (the canonical loop everyone agrees on)
- 3–4 reinforcing loops (the runaway dynamics)
- 3–4 balancing loops (the constraints)
- 1 full-system diagram

That's 8–10 diagrams total, matching the reference Winner-Takes-All article. If the topic has fewer real dynamics, scale down — don't pad. If the user asks for "a quick diagram" or "just one loop," produce one CLD JSON and a single inline embed; skip the article scaffolding entirely.

## Naming conventions

- CLD ids: lowercase, hyphenated, ending in `-cld`. Example: `bullwhip-amplification-cld`.
- Article slug: short, hyphenated, descriptive. Example: `supply-chain-bullwhip.md`.
- Loop labels: `R1: Recursive Self-Improvement`, `B1: Compute Constraint`. Always use `R<n>` for reinforcing and `B<n>` for balancing.

## What NOT to do

- **Do not embed diagrams as iframes inline in the article.** Use `<div class="cld-inline">` and the inline renderer. See [cld-pitfalls.md](cld-pitfalls.md) #1.
- **Do not use mermaid, ASCII art, or static images** for the loops. The whole point of this guide is interactive vis-network diagrams readers can drag.
- **Do not soften the `border: 2px solid blue`** on iframes or `.cld-inline` divs. It's the project-wide MicroSim standard signaling interactive content. See [cld-pitfalls.md](cld-pitfalls.md) #8.
- **Do not modify the global `iframe` CSS rule** in `extra.css` to "look nicer." Same reason.
- **Do not skip the `<script src="../cld-inline.js">` tag** at the bottom of the article. Without it, every `<div class="cld-inline">` is an empty bordered box.
- **Do not ship a CLD without `?edit=true` support**, and do not let learners drag nodes in a standalone CLD MicroSim. Lock with `dragNodes: EDIT`. See [cld-edit-mode.md](cld-edit-mode.md).
- **Do not hard-code the nodes and edges in the `.js`** of a standalone CLD. Keep them in `<id>-cld.json` so the edit-mode export is a drop-in replacement for the file.

## Confirming with the user

After you've drafted the loop list (step 1) but *before* generating files, show the user the proposed loop set with one-line descriptions. They almost always have an opinion on which loops to include and what to call them, and it's much cheaper to revise the list than to revise 8 JSON files.

After generating, tell the user the file paths and what `mkdocs.yml` changes you made, and give them the edit URL with the repo name in the path, for example `http://127.0.0.1:8000/<repo-name>/sims/<sim-id>/main.html?edit=true`, or `.../sims/cld-viewer/main.html?file=<id>-cld&edit=true` for article diagrams. Remind them that in edit mode they can drag the nodes and R/B markers, reshape the arrows, and copy or download the updated JSON to replace the data file.

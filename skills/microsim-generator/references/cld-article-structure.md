# Article Structure

The reference article ([winner-takes-all.md](https://github.com/dmccreary/tracking-ai-course/blob/main/docs/articles/winner-takes-all.md)) follows a progressive build-up pattern that works well whenever the topic has one central runaway dynamic and multiple competing forces. Use this as the default structure when generating a CLD article.

## Default outline

```
1. Frontmatter (title, description, image for social card, hide toc)
2. Lead — set up the question/hypothesis in 2–3 paragraphs.
3. "Where We Start" — one canonical example everyone agrees on.
   (For AI: the AI Flywheel. For supply chain: the bullwhip. For startups:
   the venture flywheel. The point is to anchor the reader on something familiar.)
4. R1 — the core "runaway" loop being argued.
5. R2..Rn — additional reinforcing loops, each in its own section.
6. B1..Bn — balancing loops, each in its own section.
7. Status table — current state of every loop, one row each.
8. "Putting It All Together" — the full system diagram.
9. Leverage point — the single threshold question that determines outcome.
10. Signals to watch — 3 concrete observable indicators.
11. Bottom line — one paragraph.
```

Each diagram section follows the same shape so the reader builds a rhythm:

```markdown
## R2 — Autonomous Research (the supercritical loop)

One-paragraph framing of what changed from the previous loop.

<div class="cld-inline" data-src="../../sims/cld-viewer/examples/autonomous-research-cld.json"
     data-cld="autonomous-research-cld" style="height:520px"></div>

[Open R2: Autonomous Research Fullscreen](../../sims/cld-viewer/main.html?file=autonomous-research-cld&menu=true){ .md-button }

Two or three paragraphs explaining what the loop does and why it matters.
End with a bridge sentence that motivates the next section.

---
```

## Frontmatter

```yaml
---
title: Winner Takes All? A Systems View of the AI Race
description: A causal-loop analysis of whether one AI lab can pull permanently ahead — and what would have to be true for that to happen.
image: articles/winner-takes-all.png
hide:
  - toc
---
```

- `image` — relative to `docs/`. Used by the `social_override` plugin to set the og:image meta. The PNG should be a representative screenshot or a custom social card.
- `hide: toc` — the article is too long to navigate by table of contents; force the reader to scroll, which keeps the build-up intact.

## Inline diagram block

The exact HTML to use for each diagram. **Do not use iframes here** — see `pitfalls.md` for why. The class `cld-inline` and the data attributes are what `cld-inline.js` looks for.

```html
<div class="cld-inline"
     data-src="../../sims/cld-viewer/examples/<id>-cld.json"
     data-cld="<id>-cld"
     style="height:520px"></div>
```

Heights to use:
- 520px for 3–4 node loops (most cases)
- 560px for 5-node loops
- 720px for the full-system CLD

The `data-src` path is relative to the article's URL, which is `/articles/<slug>/` after MkDocs builds with directory URLs. So `../../sims/cld-viewer/examples/...` resolves to `/sims/cld-viewer/examples/...` correctly.

## Fullscreen button

Right after the inline div, give a button that opens the same CLD in the iframe-based viewer with the menu and details panel. This is where users go to read the loop description, drag nodes, and save positions.

```markdown
[Open R2: Autonomous Research Fullscreen](../../sims/cld-viewer/main.html?file=autonomous-research-cld&menu=true){ .md-button }
```

Use `.md-button .md-button--primary` only on the final full-system diagram's button to give it visual weight.

For the author, the same viewer opens in edit mode with `?file=<id>-cld&edit=true`. Give the author that URL in your report rather than putting it in the article, and see [cld-edit-mode.md](cld-edit-mode.md).

## Status table

Place this after all individual loops, before "Putting It All Together":

```markdown
| Loop | Status | Comment |
|------|--------|---------|
| R1 — Recursive Self-Improvement | **Strong** | Every frontier lab uses its own model in its own pipeline. |
| R2 — Autonomous Research        | **Emerging** | Real but not yet self-sustaining. The supercritical question. |
| ...
```

Status values to pick from: `Very strong`, `Strong`, `Strong, accelerating`, `Strong, asymmetric`, `Emerging`, `Weakening`, `Weak`. Comments should be one terse clause.

## Bottom of article — required boilerplate

Every CLD article must end with this `<style>` block and `<script>` tag. The script enables the inline rendering. Without it, the `<div class="cld-inline">` blocks will just be empty boxes.

```html
<style>
  /* Each .cld-inline div hosts a vis-network instance that fills it. The
     network canvas is positioned absolute (set in cld-inline.js) so the
     title overlay can sit on top of it without affecting layout. */
  .cld-inline {
    position: relative;
    width: 100%;
    background: aliceblue;
    border: 2px solid blue;
    margin-bottom: 1em;
    overflow: hidden;
  }
  .cld-inline-title {
    position: absolute;
    top: 10px;
    left: 0;
    right: 0;
    text-align: center;
    font: 24px Arial, Helvetica, sans-serif;
    color: black;
    pointer-events: none;
    z-index: 10;
  }
</style>

<script src="../cld-inline.js"></script>
```

The `border: 2px solid blue` is the project-wide MicroSim standard — see `pitfalls.md`. Do not change it.

The script `src` is `../cld-inline.js` (one directory up) because the article URL is `/articles/<slug>/` and the script lives at `docs/articles/cld-inline.js` → `/articles/cld-inline.js` after build.

## MkDocs nav entries

After creating the article and CLD JSONs, add nav entries to `mkdocs.yml`:

```yaml
nav:
  - Articles/Blog Posts:
    - List of Articles: articles/index.md
    - <Your Article Title>: articles/<slug>.md
    - ...
  - MicroSims:
    - ...
    - CLD Viewer: sims/cld-viewer/index.md   # only if not already present
```

Also update `docs/articles/index.md` (the article-list page) to link to the new article with a one-line description.

## Voice and length

The reference article runs ~2,800 words. Sections vary from 60 to 200 words each — short enough that the reader doesn't lose the diagram in scroll. Match this density. Avoid long paragraphs; prefer 2–3 sentences per paragraph so each diagram stays close to its discussion.

Numbered or bulleted lists are encouraged for the "Signals to watch" section and for status enumerations. Keep prose elsewhere.

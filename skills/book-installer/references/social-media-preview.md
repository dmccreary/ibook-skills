# Social Media Preview Hook

Install an MkDocs hook that overrides `og:image` and `twitter:image` with
a page's `image:` frontmatter value. The hook is a no-op on pages that
don't declare `image:` — those keep whatever `mkdocs-material` (or the
optional `social` plugin) emits by default.

## The Logic in One Sentence

The `mkdocs-material[imaging]` social plugin, when enabled, will always
generate a per-page social preview card, and crawlers will use that card
**unless** the page's markdown frontmatter declares an `image:` field —
in which case that declared image always wins over the generated card.

This hook is the piece that enforces "declared image always wins." Without
it, `image:` frontmatter is silently ignored (it's just an unknown key as
far as MkDocs is concerned).

## When to Use This Reference

Use this guide when the user asks for any of:

- "social media preview", "social card", "social meta tags"
- "og:image", "Open Graph image override"
- "Twitter Card image", "Twitter image"
- "LinkedIn preview", "Facebook preview", "Slack unfurl"
- A failing `bk-check-social-cover` run

This hook complements `mkdocs-material`'s built-in social meta tags
(`og:title`, `og:description`, `og:url`, `twitter:card`, etc., which
Material emits on its own). The hook's only job is to swap the image URL
on pages where the author has supplied a custom cover via frontmatter.

For projects that need per-page auto-generated card images, the full
`social` plugin (`mkdocs-material[imaging]`) does that, but it requires
Cairo. This hook works alongside it (replacing the generated
`/assets/images/social/...` image with the declared cover when both are
present), or stands alone with no system dependencies.

## Prerequisites

- Existing MkDocs Material project with `site_url:` set in `mkdocs.yml`
- A cover image at `docs/img/cover.png` if the home page (or any other
  page) should have a custom preview. **The basename MUST be `cover.png`**
  for `bk-check-social-cover` to pass — the verifier hard-fails on any
  other filename. Resize/rename existing covers if needed.

## What This Installs

| File | Purpose |
|------|---------|
| `plugins/social_override.py` | Hook that overrides og:image / twitter:image when a page declares `image:` |
| `mkdocs.yml` (edited) | Adds a top-level `hooks:` entry loading the file above |

The hook is loaded via MkDocs' `hooks:` config option, **not** as a plugin.
This avoids name collisions with other projects that also have a top-level
`plugins/` directory or `social_override` package.

## Installation Workflow

### Step 1: Create the Hook File

Create `plugins/social_override.py` at the project root (NOT under `docs/`).
Use exactly this content:

```python
"""MkDocs hook that overrides og:image and twitter:image with a page's
`image:` frontmatter value.

Behavior:
    - If the page has `image:` in its frontmatter, og:image and
      twitter:image are set to site_url + image (absolute URL), and an
      existing og:image:type is corrected to match the image's extension.
    - If the page has no `image:`, the hook is a no-op. All meta tags
      emitted by mkdocs-material (and by the social plugin, if enabled)
      pass through unchanged.

The cover image (img/cover.png) is therefore used ONLY for pages that
declare it explicitly -- typically docs/index.md. There is no site-wide
default.

Loaded via the `hooks:` entry in mkdocs.yml, not as a plugin -- this
avoids collisions with other projects that also install a package
called `social_override` or a top-level module called `plugins`.
"""

import re


def on_post_page(html, page, config, **kwargs):
    image = (page.meta or {}).get("image")
    if not image:
        return html

    site_url = config.get("site_url") or ""
    if not site_url:
        return html

    if image.startswith(("http://", "https://")):
        image_url = image
    else:
        image_url = site_url.rstrip("/") + "/" + image.lstrip("/")

    og_tag = f'<meta property="og:image" content="{image_url}">'
    og_pattern = re.compile(
        r'<meta\s+property="og:image"\s+content="[^"]*"[^>]*>'
    )
    if og_pattern.search(html):
        html = og_pattern.sub(og_tag, html, count=1)
    else:
        html = html.replace("</head>", f"  {og_tag}\n</head>", 1)

    tw_tag = f'<meta name="twitter:image" content="{image_url}">'
    tw_pattern = re.compile(
        r'<meta\s+(?:property|name)="twitter:image"\s+content="[^"]*"[^>]*>'
    )
    if tw_pattern.search(html):
        html = tw_pattern.sub(tw_tag, html, count=1)
    else:
        html = html.replace("</head>", f"  {tw_tag}\n</head>", 1)

    # The social plugin's generated cards are PNGs, so it always emits
    # og:image:type image/png. Make the type match this page's image
    # instead -- a .jpg cover would otherwise be announced as a PNG.
    # (Only an existing tag is changed; none is added.)
    image_types = {".png": "image/png", ".jpg": "image/jpeg",
                   ".jpeg": "image/jpeg", ".gif": "image/gif",
                   ".webp": "image/webp"}
    extension = "." + image_url.split("?", 1)[0].rsplit(".", 1)[-1].lower()
    if extension in image_types:
        html = re.sub(r'<meta\s+property="og:image:type"[^>]*>',
                      f'<meta property="og:image:type" '
                      f'content="{image_types[extension]}">', html)

    return html
```

### Step 2: Wire the Hook into `mkdocs.yml`

Add a top-level `hooks:` block. Place it directly under the `plugins:` block
for discoverability. The exact location doesn't matter to MkDocs, but the
block must be at the top level (not nested under `plugins:` — `hooks:` is a
peer of `plugins:`, not a child).

```yaml
# Hooks -- loaded as raw Python modules, not plugins (avoids name collisions).
# `plugins/social_override.py` overrides og:image and twitter:image with the
# page's `image:` frontmatter value when present. Pages without `image:` are
# untouched -- mkdocs-material's default meta tags (and the social plugin's
# generated card, if enabled) pass through.
hooks:
  - plugins/social_override.py
```

### Step 3: Add `image:` Frontmatter to Pages That Need It

Only pages that declare `image:` in their frontmatter get a custom social
preview. For most intelligent textbooks this means the home page
(`docs/index.md`) and nothing else — sharing a chapter URL on Slack should
still brand the unfurl with the book cover, which happens naturally because
chapter pages don't override the image, and Material's defaults take over.

If the project was scaffolded by `home-page-template.md`, the home page
frontmatter already declares `image: img/cover.png`:

```yaml
---
title: {{Book Title}}
description: {{One- or two-sentence book description.}}
image: img/cover.png
hide:
  - toc
---
```

Notes:

- The hook reads only the `image:` key. `og:title`, `og:description`,
  `og:url`, `twitter:card`, `twitter:title`, and `twitter:description` are
  emitted by mkdocs-material's own templates (and by the social plugin when
  enabled) — not by this hook. To change those values, edit the page's
  `title:` / `description:` frontmatter or the project's `site_name:` /
  `site_description:`.
- Older templates may also include `og:image:` and `twitter:image:` keys —
  those are harmless but unused. The hook only looks at `image:`.

### Step 4: Build and Verify Locally

```bash
mkdocs build
grep -E '(og|twitter):image' site/index.html
```

The `og:image` and `twitter:image` URLs on a page with `image:` frontmatter
should be absolute (start with `site_url`) and point at the declared image.
On a page without `image:` frontmatter, you'll see whatever Material emits
by default — which is the correct behavior.

### Step 5: Run the Cover-Page Verifier

The verifier (`~/.local/bin/bk-check-social-cover`) checks the deployed
home page over HTTP. To test the local build before deploying, stage the
site under a `/<project>/` path and serve it:

```bash
# Replace <project> with the repo / site path segment, e.g. "psychology"
PROJ=<project>
rm -rf /tmp/bk-serve && mkdir -p /tmp/bk-serve/$PROJ
cp -r site/* /tmp/bk-serve/$PROJ/
(cd /tmp/bk-serve && python -m http.server 8765 >/tmp/bk-serve.log 2>&1 &)
sleep 1
~/.local/bin/bk-check-social-cover http://127.0.0.1:8765/$PROJ/
# cleanup:
pkill -f "python -m http.server 8765"
rm -rf /tmp/bk-serve /tmp/bk-serve.log
```

The script verifies:

1. `og:title` is present and reasonable length (warn outside 40-60 chars).
2. `og:description` is present and reasonable length (warn outside 55-200).
3. `og:image` is present, basename is **exactly** `cover.png`, and the
   image URL is reachable (HTTP 200).

The image-reachability check HEAD-requests the URL the hook produced — which
is `site_url + image`, i.e. the production URL. As long as the deployed site
already has `cover.png` at that path, this passes even when running the
verifier against a local server. (On a brand-new project with no deploy yet,
deploy first via `mkdocs gh-deploy`, then re-run.)

A successful run exits 0. Warnings are non-fatal. Errors are fatal —
typically caused by:

| Error | Fix |
|-------|-----|
| `og:image MISSING` | The hook didn't load. Check `hooks:` path in `mkdocs.yml`. |
| `og:image basename MUST be "cover.png"` | Rename the file to `cover.png` and update `image:` frontmatter. |
| `cover image not reachable (HTTP 404)` | Deploy first (`mkdocs gh-deploy --force`), or fix the `image:` path. |

### Step 6: Deploy

```bash
mkdocs gh-deploy --force
```

After deploy, run the verifier against the live URL with no localhost
plumbing:

```bash
~/.local/bin/bk-check-social-cover <project>
# or
~/.local/bin/bk-check-social-cover https://<user>.github.io/<project>/
```

## Forcing a Social Cache Refresh

When a preview image is wrong on a *deployed* site — typically because an
earlier deploy shipped the broken value and someone already shared the URL
— fixing the hook and redeploying is not enough. LinkedIn, Facebook, and
Slack cache `og:image` per URL for days or weeks. Future shares of the
same URL keep pulling the cached (broken) preview until the cache is
explicitly invalidated.

### Verify the Fix Is Actually Live First

Before fighting any cache, confirm the deployed HTML is correct.
Otherwise the scrapers will re-cache the broken value and you'll be back
where you started:

```bash
curl -s https://<user>.github.io/<project>/ | grep -E '(og|twitter):image'
~/.local/bin/bk-check-social-cover <project>
```

`og:image` should point at the intended `cover.png` and the verifier
should exit 0. Only then run the per-platform refresh below.

### Per-Platform Cache Invalidation

| Platform | Tool | URL |
|----------|------|-----|
| LinkedIn | Post Inspector | https://www.linkedin.com/post-inspector/inspect/ |
| Facebook / Threads | Sharing Debugger | https://developers.facebook.com/tools/debug/ |
| X (Twitter) | Card Validator (legacy but still triggers a re-fetch) | https://cards-dev.twitter.com/validator |
| Slack | Re-unfurl the link in any channel after deleting the prior message; Slack caches per-message, not per-URL | — |

Paste the page URL into the inspector and click Inspect / Scrape Again /
Preview. The platform re-fetches the page, replaces its cached metadata,
and subsequent shares of that URL use the new image.

### Cache-Bust with a Query String (Fallback)

If a platform still serves stale metadata after the inspector run
(LinkedIn occasionally does this for ~24 hours), share the URL with a
throwaway query parameter, e.g. `https://<user>.github.io/<project>/?v=2`.
Crawlers treat that as a new URL and fetch fresh metadata. Bump the value
again if needed.

This is a workaround, not a fix — the canonical URL will catch up on its
own once the platform's TTL expires.

## Best Practices

### Pair the Hook with a Cover Image Only Where You Want One

The hook is opt-in per page: it only acts on pages whose frontmatter
declares `image:`. If the project doesn't have a cover image yet but you
want one on the home page, route the user to `cover-image-generator.md`
first, then add `image: img/cover.png` to `docs/index.md`.

A project that never declares `image:` on any page is a valid state — the
hook is installed but inert, and Material's default social meta tags
(or the social plugin's generated cards) take over for every page.

### Compatibility with the Material Social Plugin

The `mkdocs-material[imaging]` `social` plugin generates per-page card
images but requires Cairo (`brew install cairo` on macOS, plus
`pip install "mkdocs-material[imaging]"`). When a project enables the
social plugin without Cairo present, every build fails with a
`cairosvg` import error.

This hook works fine alongside the social plugin or without it:

- **Without the social plugin:** the hook overrides only `og:image` /
  `twitter:image` on pages that declare `image:`. Other social meta tags
  use Material's defaults.
- **With the social plugin:** the hook still overrides on pages that
  declare `image:` (replacing the plugin's generated card URL with the
  declared image). Pages without `image:` keep the per-page generated
  card.

For most intelligent textbooks, the social plugin isn't needed — declaring
`image: img/cover.png` only on the home page is enough, since that's the
URL most often shared.

### Override Per Page, Not Globally

The hook is per-page-explicit by design. To override the preview image on
a specific page, add `image:` to that page's frontmatter. Pages without
`image:` are not touched, so chapter URLs unfurl using whatever Material /
the social plugin emit on their own.

### Don't Hand-Edit the Generated HTML

If a verifier failure tempts you to patch `site/index.html` directly, stop.
The fix belongs in either the hook or the frontmatter. Hand-edits get
clobbered on the next `mkdocs build`.

## Footgun: Frontmatter Key Collisions

YAML frontmatter keys with colons (`og:image:`, `twitter:image:`) parse as
**namespaced keys** in MkDocs' YAML loader, and *most* MkDocs plugins
silently ignore unknown keys. Authors who add `og:image: /img/cover.png`
to frontmatter and inspect the rendered HTML often find no meta tag and
assume MkDocs is broken.

The fix is to use the plain `image:` key (no colons in the key name) that
this hook actually reads. `og:image:` and `twitter:image:` in frontmatter
are no-ops.

## Troubleshooting

### "og:image isn't being overridden on my home page"

- Confirm `docs/index.md` frontmatter has `image: img/cover.png` (the
  plain `image:` key, not `og:image:` or `twitter:image:`).
- Confirm the `hooks:` block is at the top level of `mkdocs.yml`, not
  nested under `plugins:`.
- Confirm the file is at `plugins/social_override.py` relative to
  `mkdocs.yml`, not under `docs/`.
- Run `mkdocs build --verbose` and look for `Running on_post_page event`
  entries. If none appear for `social_override`, the path is wrong.

### "og:image points to localhost, not the production URL"

- The hook uses `site_url` from `mkdocs.yml`. Confirm it's set to the
  production URL (e.g. `https://dmccreary.github.io/<project>/`), not a
  localhost address.

### "Title is too short / description missing" warning from bk-check-social-cover

These are content fixes, not hook bugs — this hook does not control
`og:title` or `og:description`. Those come from Material's defaults
(driven by `site_name`, `site_description`, and per-page `title:` /
`description:` frontmatter), or from the social plugin when enabled.
Edit `mkdocs.yml` or the page's frontmatter to fix.

### "I want a different preview image on a specific chapter"

Add `image: img/chapters/01-foo.png` (or any path under `docs/`) to that
chapter's frontmatter. The hook picks it up automatically. Pages without
`image:` keep Material's default behavior.

## Related References

- `home-page-template.md` — establishes the frontmatter the hook reads
- `cover-image-generator.md` — generates the `cover.png` the hook points to
- `mkdocs-features.md` — alternative `social` plugin path (Cairo-based)

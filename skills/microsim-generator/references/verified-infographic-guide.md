
# Verified Infographic Poster Guide

> A route of the `microsim-generator` skill. Formerly the standalone skill
> `verified-infographic-generator`, then briefly a `book-media-generator` route.
>
> **This route does not produce a MicroSim.** It writes a static poster PNG plus its audit
> trail to `docs/posters/<slug>/`. Skip the microsim-generator SKILL.md pipeline (scaffold,
> `.js`, `CANVAS_HEIGHT`, iframe insertion, quality validator) entirely and follow the 8
> phases below instead.
>
> **Phases 1–4 are reusable on their own.** When an actual MicroSim must carry sourced facts —
> a comparison table of real products, a chart of published measurements, a timeline of dated
> events — run Phases 1–4 to produce a verified, cited claim set, then hand it to the matched
> sim guide and carry each `source_id` into that sim's data file. Phases 5–8 are poster
> rendering and do not apply.
>
> **Two standing policies gate this route:**
>
> 1. **Never render a static image unless the user specifically asked for one.** "Make an
>    infographic" is not a request for a PNG. Run Phases 1–4, then hand the claim set to an
>    interactive guide.
> 2. **Every poster that does get rendered is then wrapped in an interactive overlay** —
>    Phase 9 below. A poster is never the final deliverable.

**Version:** 1.0

## Overview

This skill produces high-quality infographic posters where **fact-verification is done by Claude in text** and the text-to-image engine is invoked **only in the final rendering step**, after all content has been locked and approved.

It exists because one-shot text-to-image generation of fact-based infographics has a very high fabrication rate. In one observed session generating a poster about biophilic design, 8 of 10 numeric claims (80%) were unsupported by the cited sources, and 2 of 5 citations were fictional or misattributed. Once incorrect text is baked into pixels, it cannot be corrected without regenerating, and readers have no way to audit where the numbers came from.

## Core Principles

1. **Separate facts from pixels.** Never let the image model choose which numbers to display.
2. **Evidence before composition.** No visual layout work begins until every claim has a verified source.
3. **Bake nothing unverified.** Any unverified claim blocks the pipeline, is downgraded to qualitative language, or is replaced.
4. **Preserve an audit trail.** Every number and citation in the final image must be traceable to a specific source URL and quoted passage in a sidecar file.
5. **Break symmetry bias.** Two-column "versus" layouts must explicitly allow asymmetric content — missing data on one side is a first-class output, not something to fabricate around.

## When to Use

Use the **full** 9-phase workflow when the user has **specifically requested a static poster,
image, or PNG** that contains numeric claims — for example:

- "Make a *poster* comparing X and Y with real numbers"
- An evidence-based summary *poster* citing research, studies, or data
- An Earth Day / science communication *poster* with statistics, requested as a printable image

Use **Phases 1–4 only** (verification, then hand off to an interactive guide) when the request
involves numeric claims but no static format was named:

- "Make an infographic about …" / "visualize the data on …" / "compare X and Y"
- Any request where an interactive sim would serve the reader at least as well

When in doubt, do not render a static image. A flat PNG emits no interaction events, so it
cannot tell us whether readers understood it; the interactive form is the default deliverable
for this library (see the Level 2+ target in the root `CLAUDE.md`).

Do **NOT** use this skill for:

- Purely decorative images with no factual claims
- Diagrams where the user supplies pre-verified data and just needs a layout rendered
- Artistic posters, logos, or illustrations without numeric content
- Static diagrams of known objects — use [infographic-overlay-guide.md](infographic-overlay-guide.md)
  for annotated scientific illustrations (see [Related Guide](#related-guide-interactive-infographic-overlays) below)

## Related Guide: Interactive Infographic Overlays

This guide and [infographic-overlay-guide.md](infographic-overlay-guide.md) both have
"infographic" in the name but solve different problems. Pick by asking **where the words live**:

| | This guide (verified poster) | infographic-overlay-guide.md |
|---|---|---|
| Produces | A static PNG + audit trail in `docs/posters/<slug>/` | A MicroSim in `docs/sims/{sim-id}/` |
| Problem solved | Keeping baked-in numbers from being fabricated | Making an image explorable |
| Text in the image | Text and numbers *are* the content | **None** — not even a title |
| Where labels live | Inside the pixels, locked before rendering | `data.json`, rendered at runtime by `diagram.js` |
| Web search / citations | Mandatory (2+ searches per claim, `source_id` per element) | Not used |
| MicroSim pipeline | No — this guide skips it entirely | Yes |

Rule of thumb: **numeric claims that could be wrong → this guide; structures that need naming
→ the overlay guide.** A "biophilic vs. brutalist offices, with percentages" poster is
verified. An anatomy diagram is an overlay.

### Combining the two

They compose in two ways:

1. **Verified facts inside an overlay.** As noted at the top of this guide, Phases 1–4 stand
   alone. When an overlay MicroSim's callout descriptions or zone `facts[]` carry sourced
   statistics, run Phases 1–4 here to produce a cited claim set, then carry each `source_id`
   into the overlay guide's `data.json`. Phases 5–8 do not apply.
2. **An overlay on top of a verified poster.** A rendered `poster.png` can become the
   background image for the overlay guide's **grid** engine, giving readers hover zones over
   the poster's columns. Because the poster already has printed column titles, keep
   `showLabels: false`. The Gallery Thumbnails section below assumes this pairing — poster
   detail pages keep the full-size PNG for hover accuracy while gallery cards use the thumbnail.

## Prerequisites

- Web search access (for Phase 2 source discovery)
- A text-to-image model available in the final step (OpenAI Images 2.0, Gemini, DALL·E, etc.)
- A project output directory (default: `docs/posters/`) where the poster, verification report, and sidecar source file will be saved together

## Workflow

The skill runs in **8 phases**. Phases 1–6 are executed by Claude. Phase 7 is the one image-model call. Phase 8 is a Claude audit of the final render.

### Phase 1: Intake & Claim Planning

Gather from the user:

- **Topic** of the poster
- **Intended audience** (grade 9-12, general public, policy maker, etc.)
- **Format** (landscape/portrait, dimensions, style preference)
- **Comparison structure** if any (A vs. B, single-subject, timeline, etc.)
- **Known references** the user wants to incorporate

Produce a **Claim Plan** — a structured list of 5–10 factual claims the poster must make. For each claim, record:

- Subject (what it's about)
- Metric type (percentage, count, range, qualitative descriptor)
- Polarity (positive outcome, negative outcome, neutral)
- Desired prominence (hero number, supporting stat, footnote)

Flag any planned comparison that invites symmetry bias. Tell the user explicitly: **"The 'versus' side may end up with less data than the main side. We will not invent numbers to balance it."**

Save the claim plan to `docs/posters/<slug>/01-claim-plan.yaml` using the template in `references/infographic-claim-plan-template.yaml`.

### Phase 2: Source Discovery

For each claim in the plan:

1. Run **at least two independent web searches** with different query phrasings.
2. Collect candidate sources. For each, record: title, authors, year, publisher or journal, URL, and a quoted sentence that directly supports the claim.
3. Prefer, in order:
   - Peer-reviewed journal articles
   - Systematic reviews and meta-analyses
   - Government reports (EPA, NOAA, USGS, UK GBC, WHO, etc.)
   - Named institutional studies with authors
4. Reject:
   - Blog posts citing unnamed "studies"
   - Marketing pages and vendor whitepapers
   - Wikipedia as a sole source (can be a pointer to primary sources)
   - Statistics without a traceable primary paper
   - Social media posts as primary sources

### Phase 3: Verification & Classification

Classify each claim into one of four buckets:

| Bucket | Meaning | What happens in the poster |
|---|---|---|
| **VERIFIED** | Specific number matches a specific peer-reviewed paper with a quoted passage | Use the exact number |
| **DIRECTIONAL** | Effect direction is well-established but the exact number differs across studies | Use a range (e.g., "+6% to +15%") or best-supported single study |
| **QUALITATIVE-ONLY** | Effect is supported but not quantified reliably | Use words ("lower," "significant," "elevated") — no fake percentage |
| **REJECTED** | No credible source | Remove from the poster or replace with a VERIFIED claim on a related subject |

For every VERIFIED and DIRECTIONAL claim, store a citation record:

```yaml
- claim_id: wellbeing_increase
  value: "+15%"
  source: "Human Spaces / Interface (2015)"
  authors: "Cooper, C. et al."
  year: 2015
  url: "https://..."
  quote: "employees who work in environments with natural elements report a 15% higher level of well-being"
  classification: VERIFIED
```

Save the full **Verification Report** to `docs/posters/<slug>/02-verification-report.md` using the template in `references/infographic-verification-report-template.md`.

**Abort condition:** If more than 20% of planned claims are REJECTED, stop the pipeline and tell the user the topic may not support the original framing. Offer to reshape the poster around the VERIFIED claims that remain.

### Phase 4: User Checkpoint (MANDATORY)

Present the Verification Report to the user. Show:

- Every original claim and its verdict
- Which claims survived with exact numbers
- Which were softened to qualitative language
- Which were dropped entirely
- Any fabrication risks detected (e.g., a "vs." side with thin evidence)

Wait for explicit user approval before proceeding. The user may:

- Approve the final claim set as-is
- Request additional sources for a specific claim
- Reshape the poster (remove comparison, change topic, widen scope)
- Accept qualitative language in place of a missing percentage

**Do not proceed to layout or rendering without this approval.** This is the single most important safety checkpoint in the pipeline.

### Phase 5: Layout Specification

Draft a structured layout spec in YAML (use `references/infographic-layout-spec-template.yaml`). Every text element must reference a `source_id` from the verification report, or be marked as a non-factual design element (title, decorative label, caption).

Key layout constraints:

- **Asymmetric layouts are allowed.** If the comparison side has only 3 verified claims to the main side's 5, render 3 vs. 5 — do not invent filler.
- **Mark qualitative claims clearly.** Use descriptor words instead of fake percentages ("Elevated," "Reduced," "Significant").
- **Cite in-place where possible.** Small parenthetical "(Author, Year)" under each statistic, with a full source list at the bottom.
- **One source per statistic minimum.** If a claim has no `source_id`, it cannot appear in the layout.

Save to `docs/posters/<slug>/03-layout-spec.yaml`.

### Phase 6: Image Prompt Assembly

Programmatically compose the text-to-image prompt from the approved layout spec. **Never re-author numbers at this stage** — copy them verbatim from the spec.

The assembled prompt must include these explicit instructions to the image model:

```
Render the following exact text verbatim. Do not substitute any numbers,
paraphrase any labels, or invent additional statistics, rows, or citations.
All percentages, author names, years, and institution names must appear
exactly as written below. If you cannot render any text element legibly
at the requested size, leave it out rather than approximating.
```

Use the prompt template in `references/poster-image-prompt.md`.

Save to `docs/posters/<slug>/04-image-prompt.md`.

**Dry-run check:** show the assembled prompt to the user one last time before sending to the image model. Ask: "Ready to render?"

### Phase 7: Final Rendering

Send the locked prompt to the configured text-to-image model. Save the rendered PNG to:

```
docs/posters/<slug>/poster.png
```

### Phase 8: Post-Render Audit

Claude reads the rendered image (multimodally) and confirms:

1. Every number in the layout spec appears correctly in the pixels.
2. Every citation (author, year, institution) is spelled correctly and matches the source list.
3. No unexpected rows, legend entries, or statistics have been hallucinated.
4. No approved rows are missing.

If drift is detected, log the specific mismatch, regenerate the image (Phase 7), and audit again. Cap at 3 regeneration attempts; beyond that, escalate to the user.

Produce the final **sidecar source file** at `docs/posters/<slug>/sources.md` — a reader-facing document listing every claim, number, and full citation with URL, so the poster is independently fact-checkable.

### Phase 9: Interactive Overlay (MANDATORY)

**A rendered poster is never the final deliverable.** Once Phase 8 passes, wrap `poster.png` in
a grid overlay by following the Grid Overlay Workflow in
[infographic-overlay-guide.md](infographic-overlay-guide.md):

1. Create the overlay page alongside the poster (`docs/posters/<slug>/main.html`), or as a sim
   directory under `docs/sims/` if the book indexes it with the other MicroSims.
2. Point `data.json.image` at the rendered `poster.png` — full size, not the thumbnail.
3. Set `showLabels: false`. The poster already has printed column titles, so chip labels would
   double them.
4. Define one `zones[]` entry per poster region, with `summary` and `facts[]` drawn from the
   approved layout spec. **Carry each claim's `source_id` into the zone facts** so the citation
   stays visible on hover — the audit trail survives into the interactive form.
5. Add quiz questions covering the poster's key claims, so the overlay measures comprehension
   rather than mere exposure.
6. Calibrate zone rectangles with `?edit=true` and copy the JSON back into `data.json`.

**Why this is mandatory.** The whole point of Phases 1–8 is that the poster's numbers are
trustworthy — but a flat image emits nothing, so we have no signal about whether any reader
engaged with those numbers. The overlay turns each region into an instrumented zone: hovers,
zone opens, and quiz attempts become interaction events that let us predict whether the concepts
in the infographic have been mastered.

**Aggregate only.** Per the "2.99" design target in the root `CLAUDE.md`, aggregate these events
across all readers to estimate concept understanding. Do not retain per-student performance
history tied to an identifiable reader — that crosses into Level 3 and the student-data-privacy
obligations this project does not take on.

## Gallery Thumbnails

Poster galleries (e.g. `docs/posters/index.md`) typically render every poster as a card in a 3-column CSS grid at ~600px wide. If the grid image points straight at the full-size rendered PNG (1536x1024, 2-3 MB is typical for these image models), a gallery of even 50-90 posters ships hundreds of MB on a single page load — the full resolution is wasted since the grid never displays the image larger than the column width.

**After adding one or more posters to a gallery** (or whenever a user reports the gallery page loading slowly), run:

```bash
python3 $BK_HOME/skills/microsim-generator/scripts/posters/generate-poster-thumbnails.py --posters-dir docs/posters
```

This generates a `<slug>-thumb.jpg` (900px wide JPEG, quality 82) next to each poster's full-size PNG and rewrites the gallery `index.md` so grid cards reference the thumbnail. It does **not** touch the poster's own detail page — the interactive callout/grid overlay (`main.html`) keeps loading the full-size PNG, since hover/zoom accuracy there benefits from full resolution. Only the gallery-grid reference is swapped.

Measured result on an 86-poster gallery: 233.5 MB → 11.9 MB (~95% reduction), no visible quality loss at gallery-card size. The script is idempotent — safe to re-run any time new posters are added, and `--dry-run` previews the change without writing files.

## Output Files

For a poster with slug `<slug>`, the skill produces:

```
docs/posters/<slug>/
├── poster.png                    # Final rendered image
├── sources.md                    # Reader-facing citation list
├── 01-claim-plan.yaml            # Phase 1
├── 02-verification-report.md     # Phase 3
├── 03-layout-spec.yaml           # Phase 5
├── 04-image-prompt.md            # Phase 6
├── data.json                     # Phase 9 - overlay zones, facts, quiz
└── main.html                     # Phase 9 - grid overlay (grid-diagram.js)
```

The numbered intermediate files are the audit trail. `poster.png` and `sources.md` are the
published artifacts; `main.html` + `data.json` are the interactive form readers actually use,
and the source of the interaction events.

## Success Criteria

- **100%** of numeric claims in the final image trace to a specific URL and quoted passage.
- **0** citations to non-existent, misattributed, or fictional sources.
- **<5%** post-render drift (percentage of claims that render incorrectly in pixels vs. the layout spec).
- **Generation time** is higher than one-shot (expect 5–15 minutes vs. seconds) but produces an artifact defensible for publication.

## Anti-Patterns to Avoid

Flag these as footgun patterns if you notice the pipeline drifting toward them:

- **Symmetry fabrication** — inventing mirror-statistics for the weaker side of a versus comparison.
- **Meta-source citation** — citing a review paper (like Browning et al. 2014) as if it were the original empirical source for a specific percentage.
- **Round-trip marketing stats** — numbers that appear in many marketing pages with no traceable primary paper (e.g., "-23% cortisol in biophilic offices").
- **Geographic misattribution** — labeling research by the wrong country (e.g., calling Japanese Shinrin-yoku research "Finnish studies").
- **Image-model number drift** — image models silently change "+12%" to "+21%" or misspell author names; Phase 8 audit exists to catch this.

## Example Session

See `references/infographic-biophilic-case-study.md` for a worked example showing how this workflow would have prevented the 10 errors found in a real one-shot-generated poster on biophilic vs. brutalist spaces.

## References

All templates and examples live in the `references/` subdirectory:

- `infographic-claim-plan-template.yaml` — Phase 1 output
- `infographic-verification-report-template.md` — Phase 3 output
- `infographic-layout-spec-template.yaml` — Phase 5 output
- `poster-image-prompt.md` — Phase 6 output
- `infographic-biophilic-case-study.md` — worked example

`scripts/posters/generate-poster-thumbnails.py` — gallery thumbnail generation (see "Gallery Thumbnails" above)

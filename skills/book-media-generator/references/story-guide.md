
# Illustrated Story / Graphic Novel Guide

> Formerly the standalone skill `story-generator`.

This skill generates complete graphic novel narratives about key contributors to science, mathematics, and technology — and fictional case-study stories — for intelligent textbooks built with MkDocs Material. The default story length is **12 panels plus a cover (13 images total)**, but the panel count is configurable: simpler stories can be told in 6–8 panels, and synthesis stories can run to 16. Each panel includes a narrative paragraph below it and a detailed image-generation prompt in a collapsible `<details>` block.

As of the 2026-04 skill update, the skill can also **automatically generate every panel image** (1 cover + N panels) natively at 16:9 (1344×768) via multiple text-to-image APIs including Google Gemini and OpenAI gpt-image-1. Current cost for high-quality images with accurate text placement is approximately **$0.039 per image** (so ~$0.51 for a default 13-image story, or ~$0.27 for a 6-panel story). See "Step 3.5: Generate Images" below.

## The `--panels N` Argument

The skill accepts an optional `--panels N` argument that controls how many numbered panels the story has. The cover image is always produced separately, so a story has **N + 1** total images.

- **Default:** `--panels 12` (the classic graphic-novel arc)
- **Recommended range:** 4 to 16
- **Below 4:** the arc has no room to develop; consider whether you want a story at all
- **Above 16:** the reader is paying attention to a lot of pictures; split into two stories

**How to choose N:**

| Story shape | Suggested N |
|---|:---:|
| Single technique, before/after only | 6 |
| Linear discovery (audit → fix → result) | 7–8 |
| Mystery + reveal + multi-step fix | 9 |
| Full historical-figure life arc | 12 (default) |
| Multi-chapter synthesis or capstone montage | 14–16 |

**How users invoke it:**

The user types something like:

> book-media-generator (story route): "The Cache That Wasn't" --panels 8

When you receive `--panels N` in the user's invocation, treat N as the canonical panel count for the rest of the workflow. If no `--panels` argument is given, default to 12.

**Why this works without script changes:**

Both `generate-images.py` and `verify-images.py` count `<details>...Image Prompt...</details>` blocks in `index.md` to determine how many images to produce or verify. They do not hardcode 12. Whatever panel count you write in `index.md` is what the scripts will generate and verify — no flag needed on the script side.

## When to Use This Skill

Use this skill when:

- The user requests a new graphic novel story about a scientist, mathematician, engineer, or other historical figure
- Adding a story to a Stories / History section of any intelligent textbook
- Creating educational narrative content with embedded image prompts
- The user mentions "story", "graphic novel", or "narrative" about a historical figure
- **The user says "give me some ideas for graphic-novel stories"** — triggers the Story Ideas Generator workflow (see below)

## Story Ideas Generator

When the user says **"give me some ideas for graphic-novel stories"**, generate a curated list of mini-graphic novel ideas tailored to the current textbook's subject matter. Save the result to `docs/stories/story-ideas.md`. Each idea should include a **suggested panel count** (typically 6 to 12) chosen to match the natural shape of that story — see the Panel Count guidance above. Don't default everything to 12; tight 6–8 panel stories are often stronger than bloated 12-panel ones.

### Workflow

#### Step 1: Analyze the Textbook's Subject Matter

Read the following files to understand the textbook's topic, audience, and key themes:

1. `docs/course-description.md` — the course title, description, target audience, and learning objectives
2. `mkdocs.yml` — the site name and nav structure for additional context
3. `docs/learning-graph/learning-graph.csv` (if it exists) — the concept list and taxonomy categories

Extract:
- The **subject domain** (e.g., theory of knowledge, geometry, functions, biology)
- The **target audience** (e.g., IB students, AP students, grades 9-12)
- The **key themes and concepts** from the course description and learning graph

#### Step 2: Generate Story Ideas

Create a list of **15-20 story ideas** that connect to the textbook's subject matter. Each story idea should be a mini-graphic novel concept with a suggested panel count between 6 and 12 (or up to 16 for synthesis/capstone stories).

**Diversity requirements — draw from ALL of these categories:**

1. **Historical figures** — scientists, mathematicians, engineers, inventors, and philosophers whose work directly relates to the textbook's topics
2. **Diverse innovators** — people from underrepresented groups (women, people of color, Global South contributors) who made significant contributions to the field
3. **Science vs. dogma** — stories of people who used evidence and reason to challenge religious dogma, political orthodoxy, or institutional resistance
4. **Fighting misinformation** — stories of people who used science and critical thinking to make the world better by exposing dangerous falsehoods (e.g., Rachel Carson's *Silent Spring* exposing the dangers of DDT, Ignaz Semmelweis championing handwashing)
5. **Unsung heroes** — lesser-known contributors whose work was foundational but overlooked
6. **Contemporary figures** — living or recently active people advancing the field today

**For each story idea, provide:**

- **Title** — a compelling, concise title (e.g., "Silent Spring — Rachel Carson's Fight Against DDT")
- **Subject** — full name, birth/death years, country (or, for fictional case-study stories, the **Setting**)
- **Theme** — the central narrative theme (e.g., "courage to challenge industry", "persistence through rejection")
- **Connection to textbook** — how this story relates to specific concepts or chapters in the textbook
- **Panels** — suggested panel count (6–16) with a one-line rationale for that length. Use the Panel Count guidance: 6 for single-technique stories, 8 for linear discoveries, 9 for mystery+fix, 12 for full life arcs, 14–16 for synthesis montages. The user can override this when invoking the skill via `--panels N`.
- **Synopsis** — 2-3 sentences describing the story arc across the suggested panels
- **Why this story inspires** — 1 sentence on why young readers will connect with it

#### Step 3: Format and Save

Save the story ideas to `docs/stories/story-ideas.md` using this format:

```markdown
# Story Ideas for {Book Title}

These mini-graphic novel ideas are designed to inspire young
readers by connecting the subject matter of this textbook to
the real people who shaped the field. Each story can be
generated using the book-media-generator story route, with the
suggested panel count or your own override via `--panels N`.

## Selection Criteria

Stories were selected for:

- **Relevance** — direct connection to the textbook's key concepts
- **Diversity** — range of backgrounds, cultures, genders, and time periods
- **Inspiration** — themes that resonate with the target audience
- **Drama** — compelling narrative arcs with conflict and resolution

## Story Ideas

### 1. {Title}

| | |
|---|---|
| **Subject** | {Full Name} ({birth}–{death}), {country} |
| **Theme** | {Central narrative theme} |
| **Connection** | {How it connects to specific textbook concepts} |
| **Panels** | **{N}** — {one-line rationale for that length} |

{2-3 sentence synopsis}

*Why this inspires:* {1 sentence}

---

### 2. {Title}

...

## How to Generate a Story

To turn any of these ideas into a full graphic novel with
generated images, use:

> book-media-generator (story route): {Story Title} --panels {N}

Provide the subject's name (and optionally `--panels N` to
override the suggested count) and the skill will handle the
rest — writing the narrative, creating image prompts, and
optionally generating all panel images via multiple
text-to-image APIs (Google Gemini, OpenAI gpt-image-1, or
others). Current cost for high-quality images with accurate
text placement is
approximately **$0.039 per image**, so $0.039 × (N + 1) per
story — about $0.27 for 6 panels, $0.51 for 12 panels.
```

#### Step 4: Update Navigation

Add the story ideas page to `mkdocs.yml` under the Stories section:

```yaml
- Stories:
    - Overview: stories/index.md
    - Story Ideas: stories/story-ideas.md
    # ... individual stories follow
```

### Example: Theory of Knowledge

For a Theory of Knowledge textbook, the story ideas might include:

1. **"Silent Spring"** — Rachel Carson's fight to expose DDT dangers (science vs. industry misinformation)
2. **"The Starry Messenger"** — Galileo's telescope and the battle against geocentric dogma
3. **"Washing Away Death"** — Ignaz Semmelweis championing handwashing against medical establishment rejection
4. **"Decoding the Secret"** — Rosalind Franklin's uncredited X-ray crystallography work on DNA
5. **"The Lady of the Lamp"** — Florence Nightingale using statistical evidence to reform military hospitals
6. **"Thinking in Pictures"** — Temple Grandin redesigning animal handling through neurodivergent perception
7. **"The Vaccine Maker"** — Edward Jenner's smallpox vaccine overcoming public fear and superstition
8. **"Mapping Cholera"** — John Snow's data visualization that proved waterborne disease transmission
9. **"The Daring Hypothesis"** — Alfred Wegener's continental drift theory, rejected for decades then vindicated
10. **"Hidden Figures"** — Katherine Johnson's calculations that sent astronauts to space despite racial barriers



Each story follows a consistent structure designed to engage teenage and young-adult readers:

### Required Components

1. **YAML Frontmatter** — Title, description, Open Graph image paths
2. **Cover Image** — With detailed generation prompt in a `<details>` block
3. **Narrative Prompt** — Background context for the whole story
4. **Prologue** — Hook introducing the subject's significance
5. **12 Panels** — Each with narrative text, image placeholder, and image prompt
6. **Epilogue** — Lessons table (Challenge / Response / Lesson for Today)
7. **Call to Action** — Inspiring message connecting to readers
8. **Quotes** — 2-3 memorable quotes from the subject
9. **References** — 5 real working URLs (first 3 Wikipedia, then secondary sources). **Never use `(PLACEHOLDER)`.**

A template for the complete structure is at `references/story-index-template.md`.

### YAML Frontmatter

Use the Open Graph protocol for social media sharing:

```yaml
---
title: <Catchy Title> - <Subject Name>'s <Theme>
description: A graphic-novel story of how <brief description>...
image: /stories/{story-dir-name}/cover.png
og:image: /stories/{story-dir-name}/cover.png
twitter:image: /stories/{story-dir-name}/cover.png
social:
   cards: false
---
```

Where `{story-dir-name}` is the kebab-case directory name.

**Length guidance:**
- Title: 60-70 characters max (longer titles get truncated on social media)
- Description: 155-200 characters (1-2 punchy sentences)

### Image Prompt Requirements

Every image prompt must specify:

- Begin every prompt body with a panel identifier line:
  - Cover: `(This is the Cover Image. Do not include this label in the image.)`
  - Panels: `(This is Panel N. Do not include the panel number in the image.)` where N is the panel number
- Wide-landscape **16:9 format** (the `generate-images.py` script passes this via API config — the text in the prompt is redundant but harmless)
- Period-appropriate art style (see the Art Style Reference table below)
- Specific characters with physical features and clothing
- Specific setting including year and location
- Color palette guidance
- Emotional tone and mood
- At least 6 specific visual details per prompt to guide the generation and avoid generic outputs
- End with: `Generate the image immediately without asking clarifying questions.`

The `generate-images.py` script parses `<details><summary>Image Prompt</summary>...</details>` blocks directly from the story's `index.md`, so the block structure is load-bearing — do not change the HTML shape.

## Workflow

Some stories are about historical figures.  Some are about fictional setting or concepts. The workflow is the same either way, but the research and writing process differs slightly.

### Step 1: Gather Information and Plan the Story

Before writing, identify:

- The subject's full name and birth/death years
- Country and historical period
- Key discoveries, contributions, or life events
- Central theme (e.g., "persistence through failure", "seeing what others could not")
- Appropriate art style for the era
- 3-5 key life events (or story beats, for fictional stories) that will anchor the N panels (default N=12). Aim for one beat per ~2–3 panels — a 6-panel story usually has 3 beats; a 12-panel story usually has 4–6 beats. If `--panels N` was specified, use that N here.

### Step 2: Create the Story Directory

```bash
mkdir -p docs/stories/{story-dir-name-in-kebab-case}
```

Use kebab-case (lowercase with hyphens) for directory names: `ada-lovelace`, `rene-descartes`, `marie-curie`. Never use spaces or underscores.

### Step 3: Write the Story

Create `docs/stories/{story-dir-name}/index.md` following the template at `references/story-index-template.md`.

**Key conventions:**
- N numbered panels plus 1 cover = **N + 1 images total** (default N = 12, override with `--panels N`)
- Panels are numbered consecutively from `panel-01` to `panel-NN` — no gaps, no extras
- Each panel-identifier line should say "panel X of N" using the actual N for this story (e.g. "panel 3 of 8" in a 6-panel story would be wrong — every prompt's denominator must equal the total panel count)
- All image references use `.png` extension
- Panel image prompts wrapped in `<details><summary>Image Prompt</summary>...</details>` blocks
- Cover image prompt wrapped in `<details><summary>Cover Image Prompt</summary>...</details>`
- Every prompt body starts with a panel identifier line (see "Image Prompt Requirements")
- Narrative paragraphs go *below* each panel's image (not inside the `<details>` block)
- References: 5 real URLs, never `(PLACEHOLDER)` — see the References Guidance section below

**The template at `references/story-index-template.md` shows the canonical 12-panel layout.** For shorter or longer stories, follow the same per-panel pattern but stop at panel N. Do not pad with filler panels just to reach 12 — a tight 6-panel story is better than a bloated 12-panel one.

### Step 3.5: Generate Images (Optional but Recommended)

Once the markdown is written, generate the N + 1 panel images automatically with `scripts/story/generate-images.py`. The script auto-detects the panel count from the `<details>...Image Prompt...</details>` blocks in `index.md`, so you do not need to pass `--panels N` to the script — whatever you wrote in the markdown is what gets generated.

**Prerequisites:**

1. **Python package:**
   ```bash
   pip install google-genai
   ```

2. **API key** — Get a free one at https://aistudio.google.com/apikey, then:
   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```
   For persistence, add it to `~/.zshrc` or `~/.bashrc`. The free tier requires no credit card and no billing account.

**First run — verify the cover image before burning credits on 12 more panels:**

```bash
python3 $BK_HOME/skills/book-media-generator/scripts/story/generate-images.py \
    docs/stories/{story-dir-name} --first-only
```

This generates only the cover, verifies it is 16:9 via `sips`, and aborts automatically if the aspect ratio is wrong. Check the cover visually — does it match the art style and composition you want? If yes, proceed to the full run.

**Full run:**

```bash
python3 $BK_HOME/skills/book-media-generator/scripts/story/generate-images.py \
    docs/stories/{story-dir-name}
```

This generates all N + 1 images (cover + N panels) at native 1344×768 (16:9). Expected wall-clock time at the 10 RPM rate limit: roughly **6 × (N + 1) seconds** — about 90 seconds for a default 12-panel story, ~45 seconds for a 6-panel story. Each image is verified immediately after generation.

**Useful flags:**

| Flag | Purpose |
|---|---|
| `--first-only` | Generate only the cover image (aspect-ratio and style check) |
| `--skip-existing` | Skip any image whose PNG file already exists (safe for retries) |
| `--rpm N` | Override the default 10 RPM rate limit (use on paid tier with higher quota) |
| `--aspect-ratio W:H` | Override default `16:9`. Supported: `21:9`, `16:9`, `4:3`, `3:2`, `1:1`, `9:16`, `3:4`, `2:3`, `5:4`, `4:5` |

**What the script produces:**

- PNG files at `docs/stories/{story-dir-name}/cover.png` and `panel-01.png` through `panel-12.png`
- A per-story markdown log at `logs/{story-dir-name}-{YYYY-MM-DD}.md` with run metadata, summary totals, per-image table, and prompt excerpts
- An appended JSONL audit line at `logs/image-generation-usage.jsonl` for each image (timestamp, tokens, computed cost)

**If an image generation fails:**

The script catches safety-filter failures and API exceptions, logs the reason (including `finish_reason` and safety ratings), and continues to the next image. Failed images are skipped, not fatal. After the run, rerun with `--skip-existing` to retry only the failures. See the "Safety Filter Patterns" section below for how to soften prompts that trip the safety filter.

### Step 4: Verify Images

After generation, run the verify script to confirm every image is present and at the right aspect ratio:

```bash
python3 $BK_HOME/skills/book-media-generator/scripts/story/verify-images.py \
    docs/stories/{story-dir-name}
```

This is a read-only audit — it only checks, never modifies. Exit code 0 means clean, 1 means issues found. Especially useful for:
- Catching leftover square images from the old Antigravity workflow
- Verifying that all 13 panels exist after a partial run
- Pre-commit hooks

### Step 5: Add to Navigation

Edit `mkdocs.yml` to add the story in **chronological order by subject's birth year**:

```yaml
- Stories:
    - Overview: stories/index.md
    - <Subject Name> - <Title>: stories/<subject-name>/index.md
```

Example chronology (adapt to your project):
- Archimedes (287 BC)
- Galileo (1564)
- Descartes (1596)
- Newton (1643)
- Euler (1707)
- Fourier (1768)
- Faraday (1791)
- Lovelace (1815)
- Maxwell (1831)
- Tesla (1856)
- Marie Curie (1867)
- Einstein (1879)
- Noether (1882)
- Ramanujan (1887)
- Turing (1912)

### Step 6: Add a Grid Card to the Stories Index

Edit `docs/stories/index.md` to add a card using the MkDocs Material grid format:

```markdown
- **[<Story Title>](<subject-name>/index.md)**

    ![<Subject Name>](./<subject-name>/cover.png)
    <2-4 sentence compelling description emphasizing the story's theme>
```

### Step 7: Reusing Stories from Other Textbooks

When a story already exists in another intelligent textbook project (e.g., Theory of Knowledge stories reused in an Ecology textbook), **link to the story on the source textbook's published site** rather than duplicating it. Each story contains ~170 lines of markdown plus 13 generated images (1 cover + 12 panels) — duplicating all of that across textbooks adds unnecessary bulk without adding value.

**Strategy: copy only the cover image, link to the external story.**

```bash
# Copy ONLY the cover image from the source project into the current project
mkdir -p docs/stories/<subject-name>
cp /path/to/other-textbook/docs/stories/<subject-name>/cover.png \
   docs/stories/<subject-name>/cover.png
```

The cover image must be local so it renders during `mkdocs serve` development. **Do NOT use external URLs for images** — they don't render locally and create a dependency on the other site.

The story title link should point to the **published URL on the source textbook's site**:

```markdown
- **[<Story Title>](https://dmccreary.github.io/<source-book>/stories/<subject-name>/)**

    ![<Subject Name>](./<subject-name>/cover.png)
    <2-4 sentence compelling description>
```

**Add a reader notice** above the grid of cross-linked stories so students are not confused when they land on a different site. Place this once, before the grid — not on every card:

```markdown
*Clicking a card below will take you to the <Source Book Name> site, where the
full story and all 12 panel images are hosted. Use your browser's back button
to return here. We link rather than duplicate because each story includes 13
generated images — copying them across textbooks would add unnecessary bulk
without adding value.*
```

**Do NOT duplicate the full story markdown or the 12 panel images** into the current project. Only the cover image is copied locally.

## References Guidance

**Write real working URLs in the first draft. Do not use `(PLACEHOLDER)`.**

Follow the standard 5-reference pattern for every story:

| # | Source | Purpose |
|---|---|---|
| 1 | **Wikipedia: <Subject biography>** | Full biographical article |
| 2 | **Wikipedia: <Main contribution>** | The subject's signature discovery or work |
| 3 | **Wikipedia: <Related concept or work>** | A second topical link (e.g., an invention they're associated with, an equation named after them, a major paper) |
| 4 | **MacTutor** (mathematicians), **Nobel Prize** (laureates), **NASA** (mission scientists), or equivalent institutional bio | Stable academic history source |
| 5 | **Encyclopaedia Britannica** or **Stanford Encyclopedia of Philosophy** | Curated reference overview |

**Example — Ada Lovelace:**

```markdown
## References

1. [Wikipedia: Ada Lovelace](https://en.wikipedia.org/wiki/Ada_Lovelace) - Biography of the English mathematician often called the first programmer
2. [Wikipedia: Analytical Engine](https://en.wikipedia.org/wiki/Analytical_Engine) - Babbage's proposed mechanical general-purpose computer
3. [Wikipedia: Note G](https://en.wikipedia.org/wiki/Note_G) - Lovelace's note describing the first published algorithm
4. [MacTutor: Augusta Ada King, Countess of Lovelace](https://mathshistory.st-andrews.ac.uk/Biographies/Lovelace/) - University of St Andrews history of mathematics archive
5. [Encyclopaedia Britannica: Ada Lovelace](https://www.britannica.com/biography/Ada-Lovelace) - Overview of Lovelace's life and contributions to computing
```

### Fixing Legacy Stories with PLACEHOLDER URLs

Some stories generated before the 2026-04 skill update still contain `(PLACEHOLDER)` reference URLs. To clean these up in bulk, copy `scripts/story/fix-references.py` to your project's `src/` directory, edit the `REFS` dict at the top to list the stories and their curated URLs, and run it:

```bash
cp $BK_HOME/skills/book-media-generator/scripts/story/fix-references.py src/stories/
# Edit src/stories/fix-references.py to fill in the REFS dict
python3 src/stories/fix-references.py
```

The script rewrites everything from the `## References` heading to EOF in each listed story's `index.md`. Safe to re-run.

This script is intentionally NOT generic — curating good references is a judgment call, and each project wants slightly different sources. Maintaining a project-local customized copy is the right approach.

## Safety Filter Patterns

Gemini 2.5 Flash Image will refuse prompts that trip its safety classifier. The refusal shows up as `finish_reason=FinishReason.IMAGE_SAFETY` in the response, and the script logs it and continues to the next image without crashing.

**Known triggers:**

- Explicit Nazi imagery (swastikas, Nazi banners, SS uniforms)
- Graphic violence, wounds, or blood
- Nudity or sexual content
- Minors in explicitly distressing scenes
- Depictions of real people being killed or tortured

**Softening patterns** — rewrite the prompt to keep the emotional weight while removing the trigger:

| Original (triggers filter) | Softened (usually works) |
|---|---|
| "Nazi banners hanging on buildings" | "empty gray street with bare trees" |
| "swastika stamp on the letter" | "generic wax seal on the letter" |
| "forced out by Nazi laws" | "preparing to leave Germany" |
| "blood on the floor" | "a broken object on the floor" |
| "executed by firing squad" | "his empty desk and overturned chair" |

**Case study — Emmy Noether panel 10 (2026-04-05):** the original prompt explicitly mentioned "Nazi banners hang on a distant building" and "dismissal letter with a swastika stamp". Gemini refused with `IMAGE_SAFETY`. Softening to "empty gray street with bare trees" and "government dismissal letter with a generic wax seal" produced a clean generation on the next attempt. The historical meaning of forced exile survives; the explicit symbology is gone.

**Workflow when a prompt gets blocked:**

1. The script logs the failure and continues — no crash
2. Edit the offending prompt in the story's `index.md` to soften trigger words
3. Rerun: `python3 generate-images.py docs/stories/<name> --skip-existing`
4. Only the previously-failed panel regenerates; all other panels are skipped
5. Commit the softened prompt so future regenerations work on the first try

## Cost Analysis

**Gemini 2.5 Flash Image pricing (verified early 2026):**

- Input text tokens: $0.30 per 1M
- Output image tokens: $30.00 per 1M
- Fixed rate: **1,290 output tokens per image** = **$0.039 per image** on the paid tier

**Free tier (CAUTION — see warning below):**

- 500 requests per day (RPD)
- 10 requests per minute (RPM)
- ~250,000 tokens per minute (TPM)
- Advertised as **no credit card required**, no billing account

> **WARNING: The "free tier" may not support image generation (as of April 2026).** When tested on 2026-04-06, newly created Google AI Studio projects on the free tier returned `RESOURCE_EXHAUSTED` with `limit: 0` for `gemini-2.5-flash-preview-image`. This means the image generation model has **zero quota** on free-tier projects — it is not a rate limit or a temporary cap, but a hard zero. Only projects with **Tier 1 Postpay billing** (credit card required) successfully generated images. The free tier may work for text-only Gemini calls but does not appear to work for image generation. This contradicts the earlier documentation below and in the Gemini docs. If Google restores free-tier image generation, this warning can be removed.

**Cost projections (paid tier only — free tier currently does not work for images):**

Per-story cost scales linearly with panel count: **$0.039 × (N + 1)** for an N-panel story.

| Scope | Images | Paid tier cost |
|---|:---:|:---:|
| 6-panel story (1 cover + 6 panels) | 7 | ~$0.27 |
| 8-panel story (1 cover + 8 panels) | 9 | ~$0.35 |
| Default 12-panel story (1 cover + 12 panels) | 13 | $0.51 |
| 16-panel story (1 cover + 16 panels) | 17 | ~$0.66 |
| One 14-story textbook (all default 12-panel) | 182 | ~$7.10 |
| One 14-story textbook (mixed: avg 8 panels) | ~126 | ~$4.91 |
| One 16-story textbook (all default 12-panel) | 208 | ~$8.07 |

**Spending cap warning:** Google AI Studio's Tier 1 Postpay projects have a configurable monthly spending cap (default varies). The cap is enforced with up to 10 minutes of latency, so overages of a few percent are possible. Monitor your spend at <https://aistudio.google.com/spend>. The cap resets on the 1st of each month (PST). If you hit the cap mid-run, the script logs each failure and continues — rerun with `--skip-existing` after raising the cap.

**Recommendation:** Budget **$0.039 × (N + 1)** per story — about $0.50 for the default 12-panel length, or under $0.30 for tight 6-panel stories. A 14-story textbook of all default-length stories costs roughly $7; a mixed-length textbook averaging 8 panels per story costs roughly $5. Set your spending cap to at least the total you expect to spend in a month, plus a small buffer for overages.

### Alternative Models (for high-volume production)

If you exceed 500 images/day per project on a sustained basis, cheaper options exist, though quality varies:

| Model | Provider | Approx cost/image | Notes |
|---|---|---|---|
| FLUX.1 [schnell] | Fal / Replicate | **$0.003** | 13× cheaper, decent quality, no native 16:9 config |
| FLUX.1 [dev] | Fal / Replicate | $0.025 | Middle tier, excellent quality |
| SD 3.5 Medium | Stability AI | ~$0.035 | Comparable to Gemini |
| gpt-image-1 (low) | OpenAI | $0.011 | 3× cheaper, lower quality, limited aspect ratios |
| Local SDXL / FLUX | Self-hosted GPU | ~free | Requires 16+ GB VRAM and setup time |

**Honest assessment:** Gemini 2.5 Flash Image remains the best quality per dollar at the scale this skill targets. The alternatives only become worthwhile above 500 images/day per project, which no realistic textbook workflow hits.

## Known Issues

### Free tier does not support image generation (as of April 2026)

Newly created Google AI Studio projects on the free tier have **zero quota** for `gemini-2.5-flash-preview-image`. The API returns `RESOURCE_EXHAUSTED` with `limit: 0` — not a rate limit, but a hard zero. This was verified on 2026-04-06 across two separate free-tier projects. Only projects with **Tier 1 Postpay billing** (requires a credit card) can generate images. This appears to be a change from earlier behavior when the functions textbook was generated. If you see `limit: 0` errors on a new project, the fix is to enable billing at <https://aistudio.google.com/billing>, not to wait or retry.

### Spending cap can silently block generation

Tier 1 Postpay projects in Google AI Studio have a configurable monthly spending cap. When the cap is reached, all API calls return `RESOURCE_EXHAUSTED` with the message "Your project has exceeded its spending cap." The `generate-images.py` script logs this and continues (non-fatal), but no images are produced. The cap is enforced with up to 10 minutes of latency, so overages of a few percent are normal. Monitor and adjust at <https://aistudio.google.com/spend>. The cap resets on the 1st of each month (PST).

### Antigravity `generate_image` tool does not expose `aspect_ratio`

Google Antigravity IDE ships an internal `generate_image` tool whose schema only accepts `Prompt`, `ImageName`, `ImagePaths`, and tool metadata. It does **not** expose `aspect_ratio` or `size`, so every image it generates defaults to 1:1 square. **Do not use Antigravity's `generate_image` for graphic novel panels.** Use `scripts/story/generate-images.py` (this skill) instead — it calls Gemini directly via `google-genai` and passes `ImageConfig(aspect_ratio="16:9")`.

Prompt-level workarounds like "16:9 landscape cinematic composition" do **not** work — Gemini obeys `ImageConfig.aspect_ratio` but treats aspect-ratio hints in the prompt as stylistic suggestions at best.

Worth reporting: the Antigravity team should expose all 10 aspect ratios Gemini supports (`21:9`, `16:9`, `4:3`, `3:2`, `1:1`, `9:16`, `3:4`, `2:3`, `5:4`, `4:5`), plus ideally `response_modalities` and a transparent-PNG option.

### Character face consistency across panels

Gemini 2.5 Flash Image maintains **style continuity** (art style, color palette, mood) across multiple generations with similar prompts, but does **not** maintain exact facial features for the same character. Panel 3's Marie Curie will look stylistically similar to Panel 5's Marie Curie, but they won't be identical. For educational graphic novels where panels are read sequentially with narration below, this is usually acceptable. For professional-grade work requiring pixel-identical character faces, consider Flux Kontext, Imagen 4 with reference images, or a fine-tuned character LoRA. Out of scope for this skill.

### Only the first image part is used

If Gemini returns multiple image parts in a single response (rare but possible), the script saves only the first one. Multi-image responses are not supported.

## Art Style Reference by Era

| Era | Suggested Art Style |
|-----|---------------------|
| Ancient (before 500 AD) | Classical Mediterranean, mosaic-inspired |
| Renaissance (1400-1600) | Italian Renaissance, warm lighting |
| Enlightenment (1600-1800) | Baroque, Dutch Golden Age |
| Napoleonic Empire (1795-1815) | Empire-era French academic painting |
| Victorian (1800-1900) | Pre-Raphaelite, industrial |
| Gilded Age (1870-1900) | Art Nouveau, American industrial |
| Early Modern (1900-1950) | Art Deco, Modernist, Bauhaus (for Weimar-era Germany) |
| WWII era (1939-1945) | 1940s noir, muted olive/khaki |
| Mid-Century (1950-1980) | Atomic Age, clean lines, Bell Labs modernism |
| Space Age (1957-1975) | NASA technical illustration, cosmic blues |
| Contemporary (1980-present) | Photorealistic with period elements |

## Writing Guidelines

### Target Audience

- Secondary-school students (grades 9-12, ages 14-18) for most intelligent textbook projects
- Adjust reading level based on project — the skill supports younger or older audiences by changing the narrative voice, not the structure

### Narrative Style

- Use active voice and vivid descriptions
- Include dialogue when historically appropriate
- Balance drama with educational accuracy
- Emphasize the human story behind discoveries
- Show struggles, failures, and persistence
- Connect historical events to modern technology or contemporary relevance

### Theme Development

Choose a central theme that resonates with the target audience:

- Overcoming doubters and skeptics
- Persistence through failure
- Self-education and curiosity
- Fighting against discrimination
- Seeing what others couldn't see
- Staying humble despite success
- Making the invisible visible

### Historical Accuracy

- Research key dates, events, and relationships
- Use historically accurate details in image prompts (clothing, architecture, technology, typography)
- Note any creative liberties in the Narrative Prompt block
- Include verifiable quotes when possible

## Scripts

### generate-images.py (primary)

Generates all panel images via the Gemini API. See "Step 3.5: Generate Images" above.

### verify-images.py

Read-only audit tool — checks that all expected panels exist, are the right aspect ratio, and meet a minimum file size. Usage:

```bash
python3 $BK_HOME/skills/book-media-generator/scripts/story/verify-images.py \
    docs/stories/{story-dir-name}
```

### fix-references.py (legacy-fix tool)

For retroactively replacing `(PLACEHOLDER)` reference URLs in older stories. **Not for new stories** — new stories should have real URLs in the first draft. See the "References Guidance" section above.

### uncomment-images.sh (fallback workflow)

For workflows that defer image generation: the markdown ships with image references wrapped in HTML comments (`<!-- ![](./panel-01.png) -->`) to prevent broken image icons, and this script uncomments them once the PNGs are produced by any means.

**Usage:**

```bash
$BK_HOME/skills/book-media-generator/scripts/story/uncomment-images.sh \
    docs/stories/{story-dir-name}/index.md
```

**When to use:**
- You want to ship markdown immediately and generate images later in a batch job
- You're using an image generation tool other than `generate-images.py`
- You're migrating from an older workflow

**When NOT to use:**
- You're using `generate-images.py` — it writes PNGs directly to the filenames referenced in `index.md`, so nothing needs uncommenting

## Checklist

After completing a story, verify:

**Content:**
- [ ] Story directory created: `docs/stories/<name>/`
- [ ] `index.md` has full narrative and all N + 1 image prompts (cover + N panels, where N matches the `--panels` argument or defaults to 12)
- [ ] Panels are numbered consecutively from `panel-01` to `panel-NN` with no gaps
- [ ] Every "panel X of N" identifier line uses the *actual* N for this story (not a leftover 12)
- [ ] All image references use `.png` extension (never `.jpg` or `.md`)
- [ ] YAML frontmatter has title, description, and og/twitter image paths
- [ ] N numbered panels with consistent structure (image + prompt + narrative)
- [ ] Epilogue includes the Challenge / Response / Lesson table
- [ ] 2-3 subject quotes present (or in-character quotes for fictional stories)
- [ ] **References section has 5 real working URLs, first 3 on Wikipedia, no `(PLACEHOLDER)` strings**

**Image generation (if using generate-images.py):**
- [ ] `GEMINI_API_KEY` set in environment
- [ ] `pip install google-genai` completed
- [ ] `generate-images.py --first-only` run and cover verified as 16:9 natively (1344×768)
- [ ] Full `generate-images.py` run completed with no fatal errors
- [ ] All N + 1 PNG files present in the story directory
- [ ] `verify-images.py` exits with code 0
- [ ] Per-story log present at `logs/{story-name}-{YYYY-MM-DD}.md`
- [ ] JSONL usage log updated at `logs/image-generation-usage.jsonl`

**Integration:**
- [ ] Added to `mkdocs.yml` navigation in chronological order by birth year
- [ ] Grid card added to `docs/stories/index.md`
- [ ] Any safety-filter softenings are committed so future regenerations don't regress
- [ ] No real brand names, product names, or trademarks appear in any image prompt (brands are OK in narrative prose only)

## Appendix: Lessons Learned from the IB Functions Textbook (2026-04-05)

The 2026-04 skill update was driven by a real-world 16-story textbook project in `/Users/dan/Documents/ws/functions`. The definitive case study lives at `/Users/dan/Documents/ws/functions/logs/stories.md`. Key lessons captured here:

1. **The old workflow produced square images.** Stories were generated via the Antigravity IDE agent's `generate_image` tool, which does not expose `aspect_ratio` and defaults to 1:1. The workaround was to upscale the square to 1280×1280 and center-crop to 1280×720 — losing ~44% of the vertical content. The fix was to bypass Antigravity and call Gemini directly via `google-genai`, which is what `scripts/story/generate-images.py` now does.

2. **~~The free tier is genuinely free.~~** *(Corrected 2026-04-06.)* The original functions textbook (208 images) may have been generated during a period when free-tier image generation worked, but as of April 2026, newly created free-tier projects return `limit: 0` for `gemini-2.5-flash-preview-image`. Only Tier 1 Postpay projects (credit card required) can generate images. A 14-story textbook (Theory of Knowledge, 182 images) cost approximately **$11 on Tier 1 Postpay**. The free tier is **not** a viable path for image generation at this time. Budget ~$0.50/story.

3. **Safety filters are rare but will bite you.** Out of 208 images generated, exactly 1 was blocked outright (Emmy Noether panel 10, because of explicit Nazi imagery) and 1 was blocked transiently (Mirzakhani panel 10, cleared on retry without any change). The script now handles both cases gracefully, and the softening pattern for Noether-style content is documented above.

4. **Placeholder references are a trap.** All 16 stories initially shipped with `(PLACEHOLDER)` URLs from an earlier version of this skill. Retroactively fixing them required writing a `fix-references.py` script. New stories should have real URLs in the first draft — this skill now teaches that explicitly.

5. **Per-run audit logs are worth the lines of code.** The JSONL audit log caught a subtle fact that would have been invisible otherwise: every single image, regardless of prompt complexity, bills for exactly 1,290 output tokens. This confirmed the published pricing model and gave the user confidence that cost projections would be accurate at scale.

6. **Character face consistency is not yet solved at this price point.** See "Known Issues" above. Users should not expect pixel-identical characters across 12 panels — the current state of the art at $0.039/image produces stylistically consistent but individually distinct characters. This is an acceptable tradeoff for educational graphic novels at scale; it is not acceptable for professional commercial publishing.

7. **The free tier stopped working for image generation (2026-04-06).** During the Theory of Knowledge textbook project, 78 images were generated on Tier 1 Postpay before hitting a $10 spending cap. Attempting to create new free-tier projects to continue generation revealed that `gemini-2.5-flash-preview-image` has `limit: 0` on all free-tier projects. This contradicts lesson #2 above (from the functions project, which may have been generated during a window when free-tier image gen worked). The skill documentation has been updated to warn users that image generation requires paid billing. Budget ~$0.50/story, ~$7–8 for a full textbook.

If you're updating this skill in the future, read `logs/stories.md` in the functions project for the full session transcript and all the decisions behind the current design.

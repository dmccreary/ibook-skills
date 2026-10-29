---
name: cover-image-generator
description: Guides users through crafting a high-quality book cover image prompt from the textbook's own resources (course description, concept list, mascot, MicroSim screenshots). Image generation via API or browser automation is optional and runs only if the user explicitly asks for it.
---

# Cover Image Generator

This guide's primary job is to produce the best possible cover image **prompt** at
`docs/img/cover-image-prompt.md` — one written from the textbook's actual content so
a text-to-image model has everything it needs to produce a professional, on-topic
cover on the first or second try.

**Generating the image itself is optional and must be explicitly requested by the
user.** Most users want to take the finished prompt, paste it into a text-to-image
tool of their choice (ChatGPT, Midjourney, Gemini, Leonardo.ai, Ideogram, etc.),
review a few draft covers, and iterate on the *prompt* — not the API call — before
anything is treated as final. Do not run `generate-cover.sh` or call any image
generation API unless the user asks for it by name (e.g., "auto-generate the
cover," "run the cover script," "call the API").

## Why the Prompt Is the Deliverable

The cover image is often the first thing a prospective reader sees — on the repo
page, in a social media unfurl, in a search result. A strong prompt, refined
against the book's real content, is what separates a generic stock-art cover from
one that actually represents the textbook. Because text-to-image results are
non-deterministic, users typically want to see 2-4 draft renders from their
preferred tool before spending API credits or committing to a final asset. This
guide optimizes for that human-in-the-loop review step, not for full automation.

## What Gets Produced

1. **Always**: a detailed cover image prompt at `docs/img/cover-image-prompt.md`,
   built from the book's title, course description, concept list, and (if present)
   mascot and MicroSim screenshots.
2. **Only if explicitly requested**: the rendered `docs/img/cover.png`, produced by
   running `generate-cover.sh` (API, browser automation, or local-prompt path — see
   [Optional: Auto-Generating the Image](#optional-auto-generating-the-image)).

## Prerequisites

Before starting, ensure you have:

1. **Project Structure**: An MkDocs project with:
   - `mkdocs.yml` containing a `site_name:` field for the book title
   - `docs/course-description.md` with book content description
   - `docs/img/` directory (will be created if missing)
   - `docs/img/mascot/` directory with book mascot images (optional)
   - `docs/img/mascot/welcome.png` welcome mascot image (optional)
   - `docs/learning-graph/concept-list.md` or `learning-graph.json` (optional, improves montage quality)
   - `docs/sims/*/*.png` MicroSim screenshots (optional, improves montage quality)

2. **Only needed if the user requests auto-generation**: `$BK_HOME` exported (the
   user's profile sets it to the `ibook-skills` checkout) and the `generate-cover.sh`
   script at:
   ```
   $BK_HOME/src/image-generation/generate-cover.sh
   ```
   This script lives in the `ibook-skills` repo itself, not inside a skill directory
   (only `skills/*` is symlinked into `~/.claude/skills/`), so it must be reached via
   `$BK_HOME` rather than a path under `~/.claude/skills/`.

## Workflow: Generating the Prompt

### Step 1: Verify Required Project Files

```bash
# Check for mkdocs.yml
ls mkdocs.yml

# Check for course description
ls docs/course-description.md

# Check/create output directory
mkdir -p docs/img
```

If `docs/course-description.md` is missing, tell the user to create it first —
it's the primary source of subject-matter keywords for the prompt.

### Step 2: Gather Source Material

Collect everything that will make the prompt specific to *this* book, not a
generic textbook:

- **Title**: read `site_name` from `mkdocs.yml`.
- **Subject matter & tone**: read `docs/course-description.md` for topic, audience,
  and any stated visual/branding preferences.
- **Montage concepts**: read `docs/learning-graph/concept-list.md` (or derive from
  `docs/learning-graph/learning-graph.json`) for the concept vocabulary of the book.
- **MicroSim screenshots**: glob `docs/sims/*/*.png` — these are strong montage
  candidates because they're real artifacts from the book, not generic stock
  imagery.
- **Mascot**: check for `docs/img/mascot/welcome.png`.

```bash
ls docs/img/mascot/welcome.png 2>/dev/null
ls docs/sims/*/*.png 2>/dev/null
```

### Step 3: Select the Montage Concepts

Choose **6-10 concepts** for the background montage using these criteria, in
priority order:

1. **Recognizable or evocative** — a reader with some familiarity with the subject
   should recognize it, or it should be visually interesting enough to draw in a
   reader with none.
2. **Spread across the book**, not clustered in one chapter — pick concepts that
   signal the book's overall scope.
3. **Prefer real MicroSim screenshots** over invented illustrations when a good
   one exists — it's authentic to the book and free.
4. **Visually distinct from each other** — avoid picking 6 concepts that would all
   render as "person looking at a screen."
5. Text is acceptable inside a montage image only if it will render legibly at
   small size (a formula, a short label, an axis) — avoid concepts that require
   paragraphs of readable text.

List the chosen concepts with a one-line visual description each (not just the
concept label) so the text-to-image model has something concrete to draw, e.g.
`Neural Network — a glowing layered node-and-edge diagram, blue on dark
background` rather than just `Neural Network`.

### Step 4: Write the Prompt File

Generate `docs/img/cover-image-prompt.md` using the template below. Fill in every
bracketed field — an unfilled placeholder is worse than an omitted section.

```markdown
# Cover Image Prompt

Please generate a professional-quality cover image for this textbook.
This image will be used in social media previews and must follow the
formatting guidelines for an Open Graph image preview.

**Required specifications:**
- Format: PNG
- Wide-landscape format
- Size: 1200x630 pixels (1.91:1 aspect ratio)
- This is the Open Graph standard for social media previews

The image has four layers, back to front: background montage, color
treatment, mascot, and title text.

## Subject & Tone

{BOOK_TITLE} is a textbook about {ONE_SENTENCE_SUBJECT_SUMMARY, drawn from
course-description.md}. The intended audience is {AUDIENCE}. The visual tone
should be {e.g. "modern and technical," "warm and approachable," "scientific
and precise"} — pick a tone that matches the subject, not a default.

## Title

Place {BOOK_TITLE} in the center of the image, in a clean, highly legible
sans-serif font. Use a light/white font color with a subtle drop shadow or
dark scrim behind it so it stays readable against the busy montage
background. Keep the title short enough to render at a large size — do not
shrink it to fit if the title is long; instead simplify the background
directly behind the text.

## Background Montage

Arrange a montage of the following {N} concepts around the title, each
rendered in a consistent illustration style (see Style below) so the
composition reads as one image rather than a collage of unrelated styles:

{MONTAGE_IMAGE_LIST — one line per concept: name + concrete visual description}

## Mascot

{IF MASCOT PRESENT:}
Place the book's mascot in the lower-left corner, sized so it does not
overlap the title text. The mascot is described as: {MASCOT_DESCRIPTION, or
"see attached reference image"}.
{IF NO MASCOT:}
(No mascot for this book — omit this element entirely.)

## Style & Composition

- Illustration style: {e.g. "flat vector," "digital painting," "isometric
  technical illustration"} — choose one style and apply it to every montage
  element for visual consistency.
- Color palette: {2-3 dominant colors drawn from the subject matter, e.g.
  "deep blue and teal with amber accents"}.
- Lighting/mood: {e.g. "bright and optimistic," "moody and dramatic"}.
- Composition: title centered, montage elements arranged in a loose ring or
  grid around it, mascot (if any) in the lower-left, generous negative space
  immediately behind the title so it stays readable.

## Avoid

- Do not render dense paragraphs of illegible text anywhere in the image.
- Avoid generic stock-photo cliches (handshakes, isolated lightbulbs, people
  pointing at whiteboards) unless one is explicitly one of the chosen concepts.
- Avoid photorealistic human faces unless the book's subject calls for a
  specific recognizable figure.
- Do not let montage elements visually compete with or overlap the title.
```

### Step 5: Present the Prompt for Review

After writing the file, tell the user the prompt is ready at
`docs/img/cover-image-prompt.md` and recommend the manual review loop:

1. Open the prompt file and copy its contents.
2. Paste it into a text-to-image tool (ChatGPT, Midjourney, Gemini, Leonardo.ai,
   Ideogram, or any preferred tool).
3. Generate 2-4 draft covers and compare them.
4. If a draft misses the mark — wrong tone, unreadable title, mascot placement
   off — refine the *prompt* (montage list, style, color palette) rather than
   just re-rolling, and regenerate the draft.
5. Once a draft looks right, save it as `docs/img/cover.png` (resize to
   1200x630 if needed).

Do not proceed to image generation yourself at this point — wait for the user
to either do this manually or explicitly ask you to automate it.

## Optional: Auto-Generating the Image

Only do this if the user explicitly asks to auto-generate, run the script, or
call the API. If they haven't, stop after Step 5 above.

### Determine the User's API Resources

Ask the user these questions to determine the best workflow:

**Question 1: OpenAI API Key**
```
Do you have an OpenAI API key set up?
(Check with: echo $OPENAI_API_KEY)

1. Yes, I have an API key with active billing
2. Yes, I have an API key but billing is not active
3. No, I don't have an API key
```

**Question 2: ChatGPT Subscription (if no active API billing)**
```
Do you have a ChatGPT Pro/Plus subscription ($20/month)?

1. Yes
2. No
```

**Question 3: Operating System (if has ChatGPT Pro)**
```
Are you running on macOS?

1. Yes (can use browser automation)
2. No (will use manual copy/paste)
```

### Select and Run the Appropriate Command

Based on the answers, use one of these workflows:

#### Path A: Full Auto Mode (API key + active billing)

This is the fastest, fully automated option.

```bash
# Navigate to the user's project root
cd /path/to/project

# Run the script with no flags
"$BK_HOME/src/image-generation/generate-cover.sh"
```

The script will:
1. Extract book title from mkdocs.yml
2. Generate an optimized image prompt
3. Call OpenAI Images API
4. Save the result to `docs/img/cover.png`

**Expected output:**
```
=== Cover Image Generator ===
Project directory: /path/to/project
Book Title: Your Book Title
...
Generating cover image...
Wrote: docs/img/cover.png
```

#### Path B: Browser Automation (ChatGPT Pro + macOS)

For users with ChatGPT Pro on macOS.

```bash
# Navigate to the user's project root
cd /path/to/project

# Run with --open-browser flag
"$BK_HOME/src/image-generation/generate-cover.sh" --open-browser
```

The script will:
1. Extract book title from mkdocs.yml
2. Generate an optimized image prompt locally (no API call)
3. Open ChatGPT in the default browser
4. Automatically paste the prompt

**Note:** First run may require granting Accessibility permissions:
- System Settings > Privacy & Security > Accessibility
- Allow Terminal (or your terminal app) to control the computer

**After the script runs:**
1. Wait for ChatGPT to generate the image
2. Download the generated image
3. Save it to `docs/img/cover.png`
4. Resize to 1200x630 pixels if needed

#### Path C: Local Prompt (ChatGPT Pro, any OS)

For users with ChatGPT Pro on non-macOS systems.

```bash
# Navigate to the user's project root
cd /path/to/project

# Run with --local-prompt flag
"$BK_HOME/src/image-generation/generate-cover.sh" --local-prompt
```

The script will:
1. Extract book title from mkdocs.yml
2. Generate an optimized image prompt locally (no API call)
3. Display the prompt for manual copying

**After the script runs:**
1. Copy the displayed IMAGE PROMPT
2. Go to https://chatgpt.com/
3. Paste the prompt
4. Download the generated image
5. Save it to `docs/img/cover.png`
6. Resize to 1200x630 pixels if needed

#### Path D: No Resources Available

If the user has neither API billing nor ChatGPT Pro:

**Option 1: Set up OpenAI API billing**
1. Go to https://platform.openai.com/account/billing
2. Add a payment method
3. Add credits ($5-10 is sufficient for many images)
4. Return and use Path A

**Option 2: Subscribe to ChatGPT Pro**
1. Go to https://openai.com/chatgpt/pricing
2. Subscribe to Plus ($20/month)
3. Return and use Path B or C

**Option 3: Use the prompt manually with a free tier**
1. Use the prompt already written to `docs/img/cover-image-prompt.md`
2. Use it with any free AI image generator:
   - Bing Image Creator (free)
   - Leonardo.ai (free tier)
   - Ideogram (free tier)

### Verify the Cover Image

After generation, verify the image:

```bash
# Check file exists
ls -la docs/img/cover.png

# Check dimensions (if ImageMagick installed)
identify docs/img/cover.png
```

## Update the Home Page (Optional)

If the user wants to display the cover on their home page, add to `docs/index.md`:

```markdown
---
title: Your Book Title
description: Brief description
image: /img/cover.png
og:image: /img/cover.png
---

![Your Book Title: Subtitle. Cover image of a one-sentence description of the montage](./img/cover.png){ width="100%" }
```

Because the cover renders the book title, apply the **Landing Page Title Rule**
in [home-page-template.md](./home-page-template.md): hide the page's duplicate
h1 with the `<style>` block shown there, and keep the title at the start of
the image's alt text so screen readers still announce it.

## Troubleshooting

The following issues only apply if the user has opted into auto-generation
via `generate-cover.sh`.

### "billing_not_active" Error

Your OpenAI API key is valid but the account lacks billing.

**Solutions:**
- Add payment method at https://platform.openai.com/account/billing
- Or use `--local-prompt` with ChatGPT Pro

### "Could not extract site_name from mkdocs.yml"

The `mkdocs.yml` file is missing the `site_name:` field.

**Fix:**
```yaml
# Add to mkdocs.yml
site_name: Your Book Title
```

### "Course description not found"

The file `docs/course-description.md` doesn't exist.

**Fix:**
Create the file with a description of your book's content, topics, and themes. This provides keywords for the image generation.

### Auto-paste not working on macOS

First run requires Accessibility permissions.

**Fix:**
1. Open System Settings
2. Go to Privacy & Security > Accessibility
3. Enable your terminal app (Terminal, iTerm2, etc.)
4. Run the script again

### Image is wrong dimensions

Text-to-image tools may not generate exact dimensions.

**Fix:**
1. Open the image in an editor (Preview on macOS, GIMP, etc.)
2. Resize to 1200x630 pixels
3. Save as PNG

## Command Reference

These commands are only relevant if the user explicitly asks for
auto-generation.

| Command | Description | Requirements |
|---------|-------------|--------------|
| `generate-cover.sh` | Full auto via API | API key + billing |
| `generate-cover.sh --local-prompt` | Generate prompt only | None |
| `generate-cover.sh --open-browser` | Open ChatGPT + paste | macOS + ChatGPT Pro |
| `generate-cover.sh --prompt-only` | API prompt only | API key + billing |

## Related Resources

- [Cover Image Workflow Diagram](https://dmccreary.github.io/ibook-skills/sims/cover-image-workflow/)
- [Home Page Template Guide](./home-page-template.md)
- [Image Generation README](https://github.com/dmccreary/ibook-skills/tree/main/src/image-generation)

---
name: learning-mascot
description: Guides users through designing a pedagogical agent (learning mascot) for their intelligent textbook, generating AI image prompts, and implementing the mascot using custom CSS admonitions with body-floated images.  Also describes how the mascot section of CONTENT-GENERATION-GUIDE.md is added.
---

# Learning Mascot (Pedagogical Agent)

This skill helps users design and implement a pedagogical agent — a visual mascot character that guides students through their intelligent textbook. Research on the "persona effect" shows that characters improve learner engagement and perception of learning.

## What This Skill Creates

1. **Character Design** - A fully defined mascot persona (name, species, appearance, voice, catchphrase)
2. **AI Image Prompts** - Ready-to-use prompts for generating mascot images in consistent poses
3. **Implementation** - Custom CSS admonitions with mascot images floated left in the admonition body
4. **CLAUDE.md Section** - Character guidelines for consistent AI-generated content
5. **Mascot Test Page** - Visual transparency/trim validation plus all seven production admonition styles

## Benefits of a Learning Mascot

- **Engagement** - Gives the textbook personality that students connect with emotionally
- **Wayfinding** - Signals special content types (tips, challenges, reflections) visually
- **Encouragement** - Character dialogue normalizes struggle and celebrates progress
- **Branding** - Distinctive mascots make courses memorable and build community identity

## Prerequisites

- Existing MkDocs Material project (use `init-textbook.md` — feature 0 — first if needed)
- Access to an AI image generator (ChatGPT/DALL-E, Midjourney, Stable Diffusion, or similar)
- Course description or learning graph to inform mascot theme

## Performance Guidelines

This skill involves interactive Q&A (Steps 1-2) followed by file generation (Steps 3-7).

**During Q&A (Steps 1-2):** Ask all design questions in as few turns as possible. Present all questions together with default suggestions so the user can answer multiple at once.

**During file generation (Steps 3-7):** Do NOT use TaskCreate/TaskUpdate — the overhead of loading deferred tools and making 12+ task calls turns a <1 minute job into 10+ minutes. Instead:

1. Run `mkdir -p docs/img/mascot docs/css` first
2. Then execute ALL file operations in a single parallel batch:
   - Write `docs/css/mascot.css`
   - Write `docs/img/mascot/character-sheet.md` (canonical character description — see Step 2b)
   - Write `docs/img/mascot/image-prompts.md`
   - Write `docs/learning-graph/mascot-test.md`
   - Write or update `CLAUDE.md` (must include a Mascot File Index — see Step 7)
   - Edit `mkdocs.yml` (theme palette, extra_css, nav entry)
3. Target: all file generation completes in one tool-call round

**During trim step (Step 4b):** The trim script path is `$PROJECT_HOME/../ibook-skills/src/image-utils/trim-padding-from-image.py`. Do NOT search for it — just run it directly on all 7 images. Use the known filenames: neutral.png, welcome.png, thinking.png, tip.png, warning.png, encouraging.png, celebration.png.

## Workflow

### Step 1: Gather Course Context

Before designing the mascot, collect information about the book:

1. **Book Title** - What is the textbook about?
2. **Subject Area** - The academic domain (math, science, history, programming, etc.)
3. **Target Audience** - Age range and level (K-5, middle school, high school, college, professional)
4. **Tone** - Serious/academic, friendly/approachable, playful/fun, inspiring/motivational
5. **Existing Color Palette** - Primary and accent colors from the book's theme

### Step 2: Design the Mascot Character

Ask the user these questions to define their mascot. Provide suggestions for each.

**Question 1: What type of character?**

Suggest options based on the subject area:

| Subject Area | Suggested Characters | Reasoning |
|-------------|---------------------|-----------|
| Mathematics | Owl, Fox, Raccoon | Wisdom, cleverness, curiosity |
| Science | Squirrel, Cat, Robot | Experimentation, curiosity, precision |
| History | Tortoise, Elephant, Raven | Longevity, memory, storytelling |
| Programming | Robot, Cat, Octopus | Logic, independence, multitasking |
| Language Arts | Parrot, Bookworm, Fox | Communication, reading, storytelling |
| Music/Art | Peacock, Songbird, Chameleon | Expression, creativity, adaptation |
| Environmental Science | Tree Frog, Bee, Dolphin | Ecology, community, intelligence |
| Engineering | Beaver, Ant, Spider | Building, teamwork, design |
| Business | Lion, Eagle, Dolphin | Leadership, vision, collaboration |
| Health/PE | Cheetah, Bear, Hawk | Speed, strength, focus |

Also offer: abstract characters (geometric shapes with faces), human characters (student, professor, explorer), or mythological creatures (phoenix, dragon, unicorn).

**Question 2: What personality traits?**

Suggest 3-4 traits that match the tone:

- **Friendly/Approachable**: Warm, patient, encouraging, slightly goofy
- **Academic/Scholarly**: Wise, precise, thoughtful, curious
- **Adventurous/Exciting**: Bold, enthusiastic, energetic, brave
- **Calm/Supportive**: Gentle, reassuring, steady, kind

**Question 3: What is the character's name?**

Suggest names that:

- Are easy to remember and pronounce
- Relate to the subject (e.g., "Ada" for programming, "Archie" for architecture)
- Have alliteration with the species (e.g., "Sylvia the Squirrel", "Otto the Owl")
- Are culturally neutral and inclusive
- **Are gender-neutral** — always prefer gender-neutral names so all students feel represented by the mascot. Avoid names that strongly imply a gender (e.g., prefer "Sage" over "Sally", "River" over "Robert"). Never use gendered pronouns for the mascot — always refer to it by name or use "they/them".

Provide 3-5 name suggestions based on the species and subject, prioritizing gender-neutral options.

**Question 4: What is the character's catchphrase?**

The catchphrase adds personality. Suggest options:

- **Math**: "Let's figure this out!", "Numbers never lie!", "Time to calculate!"
- **Science**: "Let's experiment!", "Hypothesis time!", "Let's crack this nut!"
- **Programming**: "Let's debug this!", "Time to code!", "Compile and conquer!"
- **History**: "Let's travel back in time!", "History has a lesson!", "What happened next?"
- **General**: "Great question!", "Let's explore!", "You've got this!", "Think about it!"

**Question 5: What does the character look like?**

Collect specific visual details:

- **Species/Type**: (from Question 1)
- **Colors**: Primary body color, accent colors (hat, scarf, glasses, etc.)
- **Clothing/Accessories**: Glasses, lab coat, backpack, tool belt, scarf, hat
- **Expression**: Friendly smile, curious look, thoughtful pose
- **Size Proportion**: Small (icon-sized) to medium (quarter-page)
- **Art Style**: Cartoon/flat, watercolor, pixel art, 3D rendered, hand-drawn sketch

**Question 6: Where should the mascot appear?**

Suggest placement contexts:

| Context | Purpose | Frequency | Filename |
|---------|---------|-----------|----------|
| Neutral Pose | General pose | As needed | neutral.png |
| Chapter Welcome | Welcome and preview | Start of every chapter | welcome.png |
| Key insight | Signal important insights | As needed | thinking.png |
| Tips and hints | Offer helpful guidance | As needed | tip.png |
| Warnings and pitfalls | Alert to common mistakes | As needed | warning.png |
| Difficult concepts | Provide encouragement | As needed | encouraging.png |
| Chapter summaries | Review and celebrate | End of every chapter | celebration.png |

**IMPORTANT: Restraint Guidelines**

The mascot should NOT appear:

- More than 10 times per chapter
- Back to back (with no text between the admonitions)
- In ways that interrupt reading flow
- With excessive dialogue that adds no value

### Step 2b: Save the Character Sheet

Once the design Q&A is complete, save the canonical character description as a markdown file at `docs/img/mascot/character-sheet.md`. This file is the **single source of truth** for the character's visual identity, voice, and personality — every pose prompt, every chapter admonition, and every future regeneration must re-anchor to it. Without a written character sheet, drift across poses and across content authors is guaranteed.

Use the term **"character sheet"** rather than "character bible" — the latter carries religious connotations some readers find off-putting, and "character sheet" is the more widely-used term in animation, illustration, and AI-image-generation circles.

Use this template, filling in every placeholder from the Step 2 Q&A answers:

```markdown
# Character Sheet: {{CHARACTER_NAME}} the {{SPECIES}}

The canonical identity document for {{CHARACTER_NAME}}, the pedagogical
mascot for the **{{BOOK_TITLE}}** textbook. Every pose prompt and every
piece of AI-generated content involving this character must re-anchor to
the description below — it is the source of truth for visual and voice
consistency.

## Identity

- **Name:** {{CHARACTER_NAME}}
- **Species:** {{SPECIES}}
- **Subject:** {{SUBJECT}}
- **Catchphrase:** "{{CATCHPHRASE}}"

## Visual Description

- **Body color:** {{PRIMARY_COLOR}} — hex `{{PRIMARY_HEX}}`
- **Accent color:** {{SECONDARY_COLOR}} — hex `{{SECONDARY_HEX}}`
- **Clothing / accessories:** {{ACCESSORIES}}
- **Expression:** {{EXPRESSION}}
- **Size proportion:** {{SIZE_DESCRIPTION}}
- **Art style:** {{ART_STYLE}}

## Personality

- {{TRAIT_1}}
- {{TRAIT_2}}
- {{TRAIT_3}}
- {{TRAIT_4}}

## Voice

- {{VOICE_TRAIT_1}}
- {{VOICE_TRAIT_2}}
- {{VOICE_TRAIT_3}}
- Signature phrases: "{{PHRASE_1}}", "{{PHRASE_2}}", "{{PHRASE_3}}"

## Pose Set

| Pose | Filename | Use |
|------|----------|-----|
| Neutral | `neutral.png` | General-purpose / sidebars |
| Welcome | `welcome.png` | Chapter openings |
| Thinking | `thinking.png` | Key concepts |
| Tip | `tip.png` | Hints and helpful guidance |
| Warning | `warning.png` | Common mistakes / pitfalls |
| Encouraging | `encouraging.png` | Difficult content / struggle |
| Celebration | `celebration.png` | End of chapter / achievements |

See [`image-prompts.md`](image-prompts.md) for the full text of each pose
prompt. The base description embedded in every pose prompt must match this
character sheet exactly.

## Why This Mascot

{{REASONING_FOR_CHOICE}} — a 2-3 sentence rationale for why this species,
name, and styling were chosen for the subject. Used by future maintainers
deciding whether a proposed redesign is consistent with the project's
original intent.
```

The character sheet lives alongside the pose images in `docs/img/mascot/` so any agent or human working with the mascot finds the design rules and the artwork in the same directory.

### Step 3: Generate AI Image Prompts

Create a set of prompts for generating consistent mascot images. **Each prompt must be fully self-contained** — include the complete base character description in every prompt so they can be used independently without copying a separate base block.

#### Base Character Prompt

Always put this text at the start of the docs/img/mascot/image-prompt.md file

```
I am about to ask you to generate seven different poses for a book mascot.
Please use a consistent drawing style for all seven images.
```

This is the core description to include in every pose prompt:

```
Please generate a new pose for [NAME] the [SPECIES].
A [ART_STYLE] illustration of [NAME] the [SPECIES], a friendly pedagogical mascot
for a [SUBJECT] textbook. [NAME] is [COLOR_DESCRIPTION], wearing [ACCESSORIES].
[NAME] has [EXPRESSION]. The character is [SIZE_DESCRIPTION].
Style: [ART_STYLE], clean lines, transparent background with alpha channel,
suitable for embedding in educational content. No text in image.

Please generate a new RGBA PNG image now with a fully transparent alpha-channel background.

```

#### Pose Variants

Generate prompts for each of these poses. **Always include the full base description in each prompt** — never use `[BASE]` shorthand:

**1. Neutral/Default Pose** (general sidebars, introductions, inline use)

[FULL BASE DESCRIPTION] [NAME] stands upright in a relaxed, neutral pose facing the
viewer directly, with a calm and friendly closed-mouth smile. Arms/paws/wings
rest naturally at their sides with no specific gesture. The pose is balanced
and unassuming — suitable as a general-purpose or default illustration.
Filename: neutral.png

Please generate a new RGBA PNG image now with a fully transparent alpha-channel background.
The background MUST be fully transparent with an alpha channel.  DO NOT use a white, black or a checkered background.


**2. Welcome/Introduction Pose** (chapter openings)


Please generate a new welcome pose for [NAME].
[FULL BASE DESCRIPTION] [NAME] is waving cheerfully with one hand/paw/wing,
facing the viewer with a warm, welcoming expression.
The pose suggests "welcome" and "let's get started."
Filename: welcome.png

Please generate a new RGBA PNG image now with a fully transparent alpha-channel background.
The background MUST be fully transparent with an alpha channel.
DO NOT use a white, black or a checkered background.


**3. Thinking/Teaching Pose** (key concepts)


Please generate a new thinking pose for [NAME].
[FULL BASE DESCRIPTION] [NAME] has one hand/paw on chin in a thoughtful pose,
with a small lightbulb or thought bubble above their head.
The pose suggests deep thinking and discovery.
Filename: thinking.png

Please generate a new RGBA PNG image now with a fully transparent alpha-channel background.
The background MUST be fully transparent with an alpha channel.  DO NOT use a white, black or a checkered background.


**4. Pointing/Tip Pose** (tips and hints)


Please generate a new tip pose for [NAME].
[FULL BASE DESCRIPTION] [NAME] is pointing upward with one finger/paw
as if sharing an important tip. Expression is helpful and knowing.
A small star or sparkle near the pointing gesture.
Filename: tip.png

Please generate a new RGBA PNG image now with a fully transparent alpha-channel background.
The background MUST be fully transparent with an alpha channel.  DO NOT use a white, black or a checkered background.


**5. Warning/Caution Pose** (warnings and pitfalls)


Please generate a new friendly warning pose for [NAME].
[FULL BASE DESCRIPTION] [NAME] holds up both hands/paws in a gentle "stop"
or "be careful" gesture. Expression is concerned but caring.
A small exclamation mark or caution symbol nearby.
Filename: warning.png

Please generate a new RGBA PNG image now with a fully transparent alpha-channel background.
The background MUST be fully transparent with an alpha channel.  DO NOT use a white, black or a checkered background.


**6. Encouraging Pose** (difficult sections)


Please generate a new encouraging pose for [NAME].
[FULL BASE DESCRIPTION] [NAME] gives a thumbs up (or equivalent gesture)
with a reassuring, supportive smile. The pose radiates confidence
and "you can do it" energy.
Filename: encouraging.png

Please generate a new RGBA PNG image now with a fully transparent alpha-channel background.
The background MUST be fully transparent with an alpha channel.  DO NOT use a white, black or a checkered background.


**7. Celebration Pose** (achievements, chapter completion)


Please generate a new celebration pose for [NAME].
[FULL BASE DESCRIPTION] [NAME] is jumping or raising both arms/paws/wings
in celebration. Expression is joyful and proud.
Small confetti or stars around the character.
Filename: celebration.png

Please generate a new RGBA PNG image now with a fully transparent alpha-channel background.
The background MUST be fully transparent with an alpha channel.  DO NOT use a white, black or a checkered background.


#### Example: Complete Prompt Set for "Otto the Owl"


```
Base: A flat cartoon illustration of Otto the Owl, a friendly pedagogical
mascot for a mathematics textbook. Otto is a round barn owl with warm
brown and cream feathers, wearing small round glasses and a blue
graduation cap. Otto has large, kind eyes with a gentle smile.
The character is small and compact, suitable for icon-sized display.
Style: modern flat vector, clean lines, transparent background,
suitable for embedding in educational content. No text in image.

Neutral: [Base] Otto stands upright in a relaxed, neutral pose facing
the viewer with a calm, friendly closed-mouth smile. Both wings rest
naturally at his sides. No specific gesture.

Welcome: [Base] Otto is waving one wing cheerfully, facing the viewer
with a warm, welcoming expression.

Thinking: [Base] Otto has one wing on his chin, looking upward
thoughtfully. A small lightbulb glows above his head.

Tip: [Base] Otto points upward with one wing feather, looking helpful
and knowing. A small star sparkles near the gesture.

Warning: [Base] Otto holds up both wings in a gentle "be careful"
gesture, looking concerned but caring.

Encouraging: [Base] Otto gives a wing thumbs-up with a warm,
reassuring smile.

Celebration: [Base] Otto spreads both wings wide with joy, eyes
squinted in a big smile. Small confetti falls around him.
```

Present the generated prompts to the user and ask them to generate images using their preferred AI image tool. Recommend generating at 512x512 or 1024x1024 pixels, then resizing down for use
and also running the python script that will remove extra padding around the edges with
the scripts/trim-padding-from-image.py program.  Place the trim padding command in
the screen for the user to run.

### Step 4: Save Mascot Images

After the user generates their images, instruct them to save them:

```
docs/img/mascot/
├── neutral.png       # General purpose / default
├── welcome.png       # Chapter openings
├── thinking.png      # Key concepts
├── tip.png           # Tips and hints
├── warning.png       # Warnings
├── celebration.png   # Achievements
└── encouraging.png   # Difficult sections
```

```bash
mkdir -p docs/img/mascot
```

Required specifications:

- Format: RGBA PNG with fully transparent alpha-channel background
- Dimensions: 200x200 to 400x400 pixels for display
- File size: Under 100KB per image for web performance

#### Step 4b: Trim Excess Padding from Mascot Images

AI image generators frequently add excessive transparent padding around mascot images, which makes the mascot appear too small when displayed at the target CSS size (e.g., 90px). After saving the images, recommend running the padding trimmer on each file:

```bash
python $BK_HOME/src/image-utils/trim-padding-from-image.py docs/img/mascot/neutral.png
python $BK_HOME/src/image-utils/trim-padding-from-image.py docs/img/mascot/welcome.png
python $BK_HOME/src/image-utils/trim-padding-from-image.py docs/img/mascot/thinking.png
python $BK_HOME/src/image-utils/trim-padding-from-image.py docs/img/mascot/tip.png
python $BK_HOME/src/image-utils/trim-padding-from-image.py docs/img/mascot/warning.png
python $BK_HOME/src/image-utils/trim-padding-from-image.py docs/img/mascot/celebration.png
python $BK_HOME/src/image-utils/trim-padding-from-image.py docs/img/mascot/encouraging.png
```

This script trims transparent padding to the bounding box of the visible content. It is critical to run this step because untrimmed images display much smaller than intended inside the admonition boxes.

### Step 5: Create the Custom CSS

Create or append to `docs/css/mascot.css`:

```css
/* ============================================
   Learning Mascot: {{CHARACTER_NAME}} the {{SPECIES}}
   Pedagogical agent for {{SUBJECT}}
   ============================================ */

:root {
  --mascot-primary:   {{PRIMARY_COLOR}};   /* e.g., #2e7d32 forest green  */
  --mascot-secondary: {{SECONDARY_COLOR}}; /* e.g., #795548 warm brown    */
  --mascot-bg:        {{BG_COLOR}};        /* e.g., #e8f5e9 light green   */
  --mascot-border:    {{BORDER_COLOR}};    /* e.g., #43a047 medium green  */
  --mascot-size: 90px;
}

/* ---- Shared base for all mascot admonitions ---- */
/* Override MkDocs Material's default smaller admonition font size
   so mascot admonition text matches the body text exactly. */
.md-typeset .admonition.mascot-welcome,
.md-typeset .admonition.mascot-thinking,
.md-typeset .admonition.mascot-tip,
.md-typeset .admonition.mascot-warning,
.md-typeset .admonition.mascot-celebration,
.md-typeset .admonition.mascot-encourage,
.md-typeset .admonition.mascot-neutral,
.md-typeset details.mascot-welcome,
.md-typeset details.mascot-thinking,
.md-typeset details.mascot-tip,
.md-typeset details.mascot-warning,
.md-typeset details.mascot-celebration,
.md-typeset details.mascot-encourage,
.md-typeset details.mascot-neutral {
  font-size: inherit;
}

/* ---- Welcome (chapter openings) — primary color ---- */
.md-typeset .admonition.mascot-welcome,
.md-typeset details.mascot-welcome {
  border-color: var(--mascot-primary);
  background-color: var(--mascot-bg);
}
.md-typeset .mascot-welcome > .admonition-title,
.md-typeset .mascot-welcome > summary {
  background-color: var(--mascot-primary);
  color: white;
}

/* ---- Thinking (key concepts) — secondary color ---- */
.md-typeset .admonition.mascot-thinking,
.md-typeset details.mascot-thinking {
  border-color: var(--mascot-secondary);
  background-color: #efebe9;
}
.md-typeset .mascot-thinking > .admonition-title,
.md-typeset .mascot-thinking > summary {
  background-color: var(--mascot-secondary);
  color: white;
}

/* ---- Tip (hints) — teal ---- */
.md-typeset .admonition.mascot-tip,
.md-typeset details.mascot-tip {
  border-color: #00897b;
  background-color: #e0f2f1;
}
.md-typeset .mascot-tip > .admonition-title,
.md-typeset .mascot-tip > summary {
  background-color: #00897b;
  color: white;
}

/* ---- Warning (common mistakes) — red ---- */
.md-typeset .admonition.mascot-warning,
.md-typeset details.mascot-warning {
  border-color: #c62828;
  background-color: #ffebee;
}
.md-typeset .mascot-warning > .admonition-title,
.md-typeset .mascot-warning > summary {
  background-color: #c62828;
  color: white;
}

/* ---- Celebration (achievements) — deep purple so pale confetti sparkles pop ---- */
/* NOTE: celebration poses typically contain pale gold/white confetti that
   vanishes against light backgrounds. Keep the body dark and flip text
   color to light. See "Contrast-check each pose image" below. */
.md-typeset .admonition.mascot-celebration,
.md-typeset details.mascot-celebration {
  border-color: #4a148c;
  background-color: #311b4f;
  color: #f3e5f5;
}
.md-typeset .mascot-celebration > .admonition-title,
.md-typeset .mascot-celebration > summary {
  background-color: #4a148c;
  color: white;
}

/* ---- Encourage (difficult content) — blue ---- */
.md-typeset .admonition.mascot-encourage,
.md-typeset details.mascot-encourage {
  border-color: #0277bd;
  background-color: #e1f5fe;
}
.md-typeset .mascot-encourage > .admonition-title,
.md-typeset .mascot-encourage > summary {
  background-color: #0277bd;
  color: white;
}

/* ---- Neutral (general purpose) — slate gray ---- */
.md-typeset .admonition.mascot-neutral,
.md-typeset details.mascot-neutral {
  border-color: #546e7a;
  background-color: #eceff1;
}
.md-typeset .mascot-neutral > .admonition-title,
.md-typeset .mascot-neutral > summary {
  background-color: #546e7a;
  color: white;
}

/* ---- Title: left-align text, remove default MkDocs icon completely ---- */
.md-typeset [class*="mascot-"] > .admonition-title,
.md-typeset [class*="mascot-"] > summary {
  text-align: left;
  padding-left: 0.8rem;
}
.md-typeset [class*="mascot-"] > .admonition-title::before,
.md-typeset [class*="mascot-"] > summary::before {
  display: none;
}

/* ---- Mascot image floated LEFT of admonition body text ---- */
.mascot-admonition-img {
  float: left;
  width: var(--mascot-size);
  height: var(--mascot-size);
  /* margin: top right bottom left */
  margin: 0 .5em 0 0;
  object-fit: contain;
  pointer-events: none;  /* belt-and-suspenders; real exclusion is via glightbox skip_classes */
}
```

**IMPORTANT design rules:**

- **Never** put mascot icons in the admonition title bar (no `::before` pseudo-elements with mascot images)
- **Always** place mascot images in the admonition body using Markdown image syntax: `![alt](path){ class="mascot-admonition-img" }` — never HTML `<img>` tags
- The title bar is clean text only — the default MkDocs icon is hidden via `display: none`
- **Contrast-check each pose image against its admonition background before finalizing colors.** Open the PNG and look for fine pale details — confetti sparkles, glow, LED highlights, thin white outlines. If the pose has pale elements (the celebration pose almost always does), the admonition background must be dark enough that those details remain visible; flip the body text color to a light shade to compensate. If the pose is mostly dark or saturated, a light pastel background is fine. The celebration CSS block above is the canonical example of the dark-background treatment.

#### Step 5b: Register the CSS in mkdocs.yml

Add the stylesheet to `mkdocs.yml`:

```yaml
extra_css:
  - css/mascot.css
```

Also ensure the custom admonition types are registered:

```yaml
markdown_extensions:
  - admonition
  - md_in_html
  - pymdownx.details
  - pymdownx.superfences
  - attr_list
```

### Step 6: Usage in Chapter Markdown

Authors use standard admonition syntax with the custom types. The mascot image is placed using Markdown image syntax with the `attr_list` extension (already in the required extensions list):

**IMPORTANT: Image paths** — Markdown and raw HTML use *different* base
directories, and getting this wrong produces a page that looks correct in the
browser but fails `mkdocs build --strict`.

- **Markdown images** — `![alt](path){ class="..." }` — are resolved by MkDocs
  relative to the **source `.md` file's directory**, and MkDocs then rewrites
  them for the rendered URL. Count directories from the markdown file to
  `docs/img/mascot/`. From `docs/chapters/01-intro/index.md` that is
  `../../img/mascot/`; from `docs/learning-graph/mascot-test.md` it is
  `../img/mascot/`.
- **Raw HTML `<img src>`** is passed through verbatim — MkDocs never rewrites
  it — so it must be relative to the **rendered page URL**. Both of the pages
  above render two levels deep, so both need `../../img/mascot/`.

The two rules coincide for a chapter `index.md` (both give `../../`), which is
why the discrepancy only shows up on a non-index page such as
`learning-graph/mascot-test.md`. Writing `../../` in the Markdown there still
renders correctly — MkDocs leaves the unresolvable path alone — but it emits a
"target is not found among documentation files" warning that breaks a strict
build.

```markdown
!!! mascot-neutral "A Note from {{CHARACTER_NAME}}"
    ![{{CHARACTER_NAME}} neutral pose](../../img/mascot/neutral.png){ class="mascot-admonition-img" }
    Use this for general sidebars, introductions, or any content
    that doesn't call for a specific emotional tone.

!!! mascot-welcome "Welcome!"
    ![{{CHARACTER_NAME}} waving welcome](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    In this chapter, we'll discover how to solve equations
    of the form ax² + bx + c = 0. Get ready for some
    powerful mathematical tools!

!!! mascot-thinking "Key Insight"
    ![{{CHARACTER_NAME}} thinking](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    Notice that every quadratic equation has at most two
    solutions. This connects directly to the degree of the
    polynomial!

!!! mascot-tip "{{CHARACTER_NAME}}'s Tip"
    ![{{CHARACTER_NAME}} giving a tip](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    Always check your answers by substituting back into
    the original equation. It only takes a moment and
    catches most errors!

!!! mascot-warning "Common Mistake"
    ![{{CHARACTER_NAME}} warning](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    Don't forget to account for the negative sign when
    using the quadratic formula. The ± means you need
    to solve BOTH cases!

!!! mascot-encourage "You Can Do This!"
    ![{{CHARACTER_NAME}} encouraging](../../img/mascot/encouraging.png){ class="mascot-admonition-img" }
    Factoring can feel tricky at first. That's completely
    normal! With practice, you'll start seeing patterns
    everywhere.

!!! mascot-celebration "Great Progress!"
    ![{{CHARACTER_NAME}} celebrating](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    You've now mastered the quadratic formula! This is
    one of the most important tools in all of algebra.
```

### Step 7: Add Character Guidelines to CONTENT-GENERATION-GUIDE.md

To ensure consistent mascot usage across AI-generated content, add a section
to the project's `CONTENT-GENERATION-GUIDE.md`.

**Check whether the file already exists first.** Since `init-textbook`
(book-installer feature #0) now scaffolds `CONTENT-GENERATION-GUIDE.md` at
project birth with a base template (Concept Depth & Word-Count Targets,
Anti-Padding & Writing Style Rules, MicroSims, Markdown Formatting Rules),
the file almost always exists by the time this skill runs:

- **File exists (the normal case):** Insert the mascot block below
  immediately **after the file's opening header paragraph and before the
  first existing `##` section** (an HTML comment in the base template marks
  this exact spot). Do **not** re-add Anti-Padding, MicroSims, or Markdown
  Formatting Rules sections — the base template already has them, and a
  second copy would drift out of sync with the first over time. Also add one
  sentence to the file's opening paragraph noting that instructor-facing
  content is exempt from mascot guidance, if that sentence isn't already
  there.
- **File does not exist (older project, scaffolded before this feature
  existed):** Create it from scratch using
  `skills/book-installer/assets/init-textbook/CONTENT-GENERATION-GUIDE.md` as
  the base (substitute `{{SITE_NAME}}`), then insert the mascot block the
  same way.

The mascot block MUST include a **Mascot File Index** that links to every
textbook file this skill produces, so future agents working in the repo can
find the canonical artifacts in one lookup instead of re-discovering them via
globbing.

**Do not abridge the template below.** The two sections that carry the most
weight are the ones most likely to be trimmed as "boilerplate":

- **Mascot Admonition Guidelines** — the per-pose instructional-design rules.
  Without them an agent picks poses by tone rather than by pedagogical
  function, and the mascot degrades into decoration. This is the single most
  valuable part of the file.
- **Quality Assurance & Validation** — makes the placement rules enforceable
  instead of aspirational.

Fill in every `{{PLACEHOLDER}}` from the Step 2 Q&A. Where the template gives
an example phrase in a **Tone** line, replace it with one in the character's
actual voice rather than copying the generic wording.

```markdown
## Learning Mascot: {{CHARACTER_NAME}} the {{SPECIES}}

### Mascot File Index

The canonical files for this mascot. When editing any of these, update the
others in the same turn so they stay in sync.

| File | Purpose |
|------|---------|
| [`docs/img/mascot/character-sheet.md`](docs/img/mascot/character-sheet.md) | Canonical identity document (name, species, colors, voice). Source of truth. |
| [`docs/img/mascot/image-prompts.md`](docs/img/mascot/image-prompts.md) | Self-contained AI prompts for regenerating each pose. |
| [`docs/img/mascot/neutral.png`](docs/img/mascot/neutral.png) | Default / general-purpose pose. |
| [`docs/img/mascot/welcome.png`](docs/img/mascot/welcome.png) | Chapter-opening pose. |
| [`docs/img/mascot/thinking.png`](docs/img/mascot/thinking.png) | Key-concept pose. |
| [`docs/img/mascot/tip.png`](docs/img/mascot/tip.png) | Hint / helpful-guidance pose. |
| [`docs/img/mascot/warning.png`](docs/img/mascot/warning.png) | Common-mistake / pitfall pose. |
| [`docs/img/mascot/encouraging.png`](docs/img/mascot/encouraging.png) | Difficult-content / struggle pose. |
| [`docs/img/mascot/celebration.png`](docs/img/mascot/celebration.png) | End-of-chapter / achievement pose. |
| [`docs/css/mascot.css`](docs/css/mascot.css) | Custom admonition styles for the seven pose contexts. |
| [`docs/learning-graph/mascot-test.md`](docs/learning-graph/mascot-test.md) | Rendering test page that exercises every admonition style. |

### Character Overview

- **Name**: {{CHARACTER_NAME}}
- **Species**: {{SPECIES}}
- **Personality**: {{TRAIT_1}}, {{TRAIT_2}}, {{TRAIT_3}}, {{TRAIT_4}}
- **Catchphrase**: "{{CATCHPHRASE}}"
- **Visual**: {{BRIEF_APPEARANCE_DESCRIPTION}}

### Voice Characteristics

- {{VOICE_TRAIT_1}} (e.g., "Uses simple, encouraging language")
- {{VOICE_TRAIT_2}} (e.g., "Occasionally uses subject-specific puns")
- {{VOICE_TRAIT_3}} (e.g., "Refers to students as 'explorers' or 'investigators'")
- Signature phrases: "{{PHRASE_1}}", "{{PHRASE_2}}", "{{PHRASE_3}}"

### Mascot Admonition Format

Always place mascot images in the admonition body, never in the title bar:

    !!! mascot-welcome "Title Here"
        ![{{CHARACTER_NAME}} waving welcome](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
        Admonition text goes here after the image.

### Placement Rules

| Context | Admonition Type | Frequency |
|---------|----------------|-----------|
| General note / sidebar | mascot-neutral | As needed |
| Chapter opening | mascot-welcome | Every chapter |
| Key concept | mascot-thinking | 2-3 per chapter |
| Helpful tip | mascot-tip | As needed |
| Common mistake | mascot-warning | As needed |
| Difficult content | mascot-encourage | Where students may struggle |
| Section completion | mascot-celebration | End of major sections |

### Mascot Admonition Guidelines (Instructional Design Rules)

Each pose carries a distinct cognitive and pedagogical job. The pose is a
signal to the reader, not decoration — an agent that picks a pose by vibe
rather than by function destroys the wayfinding value of the whole system.
Agents generating these admonitions must follow the rules below.

#### 1. `mascot-welcome` (Motivational Hook / Advance Organizer)

- **Instructional purpose**: Addresses the "What's In It For Me?" (WIIFM)
  question and lowers learning anxiety before technical content begins. It is
  not there to teach the chapter — it is there to **sell** the chapter.
- **Rule**: Do not summarize technical concepts or explain mechanics. Tell the
  reader *why* they should care and *what they will be able to build* by the
  end.
- **Tone**: Warm, sincere, and a little fun. Use {{SUBJECT}}-flavored
  metaphors. Include the signature catchphrase "{{CATCHPHRASE}}".
- **Length**: Strictly 2-4 sentences. *(Exception: Chapter 1, where
  {{CHARACTER_NAME}} introduces themselves and their role in the book.)*

#### 2. `mascot-thinking` (Cognitive Scaffolding / Mental Models)

- **Instructional purpose**: Marks a "eureka" moment, an abstraction, or a
  shift in mental model. Signals that the reader should pause and process the
  *why* behind the *how*.
- **Rule**: Never use this for a mere fact or a piece of syntax. Reserve it
  for underlying algorithms, core mechanics, or architectural patterns —
  the ideas a reader must restructure their thinking around.
- **Tone**: Insightful and reflective. Rhetorical questions and analogies work
  well ("Notice how…", "Think of it like…").

#### 3. `mascot-tip` (Just-in-Time Support / Heuristics)

- **Instructional purpose**: Delivers a heuristic, shortcut, or best practice
  that isn't strictly required but measurably reduces cognitive load. This is
  expert insight whispered to a novice.
- **Rule**: Must be immediately actionable — a concrete shortcut, a diagnostic
  question, a naming convention, a way to sanity-check an answer. If the
  reader cannot *do* something differently after reading it, it is not a tip.
- **Tone**: Conspiratorial and clever ("Here's a shortcut…", "Want to save
  yourself an hour?").

#### 4. `mascot-warning` (Anticipatory Guidance / Pitfall Prevention)

- **Instructional purpose**: Anticipatory guidance that heads off a known
  novice pitfall. It deliberately interrupts reading flow to prevent
  downstream frustration.
- **Rule**: State the pitfall, *why* it happens, and exactly how to avoid or
  recover from it. A warning without a remedy is just anxiety — always supply
  the fix.
- **Tone**: Alert but reassuring; never scolding or ominous ("Watch out
  for…", "A common trap here is…").

#### 5. `mascot-encourage` (Affective Support / Normalizing Struggle)

- **Instructional purpose**: Emotional support at a known point of high
  cognitive friction. Normalizes struggle and supports a growth mindset.
- **Rule**: Use ONLY when introducing a notoriously difficult topic — not as
  generic cheerleading. Validate that the difficulty is real, connect it to
  something the reader has already succeeded at, and suggest a concrete way
  forward (experiment, break it into steps, revisit a prerequisite).
- **Tone**: Empathetic and validating ("If this feels like a lot, that's
  normal — most people need two passes at it.").

#### 6. `mascot-celebration` (Formative Reinforcement / Closure)

- **Instructional purpose**: Positive reinforcement and closure at a genuine
  milestone. Satisfies the "Satisfaction" component of the ARCS motivation
  model, consolidating what was learned.
- **Rule**: Never just "Good job." Name the *specific* concept or skill the
  reader just mastered, so the achievement is concrete and reviewable.
- **Tone**: Joyful and proud ("You just built…", "That's {{TOPIC}} handled —
  and it's one of the harder ones.").

#### 7. `mascot-neutral` (General Aside / Framing)

- **Instructional purpose**: A general-purpose aside for content that carries
  no particular emotional charge — context, a historical note, a pointer to a
  related chapter.
- **Rule**: Use this when none of the six purposeful poses genuinely fits.
  Reaching for `mascot-neutral` more than once or twice per chapter usually
  means the content did not need a mascot admonition at all — use plain prose
  or a standard MkDocs admonition instead.
- **Tone**: Calm and matter-of-fact.

### Do's and Don'ts

**Do:**

- Use {{CHARACTER_NAME}} to introduce new topics warmly
- Include the catchphrase in welcome admonitions
- Keep dialogue brief (1-3 sentences, except the 2-4 sentence welcome)
- Match the pose to the *instructional purpose* above, not to the vibe
- Open each chapter with `mascot-welcome` and close it with
  `mascot-celebration`

**Don't:**

- Use {{CHARACTER_NAME}} more than 5-6 times per chapter
- Put mascot admonitions back-to-back
- Use the mascot for purely decorative purposes
- Change {{CHARACTER_NAME}}'s personality or speech patterns
- Use more than one `mascot-welcome` or `mascot-celebration` per chapter

## Quality Assurance & Validation

Language models drift away from strict formatting constraints, so mascot
placement must be checked programmatically rather than by eye.

**Post-generation rule**: after writing or editing any chapter, run the
validator before reporting the work complete:

    python $BK_HOME/skills/book-installer/scripts/validate-chapter-mascots.py docs/chapters/NN-slug/index.md

It flags: more than 6 mascot admonitions in a chapter, duplicate
`mascot-welcome` or `mascot-celebration`, back-to-back mascot admonitions,
any admonition missing its `mascot-admonition-img` image, and body text that
is clearly too short or too long for the 1-3 sentence rule.

If the validator reports issues, fix the chapter and re-run it until it exits
clean. Do not report completion on a chapter that still fails, and do not
relax a rule to make the check pass.
```

**Stop here — do not append Anti-Padding, MicroSims, or Markdown Formatting
Rules sections.** Those already exist in the base `CONTENT-GENERATION-GUIDE.md`
template (or were added when you created the file from that template in the
"file does not exist" branch above); the base template's Markdown Formatting
Rules section already covers the Markdown-vs-raw-HTML image path distinction
that mascot admonitions rely on. Two `## Markdown Formatting Rules` headings
in one file is a sign this step went wrong.

### Step 8: Verify the Implementation

After setup, verify the mascot works correctly:

```bash
mkdocs serve
```

Check the following:

1. Mascot images load correctly (no broken images)
2. Admonition styling appears as expected
3. Colors match the book's theme
4. Images are appropriately sized (not too large or small)
5. Text wrapping around images looks clean
6. Mobile/responsive layout works

### Step 9: Create a Mascot Rendering Test Page

Generate `docs/learning-graph/mascot-test.md` from the canonical template:

```sh
"$BK_HOME/skills/book-installer/scripts/render-mascot-test.sh" "{{CHARACTER_NAME}}"
```

The template is
[`references/assets/templates/docs/learning-graph/mascot-render-test.md`](assets/templates/docs/learning-graph/mascot-render-test.md).
Keep its two-part structure intact:

1. **Transparency and trim test grid** — show every pose over checkerboard and
   dark backgrounds. Run the browser-side pixel checks for transparent pixels,
   fully transparent corners, and exactly 4 px of visible-content margin on all
   four sides. Use alpha threshold 10 to match `trim-padding-from-image.py`.
2. **Mascot admonitions** — render all seven production admonition types with
   the corresponding image and `mascot-admonition-img` class. Do not replace the
   test grid with admonitions; both sections are required.

**IMPORTANT:** This page mixes the two path conventions, and they differ here.
Raw HTML `<img src>` and `data-src` attributes must use `../../img/mascot/`
(relative to the rendered URL `learning-graph/mascot-test/index.html`, since
MkDocs passes raw HTML through untouched). The seven Markdown admonition
images must use `../img/mascot/` (relative to the source file
`docs/learning-graph/mascot-test.md`, which MkDocs rewrites to `../../` on
output). Using `../../` in the Markdown renders fine but emits a
"target is not found" warning that fails `mkdocs build --strict`.

If any trim test reports a margin other than `4/4/4/4`, rerun the trimmer with
the exact image path and regenerate the page:

```sh
python "$BK_HOME/src/image-utils/trim-padding-from-image.py" docs/img/mascot/FILENAME.png
```

Do not weaken or remove a failed check to make the page pass. Fix the image.

**Note:** Place the test file in the `docs/learning-graph/` directory alongside the other learning graph assets. Include this page in the navigation unless the user requests that it is not
displayed.  If they do not want it display then add it to the exclude_docs section in the mkdocs.yml

```yml
exclude_docs: |
  docs/learning-graph/mascot-test.md
```

## Quick Reference

### File Structure

```
docs/
├── img/
│   └── mascot/
│       ├── character-sheet.md   # Canonical identity document (source of truth)
│       ├── image-prompts.md     # Self-contained pose prompts
│       ├── neutral.png
│       ├── welcome.png
│       ├── thinking.png
│       ├── tip.png
│       ├── warning.png
│       ├── encouraging.png
│       └── celebration.png
├── css/
│   └── mascot.css
└── learning-graph/
    └── mascot-test.md           # Mascot rendering test page
```

The `CONTENT-GENERATION-GUIDE.md` file at the project root MUST also contain a **Mascot File Index** linking to each of the files above (see Step 7). The index lets future agents find every mascot artifact in one lookup.

### Admonition Types

| Type | Usage | Title Bar Color |
|------|-------|-----------------|
| `mascot-neutral` | General sidebars / default | Slate gray |
| `mascot-welcome` | Chapter openings | Primary color |
| `mascot-thinking` | Key concepts | Secondary color |
| `mascot-tip` | Tips and hints | Teal |
| `mascot-warning` | Warnings | Red |
| `mascot-encourage` | Difficult content | Blue |
| `mascot-celebration` | Achievements | Purple |

### Mascot Image Placement Pattern

**Always** use this pattern — image in the body, never put the image in the title:

```markdown
!!! mascot-TYPE "Title Text"
    ![Description](PATH/TO/mascot/POSE.png){ class="mascot-admonition-img" }
    Body text goes here after the image.
```

## Step 10: Update the CLAUDE.md File

After the `CONTENT-GENERATION-GUIDE.md` mascot section has been added (Step 7), add the following to the CLAUDE.md file:

```
Before generating content for the chapters, lesson plans, quizzes, FAQ or other student facing text,
read the `CONTENT-GENERATION-GUIDE.md` file.  Note that the teacher guide or instructor guide or
other instructor facing content does not need to use the mascots described in the CONTENT-GENERATION-GUIDE.md
```


## Troubleshooting

### Images Not Loading

1. Verify images exist in `docs/img/mascot/`
2. Check file names match exactly (case-sensitive)
3. Verify path depth, remembering that Markdown and raw HTML differ:
   Markdown `![](...)` counts from the **source `.md` file**, raw HTML
   `<img src>` counts from the **rendered URL**
4. Markdown in `docs/chapters/01-intro/index.md` → `../../img/mascot/`
5. Markdown in `docs/learning-graph/mascot-test.md` → `../img/mascot/`
6. Raw HTML on either of those pages → `../../img/mascot/`
7. If `mkdocs build` warns "target is not found among documentation files" for
   an image that nonetheless displays correctly, a Markdown image is using the
   rendered-URL depth instead of the source-file depth

### Admonition Styles Not Appearing

1. Verify `css/mascot.css` is listed in `extra_css` in mkdocs.yml
2. Check browser dev tools for CSS loading errors
3. Ensure admonition type matches exactly (e.g., `mascot-welcome`, not `mascot_welcome`)
4. Verify `md_in_html` is in `markdown_extensions` (required for `<img>` tags inside admonitions)
5. Clear browser cache and rebuild: `mkdocs build --clean`

### Mascot Images Too Large/Small

- Adjust `--mascot-size` CSS variable in the `:root` section of `mascot.css`
- Default is 90px, which works well for most layouts

### Colors Don't Match Book Theme

1. Update CSS variables in `:root` section of `mascot.css`
2. Use your book's primary/secondary colors from mkdocs.yml palette
3. Use a color contrast checker to ensure text readability

### Too Much Padding Around Image

If the users says that there is too much padding around the icons, then run the `Trim Padding From Image` python program:

```sh
../scripts/trim-padding-from-image.py docs/img/mascot/FILENAME.png
```

## Related Skills

- `home-page-template.md` - Create home page with cover image
- `mkdocs-features.md` - Add admonitions and other features
- `cover-image-generator.md` - Generate AI images for book cover

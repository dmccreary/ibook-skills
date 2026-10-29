---
name: home-page-template
description: This skill creates a professional home page with cover image, social media metadata, and proper formatting for intelligent textbooks. It includes generating AI prompts for cover images with montage backgrounds and central titles, setting up Open Graph and Twitter card metadata, and configuring the index.md with proper frontmatter.
image: img/cover.png
og:image: img/cover.png
---

# Home Page Template

This skill creates a professional home page for intelligent textbooks with cover images optimized for social media sharing.

## What This Skill Creates

1. **docs/index.md** - Home page with proper frontmatter metadata
2. **docs/img/cover.png** - AI-generated cover image (user generates externally)
3. **Social media optimization** - Open Graph and Twitter Card metadata

## Prerequisites

- Existing MkDocs Material project (use `init-textbook.md` — feature 0 — first if needed)
- Access to an AI image generator (ChatGPT/DALL-E, Midjourney, or similar)
- Course/book description and key themes identified

## Workflow

### Step 1: Gather Book Information

Collect the following information from the user:

1. **Book Title** - The main title (e.g., "Automating Instructional Design")
2. **Subtitle** (optional) - A secondary tagline
3. **Description** - 1-2 sentence description for SEO and social sharing
4. **Key Themes** - 5-10 major topics/concepts covered in the book
5. **Target Audience** - Who the book is for
6. **Color Palette** - Primary colors for the book's branding
7. **Visual Style** - Modern, classic, technical, playful, etc.

### Step 2: Identify Montage Elements

Based on the book's themes, identify visual elements for the cover montage. These should be concrete, visually distinct items that represent the book's content.

#### Common Element Categories

**Technology/AI Themes:**
- Neural network patterns, circuit traces
- Chat bubbles, prompt interfaces
- Geometric AI iconography
- Data flow visualizations

**Education/Learning Themes:**
- Lightbulb icons (insight)
- Book or graduation cap silhouettes
- Ascending steps or pathways
- Connected nodes (knowledge graphs)

**Visualization/Data Themes:**
- Chart elements (bar, line, pie)
- Network graphs with nodes and edges
- Timeline bars with markers
- Map outlines with data points
- Flowchart arrows and shapes

**Process/Methodology Themes:**
- Gear mechanisms
- Puzzle pieces
- Circular workflow arrows
- Checklist elements

**Human/Interaction Themes:**
- Abstract human silhouettes
- Cursor/touch indicators
- Slider controls, buttons
- Interactive UI elements

### Step 3: Design the Cover Layout

Standard intelligent textbook cover layout:

```
+--------------------------------------------------------------+
|                                                              |
|     [Montage elements    [Montage elements                   |
|      distributed          distributed                        |
|      throughout]          throughout]                        |
|                                                              |
|               +------------------------+                     |
| Mascot        |                        |                     |
| Image         |    BOOK TITLE          |  (Semi-transparent  |
|               |    (White Text)        |   dark overlay)     |
|               |                        |                     |
|               +------------------------+                     |
|                                                              |
|  [More montage        [More montage                          |
|   elements]            elements]                             |
|                                                              |
+--------------------------------------------------------------+

Aspect Ratio: 1.91:1 (e.g., 1910x1000 pixels)
```

### Step 4: Generate the AI Image Prompt

Create a detailed prompt for the AI image generator. Follow this template:

```
A wide landscape book cover background (1.91:1 aspect ratio) for "[BOOK TITLE]".

[BACKGROUND DESCRIPTION]: Deep [PRIMARY COLOR]-to-[SECONDARY COLOR] gradient background.

[MONTAGE ELEMENTS]: A montage of [THEME] elements including:
- [Element 1 with visual description]
- [Element 2 with visual description]
- [Element 3 with visual description]
- [Continue for 6-10 elements]

[STYLE]: [VISUAL STYLE] design aesthetic with [ACCENT COLORS] accents.

[COMPOSITION]: Elements softly fade toward edges with subtle vignette, leaving center area darker/cleaner for white title text overlay.

[TECHNICAL]: Professional quality, high resolution. No text in image.
```

#### Example Prompts by Topic

**For Educational Technology Book:**
```
A wide landscape book cover background (1.91:1 aspect ratio) for an educational technology textbook. Deep blue (#1a237e) to teal (#00695c) gradient background with a montage of EdTech elements: glowing neural network patterns suggesting AI, network graph visualizations with interconnected nodes, timeline bars with milestone markers, small data charts and graphs, flowchart arrows, animated particle trails, a stylized 6-level pyramid in graduated colors (purple to blue), interactive UI elements like sliders and toggle buttons, lightbulb icons representing insight, interconnected gears showing process. Modern flat design aesthetic with warm orange (#ff7043) and electric purple (#7c4dff) accents. Elements softly fade toward edges, leaving center darker for white title text overlay. Professional, tech-forward, educational mood. No text in image.
```

**For Data Science Book:**
```
A wide landscape book cover background (1.91:1 aspect ratio) for a data science textbook. Dark navy (#0d1b2a) to deep purple (#1b0d2a) gradient background with a montage of data science elements: scatter plot visualizations, regression lines, decision tree branches, Python code snippets (stylized/blurred), Jupyter notebook cells, pandas dataframe grids, neural network layer diagrams, confusion matrix heatmaps, ROC curve shapes, bar and histogram silhouettes. Modern technical aesthetic with cyan (#00bcd4) and magenta (#e91e63) accent glows. Elements arranged as floating panels with subtle shadows, fading toward edges. Center area has darker overlay for white title text. Professional, analytical, modern mood. No text in image.
```

**For Business/Management Book:**
```
A wide landscape book cover background (1.91:1 aspect ratio) for a business management textbook. Deep charcoal (#263238) to dark blue (#1a237e) gradient background with a montage of business elements: organizational chart hierarchies, strategy matrix grids, upward trending arrows, pie chart segments, Gantt chart bars, handshake silhouettes, target/bullseye icons, ascending bar graphs, connected stakeholder nodes, briefcase icons, growth curve lines. Clean corporate aesthetic with gold (#ffc107) and teal (#009688) accents. Elements distributed evenly with professional spacing, subtle fade toward edges. Center reserved for white title text with semi-transparent overlay. Professional, strategic, authoritative mood. No text in image.
```

### Step 5: Generate the Cover Image

1. Copy the generated prompt
2. Use an AI image generator:
   - **ChatGPT/DALL-E**: Paste prompt directly
   - **Midjourney**: Add `--ar 191:100` for aspect ratio
   - **Stable Diffusion**: Use appropriate settings for 1910x1000
3. Generate 2-4 variations
4. Select the best result
5. Download at highest available resolution

### Step 6: Add Title Text Overlay (Optional)

If adding title text directly to the image:

1. Use image editing software (Canva, Figma, Photoshop, GIMP)
2. Add semi-transparent dark rectangle in center (opacity 40-60%)
3. Add title text in white
4. Recommended fonts: Inter, Montserrat, Source Sans Pro, or system sans-serif
5. Export as PNG at 1910x1000 pixels minimum

**Note:** Many users prefer to let the image stand alone without baked-in text, using HTML/CSS overlays instead for flexibility.

### Step 7: Save the Cover Image

Save the final image to the docs folder:

```
docs/img/cover.png
```

Recommended specifications:
- Format: PNG (for quality) or WebP (for size)
- Dimensions: 1910x1000 pixels minimum
- File size: Under 500KB for web performance

### Step 8: Create the Home Page (docs/index.md)

Create or update `docs/index.md` with proper frontmatter:

```markdown
---
title: {{BOOK_TITLE}}
description: {{BOOK_DESCRIPTION}}
image: /img/cover.png
og:image: /img/cover.png
twitter:image: /img/cover.png
hide:
  - toc
---
<style>
.md-content__inner h1 {display: none !important;}
</style>

# {{BOOK_TITLE}}

<figure markdown>
  ![{{BOOK_TITLE}}: {{SUBTITLE}}. Cover image of {{ONE_SENTENCE_COVER_DESCRIPTION}}](./img/cover.png){ width="100%" }
</figure>

**{{SUBTITLE}}**

{{INTRODUCTORY_PARAGRAPH}}

## About This Book

{{BOOK_DESCRIPTION_EXPANDED}}

## Who This Book Is For

{{TARGET_AUDIENCE_DESCRIPTION}}

## How to Use This Book

Use the navigation menu to explore:

- **Chapters** - Main educational content
- **Learning Graph** - Interactive concept visualization
- **Simulations** - Interactive MicroSims for hands-on learning
- **Glossary** - Key terms and definitions

## Getting Started

Start with [Chapter 1](chapters/01/index.md) to begin your learning journey.
```

### Frontmatter Fields Explained

| Field | Purpose | Example |
|-------|---------|---------|
| `title` | Page title in browser tab and SEO | `Automating Instructional Design` |
| `description` | SEO meta description, social sharing | `Learn to create interactive educational simulations using AI` |
| `image` | Default social media image path | `/img/cover.png` |
| `og:image` | Open Graph image (Facebook, LinkedIn) | `/img/cover.png` |
| `twitter:image` | Twitter Card image | `/img/cover.png` |
| `hide: - toc` | Hides table of contents on home page | - |

### Landing Page Title Rule (Required)

The cover image already shows the book title in large type, so the page's own
`<h1>` would repeat it directly above the image. Every landing page whose
cover image renders the title therefore does both of these things:

1. **Hide the h1 with the `<style>` block shown in Step 8.** Keep the
   `# {{BOOK_TITLE}}` heading in the Markdown source; the CSS only hides it
   from view.
2. **Put the book title in the cover image's alt text.** `display: none`
   removes the h1 from the accessibility tree, so the alt text is what tells a
   screen-reader user the title of the page. Start the alt text with the exact
   book title, add the subtitle if there is one, then add one sentence
   describing what the cover shows:

   ```markdown
   ![Automating Instructional Design: A Hands-On Course. Cover image of glowing network graphs, timeline bars, and slider controls on a blue background](./img/cover.png){ width="100%" }
   ```

Rules that go with it:

- **Never hide the h1 without the title in the alt text**, and never leave the
  alt text empty (`![]()`) or use the file name.
- **Only hide the h1 when the cover image actually renders the title.** The
  scaffold's placeholder `cover.png` does not, so a freshly scaffolded book
  keeps its h1 visible until the real cover is in place.
- **Show the subtitle as a visible bold line directly below the cover figure**
  when the image does not render it (see the Step 8 template), so sighted
  readers also see it.

### Step 9: Verify Social Media Preview

Test how the page appears when shared:

1. **Facebook Debugger**: https://developers.facebook.com/tools/debug/
2. **Twitter Card Validator**: https://cards-dev.twitter.com/validator
3. **LinkedIn Post Inspector**: https://www.linkedin.com/post-inspector/

Enter your deployed site URL to preview social cards.

### Step 10: Link the Cover Image (Optional)

The cover figure is already part of the Step 8 template. To make it a link to
the first chapter, wrap it in a link and keep the alt text required by the
Landing Page Title Rule:

```markdown
[![{{BOOK_TITLE}}: {{SUBTITLE}}. Cover image of {{ONE_SENTENCE_COVER_DESCRIPTION}}](./img/cover.png){ width="100%" }](chapters/01/index.md)
```

## Complete Example: docs/index.md

```markdown
---
title: Automating Instructional Design
description: Learn to transform learning objectives into interactive MicroSims using AI-assisted tools
image: /img/cover.png
og:image: /img/cover.png
twitter:image: /img/cover.png
hide:
  - toc
---
<style>
.md-content__inner h1 {display: none !important;}
</style>

# Automating Instructional Design

<figure markdown>
  ![Automating Instructional Design: Turning Learning Objectives into MicroSims. Cover image of glowing network graphs, timeline bars, a six-level pyramid, and slider controls on a blue-to-teal background](./img/cover.png){ width="100%" }
</figure>

**Turning Learning Objectives into MicroSims**

Welcome to **Automating Instructional Design**, a hands-on course for educators and training professionals.

## About This Course

This intermediate-level course teaches you how to leverage AI-assisted tools to transform learning objectives into interactive educational simulations called MicroSims. Bridge the gap between abstract pedagogical goals and concrete, interactive learning experiences.

## Who This Course Is For

- K-12 Teachers
- Corporate Training Specialists
- Higher Education Faculty
- Instructional Designers
- Curriculum Developers

No programming experience required.

## Getting Started

Start with [Chapter 1: Foundations of Learning Objective Analysis](chapters/01/index.md).
```

## Troubleshooting

### Image Not Appearing in Social Previews

1. Ensure image path starts with `/` (absolute from site root)
2. Verify image exists at `docs/img/cover.png`
3. Check image dimensions (minimum 1200x630 for best compatibility)
4. Clear social platform caches using their debug tools
5. Wait 24 hours for caches to refresh

### Image Quality Issues

- Use PNG for sharp graphics and text
- Minimum 1910x1000 pixels
- If file size is too large, use WebP or optimize PNG

### Title Appears Twice, or a Screen Reader Never Announces It

- Two titles stacked above the cover means the `<style>` block that hides the
  h1 is missing or sits before the frontmatter. It must come right after the
  closing `---`.
- A screen reader that never announces the book title means the cover alt text
  does not start with the title. The hidden h1 is not read, so fix the alt
  text as described in the Landing Page Title Rule.

### Frontmatter Not Working

- Ensure `---` delimiters are on their own lines
- No spaces before first `---`
- YAML syntax must be valid (proper indentation, colons)

## Quick Reference

```yaml
# Minimal frontmatter for social sharing
---
title: Book Title
description: Brief description for search engines and social sharing
image: /img/cover.png
og:image: /img/cover.png
twitter:image: /img/cover.png
hide:
  - toc
---
```

## Related Skills

- `init-textbook.md` - Create new MkDocs project structure (feature 0)
- `learning-graph-viewer.md` - Add interactive learning graph
- `book-publisher` (linkedin-post route) - Create social media announcements

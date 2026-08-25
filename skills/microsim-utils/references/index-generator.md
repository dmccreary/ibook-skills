---
name: microsims-index-generator
description: This skill generates a comprehensive index page for MicroSims in an intelligent textbook project. Use this skill when working with an MkDocs-based textbook that has MicroSims in a /docs/sims/ directory and needs an updated index page with screenshots, descriptions, and navigation. The skill captures missing screenshots, generates alphabetically-sorted grid cards using mkdocs-material format, and updates the mkdocs.yml navigation.
---

# MicroSims Index Generator

## Overview

This skill automates the creation and maintenance of a MicroSims index page for intelligent textbooks built with MkDocs Material theme. It scans the `/docs/sims/` directory, captures screenshots for MicroSims missing preview images, and generates a professionally formatted index page using mkdocs-material grid cards.

## Trigger Phrases

Invoke this skill when the user says:

- "Update the microsim listings"
- "Update the list of microsims"
- "Create a grid view of all the microsims"
- "Generate a listing of all the microsims"
- "Update the MicroSim index page"
- "Regenerate the sims index"

## When to Use This Skill

Use this skill when:

- A new MicroSim has been added and the index needs updating
- Multiple MicroSims exist but lack preview screenshots
- The MicroSims index page needs to be reformatted to grid cards
- MicroSim index.md files are missing description metadata
- The mkdocs.yml navigation section for MicroSims needs synchronization

## Prerequisites

- MkDocs project with Material theme configured
- `attr_list` and `md_in_html` markdown extensions enabled in mkdocs.yml
- MicroSims located in `/docs/sims/<microsim-name>/` directories
- Each MicroSim directory contains:
  - `main.html` - The interactive simulation
  - `index.md` - Documentation page with YAML frontmatter (title, description)
- Screenshot capture tool available at `~/.local/bin/bk-capture-screenshot`

## Running the Script

The whole workflow below is automated by `scripts/generate-microsim-index.py`.
Run it from the project root:

```bash
python3 $BK_HOME/skills/microsim-utils/scripts/generate-microsim-index.py --dry-run
```

Drop `--dry-run` to write the files. The course name is read from `site_name` in
`mkdocs.yml`; override with `--course-name "Physics 101"` and the sims directory
with `--base-dir`. The script is idempotent — rerunning it changes nothing once
the index is current, so it is safe to run after adding each MicroSim.

It writes `docs/sims/index.md`, rewrites `docs/sims/TODO.md` to match the current
screenshot state, and normalizes `title`/`description` quoting in each sim's
frontmatter. Directories named `template`, `shared-libs`, and `TODO` are skipped,
as is any sim whose `index.md` has no frontmatter (these are reported so you can
add one).

Do the manual steps below when you need to review or extend what the script does.

## Workflow

### Step 0: Verify mkdocs.yml Extensions

Before generating the index, verify that `mkdocs.yml` has the required markdown extensions for grid cards to render properly:

```yaml
markdown_extensions:
  - attr_list
  - md_in_html
```

Check the file:
```bash
grep -A 20 "markdown_extensions:" mkdocs.yml
```

If either `attr_list` or `md_in_html` is missing, add them to the `markdown_extensions` section before proceeding. Grid cards will not render without these extensions.

### Step 1: Discover MicroSims

List all MicroSim directories in `/docs/sims/`:

```bash
ls -d docs/sims/*/
```

Exclude the `index.md` file from the list. Each subdirectory represents a MicroSim.

### Step 2: Gather MicroSim Information

For each MicroSim directory, read the `index.md` file to extract from the YAML frontmatter:

1. **Title** - From the `title:` field or first H1 heading
2. **Description** - From the `description:` field in YAML frontmatter

Example YAML frontmatter structure:
```yaml
---
title: "Sine Function Visualization"
description: "Interactive plot of the sine function with slider control to explore points along the curve"
image: /sims/sine-function-plot/sine-function-plot.png
og:image: /sims/sine-function-plot/sine-function-plot.png
quality_score: 100
---
```

**Always wrap `title` and `description` in quotes.** An unquoted value containing
a colon (`title: Wired Logic: AND and OR`) is invalid YAML and will break the
build or silently truncate. Use double quotes normally; if the value itself
contains a double quote, use single quotes and double any apostrophe.

**Frontmatter must open with `---` on line 1.** A file whose body contains a
`---` markdown table separator or horizontal rule but has no frontmatter is NOT
a frontmatter document. Never parse one by splitting on `---` — that treats body
text as frontmatter and corrupts the file on rewrite. The script skips such files
and reports them; add real frontmatter to include them in the index.

### Step 3: Add Missing Descriptions

For any MicroSim that is **missing the `description:` field** in its index.md YAML frontmatter:

1. Read the index.md content to understand what the MicroSim does
2. Compose a concise 1-2 sentence description that explains:
   - What the MicroSim visualizes or demonstrates
   - Key interactive features (sliders, buttons, parameters)
   - Educational value or learning outcomes
3. Add the `description:` field to the YAML frontmatter

Example description format:
```yaml
description: "Interactive visualization of projectile motion with adjustable launch angle and initial velocity. Demonstrates parabolic trajectories and the effects of gravity."
```

Keep descriptions under 200 characters for optimal display in grid cards.

### Step 4: Check for Missing Screenshots

For each MicroSim, check if a PNG screenshot exists:

```bash
ls docs/sims/<microsim-name>/<microsim-name>.png
```

The screenshot filename must match the directory name (e.g., `command-syntax/command-syntax.png`).

### Step 5: Log Missing Screenshots to TODO.md (REQUIRED)

**IMPORTANT**: Before generating the index, you MUST create or update `/docs/sims/TODO.md` to log any MicroSims that are missing screenshots. This step is required even if you cannot run the screenshot capture tool.

For each MicroSim missing a screenshot, add an entry to `/docs/sims/TODO.md` with the exact shell command needed to capture the screenshot:

```markdown
# MicroSim Screenshot TODO

This file tracks MicroSims that need screenshots captured.

## Missing Screenshots

Run the following commands to capture missing screenshots:

### [MicroSim Name]
```bash
~/.local/bin/bk-capture-screenshot docs/sims/<microsim-name>
```

### [Another MicroSim Name]
```bash
~/.local/bin/bk-capture-screenshot docs/sims/<another-microsim-name>
```
```

The TODO.md file should include:
1. The MicroSim name as a heading
2. The exact shell command to run (copy-paste ready)
3. The date the issue was logged

### Step 6: Capture Screenshots (Optional)

If the screenshot capture tool is available, attempt to capture missing screenshots:

```bash
~/.local/bin/bk-capture-screenshot docs/sims/<microsim-name>
```

This tool:
- Captures an 800x600 screenshot of `main.html` using Chrome headless
- Waits 3 seconds by default for JavaScript to load
- Saves as `<microsim-name>.png` in the MicroSim directory

For MicroSims with complex animations, increase the delay:
```bash
~/.local/bin/bk-capture-screenshot docs/sims/<microsim-name> 5
```

#### Verify Screenshot Capture

After running the capture script, verify:

1. The PNG file was created
2. File size is reasonable (typically 20-100KB for rendered visualizations)
3. The image is not blank (indicating JavaScript didn't render)

#### Handle Failed Screenshots

If screenshot capture fails for a MicroSim, update the TODO.md entry with error details:

```markdown
### [MicroSim Name] - [Date]
- **Status**: Screenshot capture failed
- **Error**: [Brief description of the error]
- **Command**: `~/.local/bin/bk-capture-screenshot docs/sims/<microsim-name>`
- **Notes**: [Any observations about why it might have failed]
```

Continue processing other MicroSims rather than stopping on failure.

### Step 7: Generate Index Page Content

Create the index page at `/docs/sims/index.md` using mkdocs-material grid cards format.

#### Required YAML Frontmatter

```yaml
---
title: "List of MicroSims for [Course Name]"
description: "A list of all the MicroSims used in the [Course Name] course"
image: /sims/index-screen-image.png
og:image: /sims/index-screen-image.png
hide:
    toc
---
```

The course name comes from `site_name` in `mkdocs.yml`. Never hardcode it.

#### Grid Cards Structure

**IMPORTANT**: Use this exact format where the title/link comes first, then the image, then the description:

```markdown
# List of MicroSims for [Course Name]

Interactive Micro Simulations to help students learn [subject] fundamentals.

<div class="grid cards" markdown>

-   **[MicroSim Title](./microsim-name/index.md)**

    ![MicroSim Title](./microsim-name/microsim-name.png)

    Short description of what the MicroSim does and teaches.

</div>
```

#### Card Item Format

Each card follows this exact structure (order matters):

1. **Title with link** - Bold linked title (the link is the title text)
2. **Blank line**
3. **Image** - Screenshot with alt text matching title
4. **Blank line**
5. **Description** - 1-2 sentence summary from the index.md description field

Example card:
```markdown
-   **[Projectile Motion](./projectile-motion/index.md)**

    ![Projectile Motion](./projectile-motion/projectile-motion.png)

    A MicroSim demonstrating parabolic trajectories with adjustable launch angle, initial velocity, and gravity. Shows how changing parameters affects the path and range of a projectile.
```

**Note**: The horizontal rule (`---`) between title and image is optional. Some projects use it, some don't. Follow the existing project convention.

### Step 8: Sort Alphabetically

Sort all MicroSim cards alphabetically by their title. This ensures consistent ordering across the index page and navigation.

### Step 9: Update mkdocs.yml Navigation

Locate the MicroSims section in `mkdocs.yml` and update it with alphabetically sorted entries:

```yaml
  - MicroSims:
    - List of Microsims: sims/index.md
    - Bash vs Zsh: sims/bash-vs-zsh/index.md
    - Command Syntax Guide: sims/command-syntax/index.md
    # ... additional entries alphabetically
```

Keep "List of Microsims" as the first entry, then sort remaining items alphabetically.

## Output Files

This skill creates or updates:

1. `/docs/sims/index.md` - The main MicroSims index page with grid cards
2. `/docs/sims/<name>/<name>.png` - Screenshot for each MicroSim (if missing)
3. `/docs/sims/<name>/index.md` - Updated with description field (if missing)
4. `/docs/sims/TODO.md` - Log of any screenshot capture failures
5. `mkdocs.yml` - Updated navigation section for MicroSims

## Example Output

A complete index page for a physics course:

```markdown
---
title: List of MicroSims for Physics Course
description: A list of all the MicroSims used in the Physics course
image: /sims/index-screen-image.png
og:image: /sims/index-screen-image.png
hide:
    toc
---

# List of MicroSims for Physics

Interactive Micro Simulations to help students learn physics fundamentals.

<div class="grid cards" markdown>

-   **[Bouncing Ball](./bouncing-ball/index.md)**

    ![Bouncing Ball](./bouncing-ball/bouncing-ball.png)

    A simulation of a ball bouncing under the influence of gravity with adjustable parameters for elasticity and initial velocity.

-   **[Projectile Motion](./projectile-motion/index.md)**

    ![Projectile Motion](./projectile-motion/projectile-motion.png)

    A MicroSim demonstrating parabolic trajectories with adjustable launch angle and initial velocity.

-   **[Wave Interference](./wave-interference/index.md)**

    ![Wave Interference](./wave-interference/wave-interference.png)

    Interactive demonstration of constructive and destructive interference patterns from two wave sources.

</div>
```

## Troubleshooting

### Screenshot Capture Fails

If screenshot capture fails:
1. Verify Chrome/Chromium is installed
2. Check that `main.html` exists in the MicroSim directory
3. Increase delay for JavaScript-heavy simulations (add second parameter: `5`)
4. Check for CDN loading issues (may need network access)
5. Log the failure in `/docs/sims/TODO.md`

### Grid Cards Not Rendering

Ensure mkdocs.yml has required extensions:
```yaml
markdown_extensions:
  - attr_list
  - md_in_html
```

### Images Not Displaying

Verify image paths use relative format: `./microsim-name/microsim-name.png`

### Missing Descriptions

If a MicroSim lacks a description in its index.md:
1. Read the content to understand the MicroSim
2. Add a concise `description:` field to the YAML frontmatter
3. Keep descriptions under 200 characters

## Quality Checklist

Before completing the index generation, verify:

- [ ] All MicroSim directories have been discovered
- [ ] Each MicroSim has a `description:` field in its index.md frontmatter
- [ ] Every `title:` and `description:` value is wrapped in quotes
- [ ] No sim was skipped for missing frontmatter (the script reports these by name)
- [ ] Each MicroSim has a screenshot (or is logged in TODO.md if capture failed)
- [ ] Grid cards are sorted alphabetically
- [ ] No literal quote characters leaked into the rendered card titles
- [ ] mkdocs.yml navigation is updated and sorted
- [ ] The index.md renders correctly with `mkdocs serve`

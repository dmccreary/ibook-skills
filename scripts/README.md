# Book Utilities (bk) - Shell Scripts for Claude Skills

This directory contains the **bk*** (Book utilities) collection of shell scripts for managing Claude skills and intelligent textbook projects. All scripts use the `$BK_HOME` environment variable for consistent operation.

## Prerequisites

### Required: BK_HOME Environment Variable

All `bk*` scripts require the `$BK_HOME` environment variable to be set. This variable should point to the root directory of your ibook-skills repository.

**Setup:**

Add this line to your shell startup file (`~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`):

```bash
export BK_HOME=/path/to/your/ibook-skills
```

**Example:**
```bash
export BK_HOME=$HOME/Documents/ws/ibook-skills
```

After adding the line, reload your shell configuration:
```bash
source ~/.bashrc  # or ~/.zshrc, etc.
```

**Verify it's set:**
```bash
echo $BK_HOME
```

### Recommended: Personal Binary Location

For easy command-line access from anywhere, install scripts to your personal binary directory:

`$HOME/.local/bin` (or `~/.local/bin`)

Add this to your shell startup file:

**For Bash/Zsh:**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**For Fish:**
```fish
set -gx PATH $HOME/.local/bin $PATH
```

## Installation

### Quick Start

1. **Set BK_HOME** (required):
   ```bash
   export BK_HOME=/path/to/ibook-skills
   ```

2. **Install bk* scripts**:
   ```bash
   $BK_HOME/scripts/bk-install-scripts
   ```

3. **Install skills** into every agent present on this machine:
   ```bash
   bk-install-skills
   ```

4. **Verify with the main menu**:
   ```bash
   bk
   ```

## Available Scripts

All `bk*` scripts require `$BK_HOME` to be set and provide consistent colored output with comprehensive error checking.

**Skill Management:**
- `bk-analyze-skill-usage` - Generate skill usage analysis report
- `bk-install-skills` - Install skills into every agent present (Claude Code, Codex, Antigravity)
- `bk-list-skills` - List installed skills with their descriptions

**Script Management:**
- `bk-install-scripts` - Install bk* scripts to ~/.local/bin
- `bk` - Main menu for all utilities

**Textbook Building:**
- `bk-status` - Display textbook workflow status
- `bk-generate-book-metrics` - Generate book metrics report
- `bk-check-loops` - Verify the learning graph is a DAG (no cycles)
- `bk-diagram-reports` - Report diagram/MicroSim coverage across chapters

**Quality Checks:**
- `bk-microsim-quality-report-generator` - Score every MicroSim and write a report
- `bk-check-mascot-rules` - Enforce single-source mascot placement rules
- `bk-check-social-cover` - Verify Open Graph tags on a published book's cover page
- `bk-check-social-media` - Verify Open Graph tags in a MicroSim's main.html

**Environment Setup:**
- `bk-install-mkdocs` - Install Miniconda + a `mkdocs` env with mkdocs-material

**Image Processing:**
- `bk-resize-images` - Compress images for web
- `bk-capture-screenshot` - Capture MicroSim screenshots
- `bk-batch-capture-screenshots` - Capture screenshots for many MicroSims at once

**Plugin Installation:**
- `bk-install-social-override-plugin` - Install MkDocs social override plugin

### bk

Main menu script that lists all available `bk*` utilities with descriptions and allows running them by number.

**Usage:**
```bash
bk           # Show menu
bk 1         # Run the first utility
```

**Example output:**
```
════════════════════════════════════════════════════════════════
Build/Book Utilities
════════════════════════════════════════════════════════════════
BK_HOME: $HOME/Documents/ws/ibook-skills

  1. bk-resize-images              Compress large images to ~300KB PNG format
  2. bk-status                     Display intelligent textbook building workflow status
```

### bk-install-scripts

Installs symbolic links for all `bk*` scripts to `$HOME/.local/bin`.

**Requirements:** `$BK_HOME` must be set

**Usage:**
```bash
bk-install-scripts
```

**Features:**
- Validates `$BK_HOME` exists
- Creates `$HOME/.local/bin` if needed
- Links all executable `bk*` scripts
- Reports total count and lists all installed links
- Checks if `$HOME/.local/bin` is in PATH

### bk-install-skills

Creates symbolic links for every active skill in `$BK_HOME/skills/` inside the
skills directory of each supported agent:

| Agent | Target |
|-------|--------|
| Claude Code | `~/.claude/skills/` |
| OpenAI Codex | `~/.codex/skills/` |
| Google Antigravity | `~/.gemini/antigravity/skills/` |

All agents present on the machine are installed on every run, because the three
are often used together and a per-agent install leaves the others stale.

**Requirements:** `$BK_HOME` must be set (falls back to the script's parent directory)

**Usage:**
```bash
bk-install-skills                      # every agent present
bk-install-skills --only claude,codex  # just these
bk-install-skills --all                # include agents not yet present
bk-install-skills --list               # show agents and status
bk-install-skills --dry-run            # preview, change nothing
```

`bk-install-skills-codex` and `bk-install-skills-antigravity` remain as
deprecated shims that delegate to `--only`.

**Features:**
- Validates `$BK_HOME/skills` exists
- Creates `~/.claude/skills` if needed
- Links all skill directories
- Reports installed skills with count
- Checks for broken symlinks and suggests fixes

### bk-analyze-skill-usage

Generates a comprehensive skill usage analysis report from activity logs. Analyzes skill invocations, performance metrics, and usage patterns to help understand which skills are most used and how they perform.

**Requirements:** `$BK_HOME` must be set, Python 3 installed, activity logging enabled

**Usage:**
```bash
bk-analyze-skill-usage                    # Use default log directory
bk-analyze-skill-usage /path/to/logs      # Use custom log directory
```

**Features:**
- Analyzes skill usage frequency and patterns
- Calculates average and total duration for each skill
- Correlates prompts with skill invocations
- Shows recent skill usage history
- Provides insights and optimization suggestions
- Reports total time automated by skills

**Output includes:**
- Most used skills ranking
- Performance metrics (average/total duration)
- Common prompts that trigger skills
- Recent skill usage table (last 20 invocations)
- Insights about frequently used and slowest skills

### bk-status

Displays the status of the intelligent textbook building workflow by running a Python analysis script.

**Requirements:** `$BK_HOME` must be set, Python 3 installed

**Usage:**
```bash
bk-status                 # Analyze the current directory
bk-status /path/to/book   # Analyze a specific book directory
```

**Features:**
- Validates `$BK_HOME/src/book-status/book-status.py` exists
- Checks for Python 3 availability
- Runs workflow status analysis

### bk-list-skills

Lists every installed skill with its description, read from the YAML frontmatter
of each `SKILL.md`.

**Requirements:** `$BK_HOME` must be set

**Usage:**
```bash
bk-list-skills               # Names with descriptions
bk-list-skills --names-only  # Names only
bk-list-skills --full        # Full detail
bk-list-skills --json        # Machine-readable output
```

### bk-check-loops

Checks a vis-network learning-graph JSON file for cycles. Learning graphs must be
Directed Acyclic Graphs, so any loop indicates a broken concept dependency.

**Requirements:** Python 3; `src/learning-graph/check-loops.py`

**Usage:**
```bash
bk-check-loops                                  # docs/learning-graph/learning-graph.json
bk-check-loops path/to/learning-graph.json      # Explicit path
```

**Exit codes:** `0` when the graph is a valid DAG, `1` when loops are found.

### bk-diagram-reports

Analyzes chapter markdown for diagram and MicroSim specifications, then writes
table and detail reports on coverage across the book.

**Requirements:** `$BK_HOME` must be set, Python 3; `src/diagram-reports/diagram-report.py`

**Usage:**
```bash
cd /path/to/textbook
bk-diagram-reports
```

### bk-microsim-quality-report-generator

Scores every MicroSim in the repository and writes a quality report to
`docs/learning-graph/microsim-quality-report.md`, then opens it.

**Requirements:** Python 3; `src/book-metrics/microsim-quality-report.py`

**Usage:**
```bash
bk-microsim-quality-report-generator
```

**Output:** total MicroSim count, average quality score, and a breakdown of
perfect-scoring sims.

### bk-check-mascot-rules

Enforces that the mascot placement rules live in exactly one place:
`skills/book-installer/references/mascot-placement-rules.md`. Every other skill
must reference that file rather than restating its tables, counts, or per-pose
rules. Also detects hand-edits to a rendered `CONTENT-GENERATION-GUIDE.md` block.

**Requirements:** `$BK_HOME` must be set (falls back to the script's parent directory)

**Usage:**
```bash
bk-check-mascot-rules
```

**Exit codes:** `0` clean, `1` if any restatement or hand-edit is found.

### bk-check-social-cover

Verifies the Open Graph tags on a published book's **cover page** — `og:title`,
`og:description`, and `og:image` — including recommended length ranges.

The `og:image` basename on the home page must be exactly `cover.png`; any other
filename is an error.

**Usage:**
```bash
bk-check-social-cover algebra-1                            # Resolves the GitHub Pages URL
bk-check-social-cover https://dmccreary.github.io/algebra-1/
```

**Exit codes:** `0` when tags pass, `1` on a violation.

### bk-check-social-media

Verifies Open Graph tags inside a **MicroSim's** `main.html`, checking presence
and length of `og:title`, `og:description`, and `og:image`, and validating image
dimensions (1200x630, a 1.91:1 ratio, is recommended).

**Usage:**
```bash
cd /path/to/microsim && bk-check-social-media
bk-check-social-media /path/to/microsim
```

### bk-install-mkdocs

Installs a complete MkDocs environment: downloads Miniconda if absent, creates a
Python 3 environment named `mkdocs`, installs `mkdocs` and `mkdocs-material`,
then prints the installed versions to verify. Detects OS and architecture.

**Usage:**
```bash
bk-install-mkdocs
```

### bk-batch-capture-screenshots

Captures screenshots for a batch of MicroSims that lack PNG images, rather than
one at a time.

> **⚠️ Currently non-functional.** This script hardcodes an absolute path to
> `capture_screenshot.sh` in the retired `microsim-screen-capture` skill, which
> was consolidated into `microsim-utils`. It also hardcodes one developer's
> repository path and a fixed list of MicroSim names. Use
> `bk-capture-screenshot` per MicroSim until this is rewritten.

### bk-resize-images

Compresses large images to approximately 300KB PNG format for web optimization.

**Requirements:** `$BK_HOME` must be set, Python 3 and Pillow installed

**Usage:**
```bash
bk-resize-images [args]
```

**Features:**
- Validates `$BK_HOME/src/resize-images/compress-images.py` exists
- Checks for Python 3 and Pillow/PIL
- Passes all arguments to Python script
- Changes to `$BK_HOME` before running

### bk-capture-screenshot

Captures high-quality screenshots of MicroSims using Chrome headless mode. Can be run from within a MicroSim directory or by providing a path.

**Requirements:** Google Chrome or Chromium installed

**Usage:**
```bash
cd /path/to/microsim && bk-capture-screenshot   # Use current directory
bk-capture-screenshot /path/to/microsim         # Specify directory path
```

**Features:**
- Automatically detects MicroSim name from directory
- Validates main.html exists
- Uses Chrome headless mode for rendering
- Handles JavaScript-heavy visualizations with proper timeout
- Allows loading external CDN resources
- Generates PNG file named after the MicroSim
- Provides clear success/failure feedback with file size

**Output:**
- Creates `{microsim-name}.png` in the MicroSim directory
- Screenshot size: 1200x800 pixels
- Includes all rendered content after JavaScript execution

**Technical details:**
- Uses `--headless=new` for latest Chrome headless mode
- 5-second timeout for JavaScript rendering
- Disables web security to allow CDN resources
- Hides scrollbars for clean captures

### bk-install-social-override-plugin

Installs the social_override plugin for mkdocs-material into the current directory for custom social media card images.

**Requirements:** `$BK_HOME` must be set, pip installed

**Usage:**
```bash
cd /path/to/mkdocs-project
bk-install-social-override-plugin
```

**Features:**
- Validates `$BK_HOME` is set
- Warns if mkdocs.yml not found in current directory
- Creates plugin files in current directory
- Installs plugin with pip
- Provides clear next steps for configuration

## Architecture

### Consistent Design Pattern

All `bk*` scripts follow a consistent pattern:

1. **Validation**: Check `$BK_HOME` is set and exists
2. **Directory checks**: Validate required subdirectories exist
3. **Colored output**: Use consistent color scheme (green=success, yellow=warning, blue=info, red=error)
4. **Error handling**: Provide helpful error messages with suggestions
5. **Visual formatting**: Use consistent separators and formatting

### Color Scheme

- **Green**: Success messages, checkmarks
- **Yellow**: Warnings, important paths
- **Blue**: Section headers, informational text
- **Red**: Errors, failures

### Error Messages

All scripts provide actionable error messages:
- What went wrong
- What was expected
- How to fix it (with examples)

## Requirements

- **Bash** shell (version 4.0 or later)
- **$BK_HOME** environment variable set
- Standard Unix tools: `find`, `grep`, `sed`
- Python 3 (for scripts that call Python programs)
- Specific Python packages as needed (Pillow for image scripts)

## Benefits of BK_HOME Design

1. **Consistency**: All scripts use the same base directory
2. **Portability**: Works from any directory after installation
3. **Validation**: Scripts check environment before running
4. **Flexibility**: Easy to switch between different ibook-skills installations
5. **Error Prevention**: Clear error messages guide users to fix configuration

## Notes

- All `bk*` scripts validate `$BK_HOME` before running
- Scripts use `$BK_HOME` to locate resources (skills, Python programs, etc.)
- Symbolic linking strategy keeps scripts current with repository
- Consistent error messages help troubleshooting
- Scripts can be run from any directory (once installed)
- The `bk` menu automatically discovers and lists all `bk*` scripts

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
Most of these skills have also been tested in OpenAI Codex, Google Gemini, Cursor, Perplexity, and Hermes and have been shown to work if the CLAUDE.md file is copied to the AGENTS.md file.
Note that the skills that use image understanding to understand MicroSim layout errors
do not work well on non-Claude systems.

## Project Overview

This repository contains a curated collection of Claude AI skills for creating intelligent, interactive educational textbooks. Each skill is an autonomous agent that automates specific aspects of educational content creation - from learning graph generation to interactive p5.js simulations (MicroSims).

The skills are designed for building **Level 2+ intelligent textbooks**.  Level 2 puts a focus on generating interactive content that can be monitored using the experience API (xAPI).  Books are created using markdown, MkDocs with Material theme.
Content generated should following educational frameworks like Bloom's Taxonomy (2001) for classifying educationa objecives.
The levels include remember, understand, apply, analyze, evaluate and create.  Defintions of terms should follow the ISO 11179 metadata standards (precise, concise, distinct, non-circular, unecumbered with rules).  All books
contain a concept dependency graphs in the docs/learing-graph/learning-graph.json file.  This helps us
not use concepts in a chapter that have not been introduced yet.

## Repository Structure

```
ibook-skills/
├── skills/                          # Active skill definitions (14 loaded skills)
│   ├── archived/                    # Verbatim originals of consolidated skills (never loaded; see its README alias map)
│   │
│   │ # Meta-Skills (routers with references/ guides)
│   ├── book-installer/              # Infrastructure: init-textbook scaffold (feature 0), 40 features incl. Google Analytics, book-metrics
│   ├── microsim-generator/          # MicroSims: p5, chartjs, timeline, map, vis-network, mermaid, causal-loop, concept-classifier, infographic-overlay, docker-python-lab, verified-infographic posters, …
│   ├── microsim-utils/              # MicroSim QA: standardization, screen-capture, index-generator, iframe tools, layout-reviewer, diagram-reports
│   ├── book-media-generator/        # Media: MARP web decks, .pptx lectures, stories, chapter images, TTS + pronounce buttons
│   ├── book-publisher/              # Promotion: README, LinkedIn post, LinkedIn carousel, press release (all read book-metrics.json)
│   │
│   │ # Content-Pipeline Skills (kept separate — complex workflows)
│   ├── course-description-analyzer/ # Validates course descriptions
│   ├── learning-graph-generator/   # Generates 300-600 concept learning graphs (+ analyze/convert/taxonomy scripts)
│   ├── book-chapter-generator/      # Designs chapter structure from learning graph
│   ├── chapter-content-generator/   # Generates detailed chapter content (canonical blooms-taxonomy.md lives here)
│   ├── glossary-generator/         # Creates ISO 11179-compliant glossaries
│   ├── faq-generator/              # Generates FAQs from course content
│   ├── quiz-generator/             # Generates Bloom's Taxonomy-aligned quizzes
│   ├── reference-generator/        # Generates curated reference lists
│   │
│   │ # Standalone
│   └── docx-to-web-publisher/      # .docx → Next.js content-catalog pages (non-MkDocs)
│
├── docs/                          # MkDocs documentation site
├── scripts/                       # Utility scripts
│   └── bk-install-skills         # Symlinks skills into every agent present
├── commands/                      # Slash commands
│   └── ibook.md                  # /ibook runbook command
└── mkdocs.yml                    # MkDocs configuration
```

**Key Directories:**
- **`skills/`**: Each subdirectory contains a SKILL.md file defining the skill's behavior, plus supporting files (Python scripts, templates, reference docs)
- **`skills/archived/`**: Contains individual skills that have been consolidated into meta-skills to stay under the 30-skill limit
- **`docs/`**: Documentation site built with MkDocs Material theme, deployed to GitHub Pages

## Architecture Patterns

### Skill System

Skills are autonomous agents loaded by Claude Code. Each skill:
1. Is defined by a `SKILL.md` file with YAML frontmatter containing `name:`, `description:`, `license:`, and optional `allowed-tools:`
2. Contains workflow instructions that Claude executes step-by-step
3. May include supporting assets (Python scripts, templates, reference documents)
4. Is designed to be invoked with `/skill [skill-name]` or through the Skill tool

### Meta-Skill Architecture (30-Skill Limit Workaround)

Claude Code has a **maximum limit of 30 skills** that can be loaded at once. To work around this limitation, related skills have been consolidated into **meta-skills** that act as routers:

| Meta-Skill | Sub-Skills (in `references/` folder) | Purpose |
|------------|--------------------------------------|---------|
| `book-installer` | init-textbook (feature 0), mkdocs-features, learning-graph-viewer, skill-tracker, google-analytics, book-metrics, and many more (see its routing table) | Project scaffold, infrastructure, and book reporting |
| `microsim-generator` | p5, chartjs, timeline, map, vis-network, mermaid, plotly, venn, bubble, causal-loop, comparison-table, celebration, concept-classifier, infographic-overlay, docker-python-lab, verified-infographic | Creates MicroSims with various JS libraries, plus fact-verified posters |
| `microsim-utils` | standardization, screen-capture, add-icons, index-generator, iframe-auto-height, iframe-tester, layout-reviewer, diagram-reports | MicroSim maintenance, QA, and reports |
| `book-media-generator` | marp-deck, pptx-lecture, story, chapter-images, text-to-speech, pronounce-button | Slides, illustrations, sourced images, and audio |
| `book-publisher` | readme, linkedin-post, linkedin-carousel, press-release | Publishing and promotion (all routes read `docs/learning-graph/book-metrics.json`) |

**How meta-skills work:**
1. User invokes the meta-skill (e.g., `microsim-generator`)
2. Meta-skill analyzes the request using keyword matching
3. Meta-skill loads the appropriate guide from its `references/` directory
4. Guide contains the full workflow for that specific sub-skill

**Archived skills** in `skills/archived/` are the original individual skills that have been consolidated. They are kept for reference but are not loaded by Claude Code.

### Learning Graph Architecture

The learning graph generator follows this data flow:

```
course-description.md
  → concept enumeration (300-600 concepts)
  → dependency mapping (CSV with DAG structure)
  → quality validation (Python: analyze-graph.py)
  → taxonomy categorization (12 categories)
  → JSON conversion (vis-network format for visualization)
```

**Critical constraint**: Dependency graphs must be **Directed Acyclic Graphs (DAGs)** - no circular dependencies allowed.

### MicroSim Pattern

MicroSims are interactive simulations stored in `docs/sims/[sim-name]/`. They support multiple JavaScript libraries (p5.js, Chart.js, vis-network, Mermaid, Leaflet, etc.).

#### Standard MicroSim File Structure

Each MicroSim directory should contain separate files for maintainability:

```
docs/sims/[sim-name]/
├── main.html          # HTML structure (loads CSS, JS, and data)
├── style.css          # All styling (layout, colors, responsive design)
├── script.js          # Application logic and interactivity
├── data.json          # Data separate from code (optional, for data-driven MicroSims)
├── metadata.json      # MicroSim metadata (title, description, keywords, license)
└── index.md           # MkDocs documentation page with iframe embed
```

#### File Separation Rules

**Why separate files?**

1. **Maintainability**: Easier to update styles, logic, or data independently
2. **Reusability**: CSS and JS patterns can be shared across MicroSims
3. **Collaboration**: Different team members can work on different files
4. **Debugging**: Isolate issues to specific files
5. **Caching**: Browsers can cache static CSS/JS files

**`main.html`** - Structure only:

- Contains HTML markup and element structure
- Loads external libraries via CDN
- Links to `style.css` and `script.js`
- Should NOT contain inline `<style>` or `<script>` blocks (except for data initialization)
- Use semantic HTML elements

**`style.css`** - Presentation only:

- All CSS rules for layout, colors, typography
- Responsive design with `@media` queries
- Use CSS custom properties (variables) for theming
- No JavaScript or logic

**`script.js`** - Behavior only:

- All JavaScript for interactivity
- Event handlers, chart initialization, animations
- Configuration objects for libraries (Chart.js, vis-network, etc.)
- Should reference a `chartData` or similar config object for data

**`data.json`** - Data only (when applicable):

- Raw data separate from visualization logic
- Makes it easy to update data without touching code
- Useful for: chart data, graph nodes/edges, map markers, timeline events
- Load via `fetch('data.json')` in script.js

**`metadata.json`** - MicroSim metadata (validated by schema):

- Must conform to the schema at `skills/microsim-generator/assets/templates/shared/microsim-metadata-schema.json`
- **Required sections**: dublinCore, search, educational, technical, userInterface
- **Dublin Core**: title, creator, subject, description, date, type, format, rights
- **Search**: tags, visualizationType, keywords for discoverability
- **Educational**: gradeLevel, subjectArea, topic, learningObjectives, Bloom's taxonomy levels
- **Technical**: framework, canvasDimensions, dependencies, accessibility
- **User Interface**: controls, visual elements, layout pattern
- Enables automated indexing, catalog generation, and quality validation

**`index.md`** - MkDocs documentation page:

- Must include an iframe embedding the MicroSim for inline viewing
- Must include a fullscreen button link
- Standard format:

```markdown
# MicroSim Title

Brief description of what the MicroSim demonstrates.

<iframe src="./main.html" width="100%" height="500px" scrolling="no"></iframe>

[View Fullscreen](./main.html){ .md-button .md-button--primary }

## Overview
...
```

- The iframe allows users to interact with the MicroSim directly in the documentation
- The fullscreen button opens main.html in a new tab for larger viewing
- Adjust `height` as needed (typically 400px-600px depending on MicroSim complexity)

#### Example: ChartJS MicroSim Structure

```html
<!-- main.html -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<link rel="stylesheet" href="style.css">
<!-- ... HTML structure ... -->
<script src="script.js"></script>
```

```javascript
// script.js - define data object at top, then visualization logic
const chartData = {
    labels: ['Category A', 'Category B'],
    values: [60, 40],
    colors: ['rgba(74, 144, 226, 0.85)', 'rgba(80, 200, 120, 0.85)'],
    // ... configuration
};
// Chart initialization and event handlers follow
```

#### When Inline Code is Acceptable

- **Prototyping**: Quick experiments before refactoring
- **Single-use data**: Small datasets specific to one visualization
- **Legacy MicroSims**: Existing inline code doesn't need refactoring unless being updated

#### MicroSim Design Principles

- Each simulation focuses on one educational concept
- Uses seeded randomness for reproducibility
- Includes interactive controls (sliders, buttons, tabs)
- Responsive design that works in iframes
- Accessible color schemes and font sizes

### MicroSim Screenshot Capture

When the user says "capture screenshot", "capture screen image", or "capture microsim screen image", use the `bk-capture-screenshot` script:

```bash
~/.local/bin/bk-capture-screenshot <microsim-directory-path>
```

**Example:**
```bash
~/.local/bin/bk-capture-screenshot /Users/dan/Documents/ws/my-textbook/docs/sims/bouncing-ball
```

The script:
- Starts a local HTTP server to properly load CDN resources
- Waits 3 seconds for JavaScript to render
- Captures a 1200x800 screenshot using Chrome headless
- Saves as `{microsim-name}.png` in the MicroSim directory

**Proactive Behavior:** When a user indicates they are happy with a MicroSim's layout (e.g., "looks good", "that's perfect", "I like it"), proactively ask:

> "Would you like me to capture a screenshot of this MicroSim for the catalog listing in `docs/sims/index.md`?"

This ensures MicroSims have preview images for the index page grid display.

**Session Logging:** After capturing a screenshot, proactively ask the user if they want to log the session:

> "Would you like me to log this session's design decisions to `logs/{microsim-name}.md`?"

Session logs document the specification, instructional design decisions, technical choices, revisions made, and serve as a reference for future MicroSim development.

### Intelligent Textbook Workflow

Building an intelligent textbook follows this 12-step process using multiple skills:

1. **Course Description** (`course-description-analyzer`) → 2. **Bloom's Taxonomy Integration** → 3. **Concept Enumeration** (300-600 concepts) → 4. **Concept Dependencies** (DAG) → 5. **Concept Taxonomy** (`learning-graph-generator`) → 6. **Learning Graph Visualization** (`book-installer` → learning-graph-viewer) → 7. **Chapter Structure** (`book-chapter-generator`) → 8. **Content Generation** (`chapter-content-generator`) → 9. **MicroSim Creation** (`microsim-generator`) → 10. **Supporting Content** (`glossary-generator`, `faq-generator`, `quiz-generator`) → 11. **Quality Assurance** (`book-installer` → book-metrics, `microsim-utils`) → 12. **Deployment** (mkdocs gh-deploy) → 13. **Publish & Announce** (`book-publisher`: README, LinkedIn, press release)

## Common Development Tasks

### Working with Skills

**List available skills:** just ask Claude — skill names and descriptions are injected into context at session start at zero token cost.

**Install skills globally (for all projects):**
```bash
export BK_HOME=$HOME/Documents/ws/ibook-skills   # if not already set
scripts/bk-install-skills
```
This symlinks every active skill (any `skills/*/` containing `SKILL.md`, which excludes `skills/archived/`) into each agent present on the machine — `~/.claude/skills/`, `~/.codex/skills/`, and `~/.gemini/antigravity/skills/` — and prunes links whose skill no longer exists. Narrow it with `--only claude`, preview with `--dry-run`, inspect with `--list`.

**Install skills for a single project:**
Skills install globally for every agent. For a project-scoped install, symlink the `skills/*` directories into that project's own `.claude/skills/` directory instead.

### Working with Documentation

**Build and serve the documentation site:**
```bash
mkdocs serve
# Opens at http://localhost:8000
```

**Build for production:**
```bash
mkdocs build --strict
```

**Deploy to GitHub Pages:**
```bash
mkdocs gh-deploy
```

### Working with Learning Graphs

When the learning-graph-generator skill creates files in `/docs/learning-graph/`, you must:

1. **Run Python scripts in the learning-graph directory:**
```bash
cd docs/learning-graph
python analyze-graph.py learning-graph.csv quality-metrics.md
python csv-to-json.py learning-graph.csv learning-graph.json
python taxonomy-distribution.py learning-graph.csv taxonomy-distribution.md
```

2. **Update mkdocs.yml navigation** to include new files:
```yaml
nav:
  - Learning Graph:
    - Introduction: learning-graph/index.md
    - Course Description Assessment: learning-graph/course-description-assessment.md
    - Concept Enumeration: learning-graph/list-concepts.md
    - Graph Quality Analysis: learning-graph/quality-metrics.md
```

3. **Always verify** `learning-graph.json` is valid JSON before using in visualizations

## Educational Frameworks

### Bloom's Taxonomy (2001 Revision)

All content generation follows the six cognitive levels:
1. **Remember** (Red) - Define, list, recall, identify
2. **Understand** (Orange) - Summarize, explain, classify
3. **Apply** (Yellow) - Implement, solve, use
4. **Analyze** (Green) - Differentiate, compare, organize
5. **Evaluate** (Blue) - Judge, critique, assess
6. **Create** (Purple) - Design, construct, develop

### ISO 11179 Standards (Glossary Definitions)

Glossary terms must be:
- **Precise** - Exact meaning without ambiguity
- **Concise** - Minimal words needed
- **Distinct** - Unique from related terms
- **Non-circular** - Don't define terms using themselves
- **Free of business rules** - No implementation details

### Five Levels of Textbook Intelligence

- **Level 1**: Static text and images, no interactive elements
- **Level 2**: Interactive content — hyperlinks, embedded videos, quizzes, MicroSims, glossary
- **Level 3**: Adaptive content — personalized pathways via concept-graph traversal
- **Level 4**: Chatbot integration — an LLM-powered tutoring assistant, often via GraphRAG
- **Level 5**: Autonomous AI — fully autonomous, real-time customized lesson generation (aspirational)

This repository targets Level 2 by default, using MicroSims, quizzes, and a searchable glossary for interactivity.

**The "2.99" design target:** most skills in this library are deliberately designed to sit at
Level 2.99, not Level 3. Gather as many interactive events (xAPI statements, MicroSim
interactions, quiz attempts) as possible to predict aggregate concept understanding across
all readers — but never gather or retain data tied to a specific, identifiable student. The
moment a system stores per-student performance history to personalize that individual's
pathway (true Level 3), it becomes a regulated entity under student-data-privacy law (e.g.
FERPA/COPPA) with obligations this project does not take on. Stay one step below that line by
default; a book that wants true Level 3 adaptivity must add its own data-governance layer
deliberately, not inherit it by accident.

## Data Format Specifications

### Learning Graph CSV Format

```csv
ConceptID,ConceptLabel,Dependencies,TaxonomyID
1,Introduction to Programming,,FOUND
2,Variables and Data Types,1,BASIC
3,Control Flow,1|2,BASIC
```

- **ConceptID**: Integer (1-600)
- **ConceptLabel**: Title Case, max 32 characters
- **Dependencies**: Pipe-delimited list of ConceptIDs (empty for foundational concepts)
- **TaxonomyID**: 3-5 letter abbreviation for category

### vis-network JSON Format

The `csv-to-json.py` script converts learning graphs to vis-network format:
```json
{
  "nodes": [
    {"id": 1, "label": "Concept Name", "group": "TAXID"}
  ],
  "edges": [
    {"from": 1, "to": 2}
  ]
}
```

## Important Conventions

### Markdown Generation

**Always place a blank line before markdown lists** - required by MkDocs:
```markdown
Here is a list:

- Item 1
- Item 2
```

### Concept Labels

- Use **Title Case**
- Maximum **32 characters**
- Avoid acronyms unless necessary for brevity
- Each concept should be atomic (single, clear idea)

### File Naming

- Skills use kebab-case: `learning-graph-generator`
- Markdown files use kebab-case: `course-description.md`
- Python scripts use snake_case but are typically: `analyze-graph.py`

### Navigation Updates

After adding any `.md` file to `docs/`, update the `nav:` section in `mkdocs.yml` so it appears in the site navigation.

## Quality Standards

### Learning Graph Quality Metrics

A high-quality learning graph should have:
- Quality score ≥ 70/100
- Zero circular dependencies (must be a DAG)
- Foundational concepts with zero dependencies
- No orphan nodes (nodes with zero inbound and zero outbound edges, making the graph disconnected)
- Terminal nodes are valid (nodes with inbound edges but no outbound edges — nothing depends on them, but they have dependencies)
- Average 2-4 dependencies per concept
- No single taxonomy category exceeding 30% of concepts
- All concepts connected to the main graph

### Content Quality Standards

Generated content should:
- Respect concept dependencies (prerequisites taught first)
- Address multiple Bloom's levels
- Include worked examples (2-3 per section)
- Provide practice exercises (5-8 per section)
- Use clear markdown formatting with admonitions
- Maintain encouraging, accessible tone

## Content Generation Guide

Before generating content for the chapters, lesson plans, quizzes, FAQ or other
student-facing text, read the [`CONTENT-GENERATION-GUIDE.md`](CONTENT-GENERATION-GUIDE.md)
file. It defines the book's learning mascot — **Kit the Otter** — along with
Kit's voice, the seven mascot admonition types, and the placement rules that
keep the mascot from being overused.

Note that the teacher guide, instructor guide, or other instructor-facing
content does not need to use the mascot described in CONTENT-GENERATION-GUIDE.md.

## Website

**Documentation**: https://dmccreary.github.io/ibook-skills/
**Repository**: https://github.com/dmccreary/ibook-skills

## Technology Stack

- **MkDocs** with **Material for MkDocs** theme - static site generation
- **p5.js** - interactive simulations (MicroSims)
- **Chart.js** - data visualization charts (pie, bar, line, etc.)
- **vis-network.js** - learning graph visualization
- **Mermaid** - diagrams from text (flowcharts, sequence diagrams)
- **Leaflet** - interactive maps
- **Python** - data processing scripts
- **GitHub Pages** - hosting
- **Bash** - utility scripts

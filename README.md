# Agent Skills for Intelligent Textbooks

[![MkDocs](https://img.shields.io/badge/Made%20with-MkDocs-526CFE?logo=materialformkdocs)](https://www.mkdocs.org/)
[![Material for MkDocs](https://img.shields.io/badge/Material%20for%20MkDocs-526CFE?logo=materialformkdocs)](https://squidfunk.github.io/mkdocs-material/)
[![GitHub Pages](https://img.shields.io/badge/View%20on-GitHub%20Pages-blue?logo=github)](https://dmccreary.github.io/ibook-skills/)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Multi--Platform-4A90D9)](https://github.com/dmccreary/ibook-skills)
[![p5.js](https://img.shields.io/badge/p5.js-ED225D?logo=p5.js&logoColor=white)](https://p5js.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## View the Live Site

Visit the interactive documentation at: [https://dmccreary.github.io/ibook-skills/](https://dmccreary.github.io/ibook-skills/)

## Overview

**Agent Skills for Intelligent Textbooks** is a portable, token-efficient library of AI agent skills for building interactive educational textbooks. The skills are written as plain-language markdown workflows (`SKILL.md` files), so they aren't locked to one vendor's assistant — the same skill set has been installed and run in **Claude Code, OpenAI Codex, Google Antigravity/Gemini, Cursor, Perplexity, and Hermes**. The repository's `CLAUDE.md` instructions file doubles as an `AGENTS.md` for tools that use that convention, and a single install script (`bk-install-skills`) symlinks the same skills into the skills directory of every agent present on the machine.

This project enables the creation of **Level 2+ intelligent textbooks** using MkDocs with the Material theme, incorporating learning graphs, concept dependency mapping, interactive p5.js simulations (MicroSims), and AI-assisted content generation. Every skill follows educational best practices including Bloom's Taxonomy (2001 revision) for learning outcomes, ISO 11179 standards for terminology definitions, and concept dependency graphs (DAGs) to ensure prerequisites are taught before they're used.

Whether you're an educator building course materials, a technical writer producing documentation, or a developer exploring educational technology, these agent skills provide a systematic, repeatable pipeline from a course description all the way to a published, interactive textbook — regardless of which AI coding agent you point at the repository.

## Site Status and Metrics

| Metric | Count |
|--------|-------|
| Concepts in Learning Graph | 570 |
| Chapters | 31 |
| Appendices | 3 |
| MicroSims | 94 |
| Glossary Terms | 570 |
| FAQ Questions | 66 |
| Diagrams | 25 |
| Equations | 131 |
| Total Words | 154,857 |
| Equivalent Pages | ~672 |

Chapter-level quizzes and curated references are actively being generated and are not yet complete across all 31 chapters.

**Skills Available:** 14 active skills (several are meta-skills that route to dozens of sub-workflows) covering learning graph generation, chapter content, MicroSims, glossaries, FAQs, quizzes, references, media, and publishing.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- An AI coding agent that supports agent skills or a similar convention (e.g. Claude Code, OpenAI Codex, Google Antigravity, Cursor)
- Basic familiarity with markdown and the command line

### Clone the Repository

```bash
git clone https://github.com/dmccreary/ibook-skills.git
cd ibook-skills
```

### Install Dependencies

This project uses MkDocs with the Material theme:

```bash
pip install mkdocs
pip install mkdocs-material
pip install pymdown-extensions
```

### Build and Serve Locally

Build the documentation site:

```bash
mkdocs build
```

Serve locally for development (with live reload):

```bash
mkdocs serve
```

Open your browser to `http://localhost:8000`

### Deploy to GitHub Pages

```bash
mkdocs gh-deploy
```

This will build the site and push it to the `gh-pages` branch.

### Installing the Skills for Your Agent

Set `BK_HOME` to the repository root, then run the installer for your platform:

```bash
export BK_HOME="$HOME/path/to/ibook-skills"

# Every agent present on this machine
$BK_HOME/scripts/bk-install-skills

# Or narrow it
$BK_HOME/scripts/bk-install-skills --only codex
$BK_HOME/scripts/bk-install-skills --list      # show agents and status
$BK_HOME/scripts/bk-install-skills --dry-run   # preview, change nothing
```

The script symlinks every active skill in `skills/` (any directory with a `SKILL.md`, which excludes `skills/archived/`) into the skills directory of each supported agent — Claude Code, OpenAI Codex, and Google Antigravity. Edits to a skill here are picked up immediately by every connected agent.

It installs to **all** agents by default rather than detecting the caller: the three are often used together, so a per-agent install silently leaves the others on a stale skill set. Agents that aren't installed on the machine are skipped; `--all` forces their directories to be created.

**List available skills:**

```bash
$BK_HOME/scripts/bk-list-skills
```

**Invoking a skill:** most agents pick up a skill automatically once the task matches its description. Where a tool supports explicit invocation, reference it by name, e.g. `Use the learning-graph-generator skill to create a concept graph for my course`.

### Using the Documentation Site

**Navigation:**

- Use the left sidebar to browse chapters and skill descriptions
- Click the search icon (🔍) to search all content
- The Learning Graph section shows concept dependencies and quality metrics

**Interactive MicroSims:**

- Found throughout the chapters and in the "MicroSims" section of the documentation
- Each simulation runs standalone in your browser
- Adjust parameters with sliders and interactive controls
- View source code and customize for your own use

**Customization:**

- Edit markdown files in `docs/` to modify content
- Modify `mkdocs.yml` to change site structure and navigation
- Add your own MicroSims in `docs/sims/[microsim-name]/`
- Customize theme colors and styles in `docs/css/extra.css`
- Create custom skills in `skills/[skill-name]/SKILL.md`

## Repository Structure

```
ibook-skills/
├── docs/                          # MkDocs documentation source
│   ├── chapters/                  # 31 chapters + appendices on building intelligent textbooks
│   │   ├── 01-foundations-ai-language-models/
│   │   │   └── index.md          # Chapter content
│   │   └── ...
│   ├── sims/                      # 94 interactive MicroSims (p5.js, Chart.js, vis-network, ...)
│   ├── learning-graph/            # Learning graph data, analysis, and book metrics
│   │   ├── concept-list.md       # 570 concepts enumerated
│   │   ├── learning-graph.csv    # Concept dependencies (DAG)
│   │   ├── learning-graph.json   # vis-network JSON format
│   │   ├── book-metrics.json     # Canonical book-wide metrics (source of truth)
│   │   └── quality-metrics.md    # Graph quality analysis
│   ├── glossary.md                # ISO 11179-compliant definitions (570 terms)
│   └── faq.md                     # Frequently asked questions (66 Q&A)
├── skills/                        # AI agent skill definitions
│   ├── learning-graph-generator/  # Generates 300-600 concept dependency graphs
│   ├── book-chapter-generator/    # Designs chapter structure from the learning graph
│   ├── chapter-content-generator/ # Generates chapter content and MicroSims
│   ├── glossary-generator/        # ISO 11179-compliant glossary
│   ├── faq-generator/             # FAQs from chapter content
│   ├── quiz-generator/            # Bloom's Taxonomy-aligned quizzes
│   ├── reference-generator/       # Curated per-chapter references
│   ├── microsim-generator/        # MicroSims across many JS libraries (meta-skill)
│   ├── microsim-utils/            # MicroSim QA and maintenance (meta-skill)
│   ├── book-installer/            # Project scaffold and infrastructure (meta-skill)
│   ├── book-media-generator/      # Slides, illustrations, audio (meta-skill)
│   ├── book-publisher/            # README, LinkedIn, press release (meta-skill)
│   └── archived/                  # Original single-purpose skills, consolidated into the meta-skills above
├── scripts/                       # Utility scripts (install, metrics, screenshots, ...)
│   ├── bk-install-skills          # Install skills for every agent present
│   ├── bk-install-skills-codex    # Deprecated shim -> --only codex
│   ├── bk-install-skills-antigravity # Deprecated shim -> --only antigravity
│   └── bk-list-skills             # List all active skills
├── commands/                      # Slash commands
├── mkdocs.yml                     # MkDocs configuration
├── CLAUDE.md                      # Agent instructions (also usable as AGENTS.md)
└── README.md                      # This file
```

## Reporting Issues

Found a bug, typo, or have a suggestion for improvement? Please report it:

[GitHub Issues](https://github.com/dmccreary/ibook-skills/issues)

When reporting issues, please include:

- Clear description of the problem or suggestion
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Screenshots or error messages (if applicable)
- Skill name and the AI agent/tool you were using (if skill-specific)
- Browser/environment details (for MicroSim issues)

## License

This work is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

**You are free to:**

- **Share** — Copy and redistribute the material in any medium or format
- **Adapt** — Remix, transform, and build upon the material

**Under the following terms:**

- **Attribution** — Give appropriate credit with a link to the original repository
- **NonCommercial** — No commercial use without explicit permission
- **ShareAlike** — Distribute your contributions under the same license

**Attribution Example:**

```
This work is based on "Agent Skills for Intelligent Textbooks" by Dan McCreary,
available at https://github.com/dmccreary/ibook-skills, licensed under CC BY-NC-SA 4.0.
```

See [license details](docs/license.md) for the full legal text.

## Acknowledgements

This project is built on the shoulders of giants in the open source community. We are deeply grateful to:

### Documentation and Build Tools

- **[MkDocs](https://www.mkdocs.org/)** - Fast, simple static site generator optimized for project documentation
- **[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)** - Beautiful, responsive Material Design theme with advanced features

### Interactive Visualizations and Creative Coding

- **[p5.js](https://p5js.org/)** - Creative coding library from NYU ITP for interactive educational simulations
- **[vis-network](https://visjs.org/)** - Network visualization library for learning graph exploration
- **[Chart.js](https://www.chartjs.org/)** - Interactive charts for data visualization
- **[Mermaid](https://mermaid.js.org/)** - Diagram and flowchart generation from text

### Python Ecosystem

- **[Python](https://www.python.org/)** community - Data processing, analysis, and automation tools
- **[PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/)** - Enhanced Markdown extensions

### Hosting and Deployment

- **[GitHub Pages](https://pages.github.com/)** - Free hosting for open source documentation projects
- **[GitHub](https://github.com/)** - Version control and collaboration platform

### Educational Standards and Frameworks

- **[Bloom's Taxonomy](https://en.wikipedia.org/wiki/Bloom%27s_taxonomy)** - Framework for categorizing cognitive learning objectives
- **[ISO 11179](https://www.iso.org/standard/50340.html)** - International standard for metadata registries (glossary definitions)
- **[Dublin Core](https://www.dublincore.org/)** - Metadata standards for educational resources

Special thanks to the educators, developers, and maintainers who contribute to making educational resources accessible, interactive, and open to all. Your work enables projects like this to exist and thrive.

## Contact

**Dan McCreary**

- LinkedIn: [linkedin.com/in/danmccreary](https://www.linkedin.com/in/danmccreary/)
- GitHub: [@dmccreary](https://github.com/dmccreary)

Questions, suggestions, or collaboration opportunities? Feel free to connect on LinkedIn or open an issue on GitHub. I'm particularly interested in:

- Feedback on skill effectiveness and quality across different AI agents
- Suggestions for new skills or features
- Collaboration on educational technology projects
- Use cases and success stories from educators

## How to Cite

If you use these agent skills in your research, teaching, or projects, please cite:

```
McCreary, D. (2024). Agent Skills for Intelligent Textbooks. GitHub.
https://github.com/dmccreary/ibook-skills
```

**BibTeX:**

```bibtex
@misc{mccreary2024agentskills,
  author = {McCreary, Dan},
  title = {Agent Skills for Intelligent Textbooks},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/dmccreary/ibook-skills},
  note = {A portable, multi-platform library of AI agent skills for creating intelligent educational content}
}
```

## Available Skills

This repository includes 14 active skills for intelligent textbook creation. Several are meta-skills that route to focused sub-workflows in a `references/` folder, which keeps the total under each platform's loaded-skills limit while still covering dozens of tasks.

### Content-Pipeline Skills

1. **course-description-analyzer** - Validates and enhances course descriptions
2. **learning-graph-generator** - Creates 300-600 concept dependency graphs (DAG structure)
3. **book-chapter-generator** - Designs chapter structure from the learning graph
4. **chapter-content-generator** - Generates chapter content, diagrams, and exercises
5. **glossary-generator** - Creates ISO 11179-compliant glossaries
6. **faq-generator** - Generates FAQs from chapter content and the learning graph
7. **quiz-generator** - Creates Bloom's Taxonomy-aligned quiz questions
8. **reference-generator** - Curates per-chapter academic references

### Meta-Skills (Routers)

9. **book-installer** - Project scaffolding and infrastructure: init a new textbook, install features (math, mascot, learning-graph viewer, Google Analytics, and more), generate book metrics
10. **microsim-generator** - MicroSims across p5.js, Chart.js, Plotly, Mermaid, vis-network, timelines, maps, and more
11. **microsim-utils** - MicroSim QA: standardization, screenshots, layout review, coverage reports
12. **book-media-generator** - Slide decks, illustrated stories, chapter images, and audio
13. **book-publisher** - README, LinkedIn posts/carousels, and press releases

### Standalone

14. **docx-to-web-publisher** - Converts .docx files into structured web pages

For detailed documentation on each skill, see the [skill descriptions](https://dmccreary.github.io/ibook-skills/skill-descriptions/) in the documentation site.

---

**Portable Agent Skills** | **Works with Claude Code, Codex, Antigravity/Gemini, Cursor, Perplexity, and Hermes** | **Open Educational Resources**

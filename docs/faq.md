# Using Claude Skills to Create Intelligent Textbooks FAQ

## Getting Started Questions

### What is this course about?

This course provides comprehensive training on leveraging Claude Skills to create intelligent, interactive textbooks that enhance learning through AI-assisted content generation. You'll learn the complete workflow from course conception through deployment, including creating learning graphs, generating glossaries, building interactive simulations (MicroSims), and publishing professional educational materials using MkDocs with the Material theme.

The course emphasizes practical, hands-on skills for educators, instructional designers, and content creators who want to harness the power of AI to produce high-quality educational materials efficiently. See the [course description](course-description.md) for complete details.

### Who is this course for?

This course is designed for **professional development** and targets educators, instructional designers, technical writers, and content creators who want to use AI tools to build intelligent textbooks. You should have a basic understanding of programming, familiarity with prompt engineering concepts, access to Anthropic Claude, and curiosity about using AI to build textbooks.

While technical background is helpful, the course focuses on practical skills rather than deep programming knowledge.

### What are the prerequisites for this course?

Before starting this course, you should have:

- **Basic programming understanding**: Familiarity with concepts like variables, functions, and control flow
- **Prompt engineering basics**: Understanding how to write effective prompts for AI systems
- **Anthropic Claude access**: An active Claude Pro account for extended usage limits
- **Curiosity and motivation**: Willingness to explore AI-assisted educational content creation

See the [course description prerequisites section](course-description.md#prerequisites) for details.

### How do I install Claude Skills on my computer?

Installing Claude Skills involves two steps:

1. **Clone the repository**: Use `git clone https://github.com/dmccreary/ibook-skills.git` to download the skills
2. **Run the installation script**: Navigate to the `scripts/` directory and run `./install-ibook-skills.sh`

This creates symbolic links from your `~/.claude/skills/` directory to the cloned skills, making them available across all your projects. For project-specific installation, modify the script to point to your project's `.claude/skills/` directory instead.

**Example**: After installation, you can invoke skills using slash commands like `/skill learning-graph-generator`.

See the [getting started guide](getting-started.md) for detailed installation instructions.

### What will I be able to do after completing this course?

After completing this course, you'll be able to:

- **Create intelligent textbooks** from scratch using Claude Skills and MkDocs
- **Generate learning graphs** with 300-600 concepts and dependency relationships
- **Build interactive simulations** (MicroSims) using p5.js for educational visualization
- **Automate content generation** for chapters, glossaries, FAQs, and quizzes
- **Apply Bloom's Taxonomy** to create learning outcomes at all cognitive levels
- **Publish professional educational materials** using GitHub Pages

The capstone project involves designing and implementing a complete intelligent textbook for a subject of your choice, demonstrating mastery of the entire workflow.

### How long does this course take to complete?

The course consists of 13 chapters covering topics from AI fundamentals to deployment workflows. The time commitment varies based on your background and learning pace, but most learners should expect:

- **Core content**: 20-30 hours to work through all chapters
- **Hands-on practice**: 15-25 hours for exercises and skill experimentation
- **Capstone project**: 10-20 hours to create a complete intelligent textbook

Total estimated time: **45-75 hours** for thorough completion including the capstone project. You can work at your own pace, and the modular structure allows you to focus on specific topics as needed.

### What tools do I need to get started?

To work through this course effectively, you'll need:

- **Claude Pro account**: For extended usage limits and access to Claude Code
- **Visual Studio Code** (or similar editor): For content development and markdown editing
- **Git**: For version control and content management
- **Python 3.x**: For running learning graph processing scripts (pip for package management)
- **Terminal/command-line access**: For running shell scripts and commands
- **Web browser**: For testing MkDocs sites locally and accessing documentation

All tools are free except the Claude Pro subscription. Installation instructions are provided in [Chapter 2](chapters/02-getting-started-ibook-skills/index.md) and the [getting started guide](getting-started.md).

### Do I need to know Python or JavaScript?

Not extensively! While the course uses Python scripts for processing learning graphs and JavaScript for creating MicroSims, you don't need to be an expert programmer:

- **Python**: The course provides pre-built scripts (`analyze-graph.py`, `csv-to-json.py`, etc.) that you run as-is. Basic understanding of running Python commands is helpful.
- **JavaScript/p5.js**: The microsim-p5 skill generates simulation code for you. Understanding basic JavaScript helps customize simulations, but isn't required for core functionality.

The focus is on **using** these tools through Claude Skills rather than writing code from scratch. See [Chapter 9](chapters/09-ibook-skills-architecture-development/index.md) for more on skill architecture.

### How do I list the skills I have installed?

There are two ways to list your installed skills:

1. **Ask Claude directly**: Type "What skills do you know about?" — skill names and descriptions are injected into context at session start, so no lookup is needed.
2. **Run `bk-list-skills`**: prints every installed skill from the command line.

`bk-list-skills` provides formatted output organized by category, showing all user and project-specific skills.

!!! note "The `/skills` slash command was removed"
    Earlier versions shipped a `/skills` command. It has been retired — use
    `bk-list-skills` or just ask Claude. `/ibook` is now the only slash
    command this repository installs.

**Example output**:
```
Educational Content Creation:
  - faq-generator (user) - Generates FAQs from course content
  - glossary-generator (user) - Creates ISO 11179-compliant glossaries
  - learning-graph-generator (user) - Generates 300-600 concept learning graphs
```

See the [getting started guide](getting-started.md#testing-your-skill-list) for complete instructions.

### What is the difference between a Claude Skill and a Claude Command?

**Claude Skills** are autonomous agents with full workflow instructions defined in SKILL.md files. They can use multiple tools, make decisions, and execute complex multi-step processes. Skills are invoked with `/skill [name]` and run specialized workflows like generating learning graphs or creating glossaries.

**Claude Commands** are simpler prompt expansions defined in markdown files. They expand text instructions that Claude then interprets, similar to custom shortcuts. Commands are invoked with `/[name]` and are useful for repetitive prompts.

**Example**: The `learning-graph-generator` is a skill that autonomously generates 300-600 concepts, validates dependencies, and creates visualizations. A command might simply instruct Claude to "analyze this learning graph quality."

See [Chapter 9](chapters/09-ibook-skills-architecture-development/index.md) for detailed architecture information.

### How do I update my skills to the latest version?

Since the skills are installed via symbolic links to a Git repository, updating is simple:

1. Navigate to your cloned repository: `cd ~/projects/ibook-skills`
2. Pull the latest changes: `git pull`
3. Skills are automatically updated via symlinks

No need to reinstall or recreate links. The symbolic link structure means any changes in the repository immediately reflect in your `~/.claude/skills/` directory.

**Tip**: Run `git pull` regularly to get new features, bug fixes, and additional skills as they're released.

See the [getting started guide](getting-started.md#getting-updates) for more details.

## Core Concepts

### What is an intelligent textbook?

An intelligent textbook is an educational resource that goes beyond static text and images to provide interactive, adaptive, and AI-enhanced learning experiences. The course framework defines five levels of intelligence:

- **Level 1**: Static content (traditional PDFs), no interactivity
- **Level 2**: Interactive content — hyperlinks, embedded videos, quizzes, and MicroSims
- **Level 3**: Adaptive content that responds to learner progress via concept-graph traversal
- **Level 4**: Chatbot integration — an LLM-powered tutoring assistant
- **Level 5**: Autonomous AI — fully autonomous, real-time customized lesson generation

This course primarily targets **Level 2** textbooks using MkDocs Material theme, with MicroSims, quizzes, and interactive elements. See [Chapter 1](chapters/01-foundations-ai-language-models/index.md) for the complete intelligence framework.

### What is a learning graph?

A learning graph is a structured representation of knowledge that maps concepts and their prerequisite relationships in a course or subject domain. Each concept is a node, and directed edges represent dependencies (concept A must be learned before concept B).

**Key characteristics**:

- **300-600 concepts**: Target range for comprehensive course coverage
- **Directed Acyclic Graph (DAG)**: Dependencies flow in one direction with no circular loops
- **Taxonomy categories**: Concepts grouped by theme (e.g., BASIC, ADVANCED, TOOLS)
- **Prerequisite tracking**: Ensures proper learning sequence

**Example**: The concept "Git Commit Command" depends on "Git Add Command" and "Git Repository Structure," ensuring learners understand prerequisites before advancing.

Learning graphs serve as roadmaps guiding students through optimal learning pathways. See [Chapter 4](chapters/04-intro-learning-graphs/index.md) for comprehensive coverage.

### What is a Claude Skill?

A Claude Skill is an autonomous agent defined by a SKILL.md file that automates specific aspects of intelligent textbook creation. Skills contain:

- **YAML frontmatter**: Metadata including name, description, license, and allowed tools
- **Workflow instructions**: Step-by-step processes Claude executes autonomously
- **Supporting assets**: Python scripts, templates, and reference documentation

**Example skills**:

- `learning-graph-generator`: Creates 300-600 concept dependency graphs
- `glossary-generator`: Produces ISO 11179-compliant term definitions
- `microsim-p5`: Builds interactive p5.js educational simulations

Skills are installed in `~/.claude/skills/` and invoked with the Skill tool or `/skill [name]` command. See [Chapter 2](chapters/02-getting-started-ibook-skills/index.md) and [Chapter 9](chapters/09-ibook-skills-architecture-development/index.md) for details.

### What is Bloom's Taxonomy and why is it important?

Bloom's Taxonomy is an educational framework that classifies learning objectives into six cognitive levels, from basic recall to creative synthesis. The 2001 revision uses these levels:

1. **Remember** (Red): Retrieve, recognize, recall knowledge
2. **Understand** (Orange): Construct meaning, explain, summarize
3. **Apply** (Yellow): Use procedures in new situations
4. **Analyze** (Green): Break into parts, examine relationships
5. **Evaluate** (Blue): Make judgments based on criteria
6. **Create** (Purple): Produce original work, design solutions

**Importance**: Well-designed educational content addresses all cognitive levels, ensuring students develop both foundational knowledge and higher-order thinking skills. This course uses Bloom's Taxonomy to structure learning outcomes, quiz questions, and content generation.

See [Chapter 3](chapters/03-course-design-educational-theory/index.md) for complete coverage of educational theory.

### How does a learning graph guide student learning?

A learning graph provides a visual and structural roadmap that shows learners:

- **Where to start**: Foundational concepts with no prerequisites appear first
- **What comes next**: Prerequisites must be mastered before advancing to dependent concepts
- **How concepts connect**: Understanding relationships deepens comprehension
- **Alternative pathways**: Multiple routes may exist through the material

**Example**: A student wanting to learn "MicroSim Creation" can trace backwards through the graph to see they need "p5.js Library," "JavaScript Basics," and "HTML Structure" first.

The graph also helps instructors identify knowledge gaps, optimize chapter sequencing, and ensure comprehensive topic coverage. Interactive graph viewers let students explore the concept network visually. See [Chapter 4](chapters/04-intro-learning-graphs/index.md) for more on learning pathways.

### What is MkDocs and why use it for textbooks?

MkDocs is a fast, simple static site generator designed for building project documentation from markdown files. With the **Material for MkDocs** theme, it becomes an excellent platform for intelligent textbooks because it provides:

- **Clean, responsive design**: Professional appearance on all devices
- **Navigation features**: Table of contents, search, breadcrumbs, and page navigation
- **Markdown support**: Easy content authoring with extensions for admonitions, code highlighting, and tables
- **Customization**: Themes, colors, logos, and CSS customization
- **GitHub Pages integration**: Free hosting and automatic deployment

**Example**: This very course website is built with MkDocs Material, demonstrating the platform's capabilities for educational content.

MkDocs targets Level 2 intelligent textbooks (hyperlinked navigation) with support for Level 3 features through embedded MicroSims and interactive elements. See [Chapter 8](chapters/08-mkdocs-platform-documentation/index.md).

### What is a MicroSim?

A MicroSim is a focused, interactive educational simulation built with p5.js that helps students visualize and explore a single concept or relationship. Each MicroSim:

- **Targets one concept**: Focused learning objective
- **Provides interactivity**: Sliders, buttons, and controls for exploration
- **Uses seeded randomness**: Reproducible results for consistent learning
- **Embeds in textbooks**: iframe integration with documentation

**Example**: A "Concept Length Histogram" MicroSim visualizes the distribution of concept label lengths in a learning graph, helping students understand data visualization and statistical distributions.

MicroSims are stored in `docs/sims/[name]/` directories with `main.html` (the simulation) and `index.md` (documentation). The microsim-p5 skill automates MicroSim creation. See [Chapter 12](chapters/12-interactive-elements-microsims/index.md) for detailed coverage.

### What is ISO 11179 and why does it matter for glossaries?

ISO 11179 is an international standard for metadata registries that defines principles for creating precise, unambiguous term definitions. Glossary definitions following ISO 11179 must be:

- **Precise**: Exact meaning without ambiguity
- **Concise**: Minimal words while conveying full meaning
- **Distinct**: Clearly differentiated from related terms
- **Non-circular**: Don't define terms using themselves
- **Free of business rules**: No implementation details or procedures

**Example - Good**: "Directed Acyclic Graph (DAG): A graph structure where edges have direction and no path returns to a starting node."

**Example - Bad**: "DAG: When you create a graph that doesn't have cycles" (circular, imprecise, procedural)

Following ISO 11179 ensures glossary terms are professional, clear, and useful for learning. The glossary-generator skill automatically creates ISO 11179-compliant definitions. See the [glossary](glossary.md) for examples.

### What are the five levels of textbook intelligence?

The five-level intelligence framework classifies textbooks by their interactive and adaptive capabilities:

**Level 1 - Static Content**: Traditional PDFs with fixed text and images, no interactivity

**Level 2 - Interactive Content**: Hyperlinks, embedded videos, quizzes, MicroSims, and a searchable glossary

**Level 3 - Adaptive Content**: Personalization based on learner progress via concept-graph traversal

**Level 4 - Chatbot Integration**: An LLM-powered tutoring assistant, often built on GraphRAG, that answers questions in real time

**Level 5 - Autonomous AI**: A largely aspirational level where a system deeply understands each reader's knowledge state and generates fully customized lessons in real time

This course primarily targets **Level 2** through MicroSims, quizzes, and interactive visualizations. See [Chapter 1](chapters/01-foundations-ai-language-models/index.md) for the complete framework.

### What is the difference between concepts and topics?

**Concepts** are atomic, indivisible ideas that represent single learning units in a learning graph. Each concept should be granular enough to be taught and assessed independently.

**Topics** are broader themes or subject areas that encompass multiple concepts. Topics often become chapters or sections in textbooks.

**Example**:

- **Topic**: "Version Control with Git"
- **Concepts**: "Git Repository Structure," "Git Status Command," "Git Add Command," "Git Commit Command," "Git Push Command"

A single topic might contain 10-20 concepts in the learning graph. When generating learning graphs, focus on identifying atomic concepts rather than broad topics—the learning-graph-generator skill helps with this granularity. See [Chapter 5](chapters/05-concept-enumeration-dependencies/index.md).

### What is a Directed Acyclic Graph (DAG)?

A Directed Acyclic Graph (DAG) is a graph structure where:

- **Directed**: Edges have direction (concept A → concept B means A is a prerequisite for B)
- **Acyclic**: No path through the graph returns to a starting node (no circular dependencies)

**Why DAGs matter for learning graphs**: Prerequisites must follow a logical sequence. If Concept A requires Concept B, and Concept B requires Concept C, then Concept C cannot require Concept A (that would create a cycle).

**Example violation**: "Git Basics" → "Git Branching" → "Git Basics" creates a cycle where neither can be learned first.

The `analyze-graph.py` script validates DAG structure and detects circular dependencies. See [Chapter 6](chapters/06-learning-graph-quality-validation/index.md) for quality validation details.

### What is concept dependency mapping?

Concept dependency mapping is the process of identifying prerequisite relationships between concepts in a learning graph. For each concept, you specify which other concepts must be learned first.

Dependencies are encoded in CSV format with pipe-delimited ConceptIDs:

```csv
ConceptID,ConceptLabel,Dependencies,TaxonomyID
1,Git Basics,,TOOLS
2,Git Repository Structure,1,TOOLS
3,Git Commit Command,1|2,TOOLS
```

Concept 3 depends on both concepts 1 and 2, meaning students should understand "Git Basics" and "Git Repository Structure" before learning "Git Commit Command."

Proper dependency mapping ensures logical learning sequences and prevents students from encountering concepts before they have necessary background knowledge. See [Chapter 5](chapters/05-concept-enumeration-dependencies/index.md).

### How many concepts should a learning graph have?

The learning-graph-generator skill supports **300-600 concepts** for comprehensive courses, based on educational research suggesting this range provides optimal granularity for:

- **Breadth**: Covering all major topics and subtopics
- **Depth**: Atomic concepts that can be individually taught and assessed
- **Manageability**: Large enough to be thorough, small enough to comprehend as a whole

You can adjust this number based on course scope:

- **Introductory courses**: 100-200 concepts
- **Comprehensive courses**: 300-400 concepts
- **Advanced/graduate courses**: 400-600 concepts

More concepts provide finer granularity but increase complexity. The key is ensuring each concept is atomic (indivisible) and meaningful as a learning unit. See [Chapter 5](chapters/05-concept-enumeration-dependencies/index.md).

### What is taxonomy categorization in learning graphs?

Taxonomy categorization groups related concepts into thematic categories, helping organize and visualize the learning graph. Common categories include:

- **FOUND**: Foundational prerequisites
- **BASIC**: Core fundamental concepts
- **INTER**: Intermediate topics
- **ADVNC**: Advanced concepts
- **TOOLS**: Software tools and technologies
- **SKILL**: Practical skills and techniques

Each concept receives a TaxonomyID (3-5 letter abbreviation) in the learning graph CSV. These categories:

- **Aid visualization**: Color-coding concepts by category in graph viewers
- **Balance content**: Ensuring no category is over-represented (avoid >30% in one category)
- **Guide organization**: Informing chapter structure and content progression

See [Chapter 7](chapters/07-taxonomy-data-formats/index.md) for complete taxonomy information.

### What makes a high-quality learning graph?

A high-quality learning graph scores **70+/100** on the quality metrics generated by `analyze-graph.py`. Key indicators include:

**Structure (30 points)**:

- Valid DAG (no circular dependencies): mandatory
- No self-dependencies: mandatory
- Connected graph (no isolated subgraphs): 10 points

**Connectivity (30 points)**:

- Foundational concepts (zero dependencies): 10 points
- Average 2-4 dependencies per concept: 10 points
- No terminal nodes (concepts nothing depends on): 10 points

**Balance (20 points)**:

- Taxonomy distribution (no category >30%): 10 points
- Reasonable maximum chain length: 10 points

**Completeness (20 points)**:

- 200 concepts generated: 10 points
- All concepts have labels <32 characters: 10 points

The quality report identifies specific issues and recommendations for improvement. See [Chapter 6](chapters/06-learning-graph-quality-validation/index.md).

## Technical Detail Questions

### What file format is used for learning graphs?

Learning graphs use **CSV (Comma-Separated Values)** format with four columns:

```csv
ConceptID,ConceptLabel,Dependencies,TaxonomyID
1,Introduction to Programming,,FOUND
2,Variables and Data Types,1,BASIC
3,Control Flow,1|2,BASIC
```

**Field descriptions**:

- **ConceptID**: Integer (1-200), unique identifier
- **ConceptLabel**: Title Case, max 32 characters, human-readable name
- **Dependencies**: Pipe-delimited list of ConceptIDs (empty for foundational concepts)
- **TaxonomyID**: 3-5 letter category abbreviation

This format is human-readable, easy to edit in spreadsheet software, and processable by Python scripts. The `csv-to-json.py` script converts CSV to vis-network JSON for interactive visualization. See [Chapter 7](chapters/07-taxonomy-data-formats/index.md).

### What Python scripts are used for learning graph processing?

The learning-graph-generator skill includes four main Python scripts in `docs/learning-graph/`:

**analyze-graph.py**: Validates DAG structure, detects circular dependencies, calculates quality metrics, generates quality report markdown

**csv-to-json.py**: Converts learning graph CSV to vis-network JSON format for interactive visualization

**add-taxonomy.py**: Adds TaxonomyID column to learning graph CSV if missing

**taxonomy-distribution.py**: Generates taxonomy distribution report showing concept counts by category

All scripts are run from the `docs/learning-graph/` directory after the learning graph CSV is generated. They require Python 3.x and standard libraries (no pip packages needed for basic functionality). See [Chapter 6](chapters/06-learning-graph-quality-validation/index.md) for usage examples.

### How do I run the learning graph validation scripts?

After generating a learning graph, navigate to the `docs/learning-graph/` directory and run:

```bash
cd docs/learning-graph
python analyze-graph.py learning-graph.csv quality-metrics.md
python csv-to-json.py learning-graph.csv learning-graph.json
python taxonomy-distribution.py learning-graph.csv taxonomy-distribution.md
```

**Expected outputs**:

- `quality-metrics.md`: Quality score, validation results, recommendations
- `learning-graph.json`: vis-network format for interactive graph viewer
- `taxonomy-distribution.md`: Concept count by category with distribution chart

These reports help assess graph quality and identify improvements needed. Always verify `learning-graph.json` is valid JSON before using in visualizations. See [Chapter 6](chapters/06-learning-graph-quality-validation/index.md).

### What is vis-network JSON format?

vis-network is a JavaScript library for interactive graph visualization. The format required by vis-network includes:

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

**Structure**:

- **nodes**: Array of concepts with id, label, and group (taxonomy category)
- **edges**: Array of dependency relationships with from (prerequisite) and to (dependent concept)

The `csv-to-json.py` script automatically converts learning graph CSV to this format. The vis-network library then renders an interactive, draggable graph with color-coded nodes by taxonomy category. See [Chapter 7](chapters/07-taxonomy-data-formats/index.md).

### What is YAML frontmatter in skill definitions?

YAML frontmatter is metadata at the beginning of SKILL.md files, enclosed in `---` delimiters, that defines skill properties:

```yaml
---
name: learning-graph-generator
description: Generates a comprehensive learning graph with 200 concepts
license: Apache-2.0
allowed-tools:
  - Read
  - Write
  - Bash
---
```

**Fields**:

- **name**: Skill identifier (matches directory name)
- **description**: Brief explanation of skill purpose
- **license**: Software license (typically Apache-2.0 or MIT)
- **allowed-tools**: Optional list of Claude Code tools the skill can use

YAML frontmatter is a standard way to add metadata to markdown files, widely used in static site generators and documentation tools. See [Chapter 9](chapters/09-ibook-skills-architecture-development/index.md).

### How do I customize MkDocs theme colors?

MkDocs Material theme allows color customization through CSS and configuration:

**Method 1 - Configuration (mkdocs.yml)**:

```yaml
theme:
  palette:
    primary: 'indigo'
    accent: 'orange'
```

**Method 2 - Custom CSS**:

Create `docs/css/extra.css` and override Material theme variables:

```css
:root {
  --md-primary-fg-color: #DA7857;  /* Anthropic brown */
  --md-accent-fg-color: #FF6F00;   /* Orange accent */
}
```

Reference the custom CSS in `mkdocs.yml`:

```yaml
extra_css:
  - css/extra.css
```

This course website uses custom CSS to apply Anthropic brand colors (RGB: 218, 120, 87). See [Chapter 8](chapters/08-mkdocs-platform-documentation/index.md) for complete styling information.

### What markdown extensions does MkDocs Material support?

MkDocs Material supports many useful markdown extensions for educational content:

**admonition**: Callout boxes for notes, warnings, tips
**pymdownx.details**: Collapsible sections
**pymdownx.superfences**: Enhanced code blocks with syntax highlighting
**pymdownx.tabbed**: Tabbed content sections
**attr_list**: Add CSS classes and attributes to elements
**md_in_html**: Use markdown inside HTML blocks

Enable extensions in `mkdocs.yml`:

```yaml
markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - attr_list
```

**Example admonition**:
```markdown
!!! note "Important Concept"
    This creates a blue callout box highlighting key information.
```

See the [MkDocs Material documentation](https://squidfunk.github.io/mkdocs-material/reference/) and [Chapter 8](chapters/08-mkdocs-platform-documentation/index.md).

### How do I embed a MicroSim in a textbook page?

MicroSims are embedded using HTML iframes in markdown files. Each MicroSim has:

1. **main.html**: Standalone p5.js simulation in `docs/sims/[name]/`
2. **index.md**: Documentation page with iframe embed

**Example embedding**:

```html
<iframe src="../../sims/concept-length-histogram/main.html"
        width="100%"
        height="600px"
        frameborder="0">
</iframe>
```

The iframe loads the simulation while the surrounding markdown provides context, instructions, and learning objectives. The microsim-p5 skill automatically generates both files with proper structure. See [Chapter 12](chapters/12-interactive-elements-microsims/index.md) for MicroSim creation details.

### What is Dublin Core metadata?

Dublin Core is a standardized set of metadata elements for describing digital resources, widely used in libraries and archives. The 15 core elements include:

**Key fields for learning graphs**:

- **Title**: Name of the learning graph
- **Description**: Brief explanation of content
- **Creator**: Author or institution
- **Date**: Creation or modification date
- **Format**: File format (e.g., "text/csv", "application/json")
- **License**: Usage rights (e.g., "CC BY 4.0")

Dublin Core metadata appears in the vis-network JSON format for learning graphs, providing standardized documentation. This helps with content discovery, reusability, and academic citation. See [Chapter 7](chapters/07-taxonomy-data-formats/index.md).

### How do I configure navigation in MkDocs?

Navigation structure is defined in the `nav:` section of `mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - Chapters:
    - Overview: chapters/index.md
    - Chapter 1: chapters/01-intro/index.md
    - Chapter 2: chapters/02-skills/index.md
  - Glossary: glossary.md
```

**Features**:

- Nested structure creates dropdown menus
- Order determines menu appearance
- Section names (before colons) appear in navigation
- File paths are relative to `docs/`

After adding any new markdown file to `docs/`, update the `nav:` section so it appears in site navigation. MkDocs Material provides breadcrumbs and previous/next navigation automatically. See [Chapter 8](chapters/08-mkdocs-platform-documentation/index.md).

### What permissions does Claude Code need for skills?

Claude Code has strict default permissions that prompt for approval on every file read/write. For skill-based textbook development, recommended permissions in `.claude/config.json`:

```json
{
  "permissions": {
    "allow": [
      "Skill(*)",
      "Bash(*:*)",
      "FileSystem(read:./**/*.*,write:./**/*.*)"
    ],
    "deny": [],
    "ask": []
  }
}
```

**Explanation**:

- **Skill(*)**: Allow all skill invocations
- **Bash(*:*)**: Allow all bash commands
- **FileSystem(read:./**/*.*,write:./**/*.***: Allow reading/writing all files in project directory

Only use permissive settings in Git-tracked projects where changes can be reverted. See the [getting started guide](getting-started.md) for GitHub setup.

### How do I deploy my textbook to GitHub Pages?

MkDocs makes GitHub Pages deployment simple:

**One-time setup**:

1. Create GitHub repository for your textbook
2. Push content to main branch
3. Ensure `mkdocs.yml` has correct `site_url` and `repo_url`

**Deploy**:

```bash
mkdocs gh-deploy
```

This builds the site and pushes to the `gh-pages` branch automatically. GitHub Pages serves the content at `https://[username].github.io/[repo-name]/`.

**Continuous deployment**: Set up GitHub Actions to automatically deploy on push to main branch. See [Chapter 13](chapters/13-dev-tools-version-control-deployment/index.md) for complete deployment workflows.

### What is seeded randomness in MicroSims?

Seeded randomness means using a fixed random seed so that "random" behaviors are reproducible. In p5.js:

```javascript
function setup() {
  randomSeed(42);  // Fixed seed
  // Now random() produces same sequence every time
  let x = random(100);  // Always generates same value
}
```

**Benefits for education**:

- **Reproducibility**: Students see same visualization on reload
- **Consistency**: Discussion and documentation reference specific outputs
- **Debugging**: Easier to identify and fix issues

MicroSims use seeded randomness by default, with optional controls to change the seed for exploration. See [Chapter 12](chapters/12-interactive-elements-microsims/index.md) for MicroSim design patterns.

## Common Challenges

### Why am I getting circular dependency errors in my learning graph?

Circular dependencies occur when concept prerequisites form a cycle, making it impossible to determine learning order. Common causes:

**Reciprocal dependencies**: Concept A depends on B, and B depends on A
**Indirect cycles**: A → B → C → A creates a longer cycle
**Self-dependencies**: A concept listed as its own prerequisite

**How to fix**:

1. Run `analyze-graph.py` to identify the cycle
2. Review the concepts in the cycle to determine true prerequisite relationships
3. Break the cycle by removing or reordering one dependency
4. Consider splitting overly broad concepts into smaller atomic units

**Example**: If "Git Basics" and "Git Repository Structure" depend on each other, split into "Git Introduction" → "Git Repository Structure" → "Git Basic Commands". See [Chapter 6](chapters/06-learning-graph-quality-validation/index.md).

### My learning graph has terminal nodes. What does this mean?

Terminal nodes are concepts that nothing depends on—they have no outgoing edges (outdegree of zero). While not errors, many terminal nodes suggest:

**Missing dependencies**: Later concepts should build on these but don't
**Over-granularity**: Concepts too specific to be prerequisites
**Incomplete graph**: Advanced topics not yet added

Note: Terminal nodes are valid and expected in learning graphs (e.g., advanced capstone topics). They differ from orphaned nodes, which have no inbound AND no outbound edges (completely disconnected from the graph) and indicate a structural problem.

**How to fix**:

1. Review the quality metrics report for the list of terminal nodes
2. Identify which concepts should logically depend on these terminal nodes
3. Add dependency relationships to integrate terminal nodes into the graph
4. Consider whether very specific concepts should be merged into broader ones

**Acceptable terminal nodes**: Advanced capstone topics, specialized optional topics, or leaf concepts like specific tool configurations. Target: <10% terminal nodes. See [Chapter 6](chapters/06-learning-graph-quality-validation/index.md).

### Claude Code keeps asking for permissions. How do I fix this?

The default permission model requires approval for every file operation. To allow skills to work autonomously:

**Create `.claude/config.json` in your project**:

```json
{
  "permissions": {
    "allow": [
      "Skill(*)",
      "Bash(*:*)",
      "FileSystem(read:./**/*.*,write:./**/*.*)"
    ],
    "deny": [],
    "ask": []
  }
}
```

**Security note**: Only use permissive settings in Git-tracked directories where you can review and revert changes. Never use `allow: ["*"]` outside controlled environments.

After creating the config, restart Claude Code to apply permissions. See the [getting started guide](getting-started.md#permissions) for detailed permission configuration.

### How do I fix "module not found" errors when running Python scripts?

Python "module not found" errors typically mean missing dependencies. For learning graph scripts:

**Check Python version**: Scripts require Python 3.x
```bash
python --version  # Should show 3.x
```

**Install required packages** (if needed):
```bash
pip install pandas numpy  # For advanced analysis
```

**Run from correct directory**: Scripts expect to be run from `docs/learning-graph/`
```bash
cd docs/learning-graph
python analyze-graph.py learning-graph.csv quality-metrics.md
```

Most basic scripts use only Python standard library. If you encounter import errors, check the script's requirements or install packages individually. See [Chapter 6](chapters/06-learning-graph-quality-validation/index.md).

### Why isn't my new page showing up in the MkDocs navigation?

MkDocs only displays pages explicitly listed in the `nav:` section of `mkdocs.yml`. After creating any new markdown file:

1. Open `mkdocs.yml`
2. Find the appropriate section in `nav:`
3. Add your new page with label and path:

```yaml
nav:
  - Learning Graph:
    - Introduction: learning-graph/index.md
    - Your New Page: learning-graph/new-page.md  # Add this
```

4. Save and rebuild: `mkdocs serve` to test locally

**Note**: Files not in `nav:` are still built and accessible by direct URL, but won't appear in menus or navigation. See [Chapter 8](chapters/08-mkdocs-platform-documentation/index.md).

### My learning graph quality score is low. How do I improve it?

Low quality scores (<70/100) indicate structural or balance issues. Check the quality metrics report for specific problems:

**Circular dependencies (mandatory fix)**:

- Run `analyze-graph.py` to identify cycles
- Break cycles by removing or reordering dependencies

**Low connectivity (<2 avg dependencies)**:

- Add more prerequisite relationships
- Connect isolated concepts to the main graph

**Taxonomy imbalance (>30% in one category)**:

- Review over-represented categories
- Recategorize concepts for better distribution

**Too many terminal nodes (>20%)**:

- Add dependencies for terminal concepts
- Merge overly specific concepts

**Example improvement path**: A graph scoring 55/100 with 40% terminal nodes and taxonomy imbalance should first connect terminal concepts to reduce that to <10%, then rebalance taxonomy distribution. See [Chapter 6](chapters/06-learning-graph-quality-validation/index.md).

### How do I handle Claude token limits during content generation?

Claude Pro accounts have token limits within 4-hour usage windows. For long textbook generation sessions:

**Strategies to optimize usage**:

1. **Generate content incrementally**: Create 1-2 chapters at a time rather than entire textbook
2. **Use targeted skills**: Invoke specific skills (glossary, FAQ) rather than the full intelligent-textbook workflow
3. **Split large files**: Break chapter content into smaller sections if hitting limits
4. **Monitor usage**: Track how many skills you've run in the current window
5. **Plan generation sessions**: Space intensive tasks across multiple days

**If you hit limits**: Wait for the 4-hour window to reset, then continue. The course content discusses token management strategies and optimization techniques. See [Chapter 2](chapters/02-getting-started-ibook-skills/index.md) and the [usage limits guide](claude-usage-limits.md).

### Why is my MicroSim not displaying correctly?

Common MicroSim display issues and solutions:

**Blank iframe**:

- Check file path in iframe src (should be relative: `../../sims/[name]/main.html`)
- Verify `main.html` exists in correct location
- Open browser console for JavaScript errors

**p5.js not loading**:

- Ensure p5.js CDN link is in `main.html`:
  ```html
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
  ```

**Layout issues**:

- Adjust iframe width/height attributes
- Check canvas size in `createCanvas(width, height)`
- Test standalone `main.html` file directly in browser

**Controls not working**:

- Verify slider/button event handlers are properly attached
- Check browser console for JavaScript errors

See [Chapter 12](chapters/12-interactive-elements-microsims/index.md) for MicroSim debugging and best practices.

### How do I fix Git merge conflicts in markdown files?

Git merge conflicts occur when the same lines are modified in different branches. For markdown content:

**Identify conflicts**:
```bash
git status  # Shows conflicted files
```

**Open conflicted file** - look for conflict markers:
```markdown
<<<<<<< HEAD
Your current content
=======
Incoming content
>>>>>>> branch-name
```

**Resolve manually**:

1. Decide which content to keep (or combine both)
2. Remove conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
3. Save the file

**Complete merge**:
```bash
git add resolved-file.md
git commit -m "Resolved merge conflict in chapter 3"
```

**Prevention**: Coordinate with collaborators on which files to edit, or work on different chapters/sections simultaneously. See [Chapter 13](chapters/13-dev-tools-version-control-deployment/index.md).

## Best Practice Questions

### What's the recommended workflow for creating a new intelligent textbook?

The optimal workflow follows the intelligent-textbook skill's 12-step process:

**Phase 1 - Foundation (Steps 1-3)**:

1. Develop course description with Bloom's outcomes
2. Run course-description-analyzer skill to validate (score >70)
3. Generate 200-concept learning graph with learning-graph-generator skill

**Phase 2 - Structure (Steps 4-6)**:

4. Validate learning graph quality (analyze-graph.py)
5. Add taxonomy categorization
6. Create chapter structure with book-chapter-generator skill

**Phase 3 - Content (Steps 7-9)**:

7. Generate chapter content with chapter-content-generator skill
8. Create glossary with glossary-generator skill
9. Build MicroSims with microsim-p5 skill

**Phase 4 - Resources (Steps 10-11)**:

10. Generate FAQ with faq-generator skill
11. Create quizzes with quiz-generator skill

**Phase 5 - Publish (Step 12)**:

12. Deploy to GitHub Pages with `mkdocs gh-deploy`

This sequence ensures each step builds on previous work. See [Chapter 10](chapters/10-content-creation-workflows/index.md) for detailed workflow guidance.

### How should I structure chapters in my textbook?

Effective chapter structure follows pedagogical best practices and learning graph dependencies:

**Chapter components**:

- **Introduction**: Overview and learning objectives (2-3 paragraphs)
- **Prerequisites**: Required prior knowledge with links to prerequisite concepts
- **Core content**: 3-7 major sections covering key concepts
- **Worked examples**: 2-3 detailed examples demonstrating concepts
- **Practice exercises**: 5-8 exercises at varying Bloom's levels
- **Summary**: Key takeaways (bullet list)
- **Further reading**: Optional advanced resources

**Concept coverage**: Each chapter should address 10-20 related concepts from the learning graph, respecting dependency order.

**Length**: Target 2,000-5,000 words per chapter for comprehensive coverage without overwhelming readers.

The book-chapter-generator skill automatically creates chapter structure based on learning graph dependencies. See [Chapter 10](chapters/10-content-creation-workflows/index.md).

### When should I use skills vs. manual content creation?

**Use skills for**:

- **Repetitive structure**: Glossaries, FAQs, quiz questions that follow templates
- **Data processing**: Learning graph validation, taxonomy categorization
- **Initial drafts**: Chapter outlines, concept lists, dependency mapping
- **Boilerplate code**: MicroSim templates, HTML structures
- **Quality validation**: Running quality checks and generating reports

**Manual creation for**:

- **Creative examples**: Domain-specific scenarios and analogies
- **Nuanced explanations**: Complex concepts requiring expert insight
- **Custom visualizations**: Unique diagrams tailored to specific content
- **Refinement**: Editing AI-generated content for tone, accuracy, and clarity
- **Domain expertise**: Subject matter that requires specialized knowledge

**Best approach**: Use skills for 70% of structural work, then manually refine and customize the remaining 30% to add personality, domain expertise, and polish. See [Chapter 10](chapters/10-content-creation-workflows/index.md).

### How do I maintain consistent terminology across chapters?

Consistent terminology improves readability and comprehension. Best practices:

**Use the glossary as single source of truth**:

- Generate glossary early with glossary-generator skill
- Reference glossary terms when writing content
- Use exact glossary phrasing in all chapters

**Link to glossary on first use**:

```markdown
A [learning graph](glossary.md#learning-graph) maps concept dependencies.
```

**Create style guide**: Document conventions for:

- Capitalization (e.g., "Learning Graph" vs. "learning graph")
- Abbreviations (e.g., "DAG" after defining "Directed Acyclic Graph")
- Technical terms (e.g., "MkDocs Material theme" consistently)

**Use search and replace**: Before finalizing, search for variant terms and standardize.

The add-glossary-links skill can automatically link terms to glossary definitions throughout your textbook. See [Chapter 11](chapters/11-educational-resources-assessment/index.md).

### How do I ensure my content addresses all Bloom's Taxonomy levels?

Well-designed educational content distributes learning activities across all six cognitive levels:

**Remember (20%)**: Define terms, list components, recall facts

- "What is a learning graph?"
- "List the five levels of textbook intelligence"

**Understand (30%)**: Explain concepts, summarize processes

- "Explain how dependency mapping works"
- "Why are circular dependencies problematic?"

**Apply (25%)**: Use procedures, solve problems

- "Generate a learning graph for your course"
- "Run the quality validation scripts"

**Analyze (15%)**: Compare, categorize, examine relationships

- "Compare skills and commands"
- "Analyze your learning graph quality score"

**Evaluate (7%)**: Critique, judge, assess

- "Evaluate whether your course description is complete"
- "Assess which concepts should be split for better granularity"

**Create (3%)**: Design, develop, construct

- "Design a MicroSim for a new concept"
- "Create a custom skill for your workflow"

The quiz-generator skill automatically distributes questions across Bloom's levels. See [Chapter 3](chapters/03-course-design-educational-theory/index.md).

### What's the best way to organize MicroSims in my textbook?

Effective MicroSim organization enhances learning without overwhelming students:

**Location strategy**:

- Store all MicroSims in `docs/sims/[name]/` for centralization
- Create a MicroSim index page (`docs/sims/index.md`) listing all simulations
- Embed MicroSims in relevant chapter sections using iframes

**Integration approach**:

- **Inline**: Embed within chapter content where concept is introduced
- **Supplementary**: Link to MicroSim page for optional exploration
- **Progressive**: Start with simple sims in early chapters, advance complexity later

**Documentation**:

Each MicroSim should have:

- Learning objective (what students will understand)
- Instructions for interacting with controls
- Questions to guide exploration
- Connection to chapter concepts

**Naming**: Use descriptive, kebab-case names like `concept-dependency-graph`, `bloom-taxonomy-levels`, or `random-walk-simulation`. See [Chapter 12](chapters/12-interactive-elements-microsims/index.md).

### How often should I update my learning graph?

Learning graphs should evolve with your course content:

**Initial development**: Generate comprehensive 200-concept graph before content creation

**During content creation**: Update as you discover:

- Missing concepts that should be included
- Over-granular concepts that should be merged
- Incorrect dependency relationships

**After course delivery**: Revise based on:

- Student feedback about prerequisite gaps
- Assessment data showing struggling points
- New topics to add or outdated content to remove

**Versioning**: Use Git to track learning graph changes with semantic versioning in commit messages:

```
v1.0: Initial learning graph (200 concepts)
v1.1: Added 15 advanced ML concepts, merged 3 overly specific nodes
v2.0: Major restructuring for new curriculum
```

Update the quality metrics report and JSON visualization after each revision. See [Chapter 5](chapters/05-concept-enumeration-dependencies/index.md).

### Should I generate all content at once or incrementally?

**Incremental generation is strongly recommended**:

**Advantages**:

- **Token management**: Avoids hitting Claude usage limits
- **Quality control**: Review and refine each chapter before moving forward
- **Iteration**: Improve prompts based on early results
- **Flexibility**: Adjust structure or approach mid-project
- **Reduced risk**: Smaller changes are easier to debug and revert

**Recommended pace**:

- **Week 1**: Course description, learning graph, chapter structure
- **Week 2-3**: Chapters 1-4 (foundational content)
- **Week 4-5**: Chapters 5-8 (core concepts)
- **Week 6-7**: Chapters 9-12 (advanced topics)
- **Week 8**: Resources (glossary, FAQ, quizzes), MicroSims, final review

**Exception**: Generate glossary early (after learning graph) so you can reference consistent terminology throughout content creation. See [Chapter 10](chapters/10-content-creation-workflows/index.md).

### How do I credit AI-generated content appropriately?

Transparency about AI-assisted content is both ethical and increasingly expected:

**In textbook front matter** (preface or about page):

"This textbook was created using Claude AI and Claude Skills for automated content generation, with human review and refinement by [Author Name]. All content has been validated for accuracy."

**In individual sections** (optional, for transparency):

Add admonitions for AI-generated sections:
```markdown
!!! note "AI-Assisted Content"
    This section was generated using the chapter-content-generator skill and reviewed for accuracy.
```

**In repository**:

- Include skill names and versions in commit messages
- Document the generation workflow in README

**Licensing**: Choose appropriate licenses (CC BY, MIT, Apache 2.0) that allow derivative works. This course uses Apache 2.0 for skills, allowing commercial and academic use with attribution.

See [Chapter 10](chapters/10-content-creation-workflows/index.md) for ethical AI use guidelines.

### What are best practices for version control with textbook content?

Git best practices for educational content:

**Branching strategy**:

- `main`: Stable, published content
- `develop`: Work-in-progress chapters
- `feature/chapter-N`: Individual chapter branches

**Commit practices**:

- Commit after completing each chapter
- Write descriptive messages: "Add Chapter 5: Concept Dependencies"
- Commit generated files (learning graphs, glossaries) for reproducibility

**What to track**:

- All markdown content (chapters, glossary, FAQ)
- Configuration files (`mkdocs.yml`, `.claude/config.json`)
- Learning graph CSV and validation reports
- MicroSim HTML/JavaScript files

**What to ignore** (add to `.gitignore`):

- `site/` (MkDocs build output)
- `.DS_Store` (Mac system files)
- `__pycache__/` (Python cache)

**Collaboration**: Use pull requests for major content changes, allowing review before merging. See [Chapter 13](chapters/13-dev-tools-version-control-deployment/index.md).

## Advanced Topics

### How can I customize the intelligent-textbook skill workflow?

The intelligent-textbook skill follows a 12-step workflow defined in its SKILL.md file. To customize:

**Method 1 - Modify SKILL.md directly**:

1. Navigate to `~/.claude/skills/intelligent-textbook/`
2. Edit `SKILL.md` to change steps, add new processes, or adjust parameters
3. Save and reinvoke the skill

**Method 2 - Create project-specific variant**:

1. Copy skill to `.claude/skills/` in your project
2. Rename (e.g., `intelligent-textbook-custom`)
3. Modify workflow for your specific needs
4. Update skill name in YAML frontmatter

**Method 3 - Invoke steps manually**:

Instead of running the full intelligent-textbook skill, invoke individual component skills in custom order:

```
/skill course-description-analyzer
/skill learning-graph-generator
/skill chapter-content-generator
```

This gives maximum control over the process. See [Chapter 9](chapters/09-ibook-skills-architecture-development/index.md) for skill development patterns.

### How do I create a custom skill for my specific domain?

Creating domain-specific skills extends the intelligent textbook framework:

**Step 1 - Plan the skill**:

- Define the specific task it automates
- Identify required inputs and expected outputs
- List the Claude Code tools needed (Read, Write, Bash, etc.)

**Step 2 - Create skill structure**:

```bash
mkdir -p ~/.claude/skills/my-custom-skill
cd ~/.claude/skills/my-custom-skill
```

**Step 3 - Write SKILL.md**:

```yaml
---
name: my-custom-skill
description: Brief description of what this skill does
license: Apache-2.0
allowed-tools:
  - Read
  - Write
---

# Skill Instructions

## Purpose
Detailed explanation of skill purpose

## Workflow

### Step 1: First Task
Instructions for Claude to execute...

### Step 2: Second Task
More detailed instructions...
```

**Step 4 - Test and refine**:

Invoke with `/skill my-custom-skill` and iterate based on results.

See [Chapter 9](chapters/09-ibook-skills-architecture-development/index.md) for complete skill development guide.

### Can I integrate Claude Skills with Learning Management Systems?

While Claude Skills primarily generate static content, LMS integration is possible through several approaches:

**SCORM export**: Convert MkDocs content to SCORM packages for LMS import (requires additional tooling)

**xAPI integration**: Add Experience API tracking to MicroSims and quizzes to send learner data to LRS (Learning Record Store)

**Direct embedding**: Host MkDocs site and embed pages as iframes in LMS

**Content export**: Use generated markdown as source content, then manually import to LMS

**API integration**: Advanced users can develop custom skills that directly interface with LMS APIs (Canvas, Moodle, etc.)

The course mentions xAPI support in Level 3-4 intelligent textbooks for tracking learner interactions. Full LMS integration requires additional development beyond the core skills. See [Chapter 12](chapters/12-interactive-elements-microsims/index.md).

### How do I optimize Claude usage for large textbook projects?

Strategies to minimize token usage while maintaining quality:

**Content generation**:

- Generate chapter outlines first, then expand sections incrementally
- Use targeted skills (glossary, FAQ) rather than regenerating entire chapters
- Cache frequently referenced content (learning graph, course description) locally

**Skill efficiency**:

- Review skill YAML frontmatter to ensure `allowed-tools` is minimal
- Use Haiku model for simple tasks (faster, cheaper) vs. Sonnet for complex content
- Batch similar operations (generate all glossary terms together)

**Workflow optimization**:

- Complete structural work (learning graph, chapter planning) before content generation
- Manually create examples and domain-specific content rather than generating with AI
- Use version control to avoid regenerating content after mistakes

**Token budgeting**:

- Estimate token costs before starting (1 chapter ≈ 10K-20K tokens)
- Space intensive generation sessions across days to stay within limits
- Prioritize core chapters, defer optional content

See the [usage limits guide](claude-usage-limits.md) and [Chapter 2](chapters/02-getting-started-ibook-skills/index.md).

### What's the future roadmap for intelligent textbook skills?

While the course focuses on current Level 2-3 capabilities, future developments include:

**Level 3 - Adaptive Content**:

- Skills that generate multiple content versions for different learning styles
- Personalized learning pathways based on assessment performance
- Adaptive difficulty adjustment in exercises and MicroSims

**Level 4/5 - Chatbot Integration and Autonomous AI**:

- Integration with conversational AI tutors for real-time help
- Intelligent question answering using RAG over textbook content
- Automated formative assessment and feedback

**Enhanced skills**:

- Automated citation and reference management
- Video script generation for supplementary materials
- Advanced data visualization (3D, animated graphics)
- Accessibility auditing and remediation

**Platform evolution**:

- Cloud-based skill marketplaces
- Collaborative multi-author workflows
- Analytics dashboards for content quality

These capabilities are emerging areas of research. Contributing to the [ibook-skills repository](https://github.com/dmccreary/ibook-skills) helps drive this evolution.

### How can I contribute new skills to the repository?

The ibook-skills repository welcomes community contributions:

**Contribution process**:

1. **Fork the repository** on GitHub
2. **Create a new skill** in `skills/your-skill-name/`
3. **Write comprehensive SKILL.md** with clear workflow instructions
4. **Add supporting files** (Python scripts, templates, docs)
5. **Test thoroughly** with sample textbook projects
6. **Document in skill-descriptions/** with example usage
7. **Submit pull request** with description of skill purpose and testing

**Quality standards**:

- Follow ISO 11179 for any definitions
- Include quality validation where applicable
- Provide example outputs
- Use Apache 2.0 license for consistency
- Write clear, actionable workflow steps

**Skill ideas needed**:

- Domain-specific content generators (science, math, humanities)
- Advanced visualization tools
- Accessibility checkers
- Citation and bibliography generators
- Interactive assessment tools

See the [GitHub repository](https://github.com/dmccreary/ibook-skills) for contribution guidelines and issue tracking.

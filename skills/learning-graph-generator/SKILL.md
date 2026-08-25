---
name: learning-graph-generator
description: Generates a comprehensive learning graph from a course description, including 300-600 concepts with dependencies, taxonomy categorization, and quality validation reports. Use this when the user wants to create a structured knowledge graph for educational content.
metadata:
  ibook.version: "1.07"
---

# Learning Graph Generator

**Version:** 1.07

### Changelog

- **v1.07** — Version is now tracked in the SKILL.md frontmatter as `metadata.ibook.version`. It lives under `metadata:` rather than a bare `version:` key because strict packaging validation rejects any frontmatter key outside the six spec fields. No behavioural change.

- **v1.06** — **BREAKING:** `csv-to-json.py` (bumped to v1.04) now computes a **Concept Impact Score (CIS)** for every node and writes it into `learning-graph.json` as `node.cis`. CIS is a PageRank-style recursive importance measure: `CIS(x) = 1 + sum(CIS(d) for d in direct dependents of x)`, capturing how much of the book's total understanding transitively rests on a concept — unlike plain in-degree, which undercounts concepts that are foundational only indirectly (e.g. "Constant" or "Coefficient" in a typical algebra course, which have few direct dependents but many transitive ones). Because the graph is a DAG, CIS is computed exactly in one topological-order pass — no damping factor or iteration. Downstream skills (`book-installer`'s graph viewer, `book-chapter-generator`, `chapter-content-generator`) now read this field directly instead of recomputing their own importance measure. See the schema's `nodes[].cis` field and the "Predicting Concept Content Size" paper (Definition 3, Proposition 1) for the full derivation. This is a breaking change to the `learning-graph.json` output format (an additive field, so old readers won't break, but downstream skills now expect it to be present) — regenerate `learning-graph.json` for any existing book before running the updated `book-chapter-generator` or `chapter-content-generator`.
- **v0.06** — (prior history not tracked in this changelog format)

You are tasked with generating a comprehensive high-quality learning graph from a course description.
A learning graph is the foundational data structure for intelligent textbooks that can recommend learning paths.
A learning graph is like a roadmap of Concepts to help students achieve their learning goals.
A learning graph is an DAG Concept graph.  Each arrow is a "Learning Dependency" relationship that suggest learning order.
The markdown you generate must be compatible with the mkdocs version of markdown.  Make sure you put a blank line before any lists.

Follow these steps carefully:

## Markdown Generation Rules

1. Always place a blank line before any markdown list.  This is required by the mkdocs markdown tools.

## Mkdocs Navigation Rules

After you add a markdown file (any file with an extension `.md`) make sure to add that file
to the navigation structure in the mkdocs.yml file.  Here is an example of the nav section
for the learning graph section:

```yml
  - Learning Graph:
    - Introduction: learning-graph/index.md
    - Course Description Assessment: learning-graph/course-description-assessment.md
    - Concept Enumeration: learning-graph/list-concepts.md
    - Graph Quality Analysis: learning-graph/graph-quality-analysis.md
    - Concept Taxonomy: learning-graph/concept-taxonomy.md
    - Taxonomy Distribution Report: learning-graph/taxonomy-distribution-report.md
```

## Step 0: Setup

Tell the user that they are running the version graph generator and the version number above.

The default context is that the skill is run from claude code in the home directory of an intelligent textbook that has been checked out from GitHub.
There should be a docs directory with a standard mkdocs.yml file in the home git directory.
You will create a directory called /docs/learning-graph it it does not already exist.  
The path is relative to the git home directory.  The assumption is that /docs is relative to the directory that claude was started in.

`mkdir -p docs/learning-graph; cd docs/learning-graph`

You will copy python programs from this skill package into the `/docs/learning-graph` directory.  
You will execute python from that directory.

If you do not see the `docs` directory and the `mkdocs.yml` file suggest that the user clone a sample textbook from the following location:

`git clone https://github.com/dmccreary/intelligent-book-template`
`cd intelligent-book-template`

## Step 1: Course Description Quality Assessment

Before you begin this step, verify that it has not already been done.
To do this, check the yml metadata in the `docs/course-description.md` file.

Here is a sample of the yml metadata:

```markdown
---
title: Course Description
description: A detailed course description 
quality_score: 95
---
# Course Description
```

If you see a quality_score above 85 you may tell the user you found a score above 85 and skip this entire step.  Tell them this is a way to save tokens.

If the quality score is below 85, analyze the provided course description at [course-description.md](../course-description.md) to ensure it has enough content to generate at a minimum of 300 high-quality concepts:

1. Verify the course has a title, prerequisites, intended audience, objectives, and outcomes ("After this course students will be able to").  If these fields are missing ask the user for this information. 
1. Examine the depth and breadth of topics covered
2. Assess whether the material has sufficient granularity for at a minimum of 300 distinct concepts
3. Check for diverse topic areas and learning objectives
4. Provide detailed feedback to the user about:
   - List the expected content that you found
   - Estimated number of concepts you can derive
   - Compare this concept number with similar courses
   - Describe areas where the course description is strong
   - Any gaps or areas that might be under-represented
   - Suggest how the 2001 Bloom taxonomy (remember, understand, apply, analyze, evaluate, create) could improve the outcomes descriptions
   - Objective overall quality assessment on a scale of (1-poor to 100-perfect)
   - Suggest that the user does not proceed unless a quality score is 70 or above

Use the following rubric for creating a quality score:

### 2.2 Course Description Quality Scoring System

Evaluate the course description using this 100-point scoring system:

| Element | Points | Criteria |
|---------|--------|----------|
| **Title** | 5 | Clear, descriptive course title present |
| **Target Audience** | 5 | Specific audience identified (e.g., "college undergraduate") |
| **Prerequisites** | 5 | Prerequisites listed or explicitly stated as "None" |
| **Main Topics Covered** | 10 | Comprehensive list of topics (ideally 5-10 topics) |
| **Topics Excluded** | 5 | Clear boundaries set for what's NOT covered |
| **Learning Outcomes Header** | 5 | Clear statement: "After this course, students will be able to..." |
| **Remember Level** | 10 | Multiple specific outcomes for remembering/recalling |
| **Understand Level** | 10 | Multiple specific outcomes for understanding/explaining |
| **Apply Level** | 10 | Multiple specific outcomes for applying/using |
| **Analyze Level** | 10 | Multiple specific outcomes for analyzing/breaking down |
| **Evaluate Level** | 10 | Multiple specific outcomes for evaluating/judging |
| **Create Level** | 10 | Multiple specific outcomes for creating/synthesizing; includes capstone ideas |
| **Descriptive Context** | 5 | Additional context about course importance, relevance, or value |

**Scoring Guidelines:**
- Award full points if element is complete and high-quality
- Award partial points if element is present but incomplete or vague
- Award 0 points if element is missing
- For Bloom's Taxonomy levels, require at least 3 specific, actionable outcomes for full points

Tell user what their score was and suggest they improve the course description until the score goes above 80.

Save this report to [course-description-assessment.md](./course-description-assessment.md)

5. **Ask the user if you should proceed** with generating the learning graph

## Step 2: Generate Concept Labels

Once the course-description has been approved, generate the concept labels from the course content:

**Requirements:**
- Each Concept label must be in Title Case
- Maximum length: 32 characters
- Labels should be clear, specific, and pedagogically sound
- Cover the full breadth of the course material
- Concept Labels are entity names, not questions
- Do not use questions in the Concept Label.  Don't use "What is Git", just use "Git"

**Number of Concepts:**

For simple books, a list of 300 concepts is fine.
For complex technical books, you may generate up to 600 concepts.
Do not exceed 600 concepts unless you have good reason and the user approves this decision.
Remember that generating concept dependencies gets complex the more concepts there are.

!!! note
  Because these concept labels are used within a network graph, they must not be too long.
  Otherwise the graph will be hard to read.

**Output:**
- Save the numbered list to [concept-list.md](./concept-list.md)
- Format: Simple numbered list (1-600) in a markdown file
- Make sure that each number is unique so it can be used as a ConceptID
- Inform the user the file has been created
- Tell the user they should view the list and add and remove concepts now
- Tell the user it is best review the concept list before the next steps

Now ask the user to take some time to manually review the entire list of concept labels.
If there are concepts that are not appropriate they should be removed now.
If there are additional concepts that need to be added, they should be added now.
It will require a lot of extra tokens later to change the content later.
This is an important review step to ensure the quality of the textbook.
Pay special attention to the length of the concept labels and the quality of any abbreviations.

## Step 3: Generate Dependency Graph

Create a CSV file mapping dependencies between concepts:

**Format:**
- Filename: [learning-graph.csv](./learning-graph.csv)
- Columns: `ConceptID,ConceptLabel,Dependencies`
- ConceptID: Integer (1-600)
- ConceptLabel: The exact label from Step 2
- Dependencies: Pipe-delimited list of ConceptIDs (e.g., "1|3|7")

**Dependency Rules:**
- Foundational/prerequisite concepts have NO dependencies (empty Dependencies field)
- All other concepts must have at least one dependency
- No concept can depend on itself
- The graph must be a Directed Acyclic Graph (DAG) - no cycles
- Create meaningful learning pathways, not just linear chains
- Consider prerequisite relationships carefully

**Note:** The JSON file will be created in later steps (Steps 7-8) after the taxonomy is added to the CSV file. The complete JSON will include metadata, groups, nodes, and edges sections conforming to the learning-graph-schema.json.

## Step 4: Learning Graph Quality Validation

Perform comprehensive quality checks on the dependency graph
by using the Python program analyze-graph.py in this skill.
It will do the following checks:

1. **Verify DAG structure**: Ensure no cycles exist
2. **Check for self-dependencies**: No concept should depend on itself
3. **Foundational concepts**: Identify concepts with zero dependencies
4. **Terminal nodes**: Identify concepts that nothing depends on (leaf nodes). These are valid and expected — do not confuse with orphaned nodes (which have no connections at all)
5. **Disconnected subgraphs**: Check if all concepts are connected to the main graph
6. **Linear chains**: Flag if too many concepts only depend on the immediately prior concept
7. **Indegree analysis**: Calculate indegree (number of concepts that depend on each concept)

Shell command `python analyze-graph.py learning-graph.csv quality-metrics.md`

Verify the report has been written to [quality-metrics.md](./quality-metrics.md)

**Generate the learning graph quality metrics report:**
- Total concepts with zero dependencies - outbound arrows (foundational prerequisites)
- Total concepts with 1+ dependencies
- Average number of dependencies per concept
- Maximum dependency chain length
- Number of terminal (leaf) nodes that no other concept depends on
- Number of disconnected subgraphs
- Top 10 concepts with highest indegree (most depended-upon concepts)

Give the user a general quality score on a scale of 1 (poor) to 100 (perfect).
If the learning graph does not get a score above 70, suggest that the user iterates on the process

## Step 5: Create Concept Taxonomy

Develop a categorical taxonomy for organizing concepts:

**Requirements:**
- Target: ~12 categories (can vary by 2-3 if natural groupings emerge)
- Categories should evenly distribute concepts
- Avoid having any single category exceed 30% of total concepts
- Use clear, descriptive category names with title case and spaces
- Create 3-5 letter abbreviations for each category (TaxonomyID)
- Note that a JSON representation of the taxonomy will be created to form the groups section of the learning graph

**Output:**
- Save taxonomy to [concept-taxonomy.md](./concept-taxonomy.md)
- Format as markdown with:
  - Category name
  - TaxonomyID abbreviation (3-5 letters uppercase)
  - Brief description of what concepts belong in this category

## Step 5b: Create Taxonomy Names JSON

**CRITICAL STEP** - This prevents the common bug where taxonomy IDs appear instead of human-readable names in the graph viewer legend and reports.

Extract the taxonomy ID to human-readable name mapping from concept-taxonomy.md and save it as a JSON file:

**Create file:** `taxonomy-names.json`

**Format:**
```json
{
  "FOUND": "Foundation Concepts",
  "EDA1": "Exploratory Data Analysis I",
  "EDA2": "Exploratory Data Analysis II",
  "REG": "Regression & Correlation",
  ...
}
```

**Rules:**
- Keys are the TaxonomyID abbreviations (uppercase, 3-5 letters)
- Values are human-readable category names in Title Case with spaces
- Every taxonomy ID used in the CSV must have a corresponding name
- Names should be descriptive and meaningful to students

This file is REQUIRED for csv-to-json.py to generate correct `classifierName` values in learning-graph.json. Without it, the graph viewer legend will show cryptic IDs like "EDA1" instead of "Exploratory Data Analysis I".

---

## Step 6: Add Taxonomy to CSV

Update the dependencies CSV file:

1. Add a new column: `TaxonomyID` to the existing CSV file if it does not exist
2. For each concept, assign the best matching TaxonomyID
3. Use "MISC" for concepts without a clear category match
4. Save the updated file to [learning-graph.csv](./learning-graph.csv)

You can use the Python Program add-taxonomy.py as a template
that will do the substitution.

**Final CSV columns:** `ConceptID,ConceptLabel,Dependencies,TaxonomyID`

## Step 7: Create the `metadata` section of the learning-graph.json file

The metadata section contains Dublin Core-inspired fields for the textbook extracted from the course-description.md file. The JSON schema for the learning graph is located in the file learning-graph-schema.json within this skill.

**Required fields:**
- `title`: Extract from the course description title
- `description`: Extract or summarize from the course description

**Optional but recommended fields:**
- `creator`: Author or organization name
- `date`: Current date in YYYY-MM-DD format
- `version`: Version number (e.g., "1.0")
- `format`: "Learning Graph JSON v1.0"
- `schema`: URL to the JSON schema
- `license`: License information (e.g., "CC BY-NC-SA 4.0 DEED")

Here is an example of the metadata section:

```json
"metadata": {
    "title": "Title Text From Course Description",
    "description": "A description of the course in a few sentences.",
    "creator": "Your Name",
    "date": "2025-11-01",
    "version": "1.0",
    "format": "Learning Graph JSON v1.0",
    "schema": "https://raw.githubusercontent.com/dmccreary/learning-graphs/refs/heads/main/src/schema/learning-graph-schema.json",
    "license": "CC BY-NC-SA 4.0 DEED"
  }
```

You can create a metadata.json file with these fields to pass to the csv-to-json.py program in Step 9.

## Step 8: Create the groups section of the JSON file

Convert the taxonomy categories into JSON format for the groups section of the learning-graph.json file. The JSON schema for the learning graph is located in the file learning-graph-schema.json within this skill.

The groups section creates a legend of concept types with distinct colors for visualization.

**Important:**
- The groups section uses taxonomy IDs (e.g., "FOUND", "DEF") as keys
- Each group must have a `classifierName` field containing a **descriptive human-readable name** (e.g., "Foundation Concepts", NOT just "FOUND")
- Each group must have a `color` field using **named CSS colors** (NOT hex codes like "#E74C3C")
- Each group should have a `font` object with a `color` field — `white` on dark backgrounds, `black` on light backgrounds. `csv-to-json.py` v1.04+ picks the right font color automatically based on the background.

**Key structure:**
- **Group key**: Use the TaxonomyID from the CSV (uppercase, no spaces, e.g., "FOUND")
- **classifierName**: Descriptive display name with Title Case and spaces (e.g., "Foundation Concepts"). NEVER just repeat the TaxonomyID abbreviation.
- **color**: Use named CSS colors from the recommended distinct palette below. Avoid AliceBlue (page background).
- **font.color**: `white` on dark backgrounds, `black` on light. Auto-assigned by csv-to-json.py.

### Recommended distinct palette (24 colors)

The default palette in `csv-to-json.py` v1.04+ is hand-tuned so that adjacent legend rows never collide and same-hue families are separated by lightness. It comfortably supports up to 24 distinct categories. Use this palette (or a subset, in this order, via `color-config.json`) to keep visual clarity even with many taxonomies:

| Position | Color (CSS name) | Suggested category family | Font |
|---|---|---|---|
| 1 | SteelBlue | Foundations | white |
| 2 | DarkSlateBlue | Role / governance | white |
| 3 | DarkGreen | Architecture | white |
| 4 | LimeGreen | Application development | black |
| 5 | Gold | Data management | black |
| 6 | DarkGoldenrod | Data governance | white |
| 7 | Khaki | Business intelligence | black |
| 8 | Teal | Enterprise systems | white |
| 9 | DodgerBlue | Networks / telecom | white |
| 10 | LightSkyBlue | Cloud computing | black |
| 11 | Crimson | Security | white |
| 12 | DarkRed | Privacy / compliance | white |
| 13 | MediumPurple | Project management | white |
| 14 | Indigo | Process management | white |
| 15 | DarkOrchid | Systems analysis & design | white |
| 16 | HotPink | Human-computer interaction | black |
| 17 | OliveDrab | IT service management | white |
| 18 | Orange | AI capabilities | black |
| 19 | Coral | Responsible AI | black |
| 20 | Peru | AI law / regulation | black |
| 21 | SaddleBrown | AI security | white |
| 22 | Tomato | AI productivity | white |
| 23 | DeepPink | Knowledge graphs / accent | white |
| 24 | DimGray | Emerging / miscellaneous | white |

**Design rationale:**

- **Subject-family hue grouping** — cool blues for foundations and infrastructure, greens for build/architecture, yellows/golds for the data band, reds for security, purples for project/process, oranges/browns for the AI cluster, an accent (DeepPink) for knowledge graphs as connective tissue, neutral gray for emerging.
- **Within each hue family, lightness alternates** so neighbors never collide (Gold → DarkGoldenrod, DodgerBlue → LightSkyBlue, MediumPurple → Indigo, etc.).
- **Dark backgrounds get white text, light backgrounds get black text** — `csv-to-json.py` v1.04+ enforces this automatically. The dark set covers SteelBlue, DarkSlateBlue, DarkGreen, DarkGoldenrod, Teal, DodgerBlue, Crimson, DarkRed, MediumPurple, Indigo, DarkOrchid, OliveDrab, SaddleBrown, Tomato, DeepPink, DimGray.

### color-config.json (recommended)

Save the chosen palette to `docs/learning-graph/color-config.json` so any future regeneration preserves the exact assignment per taxonomy ID. Example:

```json
{
  "FOUND": "SteelBlue",
  "ROLE": "DarkSlateBlue",
  "ARCH": "DarkGreen",
  "APPDEV": "LimeGreen",
  "DATA": "Gold",
  "SEC": "Crimson",
  "MISC": "DimGray"
}
```

Pass it to csv-to-json.py: `python csv-to-json.py learning-graph.csv learning-graph.json color-config.json metadata.json taxonomy-names.json`

### Example groups section

```json
"groups": {
    "FOUND": {
      "classifierName": "Foundation Concepts",
      "color": "SteelBlue",
      "font": { "color": "white" }
    },
    "DATA": {
      "classifierName": "Data and Information Management",
      "color": "Gold",
      "font": { "color": "black" }
    },
    "SEC": {
      "classifierName": "Security of Information Assets",
      "color": "Crimson",
      "font": { "color": "white" }
    },
    "AIIS": {
      "classifierName": "AI in Information Systems",
      "color": "Orange",
      "font": { "color": "black" }
    },
    "MISC": {
      "classifierName": "Miscellaneous Concepts",
      "color": "DimGray",
      "font": { "color": "white" }
    }
  }
```

**Note:** The csv-to-json.py program will automatically generate the groups section based on the taxonomies found in your CSV file. Without a `color-config.json`, it positionally assigns colors from the 24-color default palette in legend order — already distinct, but a saved `color-config.json` is recommended so the assignment is stable across regenerations.

## Step 9: Generate the Complete Learning Graph JSON

Now that you have created the metadata.json file (Step 7), taxonomy-names.json (Step 5b), and have the taxonomy-enriched CSV (Step 6), run the csv-to-json.py program to generate the complete learning-graph.json file:

```bash
python csv-to-json.py learning-graph.csv learning-graph.json color-config.json metadata.json taxonomy-names.json
```

**IMPORTANT:** The `taxonomy-names.json` file is strongly recommended to ensure human-readable category names appear in the graph viewer legend. Without it, taxonomy IDs (like "EDA1") will be used as display names instead of proper names (like "Exploratory Data Analysis I").

This command will:
1. Read the learning-graph.csv file (with ConceptID, ConceptLabel, Dependencies, TaxonomyID columns)
2. Use the metadata from metadata.json
3. Use the human-readable names from taxonomy-names.json for the `classifierName` field
4. Auto-generate the groups section based on the taxonomies in the CSV
5. Create nodes with proper group references (using TaxonomyIDs)
6. Create edges based on the dependencies
7. **Compute the Concept Impact Score (CIS) for every node** and attach it as `node.cis` (see Changelog above)
8. Output a complete learning-graph.json file conforming to the schema
9. WARN if any taxonomy ID is missing a human-readable name

Verify that the file [learning-graph.json](./learning-graph.json) is present and valid. The console output will list the top 10 concepts by CIS — sanity-check that these are genuinely foundational concepts for the course (widely-depended-upon ideas), not narrow terminal topics. If a narrow/advanced concept tops the CIS list, the edge direction is very likely inverted (see the `book-chapter-generator` skill's edge-direction validation for how to diagnose this).

Optional: You can validate the JSON against the schema using:
```bash
./validate-learning-graph.sh learning-graph.json
```

## Step 10: Taxonomy Distribution Report

Generate a distribution analysis:

1. Count concepts in each category
2. Calculate percentages
3. Identify over-represented categories (>30%)
4. Suggest alternative categorization if needed

Use the python report in this skill called taxonomy-distribution.py

**Output:**
- Save to [taxonomy-distribution.md](./taxonomy-distribution.md)
- Format as markdown table with columns:
  - Category Name
  - TaxonomyID
  - Count
  - Percentage

## Step 11: Create new index.md from index-template.md

Create a new `index.md` file in the learning-graph directory from the file index-template.md in this skill.
Customize the new index.md file to reflect the name of this intelligent book.  Look for values in all uppercase (TEXTBOOK_NAME)
and replace them with the appropriate values.

## Step 12: Write session log

Export the session log to logs/learning-graph-generator-VERSION-DATE.md

Where:

1. VERSION is the version of this skill.
2. DATE is today's date in ISO format yyyy-mm-dd.

Note that the session log should also list what version of any Python program was used.
For example, not what version of the csv-to-json.py Python program was used in the session log.
This is important for debugging.

## Step 13: Completion

Inform the user that the learning graph generation is complete! Congratulate them and wish them success on their textbook or course material.  
Tell the user if they want to view the learning graph they should run the /book-installer skill with the install learning graph guide which will create a microsim in @docs/sims/graph-viewer.
Although this step is optional, it is strongly recommended.
Tell them that the next logical step is to run the /book-chapter-generator skill, but that it is critical to review the chapter overview and
the concept lists, the concept taxonomies and the learning graph before they do this next step.
Generating chapter content takes a lot of tokens and it is best to make sure each
chapter overview and concept lists are complete.

**Files created:**
- [course-description-assessment.md](./course-description-assessment.md) - quality assessment of the course description
- [concept-list.md](./concept-list.md) - Numbered list of up to 600 concepts
- [learning-graph.csv](./learning-graph.csv) - Full dependency graph with taxonomy
- [taxonomy-names.json](./taxonomy-names.json) - Mapping of taxonomy IDs to human-readable names (CRITICAL for graph viewer)
- [metadata.json](./metadata.json) - Metadata for the learning graph (title, description, creator, etc.)
- [learning-graph.json](./learning-graph.json) - Complete learning graph with metadata, groups, nodes, and edges in vis-network.js JSON format
- [concept-taxonomy.md](./concept-taxonomy.md) - Category definitions
- [quality-metrics.md](./quality-metrics.md) - Quality validation report
- [taxonomy-distribution.md](./taxonomy-distribution.md) - Category distribution analysis
- [index.md](./index.md) - Introduction page for the learning graph section


## Important Notes

- Maintain pedagogical integrity throughout the process
- Dependencies should reflect actual prerequisite knowledge
- Balance between granularity and comprehensiveness
- Ensure concepts build upon each other logically
- The learning graph should support multiple learning pathways, not just one linear path

---
name: book-chapter-generator
description: Designs the chapter structure for an intelligent textbook by analyzing the learning graph and concept dependencies. Use after the learning graph is complete and before generating chapter content.
license: 
metadata:
  ibook.version: "1.1.1"
  ibook.preferred-model: "sonnet"
---

# Book Chapter Generator

**Version:** 1.1.1

### Changelog

- **v1.1.1** — Step 4.6's completion message now always includes a strong recommendation to create a learning mascot (via `book-installer`'s learning-mascot guide) before running `chapter-content-generator`. A mascot designed up front gets placed into every chapter as content is written; adding one after dozens of chapters already exist means retrofitting each one instead. Also stated as a standing rule in the Notes section. No change to chapter design or file structure.

- **v1.1.0** — Version is now tracked in the SKILL.md frontmatter as `metadata.ibook.version`. It lives under `metadata:` rather than a bare `version:` key because strict packaging validation rejects any frontmatter key outside the six spec fields, which would block the skill from claude.ai, the Skills API, and `package_skill.py`. No behavioural change.

- **v1.0.0** — **BREAKING:** First tracked version number for this skill. Step 1.4a no longer computes its own "dependents count" from the edge list — it now reads the pre-computed **Concept Impact Score (CIS)** directly from each node's `cis` field in `learning-graph.json` (added by `learning-graph-generator` v1.06+). CIS is a strictly better importance signal than raw dependents count: it captures *transitive* impact (a concept with few direct dependents can still be highly foundational if those dependents themselves have many dependents), which plain dependents-count undercounts. The "Concepts Covered" section in each generated chapter's `index.md` (Step 4.4) is now a **markdown table** with `Concept` and `CIS Score` columns, replacing the old numbered list with a `(N dependents)` suffix. Requires `learning-graph.json` to have been regenerated with `learning-graph-generator` v1.06+ (nodes missing a `cis` field will read as `cis=1`, the minimum — check the console output when loading the graph and regenerate if every concept shows 1).

## Overview

This skill creates a comprehensive chapter structure for intelligent textbooks by analyzing the course description, learning graph, and concept taxonomy. It designs an optimal chapter outline that ensures all concepts are covered exactly once, respects dependency relationships, and distributes content appropriately across chapters.
This task is run serially after the learning graph generation.

## When to Use This Skill

Use this skill when:
- The course description is finalized and the a learning graph has been generated (learning-graph.json exists)
- Chapter content structure needs to be designed before writing begins

**Prerequisites:**
- `/docs/course-description.md` must exist
- `/docs/learning-graph/learning-graph.json` must exist with ~200 concepts
- mkdocs.yml file must be in place for the chapter links to be generated to the nav section

**Do NOT use this skill if:**
- The learning graph hasn't been generated yet (use `learning-graph-generator` first)
- Chapter content already exists and just needs updating

## Chapter Generation Workflow

This skill follows a four-step sequential workflow with user approval before generating files.

### Step 1: Analyze Input Resources

Before designing chapters, analyze the following resources:

#### 1.1 Read Course Description

Read `/docs/course-description.md` to understand:
- Course title and target audience
- Learning objectives and outcomes
- Prerequisite knowledge
- Overall scope and goals

#### 1.2 Read Learning Graph

Read `/docs/learning-graph/learning-graph.json` to extract:
- Complete list of concepts (typically 200 concepts)
- Concept dependencies (which concepts require others as prerequisites)
- Concept groupings by taxonomy category
- Metadata about the course

!!! info "Learning Graph = Concept Dependency Graph (a DAG)"
    A learning graph is a **Concept Dependency Graph** -- a directed acyclic graph
    (DAG) where each edge represents a "depends on" relationship. We chose the
    **dependency direction** (edges point FROM a concept TO the concepts it depends on)
    because this aligns with standard graph theory algorithms for topological sorting,
    cycle detection, and transitive reduction.

    Some learning management systems use an alternative called an **enablement graph**,
    where edges point in the opposite direction (FROM prerequisite TO the concepts it
    enables). The enablement direction is more intuitive for some teachers ("learning
    Ecology enables you to learn Ecosystems"), but it is less natural for graph
    algorithms. This project uses the dependency direction exclusively.

!!! danger "CRITICAL: Edge Direction in learning-graph.json"
    In the vis-network JSON format, edges point **FROM dependent TO prerequisite**
    (the dependency direction).

    - Edge `{from: 5, to: 1}` means "Biodiversity (5) depends on Ecology (1)"
    - It does NOT mean "Ecology leads to Biodiversity" (that would be the enablement direction)

    **To build a prerequisite map:**
    ```python
    prereqs = defaultdict(set)
    for edge in data['edges']:
        prereqs[edge['from']].add(edge['to'])  # CORRECT: dependency direction
    ```

    **NEVER use** `prereqs[edge['to']].add(edge['from'])` -- this accidentally
    converts to the enablement direction, inverting ALL dependencies and silently
    producing invalid chapter orderings. This bug wastes significant tokens and
    requires a complete redesign.

Validate that:
- The graph structure is a valid DAG (no circular dependencies)
- All concepts have unique IDs
- Dependency references are valid

#### 1.2a Validate Edge Direction (MANDATORY)

Before designing any chapters, verify the edge direction is correct:

1. Build the prerequisite map using `prereqs[edge['from']].add(edge['to'])`
2. Identify foundational concepts (those with zero entries in prereqs)
3. Verify foundational concepts are simple, introductory terms (e.g., "Ecology", "Energy", "System")
4. If advanced concepts appear as foundational, the direction is WRONG -- stop and fix

```python
# Quick validation
foundational = [n for n in data['nodes'] if n['id'] not in prereqs]
print(f"Foundational ({len(foundational)}):")
for n in foundational:
    print(f"  {n['id']}: {n['label']}")
# These should be simple/introductory. If you see "Sustainability",
# "Climate Change", etc., the edge direction is inverted.
```

**Do NOT proceed to chapter design until this check passes.**

#### 1.3 Read Concept Taxonomy

Read `/docs/learning-graph/concept-taxonomy.md` (if it exists) to understand:
- Taxonomy categories and their meanings
- How concepts are grouped conceptually
- Any suggested ordering or progression

#### 1.4 Identify Design Constraints

Analyze the data to identify:
- **Foundational concepts**: Concepts with no dependencies (should appear early)
- **Advanced concepts**: Concepts with many dependencies (should appear later)
- **Dependency chains**: Long sequences of prerequisite relationships
- **Concept clusters**: Groups of related concepts that should stay together
- **Terminal concepts**: Concepts that nothing depends on (can be placed flexibly)

#### 1.4a Read Concept Impact Score (CIS) Per Concept

Every node in `learning-graph.json` carries a pre-computed **`cis`** field
(added by `learning-graph-generator` v1.06+) -- the Concept Impact Score, a
PageRank-style recursive importance measure: `CIS(x) = 1 + sum(CIS(d) for d
in direct dependents of x)`. Unlike a simple dependents count (direct
dependents only), CIS captures *transitive* impact: a concept with only 1-2
direct dependents can still have a very high CIS if those dependents
themselves have many dependents. This is why CIS, not raw dependents count,
now drives per-concept word-count and non-text-element targets in
`chapter-content-generator`.

```python
# cis[concept_id] = the concept's pre-computed Concept Impact Score
cis = {n['id']: n.get('cis', 1) for n in data['nodes']}

# A concept with cis[cid] == 1 is a terminal concept (nothing transitively
# builds on it). A concept with a high cis[cid] is a foundational "hub"
# concept -- large amounts of the book's content ultimately rest on it,
# even if its direct dependents count is small.
```

**Sanity check:** if every concept shows `cis == 1`, `learning-graph.json`
predates `learning-graph-generator` v1.06 and needs to be regenerated before
proceeding -- do not fall back to computing your own dependents count.

Carry this `cis` map forward into Step 4 -- it is placed alongside each
concept name in every chapter's "Concepts Covered" table.

### Step 2: Design Chapter Structure

Design an optimal chapter structure following these principles:

#### 2.1 Determine Chapter Count

Choose the appropriate number of chapters (6-20) based on:
- **Total concepts**: ~200 concepts typically need 10-15 chapters
- **Dependency complexity**: More complex dependencies may need more chapters
- **Taxonomy distribution**: Natural groupings suggest chapter boundaries
- **Target audience**: Introductory courses may need smaller chapters

**Guidelines:**
- Minimum 6 chapters (for very concise courses)
- Optimal range: 10-15 chapters
- Maximum 20 chapters (for comprehensive graduate-level content)
- Aim for 10-20 concepts per chapter on average

#### 2.2 Assign Concepts to Chapters

Design chapter assignments that satisfy these requirements:

**CRITICAL REQUIREMENTS:**
1. **Every concept appears in exactly one chapter** (no duplicates, no omissions)
2. **No concept appears before its dependencies** (respect the DAG structure)
3. **Balanced distribution** (avoid chapters with too many or too few concepts)

**OPTIMIZATION GOALS:**
- Keep related concepts (same taxonomy category) together when possible
- Create logical progression from foundational to advanced topics
- Balance chapter sizes (avoid chapters with <8 or >25 concepts)
- Group concepts that form natural learning units
- Consider cognitive load (mix difficulty levels within chapters)

#### 2.3 Create Chapter Titles

For each chapter, create a title that:
- Uses **Title Case** formatting
- Is **no longer than 200 characters** (to fit on one line)
- Clearly describes the chapter's main topic
- Uses standard educational terminology
- Avoids acronyms unless widely known

**Examples:**
- "Introduction to Graph Theory Fundamentals"
- "Binary Trees and Tree Traversal Algorithms"
- "Graph Coloring Problems and Applications"
- "Advanced Topics in Network Flow Optimization"

#### 2.4 Write Chapter Summaries

For each chapter, write a **single sentence** (20-40 words) that:
- Describes what the chapter covers
- Mentions key concepts or themes
- Indicates the chapter's role in the learning progression

### Step 3: Present Design to User for Approval

Before creating any files, present the chapter design to the user in this format:

```
## Proposed Chapter Structure

I've designed a [number]-chapter structure for your textbook covering [total] concepts.

### Chapters:

1. **[Chapter Title]** ([X] concepts)
   [One sentence summary]

2. **[Chapter Title]** ([X] concepts)
   [One sentence summary]

[... continue for all chapters ...]

### Design Challenges & Solutions:

[Discuss any challenges encountered and how the design addresses them, such as:]
- **Challenge**: Concept X has 15 dependencies, making placement difficult
  **Solution**: Placed in Chapter 8 after all prerequisites are covered in Chapters 1-7

- **Challenge**: Taxonomy category Y contains 45 concepts
  **Solution**: Split across Chapters 3, 6, and 9 to maintain logical flow

[... other challenges ...]

### Statistics:

- Total chapters: [X]
- Average concepts per chapter: [X.X]
- Range: [min]-[max] concepts per chapter
- All [total] concepts covered: ✓
- All dependencies respected: ✓
```

#### 3.1 Get User Approval

After presenting the design, ask:

```
Do you approve this chapter structure? (y/n)

If no, please specify what changes you'd like:
- Different number of chapters?
- Specific concepts moved to different chapters?
- Chapter titles revised?
- Different grouping strategy?
```

#### 3.2 Handle User Feedback

If the user says "no" or requests changes:
- Listen to their specific feedback
- Revise the chapter design accordingly
- Re-present the updated structure
- Continue iterating until approval is received

If the user says "yes":
- Proceed to Step 4 to generate the chapter files

### Step 4: Generate Chapter Directory Structure and Files

Once the user approves the design, create the chapter structure:

#### 4.1 Create URL Path Names

For each chapter, create a URL-friendly path name:

**Rules:**
- Use only **lowercase letters** and **dashes** (no other characters)
- Remove all special characters, punctuation, and numbers (except in numbered prefixes)
- Replace spaces with dashes
- Use abbreviations if needed to keep names short (<50 characters)
- Make names descriptive but concise

**Examples:**
```
"Introduction to Graph Theory Fundamentals" → "intro-to-graph-theory"
"Binary Trees and Tree Traversal Algorithms" → "binary-trees-traversal"
"Advanced Topics in Network Flow Optimization" → "advanced-network-flow"
```

#### 4.2 Create Directory Structure

Create the following directory structure:

```
/docs/chapters/
├── index.md
├── 01-[url-path-name]/
│   └── index.md
├── 02-[url-path-name]/
│   └── index.md
├── 03-[url-path-name]/
│   └── index.md
[... continue for all chapters ...]
```

**Implementation:**
```bash
mkdir -p /docs/chapters
mkdir -p /docs/chapters/01-[url-path-name]
mkdir -p /docs/chapters/02-[url-path-name]
# ... continue for all chapters
```

#### 4.3 Create Main Chapters Index

Create `/docs/chapters/index.md` with:

```markdown
# Chapters

This textbook is organized into [X] chapters covering [Y] concepts.

## Chapter Overview

1. [Chapter 1 Title](01-[url-path-name]/index.md) - [One sentence summary]
2. [Chapter 2 Title](02-[url-path-name]/index.md) - [One sentence summary]
[... continue for all chapters ...]

## How to Use This Textbook

[Add 2-3 sentences about how readers should progress through the chapters, noting that dependencies are respected and concepts build on each other]

---

**Note:** Each chapter includes a list of concepts covered. Make sure to complete prerequisites before moving to advanced chapters.
```

#### 4.4 Create Individual Chapter Index Files

For each chapter, create `/docs/chapters/[XX]-[url-path-name]/index.md` with this structure:

```markdown
# [Chapter Title]

## Summary

[Write a 2-4 sentence summary of what the chapter covers, expanding on the one-sentence version from the design. Include:]
- Main topics and themes
- How this chapter fits in the learning progression
- What students will be able to do after completing this chapter

## Concepts Covered

This chapter covers the following [X] concepts from the learning graph:

| Concept | CIS Score |
|---------|-----------|
| [Concept Name 1] | 187 |
| [Concept Name 2] | 1 |
| [Concept Name 3] | 42 |
[... continue for all concepts in this chapter, in pedagogical order ...]

## Prerequisites

[If this is not the first chapter, list which previous chapters should be completed first:]

This chapter builds on concepts from:
- [Chapter X: Chapter Title](../[XX]-[url-path-name]/index.md)
- [Chapter Y: Chapter Title](../[YY]-[url-path-name]/index.md)

[If this is the first chapter or has no prerequisites within the book:]

This chapter assumes only the prerequisites listed in the [course description](../../course-description.md).

---

TODO: Generate Chapter Content
```

**Important formatting notes:**
- Always include a blank line before markdown lists (MkDocs requirement)
- Use relative paths for internal links
- Concept names should match exactly as they appear in learning-graph.json
- "Concepts Covered" is a markdown table with `Concept` and `CIS Score`
  columns (not a numbered list) -- one row per concept, in the same
  pedagogical order used elsewhere in this chapter, using the `cis` map
  read in Step 1.4a. Always include the blank line before the table
  (MkDocs requirement).
- Maintain consistent heading hierarchy (# → ## → ###)

#### 4.5 Update MkDocs Navigation

After creating all chapter files, add the chapters to the `Chapters:` section of
`mkdocs.yml`. Follow the canonical nav-editing rules (read-before-write,
serialize edits, only touch your section, number-only chapter labels) in
`$BK_HOME/skills/book-installer/references/mkdocs-nav-editing.md`.

```yaml
  - Chapters:
    - List of Chapters: chapters/index.md
    - 1. [Chapter 1 Title]: chapters/01-[url-path-name]/index.md
    - 2. [Chapter 2 Title]: chapters/02-[url-path-name]/index.md
    # ... continue for all chapters
```

#### 4.6 Confirm Completion

After all files are created, inform the user. **Always** include the mascot
recommendation below verbatim — do not omit it or make it conditional on
whether a mascot appears to already exist:

```
✅ Chapter structure generated successfully!

Created:
- chapters/index.md (main chapter overview)
- [X] chapter directories with index files
- Updated mkdocs.yml navigation

Strong recommendation: create a learning mascot before generating any
chapter content. Run the `book-installer` skill's learning-mascot guide (or
just ask to "add a learning mascot") now. The `chapter-content-generator`
skill places mascot admonitions as it writes each chapter, and retrofitting
a mascot into chapters that already exist is far more expensive than
designing one first.

Next steps:
1. Create a learning mascot (strongly recommended, see above) — run `book-installer`, then the learning mascot guide
2. Review the chapter structure: `mkdocs serve`
3. Navigate to the Chapters section to see all chapter outlines
4. Use the chapter content generation skill (when ready) to populate each chapter
5. Each chapter index.md has "TODO: Generate Chapter Content" as a placeholder

Statistics:
- Total chapters: [X]
- Total concepts assigned: [Y]
- All dependencies respected: ✓
```

## Design Principles

### Dependency Management

**Critical**: The chapter sequence must respect the DAG structure:
- If concept B depends on concept A, then A must appear in an earlier (or same) chapter than B
- Check all dependency relationships before finalizing chapter assignments
- Use topological sorting to verify the order is valid

**Mandatory validation before presenting to user:**

Run this strict check and achieve **zero violations** before proceeding to Step 3:

```python
# Build prereqs: from=dependent, to=prerequisite (NEVER invert this)
prereqs = defaultdict(set)
for e in data['edges']:
    prereqs[e['from']].add(e['to'])

# Map each concept to its chapter index
chapter_map = {}
for i, (title, cids) in enumerate(chapters):
    for cid in cids:
        chapter_map[cid] = i

# Check: every prerequisite must be in same or earlier chapter
violations = []
for i, (title, cids) in enumerate(chapters):
    for cid in cids:
        for dep in prereqs.get(cid, set()):
            if dep in chapter_map and chapter_map[dep] > i:
                violations.append(f"{nodes[cid]} ch{i+1} needs {nodes[dep]} ch{chapter_map[dep]+1}")

assert len(violations) == 0, f"{len(violations)} dependency violations found"
```

**Do NOT present a chapter design with any violations to the user.** Fix all violations first by moving concepts between chapters or reordering chapters.

### Content Balance

Aim for balanced chapter sizes:
- **Optimal**: 12-18 concepts per chapter
- **Acceptable**: 8-25 concepts per chapter
- **Avoid**: <8 concepts (too thin) or >25 concepts (too dense)

If a chapter is too large, consider splitting it into two chapters.
If a chapter is too small, consider merging it with a related chapter.

### Pedagogical Flow

Structure chapters to support learning:
- **Early chapters**: Foundational concepts, simple ideas, build confidence
- **Middle chapters**: Core content, increasing complexity, practical applications
- **Late chapters**: Advanced topics, integration, synthesis

Within each chapter, order concepts from:
1. Foundational to advanced (based on dependencies)
2. Simple to complex (based on cognitive load)
3. Abstract to concrete (when introducing new ideas)

### Cognitive Load

Consider student cognitive load:
- Don't overload early chapters (students are still building context)
- Mix difficulty levels within chapters when possible
- Group related concepts to reduce cognitive switching
- Ensure adequate scaffolding (prerequisite concepts in prior chapters)

## Common Challenges and Solutions

### Challenge: Taxonomy Category Too Large

**Problem**: A single taxonomy category contains 40+ concepts.

**Solutions**:
- Split the category across multiple chapters
- Use different aspects or sub-themes as chapter boundaries
- Interleave with other categories to maintain engagement

### Challenge: Long Dependency Chains

**Problem**: Concept Z depends on Y, which depends on X, which depends on W... (5+ levels deep).

**Solutions**:
- Spread the chain across multiple chapters
- Place earlier dependencies in multiple chapters if appropriate
- Consider creating a dedicated "foundations" chapter for deep dependency roots

### Challenge: Terminal Concepts

**Problem**: Some concepts have no dependents (nothing builds on them).

**Solutions**:
- Place terminal concepts at the end of related chapters
- Group terminal concepts into "Additional Topics" or "Special Topics" chapters
- Consider whether these concepts are truly necessary (but don't remove them without user approval)

### Challenge: Cluster Splitting

**Problem**: A natural concept cluster (e.g., 5 tree traversal algorithms) is too large for one chapter but splitting it feels wrong.

**Solutions**:
- Split into "Part 1" and "Part 2" chapters with clear continuation
- Use dependency relationships to find a natural split point
- Group by complexity (basic vs. advanced) or application domain

### Challenge: Uneven Distribution

**Problem**: The dependency structure forces 30 concepts into Chapter 2 and only 8 concepts into Chapter 7.

**Solutions**:
- Split the large chapter into two chapters
- Merge the small chapter with an adjacent chapter
- Revisit chapter boundaries to find better balance
- Adjust the total number of chapters

## Validation Checklist

Before finalizing the chapter structure, verify:

- [ ] All concepts from learning-graph.json are assigned to exactly one chapter
- [ ] No concept appears before any of its dependencies
- [ ] Chapter sizes are within acceptable range (8-25 concepts)
- [ ] Chapter titles are Title Case and ≤200 characters
- [ ] URL path names contain only lowercase letters and dashes
- [ ] All files follow the specified directory structure
- [ ] MkDocs navigation is correctly updated
- [ ] All markdown files have proper formatting (blank lines before lists, etc.)
- [ ] Each chapter index.md includes all required sections
- [ ] "Concepts Covered" is a table with `Concept` and `CIS Score` columns (not a numbered list)
- [ ] User has approved the chapter design

## Example Usage

**User request:**
"Create chapters for my Graph Theory textbook"

**Skill workflow:**
1. Read course-description.md, learning-graph.json, and concept-taxonomy.md
2. Analyze 200 concepts and their dependencies
3. Design 12 chapters with balanced content distribution
4. Present chapter outline to user:
   - Chapter 1: Introduction (15 concepts)
   - Chapter 2: Graph Representations (18 concepts)
   - ... etc.
5. Get user approval (y/n)
6. Create directory structure and all index.md files
7. Update mkdocs.yml navigation
8. Confirm completion

## Notes

- This skill only creates the **structure and outlines** for chapters
- It does NOT generate actual chapter content (that requires a separate skill)
- The "TODO: Generate Chapter Content" marker indicates where content should be added later
- Always preserve the concept list in each chapter index.md for use by content generation skills
- The per-concept CIS Score column is not decorative: `chapter-content-generator` reads it to size each concept's word-count target and non-text-element requirements (see `chapter-content-generator/SKILL.md`, "Elaboration Budget")
- **Always** strongly recommend a learning mascot before the user proceeds to chapter content generation (Step 4.6) — a mascot designed up front is placed into every chapter as content is written; adding one after the fact means retrofitting every already-generated chapter

---
name: glossary-generator
description: Generates a glossary from the learning graph's concept list with ISO 11179-compliant definitions (precise, concise, non-circular). Use after the learning graph concept list is finalized.
model: sonnet
license: 
metadata:
  ibook.version: "1.0"
---

# Glossary Generator

**Version:** 1.0

Generate a comprehensive glossary of terms from a learning graph's concept list with ISO 11179-compliant definitions.

## TOKEN EFFICIENCY WARNING

**This skill generates large files (2,000+ lines). Token cost matters far more than
wall-clock time for teacher users on limited budgets.**

**Default approach: ONE serial Task agent** that writes all definitions directly to
a temp file. This is the most token-efficient method because:

- System prompt / tool description overhead is paid only **once** (~12K tokens)
- No coordination or assembly overhead
- Proven to complete a 350-term glossary in **~31K tokens** (2026-03-14 benchmark)

### Measured Token Economics (350-term benchmark, 2026-03-14)

| Component | Tokens | Notes |
|-----------|--------|-------|
| Agent overhead (system prompt + tools) | ~12K | Paid once for serial, 4× for parallel |
| Definition generation (350 terms) | ~19K | Unavoidable LLM work |
| Assembly (Python script) | ~700 | Trivial programming task |
| **Total (serial)** | **~31K** | |

**Tokens per term: ~88 total, ~54 marginal** (after subtracting one-time overhead).

The marginal cost is calculated as: (30,788 − 12,000) / 350 = **~54 tokens/term**.
Use this to estimate costs for glossaries of any size:

| Glossary size | Estimated total tokens |
|---------------|----------------------|
| 100 terms | ~17K (12K overhead + 5.4K generation) |
| 200 terms | ~23K |
| 350 terms | ~31K (measured) |
| 500 terms | ~39K |

### Why Parallel Execution Should NEVER Be Used

Each parallel agent pays the full ~12K system prompt overhead independently.
For glossary generation, the definitions are completely independent — there is
no speedup benefit that justifies the cost. The serial agent writes all terms
in a single Write call and finishes in ~6 minutes, which is perfectly acceptable.

| Approach | Agent overhead | Generation | Assembly | Total | Waste |
|----------|---------------|------------|----------|-------|-------|
| **1 serial agent (recommended)** | ~12K (once) | ~19K | ~700 | **~31K** | — |
| 4 parallel agents + script | ~48K (4×) | ~19K | ~700 | **~68K** | +37K (119%) |
| 4 parallel agents + manual Edit | ~48K (4×) | ~19K | ~200K | **~267K** | +236K (761%) |

Parallel execution **more than doubles** the token cost for zero quality benefit.
For teachers on the Claude Pro plan (~200K token five-hour budget), the serial
approach uses ~16% of their budget vs. 34% (parallel) or 100%+ (manual assembly).

**NEVER use parallel agents for glossary generation. The token waste is not justified.**

**Always use the serial approach. Do not offer parallel as an option.**

The assembly step (sorting and writing the final file) MUST always use a Python
script — NEVER manually emit glossary content through Edit/Write tool calls.
See `logs/glossary-generation-very-inefficient.md` for the full post-mortem.

## Purpose

This skill automates glossary creation for intelligent textbooks by converting concept labels from a learning graph into properly formatted glossary definitions. Each definition follows ISO 11179 metadata registry standards: precise, concise, distinct, non-circular, and free of business rules. The skill ensures consistency across terminology, validates cross-references, and produces alphabetically ordered entries with relevant examples.

Following a short definition you may provide a discussion of why the term is important in the textbook and an example of how the term is used.

## When to Use This Skill

Use this skill after the Learning Graph skill has completed and the concept list has been finalized.  All markdown content in the /docs area can also be scanned looking for words or phases that might not be clear to the average high-school student.

The glossary relies on having a complete, reviewed list of concepts from the learning graph's concept enumeration phase. Specifically, trigger this skill when:

- A concept list file exists (typically `docs/learning-graph/02-concept-list-v1.md`)
- The concept list has been reviewed and approved
- The course description exists with clear learning outcomes
- Ready to create or update the textbook's glossary

## Workflow

### Step 1: Validate Input Quality

Before generating definitions, assess the quality of the concept list:

1. Read the concept list file (typically `docs/learning-graph/02-concept-list-v1.md`)
2. Check for duplicate concept labels (target: 100% unique)
3. Verify Title Case formatting (target: 95%+ compliance)
4. Validate length constraints (target: 98% under 32 characters)
5. Assess concept clarity (no ambiguous terms)

Calculate a quality score (1-100 scale):

- 90-100: All concepts unique, properly formatted, appropriate length
- 70-89: Most concepts meet standards, minor formatting issues
- 50-69: Some duplicate concepts or formatting inconsistencies
- Below 50: Significant issues requiring manual review

**User Dialog Triggers:**

- If score < 70: Ask "The concept list has quality issues. Would you like to review and clean it before generating the glossary?"
- If duplicates found: Ask "Found [N] duplicate concepts. Should I remove duplicates automatically or would you like to review?"
- If formatting issues: Ask "Found [N] concepts with formatting issues. Auto-fix?"

### Step 2: Read Course Context

Read the course description file (`docs/course-description.md`) and any other markdonw files in `/docs/**/*.md` to understand:

- Target audience (for appropriate example complexity)
- Course objectives (for terminology alignment)
- Prerequisites (for background knowledge assumptions)
- Learning outcomes (for context on concept usage)

### Step 3: Generate Definitions Using a Single Serial Agent

**Default approach (most token-efficient):** Launch ONE Task agent that generates
all definitions and writes them directly to a single temp file.

```
Task agent prompt:
"Generate ISO 11179-compliant glossary definitions for the following [N] terms.
Write ALL entries as markdown (#### headers with definitions, examples, and
discussion) to the file /tmp/glossary-raw.md using the Write tool.
Each entry uses #### for the term header. Do not return the content in your
response — just confirm the file was written and report the term count.

[Paste the full term list here]

[Paste course description context here for audience level]"
```

The single agent writes all definitions to one file. This pays system-prompt overhead
only once (~12K tokens) and avoids all coordination costs. Proven at **~31K tokens
for a 350-term glossary** (~88 tokens/term total, ~54 tokens/term marginal).

**Do NOT use parallel agents for glossary generation.** See the TOKEN EFFICIENCY
WARNING section above for why parallel execution should never be used — it more
than doubles the token cost for zero quality benefit.

For each concept in the list, create a definition that follows ISO 11179 standards:

**Precision (25 points):** Accurately capture the concept's meaning

- Define the concept specifically in the context of the course
- Use terminology appropriate for the target audience
- Ensure the definition matches how the concept is used in the course

**Conciseness (25 points):** Keep definitions brief (target: 20-50 words)

- Avoid unnecessary words or explanations
- Get to the core meaning quickly
- Use clear, direct language

**Distinctiveness (25 points):** Make each definition unique and distinguishable

- Avoid copying definitions from other sources
- Ensure no two definitions are too similar
- Highlight what makes this concept different from related concepts

**Non-circularity (25 points):** Avoid circular dependencies

- Do not reference undefined terms in definitions
- Do not create circular chains (A depends on B, B depends on A)
- Use simpler, more fundamental terms in definitions

**Example Format:**

For a concept "Learning Graph":

```markdown
#### Learning Graph

A directed graph of concepts that reflects the order that concepts should be learned to master a new concept.

Learning graphs are the foundational data structure use for intelligent textbooks.  They are used to guide
intelligent agents and recommend learning paths for students.

**Example:** In a programming course, the learning graph shows that "Variables" must be understood before "Functions," which must be understood before "Recursion."
```

### Step 4: Add Examples (60-80% of terms)

For most concepts (target: 60-80%), include a relevant example:

- Start with "**Example:**" (no newline after colon)
- Provide a concrete illustration from the course domain
- Keep examples brief (1-2 sentences)
- Ensure examples clarify the concept without adding confusion

### Step 5: Add Cross-References

Where appropriate, reference related terms:

- Use "See also:" for related concepts
- Use "Contrast with:" for opposing concepts
- Ensure all cross-referenced terms exist in the glossary
- Keep cross-references to 1-3 per term

### Step 6: Assemble Glossary File Using a Python Script

**CRITICAL: NEVER manually assemble the glossary through Edit/Write tool calls.**
Alphabetical sorting and file merging is a trivial programming task. Doing it manually
through LLM text generation wastes 100,000+ tokens that cost real money.

**MANDATORY APPROACH:** Write and execute a Python script via the Bash tool that:

1. Reads the agent output file(s) — `/tmp/glossary-raw.md` (serial) or `/tmp/glossary-part-*.md` (parallel)
2. Parses entries by splitting on `#### ` headers
3. Sorts entries alphabetically (case-insensitive) using `sorted()`
4. Writes the final `docs/glossary.md` in one pass

**Reference script (adapt paths as needed):**

```python
#!/usr/bin/env python3
"""Merge glossary parts into a single sorted glossary."""
import glob, os, re

entries = {}

# Support both serial (single file) and parallel (multiple files)
if os.path.exists('/tmp/glossary-raw.md'):
    sources = ['/tmp/glossary-raw.md']
else:
    sources = sorted(glob.glob('/tmp/glossary-part-*.md'))

for path in sources:
    with open(path) as f:
        content = f.read()
    for block in re.split(r'\n(?=#### )', content):
        block = block.strip()
        m = re.match(r'#### (.+)', block)
        if m:
            entries[m.group(1).strip()] = block

sorted_terms = sorted(entries.keys(), key=lambda t: t.lower())

with open('docs/glossary.md', 'w') as out:
    out.write('# Glossary of Terms\n\n')
    for term in sorted_terms:
        out.write(entries[term] + '\n\n')

print(f"Wrote {len(sorted_terms)} terms to docs/glossary.md")
```

Run this script with `python3 /tmp/assemble_glossary.py` via the Bash tool.
Total cost: ~500 tokens for the script + ~200 tokens for output = **~700 tokens**
(versus 200,000+ tokens if done manually through Edit calls).

**NEVER DO ANY OF THE FOLLOWING:**

- Write glossary entries directly through the Write or Edit tool
- Copy-paste subagent output into Edit tool old_string/new_string parameters
- Manually sort terms by emitting them in alphabetical order
- Append sections to the glossary file one at a time through Edit calls

**Formatting rules for the assembled file:**

- **ONLY level-4 headers (`####`) are allowed for glossary terms.** Do not use `##` section headers, `###` subheadings, or any other header level inside the glossary. The only `#` header in the file is the page title (`# Glossary of Terms`). Everything else is `####`.
- **Terms must ONLY be sorted alphabetically (case-insensitive). Never group terms by category, domain, or topic.** The glossary is a flat alphabetical list — no section dividers, no category headers, no thematic groupings. Alphabetical order is the only organizational principle.
- Do not put any `---` strings in the glossary. They are not needed.
- Use "**Example:**" for examples (bold, with colon)
- Maintain consistent spacing between entries (one blank line between entries)

### Step 7: Generate Quality Report

Create `docs/learning-graph/glossary-quality-report.md` with:

**ISO 11179 Metadata Registry Compliance Metrics:**

For each definition, score on 5 criteria (25 points each):

1. Precision: Does it accurately capture the meaning?
2. Conciseness: Is it brief (20-50 words)?
3. Distinctiveness: Is it unique and distinguishable?
4. Non-circularity: No circular dependencies?
5. Unencumbered by business rules: Free of specific policies or rules?

**Overall Quality Metrics:**

- Average definition length: [X] words
- Definitions meeting all 4 criteria: [X]%
- Circular definitions found: [X]
- Example coverage: [X]%
- Cross-references: [X] total, [X] broken

**Readability:**

- Flesch-Kincaid grade level: [X]
- Appropriate for target audience: Yes/No

**Recommendations:**

- List any definitions scoring < 70/100
- Identify circular dependencies to fix
- Suggest concepts needing examples
- Note any broken cross-references

### Step 8: Validate Output

Perform final validation:

1. Verify alphabetical ordering (100% compliance required)
2. Check all cross-references point to existing terms
3. Ensure all concepts from input list are included
4. Validate markdown syntax renders correctly
5. Confirm no circular definitions exist

**Success Criteria:**

- Overall quality score > 85/100
- Zero circular definitions
- 100% alphabetical ordering
- All terms from concept list included
- Markdown renders correctly in mkdocs

### Step 9: Update Navigation (Optional)

If `- Glossary: glossary.md` is not yet in the `nav:` of `mkdocs.yml`, add it
near the end (before License/Contact), following the canonical nav-editing
rules in `$BK_HOME/skills/book-installer/references/mkdocs-nav-editing.md`.

### Step 10: Generate Cross-Reference Index (Optional)

Create `docs/learning-graph/glossary-cross-ref.json` for semantic search:

```json
{
  "terms": [
    {
      "term": "Learning Graph",
      "related_terms": ["Concept Dependency", "Directed Acyclic Graph"],
      "contrasts_with": ["Linear Curriculum"],
      "category": "Educational Technology"
    }
  ]
}
```

This JSON file enables future features like:

- Semantic search across glossary
- Concept relationship visualization
- Automated suggestion of related terms

## Quality Scoring Reference

Use this rubric to score each definition (1-100 scale):

**85-100: Excellent**

- Meets all 4 ISO 11179 criteria (20+ pts each)
- Appropriate length (20-50 words)
- Includes relevant example
- Clear, unambiguous language
- No circular dependencies

**70-84: Good**

- Meets 3-4 ISO criteria
- Acceptable length (15-60 words)
- May lack example
- Generally clear
- No serious issues

**55-69: Adequate**

- Meets 2-3 ISO criteria
- Length issues (too short or too long)
- Missing example where helpful
- Some ambiguity
- Minor circular references

**Below 55: Needs Revision**

- Fails multiple ISO criteria
- Serious length issues
- Confusing or circular
- Missing context
- Requires complete rewrite

## Common Pitfalls to Avoid

**Circular Definitions:**

- Bad: "A Learning Graph is a graph that shows learning."
- Good: "A directed graph of concepts that reflects the order concepts should be learned."

**Too Vague:**

- Bad: "A thing used in education."
- Good: "A directed graph of concepts that reflects prerequisite relationships."

**Too Long:**

- Bad: "A learning graph is a specialized type of directed acyclic graph structure commonly used in educational technology and instructional design contexts to represent the hierarchical and sequential relationships between different conceptual elements that students need to master in order to achieve specific learning outcomes."
- Good: "A directed graph of concepts that reflects the order concepts should be learned to master a new concept."

**Business Rules:**

- Bad: "Students must complete prerequisites before advancing to dependent concepts."
- Good: "A directed graph showing prerequisite relationships between concepts."

**Undefined Terms:**

- Bad: "Uses a DAG structure" (if DAG not in glossary)
- Good: "Uses a directed acyclic graph structure"

## Output Files Summary

**Required:**

1. `docs/glossary.md` - Complete glossary in alphabetical order with ISO 11179-compliant definitions

**Recommended:**

2. `docs/learning-graph/glossary-quality-report.md` - Quality assessment and recommendations

**Optional:**

3. `docs/learning-graph/glossary-cross-ref.json` - JSON mapping for semantic search
4. Updates to `mkdocs.yml` navigation if glossary link missing

## Example Session

**User:** "Generate a glossary from my concept list"

**Claude (using this skill):**

1. Reads concept list file and `docs/course-description.md` (~5K tokens)
2. Validates quality (checks for duplicates, formatting) (~1K tokens)
3. Launches ONE serial Task agent that writes all definitions to `/tmp/glossary-raw.md` (~19K tokens)
4. Writes a Python assembly script to `/tmp/assemble_glossary.py` (~500 tokens)
5. Runs the script via Bash — it parses, sorts, and writes `docs/glossary.md` (~200 tokens)
6. Verifies term count with `grep -c "^####" docs/glossary.md` (~100 tokens)
7. Updates `mkdocs.yml` navigation if needed (~500 tokens)
8. Reports: "Created glossary with 350 terms. Added examples to 70% of terms."

**Measured result (2026-03-14):** 350 terms generated and assembled in **~31K total tokens**.
At ~88 tokens/term (or ~54 tokens/term after subtracting agent overhead), this is
the most efficient approach possible.

**REMEMBER:** The subagent generates text (unavoidable LLM work). The assembly is
a programming task — use `sorted()`, not the Edit tool. NEVER use parallel agents.

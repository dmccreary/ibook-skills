---
name: quiz-generator
description: Generates multiple-choice quiz questions for each chapter, aligned to the learning graph and distributed across Bloom's Taxonomy levels. Use after chapter content and the learning graph both exist.
license: Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
model: sonnet
metadata:
  ibook.version: "0.5"
---

# Quiz Generator for Intelligent Textbooks

**Version:** 0.5

## Overview
1. For each markdown chapter, generate interactive multiple-choice quizzes for textbook chapters with quality distractor analysis.
2. Generate quality reports in markdown format.
3. Update mkdocs.yml navigation to include quizzes and reports.

## Purpose

This skill automates quiz creation for intelligent textbooks by analyzing chapter content to generate contextually relevant multiple-choice questions. Each quiz is aligned to specific concepts from the learning graph, distributed across Bloom's Taxonomy cognitive levels, and formatted using mkdocs-material question admonition format with upper-alpha (A, B, C, D) answer choices. The skill ensures quality distractors, balanced answer distribution, and comprehensive explanations for educational value.

## When to Use This Skill

Use this skill after:

1. Chapter content has been generated or written (1000+ words per chapter)
2. Learning graph exists with concept dependencies
3. Glossary is available (recommended for terminology questions)

Trigger this skill when:

- Creating quizzes for new chapters
- Updating quizzes after content revisions
- Building comprehensive quiz bank for entire textbook
- Exporting quiz data for LMS or chatbot integration

## Token Efficiency: Serial Execution Only

!!! warning "NEVER Use Parallel Agents Unless the User Explicitly Requests It"
    **Always use a single serial agent for quiz generation.** This is a hard
    requirement, not a suggestion. Do not offer parallel execution as an option.

Each spawned agent incurs ~12,000 tokens of startup overhead (system prompt,
tool schemas, project context). Parallel execution multiplies this overhead
with zero quality benefit. Measured data from a 17-chapter quiz generation:

| Approach | System Overhead | Total Tokens | Waste |
|----------|----------------|--------------|-------|
| **Serial (1 agent)** | ~12,000 | ~310,000 | — |
| Parallel (4 agents) | ~48,000 | ~358,000 | +48,000 (13%) |

Additional problems with parallel execution observed in production:

1. **Inconsistent behavior:** Agents independently choose different strategies,
   causing 5x variation in tool calls (8 vs 39) for the same workload
2. **Conflicting file edits:** Multiple agents modifying mkdocs.yml simultaneously
   causes inconsistencies requiring manual repair
3. **No shared learning:** Each agent starts from scratch with no accumulated
   context from earlier chapters

The skill supports two modes:
- **Serial mode** (default, always): One agent processes all chapters sequentially
- **Single chapter mode**: Generate quiz for one specific chapter

## Workflow

### Phase 1: Setup (Sequential)

This phase runs once before quiz generation, reading shared context.

#### Step 1.1: Capture Start Time

```bash
date "+%Y-%m-%d %H:%M:%S"
```

Log the start time for the session report.

#### Step 1.2: Indicate Skill Running

Notify the user: "Quiz Generator Skill v0.5 running in serial mode."

#### Step 1.3: Read Shared Context

Read and cache these files for all agents:

1. **Course Description** (`docs/course-description.md`)
   - Extract target audience and reading level
   - Note Bloom's Taxonomy learning outcomes

2. **Learning Graph** (`docs/learning-graph/learning-graph.csv` or similar)
   - Load concept list with dependencies
   - Calculate concept centrality for prioritization

3. **Glossary** (`docs/glossary.md`)
   - Load term definitions for terminology questions
   - Note which concepts have glossary entries

4. **Chapter List** (scan `docs/chapters/` directory)
   - Enumerate all chapter directories
   - Count words per chapter for readiness assessment

#### Step 1.4: Assess Content Readiness

Calculate content readiness score (1-100) for each target chapter:

**Quality Checks:**

##### 1. **Chapter word count:**
   - 2000+ words = excellent (20 pts)
   - 1000-1999 words = good (15 pts)
   - 500-999 words = basic (10 pts)
   - <500 words = insufficient (5 pts)

##### 2. **Example coverage:**
   - 60%+ concepts with examples = excellent (20 pts)
   - 40-59% = good (15 pts)
   - 20-39% = basic (10 pts)
   - <20% = insufficient (5 pts)

##### 3. **Glossary coverage:**
   - 80%+ chapter concepts defined = excellent (20 pts)
   - 60-79% = good (15 pts)
   - 40-59% = basic (10 pts)
   - <40% = insufficient (5 pts)

##### 4. **Concept clarity:**
   - Clear explanations for all concepts (20 pts)
   - Most concepts clear (15 pts)
   - Some unclear concepts (10 pts)
   - Many unclear concepts (5 pts)

##### 5. **Learning graph alignment:**
   - All chapter concepts mapped (20 pts)
   - Most mapped (15 pts)
   - Some mapped (10 pts)
   - Few mapped (5 pts)

**Content Readiness Ranges:**

- 90-100: Rich content, excellent quiz quality possible
- 70-89: Good content, solid quiz possible
- 50-69: Basic content, limited quiz possible
- Below 50: Insufficient content for quality quiz

**User Dialog Triggers:**

- Score < 60: Ask "Chapter [X] has limited content ([N] words). Generate shorter quiz or skip?"
- No glossary: Ask "No glossary found. Definition questions will be limited. Proceed?"
- Concept gaps: Ask "[N] concepts in chapter not in learning graph. Continue with available concepts?"
- No learning outcomes: Ask "No Bloom's Taxonomy outcomes in course description. Use default distribution?"

### Phase 2: Quiz Generation (Serial)

Launch ONE agent that processes all chapters sequentially. The agent reads each
chapter, generates 10 questions, and writes the quiz file before moving to the
next chapter. This pays the ~12K system prompt overhead only once.

**Agent Prompt Template:**

```
You are generating quizzes for an intelligent textbook. Generate quizzes for
ALL of the following chapters, processing them one at a time.

COURSE CONTEXT:
- Course: [course name]
- Target audience: [audience]
- Reading level: [level]

BLOOM'S TAXONOMY TARGETS:
- Introductory chapters (1-3): 40% Remember, 40% Understand, 15% Apply, 5% Analyze
- Intermediate chapters (4-N): 25% Remember, 30% Understand, 30% Apply, 15% Analyze
- Advanced chapters: 15% Remember, 20% Understand, 25% Apply, 25% Analyze, 10% Evaluate, 5% Create

CHAPTERS TO PROCESS:
[List ALL chapter directories with full paths]

FOR EACH CHAPTER:
1. Read the chapter content at the index.md file
2. Identify the key concepts covered in that chapter
3. Generate exactly 10 questions following the format below
4. Ensure answer balance: A (2-3), B (2-3), C (2-3), D (2-3)
5. Write the quiz to docs/chapters/[chapter-dir]/quiz.md

QUIZ FORMAT - Each question MUST follow this exact format:

#### [N]. [Question text ending with ?]

<div class="upper-alpha" markdown>
1. [Option A text]
2. [Option B text]
3. [Option C text]
4. [Option D text]
</div>

??? question "Show Answer"
    The correct answer is **[LETTER]**. [Explanation 50-100 words]

    **Concept Tested:** [Concept Name]

---

QUIZ FILE STRUCTURE:
# Quiz: [Chapter Title]

Test your understanding of [topic] with these review questions.

---

[Questions 1-10 following the format above]

REPORT when done:
- Chapter name
- Number of questions
- Bloom's distribution (R:#, U:#, Ap:#, An:#)
- Answer distribution (A:#, B:#, C:#, D:#)
```

### Phase 2 Steps (Per Chapter)

#### Step 2: Determine Target Distribution

Based on chapter type (introductory, intermediate, advanced), set target Bloom's Taxonomy distribution:

**Introductory Chapters (typically chapters 1-3):**
- 40% Remember
- 40% Understand
- 15% Apply
- 5% Analyze
- 0% Evaluate
- 0% Create

**Intermediate Chapters:**
- 25% Remember
- 30% Understand
- 30% Apply
- 15% Analyze
- 0% Evaluate
- 0% Create

**Advanced Chapters:**
- 15% Remember
- 20% Understand
- 25% Apply
- 25% Analyze
- 10% Evaluate
- 5% Create

Determine chapter type by:
- Position in textbook (first 3 chapters = introductory)
- Concept centrality in learning graph (high centrality = advanced)
- Explicit markers in chapter metadata
- User specification

Target question count: 8-12 per chapter (default: 10)

#### Step 3: Identify Concepts to Test

Analyze chapter content and learning graph to prioritize concepts:

**Priority 1 (Must Test):**
- High-centrality concepts in learning graph
- Concepts mentioned in chapter title or introduction
- Concepts with dedicated sections
- Key terms emphasized in bold or glossary links

**Priority 2 (Should Test):**
- Supporting concepts with substantial explanation
- Concepts with examples
- Prerequisites reviewed in chapter
- Concepts from learning objectives

**Priority 3 (May Test):**
- Peripheral concepts mentioned briefly
- Related concepts for context
- Future topics previewed

Aim for 80%+ coverage of Priority 1 concepts.

#### Step 4: Generate Questions by Bloom's Level

For each concept selected for testing, generate question at appropriate Bloom's level following target distribution. For per-level action verbs and question-writing guidance, read the canonical reference `$HOME/.claude/skills/chapter-content-generator/references/blooms-taxonomy.md`.

**IMPORTANT FORMATTING REQUIREMENT:**

All questions MUST use the mkdocs-material question admonition format with upper-alpha list styling:

```markdown
#### 1. What is the primary purpose of a learning graph?

<div class="upper-alpha" markdown>
1. To create visual decorations for textbooks
2. To map prerequisite relationships between concepts
3. To generate random quiz questions
4. To organize files in a directory structure
</div>

??? question "Show Answer"
    The correct answer is **B**. A learning graph is a directed graph that maps prerequisite relationships between concepts, showing which concepts must be learned before others. This ensures proper scaffolding in educational content.

    **Concept Tested:** Learning Graph

    **See:** [Learning Graph Concept](../concepts/learning-graph.md)
```

**Formatting Rules:**

1. Use level-4 header (####) with question number
2. Write question as complete sentence ending with ?
3. Use `<div class="upper-alpha" markdown>` wrapper
4. Write 4 answer options as numbered list (1, 2, 3, 4)
5. Use `??? question "Show Answer"` admonition
6. Indent answer content with 4 spaces
7. Start with "The correct answer is **[LETTER]**."
8. Include concept name and link to source
9. Maintain blank line before and after div

**Question Writing Guidelines:**

**Remember Level:**
- Ask for definitions from glossary
- Test fact recall
- Identify terminology
- Example: "What is the definition of [concept]?"

**Understand Level:**
- Ask for explanations
- Test comprehension of relationships
- Compare/contrast concepts
- Example: "Which best describes the relationship between [A] and [B]?"

**Apply Level:**
- Present scenarios requiring concept application
- Test problem-solving using learned methods
- Example: "Given [scenario], which approach would you use?"

**Analyze Level:**
- Ask to identify patterns or causes
- Test ability to break down concepts
- Example: "What is the underlying reason for [phenomenon]?"

**Evaluate Level:**
- Ask for judgments based on criteria
- Test critical thinking
- Example: "Which approach would be most effective for [goal]?"

**Create Level:**
- Ask to design solutions
- Test synthesis of concepts
- Example: "How would you design a [system] that [requirements]?"

#### Step 5: Write Quality Distractors

For each incorrect answer option (distractors), ensure:

**Plausibility:**
- Sounds reasonable to someone who hasn't learned the material
- Uses related terminology
- Avoids obviously wrong answers
- Similar length to correct answer

**Educational Value:**
- Addresses common misconceptions
- Tests understanding of related concepts
- Discriminates between levels of knowledge
- Not trick questions or word games

**Common Distractor Patterns:**

- Partial truth (correct in different context)
- Reversal (opposite of correct answer)
- Similar terminology (related but distinct concept)
- Common error (typical student mistake)

**Avoid:**
- "All of the above" or "None of the above"
- Jokes or nonsensical options
- Grammatically inconsistent options
- Answers that overlap or both could be correct

#### Step 6: Write Explanations

For each question, write explanation that:

**Confirms Correct Answer:**
- State clearly: "The correct answer is **[LETTER]**."
- Explain why this answer is correct
- Reference chapter content or concept definition
- Target: 50-100 words

**Teaches (Optional but Recommended):**
- Briefly explain why distractors are incorrect
- Clarify common misconceptions
- Provide additional context
- Link to chapter section for more detail

**Example Explanation:**

```
The correct answer is **B**. A learning graph is a directed graph that maps
prerequisite relationships between concepts. Option A is incorrect because
learning graphs serve a structural purpose, not decorative. Option C is
incorrect because quiz generation is not the primary purpose. Option D
confuses learning graphs with file systems.

**Concept Tested:** Learning Graph

**See:** [Learning Graph Concept](../concepts/learning-graph.md#definition)
```

#### Step 7: Ensure Answer Balance

Check that correct answers are distributed evenly across A, B, C, D:

**Target Distribution:**
- A: 25% (±5%)
- B: 25% (±5%)
- C: 25% (±5%)
- D: 25% (±5%)

**Avoid Patterns:**
- All C's in a row
- Alternating A-B-A-B
- Predictable sequences
- Position bias (first/last always correct)

**Randomization Strategy:**
- Generate random sequence before writing quiz
- Shuffle for each question
- Verify distribution after completion
- Adjust if imbalanced

#### Step 8: Create Quiz File

Generate quiz file with proper structure:

**Separate Quiz File** (`docs/chapters/[chapter-name]/quiz.md`):

```markdown
# Quiz: [Chapter Name]

Test your understanding of [chapter topic] with these questions.

---

#### 1. [Question text]?

<div class="upper-alpha" markdown>
1. [Option 1]
2. [Option 2]
3. [Option 3]
4. [Option 4]
</div>

??? question "Show Answer"
    The correct answer is **[LETTER]**. [Explanation]

    **Concept Tested:** [Concept Name]

---

#### 2. [Question text]?

[Continue for all questions...]
```

**Formatting Requirements:**
- Use horizontal rules (---) between questions
- Number questions sequentially (1, 2, 3...)
- Maintain consistent spacing
- Ensure all markdown renders correctly

### Phase 3: Aggregation

After the serial agent completes, collect its results:
- List of quiz files created
- Per-chapter statistics (questions, Bloom's distribution, answer balance)
- Any errors or issues encountered

#### Step 10: Generate Metadata Files (Optional)

Create `docs/learning-graph/quizzes/[chapter-name]-quiz-metadata.json` for each chapter:

```json
{
  "chapter": "Chapter Name",
  "chapter_file": "docs/chapters/chapter-name/index.md",
  "quiz_file": "docs/chapters/chapter-name/quiz.md",
  "generated_date": "YYYY-MM-DD",
  "total_questions": 10,
  "content_readiness_score": 85,
  "overall_quality_score": 78,
  "questions": [
    {
      "id": "ch1-q001",
      "number": 1,
      "question_text": "What is the primary purpose of a learning graph?",
      "correct_answer": "B",
      "bloom_level": "Understand",
      "difficulty": "medium",
      "concept_tested": "Learning Graph",
      "source_link": "../concepts/learning-graph.md",
      "distractor_quality": 0.85,
      "explanation_word_count": 67
    }
  ],
  "answer_distribution": {
    "A": 2,
    "B": 3,
    "C": 3,
    "D": 2
  },
  "bloom_distribution": {
    "Remember": 2,
    "Understand": 4,
    "Apply": 3,
    "Analyze": 1,
    "Evaluate": 0,
    "Create": 0
  },
  "concept_coverage": {
    "total_concepts": 12,
    "tested_concepts": 10,
    "coverage_percentage": 83
  }
}
```

#### Step 11: Generate Quiz Bank (Aggregate)

Create or update `docs/learning-graph/quiz-bank.json` with all questions:

```json
{
  "textbook_title": "Building Intelligent Textbooks",
  "generated_date": "YYYY-MM-DD",
  "total_chapters": 20,
  "total_questions": 187,
  "questions": [
    {
      "id": "ch1-q001",
      "chapter": "Introduction to Learning Graphs",
      "question_text": "What is the primary purpose of a learning graph?",
      "options": {
        "A": "To create visual decorations for textbooks",
        "B": "To map prerequisite relationships between concepts",
        "C": "To generate random quiz questions",
        "D": "To organize files in a directory structure"
      },
      "correct_answer": "B",
      "explanation": "A learning graph is a directed graph...",
      "bloom_level": "Understand",
      "difficulty": "medium",
      "concept": "Learning Graph",
      "chapter_file": "docs/concepts/learning-graph.md",
      "source_section": "#definition",
      "tags": ["graph", "prerequisites", "scaffolding"]
    }
  ]
}
```

**Use Cases for Quiz Bank:**
- LMS export (Moodle, Canvas, Blackboard XML)
- Quiz randomization (select subset)
- Alternative quiz versions
- Chatbot integration (practice questions)
- Study app integration

#### Step 12: Generate Quality Report

Create `docs/learning-graph/quiz-generation-report.md`:

```markdown
# Quiz Generation Quality Report

Generated: YYYY-MM-DD
Execution Mode: Serial (1 agent)
Wall-clock Time: X minutes Y seconds

## Overall Statistics

- **Total Chapters:** 20
- **Total Questions:** 187
- **Avg Questions per Chapter:** 9.4
- **Overall Quality Score:** 76/100

## Per-Chapter Summary

| Chapter | Questions | Quality Score | Bloom's Score | Coverage |
|---------|-----------|---------------|---------------|----------|
| Ch 1: Introduction | 10 | 82/100 | 24/25 | 83% |
| Ch 2: Learning Graphs | 12 | 78/100 | 22/25 | 90% |
| ... | ... | ... | ... | ... |

## Bloom's Taxonomy Distribution (Overall)

| Level | Actual | Target | Deviation |
|-------|--------|--------|-----------|
| Remember | 22% | 25% | -3% ✓ |
| Understand | 28% | 30% | -2% ✓ |
| Apply | 27% | 25% | +2% ✓ |
| Analyze | 18% | 15% | +3% ✓ |
| Evaluate | 4% | 4% | 0% ✓ |
| Create | 1% | 1% | 0% ✓ |

**Bloom's Distribution Score:** 24/25 (excellent)

## Answer Balance (Overall)

- A: 24% (45/187)
- B: 26% (49/187)
- C: 25% (47/187)
- D: 25% (46/187)

**Answer Balance Score:** 15/15 (perfect distribution)

## Recommendations

[Include recommendations based on aggregated data]
```

#### Step 13: Validate Quality

Perform comprehensive validation across all generated quizzes:

**1. No Ambiguity:**
- Each question has exactly one defensible correct answer
- Question stem is clear and complete
- No grammatical errors

**2. Distractor Quality:**
- All wrong answers are plausible
- Distractors test understanding, not just guessing
- Similar length and grammatical structure
- No overlapping answers

**3. Grammar & Clarity:**
- Professional writing throughout
- Consistent verb tense
- Proper punctuation
- No typos

**4. Answer Balance:**
- Correct answers distributed across A, B, C, D
- Within 20-30% per option (target: 25%)
- No predictable patterns

**5. Bloom's Distribution:**
- Matches target for chapter type
- Within ±15% acceptable
- Progressive difficulty through quiz

**6. Concept Coverage:**
- 75%+ of major concepts tested
- Important concepts have multiple questions
- No over-testing trivial concepts

**7. No Duplicates:**
- Unique questions across all quizzes
- No near-duplicates (>80% similar)

**8. Explanation Quality:**
- All questions have explanations
- Explanations teach, not just confirm
- 50-100 words target
- Reference chapter sections

**9. Link Validation:**
- All source links point to existing content
- Use section anchors where appropriate
- Links render correctly
- Do not place links in quiz.md files that do not work
- Do not use link labels to sections that do not exist

**10. Bias Check:**
- No cultural bias
- No gender bias
- No assumptions about background
- Accessible language

**Success Criteria:**
- Overall quality score > 70/100
- 8-12 questions per chapter
- Bloom's distribution within ±15% of target
- 75%+ concept coverage
- Answer balance within 20-30% per option
- 100% questions have explanations
- No duplicate questions
- All links valid

#### Step 14: Update Site Navigation

Nest a `Quiz:` entry under each chapter in `mkdocs.yml`, and add the
`Quiz Generation Report:` under `Learning Graph:`. Follow the canonical
nav-editing rules in
`$HOME/.claude/skills/book-installer/references/mkdocs-nav-editing.md` —
in particular: read-before-write, **serialize nav edits when quizzes are
generated for many chapters in parallel** (apply all nav changes in one edit
at the end), label the chapter page `Content:`, and never put the string
"Chapter" in the label:

```yml
    - 1. Introduction to AI and Intelligent Textbooks:
      - Content: chapters/01-intro-ai-intelligent-textbooks/index.md
      - Quiz: chapters/01-intro-ai-intelligent-textbooks/quiz.md
```

#### Step 15: Capture End Time and Write Session Log

Capture the end time:

```bash
date "+%Y-%m-%d %H:%M:%S"
```

Export the session information to `logs/quiz-generator-YYYY-MM-DD.md`:

```markdown
# Quiz Generator Session Log

**Skill Version:** 0.4
**Date:** YYYY-MM-DD
**Execution Mode:** Serial (1 agent)

## Timing

| Metric | Value |
|--------|-------|
| Start Time | YYYY-MM-DD HH:MM:SS |
| End Time | YYYY-MM-DD HH:MM:SS |
| Elapsed Time | X minutes Y seconds |

## Token Usage

| Phase | Estimated Tokens |
|-------|------------------|
| Setup (shared context) | ~15,000 |
| Serial agent (all chapters) | ~295,000 |
| Aggregation + nav update | ~5,000 |
| **Total** | ~315,000 |

## Results

- Total chapters: N
- Total questions: N × 10
- Quality score: XX/100
- All quizzes written successfully: Yes/No

## Files Created

[List all quiz.md files and report files]
```

#### Step 16: Notify User

Notify the user:

"Quiz Generator v0.5 complete!

- **Mode:** Serial (1 agent)
- **Elapsed time:** X minutes Y seconds
- **Chapters processed:** 23
- **Questions generated:** 230
- **Quality score:** 82/100

The site navigation in `mkdocs.yml` has been updated to include Content/Quiz links for each chapter and the quiz generation report in the learning-graph section.

Session logged to `logs/quiz-generator-YYYY-MM-DD.md`"

## Question Format Reference

### Complete Example with All Elements

```markdown
#### 3. Given a course with 50 concepts, what is the most important factor in organizing the learning graph?

<div class="upper-alpha" markdown>
1. Alphabetical order of concept names
2. Prerequisite relationships between concepts
3. The length of concept definitions
4. The visual appearance of the graph diagram
</div>

??? question "Show Answer"
    The correct answer is **B**. Prerequisite relationships are the most important factor because they determine the order in which concepts must be learned. A learning graph maps these dependencies to ensure students learn foundational concepts before advanced ones. Alphabetical order (A) and visual appearance (D) are organizational preferences, not educational requirements. Definition length (C) does not affect concept sequencing.

    **Concept Tested:** Learning Graph Structure

    **See:** [Learning Graph](../concepts/learning-graph.md#prerequisites)
```

### Formatting Checklist

- [ ] Level-4 header with question number
- [ ] Complete sentence ending with ?
- [ ] `<div class="upper-alpha" markdown>` wrapper
- [ ] Numbered list (1, 2, 3, 4) for options
- [ ] Closing `</div>` tag
- [ ] `??? question "Show Answer"` admonition
- [ ] 4-space indentation in answer block
- [ ] "The correct answer is **[LETTER]**." statement
- [ ] Explanation (50-100 words)
- [ ] **Concept Tested:** label
- [ ] **See:** link with proper path
- [ ] Blank lines before and after div

## Common Pitfalls to Avoid

**Format Errors:**
- ❌ Forgetting `<div class="upper-alpha" markdown>` wrapper
- ❌ Using letters (A, B, C, D) instead of numbers in list
- ❌ Incorrect indentation in answer block
- ❌ Missing closing `</div>` tag

**Question Quality:**
- ❌ Ambiguous questions with multiple correct answers
- ❌ "All of the above" or "None of the above" options
- ❌ Trick questions or word games
- ❌ Questions testing trivial facts

**Distractor Quality:**
- ❌ Obviously wrong answers
- ❌ Joke options or nonsense
- ❌ Distractors much longer/shorter than correct answer
- ❌ Options that overlap or contradict

**Explanation Quality:**
- ❌ Just restating the question
- ❌ No teaching value
- ❌ Missing or broken links
- ❌ Too brief (< 30 words) or too long (> 150 words)

**Token Efficiency:**
- ❌ Using parallel agents (wastes ~12K tokens per extra agent in system prompt overhead)
- ❌ Spawning multiple agents when a single serial agent would produce the same output
- ❌ Offering parallel execution as an option without the user explicitly requesting it

## Output Files Summary

**Required (Per Chapter):**
1. Quiz markdown file: `docs/chapters/[chapter-name]/quiz.md`

**Recommended (Aggregate):**
2. `docs/learning-graph/quiz-generation-report.md` - Quality metrics
3. `logs/quiz-generator-YYYY-MM-DD.md` - Session log with timing

**Optional:**
4. `docs/learning-graph/quiz-bank.json` - All questions database
5. `docs/learning-graph/quizzes/[chapter-name]-quiz-metadata.json` - Per-chapter metadata
6. Navigation updates to `mkdocs.yml`

## Example Session

### All Chapters (Default Serial Mode)

**User:** "Generate quizzes for all chapters"

**Claude (using this skill):**

1. Captures start time
2. Notifies: "Quiz Generator Skill v0.5 running in serial mode."
3. Reads shared context (course description, learning graph, glossary)
4. Scans chapter directories, finds 23 chapters
5. Assesses content readiness (all chapters 2000+ words)
6. Launches ONE serial agent that processes all 23 chapters sequentially
7. Agent reads each chapter, generates 10 questions, writes quiz.md, then moves to next
8. Collects results from the single agent
9. Generates quality report (score: 82/100)
10. Updates mkdocs.yml navigation
11. Captures end time
12. Writes session log
13. Reports: "Quiz Generator v0.5 complete! Mode: Serial. Time: 33m. Questions: 230. Quality: 82/100."

### Single Chapter Mode

**User:** "Generate a quiz for Chapter 3 only"

**Claude (using this skill):**

1. Assesses Chapter 3 content readiness (score: 82/100)
2. Determines chapter type: intermediate
3. Sets target distribution: 25% Remember, 30% Understand, 30% Apply, 15% Analyze
4. Identifies 12 concepts to test (10 priority 1, 2 priority 2)
5. Generates 10 questions using question admonition format
6. Creates quality distractors
7. Ensures answer balance (A: 2, B: 3, C: 3, D: 2)
8. Writes explanations without links unless verified
9. Writes quiz to `docs/chapters/03-chapter-name/quiz.md`
10. Reports: "Created 10-question quiz for Chapter 3. Quality score: 78/100."

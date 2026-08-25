<!-- Canonical copy. Do not fork into other skills; reference by path:
     $BK_HOME/skills/chapter-content-generator/references/blooms-taxonomy.md

     `$BK_HOME` points at the ibook-skills checkout and is agent-neutral.
     Do NOT use a path under `~/.claude/skills/`, `~/.codex/skills/`, or
     `~/.gemini/antigravity/skills/` — each is specific to one agent
     framework, and these skills run on all of them. If `$BK_HOME` is
     unset, the file is at
     `chapter-content-generator/references/blooms-taxonomy.md` relative to
     the skills root that contains the calling skill. -->

# Bloom's Taxonomy (2001 Revision) — Canonical Reference

Shared by chapter-content-generator (learning objectives), faq-generator
(question distribution), and quiz-generator (question levels). Merged from
the former `bloom-taxonomy-verbs.md` and `blooms-taxonomy-guide.md`.

## Part 1: Action Verbs by Level

## Remember (L1)
list, define, recall, identify, name, recognize, locate, describe

## Understand (L2)
explain, summarize, interpret, classify, compare, contrast, exemplify, infer

## Apply (L3)
use, execute, implement, solve, demonstrate, calculate, apply, practice

## Analyze (L4)
differentiate, organize, attribute, compare, contrast, examine, deconstruct, distinguish

## Evaluate (L5)
judge, critique, assess, justify, prioritize, recommend, validate, defend

## Create (L6)
design, construct, develop, formulate, compose, produce, invent, generate

## Part 2: Writing Questions at Each Level

The guidance below was written for FAQ generation; the question starters,
characteristics, and level distinctions apply equally to quiz questions.

## The Six Cognitive Levels

### 1. Remember (Knowledge)

**Definition:** Recall facts, terms, basic concepts, and answers.

**Cognitive Actions:**
- Define, duplicate, list, memorize, recall, repeat, reproduce, state

**Question Starters:**
- "What is...?"
- "What does [term] mean?"
- "What are the components of...?"
- "Can you list...?"
- "What are the main...?"

**FAQ Examples:**

✓ "What is a Learning Graph?"
✓ "What does MicroSim mean?"
✓ "What are the five levels of intelligent textbooks?"
✓ "What is the ISO 11179 standard?"

**Answer Characteristics:**
- Factual, straightforward
- Draws from glossary or definitions
- 50-150 words
- May reference source for more detail

**Target Distribution in FAQ:** 20%

---

### 2. Understand (Comprehension)

**Definition:** Explain ideas or concepts; demonstrate understanding of facts and ideas.

**Cognitive Actions:**
- Classify, describe, discuss, explain, identify, locate, recognize, report, select, translate

**Question Starters:**
- "How would you explain...?"
- "Why is [concept] important?"
- "What is the difference between...?"
- "How does [concept] work?"
- "Can you summarize...?"
- "What is the main idea of...?"

**FAQ Examples:**

✓ "Why are learning graphs important for textbook design?"
✓ "What is the difference between a glossary and an index?"
✓ "How does scaffolding improve learning outcomes?"
✓ "What's the relationship between Bloom's Taxonomy and question difficulty?"

**Answer Characteristics:**
- Explanatory, contextual
- May compare/contrast concepts
- Often includes "because" or "in order to"
- 100-250 words
- Examples help clarify

**Target Distribution in FAQ:** 30%

---

### 3. Apply (Application)

**Definition:** Use information in new situations; solve problems using required skills or knowledge.

**Cognitive Actions:**
- Apply, build, choose, construct, develop, implement, interview, make use of, organize, solve, utilize

**Question Starters:**
- "How would you use...?"
- "What examples can you find...?"
- "How would you solve...?"
- "How would you show...?"
- "What approach would you use to...?"
- "How would you apply...?"

**FAQ Examples:**

✓ "How do I create a learning graph for my course?"
✓ "What's the best way to use MicroSims in my chapters?"
✓ "How can I apply Bloom's Taxonomy to my quiz questions?"
✓ "When should I use an infographic vs. a MicroSim?"

**Answer Characteristics:**
- Procedural, instructional
- Step-by-step guidance
- Practical examples
- "How to" focus
- 150-300 words
- May include code or concrete steps

**Target Distribution in FAQ:** 25%

---

### 4. Analyze (Analysis)

**Definition:** Draw connections among ideas; determine how parts relate to overall structure or purpose.

**Cognitive Actions:**
- Analyze, break down, compare, contrast, diagram, differentiate, distinguish, examine, experiment, identify, investigate, relate

**Question Starters:**
- "What is the relationship between...?"
- "What are the parts or features of...?"
- "How does [X] relate to [Y]?"
- "What evidence can you find...?"
- "What is the underlying cause of...?"
- "What patterns can you identify...?"

**FAQ Examples:**

✓ "What's the relationship between concept dependencies and learning order?"
✓ "How do the five levels of textbook intelligence build on each other?"
✓ "What factors determine whether a concept needs a MicroSim?"
✓ "How does prerequisite structure affect chapter organization?"

**Answer Characteristics:**
- Analytical, investigative
- Breaks down relationships
- Identifies patterns or causes
- May use diagrams or charts
- 200-300 words
- Multiple perspectives considered

**Target Distribution in FAQ:** 15%

---

### 5. Evaluate (Evaluation)

**Definition:** Justify a decision or course of action; make judgments based on criteria and standards.

**Cognitive Actions:**
- Appraise, argue, defend, judge, select, support, value, critique, evaluate, assess, recommend

**Question Starters:**
- "Which approach is best for...?"
- "What are the trade-offs of...?"
- "How would you decide between...?"
- "What criteria would you use to...?"
- "How would you prioritize...?"
- "What are the strengths and weaknesses of...?"

**FAQ Examples:**

✓ "Which approach is better for teaching complex concepts: text or MicroSim?"
✓ "What are the trade-offs between comprehensive glossaries and brief definitions?"
✓ "How do I decide which concepts need prerequisite validation?"
✓ "What's the best balance between content depth and cognitive load?"

**Answer Characteristics:**
- Evaluative, comparative
- Discusses pros/cons
- Uses criteria for judgment
- May present multiple valid options
- 200-350 words
- Nuanced, considers context

**Target Distribution in FAQ:** 7%

---

### 6. Create (Synthesis)

**Definition:** Produce new or original work; reorganize elements into new patterns or structures.

**Cognitive Actions:**
- Assemble, construct, create, design, develop, formulate, generate, plan, produce, propose, invent

**Question Starters:**
- "How would you design...?"
- "What would happen if...?"
- "Can you create a...?"
- "How could you improve...?"
- "What's the best way to combine...?"
- "How would you adapt [X] for [Y]?"

**FAQ Examples:**

✓ "How would I design a textbook for a completely new subject area?"
✓ "What's the best way to combine learning graphs with adaptive learning?"
✓ "How could I create an innovative assessment beyond traditional quizzes?"
✓ "How would you design a MicroSim to teach a highly abstract concept?"

**Answer Characteristics:**
- Creative, generative
- Proposes novel solutions
- Encourages experimentation
- Open-ended guidance
- 250-400 words
- Multiple approaches suggested

**Target Distribution in FAQ:** 3%

---

## Target Distribution by Category

Different FAQ categories should emphasize different Bloom's levels:

### Getting Started (60% Remember, 40% Understand)

Focus on basic facts and understanding course structure.

**Example Questions:**
- "What is this course about?" (Understand)
- "What are the prerequisites?" (Remember)
- "How is the textbook organized?" (Understand)

### Core Concepts (20% Remember, 40% Understand, 30% Apply, 10% Analyze)

Balance definitions with understanding and application.

**Example Questions:**
- "What is a learning graph?" (Remember)
- "Why are concept dependencies important?" (Understand)
- "How do I create a concept taxonomy?" (Apply)
- "What's the relationship between scaffolding and prerequisites?" (Analyze)

### Technical Details (30% Remember, 40% Understand, 20% Apply, 10% Analyze)

Emphasize terminology and technical understanding.

**Example Questions:**
- "What does ISO 11179 mean?" (Remember)
- "How does the glossary validator work?" (Understand)
- "When should I use cross-references?" (Apply)
- "How do metadata standards improve consistency?" (Analyze)

### Common Challenges (10% Remember, 30% Understand, 40% Apply, 20% Analyze)

Focus on problem-solving and troubleshooting.

**Example Questions:**
- "Why is my learning graph showing cycles?" (Understand)
- "How do I fix circular definitions?" (Apply)
- "What causes low concept coverage?" (Analyze)

### Best Practices (10% Understand, 40% Apply, 30% Analyze, 15% Evaluate, 5% Create)

Emphasize application and higher-order thinking.

**Example Questions:**
- "When should I use a MicroSim vs. a static diagram?" (Evaluate)
- "How do I balance content depth with cognitive load?" (Apply)
- "What patterns indicate good chapter structure?" (Analyze)
- "How could I combine multiple teaching approaches effectively?" (Create)

### Advanced Topics (10% Apply, 30% Analyze, 30% Evaluate, 30% Create)

Push toward higher cognitive levels.

**Example Questions:**
- "How would you design an adaptive learning system?" (Create)
- "What are the trade-offs of automated vs. manual content generation?" (Evaluate)
- "How do different textbook intelligence levels relate to learning outcomes?" (Analyze)

---

## Question Writing Guidelines

### For Remember Questions

**Do:**
- Ask about specific facts or definitions
- Use terminology from glossary
- Keep answers brief (50-150 words)
- Link to glossary or relevant section

**Don't:**
- Ask for explanations or reasoning
- Require understanding of relationships
- Make questions too broad

### For Understand Questions

**Do:**
- Ask "why" or "how"
- Request explanations or summaries
- Compare/contrast concepts
- Include context

**Don't:**
- Just ask for definitions (that's Remember)
- Ask for application (that's Apply)
- Require evaluation or creation

### For Apply Questions

**Do:**
- Present specific scenarios
- Ask "how would you..."
- Request step-by-step procedures
- Include practical examples

**Don't:**
- Keep questions abstract
- Just ask for understanding
- Avoid concrete contexts

### For Analyze Questions

**Do:**
- Ask about relationships
- Request identification of patterns
- Require breaking down into parts
- Compare underlying structures

**Don't:**
- Just list components (that's Remember)
- Stop at surface-level explanation (that's Understand)
- Ask for value judgments (that's Evaluate)

### For Evaluate Questions

**Do:**
- Ask for judgment or decision
- Present criteria or trade-offs
- Request recommendations
- Consider multiple options

**Don't:**
- Present only one option
- Avoid criteria or justification
- Skip the "why" behind decisions

### For Create Questions

**Do:**
- Ask for novel solutions
- Encourage innovation
- Request design or proposal
- Allow open-ended responses

**Don't:**
- Constrain to single answer
- Just ask for combining existing elements
- Make too prescriptive

---

## Common Mistakes and Corrections

### Mistake: Mislabeling Bloom's Level

❌ **Question:** "What is the best way to create a learning graph?"

**Incorrectly Labeled:** Remember (it's not asking to recall a fact)

**Correct Label:** Apply (asking how to use knowledge in practice)

**Better Phrasing:** "How do I create a learning graph for my course?" (clearly Apply)

---

❌ **Question:** "List the steps in the ADDIE model"

**Incorrectly Labeled:** Apply (it's not asking to use the steps)

**Correct Label:** Remember (asking to recall information)

---

❌ **Question:** "Explain why Bloom's Taxonomy is useful"

**Incorrectly Labeled:** Remember (not just recalling a fact)

**Correct Label:** Understand (asking for explanation)

---

### Mistake: Questions Too Vague

❌ "How does it work?"

✓ "How does concept dependency validation work in the learning graph generator?"

---

❌ "What's the difference?"

✓ "What's the difference between a learning graph and a concept taxonomy?"

---

### Mistake: Multiple Questions in One

❌ "What is a MicroSim and how do I create one and when should I use it?"

✓ Split into three questions:
- "What is a MicroSim?" (Remember)
- "How do I create a MicroSim?" (Apply)
- "When should I use a MicroSim vs. a static diagram?" (Evaluate)

---

## Balancing Distribution

### Target Overall Distribution

| Bloom's Level | Target % | Question Count (for 100 questions) |
|---------------|----------|-------------------------------------|
| Remember | 20% | 20 |
| Understand | 30% | 30 |
| Apply | 25% | 25 |
| Analyze | 15% | 15 |
| Evaluate | 7% | 7 |
| Create | 3% | 3 |

### Acceptable Deviation

Within ±10% for each level is acceptable:

- Remember: 10-30% ✓
- Understand: 20-40% ✓
- Apply: 15-35% ✓
- Analyze: 5-25% ✓
- Evaluate: 0-17% ✓
- Create: 0-13% ✓

Beyond ±10% indicates imbalance and should be corrected.

### How to Adjust

**Too many Remember/Understand questions?**
- Convert some to Apply by asking "How do I..."
- Add scenario-based questions
- Include more troubleshooting questions

**Too few Analyze/Evaluate/Create questions?**
- Add comparison questions
- Include trade-off discussions
- Ask for recommendations or designs
- Present complex scenarios

**Too many Create questions?**
- Convert some to Evaluate (trade-offs, recommendations)
- Convert some to Analyze (relationships, patterns)
- Remember Create should be small % (3% target)

---

## Quality Checklist

For each FAQ question, verify:

- [ ] **Correct Bloom's Level:** Question matches cognitive action
- [ ] **Clear Phrasing:** Specific, searchable, unambiguous
- [ ] **Appropriate Category:** Fits in assigned section
- [ ] **Complete Answer:** Fully addresses question
- [ ] **Appropriate Length:** 100-300 words (most questions)
- [ ] **Examples Present:** 40% of questions have examples
- [ ] **Links Present:** 60% of questions link to source
- [ ] **Terminology Consistent:** Uses glossary terms
- [ ] **Difficulty Appropriate:** Matches category expectations
- [ ] **No Duplicates:** Unique question not asked elsewhere

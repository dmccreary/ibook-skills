# FAQ Generator Skill

Automatically generate comprehensive, categorized FAQs for intelligent textbooks with Bloom's Taxonomy distribution and chatbot integration.

## Overview

This skill converts textbook content (chapters, glossary, learning graphs) into well-organized Frequently Asked Questions. Questions are distributed across Bloom's Taxonomy cognitive levels, categorized by learning progression, and exported as chatbot-ready JSON for RAG system integration.

## Installation

To use this skill with Claude Code or Claude.ai:

1. Install the skill by providing the path to this directory
2. The skill will be available for Claude to use when generating FAQs

## Usage

**Trigger Phrases:**

- "Generate an FAQ for my textbook"
- "Create frequently asked questions"
- "Build an FAQ from my course content"

**Prerequisites:**

- Course description file exists (`docs/course-description.md`)
- Learning graph created (`docs/learning-graph/03-concept-dependencies.csv`)
- Glossary generated (`docs/glossary.md` with 50+ terms)
- At least 30% of chapter content written (5,000+ words)

**Typical Workflow:**

1. User asks Claude to generate FAQ
2. Skill assesses content completeness (score 1-100)
3. Skill analyzes content for question opportunities
4. Skill generates 40+ questions across 6 categories
5. Skill creates `docs/faq.md` with organized Q&A
6. Skill exports chatbot training JSON
7. Skill generates quality report with recommendations

## Output Files

### Required

- **`docs/faq.md`** - Complete FAQ with categorized questions
  - 6 standard categories (Getting Started → Advanced Topics)
  - Level-2 headers for questions
  - Complete answers with examples (40% target)
  - Links to source content (60% target)
  - 100-300 words per answer

### Recommended

- **`docs/learning-graph/faq-quality-report.md`** - Quality assessment
  - Overall quality score (target: >75/100)
  - Bloom's Taxonomy distribution analysis
  - Concept coverage metrics
  - Answer quality analysis
  - Prioritized recommendations

- **`docs/learning-graph/faq-chatbot-training.json`** - RAG system data
  - JSON array of question-answer pairs
  - Metadata: Bloom's level, difficulty, concepts, keywords
  - Source links for each answer
  - Ready for chatbot/AI assistant integration

### Optional

- **`docs/learning-graph/faq-coverage-gaps.md`** - Uncovered concepts
  - Critical gaps (high-centrality concepts)
  - Medium priority gaps
  - Low priority gaps
  - Suggested questions for each gap

## Quality Standards

### Content Completeness Score (1-100)

Assesses whether sufficient content exists for quality FAQ:

- **90-100:** All inputs present, high quality
- **70-89:** Core inputs present, some gaps
- **50-69:** Limited content, basic FAQ possible
- **Below 50:** Insufficient content, user dialog triggered

### Overall FAQ Quality Score (1-100)

Four components:

1. **Coverage (30 pts):** % of concepts addressed
   - 80%+ concepts = 30 pts
   - 60-79% = 20 pts
   - <60% = 10 pts

2. **Bloom's Taxonomy Distribution (25 pts):**
   - Target: 20% Remember, 30% Understand, 25% Apply, 15% Analyze, 7% Evaluate, 3% Create
   - Scored by deviation from target (±10% acceptable)

3. **Answer Quality (25 pts):**
   - Examples: 40%+ with examples
   - Links: 60%+ with source links
   - Length: 100-300 words average
   - Completeness: 100% fully answered

4. **Organization (20 pts):**
   - Logical categorization
   - Progressive difficulty
   - No duplicates
   - Clear, searchable phrasing

### Success Criteria

- Overall quality score > 75/100
- Minimum 40 questions generated
- At least 60% concept coverage
- Bloom's distribution within ±15% of target
- All answers include source references
- Zero duplicate questions
- All internal links valid
- Chatbot JSON validates

## Question Categories

### 1. Getting Started (10-15 questions)

**Focus:** Course overview, prerequisites, navigation

**Bloom's Mix:** 60% Remember, 40% Understand

**Examples:**
- "What is this course about?"
- "Who is this course for?"
- "What do I need to know first?"
- "How is the textbook organized?"

### 2. Core Concepts (20-30 questions)

**Focus:** Key concepts from learning graph

**Bloom's Mix:** 20% Remember, 40% Understand, 30% Apply, 10% Analyze

**Examples:**
- "What is a learning graph?"
- "Why are concept dependencies important?"
- "How do I create a concept taxonomy?"
- "What's the relationship between scaffolding and prerequisites?"

### 3. Technical Details (15-25 questions)

**Focus:** Terminology, definitions, specifications

**Bloom's Mix:** 30% Remember, 40% Understand, 20% Apply, 10% Analyze

**Examples:**
- "What does ISO 11179 mean?"
- "How does the glossary validator work?"
- "When should I use cross-references?"

### 4. Common Challenges (10-15 questions)

**Focus:** Troubleshooting, misconceptions, difficult concepts

**Bloom's Mix:** 10% Remember, 30% Understand, 40% Apply, 20% Analyze

**Examples:**
- "Why is my learning graph showing cycles?"
- "How do I fix circular definitions?"
- "What causes low concept coverage?"

### 5. Best Practices (10-15 questions)

**Focus:** Application strategies, recommendations

**Bloom's Mix:** 10% Understand, 40% Apply, 30% Analyze, 15% Evaluate, 5% Create

**Examples:**
- "When should I use a MicroSim vs. a diagram?"
- "How do I balance content depth with cognitive load?"
- "What's the best approach for teaching abstract concepts?"

### 6. Advanced Topics (5-10 questions)

**Focus:** Complex scenarios, integration, innovation

**Bloom's Mix:** 10% Apply, 30% Analyze, 30% Evaluate, 30% Create

**Examples:**
- "How would you design an adaptive learning system?"
- "What are trade-offs of automated content generation?"
- "How could I combine multiple teaching approaches?"

## Skill Contents

```
faq-generator/
├── SKILL.md                              # Main skill instructions
├── README.md                             # This file
└── references/
    └── (Bloom's guidance now canonical in chapter-content-generator/references/blooms-taxonomy.md)
```

## Example Output

**FAQ File** (`docs/faq.md`):

```markdown
# Intelligent Textbooks FAQ

## Getting Started

## What is this course about?

This course teaches you how to build intelligent textbooks using
open source tools like MkDocs and AI-powered content generation.
You'll learn to create interactive educational resources that adapt
to student needs through learning graphs, MicroSims, and automated
quality assessment.

**See:** [Course Description](course-description.md)

## Core Concepts

## What is a Learning Graph?

A Learning Graph is a directed graph of concepts that reflects the
order concepts should be learned to master a new concept. It maps
prerequisite relationships as a Directed Acyclic Graph (DAG),
ensuring students learn foundational concepts before advanced ones.

**Example:** In a programming course, the learning graph shows
"Variables" must be understood before "Functions," which must be
understood before "Recursion."

**See:** [Learning Graph Concept](concepts/learning-graph.md),
[Glossary](glossary.md#learning-graph)

...
```

**Chatbot JSON** (`docs/learning-graph/faq-chatbot-training.json`):

```json
{
  "faq_version": "1.0",
  "generated_date": "2025-01-31",
  "source_textbook": "Building Intelligent Textbooks",
  "total_questions": 87,
  "questions": [
    {
      "id": "faq-001",
      "category": "Getting Started",
      "question": "What is this course about?",
      "answer": "This course teaches you how to build...",
      "bloom_level": "Understand",
      "difficulty": "easy",
      "concepts": ["Course Overview", "Intelligent Textbooks"],
      "keywords": ["course", "overview", "intelligent", "textbooks"],
      "source_links": ["docs/course-description.md"],
      "has_example": false,
      "word_count": 142
    }
  ]
}
```

**Quality Report** (`docs/learning-graph/faq-quality-report.md`):

```markdown
# FAQ Quality Report

Generated: 2025-01-31

## Overall Statistics

- **Total Questions:** 87
- **Overall Quality Score:** 82/100
- **Concept Coverage:** 73% (145/198 concepts)

## Bloom's Taxonomy Distribution

| Level | Actual | Target | Deviation |
|-------|--------|--------|-----------|
| Remember | 18% | 20% | -2% ✓ |
| Understand | 32% | 30% | +2% ✓ |
| Apply | 24% | 25% | -1% ✓ |
| Analyze | 16% | 15% | +1% ✓ |
| Evaluate | 7% | 7% | 0% ✓ |
| Create | 3% | 3% | 0% ✓ |

## Answer Quality

- **Examples:** 44% (38/87) - Target: 40%+ ✓
- **Links:** 62% (54/87) - Target: 60%+ ✓
- **Avg Length:** 187 words - Target: 100-300 ✓

## Recommendations

### High Priority
1. Add questions for 15 high-centrality uncovered concepts
2. Slightly increase Remember-level questions (+2%)

### Medium Priority
1. Add examples to 3 more answers
2. Link 5 more answers to source content
```

## References

### Bloom's Taxonomy Guide

The skill uses the canonical Bloom's Taxonomy reference at `$BK_HOME/skills/chapter-content-generator/references/blooms-taxonomy.md`. This reference covers:

- Detailed descriptions of all 6 cognitive levels
- Question starters and cognitive actions for each level
- Target distributions by category
- Question writing guidelines
- Common mistakes and corrections
- Quality checklist

Claude will reference this document when determining appropriate Bloom's levels for questions.

## Best Practices

### For Users

1. **Ensure prerequisites exist** - Generate learning graph and glossary first
2. **Write substantial content** - 5,000+ words recommended for quality FAQ
3. **Review quality report** - Use recommendations to improve coverage
4. **Iterate as needed** - Add questions for uncovered concepts
5. **Integrate with chatbot** - Use JSON export for AI assistant training

### For FAQ Generation

1. **Balance Bloom's levels** - Don't over-focus on Remember/Understand
2. **Include examples** - 40%+ of answers should have concrete examples
3. **Link to sources** - 60%+ of answers should reference original content
4. **Use clear phrasing** - Make questions searchable and specific
5. **Avoid duplicates** - Check for similar questions across categories
6. **Match audience level** - Adjust complexity to target audience

## Troubleshooting

### "Content completeness score is low (<60)"

**Cause:** Insufficient content for quality FAQ generation

**Solution:**
- Write more chapter content (target: 10,000+ words)
- Ensure glossary has 50+ terms
- Complete learning graph with dependencies
- Finalize course description with learning outcomes

### "Bloom's distribution is imbalanced"

**Cause:** Too many questions at lower cognitive levels

**Solution:**
- Add more Apply/Analyze questions (scenarios, relationships)
- Include Evaluate questions (trade-offs, recommendations)
- Add a few Create questions (designs, innovations)
- Review Bloom's guide for question templates

### "Low concept coverage (<60%)"

**Cause:** Many learning graph concepts not addressed in FAQ

**Solution:**
- Review coverage gaps report
- Add questions for high-centrality concepts first
- Focus on core concepts category
- Consider if some concepts are too granular

### "Missing examples or links"

**Cause:** Answers lack concrete illustrations or references

**Solution:**
- Add examples to abstract or complex concepts
- Link answers to relevant chapter sections
- Use specific section anchors, not just page links
- Ensure examples are from course domain

## Version History

- **v1.0** (2025-01-31) - Initial release
  - 6 standard categories
  - Bloom's Taxonomy distribution
  - Chatbot JSON export
  - Quality scoring and reporting

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or improvements:

1. Review detailed specification in `/docs/skills/faq-generator.md`
2. Check Bloom's Taxonomy reference guide
3. Examine quality reports for specific guidance
4. Review coverage gaps for missing concepts

## Related Skills

- **Learning Graph** - Generates concept dependencies used for questions
- **Glossary Generator** - Creates glossary referenced for terminology questions
- **Chapter Content Generator** - Produces content analyzed for FAQ questions
- **Concept Validator** - Validates FAQ coverage of all concepts
- **Quiz Generator** - Creates assessment questions (complementary to FAQ)

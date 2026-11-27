---
name: reference-generator
description: Generates 10 curated academic references per chapter, prioritizing Wikipedia plus credited textbook authors known for innovative explanations, with relevance descriptions, stored in chapter references.md files, then aggregates them into a book-level docs/references.md. Use when an intelligent textbook chapter needs citations.
metadata:
  ibook.version: "1.1"
---

# Reference Generator

**Version:** 1.1

### Changelog

- **v1.1** — Adds Step 8, the book-level `docs/references.md`. The skill
  previously stopped at per-chapter files, which leaves a reader with no way to
  see what the whole book rests on, and no way to find a source again without
  remembering which chapter it was in. Several books in this workspace carry a
  hand-written `docs/references.md` that drifts out of step with the chapters as
  soon as either changes; generating it from the chapter files means it cannot.
  Adds `src/book-references/build-book-references.py`.

## Overview

Generate high-quality, curated reference lists for educational textbooks. Each chapter receives exactly 10 references, prioritizing Wikipedia articles first for reliability, then crediting the specific textbook authors who pioneered clear or innovative ways of teaching the chapter's concepts, followed by authoritative online resources. References are never just a list of Wikipedia links — the textbook slots exist specifically to give credit to the authors behind influential explanations, analogies, or pedagogical techniques (e.g., a particularly intuitive derivation, a widely-copied diagram, a teaching analogy that became standard). References are stored in separate `references.md` files for token-efficient maintenance by AI agents.

## When to Use This Skill

Use this skill when:

- Creating a new intelligent textbook that needs chapter references
- Adding references to an existing textbook
- Updating or expanding references for educational content
- A user explicitly requests reference generation

## Key Principles

### 10 References Per Chapter

Every chapter receives exactly **10 high-quality references**:

- **References 1-3**: Wikipedia articles (most reliable, always accessible)
- **References 4-5**: Textbooks that credit a specific author's innovative explanation, analogy, derivation, or notation for a chapter concept (title, author, publisher - no URLs that break)
- **References 6-10**: Online resources (tutorials, courses, verified working links)

### Wikipedia First

Wikipedia links are placed first because they:

- Have stable, reliable URLs that rarely break
- Provide comprehensive, well-sourced overviews
- Are freely accessible to all students
- Cover most technical topics thoroughly
- Are maintained and updated by the community

### Separate Reference Files

References are stored in separate `references.md` files (not inline in chapters) for:

- **Token efficiency**: ~150 tokens vs ~6,000 tokens to read/update
- **Batch processing**: Agents can glob `**/references.md` for bulk updates
- **Separation of concerns**: Chapter edits don't risk breaking references

## Reference Generation Workflow

### Step 1: Analyze the Course Description

Read the `/docs/course-description.md` file to determine:

- **Subject matter** - determines reference topics
- **Target audience** - guides complexity of descriptions
- **Learning objectives** - ensures references support goals

### Step 2: Identify Chapter Structure

Locate all chapter directories:

```bash
# Find chapter folders
ls docs/chapters/
```

For each chapter, read the chapter `index.md` to understand:

- Chapter title and topic
- Key concepts covered
- Learning objectives

### Step 3: Generate 10 References Per Chapter

For each chapter, create exactly 10 references following this priority:

**Positions 1-3: Wikipedia Articles**

Find the most relevant Wikipedia articles for the chapter's main concepts:

```markdown
1. [Concept Name](https://en.wikipedia.org/wiki/Concept_Name) - Wikipedia - Description of article content and relevance to chapter.
```

**Positions 4-5: Textbooks Crediting Innovative Authors (No URL)**

These two slots exist to give explicit credit to authors, not just to cite a source. For each chapter's key concepts, identify the textbook author(s) most associated with an innovative, intuitive, or influential way of teaching that concept — a distinctive analogy, derivation, notation, worked example, or diagram that other authors have since adopted or that students consistently find clarifying. Search for who "originated" or is "best known for" the chapter's core explanation before defaulting to a generic well-known textbook. Reference these textbooks without URLs (which often break):

```markdown
4. Textbook Title (Edition) - Author Name - Publisher - Names the specific innovation (analogy, derivation, notation, example) this author is known for and why it makes the concept easier to grasp.
```

**Positions 6-10: Online Resources**

Verified online tutorials, courses, and educational sites:

```markdown
6. [Resource Title](https://verified-url.com/path) - Source Name - Description of content and specific relevance to chapter topics.
```

### Step 4: Verify Online URLs

For references 6-10, verify each URL:

```python
WebFetch(url=reference_url, prompt="Is this page accessible? What is the main topic?")
```

**Preferred sources** (stable, educational):
- All About Circuits (allaboutcircuits.com)
- Electronics Tutorials (electronics-tutorials.ws)
- ChipVerify (chipverify.com)
- HDLBits (hdlbits.01xz.net)
- Nandland (nandland.com)
- MIT OpenCourseWare (ocw.mit.edu)
- GeeksforGeeks (geeksforgeeks.org)
- Digilent Reference (digilent.com/reference)

### Step 5: Write Reference Files

Create a `references.md` file in each chapter directory:

**File location**: `docs/chapters/XX-chapter-name/references.md`

**File format**:

```markdown
# References: [Chapter Title]

1. [Wikipedia Article](https://en.wikipedia.org/wiki/Topic) - Wikipedia - Comprehensive overview of [topic] including [specific aspects relevant to chapter].

2. [Wikipedia Article 2](https://en.wikipedia.org/wiki/Topic2) - Wikipedia - Detailed explanation of [concept] with [relevant details].

3. [Wikipedia Article 3](https://en.wikipedia.org/wiki/Topic3) - Wikipedia - Coverage of [related topic] including [applications/examples].

4. Textbook Title (Edition) - Author Name - Publisher - Author Name pioneered [specific analogy/derivation/notation] for [concept], now widely adopted because [why it clarifies the idea].

5. Textbook Title 2 - Author Name - Publisher - Credits Author Name's [specific innovative approach] to [chapter concept], noted for [what makes it distinctive/effective].

6. [Online Resource](https://verified-url.com) - Source - Tutorial on [topic] with [specific features like examples, exercises, visualizations].

7. [Online Resource 2](https://verified-url.com) - Source - [Description of content and relevance].

8. [Online Resource 3](https://verified-url.com) - Source - [Description of content and relevance].

9. [Online Resource 4](https://verified-url.com) - Source - [Description of content and relevance].

10. [Online Resource 5](https://verified-url.com) - Source - [Description of content and relevance].
```

### Step 6: Update Chapter Files

Add a link at the end of each chapter's `index.md`:

```markdown
[See Annotated References](./references.md)
```

**Important**: Replace any existing `## References` section with this single link.

### Step 7: Update mkdocs.yml Navigation

Nest an `Annotated References:` entry under each chapter in `mkdocs.yml`,
following the canonical nav-editing rules (read-before-write, serialize
edits, `Content:` label for the chapter page) in
`$BK_HOME/skills/book-installer/references/mkdocs-nav-editing.md`:

```yaml
  - 1. Chapter Name:
    - Content: chapters/01-chapter-folder/index.md
    - Quiz: chapters/01-chapter-folder/quiz.md
    - Annotated References: chapters/01-chapter-folder/references.md
```

### Step 8: Generate the Book-Level References Page

The per-chapter files answer "what should I read next about *this*". They do not
answer "what does this book rest on", and they make a source impossible to find
again unless the reader remembers which chapter cited it. A source cited by six
chapters looks like six unrelated entries.

Generate one aggregated page from the chapter files:

```bash
python3 "$BK_HOME/src/book-references/build-book-references.py" .
```

It deduplicates by URL, keeps the fullest description any chapter wrote for a
source, and lists the chapters citing each one. Options: `--output`, `--title`,
`--min-shared`, and `--dry-run`.

**Generate it, never hand-write it.** A hand-written bibliography drifts the
moment a chapter's references change, and nothing warns you. Re-run this after
any change to chapter references, and after adding or removing a chapter.

Then add it to `mkdocs.yml`, following the nav-editing rules in
`$BK_HOME/skills/book-installer/references/mkdocs-nav-editing.md`:

```yaml
  - References: references.md
```

**Check the two things the script reports.** It names any chapter carrying fewer
than five references, which usually means Step 3 was skipped or a chapter was
added later. And compare the distinct-source count against the total citation
count: if they are nearly equal, no source is doing work across chapters, which
in a book with a real concept graph is a sign the chapters were researched in
isolation rather than as one book.

#### Say how the sources were handled, not only what they were

For any book where a reader might act on a claim — health, safety, legal,
financial — a list of sources is only half of what they need. Add a short
section above the list saying how citations were handled: what evidence grading
was used, whether citations were verified against primary sources or accepted on
the author's confidence, what remains unchecked, and what any automated link
checking does and does not prove. Fetching a URL tells you it resolves; it does
not tell you the page still says what it said.

## Reference Quality Guidelines

### Description Requirements

Each reference description should:

- Explain **what** the resource covers (1 sentence)
- Explain **why** it's relevant to this chapter (1 sentence)
- Mention specific features (examples, exercises, visualizations)
- Be 20-40 words total

**Good example**:
```markdown
1. [Karnaugh map](https://en.wikipedia.org/wiki/Karnaugh_map) - Wikipedia - Detailed explanation of K-map theory, grouping rules, and don't-care conditions. Essential foundation for the simplification techniques covered in this chapter.
```

**Bad example**:
```markdown
1. [Karnaugh map](https://en.wikipedia.org/wiki/Karnaugh_map) - Wikipedia - About K-maps.
```

### Wikipedia Article Selection

Choose Wikipedia articles that:

- Cover the chapter's primary concepts
- Have substantial content (not stubs)
- Include diagrams, examples, or formulas
- Link to related topics students might explore

### Textbook Selection

Reference textbooks whose author:

- Is credited with originating or popularizing a specific explanation, analogy, derivation, notation, or diagram for one of the chapter's concepts
- Is widely cited by other authors or instructors for that particular teaching innovation
- Wrote a textbook that is reasonably accessible to students
- Has an explanation the description names concretely — never just "covers the topic well"

If no author stands out as the originator of a distinctive teaching approach, choose the textbook most often praised (in reviews, syllabi, or educator discussion) for making the concept unusually clear, and say so explicitly in the description rather than defaulting to a generic "authoritative textbook" citation.

### Online Resource Selection

Choose online resources that:

- Have verified, working URLs
- Come from educational or reputable technical sources
- Provide practical examples or exercises
- Complement (not duplicate) Wikipedia content

## Reference Quality Checklist

Before finalizing references, ensure:

- [ ] Exactly 10 references per chapter
- [ ] References 1-3 are Wikipedia articles
- [ ] References 4-5 are textbooks (no URLs) that name the specific author and the innovative explanation/analogy/derivation they're credited with
- [ ] References 6-10 have verified working URLs
- [ ] All descriptions are 20-40 words
- [ ] Descriptions explain relevance to chapter
- [ ] No duplicate sources across references
- [ ] Proper formatting throughout

## File Structure After Generation

```
docs/chapters/
├── 01-chapter-name/
│   ├── index.md          # Ends with: [See Annotated References](./references.md)
│   ├── quiz.md
│   └── references.md     # 10 curated references
├── 02-chapter-name/
│   ├── index.md
│   ├── quiz.md
│   └── references.md
...
```

## Token Efficiency Benefits

| Task | Inline References | Separate Files |
|------|------------------|----------------|
| Read one chapter's refs | ~6,000 tokens | ~200 tokens |
| Update all 15 chapters | ~90,000 tokens | ~3,000 tokens |
| Batch reference check | Not feasible | Glob + process |

## Finish

After generating references:

1. Report the number of chapters processed
2. List any URLs that failed verification
3. Confirm mkdocs.yml was updated
4. Remind user to verify the site builds: `mkdocs serve`

## Resources

This skill uses web-based verification tools built into Claude Code:

- **WebSearch**: Find authoritative sources on topics
- **WebFetch**: Verify URLs are accessible and extract metadata
- **Glob**: Find all chapter directories and reference files
- **Write**: Create reference files
- **Edit**: Update chapter files and mkdocs.yml

No additional scripts or assets are required for this skill.

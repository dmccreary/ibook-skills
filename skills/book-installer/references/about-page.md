---
name: about-page
description: Generates a professional about.md page for intelligent textbooks with motivational framing, author bio, citation formats, and curriculum-staff credibility signals.
---

# About Page Generator

This guide generates a comprehensive `docs/about.md` page designed to establish credibility with curriculum staff, school administrators, and educators evaluating the textbook for adoption.

## What This Guide Creates

1. **docs/about.md** - Professional about page with all sections below
2. **Navigation entry** in mkdocs.yml

## Prerequisites

- Existing MkDocs Material project with mkdocs.yml
- `docs/course-description.md` (for subject context and audience)
- Learning graph generated (for concept/chapter counts)
- Author information available

## Workflow

### Step 1: Gather Project Variables

Read the following files and extract the variables needed for the template:

| Variable | Source | Example |
|----------|--------|---------|
| `SITE_NAME` | mkdocs.yml → `site_name` | "Ecology: Systems Thinking for a Changing Planet" |
| `SITE_AUTHOR` | mkdocs.yml → `site_author` | "Dan McCreary" |
| `SITE_URL` | mkdocs.yml → `site_url` | "https://dmccreary.github.io/ecology/" |
| `REPO_URL` | mkdocs.yml → `repo_url` | "https://github.com/dmccreary/ecology" |
| `SUBJECT` | course-description.md | "ecology" |
| `TARGET_AUDIENCE` | course-description.md | "high school students" |
| `NUM_CHAPTERS` | count `docs/chapters/*/index.md` | 17 |
| `NUM_CONCEPTS` | count rows in learning-graph.csv or nodes in learning-graph.json | 200 |
| `HAS_MASCOT` | check for `docs/img/mascot/welcome.png` | true/false |
| `MASCOT_NAME` | CLAUDE.md or mascot config | "Bailey the Beaver" |
| `PUBLICATION_YEAR` | current year | 2026 |
| `BIBTEX_KEY` | `{author_last_name}{year}{subject_slug}` | "mccreary2026ecology" |

Also check for:
- `docs/sims/` directory (to count MicroSims)
- `docs/glossary.md` (to confirm glossary exists)
- `docs/quizzes/` or quiz content in chapters
- `docs/references/` or chapter reference sections

### Step 2: Generate the About Page

Generate `docs/about.md` using the template structure below. Every section is required unless marked optional. Adapt the tone and content to the specific subject — do not produce generic filler.

---

## Template Structure

### Section 1: Title and Frontmatter

```markdown
---
title: "About This Book"
description: "About {{SITE_NAME}} — its purpose, audience, design, and the team behind it."
---

# About This Book
```

### Section 2: Mascot Welcome (optional — only if mascot exists)

If the project has a mascot (`docs/img/mascot/welcome.png` exists), add a welcome section. The mascot should speak in character using 3-5 sentences that introduce the book and set an encouraging tone.

```markdown
## Welcome from {{MASCOT_NAME}}

!!! mascot-welcome "Welcome!"
    ![{{MASCOT_NAME}} waving welcome](../img/mascot/welcome.png){ class="mascot-admonition-img" }
    {{MASCOT_WELCOME_TEXT — in character, 3-5 sentences, warm and encouraging,
    references the subject matter, ends with the mascot's catchphrase if it has one.}}
```

### Section 3: Why This Intelligent Textbook

This is the most important section of the about page. It must make the reader — especially a curriculum director, department head, or school board member — feel that this textbook addresses a real, urgent educational need and that ignoring it would be a missed opportunity.

**Structure this section as follows:**

1. **Opening hook** (1-2 sentences): State why this subject matters right now — tie it to a current event, workforce trend, societal challenge, or educational gap. Be specific, not generic.

2. **Evidence block** (bulleted statistics): Provide 4-8 cited statistics that demonstrate the scale, urgency, or opportunity. Use two groups:
   - **National/domestic** statistics (labeled with country and year)
   - **Global** statistics (labeled with source and year)

   Each statistic should be a complete sentence with the key number in bold. Use footnotes `[^1]` for citations and provide the full references at the bottom of the page.

3. **Emotional bridge** (1-2 sentences): Connect the statistics to the reader's students. Use second person ("your students") or inclusive language ("these numbers represent..."). Make it personal.

4. **What makes this book different** (1 paragraph): Explain what this intelligent textbook offers that a traditional textbook does not. Hit these points:
   - Built on a validated learning graph of {{NUM_CONCEPTS}} interconnected concepts
   - Interactive MicroSims for hands-on exploration
   - Concepts introduced in prerequisite order (no jumping ahead)
   - Open source and free — no paywalls, no access codes
   - Written at an accessible reading level with terms defined on first use

**Example (adapt to subject):**

```markdown
## Why This Intelligent Textbook

Ecology is everywhere — in the food your students eat, the air they breathe,
the water they drink, and the headlines they scroll past every day. Yet most
curricula teach ecology as a list of definitions to memorize rather than as
a systems thinking discipline that equips students to evaluate environmental
claims, trace energy flows, and spot misinformation.

**In the United States (2025):**

- The Bureau of Labor Statistics projects **7% growth** in environmental
  science occupations through 2032, faster than the national average[^1]
- Only **38% of high school graduates** demonstrate proficiency in
  science, according to the most recent NAEP assessment[^2]
- NGSS adoption has reached **44 states and the District of Columbia**,
  but fewer than half of those states provide teachers with aligned
  interactive curriculum materials[^3]

**Worldwide:**

- The United Nations Environment Programme estimates that **$8.1 trillion
  per year** in nature-based solutions investment will be needed by 2050
  to address biodiversity loss, land degradation, and climate change[^4]
- Environmental literacy is now recognized as a core competency in the
  curricula of more than **70 countries**[^5]

These numbers represent millions of students who need more than definitions —
they need the analytical tools to reason about interconnected systems. This
textbook exists to close that gap.

This book takes a fundamentally different approach. It is built on a
**learning graph of {{NUM_CONCEPTS}} interconnected concepts** organized into
{{NUM_TAXONOMY_CATEGORIES}} categories. Concepts are introduced in the order
their prerequisites are established, so understanding builds naturally from
chapter to chapter. Throughout the book you will find **interactive
MicroSims** — browser-based simulations that let students manipulate models,
explore data, and discover principles through experimentation rather than
memorization. The entire textbook is **open source and free** — no paywalls,
no access codes, no expensive annual editions.
```

**Guidelines for writing this section:**

- Do NOT use generic motivational language ("X is important for the future"). Be specific.
- Statistics must be real and cited. If you cannot find a real statistic, do not fabricate one — use a qualified estimate with a source.
- The emotional bridge should be 1-2 sentences maximum. Do not lecture.
- The "what makes this book different" paragraph should be concrete, not aspirational. Only claim features that actually exist in the project.

### Section 4: How to Use This Book

List what the book contains with specific counts. Only include items that actually exist in the project.

```markdown
## How to Use This Book

This textbook is designed for self-paced study. Each chapter builds on
previous material, so reading in order is recommended. The book includes:

- **{{NUM_CHAPTERS}} Chapters** covering {{HIGH_LEVEL_TOPIC_LIST}}
- **Interactive MicroSims** embedded in chapters — browser-based simulations
  you can manipulate to explore concepts
- **Quizzes** at the end of each chapter to test understanding
- **Annotated References** linking to Wikipedia and authoritative sources
- **Glossary** with definitions for every key concept
- **FAQ** with common questions and answers
- **Learning Graph** visualizing {{NUM_CONCEPTS}} concept dependencies
- **Search** available from any page using the search bar

The [Learning Graph](learning-graph/index.md) visualizes how concepts connect
across chapters. If you want to explore non-linearly or check prerequisites
for a specific topic, start there.
```

### Section 5: About the Author

This section establishes credibility. It should read as a professional bio appropriate for an academic publication, not a casual introduction.

**For Dan McCreary (default author — use this bio unless a different author is specified):**

The headshot image if the author is Dan McCreary is here: https://dmccreary.github.io/dmccreary/img/dan-headshot-small.png

You can fetch the image by running this shell command.

```sh
curl https://dmccreary.github.io/dmccreary/img/dan-headshot-small.png --output docs/img/dan-headshot-small.png
```

Verify Image with this command:
```sh
file --mime-type -b docs/img/dan-headshot-small.png 
```
It should return 'image/png'


```markdown
## About the Author

![](./img/dan-headshot-small.png){ width="150px" align="right"}

Dan McCreary is a semi-retired AI researcher, solution architect, and
educator who has spent more than three decades helping Fortune 100
organizations reason over massive datasets. At Optum he founded the
Generative AI Center of Excellence and led the team that built one of the
world's largest healthcare knowledge graphs — spanning over 25 billion
vertices — to unify member, provider, and patient insights. Dan's deep
background in knowledge representation and systems thinking underpins the
precise learning graphs and intelligent textbook workflows used throughout
this course.

He is the co-author of *Making Sense of NoSQL* (Manning Publications), the
founding chair of the NoSQL Now! conference, and a frequent keynote speaker
on semantic search, ontology strategy, and AI hardware. Beyond industry, Dan
has mentored students as a STEM volunteer since 2014 and now applies the same
rigor to building open educational resources. You can visit the
[Intelligent Textbooks Case Studies](https://dmccreary.github.io/intelligent-textbooks/case-studies/)
to see over 125 textbooks that Dan has created or co-created with other
authors.

**Selected Credentials**

- B.A. in Physics and Computer Science from Carleton College
- M.S.E.E. from the University of Minnesota
- MBA coursework at the University of St. Thomas
- Patent holder in semantic search and ontology management techniques
- Advocate for large-scale Enterprise Knowledge Graph adoption across
  healthcare and education
- Long-time promoter of accessible, low-cost AI-powered learning experiences
```

**For a different author:** Ask the user for:
1. Full name
2. Headshot image path (if available)
3. Professional background (2-3 sentences on career)
4. Relevant credentials and publications
5. Connection to the subject matter

Structure the bio in the same format: narrative paragraph(s) followed by a bulleted credentials list.

### Section 6: How to Cite This Book

Provide four standard citation formats. This section signals academic seriousness and makes it easy for curriculum staff to reference the textbook in adoption proposals, lesson plans, and grant applications.

```markdown
## How to Cite This Book

If you reference this textbook in academic work, curriculum proposals,
lesson plans, or other publications, please use one of the following
citation formats.

**APA (7th edition)**

McCreary, D. ({{YEAR}}). *{{SITE_NAME}}*. {{SITE_URL}}

**Chicago (17th edition)**

McCreary, Dan. {{YEAR}}. *{{SITE_NAME}}*. {{SITE_URL}}.

**MLA (9th edition)**

McCreary, Dan. *{{SITE_NAME}}*. {{YEAR}}, {{SITE_URL_WITHOUT_PROTOCOL}}.

**BibTeX**

\```bibtex
@book{ {{BIBTEX_KEY}},
  title     = { {{SITE_NAME}} },
  author    = {McCreary, Dan},
  year      = { {{YEAR}} },
  url       = { {{SITE_URL}} },
  note      = {Interactive intelligent textbook}
}
\```

To cite a specific chapter, append the chapter number and title — for
example:

McCreary, D. ({{YEAR}}). Chapter 1: {{FIRST_CHAPTER_TITLE}}. In
*{{SITE_NAME}}*. {{SITE_URL}}chapters/01-{{FIRST_CHAPTER_SLUG}}/
```

**For a different author:** Substitute the author's name in all four formats and adjust the BibTeX key accordingly.

### Section 7: License

```markdown
## License

This work is released under the
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
License (CC BY-NC-SA 4.0)](license.md). You are free to share and adapt the
material for non-commercial purposes as long as you give appropriate credit
and share your adaptations under the same license.
```

If the project uses a different license, read `docs/license.md` or `LICENSE` and adjust accordingly.

### Section 8: Footnote References

Place all footnoted references at the bottom of the file:

```markdown
## References

[^1]: Source Name. (Year). *Title*. URL
[^2]: Source Name. (Year). *Title*. URL
```

**Reference quality standards:**
- Prefer government sources (BLS, NCES, WHO, UN), peer-reviewed publications, and established industry reports
- Include the URL so readers can verify
- Use the same footnote numbering as the "Why This Intelligent Textbook" section

---

## Step 3: Update Navigation

Add the about page to `mkdocs.yml` navigation. It should appear near the bottom of the nav, typically after Glossary/FAQ/References and before Contact or License:

```yaml
nav:
  # ... chapters, learning graph, sims, glossary, etc. ...
  - About: about.md
  - Contact: contact.md
  - License: license.md
```

If the project already has an About entry in nav, no change is needed.

## Step 4: Verify

After generating the file:

1. Confirm `docs/about.md` exists and renders correctly with `mkdocs serve`
2. Check that all internal links resolve (learning graph, contact, license, chapter 1)
3. Verify the headshot image path is correct (if author photo is included)
4. Verify the mascot image path is correct (if mascot section is included)
5. Confirm all footnote references are complete and properly numbered

## Troubleshooting

### Mascot Image Not Rendering
- Check path: `./img/mascot/welcome.png` is relative to docs/about.md
- Verify image exists at `docs/img/mascot/welcome.png`

### Author Headshot Not Rendering
- Standard path is `./img/dan-headshot-small.png`
- If using a different author, confirm the image path with the user

### Statistics Feel Generic
- Re-read the course description and identify the specific educational gap
- Search for subject-specific workforce data, assessment scores, or adoption statistics
- If real statistics are unavailable, use qualified language ("estimated", "approximately") with the best available source

## Related Guides

- `home-page-template.md` - Home page with cover image and social metadata
- `learning-mascot.md` - Design and implement the pedagogical mascot
- `instructors-guide.md` - Comprehensive teacher's guide
- `init-textbook.md` - Bootstrap the MkDocs project structure (feature 0)

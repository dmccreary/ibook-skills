---
title: Publishing and Announcing a Finished Book
description: Covers README generation, LinkedIn posts and carousels, AP-style press releases, the book launch checklist, continuous improvement, and the capstone textbook project.
generated_by: claude skill chapter-content-generator
date: 2026-08-22 19:40:00
version: 0.09
---

# Publishing and Announcing a Finished Book

## Summary

This chapter covers generating a README with badges and site statistics, a LinkedIn announcement post and carousel document, and an AP-style press release, all driven by the canonical book metrics. It closes with the book completion workflow and launch checklist that bring the intelligent-textbook pipeline to its capstone project. Students will be able to produce a complete publishing package for a finished book after this chapter.

## Concepts Covered

This chapter covers the following 15 concepts from the learning graph:

1. book-metrics.py Script
2. collect-site-metrics.py
3. README Generation
4. Repository Badges
5. Getting Started Section
6. LinkedIn Announcement Post
7. Press Release
8. Continuous Book Improvement
9. AP Style Writing
10. Announcement Preview Image
11. Book Completion Workflow
12. LinkedIn Carousel Document
13. Book Launch Checklist
14. Carousel Slide Patterns
15. Capstone Textbook Project

## Prerequisites

This chapter builds on concepts from:

- [1. Foundations of AI, Language Models, and Prompting](../01-foundations-ai-language-models/index.md)
- [2. AI Coding Agents and the Five Levels of Textbook Intelligence](../02-ai-agents-textbook-intelligence/index.md)
- [4. Development Tools: Editor, Terminal, and Git Basics](../04-dev-tools-editor-git-basics/index.md)
- [7. Progressive Disclosure and Meta-Skill Routing](../07-progressive-disclosure-meta-skills/index.md)
- [11. Distributing Skills and Building Commands](../11-distributing-skills-commands/index.md)
- [13. Bloom's Taxonomy and Instructional Design](../13-blooms-taxonomy-instructional-design/index.md)
- [18. Chapter Content Quality and Review](../18-chapter-content-quality-review/index.md)
- [25. Text-to-Image Models and the Verified Infographic Pipeline](../25-verified-infographic-pipeline/index.md)
- [27. Slide Decks, Stories, and Audio Media](../27-slide-decks-stories-audio-media/index.md)
- [29. Book Installer Features](../29-book-installer-features/index.md)
- [30. Session Logs and Book Metrics](../30-session-logs-book-metrics/index.md)

---

!!! mascot-welcome "Last chapter. Let's send your book out into the world."
    ![Kit waves hello with their tool satchel](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    Thirty chapters of building, and now the part where someone else actually finds your book. Right tool, right task — one last time, together.

## Measuring the Finished Book

Publishing starts by regenerating the numbers one final time. **book-metrics.py** is the program that measures a book's content and writes the structured measurement file — the same `book-metrics.json` hub from Chapter 30, refreshed against the book's truly final state. **collect-site-metrics.py** gathers statistics from the built site itself for use in summaries and announcements, counting what actually deployed rather than what was merely written.

## The README: A Repository's Front Page

**README generation** produces a repository's front page, including a summary, badges, statistics, and setup instructions — usually the very first thing anyone new to a project reads. **Repository badges** are small status images displayed on a repository page showing license, build state, or site link, giving a visitor a fast visual sense of a project's health before reading a word of prose. A **getting started section** tells a newcomer how to install dependencies and run the site locally, turning curiosity into an actual working copy on someone else's machine.

## Announcing on LinkedIn

A **LinkedIn announcement post** is a short professional-network message announcing a book milestone, drawing its figures directly from the recorded measurements — never hand-typed, per Chapter 30's canonical metrics principle. For a richer format, a **LinkedIn carousel document** is a multi-page slideshow posted to a professional network, in which readers swipe through successive panels, following recognizable **carousel slide patterns**: recurring panel layouts such as a title panel, a statistics panel, and a closing call to action.

!!! mascot-tip "Don't invent a new slide pattern for every book."
    ![Kit holding up a tool with a knowing look](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    A reader swiping through a carousel benefits from a familiar rhythm — title, then a stat, then a highlight, then a call to action. Reuse the same pattern across announcements rather than reinventing the structure each time; the content changes, the shape doesn't need to.

Whatever format the announcement takes, it needs an **announcement preview image**: the picture accompanying a shared announcement, cropped to the proportions a platform displays — the same Open Graph and social-card mechanics from Chapter 25, aimed at one specific post instead of the site as a whole.

## The Press Release

For reaching an audience beyond a single social network, a **press release** is a formal announcement written for journalists, stating what was released, why it matters, and where to find it, following **AP style writing**: a journalistic convention governing capitalization, numbers, titles, and attribution in press material.

!!! mascot-thinking "A style guide is just a shared set of choices, made once."
    ![Kit thinking with a paw on their chin](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    AP style spells out numbers under ten, capitalizes specific titles but not general ones, and follows dozens of similar small rules. None of them matter individually — what matters is that every press release in the world follows the *same* small rules, so a journalist can read one without being distracted by inconsistency. That's the same instinct behind this book's own title-case concept labels and consistent mascot voice.

## Before You Announce: The Launch Checklist

None of this should happen before the book is actually ready. The **book completion workflow** is the coordinated final pass that generates all remaining supporting material and reports before a book is released, verified against a **book launch checklist**: the list of confirmations completed before announcing a book, covering build, deployment, metrics, and links.

!!! mascot-warning "Announcing before the checklist is done invites a broken first impression."
    ![Kit holding up a caution paw](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    A LinkedIn post that goes out before deployment verification (Chapter 29) has actually confirmed the live site works risks sending your very first readers to a broken link. Run the launch checklist all the way through, in order, before a single announcement goes out.

#### Diagram: Book Launch Checklist

<iframe src="../../sims/book-launch-checklist/main.html" width="100%" height="492px" scrolling="no"></iframe>

<details markdown="1">
<summary>Book Launch Checklist</summary>
Type: workflow
**sim-id:** book-launch-checklist<br/>
**Library:** Mermaid<br/>
**Status:** Specified

Bloom Level: Evaluate (L5)
Bloom Verb: Justify

Learning objective: Justify why each launch-checklist item must pass before an announcement goes out, in the correct order.

Visual style: Top-to-bottom Mermaid flowchart styled as a checklist

Nodes:
1. "mkdocs build --strict passes" (rounded rectangle)
2. "Deployment verified live" (rounded rectangle)
3. "book-metrics.json regenerated" (rounded rectangle)
4. "README regenerated from metrics" (rounded rectangle)
5. "Announcement drafted" (rounded rectangle)
6. "Announcement preview image checked" (rounded rectangle)
7. "Publish" (rounded rectangle, book's accent color, final node)

Edges: strictly sequential 1 --> 2 --> 3 --> 4 --> 5 --> 6 --> 7

Interactivity requirement: every node MUST have a `click` directive opening an infobox explaining why that specific step must complete before the next one, referencing the relevant earlier chapter (e.g., node 1 references Chapter 29's strict build mode, node 2 references Chapter 29's deployment verification).

Color scheme: all checklist nodes in a consistent teal until clicked, then briefly highlight green to simulate "checked off"; final "Publish" node in a distinct accent color.

Implementation: Mermaid flowchart with per-node click handlers rendered inside the MicroSim's main.html, opening a shared infobox panel below the diagram.
</details>

## After Launch: Continuous Improvement

Publishing isn't the end of a book's story. **Continuous book improvement** means using measurements, reader feedback, and usage data to revise a book and the skills that produced it after release — the quiz analytics from Chapter 20, the FAQ coverage gaps from Chapter 19, and the reading-level audits from Chapter 30 all exist to feed exactly this ongoing loop.

## The Capstone: Your Own Intelligent Textbook

Every concept in this book, across all 31 chapters, exists in service of one culminating exercise: the **capstone textbook project**, in which a learner produces a complete intelligent textbook, applying the entire pipeline end to end. You've now met every piece of it — a course description scored against a rubric, a validated 300-to-600-concept learning graph, dependency-ordered chapters, generated content with a consistent voice, MicroSims chosen from a real reuse catalog before any new one gets specified, a glossary and quizzes that meet a real standard, and a publishing package that never says two different things about the same number. The only thing left is a subject of your own.

## Key Takeaways

- **book-metrics.py** and **collect-site-metrics.py** produce the final numbers a launch is built on.
- **README generation**, with **badges** and a **getting started section**, is a project's front door.
- A **LinkedIn announcement post**, a **carousel document** with recognizable **slide patterns**, and an **announcement preview image** reach a professional audience; a **press release** in **AP style** reaches journalists.
- The **book completion workflow** and a **launch checklist** should finish, in full, before anything is announced.
- **Continuous book improvement** keeps a book alive after launch — and the **capstone textbook project** is where every concept in this book comes together in a project of your own.

!!! mascot-celebration "You just finished the whole book. Really finished it."
    ![Kit celebrating with arms raised](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    Thirty-one chapters ago, I told you I had exactly six jobs, and that if I wasn't doing one of them, I wasn't in the chapter. This is the sixth one, for the last time in this book: you built a real mental model of how an entire intelligent textbook gets made, end to end. Now go build one. Right tool, right task!

---
title: Book Launch Checklist
description: Work down the seven-step launch checklist in order and, for each step, choose the reason it has to pass before the next one, with feedback when a reason is unsound or a step is taken too soon.
image: /sims/book-launch-checklist/book-launch-checklist.png
og:image: /sims/book-launch-checklist/book-launch-checklist.png
twitter:image: /sims/book-launch-checklist/book-launch-checklist.png
social:
   cards: false
quality_score: 100
---

# Book Launch Checklist

<iframe src="main.html" height="492px" width="100%" scrolling="no"></iframe>

[Run the Book Launch Checklist MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }

## About This MicroSim

A **book launch checklist** is the list of confirmations completed before a
book is announced. It covers build, deployment, metrics, and links, and the
order matters: each step protects the one after it.

| Step | Confirmation | Why it comes before the next step | Earlier chapter |
|:----:|--------------|-----------------------------------|-----------------|
| 1 | `mkdocs build --strict` passes | A build with broken links would be deployed exactly as it is | 29, strict build mode |
| 2 | Deployment verified live | A fix found on the live site changes the book, which would make earlier measurements stale | 29, deployment verification |
| 3 | `book-metrics.json` regenerated | The README reads its statistics from this file | 30, canonical metrics principle |
| 4 | README regenerated from metrics | The announcement sends people to the repository's front page | 30, book-metrics.json hub |
| 5 | Announcement drafted | A preview image belongs to one specific post | 25, social media preview cards |
| 6 | Announcement preview image checked | Once the post is public, a bad preview is the first impression | 25, Open Graph meta tags |
| 7 | Publish | | 31, book launch checklist |

This MicroSim asks you to do more than read the list. For each step you choose
between two reasons for doing it before the next step. One reason is sound.
The other sounds plausible but does not hold up. A sound reason checks the
step off and turns it green. If you jump ahead, the panel explains what the
skipped step was protecting.

## How to Use

1. Click **1. mkdocs build --strict passes**, or select **Next Step**.
2. Read what the step confirms, then read the two candidate reasons.
3. Choose the reason you can defend. If it is sound, the step is checked off
   and the panel gives the full justification and the chapter it comes from.
   If it is not, the panel says why, and you choose again.
4. Continue down the list. The counter shows how many of the six confirmations
   are checked.
5. At any point, click a later step, or **7. Publish**, to see what the panel
   says about skipping ahead.
6. When all six are checked, **Publish** unlocks.
7. Click any green step to reread its justification. Select **Reset** to start
   over. Keyboard users can press Tab to move between steps and buttons, and
   Enter to select.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/book-launch-checklist/main.html"
        height="492px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who are about to
release an intelligent textbook. No programming background is needed.

### Learning Objective

Justify why each launch-checklist item must pass before an announcement goes
out, in the correct order. (Bloom's Taxonomy: Evaluate)

### Duration

15 minutes

### Prerequisites

- Has read about strict build mode and deployment verification (Chapter 29)
- Has read about the `book-metrics.json` hub and the canonical metrics
  principle (Chapter 30)
- Knows what a README and a social media preview card are

### Activities

1. **Exploration** (3 min): Before checking anything, click **7. Publish** and
   one other late step. Read what the panel says about skipping ahead.
2. **Guided Practice** (7 min): Work through all six confirmations. For each
   rejected reason, say in one sentence what is wrong with it.
3. **Assessment** (5 min): Close the MicroSim. From memory, write the seven
   steps in order and one sentence justifying each position. Then reopen the
   MicroSim and compare.

### Assessment

- The learner places the seven steps in the correct order.
- For each step, the learner gives a reason that names what the next step
  depends on, rather than restating the step.
- The learner explains why measuring the book before verifying the live site
  risks publishing stale numbers.
- The learner explains why the announcement and the README never copy figures
  from each other.

### Discussion Questions

1. Which two steps could you swap with the least harm, and what would the harm
   still be?
2. A colleague says the checklist is slow and wants to draft the announcement
   while the site is still deploying. Which later steps does that put at risk?
3. The metrics file is regenerated even when "nothing has changed". What is
   the cost of regenerating it needlessly, compared with the cost of
   publishing one wrong number?

## References

1. [Checklist](https://en.wikipedia.org/wiki/Checklist) - Wikipedia - Explains how an ordered list of confirmations reduces failures caused by skipped steps.
2. [Configuration: strict](https://www.mkdocs.org/user-guide/configuration/#strict) - MkDocs - Documents strict mode, in which the build fails on warnings such as broken links.
3. [The Open Graph protocol](https://ogp.me/) - Open Graph - Describes the page markup platforms read to build the preview shown when a link is shared.
4. [Flowcharts Syntax](https://mermaid.js.org/syntax/flowchart.html) - Mermaid - Documentation for the flowchart syntax and the `click` interaction used in this MicroSim.

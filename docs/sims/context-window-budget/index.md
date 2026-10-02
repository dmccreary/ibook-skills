---
title: Context Window Budget
description: Check items on and off to spend an example 50,000-token context window, and watch what happens to content that lands past the limit.
image: /sims/context-window-budget/context-window-budget.png
og:image: /sims/context-window-budget/context-window-budget.png
twitter:image: /sims/context-window-budget/context-window-budget.png
social:
   cards: false
quality_score: 100
---

# Context Window Budget

<iframe src="main.html" height="517px" width="100%" scrolling="no"></iframe>

[Run the Context Window Budget MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }
<br/>
[Edit in the p5.js Editor](https://editor.p5js.org/)

## About This MicroSim

A **context window** is the maximum amount of text, measured in tokens, that a
language model can consider at one time. This MicroSim treats that window as a
budget. The vertical bar is the window. Each item you check is stacked into
the bar as a colored segment, and the large number shows how many tokens are
used out of the maximum.

When the total passes the window limit, the part of the stack above the dashed
limit line turns red with a hatch pattern, and the message changes to *"These
items no longer fit — the model cannot see them."* Content past the limit is
not blurry or lower priority. It is simply not there.

!!! note "The numbers are examples"
    The 50,000-token window is an **example window size**. Real windows vary
    by model, and this MicroSim does not describe any particular one. The
    token sizes of the five items are also example values picked for the
    exercise, not measurements of real files.

| Item | Example size | What it contains |
|------|-------------:|------------------|
| System prompt | 2,000 tokens | Standing instructions that set the model's role, rules, and tools |
| Course description | 3,500 tokens | Audience, prerequisites, topics, and learning outcomes |
| Learning graph JSON | 18,000 tokens | Every concept in the book and the dependencies between them |
| One chapter draft | 4,500 tokens | The working text of a single chapter |
| Conversation history | 0 to 30,000 tokens | Every earlier message and reply in the session |

Items are stacked in the order shown, from the bottom of the bar up. In this
MicroSim, the item at the top of the stack is the one that gets cut off. Which
content a real tool drops or summarizes when a session grows too large depends
on that tool.

## How to Use

1. Start with only **System prompt** checked. Read the total: 2,000 of 50,000.
2. Check the other items one at a time and watch the bar fill from the bottom.
3. Hover over any bar segment to see that item's exact token count and what it
   contains.
4. Drag the **Conversation history** slider to the right. Moving the slider
   also checks the box.
5. Keep going until the bar passes the dashed limit line. Read the message and
   find which item is cut off in the list on the right.
6. Remove or shrink something until everything fits again.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/context-window-budget/main.html"
        height="517px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who are new to large
language models. No programming background is needed.

### Learning Objective

Demonstrate why content beyond a model's context-window limit becomes
unavailable to it. (Bloom's Taxonomy: Apply)

### Duration

10-15 minutes

### Prerequisites

- Knows what a token is (see the [Tokenization Visualizer](../tokenization-visualizer/index.md))
- Has read the definition of *context window* in Chapter 1

### Activities

1. **Exploration** (5 min): Check every item and move the slider across its
   full range. Find the largest conversation history that still fits when all
   four other items are loaded.
2. **Guided Practice** (5 min): Build three different combinations that total
   between 45,000 and 50,000 tokens. For each, note what you had to leave out.
3. **Assessment** (5 min): With everything checked and the history at 30,000,
   decide which single change brings the total back under the limit while
   keeping the most useful material. Explain your choice.

### Assessment

- The learner makes the bar overflow and states what happens to the content
  past the limit.
- The learner identifies the learning graph as the largest fixed item and the
  conversation history as the one that keeps growing.
- The learner explains why later chapters of this book load files only when
  they are needed.

### Discussion Questions

1. A session starts well under the limit. What makes it overflow an hour later?
2. Why is "just use a bigger window" not a complete answer?
3. Which item would you load only on demand, and why?

## References

1. [Large language model](https://en.wikipedia.org/wiki/Large_language_model) - Wikipedia - Background on context windows and how they bound what a model can consider.
2. [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) - Anthropic - Vendor documentation describing how a context window fills over a conversation.
3. [p5.js Reference](https://p5js.org/reference/) - p5.js - Documentation for the library used to build this MicroSim.

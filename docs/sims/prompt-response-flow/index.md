---
title: Prompt and Response Flow
description: Clickable flowchart showing how a system prompt and a user prompt combine in one model request, and why the same inputs can produce a different response on the next run.
image: /sims/prompt-response-flow/prompt-response-flow.png
og:image: /sims/prompt-response-flow/prompt-response-flow.png
twitter:image: /sims/prompt-response-flow/prompt-response-flow.png
social:
   cards: false
quality_score: 100
---

# Prompt and Response Flow

<iframe src="main.html" height="442px" width="100%" scrolling="no"></iframe>

[Run the Prompt and Response Flow MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }

## About This MicroSim

Every request to a language model carries two kinds of prompt. The **system
prompt** sets a persistent role, constraints, and available tools for the whole
session. The **user prompt** states what is wanted for this one turn. This
left-to-right flowchart follows both of them through a single request:

1. **System Prompt** and **User Prompt** both feed **Tokenization**.
2. Tokenization hands one sequence of tokens to the **Language Model**.
3. The Language Model samples the next tokens and returns a **Response**.
4. A dashed amber branch, **Same inputs, next run**, points back into the
   Language Model. It stands for nondeterminism: send the same two prompts
   again and the response may be different.

Clicking a box fills the panel below the diagram with that box's
glossary-style definition and its role in the request. For the two prompt
boxes, the panel also shows a small table comparing what each prompt carries
and how long it lasts.

| Box | Color | Meaning |
|-----|-------|---------|
| System Prompt | Dark blue | Persistent role and constraints for the session |
| User Prompt | Light blue | The specific request for this turn |
| Tokenization | Gray | Both inputs are split into tokens |
| Language Model | Teal | Predicts the next tokens by sampling |
| Response | Green | The generated text returned to the user |
| Same inputs, next run | Amber, dashed | The part that varies from run to run |

## How to Use

1. Click **System Prompt**, then **User Prompt**. Compare the two columns of
   the table: what each one carries and how long it lasts.
2. Click **Tokenization**, **Language Model**, and **Response** in order to
   follow one request from left to right.
3. Click **Same inputs, next run** and read why an identical request can come
   back with a different response.
4. Keyboard users can press Tab to move between boxes and Enter to select one.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/prompt-response-flow/main.html"
        height="442px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who are new to large
language models. No programming background is needed.

### Learning Objective

Differentiate the role of a system prompt from a user prompt in a single model
request, and explain why the response can vary. (Bloom's Taxonomy: Analyze)

### Duration

10 minutes

### Prerequisites

- Knows what a token is and what tokenization does
- Has read the definitions of *prompt* and *system prompt* in Chapter 1

### Activities

1. **Exploration** (3 min): Click all six boxes. For each one, say in your own
   words what it contributes to the request.
2. **Guided Practice** (4 min): Sort these five instructions into "system
   prompt" or "user prompt": *You are a patient tutor for adult learners*;
   *Keep concept labels under 32 characters*; *Write a glossary definition for
   "token"*; *Never invent a citation*; *Shorten the paragraph I just pasted*.
   Give a reason for each choice using the comparison table.
3. **Assessment** (3 min): A colleague runs the same skill twice and gets two
   different chapter outlines. Using the dashed branch in the diagram, explain
   what happened and suggest one change that would narrow the range of outputs.

### Assessment

- The learner assigns persistent, session-wide instructions to the system
  prompt and one-turn requests to the user prompt.
- The learner states that both prompts are tokenized and reach the model
  together.
- The learner explains that the response is sampled, so identical inputs can
  yield different responses, and that a more specific prompt narrows the range.

### Discussion Questions

1. When a skill is loaded, which of the two prompts does most of its content
   behave like? Why?
2. Why is running the same command again and hoping not a reliable way to get
   a better result?

## References

1. [Prompt engineering](https://en.wikipedia.org/wiki/Prompt_engineering) - Wikipedia - Overview of how prompts are written and structured to steer a language model.
2. [Large language model](https://en.wikipedia.org/wiki/Large_language_model) - Wikipedia - Background on tokenization and on how a model samples its output from a probability distribution.
3. [Flowcharts Syntax](https://mermaid.js.org/syntax/flowchart.html) - Mermaid - Documentation for the flowchart syntax and the `click` interaction used in this MicroSim.

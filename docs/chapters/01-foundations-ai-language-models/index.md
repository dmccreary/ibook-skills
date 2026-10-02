---
title: Foundations of AI, Language Models, and Prompting
description: Introduces artificial intelligence, large language models, tokens, and prompting, the five levels of textbook intelligence, and the terminal and Markdown skills needed to build one.
generated_by: claude skill chapter-content-generator
date: 2026-08-22 12:11:15
version: 0.09
---

# Foundations of AI, Language Models, and Prompting

## Summary

This chapter introduces artificial intelligence, large language models, tokens, and context windows, then covers prompting and prompt engineering as the interface between a person and a model. It also sets up the basic terminal, directory, and Markdown conventions used throughout the rest of the book. After completing this chapter, students will be able to explain what a large language model is and why its output is nondeterministic.

## Concepts Covered

This chapter covers the following 18 concepts from the learning graph:

1. Artificial Intelligence
2. Markdown Formatting
3. Terminal Commands
4. Large Language Model
5. Directory Navigation
6. Intelligent Textbook
7. Token
8. Prompt
9. Shell Scripting
10. Level 1 Static Content
11. Open Educational Resources
12. Tokenization
13. Context Window
14. Prompt Engineering
15. Nondeterminism in LLM Output
16. Level 2 Interactive Content
17. Creative Commons Licensing
18. System Prompt

## Prerequisites

This chapter assumes only the prerequisites listed in the [course description](../../course-description.md).

---

!!! mascot-welcome "Hi! I'm Kit."
    ![Kit waves hello with their tool satchel](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    Welcome to *Using Agent Skills to Create Intelligent Textbooks*! I'm **Kit**, a sea otter who keeps a favorite stone tucked in a canvas satchel and reaches for it the moment a task calls for it — that's what a skill is, and it's what this whole book is about. I'll be popping up in the margins of every chapter from here on, but I don't show up randomly. I have exactly **six jobs**, and you'll learn to recognize me by which one I'm doing:

    1. **Welcome you** at the start of every chapter — that's what I'm doing right now.
    2. **Help you think things through** when an idea asks you to restructure how you see something, not just memorize a fact.
    3. **Give you tips** — the shortcuts a working builder uses that nobody bothers to write down.
    4. **Warn you gently** about the specific spots where careful builders still get tripped up.
    5. **Encourage you** when a topic looks harder than it actually is.
    6. **Celebrate with you** at the end of a chapter, once you've actually earned it.

    That's it. If I'm not doing one of those six things, I'm not in the chapter. Right tool, right task — let's build something.

## What Is Artificial Intelligence?

**Artificial intelligence** (AI) is the field of building computer systems that perform tasks normally requiring human cognition — recognizing language, generating text, or making a decision under uncertainty. AI is not one program or one technique; it is a broad label covering everything from a spam filter to the system that will write most of the sentences in your finished textbook.

This book is built with, and built around, one specific kind of AI system: the **large language model**, or LLM. An LLM is a statistical model trained on enormous collections of text that learns to predict the next unit of text given everything that came before it. Predicting "the next unit of text, over and over" sounds too simple to produce a coherent paragraph, let alone a chapter — but at the scale modern LLMs operate, that simple prediction task is enough to draft a course description, design a learning graph, or write the very words you are reading now. Every skill described in this book — the course-description analyzer, the learning-graph generator, the chapter-content generator — is really a carefully structured set of instructions that steers an LLM toward one specific, repeatable kind of output.

## Inside a Large Language Model: Tokens and the Context Window

Before an LLM can predict anything, it has to break your text into pieces it can actually work with. That process is called **tokenization** — splitting raw text into the discrete units, called **tokens**, that the model consumes one at a time. A token is usually smaller than a whole word: common words are often a single token, while rarer or longer words split into two or three token fragments. This matters because everything about running an LLM — how much you can ask it to read, how much it costs to run, how fast it responds — is measured in tokens, not in words or characters.

!!! mascot-thinking "Models don't read words. They read tokens."
    ![Kit thinking with a paw on their chin](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    Here's the mental shift: when you type a sentence, you see words. The model never sees words at all — it sees a list of token IDs. "Tokenization" might become four separate tokens: `Token`, `iz`, `ation`, and a trailing space marker. Once you start thinking in tokens instead of words, a lot of this book's advice about token budgets and costs stops feeling arbitrary.

#### Diagram: Tokenization Visualizer

<iframe src="../../sims/tokenization-visualizer/main.html" width="100%" height="522px" scrolling="no"></iframe>

<details markdown="1">
<summary>Tokenization Visualizer</summary>
Type: microsim
**sim-id:** tokenization-visualizer<br/>
**Library:** p5.js<br/>
**Status:** Specified

Purpose: Help a reader see that a language model processes tokens, not words or characters.

Bloom Level: Understand (L2)
Bloom Verb: Explain

Learning objective: Explain why a language model's cost and capacity are measured in tokens rather than words.

Canvas layout:
- Top (100px): A text input box pre-filled with the example sentence "Tokenization splits text into pieces."
- Middle (300px): The same sentence re-rendered as a row of colored token chips, one chip per token.
- Bottom (100px): A running count showing "Words: 5  Tokens: 9" (numbers update live).

Data Visibility Requirements:
  Stage 1: Show the raw input sentence as plain text.
  Stage 2: Show the sentence split at word boundaries (5 word-shaped boxes), labeled "How you see it."
  Stage 3: Show the sentence split at token boundaries (9 smaller, uneven chips), labeled "How the model sees it," with sub-word tokens like "Token" + "iz" + "ation" visibly distinct colors.
  Final: Show the word count and token count side by side so the reader can compare.

Interactive controls:
- Text input: reader can type or paste their own short sentence (max 120 characters)
- Button: "Tokenize" to re-run the split on the current input
- Button: "Reset" to restore the example sentence

Default parameters:
- Default text: "Tokenization splits text into pieces."
- Token colors cycle through a 6-color accessible palette so adjacent tokens are always distinguishable

Behavior:
- On "Tokenize," animate the word-boxes morphing into the smaller token-chips (a single quick transition, not continuous animation)
- Clicking any token chip opens a small infobox above it showing: the token's text, its position index, and one sentence explaining why it split where it did (e.g., "iz and ation split off because they are common word-ending fragments seen often in training text")
- Long or unusual words (typed by the reader) should visibly split into more chips than short common words, so the reader can discover the pattern themselves

Instructional Rationale: A step-through, click-to-reveal design is appropriate because the Understand-level objective requires the reader to compare concrete data (their own sentence, word-split vs. token-split) rather than watch a passive animation. Letting the reader type their own text turns an abstract definition into a discoverable pattern.

Implementation notes:
- Use p5.js for rendering; use a simple rule-based approximate tokenizer (not a real model's exact vocabulary) since the goal is conceptual, not byte-exact
- Responsive: recompute chip layout and font size on window resize
</details>

Every model also has a hard limit on how much text it can consider at once, called the **context window**: the maximum amount of text, measured in tokens, that a model can hold in its working memory for a single request. Anything beyond that limit simply isn't there — the model cannot refer back to it, no matter how important it was. A course description, a 570-concept learning graph, and the instructions for a skill can together add up to a meaningful fraction of a context window, which is why later chapters spend real effort on keeping files small and loading them only when needed.

#### Diagram: Context Window Budget

<iframe src="../../sims/context-window-budget/main.html" width="100%" height="517px" scrolling="no"></iframe>

<details markdown="1">
<summary>Context Window Budget</summary>
Type: microsim
**sim-id:** context-window-budget<br/>
**Library:** p5.js<br/>
**Status:** Specified

Purpose: Let a reader experiment with how different files "spend" a fixed context-window budget.

Bloom Level: Apply (L3)
Bloom Verb: Demonstrate

Learning objective: Demonstrate why content beyond a model's context-window limit becomes unavailable to it.

Canvas layout:
- Left (350px): A single vertical bar representing the context window, filling from the bottom up as items are added, capped at a labeled maximum (default 50,000 tokens)
- Right (250px): A checklist of five sample items with token-cost sliders: "System prompt (2,000)", "Course description (3,500)", "Learning graph JSON (18,000)", "One chapter draft (4,500)", "Conversation history (variable, slider 0-30,000)"

Interactive controls:
- Checkbox next to each of the five items to add/remove it from the bar
- Slider for "Conversation history" (0 to 30,000 tokens)
- Display: total tokens used vs. the window maximum, in a large readable number

Default parameters:
- Window maximum: 50,000 tokens (labeled "example window size — real windows vary by model")
- All checkboxes start unchecked except "System prompt"

Behavior:
- As items are checked, the bar fills proportionally and shows a stacked-color segment per item
- If the total would exceed the maximum, the bar turns red past the limit and a message reads "These items no longer fit — the model cannot see them"
- Hovering any bar segment shows an infobox with that item's exact token count and one sentence about what it contains

Instructional Rationale: A parameter-exploration pattern fits the Apply-level objective because the reader must actively combine values and observe the consequence (overflow) rather than watch a fixed demonstration. This also reinforces the token-tokenization pairing from the diagram above it.

Implementation notes:
- Use p5.js; store items as an array of {name, tokens, checked} objects
- Responsive: bar height and control panel width recalculate on window resize
</details>

## Talking to a Model: Prompts, System Prompts, and Prompt Engineering

A **prompt** is the text supplied to a language model to elicit a response — it carries the request itself, any supporting material, and constraints on the output you want back. Every skill in this book's library is, underneath its folder structure, a very carefully written prompt. A **system prompt** is a special kind of prompt: instructions supplied separately from the user's own request, establishing a persistent role, constraints, and available tools for the whole session rather than for one message. When Claude Code loads a skill, much of what that skill defines behaves like a system prompt — it shapes how every later request in that session gets handled.

Writing prompts well enough that a model produces accurate, well-formed output *reliably* — rather than by chance — is its own discipline, called **prompt engineering**. A vague prompt ("write about learning graphs") invites a vague answer; a prompt that specifies the audience, the format, the length, and what to exclude gives the model far less room to guess wrong.

!!! mascot-tip "Specificity is the whole tip."
    ![Kit holding up a tool with a knowing look](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    If a generated result disappoints you, the fastest fix is almost never a longer explanation — it's a more specific constraint. "Keep concept labels under 32 characters" beats "keep concept labels short." Every skill in this library front-loads exactly this kind of constraint so you don't have to re-discover it by trial and error.

## Why Two Identical Prompts Can Give Different Answers

Send the exact same prompt to a model twice and you can get two different answers. This is **nondeterminism in LLM output**: the property that a model may produce different responses to identical input across separate runs, because the output is *sampled* — drawn from a probability distribution over likely next tokens — rather than computed by a fixed formula.

!!! mascot-warning "Same prompt, different answer — that's not a bug."
    ![Kit holding up a caution paw](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    A common trap: you run a skill, don't love the result, run the exact same command again expecting the same output, and get something noticeably different. That's expected behavior, not a broken skill. The fix isn't to keep re-running and hoping — it's to tighten the prompt (more specific constraints, an example of the format you want) so the *range* of likely outputs narrows, even though it never shrinks to exactly one.

#### Diagram: Prompt and Response Flow

<iframe src="../../sims/prompt-response-flow/main.html" width="100%" height="442px" scrolling="no"></iframe>

<details markdown="1">
<summary>Prompt and Response Flow</summary>
Type: workflow
**sim-id:** prompt-response-flow<br/>
**Library:** Mermaid<br/>
**Status:** Specified

Purpose: Show how a system prompt and a user prompt combine at request time, and why the same inputs don't guarantee the same output.

Bloom Level: Analyze (L4)
Bloom Verb: Differentiate

Learning objective: Differentiate the role of a system prompt from a user prompt in a single model request, and explain why the response can vary.

Visual style: Left-to-right Mermaid flowchart

Nodes:
1. "System Prompt" (rounded rectangle) — persistent role and constraints for the session
2. "User Prompt" (rounded rectangle) — the specific request for this turn
3. "Tokenization" (rectangle) — both inputs are split into tokens
4. "Language Model" (rounded rectangle, larger) — predicts the next tokens, sampling from a probability distribution
5. "Response" (rounded rectangle) — the generated text returned to the user
6. "Same inputs, next run" (dashed rectangle, off to the side, connecting back into the Language Model node) — represents nondeterminism

Edges:
- System Prompt --> Tokenization
- User Prompt --> Tokenization
- Tokenization --> Language Model
- Language Model --> Response
- "Same inputs, next run" -.-> Language Model (dashed edge, styled differently, with label "may produce a different Response")

Interactivity requirement: every node MUST have a `click` directive wired to an infobox callback showing that node's glossary-style definition. For example: `click LanguageModel call showInfo("language-model")` where the infobox pulls the matching term from the chapter glossary.

Color scheme: System Prompt and User Prompt in two distinguishable blues; Language Model in the book's accent color; Response in green; the dashed nondeterminism branch in amber to signal "this varies."

Implementation: Mermaid flowchart with per-node click handlers rendered inside the MicroSim's main.html, each opening a shared infobox panel below the diagram.
</details>

## The Five Levels of Textbook Intelligence

An **intelligent textbook** is an educational resource that combines written content with structured knowledge and interactive elements so it can adapt to and respond to a reader — rather than sitting on the page unchanged no matter who opens it. "Intelligent" is not all-or-nothing; the field measures it on a five-level scale, from a plain static page up to a fully autonomous tutor. This scale is the single most important mental model in this book, because every skill you'll learn exists to move a textbook up one of these levels.

**Level 1 — Static Content** is the lowest tier: fixed text and images with no navigation aids or interactivity, the traditional printed-page experience reproduced digitally. Over 90% of college textbooks in use today sit at this level.

**Level 2 — Interactive Content** is where a reader can engage beyond passively reading: hyperlinks that jump between related pages, embedded videos, searchable glossaries, short quizzes, and the AI-generated MicroSims you're interacting with right now in this very chapter. This is the level the skill library in this book targets by default.

**Level 3 — Adaptive Content** goes further: the material itself changes based on what a reader has already done, using personalized learning pathways and traversal of a concept graph like the one this book's chapters are built from. **Level 4 — Chatbot Integration** adds a conversational tutor, typically an LLM-powered assistant built on a technique called GraphRAG, that can answer a reader's specific question in real time rather than making them search for it. **Level 5 — Autonomous AI** is the current horizon: a system with a deep enough model of an individual reader's knowledge to generate entirely customized lessons on the fly. It remains mostly aspirational — Chapter 2 picks these three levels back up in depth, once you've met the AI coding agents that make them possible.

Before that, take a moment with the interactive model of all five levels below — hover any step to see what distinguishes it from the ones on either side.

#### Diagram: Five Levels of Textbook Intelligence

<iframe src="../../sims/book-levels/main.html" width="100%" height="502px" scrolling="no"></iframe>

[Run the Five Levels of Textbook Intelligence MicroSim fullscreen](../../sims/book-levels/main.html){ .md-button }

<details markdown="1">
<summary>Five Levels of Textbook Intelligence (reused MicroSim)</summary>
Type: infographic
**sim-id:** book-levels<br/>
**Library:** p5.js<br/>
**Status:** Reused<br/>
**Source:** docs/sims/book-levels

Reused from this book's own MicroSim catalog. Learning objective: Compare all five levels of textbook intelligence and identify which capabilities each level adds over the one before it.
</details>

Once you've explored the staircase above, this table reinforces the same five levels side by side:

| Level | Name | What It Adds |
|-------|------|---------------|
| 1 | Static Content | Fixed text and images, no interactivity |
| 2 | Interactive Content | Hyperlinks, videos, quizzes, MicroSims, glossary |
| 3 | Adaptive Content | Personalized pathways via concept-graph traversal |
| 4 | Chatbot Integration | An LLM-powered tutoring assistant (often GraphRAG) |
| 5 | Autonomous AI | Fully autonomous, real-time customized lessons |

## Openly Licensed Learning Materials

Textbooks — intelligent or otherwise — are usually built partly from material someone else created. **Open Educational Resources (OER)** are teaching materials released under terms that permit free use, adaptation, and redistribution, which is what makes it possible to build on prior work instead of starting every diagram and example from nothing. Most OER material carries a **Creative Commons license**: one of a family of standardized licenses that grant specified reuse rights while the original creator retains copyright. This book itself is released under CC BY-NC-SA 4.0, one such license — you'll see that same family of licenses again whenever a later chapter sources a chapter image from Wikimedia or a government archive.

## Your Builder's Toolkit: Markdown, the Terminal, and Directories

Everything in this book — chapters, glossary entries, the learning graph's supporting docs — is written in **Markdown formatting**: a lightweight, plain-text syntax for headings, lists, links, and emphasis that converts cleanly into the styled web pages you're reading. You've already seen it at work in the numbered concept list above and the table just before this paragraph.

To run the skills that generate that Markdown, you need two more basic tools. **Terminal commands** are text instructions typed at a command-line shell to run programs, inspect files, and manage a project — the interface an AI coding agent like Claude Code uses to actually do the work you ask for. **Directory navigation** is moving between folders in a filesystem and referring to files by an absolute path (starting from the filesystem's root) or a relative path (starting from wherever you currently are).

!!! mascot-encourage "The terminal looks scarier than it is."
    ![Kit giving an encouraging nod](../../img/mascot/encouraging.png){ class="mascot-admonition-img" }
    If a blinking cursor on a black screen makes you nervous, that's completely normal — most builders felt exactly the same way the first time. You only need a handful of commands to get productive, and you'll use the same small set over and over.

A short list is enough to get you moving around a project:

- `pwd` — print the current directory (where am I?)
- `ls` — list the files and folders in the current directory
- `cd project-name` — move into the `project-name` folder (relative path)
- `cd ..` — move up one level to the parent folder
- `cd ~/Documents/ws` — jump straight to an absolute path

## Automating Repeated Steps with Shell Scripts

Once you find yourself typing the same sequence of terminal commands more than once, it's time for **shell scripting**: writing that sequence of shell commands into an executable file so a multi-step task can be repeated identically, without retyping it or risking a step out of order. Several of the `bk-*` command-line tools you'll meet later in this book are exactly that — a short shell script wrapped around a Python program, saved once and reused for the life of the project.

## Key Takeaways

- An **AI coding agent** is powered by a **large language model**, which reads and writes **tokens**, not words, within a fixed **context window**.
- You steer a model with a **prompt**, sometimes paired with a persistent **system prompt**; because output is sampled, **prompt engineering** narrows the range of results rather than fixing it to exactly one.
- **Intelligent textbooks** are measured on five levels, from **Static Content** through **Autonomous AI** — this book's skill library targets **Level 2, Interactive Content**, by default.
- Course material is often released as **Open Educational Resources** under a **Creative Commons license** so it can be reused and adapted.
- **Markdown**, the **terminal**, **directory navigation**, and **shell scripting** are the four everyday tools you'll use to run every skill in the chapters ahead.

!!! mascot-celebration "You just built your first mental model of how this book gets made."
    ![Kit celebrating with arms raised](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    You can now explain what a large language model actually does with your text, why it doesn't always give the same answer twice, and where this book's own skill library sits on the five-level intelligence scale. Every later chapter builds directly on those ideas — nicely done. Right tool, right task!

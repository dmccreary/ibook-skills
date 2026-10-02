---
title: AI Coding Agents and the Five Levels of Textbook Intelligence
description: Covers AI coding agents, agentic workflows, hallucination and grounding, human-in-the-loop review, and a deep dive into Levels 3-5 of textbook intelligence.
generated_by: claude skill chapter-content-generator
date: 2026-08-22 12:30:00
version: 0.09
---

# AI Coding Agents and the Five Levels of Textbook Intelligence

## Summary

This chapter covers AI coding agents, agentic workflows, tool use, and the human-in-the-loop pattern that keeps a person in control of an agent's actions. It introduces the five levels of textbook intelligence and the overall textbook generation pipeline that this book follows. Students completing this chapter will be able to place a given textbook feature at the correct level of intelligence.

## Concepts Covered

This chapter covers the following 17 concepts from the learning graph:

1. Hallucination
2. AI Coding Agent
3. Level 3 Adaptive Content
4. Grounding and Verification
5. Tool Use by Agents
6. Claude Code Interface
7. Level 4 Chatbot Integration
8. Experience API
9. Agentic Workflow
10. Chat Versus Agent Interfaces
11. Level 5 Autonomous AI
12. Learning Record Store
13. Human in the Loop
14. Five Levels of Intelligence
15. Textbook Generation Pipeline
16. Iterative Refinement
17. Quality Gate

## Prerequisites

This chapter builds on concepts from:

- [1. Foundations of AI, Language Models, and Prompting](../01-foundations-ai-language-models/index.md)

---

!!! mascot-welcome "Ready for the next tool?"
    ![Kit waves hello with their tool satchel](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    Chapter 1 gave you the raw material — tokens, prompts, a five-level map of what "intelligent" even means. Now we build the thing that actually *uses* that material to write a book: an AI coding agent. Right tool, right task!

## AI Coding Agents: Beyond Chat

A large language model on its own can only produce text. An **AI coding agent** wraps that model with the ability to read files, run commands, and edit a project, so it can carry out a multi-step development task instead of just describing one. This is the **chat versus agent interface** distinction: a chat interface returns text and stops there, while an agent interface can also act on files and run commands, then read the results of those actions before deciding what to do next.

That "read the results, then decide" loop is called **tool use by agents**: the mechanism by which a model requests an action in the outside world — reading a file, running a command, searching the web — and receives the results as new input to reason over. Every skill in this library is, at bottom, a structured way of guiding that tool-use loop toward a specific outcome.

Before we compare the two interface styles side by side, notice the pattern: a chat interface is a dead end after its answer, while an agent interface's answer is a launching point for its next action.

| | Chat Interface | Agent Interface |
|---|---|---|
| Output | Text only | Text plus file edits, commands run |
| After responding | Waits for your next message | Can act, observe results, act again |
| Example | Asking a general question | Running the `learning-graph-generator` skill |

## Agentic Workflows and the Claude Code Interface

Chain enough tool-use steps together, with the model choosing each action based on the last one's result rather than following a fixed script, and you get an **agentic workflow**: a sequence of model-driven steps in which each step's output informs the next. Generating this book's learning graph is an agentic workflow — read the course description, draft concepts, check for cycles, revise, check again.

The specific environment where you run these workflows in this book's toolchain is the **Claude Code interface**: the command-line environment in which Claude reads a project, runs tools, and applies edits under your permission settings. "Under your permission settings" matters — an agent interface is powerful precisely because it can act, which is why every risky action in this book's workflow (a git push, a file deletion) waits for your explicit approval rather than running unattended.

## When Agents Get It Wrong: Hallucination and Grounding

An agent that reads files and runs commands is still, underneath, a language model predicting tokens — and language models can be confidently wrong. **Hallucination** is model output that is fluent and confident but factually wrong or unsupported by any source. A hallucinated citation reads exactly like a real one until someone checks it.

!!! mascot-warning "Confident isn't the same as correct."
    ![Kit holding up a caution paw](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    The most dangerous hallucinations are the boring, plausible ones — a citation that almost exists, a file path that's almost right. Never trust fluency as a proxy for accuracy. This book's verified-infographic pipeline exists entirely because one measured test found eight of ten numeric claims in a one-shot poster were unsupported by their cited sources.

The defense against hallucination is **grounding and verification**: tying generated claims to identifiable sources and confirming them before the claims are published. Grounding isn't a one-time check bolted on at the end — it's a discipline applied at each stage where a claim could enter the pipeline unverified.

## Keeping a Human in the Loop

Because agents can act and can be confidently wrong, this book's workflow leans on **human in the loop**: a working pattern in which a person reviews and approves agent output at defined checkpoints instead of accepting results unexamined. You've already practiced this — every chapter-structure design in this book gets presented to you for approval before a single file is written.

Reviewing once rarely produces a finished result. **Iterative refinement** is improving generated output through successive review-and-revise cycles rather than expecting a single correct pass. To make those cycles systematic rather than ad hoc, the pipeline uses a **quality gate**: a defined check that output must pass before the next stage begins, preventing a defect from silently propagating into expensive downstream work — a low-quality learning graph, caught early, is far cheaper to fix than 31 chapters built on top of it.

!!! mascot-tip "A quality gate you skip is a bug you ship."
    ![Kit holding up a tool with a knowing look](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    It's tempting to rush past a validation step when a result "looks fine." The whole point of a quality gate is that fine-looking output can still fail a structural check — a circular dependency, a missing concept — that isn't visible just by reading it.

## The Textbook Generation Pipeline

Put agentic workflows, human review, and quality gates together across an entire book, and you get the **textbook generation pipeline**: the ordered sequence of steps that turns a course description into a published book, passing through concepts, structure, content, media, and deployment. This book's own table of contents is a record of that pipeline in action — you're reading Chapter 2 of a structure that Chapter 1 (via the `book-chapter-generator` skill) produced from a 570-concept learning graph, validated at a quality gate before a single chapter file existed.

#### Diagram: Textbook Generation Pipeline

<iframe src="../../sims/textbook-generation-pipeline/main.html" width="100%" height="377px" scrolling="no"></iframe>

<details markdown="1">
<summary>Textbook Generation Pipeline</summary>
Type: workflow
**sim-id:** textbook-generation-pipeline<br/>
**Library:** Mermaid<br/>
**Status:** Specified

Bloom Level: Understand (L2)
Bloom Verb: Summarize

Learning objective: Summarize the ordered stages of the textbook generation pipeline and where human review and quality gates sit within it.

Visual style: Left-to-right Mermaid flowchart with six process nodes and two decision diamonds

Nodes:
1. "Course Description" (rounded rectangle)
2. "Learning Graph" (rounded rectangle)
3. "Quality Gate: Graph Valid?" (diamond) — branches back to Learning Graph on "No"
4. "Chapter Structure" (rounded rectangle)
5. "Chapter Content" (rounded rectangle)
6. "Quality Gate: Concepts Covered?" (diamond) — branches back to Chapter Content on "No"
7. "Media and MicroSims" (rounded rectangle)
8. "Deployment" (rounded rectangle)

Interactivity requirement: every node MUST have a `click` directive opening an infobox with that stage's one-sentence definition and which skill performs it (e.g., `click LearningGraph call showInfo("learning-graph")`).

Color scheme: process nodes in the book's teal accent; quality-gate diamonds in amber to signal a checkpoint; the "No" branch edges dashed red.

Implementation: Mermaid flowchart with per-node click handlers rendered inside the MicroSim's main.html, opening a shared infobox panel below the diagram.
</details>

## Revisiting the Five Levels: Adaptive, Chatbot, and Autonomous

Chapter 1 introduced the **five levels of intelligence**: a scale describing how responsive an educational resource is to its reader, progressing from static pages through interactive, adaptive, chatbot-integrated, and fully autonomous material. Now that you've met AI coding agents, agentic workflows, and human-in-the-loop review, you have the vocabulary to go deeper on the top three levels.

**Level 3 — Adaptive Content** is a tier of textbook intelligence in which the presented material changes based on a reader's demonstrated progress, using personalized pathways and traversal of a concept graph like this book's own. Notice what that requires: the system has to know, for each reader, which concepts they've already mastered — which is exactly the kind of per-reader data this book's skill library deliberately avoids collecting by default (more on that in a moment).

**Level 4 — Chatbot Integration** is a tier in which a large-language-model-powered conversational tutor, often built on a technique called GraphRAG, answers a reader's questions in real time rather than making them dig through the text. **Level 5 — Autonomous AI** is the highest, largely aspirational tier, in which a system deeply understands each reader's knowledge state and generates fully customized lessons in real time.

!!! mascot-thinking "Why this book stops at '2.99,' not 3."
    ![Kit thinking with a paw on their chin](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    True Level 3 requires storing per-reader performance history — and the moment a system does that, it becomes a regulated entity under student-data-privacy law. Most skills in this library are deliberately designed to sit at "Level 2.99" instead: gather as many interaction events as possible to understand how *readers in aggregate* engage with a concept, but never tie that data to one identifiable student. You get most of the pedagogical insight without taking on a data-governance obligation this project doesn't sign up for.

## Measuring Interaction: Experience API and the Learning Record Store

The "2.99" approach still needs a way to capture interaction events, just not ones tied to an individual. The **Experience API** (xAPI) is a specification for recording statements about learner activity in a consistent structure so that interactions can be collected and analyzed. A statement follows an "actor verb object" shape — a reader clicked a token chip, completed a quiz, hovered a diagram node — and each statement lands in a **learning record store**: a repository that receives and stores learner activity statements for later querying and analysis.

#### Diagram: xAPI Statement Builder

<iframe src="../../sims/xapi-statement-builder/main.html" width="100%" height="552px" scrolling="no"></iframe>

<details markdown="1">
<summary>xAPI Statement Builder</summary>
Type: microsim
**sim-id:** xapi-statement-builder<br/>
**Library:** p5.js<br/>
**Status:** Specified

Bloom Level: Apply (L3)
Bloom Verb: Construct

Learning objective: Construct a valid actor-verb-object xAPI statement and identify which field, if populated with a real name, would cross into regulated per-student data.

Canvas layout:
- Top: three dropdowns labeled Actor, Verb, Object
- Middle: the assembled statement rendered as a sentence, e.g. "anonymous-session-4471 completed quiz-token-basics"
- Bottom: a toggle labeled "Use real student name instead of session ID"

Interactive controls:
- Dropdown: Actor (anonymous-session-4471, anonymous-session-8820, or "Type a name...")
- Dropdown: Verb (completed, hovered, clicked, answered)
- Dropdown: Object (quiz-token-basics, diagram-node-llm, microsim-context-window)
- Toggle: real name vs. session ID for the Actor field

Behavior:
- When the toggle is set to "real name" and any name is typed, the statement sentence highlights in red and a message reads "This statement now identifies a specific student — outside this project's 2.99 design target"
- When using a session ID, the statement stays in the book's normal accent color with the message "Anonymous and aggregable — safe for concept-understanding analytics"

Instructional Rationale: An Apply-level construct-the-statement task makes the abstract actor/verb/object shape concrete, and the toggle turns the "2.99 versus Level 3" distinction from Chapter 2's prose into something the reader manipulates directly.

Implementation notes: Use p5.js; no real data is stored or transmitted, this is a conceptual builder only.
</details>

## Key Takeaways

- An **AI coding agent** extends a language model with **tool use**, turning single answers into an **agentic workflow** run inside an environment like the **Claude Code interface**.
- Agents can still **hallucinate**; **grounding and verification**, **human-in-the-loop** review, **iterative refinement**, and **quality gates** are how this book's pipeline catches that.
- The **textbook generation pipeline** chains those safeguards across the whole book, from course description to deployment.
- **Levels 3 through 5** of textbook intelligence add adaptive pathways, chatbot tutoring, and full autonomy — each requiring progressively more knowledge about an individual reader.
- This library targets **"Level 2.99"**: rich **Experience API** statements in a **Learning Record Store**, aggregated across readers, never tied to one identifiable student.

!!! mascot-celebration "You can now trace a claim all the way to its source."
    ![Kit celebrating with arms raised](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    You just learned why an agent's confidence is never proof, and how this book's pipeline turns that risk into a system of checkpoints instead of hoping for the best. That habit of mind — verify before you trust — is the one skill that makes every other skill in this book safe to use. Right tool, right task!

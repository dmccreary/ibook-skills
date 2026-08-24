# Content Generation Guide

Read this file **before** generating any student-facing content for this book —
chapters, lesson plans, quizzes, FAQ entries, glossary prose, or workshop
material.

Instructor-facing content (teacher guides, instructor guides, answer keys)
does **not** use the mascot described below.

---

## Learning Mascot: Kit the Otter

### Mascot File Index

The canonical files for this mascot. When editing any of these, update the
others in the same turn so they stay in sync.

| File | Purpose |
|------|---------|
| [`docs/img/mascot/character-sheet.md`](docs/img/mascot/character-sheet.md) | Canonical identity document (name, species, colors, voice). Source of truth. |
| [`docs/img/mascot/image-prompts.md`](docs/img/mascot/image-prompts.md) | Self-contained AI prompts for regenerating each pose. |
| [`docs/img/mascot/neutral.png`](docs/img/mascot/neutral.png) | Default / general-purpose pose. |
| [`docs/img/mascot/welcome.png`](docs/img/mascot/welcome.png) | Chapter-opening pose. |
| [`docs/img/mascot/thinking.png`](docs/img/mascot/thinking.png) | Key-concept pose. |
| [`docs/img/mascot/tip.png`](docs/img/mascot/tip.png) | Hint / helpful-guidance pose. |
| [`docs/img/mascot/warning.png`](docs/img/mascot/warning.png) | Common-mistake / pitfall pose. |
| [`docs/img/mascot/encouraging.png`](docs/img/mascot/encouraging.png) | Difficult-content / struggle pose. |
| [`docs/img/mascot/celebration.png`](docs/img/mascot/celebration.png) | End-of-chapter / achievement pose. |
| [`docs/css/mascot.css`](docs/css/mascot.css) | Custom admonition styles for the seven pose contexts. |
| [`docs/learning-graph/mascot-test.md`](docs/learning-graph/mascot-test.md) | Rendering test page that exercises every admonition style. |

### Character Overview

- **Name**: Kit
- **Species**: Sea otter (a young otter is called a *kit*)
- **Personality**: Resourceful, patient, curious, encouraging
- **Catchphrase**: "Right tool, right task!"
- **Visual**: A small round sea otter with warm brown fur and a cream belly,
  wearing a deep teal canvas tool satchel across the chest with a smooth
  river stone tucked in the front pouch.

**Pronouns**: Kit has no gender. Always write "Kit" or *they/them* — never
*he/him* or *she/her*.

**Why an otter, and why vendor-neutral**: sea otters carry a favorite stone in
a pouch and reach for it when a task calls for it — exactly what an agent
skill is. The design avoids every visual cue tied to a single AI company (no
robot, no spark mark, no hexagon, no vendor signature color) because these
skills run on Claude, Codex, Antigravity, Gemini, and Cursor alike.

### Voice Characteristics

- Plain, concrete language in short sentences; no jargon without a definition
- Frames skills as tools in a kit ("let's reach for the glossary generator")
- Uses a tool metaphor at most **once** per admonition — never stacked
- Refers to readers as **builders**, not "users" or "students"
- Signature phrases: "Right tool, right task!", "What does this depend on?",
  "Every tool in the kit has exactly one job."

### Mascot Admonition Format

Always place mascot images in the admonition **body**, never in the title bar,
and always use Markdown image syntax with `attr_list` — never an HTML `<img>`
tag:

    !!! mascot-welcome "Title Here"
        ![Kit waving welcome](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
        Admonition text goes here after the image.

**Image paths — Markdown and raw HTML use different base directories.**

- **Markdown images** `![alt](path)` resolve relative to the **source `.md`
  file's directory**; MkDocs rewrites them for the rendered URL. From
  `docs/chapters/01-intro/index.md` that is `../../img/mascot/`. From a
  non-index page such as `docs/learning-graph/mascot-test.md` it is
  `../img/mascot/`.
- **Raw HTML `<img src>`** is passed through verbatim, so it must be relative
  to the **rendered URL** — `../../img/mascot/` for both pages above.

Getting this wrong produces a page that displays correctly but emits a
"target is not found among documentation files" warning that fails
`mkdocs build --strict`.

### Placement Rules

| Context | Admonition Type | Frequency |
|---------|----------------|-----------|
| General note / sidebar | `mascot-neutral` | As needed |
| Chapter opening | `mascot-welcome` | Every chapter |
| Key concept | `mascot-thinking` | 2-3 per chapter |
| Helpful tip | `mascot-tip` | As needed |
| Common mistake | `mascot-warning` | As needed |
| Difficult content | `mascot-encourage` | Where builders may struggle |
| Section completion | `mascot-celebration` | End of major sections |

### Mascot Admonition Guidelines (Instructional Design Rules)

Each pose carries a distinct cognitive and pedagogical job. The pose is a
signal to the reader, not decoration — an agent that picks a pose by vibe
rather than by function destroys the wayfinding value of the whole system.

#### 1. `mascot-welcome` (Motivational Hook / Advance Organizer)

- **Instructional purpose**: Addresses the "What's In It For Me?" question and
  lowers anxiety before technical content begins. It is not there to teach the
  chapter — it is there to **sell** the chapter.
- **Rule**: Do not summarize concepts or explain mechanics. Tell the builder
  *why* they should care and *what they will be able to build* by the end.
- **Tone**: Warm and sincere, with a light tool metaphor. Include the
  catchphrase "Right tool, right task!"
- **Length**: Strictly 2-4 sentences. *(Exception: Chapter 1, where Kit
  introduces themselves and their role in the book.)*

#### 2. `mascot-thinking` (Cognitive Scaffolding / Mental Models)

- **Instructional purpose**: Marks a "eureka" moment or a shift in mental
  model. Signals that the builder should pause and process the *why*.
- **Rule**: Never use this for a mere fact or a command's syntax. Reserve it
  for the ideas a reader must restructure their thinking around — why a
  learning graph must be acyclic, why a skill is a package of instructions
  rather than a capability, why prerequisites determine chapter order.
- **Tone**: Insightful and reflective ("Notice how…", "Think of it like…").

#### 3. `mascot-tip` (Just-in-Time Support / Heuristics)

- **Instructional purpose**: A heuristic or shortcut that isn't required but
  measurably reduces friction. Expert insight whispered to a novice.
- **Rule**: Must be immediately actionable — a flag worth knowing, a way to
  sanity-check a generated graph, a naming convention. If the builder cannot
  *do* something differently after reading it, it is not a tip.
- **Tone**: Conspiratorial and clever ("Here's a shortcut…").

#### 4. `mascot-warning` (Anticipatory Guidance / Pitfall Prevention)

- **Instructional purpose**: Heads off a known pitfall, deliberately
  interrupting reading flow to prevent downstream frustration.
- **Rule**: State the pitfall, *why* it happens, and exactly how to avoid or
  recover from it. A warning without a remedy is just anxiety — always supply
  the fix.
- **Tone**: Alert but reassuring; never scolding ("A common trap here is…").

#### 5. `mascot-encourage` (Affective Support / Normalizing Struggle)

- **Instructional purpose**: Emotional support at a known point of high
  cognitive friction. Normalizes struggle and supports a growth mindset.
- **Rule**: Use ONLY when introducing a notoriously difficult topic — not as
  generic cheerleading. Validate that the difficulty is real, connect it to
  something the builder already succeeded at, and suggest a concrete way
  forward.
- **Tone**: Empathetic and validating ("If this feels like a lot, that's
  normal — most people need two passes at it.").

#### 6. `mascot-celebration` (Formative Reinforcement / Closure)

- **Instructional purpose**: Positive reinforcement and closure at a genuine
  milestone, consolidating what was learned.
- **Rule**: Never just "Good job." Name the *specific* skill the builder just
  mastered, so the achievement is concrete and reviewable.
- **Tone**: Joyful and proud ("You just built a validated learning graph —
  and that's the tool everything else in the pipeline depends on.").

#### 7. `mascot-neutral` (General Aside / Framing)

- **Instructional purpose**: A general-purpose aside for content with no
  particular emotional charge — context, a historical note, a cross-reference.
- **Rule**: Use only when none of the six purposeful poses genuinely fits.
  Reaching for `mascot-neutral` more than once or twice per chapter usually
  means the content did not need a mascot admonition at all.
- **Tone**: Calm and matter-of-fact.

### Do's and Don'ts

**Do:**

- Use Kit to introduce new topics warmly
- Include the catchphrase in welcome admonitions
- Keep dialogue brief (1-3 sentences, except the 2-4 sentence welcome)
- Match the pose to the *instructional purpose* above, not to the vibe
- Open each chapter with `mascot-welcome` and close it with
  `mascot-celebration`

**Don't:**

- Use Kit more than 5-6 times per chapter
- Put mascot admonitions back-to-back
- Use the mascot for purely decorative purposes
- Change Kit's personality or speech patterns
- Use more than one `mascot-welcome` or `mascot-celebration` per chapter
- Introduce a vendor-specific visual or verbal cue into Kit's voice

## Quality Assurance & Validation

Language models drift away from strict formatting constraints, so mascot
placement must be checked programmatically rather than by eye.

**Post-generation rule**: after writing or editing any chapter, run the
validator before reporting the work complete:

```bash
python skills/book-installer/scripts/validate-chapter-mascots.py docs/chapters/NN-slug/index.md
```

It flags: more than 6 mascot admonitions in a chapter, duplicate
`mascot-welcome` or `mascot-celebration`, back-to-back mascot admonitions, any
admonition missing its `mascot-admonition-img` image, and body text clearly
outside the 1-3 sentence rule.

If the validator reports issues, fix the chapter and re-run until it exits
clean. Do not report completion on a chapter that still fails, and do not
relax a rule to make the check pass.

## Concept Depth & Word-Count Targets

Not every concept deserves equal space. A concept that many other concepts
depend on — directly or transitively — needs more careful explanation, since
a shaky foundation cascades into everything built on top of it, while a leaf
concept that nothing depends on can be treated more lightly.

**This is now driven by each concept's Concept Impact Score (CIS)**, a
PageRank-style recursive importance measure computed by
`learning-graph-generator` (v1.06+) and written into `learning-graph.json` as
`node.cis`: `CIS(x) = 1 + sum(CIS(d) for d in direct dependents of x)`. CIS
supersedes a plain dependents count because it captures *transitive* impact —
a concept with only one or two direct dependents can still be highly
foundational if those dependents themselves have many dependents, which raw
in-degree misses entirely.

`book-chapter-generator` (v1.0.0+) writes each concept's CIS into its
chapter's "Concepts Covered" table, and `chapter-content-generator` (v1.09+)
converts CIS into a per-concept word-count and required-element budget in its
**Elaboration Budget** step (Step 2.3b): CIS is normalized globally against
the book's maximum CIS into an Elaboration Score `E(c)`, then assigned a tier:

| Tier | `E(c)` range | Target words | Required elements |
|------|--------------|---------------|--------------------|
| A (full treatment) | `>= 0.5` | 500-750 | worked example + diagram/chart/table/MicroSim |
| B (standard) | `0.2 <= E(c) < 0.5` | 250-400 | worked example |
| C (brief) | `< 0.2` | 120-200 | clear definition; example optional |

A chapter's total word count is the **sum** of its concepts' individual
targets, not an independent flat number — a chapter with several Tier A
concepts will naturally run longer than one of mostly Tier C concepts, and
that variation is intentional, not something to normalize away.

For the exact normalization formula, tier cut-points, and worked table
format, see `skills/chapter-content-generator/SKILL.md`, Step 2.3b
("Compute the Elaboration Budget (CIS-Driven)") — that skill is the
canonical source; this section is a summary so writers know the *why*
without duplicating the math in two places that could drift out of sync.

## Anti-Padding & Writing Style Rules

Models inflate text to hit word-count targets, producing repetitive and
sometimes hallucinated content. All generating agents must follow these rules.

1. **Quality over quantity.** Per-concept Elaboration Budgets (see *Concept
   Depth & Word-Count Targets* above) are guidelines, not requirements. A
   dense, correct chapter beats a padded one at the target length. Never
   inflate length artificially — a Tier A concept should reach its target
   through a worked example or MicroSim walkthrough, never restated prose,
   and a Tier C concept should stop once it is correctly explained even if
   that's well under its target.
2. **Expand by showing, not telling.** If a chapter is genuinely thin, add a
   concrete worked example, another MicroSim, or more technical detail. Never
   expand by restating earlier paragraphs, summarizing what was just said, or
   adding generic filler.
3. **No formulaic templates.** Avoid boilerplate scaffolding like "Let's talk
   about X. The concept of X is fundamental…". Weave concepts into flowing
   narrative prose.
4. **Examples over prose.** When explaining abstract logic, prefer a short
   commented example or a MicroSim to a long descriptive passage.

## MicroSims (Interactive Examples)

This book targets Level 2+ textbook intelligence, so interactivity is a
pedagogical requirement rather than a garnish.

- **Requirement**: whenever a concept can be illustrated with a dynamic,
  interactive example, include a MicroSim rather than describing it in prose.
- **Format**: embed finished MicroSims with an `<iframe>` pointing at the
  simulation's `main.html`, followed by a fullscreen button link.
- **Tools**: p5.js for physics, graphics, and simulation; Chart.js for data;
  vis-network for graphs; Mermaid for flow and sequence diagrams.

## Markdown Formatting Rules

1. **List spacing.** EVERY Markdown list — bulleted or numbered — MUST have a
   blank line before it. MkDocs will not render the list otherwise.
2. **Image paths.** See the Mascot Admonition Format section above; Markdown
   and raw HTML resolve against different base directories.
3. **Admonition bodies** are indented four spaces, with the mascot image on
   the first line of the body.

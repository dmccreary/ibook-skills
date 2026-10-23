# Intake Interview

The interview gathers the content a high-quality paper needs. It goes on until the
**readiness score** (the projected rubric score) is at least 80 and no blocker remains.

## Content checklist

Each item feeds one or more rubric criteria (numbers refer to `quality-rubric.md`).
**Blockers** must be resolved before drafting, whatever the readiness score.

| # | Content item | Feeds | Blocker |
|---|--------------|-------|:-------:|
| 1 | Working title and a one-sentence thesis: what the paper claims or contributes | 1, 3, 4 | ✔ |
| 2 | Authors: full names, affiliations, contacts, ORCIDs, author order | 2 | ✔ (names) |
| 3 | Paper type: framework/position, system/tool, empirical study, or survey | 6, 7 | |
| 4 | The problem, why it matters now, and who is affected | 3, 4 | |
| 5 | The gap: what existing approaches, tools or theories miss | 4, 5 | ✔ |
| 6 | The contributions, as 2–4 specific bullet points | 3, 4, 6 | ✔ |
| 7 | Details of the contribution: components, definitions, design decisions and rationale, alternatives rejected | 6, 12 | ✔ |
| 8 | Evidence: data, experiments, deployments, usage numbers, case studies, worked examples | 7, 13 | ✔ (at least worked examples) |
| 9 | Prior work: papers, systems, standards and authors the paper must engage with | 5, 10 | |
| 10 | Limitations the author already knows, and what a skeptical reviewer would say | 8 | |
| 11 | Implications and future work | 8, 9 | |
| 12 | Figures: existing images, screenshots, data for charts, diagrams to draw | 11 | |
| 13 | Audience, arXiv category, and target venue if any | 16 | |
| 14 | Length target, license, version number, AI-use disclosure wording | 16 | |

## Readiness score

After each round, estimate the most the paper could earn on each rubric criterion given
the content in hand:

- **A–C (criteria 1–13, 80 points)** depend on content. Score each one by the descriptor
  the available material would support. For example, related work with 4 known sources
  and no comparison supports 3 of 7. Evidence from one worked example supports 3–6 of 8.
- **D–E (criteria 14–17, 20 points)** are largely within the skill's control. Assume
  full marks, unless the material is so thin that the writing would have to be padded
  (cap criterion 17 at 4).

So a readiness of 80 means at most 20 of the 80 content points are at risk. Record the
breakdown in `brief.md`, so later sessions can see why drafting started or didn't.

## How to run the rounds

Ask 2–4 related questions per round. Before each round, pre-fill what the source
material already answers, and ask the user to confirm or correct it. That is faster
than asking them to write from scratch. Use multiple-choice prompts where the options
are known (paper type, category, license).

### Round 1: the core (always)

- "Here's the thesis I'd draw from <source>: '<one sentence>'. Is that the claim, or
  is it something else?"
- "What is new here: what can a reader do or know after this paper that they couldn't
  before? Give me 2–4 bullet points."
- "Who should read this, and which field's reviewers will judge it?" (This determines
  the paper type and the arXiv category.)
- "Authors: full names, in order, with an affiliation and a contact for each."

### Round 2: evidence

- "What shows this works or is true? Data, a deployment, measurements, user feedback,
  case studies?"
- "Any numbers I can quote, with their source? (For example: how many sims, users,
  pages, hours saved, scores.)"
- "Which 2–3 concrete examples best show the idea in action?"
- If the answer is "none yet", offer to reframe the paper as a framework or position
  paper, with worked examples and a proposed evaluation plan, rather than invent
  results.

### Round 3: positioning

- "Which papers, systems or standards must this paper engage with? Any you want cited?"
- "What's the closest existing work, and how is yours different?"
- "What would a skeptical reviewer object to?" (This feeds Limitations.)

### Round 4: figures and logistics

- "Which figures do you picture? Any existing diagrams, screenshots, posters or data
  I should use?"
- "License: CC BY 4.0 (most open), CC BY-NC-SA 4.0, or arXiv's default non-exclusive
  license?"
- "Target length, and any venue (conference or journal) this preprint is headed for?"

### Round 5 and later: fill the gaps

For each rubric criterion projected below 70% of its points, ask one targeted question
that would raise it. Stop when readiness is at least 80 with no blockers. Don't keep
asking for its own sake: once the content supports the paper, more questions only
burn the author's patience.

## Good follow-ups

- Vague answer → "Can you give me a specific example?" / "Roughly how many?"
- Claimed benefit → "How do you know? Is there a measurement, a source, or an anecdote?"
- Broad scope → "If the paper could make only one claim, which one?"
- Buzzword → "What does <term> mean precisely in this paper?"

## Mining a large source (a book, docs site or course)

- The thesis usually lives in: the course description or overview, chapter 1 (the
  framing), the final chapter (the synthesis), and any "why" or motivation pages.
- Evidence lives in: case-study chapters, appendices, data files, posters with numbers,
  MicroSims, and logs.
- Prior work lives in: per-chapter `references.md` files and the glossary. These are a
  starting pool; verify every entry before citing it.
- A book covers far more than one paper can. Pick the **one** argument the book makes
  that is most novel, and let everything else support it or go. A paper that
  summarizes a 20-chapter book reads like a table of contents.

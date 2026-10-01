# Writing Precise MicroSim Specifications

A specification block tells the MicroSim generator **what the learner must learn, what the learner must
do to show it, and exactly what content the sim must contain**. It does not tell the generator how to
build the sim. Layout, pixel sizes, canvas height, control placement, responsive breakpoints, fonts,
colors and library calls are the generator's job: the microsim-generator skill has rules for all of
them that a chapter author cannot see, and specs that prescribe them only create conflicts.

These rules come from a batch run that built 112 MicroSims from chapter specifications. The agents
reported 450 places where a spec was missing something they had to invent, and 49% of the sims had to
depart from their spec. The gaps fell into a few patterns, and every rule below prevents one of them:

| What went wrong | Sims affected | Rule |
|---|---|---|
| The spec named the kind of content but did not supply it (a "bank of 12 cards" with 4 given) | 91 | R4 |
| A behavior had no rule: thresholds, formulas, ranges, edge cases | 56 | R6 |
| An interaction had no stated effect or resulting state | 53 | R7 |
| A quiz or check had no item count, correctness rule or feedback | 37 | R8 |
| The spec contradicted itself (mostly layout paragraphs that disagreed) | 34 | R11, R12 |
| The spec disagreed with its own chapter, a cited source or the library | 29 | R10, R13 |
| The activity could not produce the evidence the objective names | 10 (+25 fixed by adding assessment) | R2 |
| The Bloom level could not be parsed by the batch tools | 109 | R1 |

## The Specification Block

Place the block right after the prose that defines every term it uses (see Step 2.4 "Scaffolding").
Do not add an iframe for a new specification: the MicroSim generator inserts it, with the correct
height, after the sim is built.

```markdown
#### Diagram: <Title Case Name>

<details markdown="1">
<summary><Title Case Name></summary>
Type: <microsim | chart | diagram | infographic | timeline | map | workflow | graph-model | causal-loop>
**sim-id:** <kebab-case-id><br/>
**Library:** <p5.js | Chart.js | Plotly | Mermaid | vis-network | vis-timeline | Leaflet | venn.js | html><br/>
**Status:** Specified<br/>
**Bloom Level:** <Remember | Understand | Apply | Analyze | Evaluate | Create><br/>
**Bloom Verb:** <one verb from that level's list><br/>
**Learning Objective:** The learner will <verb> <specific content> <condition or criterion>.

**Prerequisites:** <terms and ideas the learner must already have; each is defined in the chapter above this block>

**Evidence of Mastery:** <the learner action that demonstrates the verb, and the rule that decides whether it is correct>

**Misconceptions:** <the wrong ideas this sim should expose and correct, or "none">

**Instructional Rationale:** <why this kind of activity produces the evidence at this Bloom level>

**Content:** <every item, value, definition, example and label the learner sees, written out in full>

**Provenance:** <where each part of the content comes from>

**Rules:** <the domain model the sim must obey: formulas, thresholds, ranges with units, tie-breaks, edge cases>

**Learner Activity:** <numbered steps: what the learner does, what changes, what the learner should notice>

**Feedback:** <what the learner is told, when, and how many attempts they get>

**Starting State:** <what the learner sees before touching anything, and the question it poses>

**Chapter Anchors:** <every number, name and claim the chapter prose states about this sim, or "none">
</details>
```

Formatting rules the batch tools depend on:

- The six header lines (`sim-id`, `Library`, `Status`, `Bloom Level`, `Bloom Verb`, `Learning Objective`) use
  exactly these bold labels. The first five end with `<br/>`. The Learning Objective line is followed by a blank
  line. Put nothing else on these lines: `**Library:** p5.js (suggested)` breaks CDN selection.
- `Bloom Level` is the bare level name (`Analyze`), not `Analyze (L4)` and not a sentence.
- Each body field is its own paragraph, separated by blank lines. Lists inside a field need a blank line before them.
- Do not indent any line inside the `<details>` block.

## Rules for Each Field

### R1. One objective, one level, one verb

Write a single objective that starts with "The learner will", uses one verb from that level's list in
`blooms-taxonomy.md` Part 1, names the specific content, and states a condition or criterion.

- ❌ `Learning objective (Bloom level: Understand; verb: summarize): The learner will understand Bloom's levels.`
  The inline parenthetical format could not be parsed, so the tools labeled 109 of 112 sims "Create". "Understand"
  is not a measurable verb.
- ✅ `**Bloom Level:** Understand` / `**Bloom Verb:** summarize` /
  `**Learning Objective:** The learner will summarize what each of the six Bloom levels asks a learner to do, given the level's name.`

Never write "understand", "learn", "know about", "explore" or "be familiar with" as the verb. If the sim
serves two objectives, split it into two sims or pick the one the sim can actually assess.

### R2. Evidence of Mastery must be something the activity can produce and check

Name the action that demonstrates the verb and the rule that decides correct from incorrect. Then check
that the Learner Activity actually lets the learner perform that action. Every noun in the objective
must appear in the Content, and every verb must map to an action whose correctness the sim can judge.

- ❌ "The learner will choose the best library for a stated need", but the sim offers no way to state a need.
- ❌ "Resolve the winning setting across five configuration layers", but the activity has only three choices.
- ❌ "Identify the four node shapes", but the Content defines three.
- ❌ An accessibility checker with four checks, two of which can never fail on the given examples.
- ✅ "The learner assigns each of the 10 events to one of four verbs; an assignment is correct when it matches the
  answer column in Content. Mastery: 8 of 10 correct on the first attempt."

Separate evidence from exploration. A committed answer, a locked-in prediction or a submitted
ranking is evidence; hovering, dragging a slider and opening an infobox are exploration. Say which
actions count as evidence, because that is what the book's interaction data will measure.

### R3. Match the activity to the level, and say why

Use the pattern table in `content-element-types.md` ("Instructional Pattern Selection"), and state the
reason in **Instructional Rationale** in one or two sentences: why this kind of activity makes the learner
perform the verb, at this level, rather than just watch. For
Understand and Analyze objectives, include a step where the learner **predicts before the answer is
revealed**. Do not ask for continuous animation for an Understand objective unless the objective is
about motion itself. Ask for step-through with the concrete data visible at each step.

### R4. Write the Content out in full

If the learner sees N items, list all N. Never write "for example", "such as", "etc." or "a bank of 12
cards" followed by four. For anything the learner classifies, sorts, ranks or answers, give a table
with the item, the correct answer and the one-sentence reason. The reason becomes the feedback.

- ❌ "Twelve short descriptions, for example: a five-minute video on photosynthesis (Learning Object)..." (4 of 12 given)
- ❌ "Three datasets suited to different chart types." (no values, labels or units)
- ❌ "Six described objectives for the learner to route." (none given)
- ✅

```markdown
| # | Description shown to the learner | Correct bin | Why (shown as feedback) |
|---|---|---|---|
| 1 | A five-minute video on photosynthesis with a catalog record | Learning Object | Reusable and described, but it has no model the learner changes |
| 2 | ... all remaining items ... | ... | ... |
```

Keep banks small enough to write in full; 8–15 items is typical for one sim. Give a generation rule
instead of items only when the content really is procedural, such as random numeric problems. Then
state the rule, the value ranges and two worked instances.

Datasets list every value with its unit. Maps list every place with its coordinates. Timelines list
every event with its date. Code or text the learner reads is written out verbatim.

### R5. State where the content comes from

Every factual value needs a source. Use one of these forms:

- **From the chapter:** name the section. The values must match the prose exactly (see R10).
- **From a file or page:** give the path or URL and say exactly what to take. If several versions of the file
  exist, name the one. Say whether to copy it into the sim folder. "Mirror validation.py" and "use the design
  document's estimates" are not enough.
- **Synthetic:** give the generating rule and a seed, and require the sim to label the data "synthetic".
- **Illustrative:** invented numbers that only show a pattern. Require the sim to label them "illustrative".

Never let the generator invent real-world facts such as coordinates, dates, statistics, prices or
quotations. In the batch run, one map's coordinates were "entered from memory".

### R6. Give the Rules as a model, not a description

Anything the sim computes or judges needs its rule:

- formulas, with units
- thresholds with the exact comparison: "mastered when P(L) >= 0.95", not "above 0.95"
- how ties and boundary cases are decided
- what happens at degenerate values: division by zero, an empty set, the first or last item
- for every quantity the learner can change: minimum, maximum, step, default and unit

The default must sit on the step grid. The range must cover every value the chapter mentions and every
value the sim can compute. For example, a 200–900 range with step 2 cannot show a total of 1102, and a
default of 0.635 does not sit on a step of 0.01.

Describing these ranges is part of the learning design, because they decide which cases the learner can
explore. How the learner sets them (slider, box, buttons) is the generator's choice.

### R7. Describe the Learner Activity as actions and consequences

Write numbered steps in terms of what the learner does and what they should notice, not in terms of
widgets. For each action say what changes and what state follows.

- ❌ "A createSelect dropdown in the top-left of the drawing region."
- ❌ "Toggle 'Threshold for mastered'." (toggle between which values?)
- ❌ "Step advances the sketch." (one statement per step, or one frame?)
- ✅ "3. The learner chooses the threshold, 0.80 or 0.95. Every concept's mastered/not-mastered mark updates at once.
  The learner should notice that two concepts change status at 0.95."

Say what happens to an answer that has already been revealed when the learner changes an input:
it is hidden again, re-checked, or kept. Say how the item an action applies to is chosen: the selected
one, the next one, or all of them.

### R8. Specify Feedback completely

For every action that can be right or wrong, state:

- how many items the learner answers, and in what order (fixed or shuffled)
- how many attempts they get, and whether an item can be re-answered
- what counts as correct, including any numeric tolerance ("within ±0.05 s")
- the correct-answer feedback, and the incorrect-answer feedback, which names the misconception behind the likely
  wrong answer (use the "Why" column from R4)
- when the correct answer is revealed
- whether a score is shown, and what it counts

### R9. Describe meaning, not appearance

When color, shape or position carries meaning, say what the meaning is ("concepts below the threshold
are marked as not yet mastered"), not which color to use. The generator picks colors that are
color-blind safe and pairs them with a second cue. Do not ask for red/green pairs.

Do not let a label give away an answer. Naming loops "A" and "B" is safer than naming them
"Loop B (balancing)" when the task is to find the balancing loop.

### R10. Keep the spec and the chapter in agreement

List under **Chapter Anchors** every number, count, name and claim the chapter prose states about this
sim. The spec must match each one exactly. Common failures in the batch run:

- The chapter discusses 13 MicroSim types, but the spec asked for 12 buttons.
- A later chapter's worked example used this sim with a canvas of 450, but the spec produced 500.
- The chapter's table has four measured rows, but the spec's model reproduced only one.

If the chapter describes a real tool's behavior (an error message, a file name, the order of checks), the
spec must match the real tool, and **Provenance** must point to it.

### R11. State each fact once

Contradictions come from saying the same thing twice in different paragraphs. Say each fact in exactly
one field and refer to it elsewhere. If the objective says "dark rows mean struggling students", the Content
must not say the opposite. If a preset needs six attempts, the Content cannot hold only four.

### R12. Leave build decisions to the generator

Do not specify any of these:

- pixel sizes, canvas height, width, `drawHeight` or `controlHeight`
- positions, regions, left/right placement, which region the controls go in
- responsive breakpoints or narrow-screen layouts
- fonts, colors, palettes, line widths
- library function names (`createSlider`, `createSelect`, `describe()`), frame rates, animation timing
- an `Implementation:` line

The generator already applies its own rules for these: controls always sit in a separate control area,
sims are width-responsive inside a fixed-height iframe, palettes are color-blind safe, and every action
has a keyboard path. Specs that prescribed placement caused most of the layout contradictions, and ten
sims put controls in the drawing region, which the p5.js generator forbids.

**Exception:** when a visual property is the content being taught, state it as Content. Examples: a sim about
contrast ratios lists the color pairs to judge, a sim about layout defects describes each defect, and a sim about
breakpoints gives the widths.

### R13. Do not require what embedded sims cannot do

Phrase interactions by what the learner must be able to learn ("the learner can reveal what each
connection means") rather than a mechanism that may not exist. Known impossibilities:

- Mermaid cannot make edges clickable. Put edge meanings in node infoboxes or edge labels.
- Mermaid has no reverse arrow (`<--`). Use the diagram's direction instead.
- Mouse-wheel zoom is not allowed inside an embedded page, because it hijacks page scrolling. Use buttons.
- A sim cannot read files outside its own folder once published. Content from elsewhere must be copied in
  (see R5).

### R14. Choose Type and Library from the lists

Both fields must use one of the listed values; free text such as "HTML and CSS" or "Mermaid with a click
directive on every node" is not recognized by the batch tools and silently falls back to p5.js. Choose by
the shape of the content, not by preference:

| The content is... | Type | Library |
|---|---|---|
| dated events | timeline | vis-timeline |
| places with coordinates | map | Leaflet |
| a function of one variable to plot | chart | Plotly |
| a bar, line, pie, bubble or radar chart | chart | Chart.js |
| a flowchart or process whose steps the learner clicks | workflow | Mermaid |
| nodes and edges, a concept map, dependencies | graph-model | vis-network |
| feedback loops (systems thinking) | causal-loop | vis-network |
| overlapping sets | diagram | venn.js |
| a comparison table or clickable matrix | diagram | html |
| a picture with callout labels | infographic | html |
| anything else: simulations, sorters, builders, step-throughs | microsim | p5.js |

The Library is a routing hint for the batch tools. The generator may change it if the content fits
another library better.

## Self-Check Before Finishing a Chapter

Run this check on every specification block. Fix each failure before writing the chapter.

- [ ] `Bloom Level` is one of the six names. `Bloom Verb` is in that level's list. The objective starts
      "The learner will <that verb>".
- [ ] The Evidence of Mastery action is possible in the Learner Activity, and has a correctness rule.
- [ ] Every noun in the objective appears in the Content. Every count stated ("12 cards") matches the items listed.
- [ ] No "for example", "such as", "etc." or "a few" in Content.
- [ ] Every factual value has a Provenance. Synthetic and illustrative data are required to be labeled.
- [ ] Every threshold uses `>=`, `>`, `<=` or `<`. Every adjustable quantity has min, max, step, default and unit.
      Defaults sit on the step grid, and ranges cover every value mentioned.
- [ ] Every action that can be right or wrong has Feedback, attempts and a reveal rule.
- [ ] Every number in the spec matches the chapter prose, and Chapter Anchors lists them.
- [ ] No pixel sizes, positions, colors, fonts, breakpoints, library calls or `Implementation:` line, unless the
      property is itself the content.
- [ ] No Mermaid edge clicks, reverse arrows or mouse-wheel zoom.
- [ ] `Type` and `Library` come from the R14 table.
- [ ] Every term the spec uses is defined in the chapter prose before the block.

## Complete Example

```markdown
#### Diagram: Pendulum Period Calculator

<details markdown="1">
<summary>Pendulum Period Calculator</summary>
Type: microsim
**sim-id:** pendulum-period-calculator<br/>
**Library:** p5.js<br/>
**Status:** Specified<br/>
**Bloom Level:** Apply<br/>
**Bloom Verb:** calculate<br/>
**Learning Objective:** The learner will calculate the period of a simple pendulum from its length and the gravitational field strength, to within 0.05 s.

**Prerequisites:** period, simple pendulum, gravitational field strength, square root (all defined in the section "The Pendulum Equation" above).

**Evidence of Mastery:** For three challenge pendulums, the learner types a calculated period before the pendulum is released. A calculation is correct when it is within ±0.05 s of the model value. Mastery is 3 of 3 correct. Exploration (changing length, mass or amplitude and watching) is not evidence.

**Misconceptions:** (1) A heavier bob swings more slowly. (2) A wider swing takes longer. (3) Doubling the length doubles the period.

**Instructional Rationale:** Apply-level calculation needs practice with a check, so the learner commits a number before the pendulum is released. Free exploration comes after the challenges, where it confronts the three misconceptions with measurements.

**Content:**

The learner can change three quantities and choose a location:

| Quantity | Min | Max | Step | Default | Unit |
|---|---|---|---|---|---|
| Length L | 0.25 | 4.00 | 0.25 | 1.00 | m |
| Bob mass m | 0.5 | 2.0 | 0.5 | 1.0 | kg |
| Release angle | 5 | 15 | 5 | 10 | degrees |

Locations: Earth (g = 9.81 m/s²), Moon (g = 1.62 m/s²), Jupiter (g = 24.79 m/s²). Default: Earth.

Challenge pendulums, in this order:

| # | L (m) | Location | Model period (s) | Feedback when wrong |
|---|---|---|---|---|
| 1 | 1.00 | Earth | 2.01 | Use T = 2π√(L/g): √(1.00/9.81) = 0.319, times 2π is 2.01 s. |
| 2 | 4.00 | Earth | 4.01 | Four times the length gives √4 = 2 times the period, not 4 times: 2 × 2.006 s = 4.01 s. |
| 3 | 1.00 | Moon | 4.94 | Weaker gravity means a longer period: √(1.00/1.62) = 0.786, times 2π is 4.94 s. |

The equation shown after a calculation is checked: T = 2π√(L/g).

**Provenance:** The g values are standard reference values for surface gravity. Model periods are computed from the Rules and rounded to 0.01 s.

**Rules:** T = 2π√(L/g), the small-angle model. Mass does not appear in the model. The release angle changes the true period by under 0.5% at 15°, so the model treats it as having no effect, and the sim says so when the learner changes it. The measured period shown after release is the model value.

**Learner Activity:**

1. The learner reads challenge 1 (length and location) and types a period in seconds.
2. The learner presses Check. The sim releases the pendulum, times 5 swings, and shows the measured period next to the learner's answer.
3. After all three challenges, the free-exploration mode unlocks: the learner changes length, mass, angle and location, and the measured period updates after each release.
4. In exploration, changing mass or angle leaves the period unchanged. The sim points this out the first time each is changed ("Mass changed from 1.0 to 2.0 kg: period still 2.01 s").

**Feedback:** Three challenges, fixed order, two attempts each. Correct: "Correct: T = <model value> s." Incorrect: the "Feedback when wrong" text for that challenge. After the second wrong attempt the model value and the worked calculation are shown, and the challenge counts as missed. A running count "Challenges correct: n of 3" is shown.

**Starting State:** Challenge 1 is shown with an empty answer box and the pendulum at rest at 10°. The question on screen is "How long will one full swing take?"

**Chapter Anchors:** The chapter's worked example uses L = 1.00 m on Earth and gets 2.01 s. The chapter states that quadrupling the length doubles the period.
</details>
```

Note what the example leaves out: where the controls go, the canvas size, the colors, the animation
speed and the library calls. The generator decides all of those.

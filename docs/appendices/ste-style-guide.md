# Simplified Technical English (STE) Style Guide for Intelligent Textbooks

This guide defines a shared writing style for the agents that write chapter content.
Each book's `CONTENT-GENERATION-GUIDE.md` links to this file and declares one STE level.

!!! note "Not a certified standard"
    This style is **inspired by** ASD-STE100 Simplified Technical English (Issue 9, 2025).
    It does not claim compliance with the standard.
    The official standard was written for maintenance procedures.
    This guide adapts its ideas for teaching.

## Purpose

STE-inspired writing helps in four ways:

- Readers who learn English as a second language understand the text faster.
- Machine translation is more accurate.
- Procedures and definitions have only one possible meaning.
- Generated text is more consistent from chapter to chapter.

The goal is clear text that is still interesting to read.
Clarity is not the same as dullness.

## Declaring the STE Level

Each book sets one level in its `CONTENT-GENERATION-GUIDE.md`:

```markdown
**STE level for this book:** light   <!-- none | light | strict -->
```

| Level | Use when | Effect |
|-------|----------|--------|
| `none` | Reflective or advanced texts where nuance matters more than simplicity | This guide does not apply. |
| `light` | Most books. Mixed audiences, K-12, college, ESL readers | Core rules apply everywhere. Strict rules apply only to strict content types. |
| `strict` | Procedure-heavy books, or books for translation or low-bandwidth ESL audiences | Strict rules apply to all content except designated story elements. |

If a book does not declare a level, use `light`.

## Core Rules (levels `light` and `strict`)

These rules apply to all body text.

1. **One term, one meaning.**
   Use each glossary term exactly as defined in the ISO 11179 glossary.
   Do not replace a term with a synonym.
   Do not use the same word with a second meaning.
2. **Use active voice.**
   Write "The sensor sends a signal."
   Do not write "A signal is sent by the sensor."
3. **Use simple verb tenses.**
   Prefer present tense for facts and instructions.
   Use past tense for history and examples.
   Avoid complex tenses unless the meaning needs them.
4. **Keep paragraphs short.**
   Use six sentences or fewer in one paragraph.
5. **Avoid idioms and slang.**
   Do not write "rule of thumb," "a ballpark figure," or "hit the ground running."
   Write what you mean in plain words.
6. **Avoid phrasal verbs when one plain verb works.**
   Write "start" and not "kick off."
   Write "remove" and not "take out."
7. **Break up noun stacks.**
   Do not put more than three nouns in a row.
   Write "the gain of the feedback loop" and not "feedback loop gain value."
8. **Write full words.**
   Define each abbreviation on first use in a chapter.
9. **Keep articles and linking words.**
   Do not drop "the," "a," or "is" to save space.
10. **Use numerals for measurements and counts.**
    Write "5 volts" and not "five volts."

## Strict Content Rules

Apply these rules in `light` books **only** to the content types in this table.
Apply them to all content in `strict` books, except designated story elements.

| Content type | Where it appears |
|--------------|------------------|
| Procedures | Lab steps, "Try it" instructions, MicroSim usage instructions |
| Definitions | Glossary entries, inline definitions |
| Warnings and cautions | Safety notes, common-mistake alerts |
| Quiz items | Questions, answer choices, and explanations |

### Rules for strict content

1. **Write one action per step.**
   Put one instruction in each numbered step.
2. **Use the imperative voice for instructions.**
   Write "Connect the red wire to pin 3."
   Do not write "You should connect the red wire to pin 3."
3. **Keep sentences to 20 words or fewer.**
4. **For warnings, put the command first and the reason second.**
   Write "Disconnect power before you touch the circuit. Live wires can cause injury."
5. **For definitions, write one sentence in the form "A [term] is a [category] that [distinguishing feature]."**
   Do not add examples to the definition sentence. Put examples in the next sentence.
6. **For quiz items, remove ambiguity.**
   Do not use negatives in the question stem.
   Make each distractor wrong for one clear reason.

## Light Content Rules

Apply these rules to explanations, narratives, analogies, and chapter openers in `light` books.

1. **Keep sentences to 25 words or fewer on average.**
   A few longer sentences are acceptable if the meaning stays clear.
2. **Vary the sentence length.**
   Follow two medium sentences with a very short one for emphasis.
3. **Use concrete analogies in plain words.**
   Compare new ideas to physical objects the reader knows.
4. **Ask questions.**
   A direct question keeps the reader thinking.
5. **Speak to the reader.**
   Use "you" and "your."
6. **Tell short stories.**
   Use a person, a problem, and a result in three to five plain sentences.

## How to Keep the Text Interesting

STE limits vocabulary and sentence structure. It does not limit imagination.
Put the personality of the book in these places:

- **Characters.** Use a recurring student, robot, or team that faces problems.
- **Analogies.** Choose vivid, physical comparisons.
- **Challenges.** End sections with a "What would happen if...?" question.
- **Structure.** Use "Try it" boxes, MicroSim prompts, and short reflection questions.
- **Situational humor.** Funny situations translate across cultures. Wordplay and idioms do not.

### Example: flat and engaging versions

Flat but compliant:

```text
A capacitor stores charge. The capacitor releases charge when voltage decreases.
```

Engaging and compliant:

```text
A capacitor is like a small water tank. It fills with charge when voltage is high.
When voltage drops, the tank empties and keeps the circuit running.
What do you think happens if the tank is too small?
```

### Example: procedure

Not compliant:

```text
You'll want to go ahead and hook up the LED strip to the Pico, making sure
the ground is connected first so you don't fry anything.
```

Compliant:

```text
1. Connect the ground wire of the LED strip to a GND pin on the Pico.
2. Connect the data wire to GP16.
3. Connect the power wire to VBUS.

!!! warning
    Connect the ground wire first. A missing ground can damage the LED strip.
```

## Glossary Integration

This guide assumes the book glossary follows ISO 11179 metadata registry rules.

- Use the **preferred term** from the glossary in all text.
- Do not use a listed synonym or variant in body text.
- Write the definition of a term exactly as it appears in the glossary when you restate it.
- Put new terms in the glossary **before** you use them in a chapter.

## Self-Check Before You Finish a Chapter

Before you submit a chapter, check each item:

- [ ] Every glossary term matches the preferred term. No synonyms.
- [ ] No paragraph has more than six sentences.
- [ ] Procedures, definitions, warnings, and quiz items follow the strict rules.
- [ ] No sentence in strict content has more than 20 words.
- [ ] No idioms, slang, or unneeded phrasal verbs remain.
- [ ] Passive voice appears only when the actor is unknown or unimportant.
- [ ] Each abbreviation is defined on first use.
- [ ] The chapter has at least one analogy, question, or short story in a light section.
- [ ] A reader who is learning English can follow each procedure without a dictionary.

## Quick Reference

| Do | Do not |
|----|--------|
| The motor turns the wheel. | The wheel is turned by the motor. |
| Start the program. | Kick off the program. |
| Remove the cover. | Take the cover off. |
| Use the same term every time. | Switch between "sensor," "detector," and "probe" for one idea. |
| Write one action per step. | Combine three actions in one sentence. |
| Ask: "What happens next?" | Hide the question inside a long sentence. |
| Compare to a water tank. | Write "as the old saying goes..." |

## Revision History

| Date | Change |
|------|--------|
| 2026-11-06 | First draft. |
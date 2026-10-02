---
title: Tokenization Visualizer
description: Type a sentence and compare how a person splits it into words with how a language model splits it into tokens, using an illustrative rule-based tokenizer.
image: /sims/tokenization-visualizer/tokenization-visualizer.png
og:image: /sims/tokenization-visualizer/tokenization-visualizer.png
twitter:image: /sims/tokenization-visualizer/tokenization-visualizer.png
social:
   cards: false
quality_score: 100
---

# Tokenization Visualizer

<iframe src="main.html" height="522px" width="100%" scrolling="no"></iframe>

[Run the Tokenization Visualizer MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }
<br/>
[Edit in the p5.js Editor](https://editor.p5js.org/)

## About This MicroSim

A language model never reads words. It reads **tokens**, and a token is often
smaller than a word. This MicroSim shows one sentence three ways:

1. **The text you typed**, as plain text.
2. **How you see it**: one box per word.
3. **How the model sees it**: one colored chip per token.

Under the chips, a word count and a token count sit side by side. The token
count is almost always the larger number, and it is the number that a model's
cost and context-window capacity are measured in.

!!! warning "The split is an illustration, not a real tokenizer"
    The splitter in this MicroSim is a small set of hand-written rules. It is
    **not** the tokenizer of any real model, and its counts will not match a
    real model's counts. Real tokenizers, such as byte-pair encoding, learn
    their vocabulary of pieces from training text. The rules here only
    reproduce the general pattern, so use the counts to compare sentences
    with each other, not to estimate a bill.

The rules the illustrative splitter follows:

| Rule | Example |
|------|---------|
| Short or very common words stay whole | `into` is 1 token |
| A familiar word ending splits off | `Tokenization` becomes `Token` + `iz` + `ation` |
| A familiar word beginning splits off | `unbelievable` becomes `un` + `believ` + `able` |
| A long, unfamiliar stretch of letters breaks into short fragments | `establish` becomes `esta` + `blish` |
| Punctuation marks are tokens of their own | `.` is 1 token |
| Long numbers break into groups of up to three digits | `12345` becomes `123` + `45` |

## How to Use

1. Read the example sentence, then compare the five word boxes with the eight
   token chips.
2. Click any token chip. An infobox shows the token's text, its position
   index, and one sentence about why it split where it did.
3. Type or paste your own sentence (up to 120 characters). The word count
   updates as you type and the token count changes to a question mark.
4. Predict the token count, then select **Tokenize** (or press Enter) to check.
   The word boxes break apart into token chips in one quick transition.
5. Select **Reset** to bring back the example sentence.

Try a sentence of short everyday words, then a sentence with long technical
words. The tokens-per-word number shows the difference.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/tokenization-visualizer/main.html"
        height="522px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who are new to large
language models. No programming background is needed.

### Learning Objective

Explain why a language model's cost and capacity are measured in tokens rather
than words. (Bloom's Taxonomy: Understand)

### Duration

10-15 minutes

### Prerequisites

- Knows that a large language model predicts the next unit of text
- Has read the definitions of *token* and *tokenization* in Chapter 1

### Activities

1. **Exploration** (5 min): Compare the word row and the token row for the
   example sentence. Click each chip in `Token` + `iz` + `ation` and read why
   it split.
2. **Guided Practice** (5 min): Type three sentences: one made of short common
   words, one with long technical words, and one with a long number. For each,
   write down a predicted token count before selecting **Tokenize**.
3. **Assessment** (5 min): In two or three sentences, explain to a colleague
   why a 1,000-word document does not cost "1,000 units" to send to a model.

### Assessment

- The learner states that a model processes tokens, not words.
- The learner predicts that long or unusual words produce more tokens than
  short common words, and confirms it with their own sentence.
- The learner explains that limits and prices follow the token count, so the
  word count underestimates both.

### Discussion Questions

1. Which of your sentences had the highest tokens-per-word number? Why?
2. Why might a tokenizer keep a common word whole but break a rare word apart?
3. This splitter is hand-written. What would a real tokenizer need in order to
   decide where to split?

## References

1. [Byte pair encoding](https://en.wikipedia.org/wiki/Byte_pair_encoding) - Wikipedia - The subword method behind many real tokenizers, which this MicroSim only approximates.
2. [Large language model](https://en.wikipedia.org/wiki/Large_language_model) - Wikipedia - Background on tokenization and context windows in language models.
3. [OpenAI Tokenizer](https://platform.openai.com/tokenizer) - OpenAI - A real tokenizer you can use to compare actual token splits with the illustrative ones shown here.
4. [p5.js Reference](https://p5js.org/reference/) - p5.js - Documentation for the library used to build this MicroSim.

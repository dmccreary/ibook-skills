---
title: $QUIZ_TITLE
description: $QUIZ_DESCRIPTION
image: /sims/$MICROSIM_NAME/$MICROSIM_NAME.png
og:image: /sims/$MICROSIM_NAME/$MICROSIM_NAME.png
twitter:image: /sims/$MICROSIM_NAME/$MICROSIM_NAME.png
social:
   cards: false
---

# $QUIZ_TITLE

<iframe src="main.html" height="532px" width="100%" scrolling="no"></iframe>

[Run the $QUIZ_TITLE Fullscreen](./main.html){ .md-button .md-button--primary }

## About This MicroSim

$QUIZ_DESCRIPTION

### Features

- **Scenario-based questions**: Each question presents a realistic scenario to classify
- **Multiple choice format**: Select from 4 options per question
- **Hint system**: Get a hint if you're stuck (reduces points earned)
- **Detailed explanations**: Learn why each answer is correct after responding
- **Score tracking**: Earn 10 points for correct answers (5 with hint)
- **Encouraging feedback**: Supportive messages whether right or wrong
- **Randomized order**: Questions appear in random order each time

### Categories Covered

| Category | Description |
|----------|-------------|
| **Category A** | Description of Category A |
| **Category B** | Description of Category B |
| **Category C** | Description of Category C |
| **Category D** | Description of Category D |

## Embedding This MicroSim

You can include this MicroSim on your website using the following `iframe`:

```html
<iframe src="https://$GITHUB_USER.github.io/$REPO_NAME/sims/$MICROSIM_NAME/main.html"
        height="532px"
        width="100%"
        scrolling="no">
</iframe>
```

## Lesson Plan

### Learning Objectives

By completing this quiz, students will be able to:

1. **Identify** the key characteristics of each category
2. **Distinguish** between similar categories
3. **Explain** why specific examples belong to particular categories
4. **Apply** classification skills to analyze new scenarios

### Bloom's Taxonomy Level

This activity primarily addresses **Application (Level 3)** - students must apply their knowledge of categories to analyze new scenarios they haven't seen before.

### Pre-Quiz Discussion (5 minutes)

Before starting the quiz, discuss:

- What are the main categories we'll be identifying?
- What key characteristics define each category?
- Why is it important to recognize these categories?

### Quiz Activity (15-20 minutes)

1. Have students complete the quiz individually
2. Encourage them to use the "Show Hint" feature only after careful consideration
3. Ask them to read each explanation carefully after answering

### Post-Quiz Reflection (10 minutes)

Discussion questions:

1. Which category was hardest to identify? Why?
2. What patterns did you notice that helped you classify correctly?
3. How might you apply this classification skill in real situations?
4. What strategies helped you distinguish between similar categories?

### Extension Activity

Have students find or create their own examples for each category and explain their reasoning.

## Technical Details

- **Framework**: p5.js 2.3.2
- **Data Format**: Questions stored in `data.json` for easy editing
- **Canvas Size**: 800×530 pixels (responsive width)
- **Accessibility**: Includes screen reader description

## Customizing Questions

The quiz questions are stored in `data.json` and can be easily modified. Each scenario includes:

```json
{
  "id": 1,
  "scenario": "Description of the scenario...",
  "correctAnswer": "Name of the correct category",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "explanation": "Why this answer is correct...",
  "hint": "A helpful hint for students..."
}
```

To add new scenarios, simply add new objects to the `scenarios` array in `data.json`.

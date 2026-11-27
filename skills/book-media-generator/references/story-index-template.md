---
title: "{STORY_TITLE}"
description: "{STORY_DESCRIPTION}"
image: /stories/{STORY_DIR_NAME}/cover.png
og:image: /stories/{STORY_DIR_NAME}/cover.png
twitter:image: /stories/{STORY_DIR_NAME}/cover.png
social:
   cards: false
---

# {STORY TITLE}

![](./cover.png)
<details>
<summary>Cover Image Prompt</summary>
(This is the Cover Image. Do not include this label in the image.)
Please generate a wide-landscape 16:9 cover image for this story in
[period-appropriate art style]. {Detailed description of the scene, the
subject's appearance, and the setting. Include the title text rendered in
a period-appropriate typeface.} Color palette: [palette]. Emotional tone:
[tone]. Generate the image immediately without asking clarifying questions.
</details>

<details>
<summary>Narrative Prompt</summary>
[Background context and style guide for the entire story. Include the
subject's era, country, central themes, and a character-consistency note
so all panels share the same visual language.]
</details>

### Prologue – <Hook Title>

[Opening narrative establishing the subject's importance. 3-5 sentences.]

## Panel 1: {PANEL 1 Title}

![](./panel-01.png)
<details><summary>Image Prompt</summary>
(This is Panel 01. Do not include the panel number in the image.)
I am about to ask you to generate a series of images for a graphic novel.
Please make the images have a consistent style and consistent characters.
Do not ask any clarifying questions. Just generate the image immediately
when asked.

Please generate a 16:9 image in [period style] depicting panel 1 of 12.
The scene should include [specific characters with physical description],
set in [specific setting including year and location], with a color palette
of [color palette]. The emotional tone should be [emotional tone].
[At least 6 specific visual details to guide the generation.]
Generate the image immediately without asking clarifying questions.
</details>

{Panel 1 narrative text — 3-4 sentences of vivid, active-voice prose that
advances the story and complements the image. Written for the target
audience (e.g., high school students) — accessible but not dumbed down.}

## Panel 2: {PANEL 2 Title}

![](./panel-02.png)
<details><summary>Image Prompt</summary>
(This is Panel 02. Do not include the panel number in the image.)
Please generate a 16:9 image in [period style] depicting panel 2 of 12.
Make the characters and style consistent with the prior panel. The scene
should include [specific characters], set in [specific setting including
year and location], with a color palette of [color palette]. The emotional
tone should be [emotional tone]. [At least 6 specific visual details.]
Generate the image immediately without asking clarifying questions.
</details>

{Panel 2 narrative text — 3-4 sentences.}

## Panel 3: {PANEL 3 Title}

![](./panel-03.png)
<details><summary>Image Prompt</summary>
(This is Panel 03. Do not include the panel number in the image.)
Please generate a 16:9 image in [period style] depicting panel 3 of 12.
Make the characters and style consistent with the prior panel. The scene
should include [specific characters], set in [specific setting including
year and location], with a color palette of [color palette]. The emotional
tone should be [emotional tone]. [At least 6 specific visual details.]
Generate the image immediately without asking clarifying questions.
</details>

{Panel 3 narrative text — 3-4 sentences.}

[REPEAT THIS PATTERN FOR EACH PANEL — N panels total, plus the cover.
N defaults to 12 but is configurable via the skill's `--panels N` argument.
For shorter stories (6, 7, 8, 9 panels), follow the same per-panel pattern
and stop at panel N. Update each "panel X of N" identifier line so the
denominator matches the actual N for this story (e.g. "panel 3 of 8" in
an 8-panel story, NOT "panel 3 of 12"). Do not pad with filler panels
just to reach 12 — a tight 6-panel story beats a bloated 12-panel one.]

### Epilogue – What Made <Subject> Different?

[Summary narrative of lessons learned — 3-5 sentences.]

| Challenge | How <Subject> Responded | Lesson for Today |
|-----------|---------------------------|------------------|
| ... | ... | ... |
| ... | ... | ... |
| ... | ... | ... |
| ... | ... | ... |

### Call to Action

[Inspiring 2-3 sentence message connecting the subject's work to the
reader's own study or life.]

---

*"Quote from subject"*
—<Subject Name>

*"Second quote from subject"*
—<Subject Name>

---

## References

Write real, working URLs in the first draft. Do NOT use `(PLACEHOLDER)`.
Follow the standard 5-reference pattern: first three Wikipedia, then two
secondary sources.

1. [Wikipedia: <Subject Name>](https://en.wikipedia.org/wiki/<Subject_Name>) - Biography of the subject
2. [Wikipedia: <Main Contribution>](https://en.wikipedia.org/wiki/<Main_Contribution>) - The subject's main discovery or invention
3. [Wikipedia: <Related Concept>](https://en.wikipedia.org/wiki/<Related_Concept>) - A related topic or work
4. [MacTutor: <Subject Name>](https://mathshistory.st-andrews.ac.uk/Biographies/<Subject>/) - University of St Andrews history of mathematics archive
5. [Encyclopaedia Britannica: <Subject Name>](https://www.britannica.com/biography/<Subject-Name>) - Overview of the subject's life and contributions

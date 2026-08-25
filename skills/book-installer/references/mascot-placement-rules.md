---
name: mascot-placement-rules
description: Canonical, single-source rules for when and how often a learning mascot may appear in generated content. Every skill that places mascot admonitions reads this file rather than restating the rules.
---

<!-- ============================================================
     CANONICAL SOURCE — DO NOT COPY THESE RULES INTO OTHER SKILLS.

     This file is the single source of truth for mascot placement.
     Other skills MUST reference it by path instead of restating any
     table, count, or per-pose rule found below. Duplicated copies
     drift within weeks; that drift is what this file exists to end.

     To reference it from another skill, write:

       Read the canonical mascot placement rules at
       `$BK_HOME/skills/book-installer/references/mascot-placement-rules.md`
       before placing any mascot admonition. Do not restate them here.

     `$BK_HOME` points at the ibook-skills checkout and is agent-neutral.
     Do NOT use a path under `~/.claude/skills/`, `~/.codex/skills/`, or
     `~/.gemini/antigravity/skills/` — each is specific to one agent
     framework, and these skills run on all of them. If `$BK_HOME` is
     unset, the file is at `book-installer/references/mascot-placement-rules.md`
     relative to the skills root that contains the calling skill.

     To render this file into a book's CONTENT-GENERATION-GUIDE.md, use
     `book-installer/scripts/render-mascot-guide.sh` — never hand-copy it.
     ============================================================ -->

# Mascot Placement Rules

The rules below govern **when** a learning mascot may appear, **how often**, and
**which pose** carries which pedagogical job. They apply to every piece of
student-facing generated content: chapters, lesson plans, quizzes, FAQs,
glossary pages, and the home page.

**Instructor-facing content is exempt.** Teacher guides, instructor guides, and
answer keys do not use mascot admonitions at all.

Placeholders (`{{CHARACTER_NAME}}`, `{{SPECIES}}`, `{{SUBJECT}}`,
`{{CATCHPHRASE}}`, `{{TOPIC}}`) are substituted when this file is rendered into
a specific book's `CONTENT-GENERATION-GUIDE.md`.

## Mascot Admonition Format

Always place the mascot image in the admonition **body**, never in the title
bar, and always use Markdown image syntax with `attr_list` — never a raw HTML
`<img>` tag:

    !!! mascot-welcome "Title Here"
        ![{{CHARACTER_NAME}} waving welcome](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
        Admonition text goes here after the image.

**Image paths — Markdown and raw HTML use different base directories.**

- **Markdown images** `![alt](path)` resolve relative to the **source `.md`
  file's directory**; the site generator rewrites them for the rendered URL.
  From `docs/chapters/01-intro/index.md` that is `../../img/mascot/`. From a
  non-index page such as `docs/learning-graph/mascot-test.md` it is
  `../img/mascot/`.
- **Raw HTML `<img src>`** is passed through verbatim, so it must be relative
  to the **rendered URL** — `../../img/mascot/` for both pages above.

Getting this wrong produces a page that displays correctly but emits a
"target is not found among documentation files" warning that fails
`mkdocs build --strict`.

## Placement Rules

| Context | Admonition type | Per chapter |
|---------|-----------------|-------------|
| Chapter opening | `mascot-welcome` | Exactly 1 |
| Key concept or mental model | `mascot-thinking` | 1–4 |
| Heuristic or shortcut | `mascot-tip` | 0–3 |
| Common mistake or pitfall | `mascot-warning` | 0–3 |
| Known difficult passage | `mascot-encourage` | 0–2 |
| End-of-chapter closure | `mascot-celebration` | 0–1 |
| General aside or framing | `mascot-neutral` | 0–1 |

## Hard Limits

1. **Fewer than 10 mascot admonitions per chapter** (9 is the enforced
   ceiling). The per-context ranges above can sum higher than 9; the total cap
   is what binds. A long chapter with many distinct sections may legitimately
   approach the ceiling — a short chapter should sit nearer 4–5. Reaching the
   cap must be a consequence of the chapter having that many genuine
   signal-worthy moments, never a target to fill.
2. **Never place two mascot admonitions back-to-back.** At least one paragraph
   of ordinary prose must separate any two of them.
3. **At most one `mascot-welcome` and one `mascot-celebration` per chapter.**
4. **Body text is 1–3 sentences** (a `mascot-welcome` may run to 4). Longer
   than that and the admonition starts to read as the primary content, which
   defeats its purpose as an interjection.
5. **Never decorative.** Every mascot admonition must carry a message the
   reader gains something from. If the surrounding prose already says it, cut
   the admonition.

## Mascot Admonition Guidelines (Instructional Design Rules)

Each pose carries a distinct cognitive and pedagogical job. The pose is a
signal to the reader, not decoration — an agent that picks a pose by vibe
rather than by function destroys the wayfinding value of the whole system.
Agents generating these admonitions must follow the rules below.

### 1. `mascot-welcome` (Motivational Hook / Advance Organizer)

- **Instructional purpose**: Addresses the "What's In It For Me?" (WIIFM)
  question and lowers learning anxiety before technical content begins. It is
  not there to teach the chapter — it is there to **sell** the chapter.
- **Rule**: Do not summarize technical concepts or explain mechanics. Tell the
  reader *why* they should care and *what they will be able to build* by the
  end.
- **Tone**: Warm, sincere, and a little fun. Use {{SUBJECT}}-flavored
  metaphors. Include the signature catchphrase "{{CATCHPHRASE}}".
- **Length**: Strictly 2-4 sentences. *(Exception: Chapter 1, where
  {{CHARACTER_NAME}} introduces themselves — see "Chapter 1 Self-Introduction"
  below.)*

### 2. `mascot-thinking` (Cognitive Scaffolding / Mental Models)

- **Instructional purpose**: Marks a "eureka" moment, an abstraction, or a
  shift in mental model. Signals that the reader should pause and process the
  *why* behind the *how*.
- **Rule**: Never use this for a mere fact or a piece of syntax. Reserve it
  for underlying algorithms, core mechanics, or architectural patterns —
  the ideas a reader must restructure their thinking around.
- **Tone**: Insightful and reflective. Rhetorical questions and analogies work
  well ("Notice how…", "Think of it like…").

### 3. `mascot-tip` (Just-in-Time Support / Heuristics)

- **Instructional purpose**: Delivers a heuristic, shortcut, or best practice
  that isn't strictly required but measurably reduces cognitive load. This is
  expert insight whispered to a novice.
- **Rule**: Must be immediately actionable — a concrete shortcut, a diagnostic
  question, a naming convention, a way to sanity-check an answer. If the
  reader cannot *do* something differently after reading it, it is not a tip.
- **Tone**: Conspiratorial and clever ("Here's a shortcut…", "Want to save
  yourself an hour?").

### 4. `mascot-warning` (Anticipatory Guidance / Pitfall Prevention)

- **Instructional purpose**: Anticipatory guidance that heads off a known
  novice pitfall. It deliberately interrupts reading flow to prevent
  downstream frustration.
- **Rule**: State the pitfall, *why* it happens, and exactly how to avoid or
  recover from it. A warning without a remedy is just anxiety — always supply
  the fix.
- **Tone**: Alert but reassuring; never scolding or ominous ("Watch out
  for…", "A common trap here is…").

### 5. `mascot-encourage` (Affective Support / Normalizing Struggle)

- **Instructional purpose**: Emotional support at a known point of high
  cognitive friction. Normalizes struggle and supports a growth mindset.
- **Rule**: Use ONLY when introducing a notoriously difficult topic — not as
  generic cheerleading. Validate that the difficulty is real, connect it to
  something the reader has already succeeded at, and suggest a concrete way
  forward (experiment, break it into steps, revisit a prerequisite).
- **Tone**: Empathetic and validating ("If this feels like a lot, that's
  normal — most people need two passes at it.").

### 6. `mascot-celebration` (Formative Reinforcement / Closure)

- **Instructional purpose**: Positive reinforcement and closure at a genuine
  milestone. Satisfies the "Satisfaction" component of the ARCS motivation
  model, consolidating what was learned.
- **Rule**: Never just "Good job." Name the *specific* concept or skill the
  reader just mastered, so the achievement is concrete and reviewable.
- **Tone**: Joyful and proud ("You just built…", "That's {{TOPIC}} handled —
  and it's one of the harder ones.").

### 7. `mascot-neutral` (General Aside / Framing)

- **Instructional purpose**: A general-purpose aside for content that carries
  no particular emotional charge — context, a historical note, a pointer to a
  related chapter.
- **Rule**: Use this when none of the six purposeful poses genuinely fits.
  Reaching for `mascot-neutral` more than once per chapter usually means the
  content did not need a mascot admonition at all — use plain prose or a
  standard admonition instead.
- **Tone**: Calm and matter-of-fact.

## Chapter 1 Self-Introduction (one time only)

The **first mascot admonition in Chapter 1** is not a normal welcome — it is a
**self-introduction** that orients the reader to the mascot's role for the rest
of the book. This sets reader expectations once, so every later chapter can use
the mascot without re-explaining what it is.

- Use the `mascot-welcome` type; it doubles as the chapter-opening welcome.
- Have {{CHARACTER_NAME}} **state their name, species, and one personality
  detail** in a warm first-person voice, matching the voice this book defines.
- **Enumerate every pose-role** as a numbered list, in the order they typically
  appear during a chapter (welcome → think → tip → warn → encourage →
  celebrate). Each item is one short sentence describing *what the mascot does*
  in that pose, not what the pose looks like.
- **End with a contract sentence** — for example "If I'm not doing one of those
  six things, I'm not in the chapter." — so the reader understands the mascot
  is a *signal*, not decoration.
- Do not invent poses this book does not define.

Do this **only in Chapter 1, only on the mascot's very first appearance**, and
never again. Chapters 2+ open with a normal `mascot-welcome` that gets straight
into chapter-specific content.

## Do's and Don'ts

**Do:**

- Use {{CHARACTER_NAME}} to introduce new topics warmly
- Include the catchphrase in welcome admonitions
- Keep dialogue brief (1-3 sentences, except the 2-4 sentence welcome)
- Match the pose to the *instructional purpose* above, not to the vibe
- Open each chapter with `mascot-welcome` and close it with
  `mascot-celebration`

**Don't:**

- Use {{CHARACTER_NAME}} 10 or more times in one chapter
- Put mascot admonitions back-to-back
- Use the mascot for purely decorative purposes
- Change {{CHARACTER_NAME}}'s personality or speech patterns
- Use more than one `mascot-welcome` or `mascot-celebration` per chapter
- Use gendered pronouns for the mascot — use the name or *they/them*

## Quality Assurance & Validation

Language models drift away from strict formatting constraints, so mascot
placement must be checked programmatically rather than by eye.

**Post-generation rule**: after writing or editing any chapter, run the
validator before reporting the work complete:

    python "$BK_HOME/skills/book-installer/scripts/validate-chapter-mascots.py" docs/chapters/NN-slug/index.md

It flags: 10 or more mascot admonitions in a chapter, duplicate
`mascot-welcome` or `mascot-celebration`, back-to-back mascot admonitions,
any admonition missing its `mascot-admonition-img` image, and body text that
is clearly too short or too long for the 1-3 sentence rule.

If the validator reports issues, fix the chapter and re-run it until it exits
clean. Do not report completion on a chapter that still fails, and do not
relax a rule to make the check pass.

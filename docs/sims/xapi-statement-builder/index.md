---
title: xAPI Statement Builder
description: Build an Experience API statement from an actor, a verb, and an object, read it as a sentence and as JSON, and see which field turns an anonymous statement into per-student data.
image: /sims/xapi-statement-builder/xapi-statement-builder.png
og:image: /sims/xapi-statement-builder/xapi-statement-builder.png
twitter:image: /sims/xapi-statement-builder/xapi-statement-builder.png
social:
   cards: false
quality_score: 100
---

# xAPI Statement Builder

<iframe src="main.html" height="552px" width="100%" scrolling="no"></iframe>

[Run the xAPI Statement Builder MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }
<br/>
[Edit in the p5.js Editor](https://editor.p5js.org/)

## About This MicroSim

The **Experience API** (xAPI) records learner activity as statements with an
**actor**, a **verb**, and an **object**: *who* did *what* to *which thing*.
This MicroSim lets you assemble one statement from three dropdowns. It shows
the statement twice:

- as a plain sentence, such as `anonymous-session-4471 completed quiz-token-basics`
- as the xAPI JSON a learning record store would receive

The checkbox **Use real student name instead of session ID** changes one
thing: what goes in the actor field. With a session ID, the statement is
anonymous and can be counted together with everyone else's. The moment a
real name is typed, the sentence turns red and the message reads *"This
statement now identifies a specific student — outside this project's 2.99
design target."* The verb and the object did not change. Only the actor did.

Nothing you type is stored or sent anywhere. This is a conceptual builder.

### What keeps the JSON valid xAPI

| Part | Rule | In this MicroSim |
|------|------|------------------|
| Actor | Needs exactly one identifier. An `account` with a `homePage` and a `name` is one allowed form. | The session ID, or a login-style name derived from the typed name, goes in `account.name`. |
| Verb | The `id` must be an IRI. `display` gives a human-readable label per language. | `completed` and `answered` use the ADL vocabulary, for example `http://adlnet.gov/expapi/verbs/completed`. |
| Object | An activity is identified by an IRI in `id`. | Each object gets an `https://example.org/activities/...` address. |

`hovered` and `clicked` are not in the ADL vocabulary, so the MicroSim gives
them an IRI under the same placeholder domain. xAPI allows a project to define
its own verb IRIs. The note in the corner of the JSON panel says which kind of
IRI the current verb uses.

All `example.org` addresses are placeholders. A real statement can also carry
optional `result` and `context` properties, and a learning record store
fills in an `id` and a timestamp when the sender leaves them out. They are
omitted here to keep the three required parts in view.

## How to Use

1. Choose an **Actor**, a **Verb**, and an **Object**. Read the sentence, then
   find each of the three parts in the JSON below it.
2. Change only the verb. Notice that only the `verb` block of the JSON changes.
3. Check **Use real student name instead of session ID**, or pick
   *Type a name...* in the Actor dropdown.
4. Type any name in the box. Watch the sentence, the message, and the actor
   block of the JSON.
5. Uncheck the box to return to the anonymous session ID.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/xapi-statement-builder/main.html"
        height="552px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who are deciding what
interaction data an intelligent textbook should collect.

### Learning Objective

Construct a valid actor-verb-object xAPI statement and identify which field,
if populated with a real name, would cross into regulated per-student data.
(Bloom's Taxonomy: Apply)

### Duration

10-15 minutes

### Prerequisites

- Has read the definitions of *Experience API* and *learning record store* in
  Chapter 2
- Understands the "Level 2.99" design target described in Chapter 2

### Activities

1. **Exploration** (4 min): Build all four verbs against one object. Point to
   the part of the JSON that changes each time.
2. **Guided Practice** (6 min): Build the statement for each of these events:
   a reader finishes the token quiz; a reader hovers the LLM node of a diagram;
   a reader clicks inside the context-window MicroSim. For each, write the
   sentence form before you look at the screen.
3. **Assessment** (4 min): Turn on the real-name toggle and type a name. Name
   the one field that changed, and explain why the same verb and object are
   now part of a different kind of record.

### Assessment

- The learner builds a statement with all three parts and reads it as a
  sentence.
- The learner identifies the **actor** as the field that decides whether a
  statement is anonymous or identifies a person.
- The learner explains why aggregating anonymous statements still shows how
  readers in general engage with a concept.

### Discussion Questions

1. What can you learn from one thousand anonymous `completed` statements about
   the same quiz?
2. What new obligations begin when the actor field holds a real name?
3. Why does this project stop at "2.99" instead of storing per-student history?

## References

1. [Experience API](https://en.wikipedia.org/wiki/Experience_API) - Wikipedia - Overview of xAPI, the actor-verb-object statement, and the learning record store.
2. [xAPI Specification](https://github.com/adlnet/xAPI-Spec) - Advanced Distributed Learning Initiative - The specification that defines statement structure, actors, verbs, and activities.
3. [xAPI Overview](https://xapi.com/overview/) - Rustici Software - A plain-language introduction to xAPI statements.
4. [p5.js Reference](https://p5js.org/reference/) - p5.js - Documentation for the library used to build this MicroSim.

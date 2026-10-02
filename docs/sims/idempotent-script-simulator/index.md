---
title: Idempotent Script Simulator
description: Run an idempotent script and a non-idempotent script several times each and compare the end state of the two files they write to.
image: /sims/idempotent-script-simulator/idempotent-script-simulator.png
og:image: /sims/idempotent-script-simulator/idempotent-script-simulator.png
twitter:image: /sims/idempotent-script-simulator/idempotent-script-simulator.png
social:
   cards: false
quality_score: 100
---

# Idempotent Script Simulator

<iframe src="main.html" height="482px" width="100%" scrolling="no"></iframe>

[Run the Idempotent Script Simulator MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }
<br/>
[Edit in the p5.js Editor](https://editor.p5js.org/)

## About This MicroSim

An **idempotent** script produces the same end state whether you run it once
or many times. This MicroSim puts two scripts side by side. Both have the same
job: make sure the row `taxonomy-names.json` is in a file.

| | Non-Idempotent Script | Idempotent Script |
|---|---|---|
| Code | `rows.append(row)` | `if row not in rows:` then `rows.append(row)` |
| First run | Adds the row | Adds the row |
| Every later run | Adds the row again | Finds the row and adds nothing |
| End state after 3 runs | 3 rows, 2 of them duplicates | 1 row |

Each panel shows the script's one distinguishing line of code, how many times
it has run, the rows now in its file, and what the most recent run did.
Duplicate rows are tinted red and labeled.

The MicroSim opens with each script already run three times, so the two end
states can be compared right away. **Reset Both** empties both files so you can
replay the runs one at a time.

## How to Use

1. Compare the two panels as they open. Both scripts have run three times.
   Count the rows in each file.
2. Select **Reset Both**. Both files are now empty.
3. Select **Run Non-Idempotent Script** once and **Run Idempotent Script**
   once. The two files match.
4. Run each script a second time. This is the run where the files stop
   matching.
5. Use **Run Both** to run the two scripts together and keep their run counts
   equal while you compare.
6. Hover over either panel to read what kind of real script it stands for.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/idempotent-script-simulator/main.html"
        height="482px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who are starting to
read and run the Python scripts that ship with this skill library.

### Learning Objective

Differentiate the end state produced by an idempotent script from a
non-idempotent one after running each multiple times. (Bloom's Taxonomy:
Analyze)

### Duration

10 minutes

### Prerequisites

- Can read a two-line Python `if` statement
- Has read the definitions of *deterministic computation* and *idempotent
  script design* in Chapter 3

### Activities

1. **Exploration** (3 min): Reset, then run both scripts one run at a time up
   to five runs. After each run, say how many rows each file holds.
2. **Guided Practice** (4 min): Before each of the next three runs, predict
   the row count of both files. Then decide which single line of code is
   responsible for the difference.
3. **Assessment** (3 min): You find a script that adds a navigation entry to a
   configuration file. Describe the check you would add to make it safe to
   run twice.

### Assessment

- The learner states that both scripts behave the same on the first run and
  differ from the second run on.
- The learner points to the existence check as the cause of the difference.
- The learner explains why an idempotent script removes the need to remember
  whether it has already been run.

### Discussion Questions

1. The non-idempotent script never reports an error. Why is that a problem?
2. Is a script that deletes a file idempotent? What about one that appends a
   timestamp to a log?
3. Which scripts in a textbook project would you most want to be safe to
   re-run?

## References

1. [Idempotence](https://en.wikipedia.org/wiki/Idempotence) - Wikipedia - The general definition, with a section on idempotence in computer science.
2. [Data Structures: More on Lists](https://docs.python.org/3/tutorial/datastructures.html) - Python Software Foundation - The `list.append()` method and the `in` membership test used by the two scripts.
3. [p5.js Reference](https://p5js.org/reference/) - p5.js - Documentation for the library used to build this MicroSim.

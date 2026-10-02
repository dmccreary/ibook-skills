---
title: Python Fundamentals for Skill Automation
description: Covers the Python building blocks behind every automation script in the skill library, from the standard library and virtual environments to idempotent script design.
generated_by: claude skill chapter-content-generator
date: 2026-08-22 12:40:00
version: 0.09
---

# Python Fundamentals for Skill Automation

## Summary

This chapter introduces the Python building blocks used across the skill library: the standard library, pip and virtual environments, JSON and CSV parsing, regular expressions, and command-line arguments. It also covers the conventions -- shebang lines, exit codes, verbose and dry-run modes -- that make a script safe to run repeatedly. Students will be able to read and modify a short automation script after finishing this chapter.

## Concepts Covered

This chapter covers the following 18 concepts from the learning graph:

1. Python
2. Python Standard Library
3. pip Package Management
4. Virtual Environment
5. JSON Serialization
6. CSV Parsing in Python
7. Markdown Parsing in Python
8. File Globbing
9. Path Handling
10. Shebang Line
11. Regular Expressions
12. Command-Line Arguments
13. Script Exit Codes
14. Verbose Output Mode
15. Shell Script Wrapper
16. Deterministic Computation
17. Idempotent Script Design
18. Dry Run Mode

## Prerequisites

This chapter builds on concepts from:

- [1. Foundations of AI, Language Models, and Prompting](../01-foundations-ai-language-models/index.md)

---

!!! mascot-welcome "Time to meet my favorite tool."
    ![Kit waves hello with their tool satchel](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    Everything countable in this book's pipeline — parsing, validating, scaffolding — runs on Python, not on the model. This chapter is your tour of that toolbox. Right tool, right task!

## Python and Its Standard Library

**Python** is the general-purpose programming language this book's skills use for every deterministic step in the pipeline — the parts where an exact, repeatable answer matters more than a fluent one. Python ships with a **Python standard library**: the modules distributed with Python that handle common tasks such as file access, structured data, and pattern matching without installing anything extra. When a skill's script imports `json` or `re`, it's reaching into the standard library rather than a separate download.

## Managing Dependencies: pip and Virtual Environments

Not everything a script needs lives in the standard library. **pip package management** is the tool that installs and updates third-party Python packages — the ones written by someone else and published for reuse. Installing packages globally on your machine risks one project's version requirement colliding with another's, so most Python projects use a **virtual environment**: an isolated Python installation for a single project that prevents its dependencies from conflicting with those of other projects.

## Reading and Writing Structured Data

Most of this book's scripts spend their time converting one structured format into another. **JSON serialization** converts structured data to and from a text format that both programs and web pages can read — it's how `learning-graph.json` becomes something a browser-based graph viewer can render. **CSV parsing in Python** reads delimited tabular text into structured records for processing, which is how `learning-graph.csv`'s pipe-delimited dependency lists become Python lists your script can loop over. **Markdown parsing in Python** extracts structure such as headings and fenced code blocks from markdown source so content can be counted or transformed, the technique behind scripts that pull a MicroSim specification out of a chapter's `index.md`.

When the structure you need isn't a whole file format but a fragment buried inside text, reach for **regular expressions**: a pattern language for matching and extracting text, used to locate structured fragments inside documents. Before the example below, note what each part of the pattern means: `\d+` matches one or more digits, and parentheses `()` capture the matched text so your script can retrieve it afterward.

```python
import re

match = re.search(r"CANVAS_HEIGHT:\s*(\d+)", script_text)
if match:
    canvas_height = int(match.group(1))
```

This is the actual technique `sync-iframe-heights.py` uses to read the `// CANVAS_HEIGHT: 500` comment convention from a MicroSim's JavaScript file and apply that height to its embedding iframe.

## Working With Files: Globbing and Path Handling

A script rarely operates on one file at a time. **File globbing** selects files by wildcard pattern rather than naming each one, used to process every chapter or every simulation at once — `docs/chapters/*/index.md` matches all 31 chapter files in a single expression. Because a script might be run from any directory, it also needs **path handling**: constructing and resolving file locations reliably so the script works regardless of the directory it's run from, rather than breaking the moment someone runs it from somewhere other than the project root.

## Making a Script Runnable: Shebang Lines and Command-Line Arguments

A Python file becomes a program you can run directly, rather than something you always have to invoke with `python script.py`, when it starts with a **shebang line**: the first line of a script that names the interpreter to run it, allowing the file to be executed directly.

```python
#!/usr/bin/env python3
```

That line tells the operating system which interpreter to hand the rest of the file to. Once a script is runnable on its own, it typically needs input that changes each time — that's what **command-line arguments** are: values supplied to a program when it is invoked, allowing one script to operate on different inputs instead of being rewritten for each one.

```python
import sys

csv_path = sys.argv[1]   # the first argument after the script name
```

!!! mascot-tip "Name your arguments, don't just count them."
    ![Kit holding up a tool with a knowing look](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    `sys.argv[1]` works for a quick script, but the moment you have more than one or two arguments, switch to Python's `argparse` module. It gives each argument a name and a `--help` message for free — future you will not remember what argument three was supposed to be.

## Writing Scripts You Can Trust: Exit Codes, Verbose Mode, and Dry Runs

A script that another script calls needs a way to report whether it worked. **Script exit codes** are numeric values a program returns to indicate success or the kind of failure, allowing other scripts to react — by convention, `0` means success and any nonzero value signals a specific kind of failure. For a person watching a script run, **verbose output mode** is an option that makes a program report its intermediate steps, used for diagnosis when something doesn't look right. Before a script changes anything on disk, especially something that deletes or overwrites files, it should support **dry run mode**: an option that reports what a program would change without changing anything, used to preview a destructive operation before committing to it.

!!! mascot-warning "Never run an untested destructive script without --dry-run first."
    ![Kit holding up a caution paw](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    A script that renames or deletes files can't be un-run. If it supports a dry-run flag, use it the first time, every time — read the preview output carefully before you drop the flag and let it actually touch your files.

The three options work together as layers of safety, not substitutes for each other:

| Option | What It Tells You | When To Use It |
|--------|-------------------|-----------------|
| Exit code | Did the script succeed or fail? | Every run, especially in a pipeline |
| Verbose mode | What steps did the script take? | When output looks wrong and you need to trace why |
| Dry-run mode | What *would* change, without changing it | Before any destructive operation |

## Determinism and Idempotency: Why These Scripts Are Safe to Rerun

Two properties make a script trustworthy enough to fold into an automated pipeline. **Deterministic computation** is an operation that returns the same result for the same input every time, making it suitable for automated validation — the opposite of the nondeterminism you met in Chapter 1's language model output. **Idempotent script design** goes a step further: writing a program so that running it repeatedly produces the same end state as running it once, rather than duplicating work or corrupting state on a second run.

!!! mascot-thinking "Idempotent means you can always just run it again."
    ![Kit thinking with a paw on their chin](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    This is the mental shift: a non-idempotent script that appends a row to a file will produce a duplicate row if you accidentally run it twice. An idempotent version checks whether the row already exists before adding it. Once a script is idempotent, "did I already run this?" stops being a question you have to track by hand.

#### Diagram: Idempotent Script Simulator

<iframe src="../../sims/idempotent-script-simulator/main.html" width="100%" height="482px" scrolling="no"></iframe>

<details markdown="1">
<summary>Idempotent Script Simulator</summary>
Type: microsim
**sim-id:** idempotent-script-simulator<br/>
**Library:** p5.js<br/>
**Status:** Specified

Bloom Level: Analyze (L4)
Bloom Verb: Differentiate

Learning objective: Differentiate the end state produced by an idempotent script from a non-idempotent one after running each multiple times.

Canvas layout:
- Left half: "Non-Idempotent Script" panel showing a growing list of "Added row: taxonomy-names.json" entries
- Right half: "Idempotent Script" panel showing the same target list, capped at one entry no matter how many times it runs

Interactive controls:
- Button: "Run Non-Idempotent Script" (appends a new duplicate entry every click)
- Button: "Run Idempotent Script" (checks for an existing entry first; only adds once)
- Button: "Reset Both"
- Counter showing how many times each button has been clicked

Behavior:
- Clicking "Run Non-Idempotent Script" repeatedly grows the left list with visibly duplicated entries, and after 3+ clicks a warning label appears: "State has diverged from a single clean run"
- Clicking "Run Idempotent Script" repeatedly keeps the right list at exactly one entry, with a label: "Same end state, no matter how many times you run it"
- Hovering either panel shows an infobox explaining what real script behavior it represents

Instructional Rationale: An Analyze-level side-by-side comparison lets the reader directly observe divergent end states from the same repeated action, which is the core insight idempotency prose alone cannot make concrete.

Implementation notes: Use p5.js; both panels share the same click count so the contrast is visible at every step.
</details>

## Shell Script Wrappers

Not every script needs to be invoked with a long, exact Python command. A **shell script wrapper** is a short shell program that supplies standard arguments and paths to a longer program, giving it a simple name users can remember. The `bk-*` command family you'll meet in a later chapter is built this way — a one-line shell wrapper around a Python program that would otherwise need a much longer command to invoke correctly every time.

A quick reference for the standard library modules this book's scripts lean on most:

- `json` — read and write JSON files (learning graphs, metadata)
- `csv` — read and write CSV files (the learning graph's dependency table)
- `re` — regular expressions (extracting `CANVAS_HEIGHT` and MicroSim specs)
- `glob` — file globbing (finding every chapter or every simulation)
- `pathlib` — path handling (building file locations that work from any directory)
- `argparse` — naming and parsing command-line arguments
- `sys` — reading raw command-line arguments and setting exit codes

## Key Takeaways

- **Python** and its **standard library** handle the deterministic work; **pip** and **virtual environments** manage anything beyond it.
- **JSON**, **CSV**, and **Markdown parsing**, plus **regular expressions**, convert between the structured formats this book's pipeline depends on.
- **File globbing** and **path handling** let a script operate on many files reliably, from any directory.
- A trustworthy script names its interpreter with a **shebang line**, accepts **command-line arguments**, reports a clear **exit code**, offers **verbose** and **dry-run** modes, and is both **deterministic** and **idempotent**.
- A **shell script wrapper** gives a long, exact command a short name a human will actually remember.

!!! mascot-celebration "You can now read one of this book's actual scripts."
    ![Kit celebrating with arms raised](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    Open any file in `docs/learning-graph/*.py` and you'll recognize every piece now — the shebang line, the argument parsing, the exit code at the end. That's the whole toolbox. Right tool, right task!

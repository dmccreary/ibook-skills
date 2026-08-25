# Docker Python Lab Guide

> Formerly the standalone skill `docker-python-lab`.

## What This Guide Does

Generates interactive Python lab blocks for MkDocs pages in the `learning-python`
textbook (or any MkDocs project following the same pattern).  Each lab shows a
code editor, Run and Reset buttons, and an output area.  Code runs inside a fresh,
isolated Docker container via a local HTTP service on port 5001.

This is the Docker counterpart to the Skulpt lab pattern — same look and feel,
but students run real Python (not browser-emulated Python) with access to the full
standard library and third-party packages.

Use it whenever someone asks to add a Python lab, code runner, interactive Python
exercise, or runnable code block to a textbook page that uses Docker (not Skulpt).
Always follow this guide instead of writing docker lab HTML by hand.

---

## Prerequisites: Shared Infrastructure

Before generating any lab block, make sure the shared files exist.  Check once
per session; skip if already in place.

### 1. Check / create `docs/css/docker-lab.css`

If the file is missing, copy from this skill's assets:

```bash
cp $BK_HOME/skills/microsim-generator/assets/docker-python-lab/docker-lab.css \
   docs/css/docker-lab.css
```

### 2. Check / create `docs/js/docker-lab.js`

```bash
cp $BK_HOME/skills/microsim-generator/assets/docker-python-lab/docker-lab.js \
   docs/js/docker-lab.js
```

### 3. Add to `mkdocs.yml` (if not already present)

Check `extra_css` and `extra_javascript` in `mkdocs.yml`.  If the entries are
missing, add them:

```yaml
extra_css:
  - css/docker-lab.css      # ← add this line

extra_javascript:
  - js/docker-lab.js        # ← add this line
```

Do **not** duplicate entries that are already there.

### 4. Verify the service script exists

The runtime service lives at `scripts/run-python-docker.sh`.  If it is missing
from the project, tell the user — the labs won't work without it.

---

## Lab HTML Template

Each lab needs a unique **suffix** — a short string that distinguishes it from
other labs on the same page.  Use `"1"` for the first lab, `"2"` for the second,
and so on.  The suffix appears in every element ID so the JS can find the right
elements.

### Standard lab (text output only)

```html
<div id="docker-lab-SUFFIX">
<div id="docker-editor-SUFFIX">
<textarea id="docker-code-SUFFIX" spellcheck="false">PYTHON_CODE_HERE
</textarea>
<div id="docker-buttons-SUFFIX">
  <button id="docker-run-SUFFIX" onclick="runDocker('SUFFIX')">&#9654; Run</button>
  <button id="docker-reset-SUFFIX" onclick="resetDocker('SUFFIX')">&#8635; Reset</button>
</div>
<pre id="docker-output-SUFFIX" class="docker-output">Output will appear here after you click Run.</pre>
</div>
</div>
```

**Rules:**

- Replace every `SUFFIX` with the same string (e.g., `1`, `2`, `hello-world`).
- Put the Python code directly inside the `<textarea>` tag — no extra indentation
  relative to column 0, because leading spaces become part of the code.
- The `</textarea>` closing tag must be on its own line with no trailing spaces
  before it; any blank line between the code and `</textarea>` adds an empty line
  in the editor.
- Do **not** add `rows="N"` — the JS auto-sizes the textarea to fit the code.
- Do **not** add `id="main"` to any element — that conflicts with the p5.js canvas
  parent convention used elsewhere in this project.

### Timed lab (shows phase-by-phase timing breakdown)

Only add this variant when the lesson is specifically about how Docker execution
works.  It requires suffix `"4"` by convention and adds a timing table below the
buttons.

```html
<div id="docker-lab-4">
<div id="docker-editor-4">
<textarea id="docker-code-4" spellcheck="false">PYTHON_CODE_HERE
</textarea>
<div id="docker-buttons-4">
  <button id="docker-run-4" onclick="runDockerTimed()">&#9654; Run + Time</button>
  <button id="docker-reset-4" onclick="resetDockerTimed()">&#8635; Reset</button>
</div>
</div>
<div id="docker-timing-display" style="display:none; margin-top:12px;">
  <table id="docker-timing-table">
    <thead>
      <tr><th>#</th><th>Phase</th><th style="text-align:right">Time (ms)</th><th>Bar</th></tr>
    </thead>
    <tbody>
      <tr><td>1</td><td>Send to service (network)</td>
          <td id="td-network-send" style="text-align:right">—</td>
          <td><div class="timing-bar" id="bar-network-send"></div></td></tr>
      <tr><td>2</td><td>Container startup</td>
          <td id="td-startup" style="text-align:right">—</td>
          <td><div class="timing-bar" id="bar-startup"></div></td></tr>
      <tr><td>3</td><td>Python execution</td>
          <td id="td-exec" style="text-align:right">—</td>
          <td><div class="timing-bar" id="bar-exec"></div></td></tr>
      <tr><td>4</td><td>Return to browser (network)</td>
          <td id="td-network-return" style="text-align:right">—</td>
          <td><div class="timing-bar" id="bar-network-return"></div></td></tr>
      <tr style="font-weight:bold; border-top: 2px solid #642580;">
          <td colspan="2">Total round-trip</td>
          <td id="td-total" style="text-align:right">—</td>
          <td></td></tr>
    </tbody>
  </table>
  <p id="docker-timing-note" style="font-size:0.85em; color:#666; margin-top:6px;"></p>
</div>
<pre id="docker-output-4" class="docker-output" style="margin-top:10px;">Output will appear here after you click Run + Time.</pre>
</div>
```

---

## Complete Page Pattern

A page with three labs looks like this:

```markdown
# Page Title

Intro text explaining what the page covers and that students must run
`bash scripts/run-python-docker.sh` in a separate terminal first.

## Lab 1 — Hello, World!

Brief explanation of what this lab demonstrates.

<div id="docker-lab-1">
<div id="docker-editor-1">
<textarea id="docker-code-1" spellcheck="false">print("Hello, World!")
</textarea>
<div id="docker-buttons-1">
  <button id="docker-run-1" onclick="runDocker('1')">&#9654; Run</button>
  <button id="docker-reset-1" onclick="resetDocker('1')">&#8635; Reset</button>
</div>
<pre id="docker-output-1" class="docker-output">Output will appear here after you click Run.</pre>
</div>
</div>

**Try these experiments:**
- Change the message and run again.

---

## Lab 2 — Variables

<div id="docker-lab-2">
<div id="docker-editor-2">
<textarea id="docker-code-2" spellcheck="false">x = 42
print("The answer is", x)
</textarea>
<div id="docker-buttons-2">
  <button id="docker-run-2" onclick="runDocker('2')">&#9654; Run</button>
  <button id="docker-reset-2" onclick="resetDocker('2')">&#8635; Reset</button>
</div>
<pre id="docker-output-2" class="docker-output">Output will appear here after you click Run.</pre>
</div>
</div>
```

---

## Choosing Good Lab Code

- **Keep starter code short** (5–15 lines) so students can read it at a glance.
- **Every lab should produce visible output** — at least one `print()` call.
- **Avoid `input()`** — there is no stdin in the Docker runner.
- **Avoid file I/O** — the container has no persistent filesystem.
- **Avoid `import` of non-stdlib packages** unless `python:3.11-alpine` includes
  them (it ships only the stdlib).
- Match the "See It — Run It — Modify It" rhythm from the Skulpt labs:
  starter code runs and shows something, then "Try these experiments" gives
  specific, achievable modifications.

---

## Service Not Running — User-Facing Error

If a student clicks Run before starting the service, the lab shows:

> Cannot connect to the Python Docker service.
> Please open a terminal and run:
>   bash scripts/run-python-docker.sh
> Then reload this page and try again.

No extra error handling is needed in the page markdown — `docker-lab.js` handles
this automatically.

---

## Multiple Labs per Page — Checklist

When generating labs for a single page:

- [ ] Each lab has a **unique suffix** — `1`, `2`, `3`, …
- [ ] Every element ID includes that suffix (`docker-lab-1`, `docker-code-1`, etc.)
- [ ] Button `onclick` passes the matching suffix string: `runDocker('2')`
- [ ] No two labs share a suffix on the same page
- [ ] The page opens with a "Start the Docker service" instruction block
- [ ] `docs/css/docker-lab.css` and `docs/js/docker-lab.js` are in `mkdocs.yml`

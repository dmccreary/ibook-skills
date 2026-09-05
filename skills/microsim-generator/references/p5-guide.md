---
name: microsim-p5
description: Create an interactive educational MicroSim using the p5.js JavaScript library with distinct regions for drawing and interactive controls.  Each MicroSim is a directory located in the /docs/sims folder.  It has a main.html file that references the javascript code and the main.html can be referenced as an iframe from the index.md.  The metadata.json contains Dublin core metadata about the MicroSim.
---
# Educational MicroSim Creation Skill for P5.js

## Overview

This skill guides the creation of Educational MicroSims using the p5.js JavaScript library.  MicroSims are lightweight, interactive educational simulations designed for browser-based learning. MicroSims occupy a unique position at the intersection of **Simplicity** (focused scope, transparent code), **Accessibility** (browser-native, universal embedding), and **AI Generation** (standardized patterns, prompt-compatible design).

## Working Templates (REQUIRED REFERENCE)

Before generating any p5.js MicroSim, **you MUST read the template files** in `assets/templates/p5/`:

| File | Purpose |
|------|---------|
| `bouncing-ball.js` | Reference implementation showing correct structure, responsive design, and control placement |
| `main-template.html` | Standard HTML shell with correct p5.js CDN and structure |
| `index-template.md` | Documentation template with proper YAML frontmatter and sections |
| `metadata-template.json` | Dublin Core metadata structure |

**CRITICAL**: Copy the structural patterns from `bouncing-ball.js` exactly. Do not deviate from:
- Variable naming conventions (`canvasWidth`, `drawHeight`, `controlHeight`, `sliderLeftMargin`)
- The `updateCanvasSize()` pattern and its placement
- Control positioning relative to `drawHeight`
- The `windowResized()` function structure

## Standard Context

This MicroSim Skill is designed to create all the required files for running your MicroSim on your website.
This microsim skill has been designed to be run within Claude code.
The best practice is to startup Claude Code from the command line
where you at the root of the GitHub checkout directory.  This is
one level down from where you ran GitClone.  This directory should
contain a `.git` directory.
If you don't see a `.git` directory and a `mkdocs.yml` file warn the 
user that the automatic installation process may fail.

We assume that the website has a folder called `docs/sims` that each MicroSim will be placed in.  If you do not see this folder then warn the user.

The p5.js file is also designed to that it can be tested by pasting the JavaScript directly
into the p5.js editor site at https://editor.p5js.org/.  After the JavaScript file has been generated, indicate to the user that the MicroSim can now be tested.

## Purpose

Educational MicroSims transform abstract concepts into visual interactive, manipulable experiences that enable students to learn through exploration and experimentation. Each MicroSim addresses specific learning objectives while maintaining the pedagogical rigor and technical quality necessary for educational deployment.

MicroSims are designed to be referenced by an iframe on an existing website or quickly added to a website or intelligent textbook created with mkdocs.  Because MicroSims have strict rules for controls, they can generate xAPI (eXperience API IEEE 9274.1.1-2023) calls so that interaction events in JSON format can be added to a LRS learning Record Store IEEE 1484.20-2024.

## Development Process

### Step 1: Educational Requirements Specification

Before generating code, articulate the educational purpose:

1. **Subject Area and Topic**: What specific concept does this simulation teach?
2. **Grade Level**: Elementary (K-5), Middle School (6-8), High School (9-12), or Undergraduate
3. **Learning Objectives**: What should students know after using this simulation? (Align with Bloom's Taxonomy: Remember, Understand, Apply, Analyze, Evaluate, Create).  This step is critical, since the type of p5 MicroSim generated will depend on this classification.
4. **Duration**: Typical engagement time (5-15 minutes recommended)
5. **Prerequisites**: What knowledge must students have before using this?
6. **Assessment Opportunities**: How can educators verify learning?  Can the user see a "Quiz Mode" button on this version?

This information will be documented at the end of the index.md file and also stored in a file called metadata.json that is
validated by a JSON Schema at https://github.com/dmccreary/microsims/blob/main/src/microsim-schema/microsim-schema.json

### Step 1.5: Instructional Design Review (MANDATORY)

Before implementation, verify the MicroSim design follows sound pedagogical principles. Document your answers:

#### 1. Single Learning Objective Check
Can you state the learning objective in ONE sentence?
- Write it explicitly: "Students will be able to [verb] [concept] by [interaction]"
- If you cannot state it in one sentence, the scope is too broad—narrow the focus

#### 2. Appropriate Complexity Assessment
| Question | Target | Your Answer |
|----------|--------|-------------|
| How many sliders? | 1-3 | ___ |
| How many buttons? | 0-2 | ___ |
| How many checkboxes? | 0-2 | ___ |
| Total controls | 1-5 | ___ |

If total controls > 5, ask: Is each control essential to the learning objective? Remove non-essential controls.

#### 3. Progressive Disclosure Design
- **Default state**: What does the student see immediately on load? (Should demonstrate the concept without interaction)
- **Exploration path**: What do sliders let students discover? (Each slider should reveal something meaningful)
- **Edge cases**: What happens at slider min/max values? (Should remain educationally meaningful)

#### 4. Cognitive Load Checklist
- [ ] Can a student understand what to do within 5 seconds of seeing it?
- [ ] Are all labels descriptive? (Use "Gravity (m/s²)" not "g")
- [ ] Is the title clear about what concept is being demonstrated?
- [ ] Are value displays formatted with appropriate precision? (2 decimal places max for most values)

#### 5. Accessibility Considerations
- [ ] Will the `describe()` function text make sense to a screen reader user?
- [ ] Are colors distinguishable? (Don't rely solely on red/green)
- [ ] Is text size ≥ 16px for readability from back of classroom?

**If any checkbox is unchecked, address it in the implementation.**

### Step 2: MicroSim Implementation with p5.js

Generate a self-contained, interactive p5.js simulation following the standardized MicroSim architecture.  
The program is width responsive and the p5.js javascript file we create should run without changes using the p5.js editor
for easy testing by the user.

#### Folder Structure

MicroSims have two properties:

1. MICROSIM_TITLE: A title case string with spaces
2. MICROSIM_NAME: A lower-case string with dashes (kebob case)

Each MicroSim is contained in a folder within the /docs/sims directory.  The folder name is $MICROSIM_NAME and has the following contents:

```
/docs/sims/$MICROSIM_NAME # container folder for MicroSim
/docs/sims/$MICROSIM_NAME/index.md # main index markdown for each MicroSim containing the iframe and documentation
/docs/sims/$MICROSIM_NAME/main.html # main HTML5 file containing the p5.js CDN link and importing the p5.js JavaScript
/docs/sims/$MICROSIM_NAME/$MICROSIM_NAME.js # All the p5.js JavaScript
/docs/sims/$MICROSIM_NAME/metadata.json # JSON file with Dublin core metadata and description of controls
```

The following steps are an example of generating a new MicroSim within a checked out intelligent textbook built with mkdocs.
This skill contains templates for the `index.md`, `main.html`, `metadata.json` and a `bouncing-ball.js`.

1. A new folder will be created inside the `/docs/sims` area.  The folder name contains only lower case letters and dashes.  This will be the MICROSIM_NAME which is the kebab case string.
2. An `index.md` file will be generated in the folder that describes the MicroSim and contains in iframe reference to the `main.html` file
3. A small `main.html` file will contain the title, link to the p5.js library from the CDN and include the MICROSIM_NAME.js file.  The `main.html` file must contain a `main` HTML element within the body.
4. A file called `metadata.json` will be created that conforms to the schema at /src/microsim-schema/microsim-schema.json.  This will contain the Dublin core elements such as title, subject, author, publication date etc.  This file is use so that
faceted search engines can find this MicroSim

### Step 2.5: Pre-Generation Layout Planning (MANDATORY)

**Before writing ANY code**, explicitly calculate and document all layout values. This prevents overlap bugs.

#### Control Inventory
List every control the MicroSim will have:

| # | Control Type | Label Text | Value Format | Row |
|---|--------------|------------|--------------|-----|
| 1 | Button | "Start/Pause" | - | 1 |
| 2 | Slider | "Speed" | integer 0-20 | 1 |
| 3 | Checkbox | "Show Grid" | - | 2 |

#### Layout Calculations
Fill in these values based on your control inventory:

```
Number of control rows: ___
controlHeight = (___ × 35) + 10 = ___

drawHeight: ___ (typically 400)
canvasHeight = drawHeight + controlHeight = ___ + ___ = ___
iframeHeight = canvasHeight + 2 = ___

Buttons in row 1: ___ (list them)
sliderLeftMargin = ___ (calculate using formula above)
margin = 25 (standard)
```

#### Position Assignments
For each control, write the exact position call:

```javascript
// Row 1
// [control1].position(___, drawHeight + 5);
// [control2].position(___, drawHeight + 5);

// Row 2 (if applicable)
// [control3].position(___, drawHeight + 40);
```

#### Label Position Assignments
For each label, write the exact text call:

```javascript
// Row 1 labels
// text('[Label]: ' + [value], ___, drawHeight + 15);

// Row 2 labels (if applicable)
// text('[Label]: ' + [value], ___, drawHeight + 50);
```

**You MUST complete this planning before proceeding to code generation.**

## Technical Architecture Standards

### Always Use Native Builtin p5.js Controls

Always use the native builtin controls that are provided by the p5.js library.
The most common controls are button, slider, select, checkbox and input.
Do not attempt to draw your own controls using the drawing commands.

Reference for Create Button: https://p5js.org/reference/p5/createButton/
Reference for Create Slider: https://p5js.org/reference/p5/createSlider/
Reference for Create Select: https://p5js.org/reference/p5/createSelect/
Reference for Create checkBox: https://p5js.org/reference/p5/createCheckbox/
Reference for Create Input: https://p5js.org/reference/p5/createInput/

### Aligning Slider Labels and Values

The default layout is to place both the label and value to the left of a slider control.
We must make sure that the label, value and slider do not overlap.
For a single slider, the positions can be placed manually.
If we have multiple sliders, the horizontal positions of the label, value and sliders should be aligned.

For guidance on aligning the label and value to the left of a slider see the following template
which places the label, value and slider in a HTML div with an inline block CSS rule for
consistent precise placement.

microsim-generator/assets/templates/p5/slider-label-value-alignment.js

### Iframe Structure (REQUIRED)

MicroSims are designed to be called by an HTML `iframe`.  They run in a fixed height region with a variable width.  This is an essential requirement and it will impact
many design choices you make when generating a MicroSim.

Although the main.html file may have some text outside the `<main></main>` element such as a link to return to the documentation, this text is minimal so the area
taken by the `iframe` within a textbook is minimized.  Putting headers above the `<main></main>` takes away from the ability to reuse the microsim in many educational contexts where management of screen real-estate is critical.

Here is an example of how a MicroSim is integrated into any course webpage:

```html
<iframe src="https://dmccreary.github.io/microsims/sims/[MICROSIM_NAME]/main.html" height="500pt" width="100%" scrolling="no"></iframe>
```

The documentation page (index.md) will provide a sample of this iframe statement
that makes it easy for the user to copy.

All iframes that enclose a MicroSim are designed to be run in the entire width of their container and non-scrolling.  This prevents confusion to the user that sees
scrolling regions with scrolling regions of a web page.

Always use named colors like 'aliceblue', 'black' and 'white'.  Never use
a hex representation since these are much harder for the code reader to understand.

Always place a noStroke(); before each text() element.  This ensures that
no residual stroke command will corrupt the text() display.

Every MicroSim must have two distinct regions of the `iframe` canvas:

1. A top `drawing` region with a fixed height called `drawHeight`.  No user interface controls are placed in the drawing region.
2. A user interface `controls` region below the drawing region that contains buttons and sliders with a fixed height called `controlHeight`.

The **width** of the canvas is resized according to the container.  It is set initially, but reset in the draw loop when the container has changed.
This resize function is called every time the web browser window is resized.

We use this layout pattern:

```javascript
// Canvas dimensions - REQUIRED structure
let canvasWidth = 400;              // Initial width (responsive)
let drawHeight = 400;                // Drawing/simulation area height
let controlHeight = 50;              // Controls area height
let canvasHeight = drawHeight + controlHeight;
let margin = 25;                     // Margin for visual elements
let sliderLeftMargin = 140;          // Left margin for slider positioning. Adjust based on label widths.
let defaultTextSize = 16;            // Base text size

function setup() {
  updateCanvasSize(); // this gets the width of the container we are running in
  const canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent(document.querySelector('main')); // NEVER use canvas.parent('main') — that looks for id="main" which does not exist
  // This same rule applies to ALL p5 elements: sliders, buttons, checkboxes, divs, etc.
  // mySlider.parent(document.querySelector('main')); ✓
  // mySlider.parent('main');                         ✗ — null error

  // Create sliders and controls here
  // Position controls relative to drawHeight

  describe('Educational description for screen readers', LABEL);
}

function draw() {
  updateCanvasSize();

  // Drawing area (light blue background with silver border)
  // THIS IS REQUIRED for UI Consistency!  NO EXCEPTIONS!
  fill('aliceblue');
  // Draw a light gray border around BOTH the drawing region AND the control region
  // THIS IS REQUIRED for UI Consistency!  NO EXCEPTIONS!
  stroke('silver');
  rect(0, 0, canvasWidth, drawHeight);
  // Control area (white background)
  // THIS IS REQUIRED for UI Consistency!  NO EXCEPTIONS!
  fill('white');
  rect(0, drawHeight, canvasWidth, controlHeight);

  // IMPORTANT: Draw grid and axes FIRST, then title
  // This prevents title from being overwritten by background elements

  // Draw grid here (if applicable)
  // Draw axes here (if applicable)

  // Draw title AFTER grid/axes
  // If annotation panels or axis labels exist on the right side,
  // offset the title to the left to avoid overlap (e.g., canvasWidth * 0.35)
  fill('black');
  textSize(24);
  textAlign(CENTER, TOP);
  noStroke();
  text('Title of MicroSim', canvasWidth/2, 10);  // Or canvasWidth * 0.35 if right-side elements exist

  // Reset to default text settings
  textAlign(LEFT, CENTER);
  textSize(defaultTextSize);

  // Main drawing code here

  // Draw control labels and values in the control area

}
```

**Title Positioning Guidelines:**

- For simple MicroSims without annotation panels: center the title at `canvasWidth/2`
- For MicroSims with right-side annotation panels or vertical axis labels: offset title to the left (e.g., `canvasWidth * 0.35`) to avoid overlap with axis labels
- Always draw the title AFTER drawing grid/axes to prevent it from being overwritten

### Responsive Design (REQUIRED)

Implement horizontal responsiveness for embedding in various platforms:

```javascript
function windowResized() {
  updateCanvasSize();
  resizeCanvas(canvasWidth, canvasHeight);
}

function updateCanvasSize() {
  const container = document.querySelector('main');
  if (container) {
    canvasWidth = container.offsetWidth;
    // Reposition all controls to match new width
    // all horizontal sliders much be resized when the container size changes
    if (typeof speedSlider !== 'undefined') {
      // update the size of the slider
      speedSlider.size(canvasWidth - sliderLeftMargin - margin);
    }
  }
}
```

### Control Region Layout Formulas (MANDATORY)

Use these explicit formulas to prevent control overlap. **Calculate these values BEFORE writing any code.**

#### Control Height Calculation
```
controlHeight = (numberOfControlRows × 35) + 10
```

Examples:
- 1 row of controls: `controlHeight = (1 × 35) + 10 = 45` (use 50 for safety)
- 2 rows of controls: `controlHeight = (2 × 35) + 10 = 80`
- 3 rows of controls: `controlHeight = (3 × 35) + 10 = 115` (use 120)

#### Canvas Height Calculation
```
canvasHeight = drawHeight + controlHeight
iframeHeight = canvasHeight + 2  // Add 2px for border
```

#### Slider Left Margin Calculation
```
sliderLeftMargin = buttonWidths + labelWidth + valueWidth + gaps
```

| Layout Type | Formula | Typical Value |
|-------------|---------|---------------|
| Slider only (no button) | `labelWidth + valueWidth + 20` | 140px |
| Button + Slider | `buttonWidth + 10 + labelWidth + valueWidth + 20` | 200-240px |
| Two buttons + Slider | `(buttonWidth × 2) + 20 + labelWidth + valueWidth + 20` | 280-320px |

#### Control Y-Position Formulas
```javascript
// First row of controls
row1Y = drawHeight + 5;    // Button y-position
row1Y = drawHeight + 15;   // Text label y-position (vertically centered with slider)

// Second row of controls
row2Y = drawHeight + 40;   // Button y-position
row2Y = drawHeight + 50;   // Text label y-position

// General formula for row N (0-indexed)
rowNButtonY = drawHeight + 5 + (N × 35);
rowNLabelY = drawHeight + 15 + (N × 35);
```

#### Slider Width Calculation
```javascript
sliderWidth = canvasWidth - sliderLeftMargin - margin;
// This MUST be recalculated in windowResized()
```

#### Example: Two-Row Control Layout
```javascript
// Layout calculation for: [Start/Pause] [Reset] ... Speed: ## [====slider====]
//                         Show Grid [checkbox] ... Elasticity: ## [====slider====]

let controlHeight = 80;  // 2 rows × 35 + 10
let sliderLeftMargin = 240;  // Two buttons (140px) + label/value space (100px)

// Row 1
startButton.position(10, drawHeight + 5);
resetButton.position(80, drawHeight + 5);
speedSlider.position(sliderLeftMargin, drawHeight + 5);
text('Speed: ' + speed, 150, drawHeight + 15);

// Row 2
showGridCheckbox.position(10, drawHeight + 40);
elasticitySlider.position(sliderLeftMargin, drawHeight + 40);
text('Elasticity: ' + elasticity, 150, drawHeight + 50);
```

### Drawing Order (IMPORTANT)

The order in which elements are drawn affects visibility. Follow this sequence in the `draw()` function:

1. **Background areas first** - Drawing area rect, control area rect
2. **Grid lines** - If applicable
3. **Axes** - Coordinate axes with labels
4. **Title** - Draw AFTER grid/axes so it doesn't get overwritten
5. **Main visualization** - The primary educational content
6. **Annotation panels** - Info boxes, value displays
7. **Control labels** - Slider labels and values in control area

This order ensures that important elements like titles and annotations appear on top of background elements.

### Visual Design Standards

**Color Scheme**:
- Drawing area background: `'aliceblue'` with `stroke('silver')` border
- Control area background: `'white'`
- Borders: `'silver'`, 1px weight
- Interactive elements: Use high-contrast, colorblind-safe colors

**Typography**:

Try to avoid using any text smaller than 16pt.  We want the MicroSim text to be
readable from the back of the classroom.

- Default title size: 24px (reduced from 36px to fit better with annotations)
- Default text size: 16px
- Control labels: Bold, positioned consistently in the control region
- Value displays: Show current parameter values

**Axis Labels**:
- Use full descriptive labels like "Real Axis" and "Imaginary Axis" instead of abbreviations like "Re" and "Im"
- This improves clarity for students unfamiliar with conventions

**Annotation Panels**:
When creating info panels or annotation boxes:
- Use rounded corners with radius 10: `rect(x, y, w, h, 10)`
- Semi-transparent white background: `fill(255, 255, 255, 230)`
- Light gray border: `stroke(200)`
- Generous vertical spacing (allow 20px per line of text)
- Position panels to avoid overlapping with title or axis labels

### Control Patterns

**Horizontal Sliders In Control Region** (for continuous parameters):

Sliders are created with min, max, default and step parameters.

They are placed below the drawHeight at the x-position of sliderLeftMargin.
The width of the slider is controlled by the `size()` method and spans from sliderLeftMargin to `canvasWidth - margin`.

**sliderLeftMargin Guidelines:**
- Default value: 140px (sufficient for most label/value combinations)
- Increase to 200-240px when buttons appear before sliders (e.g., Play/Pause + Reset buttons)
- Calculate as: button widths + label text width + value display width + padding
- When multiple controls exist in control area, ensure sliders don't overlap with buttons or labels

#### Slider Initialization

Sliders are created in the `setup()` function.  All sliders are horizontal sliders.

```javascript
speedSlider = createSlider(0, 20, 3, 0.1);
speedSlider.position(sliderLeftMargin, drawHeight + 15);
speedSlider.size(canvasWidth - sliderLeftMargin - 15);
speedSlider.input(resetSimulation);
```

Do not use the `style` method to change the width of a slider.  Only use the `size' method.

### Slider Width Responsive Behavior

All horizontal sliders must have their width recalculated using the `size` if the container width changes.

### Slider Label Value Placement

At the end of the `draw()` function the label and values for the sliders must be updated.
They should be placed with a fixed x offset value around 10.
The label and value are concatenated together using the JavaScript "+" operator.
Each row of label/value/slider controls should be placed below the prior row by 30.

```javascript
text('Speed: ' + speed, 10, drawHeight+20);
text('Angle: ' + angle, 10, drawHeight+50);
```

### Buttons for Starting and Pausing a Simulation

For example if a simulation has a state global variable `isRunning` the
button can be created like this:

**Buttons** (for discrete actions):
```javascript
startButton = createButton(isRunning ? 'Pause' : 'Start');
startButton.position(10, drawHeight + 15);
startButton.mousePressed(toggleSimulation);
```

### Use Checkboxes to Show Additional Optional Information

**Checkboxes** (for toggle options):
```javascript
showGridCheckbox = createCheckbox('Show Grid', false);
showGridCheckbox.position(10, drawHeight + 15);
```

### Animation Control for Iframe Embedding (REQUIRED for Animated MicroSims)

When MicroSims are embedded in iframes, animations should **only run when the mouse is over the canvas**. This is important because:

1. **Saves CPU/battery** when user isn't interacting with the simulation
2. **Reduces distraction** while users read surrounding content on the page
3. **Feels responsive** - the simulation "wakes up" when the user hovers over it

**Implementation Pattern:**

Add a state variable to track mouse presence:
```javascript
// In global variables section
let mouseOverCanvas = false;
```

Set up mouse enter/leave event listeners in `setup()`:
```javascript
function setup() {
  updateCanvasSize();
  const canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent(document.querySelector('main'));

  // Track mouse enter/leave for animation control
  canvas.mouseOver(() => mouseOverCanvas = true);
  canvas.mouseOut(() => mouseOverCanvas = false);

  // ... rest of setup
}
```

Only update animation phases when mouse is over canvas:
```javascript
function draw() {
  // ... background drawing code ...

  // Update animation phases only when mouse is over canvas
  if (mouseOverCanvas) {
    pulsePhase += 0.03;
    rotationAngle += 0.02;
    // ... other animation updates
  }

  // ... rest of drawing code (always draws current state)
}
```

**Key Points:**
- The canvas still redraws every frame (showing current state)
- Only the animation *progress* is paused when mouse leaves
- Animation resumes smoothly from where it left off when mouse returns
- This pattern applies to any continuous animation (pulsing, rotating, moving particles, etc.)

## main.html

Our goal is to maintain full compatibility with the p5.js editor.  JavaScript code generated should
always be paste directly into the p5.js editing tool.  This tool uses a standard main.html file that contains a '<main></main>` element that holds our canvas.  Here is the main.html template that we recommend using:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>$SIMULATION_NAME MicroSim using P5.js 2.3.1</title>
    <script src="https://cdn.jsdelivr.net/npm/p5@2.3.1/lib/p5.js"></script>
    <style>
        body {
            margin: 0px;
            padding: 0px;
            font-family: Arial, Helvetica, sans-serif;
        }
    </style>
    <!-- Put your script file name here -->
    <script src="bouncing-ball.js"></script>
</head>
<body>
    <main></main>
    <br/>
    <a href=".">Back to Documentation</a>
</body>
</html>
```

**CRITICAL**: The `<main>` tag must have **no `id` attribute**. Never write `<main id="main">`. The JavaScript uses `document.querySelector('main')` (by tag name), not by id. Adding `id="main"` is unnecessary and using `canvas.parent('main')` (the string form) will fail with a null error because p5.js's `parent()` string lookup searches for `id="main"` — which does not exist.

### Customizing the main.html File

The following items must be modified in each main.html file:

1. The pathname to the JavaScript file should be modified to use the name of the JavaScript file in the MicroSim directory.
2. The title element in the body must be modified for each MicroSim.
3. The version number in the CDN path should only be changed if there are problems running the code.

Note that for label placement in the control area, we set both the margin and padding to be 0.  We do not use a separate CSS file.  This keeps our code simpler.

### P5.js Version Updates

Note that this template uses the jsdelivr.net CDN to get the main p5.js library.  The version number
is hard-coded in this path.  If bugs are found one suggestion is to verify that this library is
the current one used in the p5.js editor.  The following Python code will return the latest
version of p5.js.

https://github.com/dmccreary/microsims/blob/main/src/p5-version/p5-version.py

As of this guide, the default version is p5.js 2.x (currently 2.3.1). p5.js 2.x is largely backward compatible with 1.x global-mode sketches, but check the [migration guide](https://p5js.org/migration-guide/) if a sketch behaves unexpectedly after the upgrade.

## Index.md Generation

A template file `index.md` must be generated for each MicroSim.
This file contains metadata in yml format before the header 1 title

### Index.md Metadata
```yml
---
title: Bouncing Ball
description: A MicroSim of a ball bouncing within the drawing region with a control for changing the speed.
image: /sims/bouncing-ball/bouncing-ball.png
og:image: /sims/bouncing-ball/bouncing-ball.png
twitter:image: /sims/bouncing-ball/bouncing-ball.png
social:
   cards: false
---
```

Here is an example of the content of the index.md file

```markdown
# Bouncing Ball

<iframe src="main.html" height="432px" width="100%" scrolling="no"></iframe>

[Run the Bouncing Ball MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }
<br/>
[Edit the Bouncing Ball MicroSim with the p5.js editor](https://editor.p5js.org/dmccreary/sketches/icpiK4UjE)

## Description

[Description of the MicroSim]

## Lesson Plan

[Lesson Plan for Using the MicroSim]
```

In addition, the following sample iframe should be placed before the description.  Make sure to
enclose the HTML in triple grave accent characters.

You can include this MicroSim on your website using the following `iframe`:

```html
<iframe src="https://dmccreary.github.io/microsims/sims/bouncing-ball/main.html" height="432px" scrolling="no"></iframe>
```

The bouncing ball is the "Hello World!" of the Educational MicroSims.
It contains the key elements that shows the power of the width-responsive MicroSims
graphics with movement and user interaction.  When we design MicroSims, we also
want clearly-visible user interface elements in the control area that can control
the running of our simulations.  This version contains a slider to control the speed of the ball's movement.

## Lesson Plan

Both the title and the description should be modified by this SKILL.

These tags are used to create high-quality social media previews when instructors copy the MicroSim links into tools like Zoom chats.  The .png image should be created by a human with the same name as the MicroSim.
Add are reminder to do this to the user.

## Metadata Generation

The MicroSim metadata is stored within the MicroSim folder in a file called `metadata.json`.  The
structure of this file is governed by a JSON schema file located at /src/microsim-schema/microsim-schema.json.

## Step 3.5: Post-Generation Validation (MANDATORY)

**Before presenting code to the user**, verify all of the following. If ANY check fails, fix the code before presenting.

### Structural Validation Checklist

| Check | How to Verify | Pass? |
|-------|---------------|-------|
| Canvas height math | `canvasHeight === drawHeight + controlHeight` | ☐ |
| Iframe height | `index.md iframe height === canvasHeight + 2` | ☐ |
| updateCanvasSize() first | First line in `setup()` is `updateCanvasSize()` | ☐ |
| windowResized() exists | Function exists and calls `resizeCanvas()` | ☐ |
| describe() called | Accessibility description present in `setup()` | ☐ |
| main element target | Canvas parented to `document.querySelector('main')` — **NEVER** `canvas.parent('main')` (string form looks for `id="main"` which does not exist and throws a null error) | ☐ |

### Control Placement Validation

| Check | How to Verify | Pass? |
|-------|---------------|-------|
| All controls below drawHeight | Every `.position(x, y)` has `y >= drawHeight` | ☐ |
| No control exceeds canvas | Every control `y < canvasHeight - 20` | ☐ |
| Labels don't overlap sliders | Label `x < sliderLeftMargin - 10` | ☐ |
| Sliders resize correctly | `slider.size()` in `windowResized()` for each slider | ☐ |

### Code Quality Validation

| Check | How to Verify | Pass? |
|-------|---------------|-------|
| No hard-coded canvas width | Width comes from `updateCanvasSize()`, not a constant | ☐ |
| noStroke() before text | Every `text()` call preceded by `noStroke()` | ☐ |
| Drawing order correct | Background → Grid → Axes → Title → Content → Controls | ☐ |
| Variable naming | Uses standard names: `canvasWidth`, `drawHeight`, `controlHeight`, `sliderLeftMargin` | ☐ |

### Quick Mental Test

Imagine the canvas at these widths and verify nothing breaks:
- **400px** (narrow mobile)
- **800px** (tablet)
- **1200px** (desktop)

Ask yourself:
- Do sliders resize proportionally?
- Do labels stay readable?
- Does the drawing area scale correctly?

**If any validation fails, fix the issue before presenting the code to the user.**

## Common Bug Patterns (REFERENCE)

Avoid these frequent mistakes:

### ❌ Overlapping Controls
```javascript
// WRONG: Hard-coded y position ignores controlHeight
speedSlider.position(100, 420);

// RIGHT: Position relative to drawHeight
speedSlider.position(sliderLeftMargin, drawHeight + 5);
```

### ❌ Labels Covering Sliders
```javascript
// WRONG: Label x overlaps with slider starting position
text('Speed:', 150, drawHeight+15);
speedSlider.position(150, drawHeight + 5);

// RIGHT: Label before slider, value included in label
text('Speed: ' + speed, 70, drawHeight+15);
speedSlider.position(sliderLeftMargin, drawHeight + 5);  // sliderLeftMargin > 70
```

### ❌ Canvas Not Responsive
```javascript
// WRONG: Missing updateCanvasSize() in setup
function setup() {
  const canvas = createCanvas(800, 450);  // Hard-coded width!
  ...
}

// RIGHT: Get container width first
function setup() {
  updateCanvasSize();  // MUST be first line
  const canvas = createCanvas(canvasWidth, canvasHeight);
  ...
}
```

### ❌ Slider Width Not Updating on Resize
```javascript
// WRONG: Only set slider size once in setup
function windowResized() {
  updateCanvasSize();
  resizeCanvas(canvasWidth, canvasHeight);
  // Missing slider resize!
}

// RIGHT: Resize all sliders
function windowResized() {
  updateCanvasSize();
  resizeCanvas(canvasWidth, canvasHeight);
  speedSlider.size(canvasWidth - sliderLeftMargin - margin);
  // Resize ALL other sliders too
}
```

### ❌ Text Rendered with Stroke
```javascript
// WRONG: stroke still active from previous drawing
stroke('black');
rect(0, 0, 100, 100);
text('Label', 10, 50);  // Text will have ugly outline!

// RIGHT: Always noStroke before text
stroke('black');
rect(0, 0, 100, 100);
noStroke();  // Clear stroke before text
text('Label', 10, 50);
```

### ❌ Incorrect iframe Height
```markdown
<!-- WRONG: Height doesn't match canvas -->
<iframe src="main.html" height="400px"></iframe>
<!-- But canvasHeight = 400 + 80 = 480 -->

<!-- RIGHT: Height = drawHeight + controlHeight + 2 -->
<iframe src="main.html" height="482px"></iframe>
```

### ❌ Control in Drawing Area
```javascript
// WRONG: Button placed in drawing region
startButton.position(10, 50);  // y=50 is inside drawing area!

// RIGHT: All controls below drawHeight
startButton.position(10, drawHeight + 5);
```

## Educational Design Principles

### 1. Focused Scope
Each MicroSim addresses ONE specific learning objective. Do not attempt to teach an entire topic—focus on a single concept, relationship, or phenomenon that benefits from interactive exploration.

### 2. Immediate Feedback
Students must see the effects of their parameter changes instantly. The simulation should update in real-time as sliders move or buttons are clicked.

### 3. Transparent Implementation
Code should be readable and well-commented so educators and advanced students can understand the underlying model. Include comments explaining:
- Mathematical equations being modeled
- Physical principles being demonstrated
- Assumptions and simplifications made

### 4. Progressive Complexity

Start with simple defaults that demonstrate the core concept. Allow students to increase complexity through parameter manipulation.

### 5. Cognitive Load Management

- Minimize extraneous cognitive load: Keep interface clean and uncluttered
- Optimize germane cognitive load: Focus attention on the educational concept
- Support intrinsic complexity: Provide scaffolding for difficult concepts

## Example Learning Objectives by Domain

### Physics & Engineering

- Demonstrate relationship between force, mass, and acceleration
- Visualize wave interference patterns
- Explore conservation of energy in colliding objects
- Show effects of gravity on projectile motion

### Chemistry & Molecular Science

- Visualize molecular bonding and bond angles
- Demonstrate gas laws (pressure, volume, temperature relationships)
- Show chemical equilibrium and Le Chatelier's principle
- Illustrate phase changes at molecular level

### Biology & Life Sciences

- Model population dynamics and predator-prey relationships
- Simulate genetic inheritance patterns
- Demonstrate cell division processes
- Explore ecosystem energy flow

### Mathematics & Computer Science

- Explore function transformations (translations, dilations, reflections)
- Visualize geometric constructions and proofs
- Demonstrate probability distributions
- Show algorithmic behavior (sorting, searching, recursion)

### Systems Thinking

- Model feedback loops and causal relationships
- Demonstrate stock-and-flow dynamics
- Show emergent behavior in complex systems
- Explore sensitivity to initial conditions

## HTML Structure (REQUIRED)

Every MicroSim must be a self-contained HTML file following this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MicroSim: [Concept Name]</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
      background-color: #f5f5f5;
    }
    main {
      max-width: 800px;
      margin: 0 auto;
    }
    h1 {
      text-align: center;
      color: #333;
    }
  </style>
</head>
<body>
  <main>
    <h1>[Simulation Title]</h1>
  </main>
  <script>
    // MicroSim code here following standardized architecture
  </script>
</body>
</html>
```

## Metadata Requirements

For each MicroSim, generate comprehensive metadata following the Educational MicroSim Metadata Schema:

### Dublin Core Elements
- **Title**: Clear, descriptive name
- **Creator**: Author(s) name
- **Subject**: Subject area(s) covered
- **Description**: 2-3 sentence summary
- **Date**: Creation date (YYYY-MM-DD)
- **Type**: "Interactive Simulation"
- **Format**: "text/html"
- **Language**: "en" (or appropriate language code)
- **Rights**: License information (e.g., "CC BY 4.0")

### Educational Metadata
- **Grade Level**: Target age/grade range
- **Subject Area**: Primary subject (Mathematics, Science, etc.)
- **Topic**: Specific topic within subject
- **Learning Objectives**: Bullet list of objectives
- **Bloom's Taxonomy Levels**: Which cognitive levels are addressed
- **Duration**: Estimated engagement time
- **Prerequisites**: Required prior knowledge

### Technical Metadata
- **Framework**: "p5.js"
- **Canvas Dimensions**: "400×450" (initial)
- **Responsive**: "Width-responsive"
- **Dependencies**: "p5.js CDN"
- **Accessibility**: Features included (keyboard nav, screen reader support)

### User Interface Metadata
- **Controls**: List of sliders, buttons, checkboxes with descriptions
- **Parameters**: Each parameter's range, default, purpose

### Simulation Model
- **Model Type**: Type of simulation (physics-based, mathematical, agent-based, etc.)
- **Variables**: List of key variables
- **Equations**: Mathematical equations used (if applicable)
- **Assumptions**: Simplifications made for educational purposes
- **Limitations**: What the model does NOT accurately represent

## Quality Standards

Every MicroSim must meet these criteria:

### Functionality
- ✅ Runs without errors in modern browsers (Chrome, Firefox, Safari, Edge)
- ✅ Responsive design adapts to different container widths
- ✅ Controls respond immediately to user input
- ✅ Simulation resets cleanly without page reload

### Educational Quality
- ✅ Addresses specific learning objectives
- ✅ Provides meaningful interaction (not just animation)
- ✅ Includes educational context (titles, labels, instructions)
- ✅ Accurate representation of underlying concept (within stated limitations)

### Code Quality
- ✅ Follows standardized MicroSim architecture
- ✅ Well-commented and readable
- ✅ Uses meaningful variable names
- ✅ Includes `describe()` function for accessibility

### Visual Design
- ✅ Clean, uncluttered interface
- ✅ Consistent color scheme (aliceblue/white/silver)
- ✅ High contrast for readability
- ✅ Professional appearance suitable for classroom use

## Common Patterns and Examples

### Pattern 1: Parameter Exploration
Students manipulate sliders to see effects on system behavior.
**Example**: Adjust gravity and initial velocity to explore projectile motion.

### Pattern 2: Comparative Visualization
Show two scenarios side-by-side for comparison.
**Example**: Compare sorting algorithms (bubble sort vs. quicksort).

### Pattern 3: System Evolution
Observe how a system changes over time, with play/pause/reset controls.
**Example**: Population growth with birth/death rates.

### Pattern 4: Interactive Construction
Students build or modify structures to understand relationships.
**Example**: Construct geometric shapes to explore area/perimeter relationships.

### Pattern 5: Data Visualization
Transform abstract data into visual representations students can manipulate.
**Example**: Interactive histogram showing probability distributions.

## Workflow Integration

### For Educators Creating MicroSims:
1. Identify specific learning objective
2. Describe desired simulation in natural language
3. AI generates initial implementation following these standards
4. Educator previews and requests refinements
5. Metadata generated automatically
6. Deploy to learning management system via iframe

### For Students Extending MicroSims:
1. Start with existing MicroSim
2. Modify parameters or add features
3. Observe how changes affect behavior
4. Document observations and learning

## Deployment Considerations

### iframe Embedding (Universal Deployment)

MicroSims are designed to be embedded in any web page with a single HTML line:

```html
<iframe src="https://dmccreary.github.io/microsims/sims/bouncing-ball/main.html"
        height="432"
        scrolling="no">
</iframe>
```

For the height, it should be the sum of the drawHeight and the controlHeight plus 2.

### Learning Management System Integration

MicroSim should be designed to be easily integrated
with any website that supports the HTML `iframe` element.

- Compatible with Canvas, Blackboard, Moodle, Google Classroom
- No server-side requirements
- Works in restricted network environments
- Mobile-friendly for tablets and smartphones

### xAPI Integration (Optional)

For learning analytics, MicroSims can emit xAPI statements:
- Button clicks, slider adjustments
- Time spent on task
- Parameter exploration patterns
- Performance on embedded assessments

## Pedagogical Context

### Research Foundation

Educational simulations demonstrate consistent benefits:
- 15-25% improvement in conceptual understanding
- 30-40% reduction in time to mastery
- 25-35% increase in student engagement

### Effective Use Strategies
- **Guided Exploration**: Provide 2-3 open-ended questions to focus investigation
- **Predict-Test-Observe**: Have students predict before manipulating
- **Collaborative Learning**: Pairs/groups discuss observations
- **Scaffolded Challenge**: Progress from simple to complex parameter spaces

### Common Pitfalls to Avoid
- ❌ Too many controls (cognitive overload)
- ❌ Unclear cause-and-effect relationships
- ❌ Animation without interactivity
- ❌ Over-simplification that creates misconceptions
- ❌ Inaccessible interface (poor contrast, no keyboard support)

## Example MicroSim: Bouncing Ball (Physics)

### Educational Purpose
Demonstrate effects of gravity and elasticity on projectile motion, illustrating energy conservation and loss.

### Learning Objectives
- Understand relationship between gravitational acceleration and trajectory
- Observe energy loss in non-elastic collisions
- Apply physics concepts to predict behavior

### Implementation Highlights
```javascript
// Core physics model
velocity.y += gravity; // Acceleration due to gravity
position.add(velocity);

// Collision detection and response
if (position.y >= height - radius) {
  position.y = height - radius;
  velocity.y *= -elasticity; // Energy loss on bounce
}
```

### Controls Provided

- Gravity slider (0-2 m/s², default: 0.5)
- Elasticity slider (0-1, default: 0.7)
- Start/Pause button
- Reset button

This example demonstrates all core MicroSim principles: focused scope, transparent physics, immediate feedback, and clean interface.

## Continuous Improvement

### Iteration Based on Use
- Collect feedback from educators and students
- Observe which parameters students explore most
- Identify common misconceptions revealed by interactions
- Refine based on actual classroom use

### AI-Assisted Refinement
After initial generation, iteratively improve through prompts like:
- "Add a slider to control [parameter]"
- "Show the current velocity value"
- "Include a graph showing energy over time"
- "Add a grid to help students measure distances"

## Inclusion in the mkdocs Navigation System

After the files have been created the next step
is to include the MicroSim in the mkdocs navigation system.
This is done by adding a single line to the `mkdocs.yml` file
located in the home directory of the GitHub repository.
The mkdocs.yml file contains a `nav` element.  Within
that there will be a section for all the MicroSims.

```yml
nav:
  [text omitted...]
  - MicroSims:
    - List of MicroSims: sims/index.md
    - MicroSim Name 1: sims/name-1/index.md
    - MicroSim Name 2: sims/name-2/index.md

  [text omitted...]
```

The best practice is to add the new MicroSim you just created
at the end of the MicroSims like this:

```yml
nav:
  [text omitted...]
  - MicroSims:
    - List of MicroSims: sims/index.md
    - MicroSim Name 1: sims/name-1/index.md
    - MicroSim Name 2: sims/name-2/index.md
    - NEW_MICROSIM_NAME_HERE: sims/name-in-kebab-case/index.md

  [text omitted...]
```

## Zip Packaging (Optional)

By default, a zip package is not created unless the user requests
it.

If the users requests "create a package" or "create a zip package", then after you generate a MicroSim with the required files, create a zip file that the user can download.  Then return the following instruction:

Congratulations!  Your MicroSim zip file has been generated and is ready for testing.  The best way
to instal this is to run the following commands using the bouncing-ball example:

```sh
cd /doc/sims
unzip bouncing-ball.zip
```

## Testing Deployment 
If you are going to test the MicroSim within mkdocs site you can also do the following:
```sh
# move the zip file out of the way so it does not get copied to the web site
mv bouncing-ball.zip /tmp
# edit the mkdocs.yml file
open ../../mkdocs.yml
# test your code locally
mkdocs serve
# go to the right link: http://localhost:8000/[GITHUB_DIR_NAME]/sims/[sim-name]/
# check in your code with git
# deploy your new microsim to production!
mkdocs gh-deploy
```

Then make sure that the site navigation (mkdocs.yml) file includes the link to this new MicroSim.

## Auto-Standardization (REQUIRED)

**After creating the MicroSim files, you MUST run standardization automatically.**

This step is defined in the parent `SKILL.md` (Step 4: Auto-Standardization). It ensures:

1. **metadata.json** is complete and valid
2. **index.md** has proper YAML frontmatter with quality_score
3. **Lesson Plan** section is generated
4. **References** section is added
5. All documentation meets quality standards

**Do not skip this step.** It eliminates the need for manual follow-up with `microsim-utils standardization`.

Read `../microsim-utils/references/standardization.md` and implement all fixes automatically since this is a newly created MicroSim.

## Conclusion

Educational MicroSims represent a powerful convergence of pedagogical effectiveness, technical accessibility, and AI-generation capability. By following these standards, any educational concept that benefits from interactive exploration can be transformed into a high-quality, embeddable, reusable learning tool.

The key is maintaining focus: one concept, clear interactions, immediate feedback, transparent implementation. Each MicroSim should feel carefully crafted, pedagogically sound, and ready for deployment in real educational contexts.

---

**For Anthropic Claude Code**: When creating MicroSims, always reference the comprehensive rules in `.cursor/rules/microsims.mdc` and follow the metadata schema in `src/microsim-schema.json`. Each MicroSim should feel like a polished educational tool developed by expert instructional designers and developers working at the top of their field.

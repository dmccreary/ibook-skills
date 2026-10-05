// Idempotent Script Simulator MicroSim
// CANVAS_HEIGHT: 480
// Two scripts have the same job: make sure the row "taxonomy-names.json" is in
// a file. The non-idempotent script appends the row every time it runs. The
// idempotent script checks first and adds the row only if it is missing.
// Run each one several times and compare the end state of the two files.

// Canvas dimensions - REQUIRED structure
let canvasWidth = 400;               // Initial width (responsive)
let drawHeight = 400;                // Drawing area height
let controlHeight = 80;              // Controls area height (2 rows)
let canvasHeight = drawHeight + controlHeight;
let margin = 20;                     // Margin for visual elements
let defaultTextSize = 16;

const ROW_TEXT = 'taxonomy-names.json';
const PANEL_Y = 42;
const PANEL_H = 284;
const INFO_Y = 333;
const INFO_H = 58;
const MAX_VISIBLE_ROWS = 4;
const INITIAL_RUNS = 3;

// Simulation state: the two "files" and how many times each script has run
let nonIdempotentRows = [];
let idempotentRows = [];
let nonIdempotentRuns = 0;
let idempotentRuns = 0;

// Controls
let runNonButton, runIdemButton, runBothButton, resetButton;
let narrowButtons = null;

function setup() {
  updateCanvasSize();
  const canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent(document.querySelector('main'));
  const mainElement = document.querySelector('main');

  runNonButton = createButton('Run Non-Idempotent Script');
  runNonButton.parent(mainElement);
  runNonButton.mousePressed(runNonIdempotent);

  runIdemButton = createButton('Run Idempotent Script');
  runIdemButton.parent(mainElement);
  runIdemButton.mousePressed(runIdempotent);

  runBothButton = createButton('Run Both');
  runBothButton.parent(mainElement);
  runBothButton.mousePressed(function () {
    runNonIdempotent();
    runIdempotent();
  });

  resetButton = createButton('Reset Both');
  resetButton.parent(mainElement);
  resetButton.mousePressed(resetBoth);

  positionControls();

  // Start with each script already run three times, so the two end states
  // can be compared before anything is clicked. Reset Both empties the files.
  for (let i = 0; i < INITIAL_RUNS; i++) {
    runNonIdempotent();
    runIdempotent();
  }

  describe('Idempotent script simulator. Two side-by-side panels each show a file. The non-idempotent script on the left appends the row taxonomy-names.json every time it runs, so duplicates pile up. The idempotent script on the right checks first, so its file always holds exactly one row. Buttons run each script, run both, and reset.', LABEL);
}

function draw() {
  updateCanvasSize();

  // Drawing area
  fill('aliceblue');
  stroke('silver');
  strokeWeight(1);
  rect(0, 0, canvasWidth, drawHeight);
  // Control area
  fill('white');
  rect(0, drawHeight, canvasWidth, controlHeight);

  // Title
  fill('black');
  noStroke();
  textStyle(NORMAL);
  textAlign(CENTER, TOP);
  textSize(canvasWidth < 480 ? 20 : 24);
  text('Idempotent Script Simulator', canvasWidth / 2, 9);

  const panelW = (canvasWidth - margin * 3) / 2;
  const leftX = margin;
  const rightX = margin * 2 + panelW;

  drawPanel(leftX, panelW, {
    title: 'Non-Idempotent Script',
    headerColor: 'lightsalmon',
    code: ['# no check first', 'rows.append(row)'],
    rows: nonIdempotentRows,
    runs: nonIdempotentRuns,
    idempotent: false
  });
  drawPanel(rightX, panelW, {
    title: 'Idempotent Script',
    headerColor: 'mediumaquamarine',
    code: ['if row not in rows:', '    rows.append(row)'],
    rows: idempotentRows,
    runs: idempotentRuns,
    idempotent: true
  });

  drawInfo(leftX, rightX, panelW);
}

// ---------------------------------------------------------------------------
// The two scripts
// ---------------------------------------------------------------------------

// Appends the row every time: running twice leaves two rows.
function runNonIdempotent() {
  nonIdempotentRuns++;
  nonIdempotentRows.push(ROW_TEXT);
}

// Checks for an existing row first: running twice still leaves one row.
function runIdempotent() {
  idempotentRuns++;
  if (!idempotentRows.includes(ROW_TEXT)) {
    idempotentRows.push(ROW_TEXT);
  }
}

function resetBoth() {
  nonIdempotentRows = [];
  idempotentRows = [];
  nonIdempotentRuns = 0;
  idempotentRuns = 0;
}

// ---------------------------------------------------------------------------
// Drawing
// ---------------------------------------------------------------------------

function drawPanel(x, w, p) {
  const narrow = w < 250;
  // panel body
  fill('white');
  stroke('slategray');
  strokeWeight(1.5);
  rect(x, PANEL_Y, w, PANEL_H, 8);
  // header bar
  fill(p.headerColor);
  rect(x, PANEL_Y, w, 30, 8, 8, 0, 0);
  noStroke();
  fill('black');
  textStyle(BOLD);
  textAlign(CENTER, CENTER);
  textSize(narrow ? 14 : 17);
  text(p.title, x + w / 2, PANEL_Y + 16);
  textStyle(NORMAL);

  // the one line of code that differs
  fill('whitesmoke');
  stroke('silver');
  strokeWeight(1);
  rect(x + 8, PANEL_Y + 37, w - 16, 40, 4);
  noStroke();
  fill('black');
  textFont('monospace');   // code needs a fixed-width font so the indent shows
  textAlign(LEFT, TOP);
  textSize(narrow ? 11 : 14);
  text(p.code[0], x + 14, PANEL_Y + 42);
  text(p.code[1], x + 14, PANEL_Y + 59);
  textFont('sans-serif');

  // run counter
  textAlign(LEFT, CENTER);
  textSize(narrow ? 14 : 16);
  fill('black');
  text((narrow ? 'Runs: ' : 'Times run: ') + p.runs, x + 10, PANEL_Y + 93);
  textAlign(RIGHT, CENTER);
  fill('dimgray');
  textSize(narrow ? 13 : 14);
  text((narrow ? 'rows: ' : 'rows in file: ') + p.rows.length, x + w - 10, PANEL_Y + 93);

  // file contents
  const listY = PANEL_Y + 108;
  const rowH = 26;
  if (p.rows.length === 0) {
    fill('gray');
    textStyle(ITALIC);
    textAlign(CENTER, CENTER);
    textSize(14);
    text('The file is empty.', x + w / 2, listY + 40);
    textStyle(NORMAL);
  }
  const overflow = p.rows.length > MAX_VISIBLE_ROWS;
  const shown = overflow ? MAX_VISIBLE_ROWS - 1 : p.rows.length;
  for (let i = 0; i < shown; i++) {
    const y = listY + i * rowH;
    const duplicate = i > 0;
    fill(duplicate ? 'mistyrose' : 'white');
    stroke(duplicate ? 'crimson' : 'seagreen');
    strokeWeight(1.5);
    rect(x + 10, y, w - 20, rowH - 5, 4);
    noStroke();
    fill('black');
    textAlign(LEFT, CENTER);
    textSize(narrow ? 12 : 14);
    text(ROW_TEXT, x + 16, y + (rowH - 5) / 2);
    if (duplicate && !narrow) {
      fill('crimson');
      textAlign(RIGHT, CENTER);
      text('duplicate', x + w - 16, y + (rowH - 5) / 2);
    }
  }
  if (overflow) {
    const y = listY + shown * rowH;
    noStroke();
    fill('crimson');
    textAlign(LEFT, CENTER);
    textSize(narrow ? 12 : 14);
    text('+ ' + (p.rows.length - shown) + ' more duplicate rows', x + 16, y + (rowH - 5) / 2);
  }

  // what the last run did, and the verdict on the end state
  const statusY = PANEL_Y + 216;
  stroke('silver');
  strokeWeight(1);
  line(x + 8, statusY, x + w - 8, statusY);
  noStroke();
  textAlign(LEFT, TOP);
  textSize(narrow ? 12 : 14);
  textLeading(narrow ? 14 : 17);
  // long and short wording for what the last run did; the short one is used
  // when the long one does not fit on a single line
  let lastRun, lastRunShort, verdict, verdictColor;
  if (p.runs === 0) {
    lastRun = lastRunShort = 'Not run yet.';
    verdict = '';
    verdictColor = 'black';
  } else if (p.idempotent && p.runs > 1) {
    lastRun = 'Run ' + p.runs + ': row already present, nothing added.';
    lastRunShort = 'Run ' + p.runs + ': nothing added.';
    verdict = 'Same end state, no matter how many times you run it';
    verdictColor = 'seagreen';
  } else {
    lastRun = 'Run ' + p.runs + ': Added row: ' + ROW_TEXT;
    lastRunShort = 'Run ' + p.runs + ': added the row.';
    verdict = (!p.idempotent && p.runs >= 2) ? 'State has diverged from a single clean run' : '';
    verdictColor = 'crimson';
  }
  if (textWidth(lastRun) > w - 20) lastRun = lastRunShort;
  fill('black');
  text(lastRun, x + 10, statusY + 6, w - 20, 20);
  if (verdict) {
    fill(verdictColor);
    textStyle(BOLD);
    text(verdict, x + 10, statusY + (narrow ? 22 : 28), w - 20, narrow ? 44 : 38);
    textStyle(NORMAL);
  }
}

// Infobox strip: what real script behavior each panel stands for
function drawInfo(leftX, rightX, panelW) {
  const overPanels = mouseY >= PANEL_Y && mouseY <= PANEL_Y + PANEL_H;
  const overLeft = overPanels && mouseX >= leftX && mouseX <= leftX + panelW;
  const overRight = overPanels && mouseX >= rightX && mouseX <= rightX + panelW;

  if (overLeft || overRight) {
    // outline the hovered panel
    noFill();
    stroke('black');
    strokeWeight(2.5);
    rect(overLeft ? leftX : rightX, PANEL_Y, panelW, PANEL_H, 8);
  }

  fill('white');
  stroke('slategray');
  strokeWeight(1);
  rect(margin, INFO_Y, canvasWidth - margin * 2, INFO_H, 8);
  noStroke();
  textAlign(LEFT, TOP);
  const small = canvasWidth < 620;
  textSize(small ? 12 : 14);
  textLeading(small ? 14 : 17);
  let msg;
  if (overLeft) {
    fill('black');
    msg = 'Real scripts like this: one that appends a line to a file or inserts a database row every time it runs. Run it twice by accident and the data holds a duplicate.';
  } else if (overRight) {
    fill('black');
    msg = 'Real scripts like this: one that checks before it writes, such as a script that inserts an iframe only if one is not already present. Running it again is always safe.';
  } else {
    fill('dimgray');
    msg = 'Hover over either panel to see what kind of real script it stands for. Select Reset Both to empty the files, then run each script yourself and compare.';
  }
  text(msg, margin + 10, INFO_Y + 7, canvasWidth - margin * 2 - 20, INFO_H - 10);
}

// Each run button sits under its own panel; Run Both and Reset Both are below
function positionControls() {
  const panelW = (canvasWidth - margin * 3) / 2;
  const narrow = panelW < 250;
  if (narrow !== narrowButtons) {
    narrowButtons = narrow;
    runNonButton.html(narrow ? 'Run Non-Idempotent' : 'Run Non-Idempotent Script');
    runIdemButton.html(narrow ? 'Run Idempotent' : 'Run Idempotent Script');
  }
  runNonButton.position(margin, drawHeight + 8);
  runIdemButton.position(margin * 2 + panelW, drawHeight + 8);
  runBothButton.position(margin, drawHeight + 45);
  resetButton.position(margin + 95, drawHeight + 45);
}

// ---------------------------------------------------------------------------
// Responsive sizing - always at the end of the file
// ---------------------------------------------------------------------------

function windowResized() {
  updateCanvasSize();
  resizeCanvas(canvasWidth, canvasHeight);
  positionControls();
}

function updateCanvasSize() {
  const container = document.querySelector('main');
  if (container) {
    canvasWidth = Math.floor(container.getBoundingClientRect().width);
  }
}

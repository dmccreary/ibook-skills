// Serial Versus Parallel Cost Calculator MicroSim
// CANVAS_HEIGHT: 550
// Compares the total token cost of running a task with one agent (serial)
// against running it with one agent per sub-task (parallel).
//
//   serial total   = (work tokens x sub-tasks) + (1 x startup overhead)
//   parallel total = (work tokens x sub-tasks) + (sub-tasks x startup overhead)
//
// The only difference is the startup overhead, which serial execution pays
// once and parallel execution pays once per agent. The model deliberately
// leaves out everything else (elapsed time, shared context, retries).

// Canvas dimensions - REQUIRED structure
let canvasWidth = 400;               // Initial width (responsive)
let drawHeight = 400;                // Drawing area height
let controlHeight = 150;             // Controls area height (4 rows)
let canvasHeight = drawHeight + controlHeight;
let margin = 20;                     // Margin for visual elements
let sliderLeftMargin = 330;          // Recomputed for narrow canvases
let defaultTextSize = 16;

// Parallel is called "about the same" when it costs less than this much more
const ABOUT_THE_SAME = 0.05;

// Section geometry inside the drawing region
const SERIAL_LABEL_Y = 56;
const SERIAL_BAR_Y = 68;
const PARALLEL_LABEL_Y = 124;
const PARALLEL_BAR_Y = 136;
const BAR_H = 32;
const LEGEND_Y = 188;
const FORMULA_Y = 208;
const FORMULA_H = 62;
const VERDICT_Y = 282;
const VERDICT_H = 106;

// Controls
let subTaskSlider, workSlider, overheadSlider, formulaCheckbox;

function setup() {
  updateCanvasSize();
  const canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent(document.querySelector('main'));
  const mainElement = document.querySelector('main');

  subTaskSlider = createSlider(1, 20, 8, 1);
  subTaskSlider.parent(mainElement);
  subTaskSlider.attribute('aria-label', 'Number of sub-tasks');

  workSlider = createSlider(1000, 50000, 10000, 1000);
  workSlider.parent(mainElement);
  workSlider.attribute('aria-label', 'Tokens of real work per sub-task');

  overheadSlider = createSlider(5000, 20000, 12000, 500);
  overheadSlider.parent(mainElement);
  overheadSlider.attribute('aria-label', 'Startup overhead per agent in tokens');

  formulaCheckbox = createCheckbox('Show formula', false);
  formulaCheckbox.parent(mainElement);
  formulaCheckbox.style('font-size', '16px');

  positionControls();

  describe('Serial versus parallel cost calculator. Three sliders set the number of sub-tasks, the tokens of real work per sub-task, and the startup overhead per agent. Two stacked bars show the serial total and the parallel total in tokens, and a verdict line states how many more tokens parallel execution costs.', LABEL);
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
  textSize(canvasWidth < 520 ? 18 : 24);
  text('Serial Versus Parallel Cost Calculator', canvasWidth / 2, 10);

  // Read the sliders and do the arithmetic
  const n = subTaskSlider.value();
  const work = workSlider.value();
  const overhead = overheadSlider.value();
  const workTotal = work * n;
  const serialTotal = workTotal + 1 * overhead;
  const parallelTotal = workTotal + n * overhead;

  drawBars(n, work, overhead, serialTotal, parallelTotal);
  drawLegend();
  drawFormula(n, work, overhead, serialTotal, parallelTotal);
  drawVerdict(n, work, overhead, serialTotal, parallelTotal);
  drawControlLabels(n, work, overhead);
}

function fmt(value) {
  return value.toLocaleString('en-US');
}

// ---------------------------------------------------------------------------
// Drawing
// ---------------------------------------------------------------------------

// Two stacked bars on one shared scale. Each sub-task's real work is its own
// block; each agent's startup overhead is its own block.
function drawBars(n, work, overhead, serialTotal, parallelTotal) {
  const x0 = margin;
  const fullW = canvasWidth - margin * 2;
  const scale = fullW / parallelTotal;   // the parallel bar always spans the full width

  // Serial: one overhead block, then n work blocks
  barLabel('Serial Total: ' + fmt(serialTotal) + ' tokens', '1 agent', SERIAL_LABEL_Y);
  let x = x0;
  block(x, SERIAL_BAR_Y, overhead * scale, 'tomato');
  x += overhead * scale;
  for (let i = 0; i < n; i++) {
    block(x, SERIAL_BAR_Y, work * scale, 'steelblue');
    x += work * scale;
  }

  // Parallel: n agents, each paying overhead and then doing its work block
  barLabel('Parallel Total: ' + fmt(parallelTotal) + ' tokens', n + (n === 1 ? ' agent' : ' agents'), PARALLEL_LABEL_Y);
  x = x0;
  for (let i = 0; i < n; i++) {
    block(x, PARALLEL_BAR_Y, overhead * scale, 'tomato');
    x += overhead * scale;
    block(x, PARALLEL_BAR_Y, work * scale, 'steelblue');
    x += work * scale;
  }
}

function barLabel(label, agents, y) {
  noStroke();
  fill('black');
  textStyle(BOLD);
  textAlign(LEFT, BOTTOM);
  textSize(canvasWidth < 520 ? 15 : 17);
  text(label, margin, y + 8);
  textStyle(NORMAL);
  fill('dimgray');
  textAlign(RIGHT, BOTTOM);
  textSize(14);
  text(agents, canvasWidth - margin, y + 8);
}

function block(x, y, w, colorName) {
  fill(colorName);
  stroke('white');
  strokeWeight(1);
  rect(x, y, w, BAR_H);
}

function drawLegend() {
  const y = LEGEND_Y;
  textAlign(LEFT, CENTER);
  textSize(14);
  stroke('white');
  strokeWeight(1);
  fill('tomato');
  rect(margin, y - 7, 14, 14);
  noStroke();
  fill('black');
  const overheadLabel = canvasWidth < 520 ? 'Startup overhead' : 'Startup overhead (one block per agent)';
  text(overheadLabel, margin + 20, y);
  const x2 = margin + 20 + textWidth(overheadLabel) + 22;
  stroke('white');
  fill('steelblue');
  rect(x2, y - 7, 14, 14);
  noStroke();
  fill('black');
  text(canvasWidth < 520 ? 'Real work' : 'Real work (one block per sub-task)', x2 + 20, y);
}

// The two total formulas as live-updating equations
function drawFormula(n, work, overhead, serialTotal, parallelTotal) {
  const x0 = margin;
  const w = canvasWidth - margin * 2;
  fill('white');
  stroke('silver');
  strokeWeight(1);
  rect(x0, FORMULA_Y, w, FORMULA_H, 8);
  noStroke();

  if (!formulaCheckbox.checked()) {
    fill('dimgray');
    textStyle(ITALIC);
    textAlign(CENTER, CENTER);
    textSize(canvasWidth < 520 ? 13 : 15);
    text('Check "Show formula" below to see how each total is calculated.',
      x0 + 10, FORMULA_Y + 4, w - 20, FORMULA_H - 8);
    textStyle(NORMAL);
    return;
  }

  const serial = 'Serial = (' + fmt(work) + ' × ' + n + ') + (1 × ' + fmt(overhead) + ') = ' + fmt(serialTotal);
  const parallel = 'Parallel = (' + fmt(work) + ' × ' + n + ') + (' + n + ' × ' + fmt(overhead) + ') = ' + fmt(parallelTotal);
  fill('black');
  textAlign(LEFT, CENTER);
  let size = 16;
  textSize(size);
  while (size > 10 && Math.max(textWidth(serial), textWidth(parallel)) > w - 24) {
    size--;
    textSize(size);
  }
  text(serial, x0 + 12, FORMULA_Y + 20);
  text(parallel, x0 + 12, FORMULA_Y + 43);
}

// The one-line verdict, plus two supporting facts
function drawVerdict(n, work, overhead, serialTotal, parallelTotal) {
  const x0 = margin;
  const w = canvasWidth - margin * 2;
  const extra = parallelTotal - serialTotal;         // = (n - 1) x overhead
  const percentMore = extra / serialTotal;
  const overheadShare = (n * overhead) / parallelTotal;

  let headline, line2, line3, fillColor, strokeColor;
  if (n === 1) {
    headline = 'No benefit from parallel with only one sub-task';
    line2 = 'Both totals are ' + fmt(serialTotal) + ' tokens: one agent, one startup overhead.';
    line3 = 'Add sub-tasks to see the two totals separate.';
    fillColor = 'lemonchiffon';
    strokeColor = 'goldenrod';
  } else {
    if (percentMore < ABOUT_THE_SAME) {
      headline = 'Parallel and serial cost about the same here';
      fillColor = 'honeydew';
      strokeColor = 'seagreen';
    } else {
      headline = 'Parallel costs ' + fmt(extra) + ' more tokens for this workload';
      fillColor = 'mistyrose';
      strokeColor = 'crimson';
    }
    line2 = 'Parallel is ' + (percentMore * 100).toFixed(percentMore < 0.1 ? 1 : 0) + '% more than serial (' +
      fmt(extra) + ' extra tokens). Startup overhead is ' + Math.round(overheadShare * 100) + '% of the parallel total.';
    if (overhead >= work) {
      line3 = 'Each agent spends ' + fmt(overhead) + ' tokens starting up to do ' + fmt(work) + ' tokens of real work.';
    } else {
      line3 = 'Each agent does ' + fmt(work) + ' tokens of real work, ' +
        (work / overhead).toFixed(1).replace('.0', '') + ' times its startup overhead.';
    }
  }

  fill(fillColor);
  stroke(strokeColor);
  strokeWeight(1.5);
  rect(x0, VERDICT_Y, w, VERDICT_H, 8);
  noStroke();
  fill('black');
  textAlign(LEFT, TOP);
  textStyle(BOLD);
  let size = 18;
  textSize(size);
  while (size > 12 && textWidth(headline) > w - 24) {
    size--;
    textSize(size);
  }
  text(headline, x0 + 12, VERDICT_Y + 10);
  textStyle(NORMAL);
  const small = canvasWidth < 620;
  textSize(small ? 12 : 14);
  textLeading(small ? 14 : 17);
  const lineH = small ? 14 : 17;
  const line2Rows = textWidth(line2) > w - 24 ? 2 : 1;
  text(line2, x0 + 12, VERDICT_Y + 37, w - 24, lineH * 2 + 2);
  text(line3, x0 + 12, VERDICT_Y + 37 + line2Rows * lineH + 5, w - 24, lineH * 2 + 2);
}

function drawControlLabels(n, work, overhead) {
  fill('black');
  noStroke();
  textStyle(NORMAL);
  textAlign(LEFT, CENTER);
  textSize(defaultTextSize);
  const narrow = canvasWidth < 640;
  text((narrow ? 'Sub-tasks: ' : 'Number of sub-tasks: ') + n, 10, drawHeight + 18);
  text((narrow ? 'Work per sub-task: ' : 'Tokens of real work per sub-task: ') + fmt(work), 10, drawHeight + 53);
  text((narrow ? 'Startup overhead: ' : 'Startup overhead per agent: ') + fmt(overhead), 10, drawHeight + 88);
}

function positionControls() {
  sliderLeftMargin = canvasWidth < 640 ? 215 : 330;
  const sliderW = canvasWidth - sliderLeftMargin - margin;
  subTaskSlider.position(sliderLeftMargin, drawHeight + 8);
  subTaskSlider.size(sliderW);
  workSlider.position(sliderLeftMargin, drawHeight + 43);
  workSlider.size(sliderW);
  overheadSlider.position(sliderLeftMargin, drawHeight + 78);
  overheadSlider.size(sliderW);
  formulaCheckbox.position(10, drawHeight + 116);
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

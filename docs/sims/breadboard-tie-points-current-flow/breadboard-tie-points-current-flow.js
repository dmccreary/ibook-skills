// Breadboard Tie Points and Animated Current Flow MicroSim
// CANVAS_HEIGHT: 520
// Click any hole on a simplified solderless breadboard to see every other
// hole that shares its internal metal strip (its tie point group). Then
// complete a battery, resistor, and LED circuit by adding the final jumper
// wire and watch current flow around the closed loop.
//
// The model of the board:
//   - one power rail along the top (+) and one along the bottom (-); every
//     hole in a rail is joined lengthwise by one strip
//   - numbered columns of holes; in each column, rows a-e are joined by one
//     strip and rows f-j are joined by another
//   - the center gap separates rows a-e from rows f-j
// Real boards usually have a + and - pair of rails on each side, and some
// split their rails at the middle. This board is simplified to two rails.
// The moving dots show conventional current, from battery + to battery -.

// Canvas dimensions - REQUIRED structure
let canvasWidth = 400;               // Initial width (responsive)
let drawHeight = 470;                // Drawing area height
let controlHeight = 50;              // Controls area height (1 row)
let canvasHeight = drawHeight + controlHeight;
let margin = 12;                     // Margin for visual elements
let defaultTextSize = 16;

const ROWS_TOP = ['a', 'b', 'c', 'd', 'e'];
const ROWS_BOTTOM = ['f', 'g', 'h', 'i', 'j'];

// Component placement (column numbers start at 1)
const JUMPER1 = { railCol: 2, col: 3, row: 'a' };          // + rail to a3
const RESISTOR = { colA: 3, colB: 7, row: 'c' };           // c3 to c7
const LED = { col: 7, anodeRow: 'e', cathodeRow: 'f' };    // e7 to f7, across the gap
const JUMPER2 = { col: 7, row: 'j', railCol: 8 };          // j7 to - rail (the final jumper)
const BATTERY_RAIL_COL = 1;                                // both battery leads use column 1

// Layout values, recomputed every frame
let pitch = 20;                      // distance between neighboring holes
let numCols = 12;
let board = { x: 0, y: 46, w: 0, h: 0 };
let battery = { x: 0, y: 0, w: 0, h: 0 };
let rowY = {};                       // y of each row: 'railTop', 'a'..'j', 'railBottom'
let narrow = false;

// State
let circuitComplete = false;
let selectedGroup = null;            // e.g. 'railTop', 'railBottom', 'top7', 'bottom7'
let flowOffset = 0;                  // distance the current dots have travelled
let mouseOverSim = false;
let lastInteraction = -100000;

let completeButton, resetButton;

function setup() {
  updateCanvasSize();
  const canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent(document.querySelector('main'));

  // Animate only while the reader is using the sim (pointer over it, or a
  // recent click), so it does not distract from the surrounding page
  const mainElement = document.querySelector('main');
  mainElement.addEventListener('mouseenter', function () { mouseOverSim = true; });
  mainElement.addEventListener('mouseleave', function () { mouseOverSim = false; });

  completeButton = createButton('Complete the Circuit');
  completeButton.parent(mainElement);
  completeButton.style('font-size', '16px');
  completeButton.position(10, drawHeight + 10);
  completeButton.mousePressed(function () {
    circuitComplete = true;
    flowOffset = 0;
    lastInteraction = millis();
    completeButton.attribute('disabled', '');
  });

  resetButton = createButton('Reset');
  resetButton.parent(mainElement);
  resetButton.style('font-size', '16px');
  resetButton.position(190, drawHeight + 10);
  resetButton.mousePressed(function () {
    circuitComplete = false;
    selectedGroup = null;
    flowOffset = 0;
    completeButton.removeAttribute('disabled');
  });

  describe('Breadboard tie points and current flow. A simplified solderless breadboard has a plus power rail along the top, a minus power rail along the bottom, and numbered columns of holes split by a center gap into rows a to e and rows f to j. A battery, a jumper wire, a resistor, and an LED are already placed. Clicking a hole highlights every hole joined to it by the same internal strip. The Complete the Circuit button adds the final jumper wire, after which moving dots show current flowing around the loop and the LED lights. A Reset button removes the final jumper.', LABEL);
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

  layout();

  // Title
  fill('black');
  noStroke();
  textStyle(NORMAL);
  textAlign(CENTER, TOP);
  textSize(canvasWidth < 520 ? 18 : 24);
  text(canvasWidth < 520 ? 'Breadboard Tie Points and Current Flow'
    : 'Breadboard Tie Points and Animated Current Flow', canvasWidth / 2, 10);

  if (circuitComplete && (mouseOverSim || millis() - lastInteraction < 15000)) {
    flowOffset += Math.min(deltaTime, 100) * 0.06;     // 60 pixels per second
  }

  drawBoard();
  drawSelectedGroup();
  if (circuitComplete) drawCurrentStrips();
  drawHoles();
  drawBattery();
  drawWires();
  if (circuitComplete) drawCurrentDots();
  drawBodies();                      // drawn last, so the dots pass through them
  drawInfoPanel();
  cursor(holeAt(mouseX, mouseY) ? HAND : ARROW);
}

// ---------------------------------------------------------------------------
// Layout
// ---------------------------------------------------------------------------
function layout() {
  narrow = canvasWidth < 600;
  battery.w = narrow ? 40 : 64;
  const gap = narrow ? 16 : 24;
  const avail = canvasWidth - margin - battery.w - gap - margin;
  pitch = Math.min(20, avail / 11.5);
  numCols = Math.max(10, Math.min(24, Math.floor(avail / pitch - 1.5)));
  board.w = (numCols + 1.5) * pitch;
  board.h = 15.6 * pitch;
  board.y = narrow ? 38 : 46;
  const groupW = battery.w + gap + board.w;
  const left = Math.max(margin, (canvasWidth - groupW) / 2);
  battery.x = left;
  board.x = left + battery.w + gap;

  rowY = {};
  rowY.railTop = board.y + 1.1 * pitch;
  let y = rowY.railTop + 1.9 * pitch;
  for (let i = 0; i < ROWS_TOP.length; i++) { rowY[ROWS_TOP[i]] = y + i * pitch; }
  y = rowY.e + 2.0 * pitch;
  for (let i = 0; i < ROWS_BOTTOM.length; i++) { rowY[ROWS_BOTTOM[i]] = y + i * pitch; }
  rowY.railBottom = rowY.j + 1.6 * pitch;

  battery.h = 5 * pitch;
  battery.y = (rowY.e + rowY.f) / 2 - battery.h / 2;
}

function colX(col) { return board.x + 1.5 * pitch + (col - 1) * pitch; }

// The tie point group a hole belongs to
function groupOf(rowName, col) {
  if (rowName === 'railTop' || rowName === 'railBottom') return rowName;
  return (ROWS_TOP.indexOf(rowName) >= 0 ? 'top' : 'bottom') + col;
}

// The hole nearest to a point, or null
function holeAt(px, py) {
  if (px < board.x || px > board.x + board.w || py < board.y || py > board.y + board.h) return null;
  const col = Math.round((px - colX(1)) / pitch) + 1;
  if (col < 1 || col > numCols) return null;
  if (Math.abs(px - colX(col)) > pitch * 0.5) return null;
  const names = Object.keys(rowY);
  for (let i = 0; i < names.length; i++) {
    if (Math.abs(py - rowY[names[i]]) <= pitch * 0.5) return { row: names[i], col: col };
  }
  return null;
}

// ---------------------------------------------------------------------------
// The board
// ---------------------------------------------------------------------------
function drawBoard() {
  fill('ivory');
  stroke('slategray');
  strokeWeight(1.5);
  rect(board.x, board.y, board.w, board.h, 8);

  // center gap
  noStroke();
  fill('gainsboro');
  const gapTop = rowY.e + pitch * 0.6;
  rect(board.x + 4, gapTop, board.w - 8, rowY.f - rowY.e - pitch * 1.2, 3);

  // rail guide lines, as printed on a real board
  strokeWeight(2);
  stroke('red');
  line(colX(1) - pitch * 0.4, rowY.railTop - pitch * 0.55, colX(numCols) + pitch * 0.4, rowY.railTop - pitch * 0.55);
  stroke('blue');
  line(colX(1) - pitch * 0.4, rowY.railBottom + pitch * 0.55, colX(numCols) + pitch * 0.4, rowY.railBottom + pitch * 0.55);

  // rail signs, row letters, column numbers
  noStroke();
  textAlign(CENTER, CENTER);
  textStyle(BOLD);
  textSize(Math.max(14, pitch * 0.8));
  fill('red');
  text('+', board.x + board.w - pitch * 0.45, rowY.railTop);
  fill('blue');
  text('−', board.x + board.w - pitch * 0.45, rowY.railBottom);
  textStyle(NORMAL);
  fill('dimgray');
  textSize(Math.max(11, pitch * 0.6));
  const letters = ROWS_TOP.concat(ROWS_BOTTOM);
  for (let i = 0; i < letters.length; i++) {
    text(letters[i], board.x + pitch * 0.6, rowY[letters[i]]);
  }
  textSize(Math.max(11, pitch * 0.6));
  for (let c = 1; c <= numCols; c++) {
    text(c, colX(c), rowY.railTop + pitch * 0.95);
  }
}

function drawHoles() {
  const names = Object.keys(rowY);
  const d = pitch * 0.42;
  for (let i = 0; i < names.length; i++) {
    for (let c = 1; c <= numCols; c++) {
      const inGroup = selectedGroup !== null && groupOf(names[i], c) === selectedGroup;
      if (inGroup) {
        fill('gold');
        stroke('darkgoldenrod');
        strokeWeight(2);
        circle(colX(c), rowY[names[i]], d + 6);
      }
      noStroke();
      fill('dimgray');
      circle(colX(c), rowY[names[i]], d);
    }
  }
}

// A band behind the selected group, standing for the metal strip under it
function drawSelectedGroup() {
  if (!selectedGroup) return;
  const pad = pitch * 0.45;
  fill(255, 215, 0, 110);
  stroke('darkgoldenrod');
  strokeWeight(1.5);
  if (selectedGroup === 'railTop' || selectedGroup === 'railBottom') {
    rect(colX(1) - pad, rowY[selectedGroup] - pad, colX(numCols) - colX(1) + 2 * pad, 2 * pad, pad);
  } else {
    const top = selectedGroup.indexOf('top') === 0;
    const col = parseInt(selectedGroup.replace(/[a-z]/g, ''), 10);
    const y1 = rowY[top ? 'a' : 'f'];
    const y2 = rowY[top ? 'e' : 'j'];
    rect(colX(col) - pad, y1 - pad, 2 * pad, y2 - y1 + 2 * pad, pad);
  }
}

// ---------------------------------------------------------------------------
// Battery and components
// ---------------------------------------------------------------------------
function drawBattery() {
  const cx = battery.x + battery.w / 2;
  // leads: red to the + rail, black to the - rail
  noFill();
  strokeWeight(3);
  stroke('red');
  line(cx, battery.y, cx, rowY.railTop);
  line(cx, rowY.railTop, colX(BATTERY_RAIL_COL), rowY.railTop);
  stroke('black');
  line(cx, battery.y + battery.h, cx, rowY.railBottom);
  line(cx, rowY.railBottom, colX(BATTERY_RAIL_COL), rowY.railBottom);

  // body
  fill('lightgray');
  stroke('dimgray');
  strokeWeight(1.5);
  rect(battery.x, battery.y, battery.w, battery.h, 6);
  fill('darkgray');
  rect(battery.x, battery.y, battery.w, battery.h * 0.22, 6);
  noStroke();
  textAlign(CENTER, CENTER);
  textStyle(BOLD);
  textSize(18);
  fill('red');
  text('+', cx, battery.y + battery.h * 0.11 + 1);
  fill('blue');
  text('−', cx, battery.y + battery.h * 0.86);
  textStyle(NORMAL);
  fill('black');
  textSize(narrow ? 11 : 14);
  text(narrow ? 'Batt.' : 'Battery', cx, battery.y + battery.h * 0.52);
}

// Jumper wires and component legs
function drawWires() {
  // jumper 1: + rail to a3
  strokeWeight(4);
  stroke('darkorange');
  line(colX(JUMPER1.railCol), rowY.railTop, colX(JUMPER1.col), rowY[JUMPER1.row]);

  // resistor legs: c3 to c7
  stroke('gray');
  strokeWeight(2.5);
  line(colX(RESISTOR.colA), rowY[RESISTOR.row], colX(RESISTOR.colB), rowY[RESISTOR.row]);

  // LED legs: anode in e7, cathode in f7, straddling the center gap
  line(colX(LED.col), rowY[LED.anodeRow], colX(LED.col), rowY[LED.cathodeRow]);

  // jumper 2, the final jumper: j7 to the - rail
  const x1 = colX(JUMPER2.col), y1 = rowY[JUMPER2.row];
  const x2 = colX(JUMPER2.railCol), y2 = rowY.railBottom;
  if (circuitComplete) {
    stroke('green');
    strokeWeight(4);
    line(x1, y1, x2, y2);
  } else {
    // where the missing jumper will go
    stroke('green');
    strokeWeight(2);
    drawingContext.setLineDash([4, 4]);
    line(x1, y1, x2, y2);
    drawingContext.setLineDash([]);
    noStroke();
    fill('darkgreen');
    textAlign(LEFT, CENTER);
    textStyle(NORMAL);
    textSize(Math.max(11, pitch * 0.62));
    text('missing jumper', x2 + pitch * 0.6, (y1 + y2) / 2 + pitch * 0.2);
  }
}

// The resistor body and the LED
function drawBodies() {
  const ry = rowY[RESISTOR.row];
  fill('tan');
  stroke('saddlebrown');
  strokeWeight(1.5);
  const bodyX = colX(RESISTOR.colA) + pitch * 0.55;
  const bodyW = colX(RESISTOR.colB) - colX(RESISTOR.colA) - pitch * 1.1;
  rect(bodyX, ry - pitch * 0.38, bodyW, pitch * 0.76, 4);
  noStroke();
  fill('black');
  textAlign(CENTER, CENTER);
  textStyle(NORMAL);
  textSize(Math.max(11, pitch * 0.6));
  text('Resistor', bodyX + bodyW / 2, ry + 1);

  // LED body, in the center gap
  const lx = colX(LED.col);
  const lcy = (rowY[LED.anodeRow] + rowY[LED.cathodeRow]) / 2;
  if (circuitComplete) {
    // glow
    noStroke();
    for (let r = 3; r >= 1; r--) {
      fill(255, 60, 60, 45);
      circle(lx, lcy, pitch * (0.9 + r * 0.5));
    }
  }
  fill(circuitComplete ? 'red' : 'rosybrown');
  stroke('darkred');
  strokeWeight(1.5);
  circle(lx, lcy, pitch * 0.95);
  noStroke();
  fill('black');
  textAlign(LEFT, CENTER);
  textSize(Math.max(11, pitch * 0.62));
  text(circuitComplete ? 'LED (lit)' : 'LED (dark)', lx + pitch * 0.9, lcy + 1);
}

// ---------------------------------------------------------------------------
// Current flow
// ---------------------------------------------------------------------------
// The closed loop that current follows, as a list of points. Segments that
// run through an internal strip of the board are marked strip: true.
function currentPath() {
  const cx = battery.x + battery.w / 2;
  return [
    { x: cx, y: battery.y },                                          // battery +
    { x: cx, y: rowY.railTop },
    { x: colX(BATTERY_RAIL_COL), y: rowY.railTop },                   // into the + rail
    { x: colX(JUMPER1.railCol), y: rowY.railTop, strip: true },       // along the + rail strip
    { x: colX(JUMPER1.col), y: rowY[JUMPER1.row] },                   // jumper 1
    { x: colX(RESISTOR.colA), y: rowY[RESISTOR.row], strip: true },   // column 3 strip
    { x: colX(RESISTOR.colB), y: rowY[RESISTOR.row] },                // resistor
    { x: colX(LED.col), y: rowY[LED.anodeRow], strip: true },         // column 7 strip, rows a-e
    { x: colX(LED.col), y: rowY[LED.cathodeRow] },                    // LED, across the gap
    { x: colX(JUMPER2.col), y: rowY[JUMPER2.row], strip: true },      // column 7 strip, rows f-j
    { x: colX(JUMPER2.railCol), y: rowY.railBottom },                 // jumper 2
    { x: colX(BATTERY_RAIL_COL), y: rowY.railBottom, strip: true },   // along the - rail strip
    { x: cx, y: rowY.railBottom },
    { x: cx, y: battery.y + battery.h }                               // battery -
  ];
}

// Show the internal strips the current runs through
function drawCurrentStrips() {
  const path = currentPath();
  stroke(255, 140, 0, 150);
  strokeWeight(pitch * 0.5);
  for (let i = 1; i < path.length; i++) {
    if (path[i].strip) line(path[i - 1].x, path[i - 1].y, path[i].x, path[i].y);
  }
}

function drawCurrentDots() {
  const path = currentPath();
  const lengths = [];
  let total = 0;
  for (let i = 1; i < path.length; i++) {
    const len = dist(path[i - 1].x, path[i - 1].y, path[i].x, path[i].y);
    lengths.push(len);
    total += len;
  }
  const spacing = 22;
  const count = Math.floor(total / spacing);
  fill('yellow');
  stroke('black');
  strokeWeight(1);
  for (let k = 0; k < count; k++) {
    let d = (k * spacing + flowOffset) % total;
    for (let i = 0; i < lengths.length; i++) {
      if (d <= lengths[i]) {
        const t = lengths[i] === 0 ? 0 : d / lengths[i];
        circle(lerp(path[i].x, path[i + 1].x, t), lerp(path[i].y, path[i + 1].y, t), 7);
        break;
      }
      d -= lengths[i];
    }
  }
}

// ---------------------------------------------------------------------------
// Info panel
// ---------------------------------------------------------------------------
function groupDescription(group) {
  if (group === 'railTop') {
    return 'the + power rail. All ' + numCols + ' holes in this rail are joined lengthwise by one strip.';
  }
  if (group === 'railBottom') {
    return 'the − power rail. All ' + numCols + ' holes in this rail are joined lengthwise by one strip.';
  }
  const top = group.indexOf('top') === 0;
  const col = parseInt(group.replace(/[a-z]/g, ''), 10);
  const where = 'column ' + col + ', rows ' + (top ? 'a to e' : 'f to j');
  if (narrow) {
    return where + '. 5 holes on one strip, not joined to the next column or across the gap.';
  }
  return where + '. These 5 holes share one strip. The holes beside them in the next column, and the holes across the center gap, are not connected to them.';
}

function drawInfoPanel() {
  const x = margin;
  const y = board.y + board.h + 8;
  const w = canvasWidth - 2 * margin;
  const h = drawHeight - y - 6;
  fill('white');
  stroke('slategray');
  strokeWeight(1);
  rect(x, y, w, h, 8);

  const size = narrow ? 13 : 15;
  const lead = narrow ? 16 : 19;
  noStroke();
  textAlign(LEFT, TOP);
  textSize(size);
  textLeading(lead);
  textStyle(NORMAL);

  // first message: the selected tie point group
  let first;
  if (selectedGroup) {
    first = 'Same tie point group: ' + groupDescription(selectedGroup);
  } else {
    first = 'Click any hole to highlight every hole joined to it under the board.';
  }
  fill('black');
  const firstH = selectedGroup ? lead * (narrow ? 3 : 2) : lead * (narrow ? 2 : 1);
  text(first, x + 10, y + 7, w - 20, firstH + 2);

  // second message: is the circuit closed?
  let second;
  if (circuitComplete) {
    fill('darkgreen');
    second = narrow ? 'Circuit closed. Current flows from battery + through the resistor and LED to battery −.'
      : 'Circuit closed. Current flows from battery +, through the resistor and the LED, and back to battery −.';
  } else {
    fill('firebrick');
    second = 'Circuit open. Nothing connects column ' + JUMPER2.col + ' (rows f to j) to the − rail, so no current flows.';
  }
  text(second, x + 10, y + 7 + firstH + 3, w - 20, h - firstH - 12);
}

// ---------------------------------------------------------------------------
// Interaction
// ---------------------------------------------------------------------------
function mousePressed() {
  lastInteraction = millis();
  if (mouseY > drawHeight) return;
  const hole = holeAt(mouseX, mouseY);
  if (hole) {
    const g = groupOf(hole.row, hole.col);
    selectedGroup = selectedGroup === g ? null : g;
  }
}

// ---------------------------------------------------------------------------
// Responsive sizing - always at the end of the file
// ---------------------------------------------------------------------------

function windowResized() {
  updateCanvasSize();
  resizeCanvas(canvasWidth, canvasHeight);
}

function updateCanvasSize() {
  const container = document.querySelector('main');
  if (container) {
    canvasWidth = Math.floor(container.getBoundingClientRect().width);
  }
}

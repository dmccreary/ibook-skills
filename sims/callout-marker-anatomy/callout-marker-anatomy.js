// Callout Marker Anatomy MicroSim
// CANVAS_HEIGHT: 450
// Shows how a stored marker coordinate, a leader line, and a label work
// together on an annotation-free illustration. Drag a numbered marker and its
// stored x and y update in the table: the picture never changes, only data.
//
// Coordinates follow the overlay data.json convention used by this book's
// callout overlay engine: x is a percentage (0-100) of the image width from
// the left edge, and y is a percentage (0-100) of the image height from the
// top edge. The illustration is a placeholder drawn with shapes, standing in
// for a generated picture. It contains no text.

// Canvas dimensions - REQUIRED structure
let canvasWidth = 400;               // Initial width (responsive)
let drawHeight = 400;                // Drawing area height
let controlHeight = 50;              // Controls area height (1 row)
let canvasHeight = drawHeight + controlHeight;
let margin = 15;                     // Margin for visual elements
let defaultTextSize = 16;

// The three callouts, as they would be stored in data.json.
// x and y are percentages of the illustration's width and height.
const DEFAULTS = [
  { id: 1, label: 'Sun', x: 78.0, y: 22.0 },
  { id: 2, label: 'Mountain', x: 38.0, y: 50.0 },
  { id: 3, label: 'Lake', x: 64.0, y: 82.0 }
];
const MARKER_COLORS = ['darkorchid', 'crimson', 'darkorange'];
const MARKER_RADIUS = 14;

let callouts = [];
let selected = 0;                    // index of the selected callout
let dragging = -1;                   // index of the marker being dragged, or -1
let hasDragged = false;              // has the reader moved any marker yet?

// Layout rectangles, recomputed every frame from the canvas width
let illus = { x: 0, y: 0, w: 0, h: 0 };   // the illustration
let labelCol = { x: 0, w: 0 };            // the label column beside it
let panel = { x: 0, y: 0, w: 0, h: 0 };   // the data table
let sidePanel = true;                     // table beside (true) or below (false)

let leaderCheckbox, resetButton;

function setup() {
  updateCanvasSize();
  const canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent(document.querySelector('main'));

  resetCallouts();

  leaderCheckbox = createCheckbox('Show leader lines', true);
  leaderCheckbox.parent(document.querySelector('main'));
  leaderCheckbox.style('font-size', '16px');
  leaderCheckbox.position(10, drawHeight + 13);

  resetButton = createButton('Reset Positions');
  resetButton.parent(document.querySelector('main'));
  resetButton.style('font-size', '16px');
  resetButton.position(190, drawHeight + 10);
  resetButton.mousePressed(function () {
    resetCallouts();
    hasDragged = false;
  });

  describe('Callout marker anatomy. A textless placeholder illustration of a sun, a mountain, and a lake has three numbered markers. Each marker is joined by a leader line to a label outside the illustration. A table shows the x and y coordinate stored for each marker as a percentage of the image width and height. Dragging a marker changes its stored coordinate in the table. A checkbox turns the leader lines on and off, and a button resets the positions.', LABEL);
}

function resetCallouts() {
  callouts = DEFAULTS.map(function (c) {
    return { id: c.id, label: c.label, x: c.x, y: c.y };
  });
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
  textSize(canvasWidth < 480 ? 20 : 24);
  text('Callout Marker Anatomy', canvasWidth / 2, 10);

  drawIllustration();
  if (leaderCheckbox.checked()) drawLeaderLines();
  drawLabels();
  drawMarkers();
  drawDataPanel();
  updateCursor();
}

// ---------------------------------------------------------------------------
// Layout
// ---------------------------------------------------------------------------
function layout() {
  const labelW = 104;
  const gap = 26;                    // room for the leader lines to run
  sidePanel = canvasWidth >= 660;
  if (sidePanel) {
    const panelW = 232;
    illus.w = Math.min(400, canvasWidth - margin - gap - labelW - 14 - panelW - margin);
    illus.h = illus.w * 0.75;
    illus.x = margin;
    illus.y = 52;
    labelCol.x = illus.x + illus.w + gap;
    labelCol.w = labelW;
    panel.x = labelCol.x + labelW + 14;
    panel.y = 52;
    panel.w = canvasWidth - panel.x - margin;
    panel.h = 300;
  } else {
    illus.h = Math.min(170, (canvasWidth - 10 - gap - labelW - 8) * 0.75);
    illus.w = illus.h / 0.75;
    const groupW = illus.w + gap + labelW;
    illus.x = Math.max(10, (canvasWidth - groupW) / 2);
    illus.y = 44;
    labelCol.x = illus.x + illus.w + gap;
    labelCol.w = labelW;
    panel.w = Math.min(canvasWidth - 20, 520);
    panel.x = (canvasWidth - panel.w) / 2;
    panel.y = illus.y + illus.h + 24;
    panel.h = drawHeight - panel.y - 8;
  }
}

// Convert a stored percentage coordinate to canvas pixels
function toPixelX(xPercent) { return illus.x + illus.w * xPercent / 100; }
function toPixelY(yPercent) { return illus.y + illus.h * yPercent / 100; }

function labelRect(index) {
  const h = 30;
  const y = illus.y + illus.h * (0.2 + 0.3 * index) - h / 2;
  return { x: labelCol.x, y: y, w: labelCol.w, h: h };
}

// ---------------------------------------------------------------------------
// The illustration: shapes only, no text (an annotation-free illustration)
// ---------------------------------------------------------------------------
function drawIllustration() {
  const x = illus.x, y = illus.y, w = illus.w, h = illus.h;
  // sky
  noStroke();
  fill('lightskyblue');
  rect(x, y, w, h);
  // ground
  fill('darkseagreen');
  rect(x, y + h * 0.62, w, h * 0.38);
  // sun
  fill('gold');
  circle(x + w * 0.78, y + h * 0.22, w * 0.17);
  // mountain with a snow cap
  fill('slategray');
  triangle(x + w * 0.38, y + h * 0.24, x + w * 0.10, y + h * 0.70, x + w * 0.66, y + h * 0.70);
  fill('white');
  triangle(x + w * 0.38, y + h * 0.24, x + w * 0.324, y + h * 0.332, x + w * 0.436, y + h * 0.332);
  // lake
  fill('steelblue');
  ellipse(x + w * 0.64, y + h * 0.82, w * 0.46, h * 0.20);
  // frame
  noFill();
  stroke('dimgray');
  strokeWeight(1.5);
  rect(x, y, w, h);

  // caption (outside the picture)
  noStroke();
  fill('dimgray');
  textStyle(ITALIC);
  textAlign(LEFT, TOP);
  textSize(sidePanel ? 15 : 13);
  text(sidePanel ? 'Illustration: the picture itself contains no text' : 'Illustration: no text in the picture',
    x, y + h + 5);
  textStyle(NORMAL);
}

// Is the stored coordinate still on the feature the label names?
function onFeature(index) {
  const px = callouts[index].x / 100;
  const py = callouts[index].y / 100;
  if (index === 0) {
    // sun: circle of diameter 0.17 of the width; the picture is 4:3
    const dx = (px - 0.78) * illus.w;
    const dy = (py - 0.22) * illus.h;
    return Math.sqrt(dx * dx + dy * dy) <= illus.w * 0.085;
  }
  if (index === 1) {
    return inTriangle(px, py, 0.38, 0.24, 0.10, 0.70, 0.66, 0.70);
  }
  const ex = (px - 0.64) / 0.23;
  const ey = (py - 0.82) / 0.10;
  return ex * ex + ey * ey <= 1;
}

function inTriangle(px, py, ax, ay, bx, by, cx, cy) {
  const d1 = (px - bx) * (ay - by) - (ax - bx) * (py - by);
  const d2 = (px - cx) * (by - cy) - (bx - cx) * (py - cy);
  const d3 = (px - ax) * (cy - ay) - (cx - ax) * (py - ay);
  const hasNeg = d1 < 0 || d2 < 0 || d3 < 0;
  const hasPos = d1 > 0 || d2 > 0 || d3 > 0;
  return !(hasNeg && hasPos);
}

// ---------------------------------------------------------------------------
// Leader lines, labels, markers
// ---------------------------------------------------------------------------
function drawLeaderLines() {
  for (let i = 0; i < callouts.length; i++) {
    const r = labelRect(i);
    stroke(MARKER_COLORS[i]);
    strokeWeight(i === selected ? 3 : 2);
    line(toPixelX(callouts[i].x), toPixelY(callouts[i].y), r.x, r.y + r.h / 2);
  }
}

function drawLabels() {
  for (let i = 0; i < callouts.length; i++) {
    const r = labelRect(i);
    fill('white');
    stroke(i === selected ? 'black' : 'slategray');
    strokeWeight(i === selected ? 2.5 : 1.5);
    rect(r.x, r.y, r.w, r.h, 6);
    noStroke();
    fill('black');
    textStyle(NORMAL);
    textAlign(CENTER, CENTER);
    textSize(16);
    text(callouts[i].label, r.x + r.w / 2, r.y + r.h / 2 + 1);
  }
}

function drawMarkers() {
  for (let i = 0; i < callouts.length; i++) {
    const mx = toPixelX(callouts[i].x);
    const my = toPixelY(callouts[i].y);
    // white ring so the marker reads on any background
    stroke(i === selected ? 'black' : 'white');
    strokeWeight(i === selected ? 3 : 2);
    fill(MARKER_COLORS[i]);
    circle(mx, my, MARKER_RADIUS * 2);
    noStroke();
    fill('white');
    textStyle(BOLD);
    textAlign(CENTER, CENTER);
    textSize(16);
    text(callouts[i].id, mx, my + 1);
  }
  textStyle(NORMAL);
}

// ---------------------------------------------------------------------------
// The data table: what is actually stored for each marker
// ---------------------------------------------------------------------------
function drawDataPanel() {
  const p = panel;
  fill('white');
  stroke('slategray');
  strokeWeight(1.5);
  rect(p.x, p.y, p.w, p.h, 8);

  const pad = 10;
  const rowH = sidePanel ? 30 : 22;
  const size = sidePanel ? 16 : 14;
  let y = p.y + (sidePanel ? 10 : 6);

  noStroke();
  fill('black');
  textAlign(LEFT, TOP);
  textStyle(BOLD);
  textSize(size);
  text('Stored in data.json', p.x + pad, y);
  y += sidePanel ? 28 : 20;

  // column positions
  const colId = p.x + pad;
  const colLabel = colId + 26;
  const colY = p.x + p.w - pad;                    // right-aligned
  const colX = colY - (sidePanel ? 64 : Math.max(64, p.w * 0.22));

  // header row
  textSize(sidePanel ? 14 : 13);
  fill('dimgray');
  text('#', colId, y);
  text('label', colLabel, y);
  textAlign(RIGHT, TOP);
  text('x', colX, y);
  text('y', colY, y);
  y += sidePanel ? 22 : 18;

  // one row per callout
  for (let i = 0; i < callouts.length; i++) {
    const c = callouts[i];
    if (i === selected) {
      fill('lemonchiffon');
      stroke('goldenrod');
      strokeWeight(1);
      rect(p.x + 4, y - 3, p.w - 8, rowH - 2, 4);
    }
    // marker swatch with its number
    noStroke();
    fill(MARKER_COLORS[i]);
    circle(colId + 8, y + rowH / 2 - 4, 18);
    fill('white');
    textStyle(BOLD);
    textAlign(CENTER, CENTER);
    textSize(12);
    text(c.id, colId + 8, y + rowH / 2 - 3);
    // label, x, y
    fill('black');
    textStyle(i === selected ? BOLD : NORMAL);
    textAlign(LEFT, CENTER);
    textSize(size);
    text(c.label, colLabel, y + rowH / 2 - 3);
    textAlign(RIGHT, CENTER);
    text(c.x.toFixed(1), colX, y + rowH / 2 - 3);
    text(c.y.toFixed(1), colY, y + rowH / 2 - 3);
    y += rowH;
  }
  textStyle(NORMAL);

  // what the numbers mean, and what just happened
  y += sidePanel ? 6 : 2;
  noStroke();
  textAlign(LEFT, TOP);
  if (sidePanel) {
    fill('dimgray');
    textSize(14);
    textLeading(18);
    text('x = percent of the image width, from the left edge. y = percent of the image height, from the top.',
      p.x + pad, y, p.w - 2 * pad, 60);
    y += 62;
  }
  const off = [];
  for (let i = 0; i < callouts.length; i++) {
    if (!onFeature(i)) off.push(callouts[i].id);
  }
  let msg;
  if (dragging >= 0) {
    fill('black');
    msg = 'The picture is not redrawn. Only marker ' + callouts[dragging].id + '\'s stored x and y change.';
  } else if (!leaderCheckbox.checked()) {
    fill('firebrick');
    msg = 'Leader lines are off. Nothing connects a label to its marker, so a reader has to guess.';
  } else if (off.length > 0) {
    fill('firebrick');
    msg = 'Marker ' + off.join(' and ') + (off.length > 1 ? ' are' : ' is') +
      ' off ' + (off.length > 1 ? 'their features' : 'its feature') +
      '. Fix the stored coordinate, not the picture.';
  } else if (!hasDragged) {
    fill('black');
    msg = sidePanel ? 'Drag a numbered marker and watch its x and y change.'
      : 'Drag a marker and watch its x and y change. x and y are percents of the image width and height.';
  } else {
    fill('darkgreen');
    msg = 'Every marker sits on its feature.';
  }
  textSize(sidePanel ? 15 : 13);
  textLeading(sidePanel ? 19 : 16);
  text(msg, p.x + pad, y, p.w - 2 * pad, p.y + p.h - y - 2);
}

// ---------------------------------------------------------------------------
// Mouse and touch interaction
// ---------------------------------------------------------------------------
function markerAt(px, py) {
  // topmost marker first
  for (let i = callouts.length - 1; i >= 0; i--) {
    const dx = px - toPixelX(callouts[i].x);
    const dy = py - toPixelY(callouts[i].y);
    if (dx * dx + dy * dy <= (MARKER_RADIUS + 4) * (MARKER_RADIUS + 4)) return i;
  }
  return -1;
}

function labelAt(px, py) {
  for (let i = 0; i < callouts.length; i++) {
    const r = labelRect(i);
    if (px >= r.x && px <= r.x + r.w && py >= r.y && py <= r.y + r.h) return i;
  }
  return -1;
}

function mousePressed() {
  const m = markerAt(mouseX, mouseY);
  if (m >= 0) {
    selected = m;
    dragging = m;
    return false;
  }
  const l = labelAt(mouseX, mouseY);
  if (l >= 0) selected = l;
}

function mouseDragged() {
  if (dragging < 0) return;
  const c = callouts[dragging];
  // the new position is stored as a percentage, rounded to one decimal place
  c.x = Math.round(constrain((mouseX - illus.x) / illus.w * 100, 0, 100) * 10) / 10;
  c.y = Math.round(constrain((mouseY - illus.y) / illus.h * 100, 0, 100) * 10) / 10;
  hasDragged = true;
  return false;                      // keep a touch drag from scrolling the page
}

function mouseReleased() {
  dragging = -1;
}

function updateCursor() {
  if (dragging >= 0) {
    cursor('grabbing');
  } else if (markerAt(mouseX, mouseY) >= 0) {
    cursor('grab');
  } else if (labelAt(mouseX, mouseY) >= 0) {
    cursor(HAND);
  } else {
    cursor(ARROW);
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

// Context Window Budget MicroSim
// CANVAS_HEIGHT: 515
// Lets a reader "spend" a fixed context-window budget by adding files to a
// single stacked bar. When the total passes the window limit, the part of the
// stack above the limit turns red: that content is unavailable to the model.
//
// All token sizes here are EXAMPLE values chosen for the exercise. They are
// not measurements, and the 50,000-token window is an example window size,
// not the limit of any real model. Real windows vary by model.

// Canvas dimensions - REQUIRED structure
let canvasWidth = 400;               // Initial width (responsive)
let drawHeight = 400;                // Drawing area height
let controlHeight = 115;             // Controls area height (3 rows)
let canvasHeight = drawHeight + controlHeight;
let margin = 20;                     // Margin for visual elements
let sliderLeftMargin = 300;          // Recomputed for narrow canvases
let defaultTextSize = 16;

// The example window size (tokens)
const WINDOW_MAX = 50000;
const HISTORY_MAX = 30000;

// The five sample items. Stacking order is bottom to top.
let items = [
  {
    name: 'System prompt', shortName: 'System', tokens: 2000, checked: true, color: 'steelblue',
    about: 'Standing instructions that set the model\'s role, rules, and tools for the whole session.'
  },
  {
    name: 'Course description', shortName: 'Course', tokens: 3500, checked: false, color: 'mediumseagreen',
    about: 'The course\'s audience, prerequisites, topics, and learning outcomes.'
  },
  {
    name: 'Learning graph JSON', shortName: 'Graph', tokens: 18000, checked: false, color: 'orange',
    about: 'Every concept in the book plus the dependency arrows between them.'
  },
  {
    name: 'One chapter draft', shortName: 'Chapter', tokens: 4500, checked: false, color: 'orchid',
    about: 'The working text of a single chapter being written or revised.'
  },
  {
    name: 'Conversation history', shortName: 'History', tokens: 10000, checked: false, color: 'sienna',
    about: 'Every earlier message and reply in this session. It grows with each turn.'
  }
];

// Bar geometry (set in layout())
const BAR_BOTTOM = 385;
const LIMIT_Y = 112;                 // y of the window limit line
let barX, barW, panelX, panelW;
let segments = [];                   // drawn segments, used for hover hit-testing

let checkboxes = [];
let historySlider;
let narrowLabels = null;             // tracks which label set the checkboxes show

function setup() {
  updateCanvasSize();
  const canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent(document.querySelector('main'));

  for (let i = 0; i < items.length; i++) {
    const cb = createCheckbox(items[i].name, items[i].checked);
    cb.parent(document.querySelector('main'));
    cb.style('font-size', '16px');
    cb.changed(function () { items[i].checked = cb.checked(); });
    checkboxes.push(cb);
  }

  historySlider = createSlider(0, HISTORY_MAX, items[4].tokens, 500);
  historySlider.parent(document.querySelector('main'));
  historySlider.attribute('aria-label', 'Conversation history size in tokens');
  historySlider.input(function () {
    // moving the slider adds conversation history to the window
    items[4].checked = true;
    checkboxes[4].checked(true);
  });

  positionControls();

  describe('Context window budget. A vertical bar represents an example context window of 50,000 tokens. Five checkboxes add sample items to the bar as stacked colored segments, and a slider sets the size of the conversation history. When the total passes the window limit, the part above the limit line turns red and a message says those items no longer fit.', LABEL);
}

function draw() {
  updateCanvasSize();
  items[4].tokens = historySlider.value();

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
  text('Context Window Budget', canvasWidth / 2, 10);

  const total = totalTokens();
  drawBar(total);
  drawTotals(total);
  drawItemList();
  drawStatus(total);
  drawHoverInfo();
  drawControlLabels();
}

function totalTokens() {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    if (items[i].checked) total += items[i].tokens;
  }
  return total;
}

function layout() {
  const narrow = canvasWidth < 560;
  barX = narrow ? 62 : 80;
  barW = narrow ? 70 : Math.min(150, canvasWidth * 0.18);
  panelX = barX + barW + (narrow ? 18 : 40);
  panelW = canvasWidth - panelX - margin;
}

function tokensToY(tokens) {
  // 0 tokens at BAR_BOTTOM, WINDOW_MAX tokens at LIMIT_Y
  return BAR_BOTTOM - (tokens / WINDOW_MAX) * (BAR_BOTTOM - LIMIT_Y);
}

function drawBar(total) {
  // Empty window frame
  fill('white');
  stroke('slategray');
  strokeWeight(1.5);
  rect(barX, LIMIT_Y, barW, BAR_BOTTOM - LIMIT_Y);

  // Axis ticks every 10,000 tokens
  textSize(13);
  textAlign(RIGHT, CENTER);
  for (let t = 0; t <= WINDOW_MAX; t += 10000) {
    const y = tokensToY(t);
    stroke('slategray');
    strokeWeight(1);
    line(barX - 5, y, barX, y);
    noStroke();
    fill('black');
    text(t === 0 ? '0' : (t / 1000) + 'k', barX - 8, y);
  }

  // Stacked segments, bottom to top
  segments = [];
  let cum = 0;
  for (let i = 0; i < items.length; i++) {
    const it = items[i];
    if (!it.checked || it.tokens === 0) continue;
    const start = cum;
    const end = cum + it.tokens;
    cum = end;
    const fitEnd = Math.min(end, WINDOW_MAX);
    // part that fits inside the window
    if (fitEnd > start) {
      const y1 = tokensToY(fitEnd);
      const y0 = tokensToY(start);
      fill(it.color);
      stroke('white');
      strokeWeight(1);
      rect(barX, y1, barW, y0 - y1);
      segments.push({ index: i, x: barX, y: y1, w: barW, h: y0 - y1, over: false });
    }
    // part past the limit: red, drawn above the limit line
    if (end > WINDOW_MAX) {
      const overStart = Math.max(start, WINDOW_MAX);
      const y1 = tokensToY(end);
      const y0 = tokensToY(overStart);
      fill('crimson');
      stroke('white');
      strokeWeight(1);
      rect(barX, y1, barW, y0 - y1);
      // diagonal hatch so "does not fit" does not rely on color alone
      stroke('white');
      strokeWeight(1.5);
      for (let hx = barX - (y0 - y1); hx < barX + barW; hx += 9) {
        const xa = Math.max(hx, barX);
        const xb = Math.min(hx + (y0 - y1), barX + barW);
        if (xb > xa) line(xa, y0 - (xa - hx), xb, y0 - (xb - hx));
      }
      segments.push({ index: i, x: barX, y: y1, w: barW, h: y0 - y1, over: true });
    }
  }

  // Window limit line
  stroke('crimson');
  strokeWeight(2);
  drawingContext.setLineDash([7, 5]);
  line(barX - 12, LIMIT_Y, barX + barW + 12, LIMIT_Y);
  drawingContext.setLineDash([]);
  noStroke();
  fill('crimson');
  textStyle(BOLD);
  textSize(13);
  textAlign(CENTER, BOTTOM);
  text(total > WINDOW_MAX ? 'Past the limit' : 'Window limit', barX + barW / 2, tokensToY(Math.max(total, WINDOW_MAX)) - 6);
  textStyle(NORMAL);
}

function drawTotals(total) {
  const over = total > WINDOW_MAX;
  noStroke();
  textAlign(LEFT, TOP);
  fill(over ? 'crimson' : 'black');
  textStyle(BOLD);
  textSize(panelW < 300 ? 18 : 24);
  text(total.toLocaleString('en-US') + ' / ' + WINDOW_MAX.toLocaleString('en-US'), panelX, 44);
  textStyle(NORMAL);
  fill('black');
  textSize(16);
  text('tokens used', panelX, panelW < 300 ? 68 : 74);
  fill('dimgray');
  textStyle(ITALIC);
  textSize(13);
  textLeading(15);
  text('example window size, real windows vary by model', panelX, panelW < 300 ? 88 : 94, panelW, 32);
  textStyle(NORMAL);
}

function drawItemList() {
  const rowH = 32;
  const top = 134;
  const compact = panelW < 300;
  let cum = 0;
  for (let i = 0; i < items.length; i++) {
    const it = items[i];
    const y = top + i * rowH;
    let cut = false;
    let cutTokens = 0;               // how much of this item is past the limit
    if (it.checked) {
      cum += it.tokens;
      cutTokens = Math.min(it.tokens, Math.max(0, cum - WINDOW_MAX));
      cut = cutTokens > 0;
    }
    // swatch
    stroke('slategray');
    strokeWeight(1);
    fill(it.checked ? it.color : 'white');
    rect(panelX, y + 4, 18, 18, 3);
    // name and size
    noStroke();
    textAlign(LEFT, CENTER);
    textSize(compact ? 14 : 16);
    fill(it.checked ? (cut ? 'crimson' : 'black') : 'gray');
    text(compact ? it.shortName : it.name, panelX + 26, y + 13);
    textAlign(RIGHT, CENTER);
    let right = it.tokens.toLocaleString('en-US');
    if (!compact) {
      if (!it.checked) right += '  not loaded';
      else if (!cut) right += '  loaded';
      else if (cutTokens >= it.tokens) right += '  does not fit';
      else right += '  (' + cutTokens.toLocaleString('en-US') + ' cut off)';
    }
    text(right, panelX + panelW, y + 13);
  }
}

function drawStatus(total) {
  const over = total > WINDOW_MAX;
  const boxY = 302;
  const boxH = BAR_BOTTOM - boxY;
  fill(over ? 'mistyrose' : 'honeydew');
  stroke(over ? 'crimson' : 'seagreen');
  strokeWeight(1.5);
  rect(panelX, boxY, panelW, boxH, 8);
  noStroke();
  fill('black');
  textAlign(LEFT, TOP);
  textSize(panelW < 300 ? 13 : 15);
  textLeading(panelW < 300 ? 16 : 19);
  let msg;
  if (over) {
    msg = 'These items no longer fit — the model cannot see them. ' +
      (total - WINDOW_MAX).toLocaleString('en-US') + ' tokens are past the limit.';
  } else {
    msg = 'Everything loaded fits. ' + (WINDOW_MAX - total).toLocaleString('en-US') +
      ' tokens of room are left for more material and the model\'s reply.';
  }
  text(msg, panelX + 10, boxY + 9, panelW - 20, boxH - 12);
}

// Infobox for the bar segment under the mouse
function drawHoverInfo() {
  let hit = null;
  for (let i = 0; i < segments.length; i++) {
    const s = segments[i];
    if (mouseX >= s.x && mouseX <= s.x + s.w && mouseY >= s.y && mouseY <= s.y + s.h) hit = s;
  }
  if (!hit) return;
  const it = items[hit.index];
  // outline the hovered segment
  noFill();
  stroke('black');
  strokeWeight(2.5);
  rect(hit.x, hit.y, hit.w, hit.h);

  const boxW = Math.min(300, canvasWidth - 20);
  const boxH = hit.over ? 118 : 100;
  const bx = constrain(mouseX + 16, 10, canvasWidth - boxW - 10);
  const by = constrain(mouseY - boxH / 2, 40, drawHeight - boxH - 8);
  fill('white');
  stroke('slategray');
  strokeWeight(1.5);
  rect(bx, by, boxW, boxH, 10);
  noStroke();
  fill('black');
  textAlign(LEFT, TOP);
  textStyle(BOLD);
  textSize(16);
  text(it.name + ': ' + it.tokens.toLocaleString('en-US') + ' tokens', bx + 12, by + 10, boxW - 24, 22);
  textStyle(NORMAL);
  textSize(14);
  textLeading(18);
  text(it.about, bx + 12, by + 36, boxW - 24, 58);
  if (hit.over) {
    fill('crimson');
    text('This part is past the limit, so the model cannot see it.', bx + 12, by + 76, boxW - 24, 40);
  }
}

function drawControlLabels() {
  fill('black');
  noStroke();
  textStyle(NORMAL);
  textAlign(LEFT, CENTER);
  textSize(defaultTextSize);
  const label = canvasWidth < 560 ? 'History: ' : 'Conversation history: ';
  text(label + historySlider.value().toLocaleString('en-US') + ' tokens', 10, drawHeight + 92);
}

// Checkbox columns and slider width follow the canvas width
function positionControls() {
  const narrow = canvasWidth < 560;
  if (narrow !== narrowLabels) {
    narrowLabels = narrow;
    for (let i = 0; i < checkboxes.length; i++) {
      const span = checkboxes[i].elt.querySelector('span');
      if (span) span.textContent = narrow ? items[i].shortName : items[i].name;
    }
  }
  const colW = (canvasWidth - 20) / 3;
  for (let i = 0; i < checkboxes.length; i++) {
    const col = i % 3;
    const row = Math.floor(i / 3);
    checkboxes[i].position(10 + col * colW, drawHeight + 10 + row * 35);
  }
  sliderLeftMargin = narrow ? 190 : 300;
  historySlider.position(sliderLeftMargin, drawHeight + 82);
  historySlider.size(canvasWidth - sliderLeftMargin - margin);
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

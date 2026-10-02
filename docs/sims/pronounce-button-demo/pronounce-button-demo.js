// Pronounce Button and Streaming Playback MicroSim
// CANVAS_HEIGHT: 500
// Select a pronounce button beside a glossary term and watch two timelines of
// the same audio clip: one delivered by streaming playback (sound starts as
// soon as the first part of the file arrives) and one that waits for the
// whole file to download before it plays. A "slow connection" checkbox makes
// the difference in time-to-first-sound much larger.
//
// This is a timing simulation only. NO SOUND IS PLAYED and nothing is
// downloaded. The clip length, connection speeds, and startup delays below
// are example values chosen so the behavior is slow enough to watch. They are
// not measurements of any text-to-speech service.

// Canvas dimensions - REQUIRED structure
let canvasWidth = 400;               // Initial width (responsive)
let drawHeight = 420;                // Drawing area height
let controlHeight = 80;              // Controls area height (2 rows)
let canvasHeight = drawHeight + controlHeight;
let margin = 20;                     // Margin for visual elements
let defaultTextSize = 16;

// The three glossary terms, each with a pronounce button
const TERMS = [
  { term: 'GraphRAG', gloss: 'Retrieval-augmented generation that draws on a knowledge graph.' },
  { term: 'idempotent', gloss: 'Running it again gives the same end state as running it once.' },
  { term: 'Schemdraw', gloss: 'A Python library that draws electrical schematics from code.' }
];

// Example timing values (see the note at the top of this file)
const CLIP_SECONDS = 4.0;            // length of the simulated audio clip
const FIRST_CHUNK = 0.25;            // seconds of audio in the first chunk
const BUFFER_RESUME = 0.4;           // audio needed before a stalled player resumes
const CONNECTIONS = {
  normal: { startDelay: 0.2, rate: 4.0 },   // rate = seconds of audio received per second
  slow: { startDelay: 0.6, rate: 0.8 }
};

// Simulation state
let activeTerm = 1;                  // index into TERMS
let running = false;
let elapsed = 0;                     // seconds since the pronounce button was selected
let slow = false;                    // connection used for the current run
let downloaded = 0;                  // seconds of audio received so far
let stream = { pos: 0, state: 'waiting', firstSound: null };   // streaming playback
let whole = { pos: 0, state: 'waiting', firstSound: null };    // download first, then play
let isExampleFrame = true;           // true until the reader starts a run

// Layout (set in layout())
let barX, barW;
const BAR_H = 22;
let streamBarY, wholeBarY;
let termRows = [];                   // hit boxes of the drawn pronounce buttons
let narrow = false;                  // true in a narrow iframe

let termButtons = [];
let slowCheckbox;

function setup() {
  updateCanvasSize();
  const canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent(document.querySelector('main'));

  for (let i = 0; i < TERMS.length; i++) {
    const b = createButton(TERMS[i].term);
    b.parent(document.querySelector('main'));
    b.style('font-size', '16px');
    b.attribute('aria-label', 'Pronounce ' + TERMS[i].term);
    b.mousePressed(function () { startRun(i); });
    termButtons.push(b);
  }

  slowCheckbox = createCheckbox('Simulate slow connection', false);
  slowCheckbox.parent(document.querySelector('main'));
  slowCheckbox.style('font-size', '16px');
  slowCheckbox.changed(function () {
    // restart the current clip so the two connections are easy to compare
    if (!isExampleFrame) startRun(activeTerm);
  });

  positionControls();
  setExampleFrame();

  describe('Pronounce button and streaming playback. Three glossary terms, GraphRAG, idempotent, and Schemdraw, each have a pronounce button. Selecting one starts a timing simulation with two progress bars for the same audio clip. On the streaming playback bar, the playback position starts moving as soon as the first part of the file arrives, while the downloaded marker runs ahead. On the download first bar, nothing plays until the whole file has arrived. A checkbox simulates a slow connection. No sound is played.', LABEL);
}

// A frozen frame shown on load: 0.9 seconds into a run on a normal connection
function setExampleFrame() {
  startRun(1);
  for (let i = 0; i < 9; i++) step(0.1);
  running = false;
  isExampleFrame = true;
}

function startRun(index) {
  activeTerm = index;
  slow = slowCheckbox.checked();
  elapsed = 0;
  downloaded = 0;
  stream = { pos: 0, state: 'waiting', firstSound: null };
  whole = { pos: 0, state: 'waiting', firstSound: null };
  running = true;
  isExampleFrame = false;
}

// Advance the timing model by dt seconds
function step(dt) {
  const c = slow ? CONNECTIONS.slow : CONNECTIONS.normal;
  elapsed += dt;

  // Download: nothing until the first chunk arrives, then a steady rate
  if (elapsed >= c.startDelay) {
    downloaded = Math.min(CLIP_SECONDS, FIRST_CHUNK + (elapsed - c.startDelay) * c.rate);
  }

  // Streaming playback: play whatever has arrived. The playback position can
  // never pass the downloaded marker; if it catches up, the player buffers.
  if (stream.state === 'waiting' && downloaded > 0) {
    stream.state = 'playing';
    stream.firstSound = c.startDelay;          // sound starts with the first chunk
    stream.pos = Math.min(elapsed - c.startDelay, downloaded);
  } else if (stream.state === 'buffering' &&
      (downloaded - stream.pos >= BUFFER_RESUME || downloaded >= CLIP_SECONDS)) {
    stream.state = 'playing';
  } else if (stream.state === 'playing') {
    stream.pos = Math.min(stream.pos + dt, downloaded);
    if (stream.pos >= CLIP_SECONDS) {
      stream.pos = CLIP_SECONDS;
      stream.state = 'done';
    } else if (stream.pos >= downloaded) {
      stream.state = 'buffering';
    }
  }

  // Download first: nothing plays until the whole file has arrived
  if (whole.state === 'waiting' && downloaded >= CLIP_SECONDS) {
    whole.state = 'playing';
    // the moment the last part of the file arrived
    whole.firstSound = c.startDelay + (CLIP_SECONDS - FIRST_CHUNK) / c.rate;
    whole.pos = Math.min(elapsed - whole.firstSound, CLIP_SECONDS);
  } else if (whole.state === 'playing') {
    whole.pos = Math.min(whole.pos + dt, CLIP_SECONDS);
    if (whole.pos >= CLIP_SECONDS) whole.state = 'done';
  }

  if (stream.state === 'done' && whole.state === 'done') running = false;
}

function draw() {
  updateCanvasSize();
  if (running) step(Math.min(deltaTime / 1000, 0.1));

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
  text('Pronounce Button and Streaming Playback', canvasWidth / 2, 10);

  const hovered = hoveredBar();
  if (!hovered) drawGlossary();
  drawStatus();
  drawTimeline(streamBarY, 'Streaming playback', stream, true);
  drawTimeline(wholeBarY, 'Download first, then play', whole, false);
  if (hovered) drawHoverInfo(hovered);
  drawControlLabels();
  updateCursor();
}

function layout() {
  narrow = canvasWidth < 620;
  barX = margin;
  barW = canvasWidth - 2 * margin;
  // each timeline needs room above the bar for its heading and the
  // "Downloaded" label, and below it for the "Playback Position" label
  streamBarY = narrow ? 232 : 258;
  wholeBarY = narrow ? 346 : 362;
}

// ---------------------------------------------------------------------------
// Glossary card: three terms, each with a pronounce button
// ---------------------------------------------------------------------------
function drawGlossary() {
  const x = margin;
  const y = 44;
  const w = canvasWidth - 2 * margin;
  const rowH = narrow ? 30 : 36;
  const bs = narrow ? 24 : 28;       // size of the speaker button
  fill('white');
  stroke('silver');
  strokeWeight(1);
  rect(x, y, w, rowH * TERMS.length + 10, 8);

  // the short definitions are shown only when all three fit inside the card
  const glossX = x + 10 + bs + 12 + 118;
  textStyle(NORMAL);
  textSize(15);
  let showGloss = !narrow;
  for (let i = 0; i < TERMS.length; i++) {
    if (glossX + textWidth(TERMS[i].gloss) > x + w - 10) showGloss = false;
  }

  termRows = [];
  for (let i = 0; i < TERMS.length; i++) {
    const ry = y + 5 + i * rowH;
    const active = i === activeTerm && (running || isExampleFrame);
    // the pronounce button: a small speaker icon
    const bx = x + 10, by = ry + (rowH - bs) / 2;
    termRows.push({ x: bx, y: by, w: bs, h: bs });
    fill(active ? 'teal' : 'white');
    stroke('teal');
    strokeWeight(2);
    rect(bx, by, bs, bs, 6);
    drawSpeaker(bx + bs / 2, by + bs / 2, active ? 'white' : 'teal');
    // the term and its short definition
    noStroke();
    fill('black');
    textAlign(LEFT, CENTER);
    textStyle(BOLD);
    textSize(18);
    text(TERMS[i].term, bx + bs + 12, ry + rowH / 2);
    if (showGloss) {
      textStyle(NORMAL);
      textSize(15);
      fill('dimgray');
      text(TERMS[i].gloss, glossX, ry + rowH / 2);
    }
  }
  textStyle(NORMAL);
}

function drawSpeaker(cx, cy, col) {
  noStroke();
  fill(col);
  // speaker body and cone
  rect(cx - 9, cy - 4, 5, 8);
  triangle(cx - 4, cy - 4, cx + 2, cy - 9, cx + 2, cy + 9);
  triangle(cx - 4, cy - 4, cx - 4, cy + 4, cx + 2, cy + 9);
  // sound waves
  noFill();
  stroke(col);
  strokeWeight(2);
  arc(cx + 3, cy, 8, 10, -QUARTER_PI, QUARTER_PI);
  arc(cx + 3, cy, 15, 18, -QUARTER_PI, QUARTER_PI);
}

// ---------------------------------------------------------------------------
// Status line and timelines
// ---------------------------------------------------------------------------
function drawStatus() {
  noStroke();
  textAlign(LEFT, TOP);
  textSize(narrow ? 14 : 16);
  fill('black');
  let msg;
  if (isExampleFrame) {
    msg = 'Example frame: 0.9 s after a pronounce button was selected. Pick a term below to run it.';
    if (narrow || textWidth(msg) > canvasWidth - 2 * margin) {
      msg = 'Example: 0.9 s after a click. Pick a term below.';
    }
  } else {
    msg = 'Clip: ' + TERMS[activeTerm].term + '   Connection: ' + (slow ? 'slow' : 'normal') +
      '   Time: ' + elapsed.toFixed(1) + ' s';
  }
  text(msg, margin, narrow ? 150 : 170);
  fill('dimgray');
  textStyle(ITALIC);
  textSize(narrow ? 12 : 14);
  text(narrow ? 'Timing simulation only: no sound is played.'
    : 'Timing simulation only: no sound is played. Times are example values.', margin, narrow ? 169 : 192);
  textStyle(NORMAL);
}

function stateText(player, isStream) {
  if (player.state === 'waiting') {
    if (isStream) return 'waiting for the first part of the file';
    return 'silent, waiting for the whole file';
  }
  if (player.state === 'playing') return 'playing';
  if (player.state === 'buffering') return 'paused, waiting for more audio';
  return 'finished';
}

function drawTimeline(y, title, player, isStream) {
  const xDown = barX + barW * downloaded / CLIP_SECONDS;
  const xPlay = barX + barW * player.pos / CLIP_SECONDS;
  const stalled = player.state === 'buffering' || (player.state === 'waiting' && !isStream);

  // heading: name on the left, time to first sound on the right
  noStroke();
  fill('black');
  textAlign(LEFT, BOTTOM);
  textStyle(BOLD);
  textSize(narrow ? 15 : 16);
  text(title, barX, y - 26);
  const titleW = textWidth(title);
  textStyle(NORMAL);
  if (!narrow) {
    // wide layout: what the player is doing right now, beside its name
    fill(stalled ? 'firebrick' : 'black');
    text(stateText(player, isStream), barX + titleW + 14, y - 26);
  }
  textAlign(RIGHT, BOTTOM);
  textSize(narrow ? 13 : 15);
  if (player.firstSound !== null) {
    fill(isStream ? 'teal' : 'firebrick');
    textStyle(BOLD);
    text((narrow ? 'First sound: ' : 'First sound after ') + player.firstSound.toFixed(1) + ' s', barX + barW, y - 26);
    textStyle(NORMAL);
  } else {
    fill('dimgray');
    text('No sound yet', barX + barW, y - 26);
  }

  // track, downloaded part, played part
  fill('white');
  stroke('slategray');
  strokeWeight(1.5);
  rect(barX, y, barW, BAR_H);
  noStroke();
  fill('lightsteelblue');
  rect(barX, y, xDown - barX, BAR_H);
  fill('teal');
  rect(barX, y, xPlay - barX, BAR_H);
  noFill();
  stroke('slategray');
  strokeWeight(1.5);
  rect(barX, y, barW, BAR_H);

  // "Downloaded" marker above the bar
  fill('steelblue');
  noStroke();
  triangle(xDown, y - 1, xDown - 6, y - 10, xDown + 6, y - 10);
  textSize(13);
  fill('midnightblue');
  const dLabel = 'Downloaded';
  const dw = textWidth(dLabel);
  textAlign(LEFT, BOTTOM);
  text(dLabel, constrain(xDown - dw / 2, barX, barX + barW - dw), y - 10);

  // "Playback Position" marker below the bar
  fill('teal');
  triangle(xPlay, y + BAR_H + 1, xPlay - 6, y + BAR_H + 10, xPlay + 6, y + BAR_H + 10);
  fill('darkslategray');
  const pLabel = 'Playback Position';
  const pw = textWidth(pLabel);
  textAlign(LEFT, TOP);
  text(pLabel, constrain(xPlay - pw / 2, barX, barX + barW - pw), y + BAR_H + 11);

  if (narrow) {
    // narrow layout: the state gets its own line under the bar
    textAlign(RIGHT, TOP);
    textSize(13);
    fill(stalled ? 'firebrick' : 'black');
    text(stateText(player, isStream), barX + barW, y + BAR_H + 27);
  }
}

// Which progress bar is under the mouse: 'stream', 'whole', or null
function hoveredBar() {
  if (mouseX < barX || mouseX > barX + barW) return null;
  if (mouseY >= streamBarY - 4 && mouseY <= streamBarY + BAR_H + 4) return 'stream';
  if (mouseY >= wholeBarY - 4 && mouseY <= wholeBarY + BAR_H + 4) return 'whole';
  return null;
}

// Infobox for the bar under the mouse. It takes the place of the glossary
// card, so it never covers the timelines the reader is looking at.
function drawHoverInfo(which) {
  const x = margin;
  const y = 44;
  const w = canvasWidth - 2 * margin;
  const h = (narrow ? 30 : 36) * TERMS.length + 10;
  fill('lightyellow');
  stroke('slategray');
  strokeWeight(1.5);
  rect(x, y, w, h, 8);
  noStroke();
  fill('black');
  textAlign(LEFT, TOP);
  textStyle(BOLD);
  textSize(narrow ? 15 : 17);
  text(which === 'stream' ? 'Streaming playback' : 'Waiting for a full download', x + 12, y + 9);
  textStyle(NORMAL);
  textSize(narrow ? 13 : 16);
  textLeading(narrow ? 16 : 21);
  const msg = which === 'stream'
    ? 'Sound begins as soon as the first part of the file arrives, while the rest is still downloading. The playback position can never pass the downloaded marker.'
    : 'Nothing plays until the downloaded marker reaches the end of the bar. The listener waits in silence for the whole file.';
  text(msg, x + 12, y + (narrow ? 29 : 34), w - 24, h - 32);

  // outline the bar being described
  const by = which === 'stream' ? streamBarY : wholeBarY;
  noFill();
  stroke('black');
  strokeWeight(2.5);
  rect(barX, by, barW, BAR_H);
}

function drawControlLabels() {
  if (canvasWidth < 480) return;     // no room for the row label in a narrow iframe
  fill('black');
  noStroke();
  textStyle(NORMAL);
  textAlign(LEFT, CENTER);
  textSize(defaultTextSize);
  text('Pronounce:', 10, drawHeight + 21);
}

// ---------------------------------------------------------------------------
// Controls and interaction
// ---------------------------------------------------------------------------
function positionControls() {
  let x = canvasWidth < 480 ? 10 : 100;
  for (let i = 0; i < termButtons.length; i++) {
    termButtons[i].position(x, drawHeight + 8);
    x += termButtons[i].elt.offsetWidth + 8;
  }
  slowCheckbox.position(10, drawHeight + 47);
}

// The drawn speaker icons work as pronounce buttons too
function termIconAt(px, py) {
  for (let i = 0; i < termRows.length; i++) {
    const r = termRows[i];
    if (px >= r.x - 3 && px <= r.x + r.w + 3 && py >= r.y - 3 && py <= r.y + r.h + 3) return i;
  }
  return -1;
}

function mousePressed() {
  if (hoveredBar()) return;          // the glossary card is hidden while a bar is described
  const i = termIconAt(mouseX, mouseY);
  if (i >= 0) startRun(i);
}

function updateCursor() {
  cursor(!hoveredBar() && termIconAt(mouseX, mouseY) >= 0 ? HAND : ARROW);
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

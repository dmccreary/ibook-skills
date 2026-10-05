// xAPI Statement Builder MicroSim
// CANVAS_HEIGHT: 550
// Build an Experience API (xAPI) statement from an actor, a verb, and an
// object, read it as a sentence, and see the JSON it produces. A toggle swaps
// the anonymous session ID for a real student name to show which field turns
// an aggregable statement into per-student data.
//
// Nothing is stored or transmitted. This is a conceptual builder only.
//
// xAPI notes that keep the JSON valid:
// - An actor needs exactly one inverse functional identifier. This sim uses
//   an "account" object (homePage + name). "objectType" is omitted because it
//   defaults to "Agent" for the actor and "Activity" for the object.
// - A verb id is an IRI. "completed" and "answered" use the ADL vocabulary
//   (http://adlnet.gov/expapi/verbs/...). "hovered" and "clicked" are not in
//   that vocabulary, so they use an IRI defined under the example.org
//   placeholder domain, which xAPI allows.
// - An activity id is an IRI. The example.org addresses are placeholders.

// Canvas dimensions - REQUIRED structure
let canvasWidth = 400;               // Initial width (responsive)
let drawHeight = 450;                // Drawing area height
let controlHeight = 100;             // Controls area height (label row + 2 rows)
let canvasHeight = drawHeight + controlHeight;
let margin = 20;                     // Margin for visual elements
let defaultTextSize = 16;

const HOME_PAGE = 'https://example.org';
const NAME_OPTION = 'Type a name...';
const SESSION_IDS = ['anonymous-session-4471', 'anonymous-session-8820'];

const VERBS = {
  completed: { iri: 'http://adlnet.gov/expapi/verbs/completed', source: 'ADL vocabulary' },
  hovered: { iri: 'https://example.org/verbs/hovered', source: 'defined by this project' },
  clicked: { iri: 'https://example.org/verbs/clicked', source: 'defined by this project' },
  answered: { iri: 'http://adlnet.gov/expapi/verbs/answered', source: 'ADL vocabulary' }
};

const OBJECTS = ['quiz-token-basics', 'diagram-node-llm', 'microsim-context-window'];

// Section geometry inside the drawing region
const SENTENCE_Y = 44;
const SENTENCE_H = 74;
const MESSAGE_Y = 124;
const MESSAGE_H = 38;
const JSON_Y = 168;
const JSON_LINE_H = 15;

// Controls
let actorSelect, verbSelect, objectSelect, realNameCheckbox, nameInput;
let lastSessionId = SESSION_IDS[0];
let narrowCheckboxLabel = null;

function setup() {
  updateCanvasSize();
  const canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent(document.querySelector('main'));
  const mainElement = document.querySelector('main');

  actorSelect = createSelect();
  actorSelect.parent(mainElement);
  SESSION_IDS.forEach(function (id) { actorSelect.option(id); });
  actorSelect.option(NAME_OPTION);
  actorSelect.selected(SESSION_IDS[0]);
  actorSelect.attribute('aria-label', 'Actor');
  actorSelect.changed(onActorChanged);

  verbSelect = createSelect();
  verbSelect.parent(mainElement);
  Object.keys(VERBS).forEach(function (v) { verbSelect.option(v); });
  verbSelect.selected('completed');
  verbSelect.attribute('aria-label', 'Verb');

  objectSelect = createSelect();
  objectSelect.parent(mainElement);
  OBJECTS.forEach(function (o) { objectSelect.option(o); });
  objectSelect.selected(OBJECTS[0]);
  objectSelect.attribute('aria-label', 'Object');

  realNameCheckbox = createCheckbox('Use real student name instead of session ID', false);
  realNameCheckbox.parent(mainElement);
  realNameCheckbox.style('font-size', '16px');
  realNameCheckbox.changed(onToggleChanged);

  nameInput = createInput('');
  nameInput.parent(mainElement);
  nameInput.attribute('placeholder', 'Type a student name');
  nameInput.attribute('maxlength', 30);
  nameInput.attribute('aria-label', 'Student name');
  nameInput.attribute('disabled', '');

  positionControls();

  describe('xAPI statement builder. Three dropdowns choose an actor, a verb, and an object. The statement is shown as a sentence and as xAPI JSON. A checkbox swaps the anonymous session ID for a typed student name, which turns the sentence red and warns that the statement now identifies a specific student.', LABEL);
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
  text('xAPI Statement Builder', canvasWidth / 2, 10);

  const st = currentStatement();
  drawSentence(st);
  drawMessage(st);
  drawJson(st);
  drawControlLabels();
}

// ---------------------------------------------------------------------------
// Statement model
// ---------------------------------------------------------------------------

function useRealName() {
  return actorSelect.value() === NAME_OPTION;
}

// Reads the controls and returns everything the drawing code needs.
function currentStatement() {
  const real = useRealName();
  const typed = nameInput.value().trim();
  const verb = verbSelect.value();
  const object = objectSelect.value();
  const st = {
    real: real,
    hasName: real && typed.length > 0,
    verb: verb,
    verbIri: VERBS[verb].iri,
    verbSource: VERBS[verb].source,
    object: object,
    objectIri: HOME_PAGE + '/activities/' + object
  };
  if (real) {
    st.actorText = typed.length > 0 ? typed : '[type a name]';
    st.personName = typed.length > 0 ? typed : '?';
    // a login-style account name derived from the typed name
    st.accountName = typed.length > 0 ? typed.toLowerCase().replace(/[^a-z0-9]+/g, '.').replace(/^\.+|\.+$/g, '') : '?';
    if (st.accountName.length === 0) st.accountName = '?';
  } else {
    st.actorText = actorSelect.value();
    st.accountName = actorSelect.value();
  }
  return st;
}

// ---------------------------------------------------------------------------
// Control handlers
// ---------------------------------------------------------------------------

function onActorChanged() {
  const real = useRealName();
  if (!real) lastSessionId = actorSelect.value();
  realNameCheckbox.checked(real);
  setNameInputEnabled(real);
}

function onToggleChanged() {
  const real = realNameCheckbox.checked();
  actorSelect.selected(real ? NAME_OPTION : lastSessionId);
  setNameInputEnabled(real);
}

function setNameInputEnabled(enabled) {
  if (enabled) {
    nameInput.removeAttribute('disabled');
    nameInput.elt.focus();
  } else {
    nameInput.attribute('disabled', '');
  }
}

// ---------------------------------------------------------------------------
// Drawing
// ---------------------------------------------------------------------------

// The assembled statement as a sentence, with each part labeled
function drawSentence(st) {
  const x0 = margin;
  const w = canvasWidth - margin * 2;
  fill('white');
  stroke('silver');
  strokeWeight(1);
  rect(x0, SENTENCE_Y, w, SENTENCE_H, 8);

  const parts = [st.actorText, st.verb, st.object];
  const labels = ['ACTOR', 'VERB', 'OBJECT'];
  const gap = 14;

  // shrink the sentence until all three parts fit on one line
  let size = 22;
  let widths, total;
  textStyle(BOLD);
  do {
    textSize(size);
    widths = parts.map(function (p) { return textWidth(p); });
    total = widths[0] + widths[1] + widths[2] + gap * 2;
    size--;
  } while (total > w - 24 && size >= 10);

  const sentenceColor = st.hasName ? 'crimson' : (st.real ? 'gray' : 'teal');
  let x = x0 + (w - total) / 2;
  const baseY = SENTENCE_Y + 26;
  for (let i = 0; i < 3; i++) {
    noStroke();
    fill(sentenceColor);
    textStyle(BOLD);
    textSize(size + 1);
    textAlign(LEFT, CENTER);
    text(parts[i], x, baseY);
    // bracket under the part
    stroke(i === 0 && st.hasName ? 'crimson' : 'slategray');
    strokeWeight(i === 0 && st.hasName ? 3 : 1.5);
    line(x, baseY + 17, x + widths[i], baseY + 17);
    // part label
    noStroke();
    fill(i === 0 && st.hasName ? 'crimson' : 'dimgray');
    textStyle(NORMAL);
    textSize(13);
    textAlign(CENTER, TOP);
    text(labels[i], x + widths[i] / 2, baseY + 23);
    x += widths[i] + gap;
  }
  textStyle(NORMAL);
}

// The safe / unsafe verdict
function drawMessage(st) {
  const x0 = margin;
  const w = canvasWidth - margin * 2;
  let msg, fillColor, strokeColor;
  if (st.hasName) {
    msg = 'This statement now identifies a specific student — outside this project\'s 2.99 design target';
    fillColor = 'mistyrose';
    strokeColor = 'crimson';
  } else if (st.real) {
    msg = 'Type a name in the box below to see what changes.';
    fillColor = 'lemonchiffon';
    strokeColor = 'goldenrod';
  } else {
    msg = 'Anonymous and aggregable — safe for concept-understanding analytics';
    fillColor = 'honeydew';
    strokeColor = 'teal';
  }
  fill(fillColor);
  stroke(strokeColor);
  strokeWeight(1.5);
  rect(x0, MESSAGE_Y, w, MESSAGE_H, 8);
  noStroke();
  fill('black');
  textAlign(CENTER, CENTER);
  let size = 16;
  textSize(size);
  // one line if it fits, otherwise wrap onto two smaller lines
  if (textWidth(msg) <= w - 20) {
    text(msg, x0 + w / 2, MESSAGE_Y + MESSAGE_H / 2);
  } else {
    textSize(13);
    textLeading(16);
    text(msg, x0 + 10, MESSAGE_Y + 3, w - 20, MESSAGE_H - 6);
  }
}

// Builds the JSON as lines of colored segments: [text, kind]
function jsonLines(st) {
  const P = 'punct', K = 'key', S = 'string', A = 'actor';
  const lines = [];
  lines.push([['{', P]]);
  lines.push([['  ', P], ['"actor"', K], [': {', P]]);
  if (st.real) {
    lines.push([['    ', P], ['"name"', K], [': ', P], [JSON.stringify(st.personName), A], [',', P]]);
  }
  lines.push([['    ', P], ['"account"', K], [': {', P]]);
  lines.push([['      ', P], ['"homePage"', K], [': ', P], ['"' + HOME_PAGE + '"', S], [',', P]]);
  lines.push([['      ', P], ['"name"', K], [': ', P], [JSON.stringify(st.accountName), A]]);
  lines.push([['    }', P]]);
  lines.push([['  },', P]]);
  lines.push([['  ', P], ['"verb"', K], [': {', P]]);
  lines.push([['    ', P], ['"id"', K], [': ', P], ['"' + st.verbIri + '"', S], [',', P]]);
  lines.push([['    ', P], ['"display"', K], [': { ', P], ['"en-US"', K], [': ', P], ['"' + st.verb + '"', S], [' }', P]]);
  lines.push([['  },', P]]);
  lines.push([['  ', P], ['"object"', K], [': {', P]]);
  lines.push([['    ', P], ['"id"', K], [': ', P], ['"' + st.objectIri + '"', S]]);
  lines.push([['  }', P]]);
  lines.push([['}', P]]);
  return lines;
}

// The statement as xAPI JSON, with the actor value highlighted
function drawJson(st) {
  const x0 = margin;
  const w = canvasWidth - margin * 2;
  const h = drawHeight - JSON_Y - 10;
  fill('white');
  stroke('silver');
  strokeWeight(1);
  rect(x0, JSON_Y, w, h, 8);

  const lines = jsonLines(st);
  const actorColor = st.hasName ? 'crimson' : (st.real ? 'gray' : 'teal');
  const colors = { punct: 'black', key: 'darkslateblue', string: 'darkgreen', actor: actorColor };

  // monospace is required here so the JSON indentation lines up
  textFont('monospace');
  textAlign(LEFT, TOP);
  noStroke();
  let longest = 0;
  lines.forEach(function (segs) {
    const len = segs.reduce(function (n, s) { return n + s[0].length; }, 0);
    longest = Math.max(longest, len);
  });
  const size = constrain((w - 28) / (longest * 0.602), 8, 14);
  textSize(size);

  const topY = JSON_Y + 9;
  let actorTop = 0, actorBottom = 0;
  for (let i = 0; i < lines.length; i++) {
    let x = x0 + 12;
    const y = topY + i * JSON_LINE_H;
    for (let s = 0; s < lines[i].length; s++) {
      const seg = lines[i][s];
      fill(colors[seg[1]]);
      textStyle(seg[1] === 'actor' ? BOLD : NORMAL);
      text(seg[0], x, y);
      x += textWidth(seg[0]);
    }
  }
  textStyle(NORMAL);
  textFont('sans-serif');

  // Callout naming the field that decides whether a person is identified.
  // The actor block always starts on line index 1 and ends on its closing brace.
  actorTop = topY + JSON_LINE_H;
  actorBottom = topY + (st.real ? 8 : 7) * JSON_LINE_H;
  const bracketX = x0 + w - 12;
  stroke(actorColor);
  strokeWeight(st.hasName ? 3 : 1.5);
  noFill();
  line(bracketX, actorTop, bracketX, actorBottom);
  line(bracketX - 6, actorTop, bracketX, actorTop);
  line(bracketX - 6, actorBottom, bracketX, actorBottom);
  noStroke();
  fill(actorColor);
  textAlign(RIGHT, CENTER);
  textSize(canvasWidth < 560 ? 12 : 14);
  textStyle(st.hasName ? BOLD : NORMAL);
  const calloutWide = st.hasName ? 'the actor field now names one student'
    : (st.real ? 'the actor field is waiting for a name' : 'the actor field holds an anonymous session ID');
  const calloutNarrow = st.hasName ? 'names one student' : (st.real ? 'needs a name' : 'anonymous');
  const callout = canvasWidth < 640 ? calloutNarrow : calloutWide;
  text(callout, bracketX - 10, actorTop + JSON_LINE_H / 2);
  textStyle(NORMAL);

  // Where the verb IRI comes from
  fill('dimgray');
  textAlign(RIGHT, BOTTOM);
  textStyle(ITALIC);
  textSize(13);
  text('Verb IRI: ' + st.verbSource, x0 + w - 12, JSON_Y + h - 6);
  textStyle(NORMAL);
}

function drawControlLabels() {
  fill('black');
  noStroke();
  textStyle(BOLD);
  textAlign(LEFT, CENTER);
  textSize(defaultTextSize);
  const cols = controlColumns();
  text('Actor', cols[0].x, drawHeight + 14);
  text('Verb', cols[1].x, drawHeight + 14);
  text('Object', cols[2].x, drawHeight + 14);
  textStyle(NORMAL);
}

// Three columns for the dropdowns: actor 40%, verb 22%, object 38%
function controlColumns() {
  const gap = 10;
  const usable = canvasWidth - 20 - gap * 2;
  const wA = Math.floor(usable * 0.40);
  const wV = Math.floor(usable * 0.22);
  const wO = usable - wA - wV;
  return [
    { x: 10, w: wA },
    { x: 10 + wA + gap, w: wV },
    { x: 10 + wA + gap + wV + gap, w: wO }
  ];
}

function positionControls() {
  const cols = controlColumns();
  const selects = [actorSelect, verbSelect, objectSelect];
  for (let i = 0; i < 3; i++) {
    selects[i].position(cols[i].x, drawHeight + 28);
    selects[i].size(cols[i].w);
  }
  const narrow = canvasWidth < 640;
  if (narrow !== narrowCheckboxLabel) {
    narrowCheckboxLabel = narrow;
    const span = realNameCheckbox.elt.querySelector('span');
    if (span) span.textContent = narrow ? 'Use real student name' : 'Use real student name instead of session ID';
  }
  realNameCheckbox.position(10, drawHeight + 66);
  const inputX = narrow ? 205 : 365;
  nameInput.position(inputX, drawHeight + 64);
  nameInput.size(Math.max(canvasWidth - inputX - margin - 8, 80));
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

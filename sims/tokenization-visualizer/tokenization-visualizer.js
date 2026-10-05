// Tokenization Visualizer MicroSim
// CANVAS_HEIGHT: 520
// Shows the same sentence two ways: split at word boundaries ("how you see it")
// and split into smaller token pieces ("how the model sees it").
//
// IMPORTANT: the splitter below is an ILLUSTRATIVE, rule-based approximation.
// It is NOT the tokenizer of any real model. Real tokenizers (for example
// byte-pair encoding) learn their vocabulary of pieces from training text and
// will split the same sentence differently. The rules here only reproduce the
// general pattern: short common words stay whole, long or unusual words break
// into several pieces, and punctuation gets its own token.

// Canvas dimensions - REQUIRED structure
let canvasWidth = 400;               // Initial width (responsive)
let drawHeight = 440;                // Drawing area height
let controlHeight = 80;              // Controls area height (2 rows)
let canvasHeight = drawHeight + controlHeight;
let margin = 20;                     // Margin for visual elements
let defaultTextSize = 16;

// Section geometry inside the drawing region
const RAW_LABEL_Y = 46;
const RAW_BOX_Y = 58;
const RAW_BOX_H = 46;
const WORD_LABEL_Y = 124;
const WORD_AREA_Y = 136;
const WORD_AREA_H = 68;              // room for 2 rows of word boxes
const TOKEN_LABEL_Y = 224;
const TOKEN_AREA_Y = 236;
const TOKEN_AREA_H = 102;            // room for 3 rows of token chips
const STATS_Y = 350;
const STATS_H = 52;
const NOTE_Y = 422;

const DEFAULT_TEXT = 'Tokenization splits text into pieces.';
const MAX_CHARS = 120;
const ANIMATION_MS = 600;            // one quick transition, not continuous

// Six pastel fills with dark text. Adjacent tokens always get different fills.
const TOKEN_COLORS = ['lightskyblue', 'khaki', 'lightgreen', 'lightsalmon', 'plum', 'paleturquoise'];

// Short, very common words that this illustrative splitter keeps whole.
const COMMON_WORDS = new Set([
  'people', 'because', 'before', 'between', 'should', 'through', 'without',
  'another', 'something', 'really', 'always', 'little', 'different', 'example',
  'important', 'question', 'answer', 'student', 'students', 'language', 'number',
  'tokens', 'together', 'sentence', 'computer', 'children', 'school', 'around',
  'things', 'however', 'against', 'during', 'might', 'world', 'still', 'every'
]);

// Word-beginning fragments this splitter peels off (longest first).
const PREFIXES = ['counter', 'under', 'inter', 'micro', 'multi', 'super', 'trans',
  'hyper', 'anti', 'over', 'semi', 'auto', 'non', 'pre', 'dis', 'mis', 'un'];

// Word-ending fragments this splitter peels off (longest first).
// "ization" becomes two pieces so the chapter's example reads Token + iz + ation.
const SUFFIXES = [
  { match: 'ization', pieces: ['iz', 'ation'] },
  { match: 'isation', pieces: ['is', 'ation'] },
  { match: 'ation', pieces: ['ation'] },
  { match: 'ition', pieces: ['ition'] },
  { match: 'ment', pieces: ['ment'] },
  { match: 'ness', pieces: ['ness'] },
  { match: 'less', pieces: ['less'] },
  { match: 'able', pieces: ['able'] },
  { match: 'ible', pieces: ['ible'] },
  { match: 'tion', pieces: ['tion'] },
  { match: 'sion', pieces: ['sion'] },
  { match: 'ing', pieces: ['ing'] },
  { match: 'ful', pieces: ['ful'] },
  { match: 'ous', pieces: ['ous'] },
  { match: 'ive', pieces: ['ive'] },
  { match: 'ity', pieces: ['ity'] },
  { match: 'ize', pieces: ['ize'] },
  { match: 'ise', pieces: ['ise'] },
  { match: 'ism', pieces: ['ism'] },
  { match: 'ist', pieces: ['ist'] },
  { match: 'ed', pieces: ['ed'] },
  { match: 'ly', pieces: ['ly'] },
  { match: 'er', pieces: ['er'] }
];

// Application state
let textInput, tokenizeButton, resetButton;
let words = [];            // [{text, isWord}] - whitespace-separated chunks (live)
let tokens = [];           // [{text, wordIndex, reason, start, len}] from last Tokenize
let tokensFresh = false;   // false while the text has changed since the last Tokenize
let animStart = -10000;    // millis() when the last Tokenize ran
let selectedToken = -1;    // index of the clicked chip, or -1
let wordRects = [];        // layout of word boxes
let tokenRects = [];       // layout of token chips
let wordFont = 18;
let tokenFont = 18;

function setup() {
  updateCanvasSize();
  const canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent(document.querySelector('main'));

  // Row 1: text input
  textInput = createInput(DEFAULT_TEXT);
  textInput.parent(document.querySelector('main'));
  textInput.attribute('maxlength', MAX_CHARS);
  textInput.attribute('aria-label', 'Sentence to tokenize, up to 120 characters');
  textInput.position(95, drawHeight + 7);
  textInput.size(canvasWidth - 95 - margin - 8);
  textInput.input(onTextChanged);
  textInput.elt.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') runTokenize();
  });

  // Row 2: buttons
  tokenizeButton = createButton('Tokenize');
  tokenizeButton.parent(document.querySelector('main'));
  tokenizeButton.position(10, drawHeight + 45);
  tokenizeButton.mousePressed(runTokenize);

  resetButton = createButton('Reset');
  resetButton.parent(document.querySelector('main'));
  resetButton.position(90, drawHeight + 45);
  resetButton.mousePressed(resetExample);

  // Start with the example sentence already tokenized (no animation on load)
  words = splitIntoWords(DEFAULT_TEXT);
  tokens = tokenizeWords(words);
  tokensFresh = true;

  describe('Tokenization visualizer. A sentence is shown as plain text, then as word boxes labeled how you see it, then as smaller colored token chips labeled how the model sees it, with a word count and a token count side by side. A text box lets you type your own sentence, and Tokenize and Reset buttons re-run the split.', LABEL);
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
  text('Tokenization Visualizer', canvasWidth / 2, 10);

  layoutBoxes();
  drawRawText();
  drawWordRow();
  drawTokenRow();
  drawStats();
  drawNote();
  drawInfoBox();
  drawControlLabels();
  updateCursor();
}

// ---------------------------------------------------------------------------
// Illustrative tokenizer
// ---------------------------------------------------------------------------

// Stage 2: split at whitespace into the word-shaped pieces a person sees.
function splitIntoWords(str) {
  const chunks = str.match(/\S+/g) || [];
  return chunks.map(function (c) {
    return { text: c, isWord: /[\p{L}\d]/u.test(c) };
  });
}

// Stage 3: split each word into token pieces using the rules described above.
function tokenizeWords(wordList) {
  const out = [];
  wordList.forEach(function (w, wordIndex) {
    // letter runs (with inner apostrophes), digit runs, or one symbol at a time
    const runs = w.text.match(/[\p{L}]+(?:['’][\p{L}]+)*|\d+|[^\s]/gu) || [];
    let offset = 0;
    runs.forEach(function (run) {
      let pieces;
      if (/^\d+$/.test(run)) {
        pieces = splitDigits(run);
      } else if (/^[\p{L}]/u.test(run)) {
        pieces = splitLetters(run);
      } else {
        pieces = [{ t: run, r: 'punct' }];
      }
      pieces.forEach(function (p) {
        out.push({ text: p.t, reason: p.r, wordIndex: wordIndex, start: offset, len: p.t.length });
        offset += p.t.length;
      });
    });
  });
  return out;
}

// Long numbers break into groups of up to three digits.
function splitDigits(run) {
  if (run.length <= 3) return [{ t: run, r: 'number' }];
  const pieces = [];
  for (let i = 0; i < run.length; i += 3) {
    pieces.push({ t: run.slice(i, i + 3), r: 'digits' });
  }
  return pieces;
}

function splitLetters(run) {
  // Contractions: keep the part after the apostrophe as its own piece
  const apos = run.search(/['’]/);
  if (apos > 0) {
    const head = splitLetters(run.slice(0, apos));
    return head.concat([{ t: run.slice(apos), r: 'contraction' }]);
  }

  const lower = run.toLowerCase();
  if (run.length <= 5 || COMMON_WORDS.has(lower)) {
    return [{ t: run, r: 'common' }];
  }

  const pieces = [];
  let rest = run;

  // 1. Peel one familiar beginning
  for (let i = 0; i < PREFIXES.length; i++) {
    const p = PREFIXES[i];
    if (lower.startsWith(p) && run.length - p.length >= 4) {
      pieces.push({ t: run.slice(0, p.length), r: 'prefix' });
      rest = run.slice(p.length);
      break;
    }
  }

  // 2. Peel one familiar ending (allowing a plural "s" after it on long words)
  const tail = [];
  let core = rest;
  let suffix = findSuffix(core.toLowerCase());
  if (!suffix && core.length > 6 && core.toLowerCase().endsWith('s')) {
    const withoutS = findSuffix(core.toLowerCase().slice(0, -1));
    if (withoutS) {
      tail.unshift({ t: core.slice(-1), r: 'suffix' });
      core = core.slice(0, -1);
      suffix = withoutS;
    }
  }
  if (suffix) {
    let end = core.length;
    for (let i = suffix.pieces.length - 1; i >= 0; i--) {
      const n = suffix.pieces[i].length;
      tail.unshift({ t: core.slice(end - n, end), r: 'suffix' });
      end -= n;
    }
    core = core.slice(0, end);
  }

  // 3. What is left is the core. A long unfamiliar core breaks into fragments.
  const foundAffix = pieces.length > 0 || tail.length > 0;
  if (core.length > 7) {
    const chunks = [];
    for (let i = 0; i < core.length; i += 4) chunks.push(core.slice(i, i + 4));
    if (chunks.length > 1 && chunks[chunks.length - 1].length === 1) {
      const last = chunks.pop();
      chunks[chunks.length - 1] += last;
    }
    chunks.forEach(function (c) { pieces.push({ t: c, r: 'chunk' }); });
  } else if (core.length > 0) {
    pieces.push({ t: core, r: foundAffix ? 'stem' : 'whole' });
  }
  return pieces.concat(tail);
}

function findSuffix(lowerWord) {
  for (let i = 0; i < SUFFIXES.length; i++) {
    const s = SUFFIXES[i];
    if (lowerWord.endsWith(s.match) && lowerWord.length - s.match.length >= 3) return s;
  }
  return null;
}

// One sentence explaining why a token split where it did.
function reasonText(tok) {
  const q = '"' + tok.text + '"';
  switch (tok.reason) {
    case 'common': return q + ' is a short or very common word, so it stays whole as a single token.';
    case 'whole': return q + ' has no familiar beginning or ending to peel off, so it stays whole.';
    case 'stem': return q + ' is the familiar core left after the word\'s beginning or ending split off.';
    case 'prefix': return q + ' split off because it is a common word-beginning fragment seen often in training text.';
    case 'suffix': return q + ' split off because it is a common word-ending fragment seen often in training text.';
    case 'chunk': return q + ' is part of a long, unfamiliar stretch of letters, which breaks into short fragments.';
    case 'contraction': return q + ' is the tail of a contraction, which usually splits from the word in front of it.';
    case 'number': return q + ' is a short number, so it stays together as one token.';
    case 'digits': return q + ' is one group of digits; long numbers break into several short groups.';
    default: return 'Punctuation and symbols such as ' + q + ' are usually tokens of their own.';
  }
}

// ---------------------------------------------------------------------------
// Control handlers
// ---------------------------------------------------------------------------

function onTextChanged() {
  // Word split updates live; token split waits for the Tokenize button
  words = splitIntoWords(textInput.value());
  tokensFresh = false;
  selectedToken = -1;
}

function runTokenize() {
  words = splitIntoWords(textInput.value());
  tokens = tokenizeWords(words);
  tokensFresh = true;
  selectedToken = -1;
  animStart = millis();
}

function resetExample() {
  textInput.value(DEFAULT_TEXT);
  runTokenize();
}

function mousePressed() {
  if (mouseY < 0 || mouseY > drawHeight || mouseX < 0 || mouseX > canvasWidth) return;
  selectedToken = tokensFresh ? chipAt(mouseX, mouseY) : -1;
}

function chipAt(mx, my) {
  if (animationProgress() < 1) return -1;
  for (let i = 0; i < tokenRects.length; i++) {
    const r = tokenRects[i];
    if (mx >= r.x && mx <= r.x + r.w && my >= r.y && my <= r.y + r.h) return i;
  }
  return -1;
}

function updateCursor() {
  if (tokensFresh && mouseY < drawHeight && chipAt(mouseX, mouseY) >= 0) cursor(HAND);
  else cursor(ARROW);
}

function animationProgress() {
  return constrain((millis() - animStart) / ANIMATION_MS, 0, 1);
}

// ---------------------------------------------------------------------------
// Layout
// ---------------------------------------------------------------------------

// Flow items left to right, wrapping to new rows. groupOf(i) gives a group id;
// items in the same group sit close together (fragments of one word).
function flowLayout(items, areaY, areaH, maxRows, groupOf) {
  const sizes = [18, 16, 14, 13, 12];
  const x0 = margin;
  const maxX = canvasWidth - margin;
  let result = null;
  for (let s = 0; s < sizes.length; s++) {
    result = flowAtSize(items, sizes[s], x0, maxX, groupOf);
    if (result.rows <= maxRows) break;
  }
  // Rows are spread evenly; if even the smallest font overflows, rows get shorter
  const rowH = Math.min(34, Math.floor(areaH / Math.max(result.rows, 1)));
  result.rects.forEach(function (r) {
    r.y = areaY + r.row * rowH;
    r.h = rowH - 6;
  });
  return result;
}

function flowAtSize(items, fontSize, x0, maxX, groupOf) {
  textSize(fontSize);
  textStyle(NORMAL);
  const padX = fontSize >= 16 ? 8 : 5;
  const rects = [];
  let x = x0;
  let row = 0;
  for (let i = 0; i < items.length; i++) {
    const w = Math.min(textWidth(items[i].text) + padX * 2, maxX - x0);
    const sameGroup = i > 0 && groupOf(i) === groupOf(i - 1);
    const gap = i === 0 ? 0 : (sameGroup ? 3 : 12);
    if (x + gap + w > maxX && x > x0) {
      row++;
      x = x0;
    } else {
      x += gap;
    }
    rects.push({ x: x, w: w, row: row });
    x += w;
  }
  return { rects: rects, rows: row + 1, fontSize: fontSize };
}

function layoutBoxes() {
  const wl = flowLayout(words, WORD_AREA_Y, WORD_AREA_H, 2, function (i) { return i; });
  wordRects = wl.rects;
  wordFont = wl.fontSize;
  const tl = flowLayout(tokens, TOKEN_AREA_Y, TOKEN_AREA_H, 3, function (i) { return tokens[i].wordIndex; });
  tokenRects = tl.rects;
  tokenFont = tl.fontSize;
}

// ---------------------------------------------------------------------------
// Drawing
// ---------------------------------------------------------------------------

function sectionLabel(label, y) {
  fill('black');
  noStroke();
  textStyle(BOLD);
  textAlign(LEFT, BOTTOM);
  textSize(16);
  text(label, margin, y + 8);
  textStyle(NORMAL);
}

// Stage 1: the raw sentence as plain text
function drawRawText() {
  sectionLabel('1. The text you typed', RAW_LABEL_Y);
  fill('white');
  stroke('silver');
  strokeWeight(1);
  rect(margin, RAW_BOX_Y, canvasWidth - margin * 2, RAW_BOX_H, 6);
  noStroke();
  const raw = textInput.value();
  textAlign(LEFT, CENTER);
  if (raw.trim().length === 0) {
    fill('gray');
    textStyle(ITALIC);
    textSize(16);
    text('Type a sentence in the box below.', margin + 10, RAW_BOX_Y + RAW_BOX_H / 2);
    textStyle(NORMAL);
    return;
  }
  fill('black');
  // one line if it fits at 14px or larger; otherwise wrap onto two lines
  const boxW = canvasWidth - margin * 2 - 20;
  let size = 18;
  textSize(size);
  while (size > 14 && textWidth(raw) > boxW) {
    size--;
    textSize(size);
  }
  if (textWidth(raw) <= boxW) {
    text(raw, margin + 10, RAW_BOX_Y + RAW_BOX_H / 2);
  } else {
    while (size > 11 && textWidth(raw) > boxW * 1.8) {
      size--;
      textSize(size);
    }
    textAlign(LEFT, TOP);
    textLeading(size + 4);
    text(raw, margin + 10, RAW_BOX_Y + 5, boxW, RAW_BOX_H - 6);
  }
}

// Stage 2: word-shaped boxes
function drawWordRow() {
  const count = words.filter(function (w) { return w.isWord; }).length;
  sectionLabel('2. How you see it: ' + count + (count === 1 ? ' word' : ' words'), WORD_LABEL_Y);
  textSize(wordFont);
  textAlign(CENTER, CENTER);
  for (let i = 0; i < words.length; i++) {
    const r = wordRects[i];
    fill('white');
    stroke('slategray');
    strokeWeight(1.5);
    rect(r.x, r.y, r.w, r.h, 6);
    noStroke();
    fill('black');
    text(words[i].text, r.x + r.w / 2, r.y + r.h / 2);
  }
}

// Stage 3: token chips, morphing out of the word boxes on Tokenize
function drawTokenRow() {
  if (!tokensFresh) {
    sectionLabel('3. How the model sees it: ? tokens', TOKEN_LABEL_Y);
    fill('white');
    stroke('silver');
    strokeWeight(1);
    rect(margin, TOKEN_AREA_Y, canvasWidth - margin * 2, 60, 6);
    noStroke();
    fill('dimgray');
    textStyle(ITALIC);
    textAlign(LEFT, CENTER);
    textSize(16);
    text('Predict the number of tokens, then press Tokenize to check.',
      margin + 10, TOKEN_AREA_Y + 4, canvasWidth - margin * 2 - 20, 52);
    textStyle(NORMAL);
    return;
  }

  sectionLabel('3. How the model sees it: ' + tokens.length + (tokens.length === 1 ? ' token' : ' tokens'), TOKEN_LABEL_Y);
  const raw = animationProgress();
  const t = raw * raw * (3 - 2 * raw);  // smoothstep easing
  textSize(tokenFont);
  textAlign(CENTER, CENTER);
  for (let i = 0; i < tokens.length; i++) {
    const tok = tokens[i];
    const end = tokenRects[i];
    const wr = wordRects[tok.wordIndex];
    let x = end.x, y = end.y, w = end.w, h = end.h;
    if (t < 1 && wr) {
      // start as a slice of the parent word box, end as a separate chip
      const wordLen = Math.max(words[tok.wordIndex].text.length, 1);
      const sx = wr.x + wr.w * (tok.start / wordLen);
      const sw = wr.w * (tok.len / wordLen);
      x = lerp(sx, end.x, t);
      y = lerp(wr.y, end.y, t);
      w = lerp(sw, end.w, t);
      h = lerp(wr.h, end.h, t);
    }
    const chipColor = lerpColor(color('white'), color(TOKEN_COLORS[i % TOKEN_COLORS.length]), t);
    fill(chipColor);
    if (i === selectedToken) {
      stroke('black');
      strokeWeight(3);
    } else {
      stroke('slategray');
      strokeWeight(1);
    }
    rect(x, y, w, h, 6);
    noStroke();
    fill('black');
    text(tok.text, x + w / 2, y + h / 2);
  }
}

// Final: word count and token count side by side
function drawStats() {
  const wordCount = words.filter(function (w) { return w.isWord; }).length;
  const tokenCount = tokensFresh ? String(tokens.length) : '?';
  const ratio = (tokensFresh && wordCount > 0) ? (tokens.length / wordCount).toFixed(1) : '?';
  const labels = ['Words', 'Tokens', 'Tokens per word'];
  const values = [String(wordCount), tokenCount, ratio];
  const fills = ['white', 'lemonchiffon', 'white'];
  const gap = 10;
  const boxW = (canvasWidth - margin * 2 - gap * 2) / 3;
  for (let i = 0; i < 3; i++) {
    const x = margin + i * (boxW + gap);
    fill(fills[i]);
    stroke('silver');
    strokeWeight(1);
    rect(x, STATS_Y, boxW, STATS_H, 8);
    noStroke();
    fill('black');
    textAlign(CENTER, CENTER);
    textSize(canvasWidth < 480 ? 13 : 15);
    text(labels[i], x + boxW / 2, STATS_Y + 14);
    textStyle(BOLD);
    textSize(22);
    text(values[i], x + boxW / 2, STATS_Y + 36);
    textStyle(NORMAL);
  }
}

function drawNote() {
  fill('dimgray');
  noStroke();
  textStyle(ITALIC);
  textAlign(CENTER, CENTER);
  const full = 'Illustrative rule-based split, not a real model\'s tokenizer. Cost and capacity follow the token count.';
  const short = 'Illustrative split, not a real model\'s tokenizer.';
  textSize(14);
  const msg = textWidth(full) <= canvasWidth - margin * 2 ? full : short;
  if (textWidth(msg) > canvasWidth - margin * 2) textSize(12);
  text(msg, canvasWidth / 2, NOTE_Y);
  textStyle(NORMAL);
}

// Infobox for the clicked chip, drawn above the chip when there is room
function drawInfoBox() {
  if (!tokensFresh || selectedToken < 0 || selectedToken >= tokens.length) return;
  const tok = tokens[selectedToken];
  const r = tokenRects[selectedToken];
  const boxW = Math.min(380, canvasWidth - 20);
  const boxH = 116;
  let bx = constrain(r.x + r.w / 2 - boxW / 2, 10, canvasWidth - boxW - 10);
  let by = r.y - boxH - 8;
  if (by < 40) by = r.y + r.h + 8;

  fill('white');
  stroke('slategray');
  strokeWeight(1.5);
  rect(bx, by, boxW, boxH, 10);
  noStroke();
  fill('black');
  textAlign(LEFT, TOP);
  textStyle(BOLD);
  textSize(16);
  text('Token ' + (selectedToken + 1) + ' of ' + tokens.length + ':  "' + tok.text + '"', bx + 12, by + 10);
  textStyle(NORMAL);
  textSize(14);
  fill('dimgray');
  text('Position index ' + selectedToken + ', from the word "' + words[tok.wordIndex].text + '"', bx + 12, by + 33, boxW - 24, 20);
  fill('black');
  textLeading(18);
  text(reasonText(tok), bx + 12, by + 55, boxW - 24, boxH - 60);
}

function drawControlLabels() {
  fill('black');
  noStroke();
  textStyle(NORMAL);
  textAlign(LEFT, CENTER);
  textSize(defaultTextSize);
  text('Your text:', 10, drawHeight + 20);
  const hintX = 160;
  const hint = canvasWidth - hintX - margin > 330
    ? 'Click any token chip to see why it split there.'
    : (canvasWidth - hintX - margin > 190 ? 'Click a chip for details.' : '');
  fill('dimgray');
  text(hint, hintX, drawHeight + 57);
}

// ---------------------------------------------------------------------------
// Responsive sizing - always at the end of the file
// ---------------------------------------------------------------------------

function windowResized() {
  updateCanvasSize();
  resizeCanvas(canvasWidth, canvasHeight);
  textInput.size(canvasWidth - 95 - margin - 8);
}

function updateCanvasSize() {
  const container = document.querySelector('main');
  if (container) {
    canvasWidth = Math.floor(container.getBoundingClientRect().width);
  }
}

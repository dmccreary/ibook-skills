// From Hook to Dashboard - Mermaid flowchart with click-to-inspect nodes
// CANVAS_HEIGHT: 390
// Follows one skill-run event from the moment a skill runs, through the two
// hooks that record it, into an append-only JSONL log, through the analytics
// script, and out as one row of a token usage dashboard.
// Every node has a Mermaid `click` directive wired to showInfo(), which fills
// the shared infobox panel below the diagram. Previous / Next buttons step
// through the six stages in order so the reader can watch the same event
// change form at each stage.
//
// The sample values (skill name, timestamps, 154 seconds, 84,200 tokens, and
// the 5-run totals) are the example values used in this library's own skill
// tracker documentation. They are examples, not measurements of your project.

// ---------------------------------------------------------------------------
// Diagram definition (left-to-right Mermaid flowchart)
// Edge order: 0 Run-->UsageHook, 1 UsageHook-->StopHook, 2 StopHook-->Log,
//             3 Log-->Analytics, 4 Analytics-->Dashboard
// ---------------------------------------------------------------------------
const DIAGRAM = `flowchart LR
    Run("Skill<br/>Runs"):::process
    UsageHook("Skill Usage<br/>Hook"):::process
    StopHook("Stop Hook<br/>Fires"):::process
    Log["JSONL Usage Log<br/>(append one line)"]:::logFile
    Analytics["Skill Usage Analytics<br/>(Python script)"]:::process
    Dashboard("Token Usage<br/>Dashboard"):::dashboard

    Run --> UsageHook
    UsageHook --> StopHook
    StopHook --> Log
    Log --> Analytics
    Analytics --> Dashboard

    click Run call showInfo("Run")
    click UsageHook call showInfo("UsageHook")
    click StopHook call showInfo("StopHook")
    click Log call showInfo("Log")
    click Analytics call showInfo("Analytics")
    click Dashboard call showInfo("Dashboard")

    classDef process fill:#b2dfdb,stroke:#00695c,stroke-width:2px,color:#0b2e2a,font-size:18px
    classDef logFile fill:#fff8e1,stroke:#8a5a00,stroke-width:2px,color:#3b2600,font-size:18px
    classDef dashboard fill:#00695c,stroke:#003d33,stroke-width:3px,color:#ffffff,font-size:18px

    linkStyle default stroke:#455a64,stroke-width:2px
`;

// ---------------------------------------------------------------------------
// Infobox content, in pipeline order. Definitions follow this book's glossary.
// "data" is what the one example event looks like at that stage.
// ---------------------------------------------------------------------------
const STAGES = [
  {
    id: 'Run',
    title: 'Skill Runs',
    definition: 'The event that starts everything: an agent runs one skill to do one job.',
    here: 'Nothing has been recorded yet. Without a hook, this run would leave no trace of what it cost.',
    dataLabel: 'The event',
    data: 'skill: learning-graph-generator'
  },
  {
    id: 'UsageHook',
    title: 'Skill Usage Hook',
    definition: 'A configured callback that records information each time a skill runs, producing data for later analysis.',
    here: 'The hook notes which skill started and when. It runs automatically, so nobody has to remember to log anything.',
    dataLabel: 'What the hook records',
    data: 'skill:     learning-graph-generator\nevent:     start\ntimestamp: 2025-11-22 14:23:46'
  },
  {
    id: 'StopHook',
    title: 'Stop Hook Fires',
    definition: 'A stop hook is a callback that fires when an agent finishes a turn, commonly used to record results or perform cleanup.',
    here: 'The work is done, so the result can be recorded: how long the run took and how many tokens it consumed.',
    dataLabel: 'What is known at the end',
    data: 'event:            end\nduration_seconds: 154\ntotal_tokens:     84200'
  },
  {
    id: 'Log',
    title: 'JSONL Usage Log (append one line)',
    definition: 'An append-only file with one structured record per line, used to accumulate usage events without rewriting earlier entries.',
    here: 'The event becomes one new line at the end of the file. This box is storage, not computation: nothing is calculated here.',
    dataLabel: 'The line that is appended',
    data: '{"timestamp": "2025-11-22 14:26:20",\n "skill": "learning-graph-generator",\n "event": "end", "duration_seconds": "154",\n "total_tokens": 84200}'
  },
  {
    id: 'Analytics',
    title: 'Skill Usage Analytics (Python script)',
    definition: 'Processing recorded usage events to reveal which skills run most often and what each consumes.',
    here: 'A script reads every line of the log and groups the lines by skill. This is deterministic work, so a program does it, not the model.',
    dataLabel: 'After grouping by skill',
    data: 'learning-graph-generator\n  runs:         5\n  total tokens: 420.5K\n  average time: 2m 34s'
  },
  {
    id: 'Dashboard',
    title: 'Token Usage Dashboard',
    definition: 'A generated report that presents consumption and duration per skill so expensive steps can be identified.',
    here: 'The dashboard also reports <b>elapsed time</b> next to the token counts. The two are recorded separately, because a step can be slow without being expensive, or expensive without being slow.',
    dataLabel: 'One row of the dashboard',
    data: 'Skill:    learning-graph-generator\nRuns:     5x\nTokens:   420.5K   (what it costs)\nAvg time: 2m 34s   (how long it takes)'
  }
];

const STAGE_INDEX = {};
STAGES.forEach(function (s, i) { STAGE_INDEX[s.id] = i; });

let currentStep = -1;   // -1 = overview, 0..5 = a stage

// ---------------------------------------------------------------------------
// Infobox rendering
// ---------------------------------------------------------------------------
function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function renderOverview() {
  document.getElementById('infobox').innerHTML =
    '<div class="info-text">' +
    '<h2>One event, six stages</h2>' +
    '<p>A skill run is invisible unless something records it. Two hooks capture the run, one line is appended to a log file, a Python script reads the log, and the result appears on a dashboard.</p>' +
    '<p><span class="label">Try it: </span>Select <b>Next</b> to follow one example event from left to right, or click any box.</p>' +
    '</div>' +
    '<div class="data-panel"><div class="data-label">Example event used on this page</div>' +
    '<pre>One run of the\nlearning-graph-generator skill\n(example values, not measurements)</pre></div>';
}

function renderStage(index) {
  const s = STAGES[index];
  document.getElementById('infobox').innerHTML =
    '<div class="info-text">' +
    '<h2>' + (index + 1) + '. ' + s.title + '</h2>' +
    '<p>' + s.definition + '</p>' +
    '<p><span class="label">At this stage: </span>' + s.here + '</p>' +
    '</div>' +
    '<div class="data-panel' + (s.id === 'Log' ? ' file' : '') + '">' +
    '<div class="data-label">' + s.dataLabel + '</div>' +
    '<pre>' + escapeHtml(s.data) + '</pre></div>';
}

// ---------------------------------------------------------------------------
// Diagram highlighting
// ---------------------------------------------------------------------------
function nodeElement(nodeId) {
  return document.querySelector('#diagram [id^="flowchart-' + nodeId + '-"]');
}

// Stages the event has not reached yet are dimmed; the current one gets a halo.
function select(index) {
  currentStep = index;
  STAGES.forEach(function (s, i) {
    const el = nodeElement(s.id);
    if (!el) return;
    el.classList.toggle('selected', i === index);
    el.classList.toggle('dimmed', index >= 0 && i > index);
  });
  document.querySelectorAll('#diagram path.flowchart-link').forEach(function (p, i) {
    const travelled = index >= 0 && i < index;
    p.classList.toggle('dimmed', index >= 0 && !travelled);
    p.style.setProperty('stroke', travelled ? '#00695c' : '#455a64', 'important');
    p.style.setProperty('stroke-width', travelled ? '4px' : '2px', 'important');
  });
  if (index < 0) renderOverview(); else renderStage(index);
  document.getElementById('stepLabel').textContent =
    index < 0 ? 'Overview' : 'Stage ' + (index + 1) + ' of ' + STAGES.length;
  document.getElementById('prevButton').disabled = index < 0;
  document.getElementById('nextButton').disabled = index >= STAGES.length - 1;
}

// Called by the Mermaid `click` directives, so it must be global.
window.showInfo = function (nodeId) {
  if (STAGE_INDEX[nodeId] === undefined) return;
  select(STAGE_INDEX[nodeId]);
};

// Redraw the log node as a sheet of paper with a folded corner, so that it
// reads as a stored file rather than as a processing step.
function drawFoldedCorner() {
  const node = nodeElement('Log');
  if (!node) return;
  const rect = node.querySelector('rect');
  if (!rect) return;
  const x = parseFloat(rect.getAttribute('x'));
  const y = parseFloat(rect.getAttribute('y'));
  const w = parseFloat(rect.getAttribute('width'));
  const h = parseFloat(rect.getAttribute('height'));
  if ([x, y, w, h].some(isNaN)) return;
  const f = 10;   // size of the fold
  const ns = 'http://www.w3.org/2000/svg';
  const sheet = document.createElementNS(ns, 'path');
  sheet.setAttribute('d', 'M' + x + ',' + y + ' H' + (x + w - f) + ' L' + (x + w) + ',' + (y + f) +
    ' V' + (y + h) + ' H' + x + ' Z');
  sheet.setAttribute('class', rect.getAttribute('class') || '');
  sheet.setAttribute('style', rect.getAttribute('style') || '');
  const fold = document.createElementNS(ns, 'path');
  fold.setAttribute('d', 'M' + (x + w - f) + ',' + y + ' V' + (y + f) + ' H' + (x + w) + ' Z');
  fold.setAttribute('style', 'fill:#ffd54f;stroke:#8a5a00;stroke-width:2px;stroke-linejoin:round');
  rect.parentNode.insertBefore(sheet, rect);
  rect.parentNode.insertBefore(fold, rect);
  rect.parentNode.removeChild(rect);
}

// ---------------------------------------------------------------------------
// Startup
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', async function () {
  document.getElementById('prevButton').addEventListener('click', function () {
    if (currentStep >= 0) select(currentStep - 1);
  });
  document.getElementById('nextButton').addEventListener('click', function () {
    if (currentStep < STAGES.length - 1) select(currentStep + 1);
  });
  renderOverview();

  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'loose',   // required for click callbacks
    theme: 'default',
    flowchart: {
      useMaxWidth: true,
      htmlLabels: true,
      curve: 'basis',
      nodeSpacing: 20,
      rankSpacing: 34,
      padding: 10
    }
  });

  const container = document.getElementById('diagram');
  try {
    const result = await mermaid.render('hookToDashboardSvg', DIAGRAM);
    container.innerHTML = result.svg;
    if (result.bindFunctions) result.bindFunctions(container);
  } catch (err) {
    container.textContent = 'The diagram could not be drawn: ' + err.message;
    return;
  }

  const svg = container.querySelector('svg');
  if (svg) {
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Flowchart, left to right: Skill Runs, then Skill Usage Hook, then Stop Hook Fires, then JSONL Usage Log where one line is appended, then Skill Usage Analytics, a Python script, then Token Usage Dashboard.');
  }
  drawFoldedCorner();

  // Keyboard access: every node can be focused and activated with Enter or Space
  STAGES.forEach(function (s) {
    const el = nodeElement(s.id);
    if (!el) return;
    el.setAttribute('tabindex', '0');
    el.setAttribute('role', 'button');
    el.setAttribute('aria-label', s.title + ': show details');
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        window.showInfo(s.id);
      }
    });
  });

  select(-1);
});

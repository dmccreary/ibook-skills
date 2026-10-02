// MicroSim Library Routing Table - Mermaid flowchart with a routing exercise
// CANVAS_HEIGHT: 500
// Shows how the microsim-generator meta-skill routes a request to one of
// several visualization libraries by the trigger keywords in the request.
// The reader is given a request and applies the routing table: click the
// library the request should be routed to and get immediate feedback.
// Every node has a Mermaid `click` directive wired to showInfo(), which fills
// the shared infobox panel below the diagram.
//
// The trigger keywords are the real keywords for these six rows of the
// routing table in the microsim-generator skill. The skill has more routes
// than the six shown here, and it weighs a request with more judgment than
// the plain keyword count used in this exercise.

// ---------------------------------------------------------------------------
// Six rows of the routing table (order matches the Generator --> library edges)
// ---------------------------------------------------------------------------
const LIBRARIES = [
  {
    id: 'LibP5', name: 'p5.js', edgeLabel: 'simulation, physics',
    keywords: ['custom', 'simulation', 'physics', 'interactive', 'bouncing', 'movement', 'p5.js'],
    bestFor: 'Custom simulations, physics, and animation drawn on a canvas, with sliders and buttons to control them.',
    example: 'A bouncing ball whose speed is set by a slider, the generator\'s own "Hello World" example.'
  },
  {
    id: 'LibChart', name: 'Chart.js', edgeLabel: 'chart, bar, pie',
    keywords: ['chart', 'bar', 'line', 'pie', 'doughnut', 'radar', 'statistics', 'data'],
    bestFor: 'Standard charts made from structured values: bar, line, pie, doughnut, and radar.',
    example: 'The <i>Taxonomy Distribution Pie Chart</i> in this book.'
  },
  {
    id: 'LibNetwork', name: 'vis-network', edgeLabel: 'nodes, edges',
    keywords: ['network', 'nodes', 'edges', 'graph', 'dependencies', 'concept map', 'knowledge graph'],
    bestFor: 'Network graphs made of nodes and edges, such as dependency graphs and concept maps.',
    example: 'The <i>Learning Graph Viewer</i> in this book.'
  },
  {
    id: 'LibTimeline', name: 'vis-timeline', edgeLabel: 'dates, chronological',
    keywords: ['timeline', 'dates', 'chronological', 'events', 'history', 'schedule', 'milestones'],
    bestFor: 'Dated events laid out along a horizontal time axis that the reader can scroll and zoom.',
    example: 'The <i>Evolution of AI Approaches Timeline</i> in this book.'
  },
  {
    id: 'LibLeaflet', name: 'Leaflet', edgeLabel: 'geographic, coordinates',
    keywords: ['map', 'geographic', 'coordinates', 'latitude', 'longitude', 'locations', 'markers'],
    bestFor: 'Interactive geographic maps with markers and layers.',
    example: 'The <i>Major World Cities</i> map in this book.'
  },
  {
    id: 'LibMermaid', name: 'Mermaid', edgeLabel: 'flowchart, workflow',
    keywords: ['flowchart', 'workflow', 'process', 'state machine', 'UML', 'sequence diagram'],
    bestFor: 'Flowcharts, workflows, and other process diagrams written as text.',
    example: 'This diagram, and the <i>Book Build Workflow</i> in this book.'
  }
];

// Practice requests. "answer" is an index into LIBRARIES, or -1 for the
// ambiguous request that matches two rows equally.
const REQUESTS = [
  { text: 'Show the dates of key events in computer history in chronological order', answer: 3 },
  { text: 'Build a physics simulation of a bouncing ball', answer: 0 },
  { text: 'Mark the locations of five campuses using their latitude and longitude', answer: 4 },
  { text: 'Compare quiz scores for four classes in a bar chart', answer: 1 },
  { text: 'Make a flowchart of the chapter review workflow', answer: 5 },
  { text: 'Draw the nodes and edges of the concept dependencies in our learning graph', answer: 2 },
  { text: 'Create a graph of our sales data', answer: -1 }
];

// ---------------------------------------------------------------------------
// Diagram definition (left-to-right Mermaid flowchart)
// Edge order: 0 Request-->Generator, 1..6 Generator-->libraries
// ---------------------------------------------------------------------------
const DIAGRAM = `flowchart LR
    Request("Incoming<br/>Request"):::request
    Generator("MicroSim Generator<br/>(Meta-Skill)"):::generator
${LIBRARIES.map(function (g) { return '    ' + g.id + '("' + g.name + '"):::library'; }).join('\n')}

    Request --> Generator
${LIBRARIES.map(function (g) { return '    Generator -->|"' + g.edgeLabel + '"| ' + g.id; }).join('\n')}

    click Request call showInfo("Request")
    click Generator call showInfo("Generator")
${LIBRARIES.map(function (g) { return '    click ' + g.id + ' call showInfo("' + g.id + '")'; }).join('\n')}

    classDef request fill:#eceff1,stroke:#546e7a,stroke-width:2px,color:#1f2937,font-size:16px
    classDef generator fill:#00695c,stroke:#003d33,stroke-width:3px,color:#ffffff,font-size:16px
    classDef library fill:#b2dfdb,stroke:#00695c,stroke-width:2px,color:#0b2e2a,font-size:16px

    linkStyle default stroke:#546e7a,stroke-width:2px
`;

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------
let requestIndex = 0;
let solved = false;      // has the current request been routed correctly?
let wrongTries = 0;      // wrong picks for the current request

// ---------------------------------------------------------------------------
// Keyword matching
// ---------------------------------------------------------------------------
function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function keywordRegex(keyword, flags) {
  const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp('(^|[^a-z0-9])(' + escaped + 's?)(?![a-z0-9])', flags);
}

// For each library, the list of its trigger keywords found in the request.
function matchRequest(text) {
  return LIBRARIES.map(function (g) {
    return g.keywords.filter(function (k) { return keywordRegex(k, 'i').test(text); });
  });
}

// The request text with the given keywords wrapped in <mark>.
function markKeywords(text, keywords) {
  let html = escapeHtml(text);
  keywords.forEach(function (k) {
    html = html.replace(keywordRegex(k, 'ig'), '$1<mark>$2</mark>');
  });
  return html;
}

function keywordList(words) {
  return words.map(function (k) { return '<mark>' + k + '</mark>'; }).join(' ');
}

// ---------------------------------------------------------------------------
// Diagram highlighting
// ---------------------------------------------------------------------------
function nodeElement(nodeId) {
  return document.querySelector('#diagram [id^="flowchart-' + nodeId + '-"]');
}

// routes: array of library indexes whose route is lit (empty = nothing lit)
// selectedNode: node id to give the halo to, or null
function highlight(routes, selectedNode) {
  document.querySelectorAll('#diagram .node').forEach(function (n) {
    n.classList.remove('selected', 'dimmed');
  });
  const lit = routes.length > 0;
  const paths = Array.from(document.querySelectorAll('#diagram path.flowchart-link'));
  const labels = Array.from(document.querySelectorAll('#diagram g.edgeLabel'));
  paths.forEach(function (p, i) {
    const onRoute = lit && (i === 0 || routes.indexOf(i - 1) >= 0);
    p.classList.toggle('dimmed', lit && !onRoute);
    p.style.setProperty('stroke', onRoute ? '#00695c' : '#546e7a', 'important');
    p.style.setProperty('stroke-width', onRoute ? '4px' : '2px', 'important');
    if (labels[i]) labels[i].classList.toggle('dimmed', lit && !onRoute);
  });
  if (lit) {
    LIBRARIES.forEach(function (g, i) {
      const el = nodeElement(g.id);
      if (el && routes.indexOf(i) < 0) el.classList.add('dimmed');
    });
  }
  if (selectedNode) {
    const el = nodeElement(selectedNode);
    if (el) el.classList.add('selected');
  }
}

// ---------------------------------------------------------------------------
// Rendering
// ---------------------------------------------------------------------------
function renderInfo(html) {
  document.getElementById('infobox').innerHTML = html;
}

function renderRequest(markWords) {
  const r = REQUESTS[requestIndex];
  document.getElementById('requestText').innerHTML =
    '“' + (markWords ? markKeywords(r.text, markWords) : escapeHtml(r.text)) + '”';
  document.getElementById('requestLabel').textContent =
    'Request ' + (requestIndex + 1) + ' of ' + REQUESTS.length;
}

function libraryDetails(g) {
  return '<p><span class="label">Best for: </span>' + g.bestFor + '</p>' +
    '<p><span class="label">Example MicroSim: </span>' + g.example + '</p>';
}

function showPrompt() {
  highlight([], null);
  renderRequest(null);
  renderInfo('<h2>Your turn: which library?</h2>' +
    '<p>Read the request above and look for its trigger keywords. Then click the library box that the MicroSim Generator should route it to.</p>' +
    '<p class="note">The words on each arrow are some of the trigger keywords for that route.</p>');
}

function loadRequest(index) {
  requestIndex = index;
  solved = false;
  wrongTries = 0;
  showPrompt();
}

// The reader clicked a library box while the request is still unrouted.
function answer(libIndex) {
  const r = REQUESTS[requestIndex];
  const hits = matchRequest(r.text);
  const g = LIBRARIES[libIndex];

  if (r.answer === -1) {
    // Ambiguous request: two rows match equally, so the generator must ask.
    const tied = [];
    hits.forEach(function (h, i) { if (h.length > 0) tied.push(i); });
    const allWords = [];
    tied.forEach(function (i) { hits[i].forEach(function (k) { allWords.push(k); }); });
    solved = true;
    highlight(tied, g.id);
    renderRequest(allWords);
    renderInfo('<h2 class="warn">Ambiguous: the generator has to ask</h2>' +
      '<p>' + tied.map(function (i) {
        return keywordList(hits[i]) + ' is a trigger keyword for <b>' + LIBRARIES[i].name + '</b>';
      }).join(', and ') + '. Two routes match equally, so no single box is right.</p>' +
      '<p>Resolving a word that could mean several visualization types is called <b>ambiguous term clarification</b>. The generator asks: a chart of values, or a network of nodes and edges?</p>');
    return;
  }

  if (libIndex === r.answer) {
    solved = true;
    highlight([libIndex], g.id);
    renderRequest(hits[libIndex]);
    renderInfo('<h2>Correct: routed to ' + g.name + '</h2>' +
      '<p><span class="label">Matched keywords: </span>' + keywordList(hits[libIndex]) + '</p>' +
      libraryDetails(g) +
      '<p class="note">Select <b>Next Request</b> to route another one.</p>');
  } else {
    wrongTries += 1;
    highlight([], g.id);
    const mine = hits[libIndex];
    let html = '<h2 class="warn">Not ' + g.name + '. Try again.</h2>';
    if (mine.length === 0) {
      html += '<p>None of the trigger keywords for ' + g.name + ' appear in this request: <span class="kw">' +
        g.keywords.join(', ') + '</span>.</p>';
    } else {
      html += '<p>' + g.name + ' matches ' + keywordList(mine) + ', but another route matches more keywords.</p>';
    }
    if (wrongTries >= 2) {
      renderRequest(hits[r.answer]);
      html += '<p><span class="label">Hint: </span>the highlighted words in the request are trigger keywords. Find the arrow or library they belong to.</p>';
    } else {
      html += '<p>Which words in the request say what <i>kind</i> of data it has?</p>';
    }
    renderInfo(html);
  }
}

// Called by the Mermaid `click` directives, so it must be global.
window.showInfo = function (nodeId) {
  const r = REQUESTS[requestIndex];
  let libIndex = -1;
  LIBRARIES.forEach(function (g, i) { if (g.id === nodeId) libIndex = i; });

  if (libIndex >= 0) {
    if (!solved) { answer(libIndex); return; }
    // Request already routed: clicking a library just describes it
    const g = LIBRARIES[libIndex];
    highlight([libIndex], g.id);
    renderInfo('<h2>' + g.name + '</h2>' +
      '<p><span class="label">Trigger keywords: </span><span class="kw">' + g.keywords.join(', ') + '</span></p>' +
      libraryDetails(g));
  } else if (nodeId === 'Request') {
    highlight([], 'Request');
    renderInfo('<h2>Incoming Request</h2>' +
      '<p><span class="label">Example request: </span>“' + escapeHtml(r.text) + '”</p>' +
      '<p>A request is plain language. Nobody names a library in it. The words that describe the data, such as <i>dates</i> or <i>coordinates</i>, are what the generator routes on.</p>');
  } else if (nodeId === 'Generator') {
    highlight([], 'Generator');
    renderInfo('<h2>MicroSim Generator (Meta-Skill)</h2>' +
      '<p><span class="label">Its routing job: </span>compare the words of the request with the trigger keywords in its routing table, then load the one guide for the matched library. It does not draw anything itself.</p>' +
      '<p>This is <b>visualization library routing</b>: selecting the rendering technology best matched to a request. The six libraries shown are some of its routes, not all of them.</p>');
  }
};

// ---------------------------------------------------------------------------
// Startup
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', async function () {
  document.getElementById('nextButton').addEventListener('click', function () {
    loadRequest((requestIndex + 1) % REQUESTS.length);
  });
  renderRequest(null);

  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'loose',   // required for click callbacks
    theme: 'default',
    flowchart: {
      useMaxWidth: true,
      htmlLabels: true,
      curve: 'basis',
      nodeSpacing: 12,
      rankSpacing: 46,
      padding: 10
    }
  });

  const container = document.getElementById('diagram');
  try {
    const result = await mermaid.render('librarySvg', DIAGRAM);
    container.innerHTML = result.svg;
    if (result.bindFunctions) result.bindFunctions(container);
  } catch (err) {
    container.textContent = 'The diagram could not be drawn: ' + err.message;
    return;
  }

  const svg = container.querySelector('svg');
  if (svg) {
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Flowchart: an incoming request goes to the MicroSim Generator meta-skill, which fans out to six libraries: p5.js, Chart.js, vis-network, vis-timeline, Leaflet, and Mermaid. Each arrow is labeled with trigger keywords that route there.');
  }

  // Keyboard access: every node can be focused and activated with Enter or Space
  ['Request', 'Generator'].concat(LIBRARIES.map(function (g) { return g.id; })).forEach(function (nodeId) {
    const el = nodeElement(nodeId);
    if (!el) return;
    el.setAttribute('tabindex', '0');
    el.setAttribute('role', 'button');
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        window.showInfo(nodeId);
      }
    });
  });

  loadRequest(0);
});

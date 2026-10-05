// Meta-Skill Routing Table - Mermaid flowchart with click-to-inspect nodes
// CANVAS_HEIGHT: 550
// Shows how the microsim-generator meta-skill uses a trigger keyword table to
// send a request to exactly one on-demand guide. Type or pick a request and
// the matching route is highlighted. Every node also has a Mermaid `click`
// directive wired to showInfo(), which fills the shared infobox panel.
//
// The keywords are the real trigger keywords for these five guides in the
// microsim-generator skill. The full skill routes among more guides than the
// five shown here, and it weighs a request with more judgment than the plain
// keyword count used in this demonstration.

// ---------------------------------------------------------------------------
// Routing table excerpt (order matches the Table --> guide edges below)
// ---------------------------------------------------------------------------
const GUIDES = [
  {
    id: 'GuideP5', title: 'p5.js Guide', file: 'references/p5-guide.md', edgeLabel: 'simulation, physics',
    keywords: ['custom', 'simulation', 'physics', 'interactive', 'bouncing', 'movement', 'p5.js'],
    produces: 'Custom simulations, physics, and animations drawn on a canvas, with sliders and buttons to control them.'
  },
  {
    id: 'GuideChart', title: 'Chart.js Guide', file: 'references/chartjs-guide.md', edgeLabel: 'chart, bar, pie',
    keywords: ['chart', 'bar', 'line', 'pie', 'doughnut', 'radar', 'statistics', 'data'],
    produces: 'Standard data charts: bar, line, pie, doughnut, and radar.'
  },
  {
    id: 'GuideNetwork', title: 'vis-network Guide', file: 'references/vis-network-guide.md', edgeLabel: 'network, nodes, edges',
    keywords: ['network', 'nodes', 'edges', 'graph', 'dependencies', 'concept map', 'knowledge graph'],
    produces: 'Network graphs made of nodes and edges, such as dependency graphs and concept maps.'
  },
  {
    id: 'GuideMermaid', title: 'Mermaid Guide', file: 'references/mermaid-guide.md', edgeLabel: 'flowchart, workflow',
    keywords: ['flowchart', 'workflow', 'process', 'state machine', 'UML', 'sequence diagram'],
    produces: 'Flowcharts, workflows, and other process diagrams, like the one on this page.'
  },
  {
    id: 'GuideTimeline', title: 'Timeline Guide', file: 'references/timeline-guide.md', edgeLabel: 'timeline, dates',
    keywords: ['timeline', 'dates', 'chronological', 'events', 'history', 'schedule', 'milestones'],
    produces: 'Chronological displays of dated events, such as histories and schedules.'
  }
];

const EXAMPLES = [
  'Create a timeline showing key events in computer history',
  'Build an interactive bouncing ball simulation',
  'Make a bar chart comparing programming language popularity',
  'Draw a flowchart of the software release process',
  'Show a concept map of the nodes and edges in our learning graph',
  'Create a graph of our sales data'
];

// ---------------------------------------------------------------------------
// Diagram definition (left-to-right Mermaid flowchart)
// Edge order: 0 Request-->MetaSkill, 1 MetaSkill-->Table, 2..6 Table-->guides
// ---------------------------------------------------------------------------
const DIAGRAM = `flowchart LR
    Request("Incoming<br/>Request"):::request
    MetaSkill("microsim-generator<br/>(Meta-Skill)"):::meta
    Table["Trigger<br/>Keyword Table"]:::keywordTable
${GUIDES.map(function (g) { return '    ' + g.id + '("' + g.title + '"):::guide'; }).join('\n')}

    Request --> MetaSkill
    MetaSkill --> Table
${GUIDES.map(function (g) { return '    Table -->|"' + g.edgeLabel + '"| ' + g.id; }).join('\n')}

    click Request call showInfo("Request")
    click MetaSkill call showInfo("MetaSkill")
    click Table call showInfo("Table")
${GUIDES.map(function (g) { return '    click ' + g.id + ' call showInfo("' + g.id + '")'; }).join('\n')}

    classDef request fill:#eceff1,stroke:#546e7a,stroke-width:2px,color:#1f2937,font-size:16px
    classDef meta fill:#00695c,stroke:#003d33,stroke-width:3px,color:#ffffff,font-size:16px
    classDef keywordTable fill:#ffffff,stroke:#00695c,stroke-width:3px,color:#1f2937,font-size:16px
    classDef guide fill:#b2dfdb,stroke:#00695c,stroke-width:2px,color:#0b2e2a,font-size:16px

    linkStyle default stroke:#546e7a,stroke-width:2px
`;

// ---------------------------------------------------------------------------
// Keyword matching
// ---------------------------------------------------------------------------
function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function keywordRegex(keyword) {
  const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp('(^|[^a-z0-9])' + escaped + 's?(?![a-z0-9])', 'i');
}

// Returns, for each guide, the list of its keywords found in the request.
function matchRequest(request) {
  return GUIDES.map(function (g) {
    return g.keywords.filter(function (k) { return keywordRegex(k).test(request); });
  });
}

// ---------------------------------------------------------------------------
// Diagram highlighting
// ---------------------------------------------------------------------------
function nodeElement(nodeId) {
  return document.querySelector('#diagram [id^="flowchart-' + nodeId + '-"]');
}

function edgePaths() {
  return Array.from(document.querySelectorAll('#diagram path.flowchart-link'));
}

function edgeLabels() {
  return Array.from(document.querySelectorAll('#diagram g.edgeLabel'));
}

// activeGuide: index into GUIDES, or -1 for "no route highlighted"
// selectedNode: node id to give the halo to, or null
function highlight(activeGuide, selectedNode) {
  document.querySelectorAll('#diagram .node').forEach(function (n) {
    n.classList.remove('selected', 'dimmed');
  });
  const paths = edgePaths();
  const labels = edgeLabels();
  paths.forEach(function (p, i) {
    const onRoute = activeGuide >= 0 && (i < 2 || i === activeGuide + 2);
    p.classList.toggle('dimmed', activeGuide >= 0 && !onRoute);
    p.style.setProperty('stroke', onRoute ? '#00695c' : '#546e7a', 'important');
    p.style.setProperty('stroke-width', onRoute ? '4px' : '2px', 'important');
    if (labels[i]) labels[i].classList.toggle('dimmed', activeGuide >= 0 && !onRoute);
  });
  if (activeGuide >= 0) {
    GUIDES.forEach(function (g, i) {
      const el = nodeElement(g.id);
      if (el && i !== activeGuide) el.classList.add('dimmed');
    });
  }
  if (selectedNode) {
    const el = nodeElement(selectedNode);
    if (el) el.classList.add('selected');
  }
}

// ---------------------------------------------------------------------------
// Infobox rendering
// ---------------------------------------------------------------------------
function renderTable(matchedGuide, hits) {
  let html = '<caption>Trigger keyword table (five-row excerpt)</caption>' +
    '<thead><tr><th>Trigger keywords</th><th>Guide loaded</th></tr></thead><tbody>';
  GUIDES.forEach(function (g, i) {
    const found = hits ? hits[i] : [];
    const words = g.keywords.map(function (k) {
      return found.indexOf(k) >= 0 ? '<span class="kw-hit"><b>' + k + '</b></span>' : k;
    }).join(', ');
    html += '<tr' + (i === matchedGuide ? ' class="matched"' : '') + '><td>' + words + '</td><td><code>' +
      g.file.replace('references/', '') + '</code></td></tr>';
  });
  html += '</tbody>';
  document.getElementById('keywordTable').innerHTML = html;
}

function renderText(html) {
  document.getElementById('infoText').innerHTML = html;
}

// Route the request in the text box and show the result
function routeRequest() {
  const request = document.getElementById('requestInput').value.trim();
  if (request.length === 0) {
    highlight(-1, null);
    renderTable(-1, null);
    renderText('<h2>Type a request</h2><p>Describe the MicroSim you want in the Request box, or pick one of the examples, then select <b>Route</b>.</p>');
    return;
  }
  const hits = matchRequest(request);
  const counts = hits.map(function (h) { return h.length; });
  const best = Math.max.apply(null, counts);
  const winners = [];
  counts.forEach(function (c, i) { if (c === best && best > 0) winners.push(i); });

  if (winners.length === 1) {
    const g = GUIDES[winners[0]];
    highlight(winners[0], g.id);
    renderTable(winners[0], hits);
    renderText('<h2>Routed to the ' + g.title + '</h2>' +
      '<p><span class="label">Matched keywords: </span>' +
      hits[winners[0]].map(function (k) { return '<mark>' + k + '</mark>'; }).join(' ') + '</p>' +
      '<p>The meta-skill now reads <code>' + g.file + '</code>. The other four guides are never loaded for this request.</p>');
  } else if (winners.length > 1) {
    highlight(-1, 'Table');
    renderTable(-1, hits);
    const names = winners.map(function (i) { return GUIDES[i].title; }).join(' and the ');
    renderText('<h2 class="warn">Ambiguous: two routes match</h2>' +
      '<p>The request matches the ' + names + ' equally (' + best + ' keyword' + (best === 1 ? '' : 's') + ' each).</p>' +
      '<p>A routing table must end at exactly one guide. When a request is ambiguous, the real meta-skill scores the candidates and asks which one you want.</p>');
  } else {
    highlight(-1, 'Table');
    renderTable(-1, hits);
    renderText('<h2 class="warn">No trigger keyword matched</h2>' +
      '<p>None of the keywords in these five rows appears in the request, so none of these guides is loaded.</p>' +
      '<p>Add a word that says what kind of MicroSim you want, such as <i>timeline</i>, <i>chart</i>, or <i>simulation</i>.</p>');
  }
}

// Called by the Mermaid `click` directives, so it must be global.
window.showInfo = function (nodeId) {
  const request = document.getElementById('requestInput').value.trim();
  let guideIndex = -1;
  GUIDES.forEach(function (g, i) { if (g.id === nodeId) guideIndex = i; });

  if (guideIndex >= 0) {
    const g = GUIDES[guideIndex];
    highlight(guideIndex, g.id);
    renderTable(guideIndex, null);
    renderText('<h2>' + g.title + '</h2>' +
      '<p><span class="label">Produces: </span>' + g.produces + '</p>' +
      '<p><span class="label">Loaded on demand from: </span><code>' + g.file + '</code>, only when a request matches its row.</p>');
  } else if (nodeId === 'Request') {
    highlight(-1, 'Request');
    renderTable(-1, null);
    renderText('<h2>Incoming Request</h2>' +
      '<p><span class="label">Example request: </span>"' + escapeHtml(request || EXAMPLES[0]) + '"</p>' +
      '<p>The agent first compares the request with every installed skill\'s description. That match is what loads the meta-skill.</p>');
  } else if (nodeId === 'MetaSkill') {
    highlight(-1, 'MetaSkill');
    renderTable(-1, null);
    renderText('<h2>microsim-generator (Meta-Skill)</h2>' +
      '<p>A meta-skill is a skill whose primary job is to route a request to one of several detailed guides rather than to perform the task itself.</p>' +
      '<p>This one routes each MicroSim request to the guide for the right JavaScript library.</p>');
  } else if (nodeId === 'Table') {
    highlight(-1, 'Table');
    renderTable(-1, null);
    renderText('<h2>Trigger Keyword Table</h2>' +
      '<p>An explicit mapping from request phrases to the guide that should handle them, which makes routing decisions predictable.</p>' +
      '<p>The rows shown here are five of the rows in the real skill\'s table.</p>');
  }
};

// ---------------------------------------------------------------------------
// Startup
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', async function () {
  const input = document.getElementById('requestInput');
  const select = document.getElementById('exampleSelect');

  const placeholder = document.createElement('option');
  placeholder.value = '';
  placeholder.textContent = 'Examples...';
  select.appendChild(placeholder);
  EXAMPLES.forEach(function (ex, i) {
    const opt = document.createElement('option');
    opt.value = String(i);
    opt.textContent = ex;
    select.appendChild(opt);
  });
  select.addEventListener('change', function () {
    if (select.value === '') return;
    input.value = EXAMPLES[Number(select.value)];
    select.value = '';
    routeRequest();
  });
  document.getElementById('routeButton').addEventListener('click', routeRequest);
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') routeRequest();
  });
  input.value = EXAMPLES[0];
  renderTable(-1, null);

  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'loose',   // required for click callbacks
    theme: 'default',
    flowchart: {
      useMaxWidth: true,
      htmlLabels: true,
      curve: 'basis',
      nodeSpacing: 12,
      rankSpacing: 40,
      padding: 10
    }
  });

  const container = document.getElementById('diagram');
  try {
    const result = await mermaid.render('metaSkillRoutingSvg', DIAGRAM);
    container.innerHTML = result.svg;
    if (result.bindFunctions) result.bindFunctions(container);
  } catch (err) {
    container.textContent = 'The diagram could not be drawn: ' + err.message;
    return;
  }

  const svg = container.querySelector('svg');
  if (svg) {
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Flowchart: an incoming request goes to the microsim-generator meta-skill, then to its trigger keyword table, which fans out to five guides: p5.js, Chart.js, vis-network, Mermaid, and Timeline. Each edge is labeled with the keywords that route there.');
  }

  // Keyboard access: every node can be focused and activated with Enter or Space
  ['Request', 'MetaSkill', 'Table'].concat(GUIDES.map(function (g) { return g.id; })).forEach(function (nodeId) {
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

  // Start with the first example already routed
  routeRequest();
});

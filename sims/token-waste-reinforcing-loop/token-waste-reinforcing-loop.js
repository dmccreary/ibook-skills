// Token Waste Reinforcing Loop - causal loop diagram (vis-network)
// CANVAS_HEIGHT: 560
// Two linked causal loops built from this book's own token-waste example:
//   R  a reinforcing loop in which unnecessary parallel agents feed on the
//      pressure they create, and
//   B  a balancing loop in which chapter token budgeting pushes back.
// The two loops share one link. Select R or B to light up that loop, trace
// one change all the way around it, and count its minus signs.
//
// The data below uses the field names of the causal-loop JSON schema in the
// microsim-generator skill (nodes, edges with polarity, loops with path).
// Node positions are fixed (physics is off) so the two loops stay separated.

// ---------------------------------------------------------------------------
// Causal loop data
// polarity "positive": source and target move in the SAME direction
// polarity "negative": source and target move in OPPOSITE directions
// ---------------------------------------------------------------------------
const CLD = {
  nodes: [
    {
      id: 'agents', label: 'Unnecessary\nParallel Agents', position: { x: 0, y: -120 },
      description: 'The number of extra agents launched for work that one agent, or a script, could have done.'
    },
    {
      id: 'overhead', label: 'Startup Overhead\nPaid', position: { x: 0, y: 120 },
      description: 'The fixed tokens spent launching agents before any of them does useful work: roughly 12,000 tokens per agent, as measured on this project.'
    },
    {
      id: 'remaining', label: 'Tokens Remaining\nin Window', position: { x: -340, y: 127 },
      description: 'The part of a usage window\'s token allowance that has not been spent yet.'
    },
    {
      id: 'pressure', label: 'Pressure\nto Rush', position: { x: -340, y: -113 },
      description: 'The urge to finish quickly before the window\'s allowance runs out.'
    },
    {
      id: 'budgeting', label: 'Chapter Token\nBudgeting', position: { x: 340, y: 127 },
      description: 'Allocating a per-chapter allowance for generation so a long book completes without exhausting a period\'s capacity.'
    },
    {
      id: 'awareness', label: 'Cost\nAwareness', position: { x: 340, y: -113 },
      description: 'How clearly the author sees what each step actually costs before choosing how to run it.'
    }
  ],
  edges: [
    {
      id: 'agents_overhead', source: 'agents', target: 'overhead', polarity: 'positive', loops: ['R', 'B'],
      description: 'Every extra agent pays its own startup overhead, so more unnecessary agents means more overhead paid.'
    },
    {
      id: 'overhead_remaining', source: 'overhead', target: 'remaining', polarity: 'negative', loops: ['R'],
      description: 'Overhead is spent out of the same allowance as real work, so more overhead leaves fewer tokens remaining.'
    },
    {
      id: 'remaining_pressure', source: 'remaining', target: 'pressure', polarity: 'negative', loops: ['R'],
      description: 'The fewer tokens that remain in the window, the stronger the pressure to rush.'
    },
    {
      id: 'pressure_agents', source: 'pressure', target: 'agents', polarity: 'positive', loops: ['R'],
      description: 'Rushing makes "run everything in parallel" look like speed, so more pressure launches more unnecessary agents.'
    },
    {
      id: 'overhead_budgeting', source: 'overhead', target: 'budgeting', polarity: 'positive', loops: ['B'],
      description: 'Overhead that pushes a chapter past its allowance shows up as an overrun, so more overhead draws more budgeting attention.'
    },
    {
      id: 'budgeting_awareness', source: 'budgeting', target: 'awareness', polarity: 'positive', loops: ['B'],
      description: 'Comparing spending against a per-chapter allowance makes the cost of each choice visible, so more budgeting raises cost awareness.'
    },
    {
      id: 'awareness_agents', source: 'awareness', target: 'agents', polarity: 'negative', loops: ['B'],
      description: 'An author who can see the overhead matches the tool to the task\'s real size, so more cost awareness means fewer unnecessary agents.'
    }
  ],
  loops: [
    {
      id: 'R', type: 'reinforcing', label: 'R: Token Waste', position: { x: -170, y: 6 },
      path: ['agents', 'overhead', 'remaining', 'pressure', 'agents'],
      netEffect: 'The change comes back <b>amplified</b>. Left unchecked, waste keeps growing and the tokens remaining in the window collapse.'
    },
    {
      id: 'B', type: 'balancing', label: 'B: Chapter Token Budgeting', position: { x: 170, y: 6 },
      path: ['agents', 'overhead', 'budgeting', 'awareness', 'agents'],
      netEffect: 'The change comes back <b>reversed</b>. The loop pushes waste back down, so the system settles toward a stable level instead of running away.'
    }
  ]
};

const COLOR = {
  R: '#c62828',          // reinforcing loop links (red)
  B: '#1565c0',          // balancing loop links (blue)
  shared: '#37474f',     // the one link that belongs to both loops
  dim: '#b0bec5',
  nodeBorder: '#455a64',
  nodeFill: '#ffffff',
  text: '#111827'
};
const TINT = { R: '#ffebee', B: '#e3f2fd' };

let network, nodes, edges;
let selectedLoop = null;      // null, 'R', or 'B'
let pinnedHtml = '';          // the panel content to return to after a hover

function nodeById(id) { return CLD.nodes.find(function (n) { return n.id === id; }); }
function edgeById(id) { return CLD.edges.find(function (e) { return e.id === id; }); }
function loopById(id) { return CLD.loops.find(function (l) { return l.id === id; }); }
function flat(label) { return label.replace(/\n/g, ' '); }

function edgeBetween(a, b) {
  return CLD.edges.find(function (e) { return e.source === a && e.target === b; });
}

// Walk a loop from its first node, assuming that node RISES, and return the
// direction (+1 up, -1 down) of every stop, including the return to the start.
function traceLoop(loop) {
  const steps = [{ node: loop.path[0], dir: 1, edge: null }];
  let dir = 1;
  for (let i = 1; i < loop.path.length; i++) {
    const e = edgeBetween(loop.path[i - 1], loop.path[i]);
    dir = e.polarity === 'positive' ? dir : -dir;
    steps.push({ node: loop.path[i], dir: dir, edge: e });
  }
  return steps;
}

function countNegatives(loop) {
  let n = 0;
  for (let i = 1; i < loop.path.length; i++) {
    if (edgeBetween(loop.path[i - 1], loop.path[i]).polarity === 'negative') n++;
  }
  return n;
}

// ---------------------------------------------------------------------------
// Info panel
// ---------------------------------------------------------------------------
function setPanel(html, pin) {
  document.getElementById('infobox').innerHTML = html;
  if (pin) pinnedHtml = html;
}

function overviewHtml() {
  return '<h2>Two loops that share one link</h2>' +
    '<p>Every arrow is a claim about cause and effect. A <b>+</b> means the two variables move in the same direction. A <b>&minus;</b> means they move in opposite directions.</p>' +
    '<p><span class="label">Try it: </span>Select <b>R loop</b> or <b>B loop</b> (or click the R or B circle) to trace one change all the way around that loop. Hover any variable or arrow to read what it means.</p>';
}

function loopHtml(loop) {
  const steps = traceLoop(loop);
  const parts = steps.map(function (s, i) {
    const name = flat(nodeById(s.node).label);
    const arrow = s.dir > 0 ? '&#9650;' : '&#9660;';
    const word = s.dir > 0 ? 'more' : 'fewer';
    const lead = i === 0 ? 'Start: ' : (i === steps.length - 1 ? 'back to ' : '');
    return '<span class="step ' + (s.dir > 0 ? 'up' : 'down') + '">' + lead + word + ' ' + name + ' ' + arrow + '</span>';
  });
  const negatives = countNegatives(loop);
  const parity = negatives % 2 === 0 ? 'even' : 'odd';
  return '<h2 class="' + loop.id + '">' + loop.label + ' (' + loop.type + ' loop)</h2>' +
    '<p class="trace">' + parts.join(' <span class="then">&rarr;</span> ') + '</p>' +
    '<p><span class="label">Net effect: </span>' + loop.netEffect + '</p>' +
    '<p><span class="label">How to tell: </span>count the minus signs around the loop. ' +
    negatives + ' is ' + parity + ', so this loop is ' + loop.type + ' (even = reinforcing, odd = balancing).</p>';
}

function nodeHtml(n) {
  const inLoops = CLD.loops.filter(function (l) { return l.path.indexOf(n.id) >= 0; })
    .map(function (l) { return l.id; });
  return '<h2>' + flat(n.label) + '</h2>' +
    '<p>' + n.description + '</p>' +
    '<p class="note">Variable in loop' + (inLoops.length > 1 ? 's ' : ' ') + inLoops.join(' and ') + '.</p>';
}

function edgeHtml(e) {
  const same = e.polarity === 'positive';
  return '<h2>' + flat(nodeById(e.source).label) + ' &rarr; ' + flat(nodeById(e.target).label) +
    ' <span class="sign">(' + (same ? '+' : '&minus;') + ')</span></h2>' +
    '<p>' + e.description + '</p>' +
    '<p class="note">' + (same ? '+ link: the two variables move in the same direction.'
      : '&minus; link: the two variables move in opposite directions.') +
    ' Part of loop' + (e.loops.length > 1 ? 's ' : ' ') + e.loops.join(' and ') + '.</p>';
}

// ---------------------------------------------------------------------------
// Network styling for the current selection
// ---------------------------------------------------------------------------
function edgeColor(e) {
  if (selectedLoop) {
    return e.loops.indexOf(selectedLoop) >= 0 ? COLOR[selectedLoop] : COLOR.dim;
  }
  return e.loops.length > 1 ? COLOR.shared : COLOR[e.loops[0]];
}

function applySelection() {
  const loop = selectedLoop ? loopById(selectedLoop) : null;
  const dirs = {};
  if (loop) {
    const steps = traceLoop(loop);
    // the first stop is the starting rise; the last stop is the same node
    // after one trip around, which is what the reader should compare
    steps.forEach(function (s, i) { if (i < steps.length - 1) dirs[s.node] = s.dir; });
    dirs['__return'] = steps[steps.length - 1].dir;
  }

  nodes.update(CLD.nodes.map(function (n) {
    const onLoop = loop && loop.path.indexOf(n.id) >= 0;
    let label = n.label;
    if (onLoop) {
      if (n.id === loop.path[0]) {
        label += '\n▲ start, returns ' + (dirs['__return'] > 0 ? '▲' : '▼');
      } else {
        label += '\n' + (dirs[n.id] > 0 ? '▲ rises' : '▼ falls');
      }
    }
    const dimmed = loop && !onLoop;
    return {
      id: n.id,
      label: label,
      color: {
        background: onLoop ? TINT[loop.id] : COLOR.nodeFill,
        border: dimmed ? COLOR.dim : (onLoop ? COLOR[loop.id] : COLOR.nodeBorder),
        highlight: { background: onLoop ? TINT[loop.id] : '#fff8e1', border: '#111827' },
        hover: { background: onLoop ? TINT[loop.id] : '#fff8e1', border: '#111827' }
      },
      borderWidth: onLoop ? 3 : 2,
      font: { color: dimmed ? '#90a4ae' : COLOR.text }
    };
  }));

  edges.update(CLD.edges.map(function (e) {
    const c = edgeColor(e);
    const onLoop = loop && e.loops.indexOf(loop.id) >= 0;
    const dimmed = loop && !onLoop;
    return {
      id: e.id,
      color: { color: c, highlight: c, hover: c },
      width: onLoop ? 4 : 2.5,
      font: { color: dimmed ? '#90a4ae' : COLOR.text }
    };
  }));

  nodes.update(CLD.loops.map(function (l) {
    const active = !loop || loop.id === l.id;
    return {
      id: 'loop_' + l.id,
      color: { background: active ? COLOR[l.id] : COLOR.dim, border: active ? COLOR[l.id] : COLOR.dim },
      borderWidth: loop && loop.id === l.id ? 5 : 1
    };
  }));

  ['R', 'B'].forEach(function (id) {
    document.getElementById('button' + id).setAttribute('aria-pressed', selectedLoop === id ? 'true' : 'false');
  });
  document.getElementById('buttonBoth').setAttribute('aria-pressed', selectedLoop ? 'false' : 'true');
}

function selectLoop(id) {
  selectedLoop = id;
  applySelection();
  if (network) {
    network.unselectAll();
    fitView();
  }
  setPanel(id ? loopHtml(loopById(id)) : overviewHtml(), true);
}

// ---------------------------------------------------------------------------
// Zoom: buttons and pinch only, so a normal page scroll is never captured
// ---------------------------------------------------------------------------
function zoomBy(factor, pointer) {
  const scale = Math.min(3, Math.max(0.3, network.getScale() * factor));
  const options = { scale: scale, animation: false };
  if (pointer) {
    // keep the world point under the cursor fixed
    const before = network.DOMtoCanvas(pointer);
    const view = network.getViewPosition();
    const k = network.getScale() / scale;
    options.position = { x: before.x + (view.x - before.x) * k, y: before.y + (view.y - before.y) * k };
  }
  network.moveTo(options);
}

// Fit the whole diagram, with a little breathing room. In a narrow iframe the
// labels would be too small to read, so there the view fits the selected loop.
function fitView() {
  const narrow = document.getElementById('network').clientWidth < 640;
  if (narrow && selectedLoop) {
    const loop = loopById(selectedLoop);
    network.fit({ nodes: loop.path.concat(['loop_' + loop.id]), animation: false });
  } else {
    network.fit({ animation: false });
  }
  network.moveTo({ scale: network.getScale() * 0.92, animation: false });
}

// ---------------------------------------------------------------------------
// Startup
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', function () {
  const container = document.getElementById('network');

  const nodeItems = CLD.nodes.map(function (n) {
    return {
      id: n.id, label: n.label, x: n.position.x, y: n.position.y,
      shape: 'ellipse', margin: 10,
      font: { size: 18, face: 'Arial', color: COLOR.text, multi: false }
    };
  });
  CLD.loops.forEach(function (l) {
    nodeItems.push({
      id: 'loop_' + l.id, label: l.id, x: l.position.x, y: l.position.y,
      shape: 'circle', margin: 12,
      font: { size: 26, face: 'Arial', color: '#ffffff', bold: true },
      color: { background: COLOR[l.id], border: COLOR[l.id] }
    });
  });
  nodes = new vis.DataSet(nodeItems);

  edges = new vis.DataSet(CLD.edges.map(function (e) {
    // edges of the clockwise loop (R) and the counter-clockwise loop (B) bow
    // outward; the shared link between them stays straight
    let smooth = false;
    if (e.loops.length === 1) {
      smooth = { enabled: true, type: e.loops[0] === 'R' ? 'curvedCW' : 'curvedCCW', roundness: 0.18 };
    }
    return {
      id: e.id, from: e.source, to: e.target,
      label: e.polarity === 'positive' ? '+' : '−',
      arrows: { to: { enabled: true, scaleFactor: 1.1 } },
      smooth: smooth,
      font: { size: 28, face: 'Arial', bold: true, color: COLOR.text, strokeWidth: 8, strokeColor: '#f0f8ff', align: 'horizontal' }
    };
  }));

  network = new vis.Network(container, { nodes: nodes, edges: edges }, {
    physics: false,
    layout: { improvedLayout: false },
    interaction: {
      hover: true,
      dragNodes: true,
      dragView: true,       // drag the background to pan
      zoomView: false,      // wheel zoom is off so page scrolling is never hijacked
      selectConnectedEdges: false,
      tooltipDelay: 100000
    },
    nodes: { borderWidth: 2 },
    edges: { hoverWidth: 0, selectionWidth: 0 }
  });

  // Hover shows a definition; leaving restores the pinned panel
  network.on('hoverNode', function (p) {
    if (String(p.node).indexOf('loop_') === 0) {
      setPanel(loopHtml(loopById(String(p.node).slice(5))), false);
    } else {
      setPanel(nodeHtml(nodeById(p.node)), false);
    }
    container.style.cursor = 'pointer';
  });
  network.on('blurNode', function () {
    setPanel(pinnedHtml, false);
    container.style.cursor = 'default';
  });
  network.on('hoverEdge', function (p) {
    setPanel(edgeHtml(edgeById(p.edge)), false);
  });
  network.on('blurEdge', function () {
    setPanel(pinnedHtml, false);
  });

  // Click: R / B circle selects a loop; a variable or arrow pins its text
  network.on('click', function (p) {
    if (p.nodes.length > 0) {
      const id = String(p.nodes[0]);
      if (id.indexOf('loop_') === 0) {
        const loopId = id.slice(5);
        selectLoop(selectedLoop === loopId ? null : loopId);
      } else {
        setPanel(nodeHtml(nodeById(id)), true);
      }
    } else if (p.edges.length > 0) {
      setPanel(edgeHtml(edgeById(p.edges[0])), true);
    } else {
      setPanel(selectedLoop ? loopHtml(loopById(selectedLoop)) : overviewHtml(), true);
    }
  });

  // Pinch (reported by browsers as ctrl + wheel) zooms; a plain wheel scroll
  // is left alone so the page keeps scrolling
  container.addEventListener('wheel', function (event) {
    if (!event.ctrlKey) return;
    event.preventDefault();
    const delta = Math.max(-60, Math.min(60, event.deltaY));
    const rect = container.getBoundingClientRect();
    zoomBy(1 - delta * 0.004, { x: event.clientX - rect.left, y: event.clientY - rect.top });
  }, { passive: false });

  document.getElementById('buttonR').addEventListener('click', function () { selectLoop('R'); });
  document.getElementById('buttonB').addEventListener('click', function () { selectLoop('B'); });
  document.getElementById('buttonBoth').addEventListener('click', function () { selectLoop(null); });
  document.getElementById('zoomIn').addEventListener('click', function () { zoomBy(1.25); });
  document.getElementById('zoomOut').addEventListener('click', function () { zoomBy(0.8); });
  document.getElementById('zoomFit').addEventListener('click', fitView);

  window.addEventListener('resize', function () {
    network.redraw();
    fitView();
  });

  selectLoop(null);
  network.once('afterDrawing', fitView);
});

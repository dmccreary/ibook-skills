/*
    Causal Loop Diagram Viewer
    This script uses the vis-network.js library to render causal loop diagrams (CLDs).
    There are two options:
    
        1. default mode with no menus for embedding in an iframe
        2. full menu mode with menus for selecting sample diagrams and loading local files with menu=true in the URL
    
        The mode is controlled by the URL parameter "menu". If menu=true, the full mode is shown.
    Otherwise, the default mode is used.
*/

// Global variables

// When a node sits near the top of the canvas its tooltip overlaps the diagram
// title. Observe the tooltip's style attribute and flip it below the node
// whenever vis-network places it inside the title safe zone (top 60 px).
// Termination: after one flip the new top is >= SAFE_PX, so the recursive
// observer fire finds the condition false and does nothing.
function attachTooltipRepositioner(networkContainer) {
    const SAFE_PX = 60;
    const observer = new MutationObserver(function () {
        const tip = networkContainer.querySelector('.vis-tooltip');
        if (!tip) return;
        const top = parseFloat(tip.style.top) || 0;
        if (top < SAFE_PX) {
            const h = tip.offsetHeight || 80;
            tip.style.top = (top + h + 16) + 'px';
        }
    });
    observer.observe(networkContainer, {
        subtree: true,
        attributes: true,
        attributeFilter: ['style']
    });
}

// Returns a DOM element for vis-network tooltips. Passing a DOM node (not a
// string) bypasses vis-network's internal white-space override, so the text
// actually wraps instead of running off the canvas edge.
function makeTooltip(text) {
    if (!text) return undefined;
    const div = document.createElement('div');
    div.style.cssText = 'max-width:260px;white-space:normal;word-wrap:break-word;overflow-wrap:break-word;line-height:1.5;font-size:13px;padding:2px 0;';
    div.textContent = text;
    return div;
}

let network = null;
let cldData = null;
let nodes, edges;

async function loadExamplesList() {
    // TODO: Change this to list all the files in the examples directory
    // Only load files that end id the suffix "-cld.json"
    // For now, hardcode the list
    // You can add more examples by adding more JSON files to the examples directory
    // and adding them to this list
    const examples = [
        { id: 'ai-flywheel-cld', title: 'AI Flywheel' },
        { id: 'runaway-hypothesis-cld', title: 'R1: Runaway Hypothesis' },
        { id: 'autonomous-research-cld', title: 'R2: Autonomous Research' },
        { id: 'capital-compute-cld', title: 'R3: Capital → Compute' },
        { id: 'data-flywheel-cld', title: 'R4: Data Flywheel' },
        { id: 'compute-constraint-cld', title: 'B1: Compute Constraint' },
        { id: 'evaluation-bottleneck-cld', title: 'B2: Evaluation Bottleneck' },
        { id: 'diffusion-cld', title: 'B3: Diffusion / Fast-Follow' },
        { id: 'cost-performance-cld', title: 'B4: Cost-Performance' },
        { id: 'winner-takes-all-cld', title: 'Full System: Winner Takes All' }
    ];
    return examples;
}

async function loadCLDFromFile(filename) {
    try {
        const response = await fetch(`examples/${filename}.json`);
        if (!response.ok) {
            throw new Error(`Failed to load ${filename}.json: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        throw new Error(`Error loading CLD file: ${error.message}`);
    }
}

// Custom wheel-zoom handler.
// - Vertical scroll (deltaY) is left alone so the page scrolls normally over
//   the embedded diagram instead of getting hijacked.
// - Horizontal scroll (deltaX, e.g. two-finger sideways swipe on a Mac
//   trackpad) zooms.
// - Pinch gestures (wheel events with ctrlKey set, which is how Mac and most
//   browsers report pinch) also zoom.
// In all zoom cases we cap per-event magnitude and keep the world point
// under the cursor anchored.
function attachCustomZoom(container) {
    const ZOOM_PER_TICK = 0.04;   // per-event step. Lower = less sensitive.
    const MIN_SCALE = 0.1;
    const MAX_SCALE = 5.0;

    container.addEventListener('wheel', function(event) {
        if (!network) return;

        const isPinch = event.ctrlKey;
        const dx = event.deltaX;
        const dy = event.deltaY;
        const isHorizontalDominant = Math.abs(dx) > Math.abs(dy) && dx !== 0;

        // If it's not a zoom gesture, do nothing — let the page scroll.
        if (!isPinch && !isHorizontalDominant) return;

        event.preventDefault();

        // Pick the relevant axis: pinch uses dy (browser convention),
        // horizontal-swipe zoom uses dx.
        let delta = isPinch ? dy : dx;
        if (event.deltaMode === 1) delta *= 16;       // line mode
        else if (event.deltaMode === 2) delta *= 400; // page mode

        if (delta === 0) return;

        const direction = delta < 0 ? 1 : -1;

        // Cap magnitude so a fast trackpad flick doesn't compound into a jump.
        const magnitude = Math.min(Math.abs(delta), 60) / 60;
        const factor = 1 + direction * ZOOM_PER_TICK * magnitude;

        const oldScale = network.getScale();
        const newScale = Math.max(MIN_SCALE, Math.min(MAX_SCALE, oldScale * factor));
        if (newScale === oldScale) return;

        // Anchor the zoom on the cursor: the world point under the pointer
        // before zooming should remain under the pointer after zooming.
        const rect = container.getBoundingClientRect();
        const pointerDom = {
            x: event.clientX - rect.left,
            y: event.clientY - rect.top
        };
        const pointerCanvas = network.DOMtoCanvas(pointerDom);
        const view = network.getViewPosition();

        const newView = {
            x: pointerCanvas.x - (pointerCanvas.x - view.x) * (oldScale / newScale),
            y: pointerCanvas.y - (pointerCanvas.y - view.y) * (oldScale / newScale)
        };

        network.moveTo({
            scale: newScale,
            position: newView,
            animation: false
        });
    }, { passive: false });
}

// Wait until an element has real layout dimensions before invoking the
// callback. Critical for iframes that load while off-screen — without this
// vis-network can initialize against a 0x0 container and silently never
// render the canvas, even after the iframe later gets its real size.
function whenSized(el, cb, attempts) {
    attempts = attempts || 0;
    if (el.clientWidth > 0 && el.clientHeight > 0) { cb(); return; }
    if (attempts > 600) { cb(); return; } // ~10s ceiling, then try anyway
    requestAnimationFrame(function () { whenSized(el, cb, attempts + 1); });
}

// Tell the parent window we're done initializing this CLD. The article uses
// this signal to advance its per-iframe load queue precisely when the
// previous diagram has actually finished rendering.
function notifyParentReady(id) {
    try {
        if (window.parent && window.parent !== window) {
            window.parent.postMessage({ type: 'cld-ready', id: id || '' }, '*');
        }
    } catch (e) { /* cross-origin guard, ignore */ }
}

function initializeNetwork() {
    const container = document.getElementById('network');
    const options = {
        layout: {
            improvedLayout: false
        },
        physics: {
            enabled: false
        },
        interaction: {
            selectConnectedEdges: false,
            // Native zoomView is way too sensitive on trackpads. Disable it
            // and use the custom wheel handler attached below.
            zoomView: false,
            dragView: true
        },
        nodes: {
            shape: 'box',
            margin: 10,
            font: {
                size: 20,
                face: 'Arial'
            },
            borderWidth: 2,
            shadow: true,
            color: {
                background: 'white',
                border: 'dodgerblue',
                highlight: {
                    background: 'lightskyblue',
                    border: 'darkblue'
                }
            }
        },
        edges: {
            arrows: {
                to: { enabled: true, scaleFactor: 1.2 }
            },
            color: {
                color: 'gray',
                highlight: 'blue'
            },
            width: 2,
            smooth: {
                type: 'curvedCW',
                // changed from 0.3 to 0.4 to make curves more pronounced for two node loops
                roundness: 0.4
            },
            font: {
                size: 48,
                strokeWidth: 3,
                strokeColor: 'white'
            }
        }
    };

    // Defer vis-network init until the container actually has dimensions.
    // An iframe loaded while off-screen can hit this code with clientWidth=0,
    // and vis-network silently never recovers from a zero-size init.
    whenSized(container, function () {
        network = new vis.Network(container, {}, options);

        // Create the title overlay AFTER vis-network initializes — vis wipes
        // the container's contents on init, so an overlay placed in HTML would
        // vanish. #network is position:relative so this absolutely-positioned
        // div anchors to the diagram canvas in both iframe and fullscreen
        // modes.
        let overlay = document.getElementById('diagram-title-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'diagram-title-overlay';
            overlay.className = 'diagram-title-overlay';
        }
        container.appendChild(overlay);

        attachCustomZoom(container);
        attachTooltipRepositioner(container);

        attachResizeObserver(container);

        // If a CLD is already queued from a URL parameter, render it now.
        if (pendingURLLoad) {
            const fn = pendingURLLoad;
            pendingURLLoad = null;
            fn();
        }
    });
}

let pendingURLLoad = null;

function attachResizeObserver(container) {

    // Anti-loop guards: only react when the size genuinely changes — calling
    // setSize on identical dimensions can in rare cases re-fire the observer.
    if ('ResizeObserver' in window) {
        let hasFitted = false;
        let lastW = 0, lastH = 0;
        const ro = new ResizeObserver(entries => {
            if (!network) return;
            const rect = entries[0].contentRect;
            if (rect.width <= 0 || rect.height <= 0) return;
            if (rect.width === lastW && rect.height === lastH) return;
            lastW = rect.width; lastH = rect.height;
            network.setSize(rect.width + 'px', rect.height + 'px');
            network.redraw();
            if (cldData && !hasFitted) {
                network.fit({ animation: false });
                hasFitted = true;
            }
        });
        ro.observe(container);
    }

    network.on('click', function(params) {
        if (params.nodes.length > 0) {
            showNodeDetails(params.nodes[0]);
        } else if (params.edges.length > 0) {
            showEdgeDetails(params.edges[0]);
        } else {
            showDefaultDetails();
        }
    });
}

function loadCLD(data) {
    try {
        cldData = data;
        
        const title = (data.metadata && data.metadata.title) || '';
        const headerEl = document.getElementById('diagram-title');
        if (headerEl) headerEl.textContent = title;
        const overlayEl = document.getElementById('diagram-title-overlay');
        if (overlayEl) overlayEl.textContent = title;

        const visNodes = data.nodes.map(node => ({
            id: node.id,
            label: wrapText(node.label, 20),
            x: node.position.x,
            y: node.position.y,
            title: makeTooltip(node.description || `${node.label} (${node.type || 'variable'})`),
            originalData: node
        }));

        const visEdges = data.edges.map(edge => {
            const edgeConfig = {
                id: edge.id,
                from: edge.source,
                to: edge.target,
                label: edge.polarity === 'positive' ? '+' : '-',
                color: edge.polarity === 'positive' ? '#28a745' : '#dc3545',
                title: makeTooltip(edge.description || `${edge.polarity === 'positive' ? 'Positive (+)' : 'Negative (-)'} relationship from ${edge.source} to ${edge.target}`),
                originalData: edge,
            // Font configuration for edge labels
                font: {
                    size: 48,
                    strokeWidth: 2,
                    strokeColor: 'white'
                },
            };

            // Add custom curve direction if specified
            if (edge.curve) {
                edgeConfig.smooth = {
                    type: edge.curve.type || 'curvedCW',
                    roundness: edge.curve.roundness || 0.4
                };
            }

            return edgeConfig;
        });

        // Load Loops and annotation nodes
        // Convert loops with R or B in them to special nodes at the center of the loop
        // Note that the circle shape has a centering bug with the label
        if (data.loops) {
            data.loops.forEach(loop => {
                if (loop.position) {
                    visNodes.push({
                        id: 'loop_' + loop.id,
                        label: loop.id,
                        x: loop.position.x,
                        y: loop.position.y,
                        shape: 'ellipse',
                        size: 30,
                        color: {
                            background: loop.type === 'reinforcing' ? '#dc3545' : '#28a745',
                            border: 'black'
                        },
                        font: {
                            color: 'white',
                            size: 16,
                            face: 'Arial'
                        },
                        margin: {
                            left: Math.round(30 * 0.1)
                        },
                        title: makeTooltip(loop.description || `${loop.type === 'reinforcing' ? 'Reinforcing' : 'Balancing'} Loop: ${loop.label || loop.id}`),
                        originalData: loop,
                        isLoop: true
                    });
                }
            });
        }

        nodes = new vis.DataSet(visNodes);
        edges = new vis.DataSet(visEdges);

        network.setData({ nodes: nodes, edges: edges });

        // Center the diagram. Use no animation when embedded in an iframe so
        // the parent's load queue can advance immediately on the cld-ready
        // signal (see notifyParentReady below).
        const inIframe = (function () { try { return window.parent !== window; } catch (e) { return true; } })();
        network.fit({
            animation: inIframe ? false : { duration: 500, easingFunction: "easeInOutQuad" }
        });

        showDefaultDetails();

        // Tell the parent (article page) we are fully rendered. Wait one frame
        // so vis-network has actually painted before the parent advances.
        requestAnimationFrame(function () {
            notifyParentReady((data.metadata && data.metadata.id) || '');
        });

    } catch (error) {
        showError('Error loading CLD data: ' + error.message);
        notifyParentReady('error');
    }
}

function wrapText(text, maxLength) {
    if (text.length <= maxLength) return text;
    
    const words = text.split(' ');
    const lines = [];
    let currentLine = '';
    
    for (const word of words) {
        if ((currentLine + ' ' + word).length <= maxLength) {
            currentLine += (currentLine ? ' ' : '') + word;
        } else {
            if (currentLine) lines.push(currentLine);
            currentLine = word;
        }
    }
    if (currentLine) lines.push(currentLine);
    
    return lines.join('\n');
}

function showNodeDetails(nodeId) {
    const nodeData = nodes.get(nodeId);
    if (!nodeData) return;

    let content = '';
    
    if (nodeData.isLoop) {
        const loop = nodeData.originalData;
        content = `
            <div class="loop-info ${loop.type}">
                <h4>${loop.label || loop.id}</h4>
                <p><span class="label">Type:</span> ${loop.type === 'reinforcing' ? 'Reinforcing (R)' : 'Balancing (B)'}</p>
                <p><span class="label">Description:</span> ${loop.description || 'No description available'}</p>
                ${loop.behavior_pattern ? `<p><span class="label">Behavior Pattern:</span> ${loop.behavior_pattern}</p>` : ''}
                ${loop.path ? `<p><span class="label">Path:</span> ${loop.path.join(' → ')}</p>` : ''}
            </div>
        `;
    } else {
        const node = nodeData.originalData;
        content = `
            <h4>${node.label}</h4>
            <p><span class="label">Type:</span> ${node.type || 'variable'}</p>
            <p><span class="label">Description:</span> ${node.description || 'No description available'}</p>
            ${node.examples ? `<p><span class="label">Examples:</span> ${node.examples.join(', ')}</p>` : ''}
            ${node.measurement ? `<p><span class="label">Measurement:</span> ${node.measurement}</p>` : ''}
        `;
    }

    document.getElementById('details-content').innerHTML = content;
}

function showEdgeDetails(edgeId) {
    const edgeData = edges.get(edgeId);
    if (!edgeData) return;

    const edge = edgeData.originalData;
    const sourceNode = cldData.nodes.find(n => n.id === edge.source);
    const targetNode = cldData.nodes.find(n => n.id === edge.target);

    const content = `
        <h4>Causal Relationship</h4>
        <p><span class="label">From:</span> ${sourceNode ? sourceNode.label : edge.source}</p>
        <p><span class="label">To:</span> ${targetNode ? targetNode.label : edge.target}</p>
        <p><span class="label">Polarity:</span> ${edge.polarity === 'positive' ? 'Positive (+)' : 'Negative (-)'}</p>
        <p><span class="label">Description:</span> ${edge.description || 'No description available'}</p>
        ${edge.strength ? `<p><span class="label">Strength:</span> ${edge.strength}</p>` : ''}
        ${edge.delay && edge.delay.present ? `<p><span class="label">Delay:</span> ${edge.delay.duration || 'Present'}</p>` : ''}
    `;

    document.getElementById('details-content').innerHTML = content;
}

function showDefaultDetails() {
    let content = '<p>Click on a node, edge, or loop symbol to see details here.</p>';
    
    if (cldData) {
        content += `
            <h4>System Overview</h4>
            <p><span class="label">Archetype:</span> ${cldData.metadata.archetype || 'Not specified'}</p>
            <p><span class="label">Description:</span> ${cldData.metadata.description || 'No description available'}</p>
        `;
        
        if (cldData.loops && cldData.loops.length > 0) {
            content += '<h4>Feedback Loops</h4>';
            cldData.loops.forEach(loop => {
                content += `
                    <div class="loop-info ${loop.type}">
                        <strong>${loop.label || loop.id}</strong> (${loop.type === 'reinforcing' ? 'R' : 'B'})
                        <br>${loop.description || 'No description'}
                    </div>
                `;
            });
        }
    }

    document.getElementById('details-content').innerHTML = content;
}

function showError(message) {
    document.getElementById('details-content').innerHTML = `<div class="error">${message}</div>`;
}

async function loadSample(sampleName) {
    try {
        const data = await loadCLDFromFile(sampleName);
        loadCLD(data);
    } catch (error) {
        showError(error.message);
    }
}

async function initializeSampleButtons() {
    try {
        const examples = await loadExamplesList();
        const buttonsContainer = document.querySelector('.sample-buttons');
        buttonsContainer.innerHTML = '';
        
        examples.forEach(example => {
            const button = document.createElement('button');
            button.className = 'sample-btn';
            button.textContent = example.title;
            button.onclick = () => loadSample(example.id);
            buttonsContainer.appendChild(button);
        });
    } catch (error) {
        console.error('Error loading examples list:', error);
    }
}

// Build an updated copy of cldData with current network positions baked in.
// Returns null if no CLD is currently loaded.
function buildCLDWithCurrentPositions() {
    if (!cldData || !network) return null;

    // network.getPositions() returns { nodeId: {x, y}, ... } for every node
    // currently in the graph, including the synthetic loop_<id> annotation nodes.
    const livePositions = network.getPositions();

    // Deep-clone so we don't mutate the in-memory cldData (preserves clean reload)
    const updated = JSON.parse(JSON.stringify(cldData));

    if (Array.isArray(updated.nodes)) {
        updated.nodes.forEach(n => {
            const p = livePositions[n.id];
            if (p) {
                n.position = { x: Math.round(p.x), y: Math.round(p.y) };
            }
        });
    }

    if (Array.isArray(updated.loops)) {
        updated.loops.forEach(loop => {
            const p = livePositions['loop_' + loop.id];
            if (p) {
                loop.position = { x: Math.round(p.x), y: Math.round(p.y) };
            }
        });
    }

    if (updated.metadata) {
        updated.metadata.updated_date = new Date().toISOString();
    }

    return updated;
}

function downloadJSON(filename, data) {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function savePositions() {
    const updated = buildCLDWithCurrentPositions();
    if (!updated) {
        showError('No CLD loaded — nothing to save.');
        return;
    }
    const id = (updated.metadata && updated.metadata.id) || 'cld';
    downloadJSON(id + '.json', updated);
}

async function copyPositionsToClipboard() {
    const updated = buildCLDWithCurrentPositions();
    if (!updated) {
        showError('No CLD loaded — nothing to copy.');
        return;
    }
    const json = JSON.stringify(updated, null, 2);
    try {
        await navigator.clipboard.writeText(json);
        const btn = document.getElementById('copy-positions-btn');
        if (btn) {
            const orig = btn.textContent;
            btn.textContent = 'Copied!';
            setTimeout(() => { btn.textContent = orig; }, 1500);
        }
    } catch (err) {
        // Fallback: dump into the details panel for manual copy
        document.getElementById('details-content').innerHTML =
            '<p>Clipboard write failed. Copy the JSON below:</p>' +
            '<textarea style="width:100%;height:300px;font-family:monospace;font-size:12px;">' +
            json.replace(/</g, '&lt;') +
            '</textarea>';
    }
}

function wireUpControls() {
    const saveBtn = document.getElementById('save-positions-btn');
    if (saveBtn) saveBtn.addEventListener('click', savePositions);

    const copyBtn = document.getElementById('copy-positions-btn');
    if (copyBtn) copyBtn.addEventListener('click', copyPositionsToClipboard);

    const fileInput = document.getElementById('file-input');
    if (fileInput) fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const data = JSON.parse(e.target.result);
                loadCLD(data);
            } catch (error) {
                showError('Invalid JSON file: ' + error.message);
            }
        };
        reader.readAsText(file);
    });
}

// this gets all the URL parameters
// file is the name of the file to load without the .json suffix
// menu=true will show the menus (menus are hidden by default for iframe embedding)
// edit=true shows the same menus, including Save Positions and Copy Positions
function getURLParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

async function loadFileFromURL() {
    const filename = getURLParameter('file');
    if (!filename) {
        // Bare viewer with no file — still tell the parent we are "ready" so
        // the article's load queue does not stall waiting for us.
        notifyParentReady('empty');
        return;
    }
    try {
        // Remove .json extension if it was included in the URL parameter
        const cleanFilename = filename.replace('.json', '');
        const data = await loadCLDFromFile(cleanFilename);
        // The network may not exist yet — initializeNetwork() defers creation
        // until the container has dimensions (whenSized). Queue the render so
        // it runs as soon as the network is available.
        if (network) {
            loadCLD(data);
        } else {
            pendingURLLoad = function () { loadCLD(data); };
        }
    } catch (error) {
        showError(`Failed to load file from URL parameter: ${error.message}`);
        notifyParentReady('error');
    }
}

function checkMenuParameter() {
    const menu = getURLParameter('menu');
    // Default to false - menus hidden unless explicitly set to true.
    // edit=true also shows them, so the Save/Copy Positions buttons are
    // reachable with the same suffix every CLD in the skill supports.
    if (menu !== 'true' && getURLParameter('edit') !== 'true') {
        document.body.classList.add('menu-hidden');
    }
}

window.addEventListener('load', function() {
    initializeNetwork();
    initializeSampleButtons();
    wireUpControls();
    showDefaultDetails();

    // Check for menu parameter to hide UI elements
    checkMenuParameter();

    // Check for file parameter in URL and load it
    loadFileFromURL();
});
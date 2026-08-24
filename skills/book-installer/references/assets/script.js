// Learning Graph Viewer Script
// Loads and displays an interactive learning graph using vis-network

let network = null;
let allNodes = [];
let allEdges = [];
let groups = {};
let visibleGroups = new Set();

// Precomputed once at load — never change after that
let nodesWithDeps = new Set(); // set of node IDs that have outgoing edges
let groupCounts = {};          // { groupId: count } for legend labels

// CIS (Concept Impact Score) node-sizing configuration.
// Nodes use the 'box' shape, which vis-network auto-sizes to fit its label
// text -- the built-in nodes.scaling/value mechanism has NO visible effect
// on box-shaped nodes (verified empirically), so importance is instead
// conveyed by scaling font size and margin directly per node. Values are
// log-normalized (not raw CIS) because CIS is heavy-tailed: on a typical
// ~200-concept graph, roughly half of all concepts sit at the minimum CIS
// value of 1, and a linear scale would make that entire lower half
// indistinguishable while one or two hub concepts dominate the range.
const CIS_FONT_MIN = 12;
const CIS_FONT_MAX = 22;
const CIS_MARGIN_MIN = 4;
const CIS_MARGIN_MAX = 10;

// Returns a 0..1 normalized importance score for a raw CIS value, given the
// maximum CIS across the whole graph.
function cisNormalized(cis, maxCis) {
    if (!maxCis || maxCis <= 1) return 0;
    return Math.log(cis + 1) / Math.log(maxCis + 1);
}

// Load the learning graph data
async function loadGraph() {
    try {
        const response = await fetch('../../learning-graph/learning-graph.json');
        const data = await response.json();

        allNodes = data.nodes || [];
        groups = data.groups || {};

        // Assign explicit integer IDs to every edge at load time.
        allEdges = (data.edges || []).map((edge, i) => ({
            ...edge,
            id: edge.id !== undefined ? edge.id : i
        }));

        // Initialize all groups as visible
        Object.keys(groups).forEach(g => visibleGroups.add(g));

        // Precompute values that never change after load
        nodesWithDeps = new Set(allEdges.map(e => e.from));
        groupCounts = {};
        allNodes.forEach(n => {
            groupCounts[n.group] = (groupCounts[n.group] || 0) + 1;
        });

        // Size each node's font/margin by its Concept Impact Score, if present.
        // Older learning-graph.json files without a 'cis' field render at a
        // uniform size (cisNormalized returns 0 for undefined/1 values, so
        // every node lands at CIS_FONT_MIN -- no error, just no size variation).
        const maxCis = Math.max(1, ...allNodes.map(n => n.cis || 1));
        allNodes.forEach(n => {
            const t = cisNormalized(n.cis || 1, maxCis);
            n.font = { ...(n.font || {}), size: Math.round(CIS_FONT_MIN + t * (CIS_FONT_MAX - CIS_FONT_MIN)) };
            n.margin = Math.round(CIS_MARGIN_MIN + t * (CIS_MARGIN_MAX - CIS_MARGIN_MIN));
        });

        initializeNetwork();
        buildLegend();
        updateStats();
        setupSearch();
        setupControls();

    } catch (error) {
        console.error('Error loading learning graph:', error);
        document.getElementById('network').innerHTML =
            '<p style="color: red; padding: 20px;">Error loading learning graph. Make sure learning-graph.json exists at ../../learning-graph/learning-graph.json</p>';
    }
}

// Initialize the vis-network visualization
function initializeNetwork() {
    const container = document.getElementById('network');

    // Create nodes DataSet - colors are handled by the groups option
    const nodes = new vis.DataSet(allNodes);

    // Create edges DataSet — use allEdges which already have explicit IDs
    const edges = new vis.DataSet(allEdges.map(edge => ({
        ...edge,
        arrows: 'to',
        color: { color: '#888', opacity: 0.6 }
    })));

    const data = { nodes, edges };

    // Build vis-network groups configuration from JSON groups
    const visGroups = {};
    Object.entries(groups).forEach(([groupId, groupInfo]) => {
        visGroups[groupId] = {
            color: {
                background: groupInfo.color || 'lightgray',
                border: groupInfo.color || 'lightgray',
                highlight: {
                    background: groupInfo.color || 'lightgray',
                    border: '#333'
                },
                hover: {
                    background: groupInfo.color || 'lightgray',
                    border: '#666'
                }
            },
            font: {
                color: groupInfo.font?.color || 'black'
            }
        };
    });

    const options = {
        groups: visGroups,
        layout: {
            randomSeed: 42,
            improvedLayout: true
        },
        physics: {
            enabled: true,
            solver: 'forceAtlas2Based',
            forceAtlas2Based: {
                gravitationalConstant: -50,
                centralGravity: 0.01,
                springLength: 100,
                springConstant: 0.08,
                damping: 0.4,
                avoidOverlap: 0.5
            },
            stabilization: {
                enabled: true,
                iterations: 1000,
                updateInterval: 25
            }
        },
        nodes: {
            shape: 'box',
            margin: 4,
            font: {
                size: 14,
                face: 'Arial'
            },
            borderWidth: 2,
            shadow: true
        },
        edges: {
            smooth: {
                type: 'cubicBezier',
                forceDirection: 'horizontal',
                roundness: 0.4
            },
            width: 1.5
        },
        interaction: {
            hover: true,
            tooltipDelay: 200,
            zoomView: true,
            dragView: true
        }
    };

    network = new vis.Network(container, data, options);

    // Remove the loading message once the initial layout is computed.
    network.once('stabilizationIterationsDone', () => {
        const msg = document.getElementById('loading-message');
        if (msg) msg.remove();
    });

    // Turn off physics after 5 seconds to stop spinning
    setTimeout(() => {
        network.setOptions({ physics: { enabled: false } });
    }, 5000);

    // Re-enable physics when user starts dragging a node
    network.on('dragStart', function(params) {
        if (params.nodes.length > 0) {
            network.setOptions({ physics: { enabled: true } });
        }
    });

    // Turn off physics when user releases the node
    network.on('dragEnd', function(params) {
        if (params.nodes.length > 0) {
            setTimeout(() => {
                network.setOptions({ physics: { enabled: false } });
            }, 1000);
        }
    });

    // Handle node selection
    network.on('selectNode', function(params) {
        if (params.nodes.length > 0) {
            highlightNode(params.nodes[0]);
        }
    });
}

// Build the category legend
function buildLegend() {
    const legendContainer = document.getElementById('legend');
    legendContainer.innerHTML = '';

    Object.entries(groups).forEach(([groupId, groupInfo]) => {
        const count = groupCounts[groupId] || 0;

        const item = document.createElement('div');
        item.className = 'legend-item';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `group-${groupId}`;
        checkbox.checked = true;
        checkbox.addEventListener('change', () => toggleGroup(groupId, checkbox.checked));

        const colorBox = document.createElement('span');
        colorBox.className = 'color-box';
        colorBox.style.backgroundColor = groupInfo.color || 'lightgray';

        const label = document.createElement('label');
        label.htmlFor = `group-${groupId}`;
        label.textContent = `${groupInfo.classifierName || groupId} (${count})`;

        item.appendChild(checkbox);
        item.appendChild(colorBox);
        item.appendChild(label);
        legendContainer.appendChild(item);
    });
}

// Toggle visibility of a category group
function toggleGroup(groupId, visible) {
    if (visible) {
        visibleGroups.add(groupId);
    } else {
        visibleGroups.delete(groupId);
    }
    updateVisibility();
}

// Update node and edge visibility based on selected groups
function updateVisibility() {
    const visibleNodeIds = new Set(
        allNodes.filter(n => visibleGroups.has(n.group)).map(n => n.id)
    );

    const nodes = network.body.data.nodes;
    const edges = network.body.data.edges;

    // Batch update nodes — single DataSet.update() call triggers one redraw
    nodes.update(allNodes.map(node => ({
        id: node.id,
        hidden: !visibleGroups.has(node.group)
    })));

    // Batch update edges
    edges.update(allEdges.map(edge => ({
        id: edge.id,
        hidden: !(visibleNodeIds.has(edge.from) && visibleNodeIds.has(edge.to))
    })));

    updateStats(visibleNodeIds);
}

// Update statistics display
function updateStats(visibleNodeIds) {
    if (!visibleNodeIds) {
        visibleNodeIds = new Set(
            allNodes.filter(n => visibleGroups.has(n.group)).map(n => n.id)
        );
    }

    const visibleEdgeCount = allEdges.filter(
        e => visibleNodeIds.has(e.from) && visibleNodeIds.has(e.to)
    ).length;

    const foundationalCount = allNodes.filter(
        n => !nodesWithDeps.has(n.id) && visibleGroups.has(n.group)
    ).length;

    document.getElementById('visible-nodes').textContent = visibleNodeIds.size;
    document.getElementById('visible-edges').textContent = visibleEdgeCount;
    document.getElementById('foundational-nodes').textContent = foundationalCount;
}

// Setup search functionality
function setupSearch() {
    const searchInput = document.getElementById('search');
    const resultsContainer = document.getElementById('search-results');

    searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        resultsContainer.innerHTML = '';

        if (query.length < 2) {
            resultsContainer.style.display = 'none';
            return;
        }

        const matches = allNodes.filter(n =>
            n.label.toLowerCase().includes(query)
        ).slice(0, 10);

        if (matches.length === 0) {
            resultsContainer.style.display = 'none';
            return;
        }

        matches.forEach(node => {
            const item = document.createElement('div');
            item.className = 'search-result-item';

            const groupInfo = groups[node.group] || {};
            item.innerHTML = `
                <span class="result-label">${node.label}</span>
                <span class="result-category" style="background-color: ${groupInfo.color || 'lightgray'}">
                    ${groupInfo.classifierName || node.group}
                </span>
            `;

            item.addEventListener('click', () => {
                selectNode(node.id);
                searchInput.value = node.label;
                resultsContainer.style.display = 'none';
            });

            resultsContainer.appendChild(item);
        });

        resultsContainer.style.display = 'block';
    });

    // Hide results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
            resultsContainer.style.display = 'none';
        }
    });
}

// Select and focus on a node
function selectNode(nodeId) {
    network.selectNodes([nodeId]);
    network.focus(nodeId, {
        scale: 1.2,
        animation: {
            duration: 500,
            easingFunction: 'easeInOutQuad'
        }
    });
    highlightNode(nodeId);
}

// Highlight a node and its connections
function highlightNode(nodeId) {
    const connectedNodes = network.getConnectedNodes(nodeId);
    const connectedSet = new Set([nodeId, ...connectedNodes]);

    const nodes = network.body.data.nodes;
    nodes.update(allNodes.map(node => ({
        id: node.id,
        opacity: connectedSet.has(node.id) ? 1 : 0.3
    })));

    // Reset opacity after a delay — batched for performance
    setTimeout(() => {
        nodes.update(allNodes.map(node => ({ id: node.id, opacity: 1 })));
    }, 3000);
}

// Setup control buttons
function setupControls() {
    // Toggle sidebar
    document.getElementById('toggle-sidebar').addEventListener('click', function() {
        const sidebar = document.getElementById('sidebar');
        const content = document.getElementById('sidebar-content');
        sidebar.classList.toggle('collapsed');
        content.style.display = sidebar.classList.contains('collapsed') ? 'none' : 'block';
    });

    // Check all groups
    document.getElementById('check-all').addEventListener('click', function() {
        Object.keys(groups).forEach(groupId => {
            visibleGroups.add(groupId);
            document.getElementById(`group-${groupId}`).checked = true;
        });
        updateVisibility();
    });

    // Uncheck all groups
    document.getElementById('uncheck-all').addEventListener('click', function() {
        Object.keys(groups).forEach(groupId => {
            visibleGroups.delete(groupId);
            document.getElementById(`group-${groupId}`).checked = false;
        });
        updateVisibility();
    });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', loadGraph);

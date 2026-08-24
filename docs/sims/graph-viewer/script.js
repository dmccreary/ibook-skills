// Global variables
var nodes, edges, network;

// CIS (Concept Impact Score) node-sizing configuration.
// Nodes use the 'box' shape, which vis-network auto-sizes to fit its label
// text -- the built-in nodes.scaling/value mechanism has NO visible effect
// on box-shaped nodes (verified empirically), so importance is instead
// conveyed by scaling font size and margin directly per node. Values are
// log-normalized (not raw CIS) because CIS is heavy-tailed: roughly half of
// a typical concept graph sits at the minimum CIS value of 1, and a linear
// scale would make that entire lower half indistinguishable while one or
// two hub concepts dominate the range.
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

// ========== UTILITY FUNCTIONS ==========

function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  const sidebarContainer = document.getElementById("sidebar-container");
  const toggleButton = document.getElementById("toggle-button");

  if (sidebar.style.display === "none") {
    sidebar.style.display = "block";
    sidebarContainer.style.minWidth = "250px";
    toggleButton.innerHTML = "&#9776;";
  } else {
    sidebar.style.display = "none";
    sidebarContainer.style.minWidth = "auto";
    toggleButton.innerHTML = "&#8594;";
  }
}

// Function to update statistics
function updateStatistics() {
  var allNodes = nodes.get();
  var allEdges = edges.get();

  // Filter visible nodes
  var visibleNodes = allNodes.filter(node => !node.hidden);

  // Filter visible edges (both connected nodes must be visible)
  var visibleEdges = allEdges.filter(edge => {
    var fromNode = nodes.get(edge.from);
    var toNode = nodes.get(edge.to);
    return (!fromNode.hidden && !toNode.hidden);
  });

  var nodeCount = visibleNodes.length;
  var edgeCount = visibleEdges.length;

  // Find orphan nodes (nodes with no visible edges)
  var connectedNodeIds = new Set();
  visibleEdges.forEach(edge => {
    connectedNodeIds.add(edge.from);
    connectedNodeIds.add(edge.to);
  });
  var orphanNodes = visibleNodes.filter(node => !connectedNodeIds.has(node.id));
  var orphanCount = orphanNodes.length;

  // Update the HTML elements with the statistics
  document.getElementById('nodeCount').textContent = nodeCount;
  document.getElementById('edgeCount').textContent = edgeCount;
  document.getElementById('orphanCount').textContent = orphanCount;
}

// Function to toggle groups
function toggleGroup(groupName) {
  const visible = document.getElementById(`group${groupName}`).checked;
  nodes.update(
    nodes.get({ filter: node => node.group === groupName })
         .map(node => ({ id: node.id, hidden: !visible }))
  );
  updateStatistics();
}

// Function to check all groups
function checkAllGroups() {
  document.querySelectorAll('input[id^="group"]').forEach(cb => { cb.checked = true; });
  nodes.update(nodes.get().map(node => ({ id: node.id, hidden: false })));
}

// Function to uncheck all groups
function uncheckAllGroups() {
  document.querySelectorAll('input[id^="group"]').forEach(cb => { cb.checked = false; });
  nodes.update(nodes.get().map(node => ({ id: node.id, hidden: true })));
}

// Helper function to get readable color name
function getColorName(color) {
  const colorNames = {
    'red': 'Red',
    'orange': 'Orange',
    'gold': 'Gold',
    'yellow': 'Yellow',
    'green': 'Green',
    'cyan': 'Cyan',
    'blue': 'Blue',
    'navy': 'Navy',
    'indigo': 'Indigo',
    'violet': 'Violet',
    'purple': 'Purple',
    'magenta': 'Magenta',
    'gray': 'Gray',
    'grey': 'Grey',
    'brown': 'Brown',
    'teal': 'Teal',
    'black': 'Black',
    'white': 'White'
  };
  return colorNames[color.toLowerCase()] || color.charAt(0).toUpperCase() + color.slice(1);
}

// Helper function to get text color from group style or determine based on background
function getTextColorForBackground(backgroundColor, groupStyle) {
  // If group style has a font color defined, use it
  if (groupStyle && groupStyle.font && groupStyle.font.color) {
    return groupStyle.font.color;
  }

  // Fallback: determine based on background color
  const darkColors = ['red', 'green', 'blue', 'navy', 'indigo', 'violet', 'purple', 'magenta', 'gray', 'grey', 'brown', 'teal', 'black'];
  return darkColors.includes(backgroundColor.toLowerCase()) ? 'white' : 'black';
}

// Function to generate legend from groups data
function generateLegend(groups) {
  const legendContainer = document.getElementById('legend');
  legendContainer.innerHTML = ''; // Clear existing content

  // Iterate through groups and create legend items
  for (const [groupName, groupStyle] of Object.entries(groups)) {
    const item = document.createElement('div');
    item.className = 'legend-item';

    // Create checkbox
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = `group${groupName}`;
    checkbox.checked = true;
    checkbox.addEventListener('change', function() { toggleGroup(groupName); });

    // Create color swatch box
    const colorBox = document.createElement('span');
    colorBox.className = 'color-box';
    colorBox.style.backgroundColor = groupStyle.color || 'lightgray';

    // Create label
    const label = document.createElement('label');
    label.htmlFor = `group${groupName}`;
    label.textContent = groupStyle.classifierName || groupName;

    item.appendChild(checkbox);
    item.appendChild(colorBox);
    item.appendChild(label);
    legendContainer.appendChild(item);
  }
}

// Function to set metadata (title and description)
function setMetadata(metadata) {
  if (metadata && metadata.title) {
    const titleElement = document.getElementById('graph-title');
    if (titleElement) {
      titleElement.textContent = metadata.title;
    }

    // Update document title as well
    if (metadata.title) {
      document.title = metadata.title + ' - Learning Graph Viewer';
    }
  }
}

// ========== INITIALIZATION ==========

function initializeNetwork(graphData) {
  // Set metadata (title, description)
  if (graphData.metadata) {
    setMetadata(graphData.metadata);
  }

  // Generate legend from groups data
  if (graphData.groups) {
    generateLegend(graphData.groups);
  }

  // Size each node's font/margin by its Concept Impact Score, if present.
  // Older learning-graph.json files without a 'cis' field render at a
  // uniform size (cisNormalized returns 0 for undefined/1 values, so every
  // node lands at CIS_FONT_MIN -- no error, just no size variation).
  const maxCis = Math.max(1, ...graphData.nodes.map(n => n.cis || 1));
  graphData.nodes.forEach(n => {
    const t = cisNormalized(n.cis || 1, maxCis);
    n.font = { ...(n.font || {}), size: Math.round(CIS_FONT_MIN + t * (CIS_FONT_MAX - CIS_FONT_MIN)) };
    n.margin = Math.round(CIS_MARGIN_MIN + t * (CIS_MARGIN_MAX - CIS_MARGIN_MIN));
  });

  // Create DataSets from loaded data
  nodes = new vis.DataSet(graphData.nodes);
  edges = new vis.DataSet(graphData.edges);

  // Create a network
  var container = document.getElementById('mynetwork');

  // Provide the data in the vis format
  var data = {
    nodes: nodes,
    edges: edges
  };

  var options = {
    groups: graphData.groups || {},  // Apply group-based styling
    edges: {
      arrows: {
        to: { enabled: true, type: 'arrow', color: 'black', scaleFactor: 1 }
      },
      color: {
        color: 'black',
        inherit: false
      },
      width: 2,
      smooth: { type: 'continuous' }
    },
    physics: {
      solver: 'forceAtlas2Based',
      forceAtlas2Based: {
        springLength: 100
      }
    }
  };

  network = new vis.Network(container, data, options);

  // Initialize search functionality
  initializeSearch();

  // Update statistics after network is initialized
  updateStatistics();
}

function initializeSearch() {
  var searchInput = document.getElementById('search-input');
  var searchResults = document.getElementById('search-results');
  var searchContainer = document.getElementById('search-container');

  searchInput.addEventListener('input', function() {
    var query = this.value.toLowerCase();
    if (query === '') {
      searchResults.style.display = 'none';
      searchResults.innerHTML = '';
      return;
    }

    // Only search visible nodes
    var matches = nodes.get({
      filter: function (item) {
        return !item.hidden && item.label.toLowerCase().includes(query);
      }
    });

    if (matches.length > 0) {
      searchResults.innerHTML = '';
      matches.forEach(function(item) {
        var div = document.createElement('div');
        div.textContent = item.label + ' (' + item.group + ')';
        div.dataset.id = item.id;
        div.addEventListener('click', function() {
          var nodeId = parseInt(this.dataset.id);
          network.focus(nodeId, {
            animation: {
              duration: 500,
              easingFunction: 'easeInOutQuad'
            },
            scale: 1.5
          });
          network.selectNodes([nodeId]);
          searchResults.style.display = 'none';
          searchResults.innerHTML = '';
          searchInput.value = '';
        });
        searchResults.appendChild(div);
      });
      searchResults.style.display = 'block';
    } else {
      searchResults.innerHTML = '<div style="color: gray; padding: 8px;">No matches found</div>';
      searchResults.style.display = 'block';
    }
  });

  // Close the dropdown when clicking outside
  document.addEventListener('click', function(event) {
    if (!searchContainer.contains(event.target)) {
      searchResults.style.display = 'none';
      searchResults.innerHTML = '';
    }
  });
}

// ========== LOAD DATA AND START APPLICATION ==========

// Load the graph data from JSON file by going up to the learning-graph directory and reading the learning-graph.json file
// Adjust the path as necessary based on your directory structure
fetch('../../learning-graph/learning-graph.json')
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to load ../../learning-graph/learning-graph.json');
    }
    return response.json();
  })
  .then(graphData => {
    initializeNetwork(graphData);
  })
  .catch(error => {
    console.error('Error loading graph data:', error);
    document.getElementById('mynetwork').innerHTML =
      '<div style="padding: 20px; color: red;">Error loading graph data. Please check the console for details.</div>';
  });

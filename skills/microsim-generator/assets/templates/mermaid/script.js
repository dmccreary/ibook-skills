/* Mermaid MicroSim Interactive Script
   Handles hover interactions for the info panel

   IMPORTANT: Define nodeInfo object BEFORE loading this script:

   const nodeInfo = {
       'NodeId': {
           title: 'Node Title',
           description: 'Description shown on hover'
       },
       ...
   };
*/

// Get info panel element
const infoDisplay = document.getElementById('info-display');
const defaultContent = '<p class="info-placeholder">Hover over a node to see details</p>';

/**
 * Display node information in the info panel
 * @param {string} nodeId - The ID of the node to display
 */
function showNodeInfo(nodeId) {
    if (typeof nodeInfo !== 'undefined' && nodeInfo[nodeId]) {
        const info = nodeInfo[nodeId];
        infoDisplay.innerHTML = `
            <div class="info-title">${info.title}</div>
            <div class="info-content">${info.description}</div>
        `;
    }
}

/**
 * Clear the info panel back to default state
 */
function clearNodeInfo() {
    infoDisplay.innerHTML = defaultContent;
}

/**
 * Set up mouse event listeners on all Mermaid nodes
 */
function setupNodeInteractions() {
    const nodes = document.querySelectorAll('.node');
    nodes.forEach(node => {
        // Extract node ID from the element ID. Mermaid v11 emits
        // "mermaid-<timestamp>-flowchart-<NodeId>-<index>", so anchor on the
        // flowchart- segment and drop the trailing index rather than splitting
        // on the first dash.
        const nodeId = (node.id.match(/flowchart-(.+)-\d+$/) || [])[1];

        if (typeof nodeInfo !== 'undefined' && nodeInfo[nodeId]) {
            node.addEventListener('mouseenter', () => showNodeInfo(nodeId));
            node.addEventListener('mouseleave', clearNodeInfo);
        }
    });
}

/**
 * Robust polling: wait for Mermaid to finish rendering before setting up interactions
 */
function waitForMermaid() {
    const mermaidDiv = document.querySelector('.mermaid');
    const svg = mermaidDiv ? mermaidDiv.querySelector('svg') : null;
    const nodes = document.querySelectorAll('.node');

    if (svg && nodes.length > 0) {
        setupNodeInteractions();
    } else {
        // Check again after a short delay
        setTimeout(waitForMermaid, 100);
    }
}

// Start checking after initial load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(waitForMermaid, 100));
} else {
    setTimeout(waitForMermaid, 100);
}

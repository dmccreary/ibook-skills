const infoDisplay = document.getElementById('info-display');
const defaultContent = '<p class="info-placeholder">Hover over a node to see details</p>';

function showNodeInfo(nodeId) {
    if (typeof nodeInfo !== 'undefined' && nodeInfo[nodeId]) {
        const info = nodeInfo[nodeId];
        infoDisplay.innerHTML = `
            <div class="info-title">${info.title}</div>
            <div class="info-content">${info.description}</div>
        `;
    }
}

function clearNodeInfo() {
    infoDisplay.innerHTML = defaultContent;
}

function setupNodeInteractions() {
    const nodes = document.querySelectorAll('.node');
    nodes.forEach(node => {
        const nodeId = (node.id.match(/flowchart-(.+)-\d+$/) || [])[1];
        if (typeof nodeInfo !== 'undefined' && nodeInfo[nodeId]) {
            node.addEventListener('mouseenter', () => showNodeInfo(nodeId));
            node.addEventListener('mouseleave', clearNodeInfo);
        }
    });
}

function waitForMermaid() {
    const mermaidDiv = document.querySelector('.mermaid');
    const svg = mermaidDiv ? mermaidDiv.querySelector('svg') : null;
    const nodes = document.querySelectorAll('.node');

    if (svg && nodes.length > 0) {
        setupNodeInteractions();
    } else {
        setTimeout(waitForMermaid, 100);
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => setTimeout(waitForMermaid, 100));
} else {
    setTimeout(waitForMermaid, 100);
}

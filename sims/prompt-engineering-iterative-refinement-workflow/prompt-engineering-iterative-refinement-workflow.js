(function () {
  const info = {
    Goal: 'Define a precise educational generation target: concepts, audience, and quality expectations.',
    Draft: 'Draft the initial prompt with context, structure, and constraints.',
    Generate: 'Run generation to produce draft chapter content.',
    Evaluate: 'Assess output for concept coverage, level, structure, and pedagogy.',
    Gate: 'Decision gate using quality rubric thresholds.',
    Accept: 'If quality is sufficient, finalize and proceed.',
    Analyze: 'If quality is low, identify specific deficiencies.',
    Refine: 'Tighten prompt constraints and add corrective examples.',
    Loop: 'Repeat generation; typical convergence is 2-4 cycles.'
  };

  function init() {
    const main = document.querySelector('main');
    main.style.display = 'grid';
    main.style.gridTemplateColumns = '68% 32%';
    main.style.height = '600px';
    main.innerHTML = `
      <section style="padding:10px;background:#eef2ff;overflow:auto;">
        <div id="mmd" class="mermaid">
flowchart TD
  Goal(["Identify content generation goal"]):::plan --> Draft["Draft initial prompt with context"]:::plan
  Draft --> Generate["Generate content with AI"]:::gen
  Generate --> Evaluate["Evaluate output quality"]:::eval
  Evaluate --> Gate{"Meets quality standards?"}:::gate
  Gate -->|Yes| Accept(["Accept and finalize content"]):::done
  Gate -->|No| Analyze["Analyze deficiencies"]:::refine
  Analyze --> Refine["Refine prompt based on issues"]:::refine
  Refine --> Loop["Regenerate with improved prompt"]:::refine
  Loop --> Generate

  classDef plan fill:#3b82f6,stroke:#1e3a8a,color:#fff,font-size:16px
  classDef gen fill:#7c3aed,stroke:#4c1d95,color:#fff,font-size:16px
  classDef eval fill:#16a34a,stroke:#14532d,color:#fff,font-size:16px
  classDef gate fill:#fde047,stroke:#713f12,color:#111827,font-size:16px
  classDef refine fill:#f97316,stroke:#9a3412,color:#fff,font-size:16px
  classDef done fill:#f59e0b,stroke:#92400e,color:#111827,font-size:16px
  linkStyle default stroke:#334155,stroke-width:2px
        </div>
      </section>
      <section style="padding:12px;border-left:1px solid #cbd5e1;background:#f8fafc;">
        <h3 style="margin:0 0 10px 0;">Step Details</h3>
        <div id="panel" style="font-size:14px;line-height:1.5;color:#334155;">Hover a node for details.</div>
        <hr style="margin:12px 0;border:none;border-top:1px solid #e2e8f0;">
        <p style="margin:0;font-size:13px;color:#475569;">Typical convergence: 2-4 iterations.</p>
      </section>
    `;

    mermaid.initialize({ startOnLoad: false, theme: 'default', flowchart: { htmlLabels: true, useMaxWidth: true } });
    mermaid.run({ nodes: [document.getElementById('mmd')] }).then(() => {
      const panel = document.getElementById('panel');
      document.querySelectorAll('.node').forEach((n) => {
        const id = (n.id.match(/flowchart-(.+)-\d+$/) || [])[1];
        n.style.cursor = 'pointer';
        n.addEventListener('mouseenter', () => panel.textContent = info[id] || '');
        n.addEventListener('mouseleave', () => panel.textContent = 'Hover a node for details.');
      });
    });
  }

  window.addEventListener('DOMContentLoaded', init);
})();

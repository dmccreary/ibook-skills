(function () {
  const info = {
    Start: 'User invokes a skill command, e.g., /skill glossary-generator.',
    Locate: 'System searches project-local then global skill paths.',
    Found: 'If missing, fail fast and suggest /skills.',
    Err: 'Skill not found; user must choose an available skill.',
    Parse: 'Parse frontmatter: metadata and allowed tools.',
    Config: 'Apply tool restrictions and execution settings.',
    Load: 'Load markdown workflow instructions from SKILL.md.',
    Step: 'Execute workflow step(s) autonomously.',
    FS: 'Read/write files according to workflow steps.',
    More: 'Loop until all steps are complete.',
    Report: 'Generate completion summary and changed files.',
    End: 'Display output and recommended next actions.'
  };

  function init() {
    const main = document.querySelector('main');
    main.style.display = 'grid';
    main.style.gridTemplateColumns = '68% 32%';
    main.style.height = '640px';
    main.innerHTML = `
      <section style="padding:10px;background:#eef2ff;overflow:auto;">
        <div id="mmd" class="mermaid">
flowchart TD
  Start(["User types /skill skill-name"]):::user --> Locate["Locate SKILL.md"]:::system
  Locate --> Found{"Skill found?"}:::decision
  Found -->|No| Err(["Error: Skill not found"]):::user
  Found -->|Yes| Parse["Parse YAML frontmatter"]:::system
  Parse --> Config["Configure tool permissions"]:::system
  Config --> Load["Load workflow instructions"]:::exec
  Load --> Step["Execute Step N"]:::exec
  Step --> FS["Read/write files"]:::fs
  FS --> More{"More steps?"}:::decision
  More -->|Yes| Step
  More -->|No| Report["Generate completion report"]:::exec
  Report --> End(["Display results and next steps"]):::user

  classDef user fill:#2563eb,stroke:#1e3a8a,color:#fff,font-size:16px
  classDef system fill:#7c3aed,stroke:#4c1d95,color:#fff,font-size:16px
  classDef exec fill:#16a34a,stroke:#14532d,color:#fff,font-size:16px
  classDef fs fill:#f97316,stroke:#9a3412,color:#fff,font-size:16px
  classDef decision fill:#fde047,stroke:#713f12,color:#111827,font-size:16px
  linkStyle default stroke:#334155,stroke-width:2px
        </div>
      </section>
      <section style="padding:12px;border-left:1px solid #cbd5e1;background:#f8fafc;overflow:auto;">
        <h3 style="margin:0 0 10px 0;">Lifecycle Details</h3>
        <div id="panel" style="font-size:14px;line-height:1.5;color:#334155;">Hover a node for details.</div>
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

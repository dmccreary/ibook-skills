(function () {
  const info = {
    Root: 'Skill discovery checks both project and global locations.',
    Project: 'Project-local skills live in /project/.claude/skills/.',
    Global: 'Global skills live in ~/.claude/skills/ and are available everywhere.',
    Over: 'If the same skill exists in both locations, project-local wins.',
    Example: 'Example: quiz-generator in both places resolves to project-local version.'
  };

  function init() {
    const main = document.querySelector('main');
    main.style.display = 'grid';
    main.style.gridTemplateColumns = '68% 32%';
    main.style.height = '560px';
    main.innerHTML = `
      <section style="padding:10px;background:#eff6ff;overflow:auto;">
        <div id="mmd" class="mermaid">
flowchart TD
  Root["Skill Lookup"]:::neutral --> Project["/project/.claude/skills/\\nProject-Local Skills"]:::project
  Root --> Global["~/.claude/skills/\\nGlobal Skills"]:::global
  Project --> Over["Priority: Project > Global"]:::priority
  Global --> Over
  Over --> Example["If both define quiz-generator,\\nuse project-local version"]:::priority

  classDef global fill:#3b82f6,stroke:#1e3a8a,color:#fff,font-size:16px
  classDef project fill:#16a34a,stroke:#14532d,color:#fff,font-size:16px
  classDef priority fill:#f97316,stroke:#9a3412,color:#fff,font-size:16px
  classDef neutral fill:#64748b,stroke:#334155,color:#fff,font-size:16px
  linkStyle default stroke:#334155,stroke-width:2px
        </div>
      </section>
      <section style="padding:12px;border-left:1px solid #cbd5e1;background:#f8fafc;">
        <h3 style="margin:0 0 10px 0;">Directory Notes</h3>
        <div id="panel" style="font-size:14px;color:#334155;line-height:1.5;">Hover a node for details.</div>
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

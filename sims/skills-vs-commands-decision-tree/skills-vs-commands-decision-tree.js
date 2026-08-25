(function () {
  const info = {
    Q1: 'If the task has multiple sequential steps, a Skill is often better.',
    Q2: 'Cross-file read/write workflows are a strong Skill signal.',
    Q3: 'Validation, retries, and guardrails usually require workflow logic.',
    Q4: 'Reusable cross-project workflows should become Skills.',
    Cmd: 'Use Commands for simple prompt templates and one-shot actions.',
    Simple: 'Simple Skill can fit lightweight repeatable multi-step tasks.',
    Full: 'Create a full Skill for robust, reusable workflows.',
    Local: 'Use project-local Skill or command for single-project automation.'
  };

  function render() {
    const main = document.querySelector('main');
    main.style.display = 'grid';
    main.style.gridTemplateColumns = '68% 32%';
    main.style.height = '620px';
    main.innerHTML = `
      <section style="padding:10px;background:#f8fafc;overflow:auto;"><div id="mmd" class="mermaid">
flowchart TD
  Q1{"Need multiple sequential steps?"}:::d -->|No| Cmd(["Use a Command"]):::cmd
  Q1 -->|Yes| Q2{"Need read/write\nmultiple files?"}:::d
  Q2 -->|No| Cmd
  Q2 -->|Yes| Q3{"Need validation or\nerror handling?"}:::d
  Q3 -->|No| Simple(["Simple Skill\nmight work"]):::mid
  Q3 -->|Yes| Q4{"Reused across\nmultiple projects?"}:::d
  Q4 -->|Yes| Full(["Create a Skill\nwith full workflow"]):::skill
  Q4 -->|No| Local(["Project-local\nSkill or Command"]):::mid

  classDef d fill:#fde047,stroke:#713f12,color:#111827,font-size:16px
  classDef skill fill:#16a34a,stroke:#14532d,color:#fff,font-size:16px
  classDef cmd fill:#eab308,stroke:#92400e,color:#111827,font-size:16px
  classDef mid fill:#f97316,stroke:#9a3412,color:#fff,font-size:16px
  linkStyle default stroke:#334155,stroke-width:2px
      </div></section>
      <section style="padding:12px;border-left:1px solid #e2e8f0;background:#fff;">
        <h3 style="margin:0 0 8px 0;">Decision Notes</h3>
        <div id="panel" style="font-size:14px;line-height:1.5;color:#334155;">Hover a node for guidance.</div>
      </section>
    `;

    mermaid.initialize({ startOnLoad:false, theme:'default', flowchart:{htmlLabels:true,useMaxWidth:true} });
    mermaid.run({nodes:[document.getElementById('mmd')]}).then(()=>{
      const panel=document.getElementById('panel');
      document.querySelectorAll('.node').forEach((n)=>{
        const id=(n.id.match(/flowchart-(.+)-\d+$/) || [])[1];
        n.style.cursor='pointer';
        n.addEventListener('mouseenter',()=>panel.textContent=info[id]||'');
        n.addEventListener('mouseleave',()=>panel.textContent='Hover a node for guidance.');
      });
    });
  }

  window.addEventListener('DOMContentLoaded', render);
})();

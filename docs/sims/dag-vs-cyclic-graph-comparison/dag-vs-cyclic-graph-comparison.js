(function () {
  const info = {
    V_A: 'DAG node A (foundational).',
    V_B: 'DAG node B depends on A.',
    V_C: 'DAG node C depends on A and B. This is still acyclic.',
    I_A: 'Cycle node A.',
    I_B: 'Cycle node B.',
    I_C: 'Cycle node C.',
    V_OK: 'Valid DAG can be topologically ordered and taught coherently.',
    I_BAD: 'Cycle makes prerequisite ordering impossible.'
  };

  function init() {
    const main = document.querySelector('main');
    main.style.display = 'grid';
    main.style.gridTemplateColumns = '68% 32%';
    main.style.height = '560px';
    main.innerHTML = `
      <section style="padding:10px;background:#f8fafc;overflow:auto;"><div id="mmd" class="mermaid">
flowchart LR
  subgraph L["Valid Learning Graph (DAG)"]
    V_A[A]:::good --> V_B[B]:::good --> V_C[C]:::good
    V_A --> V_C
    V_OK["Pedagogically sound"]:::goodNote
  end

  subgraph R["Invalid Learning Graph (Contains Cycle)"]
    I_A[A]:::bad --> I_B[B]:::bad --> I_C[C]:::bad --> I_A
    I_BAD["Logically impossible"]:::badNote
  end

  classDef good fill:#22c55e,stroke:#166534,color:#fff,font-size:16px
  classDef bad fill:#ef4444,stroke:#991b1b,color:#fff,font-size:16px
  classDef goodNote fill:#dcfce7,stroke:#15803d,color:#14532d,font-size:15px
  classDef badNote fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d,font-size:15px
  linkStyle default stroke:#1f2937,stroke-width:2px
      </div></section>
      <section style="padding:12px;border-left:1px solid #e2e8f0;background:#fff;">
        <h3 style="margin:0 0 8px 0;">Comparison Notes</h3>
        <div id="panel" style="font-size:14px;color:#334155;line-height:1.5;">Hover a node for details.</div>
        <hr style="margin:10px 0;border:none;border-top:1px solid #e2e8f0;">
        <p style="margin:0;font-size:13px;color:#475569;">DAG supports topological order; cycle violates prerequisite logic.</p>
      </section>
    `;

    mermaid.initialize({startOnLoad:false,theme:'default',flowchart:{htmlLabels:true,useMaxWidth:true}});
    mermaid.run({nodes:[document.getElementById('mmd')]}).then(()=>{
      const panel = document.getElementById('panel');
      document.querySelectorAll('.node').forEach((n)=>{
        const id = (n.id.match(/flowchart-(.+)-\d+$/) || [])[1];
        n.style.cursor='pointer';
        n.addEventListener('mouseenter',()=>panel.textContent=info[id] || '');
        n.addEventListener('mouseleave',()=>panel.textContent='Hover a node for details.');
      });
    });
  }

  window.addEventListener('DOMContentLoaded', init);
})();

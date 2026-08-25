(function () {
  const nodeInfo = {
    Q1: 'If B is defined using A, A should be prerequisite.',
    Q2: 'Framework-level dependency often indicates prerequisite.',
    Q3: 'If B procedure includes A as substep, A is prerequisite.',
    Q4: 'Example/case dependency suggests likely prerequisite.',
    Q5: 'Related-but-independent topics should not be forced into edges.',
    Strong: 'Add edge A -> B.',
    Likely: 'Add edge A -> B, mark for review.',
    None: 'No prerequisite edge required.',
    Consider: 'Optional edge based on instructional flow benefit.'
  };

  function init() {
    const main = document.querySelector('main');
    main.style.display='grid';
    main.style.gridTemplateColumns='68% 32%';
    main.style.height='640px';
    main.innerHTML = `
      <section style="padding:10px;background:#f8fafc;overflow:auto;"><div id="mmd" class="mermaid">
flowchart TD
  Q1{"Is B defined using A?"}:::d -->|Yes| Strong(["A is prerequisite to B"]):::strong
  Q1 -->|No| Q2{"Does B require A's\nframework/principles?"}:::d
  Q2 -->|Yes| Likely(["A is likely\nprerequisite to B"]):::likely
  Q2 -->|No| Q3{"Does B procedure include\nA as a substep?"}:::d
  Q3 -->|Yes| Strong
  Q3 -->|No| Q4{"Does B build on\nexamples from A?"}:::d
  Q4 -->|Yes| Likely
  Q4 -->|No| Q5{"Are A and B related but\npedagogically independent?"}:::d
  Q5 -->|Yes| None(["No prerequisite\nrelationship"]):::none
  Q5 -->|No| Consider(["Consider edge A -> B\nif learners benefit"]):::consider

  classDef d fill:#fde047,stroke:#713f12,color:#111827,font-size:16px
  classDef strong fill:#22c55e,stroke:#166534,color:#fff,font-size:16px
  classDef likely fill:#eab308,stroke:#92400e,color:#111827,font-size:16px
  classDef consider fill:#f97316,stroke:#9a3412,color:#fff,font-size:16px
  classDef none fill:#94a3b8,stroke:#475569,color:#111827,font-size:16px
  linkStyle default stroke:#1f2937,stroke-width:2px
      </div></section>
      <section style="padding:12px;border-left:1px solid #e2e8f0;background:#fff;overflow:auto;">
        <h3 style="margin:0 0 10px 0;">Decision Detail</h3>
        <div id="panel" style="font-size:14px;color:#334155;line-height:1.5;">Hover a node for details.</div>
      </section>
    `;

    mermaid.initialize({startOnLoad:false,theme:'default',flowchart:{htmlLabels:true,useMaxWidth:true}});
    mermaid.run({nodes:[document.getElementById('mmd')]}).then(()=>{
      const panel=document.getElementById('panel');
      document.querySelectorAll('.node').forEach((n)=>{
        const id=(n.id.match(/flowchart-(.+)-\d+$/) || [])[1];
        n.style.cursor='pointer';
        n.addEventListener('mouseenter',()=>panel.textContent=nodeInfo[id] || '');
        n.addEventListener('mouseleave',()=>panel.textContent='Hover a node for details.');
      });
    });
  }

  window.addEventListener('DOMContentLoaded', init);
})();

(function(){
  const info={
    Start:'Start with flat list of 200 concepts.',
    Found:'Mark foundational concepts (zero dependencies).',
    Chain:'Add sequential A->B->C chains.',
    Conv:'Add convergent prerequisites A->C<-B.',
    Trans:'Remove transitive redundancies (A->C when A->B->C exists).',
    Dag:'Validate DAG and detect cycles.',
    Fix:'Resolve cycles by splitting or setting primacy.',
    Strength:'Validate dependency strength and remove weak edges.',
    End:'Target output: valid DAG with ~180-220 edges.'
  };
  function init(){
    const main=document.querySelector('main');
    main.style.display='grid'; main.style.gridTemplateColumns='68% 32%'; main.style.height='980px';
    main.innerHTML=`<section style="padding:10px;background:#f8fafc;overflow:visible;"><div id="mmd" class="mermaid">
flowchart TD
  Start(["200 concepts enumerated"]):::blue --> Found["Identify foundational concepts\n(10-15 marked)"]:::blue
  Found --> Chain["Map sequential chains\n(+30-40 edges)"]:::green
  Chain --> Conv["Map convergent dependencies\n(+40-60 edges)"]:::green
  Conv --> Trans["Remove transitive redundancies\n(-10-20 edges)"]:::orange
  Trans --> Dag{"DAG validation:\ncycles detected?"}:::purple
  Dag -->|Yes| Fix["Resolve cycles\n(split/primacy)"]:::purple
  Fix --> Dag
  Dag -->|No| Strength["Validate dependency strengths\n(-5-10 weak edges)"]:::orange
  Strength --> End(["Valid DAG\n(180-220 dependencies)"]):::green

  classDef blue fill:#3b82f6,stroke:#1e3a8a,color:#fff,font-size:16px
  classDef green fill:#22c55e,stroke:#166534,color:#fff,font-size:16px
  classDef orange fill:#f97316,stroke:#9a3412,color:#fff,font-size:16px
  classDef purple fill:#8b5cf6,stroke:#5b21b6,color:#fff,font-size:16px
  linkStyle default stroke:#1f2937,stroke-width:2px
    </div></section>
    <section id="notes" style="padding:12px;border-left:1px solid #e2e8f0;background:#fff;overflow:visible;">
      <h3 style="margin:0 0 8px 0;">Workflow Notes</h3>
      <div id="panelWrap" style="position:relative;height:920px;">
        <div id="panel" style="position:absolute;left:0;right:0;top:8px;font-size:14px;color:#334155;line-height:1.5;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px;">Hover a node for details.</div>
      </div>
    </section>`;

    mermaid.initialize({startOnLoad:false,theme:'default',flowchart:{htmlLabels:true,useMaxWidth:true}});
    mermaid.run({nodes:[document.getElementById('mmd')]}).then(()=>{
      const panel=document.getElementById('panel');
      const panelWrap=document.getElementById('panelWrap');
      function positionPanel(evt){
        const r=panelWrap.getBoundingClientRect();
        const panelH=panel.offsetHeight||120;
        const y=evt.clientY-r.top-20;
        const top=Math.max(8,Math.min(r.height-panelH-8,y));
        panel.style.top=`${top}px`;
      }
      document.querySelectorAll('.node').forEach((n)=>{
        const id=(n.id.match(/flowchart-(.+)-\d+$/) || [])[1];
        n.style.cursor='pointer';
        n.addEventListener('mouseenter',(evt)=>{panel.textContent=info[id]||''; positionPanel(evt);});
        n.addEventListener('mousemove',(evt)=>positionPanel(evt));
        n.addEventListener('mouseleave',()=>panel.textContent='Hover a node for details.');
      });
    });
  }
  window.addEventListener('DOMContentLoaded',init);
})();

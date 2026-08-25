(function () {
  const info = {
    Topic: 'Main topic comes from course description.',
    Components: 'Identify structural components of the topic.',
    Relations: 'Identify relationships/properties between components.',
    Procedures: 'Identify operations learners perform.',
    Standards: 'Identify conventions, formats, and rules.',
    Result: 'Typical expansion: 1 topic -> 12-15 atomic concepts.'
  };

  function init() {
    const main=document.querySelector('main');
    main.style.display='grid';
    main.style.gridTemplateColumns='68% 32%';
    main.style.height='620px';
    main.innerHTML=`
      <section style="padding:10px;background:#f8fafc;overflow:auto;"><div id="mmd" class="mermaid">
flowchart TD
  Topic(["Learning Graphs\n(Main Topic)"]):::topic --> Components["Identify core components\n(3-5 concepts)"]:::components
  Components --> Relations["Identify relationships\nand properties\n(2-4 concepts)"]:::relations
  Relations --> Procedures["Identify procedures\nand operations\n(2-3 concepts)"]:::procedures
  Procedures --> Standards["Identify standards\nand conventions\n(2-3 concepts)"]:::standards
  Standards --> Result(["12-15 atomic concepts\nfrom one topic"]):::result

  classDef topic fill:#7c3aed,stroke:#4c1d95,color:#fff,font-size:16px
  classDef components fill:#3b82f6,stroke:#1e3a8a,color:#fff,font-size:16px
  classDef relations fill:#22c55e,stroke:#166534,color:#fff,font-size:16px
  classDef procedures fill:#f97316,stroke:#9a3412,color:#fff,font-size:16px
  classDef standards fill:#eab308,stroke:#a16207,color:#111827,font-size:16px
  classDef result fill:#111827,stroke:#334155,color:#fff,font-size:16px
  linkStyle default stroke:#1f2937,stroke-width:2px
      </div></section>
      <section style="padding:12px;border-left:1px solid #e2e8f0;background:#fff;">
        <h3 style="margin:0 0 8px 0;">Expansion Notes</h3>
        <div id="panel" style="font-size:14px;line-height:1.5;color:#334155;">Hover a node for details.</div>
        <hr style="margin:10px 0;border:none;border-top:1px solid #e2e8f0;">
        <p style="margin:0;font-size:13px;color:#475569;">Repeat this process across 20-30 topics to build a full learning graph.</p>
      </section>
    `;

    mermaid.initialize({startOnLoad:false,theme:'default',flowchart:{htmlLabels:true,useMaxWidth:true}});
    mermaid.run({nodes:[document.getElementById('mmd')]}).then(()=>{
      const panel=document.getElementById('panel');
      document.querySelectorAll('.node').forEach((n)=>{
        const id=(n.id.match(/flowchart-(.+)-\d+$/) || [])[1];
        n.style.cursor='pointer';
        n.addEventListener('mouseenter',()=>panel.textContent=info[id] || '');
        n.addEventListener('mouseleave',()=>panel.textContent='Hover a node for details.');
      });
    });
  }

  window.addEventListener('DOMContentLoaded', init);
})();

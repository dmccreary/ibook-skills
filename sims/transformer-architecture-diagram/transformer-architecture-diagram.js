(function () {
  const nodeInfo = {
    Tok: "Token embeddings map input tokens into dense vectors. Example tokens: Using, Claude, Skills.",
    Pos: "Positional encoding injects sequence order information into token vectors.",
    QKV: "Queries, keys, and values are projected from input representations.",
    Attn: "Multi-head self-attention lets each token attend to all others.",
    AddNorm1: "Residual connection + layer normalization stabilizes deep training.",
    FFN: "Feed-forward network applies position-wise nonlinear transformation.",
    AddNorm2: "Second residual + normalization block after FFN.",
    Out: "Output layer maps hidden states to next-token probability distribution.",
    Heads: "Different heads capture syntax, semantics, and long-range dependencies.",
    Innov: "Self-attention is the key innovation enabling parallel sequence modeling."
  };

  function render() {
    document.body.style.margin = "0";
    const main = document.querySelector("main");
    main.style.display = "grid";
    main.style.gridTemplateColumns = "68% 32%";
    main.style.height = "560px";

    main.innerHTML = `
      <section style="padding:10px;background:#eff6ff;overflow:auto;">
        <div class="mermaid" id="mmd">
flowchart TD
  Tok["Token Embeddings\\n[Using, Claude, Skills]"]:::embed --> Pos["Positional Encoding"]:::embed
  Pos --> QKV["Q, K, V Projections"]:::attn
  QKV --> Attn["Multi-Head Self-Attention"]:::attn
  Attn --> AddNorm1["Add & LayerNorm"]:::norm
  AddNorm1 --> FFN["Feed-Forward Network"]:::ffn
  FFN --> AddNorm2["Add & LayerNorm"]:::norm
  AddNorm2 --> Out["Output: Next Token Probabilities"]:::out

  Pos -. residual .-> AddNorm1
  AddNorm1 -. residual .-> AddNorm2
  Attn --> Heads["Attention Heads Focus Patterns"]:::attn
  Heads --> Innov["Key Innovation:\\nSelf-Attention"]:::note

  classDef embed fill:#3b82f6,stroke:#1e3a8a,color:#fff,font-size:16px
  classDef attn fill:#7c3aed,stroke:#4c1d95,color:#fff,font-size:16px
  classDef ffn fill:#16a34a,stroke:#14532d,color:#fff,font-size:16px
  classDef norm fill:#cbd5e1,stroke:#334155,color:#111827,font-size:16px
  classDef out fill:#f97316,stroke:#7c2d12,color:#fff,font-size:16px
  classDef note fill:#fde047,stroke:#713f12,color:#111827,font-size:16px
  linkStyle default stroke:#334155,stroke-width:2px
        </div>
      </section>
      <section style="padding:12px;border-left:1px solid #e2e8f0;background:#f8fafc;overflow:auto;">
        <h3 style="margin:0 0 8px 0;">Transformer Components</h3>
        <div id="info" style="font-size:14px;line-height:1.5;color:#334155;">Hover a node to see details.</div>
        <hr style="margin:10px 0;border:none;border-top:1px solid #e2e8f0;">
        <p style="margin:0;font-size:13px;color:#475569;">Learned parameters: embeddings, QKV projections, attention weights, FFN weights.</p>
        <p style="margin:8px 0 0 0;font-size:13px;color:#475569;">Fixed component: sinusoidal positional encoding (common variant).</p>
      </section>
    `;

    mermaid.initialize({ startOnLoad: false, theme: "default", flowchart: { htmlLabels: true, useMaxWidth: true } });
    mermaid.run({ nodes: [document.getElementById("mmd")] }).then(() => {
      const info = document.getElementById("info");
      document.querySelectorAll('.node').forEach((node) => {
        const id = (node.id.match(/flowchart-(.+)-\d+$/) || [])[1];
        node.style.cursor = 'pointer';
        node.addEventListener('mouseenter', () => {
          info.textContent = nodeInfo[id] || "Component detail unavailable.";
        });
        node.addEventListener('mouseleave', () => {
          info.textContent = "Hover a node to see details.";
        });
      });
    });
  }

  window.addEventListener("DOMContentLoaded", render);
})();

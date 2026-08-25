(function () {
  const nodeInfo = {
    Start: "Example prompt: 'Generate content for Chapter 3 on learning graphs'.",
    Analyze: "Claude Code reads project structure and key context files.",
    Execute: "Workflow in SKILL.md is executed step-by-step.",
    Read: "Templates, references, and existing chapter files are loaded.",
    NeedExt: "Decision point: local-only context or external research needed?",
    Fetch: "Web/tool fetch retrieves current docs or external references.",
    Local: "Continue using only project-local resources.",
    Generate: "Generate markdown, code, diagrams, and config changes.",
    Write: "Write/modify files in the local repository.",
    Verify: "Validate requirements, coverage, and quality checks.",
    End: "Report output files, summaries, and follow-up actions."
  };

  function init() {
    document.body.style.margin = "0";
    const main = document.querySelector("main");
    main.style.display = "grid";
    main.style.gridTemplateColumns = "68% 32%";
    main.style.height = "600px";

    main.innerHTML = `
      <section style="padding:10px;background:#eef2ff;overflow:auto;">
        <div class="mermaid" id="workflowMermaid">
flowchart TD
  subgraph User[User / Developer]
    Start(["User initiates task via prompt"]):::user
    End(["Report results to user"]):::user
  end

  subgraph Claude[Claude Code Interface]
    Analyze["Analyze project structure"]:::claude
    Execute["Execute skill workflow"]:::claude
    Read["Read necessary files"]:::claude
    NeedExt{"Need external information?"}:::decision
    Fetch["Fetch web resources"]:::external
    Local["Proceed with local files"]:::claude
    Generate["Generate content"]:::claude
    Verify["Verify completeness"]:::claude
  end

  subgraph FS[Local File System]
    Write["Write files to project"]:::fs
  end

  Start --> Analyze --> Execute --> Read --> NeedExt
  NeedExt -->|Yes| Fetch --> Generate
  NeedExt -->|No| Local --> Generate
  Generate --> Write --> Verify --> End

  classDef user fill:#2563eb,stroke:#1e3a8a,color:#fff,font-size:16px
  classDef claude fill:#7c3aed,stroke:#4c1d95,color:#fff,font-size:16px
  classDef fs fill:#16a34a,stroke:#14532d,color:#fff,font-size:16px
  classDef external fill:#f97316,stroke:#9a3412,color:#fff,font-size:16px
  classDef decision fill:#fde047,stroke:#713f12,color:#111827,font-size:16px
  linkStyle default stroke:#334155,stroke-width:2px
        </div>
      </section>
      <section style="padding:12px;border-left:1px solid #e2e8f0;background:#f8fafc;overflow:auto;">
        <h3 style="margin:0 0 10px 0;">Workflow Details</h3>
        <div id="info" style="font-size:14px;line-height:1.5;color:#334155;">Hover a node to see details.</div>
        <hr style="margin:12px 0;border:none;border-top:1px solid #e2e8f0;">
        <p style="margin:0;font-size:13px;color:#475569;">Color map: Blue=User, Purple=Claude processing, Green=File operations, Orange=External resources.</p>
      </section>
    `;

    mermaid.initialize({ startOnLoad: false, theme: "default", flowchart: { htmlLabels: true, useMaxWidth: true } });
    mermaid.run({ nodes: [document.getElementById("workflowMermaid")] }).then(() => {
      const info = document.getElementById("info");
      document.querySelectorAll('.node').forEach((node) => {
        const id = (node.id.match(/flowchart-(.+)-\d+$/) || [])[1];
        node.style.cursor = 'pointer';
        node.addEventListener('mouseenter', () => {
          info.textContent = nodeInfo[id] || "Workflow step detail unavailable.";
        });
        node.addEventListener('mouseleave', () => {
          info.textContent = "Hover a node to see details.";
        });
      });
    });
  }

  window.addEventListener("DOMContentLoaded", init);
})();

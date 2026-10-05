// The Eight-Phase Verified Infographic Pipeline - Mermaid flowchart
// CANVAS_HEIGHT: 535
// The eight ordered phases that separate claim verification (text) from image
// rendering (pixels). Phases 1-6 are text-only work, phase 7 is the single
// image-model call, and phase 8 audits the rendered image.
// Every node has a Mermaid `click` directive wired to showInfo(), which fills
// the shared infobox panel beside the diagram. Previous / Next buttons step
// through the phases in order, and the panel lists the audit-trail files that
// exist after each phase.
//
// Phase content follows references/verified-infographic-guide.md in the
// microsim-generator skill. The guide's own phase names are shown in the
// panel next to this book's concept names.

// ---------------------------------------------------------------------------
// Diagram definition (top-to-bottom Mermaid flowchart)
// Edge order: 0..6 the sequence P1-->P2 ... P7-->P8, 7 the dashed P3-.->P1
// ---------------------------------------------------------------------------
const DIAGRAM = `flowchart TD
    subgraph TextOnly["Text only: no image model is called"]
        P1("1. Claim Planning"):::textPhase
        P2("2. Source Discovery"):::textPhase
        P3("3. Per-Claim Verification"):::textPhase
        P4("4. Verification Report"):::textPhase
        P5("5. Layout Specification Lock"):::lockPhase
        P6("6. Verbatim Text Prompt"):::textPhase
    end
    P7("7. Image Generation (single call)"):::imagePhase
    P8("8. Rendered Image Audit"):::auditPhase

    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
    P5 --> P6
    P6 --> P7
    P7 --> P8
    P3 -.->|"reject:<br/>revise"| P1

    click P1 call showInfo("P1")
    click P2 call showInfo("P2")
    click P3 call showInfo("P3")
    click P4 call showInfo("P4")
    click P5 call showInfo("P5")
    click P6 call showInfo("P6")
    click P7 call showInfo("P7")
    click P8 call showInfo("P8")

    classDef textPhase fill:#00796b,stroke:#004d40,stroke-width:2px,color:#ffffff,font-size:16px
    classDef lockPhase fill:#ffc107,stroke:#8a5a00,stroke-width:2px,color:#2b1d00,font-size:16px
    classDef imagePhase fill:#bf360c,stroke:#7f2105,stroke-width:3px,color:#ffffff,font-size:16px
    classDef auditPhase fill:#2e7d32,stroke:#1b5e20,stroke-width:2px,color:#ffffff,font-size:16px

    style TextOnly fill:#e0f2f1,stroke:#00796b,stroke-width:1px,stroke-dasharray:5 4,color:#004d40

    linkStyle default stroke:#455a64,stroke-width:2px
    linkStyle 7 stroke:#c62828,stroke-width:2px,stroke-dasharray:6 4
`;

// ---------------------------------------------------------------------------
// Infobox content, in pipeline order.
// "file" is the audit-trail file the phase adds to docs/posters/<slug>/.
// ---------------------------------------------------------------------------
const PHASES = [
  {
    id: 'P1', title: 'Claim Planning', kind: 'text',
    guide: 'Phase 1, Intake and Claim Planning',
    definition: 'The initial stage listing every factual assertion a planned poster will make, before any source is consulted.',
    detail: 'The plan lists 5 to 10 claims. Each records its subject, metric type, polarity, and how prominent it should be.',
    file: '01-claim-plan.yaml'
  },
  {
    id: 'P2', title: 'Source Discovery', kind: 'text',
    guide: 'Phase 2, Source Discovery',
    definition: 'The stage locating authoritative material that could support each planned assertion.',
    detail: 'Each claim gets at least two independent searches. Every candidate source is recorded with its authors, year, address, and a quoted sentence.',
    file: null
  },
  {
    id: 'P3', title: 'Per-Claim Verification', kind: 'text',
    guide: 'Phase 3, Verification and Classification',
    definition: 'Each claim is checked against its sources and sorted into one of four buckets: verified, directional, qualitative-only, or rejected.',
    detail: 'A rejected claim never reaches the image. It is removed or replaced, which sends the work back to the claim plan (the dashed arrow).',
    file: '02-verification-report.md'
  },
  {
    id: 'P4', title: 'Verification Report', kind: 'text',
    guide: 'Phase 4, User Checkpoint (mandatory)',
    definition: 'The record showing each planned assertion, its supporting quotation, and whether it passed, was softened, or was removed.',
    detail: 'The report is shown to the author, and nothing proceeds without explicit approval. The guide calls this the most important safety checkpoint in the pipeline.',
    file: null
  },
  {
    id: 'P5', title: 'Layout Specification Lock', kind: 'lock',
    guide: 'Phase 5, Layout Specification',
    definition: 'Fixing the exact wording and arrangement of a planned poster before generation, so nothing can drift during rendering.',
    detail: 'Every text element must point to a verified source, or be marked as a design element such as the title. After this lock, no number is written again by hand.',
    file: '03-layout-spec.yaml'
  },
  {
    id: 'P6', title: 'Verbatim Text Prompt', kind: 'text',
    guide: 'Phase 6, Image Prompt Assembly',
    definition: 'An image instruction requiring that supplied wording be reproduced exactly, with no paraphrase or substitution.',
    detail: 'The prompt is assembled from the locked layout, and its numbers are copied, never retyped. The author sees it once more before rendering.',
    file: '04-image-prompt.md'
  },
  {
    id: 'P7', title: 'Image Generation (single call)', kind: 'image',
    guide: 'Phase 7, Final Rendering',
    definition: 'The locked prompt is sent to the text-to-image model, which draws the poster.',
    detail: 'This is the only phase that calls an image model. By now every fact has been decided, so the model renders wording and never chooses a figure.',
    file: 'poster.png'
  },
  {
    id: 'P8', title: 'Rendered Image Audit', kind: 'audit',
    guide: 'Phase 8, Post-Render Audit',
    definition: 'Checking a finished picture against its locked specification to confirm every element was reproduced correctly.',
    detail: 'If a number or name has drifted, the image is regenerated and audited again, up to three times. A passing poster gets a source sidecar file, then an interactive overlay (Chapter 26).',
    file: 'sources.md'
  }
];

const KIND_LABEL = {
  text: 'Text only',
  lock: 'Text only: the lock',
  image: 'The only image-model call',
  audit: 'Audit after rendering'
};

const PHASE_INDEX = {};
PHASES.forEach(function (p, i) { PHASE_INDEX[p.id] = i; });

let currentStep = -1;   // -1 = overview, 0..7 = a phase

// ---------------------------------------------------------------------------
// Infobox rendering
// ---------------------------------------------------------------------------
// The audit-trail files that exist once phase `index` is finished.
function fileListHtml(index) {
  let html = '<div class="files"><div class="files-label">Audit trail after this phase</div><ul>';
  let any = false;
  PHASES.forEach(function (p, i) {
    if (i > index || !p.file) return;
    any = true;
    const isNew = i === index;
    html += '<li class="' + (isNew ? 'new ' : '') + (p.kind === 'image' ? 'image' : 'text') + '">' +
      '<code>' + p.file + '</code>' + (isNew ? ' <span class="tag">new</span>' : '') + '</li>';
  });
  if (!any) html += '<li class="none">No files yet</li>';
  html += '</ul>';
  if (index >= 0 && !PHASES[index].file) {
    html += '<div class="files-note">This phase adds no new file.</div>';
  }
  return html + '</div>';
}

function renderOverview() {
  document.getElementById('infobox').innerHTML =
    '<span class="badge overview">Overview</span>' +
    '<h2>Decide what is true first. Draw it second.</h2>' +
    '<p>The pipeline never lets one step both decide a fact and render it. Six phases of text work plan, source, verify, and lock every claim. Only then is an image model called, exactly once. A final phase audits the picture.</p>' +
    '<p><span class="label">Try it: </span>Select <b>Next</b> to walk through the eight phases in order, or click any box.</p>';
}

function renderPhase(index) {
  const p = PHASES[index];
  document.getElementById('infobox').innerHTML =
    '<span class="badge ' + p.kind + '">' + KIND_LABEL[p.kind] + '</span>' +
    '<h2>' + (index + 1) + '. ' + p.title + '</h2>' +
    '<p>' + p.definition + '</p>' +
    '<p>' + p.detail + '</p>' +
    '<p class="guide">In the skill guide: ' + p.guide + '</p>' +
    fileListHtml(index);
}

// ---------------------------------------------------------------------------
// Diagram highlighting
// ---------------------------------------------------------------------------
function nodeElement(nodeId) {
  return document.querySelector('#diagram [id^="flowchart-' + nodeId + '-"]');
}

function select(index) {
  currentStep = index;
  PHASES.forEach(function (p, i) {
    const el = nodeElement(p.id);
    if (!el) return;
    el.classList.toggle('selected', i === index);
    el.classList.toggle('dimmed', index >= 0 && i > index);
  });
  if (index < 0) renderOverview(); else renderPhase(index);
  document.getElementById('stepLabel').textContent =
    index < 0 ? 'Overview' : 'Phase ' + (index + 1) + ' of ' + PHASES.length;
  document.getElementById('prevButton').disabled = index < 0;
  document.getElementById('nextButton').disabled = index >= PHASES.length - 1;
}

// Called by the Mermaid `click` directives, so it must be global.
window.showInfo = function (nodeId) {
  if (PHASE_INDEX[nodeId] === undefined) return;
  select(PHASE_INDEX[nodeId]);
};

// ---------------------------------------------------------------------------
// Startup
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', async function () {
  document.getElementById('prevButton').addEventListener('click', function () {
    if (currentStep >= 0) select(currentStep - 1);
  });
  document.getElementById('nextButton').addEventListener('click', function () {
    if (currentStep < PHASES.length - 1) select(currentStep + 1);
  });
  renderOverview();

  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'loose',   // required for click callbacks
    theme: 'default',
    flowchart: {
      useMaxWidth: true,
      htmlLabels: true,
      curve: 'basis',
      nodeSpacing: 30,
      rankSpacing: 24,
      padding: 8,
      subGraphTitleMargin: { top: 10, bottom: 18 }
    }
  });

  const container = document.getElementById('diagram');
  try {
    const result = await mermaid.render('verifiedPipelineSvg', DIAGRAM);
    container.innerHTML = result.svg;
    if (result.bindFunctions) result.bindFunctions(container);
  } catch (err) {
    container.textContent = 'The diagram could not be drawn: ' + err.message;
    return;
  }

  const svg = container.querySelector('svg');
  if (svg) {
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Flowchart, top to bottom, of eight phases. Phases 1 to 6 are grouped as text only: claim planning, source discovery, per-claim verification, verification report, layout specification lock, and verbatim text prompt. A dashed arrow returns from phase 3 to phase 1 for a rejected claim. Phase 7 is image generation, a single call. Phase 8 is the rendered image audit.');
  }

  // Keyboard access: every node can be focused and activated with Enter or Space
  PHASES.forEach(function (p) {
    const el = nodeElement(p.id);
    if (!el) return;
    el.setAttribute('tabindex', '0');
    el.setAttribute('role', 'button');
    el.setAttribute('aria-label', p.title + ': show details');
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        window.showInfo(p.id);
      }
    });
  });

  select(-1);
});

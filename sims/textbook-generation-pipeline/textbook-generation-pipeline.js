// Textbook Generation Pipeline - Mermaid flowchart with click-to-inspect nodes
// CANVAS_HEIGHT: 375
// The ordered stages that turn a course description into a published book,
// with the two quality gates that send work back when a check fails.
// Every node has a Mermaid `click` directive wired to showInfo(), which fills
// the shared infobox panel below the diagram. Previous / Next buttons step
// through the stages in order.

// ---------------------------------------------------------------------------
// Diagram definition (left-to-right Mermaid flowchart)
// ---------------------------------------------------------------------------
const DIAGRAM = `flowchart LR
    CourseDescription("Course<br/>Description"):::stage
    LearningGraph("Learning<br/>Graph"):::stage
    GraphGate{"Graph<br/>valid?"}:::gate
    ChapterStructure("Chapter<br/>Structure"):::stage
    ChapterContent("Chapter<br/>Content"):::stage
    ConceptGate{"Concepts<br/>covered?"}:::gate
    Media("Media and<br/>MicroSims"):::stage
    Deployment("Deployment"):::stage

    CourseDescription --> LearningGraph
    LearningGraph --> GraphGate
    GraphGate -->|Yes| ChapterStructure
    GraphGate -.->|No| LearningGraph
    ChapterStructure --> ChapterContent
    ChapterContent --> ConceptGate
    ConceptGate -->|Yes| Media
    ConceptGate -.->|No| ChapterContent
    Media --> Deployment

    click CourseDescription call showInfo("CourseDescription")
    click LearningGraph call showInfo("LearningGraph")
    click GraphGate call showInfo("GraphGate")
    click ChapterStructure call showInfo("ChapterStructure")
    click ChapterContent call showInfo("ChapterContent")
    click ConceptGate call showInfo("ConceptGate")
    click Media call showInfo("Media")
    click Deployment call showInfo("Deployment")

    classDef stage fill:#00897b,stroke:#00574b,stroke-width:2px,color:#ffffff,font-size:18px
    classDef gate fill:#ffc107,stroke:#8a5a00,stroke-width:2px,color:#2b1d00,font-size:18px

    linkStyle default stroke:#455a64,stroke-width:2px
    linkStyle 3 stroke:#c62828,stroke-width:2px,stroke-dasharray:6 4
    linkStyle 7 stroke:#c62828,stroke-width:2px,stroke-dasharray:6 4
`;

// ---------------------------------------------------------------------------
// Infobox content, in pipeline order.
// "by" names the skill (or command) from this library that performs the stage.
// ---------------------------------------------------------------------------
const STAGES = [
  {
    id: 'CourseDescription',
    title: 'Course Description',
    definition: 'A structured document stating what a course covers, who it is for, what is excluded, and what learners will be able to do afterward.',
    by: 'the <code>course-description-analyzer</code> skill, which creates or validates the description and scores its completeness.'
  },
  {
    id: 'LearningGraph',
    title: 'Learning Graph',
    definition: 'A directed structure whose nodes are teachable concepts and whose arrows show which concepts should be understood before others.',
    by: 'the <code>learning-graph-generator</code> skill.',
    review: 'An author reviews the concept list before chapter generation begins, because correcting concepts later is far more expensive.'
  },
  {
    id: 'GraphGate',
    gate: true,
    title: 'Quality Gate: Graph Valid?',
    definition: 'A check the learning graph must pass before any chapter work begins: its dependencies must contain no cycles.',
    by: 'the <code>analyze-graph.py</code> script inside the <code>learning-graph-generator</code> skill.',
    no: 'On "No," the work goes back to the Learning Graph to be fixed, so a defect is not built into every chapter.'
  },
  {
    id: 'ChapterStructure',
    title: 'Chapter Structure',
    definition: 'The division of the learning graph\'s concepts into an ordered set of chapters, so that no chapter uses a concept before it has been introduced.',
    by: 'the <code>book-chapter-generator</code> skill.',
    review: 'The proposed chapter design is presented for approval before a single chapter file is written.'
  },
  {
    id: 'ChapterContent',
    title: 'Chapter Content',
    definition: 'The written text of each chapter, together with the specifications for its diagrams, MicroSims, and exercises.',
    by: 'the <code>chapter-content-generator</code> skill.'
  },
  {
    id: 'ConceptGate',
    gate: true,
    title: 'Quality Gate: Concepts Covered?',
    definition: 'A check that every concept assigned to a chapter is actually addressed in that chapter\'s text.',
    by: 'the <code>chapter-content-generator</code> skill, which compares the text against the chapter\'s "Concepts Covered" list.',
    no: 'On "No," the work goes back to Chapter Content until the missing concepts are written.'
  },
  {
    id: 'Media',
    title: 'Media and MicroSims',
    definition: 'The interactive and visual elements added to the chapters: MicroSims, diagrams, images, slides, and audio.',
    by: 'the <code>microsim-generator</code> and <code>book-media-generator</code> skills.'
  },
  {
    id: 'Deployment',
    title: 'Deployment',
    definition: 'Publishing the finished site to the web so readers can reach it.',
    by: 'the <code>mkdocs gh-deploy</code> command, which publishes the site to GitHub Pages.',
    review: 'A push or a deploy waits for your explicit approval instead of running unattended.'
  }
];

const STAGE_INDEX = {};
STAGES.forEach(function (s, i) { STAGE_INDEX[s.id] = i; });

let current = -1;   // -1 = overview, otherwise an index into STAGES

// ---------------------------------------------------------------------------
// Infobox rendering
// ---------------------------------------------------------------------------
function renderOverview() {
  document.getElementById('infobox').innerHTML =
    '<h2>From course description to published book</h2>' +
    '<p>The textbook generation pipeline is the ordered sequence of steps that turns a course description into a published book. Six stages do the work. Two quality gates stop a defect from flowing into the stages after them.</p>' +
    '<p><span class="label">Try it: </span>Select <b>Next</b> to walk through the pipeline in order, or click any box in the diagram.</p>';
  document.getElementById('stepLabel').textContent = 'Step 0 of ' + STAGES.length;
}

function renderStage(index) {
  const s = STAGES[index];
  let html = '<h2' + (s.gate ? ' class="gate"' : '') + '>' + s.title + '</h2>' +
    '<p>' + s.definition + '</p>' +
    '<p><span class="label">Performed by: </span>' + s.by + '</p>';
  if (s.no) html += '<p><span class="label">If the check fails: </span>' + s.no + '</p>';
  if (s.review) html += '<p><span class="label">Human review: </span>' + s.review + '</p>';
  document.getElementById('infobox').innerHTML = html;
  document.getElementById('stepLabel').textContent = 'Step ' + (index + 1) + ' of ' + STAGES.length;
}

function nodeElement(nodeId) {
  return document.querySelector('#diagram [id^="flowchart-' + nodeId + '-"]');
}

function select(index) {
  current = index;
  document.querySelectorAll('#diagram .node.selected').forEach(function (n) {
    n.classList.remove('selected');
  });
  if (index < 0) {
    renderOverview();
  } else {
    const el = nodeElement(STAGES[index].id);
    if (el) el.classList.add('selected');
    renderStage(index);
  }
  document.getElementById('prevButton').disabled = index <= 0;
  document.getElementById('nextButton').disabled = index >= STAGES.length - 1;
}

// Called by the Mermaid `click` directives, so it must be global.
window.showInfo = function (nodeId) {
  if (nodeId in STAGE_INDEX) select(STAGE_INDEX[nodeId]);
};

// ---------------------------------------------------------------------------
// Startup
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', async function () {
  document.getElementById('prevButton').addEventListener('click', function () {
    if (current > 0) select(current - 1);
  });
  document.getElementById('nextButton').addEventListener('click', function () {
    if (current < STAGES.length - 1) select(current + 1);
  });
  select(-1);

  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'loose',   // required for click callbacks
    theme: 'default',
    // Yes / No edge labels are set larger so they stay readable after the
    // wide diagram is scaled down to the iframe width
    themeCSS: '.edgeLabel { font-size: 19px; }',
    flowchart: {
      useMaxWidth: true,
      htmlLabels: true,
      curve: 'basis',
      nodeSpacing: 24,
      rankSpacing: 26,
      padding: 10
    }
  });

  const container = document.getElementById('diagram');
  try {
    const result = await mermaid.render('textbookPipelineSvg', DIAGRAM);
    container.innerHTML = result.svg;
    if (result.bindFunctions) result.bindFunctions(container);
  } catch (err) {
    container.textContent = 'The diagram could not be drawn: ' + err.message;
    return;
  }

  const svg = container.querySelector('svg');
  if (svg) {
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Flowchart of the textbook generation pipeline: course description, learning graph, quality gate graph valid, chapter structure, chapter content, quality gate concepts covered, media and MicroSims, deployment. Each quality gate has a dashed red No branch back to the stage before it.');
  }

  // Keyboard access: every node can be focused and activated with Enter or Space
  STAGES.forEach(function (s) {
    const el = nodeElement(s.id);
    if (!el) return;
    el.setAttribute('tabindex', '0');
    el.setAttribute('role', 'button');
    el.setAttribute('aria-label', s.title + ': show details');
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        window.showInfo(s.id);
      }
    });
  });
});

// Book Launch Checklist - Mermaid flowchart with an order-and-justify activity
// CANVAS_HEIGHT: 490
// The confirmations that must pass, in order, before a book is announced.
// The reader works down the checklist. For each step the reader picks the
// reason that step has to pass before the next one; a correct reason checks
// the step off (it turns green). Clicking a step out of order explains what
// would go wrong. "Publish" unlocks only after all six confirmations.
// Every node has a Mermaid `click` directive wired to showInfo(), which fills
// the shared infobox panel beside the diagram.
//
// The reasons follow Chapters 25, 29, 30, and 31 of this book.

// ---------------------------------------------------------------------------
// Diagram definition (top-to-bottom Mermaid flowchart)
// ---------------------------------------------------------------------------
const DIAGRAM = `flowchart TD
    S1("1. mkdocs build --strict passes"):::todo
    S2("2. Deployment verified live"):::todo
    S3("3. book-metrics.json regenerated"):::todo
    S4("4. README regenerated from metrics"):::todo
    S5("5. Announcement drafted"):::todo
    S6("6. Announcement preview image checked"):::todo
    S7("7. Publish"):::publish

    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7

    click S1 call showInfo("S1")
    click S2 call showInfo("S2")
    click S3 call showInfo("S3")
    click S4 call showInfo("S4")
    click S5 call showInfo("S5")
    click S6 call showInfo("S6")
    click S7 call showInfo("S7")

    classDef todo fill:#00796b,stroke:#004d40,stroke-width:2px,color:#ffffff,font-size:16px
    classDef publish fill:#e65100,stroke:#8a3200,stroke-width:3px,color:#ffffff,font-size:16px

    linkStyle default stroke:#455a64,stroke-width:2px
`;

// ---------------------------------------------------------------------------
// Checklist content, in order.
// confirms: what the step confirms
// right / wrong: one sound reason and one unsound reason for doing this step
//                before the next one, with feedback for the unsound one
// why: the full justification shown once the step is checked off
// source: the earlier chapter the reason comes from
// ---------------------------------------------------------------------------
const STEPS = [
  {
    id: 'S1', title: 'mkdocs build --strict passes',
    confirms: 'The site builds with warnings, such as broken links, treated as failures.',
    right: 'A build with broken links would be deployed exactly as it is, so the live site would be defective before anyone checked it.',
    wrong: 'A strict build makes the published site load faster for its first visitors.',
    wrongFeedback: 'Strict mode has nothing to do with speed. It turns warnings into failures so defects stop here.',
    why: 'Strict build mode stops a defective site before it is published. Verifying a live site that was built from a failing build would only confirm problems you could have caught at your desk.',
    source: 'Chapter 29, strict build mode'
  },
  {
    id: 'S2', title: 'Deployment verified live',
    confirms: 'The published site renders correctly and its links and assets resolve.',
    right: 'If the live check finds a problem, fixing it changes the book, so numbers measured earlier would describe a version nobody will read.',
    wrong: 'The metrics script can only measure a site that is hosted on GitHub Pages.',
    wrongFeedback: 'Not so. The metrics script measures the book\'s content. The point is to measure the final state, after any fixes.',
    why: 'A clean local build cannot catch everything, such as a misconfigured base path. Confirm the live site first, fix what you find, and only then measure, so the numbers describe the book readers will actually get.',
    source: 'Chapter 29, deployment verification'
  },
  {
    id: 'S3', title: 'book-metrics.json regenerated',
    confirms: 'The book\'s measurements have been refreshed against its final state.',
    right: 'The README takes its statistics from this file, so a stale file means a README with stale numbers.',
    wrong: 'The README has to be typed by hand before any numbers exist.',
    wrongFeedback: 'The opposite. Figures are never hand-typed. They are read from the measurement file.',
    why: 'Every publishing route reads the same measurement file. Regenerate it first, and the README, the post, and the press release cannot disagree with each other.',
    source: 'Chapter 30, canonical metrics principle'
  },
  {
    id: 'S4', title: 'README regenerated from metrics',
    confirms: 'The repository\'s front page shows the current summary, badges, and statistics.',
    right: 'The announcement sends people to the repository, so its front page must already show the same current figures.',
    wrong: 'The announcement copies its numbers out of the README.',
    wrongFeedback: 'No. The announcement reads the measurement file directly, just as the README does. Neither copies the other.',
    why: 'The README is usually the first thing a newcomer reads. It has to be current before an announcement points anyone at it, and both draw their figures from the same measurement file.',
    source: 'Chapter 30, book-metrics.json hub'
  },
  {
    id: 'S5', title: 'Announcement drafted',
    confirms: 'The post or press release is written, with figures drawn from the recorded measurements.',
    right: 'A preview image belongs to one specific post, so there is nothing to check until that post and its link exist.',
    wrong: 'Drafting the post creates a correct preview image automatically, so no check is needed.',
    wrongFeedback: 'A platform builds the preview from the page\'s image and tags, and it may crop it badly. That is why the next step exists.',
    why: 'The preview image is cropped to the proportions one platform displays for one post. You can only check it once you know which post and which link it accompanies.',
    source: 'Chapter 25, social media preview cards'
  },
  {
    id: 'S6', title: 'Announcement preview image checked',
    confirms: 'The picture that accompanies the shared announcement appears and is cropped correctly.',
    right: 'Once the post is public, a missing or badly cropped image is the first impression, and it cannot be taken back.',
    wrong: 'A platform will refuse to accept a post that has no preview image.',
    wrongFeedback: 'The post would still go out, and that is the risk: nothing stops a broken preview except checking it first.',
    why: 'In a feed, the preview image is seen before a single word is read. This is the last chance to fix it while the post is still private.',
    source: 'Chapter 25, Open Graph meta tags'
  },
  {
    id: 'S7', title: 'Publish',
    confirms: 'The announcement goes out.',
    why: 'Build, deployment, metrics, and links have all been confirmed, in order. Your first readers will arrive at a working site with figures that agree everywhere.',
    source: 'Chapter 31, book launch checklist'
  }
];

const STEP_INDEX = {};
STEPS.forEach(function (s, i) { STEP_INDEX[s.id] = i; });

let checked = 0;          // number of steps checked off, in order (0..7)
let wrongPicked = false;  // has the unsound reason been picked for the current step?

// ---------------------------------------------------------------------------
// Diagram state
// ---------------------------------------------------------------------------
function nodeElement(nodeId) {
  return document.querySelector('#diagram [id^="flowchart-' + nodeId + '-"]');
}

// Recolor every node for the current progress. Mermaid writes fills as inline
// !important styles, so they are overridden the same way.
function paintNodes(selectedIndex) {
  STEPS.forEach(function (s, i) {
    const el = nodeElement(s.id);
    if (!el) return;
    const shape = el.querySelector('rect');
    const label = el.querySelector('.nodeLabel');
    const done = i < checked;
    const isPublish = i === STEPS.length - 1;
    if (shape) {
      let fill = isPublish ? '#e65100' : '#00796b';
      let stroke = isPublish ? '#8a3200' : '#004d40';
      if (done) { fill = '#2e7d32'; stroke = '#1b5e20'; }
      shape.style.setProperty('fill', fill, 'important');
      shape.style.setProperty('stroke', stroke, 'important');
    }
    if (label) {
      // a check mark replaces the step number, so "done" does not rely on color
      label.textContent = (done ? '✓' : (i + 1) + '.') + ' ' + s.title;
    }
    el.classList.toggle('selected', i === selectedIndex);
    // Publish stays dimmed until the six confirmations are checked
    el.classList.toggle('locked', isPublish && checked < STEPS.length - 1);
  });
  const total = STEPS.length - 1;
  document.getElementById('progressLabel').textContent =
    checked >= STEPS.length ? 'Published' : Math.min(checked, total) + ' of ' + total + ' checked';
  document.getElementById('nextButton').disabled = checked >= STEPS.length;
  document.getElementById('nextButton').textContent =
    checked >= STEPS.length - 1 ? 'Publish' : 'Next Step';
}

// ---------------------------------------------------------------------------
// Infobox rendering
// ---------------------------------------------------------------------------
function setInfo(html) {
  document.getElementById('infobox').innerHTML = html;
}

function renderOverview() {
  setInfo('<span class="badge">Before you announce</span>' +
    '<h2>Run the checklist in order</h2>' +
    '<p>Six confirmations must pass before a book is announced. Each one protects the step after it.</p>' +
    '<p><span class="label">Your job: </span>Click step 1, or select <b>Next Step</b>. For each step, choose the reason it has to pass before the next one. A sound reason checks the step off.</p>' +
    '<p class="note">Try clicking a later step first to see what goes wrong when the order is skipped.</p>');
}

// The step that is next in line: ask the reader to justify it
function renderQuestion(index) {
  const s = STEPS[index];
  const next = STEPS[index + 1];
  // alternate which answer comes first so position is not a clue
  const rightFirst = index % 2 === 1;
  const rightBtn = '<button type="button" class="answer" data-answer="right">' + s.right + '</button>';
  const wrongBtn = '<button type="button" class="answer" data-answer="wrong"' + (wrongPicked ? ' disabled' : '') + '>' + s.wrong + '</button>';
  setInfo('<span class="badge">Step ' + (index + 1) + ' of ' + STEPS.length + '</span>' +
    '<h2>' + s.title + '</h2>' +
    '<p>' + s.confirms + '</p>' +
    '<p class="question">Why must this pass before <b>' + next.title + '</b>?</p>' +
    (rightFirst ? rightBtn + wrongBtn : wrongBtn + rightBtn) +
    (wrongPicked ? '<p class="feedback wrong"><b>Not a sound reason.</b> ' + s.wrongFeedback + '</p>' : ''));
  document.querySelectorAll('#infobox .answer').forEach(function (b) {
    b.addEventListener('click', function () {
      if (b.getAttribute('data-answer') === 'right') {
        checked = index + 1;
        wrongPicked = false;
        paintNodes(index);
        renderChecked(index, true);
      } else {
        wrongPicked = true;
        renderQuestion(index);
      }
    });
  });
}

// A step that has been checked off: show the full justification
function renderChecked(index, justNow) {
  const s = STEPS[index];
  const isPublish = index === STEPS.length - 1;
  let nextLine = '';
  if (!isPublish) {
    nextLine = checked === index + 1
      ? '<p class="note">Next: <b>' + STEPS[index + 1].title + '</b>.</p>'
      : '';
  }
  setInfo('<span class="badge done">' + (isPublish ? 'Published' : '✓ Checked') + '</span>' +
    '<h2>' + s.title + '</h2>' +
    '<p>' + (justNow && !isPublish ? '<b>Sound reason.</b> ' : '') + s.why + '</p>' +
    '<p class="source">From ' + s.source + '</p>' +
    nextLine);
}

// A step clicked before the steps above it are checked
function renderTooSoon(index) {
  const s = STEPS[index];
  const blocker = STEPS[checked];
  const isPublish = index === STEPS.length - 1;
  setInfo('<span class="badge warn">Not yet</span>' +
    '<h2>' + s.title + '</h2>' +
    '<p><b>' + blocker.title + '</b> has not been checked.</p>' +
    '<p>' + (isPublish
      ? 'Announcing before the checklist is done invites a broken first impression. A post that goes out before the live site has been verified risks sending your very first readers to a broken link.'
      : 'The checklist runs strictly in order, because each step relies on the ones above it. ' + blocker.why) + '</p>' +
    '<p class="note">Go back to step ' + (checked + 1) + '.</p>');
}

function selectStep(index) {
  if (index < checked) {
    paintNodes(index);
    renderChecked(index, false);
  } else if (index > checked) {
    paintNodes(index);
    renderTooSoon(index);
  } else if (index === STEPS.length - 1) {
    // all six confirmations are checked: publish
    checked = STEPS.length;
    paintNodes(index);
    renderChecked(index, true);
  } else {
    wrongPicked = false;
    paintNodes(index);
    renderQuestion(index);
  }
}

// Called by the Mermaid `click` directives, so it must be global.
window.showInfo = function (nodeId) {
  if (STEP_INDEX[nodeId] === undefined) return;
  selectStep(STEP_INDEX[nodeId]);
};

// ---------------------------------------------------------------------------
// Startup
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', async function () {
  document.getElementById('nextButton').addEventListener('click', function () {
    if (checked < STEPS.length) selectStep(checked);
  });
  document.getElementById('resetButton').addEventListener('click', function () {
    checked = 0;
    wrongPicked = false;
    paintNodes(-1);
    renderOverview();
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
      rankSpacing: 26,
      padding: 8
    }
  });

  const container = document.getElementById('diagram');
  try {
    const result = await mermaid.render('launchChecklistSvg', DIAGRAM);
    container.innerHTML = result.svg;
    if (result.bindFunctions) result.bindFunctions(container);
  } catch (err) {
    container.textContent = 'The diagram could not be drawn: ' + err.message;
    return;
  }

  const svg = container.querySelector('svg');
  if (svg) {
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Checklist flowchart, top to bottom: 1, mkdocs build strict passes. 2, deployment verified live. 3, book-metrics.json regenerated. 4, README regenerated from metrics. 5, announcement drafted. 6, announcement preview image checked. 7, publish.');
  }

  // Keyboard access: every node can be focused and activated with Enter or Space
  STEPS.forEach(function (s) {
    const el = nodeElement(s.id);
    if (!el) return;
    el.setAttribute('tabindex', '0');
    el.setAttribute('role', 'button');
    el.setAttribute('aria-label', s.title + ': open this step');
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        window.showInfo(s.id);
      }
    });
  });

  paintNodes(-1);
});

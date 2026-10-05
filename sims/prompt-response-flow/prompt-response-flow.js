// Prompt and Response Flow - Mermaid flowchart with click-to-inspect nodes
// CANVAS_HEIGHT: 440
// Shows how a system prompt and a user prompt combine in one model request,
// and why the same inputs do not guarantee the same response.
// Every node has a Mermaid `click` directive wired to showInfo(), which fills
// the shared infobox panel below the diagram.

// ---------------------------------------------------------------------------
// Diagram definition (left-to-right Mermaid flowchart)
// ---------------------------------------------------------------------------
const DIAGRAM = `flowchart LR
    SystemPrompt("System Prompt"):::systemPrompt
    UserPrompt("User Prompt"):::userPrompt
    Tokenization["Tokenization"]:::tokenize
    LanguageModel("Language Model<br/>samples the next tokens"):::model
    Response("Response"):::response
    NextRun["Same inputs,<br/>next run"]:::rerun

    SystemPrompt --> Tokenization
    UserPrompt --> Tokenization
    Tokenization --> LanguageModel
    LanguageModel --> Response
    NextRun -.->|"may produce a<br/>different Response"| LanguageModel

    click SystemPrompt call showInfo("SystemPrompt")
    click UserPrompt call showInfo("UserPrompt")
    click Tokenization call showInfo("Tokenization")
    click LanguageModel call showInfo("LanguageModel")
    click Response call showInfo("Response")
    click NextRun call showInfo("NextRun")

    classDef systemPrompt fill:#1565c0,stroke:#0d3c78,stroke-width:2px,color:#ffffff,font-size:16px
    classDef userPrompt fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#0d2b4e,font-size:16px
    classDef tokenize fill:#eceff1,stroke:#546e7a,stroke-width:2px,color:#1f2937,font-size:16px
    classDef model fill:#00695c,stroke:#003d33,stroke-width:3px,color:#ffffff,font-size:18px
    classDef response fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px,color:#12361a,font-size:16px
    classDef rerun fill:#ffe9a8,stroke:#b45309,stroke-width:2px,stroke-dasharray:6 4,color:#3b2600,font-size:16px

    linkStyle default stroke:#546e7a,stroke-width:2px
    linkStyle 4 stroke:#b45309,stroke-width:2px
`;

// ---------------------------------------------------------------------------
// Infobox content. Definitions follow this book's glossary.
// ---------------------------------------------------------------------------
const NODE_INFO = {
  SystemPrompt: {
    title: 'System Prompt',
    definition: 'Instructions supplied to a model separately from the user request that establish a persistent role, constraints, and available tools for a session.',
    role: 'It is sent along with every request in the session and shapes how each user prompt is handled. It is not the request itself.',
    compare: 'system'
  },
  UserPrompt: {
    title: 'User Prompt',
    definition: 'The text a person supplies to a language model to elicit a response. It carries the request, any supporting material, and constraints on the desired output.',
    role: 'It states what is wanted for this turn only, and it changes with every turn.',
    compare: 'user'
  },
  Tokenization: {
    title: 'Tokenization',
    definition: 'The process of splitting raw text into the discrete units, called tokens, that a language model consumes.',
    role: 'Both prompts are split into tokens and reach the model as one sequence. The model receives tokens, never words.'
  },
  LanguageModel: {
    title: 'Language Model',
    definition: 'A statistical model trained on very large text collections that predicts the next unit of text given the preceding text.',
    role: 'It builds the response one token at a time, sampling each token from a probability distribution over likely next tokens.'
  },
  Response: {
    title: 'Response',
    definition: 'The generated text returned to the user.',
    role: 'It is the result of one particular run of sampling, so it is one of many responses the same inputs could have produced.'
  },
  NextRun: {
    title: 'Same Inputs, Next Run (Nondeterminism)',
    definition: 'Nondeterminism in LLM output is the property that a language model may produce different responses to identical input across runs, because output is sampled rather than computed deterministically.',
    role: 'Send the same system prompt and user prompt again and the model samples again, so the response may differ. Tighter prompts narrow the range of likely responses but never shrink it to exactly one.'
  }
};

const OVERVIEW = {
  title: 'One request, two kinds of prompt',
  definition: 'A single model request combines a system prompt and a user prompt. Both are tokenized, the language model samples a response, and the same inputs can produce a different response on the next run.',
  role: 'Click each box in the diagram, starting with the two prompts, and compare their roles.',
  compare: 'both'
};

// ---------------------------------------------------------------------------
// Infobox rendering
// ---------------------------------------------------------------------------
function compareTable(active) {
  const sys = active === 'system' ? ' active' : '';
  const usr = active === 'user' ? ' active' : '';
  return '<table class="compare">' +
    '<caption>System prompt compared with user prompt</caption>' +
    '<thead><tr><th></th>' +
    '<th class="col-system' + sys + '">System prompt</th>' +
    '<th class="col-user' + usr + '">User prompt</th></tr></thead>' +
    '<tbody>' +
    '<tr><th>Carries</th><td>Role, constraints, available tools</td><td>The request and its supporting material</td></tr>' +
    '<tr><th>Lasts for</th><td>The whole session</td><td>One turn</td></tr>' +
    '</tbody></table>';
}

function renderInfo(info, isOverview) {
  const box = document.getElementById('infobox');
  let html = '<div class="info-text">' +
    '<h2>' + info.title + '</h2>' +
    '<p>' + info.definition + '</p>' +
    '<p><span class="label">' + (isOverview ? 'Try it: ' : 'In this request: ') + '</span>' + info.role + '</p>' +
    '</div>';
  if (info.compare) html += compareTable(info.compare);
  box.innerHTML = html;
}

function nodeElement(nodeId) {
  return document.querySelector('#diagram [id^="flowchart-' + nodeId + '-"]');
}

// Called by the Mermaid `click` directives, so it must be global.
window.showInfo = function (nodeId) {
  const info = NODE_INFO[nodeId];
  if (!info) return;
  document.querySelectorAll('#diagram .node.selected').forEach(function (n) {
    n.classList.remove('selected');
  });
  const el = nodeElement(nodeId);
  if (el) el.classList.add('selected');
  renderInfo(info, false);
};

// ---------------------------------------------------------------------------
// Startup
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', async function () {
  renderInfo(OVERVIEW, true);

  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'loose',   // required for click callbacks
    theme: 'default',
    flowchart: {
      useMaxWidth: true,
      htmlLabels: true,
      curve: 'basis',
      nodeSpacing: 28,
      rankSpacing: 46
    }
  });

  const container = document.getElementById('diagram');
  try {
    const result = await mermaid.render('promptResponseFlowSvg', DIAGRAM);
    container.innerHTML = result.svg;
    if (result.bindFunctions) result.bindFunctions(container);
  } catch (err) {
    container.textContent = 'The diagram could not be drawn: ' + err.message;
    return;
  }

  const svg = container.querySelector('svg');
  if (svg) {
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Flowchart: a system prompt and a user prompt both feed tokenization, which feeds the language model, which produces a response. A dashed branch labeled same inputs, next run points back into the language model and may produce a different response.');
  }

  // Keyboard access: every node can be focused and activated with Enter or Space
  Object.keys(NODE_INFO).forEach(function (nodeId) {
    const el = nodeElement(nodeId);
    if (!el) return;
    el.setAttribute('tabindex', '0');
    el.setAttribute('role', 'button');
    el.setAttribute('aria-label', NODE_INFO[nodeId].title + ': show details');
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        window.showInfo(nodeId);
      }
    });
  });
});

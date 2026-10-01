# Content Element Types for Textbook Chapters

This reference describes the various non-pure-text content elements that can be used to break up textbook content and enhance learning. Each element type should be specified in `<details markdown="1">` blocks when generating chapter content.
The content of the details blocks should be to describe what the learning objective is and
how a non-pure-text element can be used to promote learning.

**Every specification block uses the template and rules in `microsim-specification-rules.md`.** That file
defines the required fields (Bloom Level, Bloom Verb, Learning Objective, Evidence of Mastery, complete
Content, Provenance, Rules, Learner Activity, Feedback, Chapter Anchors) and a self-check. This file says
which element type fits which content. The examples below show the element-specific Content only; a real
block also carries the full header and the other fields. Specifications describe *what* the learner learns
and sees, never *how* to build it: no pixel sizes, layout, colors, fonts or library calls.

## Driven By An Learning Objective

Behind the strategy for every diagram is to help the student learn. A unit of learning
is called a Learning Objective and diagrams are a wonderful way to teach visually.

By understanding the `Bloom Levels` and `Bloom Verbs` of learning objective we encounter, we can map the objective to a specific type of interactive diagram, chart, infographic or even a MicroSim.

Here are the six Bloom Levels of learning objectives

1. Remember (L1) - Recall facts and basic concepts
2. Understand (L2) - Explain ideas or concepts
3. Apply (L3) - Use knowledge to solve problems
4. Analyze (L4) - Examine relationships, connect concepts
5. Evaluate (L5) - Judge value, make decisions
6. Create (L6) - Design new solutions, produce original work

Here are the Bloom Verbs associated with each Bloom Level.When
you generate a diagram specification within a details block, use both the Bloom Level and Bloom Verb to describe a MicroSim.

### Remember (L1)
list, define, recall, identify, name, recognize, locate, describe

### Understand (L2)
explain, summarize, interpret, classify, compare, contrast, exemplify, infer

### Apply (L3)
use, execute, implement, solve, demonstrate, calculate, apply, practice

### Analyze (L4)
differentiate, organize, attribute, compare, contrast, examine, deconstruct, distinguish

### Evaluate (L5)
judge, critique, assess, justify, prioritize, recommend, validate, defend

### Create (L6)
design, construct, develop, formulate, compose, produce, invent, generate

## Examples of MicroSims for each Bloom Level

### Remember (L1) — Recall facts, terms, and basic concepts 

1. Flash Card MicroSims — Flip cards to reveal definitions or answers 
2. Term Sorter MicroSims — Drag terms into correct category bins
3. Label the Diagram — Click or drag labels onto parts of an image
4. Matching Pairs — Connect terms to their definitions with lines 
5. Sequence Ordering — Arrange steps or events in chronological order 

### Understand (L2) — Explain ideas and demonstrate comprehension 

1. Concept Matcher — Match concepts to their explanations or examples 
2. Paraphrase Checker — Select the best restatement of a concept
3. Analogy Builder — Complete "A is to B as C is to ___" relationships
4. Translation Converter — Convert between representations (e.g., equation
↔ graph)
5. Predict the Output — Given inputs, predict what a system will produce

### Apply (L3) — Use knowledge to solve problems

1. Interactive Calculator — Adjust sliders to solve equations or formulas
2. Parameter Explorer — Modify variables and observe simulation changes
3. Step-by-Step Solver — Work through problems with guided scaffolding
4. Code Tracer — Execute code mentally and predict variable states
5. Scenario Simulator — Apply rules to new situations and see outcomes

### Analyze (L4) — Identify patterns, relationships, and structure

1. Network Graph Explorer — Identify connections between nodes
2. Data Pattern Finder — Spot trends and outliers in visualizations 
3. Cause-Effect Mapper — Draw arrows between causes and their effects 
4. Component Breakdown — Decompose systems into constituent parts 
5. Compare-Contrast Matrix — Fill in similarities and differences between 
items 

### Evaluate (L5) — Make judgments and assess quality 

1. Classification Sorter — Categorize examples as valid/invalid or by quality
2. Error Detector — Find and flag mistakes in code, proofs, or arguments
3. Ranking Ladder — Order items by effectiveness, quality, or priority
4. Decision Tree Navigator — Evaluate criteria to reach justified conclusions 
5. Rubric Rater — Score examples against defined criteria 

### Create (L6) — Design, construct, and produce original work

1. Model Editor — Build custom models with draggable components 
2. Diagram Builder — Construct flowcharts, circuits, or concept maps
3. Equation Composer — Assemble formulas from mathematical building blocks
4. Algorithm Designer — Arrange code blocks to create working programs
5. Synthesis Canvas — Combine elements to design novel solutions or systems 

## Element Types Overview

The goal is to have not have more than four paragraphs of pure text without incorporating one of these elements. Students don't like to see large blocks of pure text scrolling in their intelligent textbook. They want to interact with the content.

## CRITICAL RULE: Every Visual Element Must Be Interactive

**NEVER create static images that do not give the learner feedback.** Every diagram, chart, infographic, MicroSim, timeline, map, workflow, graph model, and causal loop diagram in an intelligent textbook MUST include at least one form of learner interactivity. A textbook page that produces no interaction events produces no xAPI statements, no engagement data, and no learning signal — which defeats the entire purpose of an intelligent textbook.

**Minimum interactivity bar (every diagram must clear this):**

- The learner can hover, click, or manipulate at least one element on the diagram
- That interaction produces visible feedback (an infobox, tooltip, highlight, panel update, parameter change, or state transition)
- The feedback teaches something — typically a definition, a property, a relationship, or a consequence

**Mermaid diagrams are permitted ONLY when every node is clickable** and the click reveals an infobox containing the term's definition (ideally pulled from the chapter glossary) or supporting context. Mermaid cannot make edges clickable, so explain what each connection means in an edge label or in the infobox of the node it leaves. A plain Mermaid diagram with no click handlers is a static image and is NOT acceptable.

**Forbidden patterns:**

- Static SVG, PNG, or JPG embedded with no surrounding interaction
- Mermaid diagrams without click handlers and infoboxes
- Charts that render once and never respond to hover, click, or filter
- Timelines where the learner cannot reveal more detail on any event
- Maps where regions and arrows are decorative and not selectable
- Workflows where boxes have no hover text or expand-on-click behavior
- Graph models where nodes and edges cannot be clicked or hovered

If a candidate diagram cannot meet the minimum interactivity bar, redesign it as a MicroSim, an interactive infographic, or a clickable Mermaid diagram with infoboxes — or cut it.

**Why this matters:** The xAPI value proposition is that every learner interaction tells a story. A static diagram tells no story. Every diagram in this textbook is also a sensor: it captures what learners explore, what they ignore, and where they get stuck. Design accordingly.

## 1. Markdown Lists

**Type identifier:** `markdown-list`

**When to use:**
- Enumerating key points, features, or characteristics
- Presenting step-by-step procedures
- Listing examples or categories

**Implementation:** Embed directly in markdown content (no `<details markdown="1">` block needed)

**Requirements:**
- ALWAYS place a blank line before the list
- Use numbered lists for sequences or ordered items
- Use bullet lists for unordered collections

**Example:**
```markdown
The following are key characteristics of graph databases:

- Native graph storage
- Constant-time traversals
- Flexible schema
```

## 2. Markdown Tables

**Type identifier:** `markdown-table`

**When to use:**
- Comparing features across multiple dimensions
- Presenting structured data
- Showing before/after comparisons

**Implementation:** Embed directly in markdown content (no `<details markdown="1">` block needed)

**Requirements:**
- ALWAYS place a blank line before the table
- Use clear, concise column headers
- Keep cell content brief
- Ensure proper markdown table syntax

**Example:**
```markdown
Here is a comparison of database types:

| Feature | RDBMS | Graph Database |
|---------|-------|----------------|
| Schema | Rigid | Flexible |
| Joins | Required | Native traversal |
| Query Speed (multi-hop) | Slow | Fast |
```

## 3. Admonitions

An admonition is another way to break up a wall of text.
They should be used only occasionally. Try to not have
more than one per page.

Our intelligent textbooks use the MkDocs Material theme
which supports admonitions.

Here are the admonition types supported by MkDocs Material:

```markdown
!!! note
 This is a note admonition.

!!! abstract
 This is an abstract/summary/tldr admonition.

!!! info
 This is an info/todo admonition.

!!! tip
 This is a tip/hint/important admonition.

!!! success
 This is a success/check/done admonition.

!!! question
 This is a question/help/faq admonition.

!!! warning
 This is a warning/caution/attention admonition.

!!! failure
 This is a failure/fail/missing admonition.

!!! danger
 This is a danger/error admonition.

!!! bug
 This is a bug admonition.

!!! example
 This is an example admonition.

!!! quote
 This is a quote/cite admonition.

With custom titles:

!!! note "Custom Title Here"
 Content with a custom title.

Collapsible (requires pymdownx.details):

??? note "Click to expand"
 This content is hidden by default.

???+ note "Expanded by default"
 This content is visible but can be collapsed.

Inline admonitions (Material theme):

!!! info inline
 Inline left admonition.

!!! info inline end
 Inline right admonition.
```

The Collapsible admonition that uses `???` is a fun way to challenge students
test their knowledge.It can be used at the end of a chapter to present
a question and then reveal an answer.

```markdown
??? note "What are the first six digits of Pi? - Click to expand"
 3.14159
```

## 4. Diagrams and Drawings

In this section, you will create a detailed specification for a diagram, drawing, chart, flowchart, workflow, infographic or interactive MicroSim.

**Type identifier:** `diagram`

**When to use:**
- Illustrating system architectures
- Showing relationships between components
- Explaining abstract concepts visually
- Depicting data flows or processes
- Defining an infographic that has items in a diagram or workflow with hover-triggered information boxes

**Interactivity requirement (REQUIRED):** Every diagram MUST be interactive. At minimum, every labeled component, node, or arrow must be clickable or hoverable to reveal a definition, property, or explanation in an infobox or side panel. If using Mermaid, you MUST add click handlers (e.g., `click NodeId call showInfo("term")`) for every node so the learner can reveal a definition. Static diagrams with no learner feedback are NOT permitted.

**Implementation:** 

Add a level 4 header that indicates we are placing a diagram in the content, followed by the
`<details markdown="1">` specification. Do not add an iframe: the microsim-generator inserts it,
with the correct height, after the sim is built.

```markdown
#### Diagram: {{DIAGRAM_NAME}}
```

The `{sim-id}` in the specification must be a kebab-case string (lowercase letters and dashes).

**Required information** (in the fields of the template in `microsim-specification-rules.md`):

- Diagram Name - A title-case name of the diagram that is unique in the chapter
- **Bloom Level** - one of the six levels of the 2001 Bloom Taxonomy: Remember, Understand, Apply, Analyze, Evaluate, Create
- **Bloom Verb** - one of the verbs for that level in blooms-taxonomy.md (Part 1)
- **Learning Objective** - what the learner will be able to do, starting "The learner will <verb>"
- **Content** - every component shown, with the text of its label and of the definition it reveals
- **Content** - every connection, and what the relationship means
- **Learner Activity** - what the learner clicks or hovers and what it reveals

**Example specification:**
```xml
#### Diagram: CMDB Architecture Diagram

<details markdown="1">
<summary>CMDB Architecture Diagram</summary>
Type: diagram
**sim-id:** cmdb-architecture-diagram<br/>
**Library:** p5.js<br/>
**Status:** Specified<br/>
**Bloom Level:** Understand<br/>
**Bloom Verb:** explain<br/>
**Learning Objective:** The learner will explain how a traditional CMDB stores configuration items and their relationships in relational tables.

Content:
- Three layers, top to bottom: CMDB Application Layer, Business Logic Layer, RDBMS Storage Layer
- Inside the storage layer: two "CI Tables" and one "Relationships" junction table
- Connections: data flows from the application layer down to storage; each relationship row points to two CI rows through "Foreign Keys"
- Definitions revealed on click:
- CMDB Application Layer: the screens and APIs people use to search and update configuration items.
- Business Logic Layer: applies the rules for creating, validating and linking configuration items.
- RDBMS Storage Layer: the relational database that stores every configuration item and relationship as table rows.
- CI Tables: one row per configuration item (a server, an application, a database), with its attributes as columns.
- Relationships table: one row per link between two configuration items, such as "runs on" or "depends on".
- Foreign Keys: the columns in the Relationships table that hold the IDs of the two CI rows it links.

Learner Activity: the learner clicks each layer and table to reveal its definition, then answers "Which table must a query read to find what a server depends on?" (answer: the Relationships table, joined to the CI Tables).
</details>
```

!!! Note
 Do not specify positions, sizes or colors. MicroSims are width responsive, and the
 microsim-generator decides the layout. Describe what the learner must see and learn.

## 5. Interactive Infographics

**Type identifier:** `infographic`

**When to use:**
- Presenting statistical information visually
- Creating clickable concept maps
- Building progressive disclosure interfaces
- Showing hierarchical information

**Implementation:** Use `<details markdown="1">` block with specification

**Required information** (in the fields of the template in `microsim-specification-rules.md`):
- the Learning Objective and main message
- **Content:** every labeled item and the full text each hover or click reveals
- **Learner Activity:** which reveals the learner uses, and what they are then asked to identify
- **Provenance:** where the image and the facts come from

Dated events are specified as a timeline (section 8), not an infographic.

**Example specification (Content section only):**
```xml
<details markdown="1">
<summary>Animal Cell Callout Explorer</summary>
Type: infographic
**sim-id:** animal-cell-callout-explorer<br/>
**Library:** html<br/>
**Status:** Specified<br/>
**Bloom Level:** Remember<br/>
**Bloom Verb:** identify<br/>
**Learning Objective:** The learner will identify five structures of an animal cell from their functions.

Content (callouts, with the text each click reveals):
- Nucleus: holds the cell's DNA and controls gene expression.
- Cell membrane: a lipid bilayer that controls what enters and leaves the cell.
- Mitochondrion: releases energy from food molecules as ATP.
- Ribosome: builds proteins from amino acids.
- Golgi apparatus: modifies, sorts and packages proteins for transport.

Learner Activity: in explore mode the learner clicks each callout to read its function. In quiz mode the function is shown and the learner clicks the matching structure; five questions, one attempt each.

Provenance: the functions are the definitions in the chapter's glossary. The image is a text-free drawing of an animal cell; all labels are rendered by the sim, not the image.
</details>
```

## 6. MicroSims (p5.js Simulations)

**Type identifier:** `microsim`

**When to use:**
- Demonstrating dynamic behavior
- Allowing students to experiment with parameters
- Visualizing algorithms or processes
- Showing cause-and-effect relationships

**Implementation:** Use `<details markdown="1">` block with specification

**Required information:** every field of the template in `microsim-specification-rules.md`. In
particular: the quantities the learner can change, each with min, max, step, default and unit (**Rules**);
what the learner does and what changes (**Learner Activity**); and what the learner is told after a
right or wrong answer (**Feedback**). Do not specify canvas size, layout, control placement or colors; the
microsim-generator decides those.

### CRITICAL: Instructional Pattern Selection

**Before specifying visual effects, determine the appropriate interaction pattern based on Bloom's level:**

| Bloom Level | Recommended Pattern | Avoid |
|-------------|---------------------|-------|
| Remember (L1) | Flashcards, matching, labeling | Complex animations |
| **Understand (L2)** | **Step-through with worked examples, concrete data visibility** | **Continuous animation** |
| Apply (L3) | Parameter exploration, calculators | Passive viewing |
| Analyze (L4) | Network explorers, pattern finders | Pre-computed results |
| Evaluate (L5) | Classification sorters, rubric raters | No feedback |
| Create (L6) | Model editors, builders | Rigid templates |

**For UNDERSTAND level objectives:** Do NOT specify animation or particle effects. Instead, specify:
- What DATA must be visible at each stage
- Step-through controls (Next/Previous buttons)
- Concrete worked examples with real values
- Prediction opportunities before revealing answers

### Data Visibility Requirements (REQUIRED for Understand/Explain objectives)

When the learning objective involves "explain," "describe," or "understand," you MUST specify what data transformations the learner needs to SEE:

```
Data Visibility Requirements:
  Stage 1: Show [raw input data]
  Stage 2: Show [first transformation with concrete values]
  Stage 3: Show [intermediate result]
  ...
  Final: Show [output with connection to input]
```

**Bad specification (visual-focused):**
```
Animation: Data flows between stages with particle effects
Visual style: Smooth transitions with glowing nodes
```

**Good specification (data-focused):**
```
Data Visibility Requirements:
  Stage 1: Show raw query "physics ball throwing"
  Stage 2: Show tokenized array ["physics", "ball", "throwing"]
  Stage 3: Show synonym expansion: throwing → [throw, projectile, launch]
  Stage 4: Show match scores with calculation breakdown
  Stage 5: Show ranked results with highlighted matching terms
Interaction: Step-through with Next/Previous buttons
```

### Instructional Rationale (REQUIRED)

Every MicroSim specification must include an Instructional Rationale explaining WHY the chosen interaction pattern supports the learning objective:

```
Instructional Rationale: Step-through with worked examples is appropriate
because the Understand/explain objective requires learners to trace the
process with concrete data. Continuous animation would prevent prediction
and obscure the actual data transformations.
```

**Example specification:**
```xml
#### Diagram: BFS and DFS Next-Node Predictor

<details markdown="1">
<summary>BFS and DFS Next-Node Predictor</summary>
Type: microsim
**sim-id:** bfs-dfs-next-node-predictor<br/>
**Library:** p5.js<br/>
**Status:** Specified<br/>
**Bloom Level:** Analyze<br/>
**Bloom Verb:** differentiate<br/>
**Learning Objective:** The learner will differentiate breadth-first from depth-first search by predicting the next node each algorithm visits from the current queue or stack.

**Prerequisites:** graph, node, edge, queue, stack, breadth-first search, depth-first search (defined in the sections above).

**Evidence of Mastery:** At each step the learner clicks the node they predict the algorithm visits next. A prediction is correct when it matches the visit order in Content. Mastery is completing both traversals with at most one wrong prediction in each. Hovering a node is exploration, not evidence.

**Misconceptions:** (1) BFS follows one branch to the bottom first. (2) DFS visits all of a node's neighbors before going deeper. (3) Both orders are simply alphabetical.

**Instructional Rationale:** Analyze-level differentiation needs the learner to use the rule, not watch it. Predicting each next node while the queue or stack is visible forces the learner to apply "front of the queue" versus "top of the stack", so the step-through has no animation.

**Content:**

- Nodes: A, B, C, D, E, F, G. Start node: A.
- Edges: A–B, A–C, B–D, B–E, C–F, C–G.
- BFS visit order: A, B, C, D, E, F, G.
- DFS visit order: A, B, D, E, C, F, G.
- Shown at every step: the visited list and the current queue (BFS) or stack (DFS).

**Provenance:** A small example graph written for this sim. The orders follow from the Rules.

**Rules:** Neighbors are considered in alphabetical order. BFS takes the node at the front of the queue and adds its unvisited neighbors to the back. DFS takes the node on top of the stack and pushes its unvisited neighbors in reverse alphabetical order, so the alphabetically first neighbor is on top. A node is marked visited when it is taken, and is never added twice.

**Learner Activity:**

1. BFS runs first. A is visited; the queue shows B, C. The learner clicks the node BFS visits next.
2. After each prediction the sim takes the next node, updates the visited list and the queue, and asks for the next prediction, until all seven nodes are visited.
3. The learner presses Next algorithm, and DFS runs on the same graph the same way, showing the stack.
4. At the end both visit orders are shown side by side.

**Feedback:** Two traversals of six predictions each, in fixed order; one attempt per prediction. Correct: "Correct: <node>." Wrong in BFS: "BFS takes the front of the queue: <queue>. It finishes a whole level before going deeper." Wrong in DFS: "DFS takes the top of the stack: <stack>. It goes as deep as it can before backing up." After a wrong prediction the correct node is taken and the traversal continues. The count of correct predictions is shown for each algorithm.

**Starting State:** The graph with A marked as the start, BFS selected, and the question "BFS has visited A. Which node does it visit next?"

**Chapter Anchors:** The chapter's worked example gives the BFS order A, B, C, D, E, F, G.
</details>
```

## 7. Charts (Bar, Line, Pie)

**Type identifier:** `chart`

**When to use:**
- Presenting quantitative data
- Showing trends over time
- Comparing values across categories
- Illustrating proportions or distributions

**Interactivity requirement (REQUIRED):** Every chart MUST respond to learner action. At minimum, hovering a bar/point/slice reveals the precise value and label in a tooltip; ideally, the learner can also toggle data series, filter categories, or adjust a parameter that re-renders the chart. Charts that render once and never respond are NOT permitted.

**Implementation:** Use `<details markdown="1">` block with specification

**Required information in description:**
- Chart type (bar, line, pie, scatter, etc.)
- **Content:** every value to be plotted, with its label and unit; never "representative data"
- **Provenance:** the source of the values, or "illustrative" (the sim must then label them so)
- Axis labels and units
- What each series stands for (its meaning, not its color)
- The insight the learner should find, and the question that makes them find it

**Example specification:**
```xml
<details markdown="1">
<summary>Query Performance Comparison: RDBMS vs Graph Database</summary>
Type: chart

Chart type: Bar chart

Purpose: Show performance degradation of RDBMS multi-hop queries compared to constant-time graph traversals

X-axis: Number of hops (1, 2, 3, 4, 5)
Y-axis: Query response time (milliseconds, logarithmic scale)

Data series:
1. RDBMS:
 - 1 hop: 10ms
 - 2 hops: 150ms
 - 3 hops: 2,500ms
 - 4 hops: 45,000ms
 - 5 hops: 780,000ms (timed out)

2. Graph Database:
 - 1 hop: 5ms
 - 2 hops: 8ms
 - 3 hops: 12ms
 - 4 hops: 15ms
 - 5 hops: 18ms

Title: "Multi-Hop Query Performance: RDBMS vs Graph Database"

Provenance: illustrative values that show the growth pattern; the chart labels them "illustrative".

Annotations:
- Arrow pointing to RDBMS 5-hop bar: "Query timed out after 13 minutes"
- Arrow pointing to graph DB series: "Constant-time traversal"
</details>
```

## 8. Timeline

**Type identifier:** `timeline`

**When to use:**
- Showing historical progression
- Illustrating project phases
- Demonstrating evolution of concepts
- Presenting sequential events

Timelines are ideal for putting current events into context.
Timelines can be used at the begging of a textbook to show
the historical events that triggered an important based of knowledge.

**Interactivity requirement (REQUIRED):** Every timeline MUST allow the learner to reveal more detail. At minimum, clicking or hovering an event opens an infobox with the event's description, significance, and links to related concepts. Decorative timelines with no click/hover behavior are NOT permitted.

**Implementation:** Use `<details markdown="1">` block with specification

**Required information in description:**
- Time period covered
- **Content:** every event with its date and the full text its click reveals
- **Provenance:** the source for each date
- Eras or groups the events belong to, if the grouping is part of what is taught
- **Learner Activity:** what the learner reveals, and the question about sequence or cause they answer

**Example specification:**
```xml
<details markdown="1">
<summary>Evolution of Configuration Management Timeline</summary>
Type: timeline

Time period: 1980-2025

Events:
- 1980: Military configuration management practices established
- 1990: ITIL v1 released (31 books including Configuration Management)
- 1995: First commercial CMDB implementations
- 2001: ITIL v2 consolidates CM practices
- 2005-2010: "CMDB crisis" - high failure rates reported
- 2012: Neo4j gains traction for IT dependency management
- 2015: Observability tools (Dynatrace, etc.) begin automated discovery
- 2018: Graph-based CMDB alternatives emerge
- 2020: COVID pandemic accelerates digital transformation
- 2023: AI-assisted IT management graphs
- 2025: Real-time graph-based IT management becomes standard

Eras (each event belongs to one):
- ITIL/traditional CMDB era (1990-2010)
- Transition period (2010-2015)
- Graph database adoption (2015-2020)
- Modern AI-enhanced approaches (2020+)

Provenance: the dates and descriptions come from the chapter section "A Short History of Configuration Management".

Learner Activity: the learner clicks each event to read its description and significance, then answers "Which event came first: the CMDB crisis or graph-based CMDB alternatives?"
</details>
```

## 9. Maps with Movement Arrows

**Type identifier:** `map`

**When to use:**
- Showing geographic distribution
- Illustrating data flows across regions
- Demonstrating adoption patterns
- Visualizing network topologies

**Interactivity requirement (REQUIRED):** Every map MUST be selectable. At minimum, regions, markers, and flow arrows must be clickable or hoverable to reveal the underlying data, jurisdiction rules, transfer requirements, or topology details in an infobox. Decorative maps with no learner feedback are NOT permitted.

**Implementation:** Use `<details markdown="1">` block with specification

**Required information in description:**
- Geographic scope (world, region, country)
- **Content:** every location to mark, with coordinates for points (with their source) or the name for regions
- Directional flows or connections, and what each one means
- Data being represented
- Legend and labels (meanings, not colors)
- **Learner Activity:** what the learner clicks and what each click reveals

**Example specification:**
```xml
<details markdown="1">
<summary>GDPR Data Flow Compliance Map</summary>
Type: map

Geographic scope: World map focusing on EU and major trading partners

Purpose: Illustrate data flow restrictions under GDPR

Locations:
- European Union
- United States
- United Kingdom
- Asia-Pacific data centers

Data flows (arrows), in three categories the learner must tell apart:
- Permitted flows (within EU)
- Conditional flows (EU to UK, adequacy decision)
- Restricted flows (EU to US, requires safeguards)
- Data center backup routes

Labels:
- "GDPR Protected Territory"
- "Adequacy Decision Required"
- "Standard Contractual Clauses (SCCs) Required"

Legend:
- The meaning of each flow category
- Icon explanations (data center, user, cloud)

Interactive features:
- Hover over arrows to see data transfer requirements
- Click regions to see compliance details
</details>
```

## 10. Workflow Diagrams with Hover Text

**Type identifier:** `workflow`

**When to use:**
- Illustrating business processes
- Showing decision trees
- Explaining system interactions
- Demonstrating procedural steps

**Interactivity requirement (REQUIRED):** Every workflow step and decision MUST reveal its hover text or expanded explanation on click or hover. Mermaid flowcharts MUST include `click` directives for every node mapped to an infobox callback. Mermaid cannot make connectors clickable, so put what each connector means in its edge label or in the infobox of the step it leaves. A workflow diagram that is just lines and boxes with no learner feedback is NOT permitted.

**Implementation:** Use `<details markdown="1">` block with specification

**Required information in description:**
- Process name and purpose
- Steps in the workflow (with descriptions)
- Decision points and branches
- Start and end states
- Hover text content for each element, written out in full
- Roles or systems involved (as swimlanes, if the roles are part of what is taught)

**Example specification:**
```xml
<details markdown="1">
<summary>Change Management Workflow with Impact Analysis</summary>
Type: workflow

Purpose: Show the change management process using graph-based impact analysis

Steps:
1. Start: "Change Request Submitted"
 Hover text: "Engineer submits change request for system update"

2. Process: "Query IT Management Graph"
 Hover text: "Run graph traversal to identify all downstream dependencies"

3. Process: "Calculate Blast Radius"
 Hover text: "Determine which services, applications, and business functions are affected"

4. Decision: "Risk Level?"
 Hover text: "Based on blast radius: Low (<10 services), Medium (10-50), High (>50)"

5a. Process: "Auto-Approve" (if Low risk)
Hover text: "Changes affecting fewer than 10 services are auto-approved"

5b. Process: "Manager Review" (if Medium risk)
Hover text: "Changes affecting 10-50 services require manager approval"

5c. Process: "CAB Review" (if High risk)
Hover text: "Changes affecting >50 services require Change Advisory Board review"

6. Process: "Notify Affected Teams"
 Hover text: "Automated notifications sent to all teams managing dependent services"

7. End: "Change Approved"
 Hover text: "Change ticket updated and implementation scheduled"

Swimlanes:
- Requester
- IT Management Graph System
- Approval Authority
- Affected Teams
</details>
```

## 11. Graph Data Models (vis-network)

**Type identifier:** `graph-model`

**When to use:**
- Showing entity relationships
- Demonstrating graph database schemas
- Illustrating dependency networks
- Visualizing knowledge graphs

**Interactivity requirement (REQUIRED):** Every node and every edge MUST be selectable. At minimum, hovering a node shows its properties; clicking a node highlights its neighborhood and reveals its definition in a side panel. The learner must also be able to drag or pan the graph; zooming uses buttons, never the mouse wheel, which would hijack page scrolling in an embedded sim. A static rendering of a graph with no interaction is NOT permitted.

**Implementation:** Use `<details markdown="1">` block with specification

**Required information in description:**
- Node types and their properties
- Edge types and their properties
- **Content:** every node and edge to display, not a sample
- What a click or hover on a node or edge reveals, written out in full
- The question the learner answers by tracing the graph (for example, which services a failed server affects)
- Legend explaining node/edge types (meanings, not colors or shapes)

**Example specification:**
```xml
<details markdown="1">
<summary>IT Management Graph Data Model</summary>
Type: graph-model

Purpose: Illustrate the node and relationship types in a typical IT management graph

Node types:
1. Business Service
 - Properties: name, owner, SLA_target
 - Example: "Customer Portal"

2. Application
 - Properties: name, version, technology_stack
 - Example: "Web Server v2.1"

3. Infrastructure
 - Properties: name, type, location
 - Example: "Server-001 (VM)"

4. Data Store
 - Properties: name, type, size_gb
 - Example: "Customer DB"

Edge types:
1. DEPENDS_ON
 - Properties: criticality (high/medium/low)
 - Example: Business Service → Application

2. HOSTS
 - Properties: deployment_type
 - Example: Infrastructure → Application

3. CONNECTS_TO
 - Properties: protocol, port
 - Example: Application → Data Store

Data (all nodes and edges):
- Customer Portal (Business Service)
├─ DEPENDS_ON → Web Application (Application)
│├─ HOSTS ← VM-Server-001 (Infrastructure)
│└─ CONNECTS_TO → Customer DB (Data Store)
└─ DEPENDS_ON → API Gateway (Application)
 └─ CONNECTS_TO → Auth Service DB (Data Store)

Learner Activity:
- Hover a node: show its properties
- Click a node: highlight every node connected to it
- Double-click: expand or collapse its dependencies
- Question: "If VM-Server-001 fails, which business service is affected?" (answer: Customer Portal, through Web Application)

Legend:
- What each node type means
- What each edge type means
</details>
```

## General Guidelines for All Content Elements

1. **Progressive Complexity:** Place simpler elements earlier in the chapter, more complex ones later
2. **Concept Coverage:** Ensure elements connect back to concepts listed in "Concepts Covered"
3. **Learning Objectives:** Every element should serve a clear pedagogical purpose
4. **Accessibility:** Provide text alternatives for visual elements
5. **Consistency:** Use the same term for the same idea in the prose and in every specification; every number a specification shares with the prose must match
6. **Interactivity:** Favor interactive elements (infographics, MicroSims) that enable student engagement tracking
7. **Balance:** Mix different types of elements rather than using the same type repeatedly

## Details Block Template

For any element requiring specification (types 3-11), use the template in
`microsim-specification-rules.md`:

```xml
#### Diagram: [Title Case Name]

<details markdown="1">
<summary>[Title Case Name]</summary>
Type: [microsim | chart | diagram | infographic | timeline | map | workflow | graph-model | causal-loop]
**sim-id:** [kebab-case-directory-name]<br/>
**Library:** [p5.js | Chart.js | Plotly | Mermaid | vis-network | vis-timeline | Leaflet | venn.js | html]<br/>
**Status:** Specified<br/>
**Bloom Level:** [Remember | Understand | Apply | Analyze | Evaluate | Create]<br/>
**Bloom Verb:** [one verb from that level's list]<br/>
**Learning Objective:** The learner will [verb] [specific content] [condition or criterion].

**Prerequisites:** ...

**Evidence of Mastery:** ...

**Misconceptions:** ...

**Instructional Rationale:** ...

**Content:** ...

**Provenance:** ...

**Rules:** ...

**Learner Activity:** ...

**Feedback:** ...

**Starting State:** ...

**Chapter Anchors:** ...
</details>
```

Do not add an iframe for a new specification; the microsim-generator inserts it after the sim is built.

The six header lines are parsed by the batch tools:
- **sim-id** — kebab-case directory name used for the `docs/sims/{sim-id}/` path
- **Library** — one value from the list; it selects the generator route and CDN
- **Status** — lifecycle state; always `Specified` for new specs in chapter content
- **Bloom Level**, **Bloom Verb** — separate lines with bare values
- **Learning Objective** — one sentence followed by a blank line

The specification must be complete about what the learner learns and sees, so that the generator never has to
invent content, rules or feedback. It must say nothing about how to build the sim.

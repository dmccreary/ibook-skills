---
title: MicroSim Library Routing Table
description: Routing exercise in which the reader reads a request, finds its trigger keywords, and clicks the visualization library the MicroSim Generator should route it to.
image: /sims/microsim-library-routing-table/microsim-library-routing-table.png
og:image: /sims/microsim-library-routing-table/microsim-library-routing-table.png
twitter:image: /sims/microsim-library-routing-table/microsim-library-routing-table.png
social:
   cards: false
quality_score: 100
---

# MicroSim Library Routing Table

<iframe src="main.html" height="537px" width="100%" scrolling="no"></iframe>

[Run the MicroSim Library Routing Table MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }

## About This MicroSim

The MicroSim Generator is a meta-skill. It does not draw anything itself.
It reads a request, finds the words that describe the *shape of the data*,
and routes the request to the one visualization library best matched to it.
This is **visualization library routing**.

The flowchart shows one request entering the generator and six of the
generator's routes fanning out. Each arrow is labeled with some of the trigger
keywords for that route:

| Library | Trigger keywords in the routing table | Best for |
|---------|----------------------------------------|----------|
| p5.js | custom, simulation, physics, interactive, bouncing, movement, p5.js | Custom simulations, physics, and animation |
| Chart.js | chart, bar, line, pie, doughnut, radar, statistics, data | Bar, line, pie, doughnut, and radar charts |
| vis-network | network, nodes, edges, graph, dependencies, concept map, knowledge graph | Graphs of nodes and edges, concept maps |
| vis-timeline | timeline, dates, chronological, events, history, schedule, milestones | Dated events along a time axis |
| Leaflet | map, geographic, coordinates, latitude, longitude, locations, markers | Interactive geographic maps |
| Mermaid | flowchart, workflow, process, state machine, UML, sequence diagram | Flowcharts and other process diagrams |

The keywords are the real trigger keywords for these six rows of the routing
table in the `microsim-generator` skill. The skill has more routes than the
six shown here (Plotly, Venn diagrams, comparison tables, and others), and it
weighs a request with more judgment than the plain keyword count this exercise
uses.

## How to Use

1. Read the request in the white bar above the diagram.
2. Decide which library the generator should route it to, then click that
   library's box.
3. If you are right, the route lights up, the matched keywords are highlighted
   in the request, and the panel shows what that library is best for and one
   example MicroSim.
4. If you are wrong, the panel tells you which keywords that library listens
   for. Try again. After two wrong picks the trigger keywords in the request
   are highlighted as a hint.
5. Select **Next Request** to route another request. There are seven.
6. The last request is ambiguous on purpose. See what the generator does when
   two routes match equally.
7. Click **Incoming Request** or **MicroSim Generator** at any time to read
   what that box does. Keyboard users can press Tab to move between boxes and
   Enter to select one.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/ibook-skills/sims/microsim-library-routing-table/main.html"
        height="537px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Audience

Adult learners, educators, and instructional designers who use AI agent
skills to build intelligent textbooks. No programming background is needed.

### Learning Objective

Demonstrate how a request's keywords route to one of several visualization
libraries. (Bloom's Taxonomy: Apply)

### Duration

10 minutes

### Prerequisites

- Knows what a meta-skill and a trigger keyword table are (Chapter 7)
- Has seen at least one MicroSim built with p5.js (Chapters 21 and 22)

### Activities

1. **Exploration** (2 min): Click **Incoming Request** and **MicroSim
   Generator** and read what each one does.
2. **Guided Practice** (5 min): Route all seven requests. Before each click,
   say out loud which word in the request you are routing on.
3. **Assessment** (3 min): Write one new request for each of three libraries
   of your choice. Swap with a partner and route each other's requests.

### Assessment

- The learner routes at least five of the six unambiguous requests correctly
  on the first try.
- The learner names the trigger keyword that decided each route.
- The learner explains why "Create a graph of our sales data" cannot be routed
  without a clarifying question.

### Discussion Questions

1. The generator routes on the shape of the data, not on the subject of the
   lesson. Why is "dates" a better routing clue than "history of computing"?
2. What would go wrong if every request were sent to p5.js, the most general
   library?
3. Chapter 7 showed a meta-skill routing a request to a reference guide. What
   is the same here, and what is one level more specific?

## References

1. [Chart.js Documentation](https://www.chartjs.org/docs/latest/) - Chart.js - The charting library the generator routes bar, line, pie, and radar chart requests to.
2. [vis-timeline Documentation](https://visjs.github.io/vis-timeline/docs/timeline/) - vis.js - The timeline library used for dated, chronological events.
3. [Leaflet](https://leafletjs.com/) - Leaflet - The open-source JavaScript library used for interactive geographic maps.
4. [Flowcharts Syntax](https://mermaid.js.org/syntax/flowchart.html) - Mermaid - Documentation for the flowchart syntax and the `click` interaction used in this MicroSim.

# MicroSim P5.js

This skill creates interactive educational MicroSimulations using the p5.js JavaScript library with distinct regions for drawing and interactive controls. Each MicroSim is designed for browser-based learning and can be embedded in websites via iframe.

## Step 1: Educational Requirements Specification

Defines the educational purpose before generating code. Identifies the subject area, grade level (K-5, 6-8, 9-12, or undergraduate), learning objectives aligned with Bloom's Taxonomy, estimated duration (5-15 minutes), prerequisites, and assessment opportunities. This information is documented in the index.md file and stored in metadata.json validated against a JSON Schema.

## Step 2: MicroSim Implementation with p5.js

Generates a self-contained, width-responsive p5.js simulation following standardized MicroSim architecture. Creates a folder structure in `/docs/sims/$MICROSIM_NAME` containing: index.md (main documentation with iframe), main.html (HTML5 file with p5.js CDN link), $MICROSIM_NAME.js (all JavaScript code), and metadata.json (Dublin core metadata and control descriptions).

## Canvas Structure Requirements

Implements a two-region layout with fixed heights: a top drawing region (drawHeight) for visualizations with no UI controls, and a bottom control region (controlHeight) for buttons and sliders. The canvas width is responsive and automatically resizes based on container width. Uses standardized color scheme with aliceblue for drawing area and white for controls area.

## Responsive Design Implementation

Implements horizontal responsiveness for embedding in various platforms. Updates canvas size dynamically when container width changes using the windowResized() and updateCanvasSize() functions. All horizontal sliders are automatically repositioned and resized to match new container dimensions.

## Visual Design Standards

Follows consistent design patterns with aliceblue background for drawing area, white background for controls, and silver borders. Uses 36px for title text and 16px minimum for all other text to ensure readability from the back of a classroom. Implements high-contrast, colorblind-safe colors for interactive elements.

## Control Patterns

Provides standardized UI control patterns: horizontal sliders in the control region for continuous parameters (positioned at sliderLeftMargin with width spanning canvas minus margins), buttons for discrete actions (start/pause, reset), and checkboxes for toggle options. All sliders must recalculate their size when container width changes.

## main.html Generation

Creates a minimal HTML5 file with a `<main></main>` element that holds the canvas. Links to p5.js via CDN (currently version 2.3.2), includes the MicroSim JavaScript file, and provides a link back to the lesson plan. Maintains full compatibility with the p5.js editor so code can be pasted directly for testing.

## index.md Generation

Generates a markdown file with YAML frontmatter metadata (title, description, image paths for social media previews). Contains an iframe embedding the MicroSim, buttons for fullscreen viewing and p5.js editor access, a description section, and a lesson plan section. Includes sample iframe code for instructors to embed on their own websites.

## metadata.json Generation

Creates a JSON file conforming to the MicroSim schema containing Dublin Core elements (title, creator, subject, description, date, type, format, language, rights), educational metadata (grade level, learning objectives, Bloom's taxonomy levels, duration, prerequisites), technical metadata (framework, canvas dimensions, dependencies, accessibility features), and UI metadata (controls, parameters, simulation model details).

## Educational Design Principles

Follows five core principles: focused scope (one specific learning objective), immediate feedback (real-time updates), transparent implementation (readable code with educational comments), progressive complexity (simple defaults with gradual sophistication), and cognitive load management (clean interface focusing on educational concepts).

## Quality Standards Verification

Ensures functionality (runs in modern browsers, responsive design, immediate control response), educational quality (addresses learning objectives, meaningful interaction, accurate concept representation), code quality (follows architecture standards, well-commented, meaningful names, accessibility with describe() function), and visual design (clean interface, consistent colors, high contrast, professional appearance).

## Deployment and User Instructions

Generates a zip file containing all MicroSim files ready for installation in the `/docs/sims` directory. Provides instructions for unzipping, testing locally with mkdocs serve, updating mkdocs.yml navigation, and deploying to production with mkdocs gh-deploy. MicroSims are designed for universal deployment via iframe embedding in any LMS (Canvas, Blackboard, Moodle, Google Classroom).

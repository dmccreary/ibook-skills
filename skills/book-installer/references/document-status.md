# Document Status Indicators

## Purpose

Adds per-page colored status dots to the navigation sidebar so authors and reviewers can see at a glance which pages are scaffolded, in progress, or ready for testing. Uses MkDocs Material's built-in `status` metadata feature.

## When to Use

Use this feature when:

- Tracking page lifecycle state (specification → prototype → testing) directly in the nav
- Running a review/approval workflow where a human must sign off on AI-generated content
- Managing a multi-chapter textbook where different chapters are at different stages
- Giving stakeholders a visual progress overview without reading every page

## Trigger Keywords

- `document status`
- `page status`
- `status indicators`
- `status dots`
- `nav status`
- `page lifecycle`
- `review workflow`

## Workflow

### Step 1: Verify Prerequisites

Check that the project has:

1. A valid `mkdocs.yml` file with `theme.name: material`
2. A `docs/css/extra.css` file (or equivalent custom CSS file referenced in `extra_css`)

If the CSS file is missing, create it and add it to `mkdocs.yml`:

```yaml
extra_css:
  - css/extra.css
```

### Step 2: Choose Your Status Codes

Decide on a set of 2-4 status codes that match your workflow. Here are two common patterns:

**Pattern A: Content authoring workflow (recommended for textbooks)**

| Status key | Color | Meaning |
|---|---|---|
| `spec-complete` | Red | Specification complete — outline and learning objectives defined, no prose yet |
| `prototype` | Orange | Initial prototype complete — draft content written, needs review |
| `ready-for-testing` | Green | Ready for testing — content reviewed, ready for classroom pilot |

**Pattern B: MicroSim review workflow**

| Status key | Color | Meaning |
|---|---|---|
| `scaffold` | Red | Specification and scaffold only, no code yet |
| `generated` | Orange | JavaScript generated, awaiting human review |
| `approved` | Green | Reviewed and approved by subject-matter expert |

You can define your own status codes — just keep them short, lowercase, and hyphenated.

### Step 3: Register Statuses in mkdocs.yml

Add the status definitions under the `extra:` key. The value string becomes the tooltip text on hover.

```yaml
extra:
  status:
    spec-complete: "Specification complete"
    prototype: "Initial prototype complete"
    ready-for-testing: "Ready for testing"
```

If you already have an `extra:` section, merge the `status:` block into it — do not create a duplicate `extra:` key (YAML only allows one).

### Step 4: Add CSS for Status Colors

Add the following to your `docs/css/extra.css` (or whichever CSS file is listed in `extra_css`):

```css
/* ============================================
   Document Status Icons (colored circles in nav)
   ============================================ */

/* Red — specification complete */
.md-status--spec-complete::after {
  background-color: #e53935;
}

/* Orange — initial prototype complete */
.md-status--prototype::after {
  background-color: #fb8c00;
}

/* Green — ready for testing */
.md-status--ready-for-testing::after {
  background-color: #43a047;
}
```

Adjust the CSS class names to match your chosen status keys from Step 2. The pattern is always `.md-status--{key}::after`.

### Step 5: Add Status to Page Frontmatter

Add a `status:` field to any page's YAML frontmatter:

```yaml
---
title: "Chapter 5: Private vs. Personal Information"
status: prototype
---
```

The colored dot will appear next to the page title in the navigation sidebar. Hovering over the dot shows the tooltip text you defined in Step 3.

### Step 6: Verify

Run `mkdocs serve` and check:

1. Pages with `status:` frontmatter show a colored dot in the left nav
2. Hovering the dot shows the tooltip text
3. Pages without `status:` show no dot (this is correct — no status means "not yet categorized" or "complete")

## Standard status: `instrumented` (xAPI), with the signal icon

A MicroSim that emits xAPI events gets `status: instrumented`. Its nav icon is **always** the
"signal" icon: the Material Design Icons **access-point** broadcast symbol, in teal
(`#00897b`). That icon is the standard for xAPI instrumentation in every book (Dan,
2026-09-26), so don't substitute a dot or another glyph.

- **Canonical CSS:** `skills/add-xapi-events-to-microsim/assets/status-instrumented.css`.
  It is self-contained: the `--md-status--instrumented` mask variable plus the `:after` and
  hover colors.
- **Tooltip:** `extra.status.instrumented: "Instrumented — the MicroSim emits xAPI events;
  add ?xapi=teaching to the URL to see them"`.
- **Installed and kept in sync by** `add-xapi-events-to-microsim/scripts/sync-status.py
  --book . --apply`. It sets the frontmatter on every sim whose `main.html` loads the xAPI
  runtime (`lrs-sim.js`) and calls `LRSSim.create`, and it adds the CSS and tooltip if the
  book lacks them.

The lifecycle it extends is `specified → scaffolded → implemented → instrumented`. If a book
also uses `implemented`, register it too. Otherwise Material shows its generic info icon
with no tooltip, as the pages did in learning-record-store before 2026-09-26. There,
`implemented` is a blue filled circle (`docs/css/extra.css`).

## How It Works

MkDocs Material renders a `<span class="md-status md-status--{value}">` element next to nav entries when a page has `status:` in its frontmatter. The theme provides a default info-circle glyph. By registering the status in `extra.status`, the tooltip is set. By styling `.md-status--{key}::after`, you control the color.

## Adding a Legend to Your Site

Consider adding a legend to your home page or a project status page so readers understand the dots:

```markdown
## Page Status Legend

| Dot | Meaning |
|-----|---------|
| :red_circle: | Specification complete — outline only |
| :orange_circle: | Initial prototype — draft content |
| :green_circle: | Ready for testing — reviewed content |
```

## Removing Status

To remove a page's status dot, simply delete the `status:` line from its frontmatter. There is no "completed" or "no status" value needed — the absence of the field means the page has no status indicator.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| No dot appears | `status:` not in frontmatter | Add `status: key` to the page's YAML frontmatter |
| Dot appears but wrong color | CSS class doesn't match key | Verify `.md-status--{key}` matches the `extra.status` key exactly |
| Tooltip shows raw key instead of text | Status not registered in `extra.status` | Add the key and tooltip text to `mkdocs.yml` |
| Dot appears but is the default gray | Missing CSS override | Add the `.md-status--{key}::after` rule to extra.css |
| Duplicate `extra:` key warning | Two `extra:` blocks in mkdocs.yml | Merge `status:` into the existing `extra:` block |

## Integration with Feature Checklist

The feature checklist generator (`generate-feature-checklist.py`) automatically detects whether document status indicators are configured by checking for `extra.status` in `mkdocs.yml` and `.md-status--` rules in CSS files. The detection result appears in the "Site-Wide Resources" section of the checklist.

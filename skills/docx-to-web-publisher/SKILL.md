---
name: docx-to-web-publisher
description: Converts .docx files (papers, briefs, reports) into styled React component pages in a Next.js content-catalog site. Use when publishing a Word document as a structured web page.
metadata:
  ibook.version: "1.0"
  ibook.preferred-model: "sonnet"
---

# docx-to-web Publisher

**Version:** 1.0

Convert a .docx document into a fully structured, styled web page within a
Next.js site that uses a content catalog pattern (product array, detail page
route, optional knowledge graph).

## When to use

- User has a `.docx` file and wants it published on their Next.js site
- User says "publish this paper/brief/report" and there's a .docx involved
- User wants to add a research document to a content library or wisdom library
- Converting any structured Word document to a web-rendered page

## Prerequisites

- Next.js App Router project with a content catalog pattern (a TypeScript
  data array + dynamic `[slug]/page.tsx` route)
- ImageMagick (`convert`/`magick`) for cover image generation (optional)
- Python 3 for .docx extraction if pandoc isn't available

## Workflow

### Step 1: Audit the site's content architecture

Before touching the document, understand how the site organizes content.
Find and read:

- **Data catalog file** — the TypeScript array of content items (e.g.,
  `src/data/products.ts`, `src/data/wisdomProducts.ts`). Note the interface
  fields: slug, title, description, author, format, tags, etc.
- **Detail page** — the `[slug]/page.tsx` that renders individual items.
  Note what components it uses and how it handles different content formats.
- **Listing page** — the page that lists all items. Check for format icon
  maps (`Record<Format, Icon>`) that need updating.
- **Knowledge graph** (if present) — tag aliases and taxonomy mappings.
- **Format types** — the union type for content formats. You may need to
  add a new format (e.g., `'research'`).

### Step 2: Extract content from the .docx

Use the approach that's available:

```bash
# Option A: pandoc (best if installed)
pandoc document.docx -t markdown -o content.md

# Option B: Python XML extraction (always available)
python3 -c "
import xml.etree.ElementTree as ET, zipfile, sys
# Extract text with style markers from document.xml
..."
```

If using the docx skill's unpack script, that works too. The goal is to get
the full text with structural markers (heading levels, list items, table
boundaries).

Read the extracted content carefully. Identify:
- Title and subtitle
- Section headings (H1, H2, H3)
- Data tables (columns, rows, header rows)
- Bullet/numbered lists
- Callout boxes or highlighted sections (investor implications, key findings)
- Author attribution and date
- Statistics or key metrics that could become a hero section

### Step 3: Add format type and catalog entry

If the site's format union type doesn't include a suitable format for
research/report content, add one:

```typescript
// In the ProductFormat or ContentFormat type
export type ProductFormat = '...' | 'research';

// In FORMAT_LABELS
research: 'Research Brief',
```

Then add the content item to the data catalog array:

```typescript
{
  slug: 'kebab-case-title',
  title: 'Full Document Title',
  description: '1-2 sentence teaser summarizing the document.',
  longDescription: [
    'Summary paragraph 1 — the challenge or situation.',
    'Summary paragraph 2 — the resolution or key finding.',
    'Summary paragraph 3 — scope of what the full document covers.',
  ],
  author: {
    name: 'Author Name',
    profileHref: '/experts/author-slug',  // if expert profiles exist
  },
  format: 'research',
  coverImage: '/path/to/cover.png',
  tags: ['Tag1', 'Tag2', 'Tag3'],  // choose 5-8 relevant tags
  featured: true,
  createdAt: 'YYYY-MM-DD',
}
```

Update ALL files that use `Record<Format, ...>` — search the codebase for
the format type name. Every icon map, label map, etc. must include the new
format. Missing one causes a TypeScript build error.

### Step 4: Create the rich content component

Create a new file for the full document content. Location pattern:
`src/content/{collection}/{slug}.tsx`

This is the core of the skill. Convert the extracted document structure
into a React server component with proper Tailwind styling:

**Component template:** See `assets/template-content-component.tsx`

Key patterns to follow:

- **Wrapper**: `<article className="prose prose-neutral dark:prose-invert max-w-none">`
- **Tables**: Wrap in `<div className="not-prose overflow-x-auto mb-8 text-neutral-700 dark:text-neutral-200">` — the `not-prose` prevents Tailwind prose from mangling table styles. Always add explicit text colors for dark mode contrast.
- **Callout boxes**: Use colored `div` with border, background, and label (see template for investor/technical/info callout patterns)
- **Stats grids**: `not-prose grid grid-cols-2 md:grid-cols-4` for hero metric blocks
- **Table headers**: Always include `text-neutral-900 dark:text-white` for contrast
- **Table row names**: Add `font-medium text-neutral-900 dark:text-white` to the first column
- **Alternating rows**: `bg-neutral-50 dark:bg-neutral-800/30` on even rows
- **HTML entities**: Use `&mdash;`, `&ndash;`, `&times;`, `&apos;` etc. — never raw special characters in JSX

**Common contrast mistakes to avoid:**
- Tables inside `not-prose` lose inherited text color — always set it explicitly
- Dark mode backgrounds need lighter text — `dark:text-neutral-200` minimum
- Header cells need `dark:text-white` to stand out from body cells
- Green/emerald metric values: use `text-emerald-700 dark:text-emerald-400`

### Step 5: Create the content registry

Create an index file that maps slugs to content components:
`src/content/{collection}/index.ts`

```typescript
import type { ComponentType } from 'react'

type ContentModule = { default: ComponentType }

const contentRegistry: Record<string, () => Promise<ContentModule>> = {
  'my-slug': () => import('./my-slug'),
}

export function hasRichContent(slug: string): boolean {
  return slug in contentRegistry
}

export async function getRichContent(slug: string): Promise<ComponentType | null> {
  const loader = contentRegistry[slug]
  if (!loader) return null
  const mod = await loader()
  return mod.default
}
```

If the registry already exists, just add a new entry.

### Step 6: Extend the detail page

Modify the `[slug]/page.tsx` to:

1. Import `getRichContent` from the content registry
2. Make the page component `async` (if not already)
3. Call `const RichContent = await getRichContent(params.slug)`
4. Render `{RichContent && <div className="mb-8 border-t ..."><RichContent /></div>}` after the summary section
5. Add the new format's icon to any `formatIcons` record

### Step 7: Update the knowledge graph (if present)

If the site has a knowledge graph generator:

1. Add **TAG_ALIASES** for new concept tags (lowercase → display name)
2. Add **TAXONOMY** entries mapping concepts to categories with colors
3. Existing tags that already have aliases/taxonomy entries don't need changes

The document's tags will automatically create new nodes and co-occurrence
edges in the graph at the next build.

### Step 8: Generate a cover image

Create an SVG with the document's title, author, key metrics, and branding,
then convert to PNG:

```bash
# Create SVG (see assets/template-cover.svg for the pattern)
# Convert with ImageMagick
magick cover.svg -resize 800x600 public/path/to/cover.png
```

If ImageMagick isn't available, create a simple placeholder or ask the user
to provide one.

### Step 9: Build and verify

```bash
npm run build  # must pass clean — TypeScript errors = missing format entries
```

Check:
- Detail page renders with full structure
- Listing page shows the new item
- Knowledge graph (if present) shows new concepts
- Dark mode contrast is readable on all tables and callouts

### Step 10: Commit and push

Stage all changed files and commit with a descriptive message.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `Property 'research' is missing in type` | A `Record<ProductFormat, ...>` wasn't updated | Search for all `Record<ProductFormat` and add the new format |
| Tables unreadable in dark mode | `not-prose` strips inherited text color | Add `text-neutral-700 dark:text-neutral-200` to table wrapper div |
| Build fails on page component | `await` used in non-async component | Add `async` to the page function signature |
| Cover image not found | Wrong path or missing file | Verify path matches `coverImage` field in catalog entry |
| Tags not appearing in graph | Missing TAG_ALIASES entry | Add lowercase tag → display name mapping |

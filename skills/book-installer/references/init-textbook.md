
# Init Textbook — Feature #0: New Textbook Scaffold

> Formerly the standalone skill `init-textbook`.

## Purpose

This skill drops a complete, sensible default scaffold into an empty (or
nearly empty) project directory so the user can run `mkdocs serve` and see a
working intelligent textbook within minutes. The scaffold matches the
consensus pattern across our recent textbooks (cybersecurity, networking,
information-systems, ancient-history, statistics-course, token-efficiency,
quantum-computing, world-history, intelligent-textbooks, book-mascots) so the
project starts from the same baseline as everything else in the workspace.

The scaffold is intentionally **minimal-but-complete**: it ships only the
features that every recent textbook ends up using anyway (search, code copy,
admonitions, math via arithmatex, side navigation, CC BY-NC-SA license, the
intelligent-textbook URI scheme, **a `cover.png` plus the social-override
hook that swaps in that cover for the home page**). Everything else — mascots, slide viewer, learning
graph viewer, custom 404, Cairo-based per-page social cards, glightbox image
zoom, Google Analytics, comments, kanban, etc. — is left commented out or
absent so the user can layer it on incrementally via the other
book-installer features once they actually need it.

This separation of concerns matters: the feature #0 scaffold is run **once** at
project birth; the other book-installer features are layered on **many times**
thereafter. Trying to ship every feature in the initial scaffold turned out to
make new books slow to start and littered with config the user didn't
understand. The 40-feature list under book-installer is the menu, not the
default order.

## When to Use

Trigger this skill when the user says any of:

- "init textbook" / "initialize textbook" / "init-textbook"
- "create a new textbook"
- "scaffold a new book"
- "start a new intelligent textbook"
- "set up a new mkdocs textbook project"
- "I'm in an empty directory and want to start a book about X"

Do **not** trigger when:

- The directory already has a `mkdocs.yml` and `docs/` — that's a job for
  the other book-installer features or for individual generator skills.
- The user is asking how to *use* an existing textbook — that's a docs
  question, not a scaffolding job.

## What This Skill Creates

Relative to the project root the user is in:

```
<project-root>/
├── .gitignore                     # Python, MkDocs, OS, and editor ignores
├── {{REPO_NAME}}.code-workspace   # VS Code workspace file
├── mkdocs.yml                     # rendered from assets/init-textbook/mkdocs.yml
├── .gitignore                     # Python / MkDocs / OS / editor ignore patterns
├── AGENTS.md                      # agent instructions — the single source of truth
├── CLAUDE.md                      # contains only `@AGENTS.md` (one line, no other content)
├── CONTENT-GENERATION-GUIDE.md    # read-before-generating rules: CIS-driven word-count
│                                   # targets, anti-padding, MicroSim, and Markdown rules
├── plugins/
│   └── social_override.py         # MkDocs hook: per-page og:image / twitter:image override
└── docs/
    ├── index.md                   # home page
    ├── about.md                   # audience + how to read
    ├── course-description.md      # seed for learning-graph-generator
    ├── contact.md                 # LinkedIn contact info
    ├── license.md                 # CC BY-NC-SA 4.0 deed
    ├── chapters/
    │   └── index.md               # "list of chapters" landing page
    ├── learning-graph/
    │   └── index.md               # learning-graph section landing page
    ├── sims/
    │   └── index.md               # MicroSim catalog landing page
    ├── css/
    │   └── extra.css              # cover-image + iframe styles
    ├── js/                        # empty — populated by book-installer features
    └── img/
        ├── cover.png              # generic 1731×909 cover (replace with book-specific art)
        └── license.png            # CC BY-NC-SA 4.0 badge image
```

All template files use `{{PLACEHOLDER}}` markers that the skill substitutes
with values gathered from the user.

## Inputs the Skill Must Gather

Before writing any files, ask the user for the following. Provide sensible
defaults where possible and let the user accept them with a single yes.

| Variable | Default | Notes |
|----------|---------|-------|
| `SITE_NAME` | (none — must ask) | The book's title in title case (e.g. "Quantum Computing") |
| `SITE_DESCRIPTION` | (none — must ask) | One-sentence description for SEO + social sharing |
| `SITE_AUTHOR` | "Dan McCreary" | Inferred from the `git config user.name` if available |
| `GITHUB_USERNAME` | "dmccreary" | Inferred from `git remote get-url origin` if available |
| `REPO_NAME` | basename of current directory | Inferred from `pwd` |
| `LINKEDIN_URL` | "https://www.linkedin.com/in/danmccreary/" | Author's LinkedIn — optional override |
| `PRIMARY_COLOR` | "indigo" | Material palette primary — common picks: indigo, blue, green, brown, deep orange |
| `ACCENT_COLOR` | "orange" | Material palette accent |
| `YEAR` | current year (2026) | For the copyright line |

If the user is in a hurry and says "use defaults", accept the inferred values
and proceed. Always confirm the substituted values back to the user in a
single block before writing files, so they can spot a wrong repo name or a
typo'd title.

## Workflow

### Step 1 — Verify the directory is fit for scaffolding

Run `ls -la` in the project root. The skill should refuse to overwrite when
any of these already exist:

- `mkdocs.yml`
- `docs/index.md`
- `docs/license.md`

If any are present, stop and tell the user — they likely want
`book-installer` instead. Do not silently merge or overwrite; the user's
existing content is the authoritative source.

### Step 2 — Gather inputs

Infer what you can:

```bash
git config user.name                 # → SITE_AUTHOR fallback
git remote get-url origin 2>/dev/null # → parse for GITHUB_USERNAME and REPO_NAME
basename "$(pwd)"                    # → REPO_NAME fallback
date +%Y                             # → YEAR
```

**Ensure the git branch is `main`.** This project's convention is `main`,
never `master` (see `edit_uri: 'blob/main/docs'` in
`assets/init-textbook/mkdocs.yml`, and every generated GitHub Pages URL). A
bare `git init` still defaults to `master` on many systems unless the user
has set `init.defaultBranch`, so don't rely on it:

```bash
if [ ! -d .git ]; then
  git init -b main                    # new repo — create it on main directly
else
  current_branch=$(git branch --show-current)
  if [ -z "$current_branch" ]; then
    # repo exists but has no commits yet — safe to repoint before the first commit
    git symbolic-ref HEAD refs/heads/main
  elif [ "$current_branch" != "main" ]; then
    echo "Repo is already on branch '$current_branch', not 'main'."
  fi
fi
```

If the repo already has commits on a branch other than `main`, do not rename
it silently — that can break anything already pushed to a remote under that
name. Tell the user and ask before running `git branch -m main`.

Then ask the user once, in a single grouped prompt, for the remaining values
(`SITE_NAME`, `SITE_DESCRIPTION`, palette preferences) and to confirm the
inferred values. Do not pepper them with one-question-at-a-time prompts.

### Step 3 — Confirm the substitution table

Before writing anything, echo the resolved values back so the user can
correct them in one shot. Example:

```
About to scaffold:
  SITE_NAME         = Quantum Computing for Skeptics
  SITE_DESCRIPTION  = An interactive intelligent textbook examining...
  SITE_AUTHOR       = Dan McCreary
  GITHUB_USERNAME   = dmccreary
  REPO_NAME         = quantum-computing
  PRIMARY_COLOR     = indigo
  ACCENT_COLOR      = orange
  YEAR              = 2026

Site URL will be: https://dmccreary.github.io/quantum-computing/
Proceed? (yes/no)
```

### Step 4 — Create directories and copy templates

Create the directory tree shown above with `mkdir -p`. Then copy each file
from `assets/init-textbook/` into the project, performing placeholder
substitution on the text files.

For text files, do a simple in-place substitution of every `{{VAR}}` token
(e.g. `{{SITE_NAME}}`, `{{SITE_DESCRIPTION}}`, etc.) with the value gathered
in Step 2. Use a small inline `sed` or Python step — do not require any
external dependencies.

For `docs/img/license.png` and `docs/img/cover.png`, copy the binaries as-is
(no substitution). Exclude image files from the substitution pass — running a
text rewriter over a PNG corrupts it.

**Agent instruction files — renamed on copy.** These two ship with a
`.template` suffix and must be renamed as they are copied, the same way
`project.code-workspace` becomes `{{REPO_NAME}}.code-workspace`:

| Asset | Copied to | Substitution |
|---|---|---|
| `AGENTS.md.template` | `AGENTS.md` | normal `{{VAR}}` pass |
| `CLAUDE.md.template` | `CLAUDE.md` | none — copy verbatim |

`AGENTS.md` is the single source of truth for agent rules. `CLAUDE.md` must end
up containing exactly one line, `@AGENTS.md`, so Claude Code imports the shared
rules instead of carrying a second copy that drifts. Never expand `CLAUDE.md`
with project rules — put them in `AGENTS.md` where every agent can read them.

The `.template` suffix exists because an unsuffixed `CLAUDE.md` sitting in
`assets/init-textbook/` is a live instruction file, not inert data: any agent
session whose working directory is at or below that assets directory loads it
and tries to import a template `AGENTS.md` still full of `{{PLACEHOLDER}}`
tokens. Suffixing both files keeps them inert until the scaffold renames them
into a real book. Do not drop the suffix to "simplify" the copy step.

**Ordering footgun.** If you implement the substitution as a shell loop reading
values from environment variables, export the variables *before* the loop runs.
Exporting them afterward makes every `{{VAR}}` expand to the empty string, and
the failure is silent — you get a valid-looking `mkdocs.yml` with
`site_name: ''` and `site_url: 'https://.github.io//'`. After substituting,
always assert that no tokens remain and no values are blank:

```bash
grep -rn '{{[A-Z_]*}}' . --exclude-dir=.git || echo "no placeholders left"
grep -nE "^(site_name|site_description|site_url):" mkdocs.yml

# No asset should survive the copy still wearing its .template suffix.
find . -name '*.template' -not -path './.git/*' | grep . && echo "ERROR: unrenamed template" || echo "no stray templates"

# CLAUDE.md must be the one-line pointer, nothing more.
[ "$(tr -d '[:space:]' < CLAUDE.md)" = "@AGENTS.md" ] && echo "CLAUDE.md OK" || echo "ERROR: CLAUDE.md is not the one-line pointer"
```

### Step 5 — Verify the result builds

After scaffolding, suggest the user run:

```bash
pip install mkdocs mkdocs-material
mkdocs build --strict
```

`--strict` will catch broken nav links right away. The scaffold is designed
to pass `--strict` with no chapter content yet, because every nav entry that
points at a not-yet-generated file is left commented out.

Confirm the social-override hook is wired correctly by checking that the
built home page's `og:image` and `twitter:image` point at the declared
cover (not whatever Material's defaults emit):

```bash
grep -E '(og|twitter):image' site/index.html
# expect: both URLs are absolute and end with /img/cover.png
```

If the URLs don't point at `cover.png`, the hook didn't load — re-check
that `hooks:` is a top-level `mkdocs.yml` key (not nested under
`plugins:`) and that `plugins/social_override.py` is at the project root,
not under `docs/`. (The hook only acts on pages that declare `image:` in
frontmatter; the scaffold's `docs/index.md` template does, so a clean
scaffold will pass this check on the home page.)

Do **not** run `mkdocs serve` yourself — per project CLAUDE.md, the user runs
their own `mkdocs serve` in their terminal and watches it for rebuilds.

### Step 6 — Print the next-steps menu

End by pointing the user at `book-installer` for everything else. Show this
exact list (it mirrors the book-installer feature checklist) so the user
knows what is **not** in the scaffold and how to add each thing later:

```
Scaffold complete. Next steps via book-installer features:

  Branding & content polish
    2.  Site logo                       (book-installer 2)
    3.  Favicon                         (book-installer 3)
    4.  Cover image & social preview    (book-installer 4)
    5.  Math equations (KaTeX/MathJax)  (book-installer 5)
    8.  Mermaid diagrams                (book-installer 8)
   10.  Image zoom (GLightbox)          (book-installer 10)
   11.  Custom prompt admonitions       (book-installer 11)

  Educational features
   12.  Interactive quizzes             (book-installer 12)
   23.  Learning graph viewer           (book-installer 23)
   30.  Learning mascot                 (book-installer 30)
   31.  Instructor's guide              (book-installer 31)
   33.  Document status indicators      (book-installer 33)
   37.  Slide generator                 (book-installer 37)

  Engagement & analytics
   15.  Simple feedback (thumbs)        (book-installer 15)
   16.  Detailed comments (Giscus)      (book-installer 16)
   25.  Google Analytics                (book-installer 25)

  Project hygiene
   24.  Skill usage tracker             (book-installer 24)
   29.  Feature checklist (auto-detect) (book-installer 29)
   34.  Kanban project board            (book-installer 34)
   36.  About page (richer)             (book-installer 36)
   38.  Reading level analysis          (book-installer 38)

Then, when the course-description.md is filled in:
   - course-description-analyzer  (validate completeness)
   - learning-graph-generator     (build 200-concept DAG)
   - book-chapter-generator       (design chapter structure)
   - chapter-content-generator    (fill chapters)
   - microsim-generator           (interactive sims)
   - glossary-generator, faq-generator, quiz-generator
```

The numbers match the book-installer feature checklist (Step 1 of SKILL.md)
so the user can paste the number straight back into book-installer.

## Why these defaults and not others

Every choice here is the consensus across the 10 most recent textbooks in the
workspace. The reasoning is worth understanding so the skill can be extended
sensibly:

- **No `navigation.tabs`.** The project CLAUDE.md is explicit: these books
  use side navigation optimized for wide landscape screens. Top tabs waste
  vertical space.
- **`pymdownx.arithmatex` is enabled but no MathJax/KaTeX JS yet.** Every
  recent book ends up needing equations. The extension itself is cheap to
  enable; the renderer is a one-line book-installer add. Generating math
  output without a renderer simply renders LaTeX as code, which is harmless.
- **`exclude_docs:` is populated up front.** Without it, every book ends up
  with `image-prompt*.md` and `TODO.md` files leaking into the search index
  and sitemap. The exclude block is small and cheap.
- **`extra.schema:` URI is always present.** This is how books are
  discovered as intelligent textbooks across GitHub; cost is one line, value
  is real.
- **`generator: false` is on by default.** Every recent book sets this;
  no point omitting it from the scaffold.
- **`watch:` lists `docs` and `mkdocs.yml`.** This makes `mkdocs serve`
  reload on config edits, which is what the user expects.
- **No `social` plugin in the default, but the social-override hook IS on.**
  The `mkdocs-material[imaging]` `social` plugin needs `pip install
  "mkdocs-material[imaging]"` plus a system-level Cairo install on macOS,
  so it's left commented out — failing on first build is a worse experience
  than a comment that says how to enable it. In its place, the scaffold
  ships `plugins/social_override.py` (loaded via `hooks:`). The hook has
  one job: when a page declares `image:` in its frontmatter, it overrides
  that page's `og:image` and `twitter:image` with `site_url + image`.
  Pages without `image:` are untouched — Material's default meta tags (and
  the social plugin's generated card image, if enabled) pass through.

  This produces a clean two-mode behavior that matches author intent:

  1. **Social plugin enabled, no `image:` frontmatter on a page** →
     crawlers see the per-page auto-generated `/assets/images/social/<page>.png`
     card.
  2. **Page declares `image:` frontmatter** → crawlers always see that
     image, regardless of whether the social plugin is enabled. The
     declared image wins over the generated card.

  The scaffold's `docs/index.md` template declares `image: img/cover.png`,
  so the home page unfurls with the book cover out of the box and verifies
  clean against `~/.local/bin/bk-check-social-cover`. Chapter pages don't
  declare `image:` and inherit whichever default is active.

  **Historical footgun:** an earlier version of this template shipped a
  broken `social_override.py` written as a `BasePlugin` class but loaded via
  `hooks:`. MkDocs hooks expect top-level functions, not classes, so the
  module imported with no effect and books had no Open Graph tags at all —
  silently. The current template uses the top-level-function form
  (`on_post_page(html, page, config, **kwargs)`). Don't refactor it back
  into a class without also moving the load mechanism to `plugins:` + an
  entry-point registration.

  **Second historical footgun:** a later version of this hook tried to be
  helpful by injecting all nine og:* / twitter:* tags on every page and
  defaulting every page's image to `img/cover.png` site-wide. That
  clobbered Material's own meta tags and forced the book cover onto every
  chapter unfurl regardless of author intent. The current hook is
  per-page-explicit: no `image:` in frontmatter means the hook is a
  no-op.
- **No mascot logo path baked in.** Several recent books point `theme.logo`
  at `img/mascot/neutral.png` — but only after the mascot exists. Pointing
  at a missing file breaks the build. The scaffold leaves `theme.logo`
  commented out and the `learning-mascot` book-installer feature wires it
  up later.
- **Light palette only at first.** Auto light/dark with custom colors (as
  in cybersecurity, networking, information-systems) requires a non-trivial
  CSS file. The scaffold uses a single Material palette pair (indigo/orange
  by default, easily swapped) and lets the user opt into dark mode later
  via book-installer if they want it.
- **`CONTENT-GENERATION-GUIDE.md` ships from birth, not bolted on later.**
  This file used to be created only by the `learning-mascot` feature (#30),
  which meant any book that skipped a mascot had no home for the
  content-generation rules that `chapter-content-generator` and
  `book-chapter-generator` actually depend on — most importantly the
  CIS-driven Elaboration Budget (Step 2.3b of `chapter-content-generator`),
  which needs the anti-padding rules right next to it to keep agents from
  padding low-tier concepts to "feel complete." Scaffolding it at project
  birth means every book gets these rules regardless of whether it ever adds
  a mascot. If `learning-mascot` is installed later, it inserts its
  `## Learning Mascot` and `## Quality Assurance & Validation` sections into
  this existing file rather than creating a second copy (see
  `learning-mascot.md`, Step 7).
- **`AGENTS.md` holds the agent rules; `CLAUDE.md` is a one-line pointer.**
  Earlier books duplicated the same instructions into both files, and the two
  copies drifted — `quantum-computing` and `information-systems` each carry a
  byte-identical 374- and 215-line pair that has to be edited twice to stay in
  sync, and any agent reading only one of them gets a stale rule set. The
  scaffold now writes the real content **once** to `AGENTS.md` and makes
  `CLAUDE.md` contain exactly `@AGENTS.md` and nothing else — Claude Code
  resolves the `@` as an import, and every other agent (Codex, Cursor, Copilot)
  reads `AGENTS.md` natively. One file to edit, every agent sees the same
  rules. `p5-textbook` is the reference implementation of this pattern.

  **Do not "helpfully" copy the rules back into `CLAUDE.md`.** A `CLAUDE.md`
  longer than one line means the split has been broken and the drift is back.

## MicroSim Status Indicators

Every scaffolded book ships with a colored status indicator wired into the
left nav for `docs/sims/<sim>/index.md` pages. The vocabulary is fixed at
three values and the indicator is glanceable at a distance:

| Status     | Color  | Meaning                                            |
|------------|--------|----------------------------------------------------|
| `scaffold` | red    | Spec exists; no implementation yet.                |
| `built`    | orange | Implementation exists; not yet reviewed by author. |
| `approved` | green  | Author tested it and approved it for learners.     |

How to use the vocabulary:

- **`scaffold`** — every MicroSim `index.md` should be born with
  `status: scaffold` in its frontmatter. The `microsim-generator` skill (and
  any sim-scaffolding skill that follows this convention) sets this when
  it first writes the file.
- **`built`** — once a generator writes a real implementation (substantive
  HTML/JS in the sim directory, not just a placeholder), it should bump the
  status to `built`. The book author still needs to sign off.
- **`approved`** — the human author flips this manually after they've
  loaded the sim, exercised the controls, and confirmed the learning value.
  Generators should never auto-advance to `approved`.

The plumbing is already in place after `init-textbook` runs:

- `mkdocs.yml` has `extra.status` declaring the three names with tooltip
  text (Material won't render the indicator unless the name is registered
  here).
- `docs/css/extra.css` defines `--md-status--scaffold`, `--md-status--built`,
  and `--md-status--approved` as CSS custom properties holding inline SVG
  data URIs, plus the `:after` rules that paint them red/orange/green.

**Do not add `theme.icon.status` to `mkdocs.yml`.** The Material docs make
this look like the right knob for setting status icons; on the community
edition it is silently ignored and the indicator falls back to a generic
"i in a circle" icon with no build-time warning. The CSS-variable approach
in `extra.css` is what actually works on community Material and is the
load-bearing piece. (This footgun cost an afternoon to track down on the
xapi-course book — see `xapi-course/logs/microsim-status-icons.md` for the
full incident report.)

If a future book wants a fourth status (e.g. `in-review`) or different
colors, the pattern is: add an `extra.status.<name>` entry to `mkdocs.yml`,
and add a matching `--md-status--<name>` CSS variable + `.md-status--<name>:after`
rule + `.md-status--<name>:hover:after` rule to `extra.css`. Keep the two
files in sync — adding only one half is the failure mode.

## Footgun Avoidance

- **Never overwrite an existing `mkdocs.yml`.** The Step 1 check is
  load-bearing: the silent-overwrite footgun (delete user's careful nav
  list, replace with template) is exactly the kind of damage that's hard to
  undo if it makes it into a commit.
- **Confirm substitutions in one block before writing.** A typo in
  `REPO_NAME` ripples into the site URL, edit URI, and copyright link.
  Showing the resolved table and waiting for "yes" makes the error visible
  before files exist.
- **Do not enable plugins that need extra pip installs by default.**
  Default-enabled `social` plugin would fail-on-first-build for any user
  without Cairo installed. Users hate "fresh project doesn't build."

## Files for this feature

```
book-installer/
└── assets/
    └── init-textbook/
        ├── .gitignore                         # Python, MkDocs, OS, editor ignores
        ├── project.code-workspace             # VS Code workspace (renamed to {{REPO_NAME}}.code-workspace)
        ├── mkdocs.yml                         # the main config template
        ├── AGENTS.md.template                 # → AGENTS.md; {{SITE_NAME}}/{{REPO_NAME}} substituted
        ├── CLAUDE.md.template                 # → CLAUDE.md; verbatim one-liner `@AGENTS.md`
        ├── CONTENT-GENERATION-GUIDE.md        # copied to project root, {{SITE_NAME}} substituted
        └── docs/
            ├── index.md
            ├── about.md
            ├── course-description.md
            ├── contact.md
            ├── license.md
            ├── chapters/
            │   └── index.md
            ├── learning-graph/
            │   └── index.md
            ├── sims/
            │   └── index.md
            ├── css/
            │   └── extra.css
            └── img/
                ├── cover.png                  # generic 1731×909 cover image (replace with book-specific art)
                └── license.png                # CC BY-NC-SA 4.0 badge
```

## Examples

### Example 1: Fresh start, defaults

**User:** "init textbook"

**Skill response:**
1. `ls -la` shows directory is empty (or just has `.git/`).
2. Read `git config user.name`, `git remote get-url origin`, `basename "$(pwd)"`.
3. Ensure the repo exists and is on branch `main` (`git init -b main` if no `.git/` yet).
4. Ask the user for `SITE_NAME` and `SITE_DESCRIPTION`; offer to default the rest.
5. Echo the resolved table; wait for confirmation.
6. Create directories, copy + substitute templates, copy `license.png`.
7. Suggest `mkdocs build --strict`.
8. Print the next-steps menu pointing at `book-installer`.

### Example 2: Directory already has content

**User:** "scaffold a new textbook"

**Skill response:** notices `mkdocs.yml` is present, refuses to overwrite,
suggests the user either use other book-installer features to enrich the
existing project, or run feature #0 from a fresh directory.

### Example 3: User wants a specific palette

**User:** "init-textbook for a biology book, primary=green accent=amber"

**Skill response:** uses `green` / `amber` for the palette in mkdocs.yml,
proceeds with the rest of the defaults inferred from git, asks only for
`SITE_NAME` and `SITE_DESCRIPTION`.

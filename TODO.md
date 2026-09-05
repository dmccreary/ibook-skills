# TODO

## Mascot generation: account for the padding-trim script

Update the mascot generation steps to be aware of the new python
program that removes the extra padding around the mascot images.
`src/image-utils/trim-padding-from-image.py`

(Carried over from the previous TODO.md. The original note pointed at
`@src/image-utils/trip-padding-from-image.py`; the file on disk is
`trim-padding-from-image.py`.)

---

# Follow-up from the `claude-skills` → `ibook-skills` rename

The rename itself is complete and verified: the GitHub repo is
`dmccreary/ibook-skills`, this repo's references are updated and pushed
(commit `226f8216`), the local directory is `~/Documents/ws/ibook-skills`,
and all 89 tool symlinks plus `BK_HOME` resolve correctly.

The items below are what's left. Nothing here blocks day-to-day use of the
skills — they all work now.

---

## 1. Deploy the site (the live build is stale)

`https://dmccreary.github.io/ibook-skills/` still serves the build from
**before** the rename (deployed from `fa205dc5`), so the homepage HTML still
contains 9 hard-coded `claude-skills` URLs. GitHub's rename redirect covers
them for now, but the deployed `site_url` is wrong until redeployed.

```bash
cd ~/Documents/ws/ibook-skills && mkdocs gh-deploy
```

Verify afterwards — this should print `0`:

```bash
curl -s https://dmccreary.github.io/ibook-skills/ | grep -c "claude-skills"
```

---

## 2. Push the other repos (112 with unpushed commits)

Two separate sweeps committed locally but did **not** push:

- **103 repos, 258 files** — the `claude-skills` → `ibook-skills` reference
  update, subject `Update claude-skills repo references to ibook-skills`
- **56 repos** — the `edit_uri` branch fix, subject
  `Point mkdocs edit_uri at main instead of master`

Together with pre-existing unpushed work, **112 repos** currently have commits
that have not been pushed.

Review what is pending before pushing anything:

```bash
cd ~/Documents/ws && for r in */; do r="${r%/}"; [ -d "$r/.git" ] || continue; n=$(git -C "$r" log @{u}..HEAD --oneline 2>/dev/null | wc -l | tr -d ' '); [ "$n" != "0" ] && { echo "=== $r ($n)"; git -C "$r" log @{u}..HEAD --oneline; }; done
```

That list includes any unpushed work of your own, so read it before running
the push:

```bash
cd ~/Documents/ws && for r in */; do r="${r%/}"; [ -d "$r/.git" ] || continue; [ "$(git -C "$r" log @{u}..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')" != "0" ] && { echo "--- $r"; git -C "$r" push; }; done
```

Many of these are MkDocs books whose **published sites** also carry the old
name. Pushing updates the source; each book still needs its own
`mkdocs gh-deploy` for the live site to change.

Note that many of these are MkDocs books whose **published sites** also have
the old name baked in. Pushing updates the source; each book still needs its
own `mkdocs gh-deploy` for the live site to change.

---

## 3. Six files rewritten but deliberately left uncommitted

These files had the old name **and** already had your uncommitted work in
them. They were rewritten on disk, but not staged — committing them would
have swept unrelated in-progress changes into the rename commit. Review each
and commit alongside whatever else you were doing:

- `Dementia/docs/learning-graph/book-metrics.json`
- `Digital-Transformation-with-AI-Spring-2026/docs/learning-graph/book-metrics.json`
- `book-dashboard/docs/book-data/books.json`
- `intelligent-textbooks/docs/case-studies/index.md`
- `learning-graphs/docs/learning-graph/book-metrics.json`
- `robot-faces/docs/learning-graph/book-metrics.json`

`book-dashboard` is the one to look at first — it was the only repo where
*every* hit was already dirty, so it got no rename commit at all.

The `edit_uri` sweep left five more `mkdocs.yml` files in the same state —
corrected on disk, not committed, because they already held your changes:

- `Dementia/mkdocs.yml`
- `algebra-1/mkdocs.yml`
- `fft-benchmarking/mkdocs.yml`
- `learning-graphs/mkdocs.yml`
- `robot-faces/mkdocs.yml`

---

## 4. Clean up 15 stale symlinks (pre-existing, not caused by the rename)

These were **already broken before the rename** — verified against commit
`fa205dc5`. They point at skills and scripts that were consolidated into
meta-skills or deleted earlier. The rename just repointed them at the
equally-nonexistent new path.

Sub-skills consolidated into meta-skills:

- `~/.agents/skills/book-metrics-generator` → now `book-installer`
- `~/.agents/skills/concept-classifier` → now `microsim-generator`
- `~/.agents/skills/diagram-reports-generator` → now `microsim-utils`
- `~/.agents/skills/linkedin-announcement-generator` → now `book-publisher`
- `~/.agents/skills/readme-generator` → now `book-publisher`
- `~/.agents/skills/story-generator` → now `book-media-generator`
- `~/.agents/skills/moving-rainbow` → lives in the `moving-rainbow` repo

Scripts and commands that no longer exist in this repo:

- `~/.claude/commands/skills.md` (only `commands/ibook.md` exists now)
- `~/.local/bin/bk-book-status`
- `~/.local/bin/book-status`
- `~/.local/bin/install-claude-skills`
- `~/.local/bin/install-scripts`
- `~/.local/bin/install-skills-command`
- `~/.local/bin/list-skills`
- `~/.local/bin/list-skills-format`

Remove every broken link in those directories:

```bash
find ~/.agents/skills ~/.claude/skills ~/.claude/commands ~/.codex/skills ~/.gemini/config/skills ~/.local/bin -maxdepth 2 -type l ! -exec test -e {} \; -print -delete
```

Then re-run `scripts/bk-install-skills` to regenerate the current set.

---

## 5. Decide on two naming side-effects of the full sweep

The sweep replaced **every** occurrence of the string, including places where
"claude-skills" named the *subject* rather than this repository. Both of these
are worth a second look, since the content teaches Claude Skills as an
Anthropic feature:

- **`install-claude-skills.sh` → `install-ibook-skills.sh`** throughout the
  chapter 2 and chapter 9 teaching content and quiz questions. This script
  doesn't exist in the repo — it's a worked example about installing Claude
  skills — so the old name arguably described it better.
- **`docs/chapters/09-ibook-skills-architecture-development/`** while its H1
  is still "Claude Skills Architecture and Development". The directory name
  and the chapter title now disagree. Same situation for
  `docs/chapters/02-getting-started-ibook-skills/` ("Getting Started with
  Claude and Skills") and `docs/slides/ibook-skills-overview/`.

Reverting any of these means renaming the directory back, updating the
`mkdocs.yml` nav entries, and fixing the inbound cross-links.

---

## 6. Restart your environment

Not really a task, but it will bite until done:

- **Restart `mkdocs serve`** — the running process is still watching the old
  `~/Documents/ws/claude-skills` path and will not see file changes.
- **Open a new terminal**, or run `source ~/.zshrc` in existing ones — old
  shells still export the old `BK_HOME`.

---

## Reference: what the rename actually touched

- **GitHub**: repo renamed; old URL 301-redirects; Pages serves at the new URL
- **This repo**: 212 files in commit `226f8216` — `mkdocs.yml`, `.claude/mcp.json`,
  `.gitignore`, all `scripts/bk*` helpers, the `.code-workspace` file, two
  chapter directories, and `docs/slides/`
- **Machine config**: `~/.zshrc` (`BK_HOME`), `~/.claude/CLAUDE.md`,
  `~/.claude/settings.json`, `~/.claude/settings.local.json`, and both
  auto-commit hooks — renamed to `auto-commit-ibook-skills-stop.sh` and
  `track-ibook-skills-edits.sh`, with `CLAUDE_SKILLS_REPO` now
  `IBOOK_SKILLS_REPO`
- **Symlinks**: 89 repointed across `.claude/skills`, `.claude/commands`,
  `.local/bin`, `.agents/skills`, `.codex/skills`, `.gemini/config/skills`
- **Left alone on purpose**: `logs/` session transcripts, so they keep
  describing the commands that were actually run at the time

<!-- p5js-v2-audit-2026-09-05 -->
## p5.js 2.x Upgrade: MicroSim Fixes Needed (2026-09-05)

A static scan of this repo's `docs/sims/` MicroSims found **1 sim(s)** using p5.js v1-only APIs that will break if upgraded to p5.js 2.x (the microsim-generator skill's templates now default to p5@2.3.2). Fix these before bumping this repo's MicroSims past p5@1.x.

- [ ] **course-description-quality-workflow** (`docs/sims/course-description-quality-workflow/`)
    - `course-description-quality-workflow.js` uses `preload()`, which p5.js v2 removed entirely — move the loading calls into `async function setup()` and `await` each `load*()` call before `createCanvas()`.

Reference: [p5.js Teachers' Guide to v2 transition](https://p5js.org/tutorials/v2_transition/)

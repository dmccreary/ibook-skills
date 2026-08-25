# Consistent Skill Versioning Across the Library

**Date:** August 25, 2026
**Project:** ibook-skills/skills
**Commit:** `16c76971` (shared with the mascot placement-rules change — see
[`consistent-mascot-placement.md`](consistent-mascot-placement.md))

## Summary

Version tracking across the 14 active skills was inconsistent: five carried a
version in four different formats, nine had none at all, and every version lived
in prose rather than anywhere machine-readable. This session gave all 14 a version
in a single canonical field, bumped the minor component on those that had one, and
established `1.0` as the starting point for those that did not.

## Problem Statement

A survey of `skills/*/SKILL.md` found no `version:` field in any frontmatter.
Versions existed only as body text, in four incompatible formats:

| Skill | Version found | Format |
|-------|---------------|--------|
| `book-chapter-generator` | `1.0.0` | 3-part semver |
| `chapter-content-generator` | `Version 1.09` | 2-part, zero-padded minor |
| `learning-graph-generator` | `v1.06` | 2-part, zero-padded minor |
| `course-description-analyzer` | `Version 0.03` | 2-part, zero-padded minor |
| `quiz-generator` | `v0.4` | 2-part, single-digit minor |

The other nine skills — `book-installer`, `book-media-generator`,
`book-publisher`, `docx-to-web-publisher`, `faq-generator`, `glossary-generator`,
`microsim-generator`, `microsim-utils`, `reference-generator` — had no version at all.

Because versions lived only in prose, some skills repeated their own version in
user-facing output strings (`"Quiz Generator Skill v0.4 running in serial mode."`),
creating four independent places per skill that could fall out of sync.

## Design Decisions

### Where the version lives: `metadata.ibook.version`

```yaml
metadata:
  ibook.version: "1.10"
```

The obvious choice — a top-level `version:` key — would have been a **latent
packaging failure**. The repo's own portability guide
(`docs/appendices/skill-portability-strategy/index.md`, "The hard-error rule")
documents that strict validation accepts exactly six frontmatter fields:

```
allowed-tools, compatibility, description, license, metadata, name
```

Anything else fails the *entire package* with `Unexpected key(s) in SKILL.md
frontmatter`, blocking upload to claude.ai, the Skills API, and
`package_skill.py` — and with it Cowork sessions, cloud sessions, and scheduled
routines. `metadata:` is the spec-blessed escape hatch that every client accepts
and none interprets. The `ibook.` namespace prefix follows the same guide's
recommendation and matches its worked example.

This is the same class of trap as the `~/.claude/skills/` path form corrected in
the mascot work: the intuitive choice is the non-portable one.

### Each skill also keeps a visible `**Version:**` line

Four skills already had one under their H1. Rather than remove them, all 14 now
carry one, so a human reading `SKILL.md` sees the version without parsing YAML.
A verification pass asserts frontmatter and body agree for every skill.

### Version numbers assigned

| Skill | Before | After |
|-------|--------|-------|
| `book-chapter-generator` | 1.0.0 | **1.1.0** |
| `chapter-content-generator` | 1.09 | **1.10** |
| `learning-graph-generator` | 1.06 | **1.07** |
| `quiz-generator` | 0.4 | **0.5** |
| `course-description-analyzer` | 0.03 | **0.04** |
| nine previously unversioned skills | — | **1.0** |

Existing formats were **preserved rather than normalised**. Rewriting
`book-chapter-generator` from `1.0.0` to `1.1` would have dropped the patch
component that `chapter-content-generator` cites in a compatibility constraint.
Consistency of *format* was judged less valuable than not breaking live references.

`1.0` for the nine new ones follows the precedent `book-chapter-generator` set
when it declared 1.0.0 its "first tracked version number for this skill." They were
given a version, not a version *and* a bump — the user asked to add one, and adding
then immediately incrementing would overstate the change.

### Self-references bumped, compatibility floors left alone

This distinction mattered and was checked explicitly:

- **Self-references** — a skill naming its own version in output, e.g.
  `"Chapter Content Generator Skill v1.09 running…"`. Nine such lines across three
  skills were updated.
- **Cross-references** — a skill naming *another* skill's minimum version, e.g.
  `` `learning-graph-generator` v1.06+ ``. Nine of these exist. They are
  compatibility floors and **remain correct after a bump** (1.07 still satisfies
  "1.06 or later"). Rewriting them would have falsely raised the requirement.

### Changelog entries only where a changelog exists

`book-chapter-generator` and `learning-graph-generator` have `### Changelog`
sections; `chapter-content-generator` uses `**Version N Features:**` blocks. Entries
were added in each file's own existing style. `book-installer` received a new
Changelog section because it absorbed a real functional change this session (it now
owns the canonical mascot rules). The remaining eight skills got the version line
only — inventing changelog history for them would have been fabrication.

## Infrastructure Finding: the auto-commit hook was silently not firing

While verifying the commit, `git log` showed the previous turn's work had **never
been committed**. `~/.claude/activity-logs/auto-commit-ibook-skills.log` showed the
same warning four times, starting 2026-08-24 — so this was a standing problem, not
a one-off.

**Root cause:** `auto-commit-ibook-skills-stop.sh` requires *two* files, not one:

| File | Written by | Purpose |
|------|-----------|---------|
| `.claude-pending-commit.txt` | the agent, per `CLAUDE.md` | commit message |
| `.claude-pending-files.txt` | a **PostToolUse tracker** on Edit/Write | which paths to stage |

The hook refuses to guess which paths belong in a commit, so a missing files-list
means it exits 0 having done nothing (script lines 81-83). This session ran in a
mode that directs file changes through Bash, so the PostToolUse tracker never fired
and the files-list was never created.

**Resolution:** the files-list was written manually with the absolute path of each
changed file, one per line, and each path dry-run staged before ending the turn.
The hook then committed and pushed normally (`16c76971`, pushed at 10:05:54).

Because two turns of work had accumulated, both changes landed in **one commit**.
This is a documented departure from the "one logical change per commit" rule in
`CLAUDE.md`, accepted here because the two were already coupled — the
`chapter-content-generator` 1.10 changelog entry describes the mascot change, so
splitting them would have produced a version-bump commit whose changelog referenced
work not yet in history.

**Follow-up worth considering:** either have the hook fall back to `git status`
when the files-list is absent, or document in `CLAUDE.md` that Bash-based edits
require writing it by hand.

## Files Changed

Line counts below are the versioning portion only; `chapter-content-generator`
and `book-installer` also carry mascot changes in the same commit.

| File | +/− | Versioning content |
|------|----:|--------------------|
| `skills/quiz-generator/SKILL.md` | +7 −5 | Version + 4 self-references |
| `skills/book-chapter-generator/SKILL.md` | +5 −1 | Version + changelog entry |
| `skills/learning-graph-generator/SKILL.md` | +5 −1 | Version + changelog entry |
| `skills/course-description-analyzer/SKILL.md` | +5 −1 | Version + 1 self-reference |
| `skills/chapter-content-generator/SKILL.md` | (shared) | Version + 4 self-refs + 1.10 block |
| `skills/book-installer/SKILL.md` | (shared) | Version + new Changelog section |
| 8 remaining skills | +4 each | Frontmatter `metadata:` + `**Version:**` line |

## Verification

A parse-and-compare pass over all 14 skills confirmed:

- every frontmatter block is valid YAML
- `metadata.ibook.version` is present in all 14
- frontmatter version equals the body `**Version:**` line in all 14
- no stale self-references remain
- all nine cross-skill compatibility floors are unchanged

## Key Takeaways for Future Sessions

- **Check the frontmatter spec before adding a field.** The natural choice
  (`version:`) is the one that breaks packaging. `metadata:` with a namespace
  prefix is the portable home for anything outside the six spec fields.
- **Distinguish a skill's own version from a floor it declares on another skill.**
  Bumping the former is required; rewriting the latter silently raises a
  requirement that was never intended to change.
- **Preserving an inconsistent format can beat normalising it** when live
  references cite the exact string.
- **Verify the commit actually landed.** The hook fails open and logs quietly, so
  a turn can appear to succeed while nothing reaches git. Checking `git log` after
  a turn that edits this repo is cheap insurance.
- The library's remaining portability hazard is `model:` in ten skills' frontmatter
  — the same hard-error rule, filed separately.

# Paper Quality Rubric (100 points)

This rubric judges whether a paper has enough content, and enough polish, to count as a
high-quality arXiv paper. It is used in two modes:

- **Readiness mode**, before drafting. For each criterion, ask: given the content in
  `brief.md` and the source material, what is the most this paper could earn here? The
  sum is the *readiness score*. Start drafting only at 80 or above
  (see `intake-interview.md`).
- **Quality mode**, after building. Score the actual paper. `scripts/score_paper.py`
  computes the criteria marked **[auto]** and reports facts for the ones marked
  **[judge]**, which you score with the descriptors below.

Award the highest descriptor the paper fully meets. Partial credit between descriptors
is fine.

| Area | Criteria | Points |
|------|----------|-------:|
| A. Front matter | 1 Title, 2 Authors, 3 Abstract | 15 |
| B. Core content | 4 Introduction, 5 Related work, 6 Core contribution, 7 Evidence, 8 Discussion & limitations, 9 Conclusion | 40 |
| C. Scholarly support | 10 References, 11 Figures, 12 Tables & formal elements, 13 Claim support | 25 |
| D. Build & arXiv compliance | 14 Clean build, 15 arXiv package, 16 Submission metadata & disclosure | 12 |
| E. Writing | 17 Writing quality | 8 |
| **Total** | | **100** |

---

## A. Front matter (15)

### 1. Title: 5 points [judge]

| Pts | Descriptor |
|----:|-----------|
| 5 | Specific and informative. It names the contribution and the domain, so a reader can guess what the paper does. At most about 15 words; a subtitle after a colon is fine. No undefined acronyms, and no hype. |
| 3 | Accurate but generic ("A Framework for X"), or long (over 20 words). |
| 1 | Vague, cute, or misleading about the content. |
| 0 | Missing or still a placeholder. |

### 2. Authors and affiliations: 3 points [judge]

| Pts | Descriptor |
|----:|-----------|
| 3 | Full names (Google Scholar can't index single names), an affiliation or "Independent Researcher", and a contact (email or URL). An ORCID is recommended. |
| 2 | Names and contact, but no affiliation. |
| 1 | Names only. |
| 0 | Missing. |

### 3. Abstract: 7 points [judge, with auto facts]

| Pts | Descriptor |
|----:|-----------|
| 7 | 150–250 words and at most 1,920 characters. Makes all five moves: context, gap, what this paper contributes, concrete evidence or results, implication. No citations and no undefined abbreviations. A Keywords line follows it. |
| 5 | One move missing, or slightly outside the word range. |
| 3 | Vague. It says what the paper is *about*, not what it *finds or contributes*. |
| 1 | Restates the title, or is a single sentence. |
| 0 | Missing. More than 1,920 characters is also a hard gate (see below). |

---

## B. Core content (40)

Interpret criteria 6 and 7 by paper type (see `section-guide.md`).

### 4. Introduction: 8 points [judge]

Four moves: (a) motivation with real stakes, (b) a precise problem statement or gap,
(c) an **enumerated** list of contributions, (d) a roadmap paragraph that names the
sections.

| Pts | Descriptor |
|----:|-----------|
| 8 | All four moves, each specific to this paper. |
| 6 | Roadmap missing, or the contributions are fuzzy. |
| 4 | Contributions implied but never stated as a list. |
| 2 | Motivation only. |
| 0 | No introduction. |

### 5. Related work: 7 points [judge]

| Pts | Descriptor |
|----:|-----------|
| 7 | At least 3 distinct strands of prior work and at least 10 citations in the section. Each strand ends by saying how this paper differs or builds on it. |
| 5 | Good coverage, but the positioning against prior work is weak. |
| 3 | A list of summaries with no comparison, or fewer than 5 citations. |
| 0 | Missing. |

### 6. Core contribution: 10 points [judge]

The framework, system, method, taxonomy or argument must be developed in enough detail
that a reader could apply, implement, replicate or rebut it. That means definitions,
components, design rationale, and formal structure where it fits: equations,
pseudocode, a schema, a decision table.

| Pts | Descriptor |
|----:|-----------|
| 10 | Complete, precise and self-contained. Terms are defined. Each design decision is justified, and the alternatives are named. |
| 7 | Clear, but some components are under-specified. |
| 4 | Described at overview level only. A reader couldn't apply it. |
| 1 | Asserted rather than developed. |
| 0 | No identifiable contribution. |

### 7. Evidence and evaluation: 8 points [judge]

The evidence must fit the paper type:

- **Empirical**: experiments with baselines, sample sizes and statistics.
- **System**: a deployment, usage metrics, benchmarks, or case studies.
- **Framework or position**: the framework applied to at least 2 concrete, detailed
  cases, plus supporting data from cited sources.
- **Survey**: a systematic, reproducible coverage method.

| Pts | Descriptor |
|----:|-----------|
| 8 | Strong evidence of the right kind. Claims and evidence line up, and the numbers are sourced. |
| 6 | Real evidence, with gaps (one case study, no baseline). |
| 3 | Anecdotal or illustrative only. |
| 0 | Assertions only. Fabricated evidence is a hard gate. |

### 8. Discussion and limitations: 4 points [judge]

| Pts | Descriptor |
|----:|-----------|
| 4 | Implications for researchers and practitioners, and an explicit Limitations subsection that names at least 3 real limitations or threats to validity. |
| 2 | Limitations are token ("more work is needed") or folded into a single sentence. |
| 0 | No discussion of limitations. |

### 9. Conclusion and future work: 3 points [judge]

| Pts | Descriptor |
|----:|-----------|
| 3 | Restates the contributions in fresh words and gives concrete, specific future directions. |
| 2 | Adequate, but the future work is generic. |
| 1 | Copies the abstract. |
| 0 | Missing. |

---

## C. Scholarly support (25)

### 10. References: 10 points [auto]

| Sub-score | Points |
|-----------|--------|
| Count of entries cited | at least 30 → 4; 20–29 → 3; 12–19 → 2; 5–11 → 1; under 5 → 0 |
| Identifiers | at least 80% have a `doi` or `url` → 2; at least 50% → 1 |
| Recency | at least 30% from the last 5 years → 2; at least 15% → 1 |
| Consistency | no undefined citations → 1; at most 10% of `.bib` entries left uncited → 1 |

Every reference must also be **verified real**. That is a hard gate, not a sub-score.
`--verify-dois` checks DOIs automatically. Check entries that have no DOI by web search.

### 11. Figures: 8 points [6 auto + 2 judge]

| Sub-score | Points |
|-----------|--------|
| Count [auto] | at least 4 → 3; 3 → 2; 1–2 → 1; none → 0 |
| Referenced [auto] | every figure `\ref`'d in the text → 2; at least 75% → 1 |
| Captions [auto] | every caption at least 15 words, saying what the figure shows and what to notice → 1 |
| Legibility [judge] | ≥ 300 effective DPI or vector; text readable at print size; consistent style; color-blind-safe palette; no clutter → 2 |

### 12. Tables and formal elements: 4 points [2 auto + 2 judge]

| Sub-score | Points |
|-----------|--------|
| Table [auto] | at least one table built with booktabs (`\toprule`) → 2; a table without booktabs → 1 |
| Formal elements [judge] | equations, pseudocode, schema or code listings wherever the content calls for them, and none gratuitous → 2. Award 2 when the content truly calls for none. |

### 13. Claim support: 3 points [judge]

| Pts | Descriptor |
|----:|-----------|
| 3 | Every quantitative or non-obvious factual claim carries a citation, or points to the paper's own evidence. |
| 2 | A few unsupported claims. |
| 0 | Many claims rest on assertion alone. |

---

## D. Build and arXiv compliance (12)

### 14. Clean build: 4 points [auto]

- 2 points: the paper compiles with no errors, and `main.pdf` is newer than every source.
- 1 point: no undefined citations or references.
- 1 point: no overfull box wider than 10pt, and no "Missing character" warnings.

### 15. arXiv package: 4 points [auto]

- 1 point: `arxiv-upload.zip` exists.
- 1 point: the zip contains `main.tex`, `main.bbl`, and every `\input` and
  `\includegraphics` target.
- 1 point: the zip compiles from a clean unzip.
- 1 point: the source is pdfLaTeX-safe. That means no unsupported Unicode, no absolute
  paths, no spaces or hidden files in the zip, and a total under 50 MB.

### 16. Submission metadata and disclosure: 4 points [auto]

- 1 point: `arxiv-metadata.md` has a valid primary category.
- 1 point: it has a plain-text abstract of at most 1,920 characters, and a Comments line
  that gives the page count.
- 1 point: a license is chosen.
- 1 point: the paper itself contains an AI-assistance disclosure, in the Acknowledgments
  or a Disclosure section.

---

## E. Writing (8)

### 17. Writing quality: 8 points [judge]

| Pts | Descriptor |
|----:|-----------|
| 8 | The argument flows, with transitions between sections. Terminology is consistent and every acronym is defined. The register is academic, with no marketing language. The text is concise: nothing is repeated across sections and there is no padding. Grammar is clean. |
| 6 | Minor issues: a few repetitive passages, uneven sections. |
| 4 | Reads like book chapters or documentation pasted together, or noticeably padded. |
| 2 | Hard to follow, or many errors. Leftover placeholder text caps this criterion at 2. |

---

## Hard gates

The paper is **submission-ready** only if all of these pass, whatever its score:

1. It compiles without errors.
2. It has no undefined citations or references.
3. Every reference is verified real; unverifiable entries are removed or flagged for the
   author.
4. It has no fabricated data, results, quotes or statistics.
5. The abstract is at most 1,920 characters.
6. It has no TODO, FIXME, `{{placeholder}}` or lorem-ipsum text in the visible paper.

## Tiers

| Score | Tier | Meaning |
|------:|------|---------|
| 90–100 | Excellent | Ready to submit after the author proofreads it. |
| 80–89 | Good | Minor revisions. |
| 70–79 | Adequate | Several categories need work. |
| 50–69 | Draft | Substantial gaps, usually evidence, references or figures. |
| under 50 | Outline | Not yet a paper. |

Readiness threshold: start drafting at a readiness score of **80** or above.
Quality target: **85** or above with every hard gate passing.

## quality-report.md format

```markdown
# Quality Report: <Paper Title>

**Version:** <paperversion> · **Date:** <YYYY-MM-DD> · **Score:** NN/100 (<Tier>)
**Submission-ready:** Yes / No (failing gates: ...)

## Score breakdown

| # | Criterion | Points | Max | Notes |
|---|-----------|-------:|----:|-------|
| 1 | Title | | 5 | |
| ... | | | | |
| | **Total** | **NN** | **100** | |

## Hard gates
- [x] Compiles without errors
- ...

## Automated facts
Pages, word count, references (count, % with DOI, % recent), figures, tables, overfull boxes.

## Gaps and recommended revisions
Ordered by points recoverable.

## Needs the author
Unverified references, data to supply, assumptions from brief.md to confirm.
```

# arXiv Submission Guide

Facts below were checked against info.arxiv.org and blog.arxiv.org in October 2026.
Policies change, so recheck before you rely on a borderline point.

## Will arXiv accept this paper? (Check it during the interview.)

- **Position, review and survey papers in CS.** Since 31 Oct 2025, arXiv's CS
  moderators accept review articles and position papers only after a journal or
  conference has accepted them through full peer review. Workshop review doesn't count.
  The submission must include the journal reference and DOI.
- **Exception.** Research papers that study the impact of science and technology on
  society (for example cs.CY, physics.soc-ph) are not subject to this rule.
- **Implications for this skill:**
  - A paper that develops a framework *and supports it with case studies or data* is a
    research paper. Frame it that way: name the research question, describe the method,
    present the evidence.
  - A pure opinion piece or a literature survey headed for cs.* needs peer review first.
    Otherwise, choose another server (below).
  - Education-focused papers fit **EdArXiv** (OSF Preprints) well. The author's
    *Five Levels* paper is there.
- arXiv only accepts scholarly research. Papers without references, or without a
  research contribution, are often reclassified or rejected.
- **First-time submitters** to a category may need an **endorsement** from an
  established author in that category.

## How arXiv compiles

- arXiv recompiles the LaTeX source; it doesn't take your PDF. TeX Live 2025 is the
  default (2023 is available). It picks the engine automatically. With PNG, JPEG or PDF
  figures that means pdfLaTeX.
- It runs BibTeX itself, but **uses `main.bbl` if one is present**. The `.bbl` name must
  match the main `.tex` file. `./build.sh arxiv` includes `main.bbl`, so the references
  come out exactly as they did locally.
- Don't use `\pdfoutput` to change the output format.
- Figures for pdfLaTeX are JPEG, PNG or PDF; arXiv doesn't convert formats.
- Compilation runs from the root of the upload. Paths must be relative
  (`figures/x.png`, `sections/02-introduction`).
- Hidden files may be deleted. Leave out leftovers such as old drafts, unused figures,
  `.py` scripts and PDFs of the paper.
- Keep the upload small, a few MB; stay well under 50 MB. Oversized submissions need
  justification.

Because Tectonic (XeTeX) builds the local PDF while arXiv uses pdfLaTeX, raw Unicode
symbols that Tectonic tolerates can break on arXiv. `score_paper.py` flags any that are
unsafe, and `build.sh arxiv` test-compiles the zip in a clean folder.

## The submission form (arxiv-metadata.md)

| Field | Rule |
|-------|------|
| Title | No all-caps, no Unicode characters, and expand obscure TeX macros. Match the PDF. |
| Authors | "Firstname Lastname", no honorifics, list everyone (no "et al."). AI tools can't be authors. |
| Abstract | **At most 1,920 characters**, plain text. No citations. A blank line plus indentation starts a new paragraph. `$...$` math is allowed but keep it minimal. |
| Comments | Number of pages and figures, e.g. "18 pages, 6 figures". May add "Submitted to <venue>". No copyright statements. |
| Primary category | Exactly one (below). |
| Cross-lists | 0–2 others where the paper truly belongs. |
| MSC / ACM class | Optional. |
| Journal-ref / DOI | Only once the paper is published; required for CS position or review papers. |
| License | Chosen at submission and can't be made more restrictive later. |

## Categories that fit this author's work

| Code | Name | Fits papers on... |
|------|------|-------------------|
| cs.CY | Computers and Society | AI in education, ethics, policy, societal impact (exempt from the position-paper rule if it's research) |
| cs.HC | Human-Computer Interaction | interactive learning tools, user studies, interfaces |
| cs.AI | Artificial Intelligence | agent frameworks, knowledge representation |
| cs.MA | Multiagent Systems | orchestrating multiple agents |
| cs.SE | Software Engineering | agent skills, AI-assisted coding workflows, tooling |
| cs.CL | Computation and Language | LLM behavior, prompting, text generation |
| cs.DL | Digital Libraries | metadata, scholarly communication, knowledge graphs of papers |
| cs.LG | Machine Learning | learning algorithms (rarely the right fit for this author's work) |
| physics.ed-ph | Physics Education | physics simulations and pedagogy |
| eess.SY / eess.SP | Systems and Control / Signal Processing | EE research methods with real technical content |

Choose the primary category by **who should review it**, and cross-list sparingly.

## Licenses

| License | Effect |
|---------|--------|
| CC BY 4.0 | Most open: anyone may reuse with attribution. Recommended for maximum reach. |
| CC BY-SA 4.0 | Share-alike. |
| CC BY-NC-SA 4.0 | Non-commercial, share-alike. Matches the author's textbook licensing. |
| CC BY-NC-ND 4.0 | No derivatives. |
| arXiv non-exclusive license 1.0 | The default minimal license. Others can't reuse it without permission. |
| CC0 | Public domain. |

Ask the author. Some journals limit which preprint licenses are compatible with later
publication.

## Generative AI policy

arXiv holds authors fully responsible for everything in the paper, including any
AI-generated text, figures or code. Generative AI tools can't be listed as authors. Use
of these tools beyond basic editing should be reported, following the conventions of
the field. That is why the template's Acknowledgments carries a disclosure paragraph.
Fabricated or unverified references count as misconduct, and they get papers rejected or
withdrawn.

## Other preprint servers

| Server | Good for | Notes |
|--------|----------|-------|
| EdArXiv (OSF Preprints) | education research, including position and framework papers | Takes a PDF upload plus metadata; can mint a DOI. The author's `five-levels/osf-metadata.json` is a worked example. |
| OSF Preprints | general multidisciplinary | Same platform as EdArXiv. |
| SSRN | policy, economics, social impact | PDF upload. |
| TechRxiv (IEEE) | electrical and electronics engineering, computing | PDF upload; IEEE-affiliated, a good fit for EE-audience papers. |

For PDF-upload servers, use `main.pdf` and the same title and abstract text from
`arxiv-metadata.md`. Google Scholar indexes these servers, and it needs full author
names in proper case.

## Pre-submission checklist

- [ ] `./build.sh arxiv` passes, including the clean-folder test compile
- [ ] `score_paper.py` shows every hard gate passing and a score of at least 85
- [ ] Every reference verified; DOIs resolve
- [ ] Title, authors and abstract in `arxiv-metadata.md` match the PDF exactly
- [ ] The category choice respects the position/review rule
- [ ] License chosen with the author
- [ ] AI-use disclosure present
- [ ] The author has proofread the PDF

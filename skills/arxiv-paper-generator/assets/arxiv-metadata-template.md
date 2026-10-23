# arXiv Submission Metadata: {{slug}}

Paste these into the arXiv submission form. They must match the PDF exactly.

**Title:** {{Title in plain text, no Unicode, no all-caps}}

**Authors:** {{Firstname Lastname, Firstname Lastname}}

**Primary category:** {{cs.CY}}

**Cross-list categories:** {{cs.HC, cs.AI, or "none"}}

**Comments:** {{N}} pages, {{M}} figures

**License:** {{CC BY 4.0}}

**MSC / ACM class:** {{optional}}

**Journal-ref / DOI:** {{only once published; required for CS position/review papers}}

## Abstract (plain text, at most 1,920 characters)

{{Abstract as plain text: no LaTeX commands, no citations. Use -- for dashes and % for
percent.}}

## Category rationale

{{Why this primary category; whether the position/review-paper rule applies and how the
paper satisfies it.}}

## Pre-submission checklist

- [ ] `./build.sh arxiv` passes the clean-folder test compile
- [ ] `score_paper.py`: every hard gate passes, score at least 85
- [ ] Every reference verified
- [ ] Title, authors and abstract above match the PDF
- [ ] License confirmed with all authors
- [ ] Endorsement obtained, if this is a first submission to the category

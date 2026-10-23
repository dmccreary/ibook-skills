# {{Paper Title}}

{{One-paragraph summary of the paper's contribution.}}

- **Authors:** {{names}}
- **Version:** {{0.01}} · **Status:** {{draft / submitted / posted}}
- **Quality score:** {{NN}}/100. See [quality-report.md](quality-report.md).
- **Target:** arXiv {{category}} ({{license}}). See [arxiv-metadata.md](arxiv-metadata.md).

## Directory structure

```
{{slug}}/
├── main.tex             # preamble, title block, section \input list
├── sections/            # one .tex file per section + references.bib
├── figures/             # figures + the scripts / TikZ sources that generate them
├── build.sh             # build, package and release script
├── brief.md             # content brief from the author interview
├── arxiv-metadata.md    # arXiv submission form fields
├── quality-report.md    # rubric score and open issues
└── main.pdf             # latest build
```

## Building

Requires [Tectonic](https://tectonic-typesetting.github.io/) (`brew install tectonic`).
Falls back to `latexmk` + pdfLaTeX if Tectonic isn't installed.

```bash
./build.sh            # build main.pdf
./build.sh arxiv      # build + arxiv-upload.zip, test-compiled in a clean folder
./build.sh release    # build + save {{slug}}-v<version>.pdf
./build.sh clean      # remove build artifacts
```

To bump the version, edit `\newcommand{\paperversion}{...}` in `main.tex`.

## Regenerating figures

{{List each figure script, e.g. `python3 figures/adoption-chart.py`.}}

## Submitting

See [arxiv-metadata.md](arxiv-metadata.md) for the form fields and the checklist.
Upload `arxiv-upload.zip` at https://arxiv.org/submit.

# Figures Guide

A high-quality paper usually has **3–6 figures**. A typical set is one overview
diagram of the contribution, one figure per major component or case, and a chart of
the evidence. Every figure must earn its place, which means it shows something the
text can't show as well.

## Choosing a method

| Figure kind | Best method | Output |
|-------------|-------------|--------|
| Architecture, process, layers, taxonomy, flow | TikZ (`figures/<name>.tikz`) | vector, compiled with the paper |
| Bar, line, scatter, or other data chart | matplotlib script (`figures/<name>.py`) | `figures/<name>.png` at 300 DPI |
| Chart when matplotlib isn't installed | pgfplots inside a `.tikz` file | vector |
| Screenshot of a MicroSim, app or page | the `microsim-utils` screen-capture route, or an existing PNG in the repo | PNG |
| Existing diagram, poster or infographic in the repo | copy it into `figures/`, if it's legible at column width | PNG |

The author's convention is **PNG for raster figures, not PDF figure files**. TikZ
figures are LaTeX source, not image files, so they are fine. arXiv's pdfLaTeX accepts
PNG, JPEG and PDF; it does not accept EPS.

Keep every generator script in `figures/`, so a figure can be rebuilt when the data
changes.

## Including a figure

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.9\textwidth]{figures/orchestration-model.png}
  \caption{The researcher as orchestrator. Twenty planning agents explore and specify
  (left); ten execution agents build and test (right). The researcher resolves
  conflicts and owns every claim. Note the review gate between the two teams.}
  \label{fig:orchestration}
\end{figure}
```

For TikZ, use `\input{figures/orchestration-model.tikz}` in place of `\includegraphics`.
Use the `.tikz` extension, not `.tex`. A stray `.tex` file in `figures/` can confuse
arXiv's search for the main file, and `build.sh` only packages `.tikz`, `.png`, `.jpg`
and `.pdf` figure files.

- Refer to every figure in the text **before** it appears:
  "As Figure~\ref{fig:orchestration} shows, ...".
- Captions are self-contained, at least 15 words: what the figure shows, how to read
  it, and what to notice. A reader skimming only the figures should still get the point.
- Widths: `0.9\textwidth` for wide diagrams, `0.6\textwidth` for square figures. Don't
  stretch a small raster image; resolution is what matters.

## Resolution and legibility

- Raster figures need at least **300 effective DPI** at their printed width. A figure
  printed at `0.9\textwidth` (≈ 5.85 in) needs about 1,750 px across. `score_paper.py`
  reports each PNG's effective DPI.
- The smallest text in a figure should print at 7–9 pt, close to the caption size.
- Use one consistent font family and palette across all figures.
- Colors: use the color-blind-safe Okabe–Ito palette: `#0072B2` blue, `#E69F00`
  orange, `#009E73` green, `#D55E00` vermillion, `#CC79A7` purple, `#56B4E9` sky,
  `#F0E442` yellow, `#000000` black. Never rely on color alone to carry meaning; add
  labels, patterns or markers too.
- Leave out chart junk: no 3D bars, no heavy gridlines, no drop shadows.

## matplotlib template (`figures/<name>.py`)

```python
"""Generate figures/<name>.png. Data source: <file or citation>."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).with_suffix(".png")
OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9"]

plt.rcParams.update({"font.family": "serif", "font.size": 9,
                     "axes.spines.top": False, "axes.spines.right": False})

labels = ["A", "B", "C"]          # every value here must come from a cited source
values = [12, 30, 21]

fig, ax = plt.subplots(figsize=(5.8, 2.8))   # inches, the printed size
ax.bar(labels, values, color=OKABE_ITO[: len(values)])
ax.set_ylabel("Units (source: ...)")
fig.tight_layout()
fig.savefig(OUT, dpi=300)
print(f"wrote {OUT}")
```

If matplotlib is missing, `pip install matplotlib` installs it. Or draw the chart with
pgfplots in TikZ (below), which needs nothing outside LaTeX.

## TikZ template (`figures/<name>.tikz`)

The preamble already loads `tikz` with the `arrows.meta`, `positioning`,
`shapes.geometric`, `fit` and `calc` libraries. Add `\usepackage{pgfplots}` and
`\pgfplotsset{compat=1.18}` to `main.tex` only when you need a pgfplots chart.

```latex
\begin{tikzpicture}[
    node distance=6mm and 10mm,
    box/.style={draw, rounded corners, align=center, minimum width=28mm,
                minimum height=9mm, font=\small},
    plan/.style={box, fill=blue!8}, exec/.style={box, fill=orange!12},
    arrow/.style={-{Latex[length=2mm]}, thick}]
  \node[box, fill=gray!10] (r) {Researcher\\(direction, judgment)};
  \node[plan, below left=of r]  (p) {Planning agents\\($\times$20)};
  \node[exec, below right=of r] (e) {Execution agents\\($\times$10)};
  \draw[arrow] (r) -- (p);
  \draw[arrow] (r) -- (e);
  \draw[arrow] (p) -- node[above, font=\scriptsize]{specs} (e);
\end{tikzpicture}
```

Keep TikZ diagrams simple: 4–12 nodes, short labels, a consistent style block. Compile
after each one; TikZ errors are easier to fix one figure at a time.

## Reusing repo assets

Intelligent-textbook repos often contain `docs/img/`, `docs/posters/`, `docs/sims/*/`
screenshots and infographics. Before reusing one, check that:

- it is legible at the printed size (not a busy poster shrunk to 3 inches)
- the effective DPI is at least 300; if not, regenerate the image or redraw it in TikZ
- the license lets you include it (the repo's own images usually do)
- the caption is rewritten for the paper, not copied from the web page

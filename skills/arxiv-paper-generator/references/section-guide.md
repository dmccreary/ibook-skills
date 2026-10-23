# Section Guide

## Choose a paper type

| Type | Use when the paper... | Example from this author |
|------|----------------------|--------------------------|
| Framework / position | proposes a model, classification, principle or argument, with examples rather than experiments | *A Five-Level Classification Framework for Intelligent Textbooks*; *Evolving Pedagogy (self-improving textbooks)* |
| System / tool | presents something built: architecture, design and its use | *MicroSims: A Framework for AI-Generated, Scalable Educational Simulations* |
| Empirical study | answers research questions with collected data | (a classroom study of MicroSim learning gains) |
| Survey / review | maps and organizes a body of existing work | (a survey of personal AI agents) |

## Section plans

Number the files in reading order: `01-abstract.tex`, `02-introduction.tex`, and so on.
Section titles can be adapted to the topic, as with "The Five Levels of Intelligent
Textbooks" in place of "Framework". Keep the *function* of each section.

**Framework / position (10–18 pages)**
1. Abstract
2. Introduction
3. Background and Related Work (may split into two)
4. The Framework (the core contribution: definitions, components, rationale)
5. Applying the Framework (at least 2 worked cases or case studies)
6. Implications (for practitioners, policy, research)
7. Discussion and Limitations
8. Conclusion and Future Work

**System / tool (12–20 pages)**
1. Abstract
2. Introduction
3. Related Work
4. Design Goals / Requirements
5. Architecture
6. Implementation (key decisions, a code listing or schema)
7. Evaluation / Case Studies / Deployment
8. Discussion and Limitations
9. Conclusion and Future Work

**Empirical study (12–25 pages)**
1. Abstract
2. Introduction (ending in research questions RQ1..RQn)
3. Related Work
4. Method (participants, materials, procedure, measures, analysis)
5. Results (one subsection per RQ)
6. Discussion
7. Threats to Validity
8. Conclusion

**Survey (15–30 pages)**
1. Abstract
2. Introduction
3. Scope and Method (sources searched, inclusion criteria, time window)
4. Taxonomy
5. Review by category (one section per category)
6. Comparison (a summary table)
7. Open Challenges and Research Directions
8. Conclusion

## What each section must do

### Abstract (`01-abstract.tex`)

```latex
\begin{abstract}
<150--250 words: context, gap, contribution, evidence, implication.>
\end{abstract}

\noindent\textbf{Keywords:} term one, term two, term three, term four, term five
```

Write it last. Use no citations, and the same terms as the body. State concrete
results ("a five-level classification...", "applied to 3 textbooks..."), not
intentions ("we discuss...").

### Introduction

1. **Hook and stakes**, 1–2 paragraphs: why this matters now, with cited evidence.
2. **Problem and gap**: what is missing, stated precisely enough that the contribution
   visibly fills it.
3. **Contributions**: an enumerated list, each item a claim a reviewer could check.
   ```latex
   This paper makes the following contributions:
   \begin{enumerate}[leftmargin=*]
     \item A ... that ...
     \item ...
   \end{enumerate}
   ```
4. **Roadmap**: "Section~\ref{sec:related} reviews ...; Section~\ref{sec:framework}
   ..."

### Related work

Organize by **strand**, not by paper. Each strand gets a paragraph or subsection that
summarizes the work (with several citations) and closes with the positioning sentence:
"Unlike these approaches, our framework ...". Close the section with a summary of the
gap this paper fills. Aim for at least 10 citations here.

### Core contribution (framework, architecture, method, taxonomy)

- Define every term before using it. A definition list or a `description` environment
  works well.
- Give the structure at a glance first (a figure or table), then go through each
  component.
- Justify each design decision, and name the alternatives that were rejected.
- Use formal elements where they make things precise: an equation, pseudocode, a JSON
  schema, a decision table.

### Evidence (evaluation, case studies, worked examples)

- Each case: the context, how the contribution was applied, what happened (with
  numbers if they exist), and what it shows.
- Tie each piece of evidence back to a specific contribution or claim.
- If there are no measurements, say so plainly, and propose the evaluation (metrics,
  design) as future work. Never fill the gap with invented numbers.

### Discussion and limitations

- Implications: who should do what differently because of this paper.
- A **Limitations** subsection naming at least 3 real limits: scope, evidence quality,
  generalizability, author bias (the authors built the system they evaluate), and how
  fast the field is moving. Honest limitations raise reviewer trust.

### Conclusion and future work

Restate the contributions in fresh words; don't paste the abstract. Then give 3–5
specific future directions, each with a "how".

### Acknowledgments and AI disclosure (in `main.tex`)

```latex
\section*{Acknowledgments}
<People, projects, funding.>

\paragraph{Use of generative AI.} <Tool and model> was used to <draft sections from the
authors' notes / generate figure scripts / format references>. The authors reviewed,
edited and verified all content, including every citation, and take full responsibility
for the paper.
```

## Turning book or course material into a paper

A book teaches; a paper argues. When the source is a textbook:

- Extract the **argument**, not the curriculum. Chapter structure, learning objectives,
  quizzes, the mascot and second-person "you will learn" phrasing don't belong in a
  paper.
- Condense explanations into definitions and claims. Keep one sentence of intuition
  where it helps.
- Promote case studies to evidence: give each one context, method, outcome and lesson.
- Cite the book itself (as `@misc` with its URL) when the paper draws on it, and cite
  the primary sources the book cites, not the book, for factual claims.

## LaTeX conventions

- Cross-references: `Section~\ref{sec:x}`, `Figure~\ref{fig:x}`, `Table~\ref{tab:x}`,
  `Equation~\eqref{eq:x}`. Put a label right after each `\section` and `\caption`.
- Lists: `enumerate` or `itemize` with `[leftmargin=*]` (enumitem is loaded).
- Emphasis: `\textit{}` for a defined term on first use; `\textbf{}` sparingly, for
  run-in headings.
- Tables: booktabs (`\toprule`, `\midrule`, `\bottomrule`), no vertical rules, caption
  *above* the table. Use the `L{width}` and `C{width}` column types for wrapping text.
- Code: `\begin{lstlisting}[caption={...},label={lst:x}]` (style already set; add
  `language=Python` and so on as needed).
- URLs: `\url{}`. Breakable and clickable through hyperref.
- Quotes: ``` ``double'' ``` and `` `single' ``. Dashes: `--` for ranges (2019--2024),
  `---` for an em dash, with no spaces around it.
- Special characters: `\%`, `\&`, `\$`, `\#`, `\_`; `$\times$`, `$\geq$`,
  `$\rightarrow$`, `$\sim$`.

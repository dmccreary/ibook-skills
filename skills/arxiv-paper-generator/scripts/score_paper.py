#!/usr/bin/env python3
"""Automated rubric checks for an arXiv-format paper folder.

Scores the mechanical criteria of references/quality-rubric.md (references, figures,
tables, build, arXiv package, submission metadata), checks the hard gates it can see,
and prints the facts needed to score the judgment criteria. Standard library only.

Usage:
    python3 score_paper.py papers/<slug>                  # print the report
    python3 score_paper.py papers/<slug> --json out.json  # also write all data as JSON
    python3 score_paper.py papers/<slug> --verify-dois    # look up every DOI (network)
    python3 score_paper.py papers/<slug> --no-compile     # skip test-compiling the zip
    python3 score_paper.py paper --main arxiv-submission.tex   # main file not named main.tex
"""

import argparse
import datetime
import json
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

TEXT_WIDTH_IN = 6.5          # 8.5in page with 1in margins (template geometry)
ABSTRACT_CHAR_LIMIT = 1920   # arXiv submission form limit
RECENT_YEARS = 5
GRAPHIC_EXTS = [".png", ".pdf", ".jpg", ".jpeg"]

# Non-ASCII characters pdfLaTeX handles with utf8 inputenc + T1 fontenc + textcomp.
# Anything else (arrows, Greek, math symbols, check marks, emoji) breaks on arXiv.
PDFLATEX_SAFE = set(chr(c) for c in range(0xA0, 0x100)) | set("\u2013\u2014\u2018\u2019\u201c\u201d\u2026\u2022")

# Template placeholders look like {{Title}}; skip LaTeX's own double braces such as
# \graphicspath{{figures/}} or {{\ttfamily #1}} by refusing /, # and backslashes inside.
PLACEHOLDER_PATTERNS = [
    r"\bTODO\b", r"\bFIXME\b", r"\bTBD\b", r"\bXXX\b", r"(?i:lorem ipsum)",
    r"\{\{(?![^{}]*[/#\\])[A-Za-z0-9][^{}]*\}\}", r"(?i:\[citation needed\])", r"\\todo\b",
]

SECTION_ROLES = {
    "introduction": r"introduction",
    "related_work": r"related|background|prior work|literature",
    "core": r"framework|method|approach|architecture|design|model|system|taxonomy|definition|levels?\b",
    "evidence": r"evaluation|results?|experiment|case stud|worked example|application|applying|validation|findings|deployment",
    "discussion": r"discussion|implication",
    "limitations": r"limitation|threats? to validity",
    "conclusion": r"conclusion|concluding|future work",
}

ARXIV_CATEGORY = re.compile(
    r"^(cs|math|stat|eess|econ|q-bio|q-fin|physics|astro-ph|cond-mat|nlin|gr-qc|hep-ex|hep-lat|"
    r"hep-ph|hep-th|math-ph|nucl-ex|nucl-th|quant-ph)(\.[A-Za-z][A-Za-z-]*)?$")
LICENSES = re.compile(r"CC[ -]BY|CC0|non-?exclusive|arXiv", re.I)


# ---------------------------------------------------------------- LaTeX parsing

def strip_comments(text):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def braced(text, start):
    """Return (content, end) for the brace group opening at text[start] == '{'."""
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{" and (i == 0 or text[i - 1] != "\\"):
            depth += 1
        elif text[i] == "}" and text[i - 1] != "\\":
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
    return text[start + 1:], len(text)


def command_args(text, cmd):
    """All brace arguments of \\cmd{...} (optional star and [options] allowed)."""
    out = []
    for m in re.finditer(r"\\" + cmd + r"\*?\s*(?:\[[^\]]*\])?\s*\{", text):
        content, _ = braced(text, m.end() - 1)
        out.append(content)
    return out


def resolve_input(base, name):
    p = base / name
    if p.suffix in (".tex", ".tikz") and p.exists():
        return p
    q = p.with_name(p.name + ".tex")
    return q if q.exists() else (p if p.exists() else None)


def load_tex(paper, rel="main.tex", seen=None, inputs=None):
    """Read rel with comments stripped, inlining \\input/\\include files recursively."""
    seen = set() if seen is None else seen
    inputs = [] if inputs is None else inputs
    path = paper / rel
    if path in seen or not path.exists():
        return "", inputs
    seen.add(path)
    text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))

    def repl(m):
        target = resolve_input(paper, m.group(1).strip())
        if target is None:
            inputs.append((m.group(1).strip(), False))
            return ""
        inputs.append((str(target.relative_to(paper)), True))
        sub, _ = load_tex(paper, str(target.relative_to(paper)), seen, inputs)
        return sub

    text = re.sub(r"\\(?:input|include)\s*\{([^}]+)\}", repl, text)
    return text, inputs


def delatex(s):
    s = re.sub(r"\\(?:cite[a-z]*|label|ref|eqref)\*?(?:\[[^\]]*\])?\{[^}]*\}", "", s)
    for _ in range(3):
        s = re.sub(r"\\(?:textbf|textit|emph|texttt|textsc|underline|mbox|text)\{([^{}]*)\}", r"\1", s)
    s = s.replace("---", "\u2014").replace("--", "\u2013").replace("``", '"').replace("''", '"')
    s = re.sub(r"\\([%&$#_])", r"\1", s).replace("~", " ").replace("\\\\", " ")
    s = re.sub(r"\\[a-zA-Z]+\*?", "", s).replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def words(s):
    return len(re.findall(r"[A-Za-z0-9][\w'\-]*", s))


# ---------------------------------------------------------------- BibTeX parsing

def parse_bib(path):
    entries = {}
    if not path.exists():
        return entries
    text = path.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        etype = m.group(1).lower()
        if etype in ("comment", "string", "preamble"):
            continue
        body, _ = braced(text, text.index("{", m.start()))
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*", body):
            pos = fm.end()
            if pos < len(body) and body[pos] == "{":
                val, _ = braced(body, pos)
            elif pos < len(body) and body[pos] == '"':
                end = body.find('"', pos + 1)
                val = body[pos + 1:end]
            else:
                val = re.match(r"[^,\n]*", body[pos:]).group(0)
            fields.setdefault(fm.group(1).lower(), val.strip())
        entries[m.group(2)] = {"type": etype, **fields}
    return entries


def verify_doi(doi, title):
    """Return (status, detail). status: verified | title-mismatch | not-found | error."""
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi.strip())
    headers = {"User-Agent": "arxiv-paper-generator/0.01 (reference check)"}
    try:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=15) as r:
            msg = json.load(r)["message"]
        found = " ".join(msg.get("title") or [""])
        a, b = (set(re.findall(r"[a-z0-9]+", t.lower())) for t in (delatex(title), found))
        overlap = len(a & b) / max(1, min(len(a), len(b)))
        return ("verified" if overlap >= 0.6 else "title-mismatch"), found
    except urllib.error.HTTPError as e:
        if e.code != 404:
            return "error", f"Crossref HTTP {e.code}"
    except Exception as e:  # network down, timeout, bad JSON
        return "error", str(e)
    # Not in Crossref (e.g. DataCite DOIs such as arXiv's 10.48550): ask the DOI resolver
    try:
        url = "https://doi.org/api/handles/" + urllib.parse.quote(doi)
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=15) as r:
            ok = json.load(r).get("responseCode") == 1
        return ("verified" if ok else "not-found"), "registered DOI (title not checked)" if ok else ""
    except urllib.error.HTTPError as e:
        return ("not-found", "") if e.code == 404 else ("error", f"doi.org HTTP {e.code}")
    except Exception as e:
        return "error", str(e)


# ---------------------------------------------------------------- images

def image_pixels(path):
    """(width_px, height_px, dpi or None) for PNG/JPEG, else None."""
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        dpi = None
        i = data.find(b"pHYs")
        if i > 0:
            ppu_x, _, unit = struct.unpack(">IIB", data[i + 4:i + 13])
            if unit == 1:
                dpi = round(ppu_x * 0.0254)
        return w, h, dpi
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h, None
            i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return None


def printed_width_in(options):
    m = re.search(r"width\s*=\s*([\d.]*)\s*\\(textwidth|linewidth|columnwidth)", options or "")
    if m:
        return float(m.group(1) or 1) * TEXT_WIDTH_IN
    m = re.search(r"width\s*=\s*([\d.]+)\s*(in|cm|mm|pt)", options or "")
    if m:
        return float(m.group(1)) / {"in": 1, "cm": 2.54, "mm": 25.4, "pt": 72.27}[m.group(2)]
    return None


def resolve_graphic(paper, name):
    p = paper / name
    if p.suffix.lower() in GRAPHIC_EXTS and p.exists():
        return p
    for ext in GRAPHIC_EXTS:
        if (paper / (name + ext)).exists():
            return paper / (name + ext)
    return None


# ---------------------------------------------------------------- checks

def check_paper(paper, verify_dois=False, compile_zip=True, main="main.tex"):
    r = {"paper": str(paper), "slug": paper.name, "auto": {}, "gates": {}, "facts": {}, "issues": []}
    stem = Path(main).stem
    tex, inputs = load_tex(paper, main)
    if not tex:
        r["issues"].append(f"{main} not found")
        return r
    body = tex.split("\\begin{document}", 1)[-1]
    f = r["facts"]

    # Title, authors, abstract, keywords
    title = (command_args(tex, "title") or [""])[0]
    f["title"] = delatex(title)
    f["title_words"] = words(f["title"])
    author_block = (command_args(tex, "author") or [""])[0]
    authors = [re.split(r"\\\\", a)[0] for a in re.split(r"\\and\b", author_block)]
    f["authors"] = [delatex(a) for a in authors if delatex(a)]
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S)
    abstract_tex = abstract.group(1) if abstract else ""
    abstract_plain = delatex(abstract_tex)
    f["abstract_words"] = words(abstract_plain)
    f["abstract_chars"] = len(abstract_plain)
    f["abstract_has_cite"] = bool(re.search(r"\\cite", abstract_tex))
    f["keywords"] = bool(re.search(r"keywords", tex, re.I))

    # Sections
    sections = [delatex(s) for s in command_args(body, "section")]
    subsections = [delatex(s) for s in command_args(body, "subsection")]
    f["sections"] = sections
    f["subsection_count"] = len(subsections)
    heads = [s.lower() for s in sections + subsections]
    f["section_roles"] = {role: any(re.search(pat, h) for h in heads) for role, pat in SECTION_ROLES.items()}
    text_only = re.sub(r"\\begin\{(figure|table|lstlisting|tikzpicture)\*?\}.*?\\end\{\1\*?\}", " ", body, flags=re.S)
    f["body_words"] = words(delatex(text_only.split("\\bibliography")[0]))

    # Inputs
    missing_inputs = [n for n, ok in inputs if not ok]
    if missing_inputs:
        r["issues"].append(f"\\input targets not found: {', '.join(missing_inputs)}")

    # Citations and references
    cited = set()
    for group in re.findall(r"\\(?:no)?cite[a-zA-Z]*\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}", body):
        cited.update(k.strip() for k in group.split(",") if k.strip())
    bib_files = command_args(tex, "bibliography")
    bib = {}
    for b in (bib_files[0].split(",") if bib_files else []):
        bib.update(parse_bib(paper / (b.strip() if b.strip().endswith(".bib") else b.strip() + ".bib")))
    # Inline bibliographies (\begin{thebibliography} ... \bibitem{key} ...) count as entries too
    for m in re.finditer(r"\\bibitem\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})", tex, re.S):
        item = m.group(2)
        doi = re.search(r"10\.\d{4,9}/[^\s},]+", item)
        url = re.search(r"\\url\{([^}]+)\}|https?://\S+", item)
        year = re.search(r"\b(?:19|20)\d{2}\b", item)
        bib[m.group(1).strip()] = {"type": "bibitem", "title": delatex(item)[:150],
                                   "doi": doi.group(0).rstrip(".") if doi else "",
                                   "url": url.group(0) if url else "", "year": year.group(0) if year else ""}
    undefined = sorted(cited - set(bib)) if "*" not in cited else []
    used = [bib[k] for k in cited if k in bib]
    uncited = sorted(set(bib) - cited)
    this_year = datetime.date.today().year
    years = [int(m.group(0)) for e in used if (m := re.search(r"\d{4}", e.get("year", "")))]
    with_id = [e for e in used if e.get("doi") or e.get("url") or e.get("eprint")]
    f["references"] = {
        "bib_entries": len(bib), "cited": len(used), "undefined_cites": undefined, "uncited_entries": uncited,
        "with_doi_or_url_pct": round(100 * len(with_id) / max(1, len(used))),
        "with_doi_pct": round(100 * sum(1 for e in used if e.get("doi")) / max(1, len(used))),
        "recent_pct": round(100 * sum(1 for y in years if y >= this_year - RECENT_YEARS) / max(1, len(used))),
        "year_range": [min(years), max(years)] if years else None,
    }
    n = len(used)
    count_pts = 4 if n >= 30 else 3 if n >= 20 else 2 if n >= 12 else 1 if n >= 5 else 0
    id_pct, rec_pct = f["references"]["with_doi_or_url_pct"], f["references"]["recent_pct"]
    id_pts = 2 if id_pct >= 80 else 1 if id_pct >= 50 else 0
    rec_pts = 2 if rec_pct >= 30 else 1 if rec_pct >= 15 else 0
    cons_pts = (1 if not undefined else 0) + (1 if len(uncited) <= 0.1 * max(1, len(bib)) else 0)
    r["auto"]["10 References"] = (count_pts + id_pts + rec_pts + cons_pts, 10,
                                  f"{n} cited; {id_pct}% DOI/URL; {rec_pct}% from {this_year - RECENT_YEARS}+; "
                                  f"{len(undefined)} undefined; {len(uncited)} uncited")

    if verify_dois:
        results = {}
        for key in sorted(cited & set(bib)):
            e = bib[key]
            if e.get("doi"):
                results[key] = verify_doi(e["doi"], e.get("title", ""))
            else:
                results[key] = ("no-doi", e.get("url", "") or "verify by web search")
        f["doi_check"] = {k: {"status": s, "detail": d} for k, (s, d) in results.items()}
        bad = [k for k, (s, _) in results.items() if s in ("not-found", "title-mismatch")]
        if bad:
            r["issues"].append(f"DOI problems (fix or remove): {', '.join(bad)}")

    # Labels and refs
    labels = set(re.findall(r"\\label\{([^}]+)\}", body))
    # lstlisting and friends take labels as an option: [caption=..., label={lst:x}]
    labels |= {m.strip() for m in re.findall(r"\blabel\s*=\s*\{?([^,}\]]+)", body)}
    refs = set()
    for group in re.findall(r"\\(?:ref|autoref|cref|Cref|eqref|pageref|nameref)\*?\{([^}]+)\}", body):
        refs.update(k.strip() for k in group.split(","))
    f["dangling_refs"] = sorted(refs - labels)

    # Figures
    figures = []
    for m in re.finditer(r"\\begin\{figure\*?\}(.*?)\\end\{figure\*?\}", body, re.S):
        block = m.group(1)
        if "\\includegraphics" not in block and "tikzpicture" not in block:
            continue  # a listing or table placed in a figure float is not a figure
        caption = (command_args(block, "caption") or [""])[0]
        label = re.search(r"\\label\{([^}]+)\}", block)
        fig = {"label": label.group(1) if label else None,
               "caption_words": words(delatex(caption)),
               "vector": "tikzpicture" in block, "graphics": []}
        fig["referenced"] = bool(label) and label.group(1) in refs
        for gm in re.finditer(r"\\includegraphics\s*(\[[^\]]*\])?\s*\{([^}]+)\}", block):
            path = resolve_graphic(paper, gm.group(2).strip())
            g = {"file": gm.group(2).strip(), "exists": bool(path)}
            if path is None:
                r["issues"].append(f"figure file not found: {gm.group(2)}")
            elif path.suffix.lower() == ".pdf":
                fig["vector"] = True
            else:
                px = image_pixels(path)
                width_in = printed_width_in(gm.group(1))
                if px and width_in:
                    g["effective_dpi"] = round(px[0] / width_in)
                elif px and px[2]:
                    g["effective_dpi"] = px[2]
                g["pixels"] = px[:2] if px else None
                g["kb"] = round(path.stat().st_size / 1024)
            fig["graphics"].append(g)
        figures.append(fig)
    f["figures"] = figures
    nfig = len(figures)
    referenced = sum(1 for x in figures if x["referenced"])
    captions_ok = nfig > 0 and all(x["caption_words"] >= 15 for x in figures)
    fig_pts = (3 if nfig >= 4 else 2 if nfig == 3 else 1 if nfig >= 1 else 0)
    fig_pts += 2 if nfig and referenced == nfig else 1 if nfig and referenced >= 0.75 * nfig else 0
    fig_pts += 1 if captions_ok else 0
    low_dpi = [g["file"] for x in figures for g in x["graphics"] if g.get("effective_dpi", 999) < 300]
    r["auto"]["11 Figures (auto part)"] = (fig_pts, 6, f"{nfig} figures; {referenced} referenced; "
                                           f"captions >= 15 words: {'yes' if captions_ok else 'no'}; "
                                           f"below 300 DPI: {', '.join(low_dpi) or 'none'}")

    # Tables and formal elements
    tables = re.findall(r"\\begin\{table\*?\}(.*?)\\end\{table\*?\}", body, re.S)
    booktabs = sum(1 for t in tables if "\\toprule" in t)
    f["tables"] = len(tables)
    f["tables_booktabs"] = booktabs
    f["equations"] = len(re.findall(r"\\begin\{(equation|align|gather|multline)\*?\}", body)) + body.count("\\[")
    f["listings"] = len(re.findall(r"\\begin\{lstlisting\}|\\lstinputlisting", body))
    f["algorithms"] = len(re.findall(r"\\begin\{algorithm", body))
    r["auto"]["12 Tables (auto part)"] = (2 if booktabs else 1 if tables else 0, 2,
                                          f"{len(tables)} tables ({booktabs} booktabs); {f['equations']} equations; "
                                          f"{f['listings']} listings; {f['algorithms']} algorithms")

    # Placeholders (anything outside comments, preamble included) and unsafe characters (all sources)
    visible_hits = []
    for pat in PLACEHOLDER_PATTERNS:
        visible_hits += [m.group(0) for m in re.finditer(pat, tex)]
    f["placeholders"] = visible_hits[:20]
    sources = [paper / main] + sorted((paper / "sections").glob("*.tex")) + sorted((paper / "figures").glob("*.tikz"))
    unsafe = []
    for src in sources:
        if not src.exists():
            continue
        for ln, line in enumerate(src.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            bad = sorted({c for c in line if ord(c) > 127 and c not in PDFLATEX_SAFE})
            if bad and not line.lstrip().startswith("%"):
                unsafe.append(f"{src.relative_to(paper)}:{ln} {' '.join(bad)}")
    f["unsafe_unicode"] = unsafe[:30]
    abs_paths = re.findall(r"\\(?:includegraphics|input|include)\s*(?:\[[^\]]*\])?\{(/[^}]*|[A-Za-z]:[^}]*)\}", tex)

    # Build log
    log = paper / f"{stem}.log"
    pdf = paper / f"{stem}.pdf"
    build = {"log": log.exists(), "pdf": pdf.exists()}
    if log.exists():
        lt = log.read_text(encoding="utf-8", errors="replace")
        build["errors"] = [l for l in lt.splitlines() if l.startswith("! ")][:10]
        build["undefined"] = sorted(set(re.findall(r"(?:Citation|Reference) `([^']+)' (?:on page \d+ )?undefined", lt)))
        build["overfull_over_10pt"] = [float(w) for w in re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide", lt) if float(w) > 10]
        build["missing_chars"] = len(re.findall(r"Missing character", lt))
        pages = re.search(r"Output written on \S+ \((\d+) pages?", lt)
        build["pages"] = int(pages.group(1)) if pages else None
    newest_src = max((p.stat().st_mtime for p in sources + list((paper / "sections").glob("*.bib"))
                      + list((paper / "figures").glob("*")) if p.exists()), default=0)
    build["pdf_fresh"] = pdf.exists() and pdf.stat().st_mtime >= newest_src - 1
    f["build"] = build
    compiles = build["log"] and build["pdf"] and not build.get("errors") and build["pdf_fresh"]
    clean_refs = compiles and not build.get("undefined") and not undefined and not f["dangling_refs"]
    tidy = compiles and not build.get("overfull_over_10pt") and not build.get("missing_chars")
    r["auto"]["14 Clean build"] = ((2 if compiles else 0) + (1 if clean_refs else 0) + (1 if tidy else 0), 4,
                                   f"pages {build.get('pages')}; errors {len(build.get('errors', []))}; "
                                   f"undefined {len(build.get('undefined', []))}; "
                                   f"overfull>10pt {len(build.get('overfull_over_10pt', []))}; "
                                   f"missing chars {build.get('missing_chars', 0)}; "
                                   f"pdf {'fresh' if build['pdf_fresh'] else 'stale or missing -- run ./build.sh'}")

    # arXiv package
    zpath = paper / "arxiv-upload.zip"
    pkg = {"exists": zpath.exists()}
    pts = 0
    if zpath.exists():
        pts += 1
        with zipfile.ZipFile(zpath) as z:
            names = z.namelist()
        needed = {main, f"{stem}.bbl"} | {n for n, ok in inputs if ok}
        for x in figures:
            for g in x["graphics"]:
                p = resolve_graphic(paper, g["file"])
                if p:
                    needed.add(str(p.relative_to(paper)))
        pkg["missing"] = sorted(needed - set(names))
        pkg["size_mb"] = round(zpath.stat().st_size / 1e6, 2)
        pkg["bad_names"] = [n for n in names if " " in n or any(part.startswith(".") for part in n.split("/"))]
        pts += 1 if not pkg["missing"] else 0
        if compile_zip and shutil.which("tectonic"):
            with tempfile.TemporaryDirectory() as tmp:
                with zipfile.ZipFile(zpath) as z:
                    z.extractall(tmp)
                try:
                    proc = subprocess.run(["tectonic", "--keep-logs", main], cwd=tmp,
                                          capture_output=True, text=True, timeout=600)
                    pkg["test_compile"] = "pass" if proc.returncode == 0 and (Path(tmp) / f"{stem}.pdf").exists() else "fail"
                except subprocess.TimeoutExpired:
                    pkg["test_compile"] = "timeout"
        else:
            pkg["test_compile"] = "skipped"
        pts += 1 if pkg["test_compile"] == "pass" else 0
        safe = not unsafe and not abs_paths and not pkg["bad_names"] and pkg["size_mb"] < 50
        pts += 1 if safe else 0
    f["package"] = pkg
    r["auto"]["15 arXiv package"] = (pts, 4, "no arxiv-upload.zip -- run ./build.sh arxiv" if not zpath.exists() else
                                     f"{pkg['size_mb']} MB; missing {pkg['missing'] or 'none'}; "
                                     f"test compile {pkg['test_compile']}; unsafe unicode lines {len(unsafe)}; "
                                     f"absolute paths {len(abs_paths)}")

    # Submission metadata and AI disclosure
    meta_path = paper / "arxiv-metadata.md"
    meta = {"exists": meta_path.exists()}
    mpts = 0
    if meta_path.exists():
        mt = meta_path.read_text(encoding="utf-8", errors="replace")

        def field(name):
            m = re.search(r"\*\*" + name + r":\*\*\s*(.+)", mt, re.I)
            return m.group(1).strip() if m else ""

        meta["primary"] = field("Primary category").strip("`")
        meta["comments"] = field("Comments")
        meta["license"] = field("License")
        am = re.search(r"##\s*Abstract[^\n]*\n(.*?)(?:\n##\s|\Z)", mt, re.S)
        meta_abs = re.sub(r"\s+", " ", am.group(1)).strip() if am else ""
        meta["abstract_chars"] = len(meta_abs)
        mpts += 1 if ARXIV_CATEGORY.match(meta["primary"]) else 0
        # TeX accents such as G\"odel are fine in the form; commands like \cite or \textbf are not
        latex_cmds = re.search(r"\\(?:cite|ref|label|text[a-z]+|emph|url|href|begin|end)\b", meta_abs)
        mpts += 1 if (meta_abs and len(meta_abs) <= ABSTRACT_CHAR_LIMIT and "{{" not in meta_abs
                      and not latex_cmds and re.search(r"\d+\s*pages", meta["comments"])) else 0
        mpts += 1 if LICENSES.search(meta["license"]) and "{{" not in meta["license"] else 0
    ack = re.search(r"\\section\*?\{[^}]*(?:Acknowledg|Disclosure)[^}]*\}(.*?)(?=\\section|\\bibliography|\\end\{document\})",
                    body, re.S | re.I)
    disclosure = bool(ack and re.search(r"generative AI|language model|AI assist|AI tool|\bLLM|Claude|ChatGPT|GPT-|Gemini|Copilot",
                                        ack.group(1), re.I) and "{{" not in ack.group(1))
    meta["ai_disclosure"] = disclosure
    mpts += 1 if disclosure else 0
    f["metadata"] = meta
    r["auto"]["16 Submission metadata"] = (mpts, 4, "no arxiv-metadata.md" if not meta_path.exists() else
                                           f"category '{meta['primary']}'; comments '{meta['comments']}'; "
                                           f"license '{meta['license']}'; abstract {meta['abstract_chars']} chars; "
                                           f"AI disclosure {'yes' if disclosure else 'no'}")

    # Hard gates visible to the script (references verified + no fabrication are judged by you)
    r["gates"] = {
        "compiles without errors": bool(compiles),
        "no undefined citations or references": bool(clean_refs),
        "abstract <= 1,920 characters": 0 < f["abstract_chars"] <= ABSTRACT_CHAR_LIMIT,
        "no placeholder text": not visible_hits,
    }
    if "doi_check" in f:
        r["gates"]["all DOIs resolve to the cited work"] = not any(
            v["status"] in ("not-found", "title-mismatch") for v in f["doi_check"].values())
    r["auto_points"] = sum(v[0] for v in r["auto"].values())
    r["auto_max"] = sum(v[1] for v in r["auto"].values())
    return r


# ---------------------------------------------------------------- report

def report(r):
    f = r["facts"]
    out = [f"# Automated checks: {r['slug']}", ""]
    if "title" not in f:
        return "\n".join(out + r["issues"])
    out += ["## Auto-scored criteria", "", "| Criterion | Points | Max | Notes |", "|---|---:|---:|---|"]
    for name, (pts, mx, note) in r["auto"].items():
        out.append(f"| {name} | {pts} | {mx} | {note} |")
    out += [f"| **Auto subtotal** | **{r['auto_points']}** | **{r['auto_max']}** | "
            f"the other {100 - r['auto_max']} points are judgment criteria |", ""]

    out += ["## Hard gates (script-visible)", ""]
    out += [f"- [{'x' if ok else ' '}] {g}" for g, ok in r["gates"].items()]
    out += ["- [ ] every reference verified real (judge; see DOI check)",
            "- [ ] no fabricated data, results, quotes or statistics (judge)", ""]

    roles = f["section_roles"]
    out += ["## Facts for judgment criteria", "",
            f"- **Title** ({f['title_words']} words): {f['title']}",
            f"- **Authors** ({len(f['authors'])}): {'; '.join(f['authors'])}",
            f"- **Abstract**: {f['abstract_words']} words, {f['abstract_chars']} chars "
            f"(limit {ABSTRACT_CHAR_LIMIT}); citations in abstract: {f['abstract_has_cite']}; keywords line: {f['keywords']}",
            f"- **Sections** ({len(f['sections'])}, {f['subsection_count']} subsections): " + " | ".join(f["sections"]),
            "- **Section roles found**: " + ", ".join(f"{k}={'yes' if v else 'NO'}" for k, v in roles.items()),
            f"- **Body length**: ~{f['body_words']} words, {f['build'].get('pages')} pages",
            f"- **References**: {f['references']}",
            f"- **Formal elements**: {f['tables']} tables, {f['equations']} equations, "
            f"{f['listings']} listings, {f['algorithms']} algorithms"]
    for i, x in enumerate(f["figures"], 1):
        gs = ", ".join(f"{g['file']} ({g.get('effective_dpi', '?')} dpi)" for g in x["graphics"]) or "TikZ/vector"
        out.append(f"- **Figure {i}** `{x['label']}`: {gs}; caption {x['caption_words']} words; "
                   f"referenced {x['referenced']}")
    if f["dangling_refs"]:
        out.append(f"- **Refs to missing labels**: {', '.join(f['dangling_refs'])}")
    if f["placeholders"]:
        out.append(f"- **Placeholder text**: {', '.join(f['placeholders'])}")
    if f["unsafe_unicode"]:
        out.append("- **pdfLaTeX-unsafe characters** (replace with LaTeX commands):")
        out += [f"    - {u}" for u in f["unsafe_unicode"]]
    if "doi_check" in f:
        counts = {}
        for v in f["doi_check"].values():
            counts[v["status"]] = counts.get(v["status"], 0) + 1
        out.append(f"- **DOI check**: {counts}")
        for k, v in f["doi_check"].items():
            if v["status"] != "verified":
                out.append(f"    - {k}: {v['status']} {v['detail'][:100]}")
    if r["issues"]:
        out += ["", "## Issues", ""] + [f"- {i}" for i in r["issues"]]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper", type=Path, help="paper folder containing main.tex")
    ap.add_argument("--main", default="main.tex", help="main .tex file name if not main.tex")
    ap.add_argument("--json", type=Path, help="write the full results as JSON")
    ap.add_argument("--verify-dois", action="store_true", help="look up every cited DOI (network)")
    ap.add_argument("--no-compile", action="store_true", help="skip test-compiling arxiv-upload.zip")
    args = ap.parse_args()
    if not (args.paper / args.main).exists():
        sys.exit(f"error: {args.paper}/{args.main} not found")
    r = check_paper(args.paper.resolve(), args.verify_dois, not args.no_compile, args.main)
    print(report(r))
    if args.json:
        args.json.write_text(json.dumps(r, indent=2, default=str))


if __name__ == "__main__":
    main()

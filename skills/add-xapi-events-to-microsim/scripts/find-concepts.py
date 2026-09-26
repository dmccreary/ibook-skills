#!/usr/bin/env python3
"""Propose learning-graph concepts for a MicroSim's objects, with namespaced concept ids.

PROPOSES ONLY. The agent chooses, and leaves an object unmapped when nothing genuinely
fits (references/concept-mapping.md: warn, never guess). Scores are token overlap plus
fuzzy similarity; they cannot tell that "Animal Cell" is about "Eukaryotic Cells".

Usage:
    find-concepts.py --book <book-root> --sim docs/sims/<name>       # terms from the sim
    find-concepts.py --book <book-root> "data loss" "prediction"     # explicit terms
    find-concepts.py --book <book-root> --id 353 15                  # look ids up
    options: --top N (default 5 per term)  --json

Concept id form: {conceptPrefix}-{ConceptID}. conceptPrefix comes from the book's
docs/js/lrs-config.js if present, else the slug of the repo directory name (the rule the
LRS seeder uses: src/lrs/catalog.py `_slug(repo.name)`).

Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import re
import sys
from pathlib import Path

STOP = set(["a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "with", "by", "from", "at", "as", "is", "are", "be", "this", "that", "these", "those", "it", "its", "into", "your", "you", "how", "what", "why", "when", "which", "using", "use", "via", "vs", "than", "then", "there", "their", "about", "simulator", "simulation", "sim", "microsim", "diagram", "interactive", "chart", "viewer", "explorer", "workflow", "flow", "step", "steps", "show", "shows", "click", "hover", "drag", "select", "pick", "press", "button", "slider"])


def slug(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def find_book_root(start: Path) -> Path:
    d = start.resolve()
    while d != d.parent:
        if (d / "mkdocs.yml").is_file():
            return d
        d = d.parent
    sys.exit(f"no mkdocs.yml above {start}")


def concept_prefix(book: Path) -> tuple[str, str]:
    cfg = book / "docs" / "js" / "lrs-config.js"
    if cfg.is_file():
        m = re.search(r"conceptPrefix\s*:\s*['\"]([^'\"]+)['\"]", cfg.read_text())
        if m:
            return m.group(1), "lrs-config.js"
    for line in (book / "mkdocs.yml").read_text(errors="replace").splitlines():
        m = re.match(r"\s*repo_url\s*:\s*['\"]?([^'\"#\s]+)", line)
        if m and m.group(1).rstrip("/").rsplit("/", 1)[-1]:
            name = m.group(1).rstrip("/").rsplit("/", 1)[-1].removesuffix(".git")
            return slug(name), "mkdocs.yml repo_url (no lrs-config.js yet)"
    return slug(book.name), "repo directory name (no lrs-config.js yet)"


def load_graph(book: Path) -> tuple[list[dict[str, str]], dict[str, str]]:
    lg = book / "docs" / "learning-graph"
    csv_path = lg / "learning-graph.csv"
    if not csv_path.is_file():
        sys.exit(f"no learning graph at {csv_path} — concept ids cannot be namespaced; "
                 "stop and ask the user (references/concept-mapping.md)")
    with csv_path.open(newline="", encoding="utf-8", errors="replace") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("ConceptID") or "").strip()]
    names: dict[str, str] = {}
    tn = lg / "taxonomy-names.json"
    if tn.is_file():
        try:
            names = json.loads(tn.read_text())
        except ValueError:
            pass
    return rows, names


def tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOP and len(t) > 1}


def stem(t: str) -> str:
    for suf in ("ing", "ies", "es", "s", "ed"):
        if t.endswith(suf) and len(t) - len(suf) >= 3:
            return t[: -len(suf)] + ("y" if suf == "ies" else "")
    return t


def score(term: str, label: str) -> float:
    a = {stem(t) for t in tokens(term)}
    b = {stem(t) for t in tokens(label)}
    if not a or not b:
        return 0.0
    overlap = len(a & b) / len(b | a)
    fuzzy = difflib.SequenceMatcher(None, term.lower(), label.lower()).ratio()
    exact = 1.0 if term.strip().lower() == label.strip().lower() else 0.0
    return round(0.55 * overlap + 0.30 * fuzzy + 0.15 * exact + (0.25 if exact else 0), 3)


def sim_terms(sim: Path) -> list[str]:
    terms: list[str] = []
    meta = sim / "metadata.json"
    if meta.is_file():
        try:
            m = json.loads(meta.read_text())
        except ValueError:
            m = {}
        for k in ("title",):
            if isinstance(m.get(k), str):
                terms.append(m[k])
        for k in ("concepts", "subject"):
            v = m.get(k)
            if isinstance(v, list):
                terms += [x for x in v if isinstance(x, str)]
    idx = sim / "index.md"
    if idx.is_file():
        for line in idx.read_text(errors="replace").splitlines():
            if line.startswith("# "):
                terms.append(line[2:].strip())
                break
    # Control and node labels in the sim's own code.
    for f in list(sim.glob("*.js")) + [sim / "main.html"]:
        if not f.is_file():
            continue
        text = f.read_text(errors="replace")
        for m in re.finditer(r"create(?:Button|Checkbox)\(\s*['\"]([^'\"]{3,40})['\"]", text):
            terms.append(m.group(1))
        for m in re.finditer(r"\btitle\s*:\s*['\"]([^'\"]{3,60})['\"]", text):
            terms.append(m.group(1))
        for m in re.finditer(r"\blabel\s*:\s*['\"]([^'\"]{3,60})['\"]", text):
            terms.append(m.group(1))
    seen: set[str] = set()
    out = []
    for t in terms:
        k = t.strip().lower()
        if k and k not in seen and tokens(t):
            seen.add(k)
            out.append(t.strip())
    return out[:40]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--book", type=Path, default=Path("."))
    ap.add_argument("--sim", type=Path)
    ap.add_argument("--id", nargs="*", default=[])
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--min", type=float, default=0.2, help="hide candidates scoring below this")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    book = find_book_root(a.book)
    prefix, source = concept_prefix(book)
    rows, taxa = load_graph(book)
    by_id = {r["ConceptID"].strip(): r for r in rows}

    def describe(r: dict[str, str], s: float | None = None) -> dict[str, object]:
        tax = (r.get("TaxonomyID") or "").strip()
        return {"concept_id": f"{prefix}-{r['ConceptID'].strip()}", "ConceptID": int(r["ConceptID"]),
                "label": r["ConceptLabel"].strip(), "taxonomy": tax, "taxonomy_name": taxa.get(tax, ""),
                **({"score": s} if s is not None else {})}

    result: dict[str, object] = {"book": str(book), "conceptPrefix": prefix, "prefix_source": source,
                                 "concepts": len(rows), "ids": [], "terms": {}}
    for i in a.id:
        r = by_id.get(str(i))
        result["ids"].append(describe(r) if r else {"ConceptID": i, "error": "not in learning graph"})  # type: ignore[attr-defined]

    terms = list(a.terms) + (sim_terms(a.sim) if a.sim else [])
    for t in terms:
        ranked = sorted(((score(t, r["ConceptLabel"]), r) for r in rows), key=lambda x: -x[0])
        result["terms"][t] = [describe(r, s) for s, r in ranked[: a.top] if s >= a.min]  # type: ignore[index]

    if a.json:
        print(json.dumps(result, indent=2))
        return 0
    print(f"book: {book}   conceptPrefix: {prefix}  (from {source})   {len(rows)} concepts")
    for d in result["ids"]:  # type: ignore[attr-defined]
        print(f"  id {d.get('ConceptID')}: " + (d.get("error") or f"{d['concept_id']}  {d['label']}  [{d['taxonomy']}]"))
    for t, cands in result["terms"].items():  # type: ignore[attr-defined]
        print(f"\n\"{t}\"")
        if not cands:
            print("    (no candidate above threshold — leave unmapped unless you find one by reading the graph)")
        for c in cands:
            tax = f"{c['taxonomy']} {c['taxonomy_name']}".strip()
            print(f"    {c['score']:.2f}  {c['concept_id']:<34} {c['label']}   [{tax}]")
    print("\nThese are proposals. Choose one concept per object, or leave it unmapped and say so.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

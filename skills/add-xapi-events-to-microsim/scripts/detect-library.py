#!/usr/bin/env python3
"""Detect a MicroSim's rendering library from its <script> tags, and inventory its interactions.

Why script tags: the MicroSim catalog's `library` field is empty for ~45% of sims, and
metadata.json is often stale. main.html is what actually runs.

Usage:
    detect-library.py docs/sims/<name>            # human-readable report
    detect-library.py docs/sims/<name> --json     # machine-readable
    detect-library.py docs/sims --all --json      # every sim under a directory (batch mode)

Reports, per sim:
    library        p5.js | mermaid | vis-network | vis-timeline | chart.js | plotly | leaflet |
                   d3 | venn | html   (plus every library found, in load order)
    adapter        the references/adapters/*.md file(s) to read
    instrumented   whether the xAPI runtime (lrs-sim.js) is already loaded, and in what order
    vendored       local scripts outside the sim's own folder (shared libraries: wrap, never edit)
    hooks          interaction hooks found in the sim's own JS, with line numbers — a starting
                   point for the inventory, not the inventory
    instructions   visible instruction text ("Click a node…"), which names the designed act

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

LIBRARIES = [
    # (library id, regex on the script src)
    ("p5.js", r"(^|/)p5(@[\d.]+)?(/lib)?/p5(\.min)?\.js|/p5\.js|p5\.min\.js"),
    ("mermaid", r"mermaid"),
    ("vis-network", r"vis-network"),
    ("vis-timeline", r"vis-timeline"),
    ("chart.js", r"chart\.js|chart\.umd|chartjs"),
    ("plotly", r"plotly"),
    ("leaflet", r"leaflet"),
    ("venn", r"venn"),
    ("d3", r"(^|/)d3(@[\d.]+)?(/dist)?/d3(\.min)?\.js|/d3@"),
]

ADAPTER = {
    "p5.js": "p5-dom-controls.md",
    "mermaid": "mermaid-html.md",
    "vis-network": "vis-network.md",
    "vis-timeline": "vis-timeline.md",
    "chart.js": "chartjs.md",
    "plotly": "plotly.md",
    "leaflet": "leaflet.md",
    "venn": "mermaid-html.md",
    "d3": "mermaid-html.md",
    "html": "mermaid-html.md",
}
VERIFIED = {"p5-dom-controls.md", "mermaid-html.md", "image-overlay.md", "quiz-page.md"}
PILOTED = {"chartjs.md", "p5-canvas.md"}   # passed an eval pilot; verified once the pilot is committed

RUNTIME = ["lrs-config.js", "lrs-xapi.js", "lrs-lite-sim.js", "lrs-sim.js", "xapi-json-viewer.js"]

# Interaction hooks worth knowing about, per family. Each is (label, regex).
HOOKS = [
    ("p5 slider", r"\bcreateSlider\s*\("),
    ("p5 button", r"\bcreateButton\s*\("),
    ("p5 select", r"\bcreateSelect\s*\("),
    ("p5 checkbox", r"\bcreateCheckbox\s*\("),
    ("p5 radio", r"\bcreateRadio\s*\("),
    ("p5 input", r"\bcreateInput\s*\("),
    ("p5 canvas mousePressed", r"^\s*function\s+mousePressed\s*\("),
    ("p5 canvas mouseReleased", r"^\s*function\s+mouseReleased\s*\("),
    ("p5 canvas mouseDragged", r"^\s*function\s+mouseDragged\s*\("),
    ("p5 canvas mouseClicked", r"^\s*function\s+mouseClicked\s*\("),
    ("p5 canvas doubleClicked", r"^\s*function\s+doubleClicked\s*\("),
    ("p5 keyPressed", r"^\s*function\s+keyPressed\s*\("),
    ("p5 touchStarted", r"^\s*function\s+touchStarted\s*\("),
    ("auto-run on load (isRunning = true / loop without pause)", r"\b(isRunning|running|playing)\s*=\s*true\s*;"),
    ("DOM listener", r"addEventListener\(\s*['\"](click|mouseenter|mouseleave|mouseover|mouseout|pointerenter|pointerleave|input|change|keydown|wheel|dblclick)['\"]"),
    ("DOM on* property", r"\.on(click|mouseenter|mouseleave|mouseover|mouseout|input|change)\s*="),
    ("stopPropagation (bubbling listeners will miss these)", r"stopPropagation\s*\("),
    ("document/window-level listener (check panel clicks don't reach it)",
     r"(document|window|document\.body)\.addEventListener\(\s*['\"](?!DOMContentLoaded|load|resize|message)"),
    ("vis-network event", r"network\.(on|once)\(\s*['\"](\w+)['\"]"),
    ("vis-timeline event", r"timeline\.(on|once)\(\s*['\"](\w+)['\"]"),
    ("Chart.js onClick", r"\bonClick\s*[:(]"),
    ("Chart.js onHover", r"\bonHover\s*[:(]"),
    ("Chart.js legend", r"legend\s*:\s*\{(?!\s*display\s*:\s*false)"),
    ("Plotly event", r"\.on\(\s*['\"]plotly_\w+['\"]"),
    ("Leaflet event", r"\.on\(\s*['\"](click|popupopen|zoomend|moveend|overlayadd|overlayremove|baselayerchange)['\"]"),
    ("Leaflet programmatic view", r"\.(setView|fitBounds|flyTo)\s*\("),
    ("quiz / answer logic", r"(?i)\b(correct|isCorrect|checkAnswer|handleAnswer|prediction|score)\b"),
    ("random order (ordinal question ids are NOT stable)", r"Math\.random\(\)\s*-\s*0\.5|shuffle\s*\("),
    ("mode switch", r"(?i)\bset_?mode\s*\(|\bmode\s*=\s*['\"]"),
]

INSTRUCTION_RE = re.compile(
    r"(?i)(click|hover|tap|drag|select|press|move the|use the|pick)\b[^<>\"'`\n]{5,120}"
)


class ScriptTags(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.scripts: list[dict[str, str | None]] = []
        self.links: list[str] = []
        self.has_main = False
        self.main_has_id = False
        self._in_module = False
        self.inline: list[str] = []
        self._capture = False
        self._buf: list[str] = []
        self.text: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag == "script":
            self.scripts.append({"src": a.get("src"), "type": a.get("type")})
            if not a.get("src"):
                self._capture = True
                self._buf = []
            self._skip += 1
        elif tag == "style":
            self._skip += 1
        elif tag == "link" and (a.get("rel") or "") == "stylesheet" and a.get("href"):
            self.links.append(a["href"] or "")
        elif tag == "main":
            self.has_main = True
            self.main_has_id = "id" in a

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            if self._capture:
                self.inline.append("".join(self._buf))
                self._capture = False
            self._skip = max(0, self._skip - 1)
        elif tag == "style":
            self._skip = max(0, self._skip - 1)

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buf.append(data)
        elif not self._skip and data.strip():
            self.text.append(data.strip())


def classify_src(src: str) -> str | None:
    for lib, pattern in LIBRARIES:
        if re.search(pattern, src, re.IGNORECASE):
            return lib
    return None


def inspect(sim: Path) -> dict[str, object]:
    main = sim / "main.html"
    if not main.is_file():
        return {"sim": str(sim), "error": "no main.html"}
    html = main.read_text(encoding="utf-8", errors="replace")
    p = ScriptTags()
    p.feed(html)

    libraries: list[str] = []
    runtime_loaded: list[str] = []
    vendored: list[str] = []
    own_js: list[Path] = []
    order: list[str] = []
    for s in p.scripts:
        src = s.get("src")
        if not src:
            order.append("<inline>")
            continue
        order.append(src)
        lib = classify_src(src)
        if lib and lib not in libraries:
            libraries.append(lib)
        name = src.rsplit("/", 1)[-1]
        if name in RUNTIME:
            runtime_loaded.append(name)
            continue
        if src.startswith(("http://", "https://", "//")):
            # ESM imports inside inline modules are handled below
            continue
        path = (sim / src).resolve()
        if sim.resolve() in path.parents:
            own_js.append(path)
        else:
            vendored.append(src)

    # Libraries imported from inline module scripts (e.g. Mermaid 11 ESM).
    for block in p.inline:
        for m in re.finditer(r"import\s+[^;]*?from\s+['\"]([^'\"]+)['\"]", block):
            lib = classify_src(m.group(1))
            if lib and lib not in libraries:
                libraries.append(lib)

    primary = libraries[0] if libraries else "html"
    adapters = []
    for lib in libraries or ["html"]:
        a = ADAPTER.get(lib, "mermaid-html.md")
        if a not in adapters:
            adapters.append(a)

    # Image-overlay / diagram.js hotspot sims.
    if any("diagram.js" in v for v in vendored) or (sim / "data.json").is_file() and re.search(
        r"callouts", (sim / "data.json").read_text(errors="replace")
    ):
        adapters.insert(0, "image-overlay.md")

    hooks: list[dict[str, object]] = []
    sources = [(f, f.read_text(encoding="utf-8", errors="replace")) for f in own_js if f.is_file()]
    for v in vendored:
        vp = (sim / v).resolve()
        if vp.is_file():
            sources.append((vp, vp.read_text(encoding="utf-8", errors="replace")))
    sources.append((main, "\n".join(p.inline)))
    canvas_hit = False
    for f, text in sources:
        lines = text.splitlines()
        # Answer logic is code, not prose: match it with string literals blanked out, so the
        # word "score" in a node's description is not reported as quiz logic.
        code_only = [re.sub(r"'[^'\n]*'|\"[^\"\n]*\"|`[^`\n]*`", "''", ln) for ln in lines]
        for label, pattern in HOOKS:
            rx = re.compile(pattern, re.MULTILINE)
            src_lines = code_only if label.startswith("quiz") else lines
            hits = [i + 1 for i, line in enumerate(src_lines) if rx.search(line)]
            if hits:
                hooks.append({"file": f.name, "hook": label, "lines": hits[:12], "count": len(hits)})
                if label.startswith("p5 canvas"):
                    canvas_hit = True
    if primary == "p5.js" and canvas_hit and "p5-canvas.md" not in adapters:
        adapters.append("p5-canvas.md")

    instructions: list[str] = []
    strings: list[str] = []
    for _, src in sources:
        for m in re.finditer(r"'([^'\n]{12,160})'|\"([^\"\n]{12,160})\"|`([^`\n]{12,160})`", src):
            strings.append(next(g for g in m.groups() if g))
    for t in p.text + strings:
        if re.search(r"[;{}=]|\w\(", t):          # code, not prose
            continue
        if INSTRUCTION_RE.search(t) and t not in instructions and len(instructions) < 8:
            instructions.append(t[:160])

    meta_lib = None
    meta = sim / "metadata.json"
    if meta.is_file():
        try:
            md = json.loads(meta.read_text())
            meta_lib = md.get("library") or (md.get("technical") or {}).get("framework")
        except (ValueError, AttributeError):
            meta_lib = "<unreadable metadata.json>"

    missing = [r for r in RUNTIME if r not in runtime_loaded]
    return {
        "sim": str(sim),
        "library": primary,
        "libraries": libraries or ["html"],
        "metadata_library": meta_lib,
        "adapters": [{"file": a, "verified": a in VERIFIED, "piloted": a in PILOTED} for a in adapters],
        "instrumented": bool(runtime_loaded),
        "runtime_loaded": runtime_loaded,
        "runtime_missing": missing if runtime_loaded else RUNTIME,
        "runtime_order_ok": runtime_loaded == [r for r in RUNTIME if r in runtime_loaded],
        "panel_css_linked": any("lrs-xapi.css" in h for h in p.links),
        "script_order": order,
        "own_js": [str(f.relative_to(sim.resolve())) for f in own_js],
        "vendored": vendored,
        "main_tag": "n/a (not p5)" if primary != "p5.js" else
                    "ok" if p.has_main and not p.main_has_id else
                    ("has id (p5-editor rule: no id)" if p.main_has_id else "absent"),
        "has_metadata": meta.is_file(),
        "hooks": hooks,
        "instructions": instructions,
    }


def report(r: dict[str, object]) -> str:
    if "error" in r:
        return f"{r['sim']}: {r['error']}"
    out = [f"== {r['sim']}"]
    out.append(f"library:       {r['library']}   (all: {', '.join(r['libraries'])}; "
               f"metadata.json says: {r['metadata_library']!r})")
    out.append("adapters:      " + ", ".join(
        f"{a['file']}{'' if a['verified'] else ' (piloted)' if a.get('piloted') else ' (UNVERIFIED)'}"
        for a in r["adapters"]))  # type: ignore[index]
    if r["instrumented"]:
        out.append(f"instrumented:  YES — runtime loaded: {', '.join(r['runtime_loaded'])}"  # type: ignore[arg-type]
                   + ("" if r["runtime_order_ok"] else "   !! load order is wrong"))
        if r["runtime_missing"]:
            out.append(f"               missing: {', '.join(r['runtime_missing'])}")  # type: ignore[arg-type]
    else:
        out.append("instrumented:  no")
    out.append(f"panel css:     {'linked' if r['panel_css_linked'] else 'not linked'}")
    out.append(f"own js:        {', '.join(r['own_js']) or '(inline only)'}")  # type: ignore[arg-type]
    if r["vendored"]:
        out.append(f"vendored:      {', '.join(r['vendored'])}   <- shared: wrap from xapi.js, never edit")  # type: ignore[arg-type]
    out.append(f"<main>:        {r['main_tag']}")
    out.append("hooks:")
    for h in r["hooks"]:  # type: ignore[attr-defined]
        more = f" (+{h['count'] - len(h['lines'])} more)" if h["count"] > len(h["lines"]) else ""
        out.append(f"  {h['file']:<28} {h['hook']:<60} lines {h['lines']}{more}")
    if r["instructions"]:
        out.append("instruction text (names the designed act):")
        for t in r["instructions"]:  # type: ignore[attr-defined]
            out.append(f"  \"{t}\"")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", type=Path, help="a sim directory, or with --all a directory of sims")
    ap.add_argument("--all", action="store_true", help="inspect every subdirectory that has a main.html")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    sims = sorted(d for d in a.path.iterdir() if (d / "main.html").is_file()) if a.all else [a.path]
    results = [inspect(s) for s in sims]
    if a.json:
        print(json.dumps(results if a.all else results[0], indent=2))
    else:
        print("\n\n".join(report(r) for r in results))
    return 0 if all("error" not in r for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())

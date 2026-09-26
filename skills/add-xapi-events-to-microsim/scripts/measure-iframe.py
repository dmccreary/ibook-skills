#!/usr/bin/env python3
"""Measure a MicroSim's content height with a FULL xAPI log, and recommend its iframe height.

A teaching sim gains the statement panel, so the iframe in index.md must grow; measured
with an empty log it looks fine and then clips the moment a student interacts. This loads
main.html at each width with the metadata.json `xapi` block rewritten in flight
(teaching on for the teaching measurement, off for the production one), fills every
statement log to overflow, and measures the document's content height.

    uv run --with playwright==1.58.0 python measure-iframe.py docs/sims/<name>
    options: --widths 375,700,900   --json out.json   --margin 10
             --eval "JS"   (repeatable) run in the sim before measuring, to reach its TALLEST
                           state: a quiz mode, an open detail panel (e.g. --eval "sim.setMode('quiz')")

It measures the state the page is in after load (plus any --eval). A sim whose height
changes with its state must be measured in its tallest state, or the iframe clips there.

The recommendation is the 700 px measurement (the book's content column) rounded up, with a
warning when 375 px (phone) is much taller. A production sim should measure the same as
before instrumenting; if it grew, the wiring added something visible.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import math
import re
import sys
import threading
from pathlib import Path
from typing import Any

FILL_LOG = """(n) => {
  const line = JSON.stringify({id: '00000000-0000-4000-8000-000000000000', verb: {id:
    'http://adlnet.gov/expapi/verbs/interacted'}, object: {id: location.href + '#a-long-fragment-name'},
    context: {extensions: {'https://w3id.org/lrs/ext/concept_id': 'some-book-123'}}});
  document.querySelectorAll('.xapi-log').forEach(log => {
    for (let i = 0; i < n; i++) {
      const a = document.createElement('div'); a.className = 'xapi-log-line'; a.textContent = '▸ interacted  some-control=0.5 (was 0.4)';
      const b = document.createElement('div'); b.className = 'xapi-log-line xapi-log-raw'; b.textContent = line;
      log.appendChild(a); log.appendChild(b);
    }
  });
  return document.querySelectorAll('.xapi-log').length;
}"""

# The lowest rendered edge, NOT descending into elements that clip their content (a
# max-height log with overflow:auto): their overflowing children report rects far below the
# box they are clipped to. Measured this way, content shorter than the viewport is still
# measured correctly, and a 100vh layout measures as the viewport it was given.
CONTENT_HEIGHT = """() => {
  let bottom = 0;
  const walk = (el) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.position === 'fixed') return;
    if (cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) return;   // e.g. Mermaid's hidden tooltip div
    const r = el.getBoundingClientRect();
    if (r.height > 0) bottom = Math.max(bottom, r.bottom + scrollY + parseFloat(cs.marginBottom || 0));
    const clips = cs.overflowY !== 'visible' || cs.overflowX !== 'visible';
    if (!clips) for (const c of el.children) walk(c);
  };
  for (const c of document.body.children) walk(c);
  const b = getComputedStyle(document.body);
  return Math.ceil(bottom + parseFloat(b.paddingBottom || 0) + parseFloat(b.marginBottom || 0));
}"""


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        pass

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def find_book_root(start: Path) -> Path:
    d = start.resolve()
    while d != d.parent:
        if (d / "mkdocs.yml").is_file():
            return d
        d = d.parent
    sys.exit(f"no mkdocs.yml above {start}")


def iframe_height(index: Path) -> int | None:
    if not index.is_file():
        return None
    text = index.read_text(errors="replace")
    m = re.search(r"<iframe[^>]*src=['\"][^'\"]*main\.html['\"][^>]*>", text)
    if not m:
        return None
    tag = m.group(0)
    h = re.search(r"height=['\"]?(\d+)", tag) or re.search(r"height:\s*(\d+)px", tag)
    return int(h.group(1)) if h else None


def embeds(docs: Path, sim: Path) -> list[tuple[str, int | None]]:
    """Every iframe in the book that shows this sim: its index.md, and chapters that embed it."""
    name = sim.name
    out: list[tuple[str, int | None]] = []
    for md in docs.rglob("*.md"):
        text = md.read_text(errors="replace")
        for m in re.finditer(r"<iframe[^>]*src=['\"]([^'\"]*)['\"][^>]*>", text):
            src = m.group(1)
            same = md.parent == sim and re.fullmatch(r"(\./)?main\.html", src)
            if same or re.search(rf"(^|/)sims/{re.escape(name)}/main\.html", src):
                h = re.search(r"height=['\"]?(\d+)", m.group(0)) or re.search(r"height:\s*(\d+)px", m.group(0))
                line = text[: m.start()].count("\n") + 1
                out.append((f"{md.relative_to(docs)}:{line}", int(h.group(1)) if h else None))
    return out


def canvas_height_source(sim: Path) -> tuple[str, int] | None:
    """sync-iframe-heights.py's priority order: // CANVAS_HEIGHT in <sim>.js, metadata canvasHeight, main.html comment."""
    js = sim / f"{sim.name}.js"
    if js.is_file():
        head = "\n".join(js.read_text(errors="replace").splitlines()[:15])
        m = re.search(r"CANVAS_HEIGHT:\s*(\d+)", head)
        if m:
            return f"{js.name} // CANVAS_HEIGHT comment", int(m.group(1))
    meta = sim / "metadata.json"
    if meta.is_file():
        m = re.search(r'"canvasHeight"\s*:\s*(\d+)', meta.read_text(errors="replace"))
        if m:
            return "metadata.json canvasHeight", int(m.group(1))
    main = sim / "main.html"
    if main.is_file():
        m = re.search(r"<!--\s*CANVAS_HEIGHT:\s*(\d+)\s*-->", main.read_text(errors="replace"))
        if m:
            return "main.html <!-- CANVAS_HEIGHT --> comment", int(m.group(1))
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sim", type=Path)
    ap.add_argument("--widths", default="375,700,900")
    ap.add_argument("--margin", type=int, default=10, help="px added before rounding up to 10")
    ap.add_argument("--lines", type=int, default=60, help="log entries to add (fills any max-height)")
    ap.add_argument("--json", type=Path)
    ap.add_argument("--eval", action="append", default=[], dest="evals")
    a = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright missing. Run: uv run --with playwright==1.58.0 python measure-iframe.py ...")
        return 2

    sim = a.sim.resolve()
    book = find_book_root(sim)
    docs = book / "docs"
    rel = sim.relative_to(docs.resolve()).as_posix()
    current = iframe_height(sim / "index.md")
    meta_path = sim / "metadata.json"
    meta = json.loads(meta_path.read_text()) if meta_path.is_file() else {}
    xmeta = meta.get("xapi") if isinstance(meta.get("xapi"), dict) else {}
    widths = [int(w) for w in a.widths.split(",")]
    view_h = current or 600

    handler = functools.partial(_Quiet, directory=str(docs))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"

    rows: list[dict[str, Any]] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for teaching in (True, False):
            for w in widths:
                ctx = browser.new_context(viewport={"width": w, "height": view_h})
                page = ctx.new_page()
                block = dict(xmeta, teaching=teaching)
                if teaching:
                    block["compact"] = False

                def rewriter(block: dict[str, Any]) -> Any:
                    # A factory: Playwright passes (route, request) to a two-parameter handler.
                    def rewrite(route: Any) -> None:
                        resp = route.fetch()
                        try:
                            m = resp.json() if resp.ok else {}
                        except ValueError:
                            m = {}
                        m["xapi"] = block
                        route.fulfill(status=200, content_type="application/json", body=json.dumps(m))
                    return rewrite

                page.route(f"**/{rel}/metadata.json", rewriter(block))
                page.goto(f"{base}/{rel}/main.html")
                try:
                    page.wait_for_function("window.LRSLite && document.documentElement.dataset.xapiMode",
                                           timeout=20000)
                except Exception:
                    pass
                page.wait_for_timeout(2000)            # async renderers (Mermaid, charts) settle
                for js in a.evals:
                    page.evaluate(js)
                    page.wait_for_timeout(500)
                logs = page.evaluate(FILL_LOG, a.lines) if teaching else 0
                page.wait_for_timeout(200)
                h = page.evaluate(CONTENT_HEIGHT)
                overflow = page.evaluate("document.documentElement.scrollWidth - innerWidth")
                rows.append({"teaching": teaching, "width": w, "height": h, "logs": logs, "overflow_x": overflow})
                ctx.close()
        browser.close()
    server.shutdown()

    print(f"sim: {rel}    index.md iframe height: {current if current else 'not found'}"
          f"    (viewport height used: {view_h})\n")
    print(f"{'mode':<12}{'width':>6}{'content px':>12}{'logs':>6}{'x-overflow':>12}")
    for r in rows:
        print(f"{'teaching' if r['teaching'] else 'production':<12}{r['width']:>6}{r['height']:>12}"
              f"{r['logs']:>6}{r['overflow_x']:>12}")

    t = {r["width"]: r["height"] for r in rows if r["teaching"]}
    pr = {r["width"]: r["height"] for r in rows if not r["teaching"]}
    col = 700 if 700 in t else max(t)
    rec = int(math.ceil((t[col] + a.margin) / 10.0) * 10)
    print()
    if not any(r["logs"] for r in rows if r["teaching"]):
        print("!! no .xapi-log rendered with teaching on — the sim is not instrumented, or its mount is wrong.")
    print(f"teaching sim:   recommend iframe height {rec}  (content {t[col]} at {col} px + {a.margin}, rounded up)")
    if 375 in t and t[375] > t[col] + 50:
        print(f"  note: at 375 px the content is {t[375]} px — {t[375] - t[col]} px taller. Size for phones "
              f"({int(math.ceil((t[375] + a.margin) / 10.0) * 10)}) only if the book's readers are mostly on phones.")
    pcol = pr.get(col, max(pr.values()))
    print(f"production sim: content {pcol} at {col} px" +
          (f" vs iframe {current}: {'fits' if pcol <= current + 2 else 'CLIPPED — grow the iframe or find what the wiring added'}"
           if current else ""))
    found = embeds(docs, sim)
    print("\nembedded by:" if found else "\nembedded by: (no iframe found)")
    for where, h in found:
        print(f"  {where:<60} height {h}")
    src = canvas_height_source(sim)
    print(f"CANVAS_HEIGHT source: {src[0]} = {src[1]}" if src else
          "CANVAS_HEIGHT source: none found (sync-iframe-heights.py would compute one from the sketch)")
    print(f"For a teaching sim: set CANVAS_HEIGHT to {rec - 2} in that source, then run\n"
          f"  python3 ~/Documents/ws/ibook-skills/src/microsim-utils/sync-iframe-heights.py "
          f"--project-dir {book} --sim {sim.name}\n"
          "so EVERY embed above gets it, and a later sync cannot shrink it back.")
    if any(r["overflow_x"] > 4 for r in rows):
        print("!! horizontal overflow — find the widest element; the usual cause is a flex or column-wrap "
              "panel sized by an unwrapped log line (references/pitfalls.md)")
    if a.json:
        a.json.write_text(json.dumps({"sim": rel, "iframe": current, "rows": rows, "recommend_teaching": rec}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

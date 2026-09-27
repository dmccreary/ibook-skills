#!/usr/bin/env python3
"""Headless contract check of an instrumented MicroSim: Full, Compact, and production modes.

Generalized from learning-record-store/tests/test_microsim_compact_xapi.py. Serves the
book's docs/ from a throwaway local server, embeds the sim in an iframe the way the book
embeds it, rewrites its metadata.json `xapi` block in flight (the committed files are never
touched), drives interactions, flushes with a hidden-tab event, and checks every statement
against the producer contract and the sim's recorded concept map.

Run with Playwright (needs network for CDN libraries):

    uv run --with playwright==1.58.0 python check-xapi.py docs/sims/<name>
    uv run --with playwright==1.58.0 python check-xapi.py docs/sims/<name> --actions actions.json
    options: --modes full,compact,production   --generic (also run generic driving with --actions)
             --json report.json   --width 900   --timeout 20   --show-statements   --verbose

MODES
  full        metadata xapi -> {compact:false, teaching:true}; every interaction a statement
  compact     metadata xapi -> {compact:true,  teaching:true}; silent until the flush, then ONE summary
              (answers still pass through as they happen)
  production  metadata xapi -> {teaching:false}, compact from the book; no teaching UI at all
  url         production metadata, embedded at the sim's real index.md iframe height, with
              ?xapi=teaching on the embedding page: the panel must appear and must fit
              (the runtime grows the iframe; a vh/100%-height layout can defeat that)
  The sim's own `concept`/`objects` keys are kept. Focus-loss timers are set long so only
  the explicit flush ends a session.

DRIVING
  Without --actions, generic driving: every input[type=range] swept (input events, then
  change), every <select> set to up to three options, every checkbox clicked twice, every
  visible button clicked twice 400 ms apart (Start/Pause gets a real run). Controls inside
  the xAPI panel are skipped. With --actions FILE, only the listed actions run (add
  --generic to run both, actions first). An actions file is a JSON list:

    {"wait": 400}                                   milliseconds
    {"wait_for": ".mermaid .node"}                  selector appears in the sim frame
    {"wait_for_js": "typeof sim !== 'undefined'"}   expression becomes truthy in the sim frame
    {"click": "button", "text": "Start", "nth": 0}  real mouse click; text filters, nth picks
    {"hover": ".mermaid .node", "nth": 2, "ms": 800}  hover, dwell, then move the mouse off the sim
    {"slider": "input[type=range]", "nth": 0, "values": [5, 7, 9]}   input events, then change
    {"select": "select", "nth": 0, "option": "Kafka"}  by label (or "value": "...")
    {"check": "input[type=checkbox]", "nth": 0}     click a checkbox
    {"type": "input[type=text]", "nth": 0, "value": "abc", "then": "blur"}   real keystrokes, then
                                                    "blur" (default), "Enter", or null to stay in the box
    {"click_at": [x, y], "on": "canvas"}            click at an offset from the element's top-left;
    {"click_at": "<js expr returning [x, y]>", "on": "#chart"}   the offset may be computed in the frame
    {"hover_at": [x, y], "on": "canvas", "ms": 800}
    {"hover_at": [x, y], "on": "canvas", "ms": 800, "leave": false}   stay put, so a following
                                                    click_at at the same point is the SAME visit
    {"drag": [[x1, y1], [x2, y2]], "on": "canvas", "steps": 12}
    {"wheel": ".vis-timeline", "delta": -400}        mouse wheel over an element
    {"key": "ArrowRight"}
    {"eval": "sim.markers.get(sim.data.callouts[0].id).click()"}   any expression in the sim frame

  Selectors never match inside the teaching panel (in teaching modes it sits in #xapi-slot,
  which comes BEFORE p5-created controls in the DOM, so "button" nth 0 would otherwise be the
  panel's own control). Add "panel": true to an action to target the panel deliberately.

Exit status: 0 all checks pass (warnings allowed), 1 any FAIL, 2 setup error.
"""

from __future__ import annotations

import argparse
import csv
import functools
import http.server
import json
import re
import sys
import threading
from pathlib import Path
from typing import Any

VERBS = {
    "http://adlnet.gov/expapi/verbs/answered": "answered",
    "http://adlnet.gov/expapi/verbs/experienced": "experienced",
    "http://adlnet.gov/expapi/verbs/interacted": "interacted",
}
TYPES = {
    "http://adlnet.gov/expapi/activities/lesson": "Page",
    "http://adlnet.gov/expapi/activities/simulation": "MicroSim",
    "http://adlnet.gov/expapi/activities/cmi.interaction": "Question",
    "http://adlnet.gov/expapi/activities/interaction": "Control",
}
VERB_TYPES = {"answered": {"Question"}, "experienced": {"MicroSim", "Page"}, "interacted": {"Control"}}
EXT = "https://w3id.org/lrs/ext/"
LONG = {"idleMs": 3_600_000, "offscreenMs": 3_600_000, "blurMs": 3_600_000}

HIDE_TAB = """() => {
  Object.defineProperty(document, 'visibilityState', {configurable: true, get: () => 'hidden'});
  document.dispatchEvent(new Event('visibilitychange'));
}"""

SET_SLIDER = """([el, values]) => {
  for (const v of values) { el.value = String(v); el.dispatchEvent(new Event('input', {bubbles: true})); }
  el.dispatchEvent(new Event('change', {bubbles: true}));
}"""

IN_PANEL = "el => !!(el.closest && el.closest('.xapi-panel'))"
# Every element outside the teaching panel; action selectors are intersected with it (Locator.and_).
NOT_IN_PANEL = ("xpath=//*[not(ancestor-or-self::*[contains(concat(' ', normalize-space(@class), ' '),"
                " ' xapi-panel ')])]")


# ------------------------------------------------------------------------------ setup ----

def find_book_root(start: Path) -> Path:
    d = start.resolve()
    while d != d.parent:
        if (d / "mkdocs.yml").is_file():
            return d
        d = d.parent
    sys.exit(f"no mkdocs.yml above {start}")


def read_config(docs: Path) -> dict[str, str]:
    cfg = docs / "js" / "lrs-config.js"
    if not cfg.is_file():
        sys.exit(f"{cfg} missing — run install-runtime.py first")
    text = cfg.read_text()
    out = {}
    for k in ("siteUrl", "textbookId", "version", "conceptPrefix"):
        m = re.search(k + r"\s*:\s*['\"]([^'\"]*)['\"]", text)
        out[k] = m.group(1) if m else ""
    if out["siteUrl"] and not out["siteUrl"].endswith("/"):
        out["siteUrl"] += "/"
    return out


def iframe_height(sim: Path) -> int | None:
    """The height of the iframe the sim's own index.md embeds it with."""
    idx = sim / "index.md"
    if not idx.is_file():
        return None
    m = re.search(r"<iframe[^>]*src=['\"](\./)?main\.html['\"][^>]*>", idx.read_text(errors="replace"))
    if not m:
        return None
    h = re.search(r"height=['\"]?(\d+)", m.group(0)) or re.search(r"height:\s*(\d+)px", m.group(0))
    return int(h.group(1)) if h else None


def graph_ids(docs: Path) -> set[str] | None:
    p = docs / "learning-graph" / "learning-graph.csv"
    if not p.is_file():
        return None
    with p.open(newline="", encoding="utf-8", errors="replace") as f:
        return {(r.get("ConceptID") or "").strip() for r in csv.DictReader(f)} - {""}


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        pass

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")   # never test yesterday's shared JS
        super().end_headers()


# ------------------------------------------------------------------------------ driving ----

class Driver:
    def __init__(self, page: Any, frame: Any, timeout_ms: int) -> None:
        self.page, self.frame, self.timeout = page, frame, timeout_ms
        self.log: list[str] = []

    def _loc(self, sel: str, text: str | None = None, nth: int = 0, panel: bool = False) -> Any:
        loc = self.frame.locator(sel)
        if not panel:
            loc = loc.and_(self.frame.locator(NOT_IN_PANEL))
        if text:
            loc = loc.filter(has_text=text)
        return loc.nth(nth)

    def _off(self) -> None:
        # Outside the iframe (it is 900 px wide at x=0): the sim sees mouseleave.
        self.page.mouse.move(980, 5)

    def _offset(self, spec: Any, on: str) -> tuple[float, float]:
        box = self.frame.locator(on).first.bounding_box()
        if box is None:
            raise RuntimeError(f"element {on!r} is not visible")
        xy = self.frame.evaluate(spec) if isinstance(spec, str) else spec
        return box["x"] + float(xy[0]), box["y"] + float(xy[1])

    def action(self, a: dict[str, Any]) -> None:
        f, pg, t = self.frame, self.page, self.timeout
        nth = int(a.get("nth", 0))
        panel = bool(a.get("panel", False))
        if "wait" in a:
            f.wait_for_timeout(int(a["wait"]))
        elif "wait_for" in a:
            f.wait_for_selector(a["wait_for"], timeout=t)
        elif "wait_for_js" in a:
            f.wait_for_function(a["wait_for_js"], timeout=t)
        elif "eval" in a:
            f.evaluate(a["eval"])
        elif "click" in a:
            self._loc(a["click"], a.get("text"), nth, panel).click(timeout=t)
        elif "check" in a:
            self._loc(a["check"], a.get("text"), nth, panel).click(timeout=t)
        elif "hover" in a:
            self._loc(a["hover"], a.get("text"), nth, panel).hover(timeout=t)
            f.wait_for_timeout(int(a.get("ms", 800)))
            if a.get("leave", True):
                self._off()
        elif "slider" in a:
            el = self._loc(a["slider"], None, nth, panel).element_handle(timeout=t)
            f.evaluate(SET_SLIDER, [el, a["values"]])
        elif "select" in a:
            loc = self._loc(a["select"], None, nth, panel)
            if "option" in a:
                loc.select_option(label=a["option"], timeout=t)
            else:
                loc.select_option(value=a["value"], timeout=t)
        elif "type" in a:
            # Real keystrokes, so the sim's own input handlers fire per character. Then commit
            # the way a student does: leaving the box (blur) or Enter; both fire `change`.
            loc = self._loc(a["type"], None, nth, panel)
            loc.click(timeout=t)
            loc.press_sequentially(str(a.get("value", "")), delay=20, timeout=t)
            then = a.get("then", "blur")
            if then == "blur":
                loc.blur(timeout=t)
            elif then:
                loc.press(str(then), timeout=t)
        elif "click_at" in a:
            x, y = self._offset(a["click_at"], a.get("on", "canvas"))
            pg.mouse.click(x, y)
        elif "hover_at" in a:
            x, y = self._offset(a["hover_at"], a.get("on", "canvas"))
            pg.mouse.move(x, y)
            f.wait_for_timeout(int(a.get("ms", 800)))
            if a.get("leave", True):
                self._off()
        elif "drag" in a:
            (x1, y1), (x2, y2) = a["drag"]
            sx, sy = self._offset([x1, y1], a.get("on", "canvas"))
            ex, ey = self._offset([x2, y2], a.get("on", "canvas"))
            pg.mouse.move(sx, sy)
            pg.mouse.down()
            pg.mouse.move(ex, ey, steps=int(a.get("steps", 10)))
            pg.mouse.up()
        elif "wheel" in a:
            self._loc(a["wheel"], None, nth).hover(timeout=t)
            pg.mouse.wheel(0, float(a.get("delta", -300)))
            f.wait_for_timeout(300)
        elif "key" in a:
            pg.keyboard.press(a["key"])
        else:
            raise ValueError(f"unknown action {a}")
        self.log.append(json.dumps(a))

    def generic(self) -> None:
        f = self.frame
        for i in range(f.locator("input[type=range]").count()):
            el = f.locator("input[type=range]").nth(i)
            if el.evaluate(IN_PANEL):
                continue
            lo, hi = (float(el.evaluate(f"e => parseFloat(e.{k}) || {d}")) for k, d in (("min", 0), ("max", 100)))
            vals = [lo + (hi - lo) * fr for fr in (0.2, 0.4, 0.6, 0.8, 0.5)]
            f.evaluate(SET_SLIDER, [el.element_handle(), vals])
            self.log.append(f"generic: slider #{i} swept {vals[0]:.3g}..{vals[3]:.3g}..{vals[4]:.3g}")
        for i in range(f.locator("select").count()):
            el = f.locator("select").nth(i)
            if el.evaluate(IN_PANEL) or not el.is_visible():
                continue
            values = el.evaluate("e => [...e.options].map(o => o.value)")
            for v in values[1:4]:
                el.select_option(value=v)
                f.wait_for_timeout(150)
            self.log.append(f"generic: select #{i} -> {values[1:4]}")
        for i in range(f.locator("input[type=checkbox]").count()):
            el = f.locator("input[type=checkbox]").nth(i)
            if el.evaluate(IN_PANEL) or not el.is_visible():
                continue
            el.click()
            f.wait_for_timeout(300)
            el.click()
            self.log.append(f"generic: checkbox #{i} x2")
        for i in range(f.locator("button").count()):
            el = f.locator("button").nth(i)
            if el.evaluate(IN_PANEL) or not el.is_visible() or el.is_disabled():
                continue
            label = (el.inner_text() or "").strip()[:30]
            el.click()
            f.wait_for_timeout(400)
            if el.is_visible() and not el.is_disabled():
                el.click()
            f.wait_for_timeout(200)
            self.log.append(f"generic: button #{i} {label!r} x2")


# ------------------------------------------------------------------------------ checks ----

class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def add(self, status: str, name: str, detail: str = "") -> None:
        self.rows.append((status, name, detail))

    def ok(self, cond: bool, name: str, fail_detail: str, pass_detail: str = "", warn: bool = False) -> None:
        self.add("PASS" if cond else ("WARN" if warn else "FAIL"), name, pass_detail if cond else fail_detail)

    @property
    def failed(self) -> bool:
        return any(s == "FAIL" for s, _, _ in self.rows)


def verb(st: dict[str, Any]) -> str:
    return VERBS.get(st.get("verb", {}).get("id", ""), st.get("verb", {}).get("id", "?"))


def otype(st: dict[str, Any]) -> str:
    t = st.get("object", {}).get("definition", {}).get("type", "")
    return TYPES.get(t, t or "?")


def concept(st: dict[str, Any]) -> str | None:
    c: str | None = st.get("context", {}).get("extensions", {}).get(EXT + "concept_id")
    return c


def frag(st: dict[str, Any]) -> str | None:
    oid = st.get("object", {}).get("id", "")
    return oid.split("#", 1)[1] if "#" in oid else None


def is_summary(st: dict[str, Any]) -> bool:
    return (st.get("result", {}).get("extensions", {}) or {}).get(EXT + "xapi_mode") == "compact"


def check_shapes(rep: Report, sts: list[dict[str, Any]], mode: str, cfg: dict[str, str],
                 page_iri: str, gids: set[str] | None, xmeta: dict[str, Any]) -> None:
    tag = f"[{mode}] "
    bad_verbs = sorted({verb(s) for s in sts if verb(s) not in VERB_TYPES})
    rep.ok(not bad_verbs, tag + "only the three v1 verbs", f"found {bad_verbs}")

    iri_problems = []
    for s in sts:
        oid = s.get("object", {}).get("id", "")
        base = oid.split("#", 1)[0]
        if not oid.startswith(cfg["siteUrl"]):
            iri_problems.append(f"{oid} does not start with siteUrl {cfg['siteUrl']}")
        if "main.html" in oid or "localhost" in oid or "127.0.0.1" in oid:
            iri_problems.append(f"{oid} names the payload or a local origin")
        if base != page_iri:
            iri_problems.append(f"{oid}: page part is not {page_iri}")
    rep.ok(not iri_problems, tag + "object IRIs (§1)", "; ".join(sorted(set(iri_problems))[:5]))

    type_problems = []
    for s in sts:
        v, t, fr = verb(s), otype(s), frag(s)
        if v in VERB_TYPES and t not in VERB_TYPES[v]:
            type_problems.append(f"{v} on a {t} ({s['object']['id']})")
        if fr is not None and t in ("MicroSim", "Page"):
            type_problems.append(f"fragment IRI typed {t}: {s['object']['id']}")
        if fr is None and t in ("Control", "Question"):
            type_problems.append(f"{t} without a fragment: {s['object']['id']}")
    rep.ok(not type_problems, tag + "verb/type pairing (§3, §5)", "; ".join(sorted(set(type_problems))[:5]))

    want = f"{cfg['siteUrl']}textbook/{cfg['textbookId']}/{cfg['version']}"
    bad_grp = [s["object"]["id"] for s in sts
               if s.get("context", {}).get("contextActivities", {}).get("grouping") != [{"id": want}]]
    rep.ok(not bad_grp, tag + "grouping[0] = textbook version (§4)", f"{len(bad_grp)} statement(s) lack {want}")

    res_problems = []
    for s in sts:
        r = s.get("result") or {}
        if verb(s) == "answered" and not isinstance(r.get("success"), bool):
            res_problems.append(f"answered without boolean success: {s['object']['id']}")
        if verb(s) == "experienced" and not str(r.get("duration", "")).startswith("PT"):
            res_problems.append(f"experienced without duration: {s['object']['id']}")
        if verb(s) == "answered" or otype(s) == "Control":
            parent = s.get("context", {}).get("contextActivities", {}).get("parent")
            if parent != [{"id": page_iri}]:
                res_problems.append(f"missing parent=page on {s['object']['id']}")
    rep.ok(not res_problems, tag + "required result fields and parent (§3, §4)", "; ".join(sorted(set(res_problems))[:5]))

    frag_problems = []
    otype_by_frag = {frag(s): otype(s) for s in sts if frag(s)}
    for fr in sorted({f for f in (frag(s) for s in sts) if f}):
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", fr):
            frag_problems.append(f"#{fr} is not a slug")
        # A generic word plus a small ordinal is a position; `year-2018` or `point-2018` names a label.
        elif re.fullmatch(r"(node|item|button|btn|slider|control|point|element|q)-?\d{1,2}", fr) \
                and not (otype_by_frag.get(fr) == "Question" and fr.startswith("q")):
            frag_problems.append(f"#{fr} looks positional — name it for what it is (§2)")
    for s in sts:
        fr = frag(s)
        if otype(s) == "Question" and fr and not re.fullmatch(r"q(\d+|-[a-z0-9-]+)", fr):
            frag_problems.append(f"question #{fr} should be #q{{N}} (fixed order) or #q-{{name}} (§2)")
    rep.ok(not frag_problems, tag + "stable fragment names (§2)", "; ".join(sorted(set(frag_problems))[:6]), warn=True)

    missing = sorted({s["object"]["id"].replace(cfg["siteUrl"], "…/") for s in sts if not concept(s)})
    rep.ok(not missing, tag + "concept_id on every statement (§6)",
           "no concept on: " + ", ".join(missing[:8]) + " — reaches no concept rollup; intended?", warn=True)

    prefix = cfg["conceptPrefix"] + "-"
    wrong, foreign = [], []
    for c in sorted({c for c in (concept(s) for s in sts) if c}):
        if c.startswith(prefix):
            num = c[len(prefix):]
            if gids is not None and num not in gids:
                wrong.append(c)
        else:
            foreign.append(c)
    rep.ok(not wrong, tag + "namespaced concept ids exist in the learning graph",
           f"not in learning-graph.csv: {wrong}")
    if foreign:
        rep.add("WARN", tag + "concept ids are namespaced",
                f"not '{prefix}N' form: {foreign} — fine only for deliberately illustrative demo sims")

    objs = xmeta.get("objects")
    page_c = xmeta.get("concept")
    if not isinstance(objs, dict) and not page_c:
        rep.add("WARN", tag + "concept map recorded in metadata.json",
                "no xapi.concept / xapi.objects — record the map (references/concept-mapping.md)")
        return
    mism, unlisted = [], []
    for s in sts:
        fr, c = frag(s), concept(s)
        if fr is None:
            if page_c and c != page_c:
                mism.append(f"page statement concept {c!r} != xapi.concept {page_c!r}")
        elif isinstance(objs, dict):
            if fr not in objs:
                if c:
                    unlisted.append(fr)
            elif objs[fr] != c:
                mism.append(f"#{fr}: emitted {c!r}, metadata says {objs[fr]!r}")
    rep.ok(not mism, tag + "emitted concepts match metadata.json map", "; ".join(sorted(set(mism))[:6]))
    if unlisted:
        rep.add("WARN", tag + "every emitted key is in xapi.objects", f"not listed: {sorted(set(unlisted))}")


# ------------------------------------------------------------------------------ main ----

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sim", type=Path)
    ap.add_argument("--actions", type=Path)
    ap.add_argument("--generic", action="store_true", help="with --actions, also run generic driving")
    ap.add_argument("--modes", default="full,compact,production,url")
    ap.add_argument("--width", type=int, default=900)
    ap.add_argument("--timeout", type=int, default=20, help="seconds for waits")
    ap.add_argument("--json", type=Path, help="write the full report, statements included")
    ap.add_argument("--show-statements", action="store_true")
    ap.add_argument("--verbose", action="store_true", help="list passing checks too")
    a = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright missing. Run: uv run --with playwright==1.58.0 python check-xapi.py ...")
        return 2

    sim = a.sim.resolve()
    if not (sim / "main.html").is_file():
        print(f"no main.html in {sim}")
        return 2
    book = find_book_root(sim)
    docs = book / "docs"
    rel = sim.relative_to(docs.resolve()).as_posix()
    cfg = read_config(docs)
    page_iri = cfg["siteUrl"] + rel + "/"
    gids = graph_ids(docs)
    meta_path = sim / "metadata.json"
    meta: dict[str, Any] = json.loads(meta_path.read_text()) if meta_path.is_file() else {}
    xmeta = meta.get("xapi") if isinstance(meta.get("xapi"), dict) else {}
    actions = json.loads(a.actions.read_text()) if a.actions else None
    modes = [m.strip() for m in a.modes.split(",") if m.strip()]
    timeout = a.timeout * 1000

    handler = functools.partial(_Quiet, directory=str(docs))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"

    rep = Report()
    results: dict[str, dict[str, Any]] = {}
    print(f"sim:      {rel}\nbook:     {book}\npage IRI: {page_iri}\nconfig:   {cfg}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for mode in modes:
            block = {k: v for k, v in xmeta.items()
                     if k not in ("compact", "teaching", "idleMs", "offscreenMs", "blurMs")}
            block.update(LONG)
            if mode == "full":
                block.update(compact=False, teaching=True)
            elif mode == "compact":
                block.update(compact=True, teaching=True)
            else:                                   # production, and url (production + ?xapi=teaching)
                block.update(teaching=False)
            # The url mode embeds the sim at its REAL index.md iframe height, because what it
            # checks is that the switched-on panel is not clipped there.
            frame_h = (iframe_height(sim) or 600) if mode == "url" else 1300
            query = "?xapi=teaching" if mode == "url" else ""

            ctx = browser.new_context(viewport={"width": 1000, "height": 1400})
            page = ctx.new_page()
            console: list[str] = []
            errors: list[str] = []
            page.on("console", lambda m, c=console: c.append(f"{m.type}: {m.text}"))
            page.on("pageerror", lambda e, er=errors: er.append(str(e)))

            def rewriter(block: dict[str, Any]) -> Any:
                # A factory, not a default argument: Playwright passes (route, request) to a
                # two-parameter handler, which would silently replace the block.
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
            host = ('<!doctype html><body style="margin:0">'
                    f'<iframe id="sim" src="/{rel}/main.html" '
                    f'style="width:{a.width}px;height:{frame_h}px;border:0"></iframe>'
                    '<div style="height:4000px"></div></body>')
            def serve_host(body: str) -> Any:   # a factory, for the same (route, request) reason
                return lambda route: route.fulfill(content_type="text/html", body=body)

            page.route("**/__lrs_check_host__.html*", serve_host(host))
            page.goto(f"{base}/__lrs_check_host__.html{query}")
            frame = page.locator("iframe#sim").element_handle().content_frame()
            r: dict[str, Any] = {"mode": mode, "console": console, "errors": errors}
            results[mode] = r
            try:
                frame.wait_for_function("window.LRSLite && document.documentElement.dataset.xapiMode",
                                        timeout=timeout)
            except Exception:
                rep.add("FAIL", f"[{mode}] runtime loaded",
                        "LRSLite never resolved a policy — is the script block in main.html, in order?")
                ctx.close()
                continue
            frame.wait_for_timeout(1000)                         # let the sim finish its own setup
            r["at_load"] = frame.evaluate("LRSLite.statements")
            d = Driver(page, frame, timeout)
            try:
                if actions:
                    for act in actions:
                        d.action(act)
                if not actions or a.generic:
                    d.generic()
            except Exception as e:                                # noqa: BLE001 — report, don't crash
                rep.add("FAIL", f"[{mode}] driving", f"{type(e).__name__}: {e} after {len(d.log)} action(s)")
            r["driven"] = d.log
            frame.wait_for_timeout(300)
            r["pre_flush"] = frame.evaluate("LRSLite.statements")
            r["overflow"] = frame.evaluate(
                "document.documentElement.scrollWidth - document.documentElement.clientWidth")
            # The runtime's teaching panel is the .xapi-panel holding a .xapi-log. A sim may reuse
            # the class for its own UI (sine-wave's MicroSim Summary box), which is not teaching UI.
            r["panel"] = frame.locator(".xapi-panel .xapi-log").count()
            r["radios"] = frame.locator(".xapi-controls input[type=radio]").count()
            r["frame_h"] = page.evaluate("document.querySelector('iframe#sim').clientHeight")
            r["panel_bottom"] = frame.evaluate(
                "(() => { const l = document.querySelector('.xapi-panel .xapi-log'); if (!l) return null;"
                " const p = l.closest('.xapi-panel'); return Math.ceil(p.getBoundingClientRect().bottom + scrollY); })()")
            frame.evaluate(HIDE_TAB)
            frame.wait_for_timeout(400)
            r["post_flush"] = frame.evaluate("LRSLite.statements")
            ctx.close()
        browser.close()
    server.shutdown()

    # --- per-mode checks ---
    for mode, r in results.items():
        tag = f"[{mode}] "
        if "post_flush" not in r:
            continue
        rep.ok(not r["errors"], tag + "no uncaught page errors", "; ".join(r["errors"][:3]))
        contract = [c for c in r["console"] if "[lrs-xapi]" in c or "[lrs-lite-sim]" in c]
        rep.ok(not contract, tag + "no runtime contract warnings", "; ".join(contract[:3]))
        unmapped = [c for c in r["console"] if "no concept" in c.lower()]
        if unmapped:
            rep.add("WARN", tag + "adapter reported unmapped objects", "; ".join(unmapped[:3]))
        rep.ok(not r["at_load"], tag + "nothing emitted before any interaction",
               f"{len(r['at_load'])} statement(s) at load — does the sim auto-run?", warn=True)
        rep.ok(r["overflow"] <= 4, tag + "no horizontal overflow",
               f"page is {r['overflow']} px wider than the frame — find the widest element (usual cause: a flex or column-wrap panel sized by an unwrapped log line)", warn=True)
        if mode in ("full", "compact"):
            rep.ok(r["panel"] >= 1, tag + "teaching panel rendered",
                   "no statement log with teaching:true — is `mount` right, and is LRSSim.create reached?", warn=True)
        check_shapes(rep, r["post_flush"], mode, cfg, page_iri, gids, xmeta)

    full, comp, prod = results.get("full"), results.get("compact"), results.get("production")
    if full and "post_flush" in full:
        sts = full["post_flush"]
        evidence = [s for s in sts if verb(s) in ("interacted", "answered")
                    or (verb(s) == "experienced" and (s.get("result", {}).get("extensions") or {})
                        .get(EXT + "run-ended-by") == "paused")]
        rep.ok(bool(evidence), "[full] driving reached the wiring (positive control)",
               f"{len(sts)} statement(s), none from an interaction — fix the drive or the wiring before "
               "trusting anything else")
        rep.ok(not any(is_summary(s) for s in sts), "[full] no compact summaries in Full mode",
               "a summary appeared in Full mode")
    if comp and "post_flush" in comp:
        pre, post = comp["pre_flush"], comp["post_flush"]
        leaked = [verb(s) for s in pre if verb(s) != "answered"]
        rep.ok(not leaked, "[compact] silent until focus loss (answers excepted)",
               f"emitted before the flush: {leaked}")
        new = post[len(pre):]
        summaries = [s for s in new if is_summary(s)]
        others = [verb(s) for s in new if not is_summary(s)]
        if full and "post_flush" in full and any(verb(s) != "answered" for s in full["post_flush"]):
            rep.ok(len(summaries) == 1, "[compact] exactly one summary on focus loss",
                   f"{len(summaries)} summaries after the flush")
        rep.ok(not others, "[compact] the flush emits only the summary", f"also emitted: {others}")
        for s in summaries:
            ctx_ext = s.get("context", {}).get("extensions", {})
            rep_n = ctx_ext.get(EXT + "statements_represented")
            ext = s.get("result", {}).get("extensions", {})
            rep.ok(isinstance(rep_n, int) and rep_n >= 1, "[compact] summary carries statements_represented",
                   f"statements_represented = {rep_n!r}")
            rep.ok(s["object"]["id"] == page_iri and otype(s) == "MicroSim",
                   "[compact] summary object is the page, typed MicroSim", s["object"]["id"])
            rep.ok(bool(ext.get(EXT + "end_reason")), "[compact] summary carries end_reason", "missing")
            comp["represented"] = rep_n
        n_full_ans = sum(verb(s) == "answered" for s in full["post_flush"]) if full and "post_flush" in full else 0
        n_comp_ans = sum(verb(s) == "answered" for s in post)
        if n_full_ans:
            rep.ok(n_comp_ans > 0, "[compact] answers pass through, never folded",
                   f"Full emitted {n_full_ans} answer(s), Compact emitted none")
            if n_comp_ans and n_comp_ans != n_full_ans:
                rep.add("WARN", "[compact] same number of answers as Full",
                        f"Full {n_full_ans} vs Compact {n_comp_ans} — driving may be nondeterministic")
        if full and "post_flush" in full and comp.get("represented") is not None:
            f_sts = full["post_flush"]
            n = sum(verb(s) == "interacted" for s in f_sts) + sum(
                verb(s) == "experienced" and not is_summary(s) for s in f_sts)
            if comp["represented"] not in (n, n - 1):
                rep.add("WARN", "[compact] statements_represented ≈ Full's exposure statements",
                        f"represented {comp['represented']} vs Full interacted+experienced {n} "
                        "(page dwell counts once in Full only; hover timing can differ)")
    url = results.get("url")
    if url and "post_flush" in url:
        rep.ok(url["panel"] >= 1, "[url] ?xapi=teaching turns the production sim into a teaching aid",
               "no statement log appeared — is the runtime current (install-runtime.py --check)?")
        if url["panel"] >= 1 and url["panel_bottom"] is not None:
            rep.ok(url["frame_h"] >= url["panel_bottom"], "[url] the switched-on panel fits its iframe",
                   f"panel ends at {url['panel_bottom']} px but the iframe is {url['frame_h']} px — a layout "
                   "sized in vh/100% grows with its frame; pin it when the panel is present "
                   "(body:has(> .xapi-panel) … { height: <px> })")
    if prod and "post_flush" in prod:
        rep.ok(prod["panel"] == 0 and prod["radios"] == 0, "[production] no teaching UI",
               f"{prod['panel']} statement log(s) / {prod['radios']} mode radio(s) rendered with teaching:false")
        rep.ok(len(prod["post_flush"]) >= 1, "[production] still records statements",
               "nothing recorded with teaching:false", warn=True)

    # --- output ---
    for mode, r in results.items():
        if "post_flush" in r:
            vs = [verb(s) + ("(summary)" if is_summary(s) else "") for s in r["post_flush"]]
            print(f"{mode:<11} driven {len(r.get('driven', []))} step(s); statements: {len(vs)}  {vs[:14]}"
                  f"{' …' if len(vs) > 14 else ''}")
            if a.show_statements:
                for s in r["post_flush"]:
                    print("    " + json.dumps({"verb": verb(s), "object": s["object"]["id"],
                                               "concept": concept(s), "result": s.get("result")})[:300])
    print()
    # Merge the same check across modes: "[full] x" + "[compact] x" -> "x  (full, compact)".
    merged: dict[tuple[str, str, str], list[str]] = {}
    for status, name, detail in rep.rows:
        m = re.match(r"\[(\w+)\] (.*)", name)
        mode_tag, bare = (m.group(1), m.group(2)) if m else ("", name)
        merged.setdefault((status, bare, detail if status != "PASS" else ""), []).append(mode_tag)
    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    width = max((len(k[1]) for k in merged), default=20)
    for (status, bare, detail), tags in sorted(merged.items(), key=lambda kv: order[kv[0][0]]):
        if status == "PASS" and not a.verbose:
            continue
        mark = {"PASS": "  ok ", "WARN": " WARN", "FAIL": " FAIL"}[status]
        where = f"({', '.join(t for t in tags if t)})"
        print(f"{mark}  {bare:<{width}}  {where:<30} {detail}")
    n = {s: sum(1 for x, _, _ in rep.rows if x == s) for s in ("PASS", "WARN", "FAIL")}
    print(f"\n{n['PASS']} passed, {n['WARN']} warnings, {n['FAIL']} failed"
          + ("" if a.verbose else "   (--verbose lists the passes)"))

    if a.json:
        a.json.write_text(json.dumps({"sim": rel, "page_iri": page_iri, "config": cfg,
                                      "checks": [{"status": s, "check": c, "detail": d} for s, c, d in rep.rows],
                                      "modes": results}, indent=2, default=str))
        print(f"report: {a.json}")
    return 1 if rep.failed else 0


if __name__ == "__main__":
    sys.exit(main())

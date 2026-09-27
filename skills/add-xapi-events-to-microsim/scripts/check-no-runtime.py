#!/usr/bin/env python3
"""Check that instrumented MicroSims still run WITHOUT the xAPI runtime.

A teacher pastes a p5 sketch into the p5.js editor, where lrs-config.js, lrs-xapi.js,
lrs-lite-sim.js, lrs-sim.js and xapi-json-viewer.js don't exist. Every call site must be guarded
(`if (lrs)`, `if (window.LRSSim)`); one unguarded call throws and the sketch never draws. This
script loads each sim's main.html with those five scripts blocked, clicks its visible buttons,
and fails on any uncaught error, on a sim that didn't render, or on a runtime that still loaded.

Usage (needs Playwright; network for CDN libraries):
    uv run --with playwright==1.58.0 python check-no-runtime.py --book .                 # every instrumented sim
    uv run --with playwright==1.58.0 python check-no-runtime.py --book . sine-wave bouncing-ball

Exit status: 0 every sim runs without the runtime, 1 any FAIL, 2 setup error.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import sys
import threading
from pathlib import Path

RUNTIME = ["lrs-config.js", "lrs-xapi.js", "lrs-lite-sim.js", "lrs-sim.js", "xapi-json-viewer.js"]
# What counts as "the sim rendered", by library: a p5/Chart.js canvas, a vis-network or
# vis-timeline root, a Mermaid SVG, a Plotly plot, a Leaflet map, or an image overlay.
RENDERED = ("() => !!document.querySelector('canvas, .vis-timeline, .vis-network, .mermaid svg,"
            " .js-plotly-plot, .leaflet-container, img')")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--book", type=Path, default=Path("."), help="book root (contains mkdocs.yml)")
    ap.add_argument("sims", nargs="*", help="sim names under docs/sims (default: every sim that loads lrs-sim.js)")
    ap.add_argument("--clicks", type=int, default=8, help="visible buttons to click per sim")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright missing: uv run --with playwright==1.58.0 python check-no-runtime.py ...")
        return 2

    docs = (args.book / "docs").resolve()
    if not docs.is_dir():
        print(f"no docs/ under {args.book}")
        return 2
    sims = args.sims or sorted(p.parent.name for p in docs.glob("sims/*/main.html")
                               if "lrs-sim.js" in p.read_text(errors="replace"))
    if not sims:
        print("no instrumented sims found (none of docs/sims/*/main.html loads lrs-sim.js)")
        return 2

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a: object) -> None:
            pass

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(docs)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"

    fails = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for sim in sims:
            ctx = browser.new_context(viewport={"width": 900, "height": 1000})
            page = ctx.new_page()
            errors: list[str] = []
            blocked: list[str] = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("console", lambda m: errors.append("console.error: " + m.text) if m.type == "error" else None)

            # One parameter only: Playwright passes (route, request) to a two-parameter handler,
            # so a `blocked=blocked` default would be overwritten and the route never released.
            def block(route):
                blocked.append(route.request.url.rsplit("/", 1)[-1])
                route.abort()
            for name in RUNTIME:
                page.route(f"**/js/{name}", block)

            page.goto(f"{base}/sims/{sim}/main.html")
            page.wait_for_timeout(1500)
            rendered = page.evaluate(RENDERED)
            runtime_loaded = page.evaluate("() => typeof window.LRSSim !== 'undefined'")
            for b in page.locator("button:visible").all()[: args.clicks]:
                try:
                    b.click(timeout=1000)
                    page.wait_for_timeout(120)
                except Exception:
                    pass
            page.wait_for_timeout(300)
            # The blocked scripts' own load failures are expected console errors.
            errors = [e for e in errors if "net::ERR_FAILED" not in e and "Failed to load resource" not in e]
            ok = rendered and not errors and not runtime_loaded and blocked
            fails += not ok
            why = [] if ok else [w for w, bad in (("did not render", not rendered),
                                                   ("runtime still loaded", runtime_loaded),
                                                   ("no runtime script requested", not blocked)) if bad]
            print(f"{'ok  ' if ok else 'FAIL'} {sim:45s} blocked={len(blocked)} {'; '.join(why)}")
            for e in errors[:5]:
                print(f"       {e}")
            ctx.close()
        browser.close()
    srv.shutdown()
    print(f"\n{len(sims) - fails}/{len(sims)} sims run without the xAPI runtime")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

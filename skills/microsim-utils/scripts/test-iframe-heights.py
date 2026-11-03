#!/usr/bin/env python3
"""
MicroSim Iframe Height Tester

Uses Playwright to load each MicroSim's main.html inside a viewport
constrained to the iframe height declared in index.md, then checks
whether all interactive controls (buttons, sliders, selects, etc.)
are fully visible without clipping.

Usage:
    python test-iframe-heights.py --sims-dir docs/sims [--sim name] [--height N] [--report file.md]

Prerequisites:
    pip install playwright
    playwright install chromium
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

TOLERANCE = 1        # px — sub-pixel rounding only; a 4px clip is a real clip
# MkDocs Material content column at a 1440px laptop window with both sidebars
# (the narrowest common desktop layout). At 1024px the column is 746px.
VIEWPORT_WIDTH = 684
# iframe height = content + BORDER: Material's border-box sizing draws the
# template's `iframe { border: solid 2px blue; }` inside the height, 2px per side.
BORDER = 4
SLACK_LIMIT = 30     # px — more unused space than this below the content is flagged

CONTROL_SELECTORS = ", ".join([
    "button",
    'input[type="range"]',
    'input[type="checkbox"]',
    'input[type="text"]',
    'input[type="number"]',
    "select",
    "textarea",
    ".p5Canvas",
    "canvas",
])

# JavaScript executed in the browser to measure control positions
MEASURE_CONTROLS_JS = """
({ sel, viewportHeight, tolerance }) => {
    const elements = document.querySelectorAll(sel);
    const results = [];
    for (const el of elements) {
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 && rect.height === 0) continue;
        if (rect.height === 0) continue;
        results.push({
            tag: el.tagName.toLowerCase(),
            type: el.getAttribute('type') || '',
            label: (el.textContent || '').trim().slice(0, 30),
            top: Math.round(rect.top),
            bottom: Math.round(rect.bottom),
            isVisible: rect.bottom <= viewportHeight + tolerance,
        });
    }
    return results;
}
"""

# JavaScript to find the actual content height
MEASURE_CONTENT_JS = """
() => {
    // Scan all of <body>: p5's createButton/createSlider append controls to
    // <body>, not to <main>, so a <main>-only scan misses the control rows.
    let maxBottom = 0;
    for (const el of document.body.querySelectorAll('*')) {
        if (el.tagName === 'SCRIPT') continue;
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        const rect = el.getBoundingClientRect();
        if (rect.height > 0 && rect.width > 0 && rect.bottom > maxBottom) {
            maxBottom = rect.bottom;
        }
    }
    return Math.ceil(maxBottom);
}
"""


@dataclass
class SimResult:
    sim: str
    iframe_height: int | None
    content_height: int | None
    status: str  # PASS, FAIL, SLACK, ERROR, SKIP
    suggested_height: int | None
    clipped_elements: list[str] = field(default_factory=list)
    error: str | None = None


def extract_iframe_height(index_md: Path) -> int | None:
    """Extract the iframe height from an index.md file."""
    text = index_md.read_text()
    match = re.search(r'<iframe[^>]*\bheight="(\d+)(px)?"', text, re.IGNORECASE)
    return int(match.group(1)) if match else None


def extract_canvas_height(sim_dir: Path) -> int | None:
    """Look for a // CANVAS_HEIGHT = N comment in the sim's JS file.

    When present this is the authoritative intended height and is more
    reliable than measuring dynamic content for responsive sims whose
    canvas height scales with viewport width.
    """
    for js_file in sim_dir.glob("*.js"):
        try:
            text = js_file.read_text()
        except Exception:
            continue
        match = re.search(r'//\s*CANVAS_HEIGHT\s*[:=]\s*(\d+)', text)
        if match:
            return int(match.group(1))
    return None


def discover_sims(base_dir: Path) -> list[dict]:
    """Find MicroSim directories containing both main.html and index.md."""
    if not base_dir.is_dir():
        print(f"Sims directory not found: {base_dir}", file=sys.stderr)
        sys.exit(1)
    sims = []
    for entry in sorted(base_dir.iterdir()):
        if not entry.is_dir():
            continue
        if (entry / "main.html").exists() and (entry / "index.md").exists():
            sims.append({"name": entry.name, "dir": entry})
    return sims


def test_sim(page, sim: dict, iframe_height: int) -> SimResult:
    """Test a single MicroSim at the given iframe height."""
    html_path = sim["dir"] / "main.html"
    file_url = f"file://{html_path.resolve()}"

    # The border is drawn inside the iframe height, so the sim only sees this much.
    visible_height = iframe_height - BORDER
    page.set_viewport_size({"width": VIEWPORT_WIDTH, "height": visible_height})

    try:
        page.goto(file_url, wait_until="networkidle", timeout=15000)
    except Exception as e:
        return SimResult(
            sim=sim["name"],
            iframe_height=iframe_height,
            content_height=None,
            status="ERROR",
            suggested_height=None,
            error=f"Failed to load: {e}",
        )

    # Wait for p5.js / vis-network / Chart.js to render controls
    page.wait_for_timeout(2000)

    # Measure control positions
    measurements = page.evaluate(
        MEASURE_CONTROLS_JS,
        {"sel": CONTROL_SELECTORS, "viewportHeight": visible_height, "tolerance": TOLERANCE},
    )

    # Measure actual content height at the real content-column width. This is
    # the number CANVAS_HEIGHT should hold; a declared value that disagrees is
    # stale (self-sizing sims compute their height at runtime from the width).
    content_height = page.evaluate(MEASURE_CONTENT_JS)
    declared_height = extract_canvas_height(sim["dir"])

    clipped = [m for m in measurements if not m["isVisible"]]
    suggested = content_height + BORDER
    if clipped:
        status = "FAIL"
    elif visible_height - content_height > SLACK_LIMIT:
        status = "SLACK"
    else:
        status = "PASS"
    notes = [
        f"{c['tag']}{'[' + c['type'] + ']' if c['type'] else ''} \"{c['label']}\" bottom={c['bottom']}px"
        for c in clipped
    ]
    if declared_height and abs(declared_height - content_height) > 2:
        notes.append(f"declared CANVAS_HEIGHT {declared_height} != measured {content_height}")

    return SimResult(
        sim=sim["name"],
        iframe_height=iframe_height,
        content_height=content_height,
        status=status,
        suggested_height=suggested if status != "PASS" else iframe_height,
        clipped_elements=notes,
    )


def write_report(path: Path, results: list[SimResult], sims_dir: str):
    """Write a markdown report of the test results."""
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    errors = sum(1 for r in results if r.status == "ERROR")
    skipped = sum(1 for r in results if r.status == "SKIP")

    lines = [
        "# MicroSim Iframe Height Test Report",
        "",
        f"Tested: {datetime.now(timezone.utc).isoformat()}",
        f"Sims directory: `{sims_dir}`",
        "",
        "| MicroSim | Iframe Height | Content Height | Status | Suggested Height |",
        "|----------|---------------|----------------|--------|------------------|",
    ]

    for r in results:
        ih = r.iframe_height or "\u2014"
        ch = r.content_height or "\u2014"
        sh = r.suggested_height or "\u2014"
        st = "**FAIL**" if r.status == "FAIL" else r.status
        lines.append(f"| {r.sim} | {ih} | {ch} | {st} | {sh} |")

    failures = [r for r in results if r.status in ("FAIL", "SLACK")]
    if failures:
        lines += ["", "## Failures and Slack Detail", ""]
        for r in failures:
            lines.append(f"### {r.sim}")
            lines.append(f"- Iframe height: {r.iframe_height}px")
            lines.append(f"- Content height: {r.content_height}px")
            lines.append(f"- Suggested height: {r.suggested_height}px")
            lines.append("- Clipped elements and notes:")
            for el in r.clipped_elements:
                lines.append(f"  - {el}")
            lines.append("")

    lines += ["", f"Summary: {passed} pass, {failed} fail, {errors} error, {skipped} skip out of {len(results)} total"]
    path.write_text("\n".join(lines))
    print(f"\nReport written to {path}")


def main():
    global VIEWPORT_WIDTH, BORDER
    parser = argparse.ArgumentParser(description="Test MicroSim iframe heights with Playwright")
    parser.add_argument("--sims-dir", default="docs/sims", help="Path to sims directory")
    parser.add_argument("--sim", default=None, help="Test a single sim by name")
    parser.add_argument("--height", type=int, default=None, help="Override iframe height for all sims")
    parser.add_argument("--report", default=None, help="Write markdown report to this path")
    parser.add_argument("--width", type=int, default=None,
                        help=f"Viewport width (default {VIEWPORT_WIDTH}; also try 746 for a 1024px window)")
    parser.add_argument("--border", type=int, default=None,
                        help=f"Pixels of iframe border inside the height (default {BORDER})")
    args = parser.parse_args()

    if args.width:
        VIEWPORT_WIDTH = args.width
    if args.border is not None:
        BORDER = args.border

    sims_dir = Path(args.sims_dir)
    sims = discover_sims(sims_dir)

    if args.sim:
        sims = [s for s in sims if s["name"] == args.sim]
        if not sims:
            print(f'MicroSim "{args.sim}" not found in {sims_dir}', file=sys.stderr)
            sys.exit(1)

    print(f"Testing {len(sims)} MicroSim(s) in {sims_dir}\n")

    results: list[SimResult] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for sim in sims:
            iframe_height = args.height or extract_iframe_height(sim["dir"] / "index.md")

            if not iframe_height:
                print(f"  SKIP  {sim['name']} \u2014 no iframe height found in index.md")
                results.append(SimResult(
                    sim=sim["name"], iframe_height=None, content_height=None,
                    status="SKIP", suggested_height=None, error="No iframe height in index.md",
                ))
                continue

            print(f"  Testing {sim['name']} ({iframe_height}px)...", end="", flush=True)
            result = test_sim(page, sim, iframe_height)
            results.append(result)

            if result.status == "PASS":
                print(" PASS")
            elif result.status in ("FAIL", "SLACK"):
                print(f" {result.status} \u2014 content {result.content_height}px, suggest {result.suggested_height}px")
                for el in result.clipped_elements:
                    print(f"         {el}")
            else:
                print(f" ERROR \u2014 {result.error}")

        browser.close()

    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    errors = sum(1 for r in results if r.status == "ERROR")
    skipped = sum(1 for r in results if r.status == "SKIP")
    slack = sum(1 for r in results if r.status == "SLACK")

    print(f"\n--- Summary ---")
    print(f"  PASS: {passed}  FAIL: {failed}  SLACK: {slack}  ERROR: {errors}  SKIP: {skipped}  Total: {len(results)}")

    if args.report:
        write_report(Path(args.report), results, str(sims_dir))

    if failed > 0 or errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

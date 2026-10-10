"""
Shared utilities for MicroSim batch processing scripts.
Standard library only, Python 3.7+.
"""

import os
import re

# ── ANSI color constants ──────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

# ── Unicode symbols ───────────────────────────────────────────────────
CHECK  = "\u2714"  # ✔
CROSS  = "\u2718"  # ✘
WARN   = "\u26A0"  # ⚠
ARROW  = "\u2192"  # →
BULLET = "\u2022"  # •


# ── Spec headings in chapter markdown ─────────────────────────────────
# A MicroSim spec is a ``#### <Type>: <Title>`` heading above a
# ``<details markdown="1">`` block.  ``Diagram`` is the standard word; the
# others are all in use across existing textbooks.  ``Table``, ``Equation``
# and ``Example`` headings are deliberately absent: they never carry a spec.
# Every tool that looks for specs must use this one pattern so they agree on
# what counts.  Group 1 is the heading type, group 2 the title.
SPEC_HEADING_TYPES = (
    "Diagram", "Drawing", "MicroSim", "Timeline",
    "Chart", "Infographic", "Workflow", "Map",
)
SPEC_HEADING_RE = re.compile(
    r"^####\s+(" + "|".join(SPEC_HEADING_TYPES) + r"):\s*(.+)$", re.MULTILINE
)

# ── Spec regions ──────────────────────────────────────────────────────
# A spec owns the lines between its own heading and the next heading, and
# nothing beyond.  Every tool that looks ahead from a spec heading for its
# iframe or ``<details markdown="1">`` block must stop at ``spec_region_end``;
# a fixed line count alone lets a heading with no block of its own borrow
# the next spec's block, and with it the next spec's sim-id.
SECTION_HEADING_RE = re.compile(r"^ {0,3}#{1,4}\s+\S")
DETAILS_OPEN_RE    = re.compile(r"<details\s+markdown=[\"']1[\"']\s*>", re.IGNORECASE)
DETAILS_CLOSE_RE   = re.compile(r"</details>", re.IGNORECASE)
_ANY_DETAILS_OPEN_RE = re.compile(r"<details\b", re.IGNORECASE)
_CODE_FENCE_RE       = re.compile(r"^(```|~~~)")


def spec_region_end(lines, heading_idx, window):
    """Return the exclusive end index of the lines owned by a spec heading.

    The region starts on the line after *heading_idx* and ends at the next
    spec heading, the next level 1-4 heading, or ``heading_idx + window``,
    whichever comes first.  A ``#`` line inside a fenced code block or a
    ``<details>`` block is text, not a heading, so it does not end the
    region.  A spec heading always does, wherever it appears, because one
    spec is emitted per spec heading.
    """
    limit = min(heading_idx + window, len(lines))
    in_fence = False
    details_depth = 0
    for j in range(heading_idx + 1, limit):
        line = lines[j]
        stripped = line.strip()
        if SPEC_HEADING_RE.match(stripped):
            return j
        if _CODE_FENCE_RE.match(stripped):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if details_depth == 0 and SECTION_HEADING_RE.match(line):
            return j
        details_depth += len(_ANY_DETAILS_OPEN_RE.findall(line))
        details_depth -= len(DETAILS_CLOSE_RE.findall(line))
        details_depth = max(details_depth, 0)
    return limit


def find_project_root(start_dir=None):
    """Walk up from *start_dir* (default: cwd) to find the directory
    that contains ``mkdocs.yml``.  Returns the absolute path or raises
    ``FileNotFoundError``.
    """
    d = os.path.abspath(start_dir or os.getcwd())
    while True:
        if os.path.isfile(os.path.join(d, "mkdocs.yml")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            raise FileNotFoundError(
                "Could not find mkdocs.yml in any parent directory"
            )
        d = parent


def load_mkdocs_config(project_dir):
    """Parse a few key fields from ``mkdocs.yml`` using regex (no PyYAML).

    Returns a dict with keys: ``site_url``, ``site_name``, ``docs_dir``
    (all strings, possibly empty).
    """
    path = os.path.join(project_dir, "mkdocs.yml")
    with open(path, encoding="utf-8") as f:
        text = f.read()

    def _val(key):
        m = re.search(rf"^{key}:\s*(.+)$", text, re.MULTILINE)
        return m.group(1).strip().strip("'\"") if m else ""

    docs_dir = _val("docs_dir") or "docs"
    return {
        "site_url": _val("site_url"),
        "site_name": _val("site_name"),
        "docs_dir": docs_dir,
    }


def kebab_case(title):
    """Convert a title string to kebab-case directory name.

    >>> kebab_case("Point Line and Plane")
    'point-line-and-plane'
    >>> kebab_case("  CMDB Architecture Diagram  ")
    'cmdb-architecture-diagram'
    """
    s = title.strip().lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def parse_yaml_frontmatter(content):
    """Extract YAML frontmatter from markdown content.

    Returns a dict of key-value pairs (simple flat parsing, no nested
    structures) and the remaining content after the frontmatter block.
    """
    fm = {}
    rest = content
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if m:
        rest = content[m.end():]
        for line in m.group(1).splitlines():
            kv = line.split(":", 1)
            if len(kv) == 2:
                key = kv[0].strip()
                val = kv[1].strip().strip("'\"")
                if key and not key.startswith("#"):
                    fm[key] = val
    return fm, rest


def detect_library(html_content):
    """Detect the JavaScript library used in a ``main.html`` file.

    Scans ``<script>`` src attributes for known CDN patterns.
    Returns a library name string (e.g. ``'p5.js'``, ``'vis-network'``,
    ``'Chart.js'``) or ``'unknown'``.
    """
    mapping = [
        (r"p5(?:\.min)?\.js",         "p5.js"),
        (r"vis-network",              "vis-network"),
        (r"vis-timeline",             "vis-timeline"),
        (r"chart(?:\.min)?\.js",      "Chart.js"),
        (r"mermaid",                  "Mermaid"),
        (r"plotly",                   "Plotly"),
        (r"leaflet",                  "Leaflet"),
    ]
    lower = html_content.lower()
    for pattern, name in mapping:
        if re.search(pattern, lower):
            return name
    return "unknown"


# ── CDN mapping for scaffold generation ───────────────────────────────
LIBRARY_CDNS = {
    "p5.js":        "https://cdn.jsdelivr.net/npm/p5@1.11.10/lib/p5.js",
    "vis-network":  "https://cdn.jsdelivr.net/npm/vis-network@9.1.9/standalone/umd/vis-network.min.js",
    "vis-timeline": "https://cdn.jsdelivr.net/npm/vis-timeline@7.7.3/standalone/umd/vis-timeline-graph2d.min.js",
    "Chart.js":     "https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js",
    "Mermaid":      "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js",
    "Plotly":       "https://cdn.plot.ly/plotly-2.35.0.min.js",
    "Leaflet":      "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
}

LIBRARY_CSS = {
    "vis-timeline": "https://cdn.jsdelivr.net/npm/vis-timeline@7.7.3/styles/vis-timeline-graph2d.min.css",
    "Leaflet":      "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
}

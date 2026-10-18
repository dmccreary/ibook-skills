#!/usr/bin/env python3
"""Emit the marketplace search-link block for one part.

Purchasing guides are read by teachers who are about to spend real money, so
every part section ends with live searches they can click rather than a part
number they have to retype. Hand-writing those URLs is where typos and stale
query syntax creep in, so generate them.

Usage:
    python3 make_search_urls.py "WS2812B LED strip 60/m 5V IP20"
    python3 make_search_urls.py "Raspberry Pi Pico 2" --sites ebay,amazon,microcenter
    python3 make_search_urls.py "solderless breadboard 400 tie point" --alt "half size breadboard"

Prints a Markdown block ready to paste under a part's "### Where to buy" heading.
"""

import argparse
import re
import sys
from urllib.parse import quote_plus

# Ordered so the cheap/slow sources come first and the fast/expensive one last --
# that ordering quietly teaches the price-vs-lead-time tradeoff every time a
# teacher reads a part section.
SITES = {
    "ebay": (
        "eBay",
        lambda q, slug: f"https://www.ebay.com/sch/i.html?_nkw={quote_plus(q)}",
    ),
    "aliexpress": (
        "AliExpress",
        lambda q, slug: f"https://www.aliexpress.com/w/wholesale-{slug}.html",
    ),
    "amazon": (
        "Amazon",
        lambda q, slug: f"https://www.amazon.com/s?k={quote_plus(q)}",
    ),
    "alibaba": (
        "Alibaba",
        lambda q, slug: "https://www.alibaba.com/trade/search"
        f"?SearchText={quote_plus(q)}",
    ),
    "microcenter": (
        "Micro Center",
        lambda q, slug: "https://www.microcenter.com/search/search_results.aspx"
        f"?Ntt={quote_plus(q)}",
    ),
    "adafruit": (
        "Adafruit",
        lambda q, slug: f"https://www.adafruit.com/?q={quote_plus(q)}",
    ),
    "digikey": (
        "Digi-Key",
        lambda q, slug: "https://www.digikey.com/en/products/result"
        f"?keywords={quote_plus(q)}",
    ),
    "sparkfun": (
        "SparkFun",
        lambda q, slug: f"https://www.sparkfun.com/search/results?term={quote_plus(q)}",
    ),
}

DEFAULT_SITES = ["ebay", "aliexpress", "amazon"]


def slugify(text: str) -> str:
    """AliExpress uses a hyphenated path slug, not a query parameter."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "part"


def build(query: str, sites, alt=None) -> str:
    lines = []
    slug = slugify(query)
    for key in sites:
        if key not in SITES:
            print(f"warning: unknown site '{key}' (skipped)", file=sys.stderr)
            continue
        label, fn = SITES[key]
        lines.append(f"- [Search {label} for \"{query}\"]({fn(query, slug)})")
    if alt:
        alt_slug = slugify(alt)
        for key in sites:
            if key not in SITES:
                continue
            label, fn = SITES[key]
            lines.append(f"- [Search {label} for \"{alt}\"]({fn(alt, alt_slug)})")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("query", help="the search phrase a buyer would actually type")
    p.add_argument("--sites", default=",".join(DEFAULT_SITES),
                   help=f"comma-separated: {', '.join(SITES)} (default: {','.join(DEFAULT_SITES)})")
    p.add_argument("--alt", help="a second phrasing to also link (aliases, alternate part names)")
    args = p.parse_args()

    sites = [s.strip().lower() for s in args.sites.split(",") if s.strip()]
    print(build(args.query, sites, args.alt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

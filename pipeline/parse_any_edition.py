#!/usr/bin/env python3
"""
Parse ANY edition of the WSDOT Standard Specifications (M 41-10, 2000-2026).

    uv run --with pymupdf pipeline/parse_any_edition.py corpus/SS2000.pdf out.json

This is the WSDOT entrypoint: it is the scheme-independent engine in `parsers/engine.py`
driven by the WSDOT profile in `parsers/clusters/wsdot_hyphen.py`. The engine derives the
section tree from typography and ordering with no table of contents — see its module
docstring for why (the TOC is unusable across the 26-year archive) and how (body-font
learning, positional header stripping, longest-non-decreasing ordering). The WSDOT profile
supplies the only things that are Washington-specific: the "1-09.7" section pattern, the
book's sort order, and the division mapping.

Validated across all 17 editions: reproduces all 2,235 TOC-listed sections of the 2026
edition with zero misses, and finds ~1,000 more that WSDOT's own TOC omits (the deepest
"(2)A" level). Section counts grow smoothly from 2,132 (2000) to 3,237 (2026).

The module-level names below (`parse`, `sort_key`, `find_headings`, `is_heading_style`,
`monotonic`, `HEAD`) are the WSDOT-bound public surface, kept stable so callers and tests
need not know the engine was split out.
"""

import json
import sys

from parsers.clusters.wsdot_hyphen import HEAD, WSDOT, sort_key
from parsers.engine import find_headings as _find_headings
from parsers.engine import is_heading_style
from parsers.engine import monotonic as _monotonic
from parsers.engine import parse as _parse

__all__ = [
    "HEAD",
    "find_headings",
    "is_heading_style",
    "monotonic",
    "parse",
    "sort_key",
]


def find_headings(lines, body_style):
    """WSDOT-bound `engine.find_headings` — headings matching the "1-09.7" pattern."""
    return _find_headings(lines, body_style, HEAD)


def monotonic(marks):
    """WSDOT-bound `engine.monotonic` — ordered by the WSDOT book sort key."""
    return _monotonic(marks, WSDOT.order_key)


def parse(pdf_path):
    """Parse one WSDOT edition into a list of sections."""
    return _parse(pdf_path, WSDOT)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: parse_any_edition.py <specs.pdf> <out.json>")
    pdf_path, out_path = sys.argv[1], sys.argv[2]

    sections, body_style, bands = parse(pdf_path)
    with open(out_path, "w") as handle:
        json.dump(sections, handle, indent=1)

    vacant = sum(1 for s in sections if s["vacant"])
    chars = sum(len(s["text"]) for s in sections)
    print(
        f"{pdf_path}: {len(sections):,} sections ({vacant} vacant), {chars:,} chars "
        f"[body {body_style[0]} {body_style[1]}pt, bands {bands}] -> {out_path}"
    )


if __name__ == "__main__":
    main()

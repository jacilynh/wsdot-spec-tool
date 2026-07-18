#!/usr/bin/env python3
"""
Adversarial parse-QA probe: dump raw page text next to what the parser captured, so a reviewer
can judge whether the parse is faithful — page by page, against the actual document.

    uv run --with pymupdf python3 pipeline/qa_probe.py <slug> [profile] [n_samples]

Parses corpus/<slug>/current.pdf with the given SpecProfile (default aashto_decimal), then for
~N pages spread across the body emits: the page's raw text, and the sections the parse says
START on that page. A faithful parse means every section heading visible in a page's raw text
appears — with the right number and title — in that page's parsed sections, and pages with no
heading (mid-section) have none. Also reports the absorbed-title rate (titleless-paragraph
symptom) and the deepest nesting seen. Output is JSON for a reviewing agent to score.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fitz
from parsers.engine import parse
from parsers.registry import get_profile

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    slug = sys.argv[1]
    profile = get_profile(sys.argv[2] if len(sys.argv) > 2 else "aashto_decimal")
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 20

    pdf = os.path.join(_ROOT, "corpus", slug, "current.pdf")
    sections, body, bands = parse(pdf, profile)

    by_page = {}
    for s in sections:
        by_page.setdefault(s["page"], []).append(
            {"num": s["num"], "title": s["title"][:90], "textlen": len(s["text"])}
        )

    doc = fitz.open(pdf)
    total = doc.page_count
    start = max(1, int(total * 0.05))  # skip front matter
    pages = sorted({int(start + (total - start - 1) * i / (n - 1)) for i in range(n)})

    absorbed = sum(1 for s in sections if len(s["title"]) > 90)
    depth = max((s["num"].count(".") + s["num"].count("(") for s in sections), default=0)
    out = {
        "slug": slug,
        "profile": profile.cluster,
        "body_style": list(body),
        "total_pages": total,
        "total_sections": len(sections),
        "absorbed_title_rate": round(absorbed / len(sections), 3) if sections else 0,
        "deepest_nesting": depth,
        "samples": [
            {
                "page": p,
                "raw_text": doc[p - 1].get_text()[:1600],
                "parsed_sections_starting_here": by_page.get(p, []),
            }
            for p in pages
        ],
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

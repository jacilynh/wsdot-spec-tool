"""The FDOT dash scheme: "1-1", "2-2.1", "105-8", "334-1.2" - Florida's numbering.

Florida is the known non-AASHTO single-PDF state (docs/national/EXPANSION.md). FDOT
Standard Specifications number a Section's subsections with a DASH between the Section
number and its first subsection level, then dot-decimals below it:

    SECTION 2  (a plain divider line, not itself a numbered section)
      2-1     Prequalification of Bidders.
      2-2     Proposals.
        2-2.1   Obtaining Proposal Forms:  <body starts on the same line>
        2-2.2   Department Modifications to Contract Documents:
      2-3.1   Lump Sum Contracts:

So the addressable unit is "N-M" with optional deeper decimals ("N-M.K.L"). The bare
"SECTION N" divider carries no body of its own and has no dash, so it is skipped; the
division a subsection belongs to is derived from its Section number instead.

This differs from `aashto_decimal` only in the number grammar (a dash where AASHTO has its
first dot), so it drives the same scheme-independent engine - a new cluster, not new engine
code. Like the AASHTO books, FDOT section numbers are not stable across editions
(`stable_numbers=False`), so history must fall back to content alignment.
"""

import re

from parsers.profiles import SpecProfile

# "1-1", "2-2.1", "105-8", "334-1.2.1": a Section number, a dash, a subsection, then
# optional dot-decimals. The title, when present, shares the line (group 2).
SECTION = re.compile(r"^(\d{1,4}-\d+(?:\.\d+)*)(?:\s+(.*))?$", re.S)


def order_key(num):
    """Book order: the dash and dots are all level separators. 2-2 < 2-2.1 < 2-3 < 105-8."""
    return tuple(int(part) for part in num.replace("-", ".").split("."))


def division_of(num):
    """Division band from the Section number (the part before the dash): FDOT's Division I
    is Sections 1-9 (band 0); Construction Details and Materials fall on hundred bands."""
    return int(num.split("-")[0]) // 100 * 100


FLORIDA = SpecProfile(
    cluster="florida_dash",
    section_re=SECTION,
    order_key=order_key,
    division_of=division_of,
    first_section="1-1",  # Section 1 (Definitions and Terms) opens the body at 1-1
    stable_numbers=False,
)

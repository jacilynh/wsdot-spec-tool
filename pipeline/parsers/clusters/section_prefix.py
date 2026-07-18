"""The "SECTION NNN" prefix scheme: headings read "SECTION 101 - Title", section-level only.

Some DOTs (VDOT's Road and Bridge Specifications, MaineDOT's Standard Specifications) print
each heading as the literal word SECTION followed by the number and title -
"SECTION 101-DEFINITIONS", "SECTION 315 - ASPHALT CONCRETE" - and do NOT print numbered
decimal subsections as headings (subsections run inline as "(a)"/"(b)" or unnumbered
paragraphs). That is why the digit-anchored `aashto_decimal` regex finds almost nothing in
these books: the heading line starts with a word, not a number, and there is no "NNN.NN"
sublevel to catch.

So the addressable unit here is the whole Section (a few hundred per book) - coarser than the
AASHTO cluster, but the correct granularity for a book that numbers nothing finer. The
separator between number and title varies (em dash, hyphen, or just spaces), so it is
optional in the pattern.

Section numbers are not stable across editions (`stable_numbers=False`). Where a book
restarts numbering for an appendix series (MaineDOT's federal-provisions "SECTION 1-3" after
"SECTION 112"), the engine's monotonic-order filter keeps the main run and drops the short
restarted tail - a documented, per-state quirk, not a scheme change.
"""

import re

from parsers.profiles import SpecProfile

# "SECTION 101 - Title", "SECTION 315-ASPHALT CONCRETE", "SECTION 102  BIDDING": the word
# SECTION, the number, an optional separator, then the title (group 2). The separator class
# is em dash / en dash / hyphen (escaped so the source stays ASCII), or just spaces.
SECTION = re.compile(r"^SECTION\s+(\d{1,4})\s*[\u2014\u2013-]?\s*(.*)$", re.S)


def order_key(num):
    """Book order is just the Section number; there is no finer numbered level."""
    return (int(num),)


def division_of(num):
    """Hundred-series division band from the Section number: 101 -> 100, 315 -> 300."""
    return int(num) // 100 * 100


SECTION_PREFIX = SpecProfile(
    cluster="section_prefix",
    section_re=SECTION,
    order_key=order_key,
    division_of=division_of,
    first_section="101",  # both VDOT and MaineDOT open the body at SECTION 101
    stable_numbers=False,
)

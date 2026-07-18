"""Pennsylvania - Wave 1 AASHTO-decimal state (PennDOT Publication 408/2026).

Pub 408 heads each hundred-series band with a round-hundred division line
("SECTION 100 GENERAL PROVISIONS" ... through "SECTION 1200 INTELLIGENT TRANSPORTATION
SYSTEM (ITS) DEVICES"), so the divisions below are the book's own names. It is the
largest Wave 1 book (1,430 sections across 1,522 pages, bands 100-1200). Constraints:

  * history=False. Only the current (2026) edition is onboarded; AASHTO-style numbers are
    not stable across editions - browse + search only.
  * reuse=UNSTATED. PennDOT grants no redistribution license, so the reuse gate blocks a
    publishing build from emitting Pennsylvania's text; local-only via --allow-uncleared.

Parse quirk (Stage 2 QA, PASS 20/20): the parser is intentionally flat at NNN.N - lettered
(a)/(b) and numbered 1./2. sub-clauses are folded into their parent section, mirroring
PennDOT's own running-header citation style, not split into addressable sub-sections.
"""

from states.base import REUSE_UNSTATED, Division, StateDescriptor

# Division titles as printed in Pub 408/2026 (the "SECTION N00" band headers; verified).
_DIVISIONS = (
    Division(100, "General Provisions"),
    Division(200, "Earthwork"),
    Division(300, "Base Courses"),
    Division(400, "Flexible Pavements"),
    Division(500, "Rigid Pavements"),
    Division(600, "Incidental Construction"),
    Division(700, "Material"),
    Division(800, "Roadside Development"),
    Division(900, "Traffic Accommodation and Control"),
    Division(1000, "Structures"),
    Division(1100, "Manufactured Material"),
    Division(1200, "Intelligent Transportation System (ITS) Devices"),
)

PENNSYLVANIA = StateDescriptor(
    slug="pa",
    state="Pennsylvania",
    dot="PennDOT",
    profile="aashto_decimal",
    edition_model="periodic",
    editions=((2026, "current.pdf"),),
    history=False,
    reuse=REUSE_UNSTATED,
    divisions=_DIVISIONS,
    source_url=(
        "https://www.pa.gov/content/dam/copapwp-pagov/en/penndot/documents/public/"
        "pubsforms/publications/pub_408/408_2026/408_2026_ie.pdf"
    ),
    source_note=(
        "Pennsylvania DOT Specifications, Publication 408 (2026). Unofficial copy; reuse "
        "terms unstated by PennDOT. Not affiliated with or endorsed by PennDOT."
    ),
    corpus_label="PennDOT Specifications · Publication 408",
    # requirements / ask / semantic default False - browse + search only.
)

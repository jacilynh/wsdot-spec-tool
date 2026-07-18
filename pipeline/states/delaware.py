"""Delaware - Wave 1 AASHTO-decimal state, on the shared profile.

DelDOT's 2026 Standard Specifications print explicit division titles
("DIVISION 100 - GENERAL PROVISIONS" ... through "DIVISION 1000 - MATERIALS"), so the
divisions below are the book's own names, not numeric placeholders. Two constraints,
both honest to the source:

  * history=False. Only the current (2026) edition is onboarded and AASHTO numbers are
    not stable across editions, so section-history stays off - browse + search only.
  * reuse=UNSTATED. DelDOT publishes the book with no redistribution grant, so the reuse
    gate blocks a publishing build from emitting Delaware's text; it builds locally with
    build_state.py --allow-uncleared until the terms are cleared.

Structural note: the X.3-style container sections are empty by design (content lives in
their child subsections) - a faithful ~4.9% empty rate, not a parse defect (Stage 2 QA).
"""

from states.base import REUSE_UNSTATED, Division, StateDescriptor

# Division titles as printed in the 2026 book (verified against the section pages).
_DIVISIONS = (
    Division(100, "General Provisions"),
    Division(200, "Earthwork"),
    Division(300, "Base Courses"),
    Division(400, "Bituminous Materials"),
    Division(500, "Rigid Pavement"),
    Division(600, "Structures"),
    Division(700, "Miscellaneous Construction"),
    Division(800, "Traffic"),
    Division(900, "Erosion, Sediment, and Stormwater Measures"),
    Division(1000, "Materials"),
)

DELAWARE = StateDescriptor(
    slug="de",
    state="Delaware",
    dot="DelDOT",
    profile="aashto_decimal",
    edition_model="periodic",
    editions=((2026, "current.pdf"),),
    history=False,
    reuse=REUSE_UNSTATED,
    divisions=_DIVISIONS,
    source_url=(
        "https://engineeringsupport.deldot.gov/images/b/b1/"
        "2026_DelDOT_Standard_Specifications.pdf"
    ),
    source_note=(
        "Delaware DOT Standard Specifications for Road and Bridge Construction (2026). "
        "Unofficial copy; reuse terms unstated by DelDOT. Not affiliated with or endorsed "
        "by DelDOT."
    ),
    corpus_label="DelDOT Standard Specifications for Road and Bridge Construction",
    # requirements / ask / semantic default False - browse + search only.
)

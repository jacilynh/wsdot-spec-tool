"""Tennessee - Wave 2 AASHTO-decimal state (TDOT April 1, 2026 Standard Specifications).

TDOT heads sections "SECTION 101 - DEFINITIONS AND TERMS" with "101.01" decimal subsections,
but prints no division divider names on the section pages, so the divisions below carry
honest numeric band labels rather than invented AASHTO titles (the North Dakota rule).
Constraints:

  * history=False. Only the April 2026 edition is onboarded; browse + search only.
  * reuse=UNSTATED. TDOT grants no redistribution license, so the reuse gate blocks a
    publishing build from emitting Tennessee's text; local-only via --allow-uncleared.

Parse quirk (Stage 2 QA, PASS 20/20): TDOT's running header (section number + page number)
is inconsistently populated across pages - cosmetic source-PDF behavior; the parser does not
rely on it for boundary detection and captures the real inline headings faithfully.
"""

from states.base import REUSE_UNSTATED, Division, StateDescriptor

# TDOT prints no division titles; use honest numeric bands (100-900 present in the book).
_DIVISIONS = tuple(
    Division(hundred, f"{hundred}-{hundred + 99} Series")
    for hundred in (100, 200, 300, 400, 500, 600, 700, 800, 900)
)

TENNESSEE = StateDescriptor(
    slug="tn",
    state="Tennessee",
    dot="TDOT",
    profile="aashto_decimal",
    edition_model="periodic",
    editions=((2026, "current.pdf"),),
    history=False,
    reuse=REUSE_UNSTATED,
    divisions=_DIVISIONS,
    source_url=(
        "https://www.tn.gov/content/dam/tn/tdot/construction/2026-standard-specifications/"
        "April_1_2026_Standard_Specifications.pdf"
    ),
    source_note=(
        "Tennessee DOT Standard Specifications for Road and Bridge Construction "
        "(April 1, 2026). Unofficial copy; reuse terms unstated by TDOT. Not affiliated "
        "with or endorsed by TDOT."
    ),
    corpus_label="TDOT Standard Specifications for Road and Bridge Construction",
    # requirements / ask / semantic default False - browse + search only.
)

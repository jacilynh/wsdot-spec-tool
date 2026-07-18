"""Colorado - Wave 2 AASHTO-decimal state (CDOT 2025 Standard Specifications).

CDOT's book prints named divisions ("Division 100 General Provisions" through
"Division 700 Materials Details"), used verbatim below. Constraints:

  * history=False. Only the 2025 edition is onboarded; AASHTO numbers are not stable
    across editions - browse + search only.
  * reuse=UNSTATED. CDOT grants no redistribution license, so the reuse gate blocks a
    publishing build from emitting Colorado's text; local-only via --allow-uncleared.

Parse quirk (Stage 2 QA, PASS 20/20): CDOT sections often have no distinct title line, so
the title-capture takes the first physical line after the number and the body continues on
the next - which makes 75.6% of sections' captured text begin lowercase. Verified cosmetic
(title + body concatenate to the exact source text, no clause dropped), NOT the PA-style
text-loss bug.
"""

from states.base import REUSE_UNSTATED, Division, StateDescriptor

# Division titles as printed in the 2025 book (verified against the section pages).
_DIVISIONS = (
    Division(100, "General Provisions"),
    Division(200, "Earthwork"),
    Division(300, "Bases"),
    Division(400, "Pavements"),
    Division(500, "Structures"),
    Division(600, "Miscellaneous Construction"),
    Division(700, "Materials Details"),
)

COLORADO = StateDescriptor(
    slug="co",
    state="Colorado",
    dot="CDOT",
    profile="aashto_decimal",
    edition_model="periodic",
    editions=((2025, "current.pdf"),),
    history=False,
    reuse=REUSE_UNSTATED,
    divisions=_DIVISIONS,
    source_url=(
        "https://www.codot.gov/business/designsupport/cdot-construction-specifications/"
        "2025-construction-specifications/specs-book/2025-cdot-specs-book.pdf"
    ),
    source_note=(
        "Colorado DOT Standard Specifications for Road and Bridge Construction (2025). "
        "Unofficial copy; reuse terms unstated by CDOT. Not affiliated with or endorsed "
        "by CDOT."
    ),
    corpus_label="CDOT Standard Specifications for Road and Bridge Construction",
    # requirements / ask / semantic default False - browse + search only.
)

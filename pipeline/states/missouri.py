"""Missouri - Wave 1 AASHTO-decimal state (MoDOT 2026 Standard Specifications).

The largest Wave 1 book by section count (6,816 sections across 874 pages). MoDOT prints
only "SECTION 101 ..." headers on the section pages, with no division titles, so the
divisions below carry honest numeric band labels rather than invented AASHTO titles (same
rule as North Dakota). Constraints:

  * history=False. Only the current (2026) edition is onboarded; browse + search only.
  * reuse=UNSTATED. MoDOT grants no redistribution license, so the reuse gate blocks a
    publishing build from emitting Missouri's text; local-only via --allow-uncleared.

Parse quirk (Stage 2 QA): MoDOT sets many sub-paragraphs as titleless numbered paragraphs
(30.7% absorbed-title rate) - a faithful reflection of the book's style, not a defect; the
supplemental appendix that duplicates body sections is de-duplicated by the engine.
"""

from states.base import REUSE_UNSTATED, Division, StateDescriptor

# MoDOT prints no division titles; use honest numeric bands (100-1000 present in the book).
_DIVISIONS = tuple(
    Division(hundred, f"{hundred}-{hundred + 99} Series")
    for hundred in (100, 200, 300, 400, 500, 600, 700, 800, 900, 1000)
)

MISSOURI = StateDescriptor(
    slug="mo",
    state="Missouri",
    dot="MoDOT",
    profile="aashto_decimal",
    edition_model="annual",
    editions=((2026, "current.pdf"),),
    history=False,
    reuse=REUSE_UNSTATED,
    divisions=_DIVISIONS,
    source_url=(
        "https://www.modot.org/sites/default/files/documents/"
        "EPS%202026%20Missouri%20Standard%20Specific%20-%20MHTC%20(July%202026).pdf"
    ),
    source_note=(
        "Missouri DOT Standard Specifications for Highway Construction (2026). Unofficial "
        "copy; reuse terms unstated by MoDOT. Not affiliated with or endorsed by MoDOT."
    ),
    corpus_label="MoDOT Standard Specifications for Highway Construction",
    # requirements / ask / semantic default False - browse + search only.
)

"""West Virginia - Wave 3 state on the new aashto_dash profile (WVDOH 2023 Standard Specs).

WVDOH uses AASHTO-decimal section numbers with a single-hyphen separator to the title
("101.1-ABBREVIATIONS:", "102.5.1-Schedule of Items:"); see
parsers/clusters/aashto_dash.py. Hundred-series divisions, no printed divider names on the
section pages, so honest numeric band labels below. Constraints:

  * history=False. Only the 2023 base edition is onboarded (WVDOH layers annual supplemental
    specifications on top rather than reissuing); browse + search only.
  * reuse=UNSTATED. WVDOH grants no redistribution license, so the reuse gate blocks a
    publishing build from emitting West Virginia's text; local-only via --allow-uncleared.

Parse quirk (Stage 2 QA, PASS 20/20): 9.8% of sections are empty - WVDOH nests numbering up
to five dot-segments, producing more bare container headings whose content lives in their
children (confirmed benign via a corpus-wide spot-check). Occasional colon left on the body
field instead of the title - cosmetic, non-lossy.
"""

from states.base import REUSE_UNSTATED, Division, StateDescriptor

_DIVISIONS = tuple(
    Division(hundred, f"{hundred}-{hundred + 99} Series")
    for hundred in (100, 200, 300, 400, 500, 600, 700)
)

WEST_VIRGINIA = StateDescriptor(
    slug="wv",
    state="West Virginia",
    dot="WVDOH",
    profile="aashto_dash",
    edition_model="overlay",
    editions=((2023, "current.pdf"),),
    history=False,
    reuse=REUSE_UNSTATED,
    divisions=_DIVISIONS,
    source_url=(
        "https://transportation.wv.gov/highways/TechnicalSupport/specifications/Documents/"
        "2023_Standard_(12-16-22).pdf"
    ),
    source_note=(
        "West Virginia Division of Highways Standard Specifications Roads and Bridges "
        "(2023). Unofficial copy; reuse terms unstated by WVDOH. Not affiliated with or "
        "endorsed by WVDOH."
    ),
    corpus_label="WVDOH Standard Specifications Roads and Bridges",
    # requirements / ask / semantic default False - browse + search only.
)

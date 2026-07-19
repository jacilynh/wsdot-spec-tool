"""Mississippi - Wave 3 state on the new aashto_dash profile (MDOT 2017 Standard Specs).

MDOT uses AASHTO-decimal section numbers with a DOUBLE-hyphen separator to the title
("101.01--Abbreviations."); see parsers/clusters/aashto_dash.py. Hundred-series divisions,
no printed divider names on the section pages, so honest numeric band labels below.
Constraints:

  * history=False. Only the 2017 edition is onboarded; browse + search only.
  * reuse=UNSTATED. MDOT grants no redistribution license, so the reuse gate blocks a
    publishing build from emitting Mississippi's text; local-only via --allow-uncleared.

Parse quirk (Stage 2 QA, PASS 20/20): a multi-line double-hyphen title splits at the PDF
line-wrap rather than at the title's closing period, so the title's last word can land at
the front of the body field - cosmetic (title+body reproduce the source), no text lost. MDOT
also uses leading-zero variants ("102.001" alongside "102.01"), both legitimate sections.
"""

from states.base import REUSE_UNSTATED, Division, StateDescriptor

_DIVISIONS = tuple(
    Division(hundred, f"{hundred}-{hundred + 99} Series")
    for hundred in (100, 200, 300, 400, 500, 600, 700, 800)
)

MISSISSIPPI = StateDescriptor(
    slug="ms",
    state="Mississippi",
    dot="MDOT",
    profile="aashto_dash",
    edition_model="periodic",
    editions=((2017, "current.pdf"),),
    history=False,
    reuse=REUSE_UNSTATED,
    divisions=_DIVISIONS,
    source_url=(
        "https://mdot.ms.gov/documents/Construction/Specifications/"
        "2017%20Standard%20Specifications.pdf"
    ),
    source_note=(
        "Mississippi DOT Standard Specifications for Road and Bridge Construction (2017). "
        "Unofficial copy; reuse terms unstated by MDOT. Not affiliated with or endorsed "
        "by MDOT."
    ),
    corpus_label="MDOT Standard Specifications for Road and Bridge Construction",
    # requirements / ask / semantic default False - browse + search only.
)

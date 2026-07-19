"""Nebraska - Wave 3 AASHTO-decimal state (NDOT 2017 Standard Specifications).

NDOT groups sections by hundred-series and prints division dividers ("DIVISION 100 --
GENERAL REQUIREMENTS AND COVENANTS"), but not consistently on each band's first section
page, so the divisions below carry honest numeric band labels rather than a partial or
invented set (the North Dakota rule). Constraints:

  * history=False. Only the 2017 edition is onboarded; browse + search only.
  * reuse=UNSTATED. NDOT grants no redistribution license, so the reuse gate blocks a
    publishing build from emitting Nebraska's text; local-only via --allow-uncleared.

Parse quirk (Stage 2 QA, PASS 20/20): the Definitions section gives each glossary term its
own four-digit suffix (101.0407, 101.0408, ...), which inflates the section count with
one-paragraph entries - a document characteristic, captured faithfully, not a defect.
"""

from states.base import REUSE_UNSTATED, Division, StateDescriptor

_DIVISIONS = tuple(
    Division(hundred, f"{hundred}-{hundred + 99} Series")
    for hundred in (100, 200, 300, 400, 500, 600, 700, 800, 900, 1000)
)

NEBRASKA = StateDescriptor(
    slug="ne",
    state="Nebraska",
    dot="NDOT",
    profile="aashto_decimal",
    edition_model="periodic",
    editions=((2017, "current.pdf"),),
    history=False,
    reuse=REUSE_UNSTATED,
    divisions=_DIVISIONS,
    source_url="https://dot.nebraska.gov/media/g4qp4y0d/2017-specbook.pdf",
    source_note=(
        "Nebraska DOT Standard Specifications for Highway Construction (2017). Unofficial "
        "copy; reuse terms unstated by NDOT. Not affiliated with or endorsed by NDOT."
    ),
    corpus_label="NDOT Standard Specifications for Highway Construction",
    # requirements / ask / semantic default False - browse + search only.
)

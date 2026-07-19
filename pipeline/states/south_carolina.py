"""South Carolina - Wave 3 AASHTO-decimal state (SCDOT 2025 Standard Specifications).

SCDOT uses hundred-series divisions; honest numeric band labels below (the North Dakota
rule). Constraints:

  * history=False. Only the 2025 edition is onboarded; browse + search only.
  * reuse=ALL_RIGHTS_RESERVED - the strongest gate. SCDOT reserves rights, so it is
    build-only under --allow-uncleared and must never be emitted by a publishing build
    until cleared.

Parse quirk (Stage 2 QA, PASS 20/20): 14.8% of sections are empty - bare container-header
sections (e.g. 401.2.2, 604.3) immediately followed by a child subsection that carries the
real content, used more heavily/deeper than most books (same mechanism as Delaware's).
"""

from states.base import REUSE_RESERVED, Division, StateDescriptor

_DIVISIONS = tuple(
    Division(hundred, f"{hundred}-{hundred + 99} Series")
    for hundred in (100, 200, 300, 400, 500, 600, 700, 800)
)

SOUTH_CAROLINA = StateDescriptor(
    slug="sc",
    state="South Carolina",
    dot="SCDOT",
    profile="aashto_decimal",
    edition_model="periodic",
    editions=((2025, "current.pdf"),),
    history=False,
    reuse=REUSE_RESERVED,
    divisions=_DIVISIONS,
    source_url=(
        "https://www.scdot.org/content/dam/scdot-legacy/business/pdf/"
        "2025_SCDOT_Standard_Specifications.pdf"
    ),
    source_note=(
        "South Carolina DOT Standard Specifications for Highway Construction (2025). "
        "Unofficial copy; SCDOT reserves rights - not cleared for redistribution. Not "
        "affiliated with or endorsed by SCDOT."
    ),
    corpus_label="SCDOT Standard Specifications for Highway Construction",
    # requirements / ask / semantic default False - browse + search only.
)

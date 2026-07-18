"""Idaho - Wave 1 AASHTO-decimal state (ITD 2023 Standard Specifications).

ITD's book groups sections by hundred-series number but prints no division names on the
section pages - only "SECTION 101 - ..." headers - so the divisions below carry honest
numeric band labels rather than invented AASHTO titles (same rule as North Dakota).
Constraints:

  * history=False. Only the 2023 edition is onboarded; browse + search only.
  * reuse=ALL_RIGHTS_RESERVED - the strongest gate. The document asserts
    "Copyright (c) 2023. All rights reserved.", so it is build-only under
    --allow-uncleared and must never be emitted by a publishing build until ITD clears it.

Parse quirk (Stage 2 QA): two-level numbering - only SSS.NN is numbered; the deeper outline
is folded into the section text (per ITD 101.02), so deepest_nesting stays at the decimal.
"""

from states.base import REUSE_RESERVED, Division, StateDescriptor

# ITD prints no division titles; use honest numeric bands (100-700 present in the 2023 book).
_DIVISIONS = tuple(
    Division(hundred, f"{hundred}-{hundred + 99} Series")
    for hundred in (100, 200, 300, 400, 500, 600, 700)
)

IDAHO = StateDescriptor(
    slug="id",
    state="Idaho",
    dot="ITD",
    profile="aashto_decimal",
    edition_model="periodic",
    editions=((2023, "current.pdf"),),
    history=False,
    reuse=REUSE_RESERVED,
    divisions=_DIVISIONS,
    source_url="https://apps.itd.idaho.gov/Apps/manuals/SpecBook/SpecBook23.pdf",
    source_note=(
        "Idaho Transportation Department Standard Specifications for Highway Construction "
        "(2023). Unofficial copy; ITD asserts 'Copyright (c) 2023. All rights reserved.' - "
        "not cleared for redistribution. Not affiliated with or endorsed by ITD."
    ),
    corpus_label="ITD Standard Specifications for Highway Construction",
    # requirements / ask / semantic default False - browse + search only.
)

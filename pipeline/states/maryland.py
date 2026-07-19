"""Maryland - on the letter_prefix_reverse profile (MDOT SHA Standard Specifications).

MDOT SHA opens with letter-prefixed parts - GP (General Provisions, "GP-1.05") and TC (Terms
and Conditions, "TC-1.01") - and then its numeric technical body ("101.01" ...). That is the
REVERSE of RIDOT (numeric first, lettered parts last), so it uses letter_prefix_reverse: the
same number grammar and division ids as letter_prefix, but an ordering that puts the lettered
parts before the numeric ones. This is why Maryland was deferred through Waves 1-3 (the
catalog mislabeled it aashto_decimal, and a plain letter_prefix parse dropped GP/TC).

The lettered parts get synthetic integer division bands (GP=1198, TC=1523) so division ids
stay ints and the app needs no change. Divisions are listed in book order (GP, TC, then the
numeric bands). Constraints:

  * history=False. Only the current edition is onboarded; browse + search only.
  * reuse=UNSTATED. MDOT SHA grants no redistribution license, so the reuse gate blocks a
    publishing build from emitting Maryland's text; local-only via --allow-uncleared.
"""

from states.base import REUSE_UNSTATED, Division, StateDescriptor

_DIVISIONS = (
    Division(1198, "GP: General Provisions"),
    Division(1523, "TC: Terms and Conditions"),
    *(
        Division(hundred, f"{hundred}-{hundred + 99} Series")
        for hundred in (100, 200, 300, 400, 500, 600, 700, 800, 900)
    ),
)

MARYLAND = StateDescriptor(
    slug="md",
    state="Maryland",
    dot="MDOT SHA",
    profile="letter_prefix_reverse",
    edition_model="periodic",
    editions=((2025, "current.pdf"),),
    history=False,
    reuse=REUSE_UNSTATED,
    divisions=_DIVISIONS,
    source_url=(
        "https://roads.maryland.gov/OCE/Specifications/"
        "2026%20Standard%20Specifications%20for%20Construction%20and%20Materials.pdf"
    ),
    source_note=(
        "Maryland DOT State Highway Administration Standard Specifications for Construction "
        "and Materials (2026 edition, July 2025). Unofficial copy; reuse terms unstated by "
        "MDOT SHA. Not affiliated with or endorsed by MDOT SHA."
    ),
    corpus_label="MDOT SHA Standard Specifications for Construction and Materials",
    # requirements / ask / semantic default False - browse + search only.
)

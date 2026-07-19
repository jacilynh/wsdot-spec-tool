"""Ohio - Wave 3 AASHTO-decimal state (ODOT 2023 Construction & Material Specifications).

ODOT's C&MS ("Spec Book") uses hundred-series divisions with no printed division-divider
names on the section pages, so honest numeric band labels below (the North Dakota rule).
Constraints:

  * history=False. Only the 2023 C&MS (Jan 2026 update) is onboarded; browse + search only.
  * reuse=UNSTATED. ODOT grants no redistribution license, so the reuse gate blocks a
    publishing build from emitting Ohio's text; local-only via --allow-uncleared.

Parse quirk (Stage 2 QA, PASS 20/20): ODOT runs "NNN.NN Caption. body..." on one physical
line, so the title field absorbs the caption plus whatever fits before the line wraps and
the captured body resumes at the next word - 62.2% of sections' text begins lowercase. This
is a cosmetic field split (title+body reproduce the source exactly), NOT the PA text-drop bug.
"""

from states.base import REUSE_UNSTATED, Division, StateDescriptor

_DIVISIONS = tuple(
    Division(hundred, f"{hundred}-{hundred + 99} Series")
    for hundred in (100, 200, 300, 400, 500, 600, 700)
)

OHIO = StateDescriptor(
    slug="oh",
    state="Ohio",
    dot="ODOT",
    profile="aashto_decimal",
    edition_model="periodic",
    editions=((2023, "current.pdf"),),
    history=False,
    reuse=REUSE_UNSTATED,
    divisions=_DIVISIONS,
    source_url=(
        "https://www.dot.state.oh.us/Divisions/ConstructionMgt/OnlineDocs/Specifications/"
        "2023_CMS_01162026_for_web_Letter%20size.pdf"
    ),
    source_note=(
        "Ohio DOT Construction and Material Specifications (2023 C&MS, Jan 2026 update). "
        "Unofficial copy; reuse terms unstated by ODOT. Not affiliated with or endorsed "
        "by ODOT."
    ),
    corpus_label="ODOT Construction and Material Specifications",
    # requirements / ask / semantic default False - browse + search only.
)

"""Virginia - Wave 2 state on the section_prefix profile (VDOT 2020 Road and Bridge Specs).

VDOT prints each heading as "SECTION 101-Title" and numbers no decimal sub-headings (its
"103.01" decimal labels are inline subsection markers folded into the parent SECTION's text),
so the addressable unit is the whole SECTION - the section_prefix cluster's granularity. The
book does group SECTIONs into named divisions ("DIVISION I-GENERAL PROVISIONS" ...), but the
division-name-to-hundred mapping is not evidenced on the section pages and division_of groups
by hundred, so the divisions below carry honest numeric band labels rather than invented
titles (the North Dakota rule). Constraints:

  * history=False. Only the 2020 edition is onboarded; browse + search only.
  * reuse=UNSTATED. VDOT grants no redistribution license, so the reuse gate blocks a
    publishing build from emitting Virginia's text; local-only via --allow-uncleared.

Parse quirk (Stage 2 QA, PASS 20/20): section-level extraction (160 sections / 1,065 pages);
decimal-labeled prose is correctly folded into its parent SECTION, not split into children.
"""

from states.base import REUSE_UNSTATED, Division, StateDescriptor

# VDOT's section hundreds; labeled by band (see the module note on why not by division name).
_DIVISIONS = tuple(
    Division(hundred, f"{hundred}-{hundred + 99} Series")
    for hundred in (100, 200, 300, 400, 500, 600, 700, 800)
)

VIRGINIA = StateDescriptor(
    slug="va",
    state="Virginia",
    dot="VDOT",
    profile="section_prefix",
    edition_model="periodic",
    editions=((2020, "current.pdf"),),
    history=False,
    reuse=REUSE_UNSTATED,
    divisions=_DIVISIONS,
    source_url=(
        "https://www.vdot.virginia.gov/media/vdotvirginiagov/doing-business/"
        "technical-guidance-and-support/technical-guidance-documents/construction/"
        "VDOT_2020_RB_Specs_acc071522.pdf"
    ),
    source_note=(
        "Virginia DOT Road and Bridge Specifications (2020). Unofficial copy; reuse terms "
        "unstated by VDOT. Not affiliated with or endorsed by VDOT."
    ),
    corpus_label="VDOT Road and Bridge Specifications",
    # requirements / ask / semantic default False - browse + search only.
)

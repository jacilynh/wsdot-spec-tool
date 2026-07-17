"""The parsing rules that vary between numbering schemes.

Everything in the engine is scheme-independent; a `SpecProfile` supplies the handful of
things that aren't. One profile serves an entire cluster of states that share a scheme —
e.g. a single AASHTO-decimal profile covers the ~36 states on the "Section 105 -> 105.01"
pattern (see `docs/national/ARCHITECTURE.md`).
"""

from collections.abc import Callable
from dataclasses import dataclass
from re import Pattern


@dataclass(frozen=True)
class SpecProfile:
    """How to read one numbering scheme. See `clusters/wsdot_hyphen.py` for an instance.

    Attributes:
        cluster: Stable id for the scheme, e.g. "wsdot_hyphen", "aashto_decimal".
        section_re: Matches a heading line's leading text. Group 1 is the section number;
            group 2 (optional) is a title sharing the same line.
        order_key: Book-order sort key for a section number, so numbers of differing depth
            stay comparable (1-01 < 1-01.2 < 1-02). Used by the monotonic-order filter.
        division_of: Maps a section number to its division id (the value stored on each
            section and used to shard the emitted data).
        first_section: The number that opens the body — the anchor the body-start search
            tries every occurrence of ("1-01" for WSDOT, "101" for AASHTO).
        stable_numbers: Whether a section keeps its number across editions. True for WSDOT,
            which lets history match on number alone; False elsewhere, where the history
            build must fall back to content alignment (`align.py`, added in Phase C).
    """

    cluster: str
    section_re: Pattern
    order_key: Callable[[str], tuple]
    division_of: Callable[[str], object]
    first_section: str
    stable_numbers: bool

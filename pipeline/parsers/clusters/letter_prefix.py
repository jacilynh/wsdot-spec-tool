"""Letter-prefixed section numbers, alongside AASHTO-decimal numeric ones (mixed books).

Some DOTs number whole parts of the book with a letter prefix. RIDOT keeps a numeric main
body ("101.01") but numbers its Landscaping / Materials / Traffic parts with a single-letter
prefix and no dash ("L02.03.7", "M02.09.2", "T13"). This one profile matches an optional
"LETTERS[-]" prefix in front of the shared AASHTO-decimal number, so a mixed book drives the
same engine.

Book order (RIDOT) is the numeric parts first, then the lettered parts alphabetically
(L, M, T). `division_of` keeps division ids as plain integers so the app needs no change: a
numeric section maps to its hundred-series band (100..900), and a lettered section to a
synthetic band above them (1000 + the sum of its letters' alphabet positions), which sorts
the lettered parts after the numeric ones and alphabetically among themselves. `order_key`
uses that same band as its most-significant element. Numbers are not stable across editions.

This serves the numeric+trailing-letters shape (RIDOT). A book that puts its lettered parts
FIRST and a numeric body second (MDOT SHA: GP/TC before the numeric sections) needs the
reverse ordering and is not handled here - see the note in docs/national/status.json.
"""

import re

from parsers.profiles import SpecProfile

# An optional "LETTERS" or "LETTERS-" prefix, then an AASHTO-decimal number, then the title.
SECTION = re.compile(r"^((?:[A-Z]{1,3}-?)?\d{1,4}(?:\.\d+)*)(?:\s+(.*))?$", re.S)
_PARTS = re.compile(r"^([A-Z]*)-?(\d+(?:\.\d+)*)$")


def _band(num):
    """Division band as an int: a numeric section -> its hundred (100..900); a lettered one ->
    1000 + a base-26 positional encoding of its letters, so lettered parts sort after numeric
    ones, alphabetically among themselves, and distinctly (single letters L=1012/M=1013/T=1020;
    two-letter GP=1198, TC=1523 - no collision, unlike a plain letter-sum)."""
    letters, digits = _PARTS.match(num).groups()
    if not letters:
        return int(digits.split(".")[0]) // 100 * 100
    value = 0
    for char in letters:
        value = value * 26 + (ord(char) - 64)
    return 1000 + value


def _nums(num):
    return tuple(int(part) for part in _PARTS.match(num).group(2).split("."))


def order_key(num):
    """Book order for a numeric-then-lettered book (RIDOT): the division band is most
    significant (numeric bands, then lettered), then the decimal number within it."""
    return (_band(num), *_nums(num))


def order_key_lettered_first(num):
    """Book order for a lettered-then-numeric book (MDOT SHA: GP/TC before the numeric body).
    A leading flag puts every lettered section before every numeric one (0 vs 1); lettered
    sections then sort alphabetically by prefix, numeric ones by number."""
    letters = _PARTS.match(num).group(1)
    if letters:
        return (0, letters, *_nums(num))
    return (1, *_nums(num))


def division_of(num):
    """Integer division id: the hundred band for a numeric section, the synthetic letter
    band otherwise (shared by both orderings)."""
    return _band(num)


LETTER_PREFIX = SpecProfile(
    cluster="letter_prefix",
    section_re=SECTION,
    order_key=order_key,
    division_of=division_of,
    first_section="101.01",  # RIDOT opens numerically
    stable_numbers=False,
)

# The reverse shape: a book whose lettered parts come FIRST, then a numeric body (MDOT SHA
# opens with GP General Provisions and TC before its numeric technical sections). Same number
# grammar and division ids as LETTER_PREFIX; only the ordering flips.
LETTER_PREFIX_REVERSE = SpecProfile(
    cluster="letter_prefix_reverse",
    section_re=SECTION,
    order_key=order_key_lettered_first,
    division_of=division_of,
    first_section="GP-1.01",  # MDOT SHA opens at GP-1.01 (General Provisions)
    stable_numbers=False,
)

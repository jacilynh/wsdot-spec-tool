"""AASHTO-decimal numbering with a DASH between the number and its title.

Some DOTs use the national AASHTO decimal section numbers ("101.01", "102.5.1") but
separate the number from the title with a hyphen instead of whitespace - MDOT (Mississippi)
with a double hyphen ("101.01--Abbreviations."), WVDOH with a single one
("101.1-ABBREVIATIONS:", "102.5.1-Schedule of Items:"). The `aashto_decimal` regex requires
whitespace after the number, so it captures almost nothing here; everything else about the
scheme - hundred-series divisions, decimal depth, book order - is identical, so this drives
the same engine as a separate cluster rather than as new engine code.

Requiring the dash is what keeps this cluster distinct from `aashto_decimal`: a
space-separated "101.01 Abbreviations" does NOT match here (it stays on aashto_decimal), and
a dash-separated "101.01--Abbreviations." does NOT match there. Numbers are not stable across
editions (`stable_numbers=False`).
"""

import re

from parsers.profiles import SpecProfile

# AASHTO-decimal number, then a one- or two-character dash separator, then the title (group 2).
SECTION = re.compile(r"^(\d{3,4}(?:\.\d+)*)(?:[-\u2013\u2014]{1,2}\s*(.*))?$", re.S)


def order_key(num):
    """Book order for a decimal number: 101 < 101.01 < 102 (identical to aashto_decimal)."""
    return tuple(int(part) for part in num.split("."))


def division_of(num):
    """Hundred-series division: 101.01 -> 100, 421.04 -> 400."""
    return int(num.split(".")[0]) // 100 * 100


AASHTO_DASH = SpecProfile(
    cluster="aashto_dash",
    section_re=SECTION,
    order_key=order_key,
    division_of=division_of,
    first_section="101",  # Section 101 opens the body (matched via the decimal subsections)
    stable_numbers=False,
)

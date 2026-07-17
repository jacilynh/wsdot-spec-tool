"""The WSDOT numbering scheme: "1-09.7", "9-03.8(2)A" — division-hyphen-section.

Washington is the only state on this scheme, and it is state #1 for the whole project.
Section numbers are stable across all 17 editions (2000-2026), which is exactly what lets
the section-history feature match on number alone.
"""

import re

from parsers.profiles import SpecProfile

# A heading opens with a section number, then whitespace or end-of-span:
#   1-01 | 1-01.2 | 9-03.8(2) | 9-03.8(2)A
HEAD = re.compile(r"^(\d-\d{2}(?:\.\d+)?(?:\([0-9A-Za-z]+\))*[A-Z]?)(?:\s+(.*))?$", re.S)

MAX_SUBPARTS = 4
LETTER_RANK = 10**6  # lettered subparts sort after numeric ones, as the book does


def sort_key(num):
    """Order section numbers as the book does: 1-01 < 1-01.2 < 1-01.2(3) < 1-02.

    Every element is an (int, str) pair and the key is padded to a fixed length, so
    numbers of differing depth stay comparable.
    """
    div, rest = num.split("-", 1)
    main = re.match(r"^(\d+)(?:\.(\d+))?", rest)

    key = [
        (int(div), ""),
        (int(main.group(1)), ""),
        (int(main.group(2)) if main.group(2) else -1, ""),
    ]
    subparts = re.findall(r"\(([0-9A-Za-z]+)\)", rest)
    for part in subparts:
        key.append((int(part), "") if part.isdigit() else (LETTER_RANK, part))
    key.extend([(-1, "")] * (MAX_SUBPARTS - len(subparts)))

    trailing = re.search(r"([A-Z])$", rest)
    key.append((0, trailing.group(1) if trailing else ""))
    return tuple(key)


WSDOT = SpecProfile(
    cluster="wsdot_hyphen",
    section_re=HEAD,
    order_key=sort_key,
    division_of=lambda num: int(num[0]),  # "1-09.7" -> division 1
    first_section="1-01",
    stable_numbers=True,
)

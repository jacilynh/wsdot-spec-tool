# DOTcompass — Multi-State Architecture (proposed)

A concrete sketch for supporting more than one state **without** 50 repositories and
without 50 copies of the parser. Nothing here is built yet — this is the shape to review
before committing to the refactor.

## The one principle

Separate the three things that actually vary from the one thing that doesn't:

| Varies | How much | Lives as |
|---|---|---|
| **Parsing rules** (section-number pattern, ordering, division mapping) | ~6 variants, by numbering scheme | a **cluster parser** + a `SpecProfile` |
| **Where the documents are** (editions, URLs, supplement model, copyright) | per state | a **state descriptor** (config) |
| **The generated data** (static JSON) | per state | `data/<slug>/` |
| Everything else — the app, the pipeline engine, the Worker, search, the scanner | **not at all** | shared code, written once |

The recon proved this split is the right one: **36 of 50 states share the AASHTO numbering
scheme**, so one cluster parser serves 36 states. A state is then a *config entry*, not a
codebase.

## Directory layout

```
pipeline/
  parsers/
    engine.py         # the shared TOC-free typography engine (today's parse_any_edition
                      #   machinery: band detection, heading-by-contrast, the LNDS
                      #   monotonic filter, body-start-by-most-prose) — parameterized
    profiles.py       # SpecProfile + the registry of clusters
    clusters/
      wsdot_hyphen.py  # "1-09.7"        (1 state)
      aashto_decimal.py# "105" -> "105.01" (~36 states)
      # ... a handful more, added as states need them
    align.py          # NEW: cross-edition section alignment (exact number, then fuzzy)
  states/
    washington.py     # a StateDescriptor: which cluster, edition sources, history?, reuse
    pennsylvania.py
    ...               # one file per state you actually build
  build_state.py      # orchestrates one state end-to-end: fetch -> parse -> align ->
                      #   history / requirements / embeddings -> data/<slug>/
  build_history.py build_requirements.py build_app_data.py   # shared; take a profile/state
corpus/<slug>/        # each state's source PDFs (git-ignored, fetched)
app/
  src/states/         # per-state StateConfig JSON (name, historyEnabled, divisions, …)
  src/config.ts       # loads the ACTIVE state's config (selected by VITE_STATE at build)
  public/data/<slug>/ # per-state static data (git-ignored, generated)
worker/               # unchanged; CORPUS_URL points at the active state's corpus
docs/national/
  catalog.json  EXPANSION.md  ARCHITECTURE.md  (this file)
```

## Two levels of configuration

Keep them separate — one is about *how to read the book*, the other is about *which book
and whether we can use it*.

### 1. `SpecProfile` — the parsing rules for a numbering scheme (shared by a cluster)

```python
# pipeline/parsers/profiles.py
from dataclasses import dataclass
from re import Pattern
from typing import Callable

@dataclass(frozen=True)
class SpecProfile:
    cluster: str                          # "wsdot_hyphen", "aashto_decimal"
    section_re: Pattern                   # group(1)=section number, group(2)=title (if inline)
    order_key: Callable[[str], tuple]     # book-order sort key for a section number
    division_of: Callable[[str], str]     # section number -> division id
    stable_numbers: bool                  # do section numbers persist across editions?
```

Only these four-plus knobs change between clusters. Everything else in the engine
(learning the body font, stripping running headers by position, the longest-non-decreasing
heading filter, choosing the real body start) is **scheme-independent and already written** —
it just stops hardcoding the WSDOT regex.

The contrast the recon found, made concrete:

```python
# clusters/wsdot_hyphen.py   (Washington only)
WSDOT = SpecProfile(
    cluster="wsdot_hyphen",
    section_re=re.compile(r"^(\d-\d{2}(?:\.\d+)?(?:\([0-9A-Za-z]+\))*[A-Z]?)(?:\s+(.*))?$", re.S),
    order_key=wsdot_sort_key,             # today's sort_key, unchanged
    division_of=lambda num: num[0],       # "1-09.7" -> division "1"
    stable_numbers=True,                  # the WSDOT luxury the history feature relies on
)

# clusters/aashto_decimal.py   (~36 states)
AASHTO = SpecProfile(
    cluster="aashto_decimal",
    section_re=re.compile(r"^(\d{3}(?:\.\d+)*)(?:\s+(.*))?$"),   # 105, 105.01, 105.15.2.1
    order_key=lambda n: tuple(int(p) for p in n.split(".")),
    division_of=lambda num: str(int(num.split(".")[0]) // 100 * 100),  # 105 -> "100"
    stable_numbers=False,                 # most states renumber -> history needs alignment
)
```

Division *titles* are not in the profile because most states print their own division
headers ("DIVISION 100 — GENERAL PROVISIONS"); the engine reads them from the document, the
same way it already learns typography.

### 2. `StateDescriptor` — which documents, and whether we may use them

```python
# pipeline/states/washington.py
from pipeline.parsers.profiles import registry

WASHINGTON = StateDescriptor(
    slug="wa",
    state="Washington",
    dot="WSDOT",
    profile="wsdot_hyphen",
    edition_model="annual",               # annual | biennial | overlay | current_only
    editions={y: f"https://.../SS{y}.pdf" for y in range(2000, 2027, 1)},
    supplements=None,                     # overlay states list their amendment PDFs here
    history=True,                         # gates the whole section-history feature
    reuse="public",                       # public | all_rights_reserved | unstated
)
```

`history` and `reuse` are the two fields the recon says must be filled per state, honestly:
`history=False` turns the timeline feature off for that state (it becomes browser + search +
scanner), and `reuse != "public"` is a **build-time gate** — the pipeline refuses to
redistribute full text for a state whose terms aren't cleared, so the legal risk can't be
shipped by accident.

## The one genuinely new component: cross-edition alignment

WSDOT's stable numbers mean "1-09.7 in 2008" *is* "1-09.7 in 2026" — history is a number
match. Almost no other state guarantees that, so history there needs an alignment layer:

```python
# pipeline/parsers/align.py
def align(prev: list[Section], cur: list[Section], profile: SpecProfile
          ) -> list[tuple[Section | None, Section | None]]:
    """Pair each current section with its predecessor across an edition boundary.

    1. Exact section-number match. For a stable_numbers profile (WSDOT) this covers ~all.
    2. For the remainder, match by title + text similarity above a threshold — a renumbered
       section is recognized by its content, not its label.
    3. Unmatched -> genuinely added / removed.
    Every fuzzy match is scored and flagged so low-confidence pairings can be shown as such,
    not asserted. (The tool doesn't bluff — including about its own matching.)
    """
```

`build_history.py` calls `align()` instead of matching on number. For WSDOT nothing changes
(step 1 is exhaustive); for other states step 2 does the work, and its confidence rides
through to the UI.

## The app: one build, per-state config

```ts
// app/src/states/pennsylvania.json  (generated by the pipeline, or hand-written)
{
  "slug": "pa", "state": "Pennsylvania", "dot": "PennDOT",
  "siteName": "DOTcompass · Pennsylvania",
  "historyEnabled": true,
  "editions": [2000, 2003, 2007, 2011, 2016, 2020, 2024], "latest": 2024,
  "divisions": [{ "id": "100", "title": "General Provisions" }, ...],
  "disclaimer": "Unofficial. Not affiliated with or endorsed by PennDOT. …"
}
```

```ts
// app/src/config.ts  — the active state is chosen at build time
import wa from "./states/washington.json";
import pa from "./states/pennsylvania.json";

const STATES = { wa, pa /* … */ };
export const STATE = STATES[import.meta.env.VITE_STATE ?? "wa"];
export const SITE_NAME = STATE.siteName;
```

`historyEnabled` is read wherever the timeline renders, so a current-only state simply
doesn't show a history tab — the same code, one flag. Data loads from `data/<slug>/…`.

**Deployment stays simple:** each state is its own self-contained static site built from the
one codebase — `VITE_STATE=pa make build-state && deploy` — giving the per-state
customization and branding you wanted, with zero duplicated code to maintain. (The ~44 MB
search model is identical across states and can be shared from one location rather than
copied 50 times.)

## Adding a state (worked example: Pennsylvania)

1. **Clear the two gates first.** Confirm the cluster (`aashto_decimal`) and, critically,
   the copyright status. If reuse is `all_rights_reserved` or `unstated`, stop and resolve
   it before ingesting.
2. **Write `states/pennsylvania.py`** — profile + edition URLs. Pull the URLs from
   `catalog.json` as *leads*, then **re-verify each against the live document** (the recon
   proved several catalog URLs served the wrong state's PDF — never trust them blind).
3. `make build-state STATE=pa` — fetches, parses with the AASHTO profile, aligns editions,
   emits `data/pa/`.
4. **QA by hand.** Spot-check the section count and one known section's history end to end.
   This step is mandatory, not optional — the recon's lesson is that structure must be
   confirmed against the real book, per state.
5. `VITE_STATE=pa` build + deploy.
6. If PennDOT has a quirk the shared AASHTO profile mis-parses, add a **per-state override**
   in its descriptor — a few lines, in the same repo. Never a new repo.

## Migration from today's code (safe, incremental)

The current WSDOT-only code becomes *state #1* under this layout, and the existing
**2,235-section regression test is the guardrail** — the refactor is "done" only when
Washington still parses byte-for-byte identically.

- **Phase A — extract the engine.** Split `parse_any_edition.py` into `engine.py` (the
  scheme-independent machinery) + `clusters/wsdot_hyphen.py` (the WSDOT profile). Ship when
  the regression test still passes. No behavior change, no new states.
- **Phase B — introduce the config layer.** Add `states/washington.py`, route the pipeline
  through it, move WA's data under `data/wa/`, give the app a state config with WA as
  default. The live site is still pure Washington.
- **Phase C — prove the abstraction.** Add `aashto_decimal.py` + `align.py`, onboard
  **Pennsylvania** (clean single PDF). This is the real test that the cluster model works.
- **Phase D — the history pilots.** Onboard **Missouri, North Dakota, Florida** — the states
  the recon flagged as having real multi-edition archives, so the flagship feature actually
  works and the demo stays impressive.

Each phase is additive and independently shippable; nothing about the working Washington
site breaks along the way.

## What this deliberately does NOT do

- **Not 50 states, and not 50 repos.** The architecture *can* take any state; you build the
  ones where data + copyright + value align, and let real demand pull the rest.
- **Not a national "history" claim.** History is enabled per state, only where the archive
  supports it (~18–20 states). Elsewhere DOTcompass is honestly a browser + search + scanner.
- **Not a data-redistribution gamble.** `reuse` is a build gate; unresolved states don't ship.

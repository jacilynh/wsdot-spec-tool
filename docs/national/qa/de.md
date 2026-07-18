# Parse QA — Delaware (DelDOT), AASHTO profile

- Source: `corpus/de/current.pdf`
- Profile: `aashto_decimal`
- Total pages: 786
- Total sections parsed: 1320
- Absorbed-title rate: 0.002 (2 / 1320) — negligible; the two flagged titles
  (104.10, 107.13) are genuinely long, semicolon-joined titles in the source
  text, not parse failures.
- Deepest nesting: 3 dot-segments (e.g. `1022.8.2.1`, `1022.8.2.2`,
  `1022.8.2.3`); depth distribution is 907 one-dot / 410 two-dot / 3
  three-dot section numbers.

## Sample verification

20 pages sampled across the body (p.39 → p.785). For each, every section
heading visible in the page's raw text was checked against
`parsed_sections_starting_here` for correct number, correct/close title, and
correct start boundary; pages with no visible heading were checked for zero
spurious parses.

**Result: 20 / 20 correct.** No failing pages.

Pages checked: 39, 78, 117, 156, 196, 235, 274, 313, 353, 392, 431, 470, 510,
549, 588, 627, 667, 706, 745, 785. Representative spot-checks:

- p.117 — `202.3.6 Proof Rolling.` and `202.3.7 Undercut Excavation.` both
  captured correctly.
- p.392 — Division start (`SECTION 711 — SANITARY SEWER SYSTEM`); `711.1
  Description.`, `711.2 Materials.`, `711.3 Construction.` all captured.
- p.431 — Division-header page (`DIVISION 800 — TRAFFIC` /
  `SECTION 801 — TEMPORARY TRAFFIC CONTROL — GENERAL`); the extra
  `DIVISION 800` banner line is correctly *not* mistaken for a section
  heading, and `801.1`/`801.2`/`801.3` parse correctly.
- p.78, p.196, p.235, p.353, p.627, p.785 — mid-section / table-of-contents /
  item-table pages with no visible heading; parser correctly returns `[]`.

## Structural quirk: zero-text "container" headers

DelDOT's book structure regularly uses a subsection number (typically the
`X.3 Construction.` tier, occasionally `X.4 Method of Measurement.` /
`X.5 Basis of Payment.`) purely as a label that introduces a run of deeper
subsections, with **no prose of its own** between the heading and the next
numbered child. Example seen directly in the sample set, p.510:

```
836.3 Construction.
836.3.1 Installation.
```

There is no sentence between `836.3 Construction.` and `836.3.1
Installation.` — the parser correctly emits `836.3` with `textlen: 0` and
immediately starts `836.3.1`.

This is not an isolated case: across the full parse, **65 of 1320 sections
(≈4.9%) have zero-length body text**, nearly all of the form `NNN.3
Construction.` (e.g. `201.3`, `202.3`, `208.3`, `404.3`, `604.3`, `628.3`,
…) — i.e., DelDOT consistently uses this numbering level as a bare
container/header rather than a section with content. The parser handles
this correctly: section numbers and titles are captured accurately, the
body is legitimately empty because the source document has no text there,
and the real content is properly attributed to the child subsections. This
is a genuine document quirk, not a parse defect — flagged here so downstream
consumers don't mistake a `textlen: 0` "Construction." section for a missing
extraction.

## Verdict: PASS

20/20 samples correct, absorbed-title rate negligible (and fully explained
by legitimately long source titles), and the one structural quirk (zero-text
container headers at the `.3 Construction.` tier) is a faithfully-captured
document characteristic, not a parsing failure.

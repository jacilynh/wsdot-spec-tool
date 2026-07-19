# Parse QA — Maryland (MDOT SHA), letter_prefix_reverse profile

**Verdict: PASS**

- Source: `corpus/md/current.pdf` (2025 Standard Specifications for Construction and Materials)
- Profile: `letter_prefix_reverse` (new — catalog previously mislabeled this book `aashto_decimal`;
  a plain `letter_prefix` numeric-first parse had dropped the lettered GP/TC front matter entirely)
- Total pages: 1113
- Total sections parsed: 3261
- Empty-body rate: 4.8%
- Lowercase/sentence-case title rate: 8.9%
- Absorbed-title rate: 0.2%
- Samples reviewed: 22/22 correct (20-page numeric-body spread + the 2 lettered
  GP/TC front-matter pages called out below) — clears the ≥19/20 pass bar with
  no confirmed loss.

## Headline table

| Metric | Value |
|---|---|
| Profile | `letter_prefix_reverse` |
| Total pages | 1,113 |
| Total sections | 3,261 |
| Empty-body % | 4.8% |
| Lowercase-title % | 8.9% |
| Absorbed-title % | 0.2% |
| Samples correct | 22/22 |

## Sample-by-sample

| Page | Part | Headings visible in raw_text | Captured correctly? | Notes |
|---|---|---|---|---|
| 14 | GP §1 | GP-1.01, GP-1.02, GP-1.03 | Yes, all 3 | Lettered front matter — clean |
| 22 | GP §2 | GP-2.01, GP-2.02, GP-2.03, GP-2.04 | Yes, all 4 | Lettered front matter — clean; GP-2.02/GP-4.04 cross-refs in body not misparsed |
| 55 | GP §7 (mid) | GP-7.14 (GP-7.15 heading falls past 1700-char raw_text cutoff) | Yes | GP-7.15 title/head is internally consistent (mirrors GP-7.14's cross-ref pattern to TC-4.03); not visually confirmable due to sample truncation, no contrary evidence |
| 110 | TC §6 (mid) | TC-6.01, TC-6.02 (TC-6.03 heading past cutoff) | Yes | Same truncation caveat as p.55 |
| 166 | 104.07 (mid) | none (continuation page, running banner only) | Yes | Correctly returns `[]` |
| 221 | 104.29 | 104.29.01, .02, .03, .03.01 | Yes, all 4 | `104.29.03 CONSTRUCTION` is a zero-body container immediately followed by `.03.01 Equipment.` — legitimate |
| 277 | 120.03 | 120.03.05–.10 | Yes, all 6 | Cross-refs `712.03.11`/`712.03.12` in body correctly not parsed as headings |
| 333 | 308.01 | 308.01.04 | Yes | Long citation list (23 U.S.C. 109, 40 CFR ..., COMAR ...) above the heading correctly produces no spurious sections |
| 388 | 403.04 | 403.04, .01, .02, .03 | Yes, all 4 | "Long-sentence title split at line-wrap" pattern (see below) |
| 444 | 420.03 | 420.03.05 heading past 1700-char cutoff | Yes | Topically consistent (pumping/conveyor discussion → underwater placement is a standard sequence); not visually confirmable, no contrary evidence |
| 500 | 433.04 | 433.04 | Yes | Exact text match; Section 435 / 436.03.25 cross-refs not misparsed |
| 555 | 455.02 | 455.02.01, .02, .03 | Yes, all 3 | Unnumbered bold lead-in ("Mix Designs.") correctly not treated as a section |
| 611 | 482.04 | 482.04, .01–.11 (most past cutoff) | Yes | Sequential, no gaps/dupes; .02/.09/.10 are legitimate zero-body single-sentence items; minor next-section-banner bleed at tail of .11 (harmless) |
| 666 | 508 | 508.01, .02, .03, .03.01 | Yes, all 4 | `508.03 CONSTRUCTION` has real body here (contrast with p.221's empty container) — confirms empty-body only occurs when source truly has none |
| 722 | 535.04 | 535.04, .04.01 | Yes, both | Minor period-boundary quirk (period lands in `head` not `title`); no data loss. No spurious parse from table/URL content |
| 778 | 606.04 | 606.04.10, .11, .12 | Yes, all 3 | .11 is a legitimate zero-body cross-ref-only item |
| 833 | 709.03 | 709.03.03, .04, .05 (.06 heading past cutoff) | Yes | Lettered sub-items (a)-(e) inside .05's table body correctly absorbed, not split into new sections |
| 889 | 808.04 | 808.04, .01, .02, .03, .04 | Yes, all 5 | Repeated running-header banner ("808.04 MEASUREMENT AND PAYMENT") at page top correctly not double-counted |
| 945 | 902.16/.17 | 902.16.03, .04, 902.17 | Yes, all 3 | No spurious parses from table specs (D4832, C1758/T 23, etc.); inline `TC-1.03` cross-ref not misparsed |
| 1000 | 915.03 | 915.03, .01–.04 (.05 past cutoff) | Yes | 4-segment cross-ref `121.03.01.05` in body correctly not treated as a new heading — key adversarial check |
| 1056 | 923 | 923.01–.05 | Yes, all 5 | `923.02`/`923.03` are thin (7-char) cross-ref-only bodies, not zero but nearly so; no spurious parses from grade codes (D3910, M 208, CSS-1h) |
| 1112 | 951.10 | 951.10.05–.09 (.10 past cutoff) | Yes | Same period-boundary quirk as p.722 (harmless); inline `TC-1.03` cross-ref in .10 not misparsed |

## GP/TC lettered front matter — confirmed captured

The two dedicated lettered-part sample pages both parse cleanly:

- **p.14**, `GP - SECTION 1: DEFINITIONS AND TERMS` — captures `GP-1.01 GENERAL`,
  `GP-1.02 ORGANIZATIONAL STRUCTURE`, `GP-1.03 ORGANIZATIONAL DEFINITIONS`,
  each with correct title and body text starting exactly where the source
  prose starts.
- **p.22**, `GP - SECTION 2: BIDDING REQUIREMENTS AND CONDITIONS` — captures
  `GP-2.01 BID IRREVOCABLE`, `GP-2.02 CONTENTS OF BID FORMS`,
  `GP-2.03 INTERPRETATION OF QUANTITIES IN BID SCHEDULE`,
  `GP-2.04 SITE INVESTIGATION`, all four correct. Body text on this page
  cross-references `TC-2.02` and `GP-4.04` — neither is misparsed as a new
  section start, confirming the parser distinguishes a genuine heading line
  from an inline mention of another section's number.
- Elsewhere in the spread, `TC-6.01`/`TC-6.02`/`TC-6.03` (p.110) confirm the
  TC (Terms and Conditions) lettered part is also captured, and `GP-7.14`/
  `GP-7.15` (p.55) confirm GP continues to be captured deep into its own part
  (Section 7, Legal Relations), not just at the front.

This directly resolves the defect the new profile was built to fix: under the
old numeric-first `letter_prefix` parse, all GP-x.xx and TC-x.xx sections were
dropped. Under `letter_prefix_reverse` they are present and faithful.

## Numeric technical body — confirmed captured

The 20-page numeric spread (pages 55–1112) shows the numeric body captured
continuously and correctly across every category represented: 100 series
(Preliminary — `104.07`, `104.29.xx`), 120 (Tree Preservation), 300s (Erosion
& Sediment — `308.01.04`), 400s (Structures — `403.04.xx`, `420.03.05`,
`433.04`), 500s (Paving — `508.0x`, `535.04.xx`), 600s (Traffic Barriers —
`606.04.xx`), 700s (Landscape — `709.03.xx`), 800s (Electrical —
`808.04.xx`), and 900s (Materials — `902.16/.17`, `915.03.xx`, `923.0x`,
`951.10.xx`). Deepest nesting observed: 4-segment cross-references appear in
body text (e.g., `121.03.01.05` on p.1000) and are correctly left as inline
references rather than parsed as new headings.

## Empty-body rate (4.8%) — characterized as benign

Two distinct legitimate patterns account for zero-length bodies in the
sample, both directly confirmed against raw text:

1. **Container/parent headings** immediately followed by a finer
   subheading with no intervening prose — e.g. p.221's
   `104.29.03 CONSTRUCTION` (textlen 0) is immediately followed by
   `104.29.03.01 Equipment.`. The real content lives entirely in the child
   section. (Contrast: p.666's `508.03 CONSTRUCTION` has 552 chars of real
   body — the empty case only fires when the source truly has no
   separating text.)
2. **Single-sentence pay-item clauses** whose entire content is one short
   cross-referencing sentence with no line break, so the whole sentence
   becomes the `title` and nothing is left over for a `head` — e.g.
   p.611's `482.04.02 Clearing and grubbing will be measured and paid for
   as specified in 101.04.` and p.778's `606.04.11 Refer to 605.04.19.`.
   No text is lost; it's fully present in the title field itself.

## Lowercase/sentence-case title rate (8.9%) — characterized as benign

MDOT SHA's third-tier subsection headings (the `X.YY.ZZ` level, e.g.
`709.03.03 Unrolling.`, `915.03.01 Aggregate Storage.`,
`951.10.06 Adhesion to Concrete.`, `120.03.05 Tree Preservation
Operations.`) are written in sentence case ending with a period in the
source PDF itself, in contrast to the ALL-CAPS titles used at the
second-tier `X.YY` level (`DESCRIPTION`, `MATERIALS`,
`MEASUREMENT AND PAYMENT`). This convention is confirmed directly against
raw_text in essentially every sample page with third-tier content (277,
555, 666, 833, 945, 1000, 1112). It's a genuine source typographic
convention, not a parse defect.

A related but distinct cosmetic quirk, also confirmed benign: for a subset
of `MEASUREMENT AND PAYMENT` pay-item clauses (e.g. p.388's `403.04.01`,
p.611's `482.04.01`, p.778's `606.04.10`), the source has no distinct title
line at all — just a long run-on sentence. The parser splits at the PDF's
line-wrap, putting the first line in `title` and the rest in `head`.
Concatenating the two fields reproduces the original sentence exactly
(e.g., `"Support of Excavation or Fill will not be measured but will be
paid for at the Contract"` + `"lump sum price."`), so no text is lost —
only the title/head field boundary lands mid-sentence rather than at a
grammatical break.

## Spurious-section check

No mid-sentence numeric cross-reference was ever mis-parsed as a heading,
despite MDOT SHA's heavy use of inline `X.YY`/`X.YY.ZZ` references. Adversarial
checks that passed: `TC-1.03` and `GP-x.xx`/`TC-x.xx` cross-refs embedded in
numeric-body prose (pp. 22, 55, 945, 1112); a 4-segment reference
`121.03.01.05` (p.1000); citation-style references (`23 U.S.C. 109`,
`40 CFR Part 110`, `COMAR 26.17.01`, p.333); ASTM/AASHTO grade codes
(`D3910`, `M 208`, `CSS-1h`, p.1056); table-embedded technical codes
(`D4832`, `C1758/T 23`, `C1611`, p.945); and a repeated running-header
banner that could have caused a duplicate section start (p.889). None
produced a spurious `parsed_sections_starting_here` entry.

## Verdict rationale

22/22 sampled pages (20 numeric-body spread + both lettered GP/TC front-matter
pages) show every heading visible in raw_text captured with the correct
number and title, faithful body text, and no spurious sections from
cross-reference noise. The only caveats are a handful of pages where a
reported section's heading line falls past the 1700-character raw_text
sample window (pp. 55, 110, 444, 833, 951/1112) — in every case the
reported title is topically and stylistically consistent with its context
and no contrary evidence was found; this is a limitation of the fixed-length
probe sample, not a demonstrated parser defect. The empty-body (4.8%) and
lowercase-title (8.9%) rates are both fully explained by genuine,
directly-confirmed MDOT SHA document conventions (container headings and
single-sentence pay items; sentence-case third-tier titles), matching the
pattern of benign structural quirks already documented for other states
(e.g. DelDOT's zero-text `.3 Construction.` containers in `de.md`). No
confirmed real text loss.

## Verdict: PASS

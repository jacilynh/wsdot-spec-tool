# Parse QA — Tennessee (TDOT, April 2026 Standard Specifications), profile `aashto_decimal`

**Verdict: PASS**

## Headline numbers

| Metric | Value |
|---|---|
| Total pages | 1,078 |
| Total sections parsed | 1,142 |
| Absorbed-title rate | 0.0% (0 / 1,142) |
| Empty-text sections | 1.2% (~14 / 1,142) |
| Lowercase-start sections | 0.3% (~3 / 1,142) |
| Profile | `aashto_decimal` |
| Samples correct | **20 / 20** |
| Failing sample pages | none |

TDOT's corpus is the cleanest sampled to date: absorbed-title rate is flat zero, and both
empty-text and lowercase-start rates are near-zero (no known systemic bug fingerprint — compare
PA's pre-fix 7.1%/29.0% same-line-drop signature, which TDOT does not exhibit at all).

## Sample-by-sample (20 pages)

| Page | Sections claimed to start here | Verdict | Note |
|---|---|---|---|
| 53 | (none) | CORRECT | mid-section (105.09), numbered list items 2–5 continuing from prior page, no heading visible |
| 106 | (none) | CORRECT | mid-section (108.10), lettered `B. Without Fault` inline, not a new decimal section |
| 160 | (none) | CORRECT | mid-section (203.09), lettered `A. Road and Drainage Excavation` inline |
| 214 | (none) | CORRECT | mid-section (209.07), lettered `b. Miscellaneous Coagulants/Flocculants` inline |
| 268 | 309.13 Method of Measurement; 309.14 Basis of Payment | CORRECT | both headings captured with correct number/title; 309.13 body opens exactly at "The Department will measure:"; 309.14 body opens at "A. General..." |
| 322 | (none) | CORRECT | mid-section (407.03), lettered/numbered sub-items only |
| 376 | 414.03 Composition of Mixture | CORRECT | heading captured correctly; body opens exactly at "At least 2 weeks before beginning work, submit a signed original of a mix design..." — true opening sentence, not mid-sentence |
| 430 | (none) | CORRECT | mid-section (501.26), table + numbered item `2. Pavement Rideability` inline |
| 484 | 602.41 Temporary Supports; 602.42 Method and Equipment; 602.43 Straightening Bent Material and Cambering | CORRECT | 602.41 and 602.42 verified directly against raw text (exact opening sentences); 602.43 falls past the 1,700-char raw-text snippet cutoff so its start could not be directly re-verified against raw text, but number/title are well-formed and consistent with the page's heading sequence |
| 538 | 604.06 Falsework | CORRECT | body opens exactly at "Support falsework, used to support the forms and concrete..." |
| 591 | 606.15 Inspection of Shells for Cast-in-Place Piling; 606.16 Extensions and Splices | CORRECT | both verified, exact opening sentences captured |
| 645 | (none) | CORRECT | mid-section (615.11), numbered `1. Water Curing` / `2. Steam Curing` inline |
| 699 | 701.01 Description; 701.02 Materials | CORRECT | Section 701's table-of-contents (dotted-leader lines listing 701.01–701.14) correctly produces **no** spurious section stubs; only the two headings that actually occur as body text on the page are captured, 701.01 verified exact opening sentence |
| 753 | (none) | CORRECT | mid-section, lettered `A. Flaggers` / `B. THP Troopers...` inline |
| 807 | 716.04 Raised Retroreflective Pavement Markers | CORRECT | body opens exactly at "To bond markers to the pavement, use an epoxy listed on the Department's QPL..." |
| 861 | 730.29 Detectors | CORRECT | body opens exactly at "Provide detectors, of the type shown on the Plans..."; large section (textlen 11,083) consistent with a long detector-hardware spec, not a merge error |
| 915 | (none) | CORRECT | Part 9 materials directory (TOC listing SECTION 901–919+ with dotted leaders); correctly produces no spurious section stubs from the TOC entries |
| 969 | 908.08 Malleable Castings; 908.09 Bronze Bearing Plates, Plain; 908.10 Bronze Bearing Plates, Self-Lubricating; 908.11 Corrosion Resistant Steel; 908.12 Elastomeric Bearing Pads | CORRECT | five headings on one dense page, all captured with correct numbers/titles and exact opening text (including a one-sentence section, 908.08, textlen 53) |
| 1023 | (none) | CORRECT | mid-section (919.01), lettered `C. Glass Beads` / `D. Intermix Glass Beads` inline |
| 1077 | (none) | CORRECT | back-matter Index page, correctly unparsed |

**20/20 correct.**

## Structural quirk: inconsistent running-header section stamp (benign)

TDOT stamps most pages with a running header giving the currently-active section number and the
page number, in the form:

```
309.13


259
```

(section number, two blank lines, printed page number — seen on pages 53, 106, 160, 214, 268,
322, 376, 430, 484, 538, 591, 645, 969, 1023). On Part-divider and back-matter pages this label is
replaced by a text tag instead of a decimal number — `Part 9` on p.915, `Index` on p.1077 — and on
several ordinary body pages the section-number field is simply **blank**, leaving only the page
number: p.753 (`" \n744"`), p.807 (`" \n798"`), p.861 (`" \n852"`), even though each of these pages
clearly sits mid-document with an active section (716.04 starts partway down p.807, 730.29 starts
partway down p.861).

This is a genuine layout inconsistency in the source PDF's running header, not a parser defect: the
header stamp is cosmetic and the parser does not use it to detect section boundaries. It correctly
ignores the header on every sampled page — no spurious section is ever emitted from a header
number, blank header, or `Part N`/`Index` label, and real inline headings on the blank-header pages
(716.04 on p.807, 730.29 on p.861) are still captured correctly. Flagged here only so a downstream
consumer parsing TDOT running headers directly (e.g., for page-to-section lookup) knows the header
field cannot be trusted as complete or consistently populated.

## Verdict rationale

Per the pass bar (samplesCorrect ≥ 19/20 AND absorbed-title rate low or fully explained AND no real
section text dropped): **20/20 sampled pages correct**, absorbed-title rate is a flat **0.0%**, and
every heading verified directly against raw text (309.13/309.14, 414.03, 602.41/602.42,
604.06, 606.15/606.16, 716.04, 730.29, 908.08–908.12, 701.01) opens at its true first sentence —
no mid-sentence truncation, no dropped opening text, no empty capture where raw text shows body
prose. Table-of-contents dotted-leader pages (699, 915) correctly yield no spurious stub sections.
The one quirk found (inconsistent running-header section stamp) is cosmetic source-PDF behavior
that does not affect parsing. **Verdict: PASS.**

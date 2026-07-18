# Parse QA — Pennsylvania (PennDOT Publication 408/2026), profile `aashto_decimal`

**Verdict: FAIL**

## Headline numbers

| Metric | Value |
|---|---|
| Total pages | 1,522 |
| Total sections parsed | 1,430 |
| Absorbed-title rate | 0.0% (0 / 1,430) |
| Deepest nesting | 1 (flat `NNN.N` only — no lettered/numbered sub-levels split out) |
| Samples correct | 15 / 20 |
| Failing sample pages | 532, 608, 988, 1064, 1216 |

Absorbed-title rate is clean (no titleless-paragraph numbering problem), and every visible top-level
section heading in all 20 sampled pages was captured with the correct number and title, with no
spurious sections on mid-section pages. **However, a separate and more serious defect was found
during boundary verification: the parser systematically drops the body text that shares a physical
PDF line with the section number/title, whenever the heading and its first sentence are typeset on
the same line.** This is not cosmetic — it deletes real requirement text from a meaningful fraction
of sections, including a "MEASUREMENT AND PAYMENT" pay-unit sentence. This is why 5 of the 20 samples
are marked INCORRECT despite every heading number/title being right.

## Sample-by-sample (20 pages)

| Page | Sections claimed to start here | Verdict | Note |
|---|---|---|---|
| 76 | (none) | CORRECT | mid-section (107.30), no heading on page |
| 152 | (none) | CORRECT | mid-section (206.3), no heading on page |
| 228 | (none) | CORRECT | mid-section (344.3), lettered (b) inline, not a new numbered section |
| 304 | 419.4 MEASUREMENT AND PAYMENT— | CORRECT | title stands alone on its line; body text intact |
| 380 | (none) | CORRECT | mid-section (502.3), lettered (h) inline |
| 456 | (none) | CORRECT | table page, no heading |
| 532 | 620.1 DESCRIPTION; 620.2 MATERIAL; 620.3 CONSTRUCTION | **INCORRECT** | 620.1 and 620.3 both lose their opening sentence — see below |
| 608 | 680.1 DESCRIPTION; 680.2 MATERIAL | **INCORRECT** | both lose their opening sentence |
| 684 | (none) | CORRECT | mid-section (704.3), lettered (d) inline |
| 760 | (none) | CORRECT | mid-section (808.2), bullets only |
| 836 | (none) | CORRECT | mid-section (930.3), lettered (c)–(g) inline headings, correctly not split |
| 912 | (none) | CORRECT | mid-section (953.3) |
| 988 | 1001.3 CONSTRUCTION | **INCORRECT** | loses opening sentence "Construct as shown on the Standard Drawings and as follows:" |
| 1064 | 1017.1 DESCRIPTION; 1017.2 MATERIAL; 1017.3 CONSTRUCTION | **INCORRECT** | 1017.1's entire body ("This work is the pointing and the surfacing of areas of structures.") is deleted — `textlen: 0` |
| 1140 | (none) | CORRECT | mid-section (1050.3) |
| 1216 | 1089.4 MEASUREMENT AND PAYMENT | **INCORRECT** | loses opening sentence "Linear Foot, measured from end to end of barrier." — the pay-unit statement itself |
| 1292 | (none) | CORRECT | mid-section (1105.03(hh)) |
| 1368 | (none) | CORRECT | mid-section (1204.2(c)), spec-sheet bullets |
| 1444 | (none) | CORRECT | Appendix B (SSP index), not decimal-numbered, correctly unparsed |
| 1521 | (none) | CORRECT | back-matter Index of Changes |

**15/20 correct.**

## The bug: same-line title+body text is dropped

Whenever a section heading is followed immediately by body text on the *same physical PDF line*
(e.g. `620.1  DESCRIPTION—This work is construction of new guide rail of the type indicated,
re-setting of existing ` wrapping to a second line `guide rail, removal of a concrete end anchor…`),
the parser discards everything on that first line and begins the section's captured text on the
*next* physical line. Confirmed directly against the PDF for:

- **620.1** (p.532): raw opens "This work is construction of new guide rail of the type indicated,
  re-setting of existing" — parsed text starts at "guide rail, removal of a concrete end anchor…"
  (missing clause entirely).
- **620.3** (p.532): raw opens "As shown on the Standard Drawings and as follows:" — parsed text
  starts directly at "(a) New Guide Rail." (missing sentence entirely).
- **680.1** (p.608): raw opens "This work is the furnishing and placing of adhesive preformed
  membrane" — parsed text starts at "waterproofing systems to concrete or other surfaces as
  indicated." (missing clause).
- **680.2** (p.608): raw opens "Unless specified or shown on the plans, select from the
  waterproofing systems listed" — parsed text starts at "in Bulletin 15." (missing clause).
- **1001.3** (p.988): raw opens "Construct as shown on the Standard Drawings and as follows:" —
  parsed text starts at "(a) Forms and Centering." (missing sentence).
- **1017.1** (p.1064): raw is a single line, "This work is the pointing and the surfacing of areas
  of structures." — entire sentence is on the shared line, so the parsed section text is **empty**
  (`textlen: 0`).
- **1089.4** (p.1216): raw opens "Linear Foot, measured from end to end of barrier." — the pay-unit
  clause, the substantive content of a MEASUREMENT AND PAYMENT section — is dropped; parsed text
  starts at "Caulking compound as specified in Section 705.7 is incidental."

Sections where the title is followed only by whitespace/newline before the body starts on its own
line (e.g. `419.4  MEASUREMENT AND PAYMENT— \n \n    (a)  SMA RPS Construction.`, or `1017.2
MATERIAL— \n \n    (a)  Cement.`) are **not** affected — text capture is correct there. So the trigger
is specifically "body prose typeset on the same line as the heading," which is PennDOT's dominant
DESCRIPTION-paragraph style (short lead sentence immediately after the title, then wrapping).

Corpus-wide sweep (independent of the 20-sample set) confirms this is not an edge case:

- **102 / 1,430 sections (7.1%) have completely empty parsed text** (`len(text) == 0`) — almost
  certainly single-line title+body sections like 1017.1 where the whole body was swallowed.
- **415 / 1,430 sections (29.0%) have text starting on a lowercase letter**, the fingerprint of a
  parsed body beginning mid-sentence because the true opening sentence/clause was dropped.

This defect corrupts the actual requirement text delivered to end users — a live risk for a
compliance tool that must quote/cite spec language faithfully — and is unrelated to, and more
serious than, the absorbed-title-rate metric (which is 0 and clean).

## Structural quirk: confirming/correcting the suspected pattern

The task's suspected quirk — "lettered sub-level (104.06(a)) appears only in running headers, not
body" — is **refuted** for PA. Lettered/numbered sub-clauses are visibly present as inline headings
in the body text throughout the document, e.g.:

- p.836 (930.3): body shows `(c) Removal of Existing Signs.`, `(d) Clearing and Grubbing.`,
  `(e) Restoration of Site.`, `(f) Motorist Service Signs.`, `(g) Posts and Foundations.` all inline.
- p.532 (620.3): body shows `(a) New Guide Rail.` inline, with numbered sub-items `1. General.`
  under it.
- p.608 (680.2): body shows `(a)`–`(e)` lettered material subsections inline.

The actual quirk is: **the parser is intentionally flat (`deepest_nesting = 1`)** — it recognizes
only `NNN.N` headings as section boundaries. Lettered `(a)`/`(b)` and numbered `1.`/`2.` sub-clauses,
though visually formatted as inline sub-headings in the body (bold run-in text ending in a period),
are correctly left folded into their parent `NNN.N` section's text rather than split into addressable
sub-sections. Running headers (e.g. `930.3(c)` / `930.3(g)` at the top of p.836, `620.1` / `620.3(a)`
on p.532) cite the first/last subsection *visible* on the page for navigation — they are not the only
place lettered content appears; they mirror what's already in the body. This flat-nesting design is a
legitimate, consistent choice (not a defect) as long as consumers know citations like "620.3(a)" will
resolve to the 620.3 section's full text, not an isolated (a) excerpt — but it is orthogonal to, and
does not explain or excuse, the same-line text-drop bug above.

## Verdict rationale

Per the pass bar (samplesCorrect ≥ 19/20 AND absorbed-title rate low or fully explained): absorbed-
title rate is fine, but **samplesCorrect is 15/20**, driven by a confirmed, reproducible, corpus-wide
text-fidelity bug (same-line heading+body text silently dropped, affecting ~7% of sections completely
and ~29%+ partially). **Verdict: FAIL.** This parser output should not be built into the PA state
until the same-line title/body text capture is fixed.

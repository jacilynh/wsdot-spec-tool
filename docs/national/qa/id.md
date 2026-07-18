# Parse QA — Idaho (ITD), 2023 Standard Specifications for Highway Construction

- Source: `corpus/id/current.pdf` (768 pages)
- Profile: `aashto_decimal`
- Total sections parsed: 878
- Absorbed-title rate: 0.0
- Deepest nesting: 1

## Sample verification (20/20 pages)

All 20 sampled pages, spread across the body (pages 38–767), were checked
against the full extracted page text (not just the first 1600 chars the probe
prints, which truncates mid-page on long pages). For every sample the section
headings visible on the page — full `XXX.YY Title.` numbers — matched the
parser's `parsed_sections_starting_here` exactly on number and title, and
every page with no visible `XXX.YY` heading (mid-section body text, lettered
sub-items, tables) correctly produced an empty parsed-sections list.

Two samples (pages 38 and 460) initially looked suspicious because the
probe's 1600-char truncation cut off before a second/third heading the parser
claimed started on that page (101.02 on p.38; 560.04/560.05 on p.460).
Pulling the full untruncated page text confirmed all of those headings do
appear later on the same page, correctly captured. No discrepancies found.

**samplesCorrect: 20/20. No failing pages.**

## Structural quirk: only two numbered levels — deeper hierarchy is unnumbered

`deepest_nesting = 1` across all 878 sections is a genuine feature of this
book, not a parser miss. Idaho's spec explicitly documents its own structure
on page 38 (§101.02 Organization of Specifications):

> "Each section contains the following primary subsections: XXX.01
> Description. XXX.02 Materials. XXX.03 Construction Requirements. XXX.04
> Method of Measurement. XXX.05 Basis of Payment. The subsections contain
> varying numbers of titled subordinate subsections composed of higher and
> lower levels."

In practice, only the `SSS.NN` level (e.g. `651.02`, `713.06`) is a numbered,
titled subsection. Everything below that — `A.`/`B.` lettered parts, `1.`/`2.`
numbered parts, `a.`/`b.` sub-lettered parts, `(1)`/`(2)` parenthetical
items — is an *unnumbered* outline level that lives as body text inside the
enclosing `SSS.NN` section, rather than being its own decimal-numbered
subsection the way WSDOT nests e.g. `5-01.3(3)C`. Confirmed by direct
inspection:

- p.613, `651.02 Materials.` contains `A. Turf Seed.`, `B. Sod.`,
  `C. Fertilizers and Soil Conditioners.`, `D. Soil Amendment.`, `E. Mulch.` —
  all folded into 651.02's text, no separate sections emitted (correct).
- p.421, inside `511.xx`, contains lettered `a.`/`b.`/`c.` items with nested
  `(1)`/`(2)` sub-items — all folded into the enclosing section's text
  (correct).
- p.460, `560.04 Method of Measurement.` and `560.05 Basis of Payment.`
  follow lettered `B. Dewatering.` / `C. Removal.` content that stays inside
  `560.03` — the two-level ceiling holds even at a section boundary.

This is why `absorbed_title_rate` is 0.0: there's no titleless-paragraph
problem to trigger it — the book simply never numbers past two levels, so the
parser has nothing deeper to absorb or drop.

## Verdict: PASS

20/20 samples correct, absorbed-title rate is 0.0 (no titleless-paragraph
issue), and the flat `deepest_nesting = 1` is fully explained and documented
as an intentional feature of Idaho's own spec-numbering convention (§101.02),
not a parse failure.

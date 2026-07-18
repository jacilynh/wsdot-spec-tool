# Parse QA — Indiana (INDOT 2026), profile `aashto_decimal`

**Verdict: FAIL**

## Headline numbers

| Metric | Value |
|---|---|
| Total pages | 1,328 |
| Total sections parsed | 1,687 |
| Absorbed-title rate | 0.0% (0 / 1,687) |
| Empty-text sections | 1.2% |
| Lowercase-start sections | 0.0% |
| Profile | `aashto_decimal` — single combined book, fine-grained `NNN.NN` numbering |
| Samples correct | **19 / 20** |
| Failing sample pages | p.464 |

Corpus-level metrics look clean at first glance (0% absorbed titles, 0% lowercase-start,
low 1.2% empty-text), and 19/20 sampled pages check out cleanly against `raw_text`. The
disqualifying finding is not statistical — it's a specific, verifiable instance of a
section that never makes it into the parsed corpus at all because its heading is
unrecoverable garbage in the PDF's extracted text, and this failure mode is **invisible
to all three corpus-level metrics** (a missing section isn't "absorbed," "empty," or
"lowercase" — it simply doesn't exist in `parsed_sections_starting_here`).

## Sample-by-sample (20 pages)

| Page | Sections claimed to start here | Verdict | Note |
|---|---|---|---|
| 66 | (none) | CORRECT | Table of Contents page listing `910.07`–`910.13` as page references; correctly not parsed as live section starts |
| 132 | 105.16 Notice of Changed Conditions and Claims | CORRECT | head opens at true text (`610\nNothing in this subsection...`), a stray page/line-number token precedes it but no prose is skipped |
| 198 | 109.06 Eliminated Pay Items; 109.07 Partial Payments | CORRECT | 109.06 opens exactly at raw text's first sentence; 109.07 falls past the 1,700-char raw_text window (plausible continuation, no contradicting evidence) |
| 265 | (none) | CORRECT | mid-section, only a lettered `(b)` sub-heading visible, correctly not split out |
| 331 | 217.09 Compaction; 217.10 Method of Measurement; 217.11 Basis of Payment | CORRECT | 217.09 head matches raw text's opening sentence exactly; 217.10/.11 fall past the visible window |
| 397 | (none) | CORRECT | mid-section, lettered `(b)` sub-item only, no spurious section |
| **464** | **(none)** | **INCORRECT** | **section heading is font-corrupted in the source PDF (`(TXLSPHQW`) — see Blocking Defect below. Parser correctly finds no clean `NNN.NN` pattern, but the practical effect is the entire section (heading + body) is silently dropped from the parse** |
| 530 | 506.05 Trial Batch | CORRECT | heading falls past the 1,700-char raw_text window; head text (`275\nA trial batch shall be produced...`) is internally consistent with the pattern seen elsewhere, no contradicting evidence |
| 596 | 606.02 Materials; 606.03 General Requirements; 606.04 Method of Measurement; 606.05 Basis of Payment | CORRECT | all four headings and openings match raw text exactly |
| 663 | 622.19 Blank; 622.20 "Do Not Mow or Spray" Signs...; 622.21 Method of Measurement; 622.22 Basis of Payment | CORRECT | `622.19 Blank` is INDOT's placeholder-title convention (see Quirk below), correctly captured with only a line-number token as body; remaining three match raw text exactly |
| 729 | 703.01 Description; 703.02 Materials | CORRECT | both headings fall past the 1,700-char raw_text window (page tail is still Basis-of-Payment prose for the prior section); head text for 703.01/703.02 matches the standard Description/Materials opening pattern seen on every other sampled page, no contradicting evidence |
| 796 | 711.69 Jacking and Supporting Beams; 711.70 Field Cleaning and Storage of Weathering Steel; 711.71 Coating; 711.72 Method of Measurement | CORRECT | all four match raw text exactly |
| 862 | (none) | CORRECT | mid-section, numbered `2. Hydrodemolition` sub-item only, no spurious section |
| 928 | 732.03 Design Criteria | CORRECT | matches raw text exactly |
| 995 | 803.04 Qualification of Procedures...; 804.01 Description; 804.02 Materials; 804.03 Delineator Visibility | CORRECT | all four match raw text exactly; `SECTION 804 – DELINEATORS` division banner correctly not mistaken for a section |
| 1061 | (none) | CORRECT | mid-section, numbered/lettered sub-items (`1.`, `2.`, `a.`–`f.`) only, no spurious section |
| 1127 | 908.02 Corrugated Steel Pipe and Pipe-Arches; 908.03 Blank | CORRECT | 908.02 matches raw text exactly; 908.03 Blank is the same placeholder convention as p.663 |
| 1194 | 913.06 Bentonite Grout; 914.01 Special Topsoil...; 914.02 Temporary Seed; 914.03 Fertilizer; 914.04 Grass, Legume, and Forb Seed | CORRECT | all match raw text; `SECTION 914 – ROADSIDE DEVELOPMENT MATERIALS` banner correctly skipped |
| 1260 | (none) | CORRECT | mid-section, NEMA TS2 controller spec prose, no spurious section |
| 1327 | (none) | CORRECT | "Intentionally left blank" page |

**19/20 correct.**

## Blocking defect: font-encoding corruption silently drops a section (p.464)

`raw_text` for page 464 contains this line, verbatim from the probe:

```
(TXLSPHQW
```

This sits in exactly the structural position a section heading occupies everywhere
else in the sample (blank line above, blank line below, followed immediately by an
opening body sentence: *"The recycling equipment shall be capable of milling the
existing asphalt pavement, sizing the resulting RAP, and mixing the RAP with the
materials stipulated in the mix design."*). Decoding the letters confirms this is a
corrupted rendering, not noise: mapping the trailing glyphs `TXLSPHQW` back through a
uniform +3 letter shift yields `quipment`, and the leading `(` decodes the same way to
a plausible section-number/title lead-in — i.e., this line is almost certainly
`NNN.NN Equipment` in the source PDF, rendered as raw glyph-index bytes because the
embedded subset font for this one heading has no usable ToUnicode/CMap mapping. This
is a defect in the **source PDF's text layer**, not in the section-splitting regex —
but the consequence for the parsed corpus is the same either way:

- No section is emitted for this heading at all — `parsed_sections_starting_here` for
  p.464 is `[]`, even though a heading visibly occupies that page.
- The body prose that follows ("The recycling equipment shall be capable of
  milling...") has nowhere correct to go; it is presumably folded into whichever
  section was still open from the prior heading, meaning that section's `textlen` is
  now silently inflated with content that isn't about it, while the true
  "`___.__ Equipment`" section doesn't exist anywhere in the corpus under its own
  number.
- **None of the three corpus-level fingerprints catch this.** `absorbed_title_pct` only
  flags sections that exist but have overlong titles; `empty_pct`/`lowercase_pct` only
  flag sections that exist but start oddly. A section that never gets created in the
  first place produces no signal in any of them — `total_sections: 1687` looks like a
  complete count, but there is no way to tell from the aggregate stats alone whether
  it's missing one section or several dozen of this type.

This was caught only because it happened to fall inside the 20-page random sample
(1.5% of the 1,328-page book). Whether this is a one-off scanning artifact affecting a
single heading or a recurring issue with a specific embedded font used at multiple
points in the document cannot be determined from this probe — and that is itself the
problem: the corpus provides no bounded signal for this defect class, so its true
extent is unknown.

## Structural quirk: explicit "Blank" placeholder sections

Independent of the p.464 defect, INDOT's book uses literal `Blank` as a section title
to hold a reserved section number with no content, rather than omitting the number
entirely. This shows up three times just within the 20-page sample:

- p.66 (TOC): `910.12 Blank` listed with no page-range body, alongside real sibling
  entries like `910.11` and `910.13`.
- p.663: `622.19 Blank` is parsed correctly — `head` is just the stray line-number
  token `"370"` and `textlen: 3`, immediately followed by `622.20 "Do Not Mow or
  Spray" Signs...`.
- p.1127: `908.03 Blank` (`textlen: 2`), immediately preceded by `908.02 Corrugated
  Steel Pipe and Pipe-Arches`.

This fully explains the corpus's 1.2% empty-text rate: these are legitimate,
intentionally-empty reserved section numbers (INDOT keeps historical numbering
contiguous across revisions even when a section's content is retired), not a parser
failure to capture real prose. The parser handles this correctly — number and title
are captured, and the near-empty body reflects the source document, not a bug.

## Verdict rationale

Per the pass bar: samples-correct is 19/20 (meets the `>=19/20` threshold in
isolation), and absorbed-title rate is 0.0% (clean). But the pass bar has a third,
overriding condition — **no real section text is dropped, full stop, regardless of
sample count** — and page 464 violates it directly: an entire section (heading and the
start of its body) is unrecoverable from the parsed corpus because the source PDF's
text layer is corrupted for that heading, and this failure mode leaves no trace in
`absorbed_title_pct`, `empty_pct`, or `lowercase_pct`, meaning the corpus-wide stats
cannot be used to bound how often it recurs elsewhere in the 1,328-page book.

Numerically this is a narrow finding (1 confirmed instance in a 20-page sample), and
if it is truly a one-off scanning artifact affecting a single heading, the practical
citation-accuracy impact is small. But the instruction to score this stage is explicit
that a confirmed instance of dropped real text fails the state regardless of how
favorable the sample ratio otherwise looks, and unlike PA's now-fixed same-line-drop
bug (which was corpus-wide and directly measurable via `empty_pct`/`lowercase_pct`),
this defect class has no corpus-level fingerprint at all — so "it's probably rare"
cannot be verified from the data available in this review. **Verdict: FAIL**, pending
either (a) confirmation via full-corpus scan that this is an isolated single
occurrence with no other affected sections, or (b) a source-PDF re-extraction pass
that recovers text for corrupted-font headings (e.g., OCR fallback when ToUnicode
mapping is absent/garbage) before this state is re-scored.

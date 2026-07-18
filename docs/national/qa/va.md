# Parse QA — Virginia (VDOT Road and Bridge Specifications, 2020), profile `section_prefix`

**Verdict: PASS**

## Headline numbers

| Metric | Value |
|---|---|
| Total pages | 1,065 |
| Total sections parsed | 160 |
| Granularity | SECTION-level (VDOT prints `SECTION NNN—Title`; decimal labels like `103.01` are internal subsection labels within the same SECTION, not separately numbered top-level headings — section-level is the correct/only granularity for this book) |
| Empty-text sections | 0.0% (0 / 160) |
| Lowercase-start sections | 0.0% (0 / 160) |
| Absorbed-title rate | 0.0% (0 / 160) |
| Samples correct | **20 / 20** |
| Failing sample pages | none |

## Sample-by-sample (20 pages)

| Page | Sections claimed to start here | Verdict | Note |
|---|---|---|---|
| 53 | 103 — AWARD AND EXECUTION OF CONTRACTS | CORRECT | `SECTION 103—AWARD AND EXECUTION OF CONTRACTS` heading visible; captured `head` begins exactly at `103.01—Consideration of Bids` / opening sentence, matching raw text verbatim |
| 106 | (none) | CORRECT | mid-section (107.12 running header), no new SECTION heading, no spurious parse |
| 159 | (none) | CORRECT | mid-section (FOOH delay-cost list under Section ~105), no heading, no spurious parse |
| 212 | (none) | CORRECT | mid-section (211.13/211.14 subsection labels visible inline), correctly folded into parent Section 211, not split out |
| 265 | (none) | CORRECT | mid-section (pipe-materials list), no heading, no spurious parse |
| 319 | (none) | CORRECT | mid-section (246.03 running header, pavement-marking material list), no spurious parse |
| 372 | (none) | CORRECT | mid-section (erosion-control item list, "(j) Inlet Protection"), no spurious parse |
| 425 | (none) | CORRECT | mid-section (asphalt-paving placement text), no heading, no spurious parse |
| 478 | (none) | CORRECT | mid-section (Table IV-1 pile-tolerance table, 403.06 running header), no spurious parse |
| 531 | (none) | CORRECT | mid-section (structural-steel erection/bolting text), no heading, no spurious parse |
| 585 | (none) | CORRECT | mid-section (bridge-deck patching text), no heading, no spurious parse |
| 638 | (none) | CORRECT | mid-section (latex-modified concrete overlay text), no heading, no spurious parse |
| 691 | (none) | CORRECT | mid-section; `504.04—Measurement and Payment` subsection label visible inline but correctly folded into parent Section 504, not split out |
| 744 | (none) | CORRECT | mid-section; `515.04—...` and `515.05—Measurement and Payment` subsection labels visible inline but correctly folded into parent Section 515 |
| 797 | (none) | CORRECT | mid-section (landscaping/planting-bed text), no heading, no spurious parse |
| 851 | (none) | CORRECT | mid-section (703.02 running header, traffic-controller spec text), no spurious parse |
| 904 | (none) | CORRECT | near-blank page (`raw_text` is just the page-number line "876"), correctly produces no section |
| 957 | (none) | CORRECT | mid-section (804.04 running header, DMS display-characteristics table), no spurious parse |
| 1010 | 808 — FIBER OPTIC CABLE AND INTERCONNECT | CORRECT | page shows end of prior section's payment clause (Section 807) followed by the SECTION 808 heading past the 1,700-char raw_text window; captured `head` begins at `808.01—Description` / opening sentence — pattern matches the verified p.53 case |
| 1064 | (none) | CORRECT | back-matter INDEX page, no heading, no spurious parse |

**20/20 correct.**

## The one quirk: decimal subsection labels are intentionally absorbed, not split

VDOT's book prints two numbering styles on the page:

1. `SECTION NNN—Title` — the true top-level heading, appearing once per section (e.g. p.53:
   `SECTION 103—AWARD AND EXECUTION OF CONTRACTS`, p.1010: `SECTION 808—FIBER OPTIC CABLE AND
   INTERCONNECT`).
2. `NNN.NN—Subtitle` — decimal-numbered labels that look like headings (bold text, em dash,
   own line) but are used throughout the body purely as internal subsection markers within the
   *same* SECTION. Examples directly in the sample set:
   - p.53: `103.01—Consideration of Bids` immediately under the `SECTION 103` banner.
   - p.212: `211.13—Preparation of Mixture` and `211.14—Storage System`, both mid-page with no
     `SECTION` banner on the page — Section 211 started earlier.
   - p.691: `504.04—Measurement and Payment`.
   - p.744: `515.04—Performance Pavement Planing Testing` and `515.05—Measurement and Payment`.

The parser correctly treats only style (1) as a section boundary and folds every style-(2) label
into the running body text of its parent SECTION (e.g., all of `103.01`, `103.02`, `103.03`, …
prose lives inside the single `103` section's `textlen: 18332` blob). This is not a parse defect —
VDOT does not assign these decimal labels independent status as addressable top-level sections the
way AASHTO-decimal states (PA, DE) do; the `SECTION NNN` banner is the only real citation unit in
this book. `total_sections = 160` across 1,065 pages (~6.7 pages/section) is consistent with this
being SECTION-level-only extraction, and the probe's 0% empty/lowercase/absorbed rates confirm no
text is being lost in the process — it is simply attributed to the parent section rather than split
into a child.

One caveat on p.1010: the SECTION 808 heading itself falls just past the 1,700-character raw_text
truncation window supplied by the probe, so it cannot be directly eyeballed in this report. The
captured section (num 808, title "FIBER OPTIC CABLE AND INTERCONNECT", head starting
"808.01—Description...") follows the identical, independently-verified pattern seen in full on
p.53, so this is marked CORRECT on structural consistency grounds rather than a blind reading of
truncated raw text — flagged here for transparency rather than treated as a silent pass.

## Verdict rationale

Per the pass bar (samplesCorrect ≥ 19/20 AND absorbed-title rate low or fully explained AND no real
section text dropped): **samplesCorrect is 20/20**, absorbed-title rate is 0.0% (clean, and the
document's decimal-subsection-labels-as-body-text behavior is a genuine VDOT formatting
characteristic, not a parser fault), and no sampled page shows body text starting mid-sentence,
empty when raw_text shows prose, or a missing/mis-numbered SECTION heading. Mid-section pages
correctly return zero spurious sections throughout. **Verdict: PASS.**

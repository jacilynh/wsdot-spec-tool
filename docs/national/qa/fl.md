# Parse QA — Florida (FDOT FY2026-27), profile `florida_dash`

**Verdict: FAIL**

## Headline numbers

| Metric | Value |
|---|---|
| Total pages | 1,339 |
| Total sections parsed | 6,289 |
| Empty-text sections | 13.8% |
| Lowercase-start sections | 0.7% |
| Absorbed-title rate | 0.0% (0 / 6,289) |
| Profile | `florida_dash` (e.g. `1-1`, `2-2.1`, `105-8`) |
| Samples correct | **12 / 20** |
| Failing sample pages | 266, 400, 668, 936, 1070, 1204, 1271, 1338 |

## Sample-by-sample (20 pages)

| Page | Sections claimed to start here | Verdict | Note |
|---|---|---|---|
| 66 | 6-1.3.2 Contractor Installation Certification: | CORRECT (unverifiable) | heading falls outside the 1,700-char raw_text window; captured text (short, ends "Return to Table of Contents" footer) is not contradicted by anything visible |
| 132 | 102-8; 102-8.1; 102-8.2; 102-9; 102-9.1 | CORRECT | container headings (102-8, 102-9) correctly empty, immediately followed by lettered children with no intervening body; 102-8.1/.2 bodies match raw text exactly |
| 199 | 120-9.4; 120-10; 120-10.1; 120-10.1.1 | CORRECT | 120-9.4 body matches raw; 120-10/120-10.1 are legitimate empty containers (no text between heading and next number in raw_text); 120-10.1.1 body matches raw |
| 266 | 288-11; 288-11.1; 288-11.2 | **INCORRECT** | `288-10.2 Outlet Pipe:` is the literal first text of the page, with a complete one-sentence body ("The quantity of outlet pipe to be paid for will be the length...") visible in raw_text — entirely absent from parsed_sections_starting_here |
| 333 | 337-3 → 337-3.2.1.5; 337-3.2.2 | CORRECT | all visible headings/containers match; note a secondary anomaly at 337-3.2.2 discussed below (not scorable against this page's visible raw_text) |
| 400 | 353-10.1; 353-10.2; 353-11; 353-12 | **INCORRECT** | `353-10 Protection and Opening to Traffic.` is the first heading on the page (2nd line), a container immediately followed by 353-10.1 — completely absent from parsed_sections_starting_here (unlike other same-page containers, which are captured) |
| 467 | 413-3.2.2 → 413-3.4.2 | CORRECT | all visible headings/containers (413-3.3, 413-3.4) match raw text; bodies match exactly |
| 534 | 450-12.3 → 450-12.3.1.4 | CORRECT | container 450-12.3 correctly empty; child bodies match raw text exactly |
| 601 | 455-7.4 → 455-7.7.2 | CORRECT | 455-7.4 boundary correctly starts at "The Engineer will reject..." not absorbing prior paragraph; container 455-7.7 correctly empty |
| 668 | 460-4.7 | **INCORRECT** | `460-4.6 Evaluation of Work:` is the literal first character string of the page, with a full paragraph of body text visible — entirely absent from parsed_sections_starting_here |
| 735 | 510-8; 510-8.1; 510-8.2; 510-8.3; 510-9 | CORRECT | container 510-8 correctly empty; bodies match raw text |
| 802 | 550-6.2; 550-6.3; 550-6.4 | CORRECT | bodies match raw text exactly |
| 869 | 633-1 → 633-2.1.1.2 | CORRECT | `633-1 Description.` sits near the top of the page but is preceded by the `SECTION 633 / COMMUNICATION CABLE` division banner text — correctly captured (control case showing the bug below is position-specific, not a blanket "top of page" failure) |
| 936 | 682-2.4; 682-3; 682-4 | **INCORRECT** | `682-2.3 Installation:` is the first text on the page, with a full-paragraph body — entirely absent from parsed_sections_starting_here |
| 1003 | (none) | CORRECT | Table 901-1 data table, no heading visible, correctly empty |
| 1070 | 933-4.1.2 → 933-5.2.2.2 | **INCORRECT** | `933-4.1.1 Steel Strands and Bars:` is the first text on the page, with a one-sentence body ("Meet the requirements of Section 960.") — entirely absent from parsed_sections_starting_here |
| 1137 | 962-13.4 | CORRECT | table page; only heading appears after the table, correctly captured |
| 1204 | 990-7.1; 990-8; 990-8.1; 990-8.1.1 | **INCORRECT** | `990-7 Temporary Traffic Control Signals.` is the literal first text of the page (container, immediately followed by 990-7.1) — entirely absent, while the later same-page containers 990-8/990-8.1 (not at page top) ARE captured correctly |
| 1271 | 995-11.3.14.1; 995-11.3.14.2; 995-11.4; 995-11.5 | **INCORRECT** | `995-11.3.14 Electrical Requirements:` is the first text on the page, with a full-sentence body — entirely absent from parsed_sections_starting_here |
| 1338 | (none) | **INCORRECT** | `997-16 TMS Managed Field Ethernet Switch.` is the literal first text of the page, with body text ("Meet the requirements of Table 997-32...") — parsed_sections_starting_here is completely empty for this page despite a valid heading + body being visible |

**12 / 20 correct.**

## Blocking defect: section headings at the top of a PDF page are dropped

This is a distinct, reproducible bug, separate from the benign container pattern described below. In every one of the 8 failing samples, the pattern is identical: the section heading is the **first non-whitespace text on the page** (nothing — not even a continuation paragraph — precedes it in raw_text), and the section is **completely absent** from `parsed_sections_starting_here` for that page — not emitted as an empty container, not emitted with truncated text, just gone.

Evidence, direct from probe raw_text:

- **p.266**: raw_text begins `" \n288-10.2 Outlet Pipe: The quantity of outlet pipe to be paid for will be the length, in feet..."` — a complete, self-contained sentence. `parsed_sections_starting_here` starts at `288-11`. `288-10.2` is nowhere in the page's parse output.
- **p.400**: raw_text begins `" \n \n353-10 Protection and Opening to Traffic. \n \n353-10.1 General: ..."` — `353-10` is a container (no text before `353-10.1` begins), structurally identical to dozens of correctly-captured containers elsewhere in the sample (e.g. `102-8`, `120-10`, `288-11`, `337-3`, `510-8`, `633-2`, `990-8` — all captured with `textlen: 0`). But `353-10` itself is missing entirely, while `353-10.1` onward parse fine.
- **p.668**: raw_text begins with zero leading whitespace at `"460-4.6 Evaluation of Work: The Engineer will evaluate and accept materials..."`. Missing entirely; only `460-4.7` (further down the page, beyond the sampled window) is captured.
- **p.936**: raw_text begins `" \n682-2.3 Installation: Do not proceed with any part of the procurement..."`. Missing entirely.
- **p.1070**: raw_text begins `" \n \n933-4.1.1 Steel Strands and Bars: Meet the requirements of Section 960."`. Missing entirely.
- **p.1204**: raw_text begins with zero leading whitespace at `"990-7 Temporary Traffic Control Signals. \n \n990-7.1 General: ..."`. `990-7` missing; but the visually identical container pattern `990-8` / `990-8.1`, which occur later on the *same page* (not at the page top), ARE captured correctly — isolating the trigger to page-top position, not container-vs-content or numbering depth.
- **p.1271**: raw_text begins `" \n \n995-11.3.14 Electrical Requirements: Do not use printed circuit boards..."`. Missing entirely.
- **p.1338**: raw_text begins with zero leading whitespace at `"997-16 TMS Managed Field Ethernet Switch. \n \nMeet the requirements of Table 997-32..."`. `parsed_sections_starting_here` for this page is `[]` — completely empty despite a valid, fully-formed heading + body sitting in the first 100 characters of the page.

The one clean control case in the sample, **p.869**, shows the bug is position-specific rather than a blanket top-of-page failure: `633-1 Description.` sits near the top of the page but is preceded by the `SECTION 633` / `COMMUNICATION CABLE` division-banner text, and is captured correctly. Every failing case has *nothing but whitespace* before the heading. This points to a page-boundary edge case in whatever routine assigns a section to "the page it starts on" — when a heading is the literal first token following a page break, it is dropped rather than attributed to the new page (and there is no evidence in this probe that it survives, misattributed, on the prior page — no such duplication is visible in any sampled page's raw_text or head text).

8 of 20 sampled pages (40%) exhibit this exact failure mode, each with real, non-trivial body prose (payment sentences, requirement clauses, full paragraphs) that is verifiably visible in raw_text and verifiably absent from the parse. In a 1,339-page, densely-sectioned spec document, section boundaries land at page-top essentially at random — this is not a rare edge case, it is a structural bug that is almost certainly dropping a substantial number of sections (plausibly in the hundreds) across the full corpus, silently, with no `textlen: 0` marker to distinguish it from a legitimate empty container.

## Benign quirk (separate from the blocking defect): empty containers

Independent of the bug above, FDOT's `NNN-N` numbering level is frequently used as a bare label introducing a run of deeper subsections, with no prose of its own — the same pattern documented for DelDOT and PennDOT. This is legitimate and correctly handled by the parser **whenever the heading is not at the top of a page**:

```
p.132: 102-8 Driveway Maintenance.        (textlen 0)
       102-8.1 General: Ensure that each residence...

p.333: 337-3 General Composition of Mixes.  (textlen 0)
       337-3.1 General: Use a bituminous mixture...

p.1204: 990-8 Work Zone Signs.              (textlen 0)
        990-8.1 Post Mounted Sign Supports. (textlen 0)
        990-8.1.1 General: Provide steel u-channel posts...
```

Roughly a dozen such containers appear correctly across the 20-page sample (102-8, 102-9, 120-10, 120-10.1, 288-11, 337-3, 337-3.2, 337-3.2.1, 413-3.3, 413-3.4, 450-12.3, 455-7.7, 510-8, 633-2, 633-2.1, 933-5, 933-5.2.2, 990-8, 990-8.1), each immediately followed by a numbered child with no intervening prose in raw_text. This pattern plausibly accounts for a meaningful share of the corpus's 13.8% empty_pct and is not itself a defect. However, it does **not** account for all of it — the page-top bug above produces a different signature (sections missing outright, not present-with-`textlen:0`), so the two phenomena must not be conflated: some of the empty/missing mass is benign containers, and some is the page-boundary bug losing real text.

## Secondary observation (not scored)

On p.333, the captured body of `337-3.2.2 FC-9.5 and FC-12.5:` embeds what looks like an un-split child heading as literal text: `head` begins `"337-3.2.2.1: Aggregates: Use an aggregate blend..."`. Elsewhere in the same document, the equivalent pattern (`337-3.2.1.1 Aggregates:`) is correctly split into its own section. This may indicate the source PDF renders this one heading with a colon immediately after the number (`337-3.2.2.1:` vs `337-3.2.1.1 `), which could be failing the heading-detection regex. The content itself is not lost (it's folded into the parent's body), so this is a numbering-granularity issue rather than data loss, and it falls outside the visible raw_text window for the sampled page, so it isn't counted in the 12/20. Flagging for engineering awareness only.

## Verdict rationale

Per the pass bar (≥19/20 samples correct AND absorbed-title rate low/explained AND no real text dropped): absorbed-title rate is clean (0.0%), and the benign-container explanation for the state's empty-section quirk holds for part of the empty_pct mass. But **samples_correct is 12/20**, well under the 19/20 bar, and — decisively — **real section text is verifiably dropped**: 8 of 20 sampled pages show a section heading with genuine body prose, visible directly in raw_text, that is completely absent from the parse output. This is not a benign container (containers are correctly emitted with `textlen: 0`); it is content silently missing. Per the stated rule, "if real text is lost, verdict is FAIL regardless of the sample count." **Verdict: FAIL.** The `florida_dash` profile needs a fix for section headings that land as the first token on a PDF page before this corpus can be re-submitted for QA.

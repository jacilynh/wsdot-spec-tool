# Parse QA — Maine (MaineDOT, March 2026), profile `section_prefix`

**Verdict: FAIL**

## Headline numbers

| Metric | Value |
|---|---|
| Total pages | 944 |
| Total sections parsed | 146 |
| Empty-text sections | 24.7% (36 / 146) |
| Lowercase-start sections | 0.0% |
| Absorbed-title rate | 0.0% |
| Samples correct | **19 / 20** |
| Profile | `section_prefix` (SECTION-level granularity only — clause numbers like `103.3.3`, `401.17`, `502.041` are body text, not separately addressable sections) |

## Sample-by-sample (20 pages)

| Page | Sections claimed to start here | Verdict | Note |
|---|---|---|---|
| 47 | (none) | CORRECT | mid-clause (103.3.3 Appeal), no SECTION heading on page |
| 94 | (none) | CORRECT | mid-clause (105.10.2), no SECTION heading on page |
| 141 | (none) | CORRECT | mid-section item/price table, no heading |
| 188 | (none) | CORRECT (quirk) | `SECTION 3 - OTHER FEDERAL REQUIREMENTS` visible in raw text but correctly absent — restarted low-numbered federal-provisions series, dropped by the monotonic section-number filter. See quirk section below. |
| 235 | (none) | CORRECT | mid-clause (202.xx removal payment), no heading |
| 282 | (none) | CORRECT | mid-clause (308.04), no heading |
| 329 | (none) | CORRECT | mid-clause (401.17–401.18), no heading |
| 377 | (none) | CORRECT | mid-clause (502.041), no heading |
| 424 | (none) | CORRECT | mid-clause (503.06), no heading |
| 471 | 508 WATERPROOFING MEMBRANE | CORRECT (limited visibility) | `SECTION 508` heading falls just past the 1700-char raw-text truncation (page tail shows end of 507's pay-item table); captured `head` opens cleanly at "508.01 Description – This work shall consist of…", consistent with well-formed openings seen elsewhere on the page |
| 518 | (none) | CORRECT | mid-clause (bearing pot/piston spec), no heading |
| 565 | (none) | CORRECT | mid-clause (gabion assembly, Div. 6 opening), no heading |
| **612** | **(none)** | **INCORRECT** | `SECTION 613 - EROSION CONTROL BLANKETS` is the very first content on the page (immediately after the "6-49" page-number header), followed by five populated subsections (613.01–613.08) — a real, substantial section. It is **not** captured in `parsed_sections_starting_here`. Not explained by the federal-series quirk (613 is a normal, monotonically-increasing Division 600 number, not a restarted low number). See blocking issue below. |
| 660 | (none) | CORRECT | mid-clause (foundation grading/sealer spec), no heading |
| 707 | (none) | CORRECT | mid-clause (sign support fatigue factors), no heading |
| 754 | 659 MOBILIZATION; 660 ON-THE-JOB TRAINING | CORRECT | both `SECTION 659` and `SECTION 660` appear mid-page (after 658's pay-item table) and are both captured cleanly, openings intact |
| 801 | (none) | CORRECT | mid-clause (677.11 backfill placement), no heading |
| 848 | 708 PAINTS AND PRESERVATIVES; 709 REINFORCING STEEL AND WELDED STEEL WIRE FABRIC | CORRECT | both mid-page SECTION headers captured cleanly, openings intact |
| 895 | (none) | CORRECT | mid-clause (cabinet testing requirements), no heading |
| 943 | (none) | CORRECT | back-matter index page, no heading |

**19 / 20 correct** — the sole failure is page 612 (see below), which is a confirmed real-content miss, not a benign quirk.

## The documented quirk: restarted federal-provisions SECTION series dropped by the monotonic filter

Maine's book embeds a "Federal Contract Provisions Supplement" (Appendix A, printed folio `A-13` on page 188) that **restarts its own SECTION numbering at 1**, independent of the main document's SECTION 100s/500s/600s/700s sequence. Page 188's raw text shows this directly:

```
End of GOALS FOR EMPLOYMENT OF FEMALES AND MINORITIES
Federally Required Contract Document
D.  Section 'D Disadvantaged Business Enterprise (DBE) Requirements' is
    removed in its entirety. The DBE material is in: Section 105.10 - Equal
    Opportunity and Civil Rights.
SECTION 3 - OTHER FEDERAL REQUIREMENTS
Unless expressly otherwise provided in the Bid Documents, the provisions contained in
this Section 3 of this "Federal Contract Provisions Supplement" are hereby incorporated...
```

By this point the main document has already emitted sections in the 100s (e.g., 103, 105) and will go on to emit 200s–900s later in the book. Because the parser's `section_prefix` extraction enforces a monotonically increasing SECTION number, `SECTION 3` (and presumably the preceding `SECTION 1`/`SECTION 2` of the same restarted federal series) falls below the running high-water mark and is correctly excluded from `parsed_sections_starting_here` — it is filtered as noise rather than mis-numbered into the main sequence. This is the state-specific quirk called out in the review brief: a legitimate, structural characteristic of MaineDOT's federal-provisions appendix, not a parser defect, **provided** the underlying prose is still retrievable as body text of whatever section it landed inside (this sample cannot confirm that either way — see below).

This quirk plausibly accounts for some fraction of the corpus's 36 empty/dropped sections, but the 20-page sample did not directly land on any of the other restarted-series pages, so its full extent across the 146-section corpus is not independently confirmed here.

## Blocking issue: SECTION 613 (EROSION CONTROL BLANKETS) is missing, not explained by the quirk

Page 612's raw text opens, immediately after the page-number header, with:

```
SECTION 613 - EROSION CONTROL BLANKETS
613.01  Description - This work shall consist of furnishing and installing erosion control
        blankets on previously prepared areas...
613.02  Materials - Erosion control blanket shall conform to the requirements specified...
613.03  Site Preparation - The area for erosion control blankets shall be prepared as follows...
613.04  Seeding - All seed shall be sown before installing erosion control blankets...
613.05  Installation - On Slopes and in ditches, blankets shall be aligned...
613.08  Method of Measurement - Erosion control blanket will be measured...
```

This is unambiguously a real SECTION heading with substantial following body text (five-plus populated subsections), not a divider page and not a restarted low number — 613 sits in normal increasing order inside Division 600 (the sample immediately before it, page 565, is already in the 601 area; the sample immediately after, page 660, is deeper in Division 600 at ~foundation specs). Nothing about it resembles the federal-series quirk.

`parsed_sections_starting_here` for page 612 is empty. Two explanations are possible from this sample alone, and this review cannot distinguish between them:

1. **Genuine drop** — Section 613 never enters the corpus under its own number, and its prose is lost to anyone citing "Section 613."
2. **Misattribution** — the heading and body text got silently folded into the tail of whatever section preceded it (e.g., 612 or an earlier 600-series section), so the prose survives somewhere but is unreachable/mis-cited under the wrong section number.

Either way this is a live defect against the QA criteria: "every section heading visible in raw_text is captured with the correct number and title" fails outright for this page, and per the review brief's instruction, a real-content miss overrides the numeric sample-pass threshold. The parser demonstrably handles the general case correctly elsewhere in this same sample set — `SECTION 659`/`660` (page 754) and `SECTION 708`/`709` (page 848) both appear mid-page and are captured cleanly — so this is not a systemic "SECTION headers never work" failure, but it is at least one confirmed, unexplained miss, and the 20-page sample has no way to bound how many similar misses exist across the other 926 pages.

## Open item: 24.7% empty-section rate not directly verified

The review brief specifically calls for evidence on whether the 24.7% empty-section rate (36/146) is benign (a SECTION header immediately followed by another SECTION header/divider page, or the restarted federal series) or real text loss. None of the 20 sampled pages happened to land on a section with `textlen: 0` — every section actually captured in this sample (508, 659, 660, 708, 709) has substantial non-zero text. This review can document the federal-series mechanism as one plausible contributor (see above) but **cannot confirm with page-level evidence** that the remaining empty sections are benign. Combined with the confirmed page-612 miss, this is treated as an unresolved risk rather than assumed-safe.

## Verdict rationale

Per the pass bar (samples correct ≥ 19/20 AND absorbed-title rate low/explained AND no real section text dropped): the sample count (19/20) technically clears the numeric bar, and the absorbed-title rate is clean (0.0%). However, page 612 is a **confirmed, unexplained loss of a real SECTION heading with substantial body content** — not covered by the one documented quirk (the restarted federal series) — and the corpus's 24.7% empty-section rate could not be verified as benign from the sample. Per explicit instruction, a real text-fidelity defect overrides the sample-count threshold. **Verdict: FAIL.**

**Required before re-review:** confirm whether Section 613's content (and any other similarly-affected sections) is fully retrievable from the corpus under its correct section number, or fix the boundary-detection miss and re-probe.

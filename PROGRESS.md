# DOTcompass — progress

_Last updated 2026-07-19._

Free public compliance/reference tool over U.S. state DOT construction specifications, by
Katabatic Engineering. Live at **dotcompass.dev** (Washington). One codebase, cluster
parsers, per-state descriptors, a reuse gate that keeps uncleared text out of production.

## Where it stands

- **19 states in the app registry** — WA (live, public) + 18 local-only demos:
  nd, de, id, mo, pa · co, tn, va, fl, me · ne, oh, sc, ms, wv, ri, md, in.
- **No blocked states remain.** Every state that was started and hit an obstacle is built
  and adversarial-QA-passed. ~31 tier-2/tier-null states are still `pending` (not started).
- **Per-state status:** `docs/national/status.json`. **Playbook:** `docs/national/AGENT_PLAYBOOK.md`.

## Accomplished (this session)

- **Three build waves through the supervised-fleet pipeline** (Stage 0 source-verify →
  Stage 1 parse → Stage 2 adversarial QA → Stage 3 descriptor + local build): Wave 1
  (nd/de/id/mo/pa), Wave 2 (co/tn/va/fl/me + in), Wave 3 (ne/oh/sc/ms/wv/ri + md).
  Adversarial QA repeatedly caught real defects that section counts missed.
- **7 cluster parser profiles** covering every numbering scheme encountered:
  `wsdot_hyphen`, `aashto_decimal`, `florida_dash`, `section_prefix`, `aashto_dash`,
  `letter_prefix` (RIDOT), `letter_prefix_reverse` (MDOT SHA).
- **Two shared-engine capabilities**, both additive and regression-gated:
  - header-band fix — don't strip a heading that opens at the top of a page in a book with
    no running header (recovered FL/ME).
  - `text_fixup` hook — per-state repair for a broken PDF text layer; `deshift_indot`
    un-scrambles INDOT's font-offset (+29) glyphs.
- **The reuse gate held throughout:** every non-WA state is `may_publish=False`, built only
  under `--allow-uncleared`, gitignored, and excluded from production (generalized
  `purge_uncleared.py`). Source PDFs are never committed.
- **The WSDOT 2,235-section corpus regression passed 11/11 on every merge** that touched
  shared code. `tsc` clean at 19 states (synthetic int division bands, no app change).
- **Commit attribution fixed** — all history rewritten to author `jacilynh`, no AI trailers;
  repo identity set so it stays that way.

## What's left

Per-state buildout:
- **Waves 4+: ~31 pending tier-2/tier-null states** (al, az, ca, ga, il, ny, tx, …). Not
  blocked — just not started; the cluster library likely covers most.

Non-parsing tracks (Opus-led, not fleet work):
- **App-scaling picker** — the header dropdown was built for ~7 states; at 19 it needs a
  searchable/grouped picker (flagged in the Wave 2 retro; `docs/national/ADR-multi-state-app.md`).
- **Reuse-clearance track** — only WA is `public`; every other state is build-only pending a
  human reuse decision + DOT outreach (Stage 4 dossiers, `docs/national/reuse/`).
- **P1/P2 features across built states** — requirements explorer (per-state party vocab),
  then semantic search + multi-state Ask (the Worker is still WSDOT-corpus-specific).
- **P3 history** — needs the `align.py` cross-edition alignment layer (not built); pilot on
  FL/MO/ND.

Known minor follow-ups: MDOT SHA book edition label (2025 vs 2026), an FDOT page-spanning
footer-boilerplate leak (cosmetic), and division names for the numeric-band states (currently
honest numeric labels where the book prints none).

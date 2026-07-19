# Wave 2 retro

**Roster:** FL, IN (playbook "hard capabilities") + CO, TN, VA, ME (tier-1).
**Outcome:** 5 of 6 built (CO, TN, VA, FL, ME); IN deferred. Two new cluster profiles and
one shared-engine fix landed, all green against the 2,235-section WSDOT regression.

## What we learned

1. **The catalog's cluster label is unreliable beyond `aashto_decimal` — always probe.**
   Wave 2 predicted "Florida = new dash cluster" and nothing else, but Stage 1 found **three**
   of six weren't `aashto_decimal`: FL (`florida_dash`), VA and ME (`section_prefix`). IN was
   labeled per-division but serves a single combined PDF. The parse probe (section count +
   monotonicity + division spread) is the source of truth; the catalog is a lead. Two new
   clusters now exist and cover more states than just these three.

2. **Books with no running header are a distinct failure mode — now fixed at the engine.**
   `detect_bands` stripped any line at the modal top-margin y. FDOT and MaineDOT print no
   running header, so a section heading that opens at the top of a page sat at that y and was
   deleted (FL 8/20 pages, ME p612). The fix validates that a band is a *separated* margin
   line before trusting it. Lesson for future waves: a top-ratio near 1.0 (top line flows
   into the body) means no running header — spot-check top-of-page headings.

3. **Stage 2 adversarial QA is load-bearing — it caught what Stage 1 could not.**
   FL passed Stage 1 (coherent 6,289-section count, monotonic) but was dropping ~290 real
   sections; only reading pages against raw text surfaced it. Same for IN (one font-corrupted
   heading) and ME (p612). Keep Stage 2 independent of Stage 1 and adversarial.

4. **New defer category: source-PDF font corruption.** INDOT's text layer is partially
   Caesar-shifted (`(TXLSPHQW` = `Equipment`); headings/body on those pages are unreadable and
   dropped. Not a parser bug. Needs a ToUnicode/OCR decode step or a documented deferral.

5. **Divisions: most books DO print names.** CO, FL, ME printed division titles (used
   verbatim); TN and VA didn't (honest numeric bands). The North Dakota rule held up.

## Process fixes (apply in Wave 3)

- **Serialize the corpus regression.** Running it concurrently with 6+ state parses starved
  both (one 8-min run took 26 min). Run the WSDOT regression alone.
- **No nested `&` in a backgrounded command without `wait`** — the child orphans and the log
  is empty. Run the command directly as the background task, or end with `wait`.
- **Verify probe freshness.** A stale/errored probe regen silently left pre-fix output;
  always confirm the corpus stat (e.g. section count) matches the current engine before QA.

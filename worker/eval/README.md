# Ask eval harness

Measures the quality of the "Ask the Specs" pipeline against a gold set of questions, so
changes to retrieval, the reranker, or the prompt can be judged by numbers instead of vibes.
Adapted from the Atli query project's retrieval eval.

## Run it

```bash
make eval                 # retrieval recall — FREE, no API key. The fast inner-loop metric.
make eval ARGS=--rerank   # + the reranker's lift (Recall@6 reranked + MRR). Needs ANTHROPIC_API_KEY.
make eval ARGS=--answer   # + end-to-end against the live Worker: citation accuracy + refusal.
```

- **retrieval** (default): loads the live corpus, runs BM25, reports **Recall@24** (did the
  right section make the candidate set?) and **Recall@6** (did it survive to the answer step
  without reranking?). Free and instant — run it on every retrieval/prompt change.
- **--rerank**: also runs the Haiku reranker and reports **Recall@6 (reranked)** and **MRR**,
  so you can see how much reranking improves the final six sections. A few cheap Haiku calls.
- **--answer**: hits the deployed Worker for the full pipeline and checks whether each answer
  actually **cites** an expected section, and whether **out-of-scope** questions are correctly
  refused / marked low confidence. Costs real (capped) spend — run sparingly.

Each mode exits non-zero below its threshold (`RECALL_THRESHOLD`, `CITATION_THRESHOLD` in
`run.ts`), so it can gate changes in CI.

## The gold set (`cases.ts`)

Each case is a question plus `expect`: section-number **prefixes**, any of which counts as a
hit (so `["1-08.6"]` matches `1-08.6(2)`, and a family prefix `["8-01"]` matches any `8-01.x`).
`outOfScope` cases have no expected section — the right behavior is to refuse.

**This is a starter set — extend it.** Adding a case is a few lines, so every "Ask got this
wrong" becomes a permanent regression test. When you add a case, confirm the expected section
against the section index (the eval itself will tell you if your label is wrong — that is how
three labels in the first run got corrected).

## Baseline (first run, 16 answerable + 3 out-of-scope cases)

| Metric | Result |
|---|---|
| Recall@24 (BM25 candidates) | 94% (15/16) |
| Recall@6 (lexical, rerank off) | 88% (14/16) |
| Citation accuracy (end-to-end) | 94% (15/16) |
| Refusal on out-of-scope | 67% (2/3) |

Known gaps this surfaced, worth tracking:

- **`materials-on-hand`** — BM25 misses §1-09.8 because the question ("materials delivered but
  not yet installed") shares no rare terms with the section ("Payment for Material on Hand").
  A classic lexical vocab gap; the Worker correctly returns **low confidence** rather than a
  confident wrong answer. This is the strongest argument for adding semantic retrieval later.
- **`structural-concrete`** — §6-02 sits at lexical rank 11 but the **reranker recovers it**
  into the final six; a clean demonstration of why the rerank stage exists.
- **`oos-human-remains`** — answered confidently instead of refusing, because WSDOT *does*
  address archaeological/cultural finds (§1-07.16). The label, not the model, is likely wrong
  here — a good reminder to verify gold against the manual.

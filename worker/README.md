# Ask-the-Specs Worker

A small Cloudflare Worker that answers questions about the WSDOT Standard Specifications,
grounded strictly in the real section text. It is the only server this project has.

## What it does

1. Accepts a **question** (a string, nothing else — never a document).
2. Retrieves the most relevant specification chunks from a cached corpus (`ask-corpus.json`,
   emitted by the build). Retrieval runs here, so the endpoint can't be steered into
   summarizing text a caller supplies.
3. Asks **Claude Haiku 4.5** to answer using only those chunks, citing sections inline.
4. Records the cost against a **hard monthly spend cap**. When the cap is hit it returns
   `{ capped: true }` and the site falls back to keyword search — it never overspends and
   never fails silently.

The API key is a Cloudflare **secret**. It is never in this repo, in `wrangler.toml`, or in
any client code.

## Cost

Haiku 4.5 is about **$1 per million input tokens and $5 per million output**. A question
retrieves ~8 short sections (~2–3k input tokens) and answers in a few hundred — roughly
**half a cent per question**. The `MONTHLY_CAP_USD` var (default `30`) is the ceiling; the
Worker stops calling the model once it's reached.

## Develop

```bash
npm install
npm test          # unit tests for retrieval, prompt building, cost, validation
npm run typecheck
cp .dev.vars.example .dev.vars   # then put your real key in .dev.vars (git-ignored)
npm run dev       # local Worker at http://localhost:8787
```

The end-to-end request path (Cloudflare bindings + a live API call) is only exercised
against a real deployment — the unit tests cover the logic that doesn't need the network.

## Deploy

You need a Cloudflare account and an Anthropic API key.

```bash
# 1. Log in
npx wrangler login

# 2. Create the spend-counter KV namespace, then paste the printed id into wrangler.toml
npx wrangler kv namespace create SPEND

# 3. Store your API key as a secret (never committed)
npx wrangler secret put ANTHROPIC_API_KEY

# 4. Set ALLOWED_ORIGIN / CORPUS_URL in wrangler.toml to your deployed site, then:
npx wrangler deploy
```

Deploy prints the Worker URL. Point the site at it and rebuild:

```bash
# from the repo root
cd app
VITE_ASK_URL="https://wsdot-ask-the-specs.<you>.workers.dev" npm run build
```

Until `VITE_ASK_URL` is set, the site's **Ask** page works in keyword-search-only mode, so
the feature degrades rather than breaks.

## Notes and limits

- **Rate limiting** uses Cloudflare's native binding (`[[unsafe.bindings]]` in
  `wrangler.toml`). If your account doesn't have it, delete that block — the Worker skips
  rate limiting gracefully when the binding is absent.
- **Abuse is bounded by the spend cap.** A public, keyless endpoint can be hammered; the
  per-IP rate limit slows that and the hard monthly cap makes the worst case "keyword
  search for the rest of the month," never a surprise bill.
- **Retrieval is keyword-based**, not semantic — good for questions phrased in the domain's
  vocabulary. Precomputed-embedding retrieval is a planned upgrade.

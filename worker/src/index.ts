/**
 * "Ask the Specs" — a stateless Cloudflare Worker that answers questions about the WSDOT
 * Standard Specifications, grounded strictly in the real section text.
 *
 * Flow: validate the question -> rate-limit the caller -> retrieve the most relevant
 * sections from a cached corpus -> check the monthly spend cap -> ask Claude Haiku to
 * answer using ONLY those sections, with citations -> record the cost.
 *
 * Design commitments (see PLAN.md):
 *   - It accepts a QUESTION only. It never receives a user's document. Retrieval happens
 *     here, over public specification text, so the endpoint can't be steered into
 *     summarizing arbitrary supplied text.
 *   - The API key is a Cloudflare secret, never in the repo or in client code.
 *   - A hard monthly spend cap makes overspending impossible: when it's reached the
 *     Worker returns `capped`, and the client falls back to keyword search — it never
 *     fails silently and never keeps spending.
 */

import Anthropic from "@anthropic-ai/sdk";

import {
  MAX_TOKENS,
  MODEL,
  SYSTEM_PROMPT,
  buildUserMessage,
  citedSections,
  estimateCostUsd,
  validateQuestion,
} from "./rag";
import { type Chunk, type PreparedChunk, prepare, retrieve } from "./retrieval";

interface Env {
  ANTHROPIC_API_KEY: string; // secret: wrangler secret put ANTHROPIC_API_KEY
  SPEND: KVNamespace; // monthly cost counter
  RATE_LIMITER?: RateLimit; // optional native rate-limit binding
  CORPUS_URL: string; // where to fetch ask-corpus.json
  ALLOWED_ORIGIN: string; // the site origin permitted to call this Worker
  MONTHLY_CAP_USD: string; // hard spend ceiling, e.g. "30"
}

const TOP_K = 8; // sections given to the model as evidence

// Cached across requests within a warm isolate — the corpus is fetched at most once per
// isolate, not per request. A promise guards concurrent first requests.
let corpusPromise: Promise<PreparedChunk[]> | null = null;

function loadCorpus(url: string): Promise<PreparedChunk[]> {
  if (!corpusPromise) {
    corpusPromise = fetch(url)
      .then((res) => {
        if (!res.ok) throw new Error(`corpus fetch failed (${res.status})`);
        return res.json() as Promise<Chunk[]>;
      })
      .then(prepare)
      .catch((err) => {
        corpusPromise = null; // let a later request retry a transient failure
        throw err;
      });
  }
  return corpusPromise;
}

function monthKey(): string {
  return `spend:${new Date().toISOString().slice(0, 7)}`; // spend:YYYY-MM
}

async function spentThisMonth(env: Env): Promise<number> {
  return Number((await env.SPEND.get(monthKey())) ?? "0");
}

async function recordSpend(env: Env, usd: number): Promise<void> {
  const key = monthKey();
  const next = (Number((await env.SPEND.get(key)) ?? "0") + usd).toFixed(6);
  // Expire a couple of months out so old counters clean themselves up.
  await env.SPEND.put(key, next, { expirationTtl: 70 * 24 * 3600 });
}

function cors(origin: string): Record<string, string> {
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    Vary: "Origin",
  };
}

function json(body: unknown, status: number, headers: Record<string, string>): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...headers },
  });
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const headers = cors(env.ALLOWED_ORIGIN);

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers });
    if (request.method !== "POST") return json({ error: "POST only" }, 405, headers);

    // 1. Validate the request — a question string, nothing else.
    let body: { question?: unknown };
    try {
      body = await request.json();
    } catch {
      return json({ error: "invalid JSON" }, 400, headers);
    }
    const check = validateQuestion(body.question);
    if (!check.ok) return json({ error: check.reason }, 400, headers);
    const question = (body.question as string).trim();

    // 2. Rate-limit by client IP, if the binding is configured.
    if (env.RATE_LIMITER) {
      const ip = request.headers.get("CF-Connecting-IP") ?? "anon";
      const { success } = await env.RATE_LIMITER.limit({ key: ip });
      if (!success) {
        return json({ error: "rate limited", retryAfter: 60 }, 429, headers);
      }
    }

    // 3. Retrieve the most relevant sections. No match -> a grounded "not found", and no
    //    model call at all (retrieval is free; generation is not).
    let corpus: PreparedChunk[];
    try {
      corpus = await loadCorpus(env.CORPUS_URL);
    } catch {
      return json({ error: "corpus unavailable" }, 503, headers);
    }
    const chunks = retrieve(corpus, question, TOP_K);
    if (chunks.length === 0) {
      return json(
        { answer: "I could not find anything about that in the specifications.", citations: [], sections: [] },
        200,
        headers,
      );
    }

    // 4. Enforce the hard monthly spend cap BEFORE spending anything.
    const cap = Number(env.MONTHLY_CAP_USD || "0");
    if (cap > 0 && (await spentThisMonth(env)) >= cap) {
      return json({ capped: true }, 200, headers);
    }

    // 5. Ask Claude to answer using only the retrieved sections.
    const supplied = [...new Set(chunks.map((c) => c.section))];
    let answer: string;
    let cost = 0;
    try {
      const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
      const message = await client.messages.create({
        model: MODEL,
        max_tokens: MAX_TOKENS,
        system: SYSTEM_PROMPT,
        messages: [{ role: "user", content: buildUserMessage(question, chunks) }],
      });
      answer = message.content
        .filter((b): b is Anthropic.TextBlock => b.type === "text")
        .map((b) => b.text)
        .join("")
        .trim();
      cost = estimateCostUsd(message.usage.input_tokens, message.usage.output_tokens);
    } catch (err) {
      // Never fail silently: log server-side for debugging (wrangler tail) and tell the
      // client so it can fall back to keyword search — without leaking internals.
      console.error("generation failed:", err);
      return json({ error: "generation failed" }, 502, headers);
    }

    // 6. Record what we spent, then answer with citations the client can link.
    await recordSpend(env, cost);
    return json(
      { answer, citations: citedSections(answer, supplied), sections: supplied, model: MODEL },
      200,
      headers,
    );
  },
};

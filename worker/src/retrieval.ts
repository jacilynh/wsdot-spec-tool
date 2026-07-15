/**
 * Keyword retrieval over the specification chunks, run inside the Worker.
 *
 * The Worker does its own retrieval — the client sends only a question — so the endpoint
 * can never be steered to summarize arbitrary text a caller supplies. Grounding always
 * comes from the real specifications.
 *
 * This is deliberately simple term-overlap scoring, not embeddings: it needs no model at
 * query time, runs in a couple of milliseconds over ~11k chunks, and is good enough for
 * questions phrased in the domain's own vocabulary. Semantic retrieval is a planned
 * upgrade; this is the honest, dependency-free baseline.
 */

export interface Chunk {
  section: string;
  text: string;
}

export interface PreparedChunk extends Chunk {
  words: Set<string>;
}

export interface ScoredChunk extends Chunk {
  score: number;
}

// Common words carry no retrieval signal and would match almost everything.
const STOPWORDS = new Set(
  ("the a an and or of to in for on at by with as is are be shall must will this that " +
    "it its which when where all any each from within into per not no such other than " +
    "may can under over between if then so").split(" "),
);

/** Lowercased alphanumeric tokens of length >= 3, minus stopwords. */
export function tokenize(text: string): string[] {
  return (text.toLowerCase().match(/[a-z0-9]+/g) ?? []).filter(
    (t) => t.length >= 3 && !STOPWORDS.has(t),
  );
}

/** Precompute each chunk's word set once, so retrieval is a set lookup per query term. */
export function prepare(corpus: Chunk[]): PreparedChunk[] {
  return corpus.map((c) => ({ ...c, words: new Set(tokenize(c.text)) }));
}

/**
 * The top `k` chunks for a question, scored by how many distinct query terms they
 * contain. Rarer query terms are worth more (a light IDF), so a question's specific noun
 * outweighs its common verb. Returns fewer than `k` when little matches, and nothing when
 * nothing does — the caller treats an empty result as "not in the specifications".
 */
export function retrieve(prepared: PreparedChunk[], question: string, k: number): ScoredChunk[] {
  const terms = [...new Set(tokenize(question))];
  if (terms.length === 0) return [];

  // Light IDF: a term in few chunks is more discriminating than one in many.
  const docFreq = new Map<string, number>();
  for (const term of terms) {
    let n = 0;
    for (const chunk of prepared) if (chunk.words.has(term)) n++;
    docFreq.set(term, n);
  }
  const total = prepared.length;
  const weight = (term: string) => Math.log((total + 1) / ((docFreq.get(term) ?? 0) + 1));

  const scored: ScoredChunk[] = [];
  for (const chunk of prepared) {
    let score = 0;
    for (const term of terms) if (chunk.words.has(term)) score += weight(term);
    if (score > 0) scored.push({ section: chunk.section, text: chunk.text, score });
  }
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, k);
}

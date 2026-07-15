/**
 * The prompt, guardrails, and cost accounting for grounded question answering — kept as
 * pure functions so they can be tested without an API key or network.
 */

import type { ScoredChunk } from "./retrieval";

export const MODEL = "claude-haiku-4-5";
export const MAX_TOKENS = 1024;

// Haiku 4.5 pricing (USD per million tokens). Used for the hard monthly spend cap.
const INPUT_PER_MTOK = 1.0;
const OUTPUT_PER_MTOK = 5.0;

export const SYSTEM_PROMPT = [
  "You answer questions about the WSDOT Standard Specifications (M 41-10) using ONLY the",
  "numbered specification sections provided in the user message. Rules:",
  "- Base every statement solely on the provided sections. Never use outside knowledge.",
  "- Cite the section you rely on inline, in square brackets, e.g. [1-09.7]. Cite often.",
  "- If the provided sections do not contain the answer, say so plainly — for example,",
  '  "I could not find that in the provided sections" — and suggest browsing the manual.',
  "- Be concise and precise. This is a reference, not a chat. Do not speculate.",
  "- You are unofficial and advisory; remind the reader to verify against the manual when",
  "  the question is consequential.",
].join("\n");

/** Assemble the user message: the question, then the retrieved sections as evidence. */
export function buildUserMessage(question: string, chunks: ScoredChunk[]): string {
  const evidence = chunks
    .map((c) => `[${c.section}]\n${c.text}`)
    .join("\n\n---\n\n");
  return `Question: ${question}\n\nSpecification sections:\n\n${evidence}`;
}

/** Section numbers the model cited that were actually among the ones we supplied. */
export function citedSections(answer: string, supplied: string[]): string[] {
  const allowed = new Set(supplied);
  const cited = new Set<string>();
  for (const m of answer.matchAll(/\[(\d-\d{2}(?:\.\d+)?(?:\([0-9A-Za-z]+\))*[A-Z]?)\]/g)) {
    if (allowed.has(m[1]!)) cited.add(m[1]!);
  }
  return [...cited];
}

/** Cost of one call in USD, from the response usage. Drives the spend cap. */
export function estimateCostUsd(inputTokens: number, outputTokens: number): number {
  return (inputTokens * INPUT_PER_MTOK + outputTokens * OUTPUT_PER_MTOK) / 1_000_000;
}

export interface QuestionCheck {
  ok: boolean;
  reason?: string;
}

/** A question must be a non-empty, reasonably short string — nothing document-sized. */
export function validateQuestion(value: unknown): QuestionCheck {
  if (typeof value !== "string") return { ok: false, reason: "question must be a string" };
  const q = value.trim();
  if (q.length < 3) return { ok: false, reason: "question is too short" };
  if (q.length > 500) return { ok: false, reason: "question is too long (500 char max)" };
  return { ok: true };
}

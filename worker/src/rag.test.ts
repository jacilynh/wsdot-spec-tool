import { describe, expect, it } from "vitest";

import { buildUserMessage, citedSections, estimateCostUsd, validateQuestion } from "./rag";

describe("validateQuestion", () => {
  it("accepts a normal question", () => {
    expect(validateQuestion("What is mobilization?").ok).toBe(true);
  });

  it("rejects non-strings, empties, and document-sized input", () => {
    expect(validateQuestion(42).ok).toBe(false);
    expect(validateQuestion("  ").ok).toBe(false);
    expect(validateQuestion("x".repeat(501)).ok).toBe(false);
  });
});

describe("buildUserMessage", () => {
  it("includes the question and each section as labelled evidence", () => {
    const msg = buildUserMessage("What is mobilization?", [
      { section: "1-09.7", text: "Mobilization consists of preconstruction expenses.", score: 2 },
    ]);
    expect(msg).toContain("Question: What is mobilization?");
    expect(msg).toContain("[1-09.7]");
    expect(msg).toContain("preconstruction expenses");
  });
});

describe("citedSections", () => {
  it("returns only the cited sections that were actually supplied", () => {
    const answer = "Mobilization is defined in [1-09.7], not [9-99.9].";
    expect(citedSections(answer, ["1-09.7", "1-07.1"])).toEqual(["1-09.7"]);
  });

  it("deduplicates repeated citations", () => {
    expect(citedSections("[1-07.1] and again [1-07.1]", ["1-07.1"])).toEqual(["1-07.1"]);
  });

  it("is empty when the model cited nothing supplied", () => {
    expect(citedSections("I could not find that.", ["1-09.7"])).toEqual([]);
  });
});

describe("estimateCostUsd", () => {
  it("prices Haiku 4.5 at $1/MTok in and $5/MTok out", () => {
    // 10k input + 1k output = 10000*1e-6 + 1000*5e-6 = 0.01 + 0.005 = 0.015
    expect(estimateCostUsd(10_000, 1_000)).toBeCloseTo(0.015, 6);
  });

  it("is zero for no usage", () => {
    expect(estimateCostUsd(0, 0)).toBe(0);
  });
});

import { describe, expect, it } from "vitest";

import { prepare, retrieve, tokenize } from "./retrieval";

const CORPUS = [
  { section: "1-09.7", text: "Mobilization consists of preconstruction expenses and the cost of moving equipment." },
  { section: "1-07.1", text: "The Contractor shall comply with all Federal, State, and local laws." },
  { section: "8-20.3", text: "Traffic signal systems shall be installed as shown in the Plans." },
  { section: "9-03.1", text: "Fine aggregate for concrete shall be manufactured from ledge rock." },
];

describe("tokenize", () => {
  it("lowercases, drops stopwords and short tokens", () => {
    expect(tokenize("The Contractor shall comply with laws")).toEqual([
      "contractor",
      "comply",
      "laws",
    ]);
  });
});

describe("retrieve", () => {
  const prepared = prepare(CORPUS);

  it("finds the section that matches the question's terms", () => {
    const hits = retrieve(prepared, "what does mobilization cost include?", 3);
    expect(hits[0]?.section).toBe("1-09.7");
  });

  it("ranks by how many distinct query terms match", () => {
    const hits = retrieve(prepared, "traffic signal installation", 4);
    expect(hits[0]?.section).toBe("8-20.3");
  });

  it("returns nothing when no meaningful term matches", () => {
    // Only stopwords and unrelated words -> empty, which the caller reads as "not found".
    expect(retrieve(prepared, "the and of with", 5)).toEqual([]);
    expect(retrieve(prepared, "helicopter avionics telemetry", 5)).toEqual([]);
  });

  it("respects the k limit", () => {
    const hits = retrieve(prepared, "shall concrete aggregate signal laws", 2);
    expect(hits.length).toBeLessThanOrEqual(2);
  });

  it("weights a rare term above a common one", () => {
    // "contractor" appears in three chunks (common, low weight); "material" in one (rare,
    // high weight). A chunk matching only the rare term must outrank one matching only the
    // common term.
    const idf = prepare([
      { section: "1-01", text: "the contractor performs the work" },
      { section: "1-02", text: "the contractor submits the forms" },
      { section: "1-03", text: "the contractor is responsible" },
      { section: "9-01", text: "material sampling procedures" },
    ]);
    const hits = retrieve(idf, "contractor material", 4);
    expect(hits[0]?.section).toBe("9-01");
  });
});

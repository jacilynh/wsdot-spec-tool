import { describe, expect, it } from "vitest";

import { splitCitations } from "./ask";

describe("splitCitations", () => {
  it("turns bracketed section numbers into citation segments", () => {
    const segs = splitCitations("Mobilization is in [1-09.7] of the manual.");
    expect(segs).toEqual([
      { text: "Mobilization is in " },
      { cite: "1-09.7" },
      { text: " of the manual." },
    ]);
  });

  it("handles multiple citations and complex numbers", () => {
    const segs = splitCitations("See [8-21.3(9)F] and [1-07.1].");
    expect(segs.filter((s) => "cite" in s)).toEqual([{ cite: "8-21.3(9)F" }, { cite: "1-07.1" }]);
  });

  it("returns a single text segment when there are no citations", () => {
    expect(splitCitations("I could not find that.")).toEqual([{ text: "I could not find that." }]);
  });

  it("does not treat ordinary bracketed text as a citation", () => {
    expect(splitCitations("[see note]")).toEqual([{ text: "[see note]" }]);
  });
});

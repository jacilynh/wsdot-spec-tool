/**
 * The Ask eval gold set: questions with the WSDOT section(s) a good answer should ground in.
 *
 * `expect` holds section-number PREFIXES — a retrieved/cited section counts as a hit when it
 * starts with any of them (so "1-08.6" and "1-08.6(2)" both satisfy expect ["1-08.6"], and a
 * family-level expect like "8-01" is satisfied by any 8-01.x chunk). Prefixes keep the gold
 * robust to sub-section granularity without being so broad they can't discriminate.
 *
 * `outOfScope` cases have no expected section: the correct behavior is to refuse / return low
 * confidence rather than invent an answer. They only matter in the end-to-end (--answer) mode.
 *
 * This is a STARTER set — extend it. The whole point of the harness is that adding a case is
 * cheap, so every "Ask got this wrong" becomes a regression test. Run `make eval` after any
 * change to retrieval, the reranker, or the prompt.
 */

export interface EvalCase {
  id: string;
  question: string;
  expect: string[];
  outOfScope?: boolean;
}

export const CASES: EvalCase[] = [
  // --- Division 1: general requirements (the most-asked, most load-bearing) ---
  {
    id: "suspension-of-work",
    question: "When can the Engineer suspend the work, and does the contractor get paid for the delay?",
    expect: ["1-08.6"],
  },
  {
    id: "mobilization-payment",
    question: "What does mobilization payment cover and when is it paid?",
    expect: ["1-09.6", "2-01.5"],
  },
  {
    id: "materials-on-hand",
    question: "How is the contractor paid for materials delivered to the site but not yet installed?",
    expect: ["1-09.8"],
  },
  {
    id: "progress-schedule",
    question: "What progress schedule is the contractor required to submit?",
    expect: ["1-08.3"],
  },
  {
    id: "liquidated-damages",
    question: "How are liquidated damages for late completion calculated?",
    expect: ["1-08.9"],
  },
  {
    id: "protest-procedure",
    question: "What is the procedure for the contractor to protest a decision?",
    expect: ["1-04.5"],
  },
  {
    id: "changed-conditions",
    question: "What happens if differing site conditions are discovered during the work?",
    expect: ["1-04.7"],
  },
  {
    id: "prosecution-progress",
    question: "What are the rules about working days and the prosecution of the work?",
    expect: ["1-08"],
  },
  // --- Traffic control ---
  {
    id: "temporary-traffic-control",
    question: "What are the requirements for temporary traffic control and flaggers?",
    expect: ["2-04"],
  },
  // --- Earthwork / erosion ---
  {
    id: "erosion-sediment-control",
    question: "What are the requirements for temporary erosion and sediment control?",
    expect: ["8-01"],
  },
  {
    id: "roadway-excavation",
    question: "How is roadway excavation and embankment measured and paid?",
    expect: ["3-03"],
  },
  {
    id: "clearing-grubbing",
    question: "What does clearing and grubbing include?",
    expect: ["3-01"],
  },
  // --- Structures / materials ---
  {
    id: "structural-concrete",
    question: "What are the requirements for placing and curing structural concrete?",
    expect: ["6-02"],
  },
  {
    id: "pile-driving",
    question: "What are the requirements for driving piles?",
    expect: ["6-05"],
  },
  {
    id: "hma-compaction",
    question: "How is hot mix asphalt compaction and density controlled?",
    expect: ["5-04"],
  },
  {
    id: "beam-guardrail",
    question: "What are the installation requirements for beam guardrail?",
    expect: ["8-11"],
  },

  // --- Out of scope: correct behavior is to refuse / low confidence (not in M 41-10) ---
  {
    id: "oos-human-remains",
    question: "If I uncover human remains or an old grave while excavating, what am I legally required to do?",
    expect: [],
    outOfScope: true,
  },
  {
    id: "oos-prevailing-wage-rate",
    question: "What is the current prevailing wage rate for an ironworker in King County?",
    expect: [],
    outOfScope: true,
  },
  {
    id: "oos-weather-forecast",
    question: "Will it rain on my paving project next Tuesday?",
    expect: [],
    outOfScope: true,
  },
  {
    // Clearly foreign — nothing in the manuals is close. The similarity floor should make
    // semantic contribute nothing here, so the worker refuses. (Contrast the weather case,
    // whose content genuinely overlaps the manuals and can clear the floor.)
    id: "oos-unrelated",
    question: "What is the best pizza restaurant in Seattle?",
    expect: [],
    outOfScope: true,
  },
];

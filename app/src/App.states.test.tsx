// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { Index, SectionText } from "./types";

// A North-Dakota-shaped index: AASHTO numbering, numeric-band divisions, history OFF, and
// no requirements block — exactly what build_state.py emits for a single, uncleared edition.
const ND_INDEX: Index = {
  stats: {
    everPublished: 540,
    live: 540,
    vacant: 0,
    sinceStart: 540,
    newInLatest: 0,
    revisions: 0,
    editions: [2025],
    latest: 2025,
    earliest: 2025,
  },
  divisions: [
    { n: 100, title: "100-199 Series" },
    { n: 200, title: "200-299 Series" },
  ],
  removed: {},
  meta: {
    slug: "nd",
    state: "North Dakota",
    dot: "NDDOT",
    historyEnabled: false,
    reuse: "unstated",
    uncleared: true,
    sourceUrl: "https://example.gov/nd.pdf",
    sourceNote: "Unofficial copy; reuse terms unstated.",
  },
  sections: [
    { num: "105.01", division: 100, title: "GENERAL", vacant: false },
    { num: "106.02", division: 100, title: "AGGREGATE SOURCES", vacant: false },
  ],
};

const ND_TEXT: Record<string, SectionText> = {
  "105.01": { title: "GENERAL", text: "The Engineer will decide all questions.", vacant: false, page: 54 },
};

vi.mock("./lib/api", () => ({
  getIndex: () => Promise.resolve(ND_INDEX),
  getDivisionText: () => Promise.resolve(ND_TEXT),
  getDivisionHistory: () => Promise.resolve({}),
  getDivisionRequirements: () => Promise.resolve([]),
}));

const { App } = await import("./App");

afterEach(cleanup);

/** Render at a path, then switch the jurisdiction to North Dakota via the header control. */
async function renderAsNorthDakota(path: string) {
  const view = render(
    <MemoryRouter initialEntries={[path]}>
      <App />
    </MemoryRouter>,
  );
  const switcher = await screen.findByLabelText(/jurisdiction/i);
  fireEvent.change(switcher, { target: { value: "nd" } });
  return view;
}

describe("App — North Dakota (second state)", () => {
  it("renders a browse/search home, not the history framing", async () => {
    await renderAsNorthDakota("/");
    expect(await screen.findByText(/made searchable/i)).toBeInTheDocument();
    // The WSDOT history-forward headline must NOT appear for a history-off state.
    expect(screen.queryByText(/A specification section is not a fact/i)).not.toBeInTheDocument();
    // Divisions use honest numeric-band labels, not invented AASHTO titles.
    expect(screen.getAllByText(/100-199 Series/).length).toBeGreaterThan(0);
  });

  it("hides Ask and Requirements from the nav when the state can't back them", async () => {
    await renderAsNorthDakota("/");
    await screen.findByText(/made searchable/i);
    expect(screen.getByRole("link", { name: "Browse" })).toBeInTheDocument();
    expect(screen.queryByRole("link", { name: "Ask" })).not.toBeInTheDocument();
    expect(screen.queryByRole("link", { name: "Requirements" })).not.toBeInTheDocument();
  });

  it("shows a section's current text with no history column", async () => {
    await renderAsNorthDakota("/section/105.01");
    expect(await screen.findByRole("heading", { name: "105.01" })).toBeInTheDocument();
    expect(screen.getByText(/The Engineer will decide all questions/)).toBeInTheDocument();
    // A history-off state renders no history aside (<aside> = complementary role).
    expect(screen.queryByRole("complementary")).not.toBeInTheDocument();
  });

  it("lands gracefully on a requirements deep link instead of crashing", async () => {
    await renderAsNorthDakota("/requirements");
    expect(await screen.findByText(/isn.t available for North Dakota/i)).toBeInTheDocument();
  });
});

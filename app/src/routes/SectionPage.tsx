import { Link, useParams } from "react-router-dom";

import { DISCLAIMER } from "../config";
import { Timeline } from "../components/Timeline";
import { VacantBadge } from "../components/badges";
import { getDivisionHistory, getDivisionText } from "../lib/api";
import { paragraphs } from "../lib/format";
import { useIndex } from "../lib/indexContext";
import { divisionOf } from "../lib/sectionNumber";
import { useAsync } from "../lib/useAsync";
import { useActiveState } from "../states";
import type { SectionHistory } from "../types";

/**
 * One section: its current text, and — for a state with a processed multi-edition archive —
 * its full history alongside. The division is taken from the index (the numbering scheme
 * differs per state), and text/history for that division are lazy-loaded here. States
 * without history (e.g. North Dakota, single edition) show the text alone.
 */
export function SectionPage() {
  const { num = "" } = useParams();
  const index = useIndex();
  const state = useActiveState();

  const entry = index.sections.find((s) => s.num === num);
  // The index carries each section's division; fall back to the WSDOT number format only
  // for a removed section that is no longer in the index (WSDOT-only case).
  const division = entry?.division ?? divisionOf(num);

  const text = useAsync(() => getDivisionText(division), [division]);
  const history = useAsync(
    () =>
      state.history
        ? getDivisionHistory(division)
        : Promise.resolve({} as Record<string, SectionHistory>),
    [division, state.history],
  );

  const section = text.data?.[num];
  const sectionHistory = state.history ? history.data?.[num] : undefined;
  const { prev, next } = useNeighbors(num);

  if (text.loading || history.loading) {
    return <p className="py-16 text-center text-muted">Loading {num}…</p>;
  }
  if (!section && !sectionHistory) {
    return (
      <div className="py-16 text-center">
        <p className="text-muted">
          Section <span className="font-mono">{num}</span> was not found in the current edition.
        </p>
        <Link to="/browse" className="mt-3 inline-block text-accent hover:underline">
          Browse the specifications
        </Link>
      </div>
    );
  }

  return (
    <article className="space-y-8">
      <header className="border-b border-border pb-5">
        <div className="flex items-center gap-3 text-sm text-muted">
          <Link to={`/browse?division=${division}`} className="hover:text-ink">
            Division {division}
          </Link>
        </div>
        <div className="mt-1 flex flex-wrap items-center gap-3">
          <h1 className="font-mono text-2xl font-semibold text-ink">{num}</h1>
          <span className="text-2xl font-semibold text-ink">
            {section?.title || sectionHistory?.title || "Vacant"}
          </span>
          {section?.vacant && <VacantBadge />}
        </div>
        {sectionHistory && (
          <p className="mt-2 text-sm text-muted">
            In the specifications from {sectionHistory.firstSeen} to {sectionHistory.lastSeen}.
          </p>
        )}
      </header>

      <div className={`grid gap-10 ${state.history ? "lg:grid-cols-[1fr_24rem]" : ""}`}>
        <section>
          <h2 className="mb-3 text-sm font-medium uppercase tracking-wider text-faint">
            Current text · {index.stats.latest} edition
          </h2>
          {section && !section.vacant ? (
            <div className="prose-spec max-w-reading">
              {paragraphs(section.text).map((p, i) => (
                <p key={i}>{p}</p>
              ))}
            </div>
          ) : (
            <p className="rounded-lg border border-vacated/30 bg-vacated/5 p-4 text-sm text-muted">
              This section is <strong className="text-vacated">Vacant</strong> in the{" "}
              {index.stats.latest} edition — the number is reserved but carries no text. Anything
              still citing it for substance is out of date.
            </p>
          )}
          <p className="mt-6 max-w-reading text-xs leading-5 text-faint">{DISCLAIMER}</p>
        </section>

        {state.history && (
          <aside className="lg:border-l lg:border-border lg:pl-8">
            <h2 className="mb-4 text-sm font-medium uppercase tracking-wider text-faint">
              History · {index.stats.earliest}–{index.stats.latest}
            </h2>
            {sectionHistory ? (
              <Timeline history={sectionHistory} />
            ) : (
              <p className="text-sm text-faint">No recorded history.</p>
            )}
          </aside>
        )}
      </div>

      <nav className="flex justify-between border-t border-border pt-5 text-sm">
        {prev ? (
          <Link to={`/section/${prev}`} className="text-accent hover:underline">
            ← {prev}
          </Link>
        ) : (
          <span />
        )}
        {next ? (
          <Link to={`/section/${next}`} className="text-accent hover:underline">
            {next} →
          </Link>
        ) : (
          <span />
        )}
      </nav>
    </article>
  );
}

/** Previous / next section within the same division, in the index's book order. */
function useNeighbors(num: string): { prev?: string; next?: string } {
  const { sections } = useIndex();
  const entry = sections.find((s) => s.num === num);
  if (!entry) return {};
  const ordered = sections.filter((s) => s.division === entry.division).map((s) => s.num);
  const i = ordered.indexOf(num);
  if (i === -1) return {};
  return { prev: ordered[i - 1], next: ordered[i + 1] };
}

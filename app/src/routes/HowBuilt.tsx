import { Link } from "react-router-dom";

import { useIndex } from "../lib/indexContext";

/**
 * The making-of. A central goal of this project is to show what's now possible, so the
 * story of building it is a first-class page — told honestly, including where the data and
 * the methods are weak.
 */
export function HowBuilt() {
  const { stats, requirements } = useIndex();
  return (
    <div className="mx-auto max-w-reading space-y-8">
      <header>
        <h1 className="text-2xl font-semibold text-ink">How this was built</h1>
        <p className="mt-2 leading-7 text-muted">
          One person, working with an AI coding assistant. The site is static and costs almost
          nothing to run: the heavy work happens once, ahead of time, and what you load is plain
          files. Everything here — the pipeline, the app, and the tests — is open source and meant
          to be forked for other agencies’ spec books.
        </p>
      </header>

      <Step n={1} title="Read 26 years of PDFs">
        WSDOT publishes each edition of the specifications as a PDF. This project gathers all{" "}
        {stats.editions.length} of them, from {stats.earliest} to {stats.latest}, and extracts every
        section — the number, the title, and the full text.
        <p className="mt-3">
          That sounds routine and isn’t. Only a handful of the editions ship a usable table of
          contents; the rest have almost none. And across 26 years nearly everything about the
          layout changed — the page size, the heading font (one era’s heading font doesn’t even
          contain the word “bold”), and whether a section’s number and title share a line or sit on
          two. So the parser <em>measures</em> each book instead of assuming, and defends against two
          traps that each quietly destroyed most of a book before being caught: numbering that
          restarts partway through, and a single stray table cell that could truncate everything
          after it.
        </p>
      </Step>

      <Step n={2} title="Reconstruct every section’s history">
        With all editions parsed, each section’s life is assembled by comparing consecutive
        editions: when it first appeared, every time its wording changed (and by how much), and
        whether it was ever struck or removed — <strong className="text-ink">
          {stats.revisions.toLocaleString()}
        </strong>{" "}
        tracked revisions across{" "}
        <strong className="text-ink">{stats.everPublished.toLocaleString()}</strong> sections. That’s
        the <Link to="/section/1-09.7" className="text-accent hover:underline">Section History</Link>{" "}
        view — the thing the printed book, which only shows you today, can’t tell you.
      </Step>

      <Step n={3} title="Pull out the requirements">
        Every “shall”, “must”, and “is required” statement — {requirements.total.toLocaleString()} of
        them — is extracted verbatim and tagged by who is bound and what it’s about, feeding the{" "}
        <Link to="/requirements" className="text-accent hover:underline">Requirements</Link> index.
        This is deliberately rule-based, not AI-generated: the entries are exact quotes, so there’s
        nothing to hallucinate. The same choice underlies the{" "}
        <Link to="/scan" className="text-accent hover:underline">draft checker</Link>, which flags
        any section number in your text that points to a struck or removed section — running entirely
        in your browser, so the draft never leaves your machine.
      </Step>

      <Step n={4} title="Add search that understands meaning">
        On top of instant keyword matching, the{" "}
        <Link to="/search?q=stormwater%20pollution%20prevention" className="text-accent hover:underline">
          search
        </Link>{" "}
        runs a small language model <em>in your browser</em> to find sections by meaning — so “who
        inspects welds on bridges” finds “Welding Inspection” even though the words don’t match. The
        section text was turned into vectors ahead of time with the same model, and both the model
        and its runtime are served from this site, so nothing is sent anywhere and it works on
        locked-down machines.
      </Step>

      <Step n={5} title="Answer questions, grounded and cited">
        The optional <Link to="/ask" className="text-accent hover:underline">Ask</Link> feature takes
        a plain-English question, finds the relevant sections, and has an AI model answer using only
        those sections — citing each one so you can click through and check. It won’t use outside
        knowledge, and if the answer isn’t in the specifications it says so. It’s the one part with a
        tiny server (a cost-capped cloud function); everything else is plain static files.
      </Step>

      <div className="rounded-lg border border-vacated/30 bg-vacated/5 p-4">
        <h2 className="font-medium text-ink">Where it’s still weak — stated plainly</h2>
        <p className="mt-2 text-sm leading-6 text-muted">
          The pre-2010 editions parse least reliably; that data is flagged as lower-confidence
          wherever it appears. The requirement classifier is right about who’s bound roughly 90% of
          the time. Search understands meaning but isn’t a lawyer, and the AI answers are advisory.
          A tool whose whole point is that it doesn’t bluff shouldn’t bluff about its own limits —
          so always verify anything that matters against the published manual.
        </p>
      </div>
    </div>
  );
}

function Step({ n, title, children }: { n: number; title: string; children: React.ReactNode }) {
  return (
    <section className="flex gap-4">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent font-mono text-sm font-semibold text-accent-ink">
        {n}
      </div>
      <div>
        <h2 className="mb-1 text-lg font-semibold text-ink">{title}</h2>
        <div className="leading-7 text-muted">{children}</div>
      </div>
    </section>
  );
}

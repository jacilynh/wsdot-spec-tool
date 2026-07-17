import { Link } from "react-router-dom";

/**
 * Shown when a feature is reached (usually by direct URL) for a state whose data can't back
 * it — the requirements explorer or Ask, for a state with no requirements/ask files. The
 * nav already hides these links per state; this is the graceful landing for a deep link.
 */
export function FeatureUnavailable({ feature, stateName }: { feature: string; stateName: string }) {
  return (
    <div className="mx-auto max-w-reading py-16 text-center">
      <h1 className="text-xl font-semibold text-ink">
        {feature} isn’t available for {stateName}
      </h1>
      <p className="mt-2 text-sm leading-6 text-muted">
        This feature needs data that hasn’t been generated for {stateName}. Try Browse or Search, or
        switch jurisdictions from the header.
      </p>
      <Link to="/browse" className="mt-4 inline-block text-accent hover:underline">
        Browse the specifications →
      </Link>
    </div>
  );
}

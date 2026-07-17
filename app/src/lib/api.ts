import { getActiveState } from "../states";
import type { Index, Requirement, SectionHistory, SectionText } from "../types";

/**
 * Data access. Everything is static JSON under `public/data/<state>`, fetched relative to
 * the deployed base so the same build works at a domain root or a Pages subpath. The active
 * state's `dataBase` selects which state's data is served (e.g. "data" or "data/nd"). Each
 * fetched file is cached in memory for the session, keyed by full URL so states cache
 * separately — the index once per state, and each division's text/history when opened.
 */

const cache = new Map<string, Promise<unknown>>();

function load<T>(path: string): Promise<T> {
  const url = `${import.meta.env.BASE_URL}${getActiveState().dataBase}/${path}`;
  let pending = cache.get(url) as Promise<T> | undefined;
  if (!pending) {
    pending = fetch(url).then((res) => {
      if (!res.ok) throw new Error(`Failed to load ${path} (${res.status})`);
      return res.json() as Promise<T>;
    });
    // Don't cache a rejected fetch — a transient failure should be retryable.
    pending.catch(() => cache.delete(url));
    cache.set(url, pending);
  }
  return pending;
}

export const getIndex = () => load<Index>("index.json");

export const getDivisionText = (division: number) =>
  load<Record<string, SectionText>>(`sections/${division}.json`);

export const getDivisionHistory = (division: number) =>
  load<Record<string, SectionHistory>>(`history/${division}.json`);

export const getDivisionRequirements = (division: number) =>
  load<Requirement[]>(`requirements/${division}.json`);

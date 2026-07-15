import { useEffect, useState, type ReactNode } from "react";
import { NavLink, useLocation } from "react-router-dom";

import { DISCLAIMER, PUBLISHER, SITE_NAME } from "../config";
import { ThemeToggle } from "./ThemeToggle";

const NAV = [
  { to: "/", label: "Home", end: true },
  { to: "/ask", label: "Ask" },
  { to: "/browse", label: "Browse" },
  { to: "/requirements", label: "Requirements" },
  { to: "/scan", label: "Check a draft" },
  { to: "/how-it-was-built", label: "How it was built" },
  { to: "/about", label: "About" },
];

export function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col overflow-x-clip">
      <Header />
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8 sm:px-6">{children}</main>
      <Footer />
    </div>
  );
}

function Header() {
  const [open, setOpen] = useState(false);
  const { pathname } = useLocation();

  // Close the mobile menu whenever navigation happens.
  useEffect(() => setOpen(false), [pathname]);

  return (
    <header className="sticky top-0 z-20 border-b border-border bg-surface/90 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center gap-4 px-4 py-3 sm:px-6">
        <NavLink to="/" className="flex items-baseline gap-2">
          <span className="text-lg font-semibold tracking-tight text-ink">{SITE_NAME}</span>
          <span className="hidden text-xs font-medium uppercase tracking-wider text-faint sm:inline">
            Unofficial
          </span>
        </NavLink>

        {/* Desktop: the full nav row, shown only at widths where it fits. */}
        <nav className="ml-auto hidden items-center gap-1 lg:flex">
          {NAV.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.end} className={navLinkClass}>
              {item.label}
            </NavLink>
          ))}
          <ThemeToggle />
        </nav>

        {/* Mobile: theme toggle + a button that opens the links below the header. */}
        <div className="ml-auto flex items-center gap-2 lg:hidden">
          <ThemeToggle />
          <button
            type="button"
            onClick={() => setOpen((o) => !o)}
            className="rounded-md border border-border bg-raised px-3 py-1.5 text-sm text-muted transition-colors hover:text-ink"
            aria-expanded={open}
            aria-controls="mobile-menu"
            aria-label={open ? "Close menu" : "Open menu"}
          >
            {open ? "✕ Close" : "Menu"}
          </button>
        </div>
      </div>

      {open && (
        <nav id="mobile-menu" className="border-t border-border bg-surface px-4 py-2 lg:hidden" aria-label="Main">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `block rounded-md px-3 py-2.5 text-sm transition-colors ${
                  isActive
                    ? "bg-raised font-medium text-ink"
                    : "text-muted hover:bg-raised hover:text-ink"
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      )}
    </header>
  );
}

function navLinkClass({ isActive }: { isActive: boolean }): string {
  return `rounded-md px-2.5 py-1.5 text-sm transition-colors ${
    isActive ? "font-medium text-ink" : "text-muted hover:text-ink"
  }`;
}

function Footer() {
  return (
    <footer className="border-t border-border bg-surface">
      <div className="mx-auto max-w-6xl px-4 py-6 text-sm sm:px-6">
        <p className="text-muted">
          A free tool from <span className="font-medium text-ink">{PUBLISHER}</span>.
        </p>
        <p className="mt-1 max-w-reading text-xs leading-5 text-faint">{DISCLAIMER}</p>
      </div>
    </footer>
  );
}

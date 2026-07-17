"""Scheme-independent parsing engine plus one profile per numbering cluster.

The engine (`engine.py`) knows how to turn a spec PDF into a section tree using only
typography and ordering — no table of contents, nothing about any one state hardcoded.
What *is* state-specific — the section-number pattern, the book's sort order, how a
number maps to a division — lives in a `SpecProfile` (`profiles.py`), one per numbering
cluster (`clusters/`). `engine.parse(pdf, profile)` combines the two.

See `docs/national/ARCHITECTURE.md` for the full design.
"""

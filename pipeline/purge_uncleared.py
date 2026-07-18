#!/usr/bin/env python3
"""Remove uncleared states' built data from an output root before a publishing build.

    uv run --with pymupdf python3 pipeline/purge_uncleared.py <out_root> [--dry-run]

The reuse gate has two halves. build_state.py refuses to EMIT an uncleared state's text
(unless --allow-uncleared is passed for a local demo). But once a state has been built
locally for a demo, its data sits in <out_root>/<slug>/ - and `npm run build` copies the
whole public dir into dist/. This is the second half of the gate: before a production build,
delete every uncleared state's data dir so uncleared text can never reach dist/ and deploy.

"Uncleared" is derived from the descriptors (reuse != public), so this stays correct as
states are added - there is nothing to hand-maintain (the old Makefile hardcoded only `nd`).
"""

import argparse
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_state import STATES, load_descriptor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("out_root", help="data root to purge, e.g. app/public/data")
    parser.add_argument(
        "--dry-run", action="store_true", help="list what would be removed, delete nothing"
    )
    args = parser.parse_args()

    would_remove, removed = [], []
    for slug in STATES:
        if load_descriptor(slug).may_publish_text:
            continue  # cleared for redistribution - keep it
        data_dir = os.path.join(args.out_root, slug)
        if not os.path.isdir(data_dir):
            continue
        would_remove.append(slug)
        if not args.dry_run:
            shutil.rmtree(data_dir)
            removed.append(slug)

    if args.dry_run:
        print(
            f"[dry-run] uncleared data present in {args.out_root}: {would_remove or '(none)'}"
        )
    else:
        print(f"purged uncleared data from {args.out_root}: {removed or '(none present)'}")


if __name__ == "__main__":
    main()

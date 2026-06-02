"""Regenerate CSV files and theme summary from the (updated) tagged JSONL.

Run after pass2_adjustments.py to keep all outputs in sync.
"""
from __future__ import annotations
import json
from pathlib import Path

import tag_corpus as tc

ROOT = Path(__file__).resolve().parent
PUBS_JSONL = ROOT / "publications_tagged.jsonl"
PROJ_JSONL = ROOT / "projects_tagged.jsonl"


def load(path: Path) -> list[dict]:
    rows = []
    with path.open() as f:
        for line in f:
            rows.append(json.loads(line))
    return rows


def main():
    pubs = load(PUBS_JSONL)
    projs = load(PROJ_JSONL)

    tc.write_pubs_csv(tc.PUBS_OUT_CSV, pubs)
    tc.write_proj_csv(tc.PROJ_OUT_CSV, projs)

    summary = tc.compute_summary(pubs, projs)
    tc.write_summary(tc.THEME_SUMMARY_CSV, summary)
    # report stats
    tc.report_stats("Publications (post pass-2)", pubs)
    tc.report_stats("Projects (post pass-2)", projs)
    meta_pubs = [p for p in pubs if p.get("is_meta")]
    print(f"  META pubs: {len(meta_pubs)}")
    print(f"  Substantive pubs: {sum(1 for p in pubs if p['in_substantive_corpus'])}")
    print(f"  Substantive projects: {sum(1 for p in projs if p['in_substantive_corpus'])}")


if __name__ == "__main__":
    main()

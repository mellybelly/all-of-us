#!/usr/bin/env python3
"""Objective collaboration & reuse signals in the AoU workspace corpus.

All metrics are directly computed from the public workspace directory feed
(team composition, institution diversity, workspace duplication). Descriptive
only — no editorializing.

Output: collaboration_evidence.csv (metric, value, denom, pct).
"""
from __future__ import annotations
import json, csv, collections, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAND = HERE.parent / "aou-research-landscape"
SRC = LAND / "projects.jsonl"


def main():
    n = 0
    team_sizes = collections.Counter()
    n_insts = collections.Counter()
    multi_owner = multi_inst = 0
    titles = collections.Counter()
    dup_of = 0
    roles = collections.Counter()
    for line in SRC.open():
        d = json.loads(line); n += 1
        owners = (d.get("team") or {}).get("owner") or []
        team_sizes[len(owners)] += 1
        if len(owners) > 1:
            multi_owner += 1
        insts = {o.get("institution") for o in owners if o.get("institution")}
        n_insts[len(insts)] += 1
        if len(insts) > 1:
            multi_inst += 1
        for o in owners:
            if o.get("role"):
                roles[o["role"]] += 1
        title = (d.get("title") or "").strip().lower()
        titles[title] += 1
        if title.startswith("duplicate of"):
            dup_of += 1

    dup_workspaces = sum(c - 1 for c in titles.values() if c > 1)
    rows = [
        ("total_workspaces", n, n, 100.0),
        ("solo_workspaces (1 owner)", team_sizes[1], n, 100 * team_sizes[1] / n),
        ("multi_owner_workspaces (>=2)", multi_owner, n, 100 * multi_owner / n),
        ("team_>=5_owners", sum(v for k, v in team_sizes.items() if k >= 5), n,
         100 * sum(v for k, v in team_sizes.items() if k >= 5) / n),
        ("multi_institution_workspaces", multi_inst, n, 100 * multi_inst / n),
        ("duplicate_title_workspaces (case-folded)", dup_workspaces, n,
         100 * dup_workspaces / n),
        ("titles_starting_'duplicate of'", dup_of, n, 100 * dup_of / n),
    ]
    with (HERE / "collaboration_evidence.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "count", "denominator", "pct"])
        for m, c, dn, p in rows:
            w.writerow([m, c, dn, round(p, 1)])

    print("Collaboration / reuse signals (AoU workspace directory):")
    for m, c, dn, p in rows:
        print(f"  {m:42} {c:>7} / {dn} = {p:4.1f}%")
    print("\nTeam-size distribution:")
    for k in sorted(team_sizes)[:9]:
        print(f"  {k} owners: {team_sizes[k]}")
    print("\nMean owners/workspace:",
          round(sum(k * v for k, v in team_sizes.items()) / n, 2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Build a stratified sample of pubs + filtered projects for taxonomy discovery.

Emits two text files:
  taxonomy_sample_discovery.txt  — 200 records for initial discovery
  taxonomy_sample_validation.txt — a different 100 records for validation
"""

import json
import random
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
random.seed(42)


def trunc(s, n=600):
    s = (s or "").strip()
    return (s[:n] + "...") if len(s) > n else s


def fmt_pub(p):
    title = (
        p.get("manual_title") or p.get("pdr_title") or p.get("calc_title") or ""
    ).strip()
    abstract = (
        p.get("manual_abstract") or p.get("pdr_abstract") or p.get("calc_abstract") or ""
    ).strip()
    year = (p.get("pdr_date_year") or "").strip()
    journal = (
        p.get("manual_journal_title") or p.get("pdr_journal_title") or ""
    ).strip()
    foci = []
    for f in ("common_focus", "rare_focus", "maternal_focus", "aging_focus", "behavioral_focus",
              "environmental_focus", "genetic_focus", "population_health_focus"):
        if str(p.get(f) or p.get(f"manual_{f}") or "").strip() == "1":
            foci.append(f.replace("_focus", ""))
    return (
        f"PUB | PMID:{p.get('pubmed_id','')} | {year} | {journal}\n"
        f"  Title: {title}\n"
        f"  Foci: {', '.join(foci) if foci else '(none)'}\n"
        f"  Abstract: {trunc(abstract, 800)}\n"
    )


def fmt_proj(p):
    return (
        f"PROJECT | workspace:{p.get('workspaceId','')} | tier:{p.get('accessTier','')}\n"
        f"  Title: {(p.get('title') or '').strip()}\n"
        f"  Purposes: {'; '.join(p.get('purposes') or [])}\n"
        f"  Question: {trunc(p.get('questions'), 500)}\n"
        f"  Approach: {trunc(p.get('approaches'), 400)}\n"
        f"  Findings: {trunc(p.get('findings'), 400)}\n"
    )


def stratified_pubs(pubs, n):
    by_year = defaultdict(list)
    for p in pubs:
        y = (p.get("pdr_date_year") or "").strip() or "unknown"
        by_year[y].append(p)
    # Weight: roughly proportional to count, but ensure at least 1 from each year w/ >=10 records
    sampled = []
    total = sum(len(v) for v in by_year.values())
    for y, group in sorted(by_year.items()):
        share = round(n * len(group) / total)
        if len(group) >= 10 and share == 0:
            share = 1
        random.shuffle(group)
        sampled.extend(group[:share])
    return sampled[:n]


def stratified_projs(projs, n):
    # Stratify by access tier + UBR focus
    buckets = defaultdict(list)
    for p in projs:
        key = (p.get("accessTier"), bool(p.get("ubrFocus")))
        buckets[key].append(p)
    sampled = []
    total = sum(len(v) for v in buckets.values())
    for key, group in buckets.items():
        share = max(1, round(n * len(group) / total))
        random.shuffle(group)
        sampled.extend(group[:share])
    random.shuffle(sampled)
    return sampled[:n]


def main():
    pubs = [json.loads(l) for l in open(HERE / "publications.jsonl")]
    projs = [json.loads(l) for l in open(HERE / "projects_filtered.jsonl")]

    # Discovery: 100 pubs + 100 projects
    disc_pubs = stratified_pubs(pubs, 100)
    disc_projs = stratified_projs(projs, 100)
    disc_ids = {p.get("pubmed_id") or p.get("record_id") for p in disc_pubs} | {
        p.get("workspaceId") for p in disc_projs
    }

    # Validation: a different 50 pubs + 50 projects
    val_pubs = [p for p in stratified_pubs(pubs, 200) if (p.get("pubmed_id") or p.get("record_id")) not in disc_ids][:50]
    val_projs = [p for p in stratified_projs(projs, 200) if p.get("workspaceId") not in disc_ids][:50]

    with open(HERE / "taxonomy_sample_discovery.txt", "w") as fh:
        fh.write(f"=== DISCOVERY SAMPLE: {len(disc_pubs)} pubs + {len(disc_projs)} projects ===\n\n")
        fh.write("--- PUBLICATIONS ---\n\n")
        for p in disc_pubs:
            fh.write(fmt_pub(p) + "\n")
        fh.write("\n--- PROJECTS ---\n\n")
        for p in disc_projs:
            fh.write(fmt_proj(p) + "\n")

    with open(HERE / "taxonomy_sample_validation.txt", "w") as fh:
        fh.write(f"=== VALIDATION SAMPLE: {len(val_pubs)} pubs + {len(val_projs)} projects ===\n\n")
        fh.write("--- PUBLICATIONS ---\n\n")
        for p in val_pubs:
            fh.write(fmt_pub(p) + "\n")
        fh.write("\n--- PROJECTS ---\n\n")
        for p in val_projs:
            fh.write(fmt_proj(p) + "\n")
    print(f"Wrote discovery ({len(disc_pubs)}+{len(disc_projs)}) and validation ({len(val_pubs)}+{len(val_projs)}) samples")


if __name__ == "__main__":
    main()

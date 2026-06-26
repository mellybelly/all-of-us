#!/usr/bin/env python3
"""Year-windowed UKB full-census pull.

A single all-years esearch truncates at NCBI's ~9,999-per-WebEnv idlist
cap, so we split the query into year windows (each well under the cap) and
union the PMIDs to retrieve the complete UKB corpus (~11.9k pubs). Year
windows also give a clean pre-2023 vs post-2023 split for the trend
analysis. Windows are uncapped (10000 is just the per-call ceiling).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from acquire import (
    EUTILS,
    RAW,
    ROOT,
    _loads_esearch,
    efetch_batch,
    http_get,
    parse_pubmed_xml,
)
import urllib.parse

UKB_BASE = '"UK Biobank"[Title/Abstract] AND humans[MeSH Terms] AND Journal Article[Publication Type]'

# Year windows, UNCAPPED for a full census. NCBI's esearch idlist is hard-
# capped near 9,999 returns per WebEnv, so a single all-years query truncates;
# splitting into year windows (each well under 10k) lets us pull every pub.
# The 10000 per-window value is just the per-call safety ceiling. Windows are
# kept narrow in the high-volume recent years so none approaches the cap.
WINDOWS = [
    ("2007:2018", 10000),
    ("2019:2020", 10000),
    ("2021:2021", 10000),
    ("2022:2022", 10000),
    ("2023:2023", 10000),
    ("2024:2024", 10000),
    ("2025:2026", 10000),
]


def esearch_for_window(date_range: str, retmax: int):
    """date_range like '2019:2020' — pulled into [DP] Date-Publication."""
    query = f'{UKB_BASE} AND ({date_range}[DP])'
    pmids = []
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": str(min(retmax, 10000)),
        "usehistory": "y",
    }
    url = f"{EUTILS}/esearch.fcgi?{urllib.parse.urlencode(params)}"
    data = _loads_esearch(url)
    res = data.get("esearchresult", {})
    pmids.extend(res.get("idlist", []))
    count = int(res.get("count", 0))
    web_env = res.get("webenv")
    query_key = res.get("querykey")
    while len(pmids) < min(count, retmax) and web_env:
        params = {
            "db": "pubmed",
            "WebEnv": web_env,
            "query_key": query_key,
            "retmode": "json",
            "retmax": "10000",
            "retstart": str(len(pmids)),
            "usehistory": "y",
        }
        url = f"{EUTILS}/esearch.fcgi?{urllib.parse.urlencode(params)}"
        data = _loads_esearch(url)
        new_ids = data.get("esearchresult", {}).get("idlist", [])
        if not new_ids:
            break
        pmids.extend(new_ids)
        time.sleep(0.4)
    return pmids[:retmax], count


def main():
    all_pmids = []
    seen = set()
    for window, cap in WINDOWS:
        print(f"\nWindow {window} (cap {cap})", flush=True)
        cache = RAW / f"ukb_pmids_{window.replace(':','_')}.txt"
        if cache.exists():
            pmids = [ln.strip() for ln in cache.read_text().splitlines() if ln.strip()]
            print(f"  cached {len(pmids)} pmids", flush=True)
        else:
            pmids, total = esearch_for_window(window, cap)
            cache.write_text("\n".join(pmids) + "\n")
            print(f"  fetched {len(pmids)} / total {total}", flush=True)
        for p in pmids:
            if p not in seen:
                seen.add(p)
                all_pmids.append(p)

    print(f"\nTotal unique PMIDs: {len(all_pmids)}", flush=True)
    out_pmids = RAW / "ukb_pmids.txt"
    out_pmids.write_text("\n".join(all_pmids) + "\n")

    # Clear and rebuild jsonl
    pubs_jsonl = ROOT / "ukb_pubs.jsonl"
    # Remove any partial cache and refetch from year-stratified PMIDs.
    # First, identify which efetch batches need to be re-fetched. Easiest:
    # delete old efetch caches that don't match new PMIDs, then re-batch.
    # For simplicity, re-batch all here against the new PMID list.
    # Clear old cache to avoid stale-index mismatches.
    for old in RAW.glob("ukb_efetch_*.xml"):
        old.unlink()

    batch = 200
    all_pubs = []
    for i in range(0, len(all_pmids), batch):
        chunk = all_pmids[i : i + batch]
        cache_path = RAW / f"ukb_efetch_{i:06d}.xml"
        xml_bytes = efetch_batch(chunk)
        cache_path.write_bytes(xml_bytes)
        time.sleep(0.4)
        recs = parse_pubmed_xml(xml_bytes)
        all_pubs.extend(recs)
        if i % 1000 == 0:
            print(f"  batch {i}: parsed {len(recs)} (total: {len(all_pubs)})", flush=True)

    with pubs_jsonl.open("w") as f:
        for r in all_pubs:
            f.write(json.dumps(r) + "\n")
    print(f"\nWrote {pubs_jsonl}: {len(all_pubs)} pubs", flush=True)


if __name__ == "__main__":
    main()

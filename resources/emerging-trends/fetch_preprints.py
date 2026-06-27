#!/usr/bin/env python3
"""Pull bioRxiv + medRxiv preprints (2021-2026) from Europe PMC.

Caches one JSONL per source/year under raw/ (idempotent — skips existing).
Each record: {id, source, year, title, abstract}.
"""
from __future__ import annotations
import json, time, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
UA = {"User-Agent": "Mozilla/5.0 (AoU emerging-trends; melissa@tislab.org)"}
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
SOURCES = ["bioRxiv", "medRxiv"]
YEARS = [2021, 2022, 2023, 2024, 2025, 2026]


def _get(url: str, attempts: int = 5) -> dict:
    last = None
    for i in range(attempts):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
            return json.loads(raw, strict=False)
        except Exception as e:
            last = e; time.sleep(1.5 + i)
    raise last


def pull(source: str, year: int) -> int:
    dest = RAW / f"preprints_{source}_{year}.jsonl"
    if dest.exists():
        n = sum(1 for _ in dest.open())
        print(f"  {source} {year}: cached {n}", flush=True)
        return n
    query = f'SRC:PPR AND PUBLISHER:"{source}" AND PUB_YEAR:{year}'
    cursor = "*"; n = 0
    with dest.open("w") as fh:
        while True:
            params = {"query": query, "format": "json", "pageSize": "1000",
                      "cursorMark": cursor, "resultType": "core"}
            d = _get(f"{EPMC}?{urllib.parse.urlencode(params)}")
            res = d.get("resultList", {}).get("result", [])
            for r in res:
                fh.write(json.dumps({
                    "id": r.get("id") or r.get("pmid") or r.get("doi"),
                    "source": source, "year": year,
                    "title": r.get("title") or "",
                    "abstract": r.get("abstractText") or "",
                }) + "\n")
            n += len(res)
            nc = d.get("nextCursorMark")
            if not nc or nc == cursor or not res:
                break
            cursor = nc; time.sleep(0.2)
    print(f"  {source} {year}: pulled {n}", flush=True)
    return n


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    total = 0
    for src in SOURCES:
        for y in YEARS:
            total += pull(src, y)
    print(f"\nTotal preprints: {total}")


if __name__ == "__main__":
    main()

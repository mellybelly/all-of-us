#!/usr/bin/env python3
"""Pull NIH RePORTER projects (FY2021-2026) for emerging-trends discovery.

RePORTER caps a search at offset+limit <= 15,000, and a fiscal year has ~76k
projects, so we partition each FY by administering IC (largest, NCI, is ~12k).
Caches one JSONL per FY under raw/ (idempotent). Each record:
{appl_id, year, ic, title, abstract, pref_terms}.
"""
from __future__ import annotations
import json, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
UA = {"User-Agent": "Mozilla/5.0 (AoU emerging-trends; melissa@tislab.org)",
      "Content-Type": "application/json"}
URL = "https://api.reporter.nih.gov/v2/projects/search"
YEARS = [2021, 2022, 2023, 2024, 2025, 2026]
# NIH administering ICs (each < 15k/FY, so each partition stays under the cap).
ICS = ["NCI","NEI","NHLBI","NHGRI","NIA","NIAAA","NIAID","NIAMS","NIBIB",
       "NICHD","NIDCD","NIDCR","NIDDK","NIDA","NIEHS","NIGMS","NIMH","NIMHD",
       "NINDS","NINR","NLM","NCATS","NCCIH","FIC","CIT","CSR","CC","OD"]
FIELDS = ["ApplId","FiscalYear","ProjectTitle","AbstractText","PrefTerms","AgencyIcAdmin"]


def _post(body: dict, attempts: int = 5) -> dict:
    last = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=UA)
            return json.loads(urllib.request.urlopen(req, timeout=120).read())
        except Exception as e:
            last = e; time.sleep(2.0 + i)
    raise last


def pull_year(year: int) -> int:
    dest = RAW / f"grants_{year}.jsonl"
    if dest.exists():
        n = sum(1 for _ in dest.open())
        print(f"  FY{year}: cached {n}", flush=True)
        return n
    n = 0
    with dest.open("w") as fh:
        for ic in ICS:
            offset = 0
            while True:
                body = {"criteria": {"fiscal_years": [year], "agencies": [ic]},
                        "limit": 500, "offset": offset, "include_fields": FIELDS}
                d = _post(body)
                res = d.get("results", [])
                if not res:
                    break
                for r in res:
                    fh.write(json.dumps({
                        "appl_id": r.get("appl_id"),
                        "year": year, "ic": ic,
                        "title": r.get("project_title") or "",
                        "abstract": r.get("abstract_text") or "",
                        "pref_terms": r.get("pref_terms") or "",
                    }) + "\n")
                n += len(res)
                offset += len(res)
                if offset >= d.get("meta", {}).get("total", 0) or offset >= 14500:
                    break
                time.sleep(0.25)
        # dedupe by appl_id (a project can appear under co-funding; admin IC is unique
        # so duplicates are rare, but guard anyway)
    print(f"  FY{year}: pulled {n}", flush=True)
    return n


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    total = 0
    for y in YEARS:
        total += pull_year(y)
    print(f"\nTotal grant records: {total}")


if __name__ == "__main__":
    main()

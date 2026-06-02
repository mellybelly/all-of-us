#!/usr/bin/env python3
"""
Phase 2 Workstream B — attribute publications to NIH Institutes/Centers (ICs)
via NIH RePORTER.

Parses free-text grant strings on each publication, queries the RePORTER
projects/search endpoint in batches of ~50, and records admin IC + co-funding
ICs back onto each pub.

Outputs:
    publications_with_ic.jsonl  (full records + admin_ics, cofunding_ics)
    publications_with_ic.csv    (flat view + admin_ics, cofunding_ics, grant_ids)
    raw/reporter/<batchhash>.json  (cached responses)
    ic_attribute_report.txt     (counts, top-10 ICs, unresolved IDs)

Usage:
    python3 ic_attribute.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import time
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORTER_CACHE = HERE / "raw" / "reporter"
REPORTER_CACHE.mkdir(parents=True, exist_ok=True)

REPORTER_URL = "https://api.reporter.nih.gov/v2/projects/search"
BATCH_SIZE = 20  # smaller batches; RePORTER returns many sub-projects per grant
REQUEST_DELAY_SEC = 0.5  # ~2 requests/sec
PAGE_LIMIT = 500  # RePORTER caps payload at 500 records per page; paginate via offset if more

# Activity-code pattern. PubMed citation grant strings look like:
#   "R01 HL156993/HL/NHLBI NIH HHS/United States"
#   "OT2 OD026549"
#   "1U24HG011449-01A1"   (rare, in raw form)
# Activity codes are 1-3 alphas + optional digit, e.g. R01, U24, RM1, OT2, P30, DP5, U2C.
# Canonical RePORTER form is concatenated: U24HG006834, OT2OD026549.
ACTIVITY_RE = re.compile(
    r"""
    (?:^|[^A-Za-z])            # start or non-letter (digit OK as leading app-type)
    \d?\s*                     # optional leading application-type digit (1, 5, 7, etc.)
    ([A-Z]{1,3}\d{0,2})        # activity code: e.g. R01, U24, OT2, RM1, P30, DP5, U2C, K23
    \s*
    ([A-Z]{2})                 # IC two-letter, e.g. HL, OD, CA, HG
    \s*
    (\d{4,7})                  # serial number
    (?:[-‐-―]\d{2}[A-Z]?\d?)?  # optional suffix like -01A1
    """,
    re.VERBOSE,
)

# Known NIH activity codes (subset that appear in this corpus / common ones).
# Allowing 1-3 alpha + 0-2 digit catches all variants we expect.
VALID_ACTIVITY_PREFIXES = {
    "R", "U", "P", "K", "T", "F", "S", "G", "H", "C", "D", "L", "M", "N",
    "RM", "RC", "RL", "UM", "UC", "UH", "UE", "UG", "UL", "UT", "UR", "UF",
    "U2", "U1", "U24", "U54",  # explicit common
    "OT", "OT1", "OT2", "OT3", "DP", "DP1", "DP2", "DP5",
    "PL", "PM", "PN", "PO",
}

# We will rely on regex match shape, not on the prefix list above — the prefix
# list is for debug clarity only.


def parse_grants(s: str) -> set[str]:
    """Return canonical NIH grant numbers from a free-text grant string.

    Canonical form: <ActivityCode><IC2letter><serial>   e.g. U24HG006834.
    Strip prefix application-type digits (e.g. "1U24HG011449") and any -NNN[A-Z]N suffix.
    """
    if not s:
        return set()
    out: set[str] = set()
    for m in ACTIVITY_RE.finditer(s):
        act, ic, serial = m.group(1), m.group(2), m.group(3)
        # filter obviously invalid: pad serial to typical 6-7 digits if too short
        if len(serial) < 4:
            continue
        canonical = f"{act}{ic}{serial}"
        out.add(canonical)
    return out


def _cache_path(batch: list[str]) -> Path:
    key = hashlib.sha1((";".join(sorted(batch))).encode()).hexdigest()[:16]
    return REPORTER_CACHE / f"batch_{key}.json"


def reporter_batch(batch: list[str]) -> list[dict]:
    """Query RePORTER for a batch of project_nums. Cached. Paginates if needed."""
    cache = _cache_path(batch)
    if cache.exists():
        try:
            return json.loads(cache.read_text())
        except Exception:
            pass

    all_results: list[dict] = []
    offset = 0
    while True:
        body = {
            "criteria": {"project_nums": batch},
            "include_fields": [
                "ProjectNum",
                "AgencyIcAdmin",
                "AgencyIcFundings",
                "ContactPiName",
                "ProjectTitle",
                "FiscalYear",
            ],
            "limit": PAGE_LIMIT,
            "offset": offset,
        }
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            REPORTER_URL,
            data=data,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "aou-research-landscape/0.1 (research)",
            },
        )
        backoff = 2.0
        payload = None
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    payload = json.loads(resp.read())
                break
            except Exception as exc:  # noqa: BLE001
                print(f"  RePORTER error (attempt {attempt+1}): {exc}", file=sys.stderr)
                time.sleep(backoff)
                backoff *= 2
        if payload is None:
            print(f"  GIVING UP on batch {batch[:3]}... (offset {offset})", file=sys.stderr)
            break
        results = payload.get("results", []) or []
        all_results.extend(results)
        total = (payload.get("meta") or {}).get("total", len(all_results))
        offset += PAGE_LIMIT
        if offset >= total or not results:
            break
        time.sleep(REQUEST_DELAY_SEC)

    cache.write_text(json.dumps(all_results))
    return all_results


def main() -> None:
    pubs_path = HERE / "publications.jsonl"
    pubs = []
    with open(pubs_path) as fh:
        for line in fh:
            pubs.append(json.loads(line))
    print(f"Loaded {len(pubs)} publications")

    # 1. Parse grant IDs per pub
    pub_grants: list[set[str]] = []
    all_grants: set[str] = set()
    pubs_with_any_grant_str = 0
    pubs_with_parseable = 0
    for r in pubs:
        s = ""
        for k in ("manual_grant_number", "pdr_grant_number", "calc_grant_number"):
            v = r.get(k)
            if v and v.strip() and v.strip().upper() != "N/A":
                s = v
                pubs_with_any_grant_str += 1
                break
        ids = parse_grants(s)
        if ids:
            pubs_with_parseable += 1
        pub_grants.append(ids)
        all_grants.update(ids)

    print(f"Publications with a non-N/A grant string: {pubs_with_any_grant_str}")
    print(f"Publications with at least one parseable grant ID: {pubs_with_parseable}")
    print(f"Unique grant IDs to query: {len(all_grants)}")

    # 2. Batch RePORTER
    grant_list = sorted(all_grants)
    grant_to_admin: dict[str, set[str]] = defaultdict(set)
    grant_to_cofund: dict[str, set[str]] = defaultdict(set)
    resolved: set[str] = set()

    n_batches = (len(grant_list) + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(0, len(grant_list), BATCH_SIZE):
        batch = grant_list[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        print(f"RePORTER batch {batch_num}/{n_batches} ({len(batch)} IDs)")
        results = reporter_batch(batch)
        if not results:
            time.sleep(REQUEST_DELAY_SEC)
            continue
        for proj in results:
            pn = (proj.get("project_num") or "").strip()
            if not pn:
                continue
            # RePORTER project_num looks like "1U24HG006834-01" or similar.
            # Strip leading app-type digit and any suffix to match our canonical form.
            m = ACTIVITY_RE.search(pn)
            if not m:
                continue
            canonical = f"{m.group(1)}{m.group(2)}{m.group(3)}"
            if canonical not in all_grants:
                # also check exact match in case our parser failed
                continue
            resolved.add(canonical)
            admin = (proj.get("agency_ic_admin") or {})
            admin_code = admin.get("code") or admin.get("abbreviation")
            if admin_code:
                grant_to_admin[canonical].add(admin_code)
            for cf in proj.get("agency_ic_fundings") or []:
                code = cf.get("code") or cf.get("abbreviation")
                if code:
                    grant_to_cofund[canonical].add(code)
        time.sleep(REQUEST_DELAY_SEC)

    unresolved = all_grants - resolved
    print(f"Resolved {len(resolved)}/{len(all_grants)} unique grant IDs")
    print(f"Unresolved: {len(unresolved)}")

    # 3. Aggregate per-pub
    out_records = []
    pub_admin_counter: Counter = Counter()
    pub_cofund_counter: Counter = Counter()
    pubs_with_ic = 0
    for rec, ids in zip(pubs, pub_grants):
        admin_set: set[str] = set()
        cofund_set: set[str] = set()
        for gid in ids:
            admin_set |= grant_to_admin.get(gid, set())
            cofund_set |= grant_to_cofund.get(gid, set())
        if admin_set:
            pubs_with_ic += 1
            for ic in admin_set:
                pub_admin_counter[ic] += 1
            for ic in cofund_set:
                pub_cofund_counter[ic] += 1
        new_rec = dict(rec)
        new_rec["_parsed_grant_ids"] = sorted(ids)
        new_rec["_admin_ics"] = sorted(admin_set)
        new_rec["_cofunding_ics"] = sorted(cofund_set)
        out_records.append(new_rec)

    # 4. Write outputs
    out_jsonl = HERE / "publications_with_ic.jsonl"
    with open(out_jsonl, "w", encoding="utf-8") as fh:
        for r in out_records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {out_jsonl}")

    # CSV: extend the normalized flat view
    sys.path.insert(0, str(HERE))
    from extract import normalize_publication, _clean

    out_csv = HERE / "publications_with_ic.csv"
    rows = []
    for r in out_records:
        flat = normalize_publication(r)
        flat["grant_ids_parsed"] = ";".join(r["_parsed_grant_ids"])
        flat["admin_ics"] = ";".join(r["_admin_ics"])
        flat["cofunding_ics"] = ";".join(r["_cofunding_ics"])
        rows.append(flat)
    fieldnames = list(rows[0].keys())
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: _clean(r.get(k)) for k in fieldnames})
    print(f"Wrote {out_csv}")

    # 5. Report
    report = HERE / "ic_attribute_report.txt"
    with open(report, "w") as fh:
        fh.write(f"Total publications: {len(pubs)}\n")
        fh.write(f"Publications with non-N/A grant string: {pubs_with_any_grant_str}\n")
        fh.write(f"Publications with at least one parseable grant ID: {pubs_with_parseable}\n")
        fh.write(f"Publications with at least one IC attribution: {pubs_with_ic}\n")
        fh.write(f"Unique grant IDs queried: {len(all_grants)}\n")
        fh.write(f"Unique grant IDs resolved: {len(resolved)}\n")
        fh.write(f"Unique grant IDs unresolved: {len(unresolved)}\n\n")
        fh.write("Top 15 admin ICs by pub count:\n")
        for ic, n in pub_admin_counter.most_common(15):
            fh.write(f"  {ic}\t{n}\n")
        fh.write("\nTop 15 co-funding ICs by pub count:\n")
        for ic, n in pub_cofund_counter.most_common(15):
            fh.write(f"  {ic}\t{n}\n")
        fh.write("\nUnresolved grant IDs (sample of up to 100):\n")
        for g in sorted(unresolved)[:100]:
            fh.write(f"  {g}\n")
    print(f"Wrote {report}")
    print()
    print("=== Summary ===")
    print(f"Pubs with IC attribution: {pubs_with_ic} / {len(pubs)} ({100*pubs_with_ic/len(pubs):.1f}%)")
    print("Top 10 admin ICs:")
    for ic, n in pub_admin_counter.most_common(10):
        print(f"  {ic}\t{n}")


if __name__ == "__main__":
    main()

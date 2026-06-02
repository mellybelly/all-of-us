#!/usr/bin/env python3
"""
Extract AoU publication and project data from raw API responses into CSV + JSONL.

Re-fetches raw data if --refetch is passed; otherwise uses files in raw/.

Data sources
------------
- Publications:
    https://www.researchallofus.org/wp-json/rh-data-caching/publications-report
    A pre-cached JSON list, currently returning 200 with ~1.3k records.
- Projects:
    Primary endpoint https://www.researchallofus.org/wp-json/rh-data-caching/projects
    is currently broken (500 from upstream rdr-api.pmi-ops.org). The legacy
    endpoint /wp-json/research-hub/projects-directory is also broken in prod.
    We fall back to the most recent Wayback Machine capture (2025-10-24,
    21,242 records).
- Stable mirror https://stable.researchallofus.org/wp-json/rh-data-caching/projects
  works but only contains ~285 test/staging records.

Usage
-----
    python3 extract.py             # builds CSV + JSONL from raw/
    python3 extract.py --refetch   # re-fetch raw responses, then build
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

PUBS_URL = (
    "https://www.researchallofus.org/wp-json/rh-data-caching/publications-report"
)
PROJ_URL_PROD = (
    "https://www.researchallofus.org/wp-json/rh-data-caching/projects"
)
PROJ_URL_LEGACY = (
    "https://www.researchallofus.org/wp-json/research-hub/projects-directory"
)
PROJ_WAYBACK = (
    "https://web.archive.org/web/20251024105034if_/"
    "https://www.researchallofus.org/wp-json/research-hub/projects-directory"
)


def _fetch(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json,*/*"})
    with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as fh:
        fh.write(resp.read())


def refetch() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    print(f"Fetching publications: {PUBS_URL}")
    _fetch(PUBS_URL, RAW / "publications_api.json")
    # Try prod projects first
    try:
        print(f"Trying projects (prod): {PROJ_URL_PROD}")
        _fetch(PROJ_URL_PROD, RAW / "projects_api_prod.json")
        with open(RAW / "projects_api_prod.json") as fh:
            data = json.load(fh)
        if isinstance(data, list) and len(data) > 500:
            print(f"  prod returned {len(data)} records — using prod")
            (RAW / "projects_api.json").write_text(json.dumps(data))
            return
        else:
            print("  prod returned too few records or non-list; falling back")
    except Exception as exc:  # noqa: BLE001
        print(f"  prod failed: {exc}")
    # Fall back to Wayback
    print(f"Falling back to Wayback: {PROJ_WAYBACK}")
    _fetch(PROJ_WAYBACK, RAW / "projects_api.json")


def _load(path: Path):
    with open(path) as fh:
        return json.load(fh)


def _ic_count(d: dict, field: str) -> str:
    v = d.get(field)
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return "; ".join(str(x) for x in v)
    return str(v)


def normalize_publication(rec: dict) -> dict:
    """Project the rich AoU pub record into a flat dict.

    We keep every original field in the JSONL; the CSV is a curated flattened
    view that prefers `pdr_*` (PubMed-derived) values, then `manual_*`
    overrides, then `calc_*` (computed) fallbacks.
    """
    def first(*fields: str) -> str:
        for f in fields:
            v = rec.get(f)
            if v is None:
                continue
            s = str(v).strip()
            if s and s.lower() != "none":
                return s
        return ""

    pmid = first("pubmed_id")
    pmcid = first("pmc_id")
    doi = first("manual_doi", "pdr_doi", "calc_doi")
    title = first("manual_title", "pdr_title", "calc_title")
    year = first("manual_date_year", "pdr_date_year", "calc_date_year")
    month = first("manual_date_month", "pdr_date_month", "calc_date_month")
    day = first("manual_date_day", "pdr_date_day", "calc_date_day")
    journal = first("manual_journal_title", "pdr_journal_title", "calc_journal_title")
    abstract = first("manual_abstract", "pdr_abstract", "calc_abstract")
    authors = first("manual_author_list", "pdr_author_list", "calc_author_list")
    institutions = first("pdr_institution_list", "manual_institution_list", "calc_institution_list")
    grant_no = first("manual_grant_number", "pdr_grant_number", "calc_grant_number")
    pub_type = first("manual_pub_type", "pdr_pub_type")
    pub_subtype = first("manual_pub_subtype", "pdr_pub_subtype", "calc_pub_subtype")
    program = first("manual_program_pub")
    highlight = first("manual_highlight")
    icite_count = rec.get("icite_count")
    icite_rcr = rec.get("icite_rcr")
    lay = first("lay_summary")
    link = first("link", "title_url")

    foci = {
        f: first(f"manual_{f}", f, f"calc_{f}")
        for f in (
            "common_focus",
            "rare_focus",
            "maternal_focus",
            "aging_focus",
            "results_focus",
            "behavioral_focus",
            "environmental_focus",
            "genetic_focus",
        )
    }
    pop_health = first("manual_pop_health_focus", "population_health_focus")

    return {
        "record_id": rec.get("record_id", ""),
        "pubmed_id": pmid,
        "pmc_id": pmcid,
        "doi": doi,
        "title": title,
        "year": year,
        "month": month,
        "day": day,
        "journal": journal,
        "abstract": abstract,
        "authors": authors,
        "institutions": institutions,
        "grant_number": grant_no,
        "pub_type": pub_type,
        "pub_subtype": pub_subtype,
        "program_pub": program,
        "highlight": highlight,
        "icite_count": icite_count if icite_count is not None else "",
        "icite_rcr": icite_rcr if icite_rcr is not None else "",
        "lay_summary": lay,
        "link": link,
        "common_focus": foci["common_focus"],
        "rare_focus": foci["rare_focus"],
        "maternal_focus": foci["maternal_focus"],
        "aging_focus": foci["aging_focus"],
        "results_focus": foci["results_focus"],
        "behavioral_focus": foci["behavioral_focus"],
        "environmental_focus": foci["environmental_focus"],
        "genetic_focus": foci["genetic_focus"],
        "population_health_focus": pop_health,
        "manual_review": rec.get("manual_review", ""),
        "show_on_site": rec.get("show_on_site", ""),
        "manually_added_record": rec.get("manually_added_record", ""),
    }


def normalize_project(rec: dict) -> dict:
    team = rec.get("team") or {}
    owners = team.get("owner") or []
    members = team.get("members") or []

    def _people(plist):
        bits = []
        for p in plist:
            name = p.get("name") or ""
            role = p.get("role") or ""
            inst = p.get("institution") or ""
            bits.append(f"{name} ({role}) — {inst}".strip())
        return "; ".join(bits)

    pi_name = owners[0].get("name") if owners else ""
    pi_institution = owners[0].get("institution") if owners else ""
    pi_role = owners[0].get("role") if owners else ""
    institutions = sorted({(o.get("institution") or "").strip() for o in owners if o.get("institution")})

    return {
        "workspaceId": rec.get("workspaceId", ""),
        "snapshotId": rec.get("snapshotId", ""),
        "title": rec.get("title", ""),
        "accessTier": rec.get("accessTier", ""),
        "ubrFocus": rec.get("ubrFocus", ""),
        "purposes": "; ".join(rec.get("purposes") or []),
        "categories": "; ".join(rec.get("categories") or []),
        "questions": rec.get("questions", ""),
        "approaches": rec.get("approaches", ""),
        "findings": rec.get("findings", ""),
        "pi_name": pi_name,
        "pi_role": pi_role,
        "pi_institution": pi_institution,
        "owner_count": len(owners),
        "member_count": len(members),
        "institutions": "; ".join(institutions),
        "owners": _people(owners),
        "members": _people(members),
        "reviewUrl": rec.get("reviewUrl", ""),
    }


def _clean(v):
    if v is None:
        return ""
    if isinstance(v, str):
        # Strip NULs (rare but breaks CSV readers) and normalize newlines
        return v.replace("\x00", "").replace("\r\n", "\n").replace("\r", "\n")
    return v


def write_csv(rows, path: Path, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: _clean(r.get(k)) for k in fieldnames})


def write_jsonl(rows, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refetch", action="store_true", help="re-fetch raw responses before extracting")
    args = ap.parse_args()

    if args.refetch:
        refetch()

    pubs_raw = RAW / "publications_api.json"
    if not pubs_raw.exists():
        # Accept the dated copy too
        candidates = sorted(RAW.glob("publications_api*.json"))
        if not candidates:
            sys.exit(f"No publications raw file in {RAW}; run with --refetch.")
        pubs_raw = candidates[-1]
    proj_raw = RAW / "projects_api.json"
    if not proj_raw.exists():
        candidates = sorted(RAW.glob("projects_*.json"))
        # Prefer the largest (Wayback dump) over the small stable mirror
        candidates = sorted(candidates, key=lambda p: p.stat().st_size, reverse=True)
        if not candidates:
            sys.exit(f"No projects raw file in {RAW}; run with --refetch.")
        proj_raw = candidates[0]

    print(f"Loading publications from {pubs_raw}")
    pubs = _load(pubs_raw)
    print(f"  {len(pubs)} records")

    print(f"Loading projects from {proj_raw}")
    projs = _load(proj_raw)
    print(f"  {len(projs)} records")

    pub_rows = [normalize_publication(r) for r in pubs]
    proj_rows = [normalize_project(r) for r in projs]

    pub_fields = list(pub_rows[0].keys())
    proj_fields = list(proj_rows[0].keys())

    write_csv(pub_rows, HERE / "publications.csv", pub_fields)
    write_csv(proj_rows, HERE / "projects.csv", proj_fields)
    write_jsonl(pubs, HERE / "publications.jsonl")  # full raw records, one per line
    write_jsonl(projs, HERE / "projects.jsonl")

    print(f"Wrote {HERE/'publications.csv'} ({len(pub_rows)} rows)")
    print(f"Wrote {HERE/'projects.csv'} ({len(proj_rows)} rows)")
    print(f"Wrote {HERE/'publications.jsonl'}")
    print(f"Wrote {HERE/'projects.jsonl'}")


if __name__ == "__main__":
    main()

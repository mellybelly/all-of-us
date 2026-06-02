#!/usr/bin/env python3
"""Run the 8 hot-area detectors (from aou-roadmap-refresh/temporal.py) on
the four peer corpora plus AoU. The detectors are keyword/regex on
title+abstract; same regexes as AoU Phase 3b for direct comparability.

Output: hot_areas_by_biobank.csv (rows = HA1..HA8, cols = aou/ukb/finngen/mvp/ckb
shares overall + pre/post-2023 trend per biobank).
"""
from __future__ import annotations

import csv
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AOU_LANDSCAPE = ROOT.parent / "aou-research-landscape"
AOU_REFRESH = ROOT.parent / "aou-roadmap-refresh"

# Import the temporal module to get detect_hot_areas + HOT_AREAS
spec = importlib.util.spec_from_file_location(
    "aou_temporal", str(AOU_REFRESH / "temporal.py")
)
aou_temporal = importlib.util.module_from_spec(spec)
sys.modules["aou_temporal"] = aou_temporal
# crosswalk import will also resolve relative to AOU_REFRESH
sys.path.insert(0, str(AOU_REFRESH))
spec.loader.exec_module(aou_temporal)  # type: ignore[union-attr]

HOT_AREAS = aou_temporal.HOT_AREAS
detect_hot_areas = aou_temporal.detect_hot_areas

CUTOFF = 2023
PEERS = ["ukb", "finngen", "mvp", "ckb"]


def load_aou_text():
    """Load AoU substantive corpus with title+abstract."""
    # publications_tagged.jsonl has themes but no abstract; join via record_id
    # to publications_with_ic.jsonl.
    subs = {}
    with (AOU_LANDSCAPE / "publications_tagged.jsonl").open() as f:
        for line in f:
            d = json.loads(line)
            if not d.get("in_substantive_corpus", True):
                continue
            subs[str(d.get("record_id"))] = {"year": d.get("year")}
    with (AOU_LANDSCAPE / "publications_with_ic.jsonl").open() as f:
        for line in f:
            d = json.loads(line)
            rid = str(d.get("record_id"))
            if rid not in subs:
                continue
            title = (
                d.get("calc_title")
                or d.get("manual_title")
                or d.get("pdr_title")
                or ""
            )
            abstract = (
                d.get("calc_abstract")
                or d.get("manual_abstract")
                or d.get("pdr_abstract")
                or ""
            )
            subs[rid]["title"] = title or ""
            subs[rid]["abstract"] = (abstract or "").replace("%28","(").replace("%29",")").replace("%2C",",")
            subs[rid]["year"] = (
                d.get("calc_date_year") or d.get("manual_date_year") or d.get("pdr_date_year") or subs[rid].get("year")
            )
    return list(subs.values())


def load_peer_text(code):
    rows = []
    with (ROOT / f"{code}_pubs.jsonl").open() as f:
        for line in f:
            d = json.loads(line)
            rows.append({
                "title": d.get("title", ""),
                "abstract": d.get("abstract", ""),
                "year": d.get("year", ""),
            })
    return rows


def parse_year(y):
    try:
        return int(str(y)[:4])
    except Exception:
        return None


def detect_corpus(rows):
    """Return dict ha_code -> (n_total, pre_count, post_count, pre_n, post_n)."""
    pre_n = 0
    post_n = 0
    ha_pre = Counter()
    ha_post = Counter()
    for r in rows:
        text = (r.get("title", "") + " " + r.get("abstract", "")).lower()
        flags = detect_hot_areas(text)
        yr = parse_year(r.get("year"))
        if yr is None:
            continue
        if yr < CUTOFF:
            pre_n += 1
            for ha, val in flags.items():
                if val:
                    ha_pre[ha] += 1
        else:
            post_n += 1
            for ha, val in flags.items():
                if val:
                    ha_post[ha] += 1
    return ha_pre, ha_post, pre_n, post_n


def main():
    print("Loading AoU...", flush=True)
    aou_rows = load_aou_text()
    print(f"  AoU substantive (with text): {len(aou_rows)}", flush=True)
    peer_rows = {}
    for c in PEERS:
        peer_rows[c] = load_peer_text(c)
        print(f"  {c}: {len(peer_rows[c])}", flush=True)

    data = {}
    aou_pre, aou_post, aou_pre_n, aou_post_n = detect_corpus(aou_rows)
    data["aou"] = (aou_pre, aou_post, aou_pre_n, aou_post_n)
    for c in PEERS:
        ha_pre, ha_post, pn, qn = detect_corpus(peer_rows[c])
        data[c] = (ha_pre, ha_post, pn, qn)

    # ---- hot_areas_by_biobank.csv ----------------------------------
    out = ROOT / "hot_areas_by_biobank.csv"
    cohorts = ["aou"] + PEERS
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        header = ["ha_code", "ha_name"]
        for c in cohorts:
            header.extend([f"{c}_share", f"{c}_pre_share", f"{c}_post_share", f"{c}_trend"])
        w.writerow(header)
        for ha_code, ha_name in HOT_AREAS:
            row = [ha_code, ha_name]
            for c in cohorts:
                ha_pre, ha_post, pn, qn = data[c]
                pre_share = ha_pre.get(ha_code, 0) / pn if pn else 0
                post_share = ha_post.get(ha_code, 0) / qn if qn else 0
                total = ha_pre.get(ha_code, 0) + ha_post.get(ha_code, 0)
                tot_n = pn + qn
                overall = total / tot_n if tot_n else 0
                trend = post_share - pre_share
                row.extend([round(overall, 4), round(pre_share, 4), round(post_share, 4), round(trend, 4)])
            w.writerow(row)
        # sizes row
        size_row = ["N", "(pre_n / post_n)"]
        for c in cohorts:
            _, _, pn, qn = data[c]
            size_row.extend([f"{pn+qn}", f"{pn}", f"{qn}", ""])
        w.writerow(size_row)
    print(f"wrote {out}")

    # Console table
    print("\nHot-area shares & trends (overall / pre / post / trend):")
    print(f"{'HA':4s} {'name':40s}  " + "  ".join(f"{c:>5s}-tot/trd" for c in cohorts))
    for ha_code, ha_name in HOT_AREAS:
        cells = []
        for c in cohorts:
            ha_pre, ha_post, pn, qn = data[c]
            total = ha_pre.get(ha_code, 0) + ha_post.get(ha_code, 0)
            tot_n = pn + qn
            overall = total / tot_n if tot_n else 0
            pre_s = ha_pre.get(ha_code, 0) / pn if pn else 0
            post_s = ha_post.get(ha_code, 0) / qn if qn else 0
            trend = post_s - pre_s
            cells.append(f"{overall:.3f}/{trend:+.3f}")
        print(f"{ha_code} {ha_name:40s}  " + "  ".join(f"{x:>11s}" for x in cells))


if __name__ == "__main__":
    main()

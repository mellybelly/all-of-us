#!/usr/bin/env python3
"""Cross-cohort comparison of AoU vs UKB / FinnGen / MVP / CKB.

Outputs:
  theme_share_by_biobank.csv     (theme x biobank -> share-of-corpus)
  theme_growth_by_biobank.csv    (theme x biobank -> pre/post-2023 + trend)
  aou_vs_peers_index.csv         (AoU share / median peer share)
  emerging_in_peers.csv          (peer trend - AoU trend, ranked)

For year splits we use the same cutoff as the AoU Phase 3b temporal
analysis (CUTOFF_YEAR=2023, where post-2023 == 2023+).

Theme-share denominators per biobank: count of substantive pubs (i.e.,
all rows in <code>_pubs_tagged.jsonl for peers; for AoU we use the
in_substantive_corpus=true subset from publications_tagged.jsonl).
"""
from __future__ import annotations

import csv
import json
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AOU_LANDSCAPE = ROOT.parent / "aou-research-landscape"

PEERS = ["ukb", "finngen", "mvp", "ckb"]
COHORTS = ["aou", "ukb", "finngen", "mvp", "ckb"]

CUTOFF = 2023

THEME_NAMES = {
    "1": "Cardiometabolic disease",
    "2": "Genomics methods & complex-trait genetics",
    "3": "Methods, infrastructure & phenotyping (non-genomic)",
    "4": "Mental health, behavioral & substance use",
    "5": "Cancer",
    "6": "Social determinants of health & health disparities",
    "7": "Wearables & digital health",
    "8": "Infectious disease & immunology",
    "9": "Autoimmune & inflammatory disease",
    "10": "Rare disease & Mendelian genetics",
    "11": "Aging, frailty & ADRD",
    "12": "Dermatology",
    "13": "Respiratory & sleep medicine",
    "14": "Neurology (non-ADRD)",
    "15": "Pregnancy, maternal & women's health",
    "16": "Pharmacogenomics & drug response",
    "17": "ELSI, participant engagement & recruitment",
    "18": "Ophthalmology, ENT & sensory medicine",
    "19": "Environmental health & climate",
}
THEME_ORDER = [str(i) for i in range(1, 20)]


def load_aou():
    """Load AoU substantive-corpus pubs with year+themes."""
    rows = []
    with (AOU_LANDSCAPE / "publications_tagged.jsonl").open() as f:
        for line in f:
            d = json.loads(line)
            if not d.get("in_substantive_corpus", True):
                continue
            y = d.get("year", "")
            try:
                yr = int(str(y)[:4]) if str(y)[:4].isdigit() else None
            except Exception:
                yr = None
            rows.append({
                "themes": [str(t) for t in d.get("themes", [])],
                "year": yr,
            })
    return rows


def load_peer(code):
    rows = []
    with (ROOT / f"{code}_pubs_tagged.jsonl").open() as f:
        for line in f:
            d = json.loads(line)
            y = d.get("year", "")
            try:
                yr = int(str(y)[:4]) if str(y)[:4].isdigit() else None
            except Exception:
                yr = None
            rows.append({
                "themes": [str(t) for t in d.get("themes", [])],
                "year": yr,
            })
    return rows


def compute_shares(rows):
    n = len(rows)
    if n == 0:
        return {}
    counts = Counter()
    for r in rows:
        for t in r["themes"]:
            counts[t] += 1
    return {t: counts.get(t, 0) / n for t in THEME_ORDER}, counts, n


def compute_split_shares(rows):
    """Return (pre_shares, post_shares, pre_n, post_n) using CUTOFF year."""
    pre = [r for r in rows if r["year"] is not None and r["year"] < CUTOFF]
    post = [r for r in rows if r["year"] is not None and r["year"] >= CUTOFF]
    pre_shares = {t: 0.0 for t in THEME_ORDER}
    post_shares = {t: 0.0 for t in THEME_ORDER}
    if pre:
        pre_counts = Counter()
        for r in pre:
            for t in r["themes"]:
                pre_counts[t] += 1
        pre_shares = {t: pre_counts.get(t, 0) / len(pre) for t in THEME_ORDER}
    if post:
        post_counts = Counter()
        for r in post:
            for t in r["themes"]:
                post_counts[t] += 1
        post_shares = {t: post_counts.get(t, 0) / len(post) for t in THEME_ORDER}
    return pre_shares, post_shares, len(pre), len(post)


def main():
    print("Loading corpora...", flush=True)
    aou = load_aou()
    print(f"  AoU substantive: {len(aou)}", flush=True)
    cohorts = {"aou": aou}
    for code in PEERS:
        c = load_peer(code)
        print(f"  {code}: {len(c)}", flush=True)
        cohorts[code] = c

    # Overall theme shares
    shares = {}      # cohort -> theme -> share
    counts = {}      # cohort -> theme -> count
    sizes = {}       # cohort -> n
    for code in COHORTS:
        s, c, n = compute_shares(cohorts[code])
        shares[code] = s
        counts[code] = c
        sizes[code] = n

    # Pre/post split
    pre = {}  # cohort -> theme -> share (pre-2023)
    post = {}
    pre_n = {}
    post_n = {}
    for code in COHORTS:
        pre_s, post_s, pn, qn = compute_split_shares(cohorts[code])
        pre[code] = pre_s
        post[code] = post_s
        pre_n[code] = pn
        post_n[code] = qn

    # ---- theme_share_by_biobank.csv ------------------------------
    out = ROOT / "theme_share_by_biobank.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        header = ["theme_code", "theme_name"]
        for code in COHORTS:
            header.append(f"{code}_share")
        for code in COHORTS:
            header.append(f"{code}_count")
        header.append("aou_share")
        header.append("peer_median_share")
        header.append("peer_max_share")
        w.writerow(header)
        for t in THEME_ORDER:
            row = [t, THEME_NAMES[t]]
            for code in COHORTS:
                row.append(round(shares[code][t], 4))
            for code in COHORTS:
                row.append(counts[code].get(t, 0))
            peer_vals = [shares[c][t] for c in PEERS]
            row.append(round(shares["aou"][t], 4))
            row.append(round(statistics.median(peer_vals), 4))
            row.append(round(max(peer_vals), 4))
            w.writerow(row)
        # corpus-size row
        size_row = ["N", "corpus size (substantive pubs)"]
        for code in COHORTS:
            size_row.append(sizes[code])
        for code in COHORTS:
            size_row.append("")
        size_row.extend(["", "", ""])
        w.writerow(size_row)
    print(f"wrote {out}")

    # ---- theme_growth_by_biobank.csv -----------------------------
    out = ROOT / "theme_growth_by_biobank.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        header = ["theme_code", "theme_name"]
        for code in COHORTS:
            header.extend([f"{code}_pre_share", f"{code}_post_share", f"{code}_trend"])
        w.writerow(header)
        for t in THEME_ORDER:
            row = [t, THEME_NAMES[t]]
            for code in COHORTS:
                ps = pre[code][t]
                qs = post[code][t]
                row.extend([round(ps, 4), round(qs, 4), round(qs - ps, 4)])
            w.writerow(row)
        # size note row
        size_row = ["N", "pre/post-2023 corpus sizes"]
        for code in COHORTS:
            size_row.extend([pre_n[code], post_n[code], ""])
        w.writerow(size_row)
    print(f"wrote {out}")

    # ---- aou_vs_peers_index.csv ---------------------------------
    out = ROOT / "aou_vs_peers_index.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "theme_code", "theme_name",
            "aou_share", "peer_median_share",
            "aou_vs_peers_index",
            "flag",
        ])
        for t in THEME_ORDER:
            aou_s = shares["aou"][t]
            peer_vals = [shares[c][t] for c in PEERS]
            peer_med = statistics.median(peer_vals)
            if peer_med > 0:
                idx = aou_s / peer_med
            else:
                idx = float("inf") if aou_s > 0 else 0.0
            flag = ""
            if peer_med > 0:
                if idx < 0.5:
                    flag = "AoU-under (<0.5)"
                elif idx > 2.0:
                    flag = "AoU-over (>2.0)"
            w.writerow([
                t, THEME_NAMES[t],
                round(aou_s, 4),
                round(peer_med, 4),
                round(idx, 3) if idx != float("inf") else "inf",
                flag,
            ])
    print(f"wrote {out}")

    # ---- emerging_in_peers.csv ----------------------------------
    # For each theme: peer-mean post-vs-pre trend minus AoU trend.
    # We use peer mean (4 peers) so a single biobank's quirk doesn't drive
    # the metric.
    out = ROOT / "emerging_in_peers.csv"
    rows_em = []
    for t in THEME_ORDER:
        aou_trend = post["aou"][t] - pre["aou"][t]
        peer_trends = [post[c][t] - pre[c][t] for c in PEERS]
        peer_mean_trend = statistics.mean(peer_trends)
        diff = peer_mean_trend - aou_trend
        rows_em.append({
            "theme_code": t,
            "theme_name": THEME_NAMES[t],
            "aou_trend": round(aou_trend, 4),
            "peer_mean_trend": round(peer_mean_trend, 4),
            "diff_peer_minus_aou": round(diff, 4),
            "ukb_trend": round(post["ukb"][t] - pre["ukb"][t], 4),
            "finngen_trend": round(post["finngen"][t] - pre["finngen"][t], 4),
            "mvp_trend": round(post["mvp"][t] - pre["mvp"][t], 4),
            "ckb_trend": round(post["ckb"][t] - pre["ckb"][t], 4),
            "aou_share_overall": round(shares["aou"][t], 4),
            "peer_median_share_overall": round(statistics.median([shares[c][t] for c in PEERS]), 4),
        })
    rows_em.sort(key=lambda r: r["diff_peer_minus_aou"], reverse=True)
    with out.open("w", newline="") as f:
        cols = ["theme_code", "theme_name", "aou_trend", "peer_mean_trend",
                "diff_peer_minus_aou", "ukb_trend", "finngen_trend",
                "mvp_trend", "ckb_trend", "aou_share_overall",
                "peer_median_share_overall"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows_em:
            w.writerow(r)
    print(f"wrote {out}")

    # ---- console summary ---------------------------------------
    print("\nCorpus sizes (substantive):")
    for code in COHORTS:
        print(f"  {code}: n={sizes[code]} (pre={pre_n[code]}, post={post_n[code]})")

    print("\nTop emerging-in-peers (peers outpacing AoU; high = AoU thinner / peer-trending-up):")
    for r in rows_em[:8]:
        print(f"  {r['theme_code']:>3} {r['theme_name']:50s} AoU-trend={r['aou_trend']:+.4f} peer-mean-trend={r['peer_mean_trend']:+.4f} diff={r['diff_peer_minus_aou']:+.4f} (AoU share={r['aou_share_overall']:.3f}, peer-med={r['peer_median_share_overall']:.3f})")

    print("\nBottom emerging-in-peers (AoU outpacing peers — AoU's distinctive growth):")
    for r in rows_em[-8:][::-1]:
        print(f"  {r['theme_code']:>3} {r['theme_name']:50s} AoU-trend={r['aou_trend']:+.4f} peer-mean-trend={r['peer_mean_trend']:+.4f} diff={r['diff_peer_minus_aou']:+.4f}")

    print("\nAoU-under-indexed themes (index < 0.5):")
    for t in THEME_ORDER:
        aou_s = shares["aou"][t]
        peer_vals = [shares[c][t] for c in PEERS]
        peer_med = statistics.median(peer_vals)
        if peer_med > 0 and aou_s / peer_med < 0.5:
            print(f"  {t:>3} {THEME_NAMES[t]:50s} AoU={aou_s:.3f} peer-med={peer_med:.3f} idx={aou_s/peer_med:.2f}")

    print("\nAoU-over-indexed themes (index > 2.0):")
    for t in THEME_ORDER:
        aou_s = shares["aou"][t]
        peer_vals = [shares[c][t] for c in PEERS]
        peer_med = statistics.median(peer_vals)
        if peer_med > 0 and aou_s / peer_med > 2.0:
            print(f"  {t:>3} {THEME_NAMES[t]:50s} AoU={aou_s:.3f} peer-med={peer_med:.3f} idx={aou_s/peer_med:.2f}")


if __name__ == "__main__":
    main()

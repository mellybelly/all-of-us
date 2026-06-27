#!/usr/bin/env python3
"""Methods gap-check: for each emerging method topic, measure adoption in AoU
publications and in AoU researcher workspaces, and rank the
trending-but-underused-and-feasible opportunities for the Researcher Workbench.

Workspace coverage uses the SUBSTANTIVE workspace set (tutorials/duplicates
filtered out) so the signal reflects real research, not training clones.

Output: methods_gap.csv (+ methods_gap.json).
"""
from __future__ import annotations
import json, csv, math
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAND = HERE.parent / "aou-research-landscape"


def load_pub_text():
    out = []
    for line in (LAND / "publications.jsonl").open():
        d = json.loads(line)
        t = (d.get("pdr_title") or d.get("manual_title") or d.get("calc_title") or "")
        a = (d.get("pdr_abstract") or d.get("manual_abstract") or d.get("calc_abstract") or "")
        out.append((t + " " + a).lower())
    return out


def load_ws_text(path):
    out = []
    for line in path.open():
        d = json.loads(line)
        out.append(" ".join(str(d.get(f) or "") for f in
                            ("title", "questions", "approaches", "findings")).lower())
    return out


def coverage(docs, kws):
    pats = [k.lower() for k in kws]
    return sum(1 for t in docs if any(p in t for p in pats))


def main():
    methods = json.load(open(HERE / "methods_topics.json"))["methods"]
    pubs = load_pub_text()
    ws_all = load_ws_text(LAND / "projects.jsonl")
    ws_sub = load_ws_text(LAND / "projects_filtered.jsonl")  # substantive only
    print(f"pubs={len(pubs)} workspaces_all={len(ws_all)} workspaces_substantive={len(ws_sub)}")

    MAT = {"frontier": 1.0, "rising": 0.8, "established-but-underused": 0.5}
    FEAS = {"high": 1.0, "med": 0.5, "low": 0.1}

    rows = []
    for m in methods:
        kw = m["keywords"]
        p_hit = coverage(pubs, kw); p_pct = 100 * p_hit / len(pubs)
        w_hit = coverage(ws_sub, kw); w_pct = 100 * w_hit / len(ws_sub)
        wa_hit = coverage(ws_all, kw); wa_pct = 100 * wa_hit / len(ws_all)
        feas = m.get("rw_feasibility", "med")
        mat = m.get("maturity", "rising")
        # Opportunity = feasibility x maturity x external-trend x absence-in-AoU.
        ext = math.log10(max(m.get("peak_growth", 1.1), 1.1))
        absence = (1 - min(w_pct, 100) / 100)          # workspace is the RW-adoption axis
        opp = round(FEAS.get(feas, 0.5) * MAT.get(mat, 0.7) * ext * absence, 3)
        rows.append({
            "id": m["id"], "label": m["label"], "maturity": mat,
            "rw_feasibility": feas, "peak_growth": m.get("peak_growth"),
            "pub_hits": p_hit, "pub_pct": round(p_pct, 2),
            "ws_sub_hits": w_hit, "ws_sub_pct": round(w_pct, 2),
            "ws_all_pct": round(wa_pct, 2),
            "opportunity": opp,
            "rw_feasibility_reason": m.get("rw_feasibility_reason", ""),
            "keywords": kw,
        })

    rows.sort(key=lambda r: -r["opportunity"])
    with (HERE / "methods_gap.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "id", "label", "maturity", "rw_feasibility",
                    "peak_growth", "pub_pct", "ws_substantive_pct", "ws_all_pct",
                    "opportunity"])
        for i, r in enumerate(rows, 1):
            w.writerow([i, r["id"], r["label"], r["maturity"], r["rw_feasibility"],
                        r["peak_growth"], r["pub_pct"], r["ws_sub_pct"],
                        r["ws_all_pct"], r["opportunity"]])
    (HERE / "methods_gap.json").write_text(json.dumps(rows, indent=1))

    print("\nTop opportunities (trending + feasible + low workspace adoption):")
    for r in rows[:15]:
        print(f"  {r['label'][:40]:40} feas={r['rw_feasibility']:4} "
              f"pub={r['pub_pct']:4.1f}% ws={r['ws_sub_pct']:4.1f}% opp={r['opportunity']}")


if __name__ == "__main__":
    main()

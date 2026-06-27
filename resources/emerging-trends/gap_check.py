#!/usr/bin/env python3
"""Gap-check emerging topics against AoU + peer biobanks, add published-literature
trajectory, and rank by white-space (emergence x absence-in-AoU/peers).

Coverage = fraction of a corpus whose title+abstract contains any topic keyword
(case-insensitive substring). Published trajectory = Europe PMC MED counts 2021
vs 2025 for an OR-of-keywords query.

Outputs: emerging_whitespace.csv  (+ emerging_whitespace.json with detail).
"""
from __future__ import annotations
import json, csv, re, time, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAND = HERE.parent / "aou-research-landscape"
PEER = HERE.parent / "peer-biobanks"
UA = {"User-Agent": "Mozilla/5.0 (AoU emerging-trends; melissa@tislab.org)"}
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


def load_aou():
    docs = []
    for line in (LAND / "publications.jsonl").open():
        d = json.loads(line)
        t = (d.get("pdr_title") or d.get("manual_title") or d.get("calc_title") or "")
        a = (d.get("pdr_abstract") or d.get("manual_abstract") or d.get("calc_abstract") or "")
        docs.append((t + " " + a).lower())
    return docs


def load_peer(code):
    docs = []
    fp = PEER / f"{code}_pubs.jsonl"
    for line in fp.open():
        d = json.loads(line)
        docs.append(((d.get("title") or "") + " " + (d.get("abstract") or "")).lower())
    return docs


def coverage(docs, keywords):
    pats = [k.lower() for k in keywords]
    hits = 0
    for txt in docs:
        if any(p in txt for p in pats):
            hits += 1
    return hits, len(docs)


def epmc_count(q):
    u = f"{EPMC}?{urllib.parse.urlencode({'query': q, 'format': 'json', 'pageSize': '1'})}"
    for i in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read())["hitCount"]
        except Exception:
            time.sleep(1.5 + i)
    return None


def pubmed_traj(keywords):
    # OR of the most specific phrase keywords (cap to keep query sane)
    phrases = [k for k in keywords if " " in k or len(k) > 6][:6] or keywords[:4]
    orq = " OR ".join(f'"{k}"' for k in phrases)
    c21 = epmc_count(f"SRC:MED AND PUB_YEAR:2021 AND ({orq})")
    c25 = epmc_count(f"SRC:MED AND PUB_YEAR:2025 AND ({orq})")
    return c21, c25, phrases


def main():
    topics = json.load(open(HERE / "emerging_topics.json"))["topics"]
    print("Loading corpora...", flush=True)
    aou = load_aou()
    peers = {c: load_peer(c) for c in ["ukb", "finngen", "mvp", "ckb"]}
    print(f"  AoU={len(aou)} UKB={len(peers['ukb'])} FinnGen={len(peers['finngen'])} "
          f"MVP={len(peers['mvp'])} CKB={len(peers['ckb'])}", flush=True)

    rows = []
    for t in topics:
        kw = t["keywords"]
        a_hit, a_n = coverage(aou, kw)
        a_pct = 100 * a_hit / a_n
        peer_hit = peer_tot = 0
        per_peer = {}
        for c, docs in peers.items():
            h, n = coverage(docs, kw)
            per_peer[c] = (h, n)
            peer_hit += h; peer_tot += n
        peer_pct = 100 * peer_hit / peer_tot
        c21, c25, phrases = pubmed_traj(kw)
        pub_growth = round((c25 or 0) / (c21 or 1), 1)

        # White-space: emergence (peak growth, log-damped) x absence in AoU & peers.
        import math
        emergence = math.log10(max(t.get("peak_growth", 1), 1.1))
        absence = (1 - a_pct / 100) * (1 - min(peer_pct, 100) / 100)
        evid = {"strong": 1.0, "moderate": 0.6, "weak": 0.3}.get(t.get("evidence_strength"), 0.5)
        ws = round(emergence * absence * evid, 3)

        rows.append({
            "id": t["id"], "label": t["label"], "corpus": t.get("primary_corpus"),
            "evidence": t.get("evidence_strength"), "peak_growth": t.get("peak_growth"),
            "aou_hits": a_hit, "aou_pct": round(a_pct, 2),
            "peer_pct": round(peer_pct, 2),
            "ukb_pct": round(100 * per_peer["ukb"][0] / per_peer["ukb"][1], 2),
            "pub_2021": c21, "pub_2025": c25, "pub_growth_x": pub_growth,
            "whitespace_score": ws,
            "artifact_risk": t.get("artifact_risk", ""),
            "keywords": kw, "pub_phrases": phrases,
        })
        print(f"  {t['id'][:30]:30} AoU={a_pct:4.1f}% peers={peer_pct:4.1f}% "
              f"pub25={c25} ws={ws}", flush=True)
        time.sleep(0.2)

    rows.sort(key=lambda r: -r["whitespace_score"])
    with (HERE / "emerging_whitespace.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "id", "label", "corpus", "evidence", "peak_growth",
                    "aou_hits", "aou_pct", "peer_pct", "ukb_pct",
                    "pub_2021", "pub_2025", "pub_growth_x", "whitespace_score"])
        for i, r in enumerate(rows, 1):
            w.writerow([i, r["id"], r["label"], r["corpus"], r["evidence"],
                        r["peak_growth"], r["aou_hits"], r["aou_pct"], r["peer_pct"],
                        r["ukb_pct"], r["pub_2021"], r["pub_2025"], r["pub_growth_x"],
                        r["whitespace_score"]])
    (HERE / "emerging_whitespace.json").write_text(json.dumps(rows, indent=1))
    print(f"\nWrote emerging_whitespace.csv / .json ({len(rows)} topics)")


if __name__ == "__main__":
    main()

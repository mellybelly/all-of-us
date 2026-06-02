#!/usr/bin/env python3
"""Tag peer-biobank corpora with the AoU 19-theme taxonomy.

Reuses tag_corpus.py's THEMES + tag_record machinery so peer tagging is
1:1 comparable to the AoU tagging. We skip the META audit because META is
an AoU-program-meta-audit specifically about AoU; for peer biobanks we
just tag substantively against the 19 themes.

Pass-2 LLM-judgment is intentionally skipped (per spec) so the keyword
heuristic is applied uniformly across all five corpora.

Output:
  <code>_pubs_tagged.jsonl
  <code>_pubs_tagged.csv
"""
from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AOU_LANDSCAPE = ROOT.parent / "aou-research-landscape"

# Load tag_corpus.py from the AoU landscape directory so we share THEMES + logic
spec = importlib.util.spec_from_file_location(
    "aou_tag_corpus", str(AOU_LANDSCAPE / "tag_corpus.py")
)
aou_tag = importlib.util.module_from_spec(spec)
sys.modules["aou_tag_corpus"] = aou_tag
spec.loader.exec_module(aou_tag)  # type: ignore[union-attr]


BIOBANKS = ["ukb", "finngen", "mvp", "ckb"]


def tag_one(code: str):
    src = ROOT / f"{code}_pubs.jsonl"
    out_jsonl = ROOT / f"{code}_pubs_tagged.jsonl"
    out_csv = ROOT / f"{code}_pubs_tagged.csv"

    n = 0
    zero = 0
    high = 0
    rows = []
    with src.open() as f:
        for line in f:
            d = json.loads(line)
            title = (d.get("title") or "").strip()
            abstract = (d.get("abstract") or "").strip()
            text = f"{title}\n{abstract}"
            themes, evidence, subthemes = aou_tag.tag_record(text, title=title)
            n += 1
            if not themes:
                zero += 1
            if len(themes) > 5:
                high += 1
            rows.append({
                "pubmed_id": d.get("pubmed_id", ""),
                "year": d.get("year", ""),
                "title": title,
                "journal": d.get("journal", ""),
                "themes": themes,
                "subthemes": subthemes,
                "tag_evidence": {k: {"source": "keyword", "keywords": v} for k, v in evidence.items()},
                "publication_types": d.get("publication_types", []),
            })

    with out_jsonl.open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    cols = ["pubmed_id", "year", "title", "journal", "themes", "subthemes", "publication_types"]
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([
                r["pubmed_id"],
                r["year"],
                r["title"],
                r["journal"],
                ";".join(r["themes"]),
                ";".join(r["subthemes"]),
                ";".join(r["publication_types"]),
            ])

    print(f"  {code}: n={n} zero-tag={zero} ({100*zero/n:.1f}%) >5-tag={high} ({100*high/n:.1f}%)", flush=True)


def main():
    for code in BIOBANKS:
        tag_one(code)


if __name__ == "__main__":
    main()

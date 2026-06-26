# Peer-biobank publication comparison

Cross-cohort comparison of All of Us against four peer biobanks
(UK Biobank, FinnGen, Million Veteran Program, China Kadoorie Biobank)
to surface emerging research areas for the 2026 AoU Scientific Roadmap
Refresh WG.

## What this is for

The existing AoU analysis (`aou-research-landscape`, `aou-ic-alignment`,
`aou-roadmap-refresh`) compares AoU's corpus against NIH IC strategic
plans. NIH plans lag the research field by 2-3 years. Peer-biobank
corpora are AoU's most direct benchmark for "what is the field doing
that we are not." If a theme is fast-growing in UK Biobank or Million
Vets but quiet in AoU, that is a Refresh-relevant signal.

## Read first

- **`emerging_themes.md`** — the Phase-4-input deliverable: top
  emerging-but-AoU-thin themes, top AoU-leads themes, caveats.
- **`comparison.md`** — methodology, corpus sizes, data-source caveats,
  reproducibility notes.

## Files

| File | Description |
|---|---|
| `emerging_themes.md` | Phase-4 input deliverable |
| `comparison.md` | Methodology + caveats |
| `acquire.py` | PubMed E-utilities fetch (FinnGen, MVP, CKB) |
| `acquire_ukb_stratified.py` | Year-windowed UKB fetch |
| `tag_peers.py` | Apply AoU 19-theme tagger to peer corpora |
| `compare.py` | Cross-cohort theme-share + trend tables |
| `hot_areas_peers.py` | Run AoU Phase 3b 8 hot-area detectors on all 5 cohorts |
| `theme_share_by_biobank.csv` | Theme × biobank: share-of-corpus + counts |
| `theme_growth_by_biobank.csv` | Theme × biobank: pre/post-2023 shares + trend |
| `aou_vs_peers_index.csv` | AoU share / peer-median share, with outlier flags |
| `emerging_in_peers.csv` | Peer-mean trend − AoU trend, ranked |
| `hot_areas_by_biobank.csv` | HA1-HA8 × biobank: shares + trends |
| `<code>_pubs.jsonl` | Raw cleaned pubs per biobank (pmid, year, title, abstract, journal) |
| `<code>_pubs_tagged.jsonl` / `.csv` | Tagged pubs per biobank |
| `raw/<code>_pmids.txt` | PMID list per biobank |
| `raw/<code>_efetch_*.xml` | Raw efetch XML (200-PMID batches; cached) |

## Data-source caveat (important)

All four peer corpora were acquired via PubMed name-search
(`"<biobank name>"[Title/Abstract]`), not from the biobank's official
curated publication list. The per-task fallback rule (10 min per
biobank) directed straight to this approach. Implications:

- Pubs that use the biobank's data but do not name-mention in title/
  abstract are missed (largest effect on MVP, where data-use
  acknowledgments typically live in the methods or acknowledgments
  section).
- Pubs that name-mention the biobank but do not analyze its data are
  included (e.g., commentaries, methodology pubs that mention UKB as
  a use case).
- Comparisons are internally consistent because the same heuristic is
  applied to all four peers.

All four corpora are **full name-search censuses** (no sampling, as of the
2026-06-26 refresh). UKB's ~11,882-pub universe exceeds NCBI's
~9,999-per-WebEnv esearch limit, so it is pulled in year windows and
unioned (11,868 pubs). FinnGen, MVP, and CKB are pulled in their entirety
(3,152 / 438 / 558 returns respectively). Note: "~12,000" denotes the UKB
publication *universe*, not a count of fetches.

## Reproducibility

```bash
python3 acquire.py finngen mvp ckb
python3 acquire_ukb_stratified.py
python3 tag_peers.py
python3 compare.py
python3 hot_areas_peers.py
```

The AoU corpus is reused as-is from
`aou-research-landscape/publications_tagged.jsonl` (1,374 substantive
pubs, post-Pass-2-audit). It is NOT re-tagged here.

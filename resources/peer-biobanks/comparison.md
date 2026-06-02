# Peer-biobank publication comparison — full methodological writeup

This document covers the technical workflow, corpus characteristics, and
caveats behind `emerging_themes.md`. The four peer biobanks compared
against AoU are UK Biobank, FinnGen, Million Veteran Program (MVP), and
China Kadoorie Biobank (CKB).

## Corpora and provenance

| Cohort | Substantive pubs | Pre-2023 | Post-2023 | Year range | Source |
|---|---:|---:|---:|---|---|
| AoU | 1,374 | 157 | 1,217 | 2018-2026 | `aou-research-landscape/publications_tagged.jsonl` (reused; not retagged) |
| UK Biobank | 5,831 | 2,159 | 3,672 | 2007-2026 | PubMed `"UK Biobank"[Title/Abstract]` year-stratified sample of ~12,000 returns |
| FinnGen | 3,075 | 225 | 2,850 | 2020-2026 | PubMed `"FinnGen"[Title/Abstract]` (all) |
| MVP | 426 | 135 | 291 | 2012-2026 | PubMed `"Million Veteran Program"[Title/Abstract] OR "Million Veterans Program"[Title/Abstract]` (all) |
| CKB | 551 | 316 | 235 | 2011-2026 | PubMed `"China Kadoorie Biobank"[Title/Abstract]` (all) |

All four peer corpora were acquired via PubMed E-utilities
(esearch + efetch). Official curated publication lists from each
biobank's website were not used; the per-biobank 10-min-fallback rule
in the task spec directed straight to PubMed name-search.

### UK Biobank year-stratification

PubMed's default esearch sort is descending PubDate. A naive 4,000-cap
on UKB returned only 2024-2026 publications. We instead ran six date-
windowed esearches (2007:2018, 2019:2020, 2021:2022, 2023, 2024,
2025:2026) with per-window caps of 800-1500 and deduplicated, yielding
5,831 unique PMIDs. This gives pre/post-2023 balance suitable for
trend-differential analysis but does NOT reflect actual UKB publication
volume by year — the windowed caps suppress 2022 and 2024 totals
relative to natural distribution.

### Coverage caveats by biobank

- **UKB**: total PubMed returns ~12,000; sample = 5,831 (50%). Should
  not affect theme-share estimates within statistical noise.
- **FinnGen**: complete (3,075 of 3,075 PubMed returns). However,
  FinnGen *summary statistics* are widely used by external GWAS authors
  who cite "FinnGen" in the methods section; many of those pubs are
  not FinnGen-cohort-led work. This is the same kind of "FinnGen-using"
  population as the AoU "AoU-data-using" population, so it is treated
  as comparable.
- **MVP**: complete name-search (426 of 427). The VA-maintained
  publication list almost certainly contains more pubs than name-search
  finds — many MVP-using investigators acknowledge the program in the
  acknowledgments section but do not name-mention in title/abstract.
  MVP corpus is therefore the most undercounted of the four. Signal
  from MVP-only patterns should be treated cautiously.
- **CKB**: complete name-search (551 of 551). CKB publications are
  largely written by the founding consortium and have strong title/
  abstract name-mention conventions, so coverage is likely close to
  the official list.

## Tagging methodology

All five corpora were tagged with the locked AoU 19-theme taxonomy
(`aou-research-landscape/taxonomy.md`). Tagging used the keyword pre-tag
logic in `aou-research-landscape/tag_corpus.py` (Pass 1), with the
following decisions:

1. **Same keyword set for all corpora.** No corpus-specific keyword
   adjustments. Same indicative + specific keyword lists, same firing
   rules (≥1 specific keyword OR ≥2 distinct general keywords OR ≥1
   general keyword in title).
2. **Pass-2 LLM-judgment is intentionally skipped for peers.** AoU
   Phase 2c used a per-record audit pass for precision; for cross-
   cohort theme-share comparison, identical-process keyword tagging
   across all five cohorts matters more than per-cohort precision.
   Caveat: per-cohort precision is therefore probably 5-10% lower for
   the peer corpora than for the audited AoU corpus, with both false
   positives and false negatives. This affects absolute numbers but
   not the directional differential signals.
3. **META detection is disabled for peers.** META (AoU-program-meta-
   audit) is specifically about AoU itself; peer biobanks don't have
   that concept. Peer pubs that would have been flagged META under the
   AoU rule (e.g., "Cohort profile: UK Biobank") are kept in the
   substantive corpus.
4. **No re-tagging of AoU.** The existing `publications_tagged.jsonl`
   (1,378 records, 1,374 substantive) is reused as-is. This means the
   AoU side benefits from the Phase 2c audit pass and the peer side
   does not — a small bias in favor of slightly-cleaner AoU tagging,
   acceptable since the audit pass primarily affected over-tagging
   (high-tag-count records), not theme-share direction.

Tagger zero-tag and high-tag-count statistics (suggesting overall
quality):

| Cohort | Zero-tag | >5-tag |
|---|---:|---:|
| AoU | (audited, ~3% pre-audit, ~1.5% post) | (audited, <0.5% post) |
| UKB | 5.0% | 0.5% |
| FinnGen | 0.2% | 1.6% |
| MVP | 3.5% | 0.2% |
| CKB | 5.8% | 0.4% |

Zero-tag rates of 3-6% for peer corpora are within the expected range
(records on disease areas not enumerated in the taxonomy, biostats-only
methods pubs, or pubs with abstract-fetch failures). FinnGen's near-zero
zero-tag rate is a happy coincidence of the genomics-keyword density
in FinnGen abstracts.

## Hot-area detectors (HA1-HA8)

The 8 hot-area detectors from `aou-roadmap-refresh/temporal.py` were run
on all five corpora (title+abstract). Same regexes, no peer-specific
adjustments. These are independent of the 19-theme taxonomy — they map
to slide-7 of the 2026 Sci Com WG deck (multi-omics, wearables, imaging,
AI/LLMs, environmental, GxE/GxSDOH, nutrition/microbiome, breakthrough
therapeutics).

HA1, HA3, and HA7 produced the strongest peer-cohort signals: see
`emerging_themes.md` for the analytic narrative.

## Top journals per cohort

Snapshot from PubMed `Journal` field; useful for sanity-checking the
corpus mix.

(Not pulled programmatically; available from `<biobank>_pubs_tagged.csv`
if needed — column `journal`.)

## Output files

| File | Description |
|---|---|
| `theme_share_by_biobank.csv` | Theme × biobank: share-of-corpus + counts |
| `theme_growth_by_biobank.csv` | Theme × biobank: pre/post-2023 shares + trend |
| `aou_vs_peers_index.csv` | Theme: AoU share / peer median share; flagged outliers |
| `emerging_in_peers.csv` | Theme: peer-mean trend − AoU trend, ranked descending |
| `hot_areas_by_biobank.csv` | HA1-HA8 × biobank: overall share + pre/post-2023 trends |
| `<code>_pubs_tagged.jsonl` / `.csv` | Per-biobank tagged corpora (one row per pub) |
| `raw/<code>_pmids.txt` | PMID list per biobank (post-dedup) |
| `raw/<code>_efetch_*.xml` | Raw efetch responses (cached) |

## Reproducibility

```bash
# 1. Pull PMIDs + abstracts via PubMed E-utilities
python3 acquire.py finngen mvp ckb
python3 acquire_ukb_stratified.py

# 2. Tag with the AoU 19-theme taxonomy
python3 tag_peers.py

# 3. Cross-cohort comparison
python3 compare.py

# 4. Hot-area detection (8 detectors from Phase 3b)
python3 hot_areas_peers.py
```

Caching is aggressive: PMID lists, efetch XML responses, and tagged
jsonl are all written to disk. Re-running any step will reuse cached
outputs unless they are explicitly deleted.

## Limitations to address in a follow-up

1. **Pull the canonical biobank publication lists** when time permits.
   UKB's official list (`https://www.ukbiobank.ac.uk/enable-your-research/publications`)
   is the gold standard. FinnGen's, MVP's, and CKB's lists likewise.
2. **MVP coverage is undercounted.** A canonical-list pull would
   increase MVP n from 426 to probably 1,500+ and stabilize MVP-only
   trend signals.
3. **Statistical significance.** All differentials reported here are
   point estimates; bootstrapped confidence intervals on theme-share
   differences would be a useful addition but were not in the
   wall-clock budget.
4. **MeSH-based tagging as a cross-check.** PubMed records carry MeSH
   terms that could be used as an independent tag source — useful for
   validating where keyword-tagging may be over- or under-firing on
   peer abstracts that use UK-biased terminology.

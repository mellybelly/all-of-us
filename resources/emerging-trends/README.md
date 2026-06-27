# Emerging-trends / white-space analysis

Horizon scan of the broad biomedical literature for trends that are
**accelerating** but **not yet realized in All of Us or peer biobanks** — and a
feasibility filter for which gaps AoU could actually act on.

**Read first:** [`emerging_trends_report.md`](emerging_trends_report.md) — the
findings (Tier 1 actionable white space, Tier 2 watch, Tier 3 already-core) and
how they connect to the Roadmap Refresh. [`SCOPING.md`](SCOPING.md) documents
the up-front feasibility study and design decisions.

## Pipeline

| Step | Script | Output |
| --- | --- | --- |
| 1. Pull preprints | `fetch_preprints.py` | `raw/preprints_*.jsonl` (bioRxiv+medRxiv 2021-26, 293,979 docs) |
| 2. Pull grants | `fetch_grants.py` | `raw/grants_*.jsonl` (NIH RePORTER FY21-26, 422,565 records, IC-partitioned) |
| 3. Term-emergence | `compute_emergence.py` | `emerging_preprints.csv`, `emerging_grants.csv`, `emerging_candidates.json` |
| 4. Topic induction | (LLM agent over `topic_induction_digest.txt`) | `emerging_topics.json` (24 topics + excluded artifacts) |
| 5. Gap-check + rank | `gap_check.py` | `emerging_whitespace.{csv,json}` |
| 6. Feasibility tiering | (in `gap_check` follow-up) | `emerging_final.json`, report |

## Method notes

- **Discover on the leading edge, locate in the mainstream.** Preprints + grants
  (tractable, lead by 1-2 yrs) are pulled in full and mined for accelerating
  terms; the 6M-record published corpus is queried only for *discovered* terms.
- **Open discovery** (data-driven topics), not the locked 19-theme taxonomy.
- **Detection** is pure-Python term-acceleration (no sklearn/embeddings needed);
  topic induction is LLM-based, which also filters writing-style boilerplate.
- **Feasibility overlay** rates each topic against AoU's data assets (WGS, EHR,
  surveys, wearables, Workbench — not tissue assays/protein structures/imaging),
  separating *actionable* white space from frontiers outside AoU's data model.

## Caveats

See the report's Caveats section. Key one: NIH RePORTER `pref_terms` vocabulary
changes inflate some grant growth multipliers — preprint (author-text) signals
are the trustworthy ones.

## Reproduce

```bash
python3 fetch_preprints.py        # ~300k preprints (cached)
python3 fetch_grants.py           # ~420k grants (cached, IC-partitioned)
python3 compute_emergence.py      # term-acceleration + candidates
# (LLM topic induction over topic_induction_digest.txt -> emerging_topics.json)
python3 gap_check.py              # coverage vs AoU+peers, published trajectory, ranking
```

`raw/` (~2.2 GB) is gitignored — regenerable from the fetch scripts.

# Full-text augmentation & dual-layer tagging (2026-06-26)

This pass adds **PMC full-text** as a tagging input for the AoU publication
corpus and **back-fills missing abstracts**, then re-tags the corpus in two
layers so trend work stays statistically honest.

## What was fetched

`fetch_fulltext.py` pulls, for every record with a valid PMC id, the Europe PMC
JATS full text (`.../{PMCID}/fullTextXML`) and extracts **body text only** —
section titles, paragraphs, and figure/table captions. Reference lists,
acknowledgments, author notes, competing-interest and funding statements,
tables, and formulae are **stripped** (JATS `<back>`, `<ref-list>`, `<ack>`,
`<fn-group>`, `<table-wrap>`, …) because they name-drop unrelated
diseases/methods and would pollute keyword tagging. Everything is cached under
`raw/fulltext/` (and `raw/abstracts/`) so re-runs are free.

| Metric | N |
| --- | ---: |
| Records in corpus | 1,432 |
| Records with a valid PMC id | 991 |
| **Full text extracted** (OA subset, >400 chars body) | **612** |
| PMC ids with no OA full text (genuine 404) | 379 |
| Missing an abstract in the feed | 205 |
| **Abstracts gap-filled** (7 from full-text XML, 3 from EPMC search) | **10** |
| Still abstract-less after gap-fill | 195 |

The 195 that stay empty are genuinely abstract-less in PubMed itself —
editorials, news, and commentaries (e.g. "Obama's Precision Medicine
Initiative", "The Illusion of Inclusion"), most of which are `is_meta` and
excluded from the substantive corpus anyway.

## Two tagging layers

`tag_corpus.py` now takes `AOU_TAG_MODE`:

| Mode | Output | Tagging text | Use for |
| --- | --- | --- | --- |
| `abstract` (default, **canonical**) | `publications_tagged.{jsonl,csv}`, `theme_summary.csv` | title + (gap-filled) abstract | year-over-year trends; peer-biobank comparison (peers are abstract-only) |
| `fulltext` | `publications_tagged_fulltext.{jsonl,csv}`, `theme_summary_fulltext.csv` | title + abstract + PMC body | richest cross-sectional theme map |

Gap-filled abstracts are used in **both** modes (a strict improvement). Meta
detection is always abstract-level — full-text body never flips a paper's
meta/substantive status.

### Per-pub theme density

| | Abstract (canonical) | Full-text |
| --- | ---: | ---: |
| Mean themes / pub | 2.06 | 3.39 |
| Median | 2 | 3 |
| Max | 7 | 14 |
| Pubs with >5 themes | 0.2% | 16.9% |

## Why abstract-level stays canonical for trends

Full-text tagging is **not year-comparable**: OA availability skews to recent
papers, so full-text mode would mechanically inflate recent-year theme counts
and manufacture spurious "hot areas."

| Year | Pubs | With full text | Coverage |
| ---: | ---: | ---: | ---: |
| 2022 | 79 | 23 | 29% |
| 2023 | 157 | 56 | 36% |
| 2024 | 343 | 141 | 41% |
| 2025 | 520 | 260 | 50% |
| 2026 | 253 | 111 | 44% |

Coverage rises ~29% → ~50% across the trend window. The roadmap-refresh
temporal analysis therefore reads `publications_tagged.jsonl` (abstract layer);
the full-text layer is a complementary cross-sectional view.

## What full text changes (theme shares)

Theme **rankings are preserved** — the big themes stay big. But **cross-cutting
and infrastructure themes are systematically under-counted by abstracts**: they
are discussed in the body (methods, engagement, disparities sub-analyses) far
more than abstracts advertise.

| # | Theme | Abstract % | Full-text % | Δ pts | ratio |
|---|---|---:|---:|---:|---:|
| 3 | Methods, infrastructure & phenotyping (non-genomic) | 18.3% | 46.0% | +27.7 | 2.5× |
| 17 | ELSI, participant engagement & recruitment | 4.9% | 21.2% | +16.3 | 4.3× |
| 6 | Social determinants of health & health disparities | 32.9% | 49.1% | +16.2 | 1.5× |
| 1 | Cardiometabolic disease | 28.4% | 40.2% | +11.8 | 1.4× |
| 4 | Mental health, behavioral & substance use | 18.8% | 28.4% | +9.5 | 1.5× |
| 14 | Neurology (non-ADRD) | 5.7% | 13.0% | +7.3 | 2.3× |
| 2 | Genomics methods & complex-trait genetics | 24.9% | 31.7% | +6.8 | 1.3× |
| 8 | Infectious disease & immunology | 6.0% | 11.6% | +5.6 | 1.9× |
| 5 | Cancer | 12.7% | 18.3% | +5.5 | 1.4× |
| 7 | Wearables & digital health | 5.4% | 9.7% | +4.3 | 1.8× |
| 10 | Rare disease & Mendelian genetics | 3.8% | 8.0% | +4.2 | 2.1× |
| 13 | Respiratory & sleep medicine | 4.2% | 7.7% | +3.5 | 1.8× |
| 9 | Autoimmune & inflammatory disease | 7.6% | 10.8% | +3.2 | 1.4× |
| 11 | Aging, frailty & ADRD | 5.5% | 8.7% | +3.2 | 1.6× |
| 15 | Pregnancy, maternal & women's health | 2.7% | 5.7% | +3.1 | 2.2× |
| 12 | Dermatology | 13.9% | 15.8% | +1.8 | 1.1× |
| 18 | Ophthalmology, ENT & sensory medicine | 7.6% | 9.0% | +1.4 | 1.2× |
| 16 | Pharmacogenomics & drug response | 2.4% | 3.4% | +1.0 | 1.4× |
| 19 | Environmental health & climate | 0.6% | 1.1% | +0.6 | 2.0× |

**Takeaway for the roadmap:** abstract-level shares *under-report* AoU's
methods/phenotyping, ELSI/engagement, and SDOH work the most. When citing
cross-cutting or infrastructure contributions, prefer the full-text layer (and
say so); for disease-theme rankings and any temporal/peer claim, the abstract
layer is the defensible series.

## Reproduce

```bash
python3 fetch_fulltext.py                 # cached; --no-net to build from cache
AOU_TAG_MODE=abstract python3 tag_corpus.py   # canonical
AOU_TAG_MODE=fulltext python3 tag_corpus.py   # full-text layer
```

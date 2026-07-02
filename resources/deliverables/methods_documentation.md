# All of Us Scientific Roadmap Refresh — Methods Documentation

End-to-end methods for the evidence base behind the Roadmap Refresh deliverables
(executive summary, slide deck, data-types list). Written for human editors and
for defensibility: every headline number traces to a script and a data file in
this repository. Corpus frozen for handoff on **2026-07-02** (see §2).

---

## 1. Overview

Seven evidence workstreams feed the recommendations:

| # | Workstream | Directory | Core question |
| --- | --- | --- | --- |
| 1 | Corpus acquisition | `aou-research-landscape/` | What has AoU produced (pubs + workspaces)? |
| 2 | Theme tagging | `aou-research-landscape/` | What is AoU science *about*? |
| 3 | IC attribution | `aou-research-landscape/` | Which NIH ICs fund it? |
| 4 | Focus-area crosswalk + trends | `aou-roadmap-refresh/` | Do the 8 focus areas still fit? What's changed since 2023? |
| 5 | Peer-biobank comparison | `peer-biobanks/` | How does AoU differ from UKB/FinnGen/MVP/CKB? |
| 6 | Emerging-trends horizon scan | `emerging-trends/` | What's rising in the field that AoU hasn't captured? |
| 7 | Researcher Workbench analysis | `rw-analysis/` | Platform gaps vs comparators; methods not yet used; what to build |

NIH-strategic-plan alignment (`aou-ic-alignment/`) and disease-burden context
(`disease-burden/`) are supporting analyses (see §10 for their status).

---

## 2. Corpus acquisition & freeze status

**Publications.** Pulled from the AoU WordPress cache of the PMI Ops
publications feed (`researchallofus.org/wp-json/rh-data-caching/publications-report`).
The feed is reconciled against PubMed/iCite. **1,432 records** (originally 1,378
on 2026-06-02; refreshed +54 on 2026-06-26). Field coverage: title 100%, year
100%, journal 98%, PMID 97%, DOI 91%, abstract 85%, PMC id 69%.

**Workspaces / projects.** The production project-directory endpoint returns
HTTP 500 (upstream RDR API down). We use the most recent Wayback Machine capture
(**2025-10-24**, 21,242 records). A substantive-research filter (drop
Educational-tagged, training-role, stub, and duplicate-title workspaces) yields
**12,899 substantive workspaces**.

**Freeze (2026-07-02).** Re-pull confirmed publications analytically unchanged
(0 records added/removed, 0 changed titles/abstracts) and no projects endpoint or
newer archive available. The corpus is frozen at its freshest available state.

**Known data limitations.** (a) Workspace snapshot is ~8 months old; a live
prod pull should replace it when the endpoint recovers. (b) Grant/funding info is
free-text and only ~34% populated. (c) No publication↔workspace linkage in the
feeds. (d) Abstract coverage 85% (title-only tagging for the rest — see §2b).

### 2b. Full-text augmentation
For richer tagging input, `fetch_fulltext.py` pulls Europe PMC JATS full text for
records with a PMC id (**612 articles**, body text only — references,
acknowledgments, tables stripped to avoid keyword pollution) and back-fills
missing abstracts (10 fillable; the rest are genuinely abstract-less editorials).
Details + the OA-coverage-by-year confound in
`aou-research-landscape/fulltext_augmentation.md`.

---

## 3. Theme tagging (19-theme taxonomy)

A locked 19-theme taxonomy (`taxonomy.md`) spans both corpora. `tag_corpus.py`
tags each record by keyword rules on **title + abstract** (specific keyword, or
≥2 general keywords, or ≥1 general keyword in title). Two layers via
`AOU_TAG_MODE`:

- **Abstract-level (canonical)** — year-comparable and comparable to the
  abstract-only peer biobanks. Feeds all trend and peer analyses.
- **Full-text-augmented** — appends PMC body text where available; a richer
  cross-sectional map. **Not** year-comparable (OA availability skews recent), so
  it is *not* used for trends.

Gap-filled abstracts feed both layers. `META` detection (program-meta/news items)
excludes non-substantive records. Mean themes/pub: 2.06 (abstract) vs 3.39
(full-text). **Caveat:** keyword tagging; peer corpora not audited (see §5).

---

## 4. IC attribution

`ic_attribute.py` parses NIH grant IDs from publication grant strings and
resolves them to administering + co-funding ICs via the NIH RePORTER API
(cached in `raw/reporter/`). **422/1,432 pubs (30%)** carry ≥1 IC attribution
(grant strings are only ~32% populated). Top admin ICs: OD, TR, HL, HG, CA.
OD dominance is structural (AoU is OD-funded).

---

## 5. Focus-area crosswalk & temporal trends

`crosswalk.py` maps the 19 themes onto the 8 focus areas (+ a proposed 9th).
`temporal.py` computes pre-2023 vs post-2023 theme/focus-area shares and trend
scores, and runs 8 "hot-area" regex detectors (HA1–HA8). The pre-2023 base is
small (157 pubs) so % "growth" reads as "presence built," not "outpacing the
field." Outputs are the CSVs in `aou-roadmap-refresh/`; narrative in
`temporal_trends.md` and `crosswalk_19_to_8.md`.

---

## 6. Peer-biobank comparison (full census)

Four peers pulled from PubMed by name-search (`acquire.py`,
`acquire_ukb_stratified.py`): **UK Biobank 11,868, FinnGen 3,152, MVP 438, CKB
558** — complete censuses (UKB is year-windowed to beat NCBI's ~9,999-per-query
esearch cap). Peers tagged with the *same* tagger (`tag_peers.py`) for
apples-to-apples theme shares; `compare.py` computes the AoU-vs-peer index.
**Caveats:** name-search over/under-includes; peers are not audited (≈5–10% lower
precision than the audited AoU corpus); read the **static share index**, not
trend differentials. Full writeup in `peer-biobanks/comparison.md`.

---

## 7. Emerging-trends horizon scan

Open-discovery scan for trends rising in the field but absent in AoU:

- **Discovery corpora** (leading edge, lead published work 1–2 yrs): **293,979
  bioRxiv+medRxiv preprints** + **422,565 NIH RePORTER grants** (2021–2026),
  pulled in full (`fetch_preprints.py`, `fetch_grants.py`).
- **Detection:** pure-Python term-acceleration (recent vs prior doc-share),
  `compute_emergence.py`.
- **Topic induction:** open-discovery LLM clustering of the top accelerating
  terms → 24 topics (not the locked taxonomy), artifacts excluded.
- **Gap-check:** each topic matched vs AoU (1,428) + the 4 peers + published-
  literature trajectory (`gap_check.py`); then an **AoU-feasibility overlay**
  (data assets) separates actionable white space from out-of-model frontiers.
- **Caveat:** NIH RePORTER `pref_terms` vocabulary changes inflate some grant
  growth; AI findings rest on named tools in author-written preprint text.

Report: `emerging-trends/emerging_trends_report.md`.

---

## 8. Researcher Workbench analysis

Three parts (`rw-analysis/`):
- **Part 1 — capability/data-asset gaps** vs N3C, Terra/AnVIL, BioData Catalyst,
  UKB-RAP, Kids First across 8 dimensions (`part1_capability_gaps.md`).
- **Part 2 — trending methods not yet adopted** on the RW, using the workspace
  corpus + a reuse/collaboration evidence pack (`part2_trending_methods.md`).
- **Part 3 — recommended tools/artifacts** to build (`part3_recommended_tools.md`).
- **BAA/LLM/egress brief** (`baa_llm_egress_evidence.md`).

**Citation integrity:** every Part-1 claim carries a URL + verbatim quote that was
re-fetched and confirmed on-page — **87/87 verified** (`verify_citations.py`,
audit trail in `citations_verified.csv`). Unverifiable claims were dropped.

---

## 9. Reproducibility

Each directory has a README and runnable scripts. Regeneration order:

```bash
# corpus + tagging (aou-research-landscape/)
python3 extract.py            # publications.* / projects.*
python3 ic_attribute.py       # publications_with_ic.*
python3 fetch_fulltext.py     # full-text augmentation (cached)
AOU_TAG_MODE=abstract python3 tag_corpus.py   # canonical
AOU_TAG_MODE=fulltext python3 tag_corpus.py   # full-text layer
# trends (aou-roadmap-refresh/)
python3 crosswalk.py && python3 temporal.py
# peers (peer-biobanks/)
python3 acquire.py && python3 acquire_ukb_stratified.py && python3 tag_peers.py && python3 compare.py && python3 hot_areas_peers.py
# horizon scan (emerging-trends/)  — raw pulls gitignored, ~2.2 GB
python3 fetch_preprints.py && python3 fetch_grants.py && python3 compute_emergence.py
# RW analysis (rw-analysis/)
python3 gap_check_methods.py && python3 collaboration_evidence.py && python3 verify_citations.py
# deliverables (deliverables/)
cd figures && python3 make_figures.py && cd .. && python3 build_deck.py
# PDFs from HTML (headless Chrome):
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --no-pdf-header-footer \
  --print-to-pdf=AoU_Roadmap_Refresh_Executive_Summary.pdf "file://$PWD/executive_summary.html"
```

Large raw caches (grant/preprint JSONL, PMC XML, peer efetch XML) are gitignored
and regenerable from the scripts.

---

## 10. Consolidated caveats

1. **Workspace snapshot is 2025-10-24** (prod endpoint down); collaboration/
   adoption stats reflect that date.
2. **Keyword tagging** (not per-record ML): directional, order-of-magnitude
   robust; PRS (10% of workspaces) / PheWAS validate that it tracks real use.
3. **Peer corpora unaudited** — use share index, not trend differentials.
4. **Grant/IC coverage** ~30% (free-text grant strings).
5. **Full-text tagging** not year-comparable (OA recency skew).
6. **Grant term-emergence** partly reflects RePORTER vocabulary onsets.
7. **IC-alignment & disease-burden modules** were *not* re-executed on the
   refreshed corpus (the 54 new pubs added no resolvable grants and shifted theme
   shares <0.5 pt); their cross-corpus figures were updated and dated notes added.
8. **RW comparator specifics** reflect 2025–2026 vendor docs; confirm exact
   AoU-collection enablement in-environment.

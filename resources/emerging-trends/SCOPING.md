# Emerging-trends analysis — scoping memo (2026-06-26)

**Goal.** Scan the *general* biomedical literature for trends that are
**accelerating** but **not yet realized in AoU or the peer biobanks** — i.e.
white-space the AoU Roadmap could move into early.

## Decisions locked (with the user)

| Choice | Decision |
| --- | --- |
| Source corpus | Grants + preprints + PubMed (all three) |
| "Emerging" signal | **Recent acceleration** (fast growth in ~2023–2026) |
| Topical scope | **Truly general** biomedical (filter for AoU-relevance at the end) |
| Detection method | **Open discovery** (data-driven, not the locked 19-theme taxonomy) |
| Deliverable | Ranked emerging white-space report: each trend with growth signal · where it's hot · AoU/peer coverage · AoU feasibility |
| Gap basis | vs AoU corpus (1,428) + 4 peer biobanks (UKB/FinnGen/MVP/CKB) |
| Process | **Scope first, sign-off, then full run** |

## Source feasibility (measured 2026-06-26)

| Source | Volume | Pull strategy |
| --- | --- | --- |
| Published (Europe PMC `SRC:MED`) | ~1.5M/yr (~6M for 2023–26) | **Do NOT bulk-pull.** Query only *discovered candidate terms* by year (targeted counts) to locate/validate where a trend is hot. |
| Preprints (`SRC:PPR`) | ~180k/yr | Core discovery corpus — leading edge. |
| └ bioRxiv | 338k all-time (~49k/2025) | Pull full 2021–2026. |
| └ medRxiv | 78k all-time (~14k/2025) | Pull full 2021–2026. |
| NIH RePORTER grants | ~76k projects/FY | Pull abstracts+terms FY2021–2026 — funding = earliest signal. |

**Why this split:** preprints and grants *lead* published work by 1–2 years, so
they are where "not-yet-realized" trends appear first — and both are tractable to
pull in full (~300k preprints + ~300k grant records). The 6M-record published
corpus is used only as a **targeted lookup** for terms we've already discovered,
which avoids an intractable bulk pull while still telling us whether a trend has
crossed into the mainstream literature.

## Method (no sklearn / embeddings needed)

Only `numpy` + `matplotlib` are installed (no sklearn/sentence-transformers).
The plan deliberately avoids fragile model downloads:

1. **Term-emergence detection (pure Python).** Tokenize titles+abstracts into
   uni/bi/tri-grams (stopword-filtered), build a year×term document-frequency
   table, and score each term's **acceleration** (recent share vs prior share,
   recency-weighted; min-count gate). Computed independently on preprints and on
   grants.
2. **LLM topic induction (open discovery).** Feed the top ~300–500 emerging
   terms + exemplar titles to LLM sub-agents that cluster them into coherent
   *emerging topics*, label each, drop noise, and dedupe. This replaces
   embeddings/clustering and — critically — filters the boilerplate noise mode
   (see below).
3. **Locate in published literature.** For each discovered topic, run targeted
   Europe PMC / PubMed year counts to chart its mainstream trajectory.
4. **Gap-check vs AoU + peers.** Keyword/again-LLM match each topic against the
   AoU tagged corpus (1,428) and the 4 peer-biobank corpora to score
   "realized / partially / not yet."
5. **Rank** by (acceleration × absence-in-AoU), annotate AoU feasibility
   (is it cohort/EHR/genomic/wearable-addressable?), and write the report.

## Demo proof (medRxiv 2022 → 2025, full year slices)

Pulled 10,523 (2022) + 13,841 (2025) medRxiv abstracts and scored bigram
acceleration. The method **works** — top genuine emerging signals:

- **LLMs in medicine** — `large language` (0.05%→2.8%, 59×), `zero shot`,
  `retrieval augmented generation`, `prompt engineering`. Dominant signal.
- **`avian influenza`** (H5N1) — emerging public-health threat.
- **`steatotic liver`** (MASLD/MASH) — the 2023 NAFLD→MASLD renaming;
  genuinely new terminology entering the literature.

**Noise mode found (and its mitigation).** Many top "emerging" bigrams are
LLM-writing boilerplate that surged in 2024–25 because papers are increasingly
LLM-drafted (`offering insights`, `underscores potential`, `offers scalable`,
`remains underexplored`…). This is real, but it is a *writing-style* artifact,
not a research trend. Mitigations: (a) an expanded boilerplate stoplist;
(b) the LLM topic-induction stage, which trivially separates real topics from
academic filler; (c) preferring noun-phrase terms over verb/adjective phrases.

## Proposed full run (for sign-off)

1. Pull bioRxiv+medRxiv 2021–2026 (~300k docs) and RePORTER FY2021–2026
   (~300k records); cache raw (gitignored).
2. Compute term-emergence on each; merge candidate lists.
3. LLM topic induction → ~30–60 coherent emerging topics, labeled & denoised.
4. Targeted published-literature trajectory per topic.
5. Gap-check vs AoU + peers; rank; write `emerging_trends_report.md` +
   a ranked CSV.

**Effort:** ~25–35 min of pulls + a handful of LLM induction agents. Raw caches
gitignored per the lean-repo decision.

## Open choices to confirm before the full run

- **Preprint breadth:** bioRxiv+medRxiv only (cleaner biomedical), or widen to
  all `SRC:PPR` (+Research Square, SSRN, Preprints.org — more volume, more noise)?
- **Year span:** 2021–2026 (5y, more baseline) vs 2022–2026 (tighter on "recent").
- **Granularity:** how many final topics (~30 tight vs ~60 broad)?

# Emerging biomedical trends & AoU white-space (2026-06-26)

**Question.** What is *accelerating* in the broad biomedical literature that
**All of Us (and peer biobanks) have not yet picked up** — and which of those
gaps could AoU actually act on?

## TL;DR

The fastest-rising frontier in biomedicine right now is **AI/ML** —
LLMs/agentic systems, foundation models (genomic, protein, single-cell), and
AI structure prediction — plus a **single-cell/spatial omics** wave and an
**aging-biology** surge. AoU is essentially **absent** from all of these in its
publication corpus (<0.3% for most).

But absence ≠ opportunity. Filtering by what AoU's *data model* can actually
support, the **actionable white space** is narrower and clear:

1. **Genomic foundation models** — AoU's diverse WGS + EHR labels are an ideal
   training/eval substrate; ~0% AoU presence today. Highest-value gap.
2. **LLMs + agentic AI on EHR / the Workbench** — AoU has the text and the
   compute platform; near-zero literature presence.
3. **MASLD/MASH** — adopt the 2023 steatotic-liver renaming as an EHR phenotype.
4. **Aging epidemiology** (not bench senescence biology) and **digital-health/
   wearables AI**.

Much of the rest (protein structure, single-cell/spatial tissue omics, iPSC,
gene-editing wet-lab) is a genuine frontier **outside AoU's data model** — worth
watching, not building.

This strongly reinforces the Roadmap's proposed **9th focus area "Data, AI &
Methods"**: the literature's leading edge is precisely the orphan AoU already
flagged.

## Method

| Stage | What |
| --- | --- |
| Discovery corpora | bioRxiv+medRxiv preprints **293,979** (2021-26) + NIH RePORTER grants **422,565** (FY21-26). Preprints/grants *lead* published work by 1-2 yrs. |
| Detection | Pure-Python term-emergence: year×n-gram doc-frequency, acceleration = recent (2024-26) vs prior (2021-23) share, recency- and size-weighted. |
| Topic induction | Open-discovery LLM clustering of the top ~600 accelerating terms → 24 coherent topics (+6 artifact clusters excluded). |
| Gap-check | Keyword match each topic vs AoU (1,428) + peers (UKB/FinnGen/MVP/CKB); Europe PMC published trajectory (2021→2025). |
| Feasibility overlay | Each topic rated against AoU's data assets (WGS, EHR, surveys, wearables, Workbench — **not** tissue assays/protein structures/imaging). |

Scripts: `fetch_preprints.py`, `fetch_grants.py`, `compute_emergence.py`,
`gap_check.py`; data in `emerging_topics.json`, `emerging_whitespace.csv`,
`emerging_final.json`.

## Tier 1 — Actionable white space (emerging · absent in AoU · AoU-feasible)

Sorted by actionability (emergence × absence × AoU-feasibility). "Peak growth" =
fastest-accelerating member term; "Pub 2025" = Europe PMC published count.

| Trend | Peak growth | AoU | Peers | Pub 2025 | Pub growth 21→25 | AoU feasibility |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Genomic / DNA sequence foundation models | 944.8× | 0.14% | 0.21% | 11,365 | 4.0× | high |
| LLMs / foundation chat models in biomedicine | 386.0× | 0.21% | 0.12% | 27,126 | 46.8× | high |
| Aging biology, senescence & longevity | 5608.9× | 0.0% | 1.27% | 51,239 | 1.2× | med (epi only) |
| Agentic AI & autonomous reasoning | 100.8× | 0.28% | 0.04% | 17,972 | 18.8× | high |
| MASLD/MASH steatotic liver (renaming) | 18.1× | 0.7% | 2.39% | 18,902 | 1.6× | high |
| Neurodegeneration & proteinopathies | 1175.3× | 1.33% | 2.1% | 44,432 | 1.2× | med (epi only) |
| mHealth & digital-health interventions | 1855.7× | 0.7% | 0.03% | 22,333 | 2.8× | med |
| Retrieval-augmented generation / knowledge assistants | 41.4× | 0.0% | 0.31% | 1,330 | 60.5× | med |
| Interpretable / zero-shot / generative ML methods | 47.0× | 4.75% | 5.5% | 159,891 | 5.6× | med |

### The three to act on

- **Genomic foundation models** (DNA language models — Evo, Nucleotide
  Transformer, AlphaGenome-style). Published work 4× since 2021 and ~0% in AoU.
  AoU's *diverse, consented WGS linked to longitudinal EHR* is arguably the best
  public substrate in the world for training/benchmarking ancestry-fair genomic
  FMs — a distinctive asset no peer biobank matches. **This is the single
  highest-leverage gap.**
- **LLMs + agentic AI on EHR / Workbench.** Published LLM-in-medicine work grew
  **47×** (2021→2025); AoU is at 0.2%. AoU already proposes a Workbench "AI
  co-scientist" (Rec 4) — this analysis is the external evidence that the field
  has moved decisively here. RAG/knowledge-assistants (60× published growth) is
  the concrete near-term build.
- **MASLD/MASH.** Not AI — a disease-definition shift. The 2023 NAFLD→MASLD
  renaming is now standard; AoU touches it in only 0.7% of pubs. Adopting MASLD
  as a curated EHR+labs phenotype is low-effort, high-credibility.

> "Aging biology" and "neurodegeneration" are **split**: the *epidemiology /
> EHR-biomarker* slice is feasible and a real AoU opportunity, but the *cellular
> senescence / proteinopathy bench biology* driving the headline growth is not
> AoU-addressable. Treat the feasible slice only.

## Tier 2 — Watch: real frontiers OUTSIDE AoU's data model

Genuinely emerging and genuinely absent from AoU — but AoU cannot act without
new assay modalities it does not collect. Listed for situational awareness, not
as recommendations.

| Frontier | Peak growth | AoU | Pub 2025 | Why not AoU |
| --- | ---: | ---: | ---: | --- |
| Single-cell & single-nucleus multi-omics | 5828× | 0.0% | 6,595 | needs tissue single-cell assays AoU doesn't collect |
| Spatial / single-cell analysis methods | 1998× | 0.84% | 107,731 | tissue-assay analysis; outside AoU data model |
| Spatial transcriptomics & in situ profiling | 56.6× | 0.14% | 83,245 | needs tissue spatial assays |
| AI protein structure & binding (AlphaFold3/Boltz) | 338.7× | 0.07% | 17,387 | no protein structure data in AoU |
| Protein language models & ML protein design | 40.6× | 0.0% | 2,824 | protein sequence/structure ML |
| iPSC-derived & induced cell models | 99× | 0.21% | 11,044 | wet-lab cell models |
| Gene editing & gene-targeted therapy | 1587× | 0.28% | 16,293 | could only track clinical *outcomes* via EHR, long-term |
| Antimicrobials & AMR | 3853× | 0.07% | 44,638 | EHR Rx/resistance signals possible, not primary |
| Emerging arbo/flaviviruses & antivirals | 4171× | 0.0% | 37,006 | EHR capture possible, not primary |
| H5N1 avian influenza | 41.4× | 0.0% | 8,423 | EHR surveillance possible, not primary |
| Single-cell foundation models | 22.9× | 0.0% | 72 | trained on single-cell atlases AoU lacks |

## Tier 3 — Already core to AoU (validation, not white space)

These rose in the *grant* signal but are AoU's existing identity, not gaps —
a useful sanity check that the pipeline isn't mislabeling AoU strengths as gaps.

| Topic | AoU | Note |
| --- | ---: | --- |
| Community-engaged & participatory research | 0.91% | AoU foundational strength (and grant-vocabulary artifact) |
| Health disparities: women & minority populations | 3.49% | AoU's UBR mission; AoU already over-indexes |
| Disability & functional impairment | 0.35% | AoU disability UBR + surveys |
| Older adults & late-life health | 1.75% | AoU aging cohort; ~at peer median |

## How this connects to the Roadmap Refresh

- The **#1 and #2 actionable gaps (genomic FMs, LLMs/agentic AI)** are exactly
  the **"Data, AI & Methods" 9th-focus-area** orphan (Rec 1) and the
  **Workbench AI co-scientist** (Rec 4). This is independent, external
  confirmation that those recommendations are pointed at the field's leading
  edge — strengthen them with this evidence.
- **MASLD** is a cheap, concrete phenotype win for the cardiometabolic line.
- The **Tier-2 "outside our data model"** list is a strategic boundary
  statement: AoU should *not* chase single-cell/spatial/protein-structure
  science, but *can* be the population-scale partner that links those
  discoveries to diverse human phenotypes.

## Caveats

- **Grant pref-terms vocabulary changes** inflate some growth multipliers
  (e.g., "anti-viral agents" prior=0 → 7000×): RePORTER added controlled terms
  over time. Excluded the obvious ones; flagged the rest. **Preprint signals
  (author-written text) are the trustworthy ones** — the AI findings rest on
  named tools (AlphaFold3, GPT-4o/5, DeepSeek, Boltz-2), not generic terms.
- **Keyword coverage** uses substring matching; small false-positive/negative
  rates. AoU percentages are directional, but the order-of-magnitude gaps
  (0.x% vs a 47× field) are robust.
- **Preprint-led by design** — favors fast-moving computational/methods fields
  over slow clinical topics; intended, since the goal is the leading edge.
- **2026 is partial** (pulled mid-year); shares (not raw counts) are used.
- Published trajectory is a *targeted* Europe PMC count per topic, not a full
  re-tag of the 6M-record published corpus.

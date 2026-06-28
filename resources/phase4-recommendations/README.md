# Phase 4 — Top-3 recommendations per 2026 AoU Science Committee need area

The 2026 Working Groups (WGs) are **topic / need areas** the program has
already recognized as priorities — not decision or governance bodies. Their
topics overlap and should be **coordinated** across need areas. The WG labels
below are used as topic references, and "Lead:" lines note the chairs for each
topic.

**Draft inputs for the Scientific Roadmap Refresh co-lead (Haendel).**
Generated 2026-06-02 from the evidence base in this repository:

- `aou-ic-alignment/gap_analysis.md` + `per_ic_briefs/`
- `aou-roadmap-refresh/crosswalk_19_to_8.md` + `temporal_trends.md`
- `peer-biobanks/emerging_themes.md` + `aou_vs_peers_index.csv`
- `aou-research-landscape/taxonomy.md`
- `disease-burden/burden_vs_attention.md` (burden × attention; added June 2026)
- `strategic-plans/nasem/` (NASEM consensus reports; added June 2026)
- Slide 7 of `2026 Science Committee Working Groups.pptx` (the "what's changed since 2023" priority list)

## Method

For each need area, this folder contains a markdown file enumerating 5–8
candidate recommendations pulled from the evidence base, the top-3 ranked
recommendations scored against the Committee's 8-criterion prioritization
rubric (1=low, 4=high; N/A excluded from the mean), and an "also-considered"
list with one-line deprioritization reasoning. The scores are a
prioritization aid, not an action taken on any recommendation.

The rubric is the format Jordan Smoller established in the November 5, 2024
Pre-Processed Data subgroup deck. Worked-example scores landed mean 1.40–4.00;
most were 3.0–3.8. For *strategic* recommendations (e.g., focus-area rename,
investment ask) some criteria don't cleanly apply — those are marked N/A
rather than forced.

## Files

| File | WG | Lead(s) |
|---|---|---|
| `wg1_roadmap_refresh.md` | Scientific Roadmap Refresh | Smoller & Haendel |
| `wg2_translational.md` | Translational Science Research Agenda | Sanchez & Cohn |
| `wg3_imaging.md` | Imaging Integration | Burnside & Giannini |
| `wg4_ai_strategies.md` | AI Strategies | Sastry |
| `wg5_communications.md` | Scientific Communications | Korf |
| `cross_cutting_synthesis.md` | — | Multi-WG / Sci Com narrative |
| `tooling_recommendations.md` | Cross-WG (WG-2 × WG-4) | Tooling/DB-integration; added per June 3, 2026 |

## How to use

This is the **draft** to inform the need-area lead's editorial judgment. Show
your work back across the need areas; expect the rubric scores per cell to
spark disagreement and that is the point. Top-3 limits are hard (per the Sci
Com format).

## Caveats inherited from the evidence base

- **Dermatology over-representation is an artifact** (1–2 prolific groups,
  14.3% of corpus, peer index 7.8×). Do NOT elevate dermatology even though
  the share index says to. This is flagged as known noise.
- **Peer-biobank counts use PubMed-name-search fallback** — use share-index
  (`aou_vs_peers_index.csv`) not trend differentials.
- **Smoller-already-prioritized**: PheWAS×GWAS (4.00, addressed by All by All),
  Phecodes update (3.80), validated phenotypes/PheKB (3.80), NLP/CLAMP (3.40).
  Recommendations here build *on* these, not duplicate.
- **HPO-using federal pipelines (GREGoR, INCLUDE, UDN, eMERGE, ClinGen,
  ClinVar, MedGen)** — out of scope for AoU WGs but worth referencing as
  external standards alignment context for the genetics/multi-omics framing.

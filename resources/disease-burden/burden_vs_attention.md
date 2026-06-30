# Disease burden vs. AoU research attention

> **Note (2026-06-26):** AoU theme shares updated to the refreshed 1,432-pub corpus; disease-burden (GBD) figures are external and unchanged.

**Disease-burden evidence layer, AoU Scientific Roadmap Refresh.**
Added per the June 3, 2026 WG request (JMV: *"consider including disease
burden"*; Melissa: *"will add along with PubMed trends"* — see
`../wg-meeting-notes/2026-06-03_second-meeting.md`).

This layer overlays **disease burden** (how much a condition harms the US
population) and **NIH funding alignment** onto the existing AoU corpus
attention map (`../aou-research-landscape/theme_summary.csv`,
`../aou-roadmap-refresh/crosswalk_19_to_8.md`). It answers a question the prior
analyses did not: **is AoU's research attention pointed at the conditions that
carry the most population burden — and where it isn't, is that a gap the
Refresh should name?**

It is also the empirical backing for Geoff's framing point (05-21): *start from
the questions/needs, then the data* — burden is the most defensible external
definition of "need."

---

## 1. The national backdrop: funding tracks burden weakly

Four independent analyses converge on one finding the Refresh should state
plainly: **NIH funding aligns weakly and inconsistently with disease burden.**

- Across 27 conditions and five burden measures, the correlation is **R² < 0.03
  excluding HIV**; DALYs give the strongest relationship and even that is only
  **R² ≈ 0.15** ([persistence paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11754078/)).
- 2008–2021, a 1% rise in DALYs/100k bought only a **0.31% rise in NIH funding
  per capita**, and the association is **absent in 2008 and in every single
  year of the past five** ([npj Health Systems 2025](https://www.nature.com/articles/s44401-025-00048-x)).
- Cross-sectionally funding looks proportional (**R² ≈ 0.31**) but **change in
  burden over a decade is uncorrelated with cumulative spend (p = 0.65)**;
  mental, neurologic, and substance-use disorders **underperform relative to
  investment** ([Nimgaonkar 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9164716/)).
- Globally, research effort and burden have diverged for noncommunicable
  disease, and the gap is projected to **widen ~⅓ over two decades**, faster
  with US international-funding withdrawal ([Nature Medicine 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12443587/)).

**Why this matters for AoU.** AoU does not allocate NIH dollars, but it *is* a
shared substrate that determines which questions become answerable at scale. If
the cohort's data assets and tooling are pointed at the same conditions that
are already over-attended, AoU inherits the national misalignment. If they are
deliberately pointed at high-burden, under-attended conditions, AoU becomes a
**corrective instrument** — a concrete, defensible value proposition for the
roadmap and for IC engagement.

## 2. Method

Each of the 19 locked themes (`../aou-research-landscape/taxonomy.md`) is
assigned a **US burden tier** — High / Medium-High / Medium / Low /
Cross-cutting — anchored to **GBD 2021 US leading-cause rankings** (IHME;
[state-level US analysis](https://www.healthdata.org/research-analysis/library/burden-diseases-injuries-and-risk-factors-state-usa-1990-2021)).
"Cross-cutting" marks methods/risk/equity themes that are not single diseases
and carry burden only via the conditions they touch. The tier is **analyst
judgment from the published GBD rankings, not an invented DALY point-estimate**
(see `sources.md` for why). Burden tier is then read against AoU corpus pub
share (`theme_burden_tiers.csv`) to classify each theme **Aligned /
Under-indexed / Over-indexed / Absent**.

This is deliberately a *first-pass tiering*. A sharper version joins the RCDC
categorical-spending table (FY2008–2024, [report.nih.gov](https://report.nih.gov/funding/categorical-spending))
and GBD US cause-level DALYs to AoU theme counts for an exact
burden × dollars × attention triple — flagged as a follow-on in `sources.md`.

## 3. Findings

### 3.1 The headline gap: musculoskeletal / low back pain has no theme at all

**Low back pain is the single leading cause of years lived with disability in
the US** (in both 1990 and 2021), and osteoarthritis and neck pain are also top
YLD causes ([GBD US](https://www.healthdata.org/research-analysis/library/burden-diseases-injuries-and-risk-factors-state-usa-1990-2021)).
**The AoU taxonomy has no musculoskeletal theme.** This cluster is not buried in
another theme the way imaging is buried in theme 3 — it is simply absent. For a
cohort whose pitch is population-scale real-world data, the absence of the
nation's #1 disability driver is the most striking burden-attention gap in the
corpus and the clearest single thing the Refresh can name.

### 3.2 High-burden, under-indexed themes

| Theme | Burden anchor | AoU pub share | Read |
|---|---|---:|---|
| 11 Aging, frailty & ADRD | Alzheimer's/dementias top & **rising** US DALYs | 5.5% | Under-indexed — and nationally *over*funded post-2016, so AoU attention lags both burden and dollars. |
| 13 Respiratory & sleep | COPD top US DALYs; sleep apnea high prevalence | 4.3% | Under-indexed high-burden cluster. |
| 14 Neurology (non-ADRD) | Stroke, migraine (high YLD), epilepsy, Parkinson's | 5.6% | Mild gap on a high-YLD cluster; aligns with the literature's "neurologic underperforms vs investment." |
| 4 Mental health & substance use | Depression #2, drug use #3 US YLDs | 18.5% | Attention looks healthy, but this is exactly the cluster the funding literature flags as **chronically underfunded vs burden** — AoU is well-positioned to be a corrective here, and should say so. |

### 3.3 The inverse gap: low-burden, over-indexed

**Dermatology** is 13.9% of the AoU pub corpus — the third-largest theme —
despite skin disease carrying **low DALY/mortality burden**. The roadmap-refresh
evidence base already flags this as a **1–2-prolific-group artifact**
(`../phase4-recommendations/README.md`); the burden lens independently confirms
it: this is high research attention on a low-burden domain. The standing
guidance holds — **do not elevate dermatology** despite its corpus share.

### 3.4 Well-aligned themes (the cohort's burden-justified core)

Cardiometabolic disease (28.4%, IHD = #1 US DALYs) and cancer (12.8%, neoplasms
top DALYs) are both high-burden and high-attention — these are the
burden-justified core of the corpus and need no Refresh intervention beyond
continued support.

### 3.5 Emerging burden that lags categorization

[Long COVID](https://www.nature.com/articles/s43856-026-01516-7) is a large,
newly-quantified disability burden that **does not yet have a clean RCDC funding
category or a settled GBD cause** — precisely the kind of signal a longitudinal,
EHR-linked cohort surfaces before the funding taxonomy catches up. This is a
forward-looking argument for AoU as an **early-warning instrument** for
burden the national funding system has not yet recognized.

## 4. PubMed-trends companion (already in the evidence base)

The "PubMed trends" half of the June 3 ask is largely already built:
`../peer-biobanks/` indexes AoU's topic mix against UK Biobank, FinnGen, MVP,
and China Kadoorie, and `../aou-roadmap-refresh/temporal_trends.md` computes
post-2023 share shifts. The burden tiers here are designed to be read *against*
those trend signals — a theme that is **high-burden, under-indexed, and
trend-flat** (e.g., respiratory/sleep) is a stronger Refresh candidate than one
that is high-burden but already accelerating. The exact burden × trend join is
the natural next deliverable.

## 5. What the Refresh should take from this

1. **Name the musculoskeletal absence.** The #1 US disability driver has no
   home in the taxonomy or the 8 focus areas. Either add it or explain the
   omission.
2. **Frame AoU as a burden-corrective, not a burden-mirror.** The national
   funding system tracks burden weakly; AoU's distinct value is enabling
   burden-aligned questions (aging/ADRD, respiratory, the underfunded
   mental-health/substance cluster) that the dollar allocation does not.
3. **Hold the line on dermatology** — the burden lens reconfirms the artifact.
4. **Position AoU as an early-warning instrument** for emergent burden (Long
   COVID-type signals) that lags RCDC categorization.
5. **Sharpen with the exact join** — RCDC dollars × GBD DALYs × AoU theme counts
   — before the September 15 presentation if a quantified figure is wanted.

## 6. Files written by this layer

| File | Purpose |
|---|---|
| `sources.md` | Annotated burden/funding sources (the 6 June-3 links + GBD + RCDC) |
| `theme_burden_tiers.csv` | Per-theme US burden tier, AoU pub share, attention-vs-burden classification |
| `burden_vs_attention.md` | (this file) synthesis and Refresh implications |

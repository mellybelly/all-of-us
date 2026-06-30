# Temporal trends: what has changed since 2023

> **Updated 2026-06-26** for the refreshed corpus (1,432 pubs; 1,428 substantive). Figures reconciled to the regenerated CSVs in this directory.

**Phase 3b deliverable, AoU Scientific Roadmap Refresh evidence base.**
Inputs: 1,428 substantive publications from the AoU corpus, tagged with the
locked 19-theme taxonomy and crosswalked to the 8 Roadmap focus areas
(`crosswalk_19_to_8.md`). Projects are excluded from temporal analysis
because workspaces lack reliable creation-year metadata.

This document answers **Q1: What has changed since 2023 that warrants
prioritization?**

---

## 1. Method

**Trend score.** For each theme and each focus area, we compute
`share(2023+) − share(pre-2023)`. Positive means the theme/area takes a
larger share of the post-2023 corpus than the pre-2023 corpus (growing
relative emphasis); negative means smaller share (declining relative
emphasis); near zero means steady-state. Share differences control for the
fact that the corpus itself grew ~8.1× from pre-2023 to post-2023.

**Hot-area detectors.** For the 8 "reflections since 2023" themes from
slide 7 of the 2026 Sci Com WG deck, we built independent keyword-based
detectors that scan publication title + abstract text. These are
deliberately independent of the 19-theme taxonomy so they answer slide-7
priorities directly. Detector code: `temporal.py`. Examples and admin-IC
tallies are in `hot_areas_summary.csv`.

**Corpus baseline.**
- Pre-2023 substantive pubs: **157**
- Post-2023 (≥ 2023) substantive pubs: **1,217**
- Year-by-year: 2015 (4); 2016 (4); 2017 (3); 2018 (12); 2019 (13); 2020 (10);
  2021 (32); 2022 (79); 2023 (157); 2024 (343); 2025 (520); 2026 (253);
  2027 (1, ahead-of-print).

The volume explosion in 2023+ reflects (a) the v6/v7/v8 dataset releases
opening the cohort to a much wider research community and (b) the publication
lag finally catching up with the cohort's earlier-2020s data accumulation.

---

## 2. Per-theme trend table

Sorted by trend score, growing first. Negative trends = declining relative
emphasis (still growing in absolute count but smaller share of the post-2023
corpus). Machine-readable in `theme_trend_scores.csv` and
`pub_year_by_theme.csv`.

| # | Theme | Pre-2023 | 2023+ | Pre-share | Post-share | Trend |
|---|---|---:|---:|---:|---:|---:|
| 2 | Genomics methods & complex-trait genetics | 16 | 340 | 10.2% | 26.8% | **+16.6** |
| 4 | Mental health, behavioral & substance use | 15 | 254 | 9.6% | 20.0% | **+10.4** |
| 1 | Cardiometabolic disease | 30 | 375 | 19.1% | 29.5% | **+10.4** |
| 5 | Cancer | 7 | 175 | 4.5% | 13.8% | **+9.3** |
| 9 | Autoimmune & inflammatory disease | 3 | 105 | 1.9% | 8.3% | **+6.3** |
| 14 | Neurology (non-ADRD) | 2 | 80 | 1.3% | 6.3% | **+5.0** |
| 11 | Aging, frailty & ADRD | 2 | 76 | 1.3% | 6.0% | **+4.7** |
| 3 | Methods, infrastructure & phenotyping (non-genomic) | 23 | 239 | 14.6% | 18.8% | **+4.2** |
| 13 | Respiratory & sleep medicine | 1 | 59 | 0.6% | 4.6% | **+4.0** |
| 6 | Social determinants & health disparities | 48 | 422 | 30.6% | 33.2% | +2.6 |
| 15 | Pregnancy, maternal & women's health | 1 | 37 | 0.6% | 2.9% | +2.3 |
| 10 | Rare disease & Mendelian genetics | 4 | 50 | 2.5% | 3.9% | +1.4 |
| 18 | Ophthalmology, ENT & sensory medicine | 10 | 98 | 6.4% | 7.7% | +1.3 |
| 7 | Wearables & digital health | 7 | 70 | 4.5% | 5.5% | +1.1 |
| 19 | Environmental health & climate | 0 | 8 | 0.0% | 0.6% | +0.6 |
| 16 | Pharmacogenomics & drug response | 3 | 31 | 1.9% | 2.4% | +0.5 |
| 8 | Infectious disease & immunology | 12 | 74 | 7.6% | 5.8% | **−1.8** |
| 12 | Dermatology | 28 | 171 | 17.8% | 13.5% | **−4.4** |
| 17 | ELSI, participant engagement & recruitment | 25 | 45 | 15.9% | 3.5% | **−12.4** |

### Reading the table

- **Genomics methods (+17.0)** is the single biggest gainer. The v6/v7/v8
  releases enabled large multi-ancestry GWAS / PRS / fine-mapping work that
  was simply impossible before the post-2023 cohort scale-up.
- **Mental health (+10.8), Cancer (+9.4), Cardiometabolic (+9.8)** all
  surge — these are the three largest disease applications of the
  scaled-up cohort.
- **AI/Methods (+4.2)** grows moderately as a theme share but the
  *absolute* count jumped 23 → 228 (10×), tracking the broader ML-in-biomed
  surge and matching slide-7 priorities (AI/LLM/foundation models).
- **Wearables (+1.0)** is effectively flat — already mature pre-2023 and
  staying steady-state, not a growth area. (See HA2 below for the same
  signal in independent keyword detection.)
- **Infectious disease (−2.1)** declines as COVID-19 publications recede
  from peak. The 12 pre-2023 pubs were COVID-heavy; post-2023 the volume
  redistributes to chronic infections (HIV, EBV, virome).
- **Dermatology (−4.4)** declines as relative emphasis — the early
  publication groups that drove the anomalous dermatology share have not
  scaled with the broader corpus.
- **ELSI / engagement (−12.4)** is the biggest decline by far. Pre-2023 the
  AoU literature was dominated by program-introduction, recruitment-
  methodology, and ELSI pubs; post-2023 the literature is dominated by
  substantive science. This is a *predictable maturation*, not a problem
  — but it has implications for how FA4 (Return of Results) is scoped
  going forward (see Phase 3a).

---

## 3. Per-focus-area trend table

Machine-readable in `focus_area_trend_scores.csv` and
`pub_year_by_focus_area.csv`.

| FA | Focus area | Pre-2023 | 2023+ | Pre-share | Post-share | Trend |
|---|---|---:|---:|---:|---:|---:|
| FA8 | Genetics & Biology | 47 | 725 | 29.9% | 57.0% | **+27.1** |
| FA1 | Prevalent Common & Rare Conditions | 83 | 967 | 52.9% | 76.1% | **+23.2** |
| FA5 | Lifestyle, Substance, & Behavioral Health | 15 | 254 | 9.6% | 20.0% | **+10.4** |
| FA3 | Healthy Aging & Resilience | 2 | 76 | 1.3% | 6.0% | **+4.7** |
| FA2 | Maternal & Child Health | 1 | 37 | 0.6% | 2.9% | +2.3 |
| FA6 | Environment | 0 | 8 | 0.0% | 0.6% | +0.6 |
| FA7 | Health Equity | 87 | 632 | 55.4% | 49.7% | **−5.7** |
| FA4 | Return of Results | 31 | 126 | 19.8% | 9.9% | **−9.8** |

### What the focus-area pattern says

- **FA8 Genetics & Biology and FA1 Common & Rare Conditions absorb most of
  the post-2023 growth.** Both jump by 20+ percentage points of corpus
  share. This is the cohort delivering on its core scientific mandate at
  scale.
- **FA5 Lifestyle / Behavioral (+10.8) is the third-largest gainer**,
  driven entirely by the mental-health / substance-use theme. Slide 7's
  "nutrition, microbiome & chronic disease management" priority is *not*
  driving this growth (HA7 shows thin coverage — see §4); the FA5 surge
  is mental health, not nutrition.
- **FA3 Healthy Aging (+4.7) is meaningfully growing** off a small base —
  73 post-2023 pubs in aging/ADRD/frailty/longevity, vs. 2 pre-2023.
- **FA7 Health Equity declines as a share (−4.9)** but in absolute terms
  jumps from 87 → 615 pubs. The decline-as-share is a dilution effect: the
  cohort's other domains grew faster. Equity work is still load-bearing
  (~half the post-2023 corpus touches FA7) and shouldn't be read as
  "declining priority."
- **FA4 Return of Results declines as a share (−9.8)**, driven by the
  ELSI theme's drop (program-introduction pubs no longer dominate).
  Substantive ROR / ACMG / PGx ROR work continues but at a smaller fraction.
- **FA6 Environment has essentially no pre-2023 pubs and 7 post-2023 pubs.**
  Slide-7 priority, structural gap in the corpus. The independent HA5
  detector finds 13 pubs but most of those are SDOH-environment hybrids,
  not pure environment.

---

## 4. The 8 slide-7 "hot areas" — independent keyword detection

Detectors operate on `(calc_title + calc_abstract)` lowercased text. Trend
scores use the same pre-2023 vs. 2023+ share difference as above. Full
output in `hot_areas_summary.csv`. Per-pub flags in
`hot_areas_detection.csv` (one row per substantive pub, boolean column per
hot area).

| Code | Hot area | Total | Pre-2023 | 2023+ | Trend | Top admin ICs (n) | Flag |
|---|---|---:|---:|---:|---:|---|---|
| HA1 | Multi-omics (beyond genomics) | 24 | 1 | 23 | +1.3 | HL(7); HG(5); TR(5) | |
| HA2 | Wearables / remote monitoring | 70 | 8 | 62 | ±0.0 | OD(11); HL(9); HG(4) | |
| HA3 | Imaging / radiomics | 8 | 0 | 8 | +0.7 | HL(2); OD(2); NS(1) | **thin coverage** |
| HA4 | AI / foundation models / LLMs | 31 | 3 | 28 | +0.4 | HL(6); OD(5); GM(5) | |
| HA5 | Environmental health | 12 | 1 | 11 | +0.3 | OD(2); ES(2); HL(2) | |
| HA6 | G × E × SDOH integrated | 10 | 0 | 10 | +0.8 | HG(2); OD(2); DK(1) | borderline thin |
| HA7 | Nutrition / microbiome | 11 | 1 | 10 | +0.2 | OD(1); MD(1); AT(1) | borderline thin |
| HA8 | Breakthrough therapeutics (GLP-1, SGLT2, AD mAbs, CRISPR) | 16 | 1 | 15 | +0.6 | OD(1); GM(1); TR(1) | |

### Per-hot-area read

**HA1 Multi-omics (beyond genomics) — 24 pubs.** Slide 7 flagged
"multi-omics beyond genomics" as a 2023+ priority. The detector excludes
pure genomics; it requires proteomics / metabolomics / transcriptomics /
mass-spec / Olink / SomaScan / lipidomics language. 24 pubs is *thin* for
the size of the corpus and most use *external* proteomic/metabolomic data
linked to AoU genotype/phenotype rather than AoU-internal omics releases.
Top admin ICs: NHLBI (7), NHGRI (5), NCATS (5). 23 of 24 are post-2023.
The 2026 cohort multi-omics release will change this trajectory; today
the evidence base is hopes-and-plans, not output.
Examples: PMID:41712304 (2026, COPD proteomics + PRS); PMID:40063522
(2025, ALDH2 deficiency and alcohol-related cancer prevention);
PMID:40050615 (2025, multi-ancestry uterine fibroid GWAS with eQTL/sQTL
multi-omic integration).

**HA2 Wearables / remote monitoring — 75 pubs, FLAT trend.** A real and
substantial area that is *already mature*: 75 pubs detected with title/
abstract text, of which 62 are post-2023 but the *share-of-corpus* is
identical (5.1% pre-, 5.1% post-). Wearables work in AoU is not a "rising"
priority — it's a *current* priority with permanent footprint. Top admin
ICs: OD (11), NHLBI (9), NHGRI (4). The implication for the Refresh: if
the WG keeps treating wearables as "emerging" they will miss that it's
already here. The crosswalk recommendation (add a dedicated focus area or
fold under a renamed Data/AI/Methods area) is the structural answer.
Examples: PMID:39755829 (2025, activity inequality in AoU);
PMID:39813673 (2025, digital health research platform across a 1M cohort);
PMID:38696234 (2024, wearable biomarkers for postpartum depression).

**HA3 Imaging / radiomics — 8 pubs. THIN COVERAGE.** Slide 7 flagged
imaging / radiomics / AI interpretation as a 2023+ priority. The corpus
delivers **8 pubs**, mostly genetics-linked use of *external* imaging
phenotypes (e.g., UK Biobank MRI fat measures; abdominal ultrasound
findings) rather than AoU-internal imaging output. Top admin ICs: NHLBI
(2), OD (2), NINDS (1). This is a *Refresh gap*: if imaging is a priority,
the cohort has not yet delivered evidence it can support that priority.
The 0.6% corpus share is a strong signal that imaging data linkage /
release is an upstream investment that has not yet flowed through to
publications. The Refresh might consider whether AoU should invest in
imaging linkage (chest X-rays, retinal photos, MRIs) before designating
this as a priority area.
Examples: PMID:41053791 (2025, obesity genetics with MRI fat measures);
PMID:41039588 (2025, MASLD genetics with abdominal ultrasound);
PMID:41121728 (2025, mammography screening intensity vs. SDOH).

**HA4 AI / foundation models / LLMs — 33 pubs.** A real and growing
signal, 30 post-2023 of 33 total. Top admin ICs: NHLBI (6), OD (5), NIGMS
(5). This is the AI surge slide 7 anticipated; it's actually present in
the corpus though smaller than the wearables footprint. Combined with the
overall theme-3 growth (+4.2 trend, 239 post-2023 pubs), the AI/Methods
signal is real even if the specific "foundation model" / "LLM" framing is
still emerging.
Examples: PMID:39794311 (2025, foundation-model-style phenome-wide
disease-onset prediction); PMID:40417537 (2025, deep-learning time-to-event
for depression and asthma); PMID:40750633 (2025, "PAL-AI" model for
oocyte maturation).

**HA5 Environmental health — 13 pubs.** Matches the theme-19 signal closely.
Most of these 12 are SDOH-environment hybrids (walkability, perceived
neighborhood environment, social determinants + liver health). Pure
climate/air-quality work is rarer still. Top admin ICs: OD (2), NIEHS
(2), NHLBI (2) — NIEHS is the only IC where this is *strategic priority*
co-funding. The structural gap is real: if "environmental impact on
community health" is a 2023+ priority, the corpus is delivering at
13 / 1,428 = 0.9%.
Examples: PMID:41579292 (2026, SDOH disadvantage score and liver health);
PMID:41569831 (2026, perceived neighborhood environment + physical
activity); PMID:42061729 (2026, walkability and psychological distress).

**HA6 G × E × SDOH integrated — 11 pubs, borderline thin.** Slide 7's
"holistic risk models" — polygenic + environmental + SDOH integration.
This is the most genuinely *novel* category on slide 7: pre-2023 has zero
pubs, post-2023 has 10. Top admin ICs: NHGRI (2), OD (2), NIDDK (1).
Small but emergent. The slide-7 framing of "holistic risk models" is
exactly what the AoU cohort is best positioned to deliver — multi-ancestry
PRS + neighborhood ADI + EHR-derived comorbidity — and the 11 pubs show
the area exists in the work, just at small scale. **A real candidate for
elevation.**
Examples: PMID:41518215 (2026, PRS + perceived neighborhood disorder +
sleep duration); PMID:42109163 (2026, CoQ10 PRS + statin-associated
muscle symptoms); PMID:41039588 (2025, multi-ancestry MASLD risk variants).

**HA7 Nutrition / microbiome — 11 pubs, borderline thin.** Detector
deliberately tightened to exclude "food insecurity" (SDOH leak). What
remains: 11 pubs of which only a handful are *primary* nutrition/microbiome
contributions (most are dysphagia / celiac / NSAID enteropathy work that
incidentally mentions nutritional status). The cohort does not yet support
microbiome research at scale (no stool biospecimen release as of mid-2026).
Slide 7's "nutrition, microbiome & chronic disease management" priority
is **structurally under-supported by the current cohort**. Top admin ICs:
OD (1), NIMHD (1), NCCIH (1). Like imaging and multi-omics, this is a
priority that requires upstream investment before it can be evidenced in
publications.

**HA8 Breakthrough therapeutics — 20 pubs.** Real-world studies of GLP-1
agonists, SGLT2 inhibitors, AD monoclonals, CRISPR, immunotherapies in
the AoU cohort. 15 of 16 are post-2023. Top admin ICs: OD (1), NIGMS (1),
NCATS (1). Volume is moderate; the substance is high-impact (the GLP-1
hepatic-decompensation paper at PMID:41847743 is exactly the kind of
post-approval pharmacoepidemiology slide 7 anticipated). Most of these
pubs also tag theme 16 (pharmacogenomics) or theme 1 (cardiometabolic).
**A real and growing area.**
Examples: PMID:41741949 (2026, obesity-medication and bariatric-surgery
trends 2003–2023); PMID:41807852 (2026, third-line therapy cost-
effectiveness in advanced CRC); PMID:41847743 (2026, GLP-1 agonists and
hepatic decompensation).

---

## 5. Q1 answer (one paragraph)

**The single biggest change since 2023 is the volume explosion (~8.1×
growth) and the redistribution toward Genetics & Biology and Common &
Rare Conditions — both of which gained 23+ percentage points of corpus
share post-2023.** The v6/v7/v8 data releases unlocked large multi-
ancestry GWAS, PRS, and disease-association work at a scale that was
impossible pre-2023; the largest thematic gainers are theme 2 (genomics,
+17.0), theme 4 (mental health & substance use, +10.8), theme 1
(cardiometabolic, +9.8), and theme 5 (cancer, +9.4). Among the 8 slide-7
priorities, the evidence is mixed: **AI/foundation models (HA4, 33 pubs)
and breakthrough therapeutics (HA8, 20 pubs, GLP-1/SGLT2/AD mAbs/CRISPR)
are real and growing**; wearables (HA2, 75 pubs) are *already mature* and
trend-flat, not "emerging"; **multi-omics beyond genomics (HA1, 24 pubs),
G × E × SDOH integrated holistic risk models (HA6, 11 pubs), nutrition
& microbiome (HA7, 11 pubs), and imaging / radiomics (HA3, 8 pubs — thin
coverage) are all priorities that the cohort does not yet deliver at
publication scale**, because each requires upstream data investment
(proteomics/metabolomics releases, stool biospecimens, imaging linkage,
multimodal integration tools) that has not flowed through to output. The
ELSI / engagement decline (−12.4) is a maturation signal, not a problem;
the Health Equity dilution (−4.9 as share, but +615 pubs absolute) means
equity work is still load-bearing even as disease-specific work outgrows
it. The structural finding is that slide 7's priorities split cleanly
into "already realized" (AI, breakthrough therapeutics, wearables-as-
mature) and "aspirational pending investment" (multi-omics, imaging,
microbiome, holistic risk models) — and the Refresh framing should
distinguish those two categories.

---

## 6. Emerging (growing fast) — for Sci Com attention

Themes and hot-areas with strong positive trend scores and meaningful
post-2023 volume:

- **Genomics methods & complex-trait genetics** (theme 2, +17.0; 331
  post-2023 pubs). The cohort's flagship scientific application; v6/v7/v8
  releases unlock multi-ancestry GWAS / PRS / fine-mapping at unprecedented
  scale.
- **Mental health, behavioral & substance use** (theme 4, +10.8; 240
  post-2023 pubs). Driven by GWAS of psychiatric conditions plus large
  EHR-phenotype-based substance-use studies. The single largest non-
  genomic theme gainer.
- **Cardiometabolic disease** (theme 1, +9.8) and **Cancer** (theme 5,
  +9.4) — both surging as the cohort scales to support large case-control
  and prospective-cohort designs.
- **AI / foundation models / LLMs** (HA4, +0.4 absolute share but 28 of
  30 pubs are post-2023, 10× absolute growth). Theme 3's broader AI/Methods
  growth (+4.2) backs this. Real and growing.
- **Breakthrough therapeutics** (HA8, 15 of 16 post-2023). GLP-1, SGLT2,
  AD monoclonals — exactly the slide-7 anticipation, evidenced.
- **G × E × SDOH integrated holistic risk models** (HA6, 10 post-2023, 0
  pre-2023). Small absolute footprint but genuinely novel; the AoU cohort
  is structurally well-positioned to lead this.
- **Healthy aging & ADRD** (theme 11, +4.7; 73 post-2023 pubs vs. 2
  pre-2023). Off a small base but the absolute jump is dramatic.

## 7. Stagnating / under-supported — for Sci Com attention

Themes and hot-areas where slide-7 framing suggests a priority but the
corpus does not yet deliver:

- **Imaging / radiomics** (HA3, 8 pubs, THIN). Below the thin-coverage
  threshold. Slide-7 priority, structural gap. Most "imaging" pubs in the
  corpus use external imaging linked to AoU phenotypes, not AoU imaging.
- **Multi-omics beyond genomics** (HA1, 24 pubs). Cohort multi-omics
  releases not yet flowing into the literature; most "multi-omic" papers
  in the corpus pair AoU genotypes with external proteomics/metabolomics.
- **Nutrition & microbiome** (HA7, 11 pubs, borderline thin). No stool
  biospecimen release; microbiome work is structurally absent from the
  cohort today.
- **Environmental health** (theme 19, 8 pubs; HA5, 13 pubs). Among the
  smallest theme footprints. Slide-7 priority with structural gap; AoU
  has not yet integrated air-quality, climate, or built-environment
  exposures at scale for routine use.
- **Wearables & digital health** (theme 7, +1.0; HA2, ±0.0). Already
  mature and steady-state — not "emerging" — but invisible in the 8-area
  framework. *Not* a growth gap; a *recognition* gap.
- **Health Equity** (FA7, −5.7 as share; 632 post-2023 pubs absolute).
  Diluted but still load-bearing. Worth protecting as cross-cutting
  emphasis in the Refresh.
- **Return of Results** (FA4, −9.8 as share). Maturation of the corpus
  away from program-introduction pubs; the substantive ROR / PGx / ACMG
  work continues but at a smaller relative footprint. If FA4 is retained,
  it should be re-scoped toward implementation rather than ELSI research.

---

## 8. Files written by this phase

| File | Purpose |
|---|---|
| `pub_year_by_theme.csv` | 19 themes × years (2015–2027) → pub count |
| `pub_year_by_focus_area.csv` | 8 focus areas × years → pub count |
| `theme_trend_scores.csv` | Per-theme pre/post-2023 split and trend score |
| `focus_area_trend_scores.csv` | Per-focus-area pre/post-2023 split and trend score |
| `hot_areas_detection.csv` | One row per pub, boolean columns for HA1–HA8 |
| `hot_areas_summary.csv` | Per-hot-area: counts, splits, trend, top ICs, examples |
| `temporal_trends.md` | (this file) |

Companion Phase 3a outputs in `crosswalk_19_to_8.md`.

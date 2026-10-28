# AoU × ECHO: Which Survey Data Should Be Harmonized First

**Purpose.** Recommend which All of Us (AoU) survey content should be harmonized with which ECHO Cohort measures, and in what order, so the two cohorts can be co-analyzed in the AoU Researcher Workbench. This document does not harmonize variables. It ranks the pairings.

**Scope.** Current data only:
- **AoU:** surveys in the current CDR (Data Browser counts from CDR 2025q4r5).
- **ECHO:** measures on the current ECHO Cohort Protocol (ECP v3.2). Legacy-only ECHO instruments are excluded, for example PHQ-9, CES-D, and EPDS.
- **Respondents:** caregiver report about a child is an acceptable ECHO respondent.

Machine-readable versions: [`harmonization_priorities.csv`](harmonization_priorities.csv) (one row per pairing, with matched AoU item codes) and [`harmonization_gaps.csv`](harmonization_gaps.csv).

## Bottom line

1. **Start with the shared sociodemographic core (C1–C7).** Every co-analysis needs race/ethnicity, sex and gender, education, income, employment, marital status/household, and insurance. Both cohorts have these for nearly everyone. The work is mapping categories, not reconciling different instruments.
2. **Then the four "same instrument" pairs, which are near-free wins (score 15):**
   - perceived stress (PSS-10)
   - everyday discrimination (Williams EDS)
   - adult ACEs (BRFSS/CDC-Kaiser)
   - PROMIS Global Health v1.2

   The items are identical, so pooled scores need little more than a coding check.
3. **Then the linkable mental-health and hardship pairs (score 13):**
   - **Depression:** AoU PHQ-9 ↔ ECHO PROMIS Depression
   - **Anxiety:** AoU GAD-7 ↔ ECHO PROMIS Anxiety

     Both are linkable to the PROMIS T-score metric with published PROsetta Stone crosswalks.
   - **Food insecurity:** the AoU Hunger Vital Sign items are a subset of the USDA items in ECHO's income/assistance form.
   - **Family medical history:** both are condition-by-relative checklists, and both have more than 30k respondents.
4. **Tier 2 is worth doing but needs more mapping effort or has smaller ECHO samples:**
   - tobacco, alcohol, and drug use
   - child health conditions as reported by a parent. AoU family history records conditions in the respondent's sons and daughters.
   - neighborhood cohesion
   - discrimination in medical settings
5. **Tier 3 is construct-level only.** The instruments differ, or the ECHO sample is under 5k. Defer these unless a specific study needs them.

## Ranked pairings

Score = 2×instrument concordance + respondent fit + sample size + analytic value (max 15). Each component is scored 1–3; the components are listed in the order shown in the Components column. Tier 1 ≥ 13, Tier 2 = 11–12, Tier 3 ≤ 10. ECHO form codes are ECP Form Short Names.

### Core covariates (do first regardless of score)

| ID | Construct | AoU survey | ECHO (ECP forms) | AoU n | ECHO n | Components | Score | Tier |
|---|---|---|---|---:|---:|---|---:|---:|
| C1 | Race and ethnicity | The Basics | REI; Dem-B; Dem-C; REI-CR | 738,040 | 63,274 | 2/3/3/3 | 13 | 1 |
| C2 | Sex assigned at birth and gender identity | The Basics | Dem-B; Dem-C | 747,040 | 63,274 | 2/3/3/3 | 13 | 1 |
| C3 | Educational attainment | The Basics | Dem-B; Dem-CG | 734,480 | 63,274 | 2/3/3/3 | 13 | 1 |
| C4 | Household income and financial strain | The Basics | IAFS-P; IAFS-C; IAFS-A | 701,340 | 25,467 | 2/3/3/3 | 13 | 1 |
| C5 | Employment and occupation | The Basics | Occ-CG; Occ-CG-P | 740,760 | 50,828 | 2/3/3/3 | 13 | 1 |
| C6 | Marital status and household composition | The Basics | Dem-B; Dem-CG | 741,640 | 63,274 | 2/3/3/3 | 13 | 1 |
| C7 | Health insurance coverage | The Basics; HCAU | HIC; HIC-A | 740,620 | 55,073 | 2/3/3/3 | 13 | 1 |
| C8 | Nativity, language, and acculturation | The Basics | LA-P; LA-C; LA-A | 741,520 | 22,997 | 1/3/3/2 | 10 | 3 |
| C9 | Housing tenure and stability | The Basics | IAFS-P; IAFS-C | 737,400 | 25,467 | 1/3/3/2 | 10 | 3 |

### Tier 1

| ID | Construct | AoU survey | ECHO (ECP forms) | AoU n | ECHO n | Components | Score |
|---|---|---|---|---:|---:|---|---:|
| P1 | Perceived stress (PSS-10) | Social Determinants of Health | NTPSS10; NTPSS10-A | 310,020 | 44,843 | 3/3/3/3 | 15 |
| P2 | Everyday discrimination | Social Determinants of Health | WEDS | 310,240 | 38,440 | 3/3/3/3 | 15 |
| P6 | Adverse childhood experiences (adult, retrospective) | Emotional Health History & Well-Being | ACE | 136,020 | 29,124 | 3/3/3/3 | 15 |
| P8 | Global physical and mental health (PROMIS Global) | Overall Health | PGH; PGH-A | 673,400 | 40,116 | 3/3/3/3 | 15 |
| H1 | Family medical history | Personal & Family Health History | MH2-F | 354,760 | 31,280 | 2/3/3/3 | 13 |
| P13 | Food insecurity | Social Determinants of Health | IAFS-P; IAFS-C | 310,780 | 25,467 | 2/3/3/3 | 13 |
| P4 | Depressive symptoms | Emotional Health History & Well-Being | PDep8a; PDep-CAT | 136,460 | 41,458 | 2/3/3/3 | 13 |
| P5 | Anxiety symptoms | Emotional Health History & Well-Being | PAnx8a; PAnx-CAT | 136,460 | 28,425 | 2/3/3/3 | 13 |

### Tier 2

| ID | Construct | AoU survey | ECHO (ECP forms) | AoU n | ECHO n | Components | Score |
|---|---|---|---|---:|---:|---|---:|
| P3 | Discrimination in medical settings | Social Determinants of Health | DMSS | 308,740 | 2,677 | 3/3/1/2 | 12 |
| S1 | Tobacco and nicotine use | Lifestyle | Life-C; Life-EP; Life-3T; YRB-SU | 669,320 | 9,620 | 2/3/2/3 | 12 |
| S2 | Alcohol use | Lifestyle | Life-C; Life-EP; Life-3T | 667,740 | 9,620 | 2/3/2/3 | 12 |
| H2 | Child health conditions, reported by parent | Personal & Family Health History | MH2-C; MH2 | 354,760 | 40,292 | 1/3/3/3 | 11 |
| P11 | Neighborhood social cohesion | Social Determinants of Health | NE-CE | 310,880 | 17,676 | 2/3/2/2 | 11 |
| S3 | Cannabis and other drug use | Lifestyle | Life-C; SubUse-R; YRB-SU | 652,720 | 8,511 | 2/3/2/2 | 11 |

### Tier 3 (construct-level overlap only)

| ID | Construct | AoU survey | ECHO (ECP forms) | AoU n | ECHO n | Components | Score |
|---|---|---|---|---:|---:|---|---:|
| H3 | Adult personal medical conditions | Personal & Family Health History | MH2-F; PMCI | 354,760 | 29,700 | 1/3/3/2 | 10 |
| H4 | Pregnancy and reproductive history | Overall Health | PMCI; PI | 423,300 | 32,129 | 1/3/3/2 | 10 |
| H5 | Health care access, utilization, affordability | HCAU | HIC; prenatal care (derived) | 365,200 | 55,073 | 1/3/3/2 | 10 |
| P14 | Traumatic events / PTSD symptoms | Emotional Health History & Well-Being | LSC; CRISYS-SF | 109,200 | 28,434 | 1/3/3/2 | 10 |
| P7 | ACEs across generations (adult retrospective vs. child) | Emotional Health History & Well-Being | ACE-PR; ACE-CR; ACE-18-20y | 136,020 | 14,889 | 2/2/2/2 | 10 |
| P9 | Social support | Social Determinants of Health | PES4a; PInfS4a; PInstrS4a (+CAT) | 310,520 | 28,389 | 1/3/3/2 | 10 |
| P16 | Physical activity | Social Determinants of Health | PA (derived); SPAD-P | 310,680 | 15,400 | 1/3/2/2 | 9 |
| P10 | Loneliness and companionship | Social Determinants of Health | PComp6a-A | 309,700 | 2,024 | 1/3/1/2 | 8 |
| P12 | Neighborhood disorder and safety | Social Determinants of Health | Neigh-C; Neigh-Preg | 308,900 | 3,511 | 1/3/1/2 | 8 |
| P15 | ADHD symptoms | Behavioral Health & Personality | CSS-SR | 138,480 | 2,480 | 1/3/1/2 | 8 |
| P18 | Health literacy | Overall Health | CHL | 672,580 | 5,945 | 1/3/2/1 | 8 |
| H6 | COVID-19 infection, impact, vaccination | COPE; COVID-19 vaccine minute surveys | ad hoc COVID-19 forms | n/a | 13,154 | 1/3/1/1 | 7 |
| P17 | Religiosity and spirituality | Social Determinants of Health | RaS | 309,180 | 2,455 | 1/3/1/1 | 7 |
| P19 | Personality / temperament | Behavioral Health & Personality | ATQ | 138,520 | 438 | 1/3/1/1 | 7 |

The rationale and harmonization notes for each pairing are in the `rationale` column of the CSV.

## Not harmonizable from surveys (gaps)

These constructs are measured in ECHO (adult respondents) or in AoU surveys, but have no survey counterpart in the other cohort:

| Construct | ECHO forms | Note |
|---|---|---|
| Sleep health | SHA; PSD4a; PSRI4a; MSHPrg | No AoU sleep survey; AoU Fitbit sleep data is a possible non-survey complement |
| Self-reported weight/height | Wt-CG; HtWt-P | AoU uses physical measurements and EHR |
| Diet | DHQ3; DSQ-SR; MFSP | No AoU diet survey |
| Couple relationship quality | CSI4 | No AoU counterpart |
| Household chemical and secondhand-smoke exposure | HCExp; HESHS | No AoU survey counterpart |
| Benevolent childhood experiences | BCE | AoU asks ACEs only |
| Suicidal thoughts/behaviors; psychosis, mania, eating disorders | none on ECP | AoU EHWB/BHP only |

## How the scores were built

| Component | 3 | 2 | 1 |
|---|---|---|---|
| Instrument concordance (×2) | Same instrument/items | Overlapping items, or a published linking/crosswalk | Same construct, different instruments |
| Respondent fit | Both self-report, or both report on the same people | Adult self-report vs. caregiver report about a child | n/a |
| Sample size, min(AoU n, ECHO n) | ≥ 20,000 | 5,000–19,999 | < 5,000 |
| Analytic value | Needed in nearly any co-analysis, or a core ECHO exposure/outcome | Commonly used | Niche |

- **AoU n:** the maximum respondent count across the matched items, from the AoU Data Browser (CDR 2025q4r5; counts rounded to 20). When item counts are suppressed, the survey's participant count is used. This applies to C2 only.
- **ECHO n:** the maximum participant count across the matched measures, from ECHOPortal PlatIPUS Browse for the de-identified release (86,327 participants). PlatIPUS counts include extant data mapped to the protocol, and its new-data-only filter returned nothing, so these counts are an upper bound on "current protocol" data. The same applies to the ECHO tobacco, alcohol, and drug counts: they use the largest current-protocol lifestyle form (Life-EP, 9,620). ECHO's derived prenatal tobacco and alcohol files are larger (~38k), but they include legacy data.
- **Concordance:** set by comparing item text across the AoU codebook / Survey Explorer sources and the ECHO public codebook. Examples:
  - ECHO WEDS item 1 and AoU `sdoh_eds_1` are both "You are treated with less courtesy than other people are."
  - ECHO NTPSS10 and the AoU PSS-10 items match.
  - ECHO CHL is a reading-comprehension test, whereas AoU uses the Chew screener.
- **Analytic value** is a judgment call. Revise it in `scripts/prioritize.py` (`PAIRS`). Rerun the script to re-rank.

## Open checks before committing effort

- **C9 housing / P13 food:** confirm which housing and food-security items ECHO IAFS carries in the current release.
- **S1–S3:** align the ECHO Lifestyle look-back windows with AoU's lifetime and current framing. ECHO uses "past 6 months" and pregnancy-trimester windows.
- **H1/H2:** the condition lists differ in granularity. Map both to a shared condition vocabulary (for example SNOMED via OMOP) before pooling.
- **P4/P5:** decide whether to pool on the PROMIS metric via PROsetta linking or to analyze AoU and ECHO scores separately.

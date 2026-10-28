# Survey Inventory: All of Us × ECHO Cohort

A variable-level inventory of the survey and questionnaire data dictionaries for the
**All of Us Research Program** and the **ECHO (Environmental influences on Child
Health Outcomes) Cohort Study**. It is the starting point for an **AoU ↔ ECHO
cross-cohort harmonization map**.

Why now: as of 2026, de-identified ECHO Cohort data are hosted in the AoU
Researcher Workbench ("ECHO Cohort – Registered Tier" / "ECHO Cohort – Controlled
Tier" data collections). Researchers can add them to the same workspace as the AoU
CDR. The two cohorts are enrolled separately and records are **not linked**, so
co-analysis depends on mapping equivalent variables. See the
[AoU ECHO data article](https://support.researchallofus.org/hc/en-us/articles/52141157141396).

## Scope decisions (2026-10-28)

| Question | Decision |
|---|---|
| Location / format | Top-level `survey-inventory/`, CSV outputs + scripts |
| ECHO source | ECHO Cohort Protocol (ECP) v3.2: Measures Master List + public-use codebook (Cycle 2 release, which also carries Cycle 1 tables) |
| AoU release / tier | Latest CDR, **Controlled Tier**. The AoU Survey Codebook covers every survey fielded in both the Registered and Controlled Tier CDRs and records the per-item privacy rules for each tier |
| Granularity | Question level **plus** answer options |
| Goal | Cross-cohort harmonization map (AoU ↔ ECHO) |

## Inventory at a glance

**All of Us: 13 survey instruments, 2,146 questions** (non-descriptive fields)

| Survey | Questions | Items with RT rules | Items with CT rules |
|---|---:|---:|---:|
| The Basics | 79 | 65 | 55 |
| Lifestyle | 37 | 6 | 1 |
| Overall Health | 40 | 17 | 4 |
| Family Health History (legacy) | 116 | 14 | 12 |
| Personal Medical History (legacy) | 480 | 15 | 15 |
| Personal and Family Health History | 704 | 99 | 99 |
| Health Care Access and Utilization | 58 | 1 | 1 |
| Social Determinants of Health | 82 | 1 | 1 |
| COVID-19 Participant Experience (COPE): May, Jun, Jul, Nov, Dec, Feb | 240 | 56 | 15 |
| Minute Survey on COVID-19 Vaccines: Summer, Fall, Winter, New Year | 141 | 69 | 52 |
| Life Functioning | 6 | 0 | 0 |
| Emotional Health History and Well-Being | 103 | 6 | 0 |
| Behavioral Health and Personality | 60 | 0 | 0 |

"Rules" are the privacy transformations applied in each tier (for example
`REGISTERED_QUESTION_SUPPRESSED` or `CONTROLLED_ANSWERS_BUCKETED`). An item with an
RT rule but no CT rule is available in more detail in the Controlled Tier.

**ECHO: 293 ECP v3.2 measures across 23 concept domains, 552 public-use datasets, 53,110 variables**

- 251 of the measures are completed by a participant, caregiver, or partner rather than by staff. These are surveys and questionnaires. The rest are staff-administered exams, biospecimens, or administrative forms.
- The largest domains are Child Neurodevelopmental Health & Functioning (41), Child Well-being (26), Caregiver Neuro-Psychosocial (23), Sociodemographics (20), and Home Social Environment (20).
- Variables by provenance:
  - Cycle 2 form variables linked to an ECP measure: 19,296
  - Cycle 2 form variables not in the master list (mostly `HHx` health history and `Prg` pregnancy extant-data tables): 2,834
  - Cycle 1 tables (`*_C1`, legacy cohort-specific instruments): 27,212
  - Derived/harmonized tables (`Der_*`): 3,211
  - Lab/biospecimen tables: 557

## Files

| File | Grain | Notes |
|---|---|---|
| `aou_surveys.csv` | 1 row / AoU survey | form names, COPE/vaccine versions, counts of tier rules |
| `aou_variables.csv` | 1 row / AoU question | PPI `item_concept` (= OMOP `observation_source_value`), question text, REDCap answer options (`code, label \| …`), branching logic, RT/CT rules |
| `echo_measures.csv` | 1 row / ECP measure | domain, data element, form short name, visits, respondent ("completed by"), child age range, database table(s) |
| `echo_variables.csv` | 1 row / ECHO codebook variable | dataset, cycle, kind (form/derived/lab), link to ECP measure, label, type, answer options from code lists, units, terminology standard (ICD/RxNorm/USDA) |
| `harmonization_map.csv` | 1 row / AoU↔ECHO variable pair | **template, header only**. To be filled in next |
| `raw/` | n/a | source dictionaries as downloaded, plus `manifest.json` (URLs, dates, original filenames) |
| `scripts/acquire.py` | n/a | re-downloads `raw/` (all sources are public, no login) |
| `scripts/build_inventory.py` | n/a | regenerates every CSV from `raw/` |

```bash
python3 survey-inventory/scripts/acquire.py
```

```bash
python3 survey-inventory/scripts/build_inventory.py
```

## Sources

- **AoU Survey Codebooks**: [support article](https://support.researchallofus.org/hc/en-us/articles/360051991531), [Google Sheet](https://docs.google.com/spreadsheets/d/1pODkE2bFN-kmVtYp89rtrJg7oXck4Fsex58237x47mA). Codebook last updated 2026-09-21.
- **ECHOPortal public Resource Library**: [Cycle 2 Public Use Data Reference Materials](https://echoportal.org/ResourceLibrary/Resources/Home). Downloaded:
  - ECP v3.2 Measures Master List (v10.2, 2025-08-13)
  - ECHO Codebook for Public Use (2025-09-01)
  - Release Notes (DL202509)
  - ECP Protocol v3.2 (2024-12-04)
- **PlatIPUS** on ECHOPortal has a searchable data dictionary and the harmonized/derived-variable documentation. Use it when deciding matches.

## Caveats / to verify

- **No AoU pediatric surveys are in this codebook.** All 13 instruments are adult self-report. If AoU pediatric instruments are released for research use, they will be the most direct counterpart to ECHO and should be added. This still needs to be verified against the latest CDR release notes.
- The AoU codebook is the *fielded instrument* dictionary. To confirm a question actually has data in the current Controlled Tier CDR, check the Data Browser or query `ds_survey` / `observation` in the Workbench.
- ECHO's public-use codebook reflects the public release (DL202509), not every ECP item. Some ECP measures have no public table (for example NIH Toolbox item-level data, address history, and some biospecimen forms).
- ECHO respondents differ from AoU's. Many ECHO items are caregiver-reported about a child, or completed by a pregnant participant. AoU items are adult self-report. The harmonization map records this in `respondent_note`.

## Next steps (harmonization map)

1. Seed candidate pairs by shared standard instruments, where matching is near-exact. Examples: PROMIS, PHQ-9, GAD-7, PSS, EPDS/CES-D, ACEs, AUDIT-C/tobacco, sleep (PSQI/PROMIS), food insecurity (Hunger Vital Sign), discrimination (EDS), neighborhood/SDOH, and demographics (race, ethnicity, education, income, insurance).
2. Rank lexical/semantic similarity between `question_text` and `variable_label` to surface the rest.
3. Have a reviewer classify each pair as `match_type` ∈ {exact, equivalent-transform, partial, related-construct}. Record answer-option recodes in `transform_note`.
4. Where possible, attach standard codes (LOINC, PhenX, NIH CDE, OMOP concept_id).

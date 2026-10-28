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

This list is complete. It matches the survey table in AoU's
[Introduction to Survey Collection and Data Transformation Methods](https://support.researchallofus.org/hc/en-us/articles/6085114880148)
and the eight surveys on the [Survey Explorer](https://www.researchallofus.org/data-tools/survey-explorer/).
Several are retired or time-limited:
- The legacy PMH and FHH surveys were replaced by PFHH.
- COPE and the vaccine minute surveys were fielded 2020–2022.
- Life Functioning collects the Basics disability items from participants who enrolled before those items were added to The Basics.

"Rules" are the privacy transformations applied in each tier (for example
`REGISTERED_QUESTION_SUPPRESSED` or `CONTROLLED_ANSWERS_BUCKETED`). An item with an
RT rule but no CT rule is available in more detail in the Controlled Tier.

### AoU enrichment: OMOP concepts, counts, and item sources

Two further sources add these columns to `aou_variables.csv`:

- **OMOP concept IDs and counts, from the Data Browser.** The public [Data Browser](https://databrowser.researchallofus.org/) API (`scripts/fetch_databrowser.py`) supplies:
  - `question_concept_id`, which is the CDR's `observation_source_concept_id`
  - answer concept IDs, which are `value_source_concept_id`
  - participant counts from the CDR the Data Browser is built on: 2025q4r5, 747,040 participants, retrieved 2026-10-28

  Survey concept IDs are the OMOP "PPI" vocabulary concepts (for example [1586134 = The Basics](https://athena.ohdsi.org/search-terms/terms/1586134)). Questions are joined on the PPI code (`item_concept` = `concept_code`). Where the Data Browser uses a LOINC code instead, they are joined on question text: the disability items are LOINC 69856-3 … 69861-3. The column `databrowser_match` records which join was used.
- **Item sources, from the Survey Explorer PDFs.** Each English "source" PDF footnotes items with the instrument they were adapted from (`scripts/survey_sources.py`). Items are matched to codebook questions by text. The bibliographies are in `aou_survey_sources.csv`.

| Survey | Questions | With OMOP concept + count | With source instrument |
|---|---:|---:|---:|
| The Basics | 79 | 23 | 24 |
| Lifestyle | 37 | 26 | 26 |
| Overall Health | 40 | 21 | 22 |
| Family Health History (legacy) | 116 | 100 | n/a (no PDF) |
| Personal Medical History (legacy) | 480 | 442 | n/a (no PDF) |
| Personal and Family Health History | 704 | 592 | 679 |
| Health Care Access and Utilization | 58 | 57 | 51 |
| Social Determinants of Health | 82 | 80 | 75 |
| COPE | 240 | n/a (not in Data Browser) | n/a |
| COVID-19 vaccine minute surveys | 141 | n/a (not in Data Browser) | n/a |
| Life Functioning | 6 | 5 | 6 |
| Emotional Health History and Well-Being | 103 | 85 | 45 |
| Behavioral Health and Personality | 60 | 46 | 50 |

Most unmatched codebook rows are expected:
- free-text "please specify" fields, which are suppressed
- numeric age/number sub-fields
- items the Data Browser doesn't display

Source coverage for Emotional Health History and Well-Being is partial. Several of its items share one footnoted stem ("Over the last 2 weeks…"), and the text match can't separate them yet.

Source instruments relevant to harmonization include:
- GAD-7, PHQ-9, PCL-C, ACEs (BRFSS), SITBI, and the WHO WMH-CIDI (Emotional Health)
- ASRS and BFI-2-XS (Behavioral Health)
- PROMIS Global Health (Overall Health)
- AUDIT-C, NIDA-modified ASSIST, and PATH (Lifestyle)
- PSS (Cohen), RAND MOS Social Support, UCLA Loneliness, Everyday Discrimination, Hunger Vital Sign, IPAQ, and the Daily Spiritual Experience Scale (Social Determinants of Health)
- ACS, NHIS, BRFSS, and GenIUSS (The Basics)

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
| `aou_variables.csv` | 1 row / AoU question | PPI `item_concept` (= OMOP `observation_source_value`), question text, REDCap answer options (`code, label \| …`), branching logic, RT/CT rules, `question_concept_id`, `n_participants_databrowser`, `answer_concepts_databrowser` (`concept_id, label \| …`), `source_refs` / `source_instruments` |
| `aou_survey_sources.csv` | 1 row / cited source | Survey Explorer bibliography per survey: citation, year of original source, description |
| `echo_measures.csv` | 1 row / ECP measure | domain, data element, form short name, visits, respondent ("completed by"), child age range, database table(s) |
| `echo_variables.csv` | 1 row / ECHO codebook variable | dataset, cycle, kind (form/derived/lab), link to ECP measure, label, type, answer options from code lists, units, terminology standard (ICD/RxNorm/USDA) |
| `harmonization_map.csv` | 1 row / AoU↔ECHO variable pair | **template, header only**. To be filled in next |
| `raw/` | n/a | source dictionaries as downloaded, `survey_explorer/` PDFs, `databrowser_questions.json`, and `manifest.json` (URLs, dates, original filenames) |
| `scripts/acquire.py` | n/a | re-downloads the codebooks and PDFs (all public, no login) |
| `scripts/fetch_databrowser.py` | n/a | re-pulls question/answer concept IDs and counts from the Data Browser API (~3 min) |
| `scripts/survey_sources.py` | n/a | parses Survey Explorer PDFs (needs poppler `pdftotext`) |
| `scripts/build_inventory.py` | n/a | regenerates every CSV from `raw/` |

```bash
python3 survey-inventory/scripts/acquire.py
```

```bash
python3 survey-inventory/scripts/fetch_databrowser.py
```

```bash
python3 survey-inventory/scripts/build_inventory.py
```

## Sources

- **AoU Survey Codebooks**: [support article](https://support.researchallofus.org/hc/en-us/articles/360051991531), [Google Sheet](https://docs.google.com/spreadsheets/d/1pODkE2bFN-kmVtYp89rtrJg7oXck4Fsex58237x47mA). Codebook last updated 2026-09-21.
- **AoU survey methods**: [Introduction to All of Us Survey Collection and Data Transformation Methods](https://support.researchallofus.org/hc/en-us/articles/6085114880148). Covers survey eligibility, release date ranges, how surveys are stored in the OMOP `observation` and `survey_conduct` tables, and `PMI_SKIP` (903096).
- **AoU Survey Explorer**: <https://www.researchallofus.org/data-tools/survey-explorer/>. Survey PDFs with item sources.
- **AoU Data Browser API**: `https://public.api.researchallofus.org/v1/databrowser/` (`domain-totals`, `survey-questions`, `sub-questions`, `survey-question-results`, `survey-question-counts`).
- **OHDSI Athena, PPI vocabulary**: [Athena search](https://athena.ohdsi.org/search-terms/terms?vocabulary=PPI&domain=Observation). Athena's API refused requests from this build environment (HTTP 403), so concept IDs come from the Data Browser, which uses the same PPI concepts. A downloaded Athena vocabulary bundle (requires a login) could add concept names, classes, and standard mappings.
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

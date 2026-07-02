# All of Us Research Landscape — Phase 1 Data Acquisition

Phase 1 work product: complete pull of the All of Us (AoU) Research Program
publication directory and research project directory, normalized to CSV +
JSONL, with raw responses kept for reproducibility.

**Pulled on:** 2026-06-02 (publications refreshed 2026-06-26 — see note below)
**Extraction script:** `extract.py` (re-run idempotently; `--refetch` to re-pull)
**Total wall time to pull + extract:** under 30 seconds (cached APIs return in 1–10 s; extract runs in ~1 s)

## Where the data came from

Both AoU directory pages are client-side React/jQuery views that fetch from
WordPress-hosted JSON caches. The static HTML contains no data; everything is
loaded via XHR on page render.

### Publications

- **URL:** `https://www.researchallofus.org/wp-json/rh-data-caching/publications-report`
- **Status:** Live and serving fresh data (most-recent record is dated 2027 — likely an "online ahead of print" date).
- **Size:** ~10 MB; one big JSON array of 1,378 records.
- **Linked from:** `https://www.researchallofus.org/publication-directory/`
- The endpoint is a WordPress-cached snapshot of an upstream PMI Ops feed; the
  data appears to be reconciled against PubMed/iCite (every record has both
  `pdr_*` fields populated from PubMed-Derived and `calc_*` fields populated
  from a separate computation step, plus iCite citation counts).

### Projects

- **Intended URL:** `https://www.researchallofus.org/wp-json/rh-data-caching/projects?cb=<hash>`
- **Status (2026-06-02):** **Broken in production.** The endpoint currently
  returns HTTP 500 because the upstream RDR API (`https://rdr-api.pmi-ops.org/rdr/v1/researchHub/projectDirectory?status=ACTIVE&pageSize=1000`)
  is also returning 500.
- **Stable mirror:** `https://stable.researchallofus.org/wp-json/rh-data-caching/projects?cb=<hash>` returns 285 records that are almost entirely test / staging / VWB-development workspaces — not the production registry.
- **Fallback used:** Wayback Machine capture from **2025-10-24**:
  `https://web.archive.org/web/20251024105034if_/https://www.researchallofus.org/wp-json/research-hub/projects-directory` — 21,242 records, fully populated. This is the legacy endpoint URL (research-hub vs rh-data-caching) which was still in use at the time of capture. The two endpoints serve the same payload shape.
- Earlier Wayback captures exist back to 2020-10-09 (114 KB / very few records) through 2024-09-24 (~5.9 MB), so it is possible to track project growth over time if useful for later phases.

If/when the production endpoint comes back online, re-run `extract.py --refetch` to capture a fresher snapshot.

## Refresh — 2026-06-26 (publications)

Re-pulled the publications endpoint on 2026-06-26: the feed now serves **1,432
records, up from 1,378** on 2026-06-02. The diff is purely additive — **54 new
records, 0 removed** — matched on PubMed ID + DOI. All 54 are 2026-dated
(online-ahead-of-print / newly indexed), lifting the 2026 bucket from 199 → 253.
Thematically they track the existing corpus (polygenic-risk / GWAS methods,
cardiometabolic & CKM, SDOH / health-disparities, dermatology, AI-on-EHR
methods). Coverage of the 54: PMID 54/54, DOI 27/54, PMC 28/54.

`publications.csv` / `publications.jsonl` were regenerated from the fresh feed
(`raw/publications_api_2026-06-26.json`); the original 2026-06-02 raw snapshot is
retained for reproducibility. The just-the-new-54 subset is in
`raw/new_publications_2026-06-26.json`. **Projects were not re-pulled** (prod
endpoint still down — see above); they remain the 2025-10-24 Wayback capture.

Downstream Phase 2 artifacts were re-run against the full 1,432-pub corpus on
2026-06-26: IC attribution (`ic_attribute.py`) and theme tagging
(`tag_corpus.py`). Tagging now also incorporates **PMC full text** (612 articles)
and **gap-filled abstracts**, with two output layers — an abstract-level
canonical series and a full-text-augmented series. See
[`fulltext_augmentation.md`](fulltext_augmentation.md) for the method, the
OA-coverage-by-year confound, and the abstract-vs-full-text theme deltas.

**Full-refresh check (2026-07-02, pre-handoff):** re-pulled the publications feed
and re-probed the projects endpoints to finalize the corpus. Publications are
analytically unchanged — still **1,432 records; 0 added / 0 removed; 0 changed
titles/abstracts** (only non-analytical fields such as citation counts differ).
The projects prod endpoint still returns HTTP 500 and no Wayback capture newer
than 2025-10-24 exists, so the workspace snapshot is unchanged. The corpus is
**frozen at its freshest available state**; all downstream numbers hold — no
pipeline re-run was required.

## Counts

| Dataset | Records |
| --- | ---: |
| Publications (`publications.csv` / `publications.jsonl`) | **1,432** (was 1,378 on 2026-06-02) |
| Projects (`projects.csv` / `projects.jsonl`) | **21,242** |

## Files

| Path | What it is |
| --- | --- |
| `raw/publications_api_2026-06-02.json` | Verbatim publications API response, original Phase 1 pull (10 MB). |
| `raw/publications_api_2026-06-26.json` | Verbatim publications API response, 2026-06-26 refresh — 1,432 records (11 MB); current source for `publications.csv`/`.jsonl`. |
| `raw/new_publications_2026-06-26.json` | The 54 records new in the 2026-06-26 refresh (diff vs 2026-06-02). |
| `raw/projects_wayback_20251024.json` | Verbatim 2025-10-24 Wayback capture of projects-directory feed (42 MB). |
| `raw/projects_stable_2026-06-02.json` | The stable-mirror response — staging workspaces only; kept for completeness, not used for analysis. |
| `raw/publication-directory.html`, `raw/research-project-directory.html` | The HTML containers (also include the JS that names the API endpoints — useful for re-discovering the feeds). |
| `publications.csv` | Curated flat view of pubs, one row per record. |
| `projects.csv` | Curated flat view of projects, one row per record. |
| `publications.jsonl`, `projects.jsonl` | Full original records, one JSON object per line, no field dropped. Use these for any analysis that needs the original nested team/owner structure or every `pdr_*`/`manual_*`/`calc_*` variant. |
| `extract.py` | Reproducible CSV/JSONL builder. |

## Publications

### Field coverage

Field-by-field coverage across the 1,378 records, using the priority order
`manual_* → pdr_* → calc_*` for each logical field (this is the same order the
AoU directory page itself uses when rendering):

| Field | Coverage |
| --- | ---: |
| Title | 1378/1378 (100%) |
| Year | 1378/1378 (100%) |
| Journal | 1353/1378 (98%) |
| PubMed ID | 1332/1378 (97%) |
| DOI | 1248/1378 (91%) |
| Abstract | 1178/1378 (85%) |
| PMC ID | 946/1378 (69%) |
| Authors (list) | 1378/1378 (100%) |
| Institutions (list) | from `pdr_institution_list`; populated for most |
| Grant numbers | 475/1378 (34%) |
| iCite count / RCR | 1378/1378 (100%; raw numbers, even where 0) |
| Lay summary | present in `lay_summary` for a subset |
| `manual_program_pub` (AoU program-pub flag) | 344/1378 (25%) — mostly `"0"` (337) with a handful of `"1"` (7) |

### What's available (and what isn't)

- **Funding source IC** is **not** present as a structured field — the closest
  is `manual_grant_number` / `pdr_grant_number` / `calc_grant_number`, which are
  free-text strings of NIH grant numbers (e.g., `"OT2OD026549, ..."`) when
  populated at all (34% coverage). Mapping grant numbers → IC will require
  joining against NIH RePORTER in a downstream phase.
- **AoU data tier** is **not** present in the publication records (data tier is
  workspace-level, not pub-level). If you want pub ↔ tier, you'd need to join
  via project workspace IDs, which aren't in the pub records either.
- **Workspace / project linkage** is **not** populated in this feed. There is
  no `workspace_id` field on publication records. Linkage would have to be
  done via author / institution overlap or via the AoU internal RDR system
  (not publicly exposed).
- **Topical "focus" flags** *are* present as per-record booleans:
  `common_focus`, `rare_focus`, `maternal_focus`, `aging_focus`,
  `results_focus`, `behavioral_focus`, `environmental_focus`, `genetic_focus`,
  `population_health_focus`. These are AoU-curated tags. Counts in the corpus:
  common 411, rare 77, maternal 27, aging 35, results 23, behavioral 252,
  environmental 30, genetic 428, population-health 452.
- **iCite enrichment** is present: every record has `icite_count` (citation
  count) and `icite_rcr` (relative citation ratio).

### Year distribution

| Year | Pubs |
| --- | ---: |
| 2015 | 4 |
| 2016 | 4 |
| 2017 | 3 |
| 2018 | 12 |
| 2019 | 14 |
| 2020 | 10 |
| 2021 | 32 |
| 2022 | 79 |
| 2023 | 157 |
| 2024 | 343 |
| 2025 | 520 |
| 2026 | 253 |
| 2027 | 1 |

(2026-06-26 refresh: 2026 rose from 199 → 253; all other years unchanged.)

Note: 2026/2027 entries are publications dated by their indexing year (online
ahead of print or accepted manuscripts), not future records.

### Top 15 journals

```
 62  Archives of Dermatological Research
 58  Journal of the American Medical Informatics Association : JAMIA
 40  Nature Communications
 35  Journal of the American Academy of Dermatology
 25  (blank journal)
 23  PloS One
 21  American Journal of Human Genetics
 20  Nature Genetics
 19  JAMA Network Open
 18  Clinical and Experimental Dermatology
 17  Scientific Reports
 14  International Journal of Dermatology
 13  Nature
 11  Nature Medicine
 10  Ophthalmology
```

Worth noting: dermatology is the single largest specialty cluster (Archives of
Dermatological Research + Journal of the American Academy of Dermatology +
Clinical and Experimental Dermatology + International Journal of Dermatology +
Journal of Cutaneous Medicine and Surgery + others ≈ 175+ pubs). This is a
non-trivial fraction (~13%) of the AoU literature and a likely signal of one
or two prolific dermatology research groups using AoU.

### Sample records (verbatim, compact form)

```python
{'record_id': '1', 'pubmed_id': '36261664', 'pmc_id': 'None',
 'pdr_doi': '10.1007/s00403-022-02413-4',
 'pdr_title': 'Onychomycosis in underrepresented groups: an all of us database analysis',
 'pdr_date_year': '2022', 'pdr_journal_title': 'Archives of Dermatological Research'}

{'record_id': '374', 'pubmed_id': '38591407', 'pmc_id': '',
 'pdr_doi': '10.1177/12034754241245965',
 'pdr_title': 'Asian and Hispanic/Latino Patients Are High Risk for Melasma Development in a Cross-Sectional Cohort Study Using the All of Us Database',
 'pdr_date_year': '2024', 'pdr_journal_title': 'Journal of Cutaneous Medicine and Surgery'}

{'record_id': '1106', 'pubmed_id': '31412182', 'pmc_id': 'PMC8291101',
 'pdr_doi': '10.1056/NEJMsr1809937',
 'pdr_title': "The 'All of Us' Research Program",
 'pdr_date_year': '2019', 'pdr_journal_title': 'The New England Journal of Medicine'}

{'record_id': '2156', 'pubmed_id': '40075078', 'pmc_id': 'PMC11903676',
 'pdr_doi': '10.1038/s41467-025-57829-z',
 'pdr_title': 'GWAS identifies genetic loci, lifestyle factors and circulating biomarkers that are risk factors for sarcoidosis',
 'pdr_date_year': '2025', 'pdr_journal_title': 'Nature Communications'}

{'record_id': '3341', 'pubmed_id': '41908500', 'pmc_id': 'PMC13019322',
 'pdr_doi': '10.1016/j.xops.2026.101124',
 'pdr_title': 'Novel Systemic Associations of Idiopathic Epiretinal Membrane Identified via Machine Learning',
 'pdr_date_year': '2026', 'pdr_journal_title': 'Ophthalmology Science'}
```

(Full records — with abstracts, author lists, focus flags, iCite stats — are in `publications.jsonl`.)

### Data-quality caveats — publications

- **No duplicate PMIDs** in the corpus (1,332 distinct PMIDs across the 1,332
  records that have one). 46 records lack a PMID — these are typically very
  recent (ahead-of-print) or non-PubMed-indexed venues.
- **25 records have a blank journal field.** Probably the same edge cases.
- **`manual_*` fields are nearly always blank** — AoU's curators rarely
  override the upstream PubMed-derived (`pdr_*`) values. The exceptions are
  the `manual_review` flag (1 = reviewed) and the focus flags. Use `pdr_*`
  values as the canonical source.
- **The dermatology over-representation is real and unexplained** by the
  metadata — the dataset itself doesn't tell us why so many derm pubs use
  AoU. Worth flagging for Phase 2.
- **Funding-source mapping requires external join.** Grant-number fields are
  populated only for 34% of records, and even then they're free-text strings
  — mapping to NIH ICs needs RePORTER lookups (this is a known Phase 2 task).
- **Records flagged `manual_false_positive = "1"`** exist (the field is in the
  schema). Filter on this if running clean analyses.

## Projects

### Field coverage

| Field | Coverage |
| --- | ---: |
| `title` | 21,242 / 21,242 (100%) |
| `workspaceId` + `snapshotId` | 100% |
| `questions` (scientific question) | 21,241 / 21,242 |
| `approaches` (methods) | 21,238 / 21,242 |
| `findings` (anticipated / actual findings) | 21,239 / 21,242 |
| `purposes` (free-text + controlled tags) | 21,242 / 21,242 |
| `accessTier` (Registered / Controlled) | 21,242 / 21,242 |
| `team.owner` (PI + role + institution) | 21,242 / 21,242 |
| `categories` (UBR demographic categories) | **6,966 / 21,242 (33%) — populated only when `ubrFocus = true`** |
| `ubrFocus` (boolean) | 21,242 / 21,242 |
| `reviewUrl` (REDCap project-review form) | 21,242 / 21,242 |

### What's available (and what isn't)

- **Scientific aim, approach, anticipated findings** are present as three
  separate free-text fields (`questions`, `approaches`, `findings`) for
  nearly every record. Text is reasonably structured (typically a paragraph or
  three per field) and is what AoU calls the "Research Description" workspace
  metadata.
- **PI institution and role** are present via `team.owner[0]`. The role
  values are AoU-controlled (Graduate Trainee, Research Fellow, Early Career
  Tenure-track Researcher, etc. — see the role distribution below).
- **No registration date, status, or completion date** is present in the
  feed. Workspaces are listed regardless of activity status. (The page's
  `?status=ACTIVE` query param at the upstream RDR API hints that there is a
  status field internally, but it's not exposed in the cached JSON.)
- **No data tier version** beyond the binary Registered/Controlled split
  (i.e., we don't see which CDR version is in use).
- **No link to publications.** AoU does not surface project ↔ publication
  joins on either feed.
- **`purposes`** is a controlled vocabulary in principle (Disease Focused
  Research, Educational, Ancestry, etc.), but in practice ~10% of records
  have free-text "Other Purpose (...)" strings as one of their purposes. The
  most common controlled values are listed below.
- **`categories`** (the UBR demographic flags — Race/Ethnicity, Age,
  Geography, Income Level, etc.) are populated only when `ubrFocus = true`;
  records that aren't UBR-focused have an empty `categories` array.

### Access tier

| Tier | N |
| --- | ---: |
| Controlled Tier | 12,737 (60%) |
| Registered Tier | 8,505 (40%) |

### UBR (Underrepresented in Biomedical Research) focus

| Flag | N |
| --- | ---: |
| `ubrFocus = true` | 6,966 (33%) |
| `ubrFocus = false` | 14,276 (67%) |

### Purpose tags (top 20)

```
 6347  Educational
 5451  Ancestry
 4925  Population Health
 4095  Methods Development
 2864  Social / Behavioral
 1193  Control Set
 1004  Drug Development
  528  Other Purpose (genomic data demo workshop)
  269  Other Purpose (Hail GWAS workshop)
  254  Ethical, Legal, and Social Implications (ELSI)
  224  Disease Focused Research (cancer)
  202  Commercial
  158  Disease Focused Research (type 2 diabetes mellitus)
  150  Other Purpose (AoU Tutorial Workspace)
  138  Disease Focused Research (Alzheimer's disease)
  134  Other Purpose (Office hours best-practice notebooks)
  130  Other Purpose (AoU Demonstration Project)
  115  Other Purpose (AoU Phenotype Library Workspace)
  109  Disease Focused Research (breast cancer)
   76  Disease Focused Research (prostate cancer)
```

A workspace can carry multiple purposes (purpose tags are not mutually
exclusive), so these don't sum to 21,242.

### UBR category distribution (where populated)

```
 5599  Race / Ethnicity
 3249  Age
 2641  Access to Care
 2621  Income Level
 2542  Geography
 2349  Education Level
 1534  Sex at Birth
 1507  Gender Identity
 1497  Disability Status
 1333  Sexual Orientation
  193  Others
```

### Role distribution (workspace owners; one per owner record)

```
 7964  Graduate Trainee
 3773  Research Fellow
 2897  Early Career Tenure-track Researcher
 2836  Project Personnel
 2663  Undergraduate Student
 2633  Other
  964  Mid-career Tenured Researcher
  827  Senior Researcher
  613  Research Associate
  378  Teacher/Instructor/Professor
  344  Late Career Tenured Researcher
  291  Research Assistant
  181  Student
   74  Administrator
```

About half of all workspace owners are graduate trainees, undergraduates,
research fellows, or postdocs (~17k of ~27k owner entries). This is consistent
with AoU's heavy use as a training platform.

### Top 20 institutions (workspace-owner count)

```
 939  Arizona State University
 908  Baylor College of Medicine
 588  Vanderbilt University Medical Center
 553  Yale University
 552  University of California, San Diego
 526  Mass General Brigham
 522  University of Pittsburgh
 433  Broad Institute
 432  University of Arizona
 417  University of California, Irvine
 403  University of Pennsylvania
 357  Stanford University
 349  Cornell University
 344  Icahn School of Medicine at Mount Sinai
 341  Columbia University
 323  Johns Hopkins University
 323  National Human Genome Research Institute (NIH - NHGRI)
 294  University of California, Los Angeles
 279  University of Washington
 279  University of Chicago
```

Note: NIH-NHGRI shows up at ~323 owners — these are AoU staff and DRC
personnel running workspaces, not external NHGRI grantees.

### Sample records (verbatim, compact form)

```python
{'workspaceId': 35015, 'snapshotId': 66857,
 'title': '20251024_rs7636910', 'accessTier': 'Controlled Tier',
 'purposes': ['Drug Development', 'Ancestry'], 'categories': [], 'ubrFocus': False}

{'workspaceId': 30012, 'snapshotId': 56656,
 'title': 'V8 Exploring the All of Us data for hypertension and other phenotypes',
 'accessTier': 'Controlled Tier', 'purposes': ['Educational'], 'categories': [], 'ubrFocus': False}

{'workspaceId': 22009, 'snapshotId': 41218,
 'title': 'Disparities in Orthopaedic & Neurosurgical Care Access',
 'accessTier': 'Controlled Tier', 'purposes': ['Population Health'],
 'categories': ['Race / Ethnicity', 'Age', 'Geography', 'Disability Status',
                'Access to Care', 'Education Level', 'Income Level'],
 'ubrFocus': True}

{'workspaceId': 13562, 'snapshotId': 25206,
 'title': 'Duplicate of Control Tier User Support Content v7 (Fall 2023)',
 'accessTier': 'Controlled Tier', 'purposes': ['Educational'], 'categories': [], 'ubrFocus': False}

{'workspaceId': 3307, 'snapshotId': 7550,
 'title': 'PracticeWorkspace', 'accessTier': 'Registered Tier',
 'purposes': ['Other Purpose (Workspace to practice and learn how AllofUs works...)'],
 'categories': [], 'ubrFocus': False}
```

(Full records — with full multi-paragraph scientific aim, approach, and
findings text — are in `projects.jsonl`.)

### Data-quality caveats — projects

- **Heavy training / educational tail.** Roughly 6,000+ workspaces are
  tagged `Educational`, and many more are titled "PracticeWorkspace", "AoU
  Tutorial", "Duplicate of …", "20251024_<gene>" (timestamped class
  exercises), or similar. For research-landscape comparison work you almost
  certainly want to **filter out trainee / tutorial workspaces**. Useful
  signals to filter on:
    - `purposes` contains `Educational`;
    - title matches `^(Test|Demo|Demonstration|AoU Tutorial|All of Us Tutorial|PracticeWorkspace|Duplicate of|V[0-9]+ |[0-9]{8}_)`;
    - `team.owner[0].role` in `Graduate Trainee`, `Undergraduate Student`,
      `Student`, `Project Personnel`;
    - all three of `questions` / `approaches` / `findings` shorter than
      ~30 chars (we counted **159 such stubs**).
  None of these is a perfect filter — there are real undergrad research
  projects with meaningful descriptions — but together they should knock out
  most of the noise. Phase 2 will need to make a deliberate call on the
  filter rule and document it.
- **Many title collisions (884 case-folded duplicates).** These are
  mostly workshop / training duplicates ("PracticeWorkspace",
  "Duplicate of …", etc.); a small minority might be the same researcher
  saving multiple snapshots of the same workspace. `workspaceId` is the
  canonical primary key — `snapshotId` is the per-version key.
- **The dataset is from 2025-10-24, not today.** Projects registered between
  then and 2026-06-02 are missing. Given the project list grew from ~5.9 MB
  (2024-09-24) to 12.6 MB (2025-10-24), the corpus is presumably ~25–30k
  workspaces by mid-2026; we're missing the recent quarter. **Mitigation:**
  retry the prod endpoint daily and refresh when it comes back online.
- **No funding-source / NIH-IC information** anywhere in the project records,
  not even free-text grant numbers. Tier 1 priority gap for Phase 2.
- **No publication ↔ project linkage** in either feed. You can sometimes
  infer linkage via PI institution + concurrent timeframe, but it's
  approximate.
- **`reviewUrl` values from the Wayback dump are wayback-wrapped.** The
  underlying REDCap survey URLs are
  `https://redcap.pmi-ops.org/surveys/?s=NMWWCNFA4L&rw_workspace_id=<id>&rw_snapshot_id=<id>&rw_workspace_name=<urlencoded>`
  — strip the `https://web.archive.org/web/<timestamp>/` prefix to get the
  real URL. The extractor leaves them as captured.

## Phase 2 enrichment (2026-06-02)

Phase 2a–2b work product: filtering projects to substantive research,
attributing publications to NIH ICs via RePORTER, and drafting a unified
theme taxonomy spanning both corpora. **Per-record taxonomy tagging is NOT
yet applied — that is Phase 2c, gated on user review of the taxonomy.**

### Filter counts (Workstream A — `filter.py`)

| Step | N | Δ |
| --- | ---: | ---: |
| Input total | 21,242 | — |
| After dropping `Educational`-tagged | 14,895 | −6,347 |
| After dropping training-role workspaces (kept 9,437 substantive-trainee, dropped 305) | 14,590 | −305 |
| After dropping stubs (all of question/approach/findings < 30 chars) | 14,570 | −20 |
| After dropping case-folded duplicate titles | **12,899** | −1,671 |

Filter rule lives in `filter.py`; outputs are `projects_filtered.jsonl` and
`projects_filtered.csv`. The trainee-role drop is permissive — workspaces
with combined Q+A+F text ≥ 300 chars are kept even if the owner role is
trainee, since many real undergrad/grad research projects have substantive
descriptions. Duplicate-title drop removed the bulk (1,671) — these are
"Duplicate of …" workshop-copies and PI-saved snapshots.

### IC attribution (Workstream B — `ic_attribute.py`)

| Metric | N | % |
| --- | ---: | ---: |
| Publications total | 1,378 | 100% |
| Pubs with a non-N/A grant string | 445 | 32.3% |
| Pubs with at least one parseable grant ID | 429 | 31.1% |
| Pubs with at least one IC attribution | **422** | **30.6%** |
| Unique grant IDs queried (RePORTER) | 858 | — |
| Unique grant IDs resolved | 806 | 94.0% |
| Unique grant IDs unresolved | 52 | 6.0% |

Unresolved IDs are mostly non-NIH grants (CDC HHSN contracts; foundation
grants like Sigrid Jusélius, Gordon & Betty Moore Foundation, BHF, NHMRC),
Z99 RePORTER placeholders, and a handful of typo'd IDs (`OT2OD35404`,
`RO1HL092577`). RePORTER does cover the AoU Awardee Operations OT2 cluster
(`OT2OD026548–026557`) and they resolved correctly in the second pass after
paginating beyond the 500-record-per-page limit.

**Top 10 admin ICs by pub count:**

| IC | Pubs (admin) | Pubs (cofunding) |
| --- | ---: | ---: |
| OD | 275 | 333 |
| TR | 75 | 245 |
| HL | 73 | 78 |
| HG | 65 | 78 |
| CA | 47 | 53 |
| GM | 38 | 38 |
| DK | 32 | 35 |
| LM | 32 | 31 |
| AG | 31 | 56 |
| MD | 28 | 30 |

Notes:
- **OD dominance is structurally expected** — the AoU program itself is
  funded out of NIH-OD via the OT2 awardee operations grants, so every
  publication using the AoU data tends to cite at least one OT2 OD grant.
- **TR co-funding (245)** is large because of CTSA UL1 grants — the
  institutional-CTSA infrastructure that funds AoU PIs at the site level.
- **HL, HG, CA, GM, DK, AG, LM** reflect the actual disease-IC science
  funding underlying AoU work. The full distribution is in
  `ic_attribute_report.txt`.

Outputs: `publications_with_ic.jsonl`, `publications_with_ic.csv`,
`ic_attribute_report.txt`, and cached RePORTER batches in `raw/reporter/`.

### Taxonomy draft (Workstream C — `taxonomy_draft.md`)

Drafted 19 top-level themes spanning both corpora, with 2–6 subthemes each
and rough fraction-of-corpus estimates. Themes span:

- Disease-anchored (Cardiometabolic, Cancer, Mental Health, Dermatology, …)
- Cross-cutting (SDOH & Health Disparities; Wearables & Digital Health)
- Methods-anchored (Genomics Methods, Methods/Infrastructure/Phenotyping)
- Specialty / smaller (Pharmacogenomics, Rare Disease, ELSI, Environmental)

Top 5 by rough share: Genomics methods (~28%), Cardiometabolic (~22%),
Methods/Phenotyping (~20%), Mental health & substance (~18%), Cancer
(~15%). See `taxonomy_draft.md` for full definitions, indicative keywords,
example records, and the **"Decisions needed from the user before tagging"**
section.

### Decisions needed from the user before tagging

Captured in `taxonomy_draft.md` — the 7 open editorial calls are:

1. Keep Dermatology as its own theme or fold it into Cancer/Autoimmune?
2. Wearables as standalone theme or subtheme of Methods?
3. Pharmacogenomics as standalone or subtheme of Genomics methods?
4. ELSI/engagement: research vs. AoU-program-meta split?
5. Stroke multi-tagging (Cardiometabolic + Neurology) — confirm?
6. CKM-Syndrome elevated to its own subtheme (for NHLBI/NIDDK trackability)?
7. AoU-program-meta pubs — own audit-only bucket?

Once these are resolved, Phase 2c (per-record tagging) can proceed.

### Phase 2a–2b scripts

| Script | What it does |
| --- | --- |
| `filter.py` | Reproducible project-filter rule → `projects_filtered.{jsonl,csv}` |
| `ic_attribute.py` | RePORTER IC attribution → `publications_with_ic.{jsonl,csv}` and `ic_attribute_report.txt`. Caches batches in `raw/reporter/`. |
| `sample_for_taxonomy.py` | Stratified sampling for taxonomy discovery + validation. Outputs `taxonomy_sample_discovery.txt` and `taxonomy_sample_validation.txt`. |

## Phase 1 deliberate non-goals

- No clustering into themes / topic modeling.
- No comparison against NIH IC strategic plans.
- No filtering decisions baked into `publications.csv` / `projects.csv` —
  every record is included as-fetched so Phase 2 can apply its own filters.
- No commit to git.

## Reproducibility

To re-pull from scratch:

```bash
python3 extract.py --refetch
```

This will:

1. Refetch `https://www.researchallofus.org/wp-json/rh-data-caching/publications-report`
2. Try `https://www.researchallofus.org/wp-json/rh-data-caching/projects`;
   if it returns fewer than 500 records (currently the case — prod is broken),
   fall back to the 2025-10-24 Wayback capture.
3. Rebuild all four output files.

Total pull + extract should complete in well under a minute when both
endpoints are healthy.

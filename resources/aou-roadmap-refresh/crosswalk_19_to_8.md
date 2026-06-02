# Crosswalk: 19-theme taxonomy → 8 AoU Scientific Roadmap focus areas

**Phase 3a deliverable, AoU Scientific Roadmap Refresh evidence base.**
Inputs: 1,374 substantive publications and 12,899 substantive project workspaces
tagged with the locked 19-theme taxonomy (`../aou-research-landscape/taxonomy.md`).
Reference for the 8 focus areas: `AOU Scientific Roadmap.pptx` and slide 7 of
`2026 Science Committee Working Groups.pptx`.

This document answers **Q6: Are the priority health domains still relevant?**

---

## 1. Method

Each of the 19 themes in the locked taxonomy was assigned to one or more of the
8 focus areas (FA1–FA8) by reading the theme definition, subthemes, and
keyword lists in `taxonomy.md` against the focus-area descriptions in the
Roadmap deck. Multi-mapping is preferred where a theme substantively touches
more than one area (e.g., Cardiometabolic disease is FA1 in its disease framing
*and* FA8 in its polygenic-genetics framing). Where no focus area provides a
clean home, the theme is marked **orphan**.

Reverse aggregation: every publication and project was assigned the union of
its themes' focus areas. Records may carry zero focus-area tags (orphan
records, ~9% of pubs / ~14% of projects); records may also carry as many as
6–7 focus-area tags simultaneously, and the per-FA counts therefore sum to
more than the corpus total. Shares below are *share-of-corpus-touched*, not
mutually exclusive.

The 8 focus areas (Roadmap deck):

| Code | Focus area |
|---|---|
| FA1 | Prevalent Common & Rare Conditions |
| FA2 | Maternal & Child Health |
| FA3 | Healthy Aging & Resilience Across the Lifespan |
| FA4 | Return of Results on Individual & Population Health |
| FA5 | Lifestyle, Substance, & Behavioral Health |
| FA6 | Environment |
| FA7 | Health Equity |
| FA8 | Genetics & Biology |

---

## 2. Per-theme focus-area assignment

| # | Theme | Focus areas | Mapping note |
|---|---|---|---|
| 1 | Cardiometabolic disease | FA1, FA8 | Primarily Common & Rare Conditions; subtheme 1.3-CKM and polygenic cardiometabolic genetics cross-touch Genetics & Biology. |
| 2 | Genomics methods & complex-trait genetics | FA8 | Maps directly to Genetics & Biology. **Caveat: "Genetics & Biology" as named is narrower than current science** — see orphan analysis on multi-omics. |
| 3 | Methods, infrastructure & phenotyping (non-genomic) | **ORPHAN** | AI/ML, EHR phenotyping, AoU workbench tooling, OMOP/FHIR harmonization. ~18% of pubs; ~19% of projects. No focus area accommodates methods/infrastructure as a first-class concern. |
| 4 | Mental health, behavioral & substance use | FA5, FA1 | Primarily Lifestyle/Substance/Behavioral Health; psychiatric disorders also fit Common & Rare Conditions. |
| 5 | Cancer | FA1, FA8 | Primarily Common & Rare Conditions; hereditary-cancer subthemes cross-touch Genetics & Biology. |
| 6 | Social determinants of health & health disparities | FA7 | Maps directly to Health Equity. Heavy double-tagging with disease themes. |
| 7 | Wearables & digital health | **ORPHAN** | No home in the 8 areas. Could be tucked into FA5 as activity-tracking but that misses sleep/HRV/biometric methods and the multimodal EHR+wearable AI subtheme. ~5% of pubs, ~7% of projects. |
| 8 | Infectious disease & immunology | FA1 | Common & Rare Conditions — HIV, COVID-19, hepatitis, EBV. |
| 9 | Autoimmune & inflammatory disease | FA1 | Common & Rare Conditions. |
| 10 | Rare disease & Mendelian genetics | FA1, FA8, FA4 | Common & Rare Conditions (explicit "rare"); Genetics & Biology; and Return of Results, since ACMG actionable variants drive ROR workflows. |
| 11 | Aging, frailty & ADRD | FA3, FA1 | Primarily Healthy Aging & Resilience; ADRD also fits Common & Rare Conditions. |
| 12 | Dermatology | FA1, FA7 | Common & Rare Conditions; the AoU dermatology corpus is largely disparities-framed. |
| 13 | Respiratory & sleep medicine | FA1 | Common & Rare Conditions. |
| 14 | Neurology (non-ADRD) | FA1 | Common & Rare Conditions. |
| 15 | Pregnancy, maternal & women's health | FA2 | Maternal & Child Health — note that the focus-area name says "Maternal & Child" but AoU is an adult cohort, so "Child" is structurally absent. |
| 16 | Pharmacogenomics & drug response | FA8, FA4 | Genetics & Biology and Return of Results (PGx is the canonical genotype-drives-treatment ROR use case). |
| 17 | ELSI, participant engagement & recruitment | FA4, FA7 | Return of Results (ROR ethics is the dominant ELSI sub-area) and Health Equity (recruitment of underrepresented groups). |
| 18 | Ophthalmology, ENT & sensory medicine | FA1, FA7 | Common & Rare Conditions; strong disparities-in-sensory-care framing. |
| 19 | Environmental health & climate | FA6 | Environment — clean fit but tiny (~0.5% of pubs). |

Machine-readable version: `theme_to_focus_area.csv`.

---

## 3. Reverse view: corpus shares per focus area (bottom-up)

Publications (n = 1,374 substantive):

| FA | Focus area | n pubs | Share | Top contributing themes (pub count) |
|---|---|---:|---:|---|
| FA1 | Prevalent Common & Rare Conditions | 1,008 | 73.4% | 1 (382); 4 (254); 12 (197); 5 (176); 18 (107); 9 (107); 8 (79); 14 (77); 11 (75); 13 (59); 10 (54) |
| FA8 | Genetics & Biology | 733 | 53.4% | 2 (347); 1 (382 carry-over via cardiometabolic genetics); 5 (176); 10 (54); 16 (32) |
| FA7 | Health Equity | 702 | 51.1% | 6 (458); 12 (197); 18 (107); 17 (69) |
| FA5 | Lifestyle, Substance, & Behavioral Health | 254 | 18.5% | 4 (254) |
| FA4 | Return of Results | 154 | 11.2% | 17 (69); 10 (54); 16 (32) |
| FA3 | Healthy Aging & Resilience | 75 | 5.5% | 11 (75) |
| FA2 | Maternal & Child Health | 37 | 2.7% | 15 (37) |
| FA6 | Environment | 7 | 0.5% | 19 (7) |

Projects (n = 12,899 substantive):

| FA | Focus area | n projects | Share | Top contributing themes (project count) |
|---|---|---:|---:|---|
| FA1 | Prevalent Common & Rare Conditions | 8,495 | 65.9% | 1 (3,292); 4 (1,937); 5 (1,722); 9 (650); 8 (639); 11 (637); 14 (567); 12 (535); 18 (470); 10 (433); 13 (405) |
| FA8 | Genetics & Biology | 7,791 | 60.4% | 2 (4,414); 1 (3,292); 5 (1,722); 10 (433); 16 (200) |
| FA7 | Health Equity | 3,813 | 29.6% | 6 (3,070); 12 (535); 18 (470); 17 (61) |
| FA5 | Lifestyle, Substance, & Behavioral Health | 1,937 | 15.0% | 4 (1,937) |
| FA2 | Maternal & Child Health | 678 | 5.3% | 15 (678) |
| FA4 | Return of Results | 668 | 5.2% | 10 (433); 16 (200); 17 (61) |
| FA3 | Healthy Aging & Resilience | 637 | 4.9% | 11 (637) |
| FA6 | Environment | 74 | 0.6% | 19 (74) |

Orphan records (no focus-area tag because their themes are all orphan themes
3 / 7): **119 pubs (8.7%)**, **1,821 projects (14.1%)**.

Machine-readable version: `focus_area_summary.csv`.

### Consistency check vs. DRC's 2023 workspace mapping

The DRC's prior workspace-mapping work (slides 15, 46, 74 of `Methods and
Findings_Scientific Roadmap Planning.pptx`) reported, on a 2,981-workspace
2023 snapshot: Health Equity ~2,000; Genetics & Biology ~1,900; Common+Rare
Conditions ~1,300–1,956.

Our corpus is ~4.3× larger (12,899 projects). Scaled proportions:

| FA | DRC 2023 share (approx) | Our bottom-up share | Ratio |
|---|---:|---:|---:|
| Health Equity | ~67% | 29.6% | substantially lower |
| Genetics & Biology | ~64% | 60.4% | comparable |
| Common+Rare | ~44–66% | 65.9% | comparable / higher |

The **Health Equity gap** is real and reflects a methodological difference,
not a finding of declining equity work: the DRC's prior mapping flagged any
workspace with *demographic stratification language* as "Health Equity,"
whereas our taxonomy reserves theme 6 for workspaces in which the analytic
contribution itself is the role of SDOH / structural inequity / disparity.
Our number is more conservative; the DRC number is more inclusive. Both are
defensible; the conservative number is more useful for arguing that equity
work needs to be *protected* in the Refresh because it isn't simply absorbed
into every other domain. The Genetics & Biology and Common+Rare shares
line up well, which is a sanity check on the crosswalk.

---

## 4. Orphan-themes analysis (the evidence for Q6)

Three groups of work in our corpus do not have a clean home in the current
8 focus areas. Each is meaningful at corpus scale, each is on slide 7's
"reflections since 2023" list, and the Refresh needs to decide whether to
elevate, rename, or absorb them.

### 4.1 Theme 3 — Methods, infrastructure, AI/ML & phenotyping (251 pubs, 2,389 projects; ~18% of pubs)

**Where it currently lives.** Nowhere cleanly. 70% of theme-3 pubs co-tag
with a disease theme (176 of 251 pubs, 1,786 of 2,389 projects) — so they
get pulled into FA1, FA8, etc. via the disease tag — but the *methods*
contribution itself is invisible in an 8-area view. The remaining 30% (75
pubs, 603 projects) are "pure methods" — AoU workbench R packages,
phenotyping algorithms, EHR data-quality work, federated-learning frameworks,
synthetic-data work, OMOP/FHIR harmonization — and they vanish entirely.

**Why the fit is awkward.** The 8 focus areas are health-domain anchored.
Methods, infrastructure, AI/ML, and the AoU workbench tooling that makes
*everything else* possible aren't a health domain — they're a substrate.
Subsuming them under FA8 "Genetics & Biology" is incorrect (the work is
explicitly non-genomic phenotyping and EHR). Subsuming them under FA1 is
incorrect (it's not disease-anchored). Subsuming them under FA4 "Return of
Results" is incorrect for most of the theme.

**Corpus volume.** 251 publications (18% of substantive pubs). 2,389
projects (19% of substantive projects). This is the *single largest orphan*.
Subtheme 3.2 ("ML / AI for disease prediction & risk stratification") and
3.4 ("AoU platform tooling") map directly to slide-7 priorities AI/LLMs and
low-code/no-code.

**Refresh recommendation evidence.** A new focus area named something like
"**Data, AI & Methods**" or "**Computational Infrastructure & AI**" would
cleanly absorb theme 3 plus the AI/LLM portion of slide 7. Without it,
~18–19% of substantive AoU output is unrepresented in the priorities
framework. The independent HA4 hot-area detector finds 31 AI/foundation/LLM
pubs (28 of them post-2023, +0.0039 trend), confirming a real and growing
sub-signal that has no current home.

### 4.2 Theme 7 — Wearables & digital health (73 pubs, 923 projects; ~5% of pubs)

**Where it currently lives.** 71% of theme-7 pubs co-tag with a disease
theme (52 of 73 pubs) — so they show up in FA1 / FA3 / FA5 via the disease
tag — but the *wearable methodology* is again invisible. The 21 "wearable-
pure" pubs (with no disease tag) and ~250 wearable-pure projects vanish.

**Why the fit is awkward.** The closest stretch-fit is FA5 "Lifestyle,
Substance & Behavioral Health" if you read wearables as activity-tracking.
But that misses sleep-stage / HRV / heart-rate / circadian biomarker work
(which is closer to FA1 cardiometabolic and respiratory) and the multimodal
EHR+wearable AI work (which sits closer to theme 3). A wearables-only home
in FA5 would also encode an outdated framing that wearables are about
behavior modification rather than physiologic measurement at scale.

**Corpus volume.** 73 pubs (5%). 923 projects (7%). Independent HA2
(wearables) detector finds 70 pubs, 62 post-2023 — large absolute volume
but trend-flat (~0.0 share change), suggesting wearables have *already*
matured to a steady-state of attention. They are not a "rising" hot area;
they are a *current* hot area with a permanent place in the corpus.

**Refresh recommendation evidence.** Either elevate wearables/remote
monitoring to its own focus area, or fold under a renamed methods area
("**Sensors, Wearables & Computational Methods**"). Slide 7 explicitly
identifies "remote monitoring & digital health assessments" as a 2023+
priority — keeping it as theme 7 only buries the evidence.

### 4.3 Multi-omics beyond genomics (currently buried inside theme 2)

**Where it currently lives.** Inside theme 2 "Genomics methods & complex-
trait genetics," which maps to FA8 "Genetics & Biology." But theme 2's
definition and keywords are heavily genomics-centric (GWAS, PRS, fine-mapping,
WGS, long-read) and the named focus area says "Genetics & Biology," not
"Multi-omics." Proteomics, metabolomics, transcriptomics, lipidomics —
slide-7 priorities — are quietly bundled in.

**Why the fit is awkward.** AoU is *not yet* a multi-omic cohort at scale
(no Olink/SomaScan/MS-proteomics release as of mid-2026), but the slide-7
WG flagged multi-omics as a 2023+ priority *because* the cohort is on the
cusp of generating that data. The independent HA1 (multi-omics beyond
genomics) detector finds **only 24 pubs total** (23 post-2023, +0.0125
trend). That is *thin coverage on a Refresh-priority topic* — i.e., the
evidence the WG suspected exists is mostly hopes-and-plans, not yet
realized output.

**Corpus volume.** 24 pubs detected by independent keyword search across
title+abstract. <2% of substantive corpus.

**Refresh recommendation evidence.** The framing question is whether to
rename FA8 from "Genetics & Biology" to "**Genetics, Multi-omics &
Biology**" so that future proteomics / metabolomics / transcriptomics
releases have a home, or to leave the rename to a later Refresh once the
output exists. The current 24-pub footprint argues for the rename to send
a forward signal without forcing a corpus-share commitment.

### 4.4 Imaging & radiomics (currently buried inside theme 3)

**Where it currently lives.** Inside theme 3 (methods/AI), which is itself
already an orphan. Imaging is a subtheme of theme 3 but was never broken
out as a top-level theme because there was insufficient corpus evidence
during taxonomy lock.

**Why the fit is awkward.** Imaging is a slide-7 priority. Our independent
HA3 (imaging/radiomics) detector finds **only 8 pubs total** — *below the
thin-coverage threshold*. AoU has not yet released imaging at scale (no
chest X-rays, MRIs, retinal photos) and the eight pubs are almost all about
*using imaging from external sources linked to AoU phenotypes*, not about
AoU's own imaging contribution. The Refresh should treat this as a gap
worth flagging: if imaging is a 2023+ priority, **the corpus shows almost
no evidence the cohort is delivering on it yet** — which is itself a
finding the WG should surface.

**Corpus volume.** 8 pubs, ~0.6% of corpus. **Below thin-coverage flag.**

---

## 5. Other notable mapping observations

- **FA2 "Maternal & Child Health" has no "child" content.** AoU enrolls
  adults only; subtheme 15.x covers maternal/pregnancy/women's health, and
  the entire FA2 share (2.7% of pubs, 5.3% of projects) is maternal-side.
  The Refresh might consider renaming this area to "**Reproductive &
  Maternal Health**" or to "**Maternal Health & Pediatric Linkage**" if a
  pediatric arm is planned. As named today, "Child" is aspirational
  rather than evidenced.
- **FA4 "Return of Results" is heterogeneous.** Three contributing themes
  (10 rare disease, 16 pharmacogenomics, 17 ELSI/engagement) come from
  very different framings. PGx ROR vs. ACMG ROR vs. consent-and-ethics
  ROR are not the same operational problem. If FA4 is retained the WG
  should clarify whether the priority is ROR *implementation* (pharmacy
  workflows, ACMG result delivery) or ROR *research* (return-of-results
  ethics, participant-facing UX). Our corpus has both but in different
  proportions.
- **FA7 "Health Equity" cross-cuts.** 51% of substantive pubs (702) touch
  FA7. The mapping is conservative — this is *not* a finding that half the
  corpus is health-equity research. It's a finding that AoU's UBR-oversampling
  design pulls equity framing into a large fraction of its output, and that
  cross-cutting role is what makes equity work load-bearing for the program
  as a whole. Reducing FA7 to a single column would lose this.
- **FA6 "Environment" is thin (0.5% pubs, 0.6% projects).** Theme 19
  exists, but the corpus is small. The independent HA5 (environmental
  health) detector finds 12 pubs — slightly above our theme-19 count
  because the detector catches "environmental exposure" framing in
  cardiometabolic/respiratory pubs that aren't theme-19-tagged. Environmental
  health is a slide-7 priority and is structurally under-represented in the
  corpus. The Refresh should either invest in environmental linkage (climate
  data, air-quality joins) or accept that this area will remain small.

---

## 6. Q6 answer (one paragraph)

**The 8 current focus areas mostly hold but show three structural problems
that the Refresh should address.** The disease-anchored areas — FA1 Common
& Rare Conditions (73% pub share), FA8 Genetics & Biology (53%), FA7 Health
Equity (51%), FA5 Lifestyle & Behavioral Health (18%), FA3 Healthy Aging
(6%), FA2 Maternal & Child Health (3%), FA6 Environment (0.5%) — all map
to real corpus volume and remain coherent priorities; FA4 Return of Results
is heterogeneous but defensible. The structural problems are that **(a)**
~18% of the substantive corpus (theme 3: methods, AI/ML, EHR phenotyping,
workbench tooling) has no first-class home in the 8 areas and is the single
largest orphan; **(b)** Wearables & digital health (theme 7, 5% of pubs but
explicitly on slide 7 as a 2023+ priority) is similarly orphaned, with the
keyword-based detector finding 70 wearable pubs and effectively flat trend,
i.e., wearables have already matured to a permanent place in the work but
no home in the priorities; and **(c)** Multi-omics beyond genomics, imaging
& radiomics, and AI/foundation models — all slide-7 priorities — are
respectively buried in FA8, buried in theme 3, and orphaned. Two concrete
recommendations follow from the evidence: **add a "Data, AI & Methods" focus
area** to absorb theme 3 plus wearables plus imaging/AI, and **rename FA8
to "Genetics, Multi-omics & Biology"** to send a forward signal as the
cohort approaches its proteomics/metabolomics releases. FA2 should also be
considered for rename ("Maternal Health" or "Reproductive & Maternal
Health") since "Child" content is structurally absent from an adult cohort.

---

## 7. Files written by this phase

| File | Purpose |
|---|---|
| `theme_to_focus_area.csv` | 19-theme → 8-focus-area assignment with notes and orphan flag |
| `focus_area_summary.csv` | Per-focus-area corpus shares, contributing themes, theme breakdown |
| `publications_tagged_with_focus.csv` | All 1,374 substantive pubs with `focus_areas` column added |
| `projects_tagged_with_focus.csv` | All 12,899 substantive projects with `focus_areas` column added |
| `crosswalk_19_to_8.md` | (this file) |

Companion Phase 3b outputs in `temporal_trends.md`.

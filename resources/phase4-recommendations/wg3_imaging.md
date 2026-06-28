# WG-3: Imaging Integration

> This is a **topic / need area**, not a decision body. Its topic overlaps
> with the other need areas and should be coordinated across them. The WG
> label is used here as a topic reference.

## Lead(s) and scope

**Co-leads (chairs):** Burnside & Giannini.
**Scope (per 2026 WG deck):** integrate imaging into AoU — which imaging
modalities, on what timeline, with what governance, and how researchers will
access them.

**Reality check (from the evidence):** AoU has **8 imaging pubs in the
corpus** (HA3, ~0.6% — *thin-coverage flag*), and almost all 8 use
*external* imaging (UKB MRI fat measures, etc.) linked to AoU phenotypes,
not AoU-originated imaging. The imaging need area is starting *from
infrastructure*, not from a research-utilization base — recommendations
should reflect that.

---

## Candidate recommendations evaluated

1. **A staged imaging data-release plan** specifying which modalities
   release first (retinal photos, ECG waveforms, chest X-rays, then MRI),
   timeline, and Workbench access tier.
2. **DICOM + downstream-standard adoption** for any imaging release, with
   FHIR ImagingStudy resource support for EHR-radiomics linkage.
3. **Radiomics-to-phecode crosswalk** pilot — building on Smoller's phecode
   priority, link radiomics-derived features to existing AoU phecode
   phenotypes so the imaging release immediately interoperates with the
   established analytic infrastructure.
4. **An AI-radiomics pilot mechanism** that explicitly invites cross-
   pollination with the AI need area.
5. **A pre-release imaging-data quality and bias framework** building on
   the WG-2 bias-in-translation framework.
6. **Partnership with UKB/NIH-Imaging Data Commons** for cross-cohort
   imaging-AI validation prior to AoU-internal release.

---

## Top-3 ranked recommendations

### 1. Adopt a staged, modality-prioritized imaging-release roadmap

**Description.** Define a publicly stated staged release plan that
sequences imaging modalities by feasibility and research demand: **(1)**
already-collected biospecimen-linked imaging (e.g., retinal photos via
ophthalmologic study modules, ECG/spirometry waveforms) — fastest, lowest
governance friction; **(2)** linked-EHR DICOM imaging via the EHR data
partnership (chest X-rays, CT, mammography — already in patient records,
governance and de-identification are the work, not collection); **(3)**
prospective imaging modules (cardiac MRI, abdominal imaging, brain MRI in
subcohort) — multi-year. Each tier gets a stated timeline and an explicit
research-question target.

**Supporting evidence.**
- HA3 corpus today: 8 pubs (`temporal_trends.md` §4 / `crosswalk_19_to_8.md`
  §4.4). Below the thin-coverage threshold. Examples PMID:41053791 (obesity
  genetics with MRI fat measures, *external* imaging), PMID:41039588
  (MASLD genetics with abdominal ultrasound), PMID:41121728 (mammography
  screening intensity vs SDOH — the closest to "AoU imaging contribution"
  but still uses EHR-derived screening data, not AoU-released images).
- NCI Annual Plan FY26 NCIB-AI explicitly calls for AI-for-screening (NCI
  per-IC brief, gap_analysis §B2). NCI imaging-data gap is real.
- NEI G6 (data science and imaging for ophthalmology) — retinal imaging is
  the lowest-friction-to-release modality with the highest IC alignment.
- NIBIB G4 (biomedical imaging) — same gap (NIBIB per-IC brief).
- Peer reference: UKB's 100k MRI release (2014–2020) drove UKB's 8.1%
  imaging share and is the field-defining benchmark. AoU does not need to
  match that scale at launch; *staged* release is the realistic path.
- Caveat (`emerging_themes.md` §2 / "Do not over-index on"): the UKB
  imaging volume reflects a *one-time endowment* — other peer cohorts sit
  at 1–2%. AoU's target is not "match UKB" but "stop being below 1%."

**Need area.** This recommendation falls under the imaging need area, which
brings together the data-release question with research-demand
prioritization. It should be coordinated with the Refresh need area's FA4 /
new-9th-area framing.

**Rubric scores.**

| Criterion | Score | Justification |
|---|---:|---|
| Unmet researcher need | 4 | Researchers already linking *external* imaging — clear demand. |
| Simplifies analysis | 3 | Native AoU imaging removes the external-linkage step. |
| Standardizes/harmonizes | 3 | Staged release implies harmonized governance; not a content-standardization per se. |
| Broad use cases | 4 | Imaging cross-cuts cardiometabolic, cancer, ophthalmology, neurology, sleep. |
| Scientific Roadmap alignment | 4 | Slide 7 imaging priority; Refresh-aligned. |
| Tool exists vs new dev | 3 | Imaging-data-release pipelines exist (UKB DNA Nexus, NIH Imaging Data Commons); AoU-specific governance is new. |
| No new data collection | 2 | Tier 1 uses existing waveforms/photos; Tier 2 uses existing EHR DICOM (no new collection); Tier 3 *is* new collection. |
| Helps with data quality | 3 | Native imaging is higher quality than external-linkage indirection. |
| **Mean (applicable only)** | **3.25** | |

**Risks / pushback expected.** Cost — this is the single most expensive WG
recommendation across all 5 WGs. Defend by tier: Tier 1 is engineering;
Tier 2 is governance; Tier 3 is the actual cost-bearing decision. Sci Com
may push to limit to Tier 1–2 in the first cycle.

---

### 2. DICOM + FHIR-ImagingStudy standards adoption; radiomics-to-phecode crosswalk

**Description.** Commit to industry-standard imaging interoperability:
DICOM for primary storage, FHIR ImagingStudy + Observation resources for
metadata, and a *radiomics-to-phecode crosswalk* so that AoU-derived
image-based features can be queried alongside the existing phecode
phenotype layer Smoller's subgroup already prioritized (phecodes scored
3.80 in the Nov 2024 rubric). Builds on the established phecode
infrastructure rather than competing with it.

**Supporting evidence.**
- The Smoller subgroup's 3.80 phecode score and 3.40 NLP/CLAMP score
  establish phecode infrastructure as the analytic spine. Anchoring
  imaging features to that spine is the highest-leverage standards
  decision.
- NLM Goal 1 + NLM-STANDARDS (data standards / terminologies) directly
  aligns; NLM is mission-explicit on AoU.
- NIBIB Goal 4 (biomedical imaging) + NCI Cancer Plan G7 (Maximize Data
  Utility).
- DICOM is the *only* viable imaging standard; FHIR ImagingStudy is the
  HL7-blessed bridge between DICOM stores and the EHR data already in
  AoU. No standards-selection ambiguity here — this is execution.
- Radiomics-to-phecode crosswalk uses existing PyRadiomics / MONAI
  feature definitions; the crosswalk itself is the new work.

**Need area.** Imaging-specific standards fall under the imaging need area;
the phecode crosswalk sits here too because imaging is the new modality
joining the existing phecode infrastructure, not the other way around.

**Rubric scores.**

| Criterion | Score | Justification |
|---|---:|---|
| Unmet researcher need | 3 | DICOM/FHIR is researcher-expected default; crosswalk is researcher-requested. |
| Simplifies analysis | 4 | The whole point — make imaging queryable alongside phecodes. |
| Standardizes/harmonizes | 4 | DICOM + FHIR are *the* harmonization decisions. |
| Broad use cases | 4 | Any radiomics-EHR study. |
| Scientific Roadmap alignment | 4 | Aligns with Refresh data-infrastructure priorities. |
| Tool exists vs new dev | 4 | DICOM, FHIR, PyRadiomics, MONAI all exist; crosswalk is configuration. |
| No new data collection | 4 | Depends on whatever the release tier from Recommendation 1 provides. |
| Helps with data quality | 4 | DICOM metadata + FHIR provenance are core QC infrastructure. |
| **Mean (applicable only)** | **3.88** | |

**Risks / pushback expected.** Sci Com may ask "why a *radiomics-to-phecode*
crosswalk rather than a separate imaging-only analytic layer?" — answer:
phecodes are the established analytic vocabulary the AoU researcher base
already uses; new vocabulary fragments the user base. Coordinate with the AI
need area (WG-4).

---

### 3. Pre-launch governance: data-quality + bias-audit framework for imaging release

**Description.** Before the first imaging release, commit to a quality and
bias-audit framework: (a) image-quality metrics published per modality
(SNR, registration accuracy, sample-completeness by ancestry/SDOH stratum);
(b) representation audit against the cohort's UBR oversample design; (c) a
released-with-the-images "bias report card" each researcher consults; (d)
explicit governance for AI-generated derivative datasets (segmentations,
radiomics features) so derivative products inherit the audit.

**Supporting evidence.**
- WG-2's bias-in-translation framework provides the parent — imaging
  inherits the same standard.
- NIMHD G7 + Leap Forward + NHGRI BP4 all converge on representation as
  central; an imaging release without representation audit would
  *underdeliver* the AoU value proposition.
- HA6 (G×E×SDOH integrated) 10 post-2023 pubs anticipate the multimodal
  use case; imaging is the next modality joining.
- NEI G4 (vision-health equity) explicitly calls for disparities-anchored
  ophthalmologic data.

**Need area.** Imaging governance is specific to imaging modalities (DICOM
provenance, segmentation derivative tracking, MR sequence parameters), so
this recommendation falls under the imaging need area, where that technical
context lives.

**Rubric scores.**

| Criterion | Score | Justification |
|---|---:|---|
| Unmet researcher need | 3 | Researchers don't know they need this yet; reviewers will. |
| Simplifies analysis | 2 | Audit adds workflow, doesn't simplify. |
| Standardizes/harmonizes | 4 | Establishes the AoU imaging-bias standard. |
| Broad use cases | 4 | Every imaging-derived product. |
| Scientific Roadmap alignment | 4 | Aligns with FA7 + the bias-in-translation thread. |
| Tool exists vs new dev | 3 | Image-QC tools exist (MRIQC, FSL, others); the bias-audit packaging is new. |
| No new data collection | 4 | Operates on whatever data the release tier provides. |
| Helps with data quality | 4 | Direct improvement of comparative validity. |
| **Mean (applicable only)** | **3.50** | |

**Risks / pushback expected.** Risk of being seen as "premature" — there
isn't an imaging release to audit yet. Defend by framing as *prerequisite
to release, not parallel to release*. Some Sci Com members will want to
focus on getting any imaging out the door first; the WG should hold the
audit as a release-gate, not a release-blocker.

---

## Also-considered (deprioritized with reasoning)

- **AI-radiomics pilot mechanism (candidate 4).** Falls under the AI
  need area (WG-4); coordinate it with the standards foundation in
  Recommendation 2 as the joint platform.
- **UKB / NIH Imaging Data Commons partnership (candidate 6).** Strong
  idea but politically delicate (foreign-use framing guidance — UKB is a
  US-funded-resource-adopted-globally case for AoU; reciprocal data
  *governance* with UKB is not without complication). Surface as
  "cross-cohort validation pathway" within Recommendation 1 Tier 1
  rather than as a separate Top-3 item. **Caveat for the WG lead:**
  this is the area where my evidence base is thinnest — the WG-3 leads
  may have direct contact with UKB-Imaging team members that should
  inform whether to elevate this.

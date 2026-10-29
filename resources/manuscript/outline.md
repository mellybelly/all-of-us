# Manuscript outline — *All of Us* scientific roadmap refresh

**Working title:** "Where a diverse national cohort should go next: a data-driven
refresh of the *All of Us* scientific roadmap"

**Type:** Narrative / data-driven *perspective* (analysis-backed), not a systematic review.
**Audience:** *All of Us* Science Committee, program leadership, NIH, the biobank/informatics community.
**Evidence base:** this repository (corpus of 1,657 AoU publications + 32,922 workspaces (20,165 substantive); full-census peer-biobank comparison; preprint+grant horizon scan; Researcher Workbench capability benchmark). Numbers cited in the manuscript should be pulled from the refreshed deliverables.

**Scope defaults (confirm/adjust):** narrative perspective; gray literature (preprints, vendor/standards/policy docs) allowed and tagged distinctly; author-group anchors (M. Haendel: N3C, Monarch Initiative, OMOP/OHDSI, phenotype ontologies) to be byline-verified. The **outline** is committed to the repo; the citation files (`references-seed.md`, `citations_cluster{A–D}.md`) remain local until reviewed.

---

## §0. Abstract / key points
- The corpus shows where AoU science concentrates and where it is absent.
- AoU's distinctive strengths (diversity, SDOH, ELSI/engagement) vs gaps (multi-omics, imaging, rare disease).
- The field's leading edge (AI/foundation models) is largely unrealized in AoU.
- Ancillary (partnered) studies add new modalities and are the program's leading edge — visible in workspaces a year+ before any publication (e.g. Exploring the Mind: 0 papers, 32 workspaces).
- Platform (Researcher Workbench) gaps constrain reuse, collaboration, and in-environment AI — a conclusion independently corroborated by a 2026 ACT-IAC/AoU AI/ML white paper.
- A refreshed roadmap: a Data/AI/Methods focus area, governed in-environment AI, reusable tooling.

## §1. Introduction — why refresh the roadmap now
1.1 The Precision Medicine Initiative and the founding of *All of Us*; its diversity mandate.
1.2 What a scientific roadmap is for; the 2020 roadmap and its 8 priority focus areas.
1.3 Why a 2026 refresh: corpus maturity, a shifting scientific frontier (AI), peer-cohort competition.
1.4 Contribution: an evidence-driven refresh from the program's own output + the external field.

## §2. The *All of Us* research landscape

### §2.1 Data and methods
A reproducible, five-step Python pipeline (public repository); every figure traces to a script and a data file.
1. **Corpus acquisition.** AoU publications pulled live from the program's publications feed (reconciled to PubMed/iCite) — **1,657 records (1,653 substantive)**; workspace projects pulled **live from the production project-directory API** (32,922 workspaces; **20,165 substantive** after dropping educational/training/stub/duplicate records; live pull 2026-10-14, re-verified 2026-10-21). Full text back-filled from Europe PMC JATS where a PMC id exists.
2. **Theme tagging.** A locked **19-theme taxonomy** applied by keyword rules over **title + abstract** (canonical, year-comparable) and a **full-text-augmented** layer; AoU data are OMOP-standardized. Mean 2.1 themes/pub (abstract) vs 3.4 (full text).
3. **IC attribution.** NIH grant IDs parsed from publication grant strings and resolved to administering + co-funding ICs via **NIH RePORTER**; mapped against **166 priority statements** extracted from **29 NIH strategic plans** → a corpus × IC alignment matrix.
4. **Peer benchmarking.** Four peer biobanks (UK Biobank, FinnGen, MVP, China Kadoorie) pulled by **full-census PubMed name-search** and tagged with the **same tagger** → a static theme-share index (AoU vs peer median).
5. **Horizon scan + platform benchmark + scoring.** Open-discovery **term-acceleration** over **322,138 preprints + 460,285 NIH grants** (2021–26) with LLM topic induction and an AoU data-feasibility overlay; the Researcher Workbench benchmarked against five comparator platforms with **87/87 fetch-verified citations**; candidate recommendations scored on an 8-criterion rubric. **Caveats:** keyword tagging is directional; peer corpora are unaudited (use the static share index, not trend differentials); workspace text is self-described intent; grant/IC coverage ~30%.
2.2 What AoU science is about: theme distribution; the 8 focus areas largely hold.
2.3 Three structural gaps in the framework: a data-science/AI/methods "orphan," wearables, multi-omics.
2.4 Funding attribution (NIH IC landscape) and the pan-NIH infrastructure framing.
2.5 Ancillary (partnered) studies as the leading edge: new modalities on top of the core protocol — Exploring the Mind (objective cognition/behavior, NIMH), Eyes on Health (retinal imaging/oculomics, NEI/NIBIB), Nutrition for Precision Health (individualized diet response, Common Fund), Environmental Health & Exposomics (NIEHS). Several post-date the 2020 roadmap and are only now releasing data, so they are near-absent from the publication record. The methodological point: **workspace activity leads publications by a year or more** — Exploring the Mind has 0 publications/preprints anywhere (verified via Europe PMC) yet 32 workspaces (27 newly visible in the 2026-10-14 live pull), which is why a live workspace census, not a cached snapshot, is essential and why these studies must be scored on goals + workspace intent. (See `aou-roadmap-refresh/ancillary_studies.md`.) Related live program activity: the Multi-Omics Working Group is generating RNA-seq + Olink proteomics + PacBio long-read on ~10,000 diverse participants (scaling toward ~50,000), and the program has publicly posted a mechanism for external (academic/nonprofit/industry) investigators to request biospecimens to generate new data types — both surfaced in the 2026 committee series (see `aou-roadmap-refresh/committee_2026_alignment.md`).

## §3. Benchmarking against peer biobanks
3.1 The comparator set and method (full-census name-search; same-tagger).
3.2 AoU's distinctive identity: SDOH/health equity, ELSI/participant engagement, pharmacogenomics, methods — enabled by its diversity.
3.3 Where AoU trails: the five most under-indexed theme areas vs the peer median — rare disease & Mendelian genetics (0.25×), environmental health (0.35×), genomics methods/complex-trait genetics (0.42×), neurology non-ADRD (0.46×), respiratory & sleep (0.53×) — plus the data-modality gaps in multi-omics and imaging. Distinguish genuine addressable gaps (rare disease, environmental health — the latter already being closed by the Exposomics ancillary study) from by-design peer dominance (FinnGen rare-disease/genetics; CKB neurology). (See `peer-biobanks/underrepresented_vs_peers.md`.)
3.4 Interpretation: distinctiveness vs growth; relative-emphasis vs data-availability vs researcher-base gaps; peer shares inflated by each cohort's recruitment design.

## §4. Emerging scientific frontiers and AoU white space
4.1 Horizon-scan method (preprints + grants; term-acceleration; open topic discovery; feasibility overlay).
4.2 The AI/ML wave: genomic foundation models, LLMs/agentic AI, multimodal modeling.
4.3 Disease-definition and methods shifts (e.g., MASLD; causal inference/target-trial emulation).
4.4 Frontiers outside AoU's data model (single-cell/spatial, protein structure) — partner, don't chase.
4.5 Actionable white space for a diverse cohort.

## §5. The analysis platform: the Researcher Workbench
5.1 Why the platform shapes the science; comparator platforms (N3C, Terra/AnVIL, BioData Catalyst, UKB-RAP, Kids First).
5.2 Capability/data-asset gaps: reusable tool/workflow registry; portable workflows/standards.
5.3 Governed in-environment AI: the BAA/egress reality and the in-VPC path.
5.4 Reuse and collaboration signals on the 32,922-workspace census (87.7% solo, 3.2% multi-institution, ~18% tutorial clones) — and what they imply for a reuse economy.
5.5 Convergent external evidence: an unreleased 2026 ACT-IAC/AoU draft white paper (*Advancing AI/ML for the NIH All of Us Research Program*), built from stakeholder interviews, independently recommends the same enablers — a governed in-environment AI research assistant with agent-ready (MCP) metadata services, a reusable-research-asset registry with graduated tool certification, portable workflows, and a hybrid/federated compute model. Qualitative triangulation of this paper's quantitative gap analysis. (Confidential draft — cited, not quoted.)

## §6. Recommendations for the refreshed roadmap
6.1 Add a "Data, AI & Methods" focus area.
6.2 Multi-omics/proteomics release roadmap; name it in the framework.
6.3 Governed in-environment AI co-scientist + reusable-tools registry + multimodal templates — and an **internal All of Us foundation model hosted securely with no data egress**, guided by a program **"super user group"** (2026 committee idea); this unifies the genomic-foundation-model white-space (§4.2) with the governed-in-environment-AI gap (§5.3).
6.4 Protect distinctive strengths (diversity, SDOH, ELSI); coordinate across recognized need areas.
6.5 Measurement: track the roadmap with the same corpus methods over time.
6.6 Adopt the **driver-project / driver-paper model** (from the 2026 committee's Women's Health Driver Project) as a standing mechanism — program biostatistical support producing exemplar analyses — and make **rare-disease and intersectional (equity × rare-disease × geography, e.g. rare disease + rurality) driver papers** an explicit near-term deliverable that attacks the rare-disease peer-gap using AoU's diversity.
6.7 Make **generalizability weighting a first-class Workbench capability** (promote the `waou`-style survey-weighting toolkit to a documented, reusable research asset), and connect the program's **publicly posted external-biospecimen-request mechanism** to a graduated partner-contribution / reusable-asset model.

## §7. Limitations
Keyword tagging; workspace snapshot recency; name-search peer corpora; grant/IC coverage; platform specifics from vendor docs. Generalizability: AoU is a volunteer cohort, so prevalence/association estimates require weighting to the US population — cite the 2026 generalizability Driver Project and the `waou` survey-weighting package (*Am J Epidemiology* 2026; verify before use) as both a caveat and an available remedy.

## §8. Conclusion
A diverse national cohort's next chapter: lead on AI-ready, equity-anchored, reusable science.

---

## Citation plan (clusters → parallel verified harvesting)
- **Cluster A** — §1–§2: AoU program, precision medicine, diversity, OMOP/phenome-wide, corpus/bibliometric methods. Ancillary studies (§2.5) cite the NIH *Partnered Research Studies* page + each study's program source (e.g. NPH on clinicaltrials.gov).
- **Cluster B** — §3: UK Biobank, FinnGen, MVP, China Kadoorie; biobank/cohort comparison & bibliometrics.
- **Cluster C** — §4: AI/foundation models, LLMs in medicine, genomic FMs, multimodal, MASLD, spatial/single-cell, causal inference/target-trial emulation.
- **Cluster D** — §5–§6: secure-analysis platforms (Terra/AnVIL, N3C, BioData Catalyst, Kids First, Researcher Workbench), GA4GH/Dockstore/FAIR, governed clinical AI/compute-to-data; author-group anchors (Haendel). The 2026 ACT-IAC/AoU AI/ML white paper (§5.5) is cited as an unreleased draft, distinctly tagged.

**Harvest status (2026-10-21):** committee-sourced + frontier citations harvested and verified — the generalizability paper (*Am J Epi* 2026) + `waou` (CRAN) and the women's-health driver paper (*J Women's Health* 2026) are confirmed published and added to Cluster D; 15 verified frontier-method citations added to Cluster C. The multi-omics "10,000 diverse individuals" preprint could not be verified and was omitted (the program activity is still described, uncited). Spot-check every DOI/PMID on import.

**Preprints as citations.** Preprints (bioRxiv/medRxiv/arXiv) are permitted throughout — especially in Cluster C, where the fastest-moving AI/ML work is preprint-first — and must be **tagged distinctly** (e.g. `[preprint]`) with their DOI/server ID, flagged for published-version replacement before submission. The same anti-fabrication rule applies: include only preprints verified to resolve to the exact record.

# Manuscript outline - *All of Us* scientific roadmap refresh

**Working title:** "Where a diverse national cohort should go next: a data-driven
refresh of the *All of Us* scientific roadmap"

**Type:** Narrative / data-driven *perspective* (analysis-backed), not a systematic review.
**Audience:** *All of Us* Science Committee, program leadership, NIH, the biobank/informatics community.
**Evidence base:** this repository (corpus of 1,657 AoU publications + 32,922 workspaces (20,165 substantive); full-census peer-biobank comparison; preprint+grant horizon scan; Researcher Workbench capability benchmark). Numbers cited in the manuscript should be pulled from the refreshed deliverables.

**Scope defaults (confirm/adjust):** narrative perspective; gray literature (preprints, vendor/standards/policy docs) allowed and tagged distinctly; author-group anchors (M. Haendel: N3C, Monarch Initiative, OMOP/OHDSI, phenotype ontologies) to be byline-verified.

**Citations:** key verified citations are embedded inline per section below (as **Key citations:** lines with DOI links); the full verified reference list with DOIs follows in the References section at the end of this document. Spot-check every DOI on import.

---

## 0. Abstract / key points
- The corpus shows where AoU science concentrates and where it is absent.
- AoU's distinctive strengths (diversity, SDOH, ELSI/engagement) vs gaps (multi-omics, imaging, rare disease).
- The field's leading edge (AI/foundation models) is largely unrealized in AoU.
- Ancillary (partnered) studies add new modalities and are the program's leading edge - visible in workspaces a year+ before any publication (e.g. Exploring the Mind: 0 papers, 32 workspaces).
- Platform (Researcher Workbench) gaps constrain reuse, collaboration, and in-environment AI - a conclusion independently corroborated by a 2026 ACT-IAC/AoU AI/ML white paper.
- A refreshed roadmap: a Data/AI/Methods focus area, governed in-environment AI, reusable tooling.

## 1. Introduction - why refresh the roadmap now
1.1 The Precision Medicine Initiative and the founding of *All of Us*; its diversity mandate.
1.2 What a scientific roadmap is for; the 2020 roadmap and its 8 priority focus areas.
1.3 Why a 2026 refresh: corpus maturity, a shifting scientific frontier (AI), peer-cohort competition.
1.4 Contribution: an evidence-driven refresh from the program's own output + the external field.

**Key citations:** [Collins & Varmus, NEJM 2015](https://doi.org/10.1056/NEJMp1500523); [PMI Working Group report, NIH 2015](https://www.nih.gov/sites/default/files/research-training/initiatives/pmi/09172015-pmi-working-group-report.pdf); [All of Us Program, NEJM 2019](https://doi.org/10.1056/NEJMsr1809937); [Mapes et al., PLoS ONE 2020](https://doi.org/10.1371/journal.pone.0234962); [Denny & Collins, Cell 2021](https://doi.org/10.1016/j.cell.2021.01.015).

## 2. The *All of Us* research landscape

### 2.1 Data and methods
A reproducible, five-step Python pipeline (public repository); every figure traces to a script and a data file.
1. **Corpus acquisition.** AoU publications pulled live from the program's publications feed (reconciled to PubMed/iCite) - **1,657 records (1,653 substantive)**; workspace projects pulled **live from the production project-directory API** (32,922 workspaces; **20,165 substantive** after dropping educational/training/stub/duplicate records; live pull 2026-10-14, re-verified 2026-10-21). Full text back-filled from Europe PMC JATS where a PMC id exists.
2. **Theme tagging.** A locked **19-theme taxonomy** applied by keyword rules over **title + abstract** (canonical, year-comparable) and a **full-text-augmented** layer; AoU data are OMOP-standardized. Mean 2.1 themes/pub (abstract) vs 3.4 (full text).
3. **IC attribution.** NIH grant IDs parsed from publication grant strings and resolved to administering + co-funding ICs via **NIH RePORTER**; mapped against **166 priority statements** extracted from **29 NIH strategic plans** → a corpus × IC alignment matrix.
4. **Peer benchmarking.** Four peer biobanks (UK Biobank, FinnGen, MVP, China Kadoorie) pulled by **full-census PubMed name-search** and tagged with the **same tagger** → a static theme-share index (AoU vs peer median).
5. **Horizon scan + platform benchmark + scoring.** Open-discovery **term-acceleration** over **322,138 preprints + 460,285 NIH grants** (2021–26) with LLM topic induction and an AoU data-feasibility overlay; the Researcher Workbench benchmarked against five comparator platforms with **87/87 fetch-verified citations**; candidate recommendations scored on an 8-criterion rubric. **Caveats:** keyword tagging is directional; peer corpora are unaudited (use the static share index, not trend differentials); workspace text is self-described intent; grant/IC coverage ~30%.
2.2 What AoU science is about: theme distribution; the 8 focus areas largely hold.
2.3 Three structural gaps in the framework: a data-science/AI/methods "orphan," wearables, multi-omics.
2.4 Funding attribution (NIH IC landscape) and the pan-NIH infrastructure framing.
2.5 Ancillary (partnered) studies as the leading edge: new modalities on top of the core protocol - Exploring the Mind (objective cognition/behavior, NIMH), Eyes on Health (retinal imaging/oculomics, NEI/NIBIB), Nutrition for Precision Health (individualized diet response, Common Fund), Environmental Health & Exposomics (NIEHS). Several post-date the 2020 roadmap and are only now releasing data, so they are near-absent from the publication record. The methodological point: **workspace activity leads publications by a year or more** - Exploring the Mind has 0 publications/preprints anywhere (verified via Europe PMC) yet 32 workspaces (27 newly visible in the 2026-10-14 live pull), which is why a live workspace census, not a cached snapshot, is essential and why these studies must be scored on goals + workspace intent. Related live program activity: the Multi-Omics Working Group is generating RNA-seq + Olink proteomics + PacBio long-read on ~10,000 diverse participants (scaling toward ~50,000), and the program has publicly posted a mechanism for external (academic/nonprofit/industry) investigators to request biospecimens to generate new data types - both surfaced in the 2026 committee series.

**Key citations:** [All of Us Genomic Data, Nature 2024](https://doi.org/10.1038/s41586-023-06957-x); [Ramirez et al., Patterns 2022](https://doi.org/10.1016/j.patter.2022.100570); [Lederer et al. (Fitbit), JMIR 2023](https://doi.org/10.2196/45103); [Overhage et al. (OMOP CDM), JAMIA 2012](https://doi.org/10.1136/amiajnl-2011-000376); [Denny et al. (PheWAS), Bioinformatics 2010](https://doi.org/10.1093/bioinformatics/btq126). Ancillary studies: [NIH Partnered Research Studies](https://www.nih.gov/allofus/funding/partnered-research-studies); [Cohn et al. (Women's Health Driver Project), J Women's Health 2026](https://doi.org/10.1177/15409996261434111).

## 3. Benchmarking against peer biobanks
3.1 The comparator set and method (full-census name-search; same-tagger).
3.2 AoU's distinctive identity: SDOH/health equity, ELSI/participant engagement, pharmacogenomics, methods - enabled by its diversity.
3.3 Where AoU trails: the five most under-indexed theme areas vs the peer median - rare disease & Mendelian genetics (0.25×), environmental health (0.35×), genomics methods/complex-trait genetics (0.42×), neurology non-ADRD (0.46×), respiratory & sleep (0.53×) - plus the data-modality gaps in multi-omics and imaging. Distinguish genuine addressable gaps (rare disease, environmental health - the latter already being closed by the Exposomics ancillary study) from by-design peer dominance (FinnGen rare-disease/genetics; CKB neurology).
3.4 Interpretation: distinctiveness vs growth; relative-emphasis vs data-availability vs researcher-base gaps; peer shares inflated by each cohort's recruitment design.

**Key citations:** [Sudlow et al. (UK Biobank), PLoS Med 2015](https://doi.org/10.1371/journal.pmed.1001779); [Gaziano et al. (MVP), J Clin Epidemiol 2016](https://doi.org/10.1016/j.jclinepi.2015.09.016); [Kurki et al. (FinnGen), Nature 2023](https://doi.org/10.1038/s41586-022-05473-8); [Chen et al. (China Kadoorie), Int J Epidemiol 2011](https://doi.org/10.1093/ije/dyr120); [Sirugo et al. (missing diversity), Cell 2019](https://doi.org/10.1016/j.cell.2019.02.048); [Martin et al. (PRS equity), Nat Genet 2019](https://doi.org/10.1038/s41588-019-0379-x); [Fry et al. (representativeness), Am J Epidemiol 2017](https://doi.org/10.1093/aje/kwx246).

## 4. Emerging scientific frontiers and AoU white space
4.1 Horizon-scan method (preprints + grants; term-acceleration; open topic discovery; feasibility overlay).
4.2 The AI/ML wave: genomic foundation models, LLMs/agentic AI, multimodal modeling.
4.3 Disease-definition and methods shifts (e.g., MASLD; causal inference/target-trial emulation).
4.4 Frontiers outside AoU's data model (single-cell/spatial, protein structure) - partner, don't chase.
4.5 Actionable white space for a diverse cohort.

**Key citations:** [Moor et al. (generalist medical AI), Nature 2023](https://doi.org/10.1038/s41586-023-05881-4); [Singhal et al. (Med-PaLM), Nature 2023](https://doi.org/10.1038/s41586-023-06291-2); [Dalla-Torre et al. (Nucleotide Transformer), Nat Methods 2025](https://doi.org/10.1038/s41592-024-02523-z); [Nguyen et al. (Evo), Science 2024](https://doi.org/10.1126/science.ado9336); [Acosta et al. (multimodal biomedical AI), Nat Med 2022](https://doi.org/10.1038/s41591-022-01981-2); [Rinella et al. (MASLD nomenclature), Hepatology 2023](https://doi.org/10.1097/HEP.0000000000000520); [Hernán & Robins (target-trial emulation), Am J Epidemiol 2016](https://doi.org/10.1093/aje/kwv254); [Jumper et al. (AlphaFold), Nature 2021](https://doi.org/10.1038/s41586-021-03819-2).

## 5. The analysis platform: the Researcher Workbench
5.1 Why the platform shapes the science; comparator platforms (N3C, Terra/AnVIL, BioData Catalyst, UKB-RAP, Kids First).
5.2 Capability/data-asset gaps: reusable tool/workflow registry; portable workflows/standards.
5.3 Governed in-environment AI: the BAA/egress reality and the in-VPC path.
5.4 Reuse and collaboration signals on the 32,922-workspace census (87.7% solo, 3.2% multi-institution, ~18% tutorial clones) - and what they imply for a reuse economy.
5.5 Convergent external evidence: an unreleased 2026 ACT-IAC/AoU draft white paper (*Advancing AI/ML for the NIH All of Us Research Program*), built from stakeholder interviews, independently recommends the same enablers - a governed in-environment AI research assistant with agent-ready (MCP) metadata services, a reusable-research-asset registry with graduated tool certification, portable workflows, and a hybrid/federated compute model. Qualitative triangulation of this paper's quantitative gap analysis. (Confidential draft - cited, not quoted.)

**Key citations:** [Haendel et al. (N3C), JAMIA 2021](https://doi.org/10.1093/jamia/ocaa196); [Schatz et al. (AnVIL), Cell Genomics 2022](https://doi.org/10.1016/j.xgen.2021.100085); [Ahalt et al. (BioData Catalyst), JAMIA 2023](https://doi.org/10.1093/jamia/ocad048); [O'Connor et al. (Dockstore), F1000Research 2017](https://doi.org/10.12688/f1000research.10137.1); [Wilkinson et al. (FAIR), Sci Data 2016](https://doi.org/10.1038/sdata.2016.18); [Rehm et al. (GA4GH), Cell Genomics 2021](https://doi.org/10.1016/j.xgen.2021.100029).

## 6. Recommendations for the refreshed roadmap
6.1 Add a "Data, AI & Methods" focus area.
6.2 Multi-omics/proteomics release roadmap; name it in the framework.
6.3 Governed in-environment AI co-scientist + reusable-tools registry + multimodal templates - and an **internal All of Us foundation model hosted securely with no data egress**, guided by a program **"super user group"** (2026 committee idea); this unifies the genomic-foundation-model white-space with the governed-in-environment-AI gap.
6.4 Protect distinctive strengths (diversity, SDOH, ELSI); coordinate across recognized need areas.
6.5 Measurement: track the roadmap with the same corpus methods over time.
6.6 Adopt the **driver-project / driver-paper model** (from the 2026 committee's Women's Health Driver Project) as a standing mechanism - program biostatistical support producing exemplar analyses - and make **rare-disease and intersectional (equity × rare-disease × geography, e.g. rare disease + rurality) driver papers** an explicit near-term deliverable that attacks the rare-disease peer-gap using AoU's diversity.
6.7 Make **generalizability weighting a first-class Workbench capability** (promote the `waou`-style survey-weighting toolkit to a documented, reusable research asset), and connect the program's **publicly posted external-biospecimen-request mechanism** to a graduated partner-contribution / reusable-asset model.

**Key citations:** [Obermeyer et al. (algorithmic bias), Science 2019](https://doi.org/10.1126/science.aax2342); [Wiens et al. (responsible ML), Nat Med 2019](https://doi.org/10.1038/s41591-019-0548-6); [Rajkomar et al. (fairness), Ann Intern Med 2018](https://doi.org/10.7326/M18-1990); [Char et al. (ethical ML), NEJM 2018](https://doi.org/10.1056/NEJMp1714229); [Montgomery et al. (generalizability), Am J Epidemiol 2026](https://doi.org/10.1093/aje/kwag010) + [waou (CRAN)](https://CRAN.R-project.org/package=waou); [Cohn et al. (driver-paper model), J Women's Health 2026](https://doi.org/10.1177/15409996261434111).

## 7. Limitations
Keyword tagging; workspace snapshot recency; name-search peer corpora; grant/IC coverage; platform specifics from vendor docs. Generalizability: AoU is a volunteer cohort, so prevalence/association estimates require weighting to the US population - cite the 2026 generalizability Driver Project and the `waou` survey-weighting package (*Am J Epidemiology* 2026; verify before use) as both a caveat and an available remedy.

## 8. Conclusion
A diverse national cohort's next chapter: lead on AI-ready, equity-anchored, reusable science.

---

## Citation plan (clusters → parallel verified harvesting)
- **Cluster A** (Introduction & research landscape): AoU program, precision medicine, diversity, OMOP/phenome-wide, corpus/bibliometric methods. Ancillary studies cite the NIH *Partnered Research Studies* page + each study's program source (e.g. NPH on clinicaltrials.gov).
- **Cluster B** (Peer biobanks): UK Biobank, FinnGen, MVP, China Kadoorie; biobank/cohort comparison & bibliometrics.
- **Cluster C** (Emerging frontiers): AI/foundation models, LLMs in medicine, genomic FMs, multimodal, MASLD, spatial/single-cell, causal inference/target-trial emulation.
- **Cluster D** (Platform & recommendations): secure-analysis platforms (Terra/AnVIL, N3C, BioData Catalyst, Kids First, Researcher Workbench), GA4GH/Dockstore/FAIR, governed clinical AI/compute-to-data; author-group anchors (Haendel). The 2026 ACT-IAC/AoU AI/ML white paper is cited as an unreleased draft, distinctly tagged.

**Harvest status (2026-10-21):** committee-sourced + frontier citations harvested and verified - the generalizability paper (*Am J Epi* 2026) + `waou` (CRAN) and the women's-health driver paper (*J Women's Health* 2026) are confirmed published and added to Cluster D; 15 verified frontier-method citations added to Cluster C. The multi-omics "10,000 diverse individuals" preprint could not be verified and was omitted (the program activity is still described, uncited). Spot-check every DOI/PMID on import.

**Preprints as citations.** Preprints (bioRxiv/medRxiv/arXiv) are permitted throughout - especially in Cluster C, where the fastest-moving AI/ML work is preprint-first - and must be **tagged distinctly** (e.g. `[preprint]`) with their DOI/server ID, flagged for published-version replacement before submission. The same anti-fabrication rule applies: include only preprints verified to resolve to the exact record.

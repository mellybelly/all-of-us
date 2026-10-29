# Where a diverse national cohort should go next: a data-driven refresh of the *All of Us* scientific roadmap

*Annotated outline: each section states what it covers (with the key findings) and why it belongs. A data-driven perspective for the All of Us Science Committee, program leadership, NIH, and the biobank and informatics community. Data current as of 2026-10-21. Verified citations are listed per section and consolidated in the References section at the end.*

---

## Key takeaways

1. The eight focus areas still hold, but three fast-growing bodies of work have no home in the framework (data science and AI methods ~18% of output, wearables, multi-omics). Propose a ninth focus area, "Data, AI & Methods."
2. All of Us has a distinctive identity worth protecting: it leads peers on health equity and social determinants (about 5.4x the peer median), ethics and engagement (about 24x), pharmacogenomics (about 4.3x), and methods (about 2.8x), all driven by its diversity.
3. All of Us trails peers in five areas the committee flagged: imaging, multi-omics, aging research, rare disease (most under-indexed, about 0.25x the peer median), and environmental and social data (some addressable now, some by-design).
4. The field's leading edge is AI and foundation models; All of Us is almost absent (under ~0.3% of its work on most AI topics) yet uniquely positioned to lead. Highest-leverage opportunity.
5. The Researcher Workbench leads on data and compute but lacks a reusable-tools registry, a governed in-environment AI assistant, and portable workflows; the workspace census shows 87.7% solo, 3.2% multi-institution, ~18% tutorial clones. Independently corroborated by a 2026 ACT-IAC/AoU white paper.
6. Ancillary studies are the leading edge the publication record cannot yet show (Exploring the Mind: 0 papers, 32 workspaces, 27 visible only in the live pull), so score them on goals and live workspace signal and analyze a live census, not a cached snapshot.

## Abstract

**Covers.** A single paragraph: the program's diversity-first thesis; what was analyzed (1,657 publications and 20,165 substantive workspaces, four peer biobanks, a 322k-preprint/460k-grant horizon scan, and a Workbench capability review); the core findings in brief; and the forward vision for All of Us as the national substrate for equity-anchored, AI-ready science.
**Why.** Gives the reader the whole argument, and the one-sentence thesis ("All of Us scaled up everything around genomics that genomics needs to work in practice"), before any detail.

## 1. Introduction: why refresh the roadmap now

**Covers.**
- The Precision Medicine Initiative origin and the diversity mandate that distinguishes All of Us from prior biobanks; diversity is the scientific thesis, not a side constraint.
- What a roadmap is for, and the 2020 roadmap's eight priority focus areas.
- The three forces that justify a 2026 refresh: corpus maturity (enough output to analyze what the community actually does), the shift of the frontier toward AI and foundation models, and intensifying peer-cohort competition.
- The contribution: an evidence-driven refresh built from the program's own output and the external field.

**Why.** Frames the refresh as earned by evidence and anchored in the program's founding purpose.
**Key citations:** [Collins & Varmus, NEJM 2015](https://doi.org/10.1056/NEJMp1500523); [PMI Working Group report, NIH 2015](https://www.nih.gov/sites/default/files/research-training/initiatives/pmi/09172015-pmi-working-group-report.pdf); [All of Us Program, NEJM 2019](https://doi.org/10.1056/NEJMsr1809937); [Mapes et al. (diversity/UBR), PLoS ONE 2020](https://doi.org/10.1371/journal.pone.0234962); [Denny & Collins, Cell 2021](https://doi.org/10.1016/j.cell.2021.01.015); [All of Us year in review 2023-2024, Am J Hum Genet 2024](https://doi.org/10.1016/j.ajhg.2024.07.023).
**Co-lead anchors (J. W. Smoller, psychiatric genomics and EHR phenotyping):** [Cross-disorder psychiatric GWAS, Lancet 2013](https://doi.org/10.1016/S0140-6736%2812%2962129-1); [EHR for psychiatric phenotyping and genomics, Am J Med Genet B 2018](https://doi.org/10.1002/ajmg.b.32548); [Schizophrenia PRS penetrance and PheWAS across four health systems, Am J Psychiatry 2019](https://doi.org/10.1176/appi.ajp.2019.18091085); [EHR automated phenotyping validated by genetics, Transl Psychiatry 2018](https://doi.org/10.1038/s41398-018-0133-7); [Mass General Brigham Biobank precision health, Nat Commun 2025](https://doi.org/10.1038/s41467-025-66598-8); [14-disorder psychiatric genomics, Nature 2026](https://doi.org/10.1038/s41586-025-09820-3).

## 2. How we did this analysis (methods)

**Covers.** A reproducible five-step pipeline (public repository) run over the program's own output and the external literature; each step answers one question:

| Step | What we did | What it answers |
| --- | --- | --- |
| 1. Inventory the corpus | Pulled publications (feed reconciled to PubMed/iCite) and workspaces (live production project-directory API). | What has All of Us produced? |
| 2. Tag by theme | Locked 19-theme taxonomy over title + abstract, plus a full-text layer where open access exists. | What is the science about? |
| 3. Map to NIH and attribute funding | Matched to 29 strategic plans (166 priorities); resolved grant IDs to Institutes via RePORTER. | Which NIH priorities and ICs does it serve? |
| 4. Compare to peer biobanks | Full-census name-search of UKB/FinnGen/MVP/CKB, same tagger, static theme-share index. | How does All of Us differ? |
| 5. Scan the frontier + benchmark the platform | Term-acceleration over 322,138 preprints + 460,285 grants; Workbench vs 5 platforms (87/87 verified); rubric scoring. | What is rising that AoU has not claimed, and what to build? |

- **The numbers:** 1,657 publications (1,653 substantive); 32,922 workspaces (20,165 substantive) from a live 2026-10-14 pull, re-verified unchanged 2026-10-21; peers UKB 12,986, FinnGen 3,376, MVP 501, CKB 588.
- **Three cautions:** peer comparisons are relative-emphasis, not head-to-head (unaudited name-search corpora, so read the share index not trend differentials); workspace text is self-described intent, not executed code; keyword tagging is directional but order-of-magnitude robust.

**Why.** The method is what makes every downstream claim defensible, and the same pipeline can re-measure the roadmap over time.
**Key citations:** [Overhage et al. (OMOP CDM), JAMIA 2012](https://doi.org/10.1136/amiajnl-2011-000376); [Denny et al. (PheWAS), Bioinformatics 2010](https://doi.org/10.1093/bioinformatics/btq126).

## 3. The All of Us research landscape

**Covers.**
- The theme distribution maps cleanly onto the eight focus areas, which largely still fit (the framework is not broken).
- Three bodies of work have outgrown the framework: data science and AI methods (~18% of publications) with no focus area of their own; wearable and remote-monitoring research; and multi-omics, currently buried inside "Genetics & Biology" as proteomics and metabolomics arrive at scale.
- Funding is overwhelmingly Office-of-the-Director (by design), with strong secondary alignment to the genomics, heart/lung, and cancer Institutes, supporting a pan-NIH infrastructure framing.
- Ancillary (partnered) studies are the leading edge: Exploring the Mind (objective cognition/behavior, NIMH), Eyes on Health (retinal imaging/oculomics, NEI/NIBIB), Nutrition for Precision Health (diet response, Common Fund), Environmental Health and Exposomics (NIEHS). Exploring the Mind has zero publications or preprints anywhere yet appears in 32 workspaces (27 visible only in the live pull); cognition/mental-health work is ~13% of all workspaces. Live multi-omics on ~10,000 participants and a new external-biospecimen mechanism are also visible only in the live signal.

**Why.** Shows what the program actually produces, where the framework strains, and why a live workspace census (not a cached snapshot) is essential to see the newest science before it reaches publication.
**Key citations:** [All of Us Genomic Data, Nature 2024](https://doi.org/10.1038/s41586-023-06957-x); [Ramirez et al. (data quality/Workbench), Patterns 2022](https://doi.org/10.1016/j.patter.2022.100570); [Cronin et al. (initial surveys), Epidemiology 2019](https://doi.org/10.1097/EDE.0000000000001028); [Tesfaye et al. (social determinants of health), Sci Rep 2024](https://doi.org/10.1038/s41598-024-57410-6); [Lederer et al. (Fitbit QC), JMIR 2023](https://doi.org/10.2196/45103); [Zheng et al. (wearable sleep and chronic disease at scale), Nat Med 2024](https://doi.org/10.1038/s41591-024-03155-8); [Khajouei et al. (APOE phenome-wide association), EBioMedicine 2025](https://doi.org/10.1016/j.ebiom.2025.105768); [NIH Partnered Research Studies](https://www.nih.gov/allofus/funding/partnered-research-studies); [Cohn et al. (Women's Health Driver Project), J Women's Health 2026](https://doi.org/10.1177/15409996261434111).

## 4. Benchmarking against peer biobanks

**Covers.**
- The comparator set (UK Biobank, FinnGen, Million Veteran Program, China Kadoorie) and method (same tagger, full census, static theme-share index).
- Distinctive strengths: All of Us leads the peer median on social-determinants/health-equity research (~5.4x), ethics and participant engagement (~24x), pharmacogenomics (~4.3x), and analytic methods (~2.8x), all enabled by its diversity.
- The five areas where it trails: imaging and multi-omics (data-modality gaps), aging research, rare disease (most under-indexed at ~0.25x the peer median), and environmental/social data.
- The key distinction: addressable gaps already being closed (rare disease via long-read sequencing; environmental via the November 2, 2026 release and the Exposomics study) versus by-design peer emphasis (FinnGen's founder-population rare-disease/genetics focus; China Kadoorie's stroke/neurology focus) that should not be chased.
- The equity argument: representativeness is itself a scientific asset, since polygenic scores and many genetic findings are far less accurate outside European-ancestry populations.

**Why.** Calibrates the program against comparable cohorts and argues that distinctiveness, not raw publication growth, is the durable signal, while taking the genuine gaps seriously.
**Key citations:** [Sudlow et al. (UK Biobank), PLoS Med 2015](https://doi.org/10.1371/journal.pmed.1001779); [Gaziano et al. (MVP), J Clin Epidemiol 2016](https://doi.org/10.1016/j.jclinepi.2015.09.016); [Kurki et al. (FinnGen), Nature 2023](https://doi.org/10.1038/s41586-022-05473-8); [Chen et al. (China Kadoorie), Int J Epidemiol 2011](https://doi.org/10.1093/ije/dyr120); [Sirugo et al. (missing diversity), Cell 2019](https://doi.org/10.1016/j.cell.2019.02.048); [Martin et al. (PRS & equity), Nat Genet 2019](https://doi.org/10.1038/s41588-019-0379-x); [Fry et al. (representativeness), Am J Epidemiol 2017](https://doi.org/10.1093/aje/kwx246).

## 5. Emerging scientific frontiers and All of Us white space

**Covers.**
- The horizon-scan method (term-acceleration over preprints and grants, open topic discovery, then an AoU data-feasibility overlay).
- The result: AI and foundation models are the fastest-rising frontier (genomic/DNA language models, LLMs and agentic AI, multimodal modeling), and All of Us is under ~0.3% on nearly all of them.
- The feasibility-filtered opportunities: genomic foundation models as the single highest-leverage gap (AoU's diverse WGS + EHR is the best public training/evaluation substrate), in-environment LLM and agentic workflows, MASLD as a cheap, high-credibility EHR phenotype, and target-trial emulation on longitudinal records.
- The boundary: single-cell/spatial tissue omics and AI protein-structure prediction need assays AoU does not generate, so AoU should be the population-scale partner, not try to reproduce them.

**Why.** Separates what is merely trendy from what All of Us can uniquely act on, and names the single highest-leverage opportunity.
**Key citations:** [Moor et al. (generalist medical AI), Nature 2023](https://doi.org/10.1038/s41586-023-05881-4); [Singhal et al. (Med-PaLM), Nature 2023](https://doi.org/10.1038/s41586-023-06291-2); [Dalla-Torre et al. (Nucleotide Transformer), Nat Methods 2025](https://doi.org/10.1038/s41592-024-02523-z); [Nguyen et al. (Evo), Science 2024](https://doi.org/10.1126/science.ado9336); [Acosta et al. (multimodal biomedical AI), Nat Med 2022](https://doi.org/10.1038/s41591-022-01981-2); [Rinella et al. (MASLD), Hepatology 2023](https://doi.org/10.1097/HEP.0000000000000520); [Hernán & Robins (target-trial emulation), Am J Epidemiol 2016](https://doi.org/10.1093/aje/kwv254); [Jumper et al. (AlphaFold), Nature 2021](https://doi.org/10.1038/s41586-021-03819-2).

## 6. The analysis platform: the Researcher Workbench

**Covers.**
- Why the platform shapes the science, and the comparator benchmark (N3C, Terra/AnVIL, BioData Catalyst, UKB-RAP, Kids First), where the Workbench leads on data assets and AI-grade compute.
- The three remediable gaps: no shared tool/workflow reuse registry (every comparator has one); no governed in-environment AI assistant (only bring-your-own-key tools today, unusable on participant data); and no portable, interoperable workflow standard.
- The open path: because All of Us runs on Google Cloud, whose BAA already covers Vertex AI/Gemini, a governed in-VPC model is a provisioning and governance task, not a legal blocker.
- The reuse signal from the workspace census: 87.7% solo, 3.2% multi-institution, ~18% duplicate-titled (mostly tutorial clones), so the pattern is copy-a-tutorial, not build-on-each-other.
- Independent corroboration: a confidential 2026 ACT-IAC/AoU white paper built from stakeholder interviews reaches the same three conclusions by a completely different method.

**Why.** Science is bounded by the platform; the gaps that matter are not data or compute but the capabilities that turn them into shared, reusable, AI-enabled science.
**Key citations:** [Haendel et al. (N3C), JAMIA 2021](https://doi.org/10.1093/jamia/ocaa196); [Schatz et al. (AnVIL), Cell Genomics 2022](https://doi.org/10.1016/j.xgen.2021.100085); [Ahalt et al. (BioData Catalyst), JAMIA 2023](https://doi.org/10.1093/jamia/ocad048); [O'Connor et al. (Dockstore), F1000Research 2017](https://doi.org/10.12688/f1000research.10137.1); [Wilkinson et al. (FAIR), Sci Data 2016](https://doi.org/10.1038/sdata.2016.18); [Rehm et al. (GA4GH), Cell Genomics 2021](https://doi.org/10.1016/j.xgen.2021.100029).

## 7. Recommendations for the refreshed roadmap

### 7a. The focus-area framework: current (2020) and proposed refresh

| # | Current focus area (2020 roadmap) | Proposed in the refresh | Why it needs to change |
| --- | --- | --- | --- |
| 1 | Prevalent Common & Rare Conditions | Keep | The core disease anchor and the largest share of output; still fits. |
| 2 | Maternal & Child Health | Maternal Health | Child-health output is thin in the corpus; sharpen the scope to where the program actually delivers. |
| 3 | Healthy Aging & Resilience | Keep (watch as a peer gap) | Fits the framework, but aging is one of the five areas AoU trails peers on. |
| 4 | Return of Results on Individual & Population Health | Reframe toward return-of-results implementation | Move from concept to implementation as ROR capabilities mature. |
| 5 | Lifestyle, Substance & Behavioral Health | Keep | Fits. |
| 6 | Environment | Environment, with an explicit environmental-exposure-linkage commitment | The single largest demand-supply gap (NIEHS priorities vs about 7 AoU publications); the November 2, 2026 release makes it actionable now. |
| 7 | Health Equity | Keep (and protect) | AoU's distinctive, defining strength; the refresh must safeguard it. |
| 8 | Genetics & Biology | Genetics, Multi-omics & Biology | Multi-omics is currently invisible inside this area; the 2026 proteomic and metabolomic releases need a named home. |
| 9 | (none) | **Data, AI & Methods (NEW)** | About 18% of publications and the entire AI and foundation-model surge have no home in the framework; this is the single most important structural change. |

### 7b. The recommendations

**Covers.**
- **Structural:** add a ninth focus area, "Data, AI & Methods"; rename the genetics area to "Genetics, Multi-omics & Biology" and pair it with a concrete proteomics-release roadmap; reframe Maternal & Child Health, Return of Results, and Environment as in the table above.
- **Platform builds:** a governed in-VPC AI co-scientist, a reusable-tools registry, and multimodal-data templates; most ambitiously, an internal All of Us foundation model hosted securely with no data egress, guided by the proposed "super user group" (this single build unifies the highest-leverage opportunity with the clearest platform gap).
- **Adopt the committee's 2026 directions as standing mechanisms:** the driver-paper model (make rare-disease and intersectional driver papers near-term deliverables), and generalizability weighting as a first-class capability (promote the released survey-weighting toolkit) connected to the external-biospecimen mechanism.
- **Protect and govern:** safeguard the distinctive strengths (diversity, SDOH, ELSI) and govern AI responsibly, since an equity-first cohort cannot deploy models that widen disparities.
- **Measure:** re-run the same corpus methods over time to track where the science actually goes.

**Why.** Translates every finding into a concrete, prioritized action.
**Key citations:** [Obermeyer et al. (algorithmic bias), Science 2019](https://doi.org/10.1126/science.aax2342); [Wiens et al. (responsible ML), Nat Med 2019](https://doi.org/10.1038/s41591-019-0548-6); [Rajkomar et al. (fairness), Ann Intern Med 2018](https://doi.org/10.7326/M18-1990); [Char et al. (ethical ML), NEJM 2018](https://doi.org/10.1056/NEJMp1714229); [Montgomery et al. (generalizability), Am J Epidemiol 2026](https://doi.org/10.1093/aje/kwag010); [waou (CRAN)](https://CRAN.R-project.org/package=waou); [Cohn et al. (driver-paper model), J Women's Health 2026](https://doi.org/10.1177/15409996261434111).

## 8. A vision for the future of All of Us

**Covers.**
- **The history that sets the thesis:** All of Us inverted the biobank model. Where others began with genomes and treated clinical data as terse biospecimen annotations, All of Us built a diverse, consented national cohort first and then surrounded its genomes with longitudinal EHR, surveys, physical measures, and wearable streams, the data genomics needs to become medicine.
- **The field's direction:** multi-modal analytics at scale, where value comes from triangulation across modalities that no single data type or context can provide, a vision that ultimately rests on shared semantic and syntactic standards (ontologies, common data models, FHIR) for comparable data within and between systems.
- **The future shape for All of Us:** the trusted, diverse substrate on which ancestry-fair AI and foundation models are built; a governed, no-egress, in-environment model that lets the whole community reason over participant data without it leaving the enclave; a platform that becomes a reusable, AI-enabled ecosystem rather than a data-access environment; a live-signal roadmap that stays ahead of the publication lag; generalizability weighting so findings speak for the whole country; and closing the research-to-care gap so algorithms discovered on All of Us data can be re-derived and used at the bedside.
- **The obligations:** model regional variation in care and policy even in a representative cohort; meet rising re-identification risk with stronger privacy, clearer consent, and partnership with the source health systems; and return genuine value to the participants who give their data repeatedly.
- **The close:** All of Us as the national model for responsible, equity-anchored, AI-ready discovery, the foundation on which precision medicine is realized at scale. The data and the diversity are here; what remains is to close the gap and complete the lifecycle.

**Why.** Gives the recommendations a destination and a narrative rooted in what All of Us uniquely is, connecting the program's history, the field's trajectory, and the roadmap. (In the drafted paper this becomes the capstone section; here it is the argument it will make.)
**Key citations (author-group anchors to build on):** [Haendel et al. (N3C), JAMIA 2021](https://doi.org/10.1093/jamia/ocaa196); [Putman et al. (Monarch Initiative), Nucleic Acids Research 2024](https://doi.org/10.1093/nar/gkad1082); [Wilkinson et al. (FAIR), Sci Data 2016](https://doi.org/10.1038/sdata.2016.18); [Rehm et al. (GA4GH), Cell Genomics 2021](https://doi.org/10.1016/j.xgen.2021.100029).

## 9. Limitations

**Covers.** Keyword tagging is directional (not per-record classification); peer corpora are unaudited name-search sets (read the share index, not trend differentials); grant/IC coverage is ~30%; the full-text layer is not year-comparable; platform specifics rest on 2025-2026 vendor documentation. One limitation doubles as a recommendation: the volunteer-cohort generalizability caveat, now addressable via the 2026 generalizability work and the `waou` package.
**Why.** States the honest bounds of the analysis and shows the main limitation has a concrete, recommended remedy.

## 10. Conclusion

**Covers.** One paragraph: keep the eight focus areas, add a ninth for data/AI/methods, name and fund multi-omics, build the governed-AI and reuse capabilities the platform lacks, and protect the distinctiveness no peer can copy. The data and the diversity are here; what remains is to close the gap.
**Why.** Leaves the reader with the single actionable throughline.

---

## Appendix: citation and sourcing notes

**Covers.** How citations were harvested and verified (four clusters mapped to the sections; every reference resolves to the exact paper; DOIs resolved via NCBI E-utilities; preprints tagged and flagged for journal-version upgrade; the ACT-IAC/AoU white paper cited as an unreleased draft and not quoted; one unverifiable multi-omics preprint deliberately omitted). The consolidated list follows in the References section.
**Why.** Documents the anti-fabrication discipline so the reference base is trustworthy on import.

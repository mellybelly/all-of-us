# Seed references — "Where a diverse national cohort should go next: a data-driven refresh of the *All of Us* scientific roadmap"

Narrative / data-driven perspective · for the 2026 *All of Us* Science Committee and the biobank/informatics community.

This is a **seed** reference list to anchor citation-gathering, organized to match
[`outline.md`](outline.md). **Every entry was verified against a real source** (PubMed / PMC /
publisher / resolvable DOI — or arXiv/bioRxiv for CS work), with title + first author + year
confirmed; nothing was invented. **Spot-check before submission — see Caveats at the end.**

- **[Author-group]** tags papers authored by M. Haendel or close collaborators (verified in the byline).
- Some papers serve more than one section; the primary listing is marked and re-uses noted `*(also §X)*`.
- `[preprint]` marks non-peer-reviewed sources.

---

## Anchor seeds (author's prior work)

- [Haendel et al. The National COVID Cohort Collaborative (N3C). JAMIA 2021](https://doi.org/10.1093/jamia/ocaa196) — Haendel first author; a secure, governed multi-site clinical-data enclave — the data-commons/governance anchor for §5. **[Author-group]** *(also §5.1)*
- [Shefchek et al. The Monarch Initiative in 2019. Nucleic Acids Research 2020](https://doi.org/10.1093/nar/gkz997) — Haendel senior author; cross-species integrative phenotype–genotype platform and ontologies. **[Author-group]**
- [Putman et al. The Monarch Initiative in 2024. Nucleic Acids Research 2024](https://doi.org/10.1093/nar/gkad1082) — Haendel senior author; current Monarch knowledge-graph release. **[Author-group]**
- [Köhler et al. The Human Phenotype Ontology in 2021. Nucleic Acids Research 2021](https://doi.org/10.1093/nar/gkaa1043) — Haendel verified in the byline; standard vocabulary for computable deep phenotyping. **[Author-group]**
- [Jacobsen et al. The GA4GH Phenopacket schema. Nature Biotechnology 2022](https://doi.org/10.1038/s41587-022-01357-4) — Haendel in byline; community standard for exchanging computable phenotypes (later ISO 4454). **[Author-group]** *(also §5.2)*
- [Vasilevsky et al. Mondo: integrating disease terminology across communities. Genetics 2025](https://doi.org/10.1093/genetics/iyaf215) — Haendel senior author; unified computable disease-classification ontology. **[Author-group]**

---

## §1. Introduction — why refresh the roadmap now

- [Collins & Varmus. A New Initiative on Precision Medicine. N Engl J Med 2015](https://pubmed.ncbi.nlm.nih.gov/25635347/) — the Precision Medicine Initiative's founding Perspective; frames the national cohort that became All of Us.
- [Precision Medicine Initiative Working Group. The PMI Cohort Program — Building a Research Foundation for 21st Century Medicine. NIH 2015](https://www.nih.gov/sites/default/files/research-training/initiatives/pmi/09172015-pmi-working-group-report.pdf) — the blueprint report recommending a 1M+ cohort; the design document behind All of Us. *(gray literature)*
- [All of Us Research Program Investigators. The All of Us Research Program. N Engl J Med 2019](https://pubmed.ncbi.nlm.nih.gov/31412182/) — the canonical program description: goals, protocol, data types, >80% underrepresented enrollment. *(also cited for §3.4 benchmarking rationale and §5.1 platform)*
- [Mapes et al. Diversity and Inclusion for the All of Us Research Program: A Scoping Review. PLoS ONE 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7329113/) — defines/justifies the UBR (underrepresented in biomedical research) mandate.
- [Denny & Collins. Precision Medicine in 2030 — Seven Ways to Transform Healthcare. Cell 2021](https://doi.org/10.1016/j.cell.2021.01.015) — forward-looking precision-medicine roadmap (cohorts, AI, phenomics, equity) from the AoU CEO and NIH Director.

## §2. The *All of Us* research landscape

- [All of Us Research Program Genomics Investigators. Genomic Data in the All of Us Research Program. Nature 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10937371/) — flagship genomics release (245,388 genomes, >1B variants); anchors the genomic resource.
- [Ramirez et al. The All of Us Research Program: Data Quality, Utility, and Diversity. Patterns 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9403360/) — characterizes the data release (EHR, surveys, measurements) and the Researcher Workbench. *(also §5.1)*
- [Lederer et al. Data Quality Control in Using Fitbit Device Data From the All of Us Research Program. JMIR Mhealth Uhealth 2023](https://doi.org/10.2196/45103) — the AoU Fitbit/wearables resource and its QC; supports the wearables data asset.
- [Overhage et al. Validation of a Common Data Model for Active Safety Surveillance Research. JAMIA 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3240764/) — foundational validation of the OMOP CDM. *(also §5.2)*
- [Hripcsak et al. OHDSI: Opportunities for Observational Researchers. Stud Health Technol Inform 2015](https://doi.org/10.3233/978-1-61499-564-7-574) — the OHDSI community/tooling on the OMOP CDM that AoU data are modeled in.
- [Denny et al. PheWAS: Feasibility of a Phenome-Wide Scan to Discover Gene–Disease Associations. Bioinformatics 2010](https://pubmed.ncbi.nlm.nih.gov/20335276/) — the original phenome-wide association method on EHR-derived phenotypes.
- [Denny et al. Systematic Comparison of Phenome-Wide Association Study of EMR Data and GWAS Data. Nat Biotechnol 2013](https://pubmed.ncbi.nlm.nih.gov/24270849/) — first large-scale PheWAS in EMRs.
- [Kohane. Using Electronic Health Records to Drive Discovery in Disease Genomics. Nat Rev Genet 2011](https://doi.org/10.1038/nrg2999) — foundational review on repurposing EHR for genomic discovery.
- [Wei & Denny. Extracting Research-Quality Phenotypes from EHRs to Support Precision Medicine. Genome Med 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4416392/) — EHR phenotyping methods underpinning phenome-wide research.
- [van Eck & Waltman. VOSviewer, a Computer Program for Bibliometric Mapping. Scientometrics 2010](https://doi.org/10.1007/s11192-009-0146-3) — standard tool for bibliometric/co-citation mapping (corpus method).
- [Boyack & Klavans. Co-Citation, Bibliographic Coupling, and Direct Citation. JASIST 2010](https://doi.org/10.1002/asi.21419) — methodological benchmark for citation-based corpus mapping.
- [Blei, Ng & Jordan. Latent Dirichlet Allocation. J Mach Learn Res 2003](https://www.jmlr.org/papers/v3/blei03a.html) — canonical topic-modeling method for thematic corpus analysis.

## §3. Benchmarking against peer biobanks

### §3.1 The comparator set
- [Sudlow et al. UK Biobank: an open access resource. PLoS Medicine 2015](https://pubmed.ncbi.nlm.nih.gov/25826379/) — canonical UK Biobank cohort profile (500k, open-access); the primary comparator.
- [Bycroft et al. The UK Biobank resource with deep phenotyping and genomic data. Nature 2018](https://doi.org/10.1038/s41586-018-0579-z) — genotyping, imputation (~96M variants), QC; template for genomics-at-scale.
- [Gaziano et al. Million Veteran Program: a mega-biobank. J Clin Epidemiol 2016](https://pubmed.ncbi.nlm.nih.gov/26441289/) — VA MVP design; an EHR-linked health-system biobank comparator.
- [Kurki et al. FinnGen: genetic insights from a well-phenotyped isolated population. Nature 2023](https://pubmed.ncbi.nlm.nih.gov/36653562/) — ~429k samples linked to national registers; the founder-population comparator.
- [Chen et al. China Kadoorie Biobank of 0.5 million people. Int J Epidemiol 2011](https://pubmed.ncbi.nlm.nih.gov/22158673/) — CKB cohort profile; the large non-Western comparator.

### §3.2 Distinctive strengths & discovery at scale
- [Backman et al. Exome sequencing of 454,787 UK Biobank participants. Nature 2021](https://doi.org/10.1038/s41586-021-04103-z) — landmark biobank-scale exome resource.
- [Halldorsson et al. The sequences of 150,119 genomes in the UK Biobank. Nature 2022](https://pubmed.ncbi.nlm.nih.gov/35859178/) — biobank-scale WGS; benchmark for the WGS resource AoU also delivers.
- [Verma et al. Diversity and scale: genetic architecture of 2,068 traits in the MVP. Science 2024](https://doi.org/10.1126/science.adj1182) — multi-ancestry GWAS atlas (635,969); the discovery case for diverse biobanks.
- [Wojcik et al. Genetic analyses of diverse populations improves discovery for complex traits. Nature 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6785182/) — PAGE study; diverse samples surface variants missed in European-only studies.
- [Zhou et al. Global Biobank Meta-analysis Initiative. Cell Genomics 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9903716/) — cross-biobank harmonization/comparison framework (23 biobanks).

### §3.3 Gaps, diversity & representativeness
- [Sirugo et al. The Missing Diversity in Human Genetic Studies. Cell 2019](https://pubmed.ncbi.nlm.nih.gov/30901543/) — the ancestry-imbalance statement (~78% of GWAS participants European) and its costs.
- [Martin et al. Clinical use of current polygenic risk scores may exacerbate health disparities. Nat Genet 2019](https://doi.org/10.1038/s41588-019-0379-x) — PRS far more accurate in European-ancestry individuals; the equity argument for AoU.
- [Popejoy & Fullerton. Genomics is failing on diversity. Nature 2016](https://doi.org/10.1038/538161a) — early audit of non-European underrepresentation; frames the gap AoU set out to close.
- [Fry et al. Comparison of UK Biobank participants with the general population. Am J Epidemiol 2017](https://pubmed.ncbi.nlm.nih.gov/28641372/) — 5.5% response rate and healthy-volunteer bias; the representativeness caveat for mega-biobanks.
- [Mills & Rahal. A scientometric review of genome-wide association studies. Commun Biol 2019](https://doi.org/10.1038/s42003-018-0261-x) — GWAS bibliometrics showing persistent European dominance; the biobank-bibliometrics anchor.

### §3.4 Interpretation
- *AoU NEJM 2019* (see §1) — the diversity-first rationale that motivates benchmarking against the above.

## §4. Emerging scientific frontiers and AoU white space

### §4.1 AI foundation models in medicine (LLMs, clinical & agentic AI)
- [Moor et al. Foundation models for generalist medical AI. Nature 2023](https://pubmed.ncbi.nlm.nih.gov/37045921/) — defines "generalist medical AI"; the conceptual anchor for the frontier.
- [Singhal et al. Large language models encode clinical knowledge. Nature 2023](https://pubmed.ncbi.nlm.nih.gov/37438534/) — Med-PaLM/MultiMedQA; LLMs reach near-expert medical QA with a safety-evaluation framework.
- [Nori et al. Capabilities of GPT-4 on Medical Challenge Problems. arXiv 2023](https://arxiv.org/abs/2303.13375) `[preprint]` — general-purpose GPT-4 exceeds USMLE passing score without fine-tuning.
- [Kung et al. Performance of ChatGPT on USMLE. PLOS Digit Health 2023](https://doi.org/10.1371/journal.pdig.0000198) — early demonstration of LLM at USMLE threshold; catalyzed clinical-LLM interest.
- [Tu et al. Towards conversational diagnostic artificial intelligence. Nature 2025](https://doi.org/10.1038/s41586-025-08866-7) — AMIE diagnostic-dialogue agent; frontier of agentic clinical AI.
- [Mehandru et al. Evaluating large language models as agents in the clinic. npj Digit Med 2024](https://www.nature.com/articles/s41746-024-01083-y) — argues LLM agents be judged by workflow impact, not exam benchmarks.

### §4.2 Genomic / DNA sequence foundation models
- [Dalla-Torre et al. Nucleotide Transformer: robust foundation models for human genomics. Nat Methods 2025](https://doi.org/10.1038/s41592-024-02523-z) — benchmark-setting DNA language models (50M–2.5B params).
- [Ji et al. DNABERT. Bioinformatics 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC11025658) — foundational transformer establishing DNA-as-language pretraining.
- [Nguyen et al. Sequence modeling and design from molecular to genome scale with Evo. Science 2024](https://doi.org/10.1126/science.ado9336) — 7B-param genomic model, 131k context; zero-shot function prediction and design.
- [Brixi et al. Genome modeling and design across all domains of life with Evo 2. bioRxiv 2025](https://doi.org/10.1101/2025.02.18.638918) `[preprint]` — 7B/40B, 1Mb context; variant-effect prediction without fine-tuning. *(confirm journal version before submission)*

### §4.3 Multimodal modeling & data integration
- [Acosta et al. Multimodal biomedical AI. Nature Medicine 2022](https://doi.org/10.1038/s41591-022-01981-2) — review of fusing biobank, EHR, imaging, biosensor, and omics data; directly relevant to AoU's integrated data.
- [Boehm et al. Harnessing multimodal data integration to advance precision oncology. Nat Rev Cancer 2022](https://pubmed.ncbi.nlm.nih.gov/34663944/) — integration of molecular/imaging/clinical modalities and its interoperability barriers.

### §4.4 Disease-definition & methods shifts
- [Rinella et al. A multisociety Delphi consensus statement on new fatty liver disease nomenclature. Hepatology 2023](https://doi.org/10.1097/HEP.0000000000000520) — NAFLD→MASLD / NASH→MASH; redefines phenotyping for cohort studies.
- [Harrison et al. A Phase 3 Trial of Resmetirom in NASH with Liver Fibrosis (MAESTRO-NASH). N Engl J Med 2024](https://pubmed.ncbi.nlm.nih.gov/38324483/) — first phase-3 success; marks MASH as an actionable entity.
- [Hernán & Robins. Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available. Am J Epidemiol 2016](https://pubmed.ncbi.nlm.nih.gov/26994063/) — the founding target-trial-emulation framework; causal-inference anchor for EHR.
- [Hubbard et al. Target Trial Emulation for Observational Studies — Potential and Pitfalls. N Engl J Med 2024](https://doi.org/10.1056/NEJMp2407586) — strengths and biases of TTE on EHR/claims.

### §4.5 Frontiers needing assays AoU lacks ("partner, don't chase")
- [Jumper et al. Highly accurate protein structure prediction with AlphaFold. Nature 2021](https://pubmed.ncbi.nlm.nih.gov/34265844/) — AlphaFold2; a frontier to leverage, not reproduce.
- [Abramson et al. Accurate structure prediction of biomolecular interactions with AlphaFold 3. Nature 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11168924) — extends to protein–ligand/nucleic-acid complexes.
- [Marx. Method of the Year 2020: spatially resolved transcriptomics. Nature Methods 2021](https://pubmed.ncbi.nlm.nih.gov/33408395/) — a tissue-assay frontier beyond a population cohort's sample types.
- [Regev et al. The Human Cell Atlas. eLife 2017](https://doi.org/10.7554/eLife.27041) — the single-cell reference effort AoU can align to rather than duplicate.
- [The Tabula Sapiens Consortium. The Tabula Sapiens single-cell transcriptomic atlas of humans. Science 2022](https://pubmed.ncbi.nlm.nih.gov/35549404/) — ~500k cells / 24 tissues; requires assays AoU does not collect.

## §5. The analysis platform: the Researcher Workbench

### §5.1 Secure analysis platforms / data commons
- *Haendel et al. N3C. JAMIA 2021* (see Anchor seeds) — the secure governed enclave model. **[Author-group]**
- *Ramirez et al. Patterns 2022* (see §2) — the cloud-based Researcher Workbench and data-passport access model.
- [Schatz et al. Inverting the model of genomics data sharing with the NHGRI AnVIL. Cell Genomics 2022](https://doi.org/10.1016/j.xgen.2021.100085) — canonical AnVIL "bring-compute-to-data" paper.
- [Ahalt et al. Building a collaborative cloud platform (NHLBI BioData Catalyst). JAMIA 2023](https://doi.org/10.1093/jamia/ocad048) — community-driven cloud data/compute commons.
- [O'Connor et al. Dockstore: sharing Docker-based tools and workflows. F1000Research 2017](https://doi.org/10.12688/f1000research.10137.1) — registry of portable containerized workflows across commons.

### §5.2 Standards & interoperability
- [Wilkinson et al. The FAIR Guiding Principles for scientific data management. Sci Data 2016](https://doi.org/10.1038/sdata.2016.18) — the canonical FAIR principles.
- [Rehm et al. GA4GH: International policies and standards for data sharing. Cell Genomics 2021](https://doi.org/10.1016/j.xgen.2021.100029) — interoperable standards and policy for responsible genomic/clinical data sharing.
- *Jacobsen et al. GA4GH Phenopacket schema. Nat Biotechnol 2022* (see Anchor seeds) — computable phenotype exchange. **[Author-group]**
- *Overhage et al. OMOP CDM. JAMIA 2012* (see §2) — harmonized multi-site analytics (as used by N3C/OHDSI).
- [Biomedical Data Translator Consortium. Toward A Universal Biomedical Data Translator. Clin Transl Sci 2019](https://doi.org/10.1111/cts.12591) — NCATS Translator reasoning over integrated knowledge graphs. *(consortium byline — not tagged; see caveats)*

## §6. Recommendations — governed/responsible AI for the refreshed roadmap

- [Obermeyer et al. Dissecting racial bias in an algorithm used to manage the health of populations. Science 2019](https://doi.org/10.1126/science.aax2342) — landmark demonstration of racial bias in a deployed clinical algorithm.
- [Wiens et al. Do no harm: a roadmap for responsible machine learning for health care. Nat Med 2019](https://doi.org/10.1038/s41591-019-0548-6) — framework for responsibly moving ML to deployment.
- [Rajkomar et al. Ensuring Fairness in Machine Learning to Advance Health Equity. Ann Intern Med 2018](https://doi.org/10.7326/M18-1990) — fairness criteria and distributive-justice principles for clinical ML.
- [Char et al. Implementing Machine Learning in Health Care — Addressing Ethical Challenges. NEJM 2018](https://doi.org/10.1056/NEJMp1714229) — ethical risks (bias, oversight) in clinical ML.

*(§5 platform-reuse recommendations are anchored by Dockstore, FAIR, GA4GH, and AnVIL/BioData Catalyst above; §7 Limitations and §8 Conclusion draw on already-cited works.)*

---

## Caveats to check before use

**Cross-listed (list once; cited in multiple sections):** AoU NEJM 2019 (§1 primary; §3.4, §5.1); Ramirez Patterns 2022 (§2 primary; §5.1); Overhage OMOP 2012 (§2 primary; §5.2); Jacobsen Phenopacket 2022 (Anchor; §5.2).

**Preprints (confirm/upgrade to journal version before submission):** Nori et al. GPT-4 (arXiv 2303.13375); Brixi et al. Evo 2 (bioRxiv 2025.02.18.638918 — reportedly later in *Nature* ~2026; verify).

**Dual-journal:** Rinella MASLD consensus co-published in *Hepatology* (DOI above) and *J Hepatol* 2023;79(6):1542–1556 — cite per the manuscript's style.

**Preprint→journal already resolved:** Nucleotide Transformer cited to *Nat Methods* 2025 (not the 2023 bioRxiv); Evo to *Science* 2024; Mondo to *Genetics* 2025 (not 2022 medRxiv).

**Author-group tagging:**
- Tagged (byline-verified): N3C (Haendel 1st), Monarch 2019/2024 (Haendel senior), HPO 2021 (Haendel in large byline), Phenopacket 2022, Mondo 2025.
- **NOT tagged:** Biomedical Data Translator Consortium (Clin Transl Sci 2019) carries a *consortium* byline with no individual authors — Haendel is a program participant, not a byline author; placed in §5.2 untagged. (Date also ambiguous: epub Nov 2018, print 2019.)

**Gray literature:** the PMI Working Group report (§1) is an NIH government report, not peer-reviewed (included as the foundational design document).

**Deliberately omitted (no verifiable canonical paper found — do not add unverified):** a dedicated **Terra** platform paper (only vendor press releases; represented via AnVIL + BioData Catalyst); a **Gabriella Miller Kids First** platform paper (only NIH program pages); a standalone "compute-to-data" citation (anchored by AnVIL/BioData Catalyst); CKB's 2005 KSCDC predecessor profile; Peterson et al. 2019 and MVP array-methods papers (surfaced but not individually fetch-verified).

**General:** all URLs resolve to the exact paper (title + first author + year matched); some full texts are paywalled. Hubbard, Mehandru, Char, Wiens are Perspective/framing pieces, not primary evidence. Spot-check every DOI against your reference manager on import.


## Committee-sourced verified additions (2026-10-21)

**AoU program papers (committee 2026 series):**
- [Montgomery et al. Assessing the generalizability of prevalence estimates from the All of Us Research Program. Am J Epidemiology 2026;195(7):1962–1973](https://academic.oup.com/aje/article/195/7/1962/8426105) — generalizability Driver Project; §6.7 + §7. DOI 10.1093/aje/kwag010 · PMID 41536210.
- [waou: Weighting All of Us (Brannock/Elkasabi/Montgomery). CRAN 2026, v0.1.1](https://CRAN.R-project.org/package=waou) — released weighting package; §6.7 tool.
- [Cohn et al. Leveraging the All of Us Research Program to advance women's health. J Womens Health 2026;35(8):724–734](https://journals.sagepub.com/doi/10.1177/15409996261434111) — Women's Health Driver Project exemplar; §2.5/§6.6. DOI 10.1177/15409996261434111 · PMID 41856979.

**Frontier-methods harvest (§4):** 15 verified additions (genomic foundation models, clinical LLMs, agentic AI, multimodal, target-trial emulation, EHR foundation models) appended to [`citations_clusterC.md`](citations_clusterC.md).

**Deliberately omitted — UNVERIFIED:** the multi-omics preprint "Multi-omics in 10,000 diverse individuals…" (Montgomery/Padhi, AoU) could not be located on PubMed, bioRxiv, medRxiv, or the web (title/authors/cohort unconfirmed). The 10k multi-omics program is described in the deliverables as a program activity (committee update), **not** cited to a paper until one is verified.

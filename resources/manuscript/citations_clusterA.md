# Cluster A — Verified Seed Citations

Manuscript: *All of Us (AoU) Research Program scientific roadmap*
Cluster A covers §1 Introduction and §2 Research landscape.
Every entry below was verified against a real source (PubMed, PMC, publisher page, or resolvable DOI); the linked URL resolves to the exact paper (title + first author + year confirmed). Items that could not be verified are listed under Caveats, not here.

### §1 Introduction

- [Collins & Varmus. A New Initiative on Precision Medicine. N Engl J Med 2015](https://pubmed.ncbi.nlm.nih.gov/25635347/) — the Precision Medicine Initiative's founding Perspective; frames precision medicine and the long-term national cohort that became All of Us.
- [Precision Medicine Initiative Working Group. The PMI Cohort Program — Building a Research Foundation for 21st Century Medicine. NIH 2015](https://www.nih.gov/sites/default/files/research-training/initiatives/pmi/09172015-pmi-working-group-report.pdf) — the blueprint report recommending a 1-million-plus participant cohort; the design document behind All of Us.
- [All of Us Research Program Investigators. The All of Us Research Program. N Engl J Med 2019](https://pubmed.ncbi.nlm.nih.gov/31412182/) — the canonical program description: goals, protocol, data types, and the >80% underrepresented-participant enrollment.
- [Mapes et al. Diversity and Inclusion for the All of Us Research Program: A Scoping Review. PLoS ONE 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7329113/) — defines and justifies the program's UBR (underrepresented in biomedical research) mandate and the categories it spans.
- [Denny & Collins. Precision Medicine in 2030 — Seven Ways to Transform Healthcare. Cell 2021](https://doi.org/10.1016/j.cell.2021.01.015) — a forward-looking roadmap for precision medicine (cohorts, AI, clinical genomics, phenomics, equity) from the AoU CEO and NIH Director.

### §2 Research landscape

- [All of Us Research Program Genomics Investigators. Genomic Data in the All of Us Research Program. Nature 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10937371/) — the flagship genomics release (245,388 genomes, >1 billion variants); anchors the genomic data resource.
- [Ramirez et al. The All of Us Research Program: Data Quality, Utility, and Diversity. Patterns 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9403360/) — characterizes the initial data release across EHR, surveys, and measurements, and the Researcher Workbench; core data-resource reference.
- [Lederer et al. The Importance of Data Quality Control in Using Fitbit Device Data From the All of Us Research Program. JMIR Mhealth Uhealth 2023](https://doi.org/10.2196/45103) — describes the AoU Fitbit/wearables data and its quality-control considerations; supports the wearables data resource.
- [Overhage et al. Validation of a Common Data Model for Active Safety Surveillance Research. JAMIA 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3240764/) — foundational validation of the OMOP Common Data Model across 10 observational databases.
- [Hripcsak et al. Observational Health Data Sciences and Informatics (OHDSI): Opportunities for Observational Researchers. Stud Health Technol Inform 2015](https://doi.org/10.3233/978-1-61499-564-7-574) — introduces OHDSI, the open-science community and tooling built on the OMOP CDM that AoU data are modeled in.
- [Denny et al. PheWAS: Demonstrating the Feasibility of a Phenome-Wide Scan to Discover Gene-Disease Associations. Bioinformatics 2010](https://pubmed.ncbi.nlm.nih.gov/20335276/) — the original phenome-wide association study method using EHR/ICD-9-derived phenotypes.
- [Denny et al. Systematic Comparison of Phenome-Wide Association Study of EMR Data and GWAS Data. Nat Biotechnol 2013](https://pubmed.ncbi.nlm.nih.gov/24270849/) — first large-scale PheWAS in EMRs; establishes the method for program-scale EHR phenotype scans.
- [Kohane. Using Electronic Health Records to Drive Discovery in Disease Genomics. Nat Rev Genet 2011](https://doi.org/10.1038/nrg2999) — foundational review on repurposing EHR data for genomic discovery, the paradigm AoU operationalizes.
- [Wei & Denny. Extracting Research-Quality Phenotypes from Electronic Health Records to Support Precision Medicine. Genome Med 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4416392/) — review of EHR-based phenotyping methods underpinning phenome-wide research.
- [van Eck & Waltman. Software Survey: VOSviewer, a Computer Program for Bibliometric Mapping. Scientometrics 2010](https://doi.org/10.1007/s11192-009-0146-3) — the standard tool for bibliometric/co-citation mapping used to chart a research program's literature.
- [Boyack & Klavans. Co-Citation Analysis, Bibliographic Coupling, and Direct Citation: Which Citation Approach Represents the Research Front Most Accurately? JASIST 2010](https://doi.org/10.1002/asi.21419) — methodological benchmark for citation-based corpus mapping of a research field.
- [Blei, Ng & Jordan. Latent Dirichlet Allocation. J Mach Learn Res 2003](https://www.jmlr.org/papers/v3/blei03a.html) — the canonical topic-modeling method for corpus/text analysis used to map research programs thematically.

### Caveats

- No citation in this cluster was authored by Melissa Haendel's group. I checked the bylines of the AoU/OMOP/OHDSI items (closest to her OMOP/N3C/Monarch work) and none list Haendel; therefore nothing is tagged `[Author-group]`. If a Haendel-authored AoU/OMOP methods paper is intended for this cluster, flag it and I will verify and tag.
- The PMI Working Group report (§1) is NIH gray literature (a government report), not a peer-reviewed article. It is included as the program's foundational design document; the link is the official NIH-hosted PDF.
- Wearables anchor substitution: I could not verify a "Master et al. 2022" wearables paper under the searched terms. I substituted the verified Lederer et al. 2023 (JMIR Mhealth Uhealth) Fitbit data-quality paper, which directly describes the AoU wearables resource. An RTI dataset description of the AoU wearables data also exists but lacks a clean peer-reviewed citation, so it was excluded.
- Hripcsak 2015 OHDSI (Stud Health Technol Inform / MEDINFO proceedings): verified via DOI 10.3233/978-1-61499-564-7-574 and multiple concordant indexers; one indexer showed a likely coauthor-initial typo ("Lim, Y.C." vs "Li, Y.C."), which does not affect the first-author/title/year verification.
- Denny & Collins 2021 (Cell): linked via DOI; free author manuscript is also at PMC9616629.
- All DOIs/PMIDs/PMCIDs above were confirmed against PubMed, PMC, or publisher/DOI records matching title + first author + year; none were guessed.

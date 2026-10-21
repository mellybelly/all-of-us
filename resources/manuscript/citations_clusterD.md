# Cluster D — Verified seed citations

Scope: §5 (analysis platforms / data commons), §6 (recommendations: data-sharing standards, responsible clinical AI), plus author-group (Melissa Haendel) anchor papers. Every entry below was verified against a real resolvable source (PMC/PubMed/publisher/DOI) confirming the exact title + first author + year. 19 verified citations.

### Author-group anchor seeds

- [Haendel et al. The National COVID Cohort Collaborative (N3C). JAMIA 2021](https://doi.org/10.1093/jamia/ocaa196) — `[Author-group]` Haendel is first author; describes N3C's secure, governed multi-site clinical-data enclave — the §5 data-commons/governance anchor.
- [Shefchek et al. The Monarch Initiative in 2019. Nucleic Acids Research 2020](https://doi.org/10.1093/nar/gkz997) — `[Author-group]` Haendel senior author; cross-species integrative phenotype-genotype platform and ontologies underpinning the group's data-translation work.
- [Putman et al. The Monarch Initiative in 2024. Nucleic Acids Research 2024](https://doi.org/10.1093/nar/gkad1082) — `[Author-group]` Haendel senior author; current Monarch knowledge-graph/app release (52(D1):D938–D949).
- [Köhler et al. The Human Phenotype Ontology in 2021. Nucleic Acids Research 2021](https://doi.org/10.1093/nar/gkaa1043) — `[Author-group]` Haendel verified in the (large) author byline; standard vocabulary for computable deep phenotyping.
- [Jacobsen et al. The GA4GH Phenopacket schema. Nature Biotechnology 2022](https://doi.org/10.1038/s41587-022-01357-4) — `[Author-group]` Haendel in byline; community standard for exchanging computable phenotypic data (later ISO 4454), bridging author-group work and GA4GH standards.
- [Vasilevsky et al. Mondo: integrating disease terminology across communities. Genetics 2025](https://doi.org/10.1093/genetics/iyaf215) — `[Author-group]` Haendel senior author (Toro corresponding); unified, computable disease-classification ontology. Published journal version cited (not the 2022 medRxiv preprint).

### §5.1 Secure biomedical analysis platforms / data commons

- [Schatz et al. Inverting the model of genomics data sharing with the NHGRI AnVIL. Cell Genomics 2022](https://doi.org/10.1016/j.xgen.2021.100085) — Canonical AnVIL paper; articulates bring-compute-to-data on a federated cloud platform.
- [Ahalt et al. Building a collaborative cloud platform (NHLBI BioData Catalyst). JAMIA 2023](https://doi.org/10.1093/jamia/ocad048) — Ecosystem paper for NHLBI BioData Catalyst, a community-driven cloud data/compute commons.
- [Ramirez et al. The All of Us Research Program: data quality, utility, and diversity. Patterns 2022](https://doi.org/10.1016/j.patter.2022.100570) — Describes the cloud-based All of Us Researcher Workbench and its data-passport access model.
- [All of Us Research Program Investigators (Denny et al.). The "All of Us" Research Program. NEJM 2019](https://doi.org/10.1056/NEJMsr1809937) — Foundational program description (design, diversity goals, 1M-participant resource) for the manuscript's subject.
- [O'Connor et al. Dockstore: sharing Docker-based tools and workflows. F1000Research 2017](https://doi.org/10.12688/f1000research.10137.1) — Registry of containerized, descriptor-documented workflows enabling portable analysis across data commons.

### §5.2 Data-sharing infrastructure, standards & interoperability

- [Wilkinson et al. The FAIR Guiding Principles for scientific data management and stewardship. Scientific Data 2016](https://doi.org/10.1038/sdata.2016.18) — The canonical FAIR data principles reference.
- [Rehm et al. GA4GH: International policies and standards for data sharing. Cell Genomics 2021](https://doi.org/10.1016/j.xgen.2021.100029) — GA4GH suite of interoperable technical standards and policy frameworks for responsible genomic/clinical data sharing.
- [Overhage et al. Validation of a common data model for active safety surveillance (OMOP). JAMIA 2012](https://doi.org/10.1136/amiajnl-2011-000376) — Foundational OMOP common data model paper underpinning harmonized multi-site analytics (as used by N3C and OHDSI).
- [Biomedical Data Translator Consortium. Toward A Universal Biomedical Data Translator. Clinical and Translational Science 2019](https://doi.org/10.1111/cts.12591) — NCATS Translator program: inferential reasoning over integrated biomedical knowledge graphs. (See caveat — consortium byline, not an individual Haendel byline.)

### §6.1 Governed / responsible clinical AI, bias & fairness

- [Obermeyer et al. Dissecting racial bias in an algorithm used to manage the health of populations. Science 2019](https://doi.org/10.1126/science.aax2342) — Landmark demonstration of racial bias from a cost proxy in a widely deployed clinical algorithm.
- [Wiens et al. Do no harm: a roadmap for responsible machine learning for health care. Nature Medicine 2019](https://doi.org/10.1038/s41591-019-0548-6) — Framework for responsibly moving ML from development to clinical deployment.
- [Rajkomar et al. Ensuring Fairness in Machine Learning to Advance Health Equity. Annals of Internal Medicine 2018](https://doi.org/10.7326/M18-1990) — Taxonomy of fairness criteria and distributive-justice principles for clinical ML.
- [Char et al. Implementing Machine Learning in Health Care — Addressing Ethical Challenges. NEJM 2018](https://doi.org/10.1056/NEJMp1714229) — Perspective on ethical risks (bias, data as actor, oversight) in clinical ML.

### Caveats

- **Biomedical Data Translator Consortium (Clin Transl Sci 2019) — NOT tagged `[Author-group]`.** The paper carries a *consortium group byline* ("The Biomedical Data Translator Consortium"); the PMC record lists no individual byline (acknowledgments credit K. Fecho as lead draft author and S. Ahalt as senior author). Melissa Haendel participates in the NCATS Translator program but is not an individual byline author here, so per the tagging rule it is placed in §5.2 and left untagged. Also note date ambiguity: epub 9 Nov 2018, print issue dated Mar 2019 (12(2):86–90); some sources cite it as 2018.
- **Köhler et al. HPO 2021 — tagged `[Author-group]` with a note.** Haendel appears within a very large (~4-dozen) author byline. She is a genuine byline co-author (verified present), not merely an acknowledgee, so the tag stands; first author is Köhler and senior author is Robinson.
- **Mondo** — cited the peer-reviewed *Genetics* 2025 journal version (DOI 10.1093/genetics/iyaf215, adv. access 6 Oct 2025); a 2022 medRxiv preprint of the same work exists but the published version is preferred.
- **Terra** — intentionally omitted. No peer-reviewed platform paper was found (only Broad/Verily/Microsoft press releases). Terra is instead represented indirectly via AnVIL (Schatz et al.) and BioData Catalyst (Ahalt et al.), which are built on it.
- **Gabriella Miller Kids First Pediatric Data Resource Center** — omitted. Searches returned only NIH Common Fund program pages and press releases, not a canonical peer-reviewed platform paper; no verifiable citation could be confirmed, so none is listed rather than risk an unverified reference.
- **"Compute-to-data" / bring-compute-to-data** — no single dedicated citation; the concept is anchored by AnVIL (Schatz et al., which frames it explicitly) and BioData Catalyst (Ahalt et al.).
- **N3C secure enclave (§5 data commons)** — the governance/enclave aspect is carried by the author-group Haendel et al. JAMIA 2021 paper rather than a separate reference.
- All DOIs above were taken from the resolved PMC/publisher record for the exact paper; none were inferred or guessed.


### Verified additions (2026-10-21) — committee-sourced AoU program papers
- [Montgomery et al. Assessing the generalizability of prevalence estimates from the All of Us Research Program. Am J Epidemiology 2026](https://academic.oup.com/aje/article/195/7/1962/8426105) — AJE 2026;195(7):1962–1973; the generalizability Driver Project (RTI/NIH/Northwestern); anchors §6.7 and the §7 generalizability limitation. DOI 10.1093/aje/kwag010 · PMID 41536210.
- [Brannock, Elkasabi & Montgomery. waou: Weighting All of Us. CRAN 2026](https://CRAN.R-project.org/package=waou) — released R package (v0.1.1, 2026-10-02) that reweights AoU prevalence estimates to a probability sample; the tool for §6.7.
- [Cohn et al. Leveraging the All of Us Research Program to advance women's health. Journal of Women's Health 2026](https://journals.sagepub.com/doi/10.1177/15409996261434111) — J Womens Health 2026;35(8):724–734; the Women's Health Driver Project exemplar behind the driver-paper model (§2.5, §6.6). DOI 10.1177/15409996261434111 · PMID 41856979.

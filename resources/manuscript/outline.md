# Where a diverse national cohort should go next: a data-driven refresh of the *All of Us* scientific roadmap

*Annotated outline (sections with coverage and rationale, not drafted prose). A data-driven perspective for the All of Us Science Committee, program leadership, NIH, and the biobank and informatics community. Data current as of 2026-10-21. Verified key citations are listed per section; the full reference list with DOIs is at the end.*

---

## Key takeaways (the points every section supports)

1. The eight focus areas still hold, but three fast-growing bodies of work have no home in the framework (data science and AI methods ~18% of output, wearables, multi-omics). Propose a ninth focus area, "Data, AI & Methods."
2. All of Us has a distinctive identity worth protecting: it leads peers on health equity and social determinants, ethics and engagement, pharmacogenomics, and methods, driven by its diversity.
3. All of Us trails peers in five areas the committee flagged: imaging, multi-omics, aging research, rare disease, and environmental and social data (some addressable now, some by-design).
4. The field's leading edge is AI and foundation models; All of Us is almost absent (under ~0.3%) yet uniquely positioned to lead. Highest-leverage opportunity.
5. The Researcher Workbench leads on data and compute but lacks a reusable-tools registry, a governed in-environment AI assistant, and portable workflows (independently corroborated by a 2026 ACT-IAC/AoU white paper).
6. Ancillary studies are the leading edge the publication record cannot yet show; workspace activity precedes publications by a year or more, so score them on goals and live workspace signal.

## Abstract

**Covers.** One paragraph: the program's diversity-first thesis, what we analyzed (own output + external field + platform), the core findings in brief, and the forward vision.
**Why.** Sets the frame and the one-sentence argument ("All of Us scaled up everything around genomics that genomics needs to work in practice") before any detail.

## 1. Introduction: why refresh the roadmap now

**Covers.** The Precision Medicine Initiative origin and diversity mandate; what a roadmap is for and the 2020 eight focus areas; the three forces that justify a 2026 refresh (corpus maturity, the AI frontier shift, peer-cohort competition); our contribution (an evidence-driven refresh from the program's own output plus the external field).
**Why.** Establishes that diversity is the scientific thesis, not a constraint, and that the refresh is earned by evidence rather than opinion.
**Key citations:** [Collins & Varmus, NEJM 2015](https://doi.org/10.1056/NEJMp1500523); [PMI Working Group report, NIH 2015](https://www.nih.gov/sites/default/files/research-training/initiatives/pmi/09172015-pmi-working-group-report.pdf); [All of Us Program, NEJM 2019](https://doi.org/10.1056/NEJMsr1809937); [Mapes et al. (diversity/UBR), PLoS ONE 2020](https://doi.org/10.1371/journal.pone.0234962); [Denny & Collins, Cell 2021](https://doi.org/10.1016/j.cell.2021.01.015).

## 2. How we did this analysis (methods)

**Covers.** The reproducible five-step pipeline, run over the program's own output and the external literature. Each step answers one question:

| Step | What we did | What it answers |
| --- | --- | --- |
| 1. Inventory the corpus | Pulled publications (feed reconciled to PubMed/iCite) and workspaces (live production API). | What has All of Us produced? |
| 2. Tag by theme | Locked 19-theme taxonomy over title + abstract, plus a full-text layer. | What is the science about? |
| 3. Map to NIH and attribute funding | Matched to 29 strategic plans (166 priorities); grant IDs to Institutes via RePORTER. | Which NIH priorities and ICs does it serve? |
| 4. Compare to peer biobanks | Full-census name-search of UKB/FinnGen/MVP/CKB, same tagger, static share index. | How does All of Us differ? |
| 5. Scan the frontier + benchmark the platform | Term-acceleration over 322,138 preprints + 460,285 grants; Workbench vs 5 platforms (87/87 verified); rubric scoring. | What is rising that AoU has not claimed, and what to build? |

**Also covers.** The numbers behind the pipeline, and three interpretive cautions (peer comparisons are relative-emphasis not head-to-head; workspace text is intent not execution; keyword tagging is directional but order-of-magnitude robust).
**Why.** The method is what makes the conclusions defensible, and it is reusable for tracking the roadmap over time.
**Key citations:** [Overhage et al. (OMOP CDM), JAMIA 2012](https://doi.org/10.1136/amiajnl-2011-000376); [Denny et al. (PheWAS), Bioinformatics 2010](https://doi.org/10.1093/bioinformatics/btq126).

## 3. The All of Us research landscape

**Covers.** The theme distribution and the finding that the eight focus areas largely still fit; the three structural gaps (a data-science/AI/methods orphan, wearables, multi-omics); the NIH funding/IC landscape and pan-NIH framing; and the ancillary (partnered) studies as the leading edge (Exploring the Mind, Eyes on Health, Nutrition for Precision Health, Environmental Health and Exposomics), including the workspace-leads-publications finding and the live multi-omics and external-biospecimen activity.
**Why.** Shows what the program actually produces, where the framework is straining, and why a live workspace census (not a cached snapshot) is essential to see the newest science.
**Key citations:** [All of Us Genomic Data, Nature 2024](https://doi.org/10.1038/s41586-023-06957-x); [Ramirez et al., Patterns 2022](https://doi.org/10.1016/j.patter.2022.100570); [Lederer et al. (Fitbit), JMIR 2023](https://doi.org/10.2196/45103); [NIH Partnered Research Studies](https://www.nih.gov/allofus/funding/partnered-research-studies); [Cohn et al. (Women's Health Driver Project), J Women's Health 2026](https://doi.org/10.1177/15409996261434111).

## 4. Benchmarking against peer biobanks

**Covers.** The comparator set and method; All of Us's distinctive strengths vs the peer median (SDOH/health equity, ELSI/engagement, pharmacogenomics, methods); the five areas where it trails (imaging, multi-omics, aging, rare disease, environmental/social); and the distinction between addressable gaps and by-design peer emphasis.
**Why.** Calibrates the program against comparable cohorts and makes the case that distinctiveness, not raw growth, is the durable signal, while taking the real gaps seriously.
**Key citations:** [Sudlow et al. (UK Biobank), PLoS Med 2015](https://doi.org/10.1371/journal.pmed.1001779); [Gaziano et al. (MVP), J Clin Epidemiol 2016](https://doi.org/10.1016/j.jclinepi.2015.09.016); [Kurki et al. (FinnGen), Nature 2023](https://doi.org/10.1038/s41586-022-05473-8); [Chen et al. (China Kadoorie), Int J Epidemiol 2011](https://doi.org/10.1093/ije/dyr120); [Sirugo et al. (missing diversity), Cell 2019](https://doi.org/10.1016/j.cell.2019.02.048); [Martin et al. (PRS & equity), Nat Genet 2019](https://doi.org/10.1038/s41588-019-0379-x); [Fry et al. (representativeness), Am J Epidemiol 2017](https://doi.org/10.1093/aje/kwx246).

## 5. Emerging scientific frontiers and All of Us white space

**Covers.** The horizon-scan method and its result that AI and foundation models are the fastest-rising frontier; the feasibility-filtered opportunities (genomic foundation models as the highest-leverage, in-environment LLM and agentic workflows, MASLD as a cheap phenotype, target-trial emulation); and the boundary of frontiers that need assays AoU does not generate (single-cell/spatial, protein structure) where AoU should partner, not chase.
**Why.** Separates what is merely trendy from what All of Us can uniquely act on, and identifies the single highest-leverage opportunity.
**Key citations:** [Moor et al. (generalist medical AI), Nature 2023](https://doi.org/10.1038/s41586-023-05881-4); [Singhal et al. (Med-PaLM), Nature 2023](https://doi.org/10.1038/s41586-023-06291-2); [Dalla-Torre et al. (Nucleotide Transformer), Nat Methods 2025](https://doi.org/10.1038/s41592-024-02523-z); [Nguyen et al. (Evo), Science 2024](https://doi.org/10.1126/science.ado9336); [Acosta et al. (multimodal), Nat Med 2022](https://doi.org/10.1038/s41591-022-01981-2); [Rinella et al. (MASLD), Hepatology 2023](https://doi.org/10.1097/HEP.0000000000000520); [Hernán & Robins (target-trial emulation), Am J Epidemiol 2016](https://doi.org/10.1093/aje/kwv254); [Jumper et al. (AlphaFold), Nature 2021](https://doi.org/10.1038/s41586-021-03819-2).

## 6. The analysis platform: the Researcher Workbench

**Covers.** Why the platform shapes the science; the comparator benchmark (N3C, Terra/AnVIL, BioData Catalyst, UKB-RAP, Kids First) and where the Workbench leads (data, compute); the three remediable gaps (reuse registry, governed in-environment AI, portable workflows) and the BAA/in-VPC path; the reuse signal from the workspace census (87.7% solo, 3.2% multi-institution, ~18% tutorial clones); and the independent corroboration from the 2026 ACT-IAC/AoU white paper.
**Why.** Science is bounded by the platform; the gaps that matter are not data or compute but the capabilities that turn them into shared, reusable, AI-enabled science.
**Key citations:** [Haendel et al. (N3C), JAMIA 2021](https://doi.org/10.1093/jamia/ocaa196); [Schatz et al. (AnVIL), Cell Genomics 2022](https://doi.org/10.1016/j.xgen.2021.100085); [Ahalt et al. (BioData Catalyst), JAMIA 2023](https://doi.org/10.1093/jamia/ocad048); [O'Connor et al. (Dockstore), F1000Research 2017](https://doi.org/10.12688/f1000research.10137.1); [Wilkinson et al. (FAIR), Sci Data 2016](https://doi.org/10.1038/sdata.2016.18); [Rehm et al. (GA4GH), Cell Genomics 2021](https://doi.org/10.1016/j.xgen.2021.100029).

## 7. Recommendations for the refreshed roadmap

**Covers.** The structural changes (add a ninth "Data, AI & Methods" focus area; rename the genetics area to "Genetics, Multi-omics & Biology" plus a proteomics-release roadmap); the Workbench builds (governed in-VPC AI co-scientist, reusable-tools registry, multimodal templates, and an internal no-egress foundation model guided by a "super user group"); adopting the committee's 2026 directions as standing mechanisms (driver-paper model for rare-disease and intersectional papers; generalizability weighting as a first-class capability tied to the external-biospecimen mechanism); protecting distinctiveness and governing AI responsibly; and measuring the roadmap by re-running the same methods over time.
**Why.** Translates every finding into a concrete, prioritized action, and unifies the highest-leverage opportunity with the clearest platform gap in a single build.
**Key citations:** [Obermeyer et al. (algorithmic bias), Science 2019](https://doi.org/10.1126/science.aax2342); [Wiens et al. (responsible ML), Nat Med 2019](https://doi.org/10.1038/s41591-019-0548-6); [Rajkomar et al. (fairness), Ann Intern Med 2018](https://doi.org/10.7326/M18-1990); [Char et al. (ethical ML), NEJM 2018](https://doi.org/10.1056/NEJMp1714229); [Montgomery et al. (generalizability), Am J Epidemiol 2026](https://doi.org/10.1093/aje/kwag010); [waou (CRAN)](https://CRAN.R-project.org/package=waou); [Cohn et al. (driver-paper model), J Women's Health 2026](https://doi.org/10.1177/15409996261434111).

## 8. A vision for the future of All of Us

**Covers.** A forward argument grounded in the program's history (it inverted the biobank model: diverse national cohort first, then surrounded genomes with longitudinal multi-modal data) and the field's trajectory (multi-modal analytics at scale, where value comes from triangulation across modalities no single data type can provide). The future shape for All of Us: the trusted diverse substrate on which ancestry-fair AI and foundation models are built; a governed no-egress in-environment model; a platform that becomes a reusable, AI-enabled ecosystem rather than a data-access environment; a live-signal roadmap that stays ahead of the publication lag; generalizability weighting so findings speak for the whole country; shared semantic and syntactic standards that close the research-to-care re-implementation gap; and reciprocity to participants. Closes on All of Us as the national model for responsible, equity-anchored, AI-ready discovery ("close the gap and complete the lifecycle").
**Why.** Gives the recommendations a destination and a narrative rooted in what All of Us uniquely is, connecting history, the field, and the roadmap.
**Key citations (author-group anchors to build on):** [Haendel et al. (N3C), JAMIA 2021](https://doi.org/10.1093/jamia/ocaa196); [Putman et al. (Monarch Initiative), Nucleic Acids Research 2024](https://doi.org/10.1093/nar/gkad1082); [Wilkinson et al. (FAIR), Sci Data 2016](https://doi.org/10.1038/sdata.2016.18); [Rehm et al. (GA4GH), Cell Genomics 2021](https://doi.org/10.1016/j.xgen.2021.100029).

## 9. Limitations

**Covers.** Keyword tagging is directional; peer corpora are unaudited (read the share index, not trend differentials); grant/IC coverage ~30%; the full-text layer is not year-comparable; platform specifics rest on vendor documentation. One limitation doubles as a recommendation: the volunteer-cohort generalizability caveat, now addressable via the 2026 generalizability work and the `waou` package.
**Why.** States the honest bounds of the analysis and shows that the main limitation has a concrete remedy the roadmap recommends.

## 10. Conclusion

**Covers.** One paragraph: keep the eight focus areas, add a ninth, name and fund multi-omics, build the governed-AI and reuse capabilities, protect distinctiveness. The data and the diversity are here; what remains is to close the gap.
**Why.** Leaves the reader with the single actionable throughline.

---

## Appendix: citation and sourcing notes

**Covers.** How citations were harvested and verified (four clusters mapped to the sections; every reference resolves to the exact paper; DOIs resolved via NCBI E-utilities; preprints tagged and flagged for journal-version upgrade; the ACT-IAC/AoU white paper cited as an unreleased draft, not quoted; the unverifiable multi-omics preprint deliberately omitted).
**Why.** Documents the anti-fabrication discipline so the reference base is trustworthy on import.

# Disease-burden & NIH-funding sources

Annotated primary sources for the disease-burden evidence layer. The first six
were shared in the June 3, 2026 WG meeting agenda (the disease-burden thread);
the remaining entries are the burden and funding reference datasets used to
build the crosswalk. Verified 2026-06-11.

## Burden ↔ funding alignment literature (from the June 3 agenda)

1. **Persistence of very low correlations between NIH funding and disease burden.**
   *The persistence of very low correlations between NIH research funding and
   disease burdens.* ScienceDirect [S2666535224001174](https://www.sciencedirect.com/science/article/pii/S2666535224001174)
   (Dec 2024); open-access mirror [PMC11754078](https://pmc.ncbi.nlm.nih.gov/articles/PMC11754078/).
   - 27 conditions; 5 burden measures (incidence, prevalence, mortality, YLLs, DALYs); 1994–2004 and 2009–2019.
   - **Very weak and declining correlations: R² < 0.03 excluding HIV** across the five burden measures. DALYs gave the strongest relationship and even that was only R² ≈ 0.15.
   - **HIV/AIDS receives the highest funding relative to burden of any disease**; including it pushes R² below 0.02. **Alzheimer's** became notably overfunded after a deliberate 2016 Congressional appropriation increase.
   - Conclusion: long-standing inefficiency; closer burden-funding matching would improve research efficiency.

2. **Allocation of NIH funding and burden of disease, 2008–2021.**
   *npj Health Systems* 2:41 (2025), [s44401-025-00048-x](https://www.nature.com/articles/s44401-025-00048-x).
   - In 2021, every 1% increase in DALYs/100k was associated with a **0.31% increase in NIH funding per capita** — i.e., funding is far less than proportional to burden.
   - Association present in 2021 but **not in 2008**, and **longitudinally not significant in any single year of the past five** — alignment is weak and inconsistent over time.
   - **Neoplasms and neurological disorders** consistently well-funded; **self-harm and interpersonal violence** persistently underfunded relative to burden.
   - Notes NIH spending tracks *prior-year* spending more than current burden.

3. **Global distribution of research efforts, disease burden, and impact of US public-funding withdrawal.**
   *Nature Medicine* (Aug 27, 2025), [s41591-025-03923-0](https://www.nature.com/articles/s41591-025-03923-0);
   open-access [PMC12443587](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12443587/).
   - Linked **8.6M disease-specific publications** to two decades of GBD data via a triangulated LLM approach.
   - Research–burden alignment improved since 1999 but **mostly incidentally** (communicable-disease declines); noncommunicable burden has grown and globalized while research effort has not kept pace.
   - Simulations: the research–burden divergence will **widen by ~a third over the next two decades** absent intentional alignment, and **US international-research funding withdrawal accelerates the gap**.

4. **NIH RCDC categorical spending** — *Estimates of Funding for Various Research,
   Condition, and Disease Categories.* [report.nih.gov/funding/categorical-spending](https://report.nih.gov/funding/categorical-spending).
   - **The page does load** (flagged "not working for me" in the agenda — likely transient). Current RCDC table published **June 17, 2025**, covering **327 categories, FY2008–FY2024**. **FY2025/FY2026 estimates are not currently posted** ("evolving changes in administration priorities").
   - This is the canonical per-category NIH funding source for any burden-vs-funding crosswalk. Combine with the RCDC table that pairs categories with NCHS/CDC mortality + prevalence.

5. **Static and dynamic relationships between burden of disease and research funding.**
   Nimgaonkar et al., *Health Research Policy and Systems* (2022), [PMC9164716](https://pmc.ncbi.nlm.nih.gov/articles/PMC9164716/).
   - 38 RCDC↔GBD-matched categories; log-log GLMs.
   - **Cross-sectional 2017 funding ∝ 2017 DALYs (R² = 0.31)** and 10-year-lagged (R² = 0.30) — but **temporal change in burden 2006–2017 is uncorrelated with cumulative spend (p = 0.65)**.
   - **Mental, neurologic, and substance-use disorders underperform** relative to investment; HIV/AIDS over-improved relative to its funding-predicted trajectory.

6. **Long COVID disability burden in US adults.**
   *Communications Medicine* (2026), [s43856-026-01516-7](https://www.nature.com/articles/s43856-026-01516-7).
   - Quantifies the disability burden of an **emergent, under-categorized condition** — the type of high-burden signal that lags RCDC categorization and that a cohort like AoU is positioned to surface early.

## Burden reference dataset

7. **GBD 2021 (IHME)** — US burden. Cause-level DALYs/YLDs for the United States.
   - Tool: [GBD Results](https://www.healthdata.org/data-tools-practices/interactive-visuals/gbd-results) · [GBD Compare](https://vizhub.healthdata.org/gbd-compare/).
   - State-level US analysis: *The burden of diseases, injuries, and risk factors by state in the USA, 1990–2021* ([IHME/Lancet](https://www.healthdata.org/research-analysis/library/burden-diseases-injuries-and-risk-factors-state-usa-1990-2021)).
   - Anchor facts used for tiering: **low back pain** is the leading US cause of YLDs (1990 and 2021); **depressive disorders** and **drug use disorders** are #2 and #3 YLDs; **ischemic heart disease** leads US DALYs; diabetes, cancers, stroke, COPD, and Alzheimer's/other dementias are top DALY causes.

## A note on what is and isn't computed here

Per the repo's factual-correctness discipline, the crosswalk in
`burden_vs_attention.md` assigns each AoU theme a **burden tier
(High/Medium/Low), an analyst judgment anchored to the GBD US leading-cause
rankings above — not invented DALY point-estimates.** Exact per-category DALY
and RCDC-dollar joins are a follow-on step (sources 4 and 7 supply the data);
they are flagged where they would sharpen a finding.

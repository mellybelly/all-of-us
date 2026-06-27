# Part 1 — capability/data-asset gap matrix: framework

Comparison of the All of Us Researcher Workbench (RW) against comparator
biomedical analysis platforms, to identify **remediable deficiencies**.

## Platforms

| Code | Platform | Stack |
| --- | --- | --- |
| AOU | All of Us Researcher Workbench (RW 2.0) | Verily Workbench / Google Cloud |
| N3C | National COVID Cohort Collaborative Enclave | Palantir Foundry / AWS (NIH UNITE) |
| TERRA | Terra + AnVIL | Broad / Google Cloud (+ Azure) |
| BDC | NHLBI BioData Catalyst | Gen3 + PIC-SURE + Seven Bridges + Terra + Dockstore |
| UKBRAP | UK Biobank Research Analysis Platform | DNAnexus / AWS |
| KF | Gabriella Miller Kids First DRC | Gen3 + Cavatica (Velsera) / AWS |

## Dimensions

1. **Data assets** — modalities hosted (genomic/WGS, EHR/OMOP, imaging, surveys, wearables, etc.).
2. **Compute & GPU** — VM scale, GPU types, Spark/Hail.
3. **AI / LLM & generative tooling** — in-environment LLM/assistants, governed vs BYO-key.
4. **Notebook / analysis environments** — Jupyter/RStudio/other; languages.
5. **Egress / security / access model** — open vs closed vs compute-to-data; review gates.
6. **Collaboration & reuse** — shared workspaces, tool/workflow registries, concept sets, provenance.
7. **Cost model** — who pays for compute/egress; credits.
8. **Standards / interoperability** — OMOP, GA4GH, Dockstore/WDL/CWL, FAIR/DOIs.

## Citation rule (non-negotiable)

Every matrix claim must cite a **fetchable URL** with a **verbatim supporting
quote**. Each citation is programmatically re-fetched and the quote confirmed
present (`citations_verified.csv`). Claims whose source 404s/403s or whose quote
cannot be located are marked **unverified** and excluded from asserted findings.

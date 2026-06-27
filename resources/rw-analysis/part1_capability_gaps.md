# RW Analysis — Part 1: capability & data-asset gaps vs comparator platforms

Systematic comparison of the All of Us Researcher Workbench (RW) against five
comparator biomedical analysis platforms, to identify **remediable
deficiencies**. Scope deliberately extends beyond biobanks to general-purpose
secure-analysis platforms (N3C, Terra/AnVIL, BioData Catalyst, Kids First).

## Citation integrity

Every factual claim below is backed by a **fetched-and-verified** citation.
Process: each claim carries a source URL + a verbatim quote; a script
(`verify_citations.py`) re-fetched every URL and confirmed the quote is present
on the page. **Result: 87/87 citations verified** (85 by automated quote-match,
2 by rendered re-fetch where the host blocks scripted access). The full audit
trail — status, platform, claim, URL, verbatim quote — is in
[`citations_verified.csv`](citations_verified.csv). Claims with no fetchable,
quote-matched source were **dropped, not asserted** (notably: no platform
publicly documents an in-environment *governed* LLM except the Terra→Azure
OpenAI connection — see gaps).

Platforms: **AOU** (Verily Workbench/GCP), **N3C** (Palantir Foundry/AWS),
**TERRA** (Terra+AnVIL/GCP), **BDC** (NHLBI BioData Catalyst), **UKBRAP**
(DNAnexus/AWS), **KF** (Kids First/Cavatica).

## Capability matrix (all cells backed by verified citations in the CSV)

| Dimension | AoU RW | N3C | Terra/AnVIL | BioData Catalyst | UKB-RAP | Kids First |
| --- | --- | --- | --- | --- | --- | --- |
| **Data assets** | EHR + short/long-read WGS + arrays + surveys + physical + Fitbit (linked, diverse) | EHR-derived RWD, 90+ institutions | NHGRI genomes (AnVIL, 280k+) | TOPMed + genomic/omics/imaging | UKB bulk + tabular health | Pediatric cancer/birth-defect genomics |
| **Compute & GPU** | **H100/H200/B200 + NeMo** | CPU/Spark (GPU not documented) | GPU on Jupyter; Parabricks | GPU ML instances | AWS/Azure/OCI GPU instances | GPU ML instances |
| **AI / LLM tooling** | Claude Code + Gemini CLI **(BYO key)** | none documented | **Azure OpenAI** connection (Azure) | none documented | none documented | none documented |
| **Notebooks** | Jupyter, RStudio, SAS (R/Py/SAS) | Code Workbooks (Py/R/SQL/PySpark) | Jupyter, RStudio/Bioconductor, Galaxy | JupyterLab, RStudio, SAS | JupyterLab Spark | JupyterLab, RStudio |
| **Egress / security** | Closed; FISMA-Mod; data passport | Closed; no download; FedRAMP-Mod | **Compute-to-data**; FedRAMP-Mod (Azure) | Compute-to-data; egress billed | Closed; admin download restriction | Open w/ optional irreversible lock |
| **Collaboration & reuse** | Workspace **sharing only** | GitHub export, branching, Notepad, interoperable artifacts | **Dockstore** workflow registry | **Public apps** repo (copy+modify) | Custom workflows, dx SDK, project sharing | **Public Apps gallery + publish-your-own**, R Shiny |
| **Cost model** | $300 credits/user | grant-funded | pay-as-you-go | monthly billed | usage-billed + limits | per-instance + storage |
| **Standards / interop** | OMOP CDM | OMOP CDM 5.3 | **Dockstore: CWL/WDL/Nextflow/Galaxy** | **GA4GH DRS** | DNAnexus platform | **GA4GH DRS** |

## Where AoU leads (so the gaps are credible, not cherry-picked)

- **Data assets** are the strongest in the set: AoU is the only platform pairing
  population-scale, ancestry-diverse short- *and* long-read WGS with longitudinal
  EHR, surveys, physical measures, and wearables on consented individuals.
- **GPU/AI compute** is arguably best-in-class: H100/H200/B200 + NeMo for
  foundation-model training is more than any comparator publicly documents.
- **Notebooks, OMOP standardization, closed-tier security** are at parity with
  the strongest comparators.

So AoU's deficiencies are **not** in data or raw compute — they are in
**platform capabilities that turn data+compute into shared, reusable, AI-enabled
science.**

## Remediable deficiencies (the deliverable)

### Gap 1 — No shared tool/workflow reuse registry *(largest, clearest gap)*
Every comparator exposes a reuse mechanism for analytical artifacts; AoU
documents only basic workspace sharing.

- **AoU:** "workspaces are collaborative and can be shared among registered
  researchers on a project team" — and nothing beyond that is publicly
  documented. ([researchallofus.org/data-tools/workbench](https://www.researchallofus.org/data-tools/workbench/))
- **Terra/AnVIL & BDC & Kids First** all integrate registries: Dockstore is "an
  app store for sharing scientific tools and workflows"
  ([docs.dockstore.org](https://docs.dockstore.org/en/develop/dockstore-introduction.html));
  BDC offers "a repository of publicly available apps"
  ([sb-biodatacatalyst.readme.io](https://sb-biodatacatalyst.readme.io/docs/use-public-apps));
  Cavatica lets "researchers publish their own tools or workflows to the…Public
  Apps gallery" ([docs.cavatica.org](https://docs.cavatica.org/docs/publish-your-app)).
- **N3C** adds branching, GitHub export, and cross-app interoperable artifacts
  ([rwdcollaborative.github.io](https://rwdcollaborative.github.io/guide-to-n3c-v1/chapters/tools.html)).
- **Why remediable / impact:** this is corroborated by Part 2's workspace data
  (86% solo workspaces, ~20% are tutorial *clones*, no reuse economy). A
  Dockstore integration or a published-reusable-app gallery + concept-set/
  knowledge store (à la N3C) is a known, off-the-shelf pattern AoU could adopt.

### Gap 2 — No *governed* in-environment LLM
- **AoU:** ships Claude Code + Gemini CLI but **bring-your-own-key**
  ([support.workbench.verily.com](https://support.workbench.verily.com/docs/guides/cloud_apps/ai_tools/)),
  so they can't compliantly process participant data.
- **Terra** documents a workspace→**Azure OpenAI Service** connection
  ([broadinstitute.org/news/terra-azure-release](https://www.broadinstitute.org/news/terra-azure-release)).
  No comparator yet offers a strong governed model either — so this is an
  *industry-wide* gap AoU could **lead** rather than trail.
- **Why remediable:** AoU runs on Google Cloud, whose BAA already covers Vertex
  AI/Gemini — a program-credentialed in-VPC model is a governance/provisioning
  task, not a legal blocker. Full mechanics + sources in
  [`baa_llm_egress_evidence.md`](baa_llm_egress_evidence.md).

### Gap 3 — No portable-workflow / interoperability standard for analysis
- Comparators standardize *analysis* portability: Dockstore supports "CWL, WDL,
  Nextflow and Galaxy" ([docs.dockstore.org](https://docs.dockstore.org/en/develop/dockstore-introduction.html));
  BDC and Cavatica are GA4GH **DRS** driver projects for cross-platform data
  import ([ga4gh.org](https://www.ga4gh.org/driver_project/nhlbi-biodata-catalyst-bdc/),
  [docs.cavatica.org](https://docs.cavatica.org/docs/import-from-a-drs-server)).
- **AoU** standardizes *data* (OMOP) but documents no portable-workflow or
  GA4GH-interchange capability — analyses are not packaged to move or be reused
  across teams/platforms. Reinforces Gap 1.

## Caveats

- **Absence of evidence ≠ evidence of absence.** "Not documented" cells (e.g.,
  N3C GPU, comparator in-env LLM) mean no fetchable public doc was found, not
  that the capability is definitely missing. These are marked accordingly.
- A few comparator claims are sourced from official *equivalent* docs
  (anvilproject.org, sb-biodatacatalyst.readme.io, NHLBI) because the primary
  support portals (support.terra.bio, support.researchallofus.org,
  biodatacatalyst.nhlbi.nih.gov) block scripted fetching — every such source is
  still public, official, and quote-verified.
- AoU specifics reflect RW 2.0 / Verily Workbench docs (2025-2026); confirm
  exact AoU-collection enablement in-environment.
- This is a capability *inventory*; it does not assess usage quality (Part 2
  covers adoption).

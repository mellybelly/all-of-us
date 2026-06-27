# RW Analysis — Part 3: tools & artifacts the Researcher Workbench should build

Synthesis of Parts 1 (capability gaps vs comparators) and 2 (trending methods +
adoption/reuse evidence) into a **prioritized set of concrete tools/artifacts**.
Each recommendation is grounded in three things: a **scientific trend** (Part 2),
a **verified comparator precedent** (Part 1 — every cited source is in
[`citations_verified.csv`](citations_verified.csv)), and an **AoU asset** that
makes it feasible. Framing follows the program's own "build / integrate /
govern" lens.

## Priority map

| # | Artifact | Addresses (gap / trend) | Comparator precedent | AoU asset | Effort | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Governed in-VPC AI co-scientist | Gap 2 (BYO-key only); Part 2 LLM/RAG/agentic ~0% | Terra→Azure OpenAI | GCP BAA covers Vertex/Gemini; H100/NeMo | Med | **Now** |
| 2 | Reusable tool/workflow registry + published-apps gallery | Gap 1 (sharing only); 86% solo / clone-reuse | Dockstore; BDC/Cavatica public apps | Workbench, OMOP | Med | **Now** |
| 3 | Multimodal integration templates + feature store | Part 2 #1 (1.6% adoption) | — (AoU-distinctive) | linked WGS+EHR+survey+Fitbit | Med | **Now** |
| 4 | Phenotype / concept-set library (reusable cohorts) | Gap 1/3; reuse | N3C interoperable artifacts; OMOP | OMOP CDM | Med | Next |
| 5 | Causal-inference & target-trial-emulation templates | Part 2 (causal 2.5%, TTE 0.4%) | — | longitudinal EHR | Low | Next |
| 6 | Genomic/EHR foundation-model resources + eval benchmarks | Part 2 #2; horizon-scan #1 | — (AoU-distinctive) | diverse WGS+EHR; H100/H200/B200+NeMo | High | Next |
| 7 | Portable-workflow + GA4GH interop (WDL/CWL/DRS) | Gap 3 | Dockstore CWL/WDL/Nextflow; GA4GH DRS | Workbench | Med | Next |
| 8 | Collaboration primitives (team/featured workspaces) | reuse evidence (3.7% multi-inst) | (cross-platform sharing) | Workbench | Low | Next |
| 9 | Benchmarking/eval harness + synthetic data | Part 2 (benchmarking 0.4%, synth 0.1%) | — | full cohort | Med | Later |

## Tier "Now" — highest impact, feasible, strongest evidence

### 1. A governed, in-VPC AI co-scientist
**What:** an AoU-credentialed LLM running inside the trust boundary (Gemini/
Vertex or Claude-on-Vertex under the program's Google Cloud BAA), surfaced as a
notebook assistant + a RAG cohort/code helper over the AoU data dictionary and
docs — *not* the current bring-your-own-key CLIs.
**Why (trend):** LLM/RAG/agentic methods are the fastest-rising in the field yet
~0% in AoU workspaces (Part 2); the RW only ships **BYO-key** Claude Code/Gemini
CLI that "are pre-installed on cloud apps created after April 2026"
([Verily docs](https://support.workbench.verily.com/docs/guides/cloud_apps/ai_tools/))
and therefore can't compliantly touch participant data.
**Precedent:** Terra documents a workspace→"Azure OpenAI Service" connection
([broadinstitute.org](https://www.broadinstitute.org/news/terra-azure-release)).
No comparator has a strong governed model — AoU can **lead**.
**Feasible:** GCP's BAA already covers Vertex/Gemini; AoU has H100/H200/B200 +
NeMo ([verily.com](https://verily.com/perspectives/verily-nvidia-ai-workbench)).
The blocker is governance/provisioning, not law (see `baa_llm_egress_evidence.md`).
**Maps to:** deck Rec 4 (Workbench AI co-scientist) + the 9th focus area.

### 2. A reusable tool/workflow registry + published-apps gallery
**What:** integrate a workflow registry and a "publish your analysis as a
reusable app" gallery + featured/curated workspaces — so analyses are shareable
artifacts, not one-off clones.
**Why (trend/evidence):** AoU documents only that "workspaces…can be shared
among registered researchers on a project team"
([researchallofus.org](https://www.researchallofus.org/data-tools/workbench/)),
and Part 2 shows the result: 86% solo workspaces and ~20% tutorial *clones*, with
no reuse economy.
**Precedent (verified):** Dockstore is "an app store for sharing scientific
tools and workflows" ([docs.dockstore.org](https://docs.dockstore.org/en/develop/dockstore-introduction.html));
BDC offers "a repository of publicly available apps"
([sb-biodatacatalyst.readme.io](https://sb-biodatacatalyst.readme.io/docs/use-public-apps));
Cavatica lets researchers "publish their own tools or workflows to the…Public
Apps gallery" ([docs.cavatica.org](https://docs.cavatica.org/docs/publish-your-app));
N3C supports GitHub export + branching for reuse
([rwdcollaborative.github.io](https://rwdcollaborative.github.io/guide-to-n3c-v1/chapters/tools.html)).
**Feasible:** Dockstore is open and already integrated by three comparators;
AoU could integrate it or stand up an equivalent gallery.

### 3. Multimodal data-integration templates + a feature store
**What:** curated templates and a feature store that join genomics + EHR +
surveys + physical measures + wearables into analysis-ready multimodal feature
sets.
**Why (trend):** multimodal modeling is the single largest *fit-to-gap* in Part 2
(fast-rising; only ~1.6% of AoU workspaces attempt cross-modality work) — and
AoU is the **only** platform pairing short/long-read WGS with EHR, surveys,
physical measures, and Fitbit on consented individuals (Part 1 data-assets row).
**Precedent:** AoU-distinctive (no comparator co-locates these modalities), so
this is a lead-not-follow opportunity rather than a catch-up.
**Feasible:** the data is already linked; the gap is tooling/templates.

## Tier "Next" — high value, modest dependencies

- **4. Phenotype / concept-set library** of validated, reusable cohort
  definitions on the OMOP CDM ([AoU uses OMOP](https://www.researchallofus.org/data-tools/data-sources/);
  [N3C OMOP 5.3](https://rwdcollaborative.github.io/guide-to-n3c-v1/chapters/tools.html)),
  so cohorts are shared assets, not re-derived per workspace (a major source of
  the duplication seen in Part 2). Pairs with #2.
- **5. Causal-inference & target-trial-emulation templates** — validated,
  documented templates for AoU's longitudinal EHR (causal inference 2.5%,
  target-trial emulation 0.4% of workspaces in Part 2; both high RW-feasibility).
  Low effort, high methodological payoff.
- **6. Genomic/EHR foundation-model resources + evaluation benchmarks** —
  publish reference embeddings / pretrained models and ancestry-fair eval
  benchmarks built on AoU, leveraging the H100/H200/B200 + NeMo stack. This is
  Part 2's #2 opportunity and the horizon scan's #1 white-space; AoU's diverse
  WGS+EHR is an unmatched substrate.
- **7. Portable-workflow + GA4GH interoperability** — adopt WDL/CWL workflow
  packaging and GA4GH **DRS** so analyses move/reuse across teams and platforms
  (Dockstore "CWL, WDL, Nextflow and Galaxy"
  [docs.dockstore.org](https://docs.dockstore.org/en/develop/dockstore-introduction.html);
  GA4GH DRS used by [BDC](https://www.ga4gh.org/driver_project/nhlbi-biodata-catalyst-bdc/)
  and [Cavatica](https://docs.cavatica.org/docs/import-from-a-drs-server)).
  Enables #2.
- **8. Collaboration primitives** — first-class multi-PI/team workspaces and
  curated featured workspaces to lift the 3.7% multi-institution / 86% solo
  pattern (Part 2).

## Tier "Later" — enabling infrastructure

- **9. Benchmarking/eval harness + synthetic-data generators** — standardized
  model evaluation (0.4% of workspaces) and synthetic data (0.1%) to accelerate
  method development and lower the barrier to the Tier-Now/Next tools.

## How the recommendations cohere
- **#1, #6** make AoU an **AI-method leader** on a uniquely diverse substrate —
  the horizon-scan white-space.
- **#2, #4, #7, #8** build the **reuse/collaboration economy** AoU lacks and
  every comparator has — the clearest Part-1 gap, corroborated by Part-2 data.
- **#3, #5** turn AoU's **distinctive data** into method templates researchers
  aren't yet using.
- Together they operationalize the proposed **"Data, AI & Methods" focus area**
  and the Workbench AI co-scientist recommendation already in the deck.

## Caveats
- This is a *recommendation synthesis*; effort/priority labels are judgment, not
  measured. Comparator precedents are quote-verified; "AoU-distinctive" items
  have no comparator by design.
- Implementation specifics (e.g., which registry, model, or feature-store tech)
  need scoping with the program/Verily; this defines the *what* and *why*, not
  the build plan.

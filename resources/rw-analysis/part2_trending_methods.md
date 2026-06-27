# Researcher Workbench analysis — Part 2: trending methods not yet adopted

**Question.** Which analytical methods/tools are *accelerating in the broad
literature* but *under-used in AoU* — in publications and, more tellingly, in the
researcher **workspaces** — and which of those are **feasible** on the Workbench?

## Method

| Input | Source |
| --- | --- |
| External method trend | Term-acceleration from 293,979 preprints + 422,565 NIH grants (2021-26), distilled to **27 analytical-method topics** (LLM induction, methods-only) — `methods_topics.json`. |
| AoU publications | 1,432 pubs (title+abstract) — adoption in the *literature* AoU produces. |
| AoU workspaces | **12,899 substantive** workspaces (tutorials/duplicates removed), matching the `approaches`/`questions`/`findings` text — adoption in *what researchers actually do on the RW*. |
| Feasibility | Each method rated against RW assets: WGS/genotyping, EHR/OMOP, surveys, physical measures, Fitbit wearables; cloud Jupyter/RStudio + BigQuery + Hail/Spark. |

Opportunity = external-trend × maturity × feasibility × (1 − workspace adoption).
Full table in `methods_gap.csv`. Workspace text is *self-described intent*, not
executed code, so percentages are directional (see Caveats).

## Tier 1 — Highest-opportunity gaps (rising · feasible · near-absent on RW)

| Method | Maturity | Field growth | AoU pubs | AoU workspaces | RW fit |
| --- | --- | ---: | ---: | ---: | --- |
| Multimodal modeling / data integration | rising | 846× | 1.6% | 1.6% | high |
| Genomic / DNA foundation models | rising | 359× | 0.1% | 0.2% | high |
| Foundation models (general / pretrained) | rising | 359× | 0.3% | 0.6% | high |
| Large language models (as analysis method) | rising | 386× | 4.1% | 1.5% | high |
| Retrieval-augmented generation (RAG) | rising | 27× | 0.0% | 0.02% | high |
| Causal inference | rising | 47× | 3.8% | 2.5% | high |
| Zero-shot / transfer learning | rising | 5.7× | 0.2% | 0.3% | high |
| Digital / wearable biomarkers | rising | 53× | 5.1% | 7.5% | high |
| Synthetic data generation | rising | 2.1× | 0.2% | 0.1% | high |
| Target trial emulation | rising | 1.7× | 0.1% | 0.4% | high |

**Reads:**
- **Multimodal data integration** is the single biggest fit-to-gap: AoU uniquely
  co-locates genomics + EHR + surveys + physical measures + wearables, yet only
  ~1.6% of workspaces attempt cross-modality modeling. The asset is there; the
  methodology isn't being used.
- **Foundation models (genomic + EHR)** are ~absent (0.1–0.6%) — the field's
  fastest-rising method on a population-scale dataset purpose-built for it.
- **Causal inference & target-trial emulation** suit AoU's longitudinal EHR but
  appear in <2.5% of workspaces.
- **Digital/wearable biomarkers** are comparatively *better* adopted (7.5% of
  workspaces) — AoU's Fitbit data is being used; this is the model for what
  good adoption looks like.

## Tier 2 — Mature, feasible, under-used (quick wins)

| Method | AoU pubs | AoU workspaces | Note |
| --- | ---: | ---: | --- |
| Mendelian randomization | 2.1% | 1.3% | well-suited to WGS+EHR; low uptake |
| Survival / time-to-event ML | 2.7% | 2.8% | longitudinal EHR is ideal |
| Transformer / deep-learning architectures | 0.1% | 0.2% | near-absent despite maturity |
| Embeddings & representation learning | 0.4% | 0.6% | foundational for modern ML |
| Benchmarking & model evaluation | 0.7% | 0.4% | little standardized evaluation |
| Interpretable / explainable ML | 3.8% | 3.5% | moderate |

**Validation check:** the two mature genomic methods AoU is *known* for —
**polygenic risk scores (10.1% of workspaces)** and **PheWAS (4.8%)** — score as
well-adopted, confirming the detector measures real adoption, not noise. The
under-used rows above are genuine gaps, not measurement artifacts.

## Tier 3 — Feasible in principle, but environment-constrained

| Method | AoU pubs | AoU workspaces | Constraint |
| --- | ---: | ---: | --- |
| Agentic AI / autonomous agents | 0.1% | 0.03% | needs in-environment LLM tooling / orchestration |
| Chain-of-thought / reasoning prompting | 0.0% | 0.02% | same |
| Digital twins / in-silico modeling | 0.0% | 0.1% | tooling + compute |

**A measurable signal worth noting:** LLMs appear in **4.1% of AoU publications
but only 1.5% of workspaces** — the only method where publication use markedly
exceeds workspace use. The most parsimonious explanation is that researchers use
LLMs *outside* the secured environment (e.g., manuscript drafting) more than *as
an in-environment analysis method*, consistent with the controlled tier's
outbound/tooling constraints. RAG, agentic AI, and chain-of-thought are all
~0% in workspaces despite being among the fastest-rising methods in the field —
i.e., the workbench's tooling has not yet brought modern LLM workflows inside.

## Out of scope (low RW feasibility — flagged, not recommended)

Single-cell/spatial analysis methods, single-cell foundation models, and protein
language models are rising fast but require assay modalities AoU does not
generate. Watch, don't build.

## Collaboration & reuse signals (objective, from the workspace directory)

Computed directly from the public workspace feed (`collaboration_evidence.csv`):

| Signal | Value |
| --- | ---: |
| Workspaces total | 21,242 |
| **Solo** (single owner) | **18,217 (85.8%)** |
| Multi-owner (≥2) | 3,025 (14.2%) |
| Teams of ≥5 | 250 (1.2%) |
| **Multi-institution** | **791 (3.7%)** |
| Mean owners / workspace | **1.24** |
| Duplicate-title workspaces (case-folded) | 4,144 (19.5%) |
| Titles beginning "Duplicate of …" | 4,649 (21.9%) |

**Descriptive read:** the dominant workspace pattern is a single researcher
working alone (86%), cross-institution teams are rare (3.7%), and roughly a fifth
of all workspaces are duplicates — predominantly clones of tutorial/workshop
content ("Duplicate of How to work with All of Us genomic data", etc.). The
public directory exposes no signal of shared/forked analytical artifacts being
reused *across* teams; the observable reuse pattern is **copy-a-tutorial**, not
**build-on-each-other**. (Limitation: notebook/code-level reuse is not exposed in
the public feed, so this bounds collaboration from team/workspace metadata only.)

## How this feeds the rest of the RW analysis

- **Part 1 (platform capability gaps):** the Tier-3 enclave constraint and the
  thin multimodal/foundation-model adoption are hypotheses to test against
  comparator platforms (AnVIL, BioData Catalyst, N3C, Terra, UKB-RAP).
- **Part 3 (what to build):** Tier-1/Tier-2 methods + the collaboration metrics
  point at concrete artifacts — multimodal templates, in-environment
  foundation-model/LLM tooling, reusable validated-method notebooks, and
  team/sharing primitives.
- Reinforces the Roadmap's proposed **"Data, AI & Methods" focus area**: the
  methods the field is adopting fastest are precisely those AoU researchers use
  least.

## Caveats

- **Workspace text = intent, not execution.** `approaches`/`questions` describe
  planned methods, not the code actually run; percentages are directional.
  PRS/PheWAS validation suggests the signal tracks real adoption, but absolute
  values should be read as order-of-magnitude.
- **Keyword matching** (substring) has small false +/−; method keywords were
  chosen to be discriminating.
- **Grant growth multipliers** are partly inflated by RePORTER vocabulary onsets;
  trend judgments lean on preprint (author-text) signals.
- Workspace corpus is the 2025-10-24 snapshot (per the landscape README).

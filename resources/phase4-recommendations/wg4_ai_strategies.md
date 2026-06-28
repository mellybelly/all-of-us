# WG-4: AI Strategies

> This is a **topic / need area**, not a decision body. Its topic overlaps
> with the other need areas and should be coordinated across them. The WG
> label is used here as a topic reference.

## Lead(s) and scope

**Lead (chair):** Sastry.
**Scope (per 2026 WG deck):** researcher-facing AI applications —
what to build, what to integrate, what governance.

**Reality check (from the evidence):** HA4 (AI / foundation models / LLMs)
already has **33 pubs (30 post-2023)** in the AoU corpus — researchers are
*already* using AI on AoU data. The AI need area's question is not whether
researchers want AI; it's what AoU should provide, build, govern, or
integrate.

**External horizon scan (`../emerging-trends/emerging_trends_report.md`).** An
open-discovery scan of 294k preprints + 423k NIH grants (2021-2026) ranks
**genomic foundation models (#1)** and **LLMs / agentic AI (#2)** as the
fastest-rising AoU-feasible white-space gaps in biomedicine (LLM-in-medicine
publications up **47× 2021→2025**; AoU <0.3% present). This directly backs
Rec 1 (co-scientist) and Rec 3 (foundation-model evaluation). It also **bounds
scope**: single-cell / spatial / protein-structure foundation models are
exploding too, but sit *outside AoU's data model* — AoU should evaluate genomic
and EHR foundation models, not chase those.

**Researcher Workbench comparator analysis (`../rw-analysis/`, 87/87 citations
source-verified).** Benchmarked vs N3C, Terra/AnVIL, BioData Catalyst, UKB-RAP,
and Kids First: AoU leads on data assets and GPU/AI compute but has three
remediable platform gaps — no shared tool/workflow reuse registry (every
comparator has one), **no governed in-environment LLM (only bring-your-own-key
Claude Code/Gemini CLI)**, and no portable-workflow/GA4GH interoperability. The
key BAA point for this WG: an in-environment LLM is *not* blocked by a missing
BAA — Google Cloud's BAA already covers Vertex AI/Gemini, so an in-VPC model
keeps data in-boundary; the gap is that AoU hasn't provisioned a governed
in-VPC model. Evidence + mechanics in `../rw-analysis/baa_llm_egress_evidence.md`;
recommended builds in `../rw-analysis/part3_recommended_tools.md`.

---

## Candidate recommendations evaluated

1. **An AI co-scientist (cohort-builder / code-writer) on the Workbench** —
   LLM-grounded cohort-definition agent that translates natural-language
   queries to OMOP/phecode/PRS cohorts; auto-generates analytic code.
2. **An agentic-AI workflow for reproducibility** — workspace build to
   analysis to publication-ready output, with provenance and replication
   trace.
3. **An AoU-anchored EHR foundation model** (or thoughtful integration of an
   existing one — Med-PaLM, Foundation Medical AI Models, NHS Foundation,
   the EHR-FM family) tuned on AoU's UBR-oversample for bias-corrected
   performance.
4. **AI governance + bias-mitigation framework** for AoU-derived AI
   products (parallel to WG-2 / WG-3 frameworks).
5. **An AI-grounded phenotype-validation pipeline** — LLM-assisted
   curation of phecode definitions and validated computational phenotypes,
   extending Smoller's PheKB / CLAMP priorities.
6. **A standing AI-tools evaluation framework** — periodic public
   benchmark of LLM/AI tools against AoU-defined tasks.

---

## Top-3 ranked recommendations

### 1. An AoU Workbench AI co-scientist (cohort-builder + code-generator)

**Description.** A researcher-facing AI agent embedded in the AoU
Researcher Workbench that translates natural-language queries to
OMOP-/phecode-/PRS-based cohort definitions, generates the Python/R
analytic skeleton, and explains its choices. Integrates with the existing
phecode and CLAMP infrastructure Smoller's subgroup already prioritized.
Reduces the days-to-first-result barrier that the AoU researcher base
consistently identifies as a friction point.

**Supporting evidence.**
- HA4 33 pubs, 30 post-2023, includes foundation-model phenome-wide
  prediction (PMID:39794311), DL time-to-event for depression and asthma
  (PMID:40417537), PAL-AI oocyte-maturation model (PMID:40750633) — the
  user base is *already* doing this kind of work and would benefit
  enormously from a Workbench-native tool.
- Theme 3 (methods / AI / phenotyping non-genomic): 262 pubs / 2,388
  projects — AoU peer-index 3.0× peer median (`aou_vs_peers_index.csv`).
  The largest distinctive-strength area outside ELSI and SDOH.
- NLM-G1-O2 (informatics R&D: curation at scale, analytics, visualization,
  modeling, NLP) and NLM-G1-O4 (sustainable computational infrastructure)
  — NLM is the most aligned IC.
- NIH-Wide CCT5 (Leveraging Data Science) — explicit cross-cutting
  alignment.
- Smoller's NLP/CLAMP (3.40) priority is the upstream foundation; AI
  co-scientist sits on top.

**Need area.** Researcher-facing AI falls under the AI need area; this is the
quintessential recommendation for it. Coordinate with the imaging need area
(WG-3, imaging integration via the same agent surface) and the communications
need area (WG-5 — researcher experience is a comms story).

**Rubric scores.**

| Criterion | Score | Justification |
|---|---:|---|
| Unmet researcher need | 4 | Time-to-first-result is the #1 cited Workbench friction; demand is large. |
| Simplifies analysis | 4 | Directly simplifies cohort definition + code scaffolding. |
| Standardizes/harmonizes | 4 | An agent that uses phecodes / OMOP / canonical AoU vocabularies *enforces* harmonization on novice users. |
| Broad use cases | 4 | Every Workbench user. |
| Scientific Roadmap alignment | 4 | Slide 7 AI/LLM priority, plus the proposed new "Data, AI & Methods" focus area. |
| Tool exists vs new dev | 3 | Anthropic Claude / OpenAI / open-source LLMs exist; the AoU-specific scaffolding (cohort-language → OMOP → code) is new. RAG-with-phecode-definitions is straightforward. |
| No new data collection | 4 | Uses existing data. |
| Helps with data quality | 4 | Enforced use of validated phenotypes (PheKB, phecodes) and canonical vocabularies *reduces* data-quality variance from researcher-defined ad-hoc cohorts. |
| **Mean (applicable only)** | **3.88** | |

**Risks / pushback expected.** "Hallucinations / wrong cohort definitions"
— defend with explicit-provenance design (every cohort/code-block links
back to the source vocabulary entry the agent invoked; researcher must
confirm before execution). "Build vs buy" — answer: build the AoU-specific
scaffolding on top of an existing foundation model, not the model itself.

---

### 2. AI governance + bias-mitigation framework for AoU-derived AI products

**Description.** Establish an AoU-specific AI governance framework
covering: (a) bias auditing for any AI tool published using AoU
(extending WG-2's bias-in-translation framework to AI-specific failure
modes — performance disparities, fairness-through-unawareness traps,
representation drift); (b) explicit data-use review for AI training
(versus inference / analysis); (c) a standing Workbench-native bias-audit
template (parallel to WG-3's imaging bias report card); (d) IRB/ELSI
integration for participant-facing AI applications.

**Supporting evidence.**
- 33 AI pubs already exist with no AoU-specific governance — the
  governance gap is operational *now*, not theoretical.
- NHGRI BP4 (move beyond race-based descriptors) directly motivates an
  AI-specific bias framework.
- NIMHD G4 (methods/metrics for HD research) + G7 (analysis of HD
  populations in big data) — AI tools that under-perform on UBR
  subgroups violate AoU's foundational mandate.
- HA6 (G×E×SDOH integrated, 11 pubs) — exactly the modeling territory
  where bias propagates fastest.
- FA7 (Health Equity) is load-bearing (51% of post-2023 corpus touches
  FA7); without an AI-bias framework, FA7 is at risk of corrosion via
  un-audited AI deployments.

**Need area.** AI-specific bias failure modes (fairness-through-
unawareness, label noise differentially distributed by group, miscalibration
across subgroups, distribution shift) sit in the AI need area, where that
technical context lives. Inherits the normative frame from the translational
need area (WG-2); coordinate the two.

**Rubric scores.**

| Criterion | Score | Justification |
|---|---:|---|
| Unmet researcher need | 3 | Demand from regulators and high-stakes deployers is high; researcher-level demand is mixed. |
| Simplifies analysis | 2 | Adds a workflow step, doesn't simplify directly. |
| Standardizes/harmonizes | 4 | Establishes the AoU AI-bias standard. |
| Broad use cases | 4 | Every AoU-derived AI product. |
| Scientific Roadmap alignment | 4 | FA7 + the proposed "Data, AI & Methods" area. |
| Tool exists vs new dev | 3 | Fairness toolkits exist (Aequitas, FairLearn, AIF360); AoU-specific packaging is new. |
| No new data collection | 4 | Operates on existing AoU data + derived models. |
| Helps with data quality | 4 | Bias audit catches representation and label-quality issues. |
| **Mean (applicable only)** | **3.50** | |

**Risks / pushback expected.** "How do we enforce?" — answer: Workbench-
native audit template + journal/preprint citation requirement (analogous
to STROBE / CONSORT). "Doesn't the Sci Com already do this?" — answer:
not for AI-specific failure modes (the field has moved past generic ML
review).

---

### 3. AoU-tuned foundation model evaluation (build-or-buy decision framework)

**Description.** Rather than building a foundation model de novo, the
recommendation is a structured **evaluation** of existing EHR foundation
models (Med-PaLM family, NHS Foundation, EHR-FM, etc.) against AoU-defined
benchmarks, leading to a **build-or-buy-or-integrate recommendation by end of
2027**. This provides an explicit decision-point rather than a permanent open
question.

**Supporting evidence.**
- HA4 33 pubs include foundation-model-style phenome-wide disease-onset
  prediction (PMID:39794311) — researchers are already inferring with
  foundation models against AoU data, but without a benchmark.
- The 2026 omics releases (multi-omics from Refresh Rec 2) will multiply
  foundation-model demand on AoU.
- NLM G1-O2 explicit ask; NIH-Wide CCT5.
- The build-cost question is real (training a foundation model is
  10s-of-millions); structured evaluation is the responsible first step.
- The field of EHR foundation models is moving so fast that *any*
  premature build commitment will be obsolete on delivery — evaluation
  with a decision-deadline is the correct posture.

**Need area.** The AI need area is where the technical context to specify
benchmarks and run an apples-to-apples evaluation lives. Any decision rests
with program leadership; the evaluation work falls under this need area.

**Rubric scores.**

| Criterion | Score | Justification |
|---|---:|---|
| Unmet researcher need | 3 | Researcher-base demand is large but currently un-articulated. |
| Simplifies analysis | 3 | A model with AoU-aware grounding would simplify analyses currently done with vanilla LLMs + manual context. |
| Standardizes/harmonizes | 3 | Benchmark establishes evaluation harmonization, not data harmonization. |
| Broad use cases | 4 | Foundation models cross-cut every analysis pattern. |
| Scientific Roadmap alignment | 4 | Direct slide-7 AI/foundation-model priority. |
| Tool exists vs new dev | 4 | The recommendation is evaluation, not build — leverages existing models. |
| No new data collection | 4 | Existing AoU data only. |
| Helps with data quality | 3 | Standardized benchmark exposes data-quality variance across subgroups. |
| **Mean (applicable only)** | **3.50** | |

**Risks / pushback expected.** "Are you saying AoU shouldn't build a
foundation model?" — answer: not yet. The evaluation is the responsible
prerequisite. Sci Com may want a definitive build/buy answer faster than
the WG can responsibly provide; defend the 2027 timeline as the realistic
duration for a proper benchmark.

---

## Also-considered (deprioritized with reasoning)

- **Agentic-AI reproducibility workflow (candidate 2).** Strong idea but
  better packaged as a *feature* of Recommendation 1 (AI co-scientist) or
  as a WG-5 (Communications, impact-tracking via reproducibility) item.
- **AI-grounded phenotype-validation pipeline (candidate 5).** Directly
  builds on Smoller's PheKB / CLAMP work but risks being read as a
  duplicate. Surface as a subcomponent of Recommendation 1.
- **Standing AI-tools evaluation framework (candidate 6).** Real need
  but better held by an ongoing AI subgroup of Sci Com rather than a
  Top-3 WG deliverable; this WG should *establish* the evaluation
  template (Recommendation 3) and hand off operations.

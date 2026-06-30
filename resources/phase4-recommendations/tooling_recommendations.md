# Tooling & database-integration recommendations

> These recommendations span the translational and AI **need areas**, which
> are topic areas, not decision bodies. Their topics overlap and should be
> coordinated. The WG labels are used here as topic references.

**Cross-need-area (WG-2 Translational × WG-4 AI) deliverable.**
Added per the June 3, 2026 WG meeting — Melissa: *"Consider making some tooling
recommendations"*; Jordan's database-integration / agentic-follow-up thread;
and the carried-over reproducibility "computable-phenotype gallery" idea. See
`../wg-meeting-notes/2026-06-03_second-meeting.md`.

## Scope and why a separate doc

The June 3 discussion surfaced a distinct concern from WG-4's *researcher-facing
AI* scope: **the integration of high-quality external biomedical knowledge
resources into the AoU Workbench so that researchers don't have to "take data
outside AoU and run it through their favorite tool"** (Jordan). The motivating
use cases were concrete: given a finding, list drug-repurposing candidates by
mechanism of action and mount a **target-trial emulation**; given a variant, do
**variant-to-function mapping** — without exporting data. Plus two cross-cutting
needs: a **curated, versioned, attributable computable-phenotype gallery**
(reproducibility), and clarity on **what tools are and aren't allowed in the
Workbench** (security/privacy).

These are tooling/integration recommendations, not AI-application
recommendations, so they live here and **cross-reference** rather than duplicate
WG-4 (the AI co-scientist) and WG-2 (RWE / NCATS-Translator linkage).

**Governance grounding.** The AI/agentic recommendations below are bounded by
the NASEM AI-governance reports now in the evidence base — *Generative AI in
Health and Medicine* and *An AI Code of Conduct for Health and Medicine*
([catalog](../strategic-plans/nasem/README.md)) — and by the workbench
security/privacy constraints (Rec 3).

**Burden grounding.** The disease-burden layer (`../disease-burden/`) gives
these tools a *direction*: an in-Workbench drug-repurposing/target-trial-
emulation capability is most valuable when pointed at high-burden,
under-attended conditions (aging/ADRD, respiratory, the underfunded
mental-health/substance cluster), letting AoU act as a burden-corrective rather
than a burden-mirror.

---

## Candidate recommendations evaluated

1. **A curated computable-phenotype & artifact gallery** — versioned,
   attributable, community-vetted/upvoted (FAIR), to fix the
   inconsistent-phenotype-definition noise (e.g., Type 2 diabetes defined
   differently across AoU papers).
2. **An integrated biomedical knowledge-base layer** on the Workbench —
   high-quality external resources (drug mechanism of action, gene–disease,
   variant-to-function, pathway/MoA) connected to AoU data so agentic
   follow-up (repurposing candidate lists, variant→function) runs in place.
3. **A vetted, security-reviewed external-tool / data integration framework** —
   an explicit process and allow-list for adding third-party tools and
   reference databases to the Workbench, resolving the "what's allowed in the
   workbench" question.
4. **An in-Workbench target-trial-emulation (TTE) toolkit** — standardized TTE
   templates for drug-repurposing and comparative-effectiveness questions.
   *(Deprioritized → folded into WG-2 RWE rec + Rec 2; see also-considered.)*
5. **A variant-to-function annotation service** — standardized VEP/AlphaMissense/
   functional-genomics annotation pipeline. *(Folded into Rec 2.)*

---

## Top-3 ranked recommendations

### 1. A curated computable-phenotype & artifact gallery (versioned, attributable, upvoted)

**Description.** A Workbench-native, FAIR registry of reusable computable
phenotypes and analytic artifacts: each entry **versioned**, **attributable** to
its author/consortium, carrying its definition logic (OMOP/phecode/SNOMED value
sets), validation provenance, and a **community vetting/upvoting** signal. Solves
the problem raised in both meetings: phenotype definitions (e.g., Type 2
diabetes) are inconsistent across AoU publications, creating noise and blocking
replication. Aligns AoU with PheKB / OHDSI-Phenotype-Library practice but
makes the gallery a first-class Workbench object with usage telemetry.

**Supporting evidence.**
- Reproducibility & inconsistent-phenotype noise raised explicitly on both 05-21
  and 06-03 (`../wg-meeting-notes/`).
- Builds directly on Smoller's already-prioritized PheKB / validated-phenotypes
  (3.80) and phecodes (3.80) work (`README.md` caveats) — this is the
  *distribution and governance layer* on top of that.
- Theme 3 (methods/infrastructure/phenotyping) is the single largest orphan —
  262 pubs / 2,388 projects — and a phenotype gallery is the canonical theme-3
  artifact that an 8-area view currently makes invisible
  (`../aou-roadmap-refresh/crosswalk_19_to_8.md`).
- NLM G1-O2 (curation at scale, NLP) is the most-aligned IC ask
  (`../aou-ic-alignment/gap_analysis.md`).

**Need area.** Tooling/infrastructure with a reproducibility mandate; bridges
the translational need area (WG-2, translational reuse) and the AI need area
(WG-4, where the AI co-scientist consumes the gallery as its grounding
vocabulary). Coordinate the two.

**Rubric scores.**

| Criterion | Score | Justification |
|---|---:|---|
| Unmet researcher need | 4 | Phenotype inconsistency is a named, recurring pain point. |
| Simplifies analysis | 4 | Reuse a vetted definition instead of re-deriving one. |
| Standardizes/harmonizes | 4 | The entire point: one attributable, versioned definition per phenotype. |
| Broad use cases | 4 | Every phenotype-based study (the majority of the corpus). |
| Scientific Roadmap alignment | 4 | Slide-7 reproducibility + the proposed "Data, AI & Methods" focus area. |
| Tool exists vs new dev | 3 | PheKB / OHDSI libraries exist; the Workbench-native, upvoted, telemetry-bearing gallery is new integration. |
| No new data collection | 4 | Operates on existing data + definitions. |
| Helps with data quality | 4 | Directly reduces phenotype-definition variance — a primary data-quality lever. |
| **Mean (applicable only)** | **3.88** | |

**Risks / pushback.** "Who curates / who vets?" — answer: community upvoting +
a light editorial board, modeled on PheKB; attribution incentivizes
contribution. "Isn't this PheKB?" — answer: PheKB is external and unversioned in
the Workbench; this makes the artifact native, versioned, and telemetered.

---

### 2. An integrated biomedical knowledge-base layer for agentic follow-up

**Description.** Connect a curated set of **highest-quality external biomedical
databases** to the Workbench so that, given an AoU finding, researchers can
prioritize and follow up **without exporting data**: drug mechanism-of-action /
target databases (to generate repurposing-candidate lists for a target-trial
emulation), gene–disease and variant-to-function resources (to map a discovered
variant to mechanism), and pathway/MoA references. Exposed as governed,
queryable reference data + an API the WG-4 AI co-scientist can call as a
grounded tool. This is the direct answer to Jordan's "low-hanging fruit:
integrate the highest-quality biomedical databases" point.

**Supporting evidence.**
- The explicit 06-03 use cases: drug-repurposing-for-depression candidate lists
  → target-trial emulation; variant → function mapping.
- Pairs with WG-2's RWE / NCATS-Translator linkage rec (`wg2_translational.md`
  candidate 4/6) — Translator and the Monarch KG are exactly the curated
  gene/disease/drug knowledge graphs this layer would surface; reuse, don't
  rebuild.
- Disease-burden direction (`../disease-burden/burden_vs_attention.md`): point
  repurposing/TTE capability at high-burden, under-attended conditions so AoU
  acts as a burden-corrective.
- NASEM *Generative AI in Health and Medicine* frames agentic database
  integration as a near-term transformative opportunity
  (`../strategic-plans/nasem/README.md`).

**Need area.** Database integration + agentic-tool surface is tooling, not
clinical translation; the *outputs* (repurposing hypotheses, variant calls)
are coordinated with the translational need area (WG-2).

**Rubric scores.**

| Criterion | Score | Justification |
|---|---:|---|
| Unmet researcher need | 4 | "Take data outside AoU and run my favorite tool" is the status quo this removes. |
| Simplifies analysis | 4 | Follow-up analysis runs in place, agentically. |
| Standardizes/harmonizes | 3 | Standardizes *which* reference resources are canonical; less about AoU data harmonization. |
| Broad use cases | 3 | High value for genetics/pharmacology/repurposing; less for pure-EHR studies. |
| Scientific Roadmap alignment | 4 | Slide-7 AI/agentic + drug-repurposing/TTE priorities. |
| Tool exists vs new dev | 3 | The external DBs (Translator, Monarch KG, DrugBank-class, AlphaMissense, etc.) exist; the governed in-Workbench integration + agent API is new. |
| No new data collection | 4 | Integrates existing external knowledge; no participant data collection. |
| Helps with data quality | 3 | Canonical references reduce ad-hoc annotation variance. |
| **Mean (applicable only)** | **3.50** | |

**Risks / pushback.** "Licensing / curation burden of external DBs" — answer:
start with open, federally-funded knowledge graphs (NCATS Translator, Monarch
KG) before commercial sources. "Consent for new data from ancillary studies
(e.g., iPSCs)?" — flagged on 06-03 as an open question; this rec covers
*reference-knowledge* integration only, not new-data generation — keep the iPSC
consent question as a separate WG-2/ELSI item.

---

### 3. A vetted, security-reviewed external-tool & data integration framework

**Description.** An explicit, published process and **allow-list** governing
which third-party tools, packages, and reference databases may be installed or
queried in the Workbench, with a security/privacy review gate. Resolves the
06-03 discussion about "what tools are and are not allowed in the workbench" —
turning an ad-hoc, opaque constraint into a transparent intake process that
researchers (and Recs 1–2) can plan around.

**Supporting evidence.**
- 06-03 security/privacy discussion: the constraint exists but is undocumented;
  researchers don't know what's permitted.
- Recs 1 and 2 both *require* a sanctioned integration path — without this
  framework they have no governed way to ship.
- NASEM *An AI Code of Conduct for Health and Medicine*
  (`../strategic-plans/nasem/README.md`) provides the external governance
  template; pairs with WG-4's AI-governance rec (`wg4_ai_strategies.md` Rec 2).

**Need area.** It is the enabling substrate for all tooling recs and the
home for the workbench-security question across these need areas.

**Rubric scores.**

| Criterion | Score | Justification |
|---|---:|---|
| Unmet researcher need | 3 | Pain is "I don't know what I'm allowed to use," not a feature request. |
| Simplifies analysis | 2 | Adds a governance step; simplifies indirectly via predictability. |
| Standardizes/harmonizes | 4 | Establishes the canonical tool/data allow-list. |
| Broad use cases | 4 | Governs every external tool/DB any researcher wants. |
| Scientific Roadmap alignment | 3 | Enabling infrastructure for slide-7 AI/tooling priorities. |
| Tool exists vs new dev | 3 | Security-review processes exist generally; the published Workbench allow-list + intake is new. |
| No new data collection | 4 | Governance only. |
| Helps with data quality | 3 | Vetting external reference tools reduces low-quality-tool contamination. |
| **Mean (applicable only)** | **3.25** | |

**Risks / pushback.** "This slows researchers down" — answer: the *absence* of a
published process already slows them down opaquely; a transparent allow-list is
faster in practice. "Security owns this, not a science WG" — answer: the WG
specifies the *scientific* intake criteria; security owns the review gate. Joint.

---

## Also-considered (deprioritized with reasoning)

- **In-Workbench target-trial-emulation toolkit (candidate 4).** Strong and
  directly requested, but TTE is the canonical WG-2 RWE deliverable
  (`wg2_translational.md` candidate 6). Surface it as a *use case* powered by
  Rec 2's knowledge-base layer rather than a standalone tooling rec, to avoid a
  WG-2/WG-4 turf duplication.
- **Standalone variant-to-function annotation service (candidate 5).** Folded
  into Rec 2 — it is one of the knowledge-base integrations, not a separate
  program.
- **iPSC / ancillary-study new-data generation.** Raised 06-03 ("are they
  covered in our consent?") but this is a consent/ELSI and data-generation
  question, not a tooling recommendation — routed to WG-2 / ELSI, noted in the
  meeting log.

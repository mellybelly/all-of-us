# LLM availability, BAAs, and data egress on the Researcher Workbench — evidence brief

Research date: 2026-06-27. This brief assembles **publicly documented** facts on
whether/how LLMs can be used in the AoU Researcher Workbench (RW) and comparator
platforms. Claims are tagged **[confirmed] / [likely] / [unknown]** with sources;
several load-bearing items need primary-source verification before external use
(see "Verify before relying").

## Direct answer: is "no BAA" why there's no easily-usable LLM in the RW?

**Not exactly — the BAA is not the binding constraint.** The picture as of mid-2026:

1. **The Google Cloud BAA already covers an in-environment Google LLM.** Vertex
   AI / Gemini (Google's enterprise generative-AI platform) is on Google Cloud's
   **HIPAA-covered services** list ([cloud.google.com/security/compliance/hipaa](https://cloud.google.com/security/compliance/hipaa),
   updated 2026-05-15) **[confirmed]**. The AoU RW runs on Google Cloud (Verily
   Workbench lineage), so a model invoked **in-VPC** keeps data inside the same
   trust boundary — processing-in-place, not an export. So at the legal/BAA layer
   there is **no barrier** to an in-environment Gemini/Vertex model.

2. **The binding constraint is the platform's own data-egress / data-use rules**,
   not the BAA. The Data User Code of Conduct (DUCC) prohibits removing any
   participant-level data from the Workbench and bars sharing aggregates for
   <20 participants ([AoU DUCC v4](https://support.researchallofus.org/hc/en-us/articles/22346176432532-Data-User-Code-of-Conduct)) **[confirmed]**.
   That rule — plus egress monitoring/alerts — is what blocks sending data to
   **external** LLM APIs, regardless of any BAA.

3. **The RW *does* now ship LLM tooling — but bring-your-own-key.** RW 2.0
   (Verily Workbench; beta Jan 2026, rollout Q1 2026) pre-installs **Claude Code
   and Gemini CLI** on cloud apps, authenticated with the **researcher's own**
   Anthropic/Google credentials ([Verily Workbench "Use Claude and Gemini"](https://support.workbench.verily.com/docs/guides/cloud_apps/ai_tools/))
   **[confirmed at platform level; AoU-enablement likely]**. Because they run on
   the *user's own* account, they operate under the user's commercial terms —
   **not** an AoU/program BAA. So feeding participant-level data through the BYO
   CLI would be **both** a DUCC violation **and** outside any BAA. They're fine
   for code help, not for putting data through.

**So the real gap is not "no BAA" — it's that AoU has not stood up an
*approved, in-VPC, program-credentialed* LLM (e.g., Gemini via Vertex under the
program's GCP BAA, with controlled retention/logging) that researchers could use
*on the data* compliantly.** A BYO-key CLI exists; a governed in-environment
model service does not (as far as public docs show) **[likely; not found]**.

## AoU RW current state (RW 2.0 / Verily Workbench)

| Item | Finding | Confidence |
| --- | --- | --- |
| In-env LLM tooling | Claude Code + Gemini CLI pre-installed, **BYO API key** ([Verily docs](https://support.workbench.verily.com/docs/guides/cloud_apps/ai_tools/)) | confirmed (platform) |
| First-party "AI co-scientist" | None found | likely none |
| GPUs | NVIDIA **H100 / H200 / B200**; NeMo (LLM/genAI), Parabricks, CUDA-X ([Verily/NVIDIA, Oct 28 2025](https://verily.com/perspectives/verily-nvidia-ai-workbench)) | confirmed |
| Open-weight model training | Supported (NeMo Automodel benchmarks vs HF Accelerate) | confirmed |
| Egress — interactive notebooks | Retain internet (can install packages / call external resources) | confirmed (platform) |
| Egress — batch/Dataproc under network policy | Outbound blocked except Google APIs | confirmed (platform) |
| Binding data rule | DUCC: no participant-level extraction; <20 aggregate suppression; uploaded software logged | confirmed |
| Program BAA over RW / over Vertex-Gemini | Not publicly documented | unknown |
| AoU guidance on AI tool use with data | Not found | unknown |
| Security posture | "Exceeds FISMA Moderate"; data-passport model; institutional DURA | confirmed |

Platform note: AoU is mid-migration from the legacy Terra-based RW to **RW 2.0
"powered by Verily Pre"** (Verily↔VUMC 5-yr extension, Jun 26 2025). Some AI/GPU
features are documented at the Verily platform level; exact AoU-collection
enablement of each should be confirmed in-environment.

## Comparator platforms (front-runs Part 1)

| Platform | In-env LLM / genAI | Egress model | GPU / AI compute | Notable collaboration / reuse |
| --- | --- | --- | --- | --- |
| **AoU RW 2.0** (Verily/GCP) | Claude Code + Gemini CLI (**BYO key**); no governed in-VPC model found | **Closed**: DUCC no participant-level export, <20 rule; notebooks keep internet | H100/H200/B200; NeMo, Parabricks | Workspace cloning; **~86% solo, 3.7% multi-institution** (this corpus); no public reuse/registry surfaced |
| **N3C Enclave** (Palantir Foundry/AWS) | **Unknown** — Foundry AIP exists; no evidence NCATS enabled it | **Closed**: no row-level download; reviewed aggregate egress (DRR), ≥20 | CPU/Spark confirmed; **GPU unknown** | **Strong**: Logic Liaison Fact Tables, Concept Set Builder + "N3C Recommended" sets (Zenodo DOIs), Knowledge Store, auto data-lineage |
| **Terra / AnVIL** (Broad/GCP-Azure) | None shipped; genAI **planned** (Broad–Manifold, Jan 2025); Azure OpenAI optional outbound | **Open**: download allowed; control is economic (downloader pays) | T4/P4/V100; Dataproc Spark + Hail | Shared workspaces (roles), WDL/Cromwell, **Dockstore "Launch with Terra"**, Featured Workspaces |
| **BioData Catalyst** (Gen3+PIC-SURE+SevenBridges+Terra+Dockstore) | None found (RHEO = workflow automation) | **Compute-to-data**; authorized dbGaP download paths exist; FISMA ATOs | V100 / L40S (Seven Bridges); Spark/Hail | **Dockstore** registry, **PIC-SURE** cohort building + handoff, DOIs/provenance |
| **UKB-RAP** (DNAnexus/AWS) | None *in-RAP* (DNAnexus launched GenAI tools May 2026; RAP availability unconfirmed) | **Closed**: no individual-level download; WGS/WES never; export monitored | T4/A10G/L4/A100 | Apps/applets, publishable global workflows, **Smart Reuse** (job-output reuse) |
| **Kids First / Cavatica** (Gen3+Velsera/AWS) | None native (BYO ML) | **Open** within dbGaP-gated access; optional irreversible download lock | P2/P3/G4dn/G5/G6 | **Public Apps Gallery** (CWL tools), public interactive analyses, WDL/CWL |

**Cross-platform reads:**
- **In-environment generative AI is rare everywhere** — only the AoU RW (via BYO-key CLIs) and *planned* Terra/Manifold are close; N3C/BDC/UKB-RAP/Kids First show none in-environment. So this is an industry-wide gap, and an opportunity for AoU to lead with a *governed* in-VPC model rather than BYO-key.
- **Egress models differ sharply:** closed (AoU, N3C, UKB-RAP) vs open (Terra/AnVIL, Kids First) vs compute-to-data (BDC). AoU is in the strict-closed camp.
- **Reuse/registry features are where comparators clearly exceed AoU:** N3C (Concept Set Browser, Logic Liaison Fact Tables, Knowledge Store), Terra/BDC/Kids First (**Dockstore** / Public Apps Gallery tool registries), UKB-RAP (Smart Reuse). The AoU RW has no comparable public tool/workflow registry surfaced — consistent with the reuse signals in `part2_trending_methods.md`.

## Cloud-LLM BAA mechanics (the factual landscape)

| Path | HIPAA/BAA status | Source |
| --- | --- | --- |
| **Google Vertex AI / Gemini** (enterprise) | Covered under Google Cloud BAA (consumer Gemini app is NOT) | [GCP HIPAA list](https://cloud.google.com/security/compliance/hipaa), 2026-05-15 [confirmed] |
| **AWS Bedrock** (Claude, etc.) | Bedrock HIPAA-eligible under AWS BAA; review each model's terms | [AWS HIPAA-eligible services](https://aws.amazon.com/compliance/hipaa-eligible-services-reference/), 2026-05-22 [confirmed] |
| **Claude on Vertex / Bedrock** | Covered via the cloud BAA (model available in Model Garden / Bedrock) | [confirmed avail; BAA scope via cloud service] |
| **Anthropic 1P API** | BAA available; "Covered Models" require 30-day retention (not ZDR, except Claude Code) | Anthropic support BAA docs [confirmed] |
| **Azure OpenAI** | Microsoft BAA auto-included; service in-scope widely reported | [MS HIPAA offering](https://learn.microsoft.com/azure/compliance/offerings/offering-hipaa-us) [likely] |
| **OpenAI 1P API** | BAA via Healthcare Addendum; only Zero-Retention API + ChatGPT Enterprise eligible | [OpenAI healthcare addendum](https://cdn.openai.com/osa/healthcare-addendum.pdf), 2024-11-11 [confirmed] |

**Implication for AoU:** because the RW is on Google Cloud, the lowest-friction
compliant path to an LLM *on the data* is an **in-VPC Vertex/Gemini model under
the program's existing GCP BAA**, with retention/logging configured so nothing
leaves the boundary — no new vendor BAA required. The work is governance +
provisioning, not a fundamental legal blocker.

## Verify before relying (primary-source checks)
1. Whether the AoU data collection enables Verily's "network policy" and the exact config.
2. Whether AoU has any in-VPC, program-credentialed LLM (vs only BYO-key CLIs) and any AI-use guidance.
3. N3C: whether Palantir AIP / any in-enclave LLM is enabled; whether GPUs are provisioned.
4. The exact GCP-BAA covered-services line for the specific Gemini/Claude endpoint.
5. AoU workspace AI-adoption numbers (`part2_trending_methods.md`) predate RW 2.0's AI tooling — re-measure after RW 2.0 GA.

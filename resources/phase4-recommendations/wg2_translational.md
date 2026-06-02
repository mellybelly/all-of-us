# WG-2: Translational Science Research Agenda

## Lead(s) and scope

**Co-leads:** Sanchez & Cohn.
**Scope (per 2026 WG deck):** define the discovery-to-impact translational
pathway for AoU science — what counts as translational impact, what
priority use cases the program should drive toward, and how to measure
translational outcomes.

This WG bridges WG-1 (Refresh content) with WG-5 (Communications / impact
measurement). Their recommendations need to interlock with both.

---

## Candidate recommendations evaluated

1. **A formal AoU translational-impact metric set** built on the
   Translational Science Benefits Model (TSBM): replication studies,
   partner-cohort adoption, clinical-trial enablement, FDA/CMS/regulatory
   citations, payer / health-system policy citations.
2. **Prioritize 3–5 named translational use cases** (a working portfolio):
   rare-disease ACMG implementation; multi-ancestry PRS clinical
   pilots; PGx implementation; cardiometabolic risk-stratification
   in primary care; cancer screening intensity by SDOH.
3. **A bias-in-translation framework** — operational guidance for
   AoU-derived models intended to be deployed in clinical/regulatory
   settings, leveraging AoU's UBR-oversample as the de-facto pan-NIH
   diversity benchmark.
4. **NCATS-Translator data-linkage roadmap** — surface AoU as a named
   data source for NCATS Translator and other federated KG ecosystems,
   noting downstream Monarch/Translator dependency.
5. **Establish a translational replication pipeline** with MVP, UKB,
   FinnGen, CKB for headline discoveries (partner-cohort cross-validation
   as a routine deliverable).
6. **Real-world-evidence (RWE) framework for post-approval drug surveillance**
   building on HA8 (breakthrough therapeutics) signal — GLP-1, SGLT2, AD
   mAbs, CRISPR.

---

## Top-3 ranked recommendations

### 1. Adopt a formal translational-impact metric set (TSBM-based)

**Description.** Define and adopt a small, defensible set of translational-
impact metrics that AoU will report annually: (1) replication / triangulation
in partner cohorts (UKB/MVP/FinnGen/CKB cross-validation); (2)
adoption-by-name in clinical-research consortia (RDCRN, ClinGen, GREGoR,
INCLUDE DCC, eMERGE, ClinVar/MedGen); (3) regulatory citations (FDA approval
decisions, label changes, CMS coverage decisions); (4) clinical-trial
enablement (NCT records that cite AoU as data source or design input); (5)
policy citations (CDC, USPSTF, NAM reports). Metric set drives WG-5
impact-tracking deliverables.

**Supporting evidence.**
- 31 AoU AI/foundation-model pubs in HA4 already exist (e.g., PMID:39794311,
  PMID:40417537) — translational impact is being generated but not measured.
- HA8 breakthrough-therapeutics pubs (16 total; PMID:41847743 GLP-1 hepatic
  decompensation; PMID:41807852 third-line CRC cost-effectiveness;
  PMID:41741949 obesity-medication / bariatric trends) are exactly the
  post-approval pharmacoepidemiology Sci Com anticipated — and the value
  is invisible without measurement.
- NIH-Wide Crosscutting Theme 4 (Collaborative Science) and NCATS G4
  (crosscutting translational strategies, partnerships) name partnership /
  replication as priorities.
- NIMHD G4 (methods, metrics, measures, tools) explicitly calls for
  improved methods/metrics in disparities-relevant research — AoU
  translational metrics inherit this.

**Why this WG.** WG-2 owns the translational frame. WG-5 owns dissemination
mechanics. The metric *definition* is upstream of dissemination and is
WG-2's natural deliverable; the *operationalization* is shared with WG-5.

**Rubric scores.**

| Criterion | Score | Justification |
|---|---:|---|
| Unmet researcher need | 3 | Researchers need a clear definition of translational success — currently undefined. |
| Simplifies analysis | 2 | Metric definition isn't an analysis simplifier per se. |
| Standardizes/harmonizes | 4 | Standardizes what "translational impact" means across AoU science. |
| Broad use cases | 4 | Covers every disease area and every research output type. |
| Scientific Roadmap alignment | 4 | Translational outcomes are slide-7's "what's changed" question — answered with measurement. |
| Tool exists vs new dev | 4 | TSBM is a published framework (Luke et al., Eval Program Plan 2018); altmetric / NIH RePORTER / NCT have APIs. Curation is the new work. |
| No new data collection | 4 | Measurement of existing output streams. |
| Helps with data quality | 3 | Indirect: tracking replication catches data-quality issues. |
| **Mean (applicable only)** | **3.50** | |

**Risks / pushback expected.** Sci Com may ask "how does this differ from
citation count / altmetric?" — answer: TSBM operationalizes *clinical and
policy use*, not just academic citation. Some may worry about under-counting
work that hasn't translated yet — frame metrics as **lagging indicators of a
healthy program**, not pass/fail.

---

### 2. Name 3–5 priority translational use cases and commit to portfolio reporting

**Description.** Identify a small portfolio of named translational use
cases that AoU explicitly drives toward and reports against. Candidates:
**(a)** rare-disease ACMG actionable-gene implementation (54 pubs / 433
projects, NHGRI BP6/BP7, NCATS G3); **(b)** multi-ancestry PRS clinical
pilots (theme 2 surge +17.0, NHGRI BP9); **(c)** PGx implementation
(theme 16, AoU peer-index 4.6× over peer median); **(d)** cardiometabolic
risk-stratification with SDOH (382 pubs / 3,292 projects, NIDDK + NHLBI);
**(e)** RWE for breakthrough therapeutics (HA8 16 pubs).

**Supporting evidence.**
- Rare disease: 54 pubs / 433 projects; NHGRI BP6/BP7 and NCATS-G3 both
  ask for this. AoU's unselected-population penetrance estimates
  (PMID:42170804) are a unique contribution.
- PRS: theme 2 (+17.0 trend) is the single biggest gainer in the corpus;
  NHGRI Bold Prediction #9 directly maps. Subcontinental ancestry work
  (PMID:40480197) puts AoU ahead of generic multi-ancestry framing.
- PGx: AoU 2.3% share vs peer median 0.5% (4.6× over) — a *distinctive
  AoU strength* that under-published given the cohort's structural fit.
  NIGMS-G4 (PGRN priority); NCATS Translator data consumer.
- Cardiometabolic + SDOH: 382 disease pubs and 458 SDOH pubs combine — the
  CKM-syndrome integration NHLBI and NIDDK both want.
- HA8 breakthrough-therapeutics is the clearest "translation in progress"
  signal in the corpus (15 of 16 pubs post-2023).

**Why this WG.** Selecting a small portfolio with reportable outcomes is the
canonical translational-WG deliverable; WG-2 owns use-case prioritization
while WG-1 owns the framework that contains them.

**Rubric scores.**

| Criterion | Score | Justification |
|---|---:|---|
| Unmet researcher need | 3 | Researchers want to know "what counts as translational?" — a named portfolio answers this. |
| Simplifies analysis | 2 | Portfolio selection is strategic, not analytical. |
| Standardizes/harmonizes | 3 | Standardizes program-level reporting; lower harmonization at researcher level. |
| Broad use cases | 4 | Portfolio of 3–5 covers most translation paths from AoU outputs. |
| Scientific Roadmap alignment | 4 | Direct deliverable for the Refresh — names what AoU is *for* translationally. |
| Tool exists vs new dev | 4 | Use cases all already have corpus activity; this is selection, not building. |
| No new data collection | 4 | All on existing AoU data. |
| Helps with data quality | 3 | Named use cases drive QC investment toward the data those use cases depend on. |
| **Mean (applicable only)** | **3.38** | |

**Risks / pushback expected.** "Why these five, not those five?" — defend
by tying each use case to *both* a peer-index strength (PGx, theme 2) and
an aligned-IC priority. Sci Com may want to add a sixth (cancer
disparities is a natural addition); the WG should hold the line at 5 to
preserve focus.

---

### 3. AoU as the de-facto pan-NIH diversity benchmark — a bias-in-translation framework

**Description.** Develop operational guidance for AoU-derived models and
findings entering clinical/regulatory pathways, leveraging the UBR
oversample as a *reportable* diversity benchmark: (a) require AoU-derived
predictive models published in AoU corpus to report performance by ancestry
group (continental + subcontinental), socioeconomic stratum, and rural/urban
status; (b) provide a standard "AoU bias-audit template" researchers run
before submitting for regulatory or clinical-system adoption; (c) establish
AoU as the citable diversity reference in FDA/CMS submissions.

**Supporting evidence.**
- Theme 6 (SDOH/disparities): 458 pubs / 3,070 projects — 33.3% of corpus
  (peer median 6.5%; 5.1× over-index — `aou_vs_peers_index.csv`).
- ELSI theme 17 peer-index 21.2× — AoU's distinctive contribution is
  *built on* an engagement and equity infrastructure peers don't have.
- NHGRI Bold Prediction #4 (move beyond race-based descriptors) explicitly
  asks for the methodology AoU is uniquely positioned to deliver.
- NIMHD Goal 7 (analysis of HD populations in big data) + Leap Forward
  Research Challenge — the cohort is *the literal answer* to this ask.
- HA6 (G×E×SDOH integrated): 10 post-2023 pubs, 0 pre-2023 — a *genuinely
  novel* category AoU is positioned to lead. Examples: PMID:41518215 (PRS
  + neighborhood disorder + sleep duration); PMID:42109163 (CoQ10 PRS +
  statin myopathy).
- FDA Modernization Act 2.0 and ongoing FDA diversity-action-plan
  rule-making (21st Century Cures, Diversity Plans Guidance) create a
  regulatory window for an AoU-anchored bias framework.

**Why this WG.** Translational outputs are where bias becomes operational
harm; WG-2 is the natural home. WG-4 (AI Strategies) will pick up the
technical implementation, but the *normative framework* lives in WG-2.

**Rubric scores.**

| Criterion | Score | Justification |
|---|---:|---|
| Unmet researcher need | 4 | Researchers building AoU-derived models lack a clear bias-reporting standard; FDA/CMS reviewers lack a reference standard. |
| Simplifies analysis | 3 | A template/audit standardizes a currently-bespoke step. |
| Standardizes/harmonizes | 4 | The whole point: standardize how AoU-derived translational products report bias. |
| Broad use cases | 4 | Every AoU translational product. |
| Scientific Roadmap alignment | 4 | Aligns with FA7 Health Equity (load-bearing) and the cross-cutting NIH disparities theme. |
| Tool exists vs new dev | 3 | NIH disparities-reporting templates exist (NIMHD); FDA diversity action plans exist. AoU-specific template is new packaging. |
| No new data collection | 4 | Uses existing AoU data and existing demographic variables. |
| Helps with data quality | 4 | Bias audit catches representation and sampling-quality issues; directly improves comparative validity. |
| **Mean (applicable only)** | **3.75** | |

**Risks / pushback expected.** "Is this a research framework or a regulatory
framework?" — answer: both, but the *normative* claim is research (AoU
defines the benchmark). Some Sci Com members may worry about over-reach
into FDA/CMS territory; defend by framing AoU as the *reference cohort* not
the *regulator*. The 21.2× ELSI over-index is the political-defense argument.

---

## Also-considered (deprioritized with reasoning)

- **NCATS-Translator data-linkage roadmap (candidate 4).** Real and
  defensible (NCATS plan G4-O4-3 names data-science standards; Translator
  Program is a downstream consumer per the gap_analysis NCATS brief).
  Deprioritized because (a) NCATS positioning is delicate per project
  guidance — frame as downstream dependency, not anchor; and (b) the
  recommendation is more an *infrastructure linkage* than a translational-
  agenda statement. Surface in cross-cutting synthesis.
- **Partner-cohort replication pipeline (candidate 5).** Strong idea but
  already implicitly covered by Recommendation 1 (metric #1 replication
  and triangulation). Treating it as separate dilutes the headline.
- **RWE post-approval surveillance (candidate 6).** Strong evidence base
  (HA8) but better held as one named use case inside Recommendation 2
  rather than as standalone Top-3.

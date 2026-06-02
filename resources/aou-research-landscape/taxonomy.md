# All of Us Research Landscape — Unified Theme Taxonomy (Locked)

This is the locked topical taxonomy spanning the 1,378 publications and 12,899
filtered project workspaces in the AoU research corpus. It was developed by
sampling ~200 records (stratified across pubs/projects, years, and access
tiers), drafting an initial taxonomy, validating against an independent
~100-record sample, and then locking after Phase 2c user decisions.

## Locked decisions applied (vs. draft)

The 7 open user-decisions at the bottom of the original draft have been
resolved as follows; each is binding for the Phase 2c tagging pass and
downstream IC-comparison work:

1. **Dermatology — keep as its own theme (theme 12).** Not folded into
   Autoimmune or Cancer.
2. **Wearables — keep as its own top-level theme (theme 7).** Not folded into
   Methods.
3. **Pharmacogenomics — keep as its own top-level theme (theme 16).** Not
   folded into Genomics; the IC alignment is too distinctive (NIGMS PGRN,
   NHLBI, NCI by drug class).
4. **ELSI / engagement split into TWO buckets.** Theme 17 is now
   `ELSI-research` (substantive ELSI / consent / engagement / recruitment
   research — counted in theme shares). Records that are *about AoU itself*
   (program-introduction pubs, "year in review," interviews with leadership,
   AoU governance descriptions) go into a NEW audit-only bucket
   `AoU-program-meta-audit` (theme code `META`) that is NOT counted in theme
   shares. A pub that uses AoU data substantively even while also describing
   AoU stays in the substantive corpus.
5. **Stroke — multi-tag both Cardiometabolic (1) AND Neurology (14).** Don't
   pick one. Subtheme 1.4 (atherosclerotic / valvular / AF / cardio-embolic
   stroke) and 14.2 (cerebrovascular / non-cardio-embolic stroke) both
   apply when the record warrants; default is to tag both top-levels.
6. **CKM Syndrome — keep as a subtheme of Cardiometabolic (1.3-CKM), with
   explicit subtheme tagging** so it's trackable against the NHLBI/NIDDK
   strategic plans without becoming its own top-level.
7. **AoU-meta pubs — into the `AoU-program-meta-audit` bucket**, separated
   from the substantive corpus. (Same as #4 above.)

**Working taxonomy: 19 top-level themes + 1 audit-only bucket (`META`).**

Theme-share denominators reported downstream use only the substantive corpus
(themes 1–19); `META` records are reported separately so the program can see
how much of the publication record is self-descriptive.

The taxonomy is intentionally **disease/topic-anchored** rather than methods-
anchored, because comparison against NIH IC strategic plans is the downstream
goal and ICs are mission-organized. Methods themes (genomics methods,
phenotyping, AI/ML) are preserved as their own top-level branch because they
constitute roughly a quarter of the corpus and don't reduce cleanly into
disease ICs.

**Important: records will typically tag with 2–4 themes.** A pub on
"polygenic susceptibility to hypertension and stroke risk in AoU" hits both
Cardiometabolic and Genomics-methods; a project on "BRCA1/2 GxE for breast
cancer in diverse populations" hits Cancer, Genomics-methods, and SDOH. The
fraction estimates below are share-of-corpus-touched, not mutually exclusive
shares.

## Top-level themes (rough fraction of corpus that touches the theme)

| # | Top-level theme | Share | Notes |
|---|---|---:|---|
| 1 | Cardiometabolic disease | ~22% | Largest disease area |
| 2 | Genomics methods & complex-trait genetics | ~28% | Largest methods area; transverse to most disease themes |
| 3 | Methods, infrastructure & phenotyping (non-genomic) | ~20% | EHR phenotyping, ML/AI, data quality, workbench tooling |
| 4 | Mental health, behavioral & substance use | ~18% | Includes wellbeing, loneliness, stress, sleep-as-behavior |
| 5 | Cancer | ~15% | All sites + survivorship + screening |
| 6 | Social determinants & health disparities | ~15% | Cross-cuts most disease themes |
| 7 | Wearables & digital health | ~8% | Fitbit, activity, sleep-tracker data |
| 8 | Infectious disease & immunology | ~6% | HIV, COVID, EBV, virome, vaccines |
| 9 | Autoimmune & inflammatory disease | ~6% | RA, SLE, IBD, psoriasis-as-autoimmune |
| 10 | Rare disease & Mendelian genetics | ~6% | ACMG variants, hereditary cancer, monogenic |
| 11 | Aging, frailty & ADRD | ~5% | AD/ADRD, frailty, healthy aging, PD |
| 12 | Dermatology | ~5% | Anomalously large — likely 1–2 prolific groups (see README) |
| 13 | Respiratory & sleep medicine | ~4% | Asthma, COPD, OSA, sleep disorders |
| 14 | Neurology (non-ADRD) | ~4% | Stroke, epilepsy, headache, TBI, MS |
| 15 | Pregnancy, maternal & women's health | ~4% | Pregnancy outcomes, gynecologic conditions |
| 16 | Pharmacogenomics & drug response | ~4% | Mostly genomics-by-drug |
| 17 | ELSI, participant engagement & recruitment | ~3% | Includes AoU-program-introduction pubs |
| 18 | Ophthalmology, ENT & sensory medicine | ~3% | Eye/hearing/voice; high disparities focus |
| 19 | Environmental health & climate | ~2% | Smallest disease theme; emerging |

Coverage of the corpus by at least one theme: estimated >95% (residual ~5%
includes very-short projects, generic "exploratory" workspaces, and pure
biostatistical-methods pubs that don't bind to any disease area).

Below: each top-level theme with definition, subthemes, indicative keywords,
and 3–5 example records (with PMID or workspaceId).

---

## 1. Cardiometabolic disease (~22%)

**Definition.** Studies of cardiovascular disease, kidney disease, metabolic
disease, and the increasingly-unified Cardiovascular-Kidney-Metabolic (CKM)
syndrome. Includes type 1/2 diabetes, obesity (as a disease — distinct from
"obesity-as-lifestyle"), dyslipidemia, hypertension, heart failure, atrial
fibrillation, stroke (cardio-embolic), MASLD/MASH/NAFLD/NASH, coronary
artery disease.

**Indicative keywords.** cardiovascular, hypertension, blood pressure, type 2
diabetes, T2D, obesity, BMI, cholesterol, LDL, HDL, atrial fibrillation, AF,
heart failure, ejection fraction, stroke, coronary, CAD, CKM syndrome,
MASLD, NAFLD, GLP-1, SGLT2, statin, beta-blocker, kidney disease, CKD,
aortic stenosis.

**Subthemes (~5).**
- 1.1 Hypertension & blood-pressure control
- 1.2 Type 1/2 diabetes & glycemic control
- 1.3 Obesity, GLP-1/SGLT2 therapeutics & cardiometabolic syndrome
- 1.4 Atherosclerotic & valvular heart disease (CAD, AS, HF, AF)
- 1.5 Chronic kidney disease & cardio-renal interactions

**Example records.**
- PMID:40130972 — "Associations between Class I, II, or III Obesity and Health Outcomes" (*NEJM Evidence* 2025)
- PMID:42028610 — "Long-Term Efficacy and Safety of GLP-1R Agonist and SGLT2 Inhibitor Therapy in the General Population: A Mendelian Randomization Study" (*Circulation Genomic Precision Medicine* 2026)
- PMID:40827941 — "Polygenic Resistance to Blood Pressure Treatment and Stroke Risk" (*Annals of Neurology* 2025)
- PMID:39222019 — "Rare Genetic Variants in LDLR, APOB, and PCSK9 Are Associated With Aortic Stenosis" (*Circulation* 2024)
- workspace:32979 — "Adrenalectomy V8" (primary aldosteronism, GWAS for cure prediction)
- workspace:25456 — "v8-Investigating obesity related health outcomes, social determinants"

---

## 2. Genomics methods & complex-trait genetics (~28%)

**Definition.** Population-genomics studies and methods development: GWAS,
PheWAS, polygenic risk scores, fine-mapping, rare-variant burden tests,
multi-ancestry methods, whole-genome / long-read sequencing analytics, repeat
expansion calling, identity-by-descent, ancestry inference. Both methods
pubs AND disease-genetics pubs whose primary contribution is genomic
discovery land here.

**Indicative keywords.** GWAS, PheWAS, polygenic risk score, PRS, polygenic
liability, fine-mapping, rare variant, burden test, SAIGE, REGENIE, Hail,
PLINK, whole-genome sequencing, WGS, long-read, HiFi, ancestry, admixture,
gnomAD, ClinVar, multi-ancestry, sub-continental, tandem repeat, IBD,
LD-score, Mendelian randomization, MR, structural variant, SV.

**Subthemes (~5).**
- 2.1 Multi-ancestry GWAS & disease-risk loci discovery
- 2.2 Polygenic risk scores — methods, portability across ancestries, clinical utility
- 2.3 Rare-variant & structural-variant association (incl. long-read)
- 2.4 Ancestry inference, admixture & subcontinental variation
- 2.5 Method development (federated learning, imputation, fine-mapping, phasing)

**Example records.**
- PMID:40691406 — "Improved multiancestry fine-mapping identifies cis-regulatory variants underlying molecular traits and disease risk" (*Nature Genetics* 2025)
- PMID:39627187 — "A phenome-wide association study of tandem repeat variation in 168,554 individuals from the UK Biobank" (*Nat Commun* 2024)
- PMID:41266648 — "Scalable and accurate rare variant meta-analysis with Meta-SAIGE" (*Nature Genetics* 2025)
- PMID:40480197 — "Subcontinental genetic variation in the All of Us Research Program" (*AJHG* 2025)
- PMID:38281971 — "Utility of long-read sequencing for All of Us" (*Nat Commun* 2024)
- workspace:29666 — "Improving prediction of outcomes from the DNA" (federated learning + PRS)

---

## 3. Methods, infrastructure & phenotyping (non-genomic) (~20%)

**Definition.** Computable-phenotype algorithms; EHR data-quality work;
machine-learning / AI on AoU data; AoU workbench tooling (R packages,
notebooks, toolkits); cohort-construction methods; missing-data and noise
handling; deidentification & privacy; harmonization with OMOP / FHIR / N3C;
synthetic-data; library / training resources.

**Indicative keywords.** phenotyping algorithm, phecode, PhecodeX, computable
phenotype, machine learning, deep learning, AI, EHR data quality, missing
data, imputation, OMOP, FHIR, SNOMED, ICD, N3C, RECOVER, allofus R package,
workbench, notebook, cohort builder, privacy-preserving, synthetic data,
data harmonization.

**Subthemes (~5).**
- 3.1 Computable phenotypes / phecode curation / case-finding algorithms
- 3.2 ML / AI for disease prediction & risk stratification on AoU data
- 3.3 EHR data quality, missingness, noise & validation
- 3.4 AoU platform tooling (R packages, notebooks, toolkits, training)
- 3.5 Data infrastructure & harmonization (OMOP, FHIR, federated learning, privacy, synthetic data)

**Example records.**
- PMID:39505999 — "Algorithms for the identification of prevalent diabetes in the All of Us Research Program validated using polygenic scores" (*Sci Reports* 2024)
- PMID:39043402 — "allofus: an R package to facilitate use of the All of Us Researcher Workbench" (*JAMIA* 2024)
- PMID:38827060 — "Development and Validation of an Individual Socioeconomic Deprivation Index in the NIH's All of Us Data Network" (*AMIA TBI* 2024)
- PMID:42004635 — "Beware the Little Foxes that Spoil the Vines: Small Inconsistencies in Clinical Data Can Distort Machine Learning Findings" (2026)
- workspace:5606 — "concordance-analysis" (variant-discordance ML predictor)
- workspace:26115 — "EHR_Wearable_v8_2025" (multimodal EHR+wearable AI)

---

## 4. Mental health, behavioral & substance use (~18%)

**Definition.** Studies of psychiatric conditions, mood disorders, anxiety,
substance use (alcohol, tobacco, e-cigarettes, cannabis, opioids,
amphetamines), suicidality, wellbeing/loneliness/meaning, stress and coping.
Includes mental-health comorbidities of physical conditions (e.g., depression
in CRS or in dysphonia) when the mental-health side is the analytic
contribution.

**Indicative keywords.** depression, MDD, anxiety, bipolar, schizophrenia,
PTSD, suicidality, mental health, psychiatric, alcohol use disorder, AUD,
smoking, tobacco, e-cigarette, cannabis, opioid, amphetamine, ketamine,
loneliness, wellbeing, well-being, stress, coping, meaning in life.

**Subthemes (~5).**
- 4.1 Mood & anxiety disorders (depression, bipolar, MDD) — epidemiology and genetics
- 4.2 Psychotic disorders, severe mental illness, treatment response
- 4.3 Substance use & addiction (alcohol, tobacco, e-cig, cannabis, opioids)
- 4.4 Wellbeing, loneliness, stress, coping & social-emotional health
- 4.5 Mental-health comorbidities of physical conditions

**Example records.**
- PMID:39362614 — "Loneliness, Discrimination, Stress, and Type 2 Diabetes Risk in Young Adults" (*Am J Prev Med* 2024)
- PMID:40007508 — "Sex-Specific Association Between Polymorphisms in ESR1 and Depression: A GWAS of AoU and UK Biobank" (*Genet Epidemiol* 2025)
- PMID:41555208 — "Dysphonia Is Associated With Anxiety and Depression in the AoU Research Program" (*Laryngoscope* 2026)
- PMID:39231067 — "Cigarette smoking, e-cigarette use, and sociodemographic correlates of mental health and tobacco-related disease risk" (*JAMIA* 2024)
- workspace:33014 — "MDD ketamine treatment: GPCR-Active Adjunct Exposures and Short-Term Outcomes"
- workspace:11494 — "Meaning and depressive symptoms"

---

## 5. Cancer (~15%)

**Definition.** Cancer epidemiology, screening, survivorship, cancer
genetics (when the analytic contribution is cancer-focused), and treatment-
response studies. All cancer sites included as subthemes.

**Indicative keywords.** cancer, carcinoma, tumor, leukemia, lymphoma,
myeloma, melanoma, sarcoma, oncology, metastasis, BRCA1, BRCA2, breast
cancer, prostate cancer, lung cancer, colorectal, HCC, hepatocellular,
pancreatic, ovarian, cervical, endometrial, renal cell, screening,
survivorship, PSA, tumor suppressor, cancer susceptibility.

**Subthemes (~6).**
- 5.1 Cancer susceptibility & hereditary cancer (BRCA, Lynch, cancer-panel)
- 5.2 Site-specific epidemiology (breast, prostate, lung, colorectal, HCC, gynecologic, hematologic)
- 5.3 Cancer screening, early detection & risk stratification
- 5.4 Cancer survivorship, quality of life & treatment outcomes
- 5.5 Cancer disparities (race/ethnicity, SES, access)
- 5.6 Pharmacogenomics of cancer therapy (overlaps with theme 16)

**Example records.**
- PMID:41881847 — "Machine learning predicts hepatocellular carcinoma risk from routine clinical data" (*Cancer Discov* 2026)
- PMID:37878135 — "Prostate-specific antigen testing rates in high-risk populations" (*Cancer Causes Control* 2023)
- PMID:38653897 — "Discrimination's Impact on Health-Related Quality of Life — Cancer Survivors" (*J Racial Ethnic Health Disp* 2024)
- workspace:35014 — "XPC Analysis Workspace" (cancer susceptibility gene variant rates in general population)
- workspace:26876 — "8q24 African Ancestry Prostate Cancer"
- workspace:34858 — "BRCA Study" (testing rate & trends)

---

## 6. Social determinants of health & health disparities (~15%)

**Definition.** Studies in which the analytic contribution is the role of
SDOH, structural inequities, demographic disparities, or differential access
in driving health outcomes. The AoU program is uniquely designed to support
this work (UBR oversampling) so this theme is large and cross-cutting.

**Indicative keywords.** social determinants of health, SDOH, discrimination,
disparities, racial disparity, ethnic disparity, income, neighborhood,
deprivation, area deprivation index, ADI, food insecurity, housing,
education level, health literacy, underrepresented, UBR, LGBTQ, sexual and
gender minorities, SGM, equity, access to care.

**Subthemes (~5).**
- 6.1 Race/ethnicity & ancestry-based health disparities
- 6.2 Neighborhood-level deprivation (ADI, walkability, built environment)
- 6.3 Discrimination & its health consequences
- 6.4 LGBTQ+ / sexual & gender minority health
- 6.5 Structural / financial / care-access barriers

**Example records.**
- PMID:39932771 — "Subtyping Social Determinants of Health in the 'All of Us' Program: Network Analysis" (*JMIR* 2025)
- PMID:39095751 — "Sexual orientation, gender identity and virologic failure among people with HIV" (*BMC Public Health* 2024)
- PMID:40085006 — "Unmet social needs and diverticulitis: a phenotyping algorithm and cross-sectional analysis" (*JAMIA* 2025)
- workspace:29011 — "BARRIERS TO CARE AMONG LGBTQ CANCER SURVIVORS"
- workspace:6963 — "Understanding Burden of Dermatologic Disease in Homeless population"
- workspace:11355 — "Discrimination & Mental health among African American adults with HIV"

---

## 7. Wearables & digital health (~8%)

**Definition.** Studies using Fitbit / WHOOP / smartwatch / other wearable-
derived data — physical activity, sleep stages, heart rate, daily steps,
heart rate phase — either for disease association or as the primary
methodologic contribution. Distinct from theme 13 (Respiratory & Sleep
Medicine) which is disease-anchored.

**Indicative keywords.** wearable, Fitbit, WHOOP, smartwatch, step count,
physical activity, sedentary, sleep duration, sleep stage, heart rate
variability, HRV, biometric, sensor, accelerometer, digital phenotyping.

**Subthemes (~3).**
- 7.1 Activity / sedentary / step-count epidemiology
- 7.2 Wearable-derived sleep stage / circadian biomarkers
- 7.3 Multimodal wearable + EHR integration for prediction

**Example records.**
- PMID:40587790 — "Sleep duration and timing are associated with next-day physical activity" (*PNAS* 2025)
- PMID:40605186 — "Fitbit Physical Activity and Sleep Data in the All of Us Research Program: Data Exploration and Processing Considerations" (*Med Sci Sports Exerc* 2025)
- PMID:41570792 — "Associations Between Objective Sleep Characteristics From Wearable Physiologic Monitors and Incident Atrial Fibrillation" (*JACC Adv* 2026)
- PMID:39755829 — "Data from the All of Us research program reinforces existence of activity inequality" (*NPJ Digit Med* 2025)
- workspace:34450 — "HealthAI" (sleep-readiness wearable analytics)
- workspace:25350 — "Investigating wearable phenotypes (CDRv8)"

---

## 8. Infectious disease & immunology (~6%)

**Definition.** Bacterial, viral, fungal, mycobacterial infection
epidemiology; host genetics of infection response; COVID-19 outcomes
(distinct from "long COVID" methods); virome characterization; HLA-disease
associations; vaccine response.

**Indicative keywords.** HIV, COVID-19, SARS-CoV-2, long COVID, PASC, EBV,
Epstein-Barr, virome, herpes, HHV, tuberculosis, mycobacter, cryptococcal,
hepatitis, sepsis, HLA, vaccine, immune response.

**Subthemes (~3).**
- 8.1 COVID-19 / SARS-CoV-2 outcomes & host genetics (incl. PASC)
- 8.2 Chronic / persistent viral infection (HIV, EBV, herpes, virome)
- 8.3 Other bacterial / fungal / mycobacterial infections

**Example records.**
- PMID:41714741 — "Host control of persistent Epstein-Barr virus infection" (*Nature* 2026)
- PMID:41882355 — "The DNA virome varies with human genes and environments" (*Nature* 2026)
- PMID:38113267 — "Uncovering associations between pre-existing conditions and COVID-19 Severity: A polygenic risk score approach" (*PLoS Genet* 2023)
- workspace:19565 — "Pulmonary mycobacterial infection"

---

## 9. Autoimmune & inflammatory disease (~6%)

**Definition.** Autoimmune and chronic inflammatory diseases — RA, SLE, IBD,
psoriatic arthritis (note: dermatologic psoriasis goes to theme 12),
Sjögren's, Behçet's, vasculitis, scleroderma, multiple sclerosis (when
inflammation is the framing), autoimmune endocrine disease.

**Indicative keywords.** autoimmune, rheumatoid arthritis, RA, systemic
lupus erythematosus, SLE, inflammatory bowel disease, IBD, Crohn's,
ulcerative colitis, psoriatic arthritis, ankylosing spondylitis,
spondyloarthritis, Sjögren, vasculitis, scleroderma, multiple sclerosis.

**Subthemes (~3).**
- 9.1 Connective-tissue / systemic autoimmune (SLE, RA, Sjögren's, scleroderma)
- 9.2 IBD & GI autoimmune
- 9.3 Multi-condition autoimmune comorbidity & shared genetics

**Example records.**
- PMID:40495997 — "Sleep and circadian disorders as risk factors for autoimmune disease" (*Neurobiol Sleep Circadian Rhythms* 2025)
- workspace:16082 — "CVD_SLE_RA" (cardiovascular comorbidity in SLE/RA)
- workspace:7755 — "V7 ARI Genomics Workspace" (autoimmune disease prevalence + COVID comorbidity)
- workspace:25676 — "Exploring endotypes in rheumatoid arthritis"

---

## 10. Rare disease & Mendelian genetics (~6%)

**Definition.** ACMG/AMP pathogenic-variant studies, hereditary cancer
syndromes (when the analytic contribution is monogenic risk rather than
common-variant association), monogenic disorders (CF, sickle cell, TSC,
Fanconi anemia, malignant hyperthermia, primary aldosteronism as monogenic-
associated), penetrance & expressivity in unselected populations,
variants-of-unknown-significance characterization. Bridges with theme 2
(rare-variant association) but differentiated by Mendelian framing.

**Indicative keywords.** rare disease, Mendelian, ACMG, pathogenic variant,
ClinVar, incomplete penetrance, expressivity, tuberous sclerosis, TSC,
cystic fibrosis, CFTR, sickle cell, hereditary, inborn error, monogenic,
hereditary cancer panel, BRCA heterozygote, founder variant, lymphedema,
Fanconi anemia, Hirschsprung.

**Subthemes (~4).**
- 10.1 Penetrance / expressivity of known Mendelian variants in unselected populations
- 10.2 Hereditary cancer & ACMG actionable-gene findings
- 10.3 Individual monogenic disorders (TSC, CF, SCD, FA, etc.)
- 10.4 VUS & founder-variant characterization

**Example records.**
- PMID:40522671 — "Diseases Common in Persons With Cystic Fibrosis Among CFTR Heterozygotes" (*JAMA Intern Med* 2025)
- PMID:42151584 — "Uncovering apparent incomplete penetrance of TSC1/TSC2 variants" (*Eur J Hum Genet* 2026)
- PMID:39081307 — "Sweet syndrome associated with moderate leukocyte adhesion deficiency type I" (*Front Immunol* 2024)
- workspace:25885 — "Disease-associated variants and clinical features in generally healthy group v8"
- workspace:9648 — "vus-control - Shengfeng Xu"
- workspace:33549 — "Lymphedema and lipedema variants"

---

## 11. Aging, frailty & ADRD (~5%)

**Definition.** Healthy-aging biomarkers, frailty (physical, hospital frailty
risk score, isotemporal substitution), longevity, Alzheimer's disease and
related dementias, Parkinson's disease, epigenetic aging, sarcopenia.

**Indicative keywords.** Alzheimer's, AD, ADRD, dementia, cognitive
impairment, cognitive decline, aging, frailty index, sarcopenia, Parkinson,
longevity, healthy aging, epigenetic age, APOE, geriatric.

**Subthemes (~3).**
- 11.1 ADRD risk, genetics & phenotyping
- 11.2 Frailty, sarcopenia & physical aging
- 11.3 Healthy aging / longevity / epigenetic age

**Example records.**
- PMID:39183196 — "Improving genetic risk modeling of dementia from real-world data in underrepresented populations" (*Commun Biol* 2024)
- PMID:41341115 — "Frailty and Physical Activity: A Compositional Isotemporal Substitution Analysis" (*J Frailty Sarcopenia Falls* 2025)
- workspace:13483 — "ADRD Exploration" (insomnia → AD trajectory, APOE × SDoH)
- workspace:1306 — "Healthy Aging" (polygenic longevity scores)
- workspace:19478 — "Biomarkers Sarcopenia"

---

## 12. Dermatology (~5%)

**Definition.** Dermatologic disease epidemiology and comorbidity studies.
Anomalously over-represented in the corpus (see Phase 1 README — ~13% of
publications by journal-count). Largely case-control epidemiology of skin
conditions using AoU's national-cohort scope.

**Indicative keywords.** dermatology, dermatologic, psoriasis, atopic
dermatitis, eczema, hidradenitis suppurativa, keloid, pyoderma gangrenosum,
mycosis fungoides, lichen planus, lichen sclerosus, alopecia, granuloma
annulare, ichthyosis, pemphigus, melanoma (as skin disease), basal cell
carcinoma, squamous cell carcinoma, melasma, onychomycosis, vitiligo.

**Subthemes (~4).**
- 12.1 Inflammatory dermatoses (psoriasis, atopic dermatitis, HS, lichen)
- 12.2 Skin cancers & precancerous lesions
- 12.3 Dermatology in underrepresented populations
- 12.4 Dermatology–systemic disease comorbidity (skin–CVD, skin–mental health, skin–autoimmune)

**Example records.**
- PMID:35817334 — "Comorbidities associated with mycosis fungoides" (*JAAD* 2022)
- PMID:38951294 — "Increased risk of allergic contact dermatitis in patients with cutaneous lichen planus" (*Arch Dermatol Res* 2024)
- PMID:40756774 — "Pyoderma gangrenosum associated with major adverse cardiovascular events" (*JEADV Clin Pract* 2025)
- PMID:40835838 — "Multi-ancestry meta-analysis of keloids" (*Nat Commun* 2025)
- workspace:6963 — "Understanding Burden of Dermatologic Disease in Homeless population"

---

## 13. Respiratory & sleep medicine (~4%)

**Definition.** Asthma, COPD, pulmonary hypertension, interstitial lung
disease, obstructive sleep apnea, insomnia and other sleep disorders as
disease entities (distinct from theme 7 which is methods-focused on
wearable-derived sleep, and theme 4 which is behavioral-sleep).

**Indicative keywords.** asthma, COPD, chronic obstructive, pulmonary
hypertension, interstitial lung disease, ILD, sleep apnea, obstructive
sleep apnea, OSA, insomnia, hypersomnia, narcolepsy, delayed sleep phase
disorder, DSPD, circadian disorder.

**Subthemes (~3).**
- 13.1 Asthma & airway disease
- 13.2 Sleep disorders (OSA, insomnia, DSPD) as disease
- 13.3 Pulmonary hypertension & rare lung disease

**Example records.**
- PMID:6614 workspace — "Asthma mortality disparity"
- PMID:1827 workspace — "Asthma Attack Prediction: Machine Learning Approach"
- PMID:36974749 — "Single Nucleotide Polymorphism rs9277336 Controls the Nuclear Alpha Actinin 4-HLA-DPA1 Axis and Pulmonary Endothelial Pathophenotypes in PAH" (*JAHA* 2023)

---

## 14. Neurology (non-ADRD) (~4%)

**Definition.** Stroke (non-cardio-embolic framing), epilepsy, headache /
migraine, traumatic brain injury, multiple sclerosis (when framed as
neurology rather than autoimmune), spinal cord disease, neuropathy.
Distinct from theme 11 (Aging/ADRD) and from theme 1 (cardio-embolic stroke).

**Indicative keywords.** stroke, epilepsy, seizure, migraine, headache,
traumatic brain injury, TBI, spinal cord, cerebrovascular, multiple
sclerosis, neurodegeneration, neuropathy.

**Subthemes (~3).**
- 14.1 Headache & migraine
- 14.2 Stroke & cerebrovascular disease
- 14.3 Epilepsy, TBI & other neurology

**Example records.**
- workspace:30067 — "Semaglutide / GLP-1-agonist / Epilepsy & Seizures"
- workspace:6544 — "Daily Step Counts and the Risk of Headache Disorders"
- workspace:28205 — "TBI Outcomes" (rehabilitation-trial representation)

---

## 15. Pregnancy, maternal & women's health (~4%)

**Definition.** Pregnancy outcomes, preeclampsia, preterm birth, postpartum
conditions, gynecologic conditions (uterine fibroids, endometriosis,
pelvic floor dysfunction), contraception, menopause. Note: gynecologic
cancers go to theme 5 unless the analytic contribution is reproductive-
biology rather than oncology.

**Indicative keywords.** pregnancy, preeclampsia, eclampsia, maternal,
postpartum, preterm birth, gestational diabetes, gestational hypertension,
gynecologic, endometriosis, uterine fibroid, pelvic floor, ovarian (non-
cancer), menopause, contraception, fertility, menstrual.

**Subthemes (~3).**
- 15.1 Pregnancy outcomes & complications (preeclampsia, preterm, gestational diabetes)
- 15.2 Postpartum & long-term post-pregnancy CV risk
- 15.3 Gynecologic conditions (fibroids, endometriosis, pelvic floor) & contraception

**Example records.**
- PMID:39670378 — "Social Determinants of Health and Lifestyle Risk Factors Modulate Genetic Susceptibility for Women's Health Outcomes" (*Pac Symp Biocomput* 2024)
- workspace:32157 — "Re-surgery rates in pelvic organ prolapse"
- workspace:19412 — "postpartum_hypertension"
- workspace:9572 — "Women of reproductive age with sickle cell"
- workspace:31977 — "APO & LT_CVD_contributing factors_v7_dis" (adverse pregnancy outcomes → CVD)

---

## 16. Pharmacogenomics & drug response (~4%)

**Definition.** Pharmacogenomic studies — gene × drug interactions, adverse
drug reactions, drug efficacy variation by genotype/ancestry. Includes the
many AoU studies of GLP-1 agonists, beta-blockers, azathioprine, tamoxifen,
metformin, ketamine, statins, cilostazol, antiretrovirals, etc.

**Indicative keywords.** pharmacogenomic, pharmacogenetic, drug response,
adverse drug reaction, ADR, CYP2D6, CYP2C19, TPMT, NUDT15, metabolizer,
warfarin, tamoxifen, azathioprine, metformin, statin, cilostazol, ketamine
response, esketamine, drug-induced, drug-gene.

**Subthemes (~3).**
- 16.1 Adverse drug reactions & toxicity (drug-induced liver injury, leukopenia, etc.)
- 16.2 Drug efficacy variation by ancestry / genotype
- 16.3 Multi-medication / polypharmacy & precision-prescribing

**Example records.**
- PMID:40442974 — "PTPN2 and Leukopenia in Individuals With Normal TPMT and NUDT15 Metabolizer Status Taking Azathioprine" (*Clin Transl Sci* 2025)
- workspace:35015 — "20251024_rs7636910" (cilostazol-induced headache pharmacogenomics)
- workspace:8871 — "Aza Controlled Tier" (azathioprine ADR genetics)
- workspace:19792 — "Cardiometabolic Pharmacology Research"
- workspace:33099 — "Response in beta-blocker (V8 Dataset) - NEVEN"

---

## 17. ELSI, participant engagement & recruitment (~3%)

**Definition.** Ethical/legal/social implications work, return-of-results,
informed consent, recruitment methodology, community engagement, AoU-
program-introduction publications, librarian/training toolkits, and the
"meta" pubs about the AoU program itself.

**Indicative keywords.** ELSI, ethical legal social, informed consent,
return of results, recruitment, community engagement, patient-reported,
participant engagement, library, toolkit, outreach, trust, dialogue, About
All of Us.

**Subthemes (~3).**
- 17.1 ELSI & ethics (return of results, consent, governance)
- 17.2 Recruitment methodology & engagement of underrepresented groups
- 17.3 Program-meta pubs & training/library resources

**Example records.**
- PMID:31412182 — "The 'All of Us' Research Program" (*NEJM* 2019)
- PMID:38917428 — "Using patient portals for large-scale recruitment of individuals underrepresented in biomedical research" (*JAMIA* 2024)
- PMID:40052488 — "A toolkit for academic libraries to create interdisciplinary interest in the All of Us Researcher Workbench across campus communities" (*Med Ref Serv Q* 2025)
- PMID:31161416 — "Mind the gap: resources required to receive, process and interpret research-returned whole genome data" (*Hum Genet* 2019)
- PMID:32064110 — "Exploring African American community perspectives about genomic medicine research" (*SAGE Open Med* 2020)

---

## 18. Ophthalmology, ENT & sensory medicine (~3%)

**Definition.** Eye disease (glaucoma, diabetic retinopathy, ERM, macular
degeneration, strabismus, ptosis), hearing loss, voice/laryngeal disease,
chronic rhinosinusitis (CRS), olfactory and other sensory conditions.
Distinct because of consistent AoU use for *disparities-in-sensory-care*
framing.

**Indicative keywords.** glaucoma, retinopathy, epiretinal, macular,
ophthalmology, vision, eye care, hearing loss, sensorineural, otolaryngology,
ENT, chronic rhinosinusitis, CRS, dysphonia, strabismus, ptosis,
otosclerosis, tinnitus.

**Subthemes (~3).**
- 18.1 Ophthalmology & vision care (incl. disparities)
- 18.2 Hearing loss & otolaryngology
- 18.3 Voice / laryngeal / CRS / olfactory

**Example records.**
- PMID:38200661 — "Access to Eye Care Providers and Glaucoma Severity in the NIH AoU Research Program" (*J Glaucoma* 2023)
- PMID:37473437 — "Hearing Loss and Sociodemographic Barriers to Health Care Access" (*Otolaryngol Head Neck Surg* 2023)
- PMID:42153790 — "Association of Depression in Patients With Chronic Rhinosinusitis Comorbid Asthma and Allergic Rhinitis" (*Am J Rhinol Allergy* 2026)
- workspace:3180 — "Ophthalmic Epidemiology"

---

## 19. Environmental health & climate (~2%)

**Definition.** Environmental-exposure studies, climate-change/heat-related
health, air pollution effects, built-environment effects (when not absorbed
into theme 6). Smallest disease theme but emerging.

**Indicative keywords.** climate change, heat, heat-related illness, air
pollution, particulate matter, PM2.5, wildfire, pesticide, environmental
exposure, built environment, walkability, green space, environmental
justice index, EJI.

**Subthemes (~2).**
- 19.1 Climate & heat-related health
- 19.2 Air pollution / environmental exposure / built environment

**Example records.**
- workspace:25846 — "Predictors of heat-related illness"
- (under-represented in the discovery sample; expect 200–300 records on tagging)

---

## META. AoU-program-meta-audit (audit-only bucket; NOT counted in theme shares)

**Definition.** Records that are primarily *about the All of Us program
itself* rather than *using AoU data to address a research question*. This
includes program-introduction publications, "year in review" pieces,
interviews with AoU leadership, governance/program-design descriptions, and
biospecimen / data-platform announcements that do not analytically use
participant data. Records that describe AoU as part of a substantive
data-analysis pub should NOT be flagged META — they stay in the substantive
corpus.

**Detection rules (used in the tagging script).**
- Title contains "All of Us Research Program" or "All of Us cohort"
  *without* a disease-specific noun.
- Title or abstract leads with "Introducing All of Us," "The All of Us
  Research Program," "Year in Review," "AoU at [year]," or similar.
- Publication type is interview / perspective / editorial about AoU
  leadership or AoU itself.
- Abstract describes the program design (consent flow, biobank, EHR
  integration, recruitment infrastructure) rather than reporting analysis
  results.

**Distinction from theme 17 (ELSI-research).** ELSI / consent / community-
engagement *research* (e.g., qualitative studies of African American
perspectives on genomic research, return-of-results methodology studies,
patient-portal recruitment evaluations) stays in theme 17 and counts in
theme shares. META is restricted to records that are not themselves research
contributions — they are program-descriptive.

**Example records.**
- PMID:31412182 — "The 'All of Us' Research Program" (*NEJM* 2019, program-
  introduction)
- AoU year-in-review pieces, interviews with the AoU CEO, governance
  descriptions.

---

## Tagging policy summary (Phase 2c)

- Records may carry 2–4 top-level theme tags.
- Subtheme tagging is only required for the trackable subthemes called out
  explicitly: `1.3-CKM` (CKM syndrome), `1.4-stroke-cardio` (cardio-embolic
  stroke), `14.2-stroke-cerebro` (non-cardio-embolic stroke). Other
  subthemes are recorded in the taxonomy for human reference but are not
  required outputs of the tagger.
- `META` flag is a separate boolean; if set, the record is excluded from
  theme-share denominators.
- Every theme tag is recorded with its evidence source: `keyword` (with the
  matched keyword list) or `llm-judgment` (when LLM judgment was used to
  add or remove a tag during the audit pass).

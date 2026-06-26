"""Phase 2c — apply locked taxonomy tags to AoU pubs + filtered projects.

Strategy (hybrid keyword pre-tag + targeted LLM-judgment review):

  Pass 1 — keyword pre-tag
    For each record, build a search string from the title + abstract
    (publications) or title + scientific_question + approach +
    anticipated_findings (projects). For each top-level theme, score by
    counting *distinct* matched indicative keywords (case-insensitive, word
    boundary checks).

    A theme tags if EITHER:
      - the record matched >=1 high-specificity keyword (a small, manually
        curated set per theme that are individually diagnostic, e.g. "atrial
        fibrillation", "BRCA1", "GLP-1", "Fitbit"), OR
      - the record matched >=2 distinct general keywords from the theme.

    Subtheme tagging is restricted to the three trackable subthemes called
    out in the locked taxonomy: 1.3-CKM, 1.4-stroke-cardio,
    14.2-stroke-cerebro. CKM tagging requires CKM-syndrome phrasing
    *together with* a cardiometabolic top-level tag. Stroke subthemes are
    derived from "stroke"-mention plus cardio vs. neuro context.

  Pass 2 — targeted LLM-judgment review
    A small audit set is generated:
      - high-tag-count records (>5 themes): keyword pass likely over-tagged
      - zero-tag records: keyword pass under-tagged or record is genuinely
        out-of-scope (likely META).
      - random 50 records: precision/recall audit.

    For records that the agent reviews and adjusts during the audit,
    tag_evidence becomes 'llm-judgment'.

  AoU-meta-audit (META) detection
    Title-pattern rules per the taxonomy. Run separately and flag a boolean.

Output files:
  publications_tagged.jsonl / .csv
  projects_tagged.jsonl   / .csv
  theme_summary.csv
"""

from __future__ import annotations

import csv
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBS_IN = ROOT / "publications_with_ic.jsonl"
PROJ_IN = ROOT / "projects_filtered.jsonl"

# Tagging text source for publications. Controlled by env var AOU_TAG_MODE:
#   "abstract" (default) — tag on title + (gap-filled) abstract. Comparable
#                          across years and to the abstract-only peer biobanks.
#   "fulltext"           — also append PMC full-text *body* (back-matter
#                          stripped) where available. Richer cross-sectional
#                          theme map; NOT year-comparable (OA coverage skews
#                          to recent papers — see README).
# Both modes use gap-filled abstracts from fulltext_augmented.jsonl when present.
MODE = os.environ.get("AOU_TAG_MODE", "abstract").strip().lower()
AUG_IN = ROOT / "fulltext_augmented.jsonl"
_SUFFIX = "_fulltext" if MODE == "fulltext" else ""

PUBS_OUT_JSONL = ROOT / f"publications_tagged{_SUFFIX}.jsonl"
PUBS_OUT_CSV = ROOT / f"publications_tagged{_SUFFIX}.csv"
PROJ_OUT_JSONL = ROOT / "projects_tagged.jsonl"
PROJ_OUT_CSV = ROOT / "projects_tagged.csv"
THEME_SUMMARY_CSV = ROOT / f"theme_summary{_SUFFIX}.csv"


def _load_augmentation() -> dict:
    """Map record_id -> {abstract_filled, fulltext_body, has_fulltext,
    abstract_source}. Empty dict if the augmentation file is absent."""
    aug = {}
    if AUG_IN.exists():
        for line in AUG_IN.open():
            r = json.loads(line)
            aug[str(r.get("record_id"))] = r
    return aug


AUG = _load_augmentation()

# ----------------------------------------------------------------------------
# Taxonomy
#
# Each theme has:
#   code (1-19)
#   name
#   general:   set of keywords (need >=2 distinct hits to fire)
#   specific:  set of high-specificity diagnostic keywords (>=1 hit fires)
#
# Multiword keywords use literal substring matching (with leading/trailing
# word-boundary characters); single-word ones use \b boundaries.
# ----------------------------------------------------------------------------

THEMES = [
    {
        "code": "1",
        "name": "Cardiometabolic disease",
        "general": {
            "cardiovascular", "hypertension", "blood pressure", "type 2 diabetes",
            "type 1 diabetes", "obesity", "BMI", "cholesterol", "LDL", "HDL",
            "heart failure", "ejection fraction", "coronary", "CAD",
            "MASLD", "NAFLD", "NASH", "MASH", "statin", "beta-blocker",
            "kidney disease", "CKD", "aortic stenosis", "diabetes",
            "metabolic syndrome", "dyslipidemia", "hyperlipidemia",
            "myocardial infarction", "cardiac", "cardiometabolic",
            "atherosclerosis", "hypertensive", "glycemic",
            "venous thromboembolism", "carotid", "vascular disorder",
            "vascular disease", "aortic", "aneurysm", "thrombosis",
            "thromboembolism", "valvular", "arrhythmia", "diabetic",
            "insulin resistance", "lipid", "triglyceride", "MELD",
            "liver transplant", "cirrhosis", "fatty liver", "acute kidney injury",
            "AKI", "end-stage renal", "ESRD", "dialysis", "renal",
            "atrial flutter", "ventricular", "ischemic heart",
            "abdominal aortic", "deep vein thrombosis", "DVT",
            "pulmonary embolism", "cardiology", "endocrine",
            "hyperglycemia", "prediabetes", "DKD",
            "cardiovascular disease", "CVD", "heart disease",
            "kidney stone", "nephrolithiasis", "nephropathy",
            "diabetic kidney", "glomerular", "proteinuria", "albuminuria",
            "eGFR", "creatinine", "renal disease",
        },
        "specific": {
            "atrial fibrillation", "GLP-1", "SGLT2", "T2D", "T2DM", "type 2 diabetes",
            "CKM syndrome", "Cardiovascular-Kidney-Metabolic",
            "hepatocellular carcinoma", "MASLD", "NAFLD",
            "preeclampsia",  # multi-tag with 15
            "stroke",  # always also tag neurology
            "heart failure", "atrial fibrillation", "aortic stenosis",
            "MELD score", "clonal hematopoiesis", "CHIP",
            "venous thromboembolism", "hypertension",
        },
    },
    {
        "code": "2",
        "name": "Genomics methods & complex-trait genetics",
        "general": {
            "GWAS", "PheWAS", "polygenic", "polygenic risk score", "PRS",
            "fine-mapping", "fine mapping", "rare variant", "burden test",
            "whole-genome sequencing", "whole genome sequencing", "WGS",
            "long-read", "HiFi", "ancestry", "admixture", "gnomAD",
            "ClinVar", "multi-ancestry", "multiancestry", "subcontinental",
            "tandem repeat", "Mendelian randomization", "structural variant",
            "imputation", "phasing", "heritability", "GWAS summary",
            "genome-wide association", "genetic association",
            "genome-wide", "association study", "association studies",
            "genetic variant", "genetic risk", "genotype imputation",
            "genotype", "haplotype", "phenome-wide", "common variant",
            "loci", "locus", "single nucleotide polymorphism", "SNP",
            "exome", "exomic", "exome sequencing", "rare-variant",
            "genomic", "genomics", "transcriptome-wide", "TWAS",
            "eQTL", "expression quantitative",
            "genetic ancestry", "global ancestry", "local ancestry",
            "trans-ethnic", "transethnic", "polygenic score",
        },
        "specific": {
            "polygenic risk score", "PheWAS", "GWAS", "SAIGE", "REGENIE",
            "long-read sequencing", "Mendelian randomization",
            "fine-mapping", "multi-ancestry", "subcontinental",
            "PRS", "whole-genome sequencing", "WGS", "TWAS",
            "polygenic score", "polygenic liability", "genetic risk score",
        },
    },
    {
        "code": "3",
        "name": "Methods, infrastructure & phenotyping (non-genomic)",
        "general": {
            "phenotyping algorithm", "phecode", "computable phenotype",
            "machine learning", "deep learning", "neural network",
            "EHR data quality", "missing data", "OMOP", "FHIR", "SNOMED",
            "ICD-10", "N3C", "RECOVER", "workbench", "notebook",
            "cohort builder", "privacy-preserving", "synthetic data",
            "data harmonization", "harmonization", "natural language processing",
            "NLP", "data quality", "data validation", "case-finding",
            "model performance", "AUC", "F1 score", "feature engineering",
            "transformer", "predictive model", "risk prediction",
            "predictive modeling", "predictive modelling", "ensemble model",
            "random forest", "XGBoost", "gradient boosting", "supervised learning",
            "unsupervised learning", "clustering", "LLM",
            "large language model", "AI model", "artificial intelligence",
            "electronic health record", "EHR", "claims data", "ICD",
            "data linkage", "data integration", "cohort identification",
            "case definition", "validation cohort", "training cohort",
            "feature selection", "model calibration", "interpretability",
            "explainability", "explainable AI",
        },
        "specific": {
            # Methods/infrastructure specifics — restricted to phrases that
            # are themselves the analytic contribution, not generic mentions.
            "PhecodeX", "phecode curation", "allofus R package",
            "All of Us Researcher Workbench tool", "computable phenotype algorithm",
            "synthetic data", "federated learning", "phenotyping algorithm",
            "re-identification", "privacy-preserving",
            "data harmonization", "record linkage methodology",
            "error detection algorithm", "data quality algorithm",
            "EHR data quality", "computational variant effect",
            "variant effect predictor", "deep learning model",
            "contrastive learning", "transformer-based",
            "AoU Researcher Workbench", "Researcher Workbench",
            "informatics innovation", "public health surveillance",
            "Public Data Browser",
        },
    },
    {
        "code": "4",
        "name": "Mental health, behavioral & substance use",
        "general": {
            "depression", "depressive", "MDD", "anxiety", "anxious", "bipolar",
            "schizophrenia", "PTSD", "post-traumatic stress", "suicidality",
            "suicide", "mental health", "psychiatric", "alcohol use disorder",
            "AUD", "smoking", "tobacco", "e-cigarette", "cannabis", "marijuana",
            "opioid", "amphetamine", "ketamine", "loneliness", "wellbeing",
            "well-being", "stress", "coping", "meaning in life",
            "substance use", "addiction", "psychological",
            "substance use disorder", "SUD", "drug abuse", "alcohol abuse",
            "nicotine", "vaping", "depressive symptom", "anxiety disorder",
            "anti-depressant", "antidepressant", "SSRI", "SNRI",
            "mood disorder", "panic disorder", "OCD", "obsessive-compulsive",
            "social anxiety", "behavioral health", "psychotherapy", "cognitive behavioral",
            "CBT", "mindfulness", "psychosocial", "suicidal ideation",
            "self-harm", "pain", "chronic pain", "pain prediction",
        },
        "specific": {
            "schizophrenia", "bipolar disorder", "major depressive disorder",
            "alcohol use disorder", "opioid use disorder", "PTSD",
            "loneliness", "depression", "anxiety", "substance use disorder",
            "suicidal ideation",
        },
    },
    {
        "code": "5",
        "name": "Cancer",
        "general": {
            "cancer", "carcinoma", "tumor", "tumour", "leukemia", "lymphoma",
            "myeloma", "melanoma", "sarcoma", "oncology", "metastasis",
            "breast cancer", "prostate cancer", "lung cancer", "colorectal cancer",
            "colorectal", "hepatocellular", "pancreatic cancer", "ovarian cancer",
            "cervical cancer", "endometrial cancer", "renal cell", "cancer screening",
            "survivorship", "PSA", "tumor suppressor", "cancer susceptibility",
            "neoplasm", "malignancy", "chemotherapy", "radiotherapy",
            "AML", "ALL", "CLL", "CML", "multiple myeloma", "non-Hodgkin",
            "Hodgkin", "uterine cancer", "thyroid cancer", "bladder cancer",
            "esophageal cancer", "gastric cancer", "stomach cancer",
            "glioma", "glioblastoma", "head and neck cancer", "oral cancer",
            "myelodysplastic", "MDS", "neoplasia", "metastatic",
            "immunotherapy", "checkpoint inhibitor", "tumor microenvironment",
            "circulating tumor", "ctDNA", "liquid biopsy",
            "hereditary breast", "Li-Fraumeni",
        },
        "specific": {
            "BRCA1", "BRCA2", "Lynch syndrome", "hereditary cancer",
            "breast cancer", "prostate cancer", "lung cancer",
            "colorectal cancer", "ovarian cancer", "hepatocellular carcinoma",
            "PSA testing", "cancer survivor", "cancer survivors",
            "leukemia", "lymphoma",
            "melanoma", "myeloma", "pancreatic cancer", "glioblastoma",
            "cervical cancer", "endometrial cancer", "carcinoma",
            "oncology", "neoplasm", "Merkel cell", "skin cancer",
            "liver cancer", "thyroid cancer", "neuroendocrine tumor",
            "ductal carcinoma", "tumor patients",
        },
    },
    {
        "code": "6",
        "name": "Social determinants of health & health disparities",
        "general": {
            "social determinants of health", "SDOH", "discrimination",
            "disparities", "disparity", "racial disparity", "ethnic disparity",
            "neighborhood", "deprivation", "area deprivation index", "ADI",
            "food insecurity", "housing", "health literacy", "underrepresented",
            "UBR", "LGBTQ", "sexual and gender minorities", "SGM", "equity",
            "access to care", "social vulnerability", "structural racism",
            "racism", "socioeconomic", "income", "education level",
            "rural", "uninsured", "Medicaid",
            "underrepresented groups", "African American", "Hispanic",
            "Latino", "Latinx", "Native American", "American Indian",
            "Asian American", "Black patients", "Black participants",
            "racial and ethnic", "race and ethnicity", "minority",
            "minorities", "marginalized", "structural barriers",
            "social inequity", "social inequality", "transgender",
            "gender minority", "sexual minority", "gay", "lesbian",
            "bisexual", "homeless", "homelessness", "uninsured",
            "poverty", "low-income", "social vulnerability index", "SVI",
        },
        "specific": {
            "social determinants of health", "area deprivation index",
            "sexual and gender minorities", "structural racism",
            "health disparities", "LGBTQ", "underrepresented groups",
            "racial disparity", "ethnic disparity",
        },
    },
    {
        "code": "7",
        "name": "Wearables & digital health",
        "general": {
            "wearable", "Fitbit", "WHOOP", "smartwatch", "step count",
            "physical activity", "sedentary", "sleep duration", "sleep stage",
            "heart rate variability", "HRV", "biometric", "sensor",
            "accelerometer", "digital phenotyping", "actigraphy",
            "steps per day", "wearable device",
        },
        "specific": {
            "Fitbit", "wearable", "accelerometer", "digital phenotyping",
            "step count",
        },
    },
    {
        "code": "8",
        "name": "Infectious disease & immunology",
        "general": {
            "HIV", "COVID-19", "SARS-CoV-2", "long COVID", "PASC",
            "Epstein-Barr", "EBV", "virome", "herpes", "HHV", "tuberculosis",
            "mycobacter", "cryptococcal", "hepatitis", "sepsis", "HLA",
            "vaccine", "immune response", "antibody", "viral load",
            "antiretroviral", "infection",
        },
        "specific": {
            "HIV", "COVID-19", "SARS-CoV-2", "long COVID", "PASC",
            "Epstein-Barr", "tuberculosis", "antiretroviral",
        },
    },
    {
        "code": "9",
        "name": "Autoimmune & inflammatory disease",
        "general": {
            "autoimmune", "rheumatoid arthritis", "RA", "systemic lupus",
            "SLE", "lupus", "inflammatory bowel disease", "IBD", "Crohn",
            "ulcerative colitis", "psoriatic arthritis", "ankylosing spondylitis",
            "spondyloarthritis", "Sjogren", "Sjögren", "vasculitis",
            "scleroderma", "multiple sclerosis", "MS",
            "discoid lupus", "cutaneous lupus", "morphea",
            "bullous pemphigoid", "pemphigus vulgaris", "myasthenia gravis",
            "Hashimoto", "Graves disease", "celiac",
            "polymyalgia rheumatica", "giant cell arteritis",
            "ankylosing", "Raynaud", "polymyositis", "dermatomyositis",
            "autoimmune comorbidities", "antibody-mediated",
            "psoriasis",  # also dermatology — both fire
        },
        "specific": {
            "rheumatoid arthritis", "systemic lupus", "Crohn's disease",
            "ulcerative colitis", "multiple sclerosis", "psoriatic arthritis",
            "Sjogren syndrome", "Sjögren syndrome", "discoid lupus",
            "vasculitis", "myasthenia gravis", "ankylosing spondylitis",
            "inflammatory bowel disease", "IBD", "sarcoidosis",
            "lupus", "autoimmune disease",
        },
    },
    {
        "code": "10",
        "name": "Rare disease & Mendelian genetics",
        "general": {
            "rare disease", "Mendelian", "ACMG", "pathogenic variant",
            "incomplete penetrance", "expressivity", "tuberous sclerosis",
            "TSC", "cystic fibrosis", "CFTR", "sickle cell", "hereditary",
            "inborn error", "monogenic", "hereditary cancer panel",
            "BRCA heterozygote", "founder variant", "lymphedema",
            "Fanconi anemia", "Hirschsprung", "ACMG actionable", "VUS",
            "variant of unknown significance", "penetrance",
            "Ehlers Danlos", "Ehlers-Danlos", "osteogenesis imperfecta",
            "Marfan", "neurofibromatosis", "NF1", "NF2",
            "Huntington disease", "Huntington's", "hemochromatosis",
            "phenylketonuria", "PKU", "G6PD", "alpha-1 antitrypsin",
            "Wilson disease", "porphyria", "Gaucher", "Pompe disease",
            "Fabry disease", "muscular dystrophy", "Duchenne",
            "spinal muscular atrophy", "SMA", "Friedreich ataxia",
            "FH familial hypercholesterolemia", "familial hypercholesterolemia",
            "primary aldosteronism", "MEN1", "MEN2",
            "secondary findings", "incidental findings", "primary immunodeficiency",
        },
        "specific": {
            "tuberous sclerosis", "cystic fibrosis", "sickle cell disease",
            "ACMG", "pathogenic variant", "incomplete penetrance",
            "monogenic", "Fanconi anemia", "Ehlers Danlos", "Ehlers-Danlos",
            "neurofibromatosis", "familial hypercholesterolemia",
            "secondary findings", "ACMG actionable",
        },
    },
    {
        "code": "11",
        "name": "Aging, frailty & ADRD",
        "general": {
            "Alzheimer", "Alzheimer's", "ADRD", "dementia",
            "cognitive impairment", "cognitive decline", "aging",
            "frailty", "sarcopenia", "Parkinson", "longevity",
            "healthy aging", "epigenetic age", "APOE", "geriatric",
            "older adults", "elderly",
        },
        "specific": {
            "Alzheimer", "ADRD", "Parkinson's disease", "frailty index",
            "sarcopenia", "APOE", "epigenetic age",
            "cerebral amyloid angiopathy", "CAA", "mild cognitive impairment",
            "dementia", "frailty",
        },
    },
    {
        "code": "12",
        "name": "Dermatology",
        "general": {
            "dermatology", "dermatologic", "psoriasis", "atopic dermatitis",
            "eczema", "hidradenitis suppurativa", "keloid",
            "pyoderma gangrenosum", "mycosis fungoides", "lichen planus",
            "lichen sclerosus", "alopecia", "granuloma annulare", "ichthyosis",
            "pemphigus", "basal cell carcinoma", "squamous cell carcinoma",
            "melasma", "onychomycosis", "vitiligo", "rosacea",
            "cutaneous", "skin disease", "skin cancer",
            "actinic keratosis", "acne", "dermatitis", "urticaria",
            "hives", "contact dermatitis", "skin condition",
            "discoid lupus erythematosus", "central centrifugal cicatricial",
            "CCCA", "androgenetic alopecia", "morphea",
            "bullous pemphigoid", "scleroderma localized",
            "scabies", "Sweet syndrome", "necrobiosis lipoidica",
            "dermatologist", "skin biopsy", "skin lesion",
        },
        "specific": {
            "psoriasis", "atopic dermatitis", "hidradenitis suppurativa",
            "alopecia areata", "vitiligo", "mycosis fungoides",
            "onychomycosis", "keloid", "granuloma annulare",
            "lichen planus", "lichen sclerosus", "discoid lupus erythematosus",
            "pemphigus", "bullous pemphigoid", "contact dermatitis",
            "morphea", "rosacea", "alopecia", "eczema", "dermatitis",
            "lichen planopilaris", "frontal fibrosing alopecia",
            "pityriasis rosea", "seborrheic dermatitis", "prurigo nodularis",
            "palmoplantar pustulosis", "pyoderma gangrenosum",
            "ichthyosis", "dermatologic", "dermatology", "skin cancer",
            "skin disease", "basal cell carcinoma", "squamous cell carcinoma",
            "melasma", "hyperhidrosis", "skin condition",
        },
    },
    {
        "code": "13",
        "name": "Respiratory & sleep medicine",
        "general": {
            "asthma", "COPD", "chronic obstructive", "pulmonary hypertension",
            "interstitial lung disease", "ILD", "sleep apnea",
            "obstructive sleep apnea", "OSA", "insomnia", "hypersomnia",
            "narcolepsy", "delayed sleep phase", "DSPD", "circadian",
            "pulmonary",
        },
        "specific": {
            "asthma", "COPD", "obstructive sleep apnea", "insomnia",
            "pulmonary hypertension", "narcolepsy",
            "pulmonary arterial hypertension", "PAH",
            "interstitial lung disease",
        },
    },
    {
        "code": "14",
        "name": "Neurology (non-ADRD)",
        "general": {
            "stroke", "epilepsy", "seizure", "migraine", "headache",
            "traumatic brain injury", "TBI", "spinal cord",
            "cerebrovascular", "multiple sclerosis", "neurodegeneration",
            "neuropathy", "neurological",
            "neuromuscular", "ALS", "amyotrophic lateral",
            "myelopathy", "neurologist", "Tourette",
            "essential tremor", "dystonia", "Bell's palsy",
            "carpal tunnel", "peripheral neuropathy", "diabetic neuropathy",
            "vertigo", "syncope", "concussion", "cerebral palsy",
            "encephalopathy", "encephalitis", "myelin", "neurodevelopment",
        },
        "specific": {
            "stroke", "epilepsy", "migraine", "traumatic brain injury",
            "multiple sclerosis", "cerebrovascular", "ALS",
            "amyotrophic lateral sclerosis", "Tourette syndrome",
            "essential tremor", "intracerebral hemorrhage",
            "subarachnoid hemorrhage", "subdural hemorrhage",
        },
    },
    {
        "code": "15",
        "name": "Pregnancy, maternal & women's health",
        "general": {
            "pregnancy", "preeclampsia", "eclampsia", "maternal", "postpartum",
            "preterm birth", "gestational diabetes", "gestational hypertension",
            "gynecologic", "endometriosis", "uterine fibroid", "pelvic floor",
            "menopause", "contraception", "fertility", "menstrual",
            "perinatal",
            "PCOS", "polycystic ovary", "polycystic ovarian", "infertility",
            "miscarriage", "stillbirth", "pelvic organ prolapse",
            "lactation", "breastfeeding", "cervix", "vaginal",
            "women's health", "obstetric", "OB-GYN", "obstetrics",
            "menarche", "perimenopause", "hormone replacement", "HRT",
            "abnormal uterine bleeding", "adenomyosis", "ovarian reserve",
            "pregnancy outcome", "adverse pregnancy",
        },
        "specific": {
            "preeclampsia", "preterm birth", "gestational diabetes",
            "endometriosis", "uterine fibroid", "menopause", "postpartum",
            "polycystic ovary syndrome", "PCOS", "infertility",
            "pelvic organ prolapse", "pregnancy", "maternal health",
            "perinatal", "reproductive-aged women", "reproductive age",
            "endometrial cancer", "uterine fibroids", "menstrual",
            "gestational", "obstetric",
        },
    },
    {
        "code": "16",
        "name": "Pharmacogenomics & drug response",
        "general": {
            "pharmacogenomic", "pharmacogenetic", "drug response",
            "adverse drug reaction", "ADR", "CYP2D6", "CYP2C19", "TPMT",
            "NUDT15", "metabolizer", "warfarin", "tamoxifen", "azathioprine",
            "metformin", "cilostazol", "esketamine", "drug-induced",
            "drug-gene", "pharmacokinetic",
        },
        "specific": {
            "pharmacogenomic", "pharmacogenetic", "CYP2D6", "CYP2C19",
            "TPMT", "NUDT15", "drug-induced liver injury",
        },
    },
    {
        "code": "17",
        "name": "ELSI, participant engagement & recruitment",
        "general": {
            "ELSI", "ethical legal social", "informed consent",
            "return of results", "recruitment", "community engagement",
            "patient-reported", "participant engagement", "library",
            "toolkit", "outreach", "trust", "dialogue",
            "qualitative interview", "focus group", "patient perspectives",
            "stakeholder", "ethics",
            "data sharing", "willingness to share", "patient portal",
            "research participation", "research engagement",
            "community-based participatory", "CBPR",
            "researcher workbench training", "librarian", "consent process",
            "biospecimen", "biobank ethics", "data governance",
            "research perspectives", "perspectives about",
            "willingness to participate", "research literacy",
        },
        "specific": {
            # ELSI specifics are deliberately restrictive — "informed consent"
            # alone shows up in any methods-section text. We require the
            # research-contribution itself to be ELSI-themed.
            "ELSI", "ethical legal social",
            "return of results methodology", "research participant perspectives",
            "consent issues in genetic research", "patient portal recruitment",
            "genetic counseling", "research capacity building",
            "FQHC", "community advisory", "advisory board",
            "research literacy", "research training",
            "co-designed curriculum", "secondary schools",
            "follow-up survey completion", "engaging African-Americans",
            "African American community", "community perspectives",
            "library toolkit",
        },
    },
    {
        "code": "18",
        "name": "Ophthalmology, ENT & sensory medicine",
        "general": {
            "glaucoma", "retinopathy", "epiretinal", "macular",
            "ophthalmology", "vision", "eye care", "hearing loss",
            "sensorineural", "otolaryngology", "ENT",
            "chronic rhinosinusitis", "CRS", "dysphonia", "strabismus",
            "ptosis", "otosclerosis", "tinnitus", "olfactory",
            "cataract", "myopia", "presbyopia", "uveitis",
            "diabetic eye", "retinal", "optic nerve", "eye disease",
            "vocal cord", "voice disorder", "laryngeal", "larynx",
            "vertigo", "Meniere", "rhinitis", "allergic rhinitis",
            "nasal polyp", "anosmia", "smell disorder",
        },
        "specific": {
            "glaucoma", "diabetic retinopathy", "chronic rhinosinusitis",
            "hearing loss", "macular degeneration", "tinnitus",
            "cataract", "Meniere's disease", "vocal cord paralysis",
            "dysphonia",
        },
    },
    {
        "code": "19",
        "name": "Environmental health & climate",
        "general": {
            "climate change", "heat", "heat-related illness",
            "air pollution", "particulate matter", "PM2.5", "wildfire",
            "pesticide", "environmental exposure", "built environment",
            "walkability", "green space", "environmental justice",
            "EJI", "ambient temperature",
        },
        "specific": {
            "climate change", "PM2.5", "wildfire smoke",
            "environmental justice index", "heat-related illness",
        },
    },
]

# ---- subthemes that need explicit tracking -------------------------------

SUBTHEME_CKM_TERMS = {
    "CKM syndrome", "Cardiovascular-Kidney-Metabolic",
    "cardiovascular kidney metabolic", "CKM staging",
}
# cardio-embolic stroke context — co-occurrence with AF or cardiac framing
CARDIO_STROKE_CONTEXT = {
    "atrial fibrillation", "AF ", "cardio-embolic", "cardioembolic",
    "embolic stroke", "valvular", "heart failure",
}
NEURO_STROKE_CONTEXT = {
    "cerebrovascular", "ischemic stroke", "hemorrhagic stroke",
    "intracerebral", "subarachnoid", "thrombectomy", "tPA",
    "tissue plasminogen", "lacunar",
}

# ---- META detection (audit bucket) ---------------------------------------

# Title patterns that ALWAYS force META (cannot be overridden by disease nouns)
META_TITLE_STRONG = [
    re.compile(r"^['\"‘’“”]*\s*the\s+['\"‘’“”]*all of us['\"‘’“”]*\s+research program['\"‘’“”]*\s*$", re.I),
    re.compile(r"^['\"‘’“”]*\s*all of us research program['\"‘’“”]*\s*$", re.I),
    re.compile(r"\ball of us\b.*\byear in review\b", re.I),
    re.compile(r"\bintroducing\b.*\ball of us\b", re.I),
    re.compile(r"^\s*interview\b.*\b(all of us|AoU)\b", re.I),
    re.compile(r"\b(all of us|AoU)\b.*\binterview\b.*\b(CEO|director|leader|principal investigator)\b", re.I),
    re.compile(r"^['\"‘’“”]*all of us['\"‘’“”]*\s*$", re.I),
]

# Title patterns that flag candidate META — disease noun in title/abstract
# overrides (substantive analysis).
META_TITLE_PATTERNS = [
    re.compile(r"\ball of us\b.*\bperspective\b", re.I),
    re.compile(r"\bdesign of\b.*\ball of us\b", re.I),
    re.compile(r"\ball of us\b.*\bcohort profile\b", re.I),
    re.compile(r"\bcohort profile\b.*\ball of us\b", re.I),
    re.compile(r"\boverview of\b.*\ball of us\b", re.I),
    re.compile(r"\ball of us\b.*\bprogram update\b", re.I),
]

META_DISEASE_NOUNS = {
    # if these appear in title alongside "All of Us", the record is likely a
    # substantive analysis and should NOT be flagged META even if title
    # matches one of the regexes above
    "cancer", "diabetes", "obesity", "hypertension", "depression",
    "anxiety", "asthma", "COPD", "stroke", "kidney", "heart", "psoriasis",
    "Alzheimer", "Parkinson", "lupus", "BRCA", "GWAS", "PRS",
    "polygenic", "screening", "phenotype", "phecode", "wearable",
    "Fitbit", "HIV", "COVID", "EHR", "machine learning", "deep learning",
    "pregnancy", "preeclampsia", "rare disease", "ELSI", "consent",
    "pharmacogenomic", "PheWAS", "Mendelian",
}


# ----------------------------------------------------------------------------
# Keyword-matching helpers
# ----------------------------------------------------------------------------

# Precompile per-keyword regexes.
# Special rules:
#   - All-uppercase acronyms <=5 chars: CASE-SENSITIVE match (so "ALL" doesn't
#     hit "All of Us" and "MS" doesn't hit "Ms.").
#   - Short tokens (<=5 chars): word boundary on both sides.
#   - Multi-word / longer terms: word boundary at start, allow trailing
#     punctuation.
def _compile_keyword(kw: str) -> re.Pattern:
    kw = kw.strip()
    is_acronym = re.fullmatch(r"[A-Z][A-Z0-9]{1,4}", kw)
    if is_acronym:
        # Case-sensitive: must appear as uppercase in the text
        return re.compile(r"\b" + re.escape(kw) + r"\b")
    if re.fullmatch(r"[A-Za-z0-9\-]+", kw) and len(kw) <= 5:
        # case-insensitive short token
        return re.compile(r"\b" + re.escape(kw) + r"\b", re.IGNORECASE)
    return re.compile(r"(?<!\w)" + re.escape(kw) + r"(?!\w)", re.IGNORECASE)


def _precompile_themes(themes: list[dict]) -> list[dict]:
    out = []
    for th in themes:
        gen = [(kw, _compile_keyword(kw)) for kw in th["general"]]
        spec = [(kw, _compile_keyword(kw)) for kw in th["specific"]]
        out.append({**th, "_gen": gen, "_spec": spec})
    return out


COMPILED_THEMES = _precompile_themes(THEMES)
CKM_PATTERNS = [(kw, _compile_keyword(kw)) for kw in SUBTHEME_CKM_TERMS]
CARDIO_STROKE_PATTERNS = [(kw, _compile_keyword(kw)) for kw in CARDIO_STROKE_CONTEXT]
NEURO_STROKE_PATTERNS = [(kw, _compile_keyword(kw)) for kw in NEURO_STROKE_CONTEXT]


# ----------------------------------------------------------------------------
# Per-record tagging
# ----------------------------------------------------------------------------

def tag_record(text: str, title: str = "") -> tuple[list[str], dict[str, list[str]], list[str]]:
    """Return (themes, evidence-per-theme, subthemes).

    Firing rule:
      - >=1 specific keyword anywhere -> fire
      - >=2 distinct general keywords anywhere -> fire
      - >=1 general keyword in the title -> fire (lower threshold for title
        hits, because titles are highly informative).
    """
    themes_hit = []
    evidence: dict[str, list[str]] = {}
    subthemes: list[str] = []

    title_text = title or ""

    for th in COMPILED_THEMES:
        spec_hits = [kw for kw, pat in th["_spec"] if pat.search(text)]
        gen_hits = [kw for kw, pat in th["_gen"] if pat.search(text)]
        # title-only hits — used for the lower threshold rule
        title_gen_hits = [kw for kw, pat in th["_gen"] if pat.search(title_text)]
        # union for evidence; uniqueness is by lowercase
        seen = set()
        all_hits = []
        for h in spec_hits + gen_hits:
            k = h.lower()
            if k not in seen:
                seen.add(k)
                all_hits.append(h)
        # decision
        fire = (
            bool(spec_hits)
            or len(set(h.lower() for h in gen_hits)) >= 2
            or bool(title_gen_hits)
        )
        if fire:
            themes_hit.append(th["code"])
            evidence[th["code"]] = all_hits

    # CKM subtheme: requires CKM-syndrome phrasing + theme 1 already firing
    if "1" in themes_hit:
        ckm_hits = [kw for kw, pat in CKM_PATTERNS if pat.search(text)]
        if ckm_hits:
            subthemes.append("1.3-CKM")

    # Stroke subthemes: "stroke" in TITLE + cardio or neuro context.
    # The locked decision says multi-tag both 1 and 14 for stroke records.
    # Restrict the forced multi-tag to records where "stroke" appears in the
    # title (otherwise a passing mention in a methods paper would force
    # cardiometabolic+neurology tags inappropriately).
    stroke_pat = _compile_keyword("stroke")
    title_has_stroke = stroke_pat.search(title_text)
    if title_has_stroke:
        cardio_ctx = any(p.search(text) for _, p in CARDIO_STROKE_PATTERNS)
        neuro_ctx = any(p.search(text) for _, p in NEURO_STROKE_PATTERNS)
        if "14" not in themes_hit:
            themes_hit.append("14")
            evidence["14"] = evidence.get("14", []) + ["stroke (title; locked decision 5)"]
        if "1" not in themes_hit and cardio_ctx:
            themes_hit.append("1")
            evidence["1"] = evidence.get("1", []) + ["stroke + cardio-embolic context"]
        if cardio_ctx:
            subthemes.append("1.4-stroke-cardio")
        if neuro_ctx or not cardio_ctx:
            subthemes.append("14.2-stroke-cerebro")

    return themes_hit, evidence, subthemes


def detect_meta(title: str, abstract: str) -> bool:
    if not title:
        return False
    t = title.strip()
    # Strong title patterns force META regardless of abstract content.
    if any(p.search(t) for p in META_TITLE_STRONG):
        return True
    # Weaker title patterns flag candidate META — disease noun in title or
    # abstract overrides (substantive analysis pub).
    matched = any(p.search(t) for p in META_TITLE_PATTERNS)
    if not matched:
        return False
    # If a disease-noun is in title or abstract, treat as substantive
    txt = (title + " " + (abstract or "")).lower()
    for noun in META_DISEASE_NOUNS:
        if re.search(r"\b" + re.escape(noun.lower()) + r"\b", txt):
            return False
    return True


# ----------------------------------------------------------------------------
# Record extraction
# ----------------------------------------------------------------------------

def extract_pub_text(d: dict) -> tuple[str, str, str, str]:
    title = d.get("pdr_title") or d.get("manual_title") or d.get("calc_title") or ""
    abstract = d.get("pdr_abstract") or d.get("manual_abstract") or d.get("calc_abstract") or ""
    # AoU pdr_abstract uses URL-encoded chars %28 %29 — replace
    abstract = abstract.replace("%28", "(").replace("%29", ")").replace("%2C", ",")
    title = title.replace("%28", "(").replace("%29", ")").replace("%2C", ",")
    year = d.get("pdr_date_year") or d.get("manual_date_year") or d.get("calc_date_year") or ""
    pmid = d.get("pubmed_id") or ""
    return title, abstract, year, pmid


def extract_proj_text(d: dict) -> tuple[str, str]:
    title = d.get("title") or ""
    parts = [title]
    for k in ("questions", "approaches", "findings"):
        v = d.get(k)
        if v:
            parts.append(str(v))
    return title, "\n".join(parts)


# ----------------------------------------------------------------------------
# Main tagging pass
# ----------------------------------------------------------------------------

def tag_publications():
    out = []
    with PUBS_IN.open() as f:
        for line in f:
            d = json.loads(line)
            title, abstract, year, pmid = extract_pub_text(d)

            # Augmentation: gap-filled abstract (both modes) + full-text body
            # (fulltext mode only). Meta detection always stays abstract-level.
            aug = AUG.get(str(d.get("record_id")), {})
            if aug.get("abstract_filled"):
                abstract = aug["abstract_filled"]
            text = f"{title}\n{abstract}"
            if MODE == "fulltext" and aug.get("has_fulltext"):
                text = f"{text}\n{aug.get('fulltext_body', '')}"

            themes, evidence, subthemes = tag_record(text, title=title)
            meta = detect_meta(title, abstract)

            # If META, exclude from substantive corpus regardless of theme hits
            in_substantive = not meta

            tag_evidence = {code: {"source": "keyword", "keywords": kws}
                            for code, kws in evidence.items()}

            out.append({
                "record_id": d.get("record_id"),
                "pubmed_id": pmid,
                "year": year,
                "title": title,
                "journal": d.get("pdr_journal_title") or d.get("manual_journal_title") or d.get("calc_journal_title") or "",
                "themes": themes,
                "subthemes": subthemes,
                "tag_evidence": tag_evidence,
                "is_meta": meta,
                "in_substantive_corpus": in_substantive,
                "admin_ics": d.get("_admin_ics", []),
                "cofunding_ics": d.get("_cofunding_ics", []),
                "tag_mode": MODE,
                "tagged_on_fulltext": bool(MODE == "fulltext" and aug.get("has_fulltext")),
                "abstract_source": aug.get("abstract_source", "orig" if abstract else "none"),
            })
    return out


def tag_projects():
    out = []
    with PROJ_IN.open() as f:
        for line in f:
            d = json.loads(line)
            title, text = extract_proj_text(d)
            themes, evidence, subthemes = tag_record(text, title=title)
            # Projects are inherently substantive — we don't run META detection
            # because "All of Us"-themed project titles are not meta-pubs.
            tag_evidence = {code: {"source": "keyword", "keywords": kws}
                            for code, kws in evidence.items()}
            out.append({
                "workspaceId": d.get("workspaceId"),
                "snapshotId": d.get("snapshotId"),
                "title": title,
                "accessTier": d.get("accessTier"),
                "ubrFocus": d.get("ubrFocus"),
                "themes": themes,
                "subthemes": subthemes,
                "tag_evidence": tag_evidence,
                "is_meta": False,
                "in_substantive_corpus": True,
            })
    return out


# ----------------------------------------------------------------------------
# I/O
# ----------------------------------------------------------------------------

def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def write_pubs_csv(path: Path, rows: list[dict]) -> None:
    cols = ["record_id", "pubmed_id", "year", "title", "journal",
            "themes", "subthemes", "is_meta", "in_substantive_corpus",
            "admin_ics", "cofunding_ics", "tag_evidence_summary"]
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            evidence_summary = "; ".join(
                f"{code}:{'|'.join(v['keywords'])}" if isinstance(v, dict) else f"{code}"
                for code, v in r["tag_evidence"].items()
            )
            w.writerow([
                r["record_id"],
                r["pubmed_id"],
                r["year"],
                r["title"],
                r["journal"],
                ";".join(r["themes"]),
                ";".join(r["subthemes"]),
                "true" if r["is_meta"] else "false",
                "true" if r["in_substantive_corpus"] else "false",
                ";".join(r["admin_ics"]),
                ";".join(r["cofunding_ics"]),
                evidence_summary,
            ])


def write_proj_csv(path: Path, rows: list[dict]) -> None:
    cols = ["workspaceId", "snapshotId", "title", "accessTier", "ubrFocus",
            "themes", "subthemes", "is_meta", "in_substantive_corpus",
            "tag_evidence_summary"]
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            evidence_summary = "; ".join(
                f"{code}:{'|'.join(v['keywords'])}" if isinstance(v, dict) else f"{code}"
                for code, v in r["tag_evidence"].items()
            )
            w.writerow([
                r["workspaceId"],
                r["snapshotId"],
                r["title"],
                r["accessTier"],
                r["ubrFocus"],
                ";".join(r["themes"]),
                ";".join(r["subthemes"]),
                "true" if r["is_meta"] else "false",
                "true" if r["in_substantive_corpus"] else "false",
                evidence_summary,
            ])


# ----------------------------------------------------------------------------
# Theme summary
# ----------------------------------------------------------------------------

THEME_NAME = {th["code"]: th["name"] for th in THEMES}


def compute_summary(pubs: list[dict], projs: list[dict]) -> list[dict]:
    pubs_sub = [p for p in pubs if p["in_substantive_corpus"]]
    pub_total = len(pubs_sub)
    proj_total = len([p for p in projs if p["in_substantive_corpus"]])

    rows = []
    # year terciles for pubs
    years = sorted([int(p["year"]) for p in pubs_sub if str(p["year"]).isdigit()])
    if years:
        n = len(years)
        early_max = years[n // 3]
        mid_max = years[2 * n // 3]
    else:
        early_max = 0
        mid_max = 0

    for th in THEMES:
        code = th["code"]
        name = th["name"]
        pubs_in = [p for p in pubs_sub if code in p["themes"]]
        projs_in = [p for p in projs if code in p["themes"]]

        admin_counter = Counter()
        cof_counter = Counter()
        early_n = mid_n = late_n = 0
        for p in pubs_in:
            for ic in p["admin_ics"]:
                admin_counter[ic] += 1
            for ic in p["cofunding_ics"]:
                cof_counter[ic] += 1
            y = p.get("year")
            if str(y).isdigit():
                yy = int(y)
                if yy <= early_max:
                    early_n += 1
                elif yy <= mid_max:
                    mid_n += 1
                else:
                    late_n += 1

        rows.append({
            "theme_code": code,
            "theme_name": name,
            "level": "top",
            "pub_count": len(pubs_in),
            "project_count": len(projs_in),
            "pub_share": round(len(pubs_in) / pub_total, 4) if pub_total else 0,
            "project_share": round(len(projs_in) / proj_total, 4) if proj_total else 0,
            "top3_admin_ics": ";".join(f"{ic}({n})" for ic, n in admin_counter.most_common(3)),
            "top3_cofunding_ics": ";".join(f"{ic}({n})" for ic, n in cof_counter.most_common(3)),
            "pubs_early": early_n,
            "pubs_mid": mid_n,
            "pubs_late": late_n,
        })

    # subthemes
    for sub_code, sub_name in [
        ("1.3-CKM", "CKM syndrome (subtheme of Cardiometabolic)"),
        ("1.4-stroke-cardio", "Cardio-embolic stroke (subtheme of Cardiometabolic)"),
        ("14.2-stroke-cerebro", "Cerebrovascular stroke (subtheme of Neurology)"),
    ]:
        pubs_in = [p for p in pubs_sub if sub_code in p["subthemes"]]
        projs_in = [p for p in projs if sub_code in p["subthemes"]]
        admin_counter = Counter()
        cof_counter = Counter()
        for p in pubs_in:
            for ic in p["admin_ics"]:
                admin_counter[ic] += 1
            for ic in p["cofunding_ics"]:
                cof_counter[ic] += 1
        rows.append({
            "theme_code": sub_code,
            "theme_name": sub_name,
            "level": "subtheme",
            "pub_count": len(pubs_in),
            "project_count": len(projs_in),
            "pub_share": round(len(pubs_in) / pub_total, 4) if pub_total else 0,
            "project_share": round(len(projs_in) / proj_total, 4) if proj_total else 0,
            "top3_admin_ics": ";".join(f"{ic}({n})" for ic, n in admin_counter.most_common(3)),
            "top3_cofunding_ics": ";".join(f"{ic}({n})" for ic, n in cof_counter.most_common(3)),
            "pubs_early": "",
            "pubs_mid": "",
            "pubs_late": "",
        })

    # audit-only META row (denominator note)
    meta_pubs = [p for p in pubs if p["is_meta"]]
    rows.append({
        "theme_code": "META",
        "theme_name": "AoU-program-meta-audit (NOT in theme-share denominator)",
        "level": "audit",
        "pub_count": len(meta_pubs),
        "project_count": 0,
        "pub_share": "",
        "project_share": "",
        "top3_admin_ics": "",
        "top3_cofunding_ics": "",
        "pubs_early": "",
        "pubs_mid": "",
        "pubs_late": "",
    })

    return rows


def write_summary(path: Path, rows: list[dict]) -> None:
    cols = ["theme_code", "theme_name", "level", "pub_count", "project_count",
            "pub_share", "project_share", "top3_admin_ics",
            "top3_cofunding_ics", "pubs_early", "pubs_mid", "pubs_late"]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)


# ----------------------------------------------------------------------------
# Stats for the audit report
# ----------------------------------------------------------------------------

def report_stats(label: str, rows: list[dict]) -> dict:
    sub = [r for r in rows if r["in_substantive_corpus"]]
    counts = [len(r["themes"]) for r in sub]
    n = len(sub)
    zero = sum(1 for c in counts if c == 0)
    high = sum(1 for c in counts if c > 5)
    mean = sum(counts) / n if n else 0
    counts_sorted = sorted(counts)
    median = counts_sorted[n // 2] if n else 0
    print(f"{label}: n={n}, zero-tag={zero} ({100*zero/n:.1f}%), >5-tag={high} ({100*high/n:.1f}%), mean={mean:.2f}, median={median}, max={max(counts) if counts else 0}")
    return {
        "n": n,
        "zero": zero,
        "high": high,
        "mean": mean,
        "median": median,
        "max": max(counts) if counts else 0,
    }


def main():
    n_aug_ft = sum(1 for r in AUG.values() if r.get("has_fulltext"))
    print(f"Tag mode: {MODE!r}  (augmentation records: {len(AUG)}, "
          f"with full text: {n_aug_ft})", flush=True)
    print("Tagging publications…", flush=True)
    pubs = tag_publications()
    print(f"  {len(pubs)} publication records processed", flush=True)
    print("Tagging projects…", flush=True)
    projs = tag_projects()
    print(f"  {len(projs)} project records processed", flush=True)

    print("\nPass-1 keyword stats:")
    pub_stats = report_stats("Publications", pubs)
    proj_stats = report_stats("Projects", projs)
    meta_pubs = [p for p in pubs if p["is_meta"]]
    print(f"  META pubs: {len(meta_pubs)}")

    write_jsonl(PUBS_OUT_JSONL, pubs)
    write_pubs_csv(PUBS_OUT_CSV, pubs)
    write_jsonl(PROJ_OUT_JSONL, projs)
    write_proj_csv(PROJ_OUT_CSV, projs)

    summary = compute_summary(pubs, projs)
    write_summary(THEME_SUMMARY_CSV, summary)

    print("\nWrote:")
    print(f"  {PUBS_OUT_JSONL}")
    print(f"  {PUBS_OUT_CSV}")
    print(f"  {PROJ_OUT_JSONL}")
    print(f"  {PROJ_OUT_CSV}")
    print(f"  {THEME_SUMMARY_CSV}")

    return pubs, projs, pub_stats, proj_stats, meta_pubs


if __name__ == "__main__":
    main()

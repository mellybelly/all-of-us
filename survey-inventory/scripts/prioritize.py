#!/usr/bin/env python3
"""Rank which AoU survey content should be harmonized with which ECHO measures.

This does NOT harmonize variables. It scores candidate AoU-survey <-> ECHO-measure
pairings (one per construct) so the harmonization work can be prioritized.

Scope: current data only. On the AoU side that means the survey content in the
current CDR; on the ECHO side it means measures on the current ECHO Cohort
Protocol (ECP v3.2). Legacy-only ECHO instruments (e.g. PHQ-9, CES-D, EPDS) are
excluded even though PlatIPUS lists them. Caregiver report about a child is an
acceptable ECHO respondent.

Inputs (all produced by the other scripts):
  aou_variables.csv              AoU items + Data Browser participant counts
  aou_surveys.csv                survey-level Data Browser participant counts
  raw/echo_platipus_counts.csv   ECHO participants per measure (PlatIPUS)

Scoring (max 15):
  2 x instrument concordance  3 same instrument | 2 overlapping items or a
                              published linking/crosswalk | 1 same construct only
  respondent fit              3 both self-report, or both reporting on the same
                              people | 2 adult self vs caregiver report about child
  sample size                 3 if min(AoU n, ECHO n) >= 20,000 | 2 if >= 5,000 | 1
  analytic value              3 needed in nearly any co-analysis, or a core ECHO
                              exposure/outcome | 2 commonly used | 1 niche
Tiers: 1 >= 13, 2 = 11-12, 3 <= 10. "core_covariate" marks the sociodemographic
pairs every co-analysis needs regardless of score.

Usage:  python3 survey-inventory/scripts/prioritize.py
"""
import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

BASICS, LIFESTYLE, OH = "The Basics", "Lifestyle", "Overall Health"
PFHH, HCAU = "Personal and Family Health History", "Health Care Access and Utilization"
SDOH, EHWB = "Social Determinants of Health", "Emotional Health History and Well-Being"
BHP, COPE = "Behavioral Health and Personality", "COVID-19 Participant Experience (COPE)"
VAX = "Minute Survey on COVID-19 Vaccines"

# Each pair: AoU selectors are (survey, kind, pattern) with kind "code" (regex on
# item_concept), "src" (substring of source_instruments) or "text" (substring of
# question_text). ECHO selectors are PlatIPUS short names or full names.
PAIRS = [
    # ---------------------------------------------------- core covariates
    dict(id="C1", domain="Sociodemographics", construct="Race and ethnicity",
         core=True, aou=[(BASICS, "code", r"^(race_|whatraceethnicity)")],
         echo=["REI", "Dem-B", "Dem-C"], ecp="REI; Dem-B; Dem-C; REI-CR",
         conc=2, resp=3, value=3,
         note="Both are multi-select self-identification. AoU follows the 2015 Census "
              "test (incl. MENA, detailed subgroups); ECHO REI was revised in v03.10. "
              "Needs a shared category scheme (e.g. OMB SPD 15)."),
    dict(id="C2", domain="Sociodemographics", construct="Sex assigned at birth and gender identity",
         core=True, aou=[(BASICS, "code", r"^(biologicalsexatbirth|gender_)")],
         echo=["Dem-B", "Dem-C"], ecp="Dem-B; Dem-C",
         conc=2, resp=3, value=3,
         note="AoU uses GenIUSS two-step items. ECHO records sex of child and caregiver "
              "in demographics forms."),
    dict(id="C3", domain="Sociodemographics", construct="Educational attainment",
         core=True, aou=[(BASICS, "code", r"^educationlevel")],
         echo=["Dem-B", "Dem-CG"], ecp="Dem-B; Dem-CG",
         conc=2, resp=3, value=3,
         note="Different category cut-points; collapse to a common ordinal scale."),
    dict(id="C4", domain="Sociodemographics", construct="Household income and financial strain",
         core=True, aou=[(BASICS, "code", r"^income")],
         echo=["IAFS-P", "IAFS-C", "IAFS_C"], ecp="IAFS-P; IAFS-C; IAFS-A",
         conc=2, resp=3, value=3,
         note="Both ask annual household income in brackets; brackets differ, and ECHO "
              "also has household size for income-to-poverty ratio."),
    dict(id="C5", domain="Sociodemographics", construct="Employment and occupation",
         core=True, aou=[(BASICS, "code", r"^employment_")],
         echo=["Occ-CG"], ecp="Occ-CG; Occ-CG-P",
         conc=2, resp=3, value=3, note="Employment status categories alignable."),
    dict(id="C6", domain="Sociodemographics", construct="Marital status and household composition",
         core=True, aou=[(BASICS, "code", r"^(maritalstatus|livingsituation_(howmanypeople|peopleunder))")],
         echo=["Dem-B", "HHC-C", "HHC-P"], ecp="Dem-B; Dem-CG",
         conc=2, resp=3, value=3, note=""),
    dict(id="C7", domain="Sociodemographics", construct="Health insurance coverage",
         core=True, aou=[(BASICS, "code", r"^(insurance|healthinsurance)"), (HCAU, "code", r"^insurance")],
         echo=["HIC"], ecp="HIC; HIC-A",
         conc=2, resp=3, value=3,
         note="Both enumerate coverage types (employer, direct purchase, Medicaid, "
              "Medicare, military, IHS...)."),
    dict(id="C8", domain="Sociodemographics", construct="Nativity, language, and acculturation",
         core=True, aou=[(BASICS, "code", r"^thebasics_(birthplace|countryborn)")],
         echo=["LA-P", "LA-C", "LA_C", "LA_P"], ecp="LA-P; LA-C; LA-A",
         conc=1, resp=3, value=2,
         note="AoU asks only country of birth; ECHO has language and acculturation scales."),
    dict(id="C9", domain="Sociodemographics", construct="Housing tenure and housing stability",
         core=True, aou=[(BASICS, "code", r"^(homeown|livingsituation_(stablehouseconcern|currentliving|livingsituation))")],
         echo=["IAFS-P", "IAFS-C"], ecp="IAFS-P; IAFS-C",
         conc=1, resp=3, value=2,
         note="Verify which housing items ECHO carries (assistance/strain) before committing."),

    # ---------------------------------------------------- psychosocial (adult self-report)
    dict(id="P1", domain="Psychosocial stress", construct="Perceived stress (PSS-10)",
         aou=[(SDOH, "src", "Cohen S")], echo=["PSS10", "NTPSS10"], ecp="NTPSS10; NTPSS10-A",
         conc=3, resp=3, value=3,
         note="Same 10-item Cohen PSS in both (ECHO via NIH Toolbox v2.0)."),
    dict(id="P2", domain="Discrimination", construct="Everyday discrimination",
         aou=[(SDOH, "src", "Williams DR")], echo=["WEDS"], ecp="WEDS",
         conc=3, resp=3, value=3,
         note="Same Williams Everyday Discrimination Scale items and attribution follow-up."),
    dict(id="P3", domain="Discrimination", construct="Discrimination in medical settings",
         aou=[(SDOH, "src", "Peek ME")], echo=["DMSS"], ecp="DMSS",
         conc=3, resp=3, value=2,
         note="Same Peek et al. adaptation of the EDS to health care settings."),
    dict(id="P4", domain="Mental health", construct="Depressive symptoms",
         aou=[(EHWB, "code", r"^phq9")], echo=["PDep_CAT", "PDep8a", "PDep"], ecp="PDep8a; PDep-CAT",
         conc=2, resp=3, value=3,
         note="PHQ-9 vs PROMIS Depression: published PROsetta Stone linking puts both on "
              "the PROMIS T-score metric. Legacy ECHO PHQ-9 data are out of scope."),
    dict(id="P5", domain="Mental health", construct="Anxiety symptoms",
         aou=[(EHWB, "code", r"^gad7")], echo=["PAnx_CAT", "PAnx8a"], ecp="PAnx8a; PAnx-CAT",
         conc=2, resp=3, value=3,
         note="GAD-7 vs PROMIS Anxiety: PROsetta Stone linking available."),
    dict(id="P6", domain="Early-life adversity", construct="Adverse childhood experiences (adult, retrospective)",
         aou=[(EHWB, "code", r"^ace_")], echo=["ACEMat"], ecp="ACE",
         conc=3, resp=3, value=3,
         note="Both use the CDC-Kaiser/BRFSS ACE items about the respondent's first 18 years."),
    dict(id="P7", domain="Early-life adversity", construct="ACEs across generations (adult retrospective vs child, by caregiver)",
         aou=[(EHWB, "code", r"^ace_")], echo=["ACE-PR", "ACE-CR", "ACE_18_20y"], ecp="ACE-PR; ACE-CR; ACE-18-20y",
         conc=2, resp=2, value=2,
         note="Same ACE domains; ECHO child ACEs are prospective (caregiver or child report)."),
    dict(id="P8", domain="General health", construct="Global physical and mental health (PROMIS Global)",
         aou=[(OH, "src", "PROMIS Global")], echo=["PGH"], ecp="PGH; PGH-A",
         conc=3, resp=3, value=3,
         note="Same PROMIS Global Health v1.2 items; T-scores directly comparable."),
    dict(id="P9", domain="Social environment", construct="Social support",
         aou=[(SDOH, "src", "Social Support Survey")],
         echo=["PES_CAT", "PES4a", "PInfS4a", "PInstrS4a"], ecp="PES4a; PInfS4a; PInstrS4a (+CAT)",
         conc=1, resp=3, value=2,
         note="MOS Social Support vs PROMIS support item banks: same subdomains "
              "(emotional, informational, tangible), different items."),
    dict(id="P10", domain="Social environment", construct="Loneliness and companionship",
         aou=[(SDOH, "src", "Hays RD")], echo=["PComp6a-A"], ecp="PComp6a-A",
         conc=1, resp=3, value=2, note="UCLA LS-8 vs PROMIS Companionship (18-20 yr olds only)."),
    dict(id="P11", domain="Neighborhood", construct="Neighborhood social cohesion",
         aou=[(SDOH, "src", "Bateman")], echo=["NE-CE-C", "NE-CE-P"], ecp="NE-CE",
         conc=2, resp=3, value=2,
         note="AoU items overlap the Sampson collective-efficacy cohesion items ECHO uses."),
    dict(id="P12", domain="Neighborhood", construct="Neighborhood disorder and safety",
         aou=[(SDOH, "src", "Ross CE")], echo=["Neigh-C", "Neigh-Preg", "NE-S-C"], ecp="Neigh-C; Neigh-Preg",
         conc=1, resp=3, value=2, note=""),
    dict(id="P13", domain="Material hardship", construct="Food insecurity",
         aou=[(SDOH, "code", r"^hvs")], echo=["IAFS-P", "IAFS-C"], ecp="IAFS-P; IAFS-C",
         conc=2, resp=3, value=3,
         note="AoU Hunger Vital Sign items are a subset of the USDA food-security items in "
              "ECHO IAFS; the 2-item HVS screen can be derived on both sides."),
    dict(id="P14", domain="Mental health", construct="Traumatic events and PTSD symptoms",
         aou=[(EHWB, "code", r"^pcl")], echo=["LSC", "CRISYS-SF"], ecp="LSC; CRISYS-SF",
         conc=1, resp=3, value=2,
         note="AoU measures PTSD symptoms (PCL-C); ECHO measures stressful/traumatic event "
              "exposure. Align on event exposure only."),
    dict(id="P15", domain="Mental health", construct="ADHD symptoms",
         aou=[(BHP, "code", r"^asrs")], echo=["CSS-SR", "CADHD-SR"], ecp="CSS-SR",
         conc=1, resp=3, value=2, note="ASRS (adults) vs Current Symptoms Scale (18-20 yr olds)."),
    dict(id="P16", domain="Health behaviors", construct="Physical activity",
         aou=[(SDOH, "src", "Bauman A")], echo=["PA", "PPAQ"], ecp="PA (derived); SPAD-P",
         conc=1, resp=3, value=2, note="IPAQ item vs pregnancy physical-activity measures."),
    dict(id="P17", domain="Social environment", construct="Religiosity and spirituality",
         aou=[(SDOH, "src", "Daily Spiritual")], echo=["RaS"], ecp="RaS",
         conc=1, resp=3, value=1, note="DSES vs ECHO attendance/religiosity items."),
    dict(id="P18", domain="General health", construct="Health literacy",
         aou=[(OH, "src", "Chew LD")], echo=["CHL"], ecp="CHL",
         conc=1, resp=3, value=1,
         note="AoU uses Chew self-report screener; ECHO uses a comprehension test."),
    dict(id="P19", domain="Personality", construct="Personality / temperament",
         aou=[(BHP, "code", r"^bfi2xs")], echo=["ATQ"], ecp="ATQ",
         conc=1, resp=3, value=1, note="BFI-2-XS vs Adult Temperament Questionnaire (18-20 yr olds)."),

    # ---------------------------------------------------- substance use
    dict(id="S1", domain="Substance use", construct="Tobacco and nicotine use",
         aou=[(LIFESTYLE, "code", r"^(smoking|electronicsmoking|cigarsmoking|hookahsmoking|smokelesstobacco)")],
         echo=["Life_C", "Life_EP", "Life_3T", "YRB-SU"], ecp="Life-C; Life-EP; Life-3T; YRB-SU",
         conc=2, resp=3, value=3,
         note="Ever/current cigarette, e-cigarette and other tobacco use alignable; "
              "prenatal tobacco is a core ECHO exposure."),
    dict(id="S2", domain="Substance use", construct="Alcohol use",
         aou=[(LIFESTYLE, "code", r"^alcohol")], echo=["Life_C", "Life_EP", "Life_3T"],
         ecp="Life-C; Life-EP; Life-3T",
         conc=2, resp=3, value=3,
         note="AUDIT-C vs ECHO quantity/frequency items: align on any use, frequency, "
              "and drinks per occasion."),
    dict(id="S3", domain="Substance use", construct="Cannabis and other drug use",
         aou=[(LIFESTYLE, "code", r"^(recreationaldruguse|past3monthusefrequency)")],
         echo=["Life_C", "SubUse_R", "YRB-SU"], ecp="Life-C; SubUse-R; YRB-SU",
         conc=2, resp=3, value=2, note="NIDA-modified ASSIST drug classes vs ECHO drug lists."),

    # ---------------------------------------------------- health history
    dict(id="H1", domain="Health history", construct="Family medical history",
         aou=[(PFHH, "text", "who in your family")], echo=["MH2_F", "MH-BF", "MH2-BF"],
         ecp="MH2-F",
         conc=2, resp=3, value=3,
         note="Both are condition checklists by biological relative; enables "
              "intergenerational analyses. Condition lists must be mapped (e.g. to ICD/SNOMED)."),
    dict(id="H2", domain="Health history", construct="Child health conditions, reported by parent",
         aou=[(PFHH, "text", "who in your family")], echo=["MH2_C", "MH2", "MHCh"],
         ecp="MH2-C; MH2",
         conc=1, resp=3, value=3,
         note="AoU family history records conditions in the respondent's sons/daughters; "
              "ECHO caregivers report the child's diagnoses (asthma, ADHD, ASD, obesity...)."),
    dict(id="H3", domain="Health history", construct="Adult personal medical conditions",
         aou=[(PFHH, "code", r"^(diagnosedhealthcondition|.*currently|.*howold)")],
         echo=["MH2_F", "PMCI"], ecp="MH2-F; PMCI",
         conc=1, resp=3, value=2,
         note="ECHO captures the biological mother's own conditions via family history and "
              "pregnancy conditions; AoU EHR data may be a better complement."),
    dict(id="H4", domain="Reproductive health", construct="Pregnancy and reproductive history",
         aou=[(OH, "code", r"^(pregnancy|overallhealth_(hysterectomy|menstrual|ovary|pregnan))")],
         echo=["Par", "PMCI", "PI"], ecp="PMCI; PI",
         conc=1, resp=3, value=2,
         note="AoU has limited items (current pregnancy, hysterectomy); ECHO is detailed."),
    dict(id="H5", domain="Health care", construct="Health care access, utilization and affordability",
         aou=[(HCAU, "code", r"^(healthadvice|delayedmedicalcare|cantaffordcare)")],
         echo=["ReceiptPC", "Dent-PR", "HIC"], ecp="HIC; (prenatal care derived)",
         conc=1, resp=3, value=2, note="Few shared items beyond insurance."),
    dict(id="H6", domain="COVID-19", construct="COVID-19 infection, impact and vaccination",
         aou=[(COPE, "code", r"."), (VAX, "code", r".")],
         echo=["C19-aPV", "C19-3-aPV", "C19_4_aPV", "C19Vac"], ecp="(ad hoc COVID-19 forms)",
         conc=1, resp=3, value=1,
         note="Both time-limited (2020-2022); AoU counts not in Data Browser."),
]

# Constructs ECHO measures (adult respondents) with no AoU survey counterpart.
GAPS = [
    ("Sleep health", "SHAdult; PSD4a; PSRI4a; MSHPrg", "No AoU sleep survey items (Fitbit sleep is not survey data)."),
    ("Self-reported weight/height", "Wt-CG; HtWt-P", "AoU uses physical measurements and EHR, not survey items."),
    ("Diet", "DHQ3; DSQ-SR; MFSP", "No AoU diet survey."),
    ("Couple relationship quality", "CSI4", "No AoU counterpart."),
    ("Household chemical and secondhand smoke exposure", "HCExp; HESHS", "No AoU survey counterpart."),
    ("Benevolent childhood experiences", "BCE", "AoU asks ACEs only."),
    ("Suicidal thoughts and behaviors", "(none on ECP)", "AoU EHWB has SITBI items; no ECHO adult counterpart."),
    ("Psychosis, mania, eating disorders", "(none on ECP)", "AoU BHP/EHWB UK Biobank items; no ECHO counterpart."),
]


def size_score(n):
    return 3 if n >= 20000 else 2 if n >= 5000 else 1


def main():
    aou = list(csv.DictReader((ROOT / "aou_variables.csv").open()))
    survey_n = {r["survey"]: r["databrowser_participants"]
                for r in csv.DictReader((ROOT / "aou_surveys.csv").open())}
    echo = list(csv.DictReader((ROOT / "raw" / "echo_platipus_counts.csv").open(encoding="utf-8", errors="replace")))

    out = []
    for p in PAIRS:
        items, surveys = [], []
        for survey, kind, pat in p["aou"]:
            for r in aou:
                if r["survey"] != survey or r["field_type"] == "descriptive":
                    continue
                if (kind == "code" and re.search(pat, r["item_concept"])) or \
                   (kind == "src" and pat in r["source_instruments"]) or \
                   (kind == "text" and pat.lower() in r["question_text"].lower()):
                    items.append(r)
            surveys.append(survey)
        counts = [int(r["n_participants_databrowser"]) for r in items if r["n_participants_databrowser"]]
        n_aou = max(counts) if counts else max(
            (int(survey_n[s]) for s in surveys if survey_n.get(s)), default=0)
        n_aou_basis = "items" if counts else ("survey" if n_aou else "unknown")

        matched = [e for e in echo if e["short_name"] in p["echo"] or e["name"] in p["echo"]]
        n_echo = max((int(e["n_participants"]) for e in matched if e["n_participants"]), default=0)

        size = size_score(min(n_aou, n_echo)) if n_aou and n_echo else 1
        score = 2 * p["conc"] + p["resp"] + size + p["value"]
        tier = 1 if score >= 13 else 2 if score >= 11 else 3
        out.append([
            p["id"], tier, score, "yes" if p.get("core") else "", p["domain"], p["construct"],
            "; ".join(dict.fromkeys(surveys)), len(items),
            "; ".join(dict.fromkeys(r["item_concept"] for r in items))[:400],
            n_aou or "", n_aou_basis, p["ecp"],
            "; ".join(f"{e['short_name'] or e['name']} ({e['n_participants']})" for e in matched),
            n_echo or "", p["conc"], p["resp"], size, p["value"], p["note"],
        ])
    out.sort(key=lambda r: (r[3] != "yes", r[1], -r[2], r[0]))
    header = ["id", "tier", "priority_score", "core_covariate", "domain", "construct",
              "aou_surveys", "aou_n_items", "aou_item_concepts", "aou_n_participants",
              "aou_n_basis", "echo_ecp_forms", "echo_platipus_measures_n",
              "echo_n_participants", "score_instrument_concordance",
              "score_respondent_fit", "score_sample_size", "score_analytic_value", "rationale"]
    with (ROOT / "harmonization_priorities.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(out)
    with (ROOT / "harmonization_gaps.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["construct", "echo_forms", "note"])
        w.writerows(GAPS)
    for r in out:
        print(f"T{r[1]} {r[2]:>2} {r[3]:3} {r[0]:4} {r[5][:50]:50} AoU n={r[9]!s:>7} ({r[7]} items)  ECHO n={r[13]!s:>6}")


if __name__ == "__main__":
    main()

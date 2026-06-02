"""Generate per-IC briefs (~1 page each) under per_ic_briefs/.

For each IC in scope, build a brief with:
- IC mission paragraph (curated)
- IC priorities (bulleted)
- AoU activity per priority (corpus counts + example PMIDs)
- Alignment verdict (strong/partial/weak/none)
- Recommended Refresh actions

Pulls per-pub theme tags and PMIDs from publications_tagged.csv to surface
3 example PMIDs per IC per major theme.
"""
import csv
import os
from collections import defaultdict

LANDSCAPE = "/Users/melissahaendel/Documents/GitHub/all-of-us/resources/aou-research-landscape"
OUT_DIR = "/Users/melissahaendel/Documents/GitHub/all-of-us/resources/aou-ic-alignment"
BRIEFS_DIR = os.path.join(OUT_DIR, "per_ic_briefs")
os.makedirs(BRIEFS_DIR, exist_ok=True)

IC_MISSION = {
    "NIH-Wide": "NIH is the largest public funder of biomedical research worldwide, organized as 27 Institutes and Centers under a 2021–2025 Strategic Plan with three Objectives (advance biomedical and behavioral sciences; develop and sustain scientific capacity; ensure integrity and accountability) and five crosscutting themes (minority health, women's health, lifespan, collaboration, data science).",
    "NCI": "The National Cancer Institute leads, conducts, and supports cancer research, training, dissemination, and access programs across the National Cancer Program. Its strategic frame is the 2023 National Cancer Plan (8 goals to end cancer as we know it) and the Annual Plan & Budget Proposal that translates the plan into funding priorities.",
    "NHGRI": "NHGRI is NIH's institute for human genomics, with the 2020 Strategic Vision (Nature, 'Forefront of Genomics') organized as four areas (principles & values; robust foundation; breaking down barriers; compelling research projects) and ten Bold Predictions for human genomics by 2030.",
    "NHLBI": "NHLBI funds heart, lung, blood, and sleep (HLBS) research. Its FY2026–2030 Strategic Vision sets four goals, eight objectives, and five crosscutting themes (data science, health disparities, lifestyle, community engagement, women's health).",
    "NIA": "NIA leads NIH research on aging and is the designated lead Institute for Alzheimer's disease and related dementias. Its 2020–2025 Strategic Directions are organized as Goals A–I across aging biology, dementia, social factors, disparities, infrastructure, and dissemination.",
    "NIAAA": "NIAAA funds alcohol research. Its FY2024–2028 Strategic Plan covers etiology of alcohol-related harms, prevention, treatment of AUD, alcohol-HIV intersection, FASD, health disparities, and alcohol-research infrastructure.",
    "NIAID": "NIAID funds research on infectious, immune-mediated, and allergic diseases. The FY2026 Congressional Justification reaffirms priorities in emerging infectious diseases, HIV/AIDS, TB, antimicrobial resistance, fundamental immunology, autoimmune disease, allergy/asthma, and transplantation.",
    "NIAMS": "NIAMS supports research on arthritis, musculoskeletal, and skin diseases (AMS). The FY2025–2029 Strategic Plan emphasizes foundational research, clinical and translational AMS science, workforce, and health equity.",
    "NIBIB": "NIBIB funds biomedical engineering, imaging, and bioengineering research. Its strategic plan's four goals cover innovative biomedical technologies, point-of-care/wireless/personal health informatics, mechanism-to-clinical translation, and biomedical imaging.",
    "NICHD": "NICHD funds research on child health, human development, reproductive biology, and rehabilitation. The 2025 plan's five priorities cover molecular/cellular development, gynecologic/andrologic/urologic health, healthy pregnancies, child & adolescent health, and therapeutics/devices for pregnant/lactating women, children, and people with disabilities.",
    "NIDA": "NIDA funds research on the causes, consequences, prevention, and treatment of drug use and substance use disorders. The 2022–2026 plan's thematic areas are prevention, treatment, public health (including HIV), neurobiology of addiction, disparities, workforce, and emerging issues (polysubstance, cannabis, e-cigarettes, fentanyl).",
    "NIDDK": "NIDDK supports research on diabetes, digestive, kidney, and hematologic diseases; obesity; and nutrition. Its 2025 plan has four Scientific Goals (foundational, clinical trials, dissemination, stakeholder engagement) and detailed Research Opportunities under each.",
    "NIEHS": "NIEHS leads environmental health science research. The FY2025–2029 Strategic Plan (final draft) covers foundational environmental health science, climate & health, environmental justice, exposome/exposure science, New Approach Methodologies (NAMs), and workforce/infrastructure.",
    "NIGMS": "NIGMS funds basic biomedical research not focused on a specific disease, including pharmacogenomics (PGRN), training, and capacity building (IDeA). The 2021–2025 plan has five goals around investigator-initiated research, diverse workforce, capacity building, scientific themes (including PGx), and stewardship.",
    "NIMH": "NIMH funds research on mental illnesses. The 2023 Strategic Plan Update has four goals (brain mechanisms; lifespan; interventions; public health impact) with cross-cutting themes including comorbidities, computational approaches, harnessing data, and suicide prevention.",
    "NIMHD": "NIMHD leads research on minority health and health disparities. The 2021–2025 plan has nine goals organized in three categories (scientific research, research sustaining, outreach), plus a Leap Forward Research Challenge for visionary cross-NIH disparities science.",
    "NINDS": "NINDS funds research on neurological disorders. The Interim 2025–2026 Strategic Plan covers foundational neuroscience, translational/clinical neurology, workforce, data science & cohort infrastructure, health equity, pain research (HEAL Initiative), and stroke.",
    "NLM": "NLM is the world's largest biomedical library and the locus for data science and open science at NIH. The 2017–2027 plan has three Goals (digital research enterprise; dissemination & engagement; workforce) with explicit mention of supporting All of Us, BRAIN Initiative, and Cancer Moonshot data.",
    "NCATS": "NCATS funds translational science research and supports the CTSA Program. The 2025–2030 plan covers therapeutic & diagnostic development, the CTSA Program, rare diseases (RDCRN/TRND/repurposing), crosscutting strategies (team science, data science, partnerships), and stewardship.",
    "NCCIH": "NCCIH funds research on complementary and integrative health, including the new (since 2021) emphasis on Whole Person Health: empowering people in interconnected biological, behavioral, social, and environmental domains.",
    "NEI": "NEI funds vision research. The 2021–2025 plan covers visual neuroscience, retinal disease, glaucoma, regenerative medicine (Audacious Goals Initiative), vision-care disparities, data science & imaging, and workforce.",
}


def load_themes_per_pub():
    """Returns dict[ic_code → list[(pmid, year, title, theme_tags)]]
    grouped by primary IC under the theme-attribution rules."""
    rows = []
    with open(os.path.join(LANDSCAPE, "publications_tagged.csv")) as f:
        for r in csv.DictReader(f):
            if r["in_substantive_corpus"].lower() != "true":
                continue
            rows.append(r)
    return rows


def main():
    # Load priorities by IC
    priorities_by_ic = defaultdict(list)
    with open(os.path.join(OUT_DIR, "ic_priorities.csv")) as f:
        for r in csv.DictReader(f):
            priorities_by_ic[r["ic"]].append(r)

    # Load theme name lookup
    theme_names = {}
    with open(os.path.join(LANDSCAPE, "theme_summary.csv")) as f:
        for row in csv.DictReader(f):
            theme_names[row["theme_code"]] = row["theme_name"]

    # Load alignment_matrix_corpus_only & priority_only for verdict
    corpus_m = {}
    priority_m = {}
    for path, m in [("alignment_matrix_corpus_only.csv", corpus_m),
                    ("alignment_matrix_priority_only.csv", priority_m)]:
        with open(os.path.join(OUT_DIR, path)) as f:
            reader = csv.reader(f)
            header = next(reader)
            ic_cols = header[2:-1]  # skip theme_code, theme_name, row_total
            for row in reader:
                if row[0] == "TOTAL":
                    continue
                th = row[0]
                m[th] = {ic: float(v) for ic, v in zip(ic_cols, row[2:-1])}

    # Build example-pub index for each IC (theme attribution)
    THEME_TO_IC = {
        "1":  [("NHLBI", 0.7), ("NIDDK", 0.3)],
        "2":  [("NHGRI", 1.0)],
        "3":  [("NLM",  1.0)],
        "4":  [("NIMH", 0.7), ("NIDA", 0.2), ("NIAAA", 0.1)],
        "5":  [("NCI",  1.0)],
        "6":  [("NIMHD", 1.0)],
        "7":  [("NIBIB", 0.5), ("NHLBI", 0.2), ("NIDDK", 0.15), ("NIMH", 0.15)],
        "8":  [("NIAID", 1.0)],
        "9":  [("NIAID", 0.5), ("NIAMS", 0.5)],
        "10": [("NCATS", 0.5), ("NHGRI", 0.5)],
        "11": [("NIA",   0.8), ("NINDS", 0.2)],
        "12": [("NIAMS", 0.7), ("NCI",   0.3)],
        "13": [("NHLBI", 1.0)],
        "14": [("NINDS", 1.0)],
        "15": [("NICHD", 1.0)],
        "16": [("NIGMS", 0.6), ("NHGRI", 0.2), ("NHLBI", 0.1), ("NCI", 0.1)],
        "17": [("NIH-Wide", 0.7), ("NHGRI", 0.3)],
        "18": [("NEI",  1.0)],
        "19": [("NIEHS", 1.0)],
    }

    pub_rows = load_themes_per_pub()
    examples_by_ic_theme = defaultdict(lambda: defaultdict(list))
    pub_count_by_ic_theme = defaultdict(lambda: defaultdict(float))

    for r in pub_rows:
        themes = [t for t in r["themes"].split(";") if t.strip().isdigit()]
        themes = [t for t in themes if t in THEME_TO_IC]
        if not themes:
            continue
        per_theme = 1.0 / len(themes)
        for th in themes:
            for ic, w in THEME_TO_IC[th]:
                weight = per_theme * w
                pub_count_by_ic_theme[ic][th] += weight
                if r.get("pubmed_id") and weight >= 0.1:
                    examples_by_ic_theme[ic][th].append((float(r["year"] or 0), r["pubmed_id"], r["title"]))

    for ic in examples_by_ic_theme:
        for th in examples_by_ic_theme[ic]:
            examples_by_ic_theme[ic][th].sort(reverse=True)  # newest first

    # Generate brief for each IC
    for ic in IC_MISSION:
        priorities = priorities_by_ic.get(ic, [])
        out = []
        out.append(f"# {ic} — AoU Alignment Brief")
        out.append("")
        out.append("## Mission")
        out.append("")
        out.append(IC_MISSION[ic])
        out.append("")
        out.append("## Strategic-plan priorities")
        out.append("")
        for p in priorities:
            out.append(f"- **{p['priority_name']}** ({p['priority_id']}). {p['priority_description']}")
        out.append("")
        out.append("## AoU corpus activity by aligned theme")
        out.append("")
        # For each theme this IC has priority for, show count + 3 examples
        ic_themes = set()
        for p in priorities:
            for t in p["aou_theme_tags"].split(";"):
                t = t.strip()
                if t.isdigit():
                    ic_themes.add(t)
        # Also include themes the IC dominates in corpus
        for th in corpus_m:
            if corpus_m[th].get(ic, 0) >= 5.0:
                ic_themes.add(th)
        for th in sorted(ic_themes, key=lambda x: int(x)):
            count = pub_count_by_ic_theme[ic].get(th, 0)
            prio_n = sum(
                1 for p in priorities if th in [x.strip() for x in p["aou_theme_tags"].split(";")]
            )
            line = f"- **Theme {th} {theme_names.get(th, '')}** — {count:.1f} fractional pubs attributed; IC plan priorities tagged with this theme: {prio_n}."
            ex = examples_by_ic_theme[ic].get(th, [])[:3]
            if ex:
                line += " Example PMIDs: " + "; ".join(f"PMID:{e[1]}" for e in ex)
            out.append(line)
        out.append("")

        # Verdict
        total_corpus = sum(corpus_m[th].get(ic, 0) for th in corpus_m)
        total_priority = sum(priority_m[th].get(ic, 0) for th in priority_m)
        # heuristic
        if total_corpus > 100 and total_priority >= 5:
            verdict = "**STRONG** — substantial AoU corpus footprint and clear IC strategic priorities align."
        elif total_corpus > 30 or total_priority >= 5:
            verdict = "**PARTIAL** — alignment exists in subset of themes; some IC priorities under-served by AoU corpus."
        elif total_corpus > 5:
            verdict = "**WEAK** — limited AoU activity in this IC's domain; small set of overlapping themes."
        else:
            verdict = "**NONE/MINIMAL** — almost no AoU corpus material; IC depends on other infrastructure."
        out.append("## Alignment verdict")
        out.append("")
        out.append(verdict)
        out.append(f" Composite corpus weight: {total_corpus:.1f}; priority count: {total_priority:.0f}.")
        out.append("")

        # Recommended Refresh actions — hand-curated per IC
        actions = REFRESH_ACTIONS.get(ic, [
            f"Confirm IC priority list against the most recent {ic} plan update before recommending specific Refresh investments.",
        ])
        out.append("## Recommended Refresh actions")
        out.append("")
        for a in actions:
            out.append(f"- {a}")
        out.append("")
        out.append("---")
        out.append("")
        out.append(f"*Generated from `ic_priorities.csv`, `publications_reattributed.csv`, "
                   f"`alignment_matrix_*.csv`. {len(priorities)} priorities extracted from the {ic} "
                   f"strategic plan PDF in `strategic-plans/`.*")

        path = os.path.join(BRIEFS_DIR, f"{ic}.md")
        with open(path, "w") as f:
            f.write("\n".join(out))
        print(f"wrote {path}")


REFRESH_ACTIONS = {
    "NIH-Wide": [
        "Use AoU's track record on 4 of 5 NIH-Wide Crosscutting Themes (minority health, lifespan, collaborative science, data science) to anchor the WG-1 (Roadmap Refresh) framing that AoU is pan-NIH infrastructure, not a single-IC asset.",
        "Acknowledge the climate / environmental crosscutting gap honestly — AoU does not yet deliver on the Lifespan-Environment intersection some NIH-Wide framings imply.",
        "Position AoU's Researcher Workbench as the empirical proof-point for the NIH-Wide collaborative-science crosscut.",
    ],
    "NCI": [
        "Highlight AoU's contribution to Cancer Plan Goal 4 (Eliminate Inequities) and Goal 7 (Maximize Data Utility) — the two goals where AoU's design uniquely advances NCP execution.",
        "Engage NCI Cancer Screening Research Network on potential AoU data linkage for multi-cancer detection studies.",
        "Note the imaging-data supply gap relative to NCI's AI-for-screening priority — consider whether the Refresh recommends upstream imaging-data investment.",
    ],
    "NHGRI": [
        "Position AoU as the empirical instrument for NHGRI's Bold Prediction #5 (millions of participants with genome + phenotype data) and #9 (equitable benefit across ancestries).",
        "Surface AoU's subcontinental ancestry work (PMID:40480197) as evidence AoU is ahead of generic 'multi-ancestry' framing.",
        "Use the VUS-and-penetrance work in AoU corpus to support NHGRI Bold Prediction #7 (VUS obsolescence).",
    ],
    "NHLBI": [
        "Lead with the 382-pub / 3,292-project Cardiometabolic footprint as the WG-1 evidence that AoU delivers NHLBI's largest mission area at scale.",
        "Surface wearables-derived sleep work as alignment with NHLBI Objective 7 (data science) + Crosscutting Lifestyle theme.",
        "Note multi-omics gap (HA1: 24 pubs) — the 2026 omics release should close this for NHLBI's Objective 4 (individual differences).",
    ],
    "NIA": [
        "Highlight rapid post-2023 growth in Aging/ADRD theme (+4.7 trend, 75 pubs) as evidence AoU is becoming a real aging-research resource.",
        "Surface the loneliness/social-factors → biological-aging integration as alignment with NIA Goal C (personal/interpersonal/societal factors on aging).",
    ],
    "NIAAA": [
        "Connect AoU's tobacco/alcohol/SDOH multi-tag work with NIAAA Goal 5 (alcohol-related health disparities).",
        "Flag the alcohol-HIV intersection opportunity (NIAAA Objective 2) — AoU's combined cohort enables this in a way registries cannot.",
    ],
    "NIAID": [
        "Surface the AoU long-COVID / EBV / virome work (PMIDs 41714741, 41882355) as alignment with NIAID's emerging-infectious-disease and immunology priorities.",
        "Use the autoimmune corpus (107 pubs) as joint NIAID/NIAMS evidence.",
    ],
    "NIAMS": [
        "Acknowledge that the large dermatology footprint (197 pubs) is concentrated in a few groups; do NOT recommend elevating dermatology as a Refresh priority.",
        "Surface the autoimmune-systemic-comorbidity work (e.g., SLE + CVD) as NIAMS strategic-plan alignment.",
    ],
    "NIBIB": [
        "Lead with wearables (73 pubs / 923 projects) as alignment with NIBIB Goal 2 (point-of-care/wireless/personal health informatics).",
        "Flag imaging gap (HA3: 8 pubs) and consider whether the Refresh should recommend upstream imaging data infrastructure investment in partnership with NIBIB.",
    ],
    "NICHD": [
        "Note the pub:project ratio gap in maternal/pregnancy (37 pubs vs. 678 projects) — work is underway but not yet flowing to publications.",
        "Surface the postpartum-CV-risk multi-tag work as NICHD/NHLBI/NIH-Wide CCT-Women's Health alignment.",
        "Pediatric data linkage is a gap — connect to NICHD Priority 4 (Child & Adolescent Health).",
    ],
    "NIDA": [
        "Surface the e-cigarette + cannabis + tobacco multi-substance work as alignment with NIDA's emerging-issues (G7) priority.",
        "Use AoU's national-cohort SDOH dimension to differentiate from NIDA's traditional treatment-population samples.",
    ],
    "NIDDK": [
        "Lead with diabetes + obesity + CKD as the major NIDDK-aligned cluster (combined ~100 fractional pubs).",
        "Flag microbiome gap (HA7: 11 pubs) — AoU does not collect microbiome samples, a structural limit on NIDDK alignment.",
        "Surface the MASLD genetics + ultrasound-phenotype work as NIDDK digestive-diseases alignment.",
    ],
    "NIEHS": [
        "**Largest single demand-supply gap** in the matrix: NIEHS has 6 plan priorities in T19; AoU has 7 substantive pubs. Refresh should consider whether to recommend material environmental-exposure linkage investment (PM2.5, EJI, heat, water).",
        "Position AoU as a potential human-data source for NIEHS NAMs validation pipelines.",
        "Use AoU's SDOH-environment hybrid work (HA5: 12 pubs) as a partial-alignment bridge.",
    ],
    "NIGMS": [
        "Surface AoU PGx footprint (32 pubs) as alignment with NIGMS PGRN priority — but flag the small absolute size relative to AoU's multi-ancestry PGx potential.",
        "Note that NIGMS is included in scope specifically for the pharmacogenomics dimension.",
    ],
    "NIMH": [
        "Lead with the 254-pub mental-health footprint as 4th-largest theme in AoU.",
        "Highlight the genomic-and-non-genomic alignment with NIMH Goal 1 Objective 1.2 (e.g., PMID:40007508).",
        "Surface mental-physical comorbidity work (dysphonia+depression, sleep+AF) as alignment with NIMH X-COMOR cross-cut and as a 'latent area' where AoU is ahead of IC plan articulation.",
    ],
    "NIMHD": [
        "**The pan-IC infrastructure case strongest cell:** NIMHD Goal 7 explicitly asks for 'analysis of populations experiencing health disparities in big data sets ... and future big science initiatives' — AoU is the literal answer to this.",
        "Use the 458-pub / 3,070-project SDOH footprint as Refresh evidence that the disparities mandate is being delivered at scale.",
        "Connect AoU's UBR-oversample design to NIMHD's Leap Forward Research Challenge.",
    ],
    "NINDS": [
        "Note non-ADRD neurology footprint (77 pubs / 567 projects) is mid-size and growing post-2023.",
        "Surface stroke work (14.2-stroke-cerebro subtheme) as joint NINDS/NHLBI alignment.",
        "Connect to NINDS HEAL portfolio on pain research.",
    ],
    "NLM": [
        "**Most mission-explicit alignment in any plan:** NLM 2017–2027 Strategic Plan literally names All of Us as one of the initiatives NLM will accommodate.",
        "Lead with NLM Goal 1 (digital research enterprise) + AoU Researcher Workbench as paired infrastructure.",
        "Position AoU + NLM as the empirical proof-point that the agency's data-science strategy works.",
    ],
    "NCATS": [
        "Use AoU rare-disease + ACMG-actionable-gene work to align with NCATS rare-diseases priority (G3).",
        "Surface NCATS Translator as a downstream Monarch/AoU data consumer (cross-IC infrastructure linkage).",
        "Note PER USER GUIDANCE: NCATS is a downstream dependency but should NOT be positioned as a plausible anchor for pan-NIH coordination — keep this in mind when drafting recommendations.",
    ],
    "NCCIH": [
        "Use AoU's mental-health + SDOH + cardiometabolic + lifestyle integration as partial alignment with NCCIH Whole Person Health (O3).",
        "Acknowledge the environmental-domain gap: NCCIH's whole-person framework requires environmental data AoU largely lacks.",
        "Surface NCCIH pain priority (X-PAIN) as alignment with NINDS HEAL portfolio for cross-IC framing.",
    ],
    "NEI": [
        "Lead with ophthalmology-disparities work (e.g., glaucoma access, PMID:38200661) as alignment with NEI Vision Health Equity priority.",
        "Flag retinal-imaging data gap as a barrier to NEI G6 (data science & imaging) alignment.",
    ],
}


if __name__ == "__main__":
    main()

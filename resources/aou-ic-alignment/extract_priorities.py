"""Extract priorities-section text from each strategic plan PDF.

Pulls full text by page so we can find "Strategic Priorities", "Research
Goals", "Objectives", "Goals", etc. and then tag priorities to AoU themes.

Outputs a JSON file with per-IC chunks of text from priority-relevant pages
for downstream curation into ic_priorities.csv.
"""
import json
import os
import re
import sys

import pypdf

PLAN_DIR = "/Users/melissahaendel/Documents/GitHub/all-of-us/resources/strategic-plans"
OUT_DIR = "/Users/melissahaendel/Documents/GitHub/all-of-us/resources/aou-ic-alignment"

# IC scope. Map filename -> (IC code, plan_year_label)
IN_SCOPE = {
    "NIH_Wide_Strategic_Plan_FY2021-2025.pdf": ("NIH-Wide", "2021-2025"),
    "NCI_National_Cancer_Plan.pdf": ("NCI", "NationalCancerPlan-2023"),
    "NCI_Annual_Plan_Budget_Proposal_FY2026.pdf": ("NCI", "AnnualPlanBudget-FY2026"),
    "NHGRI_Strategic_Vision_2020.pdf": ("NHGRI", "2020"),
    "NHLBI_Strategic_Vision_FY2026-2030.pdf": ("NHLBI", "FY2026-2030"),
    "NIA_Strategic_Directions_2020-2025.pdf": ("NIA", "2020-2025"),
    "NIAAA_Strategic_Plan_FY2024-2028.pdf": ("NIAAA", "FY2024-2028"),
    "NIAID_Congressional_Justification_FY2026.pdf": ("NIAID", "CJ-FY2026"),
    "NIAMS_Strategic_Plan_FY2025-2029_FactSheet.pdf": ("NIAMS", "FY2025-2029"),
    "NIBIB_Strategic_Plan.pdf": ("NIBIB", "current"),
    "NICHD_Strategic_Plan_2025.pdf": ("NICHD", "2025"),
    "NIDA_Strategic_Plan_2022-2026.pdf": ("NIDA", "2022-2026"),
    "NIDDK_Strategic_Plan_for_Research_2025.pdf": ("NIDDK", "2025"),
    "NIEHS_Strategic_Plan_FY2025-2029_FinalDraft.pdf": ("NIEHS", "FY2025-2029-Draft"),
    "NIGMS_Strategic_Plan_2021-2025.pdf": ("NIGMS", "2021-2025"),
    "NIMH_Strategic_Plan_for_Research_2023_Update.pdf": ("NIMH", "2023Update"),
    "NIMHD_Strategic_Plan_2021-2025.pdf": ("NIMHD", "2021-2025"),
    "NINDS_Interim_Strategic_Plan_2025-2026.pdf": ("NINDS", "Interim2025-2026"),
    "NLM_Strategic_Plan_2017-2027.pdf": ("NLM", "2017-2027"),
    "NCATS_Strategic_Plan_2025-2030.pdf": ("NCATS", "2025-2030"),
    "NCCIH_Strategic_Plan_2021-2025.pdf": ("NCCIH", "2021-2025"),
    "NEI_Strategic_Plan_Vision_for_the_Future_2021-2025.pdf": ("NEI", "2021-2025"),
}


def page_text(path):
    out = []
    try:
        r = pypdf.PdfReader(path)
        for i, p in enumerate(r.pages):
            t = ""
            try:
                t = p.extract_text() or ""
            except Exception:
                t = ""
            out.append({"page": i + 1, "text": t})
    except Exception as e:
        print(f"ERR reading {path}: {e}", file=sys.stderr)
    return out


def main():
    blob = {}
    for fn, (ic, year) in IN_SCOPE.items():
        path = os.path.join(PLAN_DIR, fn)
        if not os.path.exists(path):
            print(f"MISSING {path}", file=sys.stderr)
            continue
        pages = page_text(path)
        n_chars = sum(len(p["text"]) for p in pages)
        print(f"{ic:9s} {year:25s} {fn:55s} {len(pages):4d}p {n_chars:7d}ch")
        blob[fn] = {"ic": ic, "year": year, "pages": pages}
    out_path = os.path.join(OUT_DIR, "plan_pages.json")
    with open(out_path, "w") as f:
        json.dump(blob, f)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()

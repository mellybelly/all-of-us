#!/usr/bin/env python3
"""
Phase 3a — Crosswalk between the 19-theme corpus taxonomy and the 8 current AoU
Scientific Roadmap focus areas.

Inputs:
  ../aou-research-landscape/publications_tagged.jsonl
  ../aou-research-landscape/projects_tagged.jsonl
  ../aou-research-landscape/theme_summary.csv
  ../aou-research-landscape/taxonomy.md

Outputs (in same directory as this script):
  theme_to_focus_area.csv      — 19 themes x focus-area assignments
  publications_tagged_with_focus.csv  — pubs + focus-area columns
  projects_tagged_with_focus.csv      — projects + focus-area columns
  focus_area_summary.csv       — bottom-up corpus shares per focus area
  crosswalk_19_to_8.md         — full markdown narrative (separate file, written by hand-tuned writer)
"""
from __future__ import annotations
import csv
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANDSCAPE = HERE.parent / "aou-research-landscape"

# ---------------------------------------------------------------------------
# 8 Roadmap focus areas (canonical short codes)
# ---------------------------------------------------------------------------
FOCUS_AREAS = {
    "FA1": "Prevalent Common & Rare Conditions",
    "FA2": "Maternal & Child Health",
    "FA3": "Healthy Aging & Resilience Across the Lifespan",
    "FA4": "Return of Results on Individual & Population Health",
    "FA5": "Lifestyle, Substance, & Behavioral Health",
    "FA6": "Environment",
    "FA7": "Health Equity",
    "FA8": "Genetics & Biology",
}

# ---------------------------------------------------------------------------
# Theme -> focus-area mapping.
# Each theme can map to one or more focus areas. The first is the "primary" home;
# subsequent are cross-touches. Themes flagged as orphan have no clean home.
#
# The mapping logic is captured in the per-theme `notes`. Where a theme is
# substantively split across focus areas, multi-mapping is preserved.
# ---------------------------------------------------------------------------
THEME_MAP = {
    "1": {
        "name": "Cardiometabolic disease",
        "focus_areas": ["FA1", "FA8"],
        "is_orphan": False,
        "notes": (
            "Primarily Common & Rare Conditions (FA1); subtheme 1.3-CKM and "
            "polygenic/Mendelian cardiometabolic genetics cross-touch Genetics & "
            "Biology (FA8)."
        ),
    },
    "2": {
        "name": "Genomics methods & complex-trait genetics",
        "focus_areas": ["FA8"],
        "is_orphan": False,
        "notes": (
            "Maps directly to Genetics & Biology (FA8). NOTE: 'Genetics & Biology' "
            "as named excludes proteomics/metabolomics/transcriptomics — those "
            "would need a renamed 'Multi-omics & Biology' area to fit cleanly. "
            "See orphan analysis."
        ),
    },
    "3": {
        "name": "Methods, infrastructure & phenotyping (non-genomic)",
        "focus_areas": [],
        "is_orphan": True,
        "notes": (
            "ORPHAN. AI/ML, EHR phenotyping, AoU workbench tooling, OMOP/FHIR "
            "harmonization. None of the 8 focus areas accommodates methods/"
            "infrastructure as a first-class concern. ~20% of corpus — the "
            "single largest orphan."
        ),
    },
    "4": {
        "name": "Mental health, behavioral & substance use",
        "focus_areas": ["FA5", "FA1"],
        "is_orphan": False,
        "notes": (
            "Primarily Lifestyle, Substance & Behavioral Health (FA5); psychiatric "
            "disorders also fit Common & Rare Conditions (FA1)."
        ),
    },
    "5": {
        "name": "Cancer",
        "focus_areas": ["FA1", "FA8"],
        "is_orphan": False,
        "notes": (
            "Primarily Common & Rare Conditions (FA1); hereditary-cancer "
            "subthemes (5.1, 5.6) cross-touch Genetics & Biology (FA8)."
        ),
    },
    "6": {
        "name": "Social determinants of health & health disparities",
        "focus_areas": ["FA7"],
        "is_orphan": False,
        "notes": (
            "Maps directly to Health Equity (FA7). The cross-cutting nature of "
            "SDOH means many pubs in this theme are double-tagged with disease "
            "themes."
        ),
    },
    "7": {
        "name": "Wearables & digital health",
        "focus_areas": [],
        "is_orphan": True,
        "notes": (
            "ORPHAN. Wearables/remote monitoring are slide-7 'reflections since "
            "2023' candidates for elevation but have no home in the 8 areas. "
            "Could be tucked into FA5 (Lifestyle) as activity-tracking, but that "
            "misses sleep/HRV/biometric methods work."
        ),
    },
    "8": {
        "name": "Infectious disease & immunology",
        "focus_areas": ["FA1"],
        "is_orphan": False,
        "notes": (
            "Common & Rare Conditions (FA1) — HIV, COVID-19, hepatitis, EBV, "
            "etc. are all prevalent/chronic disease topics."
        ),
    },
    "9": {
        "name": "Autoimmune & inflammatory disease",
        "focus_areas": ["FA1"],
        "is_orphan": False,
        "notes": "Common & Rare Conditions (FA1).",
    },
    "10": {
        "name": "Rare disease & Mendelian genetics",
        "focus_areas": ["FA1", "FA8", "FA4"],
        "is_orphan": False,
        "notes": (
            "Common & Rare Conditions (FA1, explicit 'rare'); Genetics & Biology "
            "(FA8); and Return of Results (FA4) since ACMG actionable variants "
            "directly drive return-of-results workflows."
        ),
    },
    "11": {
        "name": "Aging, frailty & ADRD",
        "focus_areas": ["FA3", "FA1"],
        "is_orphan": False,
        "notes": (
            "Primarily Healthy Aging & Resilience (FA3); ADRD also fits Common "
            "& Rare Conditions (FA1)."
        ),
    },
    "12": {
        "name": "Dermatology",
        "focus_areas": ["FA1", "FA7"],
        "is_orphan": False,
        "notes": (
            "Common & Rare Conditions (FA1); the heavy AoU dermatology corpus "
            "is largely disparities-framed and cross-touches Health Equity (FA7)."
        ),
    },
    "13": {
        "name": "Respiratory & sleep medicine",
        "focus_areas": ["FA1"],
        "is_orphan": False,
        "notes": "Common & Rare Conditions (FA1).",
    },
    "14": {
        "name": "Neurology (non-ADRD)",
        "focus_areas": ["FA1"],
        "is_orphan": False,
        "notes": "Common & Rare Conditions (FA1).",
    },
    "15": {
        "name": "Pregnancy, maternal & women's health",
        "focus_areas": ["FA2"],
        "is_orphan": False,
        "notes": (
            "Maternal & Child Health (FA2) — note that the 8-area name says "
            "'Maternal & Child' but AoU is an adult cohort, so 'Child' is "
            "structurally thin (no peds enrollment yet)."
        ),
    },
    "16": {
        "name": "Pharmacogenomics & drug response",
        "focus_areas": ["FA8", "FA4"],
        "is_orphan": False,
        "notes": (
            "Genetics & Biology (FA8) and Return of Results (FA4) — PGx is the "
            "canonical 'genotype-drives-treatment-decision' use case for ROR."
        ),
    },
    "17": {
        "name": "ELSI, participant engagement & recruitment",
        "focus_areas": ["FA4", "FA7"],
        "is_orphan": False,
        "notes": (
            "Return of Results (FA4, ROR ethics is the dominant ELSI sub-area) "
            "and Health Equity (FA7, recruitment of underrepresented groups)."
        ),
    },
    "18": {
        "name": "Ophthalmology, ENT & sensory medicine",
        "focus_areas": ["FA1", "FA7"],
        "is_orphan": False,
        "notes": (
            "Common & Rare Conditions (FA1); strong disparities-in-sensory-care "
            "framing cross-touches Health Equity (FA7)."
        ),
    },
    "19": {
        "name": "Environmental health & climate",
        "focus_areas": ["FA6"],
        "is_orphan": False,
        "notes": "Environment (FA6) — clean fit but tiny theme (<1% of pubs).",
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_jsonl(path: Path):
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def theme_focus_areas(theme_code: str) -> list[str]:
    return THEME_MAP.get(theme_code, {}).get("focus_areas", [])


def record_focus_areas(themes: list[str]) -> list[str]:
    fas: set[str] = set()
    for t in themes:
        for fa in theme_focus_areas(str(t)):
            fas.add(fa)
    return sorted(fas)


# ---------------------------------------------------------------------------
# Build outputs
# ---------------------------------------------------------------------------
def write_theme_to_focus_area_csv():
    out = HERE / "theme_to_focus_area.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "theme_code",
                "theme_name",
                "focus_areas",
                "focus_area_names",
                "is_orphan",
                "notes",
            ]
        )
        for code, info in THEME_MAP.items():
            w.writerow(
                [
                    code,
                    info["name"],
                    ";".join(info["focus_areas"]),
                    ";".join(FOCUS_AREAS[fa] for fa in info["focus_areas"]),
                    "yes" if info["is_orphan"] else "no",
                    info["notes"],
                ]
            )
    print(f"wrote {out}")


def attach_focus_to_pubs():
    src = LANDSCAPE / "publications_tagged.jsonl"
    out = HERE / "publications_tagged_with_focus.csv"
    fa_counter_pub: Counter[str] = Counter()
    fa_orphan_pub = 0
    total_substantive = 0
    pub_rows = []
    for rec in load_jsonl(src):
        if not rec.get("in_substantive_corpus", True):
            continue
        total_substantive += 1
        themes = [str(t) for t in rec.get("themes", [])]
        fas = record_focus_areas(themes)
        if not fas:
            fa_orphan_pub += 1
        for fa in fas:
            fa_counter_pub[fa] += 1
        pub_rows.append(
            {
                "record_id": rec.get("record_id"),
                "pubmed_id": rec.get("pubmed_id"),
                "year": rec.get("year"),
                "themes": ";".join(themes),
                "focus_areas": ";".join(fas),
                "n_focus_areas": len(fas),
                "is_orphan_pub": int(len(fas) == 0),
                "title": (rec.get("title") or "").replace("\n", " ").strip(),
            }
        )
    with out.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "record_id",
                "pubmed_id",
                "year",
                "themes",
                "focus_areas",
                "n_focus_areas",
                "is_orphan_pub",
                "title",
            ],
        )
        w.writeheader()
        for row in pub_rows:
            w.writerow(row)
    print(f"wrote {out} ({len(pub_rows)} substantive pubs)")
    return fa_counter_pub, fa_orphan_pub, total_substantive


def attach_focus_to_projects():
    src = LANDSCAPE / "projects_tagged.jsonl"
    out = HERE / "projects_tagged_with_focus.csv"
    fa_counter_proj: Counter[str] = Counter()
    fa_orphan_proj = 0
    total_substantive = 0
    proj_rows = []
    for rec in load_jsonl(src):
        if not rec.get("in_substantive_corpus", True):
            continue
        total_substantive += 1
        themes = [str(t) for t in rec.get("themes", [])]
        fas = record_focus_areas(themes)
        if not fas:
            fa_orphan_proj += 1
        for fa in fas:
            fa_counter_proj[fa] += 1
        proj_rows.append(
            {
                "workspaceId": rec.get("workspaceId"),
                "themes": ";".join(themes),
                "focus_areas": ";".join(fas),
                "n_focus_areas": len(fas),
                "is_orphan_proj": int(len(fas) == 0),
                "title": (rec.get("title") or "").replace("\n", " ").strip(),
            }
        )
    with out.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "workspaceId",
                "themes",
                "focus_areas",
                "n_focus_areas",
                "is_orphan_proj",
                "title",
            ],
        )
        w.writeheader()
        for row in proj_rows:
            w.writerow(row)
    print(f"wrote {out} ({len(proj_rows)} substantive projects)")
    return fa_counter_proj, fa_orphan_proj, total_substantive


def write_focus_area_summary(
    fa_pub: Counter[str],
    fa_proj: Counter[str],
    total_pub: int,
    total_proj: int,
):
    """Per-focus-area: corpus counts and shares; also per-focus-area theme breakdown."""
    out = HERE / "focus_area_summary.csv"
    # for each focus area, which themes contribute, and how many pubs/projects of each
    # we need to re-walk the data to get per-theme-within-focus-area counts
    src_pub = LANDSCAPE / "publications_tagged.jsonl"
    src_proj = LANDSCAPE / "projects_tagged.jsonl"
    fa_theme_pub: dict[str, Counter[str]] = defaultdict(Counter)
    fa_theme_proj: dict[str, Counter[str]] = defaultdict(Counter)
    for rec in load_jsonl(src_pub):
        if not rec.get("in_substantive_corpus", True):
            continue
        themes = [str(t) for t in rec.get("themes", [])]
        for t in themes:
            for fa in theme_focus_areas(t):
                fa_theme_pub[fa][t] += 1
    for rec in load_jsonl(src_proj):
        if not rec.get("in_substantive_corpus", True):
            continue
        themes = [str(t) for t in rec.get("themes", [])]
        for t in themes:
            for fa in theme_focus_areas(t):
                fa_theme_proj[fa][t] += 1
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "focus_area_code",
                "focus_area_name",
                "n_pubs",
                "pub_share_of_corpus",
                "n_projects",
                "proj_share_of_corpus",
                "contributing_themes",
                "theme_pub_breakdown",
                "theme_proj_breakdown",
            ]
        )
        for fa_code, fa_name in FOCUS_AREAS.items():
            n_pub = fa_pub.get(fa_code, 0)
            n_proj = fa_proj.get(fa_code, 0)
            pub_share = round(n_pub / total_pub, 4) if total_pub else 0
            proj_share = round(n_proj / total_proj, 4) if total_proj else 0
            theme_pub_break = ";".join(
                f"{t}({n})" for t, n in fa_theme_pub[fa_code].most_common()
            )
            theme_proj_break = ";".join(
                f"{t}({n})" for t, n in fa_theme_proj[fa_code].most_common()
            )
            contributing_themes = ";".join(
                t for t, info in THEME_MAP.items() if fa_code in info["focus_areas"]
            )
            w.writerow(
                [
                    fa_code,
                    fa_name,
                    n_pub,
                    pub_share,
                    n_proj,
                    proj_share,
                    contributing_themes,
                    theme_pub_break,
                    theme_proj_break,
                ]
            )
    print(f"wrote {out}")


def main():
    write_theme_to_focus_area_csv()
    fa_pub, orphan_pub, total_pub = attach_focus_to_pubs()
    fa_proj, orphan_proj, total_proj = attach_focus_to_projects()
    write_focus_area_summary(fa_pub, fa_proj, total_pub, total_proj)

    # Print summary stats
    print()
    print(f"Substantive pubs:     {total_pub}")
    print(f"  Orphan (no FA):     {orphan_pub} ({orphan_pub / total_pub:.1%})")
    print(f"Substantive projects: {total_proj}")
    print(f"  Orphan (no FA):     {orphan_proj} ({orphan_proj / total_proj:.1%})")
    print()
    print("Pub counts by focus area:")
    for fa, name in FOCUS_AREAS.items():
        n = fa_pub.get(fa, 0)
        print(f"  {fa} {name:55s} {n:5d}  ({n / total_pub:.1%})")
    print()
    print("Project counts by focus area:")
    for fa, name in FOCUS_AREAS.items():
        n = fa_proj.get(fa, 0)
        print(f"  {fa} {name:55s} {n:5d}  ({n / total_proj:.1%})")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build survey- and variable-level inventories for All of Us and ECHO.

Reads the raw data dictionaries fetched by acquire.py and writes:

  aou_surveys.csv        one row per All of Us survey instrument (codebook tab)
  aou_variables.csv      one row per AoU survey question, with answer options
                         and Registered/Controlled Tier privacy rules
  echo_measures.csv      one row per ECHO ECP v3.2 measure (Measures Master List)
  echo_variables.csv     one row per variable in the ECHO public-use codebook,
                         with answer options, linked back to its ECP measure
  harmonization_map.csv  header-only template for the AoU <-> ECHO crosswalk

Usage:  python3 survey-inventory/scripts/build_inventory.py
"""
import collections
import csv
import html
import pathlib
import re
import warnings

import openpyxl

warnings.filterwarnings("ignore", module="openpyxl")

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"

# Codebook tabs that are scoring guides, not survey instruments.
AOU_SKIP_TABS = {"ReadMe"}
# Excel truncates tab names at 31 chars; restore the full survey names.
AOU_SURVEY_NAMES = {
    "Basics": "The Basics",
    "Personal and Family Health Hist": "Personal and Family Health History",
    "Healthcare Access and Utilizati": "Health Care Access and Utilization",
    "COPE": "COVID-19 Participant Experience (COPE)",
    "Minute Survey on COVID-19 Vacci": "Minute Survey on COVID-19 Vaccines",
    "Emotional Health History": "Emotional Health History and Well-Being",
    "Behavioral Health": "Behavioral Health and Personality",
}


def clean(value):
    """Strip HTML, collapse whitespace; None -> ''."""
    if value is None:
        return ""
    text = html.unescape(str(value))
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()


def norm_header(value):
    return clean(value).lower()


def write_csv(name, header, rows):
    path = ROOT / name
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"{name}: {len(rows):,} rows")


# ---------------------------------------------------------------- All of Us

def is_scoring_tab(title):
    return "Scoring" in title or title.endswith(" S")


def read_aou_tab(ws):
    """Return (header->index map, data rows) for a REDCap-format codebook tab."""
    rows = [r for r in ws.iter_rows(values_only=True) if any(c is not None for c in r)]
    for i, row in enumerate(rows):
        headers = [norm_header(c) for c in row]
        if "item concept" in headers:
            return {h: j for j, h in enumerate(headers) if h}, rows[i + 1:]
    return None, []


def build_aou():
    wb = openpyxl.load_workbook(RAW / "aou_survey_codebook.xlsx", read_only=True)
    surveys, variables = [], []
    for ws in wb.worksheets:
        title = ws.title.strip()
        if title in AOU_SKIP_TABS or is_scoring_tab(title):
            continue
        title = AOU_SURVEY_NAMES.get(title, title)
        cols, rows = read_aou_tab(ws)
        if cols is None:
            print(f"WARNING: no 'Item Concept' header in AoU tab {title!r}")
            continue

        def get(row, *names):
            for n in names:
                j = cols.get(n)
                if j is not None and j < len(row) and row[j] is not None:
                    return clean(row[j])
            return ""

        n_questions = 0
        forms, versions = [], []
        rt_rules = ct_rules = 0
        for row in rows:
            concept = get(row, "item concept")
            if not concept:
                continue
            ftype = get(row, "field type")
            form = get(row, "form name")
            version = get(row, "version")
            if form and form not in forms:
                forms.append(form)
            for v in filter(None, (s.strip() for s in version.split(","))):
                if v not in versions:
                    versions.append(v)
            if ftype == "descriptive":
                continue
            n_questions += 1
            # Basics/Lifestyle/etc. carry tier rules in "Field Annotation";
            # newer tabs have explicit Registered/Controlled Tier Rules columns.
            annotation = get(row, "field annotation")
            rt = get(row, "registered tier rules") or (
                annotation if annotation.startswith("REGISTERED_") else "")
            ct = get(row, "controlled tier rules") or (
                annotation if annotation.startswith("CONTROLLED_") else "")
            rt_rules += bool(rt)
            ct_rules += bool(ct)
            variables.append([
                title, version, form, get(row, "section header")[:300], concept,
                ftype, get(row, "field label"),
                get(row, "choices, calculations, or slider labels"),
                get(row, "text validation type or show slider number"),
                get(row, "branching logic (show field only if...)"),
                rt, ct,
            ])
        surveys.append([title, "; ".join(forms), "; ".join(versions),
                        n_questions, rt_rules, ct_rules])

    write_csv("aou_surveys.csv",
              ["survey", "form_names", "versions", "n_questions",
               "n_registered_tier_rules", "n_controlled_tier_rules"], surveys)
    write_csv("aou_variables.csv",
              ["survey", "version", "form_name", "section_header",
               "item_concept", "field_type", "question_text", "answer_options",
               "validation", "branching_logic", "registered_tier_rule",
               "controlled_tier_rule"], variables)


# --------------------------------------------------------------------- ECHO

def flag_cols(row, header_row2, start, stop):
    """Names of the sub-columns in [start, stop) that are marked non-blank."""
    return [clean(header_row2[i]) for i in range(start, stop)
            if row[i] not in (None, "", "N", "n")]


def build_echo():
    ws = openpyxl.load_workbook(RAW / "echo_measures_master_list.xlsx",
                                read_only=True)["ECP v3.2"]
    rows = list(ws.iter_rows(values_only=True))
    h1 = [clean(c) for c in rows[0]]
    h2 = rows[1]

    def idx(name):
        return h1.index(name)

    i_spec, i_first = idx("Specializations (v3.2)"), idx("First Visit")
    i_cb, i_age = idx("Completed by"), idx("Child Age Range (months)")
    i_table = idx("Database Table Name")
    visit_cols = list(range(i_first, idx("Preg ID")))
    # Visit headers span year sub-columns (e.g. "Ages 3-5yrs" x 2024..2030).
    visit_names, last = [], ""
    for i in visit_cols:
        last = h1[i] or last
        visit_names.append(last)

    measures, table_to_measure = [], {}
    for row in rows[3:]:
        if not row[2]:
            continue
        visits = []
        for i, name in zip(visit_cols, visit_names):
            if row[i] not in (None, "", "N", "n") and name not in visits:
                visits.append(name)
        tables = [t.strip() for t in re.split(r"[,;\n]", clean(row[i_table]) and str(row[i_table])) if t.strip()]
        rec = [clean(row[0]), clean(row[1]), clean(row[2]), clean(row[3]),
               clean(row[5]), clean(row[6]),
               "; ".join(flag_cols(row, h2, i_spec, i_first)),
               "; ".join(visits),
               "; ".join(flag_cols(row, h2, i_cb, i_age)),
               clean(row[i_age]), clean(row[i_age + 1]),
               "; ".join(tables)]
        measures.append(rec)
        for t in tables:
            table_to_measure.setdefault(t, rec)

    write_csv("echo_measures.csv",
              ["concept_domain", "data_element", "form_short_name", "measure",
               "group", "protocol_version", "specializations", "visits",
               "completed_by", "child_age_min_months", "child_age_max_months",
               "database_tables"], measures)

    wb = openpyxl.load_workbook(RAW / "echo_codebook_public_use.xlsx",
                                read_only=True)
    codes = collections.defaultdict(list)
    ws = wb["Code_Lists"]
    ws.reset_dimensions()
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r and r[0]:
            codes[clean(r[0])].append(f"{clean(r[1])}, {clean(r[2])}")

    ws = wb["Study_Variables"]
    ws.reset_dimensions()
    variables = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r or not r[0]:
            continue
        r = tuple(r[:12]) + (None,) * (12 - len(r))
        dataset = clean(r[0])
        base = re.sub(r"_C1$", "", dataset)
        m = table_to_measure.get(dataset) or table_to_measure.get(base)
        prefix = dataset.split("_")[0]
        kind = ("derived" if prefix in ("Der", "Scores") else
                "lab/biospecimen" if prefix in ("Lab", "Spec") or prefix.startswith("BC") else
                "form")
        code_list = clean(r[5])
        variables.append([
            dataset, "Cycle 1" if dataset.endswith("_C1") else "Cycle 2", kind,
            clean(r[1]),
            m[2] if m else "", m[3] if m else "", m[0] if m else "",
            clean(r[2]), clean(r[3]), clean(r[4]), code_list,
            " | ".join(codes.get(code_list, [])),
            clean(r[6]) or clean(r[7]), clean(r[8]),
            "; ".join(filter(None, (clean(r[9]), clean(r[10]), clean(r[11])))),
        ])

    write_csv("echo_variables.csv",
              ["dataset", "cycle", "dataset_kind", "instrument_name",
               "ecp_form_short_name", "ecp_measure", "ecp_concept_domain",
               "variable_name", "variable_label", "variable_type", "code_list",
               "answer_options", "unit", "variable_category",
               "terminology_standard"], variables)


def main():
    build_aou()
    build_echo()
    template = ROOT / "harmonization_map.csv"
    if not template.exists():
        write_csv("harmonization_map.csv",
                  ["construct", "construct_domain", "aou_survey",
                   "aou_item_concept", "aou_question_text", "echo_measure",
                   "echo_dataset", "echo_variable_name", "echo_variable_label",
                   "match_type", "respondent_note", "transform_note",
                   "standard_code", "reviewer", "status"], [])


if __name__ == "__main__":
    main()

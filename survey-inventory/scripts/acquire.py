#!/usr/bin/env python3
"""Download the public source data dictionaries for the survey inventory.

Sources (all publicly downloadable, no login required):

  All of Us
    - Survey Codebooks (REDCap data-dictionary format, one tab per survey),
      linked from https://support.researchallofus.org/hc/en-us/articles/360051991531
      (Google Sheet, exported as .xlsx). Covers every fielded survey available
      in the Registered and Controlled Tier CDRs, with tier privacy rules.

  ECHO Cohort (ECHOPortal public Resource Library, Cycle 2 "Public Use Data
  Reference Materials": https://echoportal.org/ResourceLibrary/Resources/Home)
    - ECP v3.2 Measures Master List  (one row per measure/form)
    - ECHO Codebook for Public Use    (one row per variable + code lists)
    - Release Notes                   (public data release contents)
    - ECHO Cohort Data and Biospecimen Collection Protocol (ECP) v3.2

ECHOPortal resource IDs change between releases; if a download returns HTML
instead of a file, re-check the IDs on the Cycle 2 Public Use Data page.

Usage:  python3 survey-inventory/scripts/acquire.py
"""
import datetime
import json
import pathlib
import urllib.request

RAW = pathlib.Path(__file__).resolve().parent.parent / "raw"

AOU_CODEBOOK_SHEET = "1pODkE2bFN-kmVtYp89rtrJg7oXck4Fsex58237x47mA"
ECHO_DL = "https://echoportal.org/ResourceLibrary/Resources/DownloadResource/{}"

SOURCES = {
    "aou_survey_codebook.xlsx":
        f"https://docs.google.com/spreadsheets/d/{AOU_CODEBOOK_SHEET}/export?format=xlsx",
    "echo_measures_master_list.xlsx": ECHO_DL.format(9629),
    "echo_codebook_public_use.xlsx": ECHO_DL.format(9636),
    "echo_release_notes.pdf": ECHO_DL.format(9634),
    "echo_ecp_protocol_v3.2.pdf": ECHO_DL.format(9610),
}

# AoU Research Hub Survey Explorer (https://www.researchallofus.org/data-tools/survey-explorer/):
# English survey PDFs annotated with the original source of each item and a
# numbered "Sources" bibliography.
SURVEY_EXPLORER = "https://www.researchallofus.org/wp-content/themes/research-hub-wordpress-theme/media/"
for _name, _path in {
    "The Basics": "2024/The_Basics_LF.pdf",
    "Lifestyle": "surveys/Survey_Lifestyle_Eng_Src.pdf",
    "Overall Health": "surveys/Survey_OverallHealth_Eng_Src.pdf",
    "Personal and Family Health History": "surveys/Survey_PaFHH_Eng_Src.pdf",
    "Health Care Access and Utilization": "surveys/Survey_HealthCare_Eng_Src.pdf",
    "Social Determinants of Health": "surveys/Survey_SDOH_Eng_Src.pdf",
    "Emotional Health History and Well-Being": "surveys/Survey_EHWB_Eng_Src.pdf",
    "Behavioral Health and Personality": "surveys/Survey_BHP_Eng_Src.pdf",
}.items():
    SOURCES[f"survey_explorer/{_path.rsplit('/', 1)[1]}"] = SURVEY_EXPLORER + _path


def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        disposition = r.headers.get("Content-Disposition", "")
        body = r.read()
    if body[:15].lower().startswith((b"<!doctype", b"<html")):
        raise RuntimeError(f"{url} returned HTML, not a file (resource ID moved?)")
    dest.write_bytes(body)
    return disposition, len(body)


def main():
    (RAW / "survey_explorer").mkdir(parents=True, exist_ok=True)
    manifest = {"retrieved": datetime.date.today().isoformat(), "files": {}}
    for name, url in SOURCES.items():
        disposition, size = fetch(url, RAW / name)
        manifest["files"][name] = {"url": url, "bytes": size,
                                   "content_disposition": disposition}
        print(f"{name}: {size:,} bytes  {disposition}")
    (RAW / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()

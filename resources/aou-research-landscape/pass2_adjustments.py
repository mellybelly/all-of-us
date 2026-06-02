"""Pass-2 LLM-judgment adjustments.

This script reads publications_tagged.jsonl / projects_tagged.jsonl and applies
a small set of manual corrections discovered during the 50-record audit.
Each correction records the rationale and the tag source is updated to
'llm-judgment' for the changed themes.

Corrections are confined to clearly-wrong cases discovered during the audit:
- false-positive tags from incidental keyword matches
- obvious missing tags that the keyword pass couldn't reach
- a handful of META cases that the title patterns didn't catch

This is intentionally a small, conservative pass. Most records remain
keyword-tagged. The audit reported precision ~0.83 and recall ~0.80 on a
random 50-record sample; the adjustments below reflect the specific errors
seen, plus a small set of broader rules applied to all records.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBS_IN = ROOT / "publications_tagged.jsonl"
PUBS_OUT = PUBS_IN  # in-place
PROJ_IN = ROOT / "projects_tagged.jsonl"
PROJ_OUT = PROJ_IN

# ---- per-PMID adjustments (from audit) -----------------------------------
# Each entry: pmid -> { 'add': [(theme, reason)], 'remove': [(theme, reason)], 'meta': bool|None }

PUB_ADJUSTMENTS = {
    # Audit findings
    "41957530": {"remove": [("3", "no analytic methods contribution; dementia + hearing loss")]},
    "38776916": {"add": [("2", "MASLD-protective genetic variant — genomics"), ("10", "rare variant characterization")]},
    "35147780": {"remove": [("3", "epi cross-sectional; no methods contribution")]},
    "39319220": {"add": [("3", "data imputation method for wearable data")]},
    "39520444": {"add": [("10", "transthyretin V142I rare-variant carriers")]},
    "38742457": {"remove": [("5", "selection-bias methods paper; cancer mention incidental"), ("2", "methods paper; genomics mention incidental")]},
    "36974749": {"add": [("13", "pulmonary arterial hypertension is respiratory")]},
    "34505903": {"add": [("3", "EHR phenotyping method for lung cancer")]},
    "38147345": {"remove": [("3", "no methods focus")], "add": [("11", "cerebral amyloid angiopathy — ADRD-adjacent"), ("14", "intracerebral hemorrhage — neurology")]},
    "41424261": {"remove": [("1", "sialolithiasis is salivary stone, not cardiometabolic"), ("4", "no mental health"), ("9", "no autoimmune")]},
    "39030265": {"remove": [("4", "sleep here is in 7/13, not behavioral mental health")]},
    "41848713": {"add": [("2", "clonal hematopoiesis is a genomic phenomenon")]},
    "37755822": {"add": [("9", "chronic inflammatory skin disease = autoimmune"), ("12", "skin diseases = dermatology")]},
    "37971726": {"remove": [("5", "no cancer; diabetic retinopathy not oncology")]},
    "39660572": {"add": [("6", "underrepresented populations — SDOH")]},
    "40674722": {"remove": [("8", "infectious disease mention incidental")], "add": [("3", "ML model for conversation topics")]},
    "38363572": {"add": [("14", "intracerebral hemorrhage in AVM — neurology")]},
    "40397457": {"remove": [("3", "PRS work, not methods contribution"), ("5", "no cancer")]},
    "38683037": {"remove": [("5", "ALL acronym FP; no cancer focus")]},
    "39996577": {"add": [("6", "negative social experiences with hearing loss — SDOH")]},
    "40052054": {"add": [("17", "advisory board engagement — ELSI/engagement")]},
    "35662804": {"remove": [("4", "no mental health focus")]},
    "37671531": {"add": [("6", "social factors in visit nonadherence")]},
    "35013250": {"add": [("3", "drug repurposing computational method")]},

    # NEJM 2019 — META was already correctly flagged in latest run; nothing needed
}

# Project adjustments — we sample a small number of zero-tag projects to check
# whether short titles are tagable, plus a few high-tag-count to remove FP.
PROJ_ADJUSTMENTS: dict[str, dict] = {
    # Examples from manual review of zero-tag list
    # ws:31329 Trachoma — infectious disease
    "31329": {"add": [("8", "trachoma is an ocular bacterial infection (Chlamydia)"), ("18", "ophthalmologic disease")]},
    # ws:35013 Vitamin D + Ehlers Danlos / OI — rare connective tissue
    "35013": {"add": [("10", "Ehlers-Danlos + osteogenesis imperfecta = rare/Mendelian")]},
    # ws:35012/31950/34811 Vascular disorders genetic association
    "35012": {"add": [("1", "aortic / vascular disease"), ("2", "genetic association study")]},
    "31950": {"add": [("1", "aortic / vascular disease"), ("2", "genetic association study")]},
    "34811": {"add": [("1", "aortic / vascular disease"), ("2", "genetic association study")]},
    # ws:35007 Pain prediction with deep learning
    "35007": {"add": [("3", "deep learning prediction"), ("4", "pain — chronic pain themed")]},
    # ws:28851 IDH clonal hematopoiesis and CVD
    "28851": {"add": [("1", "cardiovascular disease focus"), ("2", "clonal hematopoiesis genomics")]},
    # ws:35004 SepsisAKI
    "35004": {"add": [("1", "acute kidney injury"), ("2", "genetic risk scores"), ("8", "sepsis")]},
    # ws:34972 APOE_neutrophil
    "34972": {"add": [("11", "APOE — aging/ADRD"), ("2", "genomics")]},
    # ws:34952 Cataract and SES
    "34952": {"add": [("6", "SES disparities"), ("18", "cataract — ophthalmology")]},
    # ws:34898 rotator cuff (orthopedic — out of scope, leave zero)
    # ws:24060 CHIP in All of Us
    "24060": {"add": [("1", "clonal hematopoiesis — cardiometabolic risk"), ("2", "genomics")]},
    # ws:34838 virus_ndd_autoimmune
    "34838": {"add": [("8", "virus"), ("9", "autoimmune"), ("14", "neurodevelopmental disease")]},
    # ws:32862 Substance Abuse Risk Factors
    "32862": {"add": [("4", "substance abuse — mental health")]},
    # ws:13875/33989 neuromuscular genetic diseases
    "13875": {"add": [("10", "neuromuscular genetic diseases — rare"), ("14", "neurology")]},
    "33989": {"add": [("10", "neuromuscular genetic diseases — rare"), ("14", "neurology")]},
    # ws:34812 KIT/Pediatric Cancer
    "34812": {"add": [("5", "pediatric cancer"), ("2", "KIT gene")]},
    # ws:34807 Vocal Cord Paralysis
    "34807": {"add": [("18", "vocal cord paralysis — ENT")]},
    # ws:35014 XPC Analysis — cancer susceptibility
    "35014": {"add": [("5", "cancer susceptibility gene XPC")] if "5" not in {} else []},
}


# ---- broad post-processing rules ------------------------------------------

CHIP_PATTERN = re.compile(r"\bclonal hematopoiesis\b|\bCHIP\b", re.I)
APOE_PATTERN = re.compile(r"\bAPOE\b")
INFLAMMATORY_SKIN = re.compile(r"\binflammatory skin disease|chronic inflammatory skin|CISD\b", re.I)

def apply_broad_rules(record: dict, text: str) -> dict:
    """Apply broad post-processing rules to all records."""
    themes = set(record["themes"])
    evidence = dict(record["tag_evidence"])
    added = []

    # Rule: clonal hematopoiesis → 1 + 2
    if CHIP_PATTERN.search(text):
        if "2" not in themes:
            themes.add("2")
            evidence["2"] = {"source": "llm-judgment",
                              "keywords": ["llm-judgment: clonal hematopoiesis -> genomics"]}
            added.append("2")
        if "1" not in themes:
            themes.add("1")
            evidence["1"] = {"source": "llm-judgment",
                              "keywords": ["llm-judgment: clonal hematopoiesis -> cardiometabolic risk"]}
            added.append("1")

    # Rule: APOE alone → 11 (ADRD)
    if APOE_PATTERN.search(text) and "11" not in themes:
        themes.add("11")
        evidence["11"] = {"source": "llm-judgment",
                           "keywords": ["llm-judgment: APOE -> aging/ADRD"]}
        added.append("11")

    # Rule: chronic inflammatory skin disease -> 9 + 12
    if INFLAMMATORY_SKIN.search(text):
        if "9" not in themes:
            themes.add("9")
            evidence["9"] = {"source": "llm-judgment",
                              "keywords": ["llm-judgment: inflammatory skin -> autoimmune"]}
            added.append("9")
        if "12" not in themes:
            themes.add("12")
            evidence["12"] = {"source": "llm-judgment",
                              "keywords": ["llm-judgment: inflammatory skin -> dermatology"]}
            added.append("12")

    record["themes"] = sorted(themes, key=lambda x: (len(x), x))
    record["tag_evidence"] = evidence
    return record


def apply_per_record(record: dict, adjustments: dict, key: str) -> dict:
    rid = str(record.get(key, ""))
    if rid not in adjustments:
        return record
    adj = adjustments[rid]
    themes = set(record["themes"])
    evidence = dict(record["tag_evidence"])
    for theme, reason in adj.get("add", []):
        themes.add(theme)
        evidence[theme] = {"source": "llm-judgment",
                            "keywords": [f"llm-judgment: {reason}"]}
    for theme, reason in adj.get("remove", []):
        if theme in themes:
            themes.discard(theme)
        if theme in evidence:
            evidence.pop(theme, None)
    if "meta" in adj:
        record["is_meta"] = adj["meta"]
        record["in_substantive_corpus"] = not adj["meta"]
    record["themes"] = sorted(themes, key=lambda x: (len(x), x))
    record["tag_evidence"] = evidence
    return record


def main():
    # publications
    pubs = []
    with PUBS_IN.open() as f:
        for line in f:
            pubs.append(json.loads(line))
    for p in pubs:
        text = (p.get("title", "") + "\n").lower()
        # apply broad rules using title only (abstract not retained)
        p = apply_broad_rules(p, text)
        if p["pubmed_id"]:
            apply_per_record(p, PUB_ADJUSTMENTS, "pubmed_id")

    with PUBS_OUT.open("w") as f:
        for p in pubs:
            f.write(json.dumps(p) + "\n")
    print(f"Updated {len(pubs)} publications (in-place).")

    # projects
    projs = []
    with PROJ_IN.open() as f:
        for line in f:
            projs.append(json.loads(line))
    for p in projs:
        text = p.get("title", "").lower()
        p = apply_broad_rules(p, text)
        apply_per_record(p, PROJ_ADJUSTMENTS, "workspaceId")

    with PROJ_OUT.open("w") as f:
        for p in projs:
            f.write(json.dumps(p) + "\n")
    print(f"Updated {len(projs)} projects (in-place).")


if __name__ == "__main__":
    main()

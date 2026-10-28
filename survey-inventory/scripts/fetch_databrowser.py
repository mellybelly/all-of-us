#!/usr/bin/env python3
"""Pull OMOP concept IDs and participant counts for AoU survey questions.

Uses the public All of Us Data Browser API (https://databrowser.researchallofus.org,
backed by https://public.api.researchallofus.org). For every survey module it walks
the question tree (including branching sub-questions) and records:

  - survey_concept_id    e.g. 1586134 = The Basics (OMOP PPI vocabulary)
  - question_concept_id  = observation_source_concept_id in the CDR
  - concept_code         = observation_source_value (PPI code, or LOINC for some items)
  - answers              answer_concept_id (= value_source_concept_id), label, count
  - n_participants       participants with a response in the current public CDR

Counts are the Data Browser's public aggregates (rounded to the nearest 20, which
reflects the CDR the Data Browser is built on; see `cdr` in the output).

Output: raw/databrowser_questions.json
Usage:  python3 survey-inventory/scripts/fetch_databrowser.py
"""
import concurrent.futures
import json
import pathlib
import time
import urllib.parse
import urllib.request

API = "https://public.api.researchallofus.org/v1/databrowser"
OUT = pathlib.Path(__file__).resolve().parent.parent / "raw" / "databrowser_questions.json"


def get(endpoint, **params):
    url = f"{API}/{endpoint}?{urllib.parse.urlencode(params)}"
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


def items(payload):
    q = payload.get("questions", payload)
    return q.get("items", []) if isinstance(q, dict) else q


def question_detail(survey_id, q, level):
    """Answers + respondent count for one question; returns (record, child stubs)."""
    path = q["path"]
    results = get("survey-question-results", survey_concept_id=survey_id,
                  question_concept_id=q["conceptId"], questionPath=path)
    answers, branching = [], []
    for analysis in results.get("items", []):
        if analysis["analysisId"] == 3110:  # response distribution
            for r in analysis["results"]:
                answers.append({"answer_concept_id": r["stratum3"],
                                "answer": r["stratum4"].strip(),
                                "count": r["countValue"]})
                if r["stratum7"] == "1":
                    branching.append(r["stratum3"])
    counts = get("survey-question-counts", questionConceptId=q["conceptId"],
                 questionPath=path)
    n = None
    for analysis in counts.get("items", []):
        if analysis["analysisName"] == "Sex Assigned at Birth":
            n = sum(r["countValue"] for r in analysis["results"])
    children, errors = [], []
    for answer_id in branching:
        try:
            sub = get("sub-questions", survey_concept_id=survey_id,
                      question_concept_id=q["conceptId"], answer_concept_id=answer_id,
                      level=level + 1, path=path)
        except Exception as exc:  # API 500s on some deep PFHH branches
            errors.append(f"sub-questions answer {answer_id}: {exc}")
            continue
        children.extend(items(sub))
    record = {"question_concept_id": q["conceptId"], "concept_code": q["conceptCode"],
              "question": q["conceptName"], "path": path, "level": level,
              "n_participants": n, "answers": answers}
    if errors:
        record["errors"] = errors
    return record, children


def main():
    cdr = get("cdrversion-used")
    modules = get("domain-totals", searchWord="", testFilter=1, orderFilter=1)["surveyModules"]
    out = {"cdr": cdr, "retrieved": time.strftime("%Y-%m-%d"), "surveys": []}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for m in modules:
            sid = m["conceptId"]
            frontier = [(q, 0) for q in items(get("survey-questions",
                                                  survey_concept_id=sid, search_word=""))]
            seen, questions = set(), []
            while frontier:
                frontier = [(q, lvl) for q, lvl in frontier if q["path"] not in seen]
                seen.update(q["path"] for q, _ in frontier)
                futures = [pool.submit(question_detail, sid, q, lvl) for q, lvl in frontier]
                next_frontier = []
                for fut in futures:
                    record, children = fut.result()
                    questions.append(record)
                    next_frontier.extend((c, record["level"] + 1) for c in children)
                frontier = next_frontier
            questions.sort(key=lambda r: r["path"])
            out["surveys"].append({"survey_concept_id": sid, "name": m["name"],
                                   "participant_count": m["participantCount"],
                                   "questions": questions})
            print(f"{m['name']}: {len(questions)} questions/sub-questions")
    OUT.write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()

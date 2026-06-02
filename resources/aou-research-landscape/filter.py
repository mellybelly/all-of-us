#!/usr/bin/env python3
"""
Phase 2 filter for AoU project workspaces.

Applies the filter rule from README.md to projects.jsonl, producing
projects_filtered.jsonl + projects_filtered.csv.

Filter rule (apply in order; report counts at each step):
  1. Drop workspaces tagged 'Educational' (purposes contains 'Educational').
  2. Drop workspaces whose owner role indicates training (Graduate Trainee,
     Undergraduate Student, Research Fellow, Project Personnel, Student),
     UNLESS the workspace also has substantive descriptions
     (sum of question + approach + findings >= 300 chars).
  3. Drop stub records (all three of question / approach / findings under 30 chars).
  4. Drop case-folded duplicate titles after the first occurrence (keep one).

Usage:
    python3 filter.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

TRAINING_ROLES = {
    "Graduate Trainee",
    "Undergraduate Student",
    "Research Fellow",
    "Project Personnel",
    "Student",
}

SUBSTANTIVE_MIN_CHARS = 300  # combined Q+A+F length to override the trainee-role drop
STUB_MAX_CHARS = 30          # per-field cap below which a record is a stub if ALL three apply


def _txt(rec: dict, field: str) -> str:
    v = rec.get(field)
    return v.strip() if isinstance(v, str) else ""


def is_educational(rec: dict) -> bool:
    purposes = rec.get("purposes") or []
    return any(p == "Educational" for p in purposes)


def owner_role(rec: dict) -> str:
    team = rec.get("team") or {}
    owners = team.get("owner") or []
    if owners:
        return (owners[0].get("role") or "").strip()
    return ""


def is_stub(rec: dict) -> bool:
    q = _txt(rec, "questions")
    a = _txt(rec, "approaches")
    f = _txt(rec, "findings")
    return len(q) < STUB_MAX_CHARS and len(a) < STUB_MAX_CHARS and len(f) < STUB_MAX_CHARS


def substantive_chars(rec: dict) -> int:
    return len(_txt(rec, "questions")) + len(_txt(rec, "approaches")) + len(_txt(rec, "findings"))


def main() -> None:
    src = HERE / "projects.jsonl"
    if not src.exists():
        sys.exit(f"Missing {src}")

    records = []
    with open(src) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    total = len(records)
    print(f"Total input projects: {total}")

    # Step 1: drop Educational
    after_edu = [r for r in records if not is_educational(r)]
    print(f"After dropping Educational-tagged: {len(after_edu)}  (-{total - len(after_edu)})")

    # Step 2: drop trainee-role records unless substantive
    after_trainee = []
    trainee_kept = 0
    trainee_dropped = 0
    for r in after_edu:
        role = owner_role(r)
        if role in TRAINING_ROLES:
            if substantive_chars(r) >= SUBSTANTIVE_MIN_CHARS:
                after_trainee.append(r)
                trainee_kept += 1
            else:
                trainee_dropped += 1
        else:
            after_trainee.append(r)
    print(
        f"After dropping trainee-role (kept {trainee_kept} substantive trainee-led; "
        f"dropped {trainee_dropped}): {len(after_trainee)}"
    )

    # Step 3: drop stubs (all three fields < 30 chars)
    after_stub = [r for r in after_trainee if not is_stub(r)]
    print(f"After dropping stubs (<{STUB_MAX_CHARS} chars in all 3 fields): {len(after_stub)}  (-{len(after_trainee) - len(after_stub)})")

    # Step 4: drop case-folded duplicate titles (keep first occurrence)
    seen_titles = set()
    after_dups = []
    for r in after_stub:
        t = (r.get("title") or "").strip().casefold()
        if t in seen_titles:
            continue
        seen_titles.add(t)
        after_dups.append(r)
    print(f"After dropping duplicate titles: {len(after_dups)}  (-{len(after_stub) - len(after_dups)})")

    # Write outputs
    out_jsonl = HERE / "projects_filtered.jsonl"
    out_csv = HERE / "projects_filtered.csv"

    with open(out_jsonl, "w", encoding="utf-8") as fh:
        for r in after_dups:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {out_jsonl}  ({len(after_dups)} records)")

    # Reuse extract.normalize_project for CSV
    sys.path.insert(0, str(HERE))
    from extract import normalize_project, _clean

    if after_dups:
        rows = [normalize_project(r) for r in after_dups]
        fieldnames = list(rows[0].keys())
        with open(out_csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow({k: _clean(r.get(k)) for k in fieldnames})
        print(f"Wrote {out_csv}  ({len(rows)} rows)")


if __name__ == "__main__":
    main()

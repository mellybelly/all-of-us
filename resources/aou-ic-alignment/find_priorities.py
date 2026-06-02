"""Find pages with priorities/goals/objectives/themes headings.

For each in-scope plan, locate pages that look like the priorities scaffold
and dump a compact text section so we can curate ic_priorities.csv from a
short summary view.
"""
import json
import os
import re
import sys

IN = "/Users/melissahaendel/Documents/GitHub/all-of-us/resources/aou-ic-alignment/plan_pages.json"
OUT = "/Users/melissahaendel/Documents/GitHub/all-of-us/resources/aou-ic-alignment/priorities_text/"
os.makedirs(OUT, exist_ok=True)

# Headings used by various plans
HEADING_PATTERNS = [
    r"(?i)\bstrategic\s+(priorit|goal|objectiv|themes?)\b",
    r"(?i)\bresearch\s+(goal|priorit|objectiv|themes?)\b",
    r"(?i)\bgoal\s*\d+\b",
    r"(?i)\bobjective\s*\d+\b",
    r"(?i)\bpriority\s+area\s*\d*\b",
    r"(?i)\bscientific\s+priorit",
    r"(?i)\bcross[-\s]?cutting\s+(theme|area|priorit)",
    r"(?i)\bstrategic\s+plan\b",
    r"(?i)\bgoals?\s+and\s+objectives?\b",
    r"(?i)\bgoals?,?\s+and\s+strategies\b",
    r"(?i)\bplan\s+overview\b",
    r"(?i)\btable\s+of\s+contents\b",
    r"(?i)\bvision\b",
    r"(?i)\bmission\b",
    r"(?i)\bresearch\s+areas?\b",
    r"(?i)\bareas?\s+of\s+focus\b",
    r"(?i)\bdivision\s+of\s+\b",
    r"(?i)\bcrosscutting\b",
]


def find_priority_pages(pages):
    """Return list of page numbers that match at least one heading pattern."""
    hits = []
    for p in pages:
        text = p["text"]
        if not text:
            continue
        matches = []
        for pat in HEADING_PATTERNS:
            m = re.search(pat, text)
            if m:
                matches.append(m.group(0))
        if matches:
            hits.append((p["page"], matches[:3], text))
    return hits


def main():
    with open(IN) as f:
        blob = json.load(f)
    for fn, info in blob.items():
        ic = info["ic"]
        year = info["year"]
        hits = find_priority_pages(info["pages"])
        # write compact view: pages with hits
        out_path = os.path.join(OUT, f"{ic}__{year}.txt")
        with open(out_path, "w") as fh:
            fh.write(f"# {ic} ({year}) — file: {fn}\n")
            fh.write(f"# {len(hits)} pages matched priority-heading patterns\n\n")
            for page, m, text in hits:
                fh.write(f"\n--- PAGE {page} matched={m} ---\n")
                # truncate long pages — keep first 3500 chars
                fh.write(text[:3500])
                fh.write("\n")
        print(f"{ic:9s} {year:25s} hits={len(hits):3d}  -> {out_path}")


if __name__ == "__main__":
    main()

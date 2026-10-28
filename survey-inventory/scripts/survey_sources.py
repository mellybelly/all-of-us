"""Parse AoU Survey Explorer PDFs for item-level source instruments.

Each English "Src" PDF annotates question text with superscript footnote numbers
(rendered by pdftotext as trailing digits, e.g. "Trouble relaxing1") that point to
a numbered bibliography ("Sources" / "Source Information") at the end, where each
entry has "a. Year of Original Source" and "b. Brief Description of Source".

Requires poppler's `pdftotext`.
"""
import re
import subprocess

TOP_ITEM = re.compile(r"^\s{1,6}(\d{1,2})\.\s+(\S.*)$")
FOOTNOTE = re.compile(r"^(.*?[A-Za-z?.):,'\"”’])(\d{1,2}(?:,\s?\d{1,2})*)\s*$")
PAGE_NOISE = re.compile(r"^\s*(All of Us Research Program|Participant Provided Information \(PPI\)|\d+)\s*$")
BULLET = re.compile(r"^\s*[●•○]")


def pdf_lines(path):
    text = subprocess.run(["pdftotext", "-layout", str(path), "-"], check=True,
                          capture_output=True, text=True).stdout
    return [l for l in text.splitlines() if not PAGE_NOISE.match(l)]


def parse_bibliography(lines):
    """Return {block: {number: {citation, year, description}}}.

    A block starts at a top-level "1." entry that is followed by a
    "Year of Original Source" line; The Basics PDF has two blocks (Basics and
    the Life Functioning companion survey).
    """
    starts = [i for i, l in enumerate(lines) if "Year of Original Source" in l]
    if not starts:
        # PFHH: a bare "Sources" heading with unindented one-line entries.
        heading = [i for i, l in enumerate(lines) if l.strip() in ("Sources", "Sources:")]
        entries = {}
        for line in lines[heading[-1] + 1:] if heading else []:
            m = re.match(r"^\s*(\d{1,2})\.\s+(\S.*)$", line)
            if m:
                entries[int(m.group(1))] = {"citation": m.group(2).strip(),
                                            "year": "", "description": ""}
        return {0: entries} if entries else {}
    # Walk back from the first "Year" line to its numbered entry.
    first = starts[0]
    while first > 0 and not TOP_ITEM.match(lines[first]):
        first -= 1
    blocks, block, current, field = {}, -1, None, None
    for line in lines[first:]:
        m = TOP_ITEM.match(line)
        if m and len(line) - len(line.lstrip()) <= 6:
            num = int(m.group(1))
            if num == 1:
                block += 1
            current = {"citation": m.group(2).strip(), "year": "", "description": ""}
            blocks.setdefault(block, {})[num] = current
            field = "citation"
            continue
        if current is None:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        year = re.search(r"Year of Original Source:\s*(.*)", stripped)
        desc = re.search(r"Brief Description of Source:\s*(.*)", stripped)
        if year:
            current["year"], field = year.group(1).strip(), "year"
        elif desc:
            current["description"], field = desc.group(1).strip(), "description"
        elif field in ("citation", "description"):
            current[field] += " " + stripped
    return blocks


def parse_items(lines):
    """Yield (question_text, [source numbers]) for footnoted question lines."""
    end = next((i for i, l in enumerate(lines) if "Year of Original Source" in l), len(lines))
    for i, line in enumerate(lines[:end]):
        m = FOOTNOTE.match(line.rstrip())
        if not m or BULLET.match(line) or line.strip().startswith("["):
            continue
        parts = [m.group(1).strip()]
        j = i - 1
        while j >= 0 and lines[j].strip() and not BULLET.match(lines[j]) \
                and not lines[j].strip().startswith(("[", "(")) and not lines[j].rstrip().endswith("]"):
            parts.insert(0, lines[j].strip())
            j -= 1
        refs = [int(n) for n in re.split(r",\s?", m.group(2))]
        yield " ".join(parts), refs


def parse_pdf(path):
    lines = pdf_lines(path)
    blocks = parse_bibliography(lines)
    bib = blocks.get(0, {})
    items = [(q, refs, [bib.get(r, {}).get("citation", "") for r in refs])
             for q, refs in parse_items(lines)]
    return blocks, items

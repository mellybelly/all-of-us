#!/usr/bin/env python3
"""
Fetch PMC full text (and backfill missing abstracts) for the AoU publication
corpus, for use as richer tagging input.

What it does
------------
For every record in ``publications.jsonl``:

1. If the record has a valid PMC id, fetch the Europe PMC JATS full text
   (``.../{PMCID}/fullTextXML``) and extract **body text only** — section
   titles, paragraphs, and figure/table *captions*. Reference lists,
   acknowledgments, author notes, competing-interest statements, tables, and
   formulae are stripped, because they name-drop unrelated diseases/methods
   and would pollute keyword tagging. The article abstract is also pulled out
   of the XML (used for gap-filling, below).

2. If the record is missing an abstract (no ``*_abstract`` field) we try, in
   order: (a) the abstract parsed from the full-text XML; (b) an Europe PMC
   ``core`` search by PMID (``abstractText``). This is the "fill any abstract
   gaps" step.

Everything is cached on disk under ``raw/fulltext/`` so re-runs are free.

Output
------
``fulltext_augmented.jsonl`` — one object per publication record:

    {record_id, pubmed_id, pmc_id,
     has_fulltext, fulltext_chars, fulltext_body,
     abstract_source, abstract_filled}

``abstract_source`` is one of: ``orig`` (already had one), ``epmc_fulltext``,
``epmc_search``, or ``none``.

Usage
-----
    python3 fetch_fulltext.py            # fetch (cached) + build augmentation
    python3 fetch_fulltext.py --no-net   # build only from existing cache
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
FT_DIR = RAW / "fulltext"          # cached JATS XML, one file per PMCID
ABS_DIR = RAW / "abstracts"        # cached Europe PMC search JSON, one per PMID
PUBS_IN = HERE / "publications.jsonl"
OUT = HERE / "fulltext_augmented.jsonl"

UA = {"User-Agent": "Mozilla/5.0 (AoU-research-landscape; melissa@tislab.org)"}
EPMC_FT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/fullTextXML"
EPMC_SEARCH = (
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
    "query=EXT_ID:{pmid}%20AND%20SRC:MED&resultType=core&format=json"
)

# JATS elements whose content we drop entirely before extracting body text.
DROP_TAGS = {
    "ref-list", "ref", "back", "ack", "fn-group", "fn", "author-notes",
    "table-wrap", "table", "fig", "disp-formula", "inline-formula",
    "tex-math", "mml:math", "xref", "label", "graphic", "media",
    "supplementary-material", "funding-group", "funding-source",
    "conflict", "coi-statement",
}


def _val(d: dict, *keys: str) -> str:
    for k in keys:
        v = (d.get(k) or "").strip()
        if v and v.lower() != "none":
            return v
    return ""


def norm_pmc(v: str) -> str:
    v = v.strip().upper()
    if not v:
        return ""
    if not v.startswith("PMC"):
        v = "PMC" + v
    return v


def _fetch(url: str, dest: Path, sleep: float = 0.15) -> bool:
    """Fetch url -> dest (bytes). Returns True on success. Cached: skip if exists."""
    if dest.exists():
        return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = resp.read()
        dest.write_bytes(data)
        time.sleep(sleep)
        return True
    except Exception as e:
        # Record the miss so we don't re-hit a known-404 every run.
        code = getattr(e, "code", "ERR")
        dest.with_suffix(dest.suffix + f".miss-{code}").write_text(str(e))
        time.sleep(sleep)
        return False


def _missed(dest: Path) -> bool:
    return any(dest.parent.glob(dest.name + ".miss-*"))


def _localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _strip(elem: ET.Element) -> None:
    """Recursively remove DROP_TAGS children in place."""
    for child in list(elem):
        if _localname(child.tag) in DROP_TAGS:
            elem.remove(child)
        else:
            _strip(child)


def _text_of(elem: ET.Element) -> str:
    return re.sub(r"\s+", " ", "".join(elem.itertext())).strip()


def parse_jats(xml_bytes: bytes) -> tuple[str, str]:
    """Return (abstract_text, body_text) from JATS full-text XML."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return "", ""

    # Abstract: collect all <abstract> blocks (skip the structured 'graphical'
    # ones if labelled, but keeping them is harmless).
    abs_parts = []
    for ab in root.iter():
        if _localname(ab.tag) == "abstract":
            a = ET.fromstring(ET.tostring(ab))
            _strip(a)
            t = _text_of(a)
            if t:
                abs_parts.append(t)
    abstract = " ".join(dict.fromkeys(abs_parts))  # dedupe, keep order

    # Body: first <body> element, back-matter stripped.
    body_text = ""
    for b in root.iter():
        if _localname(b.tag) == "body":
            bb = ET.fromstring(ET.tostring(b))
            _strip(bb)
            body_text = _text_of(bb)
            break
    return abstract, body_text


def epmc_search_abstract(pmid: str) -> str:
    dest = ABS_DIR / f"{pmid}.json"
    url = EPMC_SEARCH.format(pmid=pmid)
    if not _fetch(url, dest):
        return ""
    try:
        data = json.loads(dest.read_text())
        results = data.get("resultList", {}).get("result", [])
        if results:
            return (results[0].get("abstractText") or "").strip()
    except Exception:
        pass
    return ""


def clean_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)             # strip any HTML/JATS inline tags
    s = s.replace("%28", "(").replace("%29", ")").replace("%2C", ",")
    return re.sub(r"\s+", " ", s).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-net", action="store_true",
                    help="build only from cache, do not hit the network")
    args = ap.parse_args()

    FT_DIR.mkdir(parents=True, exist_ok=True)
    ABS_DIR.mkdir(parents=True, exist_ok=True)

    pubs = [json.loads(l) for l in PUBS_IN.open()]
    print(f"Records: {len(pubs)}")

    n_ft = n_ft_ok = n_fill_ft = n_fill_search = 0
    rows = []
    for i, d in enumerate(pubs, 1):
        rid = d.get("record_id")
        pmid = _val(d, "pubmed_id")
        pmc = norm_pmc(_val(d, "pmc_id"))
        orig_abs = clean_html(_val(d, "pdr_abstract", "manual_abstract", "calc_abstract"))

        has_fulltext = False
        fulltext_body = ""
        xml_abstract = ""

        if pmc:
            n_ft += 1
            dest = FT_DIR / f"{pmc}.xml"
            got = dest.exists()
            if not got and not args.no_net and not _missed(dest):
                got = _fetch(EPMC_FT.format(pmc=pmc), dest)
            if got and dest.exists():
                xml_abstract, fulltext_body = parse_jats(dest.read_bytes())
                if len(fulltext_body) > 400:   # guard against stub/empty bodies
                    has_fulltext = True
                    n_ft_ok += 1
                else:
                    fulltext_body = ""

        # Abstract gap-fill
        abstract_filled = orig_abs
        abstract_source = "orig" if orig_abs else "none"
        if not orig_abs:
            if xml_abstract:
                abstract_filled = clean_html(xml_abstract)
                abstract_source = "epmc_fulltext"
                n_fill_ft += 1
            elif pmid and not args.no_net:
                got = epmc_search_abstract(pmid)
                if got:
                    abstract_filled = clean_html(got)
                    abstract_source = "epmc_search"
                    n_fill_search += 1
            elif pmid and args.no_net:
                # try cache only
                cached = ABS_DIR / f"{pmid}.json"
                if cached.exists():
                    try:
                        r = json.loads(cached.read_text()).get(
                            "resultList", {}).get("result", [])
                        if r and r[0].get("abstractText"):
                            abstract_filled = clean_html(r[0]["abstractText"])
                            abstract_source = "epmc_search"
                            n_fill_search += 1
                    except Exception:
                        pass

        rows.append({
            "record_id": rid,
            "pubmed_id": pmid,
            "pmc_id": pmc,
            "has_fulltext": has_fulltext,
            "fulltext_chars": len(fulltext_body),
            "fulltext_body": fulltext_body,
            "abstract_source": abstract_source,
            "abstract_filled": abstract_filled,
        })

        if i % 200 == 0:
            print(f"  {i}/{len(pubs)} processed "
                  f"(full text ok: {n_ft_ok}, abstracts filled: "
                  f"{n_fill_ft + n_fill_search})")

    with OUT.open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    filled = n_fill_ft + n_fill_search
    print("\n=== Summary ===")
    print(f"PMC ids attempted:        {n_ft}")
    print(f"Full text extracted:      {n_ft_ok}")
    print(f"Abstracts gap-filled:     {filled} "
          f"(from full text: {n_fill_ft}, from EPMC search: {n_fill_search})")
    still_missing = sum(1 for r in rows if r["abstract_source"] == "none")
    print(f"Still missing abstract:   {still_missing}")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

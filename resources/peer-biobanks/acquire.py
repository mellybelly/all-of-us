#!/usr/bin/env python3
"""Acquire peer-biobank publication corpora via PubMed E-utilities.

For each of UK Biobank, FinnGen, Million Veterans Program, China Kadoorie
Biobank we run a PubMed-search-by-name (esearch) to collect PMIDs, then
batch-fetch records (efetch) to extract title/abstract/year/journal.

Data-source caveat: this is a PubMed-name-search fallback, not the
biobank's official curated list. The official lists were not pulled because
of the per-task 10-min-per-biobank fallback rule. PubMed name-search is
known to over- and under-include: any pub that mentions the biobank name
in title/abstract gets included even if the biobank wasn't the primary
data source, and pubs that use the data but don't name-mention will miss.
This is acceptable for cross-cohort theme-share comparison because the
same heuristic is applied uniformly.

Output:
  raw/<biobank>_pmids.txt
  raw/<biobank>_pubmed.xml     (raw efetch XML, cached)
  <biobank>_pubs.jsonl         (cleaned, one pub per line)
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
RAW.mkdir(parents=True, exist_ok=True)

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
USER_AGENT = "AoU-roadmap-refresh/1.0 (melissa@tislab.org)"

# Full census: no effective cap. Every PubMed name-search return is pulled
# for all biobanks (UKB ~11.9k, FinnGen ~3.2k, MVP ~440, CKB ~560). The
# 20000 ceiling is just a pagination safety bound, well above any biobank's
# current total. (Previously capped at 4000 with a year-stratified UKB
# sub-sample; we now pull the complete corpus per user request.)
CAP_PMIDS = 20000

BIOBANKS = [
    {
        "code": "ukb",
        "name": "UK Biobank",
        "query": '"UK Biobank"[Title/Abstract] AND humans[MeSH Terms] AND Journal Article[Publication Type]',
    },
    {
        "code": "finngen",
        "name": "FinnGen",
        "query": '"FinnGen"[Title/Abstract] AND Journal Article[Publication Type]',
    },
    {
        "code": "mvp",
        "name": "Million Veteran Program",
        "query": '("Million Veteran Program"[Title/Abstract] OR "Million Veterans Program"[Title/Abstract]) AND Journal Article[Publication Type]',
    },
    {
        "code": "ckb",
        "name": "China Kadoorie Biobank",
        "query": '"China Kadoorie Biobank"[Title/Abstract] AND Journal Article[Publication Type]',
    },
]


def http_get(url: str, retries: int = 3) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.read()
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"GET failed after {retries} retries: {url}\n{last_err}")


def _loads_esearch(url: str, attempts: int = 4) -> dict:
    """Fetch + JSON-parse an esearch URL. NCBI occasionally returns a response
    with raw control characters (or a transient error page); tolerate control
    chars and retry on parse failure."""
    last = None
    for i in range(attempts):
        raw = http_get(url)
        try:
            return json.loads(raw, strict=False)
        except json.JSONDecodeError as e:
            last = e
            time.sleep(1.0 + i)  # back off, then retry
    raise last


def esearch_pmids(query: str, retmax: int = 4000):
    pmids: list[str] = []
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": str(min(retmax, 10000)),
        "usehistory": "y",
    }
    url = f"{EUTILS}/esearch.fcgi?{urllib.parse.urlencode(params)}"
    data = _loads_esearch(url)
    res = data.get("esearchresult", {})
    pmids.extend(res.get("idlist", []))
    count = int(res.get("count", 0))
    web_env = res.get("webenv")
    query_key = res.get("querykey")
    while len(pmids) < min(count, retmax) and web_env:
        params = {
            "db": "pubmed",
            "WebEnv": web_env,
            "query_key": query_key,
            "retmode": "json",
            "retmax": "10000",
            "retstart": str(len(pmids)),
            "usehistory": "y",
        }
        url = f"{EUTILS}/esearch.fcgi?{urllib.parse.urlencode(params)}"
        data = _loads_esearch(url)
        new_ids = data.get("esearchresult", {}).get("idlist", [])
        if not new_ids:
            break
        pmids.extend(new_ids)
        time.sleep(0.4)
    return pmids[:retmax], count


def efetch_batch(pmids):
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "rettype": "xml",
        "retmode": "xml",
    }
    url = f"{EUTILS}/efetch.fcgi?{urllib.parse.urlencode(params)}"
    return http_get(url)


def parse_pubmed_xml(xml_bytes):
    out = []
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        print(f"  XML parse error: {e}", file=sys.stderr)
        return out
    for article in root.iter("PubmedArticle"):
        pmid_el = article.find(".//PMID")
        pmid = pmid_el.text if pmid_el is not None else ""
        title_el = article.find(".//ArticleTitle")
        title = "".join(title_el.itertext()) if title_el is not None else ""
        abstract_parts = []
        for ab in article.findall(".//Abstract/AbstractText"):
            abstract_parts.append("".join(ab.itertext()))
        abstract = " ".join(p.strip() for p in abstract_parts if p)
        year = ""
        pubdate = article.find(".//Article//Journal//JournalIssue/PubDate")
        if pubdate is not None:
            y_el = pubdate.find("Year")
            if y_el is not None and y_el.text:
                year = y_el.text
            else:
                md = pubdate.find("MedlineDate")
                if md is not None and md.text:
                    m = re.search(r"(19|20)\d{2}", md.text)
                    if m:
                        year = m.group(0)
        if not year:
            ad = article.find(".//ArticleDate/Year")
            if ad is not None and ad.text:
                year = ad.text
        journal_el = article.find(".//Article/Journal/Title")
        if journal_el is None:
            journal_el = article.find(".//Article/Journal/ISOAbbreviation")
        journal = journal_el.text if journal_el is not None else ""
        pub_types = [pt.text for pt in article.findall(".//PublicationType") if pt.text]
        out.append({
            "pubmed_id": pmid,
            "year": year,
            "title": title.strip(),
            "abstract": abstract.strip(),
            "journal": journal or "",
            "publication_types": pub_types,
        })
    return out


def fetch_biobank(spec):
    code = spec["code"]
    name = spec["name"]
    print(f"\n=== {name} ({code}) ===", flush=True)
    pmids_file = RAW / f"{code}_pmids.txt"
    pubs_jsonl = ROOT / f"{code}_pubs.jsonl"

    if pmids_file.exists():
        pmids = [ln.strip() for ln in pmids_file.read_text().splitlines() if ln.strip()]
        print(f"  cached PMIDs: {len(pmids)}", flush=True)
        total = len(pmids)
    else:
        print(f"  esearch query: {spec['query']}", flush=True)
        pmids, total = esearch_pmids(spec["query"], retmax=CAP_PMIDS)
        pmids_file.write_text("\n".join(pmids) + "\n")
        print(f"  PMIDs returned: {len(pmids)} / esearch total={total}", flush=True)

    if pubs_jsonl.exists():
        print(f"  pubs jsonl cached at {pubs_jsonl}; skipping efetch", flush=True)
        return

    batch = 200
    all_pubs = []
    for i in range(0, len(pmids), batch):
        chunk = pmids[i : i + batch]
        cache_path = RAW / f"{code}_efetch_{i:06d}.xml"
        if cache_path.exists():
            xml_bytes = cache_path.read_bytes()
        else:
            xml_bytes = efetch_batch(chunk)
            cache_path.write_bytes(xml_bytes)
            time.sleep(0.4)
        recs = parse_pubmed_xml(xml_bytes)
        all_pubs.extend(recs)
        if i % 1000 == 0:
            print(f"  batch {i}-{i+len(chunk)-1}: parsed {len(recs)} (total: {len(all_pubs)})", flush=True)

    with pubs_jsonl.open("w") as f:
        for r in all_pubs:
            f.write(json.dumps(r) + "\n")
    print(f"  wrote {pubs_jsonl}: {len(all_pubs)} pubs", flush=True)


def main():
    only = set(sys.argv[1:])
    for spec in BIOBANKS:
        if only and spec["code"] not in only:
            continue
        try:
            fetch_biobank(spec)
        except Exception as e:  # noqa: BLE001
            print(f"  ERROR fetching {spec['code']}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()

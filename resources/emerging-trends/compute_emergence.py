#!/usr/bin/env python3
"""Compute term-emergence (acceleration) on the preprint and grant corpora.

For each corpus, builds a year x term document-frequency table over uni/bi/tri-grams
(stopword- and boilerplate-filtered), then scores each term's acceleration:
recent (2024-2026) doc-share vs prior (2021-2023) doc-share.

Outputs:
  emerging_preprints.csv, emerging_grants.csv  (ranked terms + yearly shares)
  emerging_candidates.json  (top terms from both, with exemplar recent titles,
                             for the LLM topic-induction step)
"""
from __future__ import annotations
import json, re, csv, glob, math
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
PRIOR = {2021, 2022, 2023}
RECENT = {2024, 2025, 2026}

# Generic stopwords + academic filler. The filler set is the key defense against
# the LLM-writing-boilerplate noise mode (e.g. "underscores potential").
STOP = set("""the a an and or of to in for with on by from as at is are be was were been being
this that these those we our us it its their they them he she his her you your i
study studies data analysis analyses result results method methods using used use uses
based associated association associations risk patient patients health among between within
not no can may also more most than then thus therefore however which while whether due per
via did does do done has have had having such both each into out over under after before during
high higher low lower large small new novel using used significant significantly increased decreased
increase decrease compared comparison cohort participant participants individual individuals
total mean median age year years group groups outcome outcomes effect effects model models
background methods conclusion conclusions objective objectives introduction findings finding
preprint preprints medrxiv biorxiv abstract paper papers article articles research
present presents presented presenting show shows showed showing demonstrate demonstrates
suggest suggests suggesting reveal reveals revealed indicate indicates report reports reported
provide provides provided offering offers offer underscore underscores underscoring
highlight highlights highlighting improve improves improved improving improvement
potential insights insight scalable promising critical important emerging emergent
remains remain underexplored understudied poorly understood comprehensive robust
framework frameworks approach approaches strategy strategies tool tools pipeline pipelines
performance accuracy benchmark benchmarked benchmarks evaluate evaluated evaluation
enhance enhances enhanced enhancing enabling enables enabled enable leverage leverages
leveraging utilize utilizes utilizing develop developed developing development
ultimately consistent strong unique need needs needed achieving achieve achieved
across toward towards within without including included include includes well also
findings suggest may provide could would should within across global key main major
furthermore moreover additionally respectively particularly especially notably
purpose summary narrative aim aims goal goals
integrating integrates integrate integrated establish establishes established establishing
exhibited exhibit exhibits advancing advance advances advanced revealing reveal reveals
broader linking link links alongside distinct distinctly supporting support supports
introduce introduces introduced investigates investigate investigated investigating
challenges challenge challenging diverse beyond together previously unrecognized
indicate indicating indicated providing provides consistently characterize characterized
characterizing examine examined examining elucidate elucidating determine determined
identifying identified identify investigation investigations understanding understand
addressing address addresses examining underlying related changes change versus""".split())

# Filler-ish tokens that, if present anywhere in an n-gram, mark it as boilerplate.
FILLER = set("""offering offers offer underscores underscoring highlighting improving enabling
leveraging utilizing achieving ultimately scalable promising insights potential
remains underexplored comprehensive robust enhance enhancing consistent strong
preserving promising suggesting indicating revealing demonstrating showing providing
crucial critical important significant novel emerging valuable effective efficient
performance accuracy benchmarked benchmark generalizable interpretable""".split())

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9\-]+")


SEG_RE = re.compile(r"[.;:!?]|<[^>]*>|\n")  # sentence / pref_term / terms delimiters


def tokens(text: str):
    return [w for w in TOKEN_RE.findall(text.lower())
            if len(w) > 3 and not w.isdigit() and w not in STOP]


def doc_terms(fields: dict, text_fields) -> set:
    """Build the n-gram set for a doc, forming n-grams only *within* a segment
    (sentence / semicolon-delimited pref_term) so we don't create spurious
    cross-boundary bigrams."""
    out = set()
    for fld in text_fields:
        raw = str(fields.get(fld) or "")
        for seg in SEG_RE.split(raw):
            out |= ngrams(tokens(seg))
    return out


def ngrams(words):
    out = set()
    for w in words:
        out.add(w)
    for a, b in zip(words, words[1:]):
        if a in FILLER or b in FILLER:
            continue
        out.add(f"{a} {b}")
    for a, b, c in zip(words, words[1:], words[2:]):
        if a in FILLER or b in FILLER or c in FILLER:
            continue
        out.add(f"{a} {b} {c}")
    return out


def load(patterns):
    for pat in patterns:
        for fp in sorted(glob.glob(str(RAW / pat))):
            for line in open(fp):
                yield json.loads(line)


def analyze(patterns, text_fields, label, min_recent=40, prune_every=50000):
    year_n = Counter()
    term_year = defaultdict(Counter)   # term -> Counter(year -> docfreq)
    seen = 0
    for d in load(patterns):
        y = int(d.get("year"))
        year_n[y] += 1
        seen += 1
        for t in doc_terms(d, text_fields):
            term_year[t][y] += 1
        # Memory bound: periodically drop hapax terms (most of the vocab). High-
        # frequency terms that matter survive; borderline terms may be slightly
        # undercounted, which is acceptable for ranking.
        if seen % prune_every == 0:
            for t in [t for t, yc in term_year.items() if sum(yc.values()) <= 1]:
                del term_year[t]
            print(f"  [{label}] {seen} docs, vocab={len(term_year)}", flush=True)

    n_prior = sum(year_n[y] for y in PRIOR) or 1
    n_recent = sum(year_n[y] for y in RECENT) or 1
    rows = []
    for term, yc in term_year.items():
        rec = sum(yc[y] for y in RECENT)
        if rec < min_recent:
            continue
        pri = sum(yc[y] for y in PRIOR)
        s_rec = rec / n_recent
        s_pri = pri / n_prior
        ratio = (s_rec + 1e-6) / (s_pri + 1e-6)
        delta = s_rec - s_pri
        # Emergence score: reward both growth (log ratio) and absolute recent
        # footprint (sqrt of recent count), so we don't over-rank tiny spikes.
        score = math.log(ratio) * math.sqrt(rec) * (1 if delta > 0 else 0.1)
        rows.append({"term": term, "recent_n": rec, "prior_n": pri,
                     "share_prior_pct": round(s_pri * 100, 3),
                     "share_recent_pct": round(s_rec * 100, 3),
                     "growth_x": round(ratio, 1), "score": round(score, 2),
                     "by_year": {str(y): yc.get(y, 0) for y in sorted(year_n)}})
    rows.sort(key=lambda r: -r["score"])
    out = HERE / f"emerging_{label}.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["term", "recent_n", "prior_n", "share_prior_pct",
                    "share_recent_pct", "growth_x", "score"])
        for r in rows:
            w.writerow([r["term"], r["recent_n"], r["prior_n"],
                        r["share_prior_pct"], r["share_recent_pct"],
                        r["growth_x"], r["score"]])
    print(f"{label}: {sum(year_n.values())} docs, years={dict(sorted(year_n.items()))}, "
          f"{len(rows)} emerging terms -> {out.name}", flush=True)
    return rows


def exemplars(patterns, text_fields, terms, k=3):
    """Grab up to k recent (2025/2026) titles per term."""
    want = {t: [] for t in terms}
    termset = set(terms)
    for d in load(patterns):
        if int(d.get("year")) < 2025:
            continue
        title = (d.get("title") or "").strip()
        if not title:
            continue
        toks = doc_terms({"title": title}, ["title"])
        for t in termset & toks:
            if len(want[t]) < k:
                want[t].append(title[:160])
    return want


def main():
    pp = analyze(["preprints_*.jsonl"], ["title", "abstract"], "preprints")
    # Grants: use curated pref_terms + title (cleaner concept signal, far smaller
    # vocab than the verbose abstract text).
    gr = analyze(["grants_*.jsonl"], ["title", "pref_terms"], "grants")

    top_pp = [r["term"] for r in pp[:300]]
    top_gr = [r["term"] for r in gr[:300]]
    ex_pp = exemplars(["preprints_*.jsonl"], ["title", "abstract"], top_pp)

    cand = {
        "preprints_top": [{**r, "exemplars": ex_pp.get(r["term"], [])} for r in pp[:300]],
        "grants_top": gr[:300],
    }
    (HERE / "emerging_candidates.json").write_text(json.dumps(cand, indent=1))
    print(f"\nWrote emerging_candidates.json "
          f"({len(cand['preprints_top'])} preprint + {len(cand['grants_top'])} grant terms)")


if __name__ == "__main__":
    main()

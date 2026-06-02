#!/usr/bin/env python3
"""
Phase 3b — Temporal trends (publications only — projects lack reliable dates).

For each theme and focus area:
  - Pub count by year (2015-2027)
  - Pre-2023 vs 2023+ split
  - Trend score: share(2023+) - share(pre-2023). Positive => growing.

Independent 8-hot-area detection (slide 7 of 2026 Sci Com WG deck), keyword-
based on title+abstract from publications_with_ic.jsonl (since
publications_tagged.jsonl only carries themes, not abstracts).

Outputs:
  pub_year_by_theme.csv         (theme_code x year -> count)
  pub_year_by_focus_area.csv    (focus_area_code x year -> count)
  theme_trend_scores.csv        (per-theme pre/post-2023 and trend)
  focus_area_trend_scores.csv   (per-FA pre/post-2023 and trend)
  hot_areas_detection.csv       (one row per pub, bool columns per hot area)
  hot_areas_summary.csv         (per-hot-area: counts, splits, trend, examples)
"""
from __future__ import annotations
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANDSCAPE = HERE.parent / "aou-research-landscape"

# import the theme->focus-area map from the crosswalk module
import sys
sys.path.insert(0, str(HERE))
from crosswalk import THEME_MAP, FOCUS_AREAS, theme_focus_areas  # type: ignore  # noqa: E402

CUTOFF_YEAR = 2023  # 2023+ is "post-Refresh-inflection"
YEARS = list(range(2015, 2028))  # 2015..2027 inclusive


# ---------------------------------------------------------------------------
# Load publication corpus with usable text for keyword detection.
# publications_tagged.jsonl is the tagged universe; publications_with_ic.jsonl
# has the title/abstract fields. Join on record_id.
# ---------------------------------------------------------------------------
def load_tagged_pubs() -> dict[str, dict]:
    src = LANDSCAPE / "publications_tagged.jsonl"
    out: dict[str, dict] = {}
    with src.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if not rec.get("in_substantive_corpus", True):
                continue
            out[str(rec["record_id"])] = rec
    return out


def load_text_for_pubs(record_ids: set[str]) -> dict[str, dict]:
    """Return {record_id: {title, abstract, year}} for the requested set."""
    src = LANDSCAPE / "publications_with_ic.jsonl"
    out: dict[str, dict] = {}
    with src.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            rid = str(rec.get("record_id"))
            if rid not in record_ids:
                continue
            title = (
                rec.get("calc_title")
                or rec.get("manual_title")
                or rec.get("pdr_title")
                or ""
            )
            abstract = (
                rec.get("calc_abstract")
                or rec.get("manual_abstract")
                or rec.get("pdr_abstract")
                or ""
            )
            year = (
                rec.get("calc_date_year")
                or rec.get("manual_date_year")
                or rec.get("pdr_date_year")
            )
            out[rid] = {
                "title": title or "",
                "abstract": abstract or "",
                "year": str(year) if year else None,
            }
    return out


# ---------------------------------------------------------------------------
# Hot-area detectors (keyword/regex on lowercased title+abstract).
# The names HA1..HA8 align with slide 7 reflections-since-2023.
# Each detector returns True/False given a lowercased text blob.
# Genomics terms are explicitly EXCLUDED from the multi-omics detector so the
# slide-7 "beyond genomics" question is answered honestly.
# ---------------------------------------------------------------------------

# Compile regexes once
def _re(*patterns: str) -> re.Pattern:
    return re.compile("|".join(patterns), re.IGNORECASE)


# Multi-omics (beyond genomics)
MULTIOMICS_POS = _re(
    r"\bproteomics?\b",
    r"\bmetabolomics?\b",
    r"\btranscriptomics?\b",
    r"\blipidomics?\b",
    r"\bepigenomics?\b",
    r"\bmethylomics?\b",
    r"\bmetagenomics?\b",
    r"\bmass spectrometry\b",
    r"\bolink\b",
    r"\bsomascan\b",
    r"\bsomalogic\b",
    r"\bmulti[- ]omics?\b",
    r"\bmultiomics?\b",
    r"\bmrna expression\b",
    r"\bgene expression\b",
    r"\bplasma proteome\b",
    r"\bplasma proteomic\b",
    r"\bserum proteome\b",
    r"\bmetabolite\b",
    r"\bmetabolic profil\w+\b",
    r"\bproteome[- ]wide\b",
)
# Things that look multi-omic-ish but are actually pure-genomics; we use this
# to reject false positives. We require at least one MULTIOMICS_POS hit and
# we keep the detector independent of GWAS-only language.

# Wearables / remote monitoring
WEARABLE_RE = _re(
    r"\bfitbit\b",
    r"\bapple watch\b",
    r"\baccelerometer\b",
    r"\bwearable\w*\b",
    r"\bactivity tracker\b",
    r"\bheart rate variability\b",
    r"\bhrv\b",
    r"\bcontinuous glucose monitor\w*\b",
    r"\bcgm\b",
    r"\bwhoop\b",
    r"\bsmartwatch\b",
    r"\bremote monitor\w+\b",
    r"\bdigital phenotyp\w+\b",
    r"\bsleep stage\b",
    r"\bsleep[- ]derived\b",
    r"\bstep count\b",
    r"\bpedometer\b",
)

# Imaging / radiomics
IMAGING_RE = _re(
    r"\bradiomics?\b",
    r"\bmri\b",
    r"\bmagnetic resonance imag\w*\b",
    r"\bct scan\b",
    r"\bcomputed tomography\b",
    r"\bultrasound\b",
    r"\boptical coherence tomography\b",
    r"\boct\b",
    r"\bretinal imag\w*\b",
    r"\bfundus imag\w*\b",
    r"\bfundus photograph\w*\b",
    r"\bchest x[- ]?ray\b",
    r"\bmammograph\w+\b",
    r"\bpet imag\w*\b",
    r"\bechocardiograph\w*\b",
    r"\bdxa scan\b",
)
IMAGING_COMBO_RE = _re(
    r"\bdeep learning\b.*\bimage\w*\b",
    r"\bimage\w*\b.*\bdeep learning\b",
)

# AI / foundation models / LLMs (careful: do not over-tag generic "ML in pub")
AI_LLM_RE = _re(
    r"\blarge language model\w*\b",
    r"\bllms?\b",
    r"\bfoundation model\w*\b",
    r"\btransformer model\w*\b",
    r"\bbert\b",
    r"\bgpt\b",
    r"\bchatgpt\b",
    r"\bclinicalbert\b",
    r"\bbiobert\b",
    r"\bgenerative ai\b",
    r"\bdeep learning\b",
    r"\bneural network\w*\b",
    r"\bconvolutional neural\b",
    r"\bself[- ]supervised\b",
    r"\bautoencoder\b",
)
AI_ML_CLINICAL_COMBO_RE = _re(
    r"\bmachine learning\b.{0,80}\bclinical\b",
    r"\bclinical\b.{0,80}\bmachine learning\b",
    r"\bmachine learning\b.{0,80}\bpredict\w+\b.{0,40}\b(risk|outcome|disease)\b",
)

# Environmental
ENV_RE = _re(
    r"\bair pollution\b",
    r"\bpm2\.5\b",
    r"\bpm 2\.5\b",
    r"\bparticulate matter\b",
    r"\bpfas\b",
    r"\bgreenness\b",
    r"\bndvi\b",
    r"\bgreen space\b",
    r"\bresidential exposure\b",
    r"\benvironmental exposure\b",
    r"\bheat exposure\b",
    r"\bheat[- ]related\b",
    r"\bclimate change\b",
    r"\bwildfire\b",
    r"\bbuilt environment\b",
    r"\bwalkability\b",
    r"\benvironmental justice\b",
    r"\beji\b",
)

# G x E x SDOH integrated
GXE_RE = _re(
    r"\bgene[- ]environment\b",
    r"\bgene[- ]by[- ]environment\b",
    r"\bg\s*x\s*e\b",
    r"\bgxe\b",
    r"\bgene[- ]\w+ interaction\b",
    r"\bsocial genomic\w*\b",
)
GXE_COMBO_RE_1 = _re(r"\bpolygenic\b.{0,80}\benvironment\w*\b")
GXE_COMBO_RE_2 = _re(r"\bpolygenic\b.{0,80}\b(sdoh|social determ\w+)\b")
GXE_COMBO_RE_3 = _re(r"\bprs\b.{0,80}\b(sdoh|social determ\w+|environment)\b")

# Nutrition / microbiome
# Per spec keyword list: microbiome, gut microbiota, diet, dietary intake,
# Mediterranean diet, plant-based diet, nutrition+chronic disease combo.
# Deliberately NOT including "food insecurity" / "food security" — those are
# SDOH framings and would leak into the nutrition signal. Also using a tight
# match for "diet" / "dietary" (no \w* tail) to avoid false positives like
# "differentiated."
NUTRITION_RE = _re(
    r"\bmicrobiome\b",
    r"\bgut microbiota\b",
    r"\bgut microbi\w+\b",
    r"\bdiet\b",
    r"\bdiets\b",
    r"\bdietary\b",
    r"\bmediterranean diet\b",
    r"\bplant[- ]based diet\b",
    r"\bplant[- ]based eating\b",
    r"\bnutritional intake\b",
    r"\bnutritional status\b",
    r"\bnutritional epidemiology\b",
)
NUTRITION_COMBO_RE = _re(
    r"\bnutrition\b.{0,80}\bchronic disease\b",
    r"\bdiet\b.{0,80}\bchronic disease\b",
    r"\bdietary\b.{0,80}\bchronic disease\b",
)

# Breakthrough therapeutics
BREAKTHROUGH_RE = _re(
    r"\bglp[- ]?1\b",
    r"\bglp[- ]?1r\b",
    r"\bsemaglutide\b",
    r"\bozempic\b",
    r"\bwegovy\b",
    r"\btirzepatide\b",
    r"\bmounjaro\b",
    r"\bzepbound\b",
    r"\bsglt2\b",
    r"\bsglt[- ]2\b",
    r"\bdapagliflozin\b",
    r"\bempagliflozin\b",
    r"\bcanagliflozin\b",
    r"\blecanemab\b",
    r"\bdonanemab\b",
    r"\baducanumab\b",
    r"\bleqembi\b",
    r"\bkisunla\b",
    r"\baduhelm\b",
    r"\bcheckpoint inhibitor\b",
    r"\bpembrolizumab\b",
    r"\bnivolumab\b",
    r"\bkeytruda\b",
    r"\bopdivo\b",
    r"\bcar[- ]t\b",
    r"\bimmunotherapy\b",
)
BREAKTHROUGH_CRISPR_COMBO_RE = _re(r"\bcrispr\b.{0,80}\bclinical\b")

# Hot-area definitions, keyed by code
HOT_AREAS = [
    ("HA1", "Multi-omics (beyond genomics)"),
    ("HA2", "Wearables / Remote monitoring"),
    ("HA3", "Imaging / Radiomics"),
    ("HA4", "AI / Foundation models / LLMs"),
    ("HA5", "Environmental health"),
    ("HA6", "G x E x SDOH integrated"),
    ("HA7", "Nutrition / Microbiome"),
    ("HA8", "Breakthrough therapeutics"),
]


def detect_hot_areas(text: str) -> dict[str, bool]:
    """Return {HA_code: bool} for the 8 hot areas given title+abstract text."""
    t = text or ""
    result = {}

    # HA1 Multi-omics
    result["HA1"] = bool(MULTIOMICS_POS.search(t))

    # HA2 Wearables
    result["HA2"] = bool(WEARABLE_RE.search(t))

    # HA3 Imaging
    result["HA3"] = bool(IMAGING_RE.search(t) or IMAGING_COMBO_RE.search(t))

    # HA4 AI / LLM / foundation
    result["HA4"] = bool(AI_LLM_RE.search(t) or AI_ML_CLINICAL_COMBO_RE.search(t))

    # HA5 Environment
    result["HA5"] = bool(ENV_RE.search(t))

    # HA6 GxE / GxSDOH
    result["HA6"] = bool(
        GXE_RE.search(t)
        or GXE_COMBO_RE_1.search(t)
        or GXE_COMBO_RE_2.search(t)
        or GXE_COMBO_RE_3.search(t)
    )

    # HA7 Nutrition / microbiome
    result["HA7"] = bool(NUTRITION_RE.search(t) or NUTRITION_COMBO_RE.search(t))

    # HA8 Breakthrough therapeutics
    result["HA8"] = bool(BREAKTHROUGH_RE.search(t) or BREAKTHROUGH_CRISPR_COMBO_RE.search(t))

    return result


# ---------------------------------------------------------------------------
# Build temporal tables
# ---------------------------------------------------------------------------
def parse_year(y) -> int | None:
    if y is None:
        return None
    try:
        return int(str(y).strip()[:4])
    except (ValueError, TypeError):
        return None


def build_temporal():
    pubs = load_tagged_pubs()
    record_ids = set(pubs.keys())
    texts = load_text_for_pubs(record_ids)

    # Theme x year, FA x year
    theme_year: dict[str, Counter[int]] = defaultdict(Counter)
    fa_year: dict[str, Counter[int]] = defaultdict(Counter)
    year_total: Counter[int] = Counter()

    # Theme/FA pre/post counts
    theme_pre: Counter[str] = Counter()
    theme_post: Counter[str] = Counter()
    fa_pre: Counter[str] = Counter()
    fa_post: Counter[str] = Counter()
    pre_total = 0
    post_total = 0

    # Per-pub hot-area detection
    hot_rows = []
    ha_pre: Counter[str] = Counter()
    ha_post: Counter[str] = Counter()
    ha_examples: dict[str, list[tuple[str, str, str]]] = defaultdict(list)  # ha -> (year, pmid, title)
    ha_admin_ics: dict[str, Counter[str]] = defaultdict(Counter)

    for rid, rec in pubs.items():
        year = parse_year(rec.get("year"))
        text_rec = texts.get(rid, {})
        if year is None:
            year = parse_year(text_rec.get("year"))
        if year is None:
            # skip from temporal but still detect hot areas
            year_for_split = None
        else:
            year_total[year] += 1
            year_for_split = year

        themes = [str(t) for t in rec.get("themes", [])]
        fas = set()
        for t in themes:
            theme_year[t][year] += 1 if year else 0
            for fa in theme_focus_areas(t):
                fas.add(fa)
        for fa in fas:
            fa_year[fa][year] += 1 if year else 0

        # pre/post split
        if year_for_split is not None:
            if year_for_split < CUTOFF_YEAR:
                pre_total += 1
                for t in themes:
                    theme_pre[t] += 1
                for fa in fas:
                    fa_pre[fa] += 1
            else:
                post_total += 1
                for t in themes:
                    theme_post[t] += 1
                for fa in fas:
                    fa_post[fa] += 1

        # hot-area detection
        title = text_rec.get("title", "")
        abstract = text_rec.get("abstract", "")
        text_blob = f"{title} {abstract}".lower()
        ha_flags = detect_hot_areas(text_blob)
        hot_row = {
            "record_id": rid,
            "pubmed_id": rec.get("pubmed_id"),
            "year": year,
            "title": (title or "").replace("\n", " ").strip()[:300],
        }
        for ha_code, _ in HOT_AREAS:
            hot_row[ha_code] = int(ha_flags[ha_code])
        hot_rows.append(hot_row)

        # tally pre/post per hot area and examples
        for ha_code, _ in HOT_AREAS:
            if ha_flags[ha_code]:
                if year_for_split is not None:
                    if year_for_split < CUTOFF_YEAR:
                        ha_pre[ha_code] += 1
                    else:
                        ha_post[ha_code] += 1
                # cap examples per HA at ~10 (we'll pick top-3 later by recency)
                if len(ha_examples[ha_code]) < 20:
                    ha_examples[ha_code].append(
                        (
                            str(year) if year else "",
                            str(rec.get("pubmed_id") or ""),
                            title[:160],
                        )
                    )
                # admin IC tally
                for ic in rec.get("admin_ics", []):
                    ha_admin_ics[ha_code][ic] += 1

    # ---------------------------------------------------------------------
    # Write outputs
    # ---------------------------------------------------------------------
    # pub_year_by_theme.csv
    out = HERE / "pub_year_by_theme.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["theme_code", "theme_name"] + [str(y) for y in YEARS] + ["total"])
        for code, info in THEME_MAP.items():
            row = [code, info["name"]]
            total = 0
            for y in YEARS:
                c = theme_year[code].get(y, 0)
                row.append(c)
                total += c
            row.append(total)
            w.writerow(row)
    print(f"wrote {out}")

    # pub_year_by_focus_area.csv
    out = HERE / "pub_year_by_focus_area.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["focus_area_code", "focus_area_name"] + [str(y) for y in YEARS] + ["total"])
        for fa_code, fa_name in FOCUS_AREAS.items():
            row = [fa_code, fa_name]
            total = 0
            for y in YEARS:
                c = fa_year[fa_code].get(y, 0)
                row.append(c)
                total += c
            row.append(total)
            w.writerow(row)
    print(f"wrote {out}")

    # theme_trend_scores.csv
    out = HERE / "theme_trend_scores.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "theme_code",
                "theme_name",
                "pre_2023",
                "post_2023",
                "share_pre",
                "share_post",
                "trend_score",
                "ratio_post_pre",
            ]
        )
        for code, info in THEME_MAP.items():
            pre = theme_pre.get(code, 0)
            post = theme_post.get(code, 0)
            sp = pre / pre_total if pre_total else 0
            spost = post / post_total if post_total else 0
            trend = round(spost - sp, 4)
            ratio = round(post / pre, 3) if pre else (float("inf") if post else 0)
            w.writerow(
                [
                    code,
                    info["name"],
                    pre,
                    post,
                    round(sp, 4),
                    round(spost, 4),
                    trend,
                    ratio,
                ]
            )
    print(f"wrote {out}")

    # focus_area_trend_scores.csv
    out = HERE / "focus_area_trend_scores.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "focus_area_code",
                "focus_area_name",
                "pre_2023",
                "post_2023",
                "share_pre",
                "share_post",
                "trend_score",
                "ratio_post_pre",
            ]
        )
        for fa_code, fa_name in FOCUS_AREAS.items():
            pre = fa_pre.get(fa_code, 0)
            post = fa_post.get(fa_code, 0)
            sp = pre / pre_total if pre_total else 0
            spost = post / post_total if post_total else 0
            trend = round(spost - sp, 4)
            ratio = round(post / pre, 3) if pre else (float("inf") if post else 0)
            w.writerow(
                [fa_code, fa_name, pre, post, round(sp, 4), round(spost, 4), trend, ratio]
            )
    print(f"wrote {out}")

    # hot_areas_detection.csv (per-pub bool columns)
    out = HERE / "hot_areas_detection.csv"
    with out.open("w", newline="") as f:
        cols = ["record_id", "pubmed_id", "year", "title"] + [ha for ha, _ in HOT_AREAS]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in hot_rows:
            w.writerow(r)
    print(f"wrote {out}")

    # hot_areas_summary.csv
    out = HERE / "hot_areas_summary.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "ha_code",
                "ha_name",
                "total_pubs",
                "pre_2023",
                "post_2023",
                "share_pre",
                "share_post",
                "trend_score",
                "ratio_post_pre",
                "top3_admin_ics",
                "example1",
                "example2",
                "example3",
                "thin_coverage_flag",
            ]
        )
        for ha_code, ha_name in HOT_AREAS:
            pre = ha_pre.get(ha_code, 0)
            post = ha_post.get(ha_code, 0)
            total = pre + post
            sp = pre / pre_total if pre_total else 0
            spost = post / post_total if post_total else 0
            trend = round(spost - sp, 4)
            ratio = round(post / pre, 3) if pre else (float("inf") if post else 0)
            top_ics = ha_admin_ics[ha_code].most_common(3)
            top_ic_str = ";".join(f"{ic}({n})" for ic, n in top_ics) if top_ics else ""
            # pick 3 examples — prefer 2023+ and highest year
            ex = sorted(
                ha_examples[ha_code],
                key=lambda x: (int(x[0]) if x[0].isdigit() else 0),
                reverse=True,
            )
            ex = [(yr, pmid, title) for yr, pmid, title in ex if pmid][:3]
            ex_str = [
                (f"PMID:{pmid} ({yr}) {title}" if pmid else f"({yr}) {title}")
                for yr, pmid, title in ex
            ]
            while len(ex_str) < 3:
                ex_str.append("")
            thin = "thin coverage (<10 pubs)" if total < 10 else ""
            w.writerow(
                [
                    ha_code,
                    ha_name,
                    total,
                    pre,
                    post,
                    round(sp, 4),
                    round(spost, 4),
                    trend,
                    ratio,
                    top_ic_str,
                    *ex_str,
                    thin,
                ]
            )
    print(f"wrote {out}")

    # Print summary table for inline narrative
    print()
    print(f"pre-2023 substantive pubs: {pre_total}")
    print(f"post-2023 substantive pubs: {post_total}")
    print()
    print("Hot area | total | pre | post | trend_score | top admin ICs")
    for ha_code, ha_name in HOT_AREAS:
        pre = ha_pre.get(ha_code, 0)
        post = ha_post.get(ha_code, 0)
        total = pre + post
        sp = pre / pre_total if pre_total else 0
        spost = post / post_total if post_total else 0
        trend = round(spost - sp, 4)
        top_ics = ha_admin_ics[ha_code].most_common(3)
        top_ic_str = ";".join(f"{ic}({n})" for ic, n in top_ics) if top_ics else ""
        print(
            f"  {ha_code} {ha_name:38s} {total:4d} | {pre:4d} | {post:4d} | {trend:+.4f} | {top_ic_str}"
        )

    print()
    print("Theme trend scores (sorted by trend, growing first):")
    th_rows = []
    for code, info in THEME_MAP.items():
        pre = theme_pre.get(code, 0)
        post = theme_post.get(code, 0)
        sp = pre / pre_total if pre_total else 0
        spost = post / post_total if post_total else 0
        trend = spost - sp
        th_rows.append((trend, code, info["name"], pre, post))
    th_rows.sort(reverse=True)
    for trend, code, name, pre, post in th_rows:
        print(f"  {code:>2}  {name:55s} pre={pre:3d}  post={post:3d}  trend={trend:+.4f}")

    print()
    print("Focus-area trend scores (sorted by trend, growing first):")
    fa_rows = []
    for fa_code, fa_name in FOCUS_AREAS.items():
        pre = fa_pre.get(fa_code, 0)
        post = fa_post.get(fa_code, 0)
        sp = pre / pre_total if pre_total else 0
        spost = post / post_total if post_total else 0
        trend = spost - sp
        fa_rows.append((trend, fa_code, fa_name, pre, post))
    fa_rows.sort(reverse=True)
    for trend, fa_code, fa_name, pre, post in fa_rows:
        print(
            f"  {fa_code}  {fa_name:55s} pre={pre:4d}  post={post:4d}  trend={trend:+.4f}"
        )

    print()
    print("Year totals:")
    for y in YEARS:
        print(f"  {y}: {year_total.get(y, 0)}")


if __name__ == "__main__":
    build_temporal()

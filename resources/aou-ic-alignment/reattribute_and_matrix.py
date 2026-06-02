"""Phase 3c: OD re-attribution + 3 alignment matrices.

Reads:
  - publications_tagged.csv  (1378 pubs, themes + admin_ics + cofunding_ics)
  - projects_tagged.csv      (12,899 projects, themes only — no IC info)
  - ic_priorities.csv        (curated priorities + aou_theme_tags)
  - theme_to_ic_mapping.csv  (documented OD re-attribution rules)

Writes:
  - publications_reattributed.csv
  - alignment_matrix.csv             — composite (corpus activity + priorities)
  - alignment_matrix_normalized.csv  — each row sums to 1.0 across ICs
  - alignment_matrix_priority_only.csv
  - alignment_matrix_corpus_only.csv
"""
import csv
import json
import os
from collections import defaultdict

LANDSCAPE = "/Users/melissahaendel/Documents/GitHub/all-of-us/resources/aou-research-landscape"
OUT_DIR = "/Users/melissahaendel/Documents/GitHub/all-of-us/resources/aou-ic-alignment"

# -----------------------------------------------------------------------
# IC scope (column order for matrices)
# Plus NIH-Wide. Plus a residual "OD-unattributable" bucket for transparency.
# -----------------------------------------------------------------------
IC_SCOPE = [
    "NIH-Wide",
    "NCI", "NHGRI", "NHLBI", "NIA", "NIAAA", "NIAID", "NIAMS",
    "NIBIB", "NICHD", "NIDA", "NIDDK", "NIEHS", "NIGMS",
    "NIMH", "NIMHD", "NINDS", "NLM", "NCATS", "NCCIH", "NEI",
]

# NIH RePORTER 2-letter admin/cofunding codes → IC short name
IC_CODE_MAP = {
    "CA": "NCI", "HG": "NHGRI", "HL": "NHLBI", "AG": "NIA",
    "AA": "NIAAA", "AI": "NIAID", "AR": "NIAMS", "EB": "NIBIB",
    "HD": "NICHD", "DA": "NIDA", "DK": "NIDDK", "ES": "NIEHS",
    "GM": "NIGMS", "MH": "NIMH", "MD": "NIMHD", "NS": "NINDS",
    "LM": "NLM", "TR": "NCATS", "AT": "NCCIH", "EY": "NEI",
    # Out-of-scope but present in source data; will be skipped for matrix col
    "DC": "NIDCD-OOS", "DE": "NIDCR-OOS", "NR": "NINR-OOS",
    "FD": "FIC-OOS", "RR": "NCRR-OOS", "OD": "OD",
}

# Themes considered in scope (top-level 1..19). Subthemes & META excluded.
THEMES = [str(i) for i in range(1, 20)]

# -----------------------------------------------------------------------
# OD re-attribution rules (theme_code → list of (IC, weight))
# Implements `theme_to_ic_mapping.csv` programmatically.
# Weights for a single theme sum to 1.0; pub-level weights are renormalized.
# -----------------------------------------------------------------------
THEME_TO_IC = {
    "1":  [("NHLBI", 0.7), ("NIDDK", 0.3)],  # Cardiometabolic
    "2":  [("NHGRI", 1.0)],                  # Genomics methods
    "3":  [("NLM",  1.0)],                   # Methods/Infrastructure
    "4":  [("NIMH", 0.7), ("NIDA", 0.2), ("NIAAA", 0.1)],
    "5":  [("NCI",  1.0)],
    "6":  [("NIMHD", 1.0)],
    "7":  [("NIBIB", 0.5), ("NHLBI", 0.2), ("NIDDK", 0.15), ("NIMH", 0.15)],
    "8":  [("NIAID", 1.0)],
    "9":  [("NIAID", 0.5), ("NIAMS", 0.5)],
    "10": [("NCATS", 0.5), ("NHGRI", 0.5)],
    "11": [("NIA",   0.8), ("NINDS", 0.2)],
    "12": [("NIAMS", 0.7), ("NCI",   0.3)],  # Dermatology
    "13": [("NHLBI", 1.0)],
    "14": [("NINDS", 1.0)],
    "15": [("NICHD", 1.0)],
    "16": [("NIGMS", 0.6), ("NHGRI", 0.2), ("NHLBI", 0.1), ("NCI", 0.1)],
    "17": [("NIH-Wide", 0.7), ("NHGRI", 0.3)],
    "18": [("NEI",  1.0)],
    "19": [("NIEHS", 1.0)],
}


def parse_ics(s):
    """Parse a semi-colon separated IC code string into a list of (IC, count).
    Format examples: 'OD(2);TR(1);HG(1)' or 'OD' or ''."""
    out = []
    if not s:
        return out
    for tok in s.split(";"):
        tok = tok.strip()
        if not tok:
            continue
        if "(" in tok:
            code, rest = tok.split("(", 1)
            n = int(rest.rstrip(")"))
        else:
            code, n = tok, 1
        out.append((code.strip(), n))
    return out


def code_to_ic(code):
    return IC_CODE_MAP.get(code, code)


def pub_themes_to_ic_weights(themes_str):
    """Given semicolon-separated theme codes (e.g. '1;3;6'), return dict IC -> weight.
    Weights renormalized so the pub's total weight = 1.0.
    """
    themes = [t for t in (themes_str or "").split(";") if t.strip() in THEMES]
    if not themes:
        return None
    raw = defaultdict(float)
    per_theme = 1.0 / len(themes)
    for th in themes:
        for ic, w in THEME_TO_IC.get(th, []):
            raw[ic] += w * per_theme
    if not raw:
        return None
    s = sum(raw.values())
    if s > 0:
        for k in raw:
            raw[k] /= s
    return dict(raw)


def main():
    # ---- Load priorities -------------------------------------------------
    priority_ic_themes = defaultdict(list)  # IC -> list of priority theme tag-lists
    with open(os.path.join(OUT_DIR, "ic_priorities.csv")) as f:
        for row in csv.DictReader(f):
            tags = [t.strip() for t in row["aou_theme_tags"].split(";") if t.strip() in THEMES]
            priority_ic_themes[row["ic"]].append(tags)

    # ---- Read publications --------------------------------------------------
    pub_rows = []
    with open(os.path.join(LANDSCAPE, "publications_tagged.csv")) as f:
        for row in csv.DictReader(f):
            if row["in_substantive_corpus"].lower() != "true":
                continue
            pub_rows.append(row)
    print(f"Loaded {len(pub_rows)} substantive pubs")

    # ---- Re-attribute --------------------------------------------------
    out_rows = []
    pub_ic_weights = defaultdict(lambda: defaultdict(float))  # theme -> ic -> sum
    pub_total_per_ic = defaultdict(float)
    od_reattributed = 0
    od_unattributable = 0

    for r in pub_rows:
        themes = [t for t in r["themes"].split(";") if t.strip() in THEMES]
        admin_orig = parse_ics(r["admin_ics"])
        cofund_orig = parse_ics(r["cofunding_ics"])

        # Determine if original admin contains OD-only or OD-primary
        admin_ic_codes = [code_to_ic(c) for c, n in admin_orig]
        is_od = (len(admin_ic_codes) >= 1) and (admin_ic_codes[0] == "OD")
        is_od_only = is_od and len([c for c in admin_ic_codes if c != "OD"]) == 0

        # Compute IC weights from themes (this is the re-attribution table)
        theme_weights = pub_themes_to_ic_weights(r["themes"])

        if is_od_only:
            if theme_weights:
                reattr_admin = ";".join(
                    [f"{ic}({w:.2f})" for ic, w in sorted(theme_weights.items(),
                                                          key=lambda x: -x[1])]
                )
                od_reattributed += 1
                weights_for_matrix = theme_weights
            else:
                reattr_admin = "OD-unattributable"
                od_unattributable += 1
                weights_for_matrix = {"OD-unattributable": 1.0}
        else:
            # Non-OD admin pub: keep original; but also compute theme-weights
            # for use in the matrix corpus_only attribution (because the matrix
            # is theme-resolved, not admin-resolved). For consistency we use
            # the theme-derived weights as the per-pub IC distribution for the
            # matrix, but ALSO preserve admin_orig in the output.
            reattr_admin = r["admin_ics"]
            if theme_weights:
                weights_for_matrix = theme_weights
            else:
                # fallback: distribute to non-OD admin ICs equally
                non_od = [c for c in admin_ic_codes if c != "OD"]
                if non_od:
                    s = 1.0 / len(non_od)
                    weights_for_matrix = {ic: s for ic in non_od}
                else:
                    weights_for_matrix = {}

        # Update the matrix counts: pubs split fractionally across themes AND ICs
        # The cell value is: theme-share × ic-share within that theme-share.
        if themes:
            per_theme = 1.0 / len(themes)
            for th in themes:
                for ic, w in THEME_TO_IC.get(th, []):
                    pub_ic_weights[th][ic] += per_theme * w
                    pub_total_per_ic[ic] += per_theme * w

        out_rows.append({
            "record_id": r["record_id"],
            "pubmed_id": r.get("pubmed_id", ""),
            "year": r.get("year", ""),
            "title": r.get("title", ""),
            "themes": r["themes"],
            "ic_admin_original": r.get("admin_ics", ""),
            "ic_admin_reattributed": reattr_admin,
            "cofunding_ics_original": r.get("cofunding_ics", ""),
            "fractional_attribution": ";".join(
                f"{k}({v:.3f})" for k, v in sorted(
                    (weights_for_matrix or {}).items(), key=lambda x: -x[1]
                )
            ),
        })

    print(f"OD re-attributed: {od_reattributed}; OD unattributable: {od_unattributable}")

    # write per-pub
    with open(os.path.join(OUT_DIR, "publications_reattributed.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    print(f"wrote publications_reattributed.csv  ({len(out_rows)} rows)")

    # ---- Project density (no IC info on projects, so attribute by theme rule)
    proj_ic_weights = defaultdict(lambda: defaultdict(float))
    proj_n = 0
    with open(os.path.join(LANDSCAPE, "projects_tagged.csv")) as f:
        for row in csv.DictReader(f):
            if row["in_substantive_corpus"].lower() != "true":
                continue
            themes = [t for t in row["themes"].split(";") if t.strip() in THEMES]
            if not themes:
                continue
            proj_n += 1
            per_theme = 1.0 / len(themes)
            for th in themes:
                for ic, w in THEME_TO_IC.get(th, []):
                    proj_ic_weights[th][ic] += per_theme * w
    print(f"Substantive projects: {proj_n}")

    # ---- Build the matrix ---------------------------------------------------
    # Cells = composite score:
    #   composite = 0.5 * z_corpus + 0.5 * z_priority
    # Where:
    #   z_corpus    = normalized( pub-weight + 0.1 * project-weight ) by theme
    #   z_priority  = count of priorities for that IC tagged with this theme
    # Three matrices:
    #   1) raw composite (sum of pub fractional weights + 0.1 * project + priority count)
    #   2) row-normalized (each row sums to 1.0 across ICs)
    #   3) priority_only
    #   4) corpus_only

    # priority count per IC per theme
    priority_count = defaultdict(lambda: defaultdict(int))
    for ic, plist in priority_ic_themes.items():
        for tags in plist:
            for th in tags:
                priority_count[ic][th] += 1

    # Build matrices: theme rows × IC cols. Include extra audit columns for OD-unattributable
    # but we keep matrix at THEMES × IC_SCOPE.
    def build_matrix(score_fn):
        # Returns dict[theme][ic] -> score
        m = {th: {ic: 0.0 for ic in IC_SCOPE} for th in THEMES}
        for th in THEMES:
            for ic in IC_SCOPE:
                m[th][ic] = score_fn(th, ic)
        return m

    def corpus_score(th, ic):
        return pub_ic_weights[th].get(ic, 0.0) + 0.1 * proj_ic_weights[th].get(ic, 0.0)

    def priority_score(th, ic):
        return float(priority_count[ic].get(th, 0))

    def composite_score(th, ic):
        # Composite combines corpus (scaled by IC-pub volume) + priority count
        # Use a simple sum with the convention that 1 unit of priority count ~=
        # 5 fractional pubs (approximately equal weight in the strong cells).
        return corpus_score(th, ic) + 5.0 * priority_score(th, ic)

    def normalize_rows(m):
        out = {}
        for th, row in m.items():
            s = sum(row.values())
            if s > 0:
                out[th] = {ic: v / s for ic, v in row.items()}
            else:
                out[th] = {ic: 0.0 for ic in row}
        return out

    matrix_composite = build_matrix(composite_score)
    matrix_corpus_only = build_matrix(corpus_score)
    matrix_priority_only = build_matrix(priority_score)
    matrix_normalized = normalize_rows(matrix_composite)

    def write_matrix(m, path, theme_name_map):
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["theme_code", "theme_name"] + IC_SCOPE + ["row_total"])
            for th in THEMES:
                row = [m[th].get(ic, 0) for ic in IC_SCOPE]
                w.writerow([th, theme_name_map.get(th, "")] + [
                    f"{v:.4f}" for v in row
                ] + [f"{sum(row):.4f}"])
            # Total
            col_totals = [sum(m[th].get(ic, 0) for th in THEMES) for ic in IC_SCOPE]
            w.writerow(["TOTAL", ""] + [f"{v:.4f}" for v in col_totals] + [
                f"{sum(col_totals):.4f}"
            ])
        print(f"wrote {path}")

    # theme code -> name
    theme_names = {}
    with open(os.path.join(LANDSCAPE, "theme_summary.csv")) as f:
        for row in csv.DictReader(f):
            theme_names[row["theme_code"]] = row["theme_name"]

    write_matrix(matrix_composite, os.path.join(OUT_DIR, "alignment_matrix.csv"), theme_names)
    write_matrix(matrix_normalized, os.path.join(OUT_DIR, "alignment_matrix_normalized.csv"), theme_names)
    write_matrix(matrix_priority_only, os.path.join(OUT_DIR, "alignment_matrix_priority_only.csv"), theme_names)
    write_matrix(matrix_corpus_only, os.path.join(OUT_DIR, "alignment_matrix_corpus_only.csv"), theme_names)

    # ---- Print quick summary
    print("\n=== Corpus-only top theme/IC pairs ===")
    pairs = []
    for th in THEMES:
        for ic in IC_SCOPE:
            v = matrix_corpus_only[th][ic]
            if v > 0:
                pairs.append((v, th, theme_names.get(th, ""), ic))
    pairs.sort(reverse=True)
    for v, th, n, ic in pairs[:25]:
        print(f"  T{th:3s} {ic:8s} corpus={v:.2f}  ({n})")

    print("\n=== Priority-only top theme/IC pairs ===")
    pairs = []
    for th in THEMES:
        for ic in IC_SCOPE:
            v = matrix_priority_only[th][ic]
            if v > 0:
                pairs.append((v, th, theme_names.get(th, ""), ic))
    pairs.sort(reverse=True)
    for v, th, n, ic in pairs[:25]:
        print(f"  T{th:3s} {ic:8s} priority={v:.0f}  ({n})")


if __name__ == "__main__":
    main()

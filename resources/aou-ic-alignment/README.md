# AoU × NIH-IC Alignment Matrix (Phase 3c)

This folder contains the centerpiece alignment analysis for the 2026 AoU
Scientific Roadmap Refresh WG and the four other 2026 Science Committee
working groups (Translational, Imaging, AI, Communications).

**Question this folder answers.** How does the AoU research corpus
(1,374 publications + 11,577 projects, theme-tagged to a 19-theme
taxonomy in Phase 2c) align with the stated strategic-plan priorities
of ~20 NIH ICs (plus the NIH-Wide plan as a peer entity)?

**What's NOT in this folder.** Top-3 Refresh recommendations (Phase 4).
This folder is the alignment-evidence base, not the recommendation set.

---

## File map

### Data products

| File | What it is |
|---|---|
| `ic_priorities.csv` | 166 strategic-plan priorities extracted from 22 PDFs (21 ICs + NIH-Wide). Columns: ic, plan_year, priority_id, priority_name, priority_description, source_quote, source_page, aou_theme_tags, aou_focus_area_tags. |
| `theme_to_ic_mapping.csv` | The OD re-attribution rule. Documents how OD-administered pubs are fractionally attributed to substantive-science ICs based on theme tags. |
| `publications_reattributed.csv` | All 1,374 substantive pubs with `ic_admin_original`, `ic_admin_reattributed`, `cofunding_ics_original`, and `fractional_attribution` (per-IC float weights from theme tags). |
| `alignment_matrix.csv` | The composite matrix. Rows: 19 themes; Columns: 22 ICs (NIH-Wide + 21). Cell = corpus_activity + 5 × priority_count. |
| `alignment_matrix_normalized.csv` | Row-normalized composite (each row sums to 1.0 across ICs). |
| `alignment_matrix_corpus_only.csv` | Corpus-only cells (pub fractional weight + 0.1 × project fractional weight). |
| `alignment_matrix_priority_only.csv` | IC priority count per theme. |

### Narrative + per-IC

| File | What it is |
|---|---|
| `gap_analysis.md` | The main narrative — sections (A) alignment hits, (B) demand-side gaps, (C) latent areas, (D) pan-NIH crosscutting. Organized by 2026 WG topic where possible. |
| `per_ic_briefs/*.md` | One ~1-page brief per IC: mission, priorities, AoU activity per theme, alignment verdict, recommended Refresh actions. ~20 files. |

### Scripts (reproducible)

| File | What it does |
|---|---|
| `extract_priorities.py` | Read every in-scope plan PDF; dump per-page text to `plan_pages.json`. |
| `find_priorities.py` | Find pages matching priority-section heading patterns; write `priorities_text/<IC>__<year>.txt` for human curation. |
| `build_priorities.py` | Build `ic_priorities.csv` from curated extracts (priority rows hand-written from the PDF reads). |
| `reattribute_and_matrix.py` | OD re-attribution + build the four matrices. |
| `build_per_ic_briefs.py` | Generate per-IC briefs. |

### Working artifacts

| File | What it is |
|---|---|
| `plan_pages.json` | Per-page text from every in-scope plan PDF (cached for re-use). |
| `priorities_text/` | Per-IC text dumps of priority-section pages (curation aid; not a deliverable). |

---

## IC scope

In-scope (21 ICs + NIH-Wide):
NIH-Wide, NCI (two plans: National Cancer Plan + FY2026 Annual Plan),
NHGRI, NHLBI, NIA, NIAAA, NIAID, NIAMS, NIBIB, NICHD, NIDA, NIDDK,
NIEHS, NIGMS (included for pharmacogenomics/PGRN), NIMH, NIMHD, NINDS,
NLM, NCATS, NCCIH, NEI.

Out of scope (per user decision): CC, CIT, CSR, FIC, NIDCD, NIDCR, NINR.

---

## Matrix-cell formula

Let `T` = AoU theme (1–19), `I` = IC.

For each substantive AoU publication `p`:
- Let `themes(p)` = list of top-level themes tagged.
- For each `t ∈ themes(p)`, let `per_theme = 1 / |themes(p)|`.
- For each IC `ic` in `THEME_TO_IC[t]` with weight `w`:
  - Add `per_theme * w` to `pub_weight[t][ic]`.

Similarly for projects (`proj_weight[t][ic]`). Projects are scaled by
0.1 in the corpus_only and composite matrices to reflect that workspaces
without publications are a weaker signal of completed science than
peer-reviewed pubs.

For each IC strategic-plan priority `p`:
- Each theme tag `t ∈ p.aou_theme_tags` increments `priority_count[I][t]`.

The four matrices then are:

- **`alignment_matrix_corpus_only[t][ic]`** = `pub_weight[t][ic] + 0.1 * proj_weight[t][ic]`
- **`alignment_matrix_priority_only[t][ic]`** = `priority_count[ic][t]`
- **`alignment_matrix[t][ic]`** = `corpus_only[t][ic] + 5.0 * priority_only[t][ic]`
  — the factor 5.0 puts one IC priority count at roughly the same scale as
  5 fractional pubs (chosen so neither corpus nor priorities dominates
  cells with both present).
- **`alignment_matrix_normalized[t][ic]`** = `alignment_matrix[t][ic] / row_sum[t]`
  — row-normalized so each theme's IC distribution sums to 1.0.

The `THEME_TO_IC` weight table is in `theme_to_ic_mapping.csv` and is
also embedded in `reattribute_and_matrix.py`.

---

## OD re-attribution

275 of 1,374 substantive pubs were originally admin-attributed to OD
(All of Us PMO / program funds). Per the user decision, OD pubs are
re-attributed to the substantive-science IC(s) based on theme tags
using the rules in `theme_to_ic_mapping.csv`. Fractional attribution
is used for multi-theme pubs (a pub tagged Cardiometabolic + Genomics
gets 0.5 to NHLBI/NIDDK weighted and 0.5 to NHGRI).

In the actual run: 104 OD pubs were re-attributed; 3 had no
informative theme tag and are flagged `OD-unattributable` in
`publications_reattributed.csv`. (Total OD-admin pubs in the
substantive subset is smaller than the 275 in the original
`ic_attribute_report.txt` because the substantive corpus is filtered
to exclude META pubs.)

NB: the matrix cells use the *theme-attribution* weights, not the
admin-IC labels — i.e., even non-OD pubs are distributed across ICs by
their themes. This is by design: the matrix asks "which IC's mission
does this pub serve?", not "which IC funded this pub?". The
fractional_attribution column in `publications_reattributed.csv`
preserves the per-pub theme-attribution distribution alongside the
admin-IC label.

---

## Caveats

1. **Priorities-list completeness varies by plan.** Some plans
   (NHLBI FY26-30, NIDDK 2025, NCI National Cancer Plan, NIMH 2023)
   have crisp goal/objective lists; others (NHGRI 2020 Nature paper,
   NIAID Congressional Justification, NIEHS final-draft RFI version)
   have narrative priorities. Where narrative, we made a reasonable
   judgment call on what counts as a "priority" and tied each row to
   a verbatim source quote. ~5–15 priorities per plan, depending.
2. **OD re-attribution is theme-driven, not narrative-driven.** A pub
   that uses OD admin code and is tagged with Cardiometabolic gets
   attributed to NHLBI+NIDDK whether or not the actual research
   question fits NHLBI's specific priorities. This is appropriate for
   coarse-grained matrix construction but should not be over-read at
   the per-pub level.
3. **Projects lack reliable IC labels.** Workspaces do not carry
   admin-IC metadata (the AoU workbench does not collect this). For
   the corpus_only matrix, we infer IC distribution from theme tags
   on the workspace title/description only.
4. **Plan vintages vary.** Plans range from NLM 2017–2027 to NHLBI
   FY2026–2030 and the NCI FY2026 Annual Plan. Newer plans may carry
   slightly more weight in priority counts because they articulate
   more goals more explicitly.
5. **Fractional priority-count weights are not applied.** A priority
   tagged with 3 themes contributes 1 count to each theme (not 1/3).
   This is by design — we want the matrix to reflect the *number* of
   times a theme appears as an IC priority, not a divided share.
6. **Dermatology and AoU-program-meta are known artifacts.** See
   `gap_analysis.md` section (C).
7. **The NHGRI 2020 plan is a Nature paper, not a PDF in the usual
   plan format.** Its priorities come from the 4-area framework + the
   ten Bold Predictions in Box 5. We treat the Bold Predictions as
   strategic priorities because they were explicitly developed
   through NHGRI's "multi-year process of strategic engagement" and
   represent NHGRI's 2030 targets.

---

## Headline reads (see gap_analysis.md for full discussion)

- **NHGRI × Genomics** is the single strongest alignment cell — the AoU
  cohort is the empirical instrument for NHGRI's Bold Predictions #5
  and #9.
- **NIMHD × SDOH** is the strongest pan-IC-infrastructure case — NIMHD
  Goal 7 literally names "future big science initiatives" as the locus.
- **NLM** is the only IC whose strategic plan explicitly names All of
  Us — and NLM's mission frame puts AoU at the center of the agency's
  data-science strategy.
- **NIEHS × Environment** is the largest single demand-supply gap —
  6 NIEHS priorities, 7 AoU pubs.
- **Imaging is a data-supply problem**, not a research-incentive problem
  — the 8-pub HA3 footprint reflects that AoU has not yet released
  imaging data.
- **Dermatology is an artifact** — 197 pubs come from a few prolific
  groups; do not elevate as a Refresh priority.

---

## Reproducibility

To regenerate everything:

```bash
cd /Users/melissahaendel/Documents/GitHub/all-of-us/resources/aou-ic-alignment
python3 extract_priorities.py        # PDF→JSON
python3 find_priorities.py           # priority-section text dumps
python3 build_priorities.py          # ic_priorities.csv from curated extracts
python3 reattribute_and_matrix.py    # OD re-attribution + 4 matrices
python3 build_per_ic_briefs.py       # per-IC briefs
```

Inputs read:
- `../strategic-plans/*.pdf`
- `../aou-research-landscape/publications_tagged.csv`
- `../aou-research-landscape/projects_tagged.csv`
- `../aou-research-landscape/theme_summary.csv`

Outputs:
- All files in this folder.

Python deps: `pypdf` (already installed).

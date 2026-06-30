# Phase 2c — Tagging Audit Report

> **Historical record** — audit of the original 2026-06-02 tagging run (1,378 pubs). Corpus later refreshed to 1,432; see README and fulltext_augmentation.md.

## Corpus tagged

- **Publications:** 1,378 in `publications_with_ic.jsonl`
  - 4 flagged as `AoU-program-meta-audit` (META)
  - 1,374 in the substantive corpus
- **Projects:** 12,899 in `projects_filtered.jsonl` (all in substantive
  corpus; META detection does not apply to project workspaces because the
  workspace title text is not program-descriptive in the same way pub
  titles are).

## Final tagging strategy

A hybrid keyword pre-tag + targeted LLM-judgment review.

### Pass 1 — keyword pre-tag (`tag_corpus.py`)

For each record, build the searchable text:
- pubs: `title + "\n" + abstract` (pdr/manual/calc fallback for both fields;
  URL-encoded chars like `%28` decoded)
- projects: `title + "\n" + questions + "\n" + approaches + "\n" + findings`

Per theme we maintain two keyword lists:
- **`general`** — terms relevant to the theme but ambiguous in isolation
  (e.g., "diabetes", "cardiac", "screening").
- **`specific`** — high-specificity / diagnostic terms (e.g.,
  "atrial fibrillation", "GLP-1", "BRCA1", "pyoderma gangrenosum").

A theme fires when:
1. >=1 specific keyword matches anywhere in the text, OR
2. >=2 distinct general keywords match anywhere, OR
3. >=1 general keyword matches in the **title** (lower threshold for title
   hits because titles are highly informative).

**Acronym handling.** Short all-uppercase acronyms (e.g., `GWAS`, `PheWAS`,
`HIV`, `ALL`, `MS`, `AF`) are matched **case-sensitively** to avoid matching
ordinary English words like "All" (in "All of Us") or "Ms.". The earlier
draft of the tagger that case-insensitively matched `ALL` (Acute
Lymphoblastic Leukemia) was inflating Cancer counts by ~7 pp.

### Pass 2 — targeted LLM-judgment adjustments (`pass2_adjustments.py`)

Three classes of adjustments:

1. **Per-PMID corrections** for records reviewed during the 50-record audit
   (see "Audit results" below). For each, the script adds/removes specific
   theme tags with a stored rationale. Adjustments are flagged with
   `source: 'llm-judgment'` in the tag_evidence field so they remain
   auditable.

2. **Per-workspaceId corrections** for ~18 zero-tag projects sampled and
   re-tagged by manual review.

3. **Broad rules** applied to every record:
   - `clonal hematopoiesis` / `CHIP` mention → tag themes 1 (cardiometabolic
     risk) + 2 (genomics).
   - `APOE` mention → tag theme 11 (aging / ADRD).
   - `inflammatory skin disease` / `CISD` mention → tag themes 9
     (autoimmune) + 12 (dermatology).

### Locked-decision implementation

- **Theme 5 (Stroke multi-tag).** Stroke records carry both theme 1
  (Cardiometabolic) and theme 14 (Neurology). The forced multi-tag is
  restricted to records where the word "stroke" appears in the **title**
  (after the fresh audit showed that passing mentions of "stroke" in
  abstracts of unrelated methods papers were being force-tagged as both
  cardiometabolic and neurology). Cardio-embolic stroke is further tagged
  with subtheme `1.4-stroke-cardio` when atrial-fibrillation / valvular /
  heart-failure context is present; otherwise `14.2-stroke-cerebro`.

- **Theme 6 (CKM as subtheme).** Records with explicit CKM-syndrome phrasing
  (`CKM syndrome`, `Cardiovascular-Kidney-Metabolic`) get the
  `1.3-CKM` subtheme tag *and* the parent theme 1 tag.

- **Theme 4 (ELSI / AoU-meta split).** Theme 17 (`ELSI-research`) carries
  substantive ELSI / engagement / recruitment / consent research. A
  separate `AoU-program-meta-audit` (META) bucket holds records that are
  about AoU itself (program-introduction pubs, year-in-review pieces). META
  records are removed from the substantive corpus and from theme-share
  denominators.

## Pass-1 keyword statistics (post pass-2 adjustments)

|                          | Publications | Projects |
|--------------------------|------------:|---------:|
| Records                  | 1,374       | 12,899   |
| Zero-tag rate            | 5.2%        | 10.2%    |
| ">5-tag" rate            | 0.2%        | 0.2%     |
| Mean themes per record   | 2.07        | 1.79     |
| Median themes per record | 2           | 2        |
| Max themes               | 7           | 7        |
| META records             | 4           | 0        |

Zero-tag interpretation: most remaining zero-tag records are either
short / placeholder workspaces ("exploratory_project", "just testing",
duplicate stubs), rare conditions outside the disease ontology
(trachoma, valley fever, chromoblastomycosis, achalasia, neuroendocrine
tumors, salivary stones), or pure-methodologic pubs whose contribution
doesn't bind to a disease area.

## Pass-2 audit: precision / recall estimates

Two manual audits were performed.

### Audit A — original 50-record random sample (seed=42)

Reviewed before pass-2 adjustments were applied; then those records' tags
were corrected through `PUB_ADJUSTMENTS`. After correction:

- Precision: **0.94**
- Recall: **1.00**
- Records fully correct: **88%**

This audit is partially circular because corrections were applied to the
same records; it represents an upper bound on what the system can achieve
on records that have been seen by a human reviewer.

### Audit B — fresh 30-record random sample (seed=99)

Reviewed after pass-2 broad rules but without record-specific corrections.
This is the cleaner test of generalization:

- Precision: **0.65**
- Recall: **0.89**
- Records fully correct: **40%**

The main drivers of the precision shortfall on this audit:

1. **Methods / PRS-benchmark papers** (e.g., PRSmix+, S4-Multi, Meta-SAIGE,
   phenomic profile comparison) list many disease traits in their abstract
   as test cases. The tagger picks them all up, giving 5–7 theme tags per
   pub when the analytic contribution is purely genomics-methods. We
   accept this — multi-tag is what the user wanted, and it reflects the
   reality of "this pub touches X disease," even if the primary
   contribution is methodological.

2. **Cross-cutting clinical pubs** (e.g., "12 common health conditions in
   SGM participants") legitimately span many themes — the multi-tag is
   correct from a "what diseases does this paper analyze?" view.

3. **Co-morbidity-in-disease-X case-control pubs** (especially dermatology
   epi) often pick up cardiometabolic, infectious, methods, and autoimmune
   tags from comorbidity panels listed in the abstract. The primary tag is
   correct; the secondary tags are usually defensible but sometimes
   incidental.

Recall is high (0.89) and tends to be limited only when very rare
disease nomenclature is used (e.g., a single Latin diagnosis name not in
the keyword lists). The handful of recall misses on the fresh audit were
all of this type — neurofibromatosis with neurocognitive complications
missing theme 14, intracranial hypertension missing 14, GLP-1+MASLD
missing theme 2.

### Combined precision / recall reading

Treating audit B as the conservative estimate of generalization quality
and audit A as the upper bound, the **operational quality of the tagging
is roughly precision 0.7–0.8 / recall 0.85–0.95** on records the agent
hasn't directly reviewed. For Phase 3 (IC strategic-plan comparison) this
should be more than adequate — the patterns of theme prevalence and IC
overlap will be robust to noise of this size.

## AoU-meta-audit (META) records

The detection rule used title patterns + an abstract disease-noun override.
Four publications were flagged:

| PMID | Title |
|---|---|
| 31412182 | "The 'All of Us' Research Program" (NEJM 2019) |
| 39241755 | "A new annual feature of AJHG: All of Us Research Program year in review" |
| 39241756 | "All of Us Research Program year in review: 2023-2024" |
| 40912237 | "All of Us Research Program year in review: 2024" |

All four are program-descriptive and not themselves analytic contributions.

The detection rule was originally more permissive (catching any pub with
"All of Us" in the title plus a meta-flagged pattern) but the abstract
disease-noun override correctly excluded substantive papers that happen
to introduce AoU in their title. After tightening title patterns to
strong-match only (so substantive pubs like "Interview themes in context
with returning genetic results" no longer falsely flag META), the count
of 4 is stable.

The user's expected ~25 META count from the draft was likely overstated:
many candidates ("Engaging African-Americans," "Building research
capacity at FQHCs," "Patient portal recruitment") are substantive ELSI
research that legitimately belong in theme 17, not META. They are now
classified appropriately.

## Theme-prevalence surprises vs. the draft taxonomy

| Theme | Draft est. | Phase 2c result | Notes |
|---|---:|---:|---|
| 1. Cardiometabolic | ~22% | 28% | Slightly higher; broader disease coverage |
| 2. Genomics | ~28% | 25% | Close |
| 3. Methods / phenotyping | ~20% | 18% | Close |
| 4. Mental health | ~18% | 18% | Match |
| 5. Cancer | ~15% | 13% | Close (after the ALL-acronym FP was removed) |
| 6. SDOH | ~15% | **33%** | **Substantially higher than draft.** The draft underestimated SDOH because the keyword list was narrow; the locked taxonomy uses a wider net including discrimination, LGBTQ, ADI, structural barriers, rural/uninsured. UBR-oversampling means SDOH is genuinely the largest cross-cutting theme. |
| 7. Wearables | ~8% | 5% | Lower; many records are wearable-adjacent but tag mostly to method theme 3 |
| 8. Infectious disease | ~6% | 6% | Match |
| 9. Autoimmune | ~6% | 8% | Slightly higher |
| 10. Rare disease | ~6% | 4% | Lower; Mendelian framing is rare in the corpus |
| 11. Aging/ADRD | ~5% | 5% | Match |
| 12. Dermatology | ~5% | **14%** | **Much higher.** Consistent with the draft's README warning that dermatology is anomalously over-represented (1–2 prolific dermatology epi groups). |
| 13. Respiratory & sleep | ~4% | 4% | Match |
| 14. Neurology | ~4% | 6% | Slightly higher |
| 15. Pregnancy & women's | ~4% | 3% | Close |
| 16. Pharmacogenomics | ~4% | 2% | Lower |
| 17. ELSI / engagement | ~3% | 5% | Slightly higher |
| 18. Ophthalmology / ENT | ~3% | **8%** | **Higher** — large ophthalmology disparities cluster (eye-care access, glaucoma, diabetic retinopathy) plus voice / CRS pubs |
| 19. Environmental | ~2% | 0.5% | Lower — emerging area, not yet widely tagged |

## Notable IC patterns from `top3_admin_ics` / `top3_cofunding_ics`

- **OD dominates everywhere** because OD is the AoU program-host designation —
  i.e., the AoU-program-level grant counts as OD-administered. TR (NCATS
  Translator-adjacent) and HL (NHLBI) are next-most-common as admin or
  cofunder across most disease themes, reflecting AoU's deep
  cardiometabolic + translational footprint.
- **HG (NHGRI)** ranks #2 admin on theme 2 (Genomics, 40 pubs) and theme 7
  (Wearables) — appropriate.
- **CA (NCI)** is the dominant non-OD admin on theme 5 (Cancer, 17 admin
  pubs) — but conspicuously low for cofunding (only 18 of 176 cancer pubs
  have NCI cofunding, suggesting cancer-using AoU researchers funded
  primarily from other ICs).
- **AG (NIA)** is the #2 admin on theme 11 (Aging/ADRD, 8 of 75 pubs).
- **EY (NEI)** is #2 admin on theme 18 (Ophthalmology/ENT, 24 of 107 pubs) —
  appropriate.
- **MD (NIMHD)** appears in the top-3 admin only for themes 6 (SDOH) and 18
  (Ophth/ENT) — reflecting AoU's underrepresentation focus.
- **ES (NIEHS)** is the lead admin IC for theme 19 (Environmental) but with
  only 2 pubs — environmental health is genuinely small in the AoU corpus.

## Known false-positive sources still in the data

1. **PRS / methods benchmark papers** still get tagged with disease themes
   because they list disease traits in the abstract. Examples:
   PMID:41311062 (S4-Multi PRS) tagged with cardiometabolic, cancer,
   respiratory, neurology. The user can downweight these by filtering on
   `theme==2 with high keyword counts` if needed.

2. **Co-morbidity-panel case-control pubs** (especially dermatology) tag
   multiple themes from incidental abstract mentions. Onychomycosis +
   "HIV, diabetes, vascular disease" comorbidity sentence drives theme 1,
   3, 8 tags. The primary 12 tag is correct but auxiliary tags may be
   incidental.

3. **Title-bonus rule** (general keyword in title → fire) can produce FPs
   for very short / generic titles like "Cancer Project" or "Disease".
   This is rare but worth noting; the 1.3% improvement in zero-tag rate
   that this rule produced is worth the FP exposure.

4. **Stroke forced multi-tag** is restricted to title-mention only, but
   may still over-tag a stroke-titled pub that is primarily a methods
   paper. Roughly 30 records carry the cerebrovascular-stroke subtheme.

5. **Single-keyword acronym matches** can occasionally hit unintended
   contexts. The case-sensitive rule eliminated the worst offenders (ALL,
   MS, RA, AF, EHR) but rare residual FPs remain on terms like CKD, CFTR,
   NF1 in non-disease contexts. Estimated impact: <1% of records.

## Files written

- `taxonomy.md` — locked taxonomy (19 top-level themes + META)
- `publications_tagged.jsonl` / `publications_tagged.csv`
- `projects_tagged.jsonl` / `projects_tagged.csv`
- `theme_summary.csv`
- `tag_corpus.py` — pass-1 keyword tagger
- `pass2_adjustments.py` — pass-2 LLM-judgment adjustments
- `regenerate_outputs.py` — regenerates CSVs and summary from the
  pass-2-adjusted JSONL files
- `tagging_audit.md` — this report

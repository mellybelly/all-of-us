# Deliverables — editor's guide

Handoff package for the AoU Scientific Roadmap Refresh. The corpus is **frozen**
(2026-07-02) and all numbers are **reconciled** across every document, so these
are ready for human editing. Start here.

## Canonical deliverables (edit these)

| Deliverable | Files | Format | Notes |
| --- | --- | --- | --- |
| **Executive summary** | `executive_summary.html` → `AoU_Roadmap_Refresh_Executive_Summary.pdf` | HTML (source) → PDF | ~2 pp, leadership-facing (AoU CEO / NIH). Edit the HTML, then regenerate the PDF. |
| **Slide deck** | `AoU_Roadmap_Refresh_Draft_Deck.pptx` (built by `build_deck.py`) | PPTX | 21 slides. Rebuilt from the script — **edit `build_deck.py`, not the PPTX directly**, or your edits are lost on rebuild. |
| **Data-types list** | `data_types_inventory.html` → `AoU_Data_Types_Inventory.pdf` | HTML → PDF | AoU data modalities + peer gaps + build effort. Edit HTML, regenerate PDF. |
| **Methods documentation** | `methods_documentation.md` | Markdown | End-to-end methods for defensibility. Edit directly. |

## How to regenerate after edits

```bash
# Deck (after editing build_deck.py):
python3 build_deck.py

# PDFs from HTML (headless Chrome):
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --no-pdf-header-footer \
  --print-to-pdf=AoU_Roadmap_Refresh_Executive_Summary.pdf "file://$PWD/executive_summary.html"
"$CHROME" --headless --no-pdf-header-footer \
  --print-to-pdf=AoU_Data_Types_Inventory.pdf "file://$PWD/data_types_inventory.html"
```
(PDFs are currently produced with headless Chrome; any HTML→PDF tool is fine.)

## Editorial conventions already applied (please preserve)

- **Working groups are "need areas," not decision bodies.** The 2026 WGs are
  topics already recognized as program needs; they do not vote/lead/discuss/fund.
  Recommendations are stated as recommendations; areas overlap and coordinate.
- **The current 8 focus areas are listed for reference** in the exec summary,
  the deck (focus-areas slide), and `../phase4-recommendations/wg1_roadmap_refresh.md`.
- **Leadership register** in the exec summary (no internal shorthand like
  "orphan"/"slide-7"/rubric codes in prose).
- **Dermatology is deliberately de-emphasized** (a minor, non-load-bearing
  outlier), not a strategic priority.
- **Priority scores** (of 4) come from the Committee's 8-criterion rubric.

## Supporting evidence (reference, not primary edit targets)

The recommendations trace to these analysis modules (see `methods_documentation.md`):

| Module | Directory | Status |
| --- | --- | --- |
| Corpus + tagging | `../aou-research-landscape/` | Current (frozen 2026-07-02) |
| Focus-area trends | `../aou-roadmap-refresh/` | Current |
| Peer biobanks | `../peer-biobanks/` | Current (full census) |
| Emerging-trends horizon scan | `../emerging-trends/` | Current |
| Researcher Workbench analysis | `../rw-analysis/` | Current (87/87 citations verified) |
| Recommendation briefs (per need area) | `../phase4-recommendations/` | Current |
| NIH-plan alignment | `../aou-ic-alignment/` | Cross-corpus figures updated; IC attribution not re-run (dated note — immaterial change) |
| Disease-burden context | `../disease-burden/` | Cross-corpus figures updated; dated note |

## Status snapshot

- Corpus: **1,432 publications**, **12,899 substantive workspaces** (frozen 2026-07-02).
- Peers: full PubMed censuses (UKB 11,868 · FinnGen 3,152 · MVP 438 · CKB 558).
- All figures reconciled across deck, exec summary, data-types, methods doc, and
  the supporting narratives.

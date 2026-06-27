# Researcher Workbench analysis

Evidence-based analysis of analytical methods, tools, deficiencies, and
opportunities for the All of Us Researcher Workbench (RW). All findings are
data-derived and verifiable; framing is descriptive, not editorial.

## Parts

1. **Capability & data-asset gaps vs comparator platforms** (AnVIL, BioData
   Catalyst, N3C, Kids First, UKB-RAP/DNAnexus, Terra) — *in progress*. First
   evidence in [`baa_llm_egress_evidence.md`](baa_llm_egress_evidence.md)
   (LLM tooling, data-egress models, BAA mechanics, comparator table).
2. **Trending methods not yet adopted** — DONE. See
   [`part2_trending_methods.md`](part2_trending_methods.md).
3. **Tools/artifacts the RW should build** — *planned* (synthesis of Parts 1 & 2).

## Part 2 pipeline

| Step | Script / input | Output |
| --- | --- | --- |
| Method topics | LLM induction over `../emerging-trends/topic_induction_digest.txt` | `methods_topics.json` (27 method topics) |
| Gap-check | `gap_check_methods.py` (vs AoU pubs + substantive workspaces + feasibility) | `methods_gap.{csv,json}` |
| Collaboration/reuse signals | `collaboration_evidence.py` | `collaboration_evidence.csv` |
| Report | — | `part2_trending_methods.md` |

## Reproduce

```bash
python3 gap_check_methods.py
python3 collaboration_evidence.py
```

Depends on the emerging-trends term data and the aou-research-landscape corpora
(publications + workspaces). No new raw pulls.

# Emerging research themes in peer biobanks — implications for AoU

> **Updated 2026-06-26** — peer corpora are now full PubMed censuses (UKB 11,868; FinnGen 3,152; MVP 438; CKB 558); tables regenerated accordingly.

**Phase 4 input for the 2026 AoU Scientific Roadmap Refresh WG (Smoller & Haendel)**

## TL;DR

Comparing All of Us's 1,428-pub substantive corpus against UK Biobank
(11,868 pubs, full name-search census), FinnGen (3,152), Million Veteran
Program (438), and China Kadoorie Biobank (558)
surfaces a consistent signal: **AoU is materially under-indexed on
multi-omics-beyond-genomics, imaging-anchored analyses, nutrition /
microbiome, and rare-disease / Mendelian genetics.** These four areas
together touch roughly 30-40% of the peer corpora and under 5% of AoU's.
The gap on multi-omics, imaging, and microbiome reflects AoU's current
data scope (no proteomics or imaging release at AoU's tenure-comparable
phase); the gap on rare-disease / Mendelian work is more recruitment-
and design-driven. AoU is correspondingly **over-indexed on SDOH /
disparities (5× peer median), ELSI / engagement, dermatology, and
methods-infrastructure pubs** — defensible distinctive contributions
that should be preserved. These signals come from a same-tagger
keyword-only comparison and should be read against the caveats below
before acting on any single number.

## Top 5 emerging-but-AoU-thin themes

Ranked by a combination of (1) consistent peer growth or large peer
share, and (2) substantial AoU gap. Multi-omics, imaging, and nutrition
are reported from the 8 hot-area detectors (HA1, HA3, HA7) — these
detectors are run on the same title+abstract regexes used in AoU
Phase 3b, so the comparison is apples-to-apples.

### 1. Multi-omics beyond genomics (proteomics / metabolomics / transcriptomics) — HA1

| Cohort | Overall share | Pre-2023 share | Post-2023 share | Trend |
|---|---:|---:|---:|---:|
| AoU | 1.7% | 0.6% | 1.8% | +0.012 |
| UKB | 10.1% | 5.2% | 12.2% | +0.070 |
| FinnGen | 18.5% | 7.1% | 19.3% | +0.122 |
| MVP | 10.3% | 10.4% | 10.2% | -0.001 |
| CKB | 3.9% | 2.2% | 6.2% | +0.040 |

This is the single largest growth differential in the analysis. The
2018 UKB Olink + 2023 UKB-PPP proteomics releases drove UKB's 12.2%
post-2023 share; FinnGen's high share reflects integration with Olink
and metabolomics platforms. AoU has no proteomics or metabolomics data
release; this is a data-availability gap, not a researcher-base gap.
**Suggestion to Roadmap Refresh WG:** treat a proteomics data release
(an Olink-scale or SomaScan release) as a near-term Refresh priority;
without one, AoU will fall progressively further behind on this
fastest-growing peer-cohort research stream.

### 2. Imaging / radiomics — HA3

| Cohort | Overall share | Trend |
|---|---:|---:|
| AoU | 0.6% | +0.006 |
| UKB | 8.0% | +0.000 |
| FinnGen | 1.1% | -0.003 |
| MVP | 1.6% | +0.012 |
| CKB | 1.6% | +0.001 |

The UKB gap on imaging is structural: UKB released ~100k MRI brain /
heart / abdomen scans starting 2014, with the full dataset reaching
the field in 2017-2020. AoU has no imaging-data release at this point
in its tenure. **Caveat (per spec):** do not over-index on this signal —
it is mostly a UKB-specific endowment effect, not a fast-growing
field-wide signal. The other three peers all sit at 1-2% and the trend
is essentially flat. The UKB volume is real but the question for AoU
isn't "match UKB" — it's "is imaging on the medium-term roadmap or
not." Worth a WG discussion.

### 3. Nutrition / microbiome — HA7

| Cohort | Overall share | Pre-2023 share | Post-2023 share | Trend |
|---|---:|---:|---:|---:|
| AoU | 0.8% | 0.6% | 0.8% | +0.002 |
| UKB | 10.0% | 7.1% | 11.3% | +0.042 |
| FinnGen | 14.1% | 7.1% | 14.6% | +0.075 |
| MVP | 5.5% | 5.9% | 5.3% | -0.006 |
| CKB | 11.1% | 11.4% | 10.7% | -0.006 |

A genuinely-emerging-in-the-field signal: UKB and FinnGen both up
~50-100% post-2023. AoU's diet-and-nutrition footprint is unusually
thin compared to peers — partly because AoU's dietary surveys are
limited compared to UKB's 24-hour recall instruments, partly because
the AoU researcher base has tilted to SDOH/disparities and EHR
phenotyping rather than nutritional epidemiology. **Suggestion:**
either expand dietary-survey instruments (UKB's 24-hour recall model
is the field default) or flag nutrition as an explicitly-de-prioritized
area so the WG isn't surprised when peer-cohort pubs in this area
continue to outpace AoU's. Microbiome specifically requires sample
collection; no near-term path on AoU at current scope.

### 4. Rare disease & Mendelian genetics (Theme 10)

| Cohort | Overall share | Pre-2023 share | Post-2023 share | Trend |
|---|---:|---:|---:|---:|
| AoU | 3.8% | 2.5% | 3.9% | +0.014 |
| UKB | 17.7% | 16.7% | 18.1% | +0.014 |
| FinnGen | 72.6% | 64.9% | 73.2% | +0.083 |
| MVP | 13.0% | 9.6% | 14.5% | +0.049 |
| CKB | (rare-disease keywords sparse, ~3%) | | | |

Across UKB / FinnGen / MVP, rare-disease / Mendelian work is growing
sharply and AoU is roughly 4-5× under-indexed at the peer-median.
FinnGen's outsized share (73%) reflects the Finnish founder-population
design — that is not a directly-actionable comparison for AoU. But UKB
(17%) and MVP (13%) suggest the rare-disease space is a viable
biobank-scale research area regardless of population isolate.
**Hypothesis for the gap:** AoU's WGS release (~250k v7 / ~315k v8) is
substantial, but the rare-disease analysis community has not migrated
to AoU at the rate that UKB and MVP have seen. This may be (a) timing
(UKB's WES was 2020), (b) AoU's recall-of-results channel for ACMG
findings, or (c) researcher-base lock-in to UKB's analysis platform
(DNA Nexus + downstream pipelines). **Suggestion:** the WG should
investigate whether the rare-disease researcher base has tried-and-not-
returned vs. has-not-yet-tried, since the implications differ
(usability problem vs. outreach problem).

### 5. Aging / ADRD (Theme 11)

| Cohort | Overall share | Pre-2023 share | Post-2023 share | Trend |
|---|---:|---:|---:|---:|
| AoU | 5.5% | 1.3% | 6.0% | +0.047 |
| UKB | 15.7% | 10.9% | 17.8% | +0.069 |
| FinnGen | 6.4% | 9.3% | 6.2% | -0.032 |
| MVP | 5.9% | 2.2% | 7.6% | +0.054 |
| CKB | 6.6% | 4.4% | 9.5% | +0.051 |

UKB, MVP, and CKB are all post-2023-growing on aging / ADRD; AoU is
now growing too (6.0% post-2023, near the peer median) but still trails UKB. Lecanemab / donanemab approvals (2023-2024) and the
disease-modifying-AD-therapy era have driven enormous renewed
biobank-scale aging-cohort work, and AoU is structurally well-positioned
(EHR / consent / diversity) and the gap is now narrowing. **Suggestion:** an
NIA-anchored aging-cohort engagement workstream (or a Refresh focus
area dedicated to aging-trajectory analyses) would close a real gap
given the field's post-2023 shift.

## Top 5 themes where AoU leads the peer set (defensive evidence)

These are themes where AoU's share is materially higher than the peer
median — AoU's distinctive contribution that the Refresh should
preserve / reinforce in the forward roadmap.

| Theme | AoU share | Peer median | Index | Notes |
|---|---:|---:|---:|---|
| 17 ELSI, participant engagement & recruitment | 4.9% | 0.2% | 26.3× | AoU's unique program-meta + community-engagement work; expected lead |
| 12 Dermatology | 13.9% | 2.0% | 6.9× | Driven by 1-2 prolific groups (see Phase 1 README); not a strategic priority but a real corpus feature |
| 6 SDOH / disparities | 32.9% | 6.5% | 5.1× | AoU's UBR-oversampling structurally enables this; defining feature of the cohort |
| 16 Pharmacogenomics | 2.4% | 0.5% | 4.6× | Modest but meaningfully higher than peers |
| 3 Methods / infrastructure / phenotyping | 18.4% | 6.1% | 3.0× | Workbench-tooling + phecode-curation pubs; AoU-specific researcher base |

SDOH (5×) and ELSI / engagement (26×) are the clearest "AoU's
distinctive contribution" lines for the Refresh narrative. Dermatology
is included as a defensive observation rather than a strategic
priority — the 6.9× over-index is largely two prolific groups (per
the AoU landscape README).

## Caveats the WG should know

1. **PubMed-name-search fallback was used for all four peer
   biobanks.** Official curated publication lists from each biobank's
   website were not pulled (10-min-per-biobank fallback rule). PubMed
   name-search over-includes pubs that mention the biobank name in
   title/abstract even when the data isn't primary, and under-includes
   pubs that use the data but don't mention the name. Comparisons are
   internally consistent (same heuristic across all peers) but
   absolute counts should not be treated as authoritative.
2. **UKB is a full census pulled via year windows** (uncapped) to work
   around NCBI's ~9,999-per-WebEnv esearch limit on a single all-years
   query. The 11,868 UKB pubs are the complete name-search corpus (~14
   short of the ~11,882 universe, pre-2007 pubs outside the windows), so
   the UKB year distribution now reflects actual publication volume.
3. **MVP's 426-pub corpus is small.** PubMed name-search for MVP is
   known to undercount; the VA-maintained list is likely 2-3× larger.
   The signals from MVP are therefore noisier than from UKB / FinnGen.
   Treat single-MVP-only signals with caution; use only when reinforced
   by another peer.
4. **AoU corpus tenure is shorter than UKB / CKB.** UKB pubs go back
   to 2007; AoU pubs really get going 2020+. The pre-2023 / post-2023
   trend comparison favors AoU because AoU's pre-2023 baseline is small
   (157 pubs) — almost any post-2023 theme will trend positive in AoU.
   For this reason, the **static share index** (`aou_vs_peers_index.csv`)
   is more reliable than the trend differential
   (`emerging_in_peers.csv`) for action-relevant comparisons.
5. **FinnGen's 97% genomics share is not a meaningful "AoU under-indexed
   on genomics" signal.** FinnGen IS a genomics consortium — virtually
   all FinnGen pubs are GWAS-anchored by design. The peer-median is a
   better reference than the peer-max for genomics specifically.
6. **CKB's heavy cardio focus (66% of pubs) reflects the consortium's
   founding mission** (cardiovascular epidemiology in a 500k Chinese
   cohort). Same caveat: cardio-share isn't an AoU-specific signal,
   it's a peer-baseline difference.
7. **Same-tagger comparability is the main strength of this analysis.**
   The taxonomy keyword set was tuned for AoU title+abstract text; peer
   abstracts may use slightly different language, so peer
   theme-detection precision is probably 5-10% lower than the AoU
   pass-2-audited corpus. This affects absolute numbers but not the
   directional comparisons that drive the recommendations above.

## Do not over-index on

- **The UKB imaging share (HA3 = 8.1%).** That reflects a one-time
  2014-2020 imaging release. UKB-imaging-volume is structural, not a
  field-wide growth signal. Multi-omics, by contrast, IS a field-wide
  signal — UKB, FinnGen, and CKB all show post-2023 growth there.
- **FinnGen's 73% rare-disease share.** Founder-population structural
  feature. The relevant signal is UKB (17%) + MVP (13%), which AoU
  could plausibly approach with the existing genomic-data release.
- **AoU's apparent "growth" on cardiometabolic / mental health /
  cancer.** Almost certainly a small-baseline artifact (AoU pre-2023
  had only 157 pubs; any active theme will look growing in the
  post-2023 split). Read these as "AoU has built a presence here," not
  "AoU is uniquely outpacing the field."

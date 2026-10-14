# Where All of Us is under-represented vs. peer biobanks/cohorts

> **Created 2026-10-14.** Five research areas where AoU's published output is
> *under-indexed* relative to the median of four peer cohorts — UK Biobank (UKB),
> FinnGen, Million Veteran Program (MVP), and China Kadoorie Biobank (CKB). Basis:
> theme-share of each cohort's substantive publication corpus (AoU 1,653 · UKB
> 12,986 · FinnGen 3,376 · MVP 501 · CKB 588), tagged against the locked 19-theme
> taxonomy. Source tables: [`aou_vs_peers_index.csv`](aou_vs_peers_index.csv),
> [`theme_share_by_biobank.csv`](theme_share_by_biobank.csv).

## Method & how to read the index

For each theme, **index = AoU theme-share ÷ peer-median theme-share.** Index < 1
means the theme is a smaller fraction of AoU's literature than of the typical peer;
**< 0.5 = materially under-represented** (AoU produces proportionally less than half
the peer norm). Shares are of each cohort's *own* corpus, so this measures **relative
emphasis**, not absolute volume, and is independent of AoU's smaller corpus size.

Crucially, under-indexing is not automatically a *deficiency*: some is **by design**
(a peer's founder-population or recruitment design inflates its share) and some is a
**genuine, addressable gap**. Each area below is labeled accordingly.

## The five under-represented areas (ranked by severity)

| # | Theme | AoU share | Peer median | Peer max (cohort) | Index | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | **Rare disease & Mendelian genetics** | 3.75% | 15.02% | 72.25% (FinnGen) | **0.25** | Partly by-design, partly gap |
| 2 | **Environmental health & climate** | 0.60% | 1.72% | 2.89% (UKB) | **0.35** | **Genuine addressable gap** |
| 3 | **Genomics methods & complex-trait genetics** | 25.77% | 61.68% | 97.13% (FinnGen) | **0.42** | Largely by-design + maturity |
| 4 | **Neurology (non-ADRD)** | 6.11% | 13.20% | 29.93% (CKB) | **0.46** | Mixed — emerging gap |
| 5 | **Respiratory & sleep medicine** | 4.17% | 7.85% | 11.39% (CKB) | **0.53** | Modest gap |

### 1. Rare disease & Mendelian genetics — index 0.25 (most under-indexed)
- **AoU 3.75% vs. FinnGen 72.25%, UKB 17.06%, MVP 12.97%, CKB 3.57%.**
- **Why:** FinnGen is a *founder-population isolate* purpose-built for Mendelian and
  rare-variant discovery — its share is structurally enormous and not a fair target.
  But UKB (17%) and MVP (13%) show the realistic ceiling, and AoU sits well below it.
- **Read — partly by-design, partly gap.** AoU's short+long-read WGS on a diverse
  cohort is ideally suited to rare-disease discovery, yet its literature barely uses
  it. This is the clearest *addressable* rare-disease opportunity in the set and
  aligns with the roadmap's rare-disease focus and long-read assets.

### 2. Environmental health & climate — index 0.35 (genuine gap)
- **AoU 0.60% vs. UKB 2.89%, CKB 2.72%, FinnGen 0.71%, MVP 0%.**
- **Why:** AoU has geocoded addresses and is building environmental linkages, but the
  published output is near-absent. UKB's environmental/exposure literature shows what
  a linked cohort can produce.
- **Read — genuine, addressable gap, and already being closed.** AoU's **Environmental
  Health & Exposomics** partnered study (NIEHS; 5,500+ samples assayed for exposures ×
  genomic/behavioral factors) directly targets this gap — 399 workspaces already carry
  environmental-exposure intent (196 newly visible in the 2026-10-14 pull). The
  publications will lag the workspaces; the roadmap should credit this trajectory.

### 3. Genomics methods & complex-trait genetics — index 0.42 (largely by-design)
- **AoU 25.77% vs. FinnGen 97.13%, MVP 72.65%, UKB 50.70%, CKB 13.78%.**
- **Why:** FinnGen and MVP are, in effect, *GWAS factories* — near their entire output
  is complex-trait genetics. AoU is deliberately broader (it is the only cohort where
  SDOH is 33% and methods/phenotyping 19% of output), so a lower genetics *share* is
  partly a denominator effect, not a deficit in genetics volume.
- **Read — mostly by-design, with a maturity component.** AoU's genomic data matured
  later than UKB/FinnGen; GWAS/PheWAS output is rising. Watch the trajectory rather
  than treat 0.42 as a standing deficiency — but note AoU is still below even UKB's
  50%, so there is room.

### 4. Neurology (non-ADRD) — index 0.46 (emerging gap)
- **AoU 6.11% vs. CKB 29.93%, MVP 14.57%, UKB 11.84%, FinnGen 9.60%.**
- **Why:** CKB's stroke-heavy design and MVP's veteran neurology inflate peers. But
  every peer out-indexes AoU, so the under-emphasis is broad-based, not one-cohort.
- **Read — mixed/emerging gap.** AoU's EHR + imaging roadmap and the **Exploring the
  Mind** (cognition/behavior) and **Eyes on Health** (eye→neurological disease)
  ancillary studies create a path to close it; cognition/mental-health workspaces are
  already 13% of the registry. Flag as a watch-and-build area.

### 5. Respiratory & sleep medicine — index 0.53 (modest gap)
- **AoU 4.17% vs. CKB 11.39%, FinnGen 9.36%, UKB 6.34%, MVP 3.59%.**
- **Why:** The nearest-the-threshold area; AoU is comparable to MVP but below UKB/CKB.
- **Read — modest, lower-priority gap.** Wearable + EHR assets (sleep from Fitbit)
  make this feasible, but it is the least severe of the five. Opportunistic, not
  structural.

## Synthesis — which gaps the roadmap should act on

- **Act now (addressable, high-value):** *Environmental health* (already being closed
  by the Exposomics ancillary study) and *Rare disease & Mendelian genetics* (AoU's
  diverse long-read WGS is an unmatched substrate the literature isn't yet using).
- **Watch the trajectory (largely by-design / maturing):** *Genomics methods* and
  *Neurology* — the share gap partly reflects AoU's deliberate breadth and younger
  genomic data; both are rising and are supported by ancillary studies.
- **Opportunistic:** *Respiratory & sleep* — feasible via wearables+EHR, lowest priority.

> **Caveat.** This is a *relative-emphasis* measure on tagged publication corpora;
> peer shares are inflated by each cohort's recruitment/design (FinnGen rare-disease &
> genetics; CKB neurology/respiratory; MVP veteran psychiatry/neurology). It does not
> measure data availability or absolute output, and (like all our publication-based
> views) it lags released data — the ancillary-study workspace signal is the forward
> indicator. For AoU's *over*-indexed distinctive strengths (SDOH 5.4×, ELSI 24×,
> dermatology 6.4×, pharmacogenomics 4.3×) see `comparison.md` / `aou_vs_peers_index.csv`.

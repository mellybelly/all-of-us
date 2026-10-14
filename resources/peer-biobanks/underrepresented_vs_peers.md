# Where All of Us lags peer biobanks/cohorts — the five areas

> **Created 2026-10-14; realigned to the Science Committee's framing (Roadmap Refresh
> WG, 2026-10-14).** The committee identified **five areas where All of Us lags peer
> cohorts despite having comparable data: imaging, multi-omics, aging research, rare
> disease, and environmental/social data.** This report backs each with the
> quantitative evidence from our analysis. Peer set: UK Biobank (UKB), FinnGen,
> Million Veteran Program (MVP), China Kadoorie Biobank (CKB). Two complementary lenses
> are used: **publication theme-share** (each cohort's own corpus, tagged against the
> 19-theme taxonomy — `aou_vs_peers_index.csv`) for research-area gaps, and
> **data-modality availability** (`../deliverables/data_types_inventory.html`) for
> modality gaps. Corpus sizes: AoU 1,653 · UKB 12,986 · FinnGen 3,376 · MVP 501 · CKB 588.

## How to read it
Where a gap is a **research area**, we report the **theme-share index** = AoU share ÷
peer-median share (<1 = AoU under-emphasizes it; <0.5 = materially under). Where a gap
is a **data modality** (imaging, multi-omics, environmental linkage), publication
theme-share understates it because the modality isn't a taxonomy theme — there we report
the **data-availability gap** vs peers. Several gaps have **remedies already in motion**
(ancillary studies, the 10k multi-omics project, the Nov 2 environmental release).

## The five areas

### 1. Imaging  *(data-modality gap)*
- **Evidence:** AoU has ~8 imaging publications total; UKB imaging is ~8.1% of its
  corpus structurally. UKB's research-purpose imaging reached ~100,000 images by
  end-2025 and ~1,300 publications — the productivity benchmark.
- **Why AoU lags:** a **data-supply** problem, compounded by **compute/cost** (large
  files, cloud-only compute, no institutional-HPC equivalent — WG discussion 2026-10-14)
  and the low yield of legacy/opportunistic scans (much legacy neuroimaging is unusable).
- **Remedy in motion / recommended:** research-purpose, QA-harmonized acquisition with
  partners (**RSNA, MIDRC**), an incidental-findings policy, imaging statistical
  expertise upfront, and a hybrid/federated compute model for the file/cost burden.

### 2. Multi-omics  *(data-modality gap)*
- **Evidence:** plasma proteomics is the largest peer-comparative modality gap — UKB
  ~13.5% (post-2023, UKB-PPP) vs **AoU 2.1%**; UKB has NMR metabolomics on ~120k;
  stool→metagenomics AoU ~0.8% vs peer median ~11.1%.
- **Why AoU lags:** these assays were not generated at scale early; genomics matured
  first.
- **Remedy in motion:** the AoU **Multi-Omics Working Group** is now generating
  **RNA-seq + Olink Explorer HT proteomics + PacBio long-read WGS on ~10,000 diverse
  participants, scaling toward ~50,000** — on a diversity substrate no peer matches.
  Supports renaming FA8 to "Genetics, Multi-omics & Biology."

### 3. Aging research  *(research-area gap)*
- **Evidence:** theme "Aging, frailty & ADRD" — **AoU 5.7% vs peer median 7.1%
  (index 0.80); UKB 15.9%** is the outlier that AoU trails most.
- **Why AoU lags:** a younger/earlier cohort and no dedicated aging-imaging/biomarker
  program at UKB's scale (AoU is 4× under-indexed on aging/ADRD in the data-types view).
- **Remedy / recommended:** EHR + biomarker + wearable aging phenotypes; the
  **Exploring the Mind** ancillary (objective cognition) and **Eyes on Health**
  (eye→neurological disease) create a path; cellular-senescence bench biology stays
  out of scope.

### 4. Rare disease & Mendelian genetics  *(research-area gap — most under-indexed)*
- **Evidence:** **AoU 3.75% vs peer median 15.02%, index 0.25** (FinnGen 72.25%,
  UKB 17.06%, MVP 12.97%). FinnGen's founder-population design inflates its share, but
  UKB/MVP show the realistic ceiling AoU sits well below.
- **Why AoU lags:** its diverse long-read WGS substrate is ideal for rare-disease
  discovery but the literature barely uses it yet.
- **Remedy in motion:** the **Long Read Analysis (Phase 1 + 2)** program and the
  committee's **driver-paper model** — explicitly proposed for **rare-disease and
  intersectional (rare disease + rurality) driver papers** — target this directly. The
  clearest *addressable* gap in the set.

### 5. Environmental / social data  *(data-modality gap — remedy imminent)*
- **Evidence:** environmental-health theme **AoU 0.60% vs peer median 1.72% (index
  0.35); UKB 2.89%.** NIEHS strategic priorities vastly outnumber AoU's ~7 substantive
  environmental publications.
- **Why AoU lags:** residential history is collected, but the linked environmental/
  social data layer and releases lagged.
- **Remedy in motion:** the **November 2, 2026 release** of the environmental dataset
  (geocoded residential history + linked social/environmental variables) is the major
  upcoming milestone closing this gap, alongside the **Environmental Health & Exposomics**
  ancillary study (5,500+ samples; 399 workspaces, 196 newly visible).

## Secondary lens — publication-emphasis (theme-share) ranking
Ranking *solely* by publication theme-share surfaces a partly different set, useful as a
complementary view: rare disease (0.25), environmental health (0.35), genomics-methods/
complex-trait genetics (0.42), neurology non-ADRD (0.46), respiratory & sleep (0.53).
Rare disease and environmental health appear in **both** lenses (strongest signals);
genomics-methods' low share is largely **by design** (AoU is deliberately broader —
SDOH 33%, methods 19% of output — so genetics is a smaller fraction, not a deficit in
volume), and the committee's imaging/multi-omics/aging gaps are **modality/area** gaps
that theme-share understates. Both lenses agree on the actionable priorities.

## Synthesis — priorities
- **Remedy already in motion:** environmental/social (Nov 2 release + Exposomics),
  multi-omics (10k project), rare disease (long-read + driver papers). Credit the
  trajectory in the roadmap.
- **Harder / needs investment:** imaging (data-supply + compute/cost — needs partners
  and a compute model), aging research (needs dedicated phenotyping).

> **Caveats.** Theme-share is relative emphasis on tagged corpora; peer shares are
> inflated by each cohort's recruitment design (FinnGen rare-disease/genetics; UKB
> aging/imaging; CKB neurology). Data-modality gaps reflect availability, not demand.
> All publication-based views lag released data — the ancillary-study/workspace signal
> and the committee's milestone calendar (Nov 2 environmental release) are the forward
> indicators. For AoU's *over*-indexed strengths (SDOH 5.4×, ELSI 24×, dermatology
> 6.4×, PGx 4.3×) see `comparison.md` / `aou_vs_peers_index.csv`.

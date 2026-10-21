# Cluster C — §4 Emerging scientific frontiers (verified seed citations)

Scope: leading-edge methods/topics in the biomedical literature that a national cohort (All of Us) should consider. Every entry below was verified against a real source (PubMed/PMC, publisher, resolvable DOI, or arXiv/bioRxiv) — title, first author, and year confirmed. Preprints are tagged `[preprint]`.

### §4.1 AI foundation models in medicine & health (LLMs, clinical & agentic AI)

- [Moor et al. Foundation models for generalist medical AI. Nature 2023](https://pubmed.ncbi.nlm.nih.gov/37045921/) — Defines "generalist medical AI": self-supervised, multimodal foundation models as a new paradigm for medicine; the conceptual anchor for the frontier.
- [Singhal et al. Large language models encode clinical knowledge. Nature 2023](https://pubmed.ncbi.nlm.nih.gov/37438534/) — Med-PaLM / MultiMedQA; landmark showing instruction-tuned LLMs reach near-expert medical QA, with a human-evaluation framework for safety.
- [Nori et al. Capabilities of GPT-4 on Medical Challenge Problems. arXiv 2023](https://arxiv.org/abs/2303.13375) `[preprint]` — General-purpose GPT-4 exceeds USMLE passing score with no medical fine-tuning; evidence that frontier LLMs generalize to clinical reasoning.
- [Kung et al. Performance of ChatGPT on USMLE. PLOS Digital Health 2023](https://doi.org/10.1371/journal.pdig.0000198) — Early, widely cited demonstration that an LLM performs at/near USMLE passing threshold; catalyzed clinical-LLM interest.
- [Tu et al. Towards conversational diagnostic artificial intelligence. Nature 2025](https://doi.org/10.1038/s41586-025-08866-7) — AMIE: an LLM diagnostic-dialogue agent that outperformed primary-care physicians across most evaluation axes in a randomized study; frontier of agentic clinical AI.
- [Mehandru et al. Evaluating large language models as agents in the clinic. npj Digital Medicine 2024](https://www.nature.com/articles/s41746-024-01083-y) — Argues LLM *agents* must be judged by workflow impact in simulated clinics ("AI-SCE"), not exam benchmarks; frames evaluation needs for agentic AI.

### §4.2 Genomic / DNA sequence foundation models

- [Dalla-Torre et al. Nucleotide Transformer: robust foundation models for human genomics. Nature Methods 2025](https://doi.org/10.1038/s41592-024-02523-z) — 50M–2.5B-parameter DNA language models over 3,202 human + 850 species genomes; benchmark-setting genomic foundation model family.
- [Ji et al. DNABERT: pre-trained Bidirectional Encoder Representations from Transformers for DNA-language. Bioinformatics 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC11025658) — Foundational transformer for genomic sequence; established the DNA-as-language pretraining approach now standard in the field.
- [Nguyen et al. Sequence modeling and design from molecular to genome scale with Evo. Science 2024](https://doi.org/10.1126/science.ado9336) — 7B-parameter genomic model with 131k-token context; zero-shot function prediction and generative design across DNA/RNA/protein.
- [Brixi et al. Genome modeling and design across all domains of life with Evo 2. bioRxiv 2025](https://doi.org/10.1101/2025.02.18.638918) `[preprint]` — 7B/40B model, 1Mb context, 9.3T bp across all domains of life; variant-effect prediction (incl. BRCA1) without task-specific fine-tuning.

### §4.3 Multimodal modeling & data integration

- [Acosta et al. Multimodal biomedical AI. Nature Medicine 2022](https://doi.org/10.1038/s41591-022-01981-2) — Review mapping how biobank, EHR, imaging, biosensor, and omics data can be fused by multimodal AI; directly relevant to a national cohort's integrated data.
- [Boehm et al. Harnessing multimodal data integration to advance precision oncology. Nature Reviews Cancer 2022](https://pubmed.ncbi.nlm.nih.gov/34663944/) — Perspective on integrating molecular, imaging, and clinical modalities; articulates the data-engineering and interoperability barriers to multimodal modeling.

### §4.4 MASLD/MASH disease-definition change

- [Rinella et al. A multisociety Delphi consensus statement on new fatty liver disease nomenclature. Hepatology 2023](https://doi.org/10.1097/HEP.0000000000000520) — The nomenclature change: NAFLD→MASLD, NASH→MASH, with cardiometabolic-criteria definition and MetALD category; redefines phenotyping for cohort studies.
- [Harrison et al. A Phase 3 Trial of Resmetirom in NASH with Liver Fibrosis (MAESTRO-NASH). N Engl J Med 2024](https://pubmed.ncbi.nlm.nih.gov/38324483/) — First phase-3 drug to meet NASH-resolution and fibrosis-improvement endpoints; marks MASH as an actionable, treatable disease entity.

### §4.5 Causal inference & target-trial emulation on EHR

- [Hernán & Robins. Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available. Am J Epidemiol 2016](https://pubmed.ncbi.nlm.nih.gov/26994063/) — The founding framework for target-trial emulation; the methodological anchor for causal inference on observational/EHR data.
- [Hubbard et al. Target Trial Emulation for Observational Studies — Potential and Pitfalls. N Engl J Med 2024](https://doi.org/10.1056/NEJMp2407586) — Recent perspective on strengths and biases (unmeasured confounding) of TTE on EHR/claims; design-discipline guidance for cohort analyses.

### §4.6 Frontiers needing assays AoU lacks ("partner, don't chase")

*Protein structure prediction*
- [Jumper et al. Highly accurate protein structure prediction with AlphaFold. Nature 2021](https://pubmed.ncbi.nlm.nih.gov/34265844/) — AlphaFold2: atomic-accuracy structure from sequence; Nobel-recognized frontier an EHR/genomic cohort should leverage, not reproduce.
- [Abramson et al. Accurate structure prediction of biomolecular interactions with AlphaFold 3. Nature 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11168924) — AlphaFold3 extends prediction to protein–ligand/nucleic-acid/antibody complexes; illustrates a specialized assay-driven capability to partner with.

*Single-cell & spatial omics*
- [Marx. Method of the Year 2020: spatially resolved transcriptomics. Nature Methods 2021](https://pubmed.ncbi.nlm.nih.gov/33408395/) — Flagship recognition of spatial transcriptomics; a tissue-assay frontier beyond a population cohort's current sample types.
- [Regev et al. The Human Cell Atlas. eLife 2017](https://doi.org/10.7554/eLife.27041) — Founding vision for a reference atlas of all human cell types; the single-cell reference effort AoU can align to rather than duplicate.
- [The Tabula Sapiens Consortium. The Tabula Sapiens: a multiple-organ, single-cell transcriptomic atlas of humans. Science 2022](https://pubmed.ncbi.nlm.nih.gov/35549404/) — ~500k cells across 24 tissues from shared donors; concrete single-cell atlas requiring tissue assays AoU does not collect.

### Caveats

- **Preprints (not peer-reviewed at verification):** Nori et al. (arXiv 2303.13375) and Brixi et al. Evo 2 (bioRxiv 2025.02.18.638918). Secondary coverage indicates Evo 2 was subsequently published in *Nature* (reported ~March 2026); the Nature version was not directly verified here — confirm and update the citation to the journal version before final submission.
- **Dual-journal nomenclature statement:** The Rinella et al. MASLD consensus was co-published in *Hepatology* (DOI above) and *Journal of Hepatology* 2023;79(6):1542–1556. Cite whichever the manuscript's reference style prefers; they are the same work.
- **Nucleotide Transformer** carries a 2023 bioRxiv preprint (10.1101/2023.01.11.523679); the citation above is to the peer-reviewed *Nature Methods* 2025 version (vol. 22:287–297).
- **Evo (Nguyen et al.)** also exists as a 2024 bioRxiv preprint; the *Science* 2024 version (386:eado9336) is cited. Note a known corpus-size discrepancy between preprint and published abstract.
- **Hubbard et al.** and **Mehandru et al.** are Perspective/Comment pieces, not primary studies — appropriate as framing citations, not as evidence of effect sizes.
- **AMIE (Tu et al.)** and several LLM studies were evaluated in simulated/benchmark settings; authors explicitly caution against inferring real-world clinical readiness.
- URLs point to PubMed/PMC, publisher, or DOI landing pages verified to resolve to the exact paper (title + first author + year); some full texts are paywalled.


### Verified additions (2026-10-21) — frontier methods harvest
*New verified entries from a targeted preprint+published harvest. Entries already cited above (Singhal/Med-PaLM, Nucleotide Transformer, Evo) are not repeated.*

**Genomic / DNA foundation models**
- [Avsec et al. Effective gene expression prediction from sequence (Enformer). Nature Methods 2021](https://doi.org/10.1038/s41592-021-01252-x) — landmark sequence-to-function transformer predicting expression + variant effects from ~100 kb.
- [Nguyen et al. HyenaDNA: long-range genomic sequence modeling at single-nucleotide resolution. NeurIPS 2023](https://arxiv.org/abs/2306.15794) — sub-quadratic long-context (~1M tokens) single-nucleotide model. `[preprint]`
- [Avsec et al. Advancing regulatory variant-effect prediction with AlphaGenome. Nature 2026](https://doi.org/10.1038/s41586-025-10014-0) — megabase-context single-base model predicting thousands of functional tracks + regulatory variant effects.

**LLMs in medicine & clinical NLP**
- [Yang et al. A large language model for electronic health records (GatorTron). npj Digital Medicine 2022](https://doi.org/10.1038/s41746-022-00742-2) — clinical LM trained on >90B words (82B+ clinical), 8.9B params; improves core clinical NLP.

**Agentic AI / AI co-scientist systems**
- [Gottweis et al. Towards an AI co-scientist. arXiv 2025](https://arxiv.org/abs/2502.18864) — Gemini multi-agent "generate–debate–evolve" hypothesis system; validated on drug repurposing/target discovery. `[preprint]`
- [Swanson et al. The Virtual Lab: AI agents design new SARS-CoV-2 nanobodies with experimental validation. bioRxiv 2024](https://www.biorxiv.org/content/10.1101/2024.11.11.623004) — multi-agent LLM "lab" that designed + wet-lab-validated nanobodies (later in Nature 2025). `[preprint]`

**Multimodal / cross-modal (genomics + EHR + imaging)**
- [Saab et al. Capabilities of Gemini models in medicine (Med-Gemini). arXiv 2024](https://arxiv.org/abs/2404.18416) — multimodal medical FM over text, images, long EHR retrieval, and biomedical signals. `[preprint]`
- [Yang et al. Advancing multimodal medical capabilities of Gemini. arXiv 2024](https://arxiv.org/abs/2405.03162) — Med-Gemini variants across radiology, pathology, ophthalmology, dermatology, and polygenic/genomic data. `[preprint]`

**Causal inference & target-trial emulation (§4.3)**
- [Hernán & Robins. Using big data to emulate a target trial when a randomized trial is not available. Am J Epidemiology 2016](https://doi.org/10.1093/aje/kwv254) — seminal target-trial-emulation framework for EHR/observational causal inference.
- [Hernán, Wang & Leaf. Target trial emulation: a framework for causal inference from observational data. JAMA 2022](https://doi.org/10.1001/jama.2022.21383) — the standard concise methods citation.
- [Cashin et al. Transparent reporting of observational studies emulating a target trial: the TARGET statement. JAMA 2025](https://doi.org/10.1001/jama.2025.13350) — new 21-item reporting guideline; rigor/reproducibility for biobank causal analyses.

**Health / EHR foundation models (patient-trajectory)**
- [Rasmy et al. Med-BERT: pretrained contextualized embeddings on structured EHR. npj Digital Medicine 2021](https://doi.org/10.1038/s41746-021-00455-y) — early EHR FM (28.5M patients); large gains under limited labels.
- [Kraljevic et al. Foresight — a generative pretrained transformer for modelling patient timelines. Lancet Digital Health 2024](https://doi.org/10.1016/S2589-7500(24)00025-6) — GPT-style forecasting of future patient events from free-text + structured records.
- [Renc et al. Zero-shot health-trajectory prediction using a transformer (ETHOS). npj Digital Medicine 2024](https://doi.org/10.1038/s41746-024-01235-0) — tokenized patient-timeline transformer; zero-shot forecasting across outcomes.
- [Wornow et al. The shaky foundations of foundation models for electronic health records. npj Digital Medicine 2023](https://doi.org/10.1038/s41746-023-00879-8) — critical survey of ~84 clinical FMs; evaluation-limitations framing.

*Caveats: HyenaDNA/AI co-scientist/Virtual Lab/Med-Gemini are preprints (verify any journal versions before submission); AlphaGenome is dated by the publisher to early 2026.*

# Cross-cutting synthesis — WGs 1–5

**Purpose.** Identify the recommendations that span multiple WGs, the
coordination points the WG leads should resolve before final Sci Com
presentation, and the defensive narrative the Sci Com presentation should
land on.

---

## 1. Multi-WG recommendations (coordinate, don't duplicate)

### CC-1. The "Data, AI & Methods" 9th focus area (WG-1 → WG-3, WG-4)

WG-1's framework change is the *enabling structural decision* for WG-3 and
WG-4. Without it, both Imaging and AI work is permanently orphaned in the
focus-area framework. Coordination point: WG-1 chairs WG-3 + WG-4 should
confirm the new FA name covers what they need (DICOM/FHIR standards under
"Methods"; AI co-scientist under "AI"; imaging-radiomics under
"Imaging-as-data-subarea").

### CC-2. Bias-in-translation framework (WG-2 → WG-3, WG-4)

WG-2's normative framework sits over WG-3's imaging-bias audit and WG-4's
AI-bias audit. The three WGs should align on the **single AoU
bias-reporting standard** rather than producing three semi-aligned
frameworks. The Sci Com presentation should show this as a stacked /
inherited hierarchy.

### CC-3. Translational-impact metrics → Impact Report (WG-2 → WG-5)

WG-2 defines the metrics; WG-5 produces the annual Report. Coordinate on
metric provenance and reporting cadence so the Report v1 ships within 12
months. Risk if uncoordinated: WG-2 specifies metrics that WG-5 can't
operationally capture.

### CC-4. The distinctive-evidence narrative (WG-5 ↔ WG-1)

WG-5's peer-index narrative (ELSI 21.2×, SDOH 5.1×, PGx 4.6×, methods 3.0×)
is the *Refresh's external face*. WG-1 owns the framework changes that the
narrative depends on (focus-area structure, multi-omics signal). The
narrative cannot land cleanly without the framework being settled.

### CC-5. Aging/ADRD engagement (no WG owns it cleanly)

AoU is flat at 4.2% post-2023 in aging/ADRD while UKB/MVP/CKB all surge in
the lecanemab/donanemab era (`emerging_themes.md` §5). This is a real
peer-comparative gap but doesn't fit cleanly in any one Top-3. The Refresh
WG should consider naming it as a Tier-2 priority (below the Top-3 but on
the radar); the Communications WG should consider it as a story for the
patient-facing dissemination product. **Flag for WG leads.**

---

## 2. The defensive narrative — what the Sci Com presentation should emphasize

The corpus and peer-comparison analysis surfaces *four* genuinely distinctive
AoU strengths. Each is quantified, each has IC alignment, each survives
adversarial reading.

| Distinctive strength | AoU share | Peer median | Peer index | Anchor IC alignment |
|---|---:|---:|---:|---|
| ELSI / participant engagement | 5.0% | 0.2% | **21.2×** | NHGRI A4; NIH-Wide CCT5 |
| SDOH / disparities | 33.3% | 6.5% | **5.1×** | NIMHD G7 (literal mandate); NIH-Wide CCT1 |
| Pharmacogenomics | 2.3% | 0.5% | **4.6×** | NIGMS-G4 (PGRN); NCATS Translator |
| Methods / infrastructure / phenotyping | 18.3% | 6.1% | **3.0×** | NLM G1 (mission-explicit AoU) |

**The narrative sentence:** *"AoU is the cohort that, alone among the
world's biobanks, built participant-engagement (21× peers), structural
diversity (5× peers), pharmacogenomic depth (5× peers), and platform/methods
infrastructure (3× peers) into its design. Every other cohort scaled up
genomics; AoU scaled up everything *around* genomics that genomics actually
needs to work in practice."*

This narrative is the **defensive frame** under which every WG's
recommendations should be read. The framework changes WG-1 proposes
(9th FA, multi-omics rename, FA2/FA4 reframes) **protect** these strengths;
the metrics and bias frameworks WG-2/WG-3/WG-4 propose **measure** them; the
products WG-5 proposes **communicate** them.

### Honest gaps to name explicitly

A credible communications posture acknowledges gaps before adversarial
audiences raise them. The honest gaps in the current corpus are:

- **Imaging.** 8 pubs / 0.6% share. AoU has not yet released imaging at
  scale. WG-3 is starting from infrastructure.
- **Environmental health.** 7 pubs / 0.5% share. The single largest
  IC-demand vs AoU-supply gap (NIEHS 6 priorities; 7 corpus pubs).
- **Multi-omics beyond genomics.** 24 pubs / 1.7% share vs UKB 12.8%
  post-2023. The 2026 releases will close this; the framework rename
  (WG-1 Rec 2) signals the intent.
- **Stool biospecimen / microbiome.** AoU does not collect; structural.
- **Pediatric / "Child" content in FA2.** AoU is an adult cohort; the
  "Child" naming overreaches.

Naming these openly *strengthens* the distinctive-evidence claim by
showing the program knows the difference between strength and gap.

### Known noise to flag, not elevate

- **Dermatology at 14.3% / peer-index 7.8×.** Driven by 1–2 prolific
  groups; declining as a share (trend −3.9); not a strategic priority.
  Surface only if Sci Com asks; do not lead with it.
- **AoU growth on cardiometabolic / mental health / cancer.** Almost
  certainly a small-baseline artifact (157 pre-2023 vs 1,217 post-2023);
  read as "AoU has built presence here," not "AoU is uniquely outpacing
  the field." Per `emerging_themes.md` "do not over-index on."

---

## 3. Slide-7 priorities — clean read

For Sci Com clarity, here is the read of slide 7's eight priorities the
WG leads should align on:

| Slide 7 priority | Evidence read | WG ownership |
|---|---|---|
| AI / LLM / foundation models | Already realized — HA4 31 pubs, 28 post-2023 | WG-4 lead; WG-1 enables via 9th FA |
| Breakthrough therapeutics (GLP-1, SGLT2, AD mAbs, CRISPR) | Already realized — HA8 16 pubs | WG-2 (use case) |
| Wearables / remote monitoring | Already realized but **trend-flat** — HA2 70 pubs, ±0.0; **recognition gap, not growth gap** | WG-1 frames via 9th FA |
| Multi-omics beyond genomics | **Aspirational, pending investment** — HA1 24 pubs, 23 post-2023 | WG-1 leads via FA8 rename + release roadmap |
| Imaging / radiomics | **Aspirational, pending investment** — HA3 8 pubs *thin* | WG-3 leads (infrastructure-from-scratch) |
| G×E×SDOH integrated holistic risk models | **Emerging, AoU positioned to lead** — HA6 10 pubs, 0 pre-2023 | WG-1 surface as latent strength; WG-2 use case |
| Nutrition / microbiome / chronic disease | **Structurally under-supported** — HA7 11 pubs; no stool biospecimen | Flag as a known gap (cross-cutting); no WG can resolve in current cycle |
| Environmental health | **Largest gap with named IC demand** — HA5 12 pubs; NIEHS 6 priorities | WG-1 framework commitment via FA6 |

**The clean split:** four priorities are *already realized* (AI,
breakthrough therapeutics, wearables-as-mature, G×E×SDOH integrated); four
are *aspirational pending upstream investment* (multi-omics, imaging,
nutrition/microbiome, environmental). The Sci Com presentation should
make this split explicit — it reframes "are we delivering on the 2023
priorities?" from a single yes/no into a two-bucket conversation that
honors the corpus evidence.

---

## 4. Coordination calendar for WG leads (suggested)

1. **Pre-Sci Com circulation:** WG-1 + WG-5 align on framework + narrative
   wording (CC-4) before either presents. The Refresh framework changes
   must precede the Communications narrative.
2. **Joint WG-2 / WG-3 / WG-4 standards session:** align on the
   bias-in-translation hierarchy (CC-2) so the three WGs aren't producing
   three different audit templates.
3. **WG-2 / WG-5 metrics handshake:** confirm WG-2's metric definitions
   are operationally captureable for WG-5's Impact Report v1 (CC-3).
4. **WG-1 / WG-3 / WG-4 framework confirmation:** confirm 9th-FA name and
   scope before WG-3 and WG-4 finalize their recommendations.

---

## 5. Places the evidence is thin (judgment > evidence flag)

For the WG-1 lead to know which Top-3 elements are most "judgment" vs most
"evidence":

- **WG-1 Rec 1 (9th focus area).** Strong evidence (18% orphan, +
  AI/wearables peers).
- **WG-1 Rec 2 (multi-omics rename + roadmap).** Strong peer-index evidence
  but the *release roadmap* is a strategic ask, not a corpus finding.
- **WG-1 Rec 3 (FA2/FA4/FA6 reframes).** FA4 is well-evidenced (−9.6
  trend); FA2 is judgment about naming accuracy; FA6 is well-evidenced
  (largest gap).
- **WG-2 Rec 3 (bias-in-translation framework).** Strong peer-index
  defense; the FDA-readiness angle is more political-window framing than
  corpus evidence.
- **WG-3 Rec 1 (staged release plan).** *Judgment-heavy.* Modality
  prioritization is informed but not corpus-driven (corpus has 8 imaging
  pubs total).
- **WG-3 Rec 3 (imaging bias-audit framework).** Inferred from WG-2; the
  WG-3 leads have technical context I don't.
- **WG-4 Rec 3 (foundation-model evaluation).** Judgment call —
  "evaluate-don't-build" is a recommendation about process, not evidence
  from the corpus.
- **WG-5 Rec 2 (distinctive-evidence narrative).** *Most evidence-driven
  of any recommendation* — peer-index numbers are precise.
- **Aging/ADRD (CC-5).** Real evidence (peer surge while AoU flat) but no
  WG owns it cleanly; flag-only.

---

## 6. One-line recommendation summary for the WG leads' joint planning

If Sci Com only attends to *three* recommendations across the five WGs,
they should be:

1. **WG-1 Rec 1 — Add a "Data, AI & Methods" 9th focus area.** Mean 3.71.
   Frame-defining; no other WG can do this.
2. **WG-4 Rec 1 — AoU Workbench AI co-scientist.** Mean 3.88. Highest-
   rubric-mean researcher-impact recommendation in the entire set.
3. **WG-5 Rec 2 — Plain-language distinctive-evidence narrative.** Mean
   3.60. The political-defense story that funds all the rest.

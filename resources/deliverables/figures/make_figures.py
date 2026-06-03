#!/usr/bin/env python3
"""Generate small PNG figures for the AoU Roadmap Refresh deck."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

HERE = os.path.dirname(os.path.abspath(__file__))

NAVY = "#1A3A6B"
ACCENT = "#216bb3"
GRAY = "#666"
LIGHT = "#cfd8e3"

plt.rcParams.update({
    "font.family": "Helvetica",
    "font.size": 11,
    "axes.edgecolor": "#888",
    "axes.labelcolor": NAVY,
    "axes.titlecolor": NAVY,
    "xtick.color": "#333",
    "ytick.color": "#333",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# ---------------------------------------------------------------------------
# Figure 1: Corpus publications by year (temporal slope)
# ---------------------------------------------------------------------------
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
counts = [4, 4, 3, 12, 13, 10, 32, 79, 157, 341, 519, 199]
fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=160)
bars = ax.bar(years, counts, color=ACCENT, edgecolor=NAVY, linewidth=0.5)
# Color pre-2023 differently
for b, y in zip(bars, years):
    if y < 2023:
        b.set_color(LIGHT)
        b.set_edgecolor("#888")
ax.set_xticks(years)
ax.set_ylabel("Substantive AoU publications", fontsize=10)
ax.set_title("AoU corpus growth: 157 pubs pre-2023 vs 1,217 post-2023 (≥7.8× scale-up)",
             fontsize=11, weight="bold", pad=10, loc="left")
for b, c in zip(bars, counts):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+8, str(c),
            ha="center", va="bottom", fontsize=8.5, color="#333")
ax.axvline(2022.5, color=NAVY, linestyle="--", linewidth=1, alpha=0.6)
ax.text(2022.5, max(counts)*0.95, "  v6/v7/v8 releases",
        color=NAVY, fontsize=9, ha="left", style="italic")
ax.tick_params(axis="x", labelsize=9)
ax.tick_params(axis="y", labelsize=9)
ax.set_ylim(0, max(counts)*1.12)
plt.tight_layout()
plt.savefig(os.path.join(HERE, "corpus_by_year.png"), bbox_inches="tight", dpi=160)
plt.close()

# ---------------------------------------------------------------------------
# Figure 2: AoU vs peer-biobank share comparison for the 5 under-indexed themes
# ---------------------------------------------------------------------------
# Source: aou_vs_peers_index.csv + emerging_themes.md
themes = ["Multi-omics\n(HA1)", "Imaging\n(HA3)", "Microbiome/\nNutrition (HA7)",
          "Rare disease\n(Theme 10)", "Aging/ADRD\n(Theme 11)"]
aou_share = [1.7, 0.6, 0.8, 3.9, 4.2]
peer_med  = [10.0, 1.6, 11.1, 13.0, 6.7]  # using representative peer values

fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=160)
x = list(range(len(themes)))
w = 0.36
b1 = ax.bar([i-w/2 for i in x], aou_share, width=w, color=ACCENT,
            edgecolor=NAVY, linewidth=0.5, label="AoU share (%)")
b2 = ax.bar([i+w/2 for i in x], peer_med, width=w, color=LIGHT,
            edgecolor="#888", linewidth=0.5, label="Peer median (%)")
for b, v in zip(b1, aou_share):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.15,
            f"{v}%", ha="center", va="bottom", fontsize=8.5, color=NAVY, weight="bold")
for b, v in zip(b2, peer_med):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.15,
            f"{v}%", ha="center", va="bottom", fontsize=8.5, color="#333")
ax.set_xticks(x)
ax.set_xticklabels(themes, fontsize=9)
ax.set_ylabel("Share of corpus (%)", fontsize=10)
ax.set_title("AoU is under-indexed on 5 peer-biobank themes",
             fontsize=11, weight="bold", pad=10, loc="left")
ax.legend(fontsize=9, frameon=False, loc="upper right")
ax.tick_params(axis="y", labelsize=9)
ax.set_ylim(0, max(peer_med)*1.18)
plt.tight_layout()
plt.savefig(os.path.join(HERE, "peer_under_indexed.png"), bbox_inches="tight", dpi=160)
plt.close()

# ---------------------------------------------------------------------------
# Figure 3: AoU distinctive strengths (peer over-indexes)
# ---------------------------------------------------------------------------
themes = ["ELSI /\nengagement", "SDOH /\ndisparities", "Pharmaco-\ngenomics",
          "Methods /\ninfrastructure"]
indices = [21.2, 5.1, 4.6, 3.0]
fig, ax = plt.subplots(figsize=(8.0, 3.8), dpi=160)
bars = ax.barh(themes, indices, color=ACCENT, edgecolor=NAVY, linewidth=0.5)
for b, v in zip(bars, indices):
    ax.text(b.get_width()+0.3, b.get_y()+b.get_height()/2,
            f"{v}×", ha="left", va="center", fontsize=11, color=NAVY, weight="bold")
ax.set_xlabel("AoU share ÷ peer-biobank median share", fontsize=10)
ax.set_title("AoU's four distinctive strengths (vs peer-biobank median)",
             fontsize=11, weight="bold", pad=10, loc="left")
ax.tick_params(axis="x", labelsize=9)
ax.tick_params(axis="y", labelsize=10)
ax.invert_yaxis()
ax.set_xlim(0, 24)
ax.axvline(1.0, color="#999", linewidth=1, linestyle="--")
ax.text(1.05, 3.6, "parity (1×)", fontsize=8, color="#666", style="italic")
plt.tight_layout()
plt.savefig(os.path.join(HERE, "distinctive_strengths.png"), bbox_inches="tight", dpi=160)
plt.close()

# ---------------------------------------------------------------------------
# Figure 4: 8-area + 9th-area focus-area framework visual
# ---------------------------------------------------------------------------
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(11.5, 4.6), dpi=160)
ax.set_xlim(0, 11.5)
ax.set_ylim(0, 4.6)
ax.axis("off")

current_areas = [
    ("FA1", "Common &\nRare Conditions", "73%"),
    ("FA2", "Maternal &\nChild Health", "3%"),
    ("FA3", "Healthy Aging\n& Resilience", "5%"),
    ("FA4", "Return\nof Results", "11%"),
    ("FA5", "Lifestyle, Substance,\n& Behavioral", "18%"),
    ("FA6", "Environment", "0.5%"),
    ("FA7", "Health Equity", "51%"),
    ("FA8", "Genetics &\nBiology", "53%"),
]
proposed = ("FA9", "Data, AI &\nMethods", "18%")

box_w, box_h = 1.25, 1.55
gap_x = 0.06
start_x = 0.3
y_top = 2.6

for i, (code, name, share) in enumerate(current_areas):
    x = start_x + i*(box_w + gap_x)
    rect = patches.FancyBboxPatch((x, y_top), box_w, box_h,
                                  boxstyle="round,pad=0.02",
                                  linewidth=1.0, edgecolor=NAVY,
                                  facecolor="#eaf0fa")
    ax.add_patch(rect)
    ax.text(x+box_w/2, y_top+box_h-0.22, code, ha="center", va="top",
            fontsize=10, color=NAVY, weight="bold")
    ax.text(x+box_w/2, y_top+box_h/2-0.05, name, ha="center", va="center",
            fontsize=8.5, color="#222")
    ax.text(x+box_w/2, y_top+0.18, share, ha="center", va="bottom",
            fontsize=9, color=ACCENT, weight="bold", style="italic")

# Proposed 9th area below, highlighted
x9 = start_x + 3.5*(box_w + gap_x)
rect = patches.FancyBboxPatch((x9, 0.5), box_w*1.3, box_h*0.95,
                              boxstyle="round,pad=0.02",
                              linewidth=2.0, edgecolor=ACCENT,
                              facecolor="#fff7e8")
ax.add_patch(rect)
ax.text(x9+box_w*1.3/2, 0.5+box_h*0.95-0.22, "FA9 (proposed)",
        ha="center", va="top", fontsize=10, color=ACCENT, weight="bold")
ax.text(x9+box_w*1.3/2, 0.5+box_h*0.95/2-0.05, proposed[1],
        ha="center", va="center", fontsize=9, color="#222", weight="bold")
ax.text(x9+box_w*1.3/2, 0.5+0.18, f"{proposed[2]} corpus orphan",
        ha="center", va="bottom", fontsize=9, color="#b35900", weight="bold", style="italic")

# Title
ax.text(0.3, 4.3, "Proposed framework: add a 9th focus area for the 18% Methods/AI orphan",
        fontsize=12, weight="bold", color=NAVY)
ax.text(0.3, 4.0, "Share = % of substantive AoU pubs touching the area (multi-tagged; rows sum > 100%)",
        fontsize=8.5, color="#666", style="italic")

plt.tight_layout()
plt.savefig(os.path.join(HERE, "framework_8_plus_1.png"), bbox_inches="tight", dpi=160)
plt.close()

print("Figures written to", HERE)
print(os.listdir(HERE))

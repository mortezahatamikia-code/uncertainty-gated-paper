# -*- coding: utf-8 -*-
"""
Generate a publication-grade, vector-quality architecture diagram for BioDINO-Edge.
Outputs both PDF (for LaTeX compilation) and PNG (for raster review).
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
PAPER_DIR = PROJECT_ROOT / "paper"
PAPER_DIR.mkdir(exist_ok=True)

def create_architecture_diagram():
    # Set publication-standard font styling
    plt.rcParams.update({
        'font.sans-serif': 'DejaVu Sans',
        'font.family': 'sans-serif',
        'font.size': 8.5,
        'axes.labelsize': 9,
        'figure.titlesize': 11
    })

    fig = plt.figure(figsize=(14.0, 7.8), dpi=300)
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)

    # Palette
    c_blue_dark   = "#1A365D"
    c_blue_med    = "#2B6CB0"
    c_blue_light  = "#EBF8FF"
    c_blue_border = "#3182CE"

    c_teal_dark   = "#1D4044"
    c_teal_med    = "#285E61"
    c_teal_light  = "#E6FFFA"
    c_teal_border = "#319795"

    c_amber_dark  = "#744210"
    c_amber_med   = "#B7791F"
    c_amber_light = "#FEFCBF"
    c_amber_border= "#D69E2E"

    c_green_dark  = "#1C4532"
    c_green_med   = "#276749"
    c_green_light = "#F0FFF4"
    c_green_border= "#38A169"

    c_purple_dark = "#44337A"
    c_purple_med  = "#6B46C1"
    c_purple_light= "#FAF5FF"
    c_purple_border = "#805AD5"

    c_gray_bg     = "#F7FAFC"
    c_gray_border = "#CBD5E0"
    c_text_dark   = "#2D3748"

    # -------------------------------------------------------------
    # Helper functions
    # -------------------------------------------------------------
    def draw_box(x, y, w, h, bg, border, title="", subtitle="", radius=1.0, title_color="#000", sub_color="#4A5568", fontsize=8.5):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.2,rounding_size={radius}",
                                     facecolor=bg, edgecolor=border, linewidth=1.4, zorder=2)
        ax.add_patch(box)
        if title and subtitle:
            ax.text(x + w/2, y + h*0.62, title, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=title_color, zorder=3)
            ax.text(x + w/2, y + h*0.30, subtitle, ha='center', va='center', fontsize=fontsize-1.2, color=sub_color, zorder=3)
        elif title:
            ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=title_color, zorder=3)

    def draw_arrow(x1, y1, x2, y2, color="#4A5568", style='->', lw=1.5, ls='-', label="", label_pos=0.5, label_offset=(0, 1.2), label_fontsize=7.5, label_color="#2D3748"):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0), zorder=4)
        if label:
            lx = x1 + (x2 - x1) * label_pos + label_offset[0]
            ly = y1 + (y2 - y1) * label_pos + label_offset[1]
            ax.text(lx, ly, label, ha='center', va='center', fontsize=label_fontsize, color=label_color, fontweight='bold', zorder=5,
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor=color, alpha=0.9, lw=0.8))

    # -------------------------------------------------------------
    # 1. Background Section Panels
    # -------------------------------------------------------------
    # Panel A: Offline Preparation (Left Column)
    panel_a = patches.FancyBboxPatch((2, 3), 29, 54, boxstyle="round,pad=0.4,rounding_size=1.5",
                                     facecolor="#F7FAFC", edgecolor="#CBD5E0", linewidth=1.5, linestyle="--", zorder=1)
    ax.add_patch(panel_a)
    ax.text(16.5, 55.2, "STAGE I: OFFLINE SUPPORT CALIBRATION", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=c_blue_dark, zorder=3)
    ax.text(16.5, 53.6, "One-Time Analytical Processing (~50 ms, Zero-Backpropagation)", ha='center', va='center',
            fontsize=7.5, color="#4A5568", zorder=3)

    # Panel B: Online Inference & Dynamic Gating (Middle & Right Columns)
    panel_b = patches.FancyBboxPatch((33, 3), 65, 54, boxstyle="round,pad=0.4,rounding_size=1.5",
                                     facecolor="#FFFFFF", edgecolor="#CBD5E0", linewidth=1.5, zorder=1)
    ax.add_patch(panel_b)
    ax.text(65.5, 55.2, "STAGE II: DUAL-TIER CASCADED INFERENCE & ADAPTIVE GATING", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=c_green_dark, zorder=3)
    ax.text(65.5, 53.6, "Real-Time Streaming Edge Architecture (Sub-22 ms Latency on ARM CPU)", ha='center', va='center',
            fontsize=7.5, color="#4A5568", zorder=3)

    # -------------------------------------------------------------
    # Stage I Elements (Offline Calibration)
    # -------------------------------------------------------------
    # Few-shot support box
    draw_box(4.5, 45.0, 24, 6.2, c_blue_light, c_blue_border,
             "Few-Shot Support Foliage", r"$\mathcal{S} = \{(x_i, y_i)\}_{i=1}^{N_s}$ ($K=5$ shots per class)",
             title_color=c_blue_dark)

    # Multi-view orbital augmentation
    draw_box(4.5, 36.2, 24, 6.0, "#FFFFFF", c_blue_med,
             r"Multi-View Fréchet Orbit ($V=8$)", r"Rotation, Jitter, Flip $\to N_{\mathrm{eff}} = 440$ vectors",
             title_color=c_blue_dark)
    draw_arrow(16.5, 45.0, 16.5, 42.2, color=c_blue_med)

    # Dual extraction split
    draw_box(4.5, 27.5, 11.2, 6.0, c_teal_light, c_teal_border,
             "DINOv2 Small", r"$\mathbf{f}_{\mathrm{dino}} \in \mathbb{R}^{384}$", title_color=c_teal_dark)
    draw_box(17.3, 27.5, 11.2, 6.0, c_purple_light, c_purple_border,
             "BioCLIP ViT-B", r"$\mathbf{f}_{\mathrm{bio}} \in \mathbb{R}^{512}$", title_color=c_purple_dark)

    draw_arrow(12.0, 36.2, 10.1, 33.5, color=c_teal_med)
    draw_arrow(21.0, 36.2, 22.9, 33.5, color=c_purple_med)

    # Purified Domain Prompts
    draw_box(4.5, 19.0, 24, 6.0, c_purple_light, c_purple_border,
             "Purified Botanical Taxonomy", "Latin binomials & positive structural etiology",
             title_color=c_purple_dark)
    draw_arrow(22.9, 27.5, 22.9, 25.0, color=c_purple_med)

    # Joint Manifold & Ledoit-Wolf Fisher-LDA
    draw_box(4.5, 9.8, 24, 6.8, c_amber_light, c_amber_border,
             r"Joint 896-d Manifold ($\mathcal{H}_{\mathrm{dino}} \oplus \mathcal{H}_{\mathrm{bio}}$)",
             r"Ledoit-Wolf Shrinkage: $\hat{\mathbf{\Sigma}} = (1-\rho^*)\mathbf{S}_W + \rho^* \nu \mathbf{I}$" + "\n" + r"$\to \mathbf{W} = \hat{\mathbf{\Sigma}}^{-1}[\boldsymbol{\mu}_1,\dots,\boldsymbol{\mu}_C]^T$",
             title_color=c_amber_dark, fontsize=8.0)

    draw_arrow(10.1, 27.5, 10.1, 16.6, color=c_amber_med)
    draw_arrow(22.9, 19.0, 22.9, 16.6, color=c_amber_med)

    # Output weights arrow to online stage
    draw_arrow(28.5, 13.2, 63.5, 13.2, color=c_amber_med, lw=1.8, style='->',
               label="Trained Fisher Head (W, b) [<10 KB]", label_pos=0.45, label_offset=(0, 1.4), label_color=c_amber_dark)

    # -------------------------------------------------------------
    # Stage II Elements (Online Cascaded Inference)
    # -------------------------------------------------------------
    # Input Query Leaf
    draw_box(35.5, 45.0, 18.0, 6.2, c_green_light, c_green_border,
             "Input Query Leaf", r"$x_q \in \mathbb{R}^{H \times W \times 3}$ (Field Photo / UAV Stream)",
             title_color=c_green_dark)

    # Tier 1 Box (Enclosing Fast Path)
    tier1_bg = patches.FancyBboxPatch((57.5, 33.5), 38.5, 18.5, boxstyle="round,pad=0.3,rounding_size=1.0",
                                     facecolor="#F0FFF4", edgecolor=c_green_border, linewidth=1.4, linestyle=":", zorder=1)
    ax.add_patch(tier1_bg)
    ax.text(76.75, 50.4, "TIER 1: STANDALONE FAST-PATH (APK BUNDLE, ~21 MB INT8)",
            ha='center', va='center', fontsize=8.0, fontweight='bold', color=c_green_dark, zorder=3)

    # DINOv2 Fast-Path
    draw_box(59.5, 42.0, 15.0, 6.5, "#FFFFFF", c_teal_med,
             "DINOv2 Small", r"$\mathbf{f}_{\mathrm{dino}} \in \mathbb{R}^{384}$" + "\n" + r"Latency: 21.1 ms",
             title_color=c_teal_dark, fontsize=8.0)

    draw_arrow(53.5, 48.1, 59.5, 45.2, color=c_teal_med, lw=1.6)

    # Shannon Margin-Entropy Gate
    draw_box(78.5, 41.5, 15.5, 7.5, c_amber_light, c_amber_border,
             r"Shannon Gate $\mathcal{C}(\mathbf{x})$",
             r"$\Delta p \cdot (1 - \tilde{\mathcal{H}}(\mathbf{p}))$" + "\n" + r"Threshold: $\tau_{\mathrm{conf}} = 0.35$",
             title_color=c_amber_dark, fontsize=8.0)

    draw_arrow(74.5, 45.2, 78.5, 45.2, color=c_amber_med, lw=1.6)

    # Decision branches from Gate
    # Branch 1: Fast-Exit (Green)
    draw_box(79.0, 35.0, 14.5, 4.5, "#C6F6D5", c_green_dark,
             r"Fast-Exit (88.4% Queries)", ">45 FPS | High Certainty",
             title_color=c_green_dark, fontsize=7.5)
    draw_arrow(86.25, 41.5, 86.25, 39.5, color=c_green_dark, lw=1.8,
               label=r"$\mathcal{C} \geq 0.35$", label_pos=0.5, label_offset=(2.8, 0), label_color=c_green_dark)

    # Branch 2: Ambiguous Fallback to Tier 2
    # Tier 2 Box (Enclosing Deep Path)
    tier2_bg = patches.FancyBboxPatch((35.5, 5.0), 60.5, 25.5, boxstyle="round,pad=0.3,rounding_size=1.0",
                                     facecolor="#FAF5FF", edgecolor=c_purple_border, linewidth=1.4, linestyle=":", zorder=1)
    ax.add_patch(tier2_bg)
    ax.text(65.75, 29.0, "TIER 2: ON-DEMAND DEEP COMPANION (~84 MB INT8, 896-d FISHER + TRANSDUCTIVE)",
            ha='center', va='center', fontsize=8.0, fontweight='bold', color=c_purple_dark, zorder=3)

    # Arrow from Gate to Tier 2
    draw_arrow(86.25, 41.5, 86.25, 26.5, color=c_purple_med, lw=1.8, style='->',
               label=r"$\mathcal{C} < 0.35$ (Ambiguous / 11.6%)", label_pos=0.6, label_offset=(7.5, 0), label_color=c_purple_dark)

    # BioCLIP in Tier 2
    draw_box(37.5, 17.5, 16.0, 6.5, "#FFFFFF", c_purple_med,
             "BioCLIP ViT-B", r"$\mathbf{f}_{\mathrm{bio}} \in \mathbb{R}^{512}$" + "\n" + r"Taxonomic Vision",
             title_color=c_purple_dark, fontsize=8.0)

    # Query image arrow to BioCLIP
    draw_arrow(44.5, 45.0, 44.5, 24.0, color=c_purple_med, lw=1.5, style='->', ls='--')

    # Concatenate 896-d
    draw_box(57.5, 17.5, 15.0, 6.5, c_amber_light, c_amber_border,
             r"896-d Concatenation", r"$\mathbf{z}_q = [\mathbf{f}_{\mathrm{bio}}, \mathbf{f}_{\mathrm{dino}}]$",
             title_color=c_amber_dark, fontsize=8.0)

    draw_arrow(53.5, 20.75, 57.5, 20.75, color=c_amber_med, lw=1.5)
    # DINOv2 feature link into concatenation
    ax.plot([67.0, 67.0], [42.0, 24.0], color=c_teal_med, lw=1.4, linestyle=':')
    draw_arrow(67.0, 24.0, 67.0, 24.0, color=c_teal_med)

    # Fisher Alignment & Text Blend
    draw_box(76.0, 17.5, 18.0, 6.5, "#FFFFFF", c_blue_med,
             r"Fisher + Text Ensemble", r"$\mathbf{p} = 0.75 \mathbf{p}_{\mathrm{fisher}} + 0.25 \mathbf{p}_{\mathrm{text}}$",
             title_color=c_blue_dark, fontsize=8.0)
    draw_arrow(72.5, 20.75, 76.0, 20.75, color=c_blue_med, lw=1.5)

    # Transductive Self-Calibration / Incremental Buffer
    draw_box(63.5, 7.5, 30.5, 6.8, c_purple_light, c_purple_border,
             r"Soft-Anchored Transductive Recalibration ($3\times$ Anchor)",
             r"Online Buffer $\to$ Closed-Form $\hat{\mathbf{\Sigma}}^{\mathrm{trans}}$ & $\mathbf{W}^{\mathrm{trans}}$ re-estimation (<22 ms)",
             title_color=c_purple_dark, fontsize=7.8)

    draw_arrow(85.0, 17.5, 85.0, 14.3, color=c_purple_med, lw=1.5)

    # Output Box: Diagnosis & Calibrated Confidence
    draw_box(37.5, 7.5, 22.0, 6.8, "#FFFFFF", c_green_dark,
             r"Diagnostic Prediction \& ECE",
             r"Peak Accuracy: 98.67% | ECE: 0.79%" + "\n" + r"Temperature Scaling ($T=0.50$)",
             title_color=c_green_dark, fontsize=8.0)

    draw_arrow(63.5, 10.9, 59.5, 10.9, color=c_green_dark, lw=1.8)
    draw_arrow(86.25, 35.0, 48.5, 14.3, color=c_green_dark, lw=1.5, ls='--',
               label="Fast-Exit Routing", label_pos=0.65, label_offset=(-3.5, 1.0), label_color=c_green_dark)

    # Save outputs
    pdf_path = PAPER_DIR / "fig_architecture.pdf"
    png_path = PAPER_DIR / "fig_architecture.png"
    plt.savefig(pdf_path, format='pdf', bbox_inches='tight', pad_inches=0.04)
    plt.savefig(png_path, format='png', bbox_inches='tight', pad_inches=0.04, dpi=300)
    plt.close()
    print(f"[OK] Saved {pdf_path} and {png_path} successfully!")

if __name__ == "__main__":
    create_architecture_diagram()

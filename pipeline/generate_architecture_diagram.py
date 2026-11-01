# -*- coding: utf-8 -*-
"""
Generate a publication-grade, vector-quality architecture diagram for BioDINO-Edge.
Produces both PDF (for LaTeX publication) and high-res PNG.
Clean left-to-right cascaded layout with zero line crossings or text collisions.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

_curr = Path(__file__).resolve().parent
PROJECT_ROOT = _curr if (_curr / "paper").exists() else _curr.parent
PAPER_DIR = PROJECT_ROOT / "paper"
PAPER_DIR.mkdir(exist_ok=True)

def create_architecture_diagram():
    plt.rcParams.update({
        'font.sans-serif': 'DejaVu Sans',
        'font.family': 'sans-serif',
        'font.size': 8.5,
        'axes.labelsize': 9,
        'figure.titlesize': 11
    })

    fig = plt.figure(figsize=(14.2, 7.6), dpi=300)
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)

    # Cohesive, publication-grade color palette
    c_navy_dark    = "#0F172A"  # Slate 900
    c_subtext      = "#475569"  # Slate 600

    # Stage I: Professional Blue theme
    c_blue_box_bg  = "#F0F9FF"
    c_blue_box_brd = "#0284C7"
    c_blue_txt     = "#0369A1"

    # Fast-Path / Tier 1: Emerald theme
    c_green_bg     = "#F0FDF4"
    c_green_brd    = "#16A34A"
    c_green_txt    = "#15803D"
    c_green_pill   = "#DCFCE7"

    # Companion / Tier 2: Royal Purple theme
    c_purple_bg    = "#FAF5FF"
    c_purple_brd   = "#9333EA"
    c_purple_txt   = "#7E22CE"
    c_purple_box   = "#F3E8FF"

    # Fusion & Manifold: Warm Amber / Gold theme
    c_amber_bg     = "#FEFCE8"
    c_amber_brd    = "#CA8A04"
    c_amber_txt    = "#A16207"

    # Helper: Draw smooth rounded cards
    def draw_card(x, y, w, h, bg, border, title="", subtitle="", detail="",
                  radius=0.9, lw=1.3, title_color="#0F172A", sub_color="#475569", detail_color="#64748B",
                  fontsize=8.2, zorder=2):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.25,rounding_size={radius}",
                                     facecolor=bg, edgecolor=border, linewidth=lw, zorder=zorder)
        ax.add_patch(box)
        
        if title and subtitle and detail:
            ax.text(x + w/2, y + h*0.72, title, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=title_color, zorder=zorder+1)
            ax.text(x + w/2, y + h*0.42, subtitle, ha='center', va='center', fontsize=fontsize-1.1, color=sub_color, zorder=zorder+1)
            ax.text(x + w/2, y + h*0.18, detail, ha='center', va='center', fontsize=fontsize-1.6, color=detail_color, zorder=zorder+1)
        elif title and subtitle:
            ax.text(x + w/2, y + h*0.64, title, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=title_color, zorder=zorder+1)
            ax.text(x + w/2, y + h*0.30, subtitle, ha='center', va='center', fontsize=fontsize-1.2, color=sub_color, zorder=zorder+1)
        elif title:
            ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=title_color, zorder=zorder+1)

    # Helper: Draw clean orthogonal or straight arrows
    def draw_arrow(x1, y1, x2, y2, color="#475569", lw=1.4, ls='-', label="", label_pos=0.5,
                   label_offset=(0, 0), label_color="#0F172A", label_bg="white", label_fs=7.2):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.32,head_length=0.45",
                                    color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0), zorder=6)
        if label:
            lx = x1 + (x2 - x1) * label_pos + label_offset[0]
            ly = y1 + (y2 - y1) * label_pos + label_offset[1]
            ax.text(lx, ly, label, ha='center', va='center', fontsize=label_fs,
                    color=label_color, fontweight='bold', zorder=7,
                    bbox=dict(boxstyle="round,pad=0.22", facecolor=label_bg, edgecolor=color, alpha=0.96, lw=0.8))

    # =========================================================================
    # 1. Background Section Panels
    # =========================================================================
    # Panel I: Offline Support Calibration (Left)
    panel_i = patches.FancyBboxPatch((2.0, 2.5), 26.5, 55.0, boxstyle="round,pad=0.4,rounding_size=1.2",
                                     facecolor="#F8FAFC", edgecolor="#94A3B8", linewidth=1.4, linestyle="--", zorder=1)
    ax.add_patch(panel_i)
    ax.text(15.25, 55.4, "STAGE I: OFFLINE SUPPORT CALIBRATION", ha='center', va='center',
            fontsize=9.2, fontweight='bold', color="#0F172A", zorder=3)
    ax.text(15.25, 53.6, "One-Time Analytical Processing (~50 ms, No Backprop)", ha='center', va='center',
            fontsize=7.3, color=c_subtext, zorder=3)

    # Panel II: Online Inference & Adaptive Gating (Right)
    panel_ii = patches.FancyBboxPatch((30.0, 2.5), 68.0, 55.0, boxstyle="round,pad=0.4,rounding_size=1.2",
                                      facecolor="#FFFFFF", edgecolor="#94A3B8", linewidth=1.4, zorder=1)
    ax.add_patch(panel_ii)
    ax.text(64.0, 55.4, "STAGE II: DUAL-TIER CASCADED INFERENCE & ADAPTIVE GATING", ha='center', va='center',
            fontsize=9.2, fontweight='bold', color="#0F172A", zorder=3)
    ax.text(64.0, 53.6, "Real-Time Streaming Edge Architecture (Sub-22 ms Latency on 4-Thread ARM CPU)", ha='center', va='center',
            fontsize=7.3, color=c_subtext, zorder=3)

    # =========================================================================
    # 2. Stage I: Offline Support Alignment (Top-to-Bottom Flow)
    # =========================================================================
    # 1) Few-shot support leaves
    draw_card(4.0, 45.2, 22.5, 6.2, c_blue_box_bg, c_blue_box_brd,
              "Few-Shot Support Foliage", r"$\mathcal{S} = \{(x_i, y_i)\}_{i=1}^{N_s}$ ($K=5$ shots per class)",
              title_color=c_blue_txt)

    # 2) Multi-View Orbit
    draw_card(4.0, 36.2, 22.5, 6.0, "#FFFFFF", "#64748B",
              r"Multi-View Fréchet Orbit ($V=8$)", r"Rotation, Jitter, Flip $\to N_{\mathrm{eff}} = 440$ vectors",
              title_color="#1E293B")
    draw_arrow(15.25, 45.2, 15.25, 42.2, color="#0284C7")

    # 3) Parallel Dual Feature Extraction (Side-by-Side!)
    # Left: DINOv2
    draw_card(4.0, 25.0, 10.8, 8.0, "#F0FDFA", "#0D9488",
              "DINOv2 Small", r"$\mathbf{f}_{\mathrm{dino}} \in \mathbb{R}^{384}$",
              "Spatial Patch Tokens", title_color="#0F766E", fontsize=7.8)
    # Right: BioCLIP + Purified Botanical Taxonomy
    draw_card(15.7, 25.0, 10.8, 8.0, c_purple_box, c_purple_brd,
              "BioCLIP ViT-B", r"$\mathbf{f}_{\mathrm{bio}} \in \mathbb{R}^{512}$",
              "+ Botanical Prompts", title_color=c_purple_txt, fontsize=7.8)

    draw_arrow(10.0, 36.2, 9.4, 33.0, color="#0D9488")
    draw_arrow(20.5, 36.2, 21.1, 33.0, color=c_purple_brd)

    # 4) Joint Manifold & Ledoit-Wolf Fisher-LDA
    draw_card(4.0, 12.0, 22.5, 9.5, c_amber_bg, c_amber_brd,
              r"Joint 896-d Manifold ($\mathcal{H}_{\mathrm{dino}} \oplus \mathcal{H}_{\mathrm{bio}}$)",
              r"Analytical Shrinkage: $\hat{\mathbf{\Sigma}} = (1-\rho^*)\mathbf{S}_W + \rho^* \nu \mathbf{I}_{896}$",
              r"Fisher Weights: $\mathbf{W} = \hat{\mathbf{\Sigma}}^{-1}[\boldsymbol{\mu}_1,\dots,\boldsymbol{\mu}_C]^T$",
              title_color=c_amber_txt, fontsize=7.8)

    draw_arrow(9.4, 25.0, 9.4, 21.5, color="#0D9488")
    draw_arrow(21.1, 25.0, 21.1, 21.5, color=c_purple_brd)

    # Output Arrow from Manifold into Tier 2 Companion (Clean gap between panels)
    draw_arrow(26.5, 16.75, 33.5, 16.75, color=c_amber_brd, lw=1.8,
               label=r"Fisher $(\mathbf{W}, \mathbf{b})$", label_pos=0.5, label_offset=(0, 1.4),
               label_color=c_amber_txt, label_bg="#FEFCE8", label_fs=7.0)

    # =========================================================================
    # 3. Stage II: Cascaded Dual-Tier Inference (Clean Left-to-Right Flow)
    # =========================================================================
    # A) Input Query Leaf
    draw_card(31.8, 41.5, 12.5, 7.5, "#F1F5F9", "#64748B",
              "Input Query Leaf", r"$x_q \in \mathbb{R}^{H \times W \times 3}$",
              "Field / UAV Leaf Photo", title_color="#1E293B", fontsize=7.8)

    # B) Container Tier 1: Standalone Fast-Path
    tier1_rect = patches.FancyBboxPatch((46.5, 35.5), 37.0, 15.8, boxstyle="round,pad=0.3,rounding_size=1.0",
                                        facecolor=c_green_bg, edgecolor=c_green_brd, linewidth=1.3, linestyle=":", zorder=2)
    ax.add_patch(tier1_rect)
    ax.text(65.0, 49.8, "TIER 1: STANDALONE FAST-PATH (APK BUNDLE, 22.05 MB INT8)",
            ha='center', va='center', fontsize=7.8, fontweight='bold', color=c_green_txt, zorder=4)

    # Inside Tier 1:
    # 1) DINOv2 Small Fast-Extractor
    draw_card(48.5, 37.5, 15.0, 10.2, "#FFFFFF", "#0D9488",
              "DINOv2 Small (INT8)", r"$\mathbf{f}_{\mathrm{dino}} \in \mathbb{R}^{384}$" + "\n" + r"Latency: 21.1 ms (CPU)",
              "Fast Spatial Feature", title_color="#0F766E", fontsize=7.8)
    draw_arrow(44.3, 45.2, 48.5, 45.2, color="#0D9488", lw=1.6)

    # 2) Shannon Margin-Entropy Gate
    draw_card(66.5, 37.5, 15.0, 10.2, c_amber_bg, c_amber_brd,
              r"Shannon Gate $\mathcal{C}(\mathbf{x})$",
              r"$\Delta p \cdot (1 - \tilde{\mathcal{H}}_{\mathrm{norm}})$" + "\n" + r"$\tau_{\mathrm{conf}} = 0.35$",
              "Uncertainty Metric", title_color=c_amber_txt, fontsize=7.8)
    draw_arrow(63.5, 42.6, 66.5, 42.6, color=c_amber_brd, lw=1.6)

    # C) Gating Routing:
    # Path 1: Fast-Exit Branch (Straight Right into Confident Exit)
    draw_card(86.0, 39.5, 10.5, 8.0, c_green_pill, c_green_brd,
              "Fast-Exit", "88.4% Queries", ">45 FPS | Confident",
              title_color=c_green_txt, fontsize=8.0)
    draw_arrow(81.5, 43.5, 86.0, 43.5, color=c_green_brd, lw=1.8,
               label=r"$\mathcal{C} \geq 0.35$", label_pos=0.48, label_offset=(0, 1.3),
               label_color=c_green_txt, label_bg="#F0FDF4")

    # D) Container Tier 2: On-Demand Deep Companion
    tier2_rect = patches.FancyBboxPatch((31.8, 4.5), 51.7, 26.5, boxstyle="round,pad=0.3,rounding_size=1.0",
                                        facecolor=c_purple_bg, edgecolor=c_purple_brd, linewidth=1.3, linestyle=":", zorder=2)
    ax.add_patch(tier2_rect)
    ax.text(57.65, 29.5, "TIER 2: ON-DEMAND DEEP COMPANION (83.57 MB INT8, 896-d FISHER + TRANSDUCTIVE)",
            ha='center', va='center', fontsize=7.6, fontweight='bold', color=c_purple_txt, zorder=4)

    # Path 2: Ambiguous Fallback Arrow from Shannon Gate down into Tier 2 (Label sits in empty band between boxes)
    draw_arrow(74.0, 37.5, 74.0, 23.5, color=c_purple_brd, lw=1.6, ls='--',
               label=r"$\mathcal{C} < 0.35$ (Ambiguous / 11.6%)", label_pos=0.42, label_offset=(-7.6, 0),
               label_color=c_purple_txt, label_bg="#FAF5FF")

    # Inside Tier 2:
    # 1) BioCLIP ViT-B Companion Extractor
    draw_card(33.5, 15.5, 13.5, 9.5, "#FFFFFF", c_purple_brd,
              "BioCLIP ViT-B (INT8)", r"$\mathbf{f}_{\mathrm{bio}} \in \mathbb{R}^{512}$",
              "Taxonomic Prior + Prompts", title_color=c_purple_txt, fontsize=7.6)
    # Feed from Query Leaf down into BioCLIP
    draw_arrow(38.0, 41.5, 38.0, 25.0, color="#64748B", lw=1.4, ls=':')

    # 2) 896-d Concatenation
    draw_card(49.5, 15.5, 14.5, 9.5, c_amber_bg, c_amber_brd,
              "896-d Concatenation", r"$\mathbf{z}_q = [\mathbf{f}_{\mathrm{bio}}, \mathbf{f}_{\mathrm{dino}}]$",
              "Joint Geometry", title_color=c_amber_txt, fontsize=7.8)
    draw_arrow(47.0, 20.25, 49.5, 20.25, color=c_purple_brd, lw=1.5)
    # Clean downward feed of f_dino from Tier 1 into Concatenation
    draw_arrow(56.0, 37.5, 56.0, 25.0, color="#0D9488", lw=1.4, ls=':')

    # 3) Fisher + Text Ensemble
    draw_card(66.5, 15.5, 15.0, 9.5, "#FFFFFF", "#0284C7",
              "Fisher + Text Blend", r"$\mathbf{p} = 0.75 \mathbf{p}_{\mathrm{fish}} + 0.25 \mathbf{p}_{\mathrm{text}}$",
              "Regularized Projection", title_color="#0369A1", fontsize=7.6)
    draw_arrow(64.0, 20.25, 66.5, 20.25, color=c_amber_brd, lw=1.5)

    # 4) Soft-Anchored Transductive Recalibration (Underneath Concatenation & Blend)
    draw_card(42.0, 6.0, 39.5, 7.5, c_purple_box, c_purple_brd,
              r"Soft-Anchored Transductive Recalibration ($3\times$ Anchor)",
              r"Online Buffer $\to$ Closed-Form $\hat{\mathbf{\Sigma}}^{\mathrm{trans}}$ & $\mathbf{W}^{\mathrm{trans}}$ Re-estimation (<22 ms)",
              "Resolves 5-Shot Prototype Shift Without Backprop",
              title_color=c_purple_txt, fontsize=7.6)
    draw_arrow(74.0, 15.5, 74.0, 13.5, color=c_purple_brd, lw=1.5)

    # E) Unified Final Decision & Calibrated Diagnosis Block (Far Right)
    draw_card(85.5, 6.0, 11.5, 26.5, "#F0FDF4", "#15803D",
              "Final Diagnostic\nDecision & ECE",
              "Peak Acc: 98.72%\nMean: 97.37%\nECE: 0.81%\n($T=0.50$)\n\nCross-Crop: 0.01%\nFN-Rate: 0.60%",
              "Calibrated Output",
              radius=1.0, lw=1.6, title_color="#14532D", sub_color="#166534", detail_color="#15803D", fontsize=7.8)

    # Fast-Exit connection down into Final Decision
    draw_arrow(91.25, 39.5, 91.25, 32.5, color="#16A34A", lw=1.8,
               label="Routine Path", label_pos=0.5, label_offset=(0, 0), label_color="#15803D", label_bg="#F0FDF4")

    # Transductive calibrated connection right into Final Decision
    draw_arrow(81.5, 9.75, 85.5, 9.75, color=c_purple_brd, lw=1.8,
               label="Deep Path", label_pos=0.5, label_offset=(0, 1.4), label_color=c_purple_txt, label_bg="#FAF5FF")

    # Save vector PDF and high-res raster PNG
    pdf_path = PAPER_DIR / "fig_architecture.pdf"
    png_path = PAPER_DIR / "fig_architecture.png"
    plt.savefig(pdf_path, format='pdf', bbox_inches='tight', pad_inches=0.04)
    plt.savefig(png_path, format='png', bbox_inches='tight', pad_inches=0.04, dpi=300)
    plt.close()
    print(f"[SUCCESS] Saved publication-grade {pdf_path} and {png_path}!")

if __name__ == "__main__":
    create_architecture_diagram()

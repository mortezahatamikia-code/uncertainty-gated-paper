# -*- coding: utf-8 -*-
"""
Generate an ultra-clean, publication-grade architecture diagram for BioDINO-Edge.
Completely eliminates all hidden, overlapping, or clipped text:
- Every container now has a crisp, dedicated top header banner (matching reference style).
- No floating subtitles that can collide with or hide under cards.
- 1.5 units of clean physical clearance between header banners and card tops.
- Dynamic, evenly-spaced text rendering inside all cards.
- Clean orthogonal (90-degree) routing with zero line crossings.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
import shutil

_curr = Path(__file__).resolve().parent
PROJECT_ROOT = _curr if (_curr / "paper").exists() else _curr.parent
PAPER_DIR = PROJECT_ROOT / "paper"
PAPER_DIR.mkdir(exist_ok=True)
WEB_FIG_DIR = PROJECT_ROOT / "web" / "public" / "figures"


def create_architecture_diagram():
    plt.rcParams.update({
        'font.sans-serif': 'DejaVu Sans',
        'font.family': 'sans-serif',
        'font.size': 8.5,
        'axes.labelsize': 9,
        'figure.titlesize': 11
    })

    fig = plt.figure(figsize=(16.0, 8.8), dpi=300)
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)

    # -------------------------------------------------------------------------
    # 0. Outer Canvas Framing
    # -------------------------------------------------------------------------
    outer_box = patches.Rectangle((0.6, 0.6), 98.8, 58.8, fill=False,
                                  edgecolor="#475569", linewidth=1.1, zorder=1)
    ax.add_patch(outer_box)

    # Helper: Draw container panels with solid top header banners
    def draw_container(x, y, w, h, bg, border, title,
                       banner_bg, banner_txt_color, banner_h=2.8, lw=1.4):
        # Outer panel
        panel = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15,rounding_size=0.8",
                                       facecolor=bg, edgecolor=border, linewidth=lw, zorder=2)
        ax.add_patch(panel)

        # Header banner pill
        banner = patches.FancyBboxPatch((x + 0.6, y + h - banner_h - 0.5), w - 1.2, banner_h,
                                        boxstyle="round,pad=0.12,rounding_size=0.45",
                                        facecolor=banner_bg, edgecolor=border, linewidth=0.9, zorder=3)
        ax.add_patch(banner)
        ax.text(x + w / 2, y + h - banner_h / 2 - 0.5, title, ha='center', va='center',
                fontsize=8.2, fontweight='bold', color=banner_txt_color, zorder=4)

    # Helper: Draw inner component cards with evenly distributed content
    def draw_card(x, y, w, h, bg, border, title="", items=None, radius=0.55, lw=1.0,
                  title_color="#0F172A", title_fs=7.5, zorder=4):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.15,rounding_size={radius}",
                                     facecolor=bg, edgecolor=border, linewidth=lw, zorder=zorder)
        ax.add_patch(box)

        if items is None:
            items = []

        total_elements = 1 + len(items) if title else len(items)
        if total_elements == 0:
            return

        step = h / (total_elements + 1)
        curr_y = y + h - step

        if title:
            ax.text(x + w / 2, curr_y, title, ha='center', va='center',
                    fontsize=title_fs, fontweight='bold', color=title_color, zorder=zorder + 1)
            curr_y -= step

        for text_str, color, fs, is_bold in items:
            ax.text(x + w / 2, curr_y, text_str, ha='center', va='center',
                    fontsize=fs, color=color, fontweight='bold' if is_bold else 'normal', zorder=zorder + 1)
            curr_y -= step

    # Helper: Draw straight arrow with centered label
    def draw_arrow(x1, y1, x2, y2, color="#DC2626", lw=1.4, ls='-',
                   label="", label_pos=0.5, label_offset=(0, 0),
                   label_color="#991B1B", label_bg="white", label_fs=6.7):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.26,head_length=0.38",
                                    color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0), zorder=6)
        if label:
            lx = x1 + (x2 - x1) * label_pos + label_offset[0]
            ly = y1 + (y2 - y1) * label_pos + label_offset[1]
            ax.text(lx, ly, label, ha='center', va='center', fontsize=label_fs,
                    color=label_color, fontweight='bold', zorder=7,
                    bbox=dict(boxstyle="round,pad=0.18", facecolor=label_bg, edgecolor=color, alpha=0.96, lw=0.7))

    # Helper: Draw 90-degree orthogonal elbow arrow
    def draw_elbow_arrow(x1, y1, x_corner, y_corner, x2, y2, color="#DC2626", lw=1.4, ls='-',
                         label="", label_offset=(0, 0),
                         label_color="#991B1B", label_bg="white", label_fs=6.7):
        ax.plot([x1, x_corner], [y1, y_corner], color=color, lw=lw, linestyle=ls, zorder=5)
        ax.annotate('', xy=(x2, y2), xytext=(x_corner, y_corner),
                    arrowprops=dict(arrowstyle="->,head_width=0.26,head_length=0.38",
                                    color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0), zorder=6)
        if label:
            lx = x_corner + label_offset[0]
            ly = y_corner + label_offset[1]
            ax.text(lx, ly, label, ha='center', va='center', fontsize=label_fs,
                    color=label_color, fontweight='bold', zorder=7,
                    bbox=dict(boxstyle="round,pad=0.18", facecolor=label_bg, edgecolor=color, alpha=0.96, lw=0.7))

    # =========================================================================
    # 1. COLUMN 1 (LEFT): Inputs (Top) & Calibration (Bottom)
    #    x = 2.0 to 23.0 (Width = 21.0)
    # =========================================================================

    # --- Box 1: Raw Inputs & Botanical Priors (Top-Left) ---
    # Container y: 33.5 to 58.0 (h = 24.5). Banner y: 54.7 to 57.5.
    # Cards occupy y = 34.6 to 52.8 -> Clean 1.9 unit clearance below banner!
    draw_container(x=2.0, y=33.5, w=21.0, h=24.5,
                   bg="#FEF9C3", border="#CA8A04",
                   title="RAW INPUTS & BOTANICAL PRIORS",
                   banner_bg="#FEF08A", banner_txt_color="#713F12")

    draw_card(3.0, 47.0, 19.0, 5.6, "#FFFFFF", "#EAB308",
              title="Few-Shot Support Foliage",
              items=[
                  (r"$\mathcal{S}_c = \{(\mathbf{x}_i, c)\}_{i=1}^5$ ($K=5$ Shots/Class)", "#334155", 6.8, False),
                  ("Clean Reference Images (PlantVillage)", "#854D0E", 6.5, False)
              ], title_color="#854D0E")

    draw_card(3.0, 40.8, 19.0, 5.6, "#FFFFFF", "#EAB308",
              title="Taxonomic Botanical Prompts",
              items=[
                  (r"$\{T_c^{(m)}\}_{m=1}^M$ (Host, Pathogen, Lesion)", "#334155", 6.8, False),
                  ("Affirmative Botanical Morphology", "#854D0E", 6.5, False)
              ], title_color="#854D0E")

    draw_card(3.0, 34.6, 19.0, 5.6, "#F8FAFC", "#94A3B8",
              title="Live Field Query Stream",
              items=[
                  (r"Un-augmented Leaf Photos ($\mathbf{x}_q$)", "#0F172A", 6.8, False),
                  ("Streaming Camera / Drone Video Input", "#475569", 6.5, False)
              ], title_color="#0F172A")

    # --- Box 2: Support Calibration Engine (Bottom-Left) ---
    # Container y: 2.0 to 30.5 (h = 28.5). Banner y: 27.2 to 30.0.
    # Cards occupy y = 2.8 to 25.1 -> Clean 2.1 unit clearance below banner!
    draw_container(x=2.0, y=2.0, w=21.0, h=28.5,
                   bg="#FFF7ED", border="#EA580C",
                   title="SUPPORT CALIBRATION ENGINE (<50 ms)",
                   banner_bg="#FED7AA", banner_txt_color="#9A3412")

    draw_card(3.0, 19.5, 19.0, 5.6, "#FFFFFF", "#FB923C",
              title=r"8$\times$ Multi-View Augmentation",
              items=[
                  (r"Spatial Affine ($\pm 15^\circ$) + Photometric Jitter (0.2)", "#334155", 6.7, False),
                  (r"Expands 5 Support Leaves $\to N=440$ Views", "#C2410C", 6.6, True)
              ], title_color="#C2410C")

    # Arrow from Support Input down into Augmentation in the 3.0-unit gap
    draw_arrow(12.5, 33.5, 12.5, 25.1, color="#EA580C", lw=1.4,
               label="Support Exemplars", label_pos=0.5, label_offset=(0, 0),
               label_color="#C2410C", label_bg="#FFF7ED", label_fs=6.6)

    # Correction 3: Terminology Fix (Joint Representation Z in R^{440 x 896})
    draw_card(3.0, 11.2, 19.0, 7.3, "#FFFFFF", "#F97316",
              title="Dual Foundation Extraction",
              items=[
                  ("DINOv2 Small (384-d) + BioCLIP ViT-B (512-d)", "#334155", 6.7, False),
                  (r"Joint Representation: $\mathbf{Z} \in \mathbb{R}^{440 \times 896}$", "#9A3412", 7.0, True),
                  ("Concatenated Foliar Embedding Matrix", "#64748B", 6.5, False)
              ], title_color="#9A3412")

    draw_arrow(12.5, 19.5, 12.5, 18.5, color="#EA580C", lw=1.3)

    draw_card(3.0, 2.8, 19.0, 7.4, "#FEFCE8", "#CA8A04",
              title="Ledoit-Wolf & Fisher-LDA",
              items=[
                  (r"Exact Covariance Shrinkage: $\hat{\mathbf{\Sigma}}^{-1}$", "#334155", 6.8, False),
                  (r"Solved Projection: $(\mathbf{W}, \mathbf{b})$ ($<50$ ms)", "#A16207", 7.0, True),
                  ("Closed-Form Solution | Zero Backpropagation", "#64748B", 6.5, False)
              ], title_color="#A16207")

    draw_arrow(12.5, 11.2, 12.5, 10.2, color="#CA8A04", lw=1.3)

    # =========================================================================
    # 2. COLUMN 2 (CENTER): Cascaded Inference & Recalibration
    #    x = 27.5 to 74.0 (Width = 46.5)
    #    Gutter 1 on left (x=23.0 to 27.5, Width=4.5)
    # =========================================================================

    # --- Box 3: Tier-1 Edge Fast Path (Top-Center) ---
    # Container y: 40.0 to 58.0 (h = 18.0). Banner y: 54.7 to 57.5.
    # Cards occupy y = 41.2 to 53.0 -> Clean 1.7 unit clearance below banner!
    draw_container(x=27.5, y=40.0, w=46.5, h=18.0,
                   bg="#F0FDF4", border="#16A34A",
                   title="TIER-1 EDGE FAST PATH (REAL-TIME SYSTEM 1)",
                   banner_bg="#BBF7D0", banner_txt_color="#14532D")

    draw_card(28.7, 41.2, 13.6, 11.8, "#FFFFFF", "#16A34A",
              title="DINOv2 Small (INT8)",
              items=[
                  (r"$\mathbf{f}_{\mathrm{dino}} \in \mathbb{R}^{384}$ (Patch 14)", "#15803D", 6.8, True),
                  ("Latency: 21.1 ms on CPU", "#334155", 6.6, False),
                  ("Microscopic Lesion Details", "#64748B", 6.5, False)
              ], title_color="#15803D")

    # Correction 1: Fast Fisher-LDA Projection
    draw_card(43.5, 41.2, 14.5, 11.8, "#FFFFFF", "#10B981",
              title="Fast Fisher-LDA Projection",
              items=[
                  (r"$\mathbf{p}_{\mathrm{fast}} = \mathrm{softmax}(\mathbf{W}_{\mathrm{dino}} \mathbf{f}_{\mathrm{dino}} + \mathbf{b}_{\mathrm{dino}})$", "#047857", 6.8, True),
                  ("Precomputed 384-d Parameters", "#334155", 6.6, False),
                  ("Fast Class Posteriors", "#64748B", 6.5, False)
              ], title_color="#047857", title_fs=7.3)

    draw_arrow(42.3, 47.1, 43.5, 47.1, color="#10B981", lw=1.4)

    # Correction 4 (Clarification): Main Routing Gate tau_conf = 0.35
    draw_card(59.2, 41.2, 13.6, 11.8, "#FEFCE8", "#CA8A04",
              title=r"Main Routing Gate $\mathcal{C}(\mathbf{x})$",
              items=[
                  (r"$\mathcal{C} = \Delta p \cdot (1 - \mathcal{H}_{\mathrm{norm}})$", "#A16207", 6.9, True),
                  (r"$\tau_{\mathrm{conf}} = 0.35$ (Routing Cutoff)", "#C2410C", 6.7, True),
                  ("Routes: Fast-Exit vs Tier-2", "#64748B", 6.5, False)
              ], title_color="#A16207")

    draw_arrow(58.0, 47.1, 59.2, 47.1, color="#CA8A04", lw=1.4)

    # Wire 1: Live Query from Col 1 up into Tier-1 (Runs cleanly in Gutter 1)
    ax.plot([23.0, 25.2], [37.4, 37.4], color="#2563EB", lw=1.5, zorder=5)
    ax.plot([25.2, 25.2], [37.4, 47.1], color="#2563EB", lw=1.5, zorder=5)
    ax.annotate('', xy=(28.7, 47.1), xytext=(25.2, 47.1),
                arrowprops=dict(arrowstyle="->,head_width=0.26,head_length=0.38",
                                color="#2563EB", lw=1.5, shrinkA=0, shrinkB=0), zorder=6)
    ax.text(25.2, 42.2, "Live Query", ha='center', va='center', fontsize=6.7,
            color="#1D4ED8", fontweight='bold', zorder=7,
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#EFF6FF", edgecolor="#2563EB", lw=0.7))

    # --- Box 4: Tier-2 Deep Escalation (Middle-Center) ---
    # Container y: 21.0 to 37.0 (h = 16.0). Banner y: 33.7 to 36.5.
    # Cards occupy y = 22.2 to 32.2 -> Clean 1.5 unit clearance below banner!
    draw_container(x=27.5, y=21.0, w=46.5, h=16.0,
                   bg="#FAF5FF", border="#9333EA",
                   title="TIER-2 DEEP ESCALATION (MULTIMODAL SYSTEM 2)",
                   banner_bg="#E9D5FF", banner_txt_color="#581C87")

    draw_card(28.7, 22.2, 13.6, 10.0, "#FFFFFF", "#9333EA",
              title="BioCLIP ViT-B (INT8)",
              items=[
                  (r"$\mathbf{f}_{\mathrm{bio}} \in \mathbb{R}^{512}$ (ViT-B/16)", "#7E22CE", 6.8, True),
                  ("Evolutionary & Botanical Priors", "#334155", 6.6, False),
                  ("On-Demand Multimodal Encoding", "#64748B", 6.5, False)
              ], title_color="#7E22CE")

    draw_card(43.5, 22.2, 14.5, 10.0, "#FEFCE8", "#CA8A04",
              title="896-D Feature Fusion",
              items=[
                  (r"$\mathbf{z}_q = [\mathbf{f}_{\mathrm{bio}} \,\|\, \mathbf{f}_{\mathrm{dino}}]$", "#A16207", 6.9, True),
                  (r"Reuses Cached Fast $\mathbf{f}_{\mathrm{dino}}$", "#334155", 6.6, False),
                  ("Zero Redundant Computation", "#64748B", 6.5, False)
              ], title_color="#A16207")

    draw_arrow(42.3, 27.2, 43.5, 27.2, color="#CA8A04", lw=1.4)

    # Correction 2: Total Latency: 42.9 ms (CPU) and p_blend = 0.75 p_fisher + 0.25 p_text
    draw_card(59.2, 22.2, 13.6, 10.0, "#FFFFFF", "#0284C7",
              title="Fisher Projection & Blend",
              items=[
                  (r"$\mathbf{l}_{\mathrm{fish}} = \mathbf{z}_q \mathbf{W}^T + \mathbf{b}$", "#0369A1", 6.7, False),
                  (r"$\mathbf{p}_{\mathrm{blend}} = 0.75 \mathbf{p}_{\mathrm{fish}} + 0.25 \mathbf{p}_{\mathrm{text}}$", "#0284C7", 6.6, True),
                  ("Total Latency: 42.9 ms (CPU)", "#1E293B", 6.6, True)
              ], title_color="#0369A1", title_fs=7.2)

    draw_arrow(58.0, 27.2, 59.2, 27.2, color="#0284C7", lw=1.4)

    # Wire 2: Ambiguous Fallback from Tier-1 down into Tier-2 (Straight Vertical in Gutter)
    draw_arrow(66.0, 41.2, 66.0, 36.5, color="#9333EA", lw=1.5, ls="--",
               label=r"Ambiguous: $\mathcal{C}(\mathbf{x}) < 0.35$ (11.6%)",
               label_pos=0.5, label_offset=(0, 0), label_color="#7E22CE", label_bg="#FAF5FF", label_fs=6.6)

    # Wire 3: Fisher Weights (W, b) from Calibration to Tier-2 (Runs in Gutter 1)
    ax.plot([23.0, 25.2], [6.5, 6.5], color="#EA580C", lw=1.4, linestyle=":", zorder=5)
    ax.plot([25.2, 25.2], [6.5, 27.2], color="#EA580C", lw=1.4, linestyle=":", zorder=5)
    ax.annotate('', xy=(28.7, 27.2), xytext=(25.2, 27.2),
                arrowprops=dict(arrowstyle="->,head_width=0.26,head_length=0.38",
                                color="#EA580C", lw=1.4, linestyle=":", shrinkA=0, shrinkB=0), zorder=6)
    ax.text(25.2, 16.8, r"Fisher $(\mathbf{W}, \mathbf{b})$", ha='center', va='center', fontsize=6.7,
            color="#C2410C", fontweight='bold', zorder=7,
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#FFF7ED", edgecolor="#EA580C", lw=0.7))

    # --- Box 5: Soft-Anchored Recalibration Engine (Bottom-Center) ---
    # Container y: 2.0 to 18.0 (h = 16.0). Banner y: 14.7 to 17.5.
    # Cards occupy y = 3.2 to 13.2 -> Clean 1.5 unit clearance below banner!
    draw_container(x=27.5, y=2.0, w=46.5, h=16.0,
                   bg="#F0F9FF", border="#0284C7",
                   title="SOFT-ANCHORED RECALIBRATION ENGINE",
                   banner_bg="#BAE6FD", banner_txt_color="#075985")

    # Correction 4: Anchor Gate C(x) >= 0.70 distinctly highlighted from tau_conf = 0.35
    draw_card(28.7, 3.2, 13.6, 10.0, "#E0F2FE", "#0284C7",
              title="On-Device FIFO Buffer",
              items=[
                  (r"Anchor Gate: $\mathcal{C}(\mathbf{x}) \geq 0.70$", "#0369A1", 6.8, True),
                  ("Top-20 Pseudo-Anchors / Class", "#334155", 6.6, False),
                  ("Strict High-Confidence Filter", "#64748B", 6.5, False)
              ], title_color="#0369A1", title_fs=7.2)

    draw_card(43.5, 3.2, 14.5, 10.0, "#FEFCE8", "#CA8A04",
              title=r"Soft-Anchoring ($3\times$ Weight)",
              items=[
                  (r"$\tilde{\mathcal{S}}_c^{\mathrm{trans}} = (\tilde{\mathcal{S}}_c \otimes 3) \cup \mathcal{Q}_{\mathrm{anc}}$", "#A16207", 6.8, True),
                  ("Canonical Support Protected", "#334155", 6.6, False),
                  ("Prevents Label Noise Drift", "#64748B", 6.5, False)
              ], title_color="#A16207")

    draw_arrow(42.3, 8.2, 43.5, 8.2, color="#CA8A04", lw=1.4)

    draw_card(59.2, 3.2, 13.6, 10.0, "#FFFFFF", "#16A34A",
              title="Closed-Form Update",
              items=[
                  (r"Re-estimates $\hat{\mathbf{\Sigma}}^{\mathrm{trans}}$ \& $\mathbf{W}^{\mathrm{trans}}$", "#15803D", 6.8, True),
                  ("Runs in <22 ms on Edge CPU", "#334155", 6.6, False),
                  ("Zero Gradient Retraining", "#64748B", 6.5, False)
              ], title_color="#15803D")

    draw_arrow(58.0, 8.2, 59.2, 8.2, color="#16A34A", lw=1.4)

    # Wire 4: High-Confidence Anchors from Tier-2 down into Buffer (in Gutter)
    draw_arrow(35.5, 22.2, 35.5, 17.5, color="#0284C7", lw=1.4, ls="--",
               label=r"Anchor Filter: $\mathcal{C}(\mathbf{x}) \geq 0.70$",
               label_pos=0.5, label_offset=(0, 0), label_color="#0369A1", label_bg="#F0F9FF", label_fs=6.6)

    # Correction 4 (Visual Flow): Arrow pointing from Closed-Form Update UP into Tier-2 labeled "Updates Tier-2 Boundaries"
    draw_arrow(66.0, 13.2, 66.0, 22.2, color="#059669", lw=1.6, ls=":",
               label="Updates Tier-2 Boundaries", label_pos=0.5, label_offset=(0, 0),
               label_color="#047857", label_bg="#ECFDF5", label_fs=6.6)

    # =========================================================================
    # 3. COLUMN 3 (RIGHT): Field Diagnostic Output
    #    x = 78.5 to 98.0 (Width = 19.5, Height = 56.0)
    #    Gutter 2 on left (x=74.0 to 78.5, Width=4.5)
    # =========================================================================
    draw_container(x=78.5, y=2.0, w=19.5, h=56.0,
                   bg="#ECFDF5", border="#059669",
                   title="FIELD DIAGNOSTIC OUTPUT",
                   banner_bg="#059669", banner_txt_color="#FFFFFF", lw=1.6)

    # Card 6.1 (Top): Immediate Live Classification
    draw_card(79.7, 41.2, 17.1, 11.8, "#FFFFFF", "#10B981",
              title="Immediate Live Classification",
              items=[
                  ("Fast-Exit (Tier-1): 21.1 ms (>45 FPS)", "#047857", 6.8, True),
                  ("Deep-Path (Tier-2): 42.9 ms (23 FPS)", "#0369A1", 6.8, True),
                  ("Real-time Foliar Diagnosis On-Device", "#334155", 6.6, False)
              ], title_color="#047857")

    # Wire 5: Tier-1 Fast-Exit straight into Immediate Classification
    draw_arrow(72.8, 47.1, 79.7, 47.1, color="#16A34A", lw=1.6,
               label=r"Fast-Exit ($\mathcal{C} \geq 0.35$ | 88.4%)",
               label_pos=0.5, label_offset=(0, 1.4), label_color="#15803D", label_bg="#F0FDF4", label_fs=6.6)

    # Wire 6: Tier-2 Deep Result straight into Immediate Classification
    draw_elbow_arrow(72.8, 27.2, 76.2, 27.2, 79.7, 44.0, color="#0284C7", lw=1.5,
                     label="Deep Consensus (11.6%)", label_offset=(0, 1.2),
                     label_color="#0369A1", label_bg="#F0F9FF", label_fs=6.6)

    # Card 6.2 (Middle): Continuous Session Adaptation
    draw_card(79.7, 24.2, 17.1, 14.0, "#FFFFFF", "#0284C7",
              title="Session Adaptation Log",
              items=[
                  ("Recalibrates Decision Boundaries", "#0369A1", 6.8, True),
                  ("Applied to Subsequent Video Frames", "#334155", 6.6, False),
                  ("Refines Full Agricultural Survey Log", "#334155", 6.6, False),
                  ("Continuous On-Device Adaptation", "#047857", 6.5, True)
              ], title_color="#0369A1")

    # Wire 7: Updated Hyperplanes from Recalibration into Session Log
    draw_elbow_arrow(72.8, 8.2, 76.2, 8.2, 79.7, 30.5, color="#059669", lw=1.5,
                     label=r"Updated $\mathbf{W}^{\mathrm{trans}}$ (<22 ms)", label_offset=(0, 1.2),
                     label_color="#047857", label_bg="#ECFDF5", label_fs=6.6)

    # Card 6.3 (Bottom): Validated Hardware Benchmark Specs
    draw_card(79.7, 3.0, 17.1, 18.5, "#064E3B", "#047857",
              title="Validated Benchmark Specs",
              items=[
                  ("Peak Accuracy: 98.72%", "#A7F3D0", 7.0, True),
                  ("Mean Accuracy: 97.37% (PlantVillage)", "#FFFFFF", 6.8, True),
                  ("Calibration ECE: 0.81% | FPS: 47.4", "#E2E8F0", 6.6, False),
                  (r"Memory Budget: $\leq$ 110 MB", "#6EE7B7", 6.8, True),
                  ("APK Size: 22.7 MB (INT8)", "#E2E8F0", 6.6, False),
                  ("100% Offline Edge CPU Execution", "#A7F3D0", 6.7, True)
              ], title_color="#A7F3D0", title_fs=7.6)

    # Save vector PDF and high-res raster PNG
    pdf_path = PAPER_DIR / "fig_architecture.pdf"
    png_path = PAPER_DIR / "fig_architecture.png"
    plt.savefig(pdf_path, format='pdf', bbox_inches='tight', pad_inches=0.03)
    plt.savefig(png_path, format='png', bbox_inches='tight', pad_inches=0.03, dpi=300)
    plt.close()

    if WEB_FIG_DIR.exists():
        shutil.copy2(png_path, WEB_FIG_DIR / "fig_architecture.png")

    print(f"[SUCCESS] Saved publication-grade {pdf_path} and {png_path}!")


if __name__ == "__main__":
    create_architecture_diagram()

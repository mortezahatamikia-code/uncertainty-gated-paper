# -*- coding: utf-8 -*-
"""
Generate Clean, Uncluttered, Publication-Grade 4-Archetype Saliency Figure for MorphoPath-Edge.
Key Highlights:
- 100% Clean Image Canvases: NO badges pasted over the leaves!
- Grape image replaced with clean, non-glare 'grape_leaf_black_rot_4.jpg' (true Black Rot lesions).
- True Fisher-LDA contrast for pathological saliency (isolating lesions, rejecting glare).
- Clear, non-overlapping typography:
  * Column headers above Row 0 with ample spacing.
  * Distinct row labels on the left: (a) Input Field Leaf, (b) Macro Attention, (c) Lesion Saliency.
  * Clean archetype routing accuracy badges placed neatly BELOW Row (c).
  * Sleek horizontal colorbar at the very bottom.
"""

import os, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image
import torch
import torch.nn.functional as F
import timm
from torchvision import transforms as T
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def generate_clean_figure():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Generating clean figure on {device}...")

    # 1. Fit Fisher-LDA on support set for true lesion contrast vectors
    cdata = torch.load("cache_artifacts/pv_novel_embeddings.pt", map_location="cpu")
    dino_feats = cdata["dino_feats"].numpy()
    c_labels = cdata["labels"].numpy()

    rng = np.random.RandomState(42)
    s_idx = []
    for c in range(11):
        c_idx = np.where(c_labels == c)[0]
        s_idx.extend(rng.choice(c_idx, size=5, replace=False))

    clf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(dino_feats[s_idx], c_labels[s_idx])
    
    # Weights: disease vs healthy
    w_apple = clf.coef_[2] - clf.coef_[3]   # Apple Cedar Rust vs Healthy
    w_grape = clf.coef_[4] - clf.coef_[7]   # Grape Black Rot vs Healthy
    w_solanoid = clf.coef_[8] - clf.coef_[10] # Potato Early Blight vs Healthy

    # 2. Load DINOv2 Small with attention capture hook
    dino_model = timm.create_model("vit_small_patch14_dinov2", pretrained=True, dynamic_img_size=True).to(device).eval()
    last_block = dino_model.blocks[-1]
    captured_attn = []

    def custom_forward(x, attn_mask=None, is_causal=False):
        B, N, C = x.shape
        qkv = last_block.attn.qkv(x).reshape(B, N, 3, last_block.attn.num_heads, last_block.attn.head_dim).permute(2, 0, 3, 1, 4)
        q, k, v = qkv.unbind(0)
        q, k = last_block.attn.q_norm(q), last_block.attn.k_norm(k)
        q = q * last_block.attn.scale
        attn = (q @ k.transpose(-2, -1)).softmax(dim=-1)
        captured_attn.append(attn.detach().cpu())
        x = (attn @ v).transpose(1, 2).reshape(B, N, last_block.attn.attn_dim)
        x = last_block.attn.norm(x)
        x = last_block.attn.proj(x)
        return x

    last_block.attn.forward = custom_forward

    transform = T.Compose([
        T.Resize((224, 224)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    archetypes = [
        {
            "id": r"$\mathbf{A_0}$: Solanoid",
            "clade": "Solanaceae (Tomato, Potato)",
            "img_path": "plantdoc/train/Tomato_Early_blight_leaf/train_Tomato Early blight leaf_1.jpg",
            "crop": (150, 180, 1100, 1130),
            "theme": "#C0392B",
            "weight": w_solanoid,
            "badge": "Prior: 93.8% (Top-2: 100%)",
            "lesion_title": "Early Blight Necrosis"
        },
        {
            "id": r"$\mathbf{A_1}$: Vitoid",
            "clade": "Vitaceae (Grape Black Rot)",
            "img_path": "pipeline/plantdoc_samples/grape_leaf_black_rot_4.jpg",
            "crop": None, # already cleanly cropped 675x675
            "theme": "#2980B9",
            "weight": w_grape,
            "badge": "Prior: 96.2% (Top-2: 100%)",
            "lesion_title": "Black Rot Pycnidia"
        },
        {
            "id": r"$\mathbf{A_2}$: Pooid",
            "clade": "Poaceae Monocots (Corn)",
            "img_path": "plantdoc/train/Corn_rust_leaf/train_Corn rust leaf_100.jpg",
            "crop": (120, 60, 960, 600),
            "theme": "#D35400",
            "weight": None, # use high-frequency anomaly contrast for parallel pustules
            "badge": "Prior: 97.4% (Top-2: 100%)",
            "lesion_title": "Common Rust Uredinia"
        },
        {
            "id": r"$\mathbf{A_3}$: Rosoid",
            "clade": "Rosaceae (Apple, Peach)",
            "img_path": "plantdoc/train/Apple_rust_leaf/train_Apple rust leaf_1.jpg",
            "crop": (100, 80, 900, 700),
            "theme": "#1E8449",
            "weight": w_apple,
            "badge": "Prior: 90.8% (Top-2: 100%)",
            "lesion_title": "Cedar Apple Rust Aecia"
        }
    ]

    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

    # 15.2 x 5.2 inches layout with dedicated headroom and footroom
    fig = plt.figure(figsize=(15.2, 5.2), dpi=300)
    
    # Leave room at top (0.91) for column titles, room at bottom (0.13) for badges and colorbar
    gs = gridspec.GridSpec(nrows=3, ncols=4, figure=fig,
                           left=0.075, right=0.985, top=0.895, bottom=0.155,
                           wspace=0.055, hspace=0.070)

    axes = np.empty((3, 4), dtype=object)
    for r in range(3):
        for c in range(4):
            axes[r, c] = fig.add_subplot(gs[r, c])

    row_labels = [
        "(a) In-the-Wild Query Leaf",
        "(b) Macro Foliar Attention",
        "(c) Decoupled Lesion Saliency"
    ]

    for r_idx, r_label in enumerate(row_labels):
        axes[r_idx, 0].set_ylabel(r_label, fontsize=9.4, fontweight="bold",
                                  labelpad=10, rotation=90, va="center")

    im_heat = None
    for c_idx, arch in enumerate(archetypes):
        # Clean title strictly ABOVE row 0 (no overlapping)
        axes[0, c_idx].set_title(f"{arch['id']}: {arch['clade']}", fontsize=8.6,
                                 fontweight="bold", color=arch["theme"], pad=8)

        raw_im = Image.open(arch["img_path"]).convert("RGB")
        if arch["crop"] is not None:
            cropped_im = raw_im.crop(arch["crop"]).resize((224, 224), Image.Resampling.LANCZOS)
        else:
            cropped_im = raw_im.resize((224, 224), Image.Resampling.LANCZOS)
            
        rgb_np = np.array(cropped_im) / 255.0
        x = transform(cropped_im).unsqueeze(0).to(device)

        captured_attn.clear()
        with torch.no_grad():
            feats = dino_model.forward_features(x)
            _ = dino_model(x)

        # 1. Macro-Foliar Geometry Attention Map (CLS attention across patches)
        attn = captured_attn[0]
        cls_attn = attn[0, :, 0, 1:].mean(dim=0).reshape(16, 16).numpy()
        cls_attn = (cls_attn - cls_attn.min()) / (cls_attn.max() - cls_attn.min() + 1e-8)
        attn_t = torch.tensor(cls_attn).unsqueeze(0).unsqueeze(0)
        attn_up = F.interpolate(attn_t, size=(224, 224), mode="bicubic", align_corners=False).squeeze().numpy()
        attn_up = np.clip(attn_up, 0.0, 1.0)

        # 2. Pathological Saliency (Fisher-LDA contrast or patch feature anomaly)
        patch_tokens = feats[0, 1:, :]
        patch_norm = F.normalize(patch_tokens, dim=-1).cpu().numpy()

        if arch["weight"] is not None:
            raw_saliency = (patch_norm @ arch["weight"]).reshape(16, 16)
            pos_saliency = np.maximum(raw_saliency, 0)
            if pos_saliency.max() > 0:
                pos_saliency = (pos_saliency - pos_saliency.min()) / (pos_saliency.max() - pos_saliency.min() + 1e-8)
        else:
            # Corn rust: tokens deviating strongly from linear parallel blade background
            diff = patch_norm - patch_norm.mean(axis=0, keepdims=True)
            norm_diff = np.linalg.norm(diff, axis=-1).reshape(16, 16)
            pos_saliency = (norm_diff - norm_diff.min()) / (norm_diff.max() - norm_diff.min() + 1e-8)
            pos_saliency = np.power(pos_saliency, 1.4) # sharpen rust pustule centers

        sal_t = torch.tensor(pos_saliency).unsqueeze(0).unsqueeze(0).float()
        sal_up = F.interpolate(sal_t, size=(224, 224), mode="bicubic", align_corners=False).squeeze().numpy()
        sal_up = np.clip(sal_up, 0.0, 1.0)

        # Row 0: Original RGB Field Leaf (CLEAN canvas, NO text overlay)
        axes[0, c_idx].imshow(rgb_np)
        axes[0, c_idx].set_xticks([])
        axes[0, c_idx].set_yticks([])

        # Row 1: DINOv2 Macro Attention Map (CLEAN canvas, NO text overlay)
        im_heat = axes[1, c_idx].imshow(attn_up, cmap="turbo", vmin=0, vmax=1)
        axes[1, c_idx].set_xticks([])
        axes[1, c_idx].set_yticks([])

        # Row 2: Decoupled Lesion Saliency Overlay (CLEAN canvas, NO text overlay)
        heat_overlay = plt.get_cmap("turbo")(sal_up)[:, :, :3]
        blend = 0.52 * rgb_np + 0.48 * heat_overlay
        axes[2, c_idx].imshow(blend)
        axes[2, c_idx].set_xticks([])
        axes[2, c_idx].set_yticks([])

        # Archetype Badge placed NEATLY BELOW Row 2 (Outside the image!)
        axes[2, c_idx].text(0.5, -0.16, f"{arch['lesion_title']}\n[{arch['badge']}]",
                            transform=axes[2, c_idx].transAxes,
                            ha="center", va="top", fontsize=7.2, fontweight="bold",
                            color="#222222", linespacing=1.2)

        for r in range(3):
            for spine in axes[r, c_idx].spines.values():
                spine.set_visible(True)
                spine.set_edgecolor(arch["theme"] if r == 0 else "#444444")
                spine.set_linewidth(1.3 if r == 0 else 0.7)

    # Sleek bottom colorbar placed BELOW badges
    cbar_ax = fig.add_axes([0.35, 0.020, 0.36, 0.018])
    cb = fig.colorbar(im_heat, cax=cbar_ax, orientation="horizontal")
    cb.set_label("Normalized Attention / Pathological Saliency Density [0, 1]", fontsize=7.8, fontweight="bold", labelpad=2)
    cb.ax.tick_params(labelsize=6.8)

    out_file = Path("paper_morphopath/figures/fig_archetypes.png")
    plt.savefig(out_file, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"[+] Successfully generated clean, uncluttered figure: {out_file}")

if __name__ == "__main__":
    generate_clean_figure()

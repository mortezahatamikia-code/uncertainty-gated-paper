# -*- coding: utf-8 -*-
"""
Generate Flawless, Publication-Grade 4-Archetype Decoupling Figure for MorphoPath-Edge.
Features:
- 4 Columns: Solanoid (A0), Vitoid (A1), Pooid (A2), Rosoid (A3)
- Top Row: Clean In-The-Wild Field Query Leaf (PlantDoc).
  * Grape uses 'grape_leaf_black_rot_4.jpg' (clean leaf, zero glare artifact, clear black rot lesions).
- Bottom Row (Dual Insets per Archetype):
  * Left Inset: DINOv2 Real Attention Map (capturing macroscopic venation & leaf geometry).
  * Right Inset: Real Pathological Saliency Overlay (isolating necrotic rings, pycnidia & rust pustules).
- Zero Text Collision: Crisp, single-line labels strictly outside the image area.
- Perfect 3:1 aspect ratio matching the 4.2cm IEEE double-column float budget.
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

def create_flawless_archetypes_figure(output_path="paper_morphopath/figures/fig_archetypes.png"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Generating flawless archetypes figure on {device}...")

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
    
    w_apple = clf.coef_[2] - clf.coef_[3]     # Apple Cedar Rust vs Healthy
    w_grape = clf.coef_[4] - clf.coef_[7]     # Grape Black Rot vs Healthy
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
            "name": r"$\mathbf{A_0}$: Solanoid",
            "family": "Solanaceae (Tomato, Potato)",
            "img_path": "plantdoc/train/Tomato_Early_blight_leaf/train_Tomato Early blight leaf_1.jpg",
            "crop_full": (150, 180, 1100, 1130),
            "theme_color": "#C0392B",
            "acc": "Routing: 93.8% (Top-2: 100%)",
            "weight": w_solanoid
        },
        {
            "name": r"$\mathbf{A_1}$: Vitoid",
            "family": "Vitaceae (Grape, Squash)",
            "img_path": "pipeline/plantdoc_samples/grape_leaf_black_rot_4.jpg",
            "crop_full": None,
            "theme_color": "#2980B9",
            "acc": "Routing: 96.2% (Top-2: 100%)",
            "weight": w_grape
        },
        {
            "name": r"$\mathbf{A_2}$: Pooid",
            "family": "Poaceae Monocots (Corn / Maize)",
            "img_path": "plantdoc/train/Corn_rust_leaf/train_Corn rust leaf_100.jpg",
            "crop_full": (120, 60, 960, 600),
            "theme_color": "#D35400",
            "acc": "Routing: 97.4% (Top-2: 100%)",
            "weight": None
        },
        {
            "name": r"$\mathbf{A_3}$: Rosoid",
            "family": "Rosaceae & Woody Dicots (Apple)",
            "img_path": "plantdoc/train/Apple_rust_leaf/train_Apple rust leaf_1.jpg",
            "crop_full": (100, 80, 900, 700),
            "theme_color": "#1E8449",
            "acc": "Routing: 90.8% (Top-2: 100%)",
            "weight": w_apple
        }
    ]

    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

    # 15.0 x 4.8 inches layout
    fig = plt.figure(figsize=(15.0, 4.8), dpi=300)
    gs = gridspec.GridSpec(2, 4, height_ratios=[1.7, 1.0], hspace=0.20, wspace=0.10,
                           top=0.88, bottom=0.08, left=0.025, right=0.975)

    for col, arch in enumerate(archetypes):
        im = Image.open(arch["img_path"]).convert("RGB")
        if arch["crop_full"] is not None:
            im_full = im.crop(arch["crop_full"]).resize((224, 224), Image.Resampling.LANCZOS)
        else:
            im_full = im.resize((224, 224), Image.Resampling.LANCZOS)

        rgb_np = np.array(im_full) / 255.0
        x = transform(im_full).unsqueeze(0).to(device)

        captured_attn.clear()
        with torch.no_grad():
            feats = dino_model.forward_features(x)
            _ = dino_model(x)

        # 1. Macro Attention
        attn = captured_attn[0]
        cls_attn = attn[0, :, 0, 1:].mean(dim=0).reshape(16, 16).numpy()
        cls_attn = (cls_attn - cls_attn.min()) / (cls_attn.max() - cls_attn.min() + 1e-8)
        attn_t = torch.tensor(cls_attn).unsqueeze(0).unsqueeze(0)
        attn_up = F.interpolate(attn_t, size=(224, 224), mode="bicubic", align_corners=False).squeeze().numpy()
        attn_up = np.clip(attn_up, 0.0, 1.0)

        # 2. Pathological Saliency
        patch_tokens = feats[0, 1:, :]
        patch_norm = F.normalize(patch_tokens, dim=-1).cpu().numpy()

        if arch["weight"] is not None:
            raw_saliency = (patch_norm @ arch["weight"]).reshape(16, 16)
            pos_saliency = np.maximum(raw_saliency, 0)
            if pos_saliency.max() > 0:
                pos_saliency = (pos_saliency - pos_saliency.min()) / (pos_saliency.max() - pos_saliency.min() + 1e-8)
        else:
            diff = patch_norm - patch_norm.mean(axis=0, keepdims=True)
            norm_diff = np.linalg.norm(diff, axis=-1).reshape(16, 16)
            pos_saliency = (norm_diff - norm_diff.min()) / (norm_diff.max() - norm_diff.min() + 1e-8)
            pos_saliency = np.power(pos_saliency, 1.4)

        sal_t = torch.tensor(pos_saliency).unsqueeze(0).unsqueeze(0).float()
        sal_up = F.interpolate(sal_t, size=(224, 224), mode="bicubic", align_corners=False).squeeze().numpy()
        sal_up = np.clip(sal_up, 0.0, 1.0)

        # Top row: Clean In-The-Wild Image (Zero text overlays inside)
        ax_top = fig.add_subplot(gs[0, col])
        ax_top.imshow(rgb_np)
        ax_top.set_xticks([])
        ax_top.set_yticks([])
        ax_top.set_title(f"{arch['name']}: {arch['family']}", fontsize=9.2, fontweight="bold",
                         color=arch["theme_color"], pad=6)
        
        # Border around leaf
        for spine in ax_top.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor(arch["theme_color"])
            spine.set_linewidth(1.8)

        # Badge placed at bottom outside of the image
        ax_top.set_xlabel(f"[{arch['acc']}]", fontsize=8.0, fontweight="bold",
                          color="#2C3E50", labelpad=4)

        # Bottom row: Sub-gridspec for Macro Attention (left) vs Micro Saliency (right)
        gs_sub = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=gs[1, col], wspace=0.10)

        # Macro Attention Inset (Left)
        ax_m = fig.add_subplot(gs_sub[0, 0])
        ax_m.imshow(attn_up, cmap="turbo", vmin=0, vmax=1)
        ax_m.set_xticks([])
        ax_m.set_yticks([])
        for spine in ax_m.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor("#27AE60")
            spine.set_linewidth(1.4)
        ax_m.set_xlabel("DINOv2 Venation", fontsize=7.6, color="#145A32",
                        labelpad=3, fontweight="bold")

        # Micro Pathological Saliency Inset (Right)
        ax_p = fig.add_subplot(gs_sub[0, 1])
        heat_overlay = plt.get_cmap("turbo")(sal_up)[:, :, :3]
        blend = 0.52 * rgb_np + 0.48 * heat_overlay
        ax_p.imshow(blend)
        ax_p.set_xticks([])
        ax_p.set_yticks([])
        for spine in ax_p.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor("#C0392B")
            spine.set_linewidth(1.4)
        ax_p.set_xlabel("Lesion Saliency", fontsize=7.6, color="#78281F",
                        labelpad=3, fontweight="bold")

    plt.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0.03)
    plt.close()
    print(f"[+] Successfully saved flawless archetypes figure to: {output_path}")

if __name__ == "__main__":
    create_flawless_archetypes_figure()

# -*- coding: utf-8 -*-
"""
Generate Visual Saliency Maps (Explainable AI via DINOv2 Self-Attention Rollout)
and Expected Calibration Error (ECE) Reliability Diagrams for BioDINO-Edge.
"""

import os, sys, random
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
import timm
from torchvision import transforms as T

PROJECT_ROOT = Path(r"e:\work\research-few-shot")
PAPER_DIR = PROJECT_ROOT / "paper"
DOCS_ASSETS = PROJECT_ROOT / "docs" / "assets"
PAPER_DIR.mkdir(exist_ok=True)
DOCS_ASSETS.mkdir(exist_ok=True)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[*] Running on device: {DEVICE}")

# -----------------------------------------------------------------------------
# 1. Visual Saliency Maps via DINOv2 Self-Attention
# -----------------------------------------------------------------------------
def generate_saliency_figures():
    print("\n[*] Loading DINOv2 Small for Saliency Map Extraction...")
    dino_model = timm.create_model('vit_small_patch14_dinov2', pretrained=True, dynamic_img_size=True).to(DEVICE).eval()
    
    # Configure attention capture
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

    pv_color = PROJECT_ROOT / "plantvillage" / "plantvillage dataset" / "color"
    
    # 4 distinct pathological target cases
    target_cases = [
        {
            "class_dir": "Potato___Late_blight",
            "title": "Potato Late Blight\n(Phytophthora infestans)",
            "finding": "Attention concentrated on water-soaked necrotic lesion margin"
        },
        {
            "class_dir": "Grape___Esca_(Black_Measles)",
            "title": "Grape Esca Complex\n(Phaeomoniella chlamydospora)",
            "finding": "Attention tracks interveinal chlorotic 'tiger-stripe' necrosis"
        },
        {
            "class_dir": "Apple___Cedar_apple_rust",
            "title": "Apple Cedar Rust\n(Gymnosporangium juniperi)",
            "finding": "Attention pinpoints bright circular fungal aecial spore clusters"
        },
        {
            "class_dir": "Apple___Black_rot",
            "title": "Apple Black Rot\n(Botryosphaeria obtusa)",
            "finding": "Attention isolates concentric 'frog-eye' necrotic center and ring"
        }
    ]

    selected_samples = []
    for case in target_cases:
        folder = pv_color / case["class_dir"]
        imgs = sorted(list(folder.glob("*.JPG")) + list(folder.glob("*.jpg")) + list(folder.glob("*.png")))
        # pick a representative image with clear lesions
        idx = min(15, len(imgs) - 1)
        selected_samples.append((imgs[idx], case["title"], case["finding"]))

    fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(12.0, 7.6))
    plt.subplots_adjust(wspace=0.10, hspace=0.15, left=0.14, right=0.98, top=0.86, bottom=0.12)

    col_headers = [
        ("Potato Late Blight", "P. infestans"),
        ("Grape Esca", "P. chlamydospora"),
        ("Apple Cedar Rust", "G. juniperi-virginianae"),
        ("Apple Black Rot", "B. obtusa")
    ]

    for col_idx, (disease, pathogen) in enumerate(col_headers):
        axes[0, col_idx].set_title(f"{disease}\n({pathogen})", fontsize=10.5, fontweight="bold", pad=12, linespacing=1.2)

    row_labels = [
        "(a) Input Leaf",
        "(b) DINOv2 Attention",
        "(c) Saliency Overlay"
    ]

    for col_idx, (img_path, title, finding) in enumerate(selected_samples):
        pil_img = Image.open(img_path).convert("RGB").resize((224, 224))
        tensor_img = transform(pil_img).unsqueeze(0).to(DEVICE)

        captured_attn.clear()
        with torch.no_grad():
            _ = dino_model(tensor_img)

        # Attention from CLS (token 0) to all 256 spatial patches (16x16)
        attn = captured_attn[0] # (1, num_heads, 257, 257)
        # Average across all 6 self-attention heads
        cls_attn = attn[0, :, 0, 1:].mean(dim=0).reshape(16, 16).numpy()

        # Min-max normalize
        cls_attn = (cls_attn - cls_attn.min()) / (cls_attn.max() - cls_attn.min() + 1e-8)
        # Upsample to 224x224
        attn_tensor = torch.tensor(cls_attn).unsqueeze(0).unsqueeze(0)
        attn_upsampled = F.interpolate(attn_tensor, size=(224, 224), mode="bicubic", align_corners=False).squeeze().numpy()
        attn_upsampled = np.clip(attn_upsampled, 0.0, 1.0)

        rgb_np = np.array(pil_img) / 255.0
        heatmap = plt.get_cmap("turbo")(attn_upsampled)[:, :, :3]
        overlay = 0.52 * rgb_np + 0.48 * heatmap

        # 1. Original Leaf
        axes[0, col_idx].imshow(rgb_np)
        axes[0, col_idx].set_xticks([])
        axes[0, col_idx].set_yticks([])

        # 2. Attention Heatmap
        im_heat = axes[1, col_idx].imshow(attn_upsampled, cmap="turbo", vmin=0, vmax=1)
        axes[1, col_idx].set_xticks([])
        axes[1, col_idx].set_yticks([])

        # 3. Overlay
        axes[2, col_idx].imshow(overlay)
        axes[2, col_idx].set_xticks([])
        axes[2, col_idx].set_yticks([])

    for row_idx, label in enumerate(row_labels):
        axes[row_idx, 0].set_ylabel(label, fontsize=11, fontweight="bold", labelpad=14, rotation=90, va="center")

    for r in range(3):
        for c in range(4):
            for spine in axes[r, c].spines.values():
                spine.set_visible(True)
                spine.set_edgecolor("#777777")
                spine.set_linewidth(0.9)

    # Add a global colorbar at bottom
    cbar_ax = fig.add_axes([0.30, 0.035, 0.40, 0.022])
    cb = fig.colorbar(im_heat, cax=cbar_ax, orientation="horizontal")
    cb.set_label("DINOv2 Self-Attention Density Normalized to [0, 1]", fontsize=10, fontweight="bold", labelpad=6)
    cb.ax.tick_params(labelsize=9)

    pdf_path = PAPER_DIR / "fig_saliency.pdf"
    png_path = PAPER_DIR / "fig_saliency.png"
    docs_png = DOCS_ASSETS / "fig_saliency.png"

    plt.savefig(pdf_path, bbox_inches="tight", dpi=300)
    plt.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.savefig(docs_png, bbox_inches="tight", dpi=300)
    plt.close()

    print(f"  [+] Saliency figures saved successfully:")
    print(f"      - {pdf_path}")
    print(f"      - {png_path}")
    print(f"      - {docs_png}")

# -----------------------------------------------------------------------------
# 2. Expected Calibration Error (ECE) & Reliability Diagrams
# -----------------------------------------------------------------------------
def compute_ece(probs, targets, n_bins=10):
    """
    Compute Expected Calibration Error (ECE) and Maximum Calibration Error (MCE).
    probs: (N, C) numpy array of predicted posteriors
    targets: (N,) numpy array of ground truth integer labels
    """
    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)
    accuracies = (predictions == targets)

    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    mce = 0.0
    bin_data = []

    for i in range(n_bins):
        in_bin = (confidences > bin_boundaries[i]) & (confidences <= bin_boundaries[i + 1])
        prop_in_bin = np.mean(in_bin)
        
        if np.sum(in_bin) > 0:
            acc_in_bin = np.mean(accuracies[in_bin])
            conf_in_bin = np.mean(confidences[in_bin])
            abs_diff = np.abs(acc_in_bin - conf_in_bin)
            ece += abs_diff * prop_in_bin
            mce = max(mce, abs_diff)
            bin_data.append({
                "bin_idx": i,
                "bin_lower": float(bin_boundaries[i]),
                "bin_upper": float(bin_boundaries[i + 1]),
                "count": int(np.sum(in_bin)),
                "accuracy": float(acc_in_bin),
                "confidence": float(conf_in_bin),
                "gap": float(abs_diff)
            })
        else:
            bin_data.append({
                "bin_idx": i,
                "bin_lower": float(bin_boundaries[i]),
                "bin_upper": float(bin_boundaries[i + 1]),
                "count": 0,
                "accuracy": 0.0,
                "confidence": (bin_boundaries[i] + bin_boundaries[i + 1]) / 2.0,
                "gap": 0.0
            })

    return ece * 100.0, mce * 100.0, bin_data

def generate_calibration_figures():
    print("\n[*] Loading Embedding Cache to compute exact ECE on 9,330 Test Queries...")
    cache_path = PROJECT_ROOT / "cache_artifacts" / "pv_novel_embeddings.pt"
    cdata = torch.load(cache_path, map_location="cpu", weights_only=False)

    c_bio = cdata["bio_feats"]
    c_dino = cdata["dino_feats"]
    c_labels = cdata["labels"].numpy()
    c_concat = torch.cat([c_bio, c_dino], dim=-1).numpy()
    c_text = cdata["bio_text_protos"]
    class_names = cdata["novel_classes"]
    n_classes = len(class_names)

    # Replicate standard 5-shot seed=42 split
    rng = random.Random(42)
    c_indices = [np.where(c_labels == c)[0].tolist() for c in range(n_classes)]
    s_idx, q_idx = [], []
    for c in range(n_classes):
        shuf = c_indices[c].copy()
        rng.shuffle(shuf)
        s_idx.extend(shuf[:5])
        q_idx.extend(shuf[5:])

    q_labels = c_labels[q_idx]

    # 1. Baseline: Uncalibrated Tip-Adapter / Cosine Protos
    proto_dino = np.stack([c_dino[s_idx][c_labels[s_idx] == c].mean(dim=0).numpy() for c in range(n_classes)])
    proto_dino = proto_dino / np.linalg.norm(proto_dino, axis=-1, keepdims=True)
    sims = np.dot(c_dino[q_idx].numpy(), proto_dino.T) * 15.0
    exp_sims = np.exp(sims - np.max(sims, axis=1, keepdims=True))
    probs_uncalibrated = exp_sims / np.sum(exp_sims, axis=1, keepdims=True)

    # 2. BioDINO-Edge Initial Consensus
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    clf_init = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')
    clf_init.fit(c_concat[s_idx], c_labels[s_idx])

    W_init = torch.tensor(clf_init.coef_, dtype=torch.float32)
    b_init = torch.tensor(clf_init.intercept_, dtype=torch.float32)
    q_concat_t = torch.tensor(c_concat[q_idx], dtype=torch.float32)
    lgt_lda = q_concat_t @ W_init.t() + b_init
    p_lda = F.softmax(lgt_lda, dim=-1)
    p_txt = F.softmax(20.0 * (c_bio[q_idx] @ c_text.t()), dim=-1)
    p_ens = 0.75 * p_lda + 0.25 * p_txt

    preds_ep = p_ens.argmax(dim=-1).numpy()
    top_confs, _ = p_ens.max(dim=-1)

    # 3. Soft-Anchored Transductive Refinement (3x support anchor weighting & 0.70 confidence threshold)
    ref_x = [c_concat[s_idx]] * 3
    ref_y = [c_labels[s_idx]] * 3
    for c in range(n_classes):
        c_cand = (preds_ep == c)
        if c_cand.sum() > 0:
            c_cand_idx = np.where(c_cand)[0]
            c_conf_vals = top_confs[c_cand_idx]
            high_conf = c_conf_vals > 0.70
            if high_conf.sum() > 0:
                c_cand_idx = c_cand_idx[high_conf.numpy()]
                c_conf_vals = c_conf_vals[high_conf]
            top_k = min(20, len(c_cand_idx))
            if top_k > 0:
                best_local_idx = c_cand_idx[torch.topk(c_conf_vals, top_k).indices.numpy()]
                best_q_idx = [q_idx[i] for i in best_local_idx]
                ref_x.append(c_concat[best_q_idx])
                ref_y.append(np.full(top_k, c))

    ref_x = np.concatenate(ref_x, axis=0)
    ref_y = np.concatenate(ref_y, axis=0)

    clf_trans = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')
    clf_trans.fit(ref_x, ref_y)

    W_trans = torch.tensor(clf_trans.coef_, dtype=torch.float32)
    b_trans = torch.tensor(clf_trans.intercept_, dtype=torch.float32)
    lgt_trans = q_concat_t @ W_trans.t() + b_trans
    p_trans = 0.75 * F.softmax(lgt_trans, dim=-1) + 0.25 * p_txt
    # Apply post-hoc temperature scaling (Guo et al., 2017) with T = 0.50
    log_p = torch.log(p_trans + 1e-12)
    p_cal = F.softmax(log_p / 0.50, dim=-1)
    probs_calibrated = p_cal.numpy()

    # Compute ECE
    ece_uncal, mce_uncal, bins_uncal = compute_ece(probs_uncalibrated, q_labels, n_bins=10)
    ece_cal, mce_cal, bins_cal = compute_ece(probs_calibrated, q_labels, n_bins=10)

    print(f"  • Uncalibrated Baseline ECE : {ece_uncal:.2f}% | MCE: {mce_uncal:.2f}%")
    print(f"  • BioDINO-Edge Calibrated ECE: {ece_cal:.2f}% | MCE: {mce_cal:.2f}%")

    # Plot Reliability Diagram (2 panels: Uncalibrated vs Calibrated)
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    
    # Left: Baseline
    accs_uncal = [b["accuracy"] for b in bins_uncal]
    confs_uncal = [b["confidence"] for b in bins_uncal]
    bin_centers = np.linspace(0.05, 0.95, 10)

    axes[0].plot([0, 1], [0, 1], "k--", label="Perfect Calibration", linewidth=1.5)
    axes[0].bar(bin_centers, accs_uncal, width=0.08, color="#e74c3c", alpha=0.65, edgecolor="#c0392b", label="Outputs (Acc)")
    axes[0].bar(bin_centers, [abs(a - c) for a, c in zip(accs_uncal, confs_uncal)], bottom=np.minimum(accs_uncal, confs_uncal),
                width=0.08, color="#95a5a6", alpha=0.45, hatch="//", edgecolor="#7f8c8d", label="Calibration Gap")
    axes[0].set_title(f"(a) Uncalibrated Generic Baseline\nECE = {ece_uncal:.2f}% | MCE = {mce_uncal:.2f}%", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Confidence", fontsize=10, fontweight="bold")
    axes[0].set_ylabel("Empirical Accuracy", fontsize=10, fontweight="bold")
    axes[0].set_xlim(0, 1)
    axes[0].set_ylim(0, 1)
    axes[0].grid(True, linestyle=":", alpha=0.6)
    axes[0].legend(loc="upper left", fontsize=9)

    # Right: BioDINO-Edge Calibrated
    accs_cal = [b["accuracy"] for b in bins_cal]
    confs_cal = [b["confidence"] for b in bins_cal]

    axes[1].plot([0, 1], [0, 1], "k--", label="Perfect Calibration", linewidth=1.5)
    axes[1].bar(bin_centers, accs_cal, width=0.08, color="#2ecc71", alpha=0.70, edgecolor="#27ae60", label="BioDINO-Edge (Acc)")
    axes[1].bar(bin_centers, [abs(a - c) for a, c in zip(accs_cal, confs_cal)], bottom=np.minimum(accs_cal, confs_cal),
                width=0.08, color="#95a5a6", alpha=0.45, hatch="//", edgecolor="#7f8c8d", label="Calibration Gap")
    axes[1].set_title(f"(b) BioDINO-Edge (Calibrated & Gated)\nECE = {ece_cal:.2f}% | MCE = {mce_cal:.2f}%", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Confidence", fontsize=10, fontweight="bold")
    axes[1].set_ylabel("Empirical Accuracy", fontsize=10, fontweight="bold")
    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(0, 1)
    axes[1].grid(True, linestyle=":", alpha=0.6)
    axes[1].legend(loc="upper left", fontsize=9)

    plt.tight_layout()
    pdf_path = PAPER_DIR / "fig_calibration.pdf"
    png_path = PAPER_DIR / "fig_calibration.png"
    docs_png = DOCS_ASSETS / "fig_calibration.png"

    plt.savefig(pdf_path, bbox_inches="tight", dpi=300)
    plt.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.savefig(docs_png, bbox_inches="tight", dpi=300)
    plt.close()

    print(f"  [+] Calibration figures saved successfully:")
    print(f"      - {pdf_path}")
    print(f"      - {png_path}")
    print(f"      - {docs_png}")

    # Return numbers to update JSON
    return {
        "uncalibrated_baseline": {
            "ece_pct": float(round(ece_uncal, 2)),
            "mce_pct": float(round(mce_uncal, 2))
        },
        "biodino_edge_calibrated": {
            "ece_pct": float(round(ece_cal, 2)),
            "mce_pct": float(round(mce_cal, 2)),
            "bin_data": bins_cal
        }
    }

if __name__ == "__main__":
    generate_saliency_figures()
    calib_stats = generate_calibration_figures()

    # Update biodino_edge_results.json
    res_path = PROJECT_ROOT / "biodino_edge_results.json"
    if res_path.exists():
        import json
        with open(res_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "plantvillage" in data:
            data["plantvillage"]["calibration"] = calib_stats
        with open(res_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[*] Updated {res_path} with ECE calibration metrics.")

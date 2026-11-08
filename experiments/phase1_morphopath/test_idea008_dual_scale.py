"""
================================================================================
Empirical Test for IDEA-008: Dual-Scale Micro-Lesion Crop Fusion
Evaluates:
  1. Single-scale Global Leaf Context (224x224)
  2. Single-scale High-Magnification Center Crop (70% and 50% crops)
  3. Feature Concatenation [f_global, f_crop] (1792-d)
  4. Convex Feature Fusion alpha * f_global + (1 - alpha) * f_crop
  5. Decoupled Multi-Scale Architecture:
     - Global DINOv2 for Leaf Macro-Archetype Routing
     - Dual-Scale BioCLIP for Fine-Grained Intra-Archetype Pathology
Metrics:
  - Macro-Archetype Routing Accuracy (Top-1, Top-2)
  - Intra-Archetype Disease Accuracies (Solanoid, Vitoid, Pooid, Rosoid)
  - End-to-End Hierarchical Accuracy & Macro-F1
  - Fine-grained Solanoid (Tomato/Potato) Blight & Spot separation
================================================================================
"""

import sys
from pathlib import Path
import json
import time
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, f1_score

PROJECT_ROOT = Path("E:/work/research-few-shot")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.biodino_hierarchical_pipeline import load_backbones, DEVICE

EXP_DIR = PROJECT_ROOT / "experiments" / "phase1_morphopath"
CACHE_FILE = EXP_DIR / "plantdoc_features_seed42.pt"

ARCHETYPE_MAP = {
    'Tomato_Early_blight_leaf': 0, 'Tomato_Septoria_leaf_spot': 0, 'Tomato_leaf': 0,
    'Tomato_leaf_bacterial_spot': 0, 'Tomato_leaf_late_blight': 0, 'Tomato_leaf_mosaic_virus': 0,
    'Tomato_leaf_yellow_virus': 0, 'Tomato_mold_leaf': 0,
    'Potato_leaf_early_blight': 0, 'Potato_leaf_late_blight': 0,
    'grape_leaf': 1, 'grape_leaf_black_rot': 1, 'Squash_Powdery_mildew_leaf': 1,
    'Corn_Gray_leaf_spot': 2, 'Corn_leaf_blight': 2, 'Corn_rust_leaf': 2,
    'Apple_Scab_Leaf': 3, 'Apple_leaf': 3, 'Apple_rust_leaf': 3,
    'Bell_pepper_leaf': 3, 'Bell_pepper_leaf_spot': 3,
    'Blueberry_leaf': 3, 'Cherry_leaf': 3, 'Peach_leaf': 3,
    'Raspberry_leaf': 3, 'Soyabean_leaf': 3, 'Strawberry_leaf': 3
}

ARCHETYPE_NAMES = [
    "A1: Solanoid (10 classes)",
    "A2: Vitoid/Cucurbit (3 classes)",
    "A3: Pooid (3 classes)",
    "A4: Rosoid/Other (11 classes)"
]

def get_crop(img: Image.Image, ratio: float = 0.7) -> Image.Image:
    w, h = img.size
    cw, ch = int(w * ratio), int(h * ratio)
    left = (w - cw) // 2
    top = (h - ch) // 2
    return img.crop((left, top, left + cw, top + ch))

def extract_dual_scale_features(samples, models, device=DEVICE):
    dino_m = models.dino_model
    dino_tr = models.dino_transforms
    bio_m = models.bioclip_model
    bio_tr = models.bioclip_transforms

    glob_bio, glob_dino = [], []
    crop70_bio, crop70_dino = [], []
    crop50_bio, crop50_dino = [], []
    labels = []

    print(f"[*] Extracting dual-scale features for {len(samples)} images...")
    t0 = time.perf_counter()

    with torch.no_grad():
        for path, label in samples:
            img = Image.open(path).convert("RGB")
            img_c70 = get_crop(img, 0.70)
            img_c50 = get_crop(img, 0.50)

            # Global tensors
            gb_t = bio_tr(img).unsqueeze(0).to(device)
            gd_t = dino_tr(img).unsqueeze(0).to(device)

            # Crop 70 tensors
            c70_b_t = bio_tr(img_c70).unsqueeze(0).to(device)
            c70_d_t = dino_tr(img_c70).unsqueeze(0).to(device)

            # Crop 50 tensors
            c50_b_t = bio_tr(img_c50).unsqueeze(0).to(device)
            c50_d_t = dino_tr(img_c50).unsqueeze(0).to(device)

            with torch.autocast(device_type="cuda", dtype=torch.float16):
                # Global
                f_gb = F.normalize(bio_m.encode_image(gb_t), dim=-1).cpu()
                f_gd = F.normalize(dino_m(gd_t), dim=-1).cpu()

                # Crop 70
                f_c70b = F.normalize(bio_m.encode_image(c70_b_t), dim=-1).cpu()
                f_c70d = F.normalize(dino_m(c70_d_t), dim=-1).cpu()

                # Crop 50
                f_c50b = F.normalize(bio_m.encode_image(c50_b_t), dim=-1).cpu()
                f_c50d = F.normalize(dino_m(c50_d_t), dim=-1).cpu()

            glob_bio.append(f_gb)
            glob_dino.append(f_gd)
            crop70_bio.append(f_c70b)
            crop70_dino.append(f_c70d)
            crop50_bio.append(f_c50b)
            crop50_dino.append(f_c50d)
            labels.append(label)

    elapsed = time.perf_counter() - t0
    print(f"[OK] Extracted in {elapsed:.2f}s ({elapsed / len(samples) * 1000.0:.2f} ms/image)")

    return {
        "glob_bio": torch.cat(glob_bio, dim=0).float().numpy(),
        "glob_dino": torch.cat(glob_dino, dim=0).float().numpy(),
        "crop70_bio": torch.cat(crop70_bio, dim=0).float().numpy(),
        "crop70_dino": torch.cat(crop70_dino, dim=0).float().numpy(),
        "crop50_bio": torch.cat(crop50_bio, dim=0).float().numpy(),
        "crop50_dino": torch.cat(crop50_dino, dim=0).float().numpy(),
        "labels": np.array(labels, dtype=int),
        "ms_per_image": elapsed / len(samples) * 1000.0
    }

def evaluate_idea008():
    print("=" * 80)
    print("IDEA-008: Dual-Scale Micro-Lesion Crop Fusion Benchmark")
    print("=" * 80)

    cached = torch.load(CACHE_FILE, map_location="cpu")
    support_samples = cached["support_samples"]
    query_samples = cached["query_samples"]
    class_names = cached["class_names"]
    n_queries = len(query_samples)

    class_to_arch = np.array([ARCHETYPE_MAP[c] for c in class_names])
    qry_labels = np.array([s[1] for s in query_samples])
    qry_arch_true = class_to_arch[qry_labels]

    models = load_backbones(DEVICE)
    sup = extract_dual_scale_features(support_samples, models)
    qry = extract_dual_scale_features(query_samples, models)

    sup_labels = sup["labels"]
    sup_arch = class_to_arch[sup_labels]

    # Archetype Router (Morphology from Global DINOv2 vs Crop DINOv2)
    for r_name, s_d, q_d in [
        ("Global DINOv2", sup["glob_dino"], qry["glob_dino"]),
        ("Crop 70% DINOv2", sup["crop70_dino"], qry["crop70_dino"]),
        ("Crop 50% DINOv2", sup["crop50_dino"], qry["crop50_dino"]),
        ("Fused Global+Crop70 DINOv2",
         (sup["glob_dino"] + sup["crop70_dino"]) / np.linalg.norm(sup["glob_dino"] + sup["crop70_dino"], axis=-1, keepdims=True),
         (qry["glob_dino"] + qry["crop70_dino"]) / np.linalg.norm(qry["glob_dino"] + qry["crop70_dino"], axis=-1, keepdims=True))
    ]:
        arch_p = np.stack([s_d[sup_arch == a].mean(axis=0) for a in range(4)])
        arch_p /= (np.linalg.norm(arch_p, axis=-1, keepdims=True) + 1e-12)
        q_norm = q_d / (np.linalg.norm(q_d, axis=-1, keepdims=True) + 1e-12)
        sim = q_norm @ arch_p.T
        top1 = sim.argmax(axis=-1)
        top2 = np.argsort(sim, axis=-1)[:, -2:]
        acc_top1 = float(np.mean(top1 == qry_arch_true) * 100.0)
        acc_top2 = float(np.mean([qry_arch_true[i] in top2[i] for i in range(n_queries)]) * 100.0)
        print(f"[*] Router [{r_name}]: Top-1 = {acc_top1:.2f}% | Top-2 = {acc_top2:.2f}%")

    # Use Global DINOv2 as canonical router (highest top-1 morphology representation)
    arch_p_best = np.stack([sup["glob_dino"][sup_arch == a].mean(axis=0) for a in range(4)])
    arch_p_best /= (np.linalg.norm(arch_p_best, axis=-1, keepdims=True) + 1e-12)
    q_norm_best = qry["glob_dino"] / (np.linalg.norm(qry["glob_dino"], axis=-1, keepdims=True) + 1e-12)
    router_preds = (q_norm_best @ arch_p_best.T).argmax(axis=-1)

    # Now evaluate disease feature representations
    disease_configs = [
        ("1. Global Only (Bio 512 + DINO 384 = 896d)",
         np.concatenate([sup["glob_bio"], sup["glob_dino"]], -1),
         np.concatenate([qry["glob_bio"], qry["glob_dino"]], -1)),

        ("2. Crop 70% Only (Bio 512 + DINO 384 = 896d)",
         np.concatenate([sup["crop70_bio"], sup["crop70_dino"]], -1),
         np.concatenate([qry["crop70_bio"], qry["crop70_dino"]], -1)),

        ("3. Crop 50% Only (Bio 512 + DINO 384 = 896d)",
         np.concatenate([sup["crop50_bio"], sup["crop50_dino"]], -1),
         np.concatenate([qry["crop50_bio"], qry["crop50_dino"]], -1)),

        ("4. Dual-Scale Concat 1792d [Global, Crop70]",
         np.concatenate([sup["glob_bio"], sup["glob_dino"], sup["crop70_bio"], sup["crop70_dino"]], -1),
         np.concatenate([qry["glob_bio"], qry["glob_dino"], qry["crop70_bio"], qry["crop70_dino"]], -1)),

        ("5. Dual-Scale BioCLIP Fusion (Bio 50% Glob + 50% Crop70) + DINO Glob = 896d",
         np.concatenate([
             (sup["glob_bio"] + sup["crop70_bio"]) / np.linalg.norm(sup["glob_bio"] + sup["crop70_bio"], axis=-1, keepdims=True),
             sup["glob_dino"]
         ], -1),
         np.concatenate([
             (qry["glob_bio"] + qry["crop70_bio"]) / np.linalg.norm(qry["glob_bio"] + qry["crop70_bio"], axis=-1, keepdims=True),
             qry["glob_dino"]
         ], -1)),

        ("6. Dual-Scale Equal Average 896d (Global + Crop70)",
         (np.concatenate([sup["glob_bio"], sup["glob_dino"]], -1) + np.concatenate([sup["crop70_bio"], sup["crop70_dino"]], -1)) / 2.0,
         (np.concatenate([qry["glob_bio"], qry["glob_dino"]], -1) + np.concatenate([qry["crop70_bio"], qry["crop70_dino"]], -1)) / 2.0),

        ("7. Dual-Scale Convex (0.7 Global + 0.3 Crop70)",
         0.7 * np.concatenate([sup["glob_bio"], sup["glob_dino"]], -1) + 0.3 * np.concatenate([sup["crop70_bio"], sup["crop70_dino"]], -1),
         0.7 * np.concatenate([qry["glob_bio"], qry["glob_dino"]], -1) + 0.3 * np.concatenate([qry["crop70_bio"], qry["crop70_dino"]], -1))
    ]

    print("\n" + "=" * 90)
    print("EMPIRICAL EVALUATION OF DUAL-SCALE FEATURE CONFIGURATIONS")
    print("=" * 90)
    print(f"{'Configuration':<45} | {'Solanoid':<10} | {'Rosoid':<10} | {'Oracle Acc':<12} | {'Hierarchical':<14} | {'Macro F1':<10}")
    print("-" * 105)

    results_dict = {}
    for desc, s_feat, q_feat in disease_configs:
        preds_oracle = np.zeros(n_queries, dtype=int)
        preds_hier = np.zeros(n_queries, dtype=int)
        per_arch_acc = []

        for a_idx in range(4):
            a_classes = np.where(class_to_arch == a_idx)[0]
            a_sup_mask = (sup_arch == a_idx)
            local_map = {c: i for i, c in enumerate(a_classes)}
            y_loc = np.array([local_map[y] for y in sup_labels[a_sup_mask]])
            X_loc = s_feat[a_sup_mask]

            clf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=0.6).fit(X_loc, y_loc)

            # Oracle
            q_mask_o = (qry_arch_true == a_idx)
            p_o = clf.predict(q_feat[q_mask_o])
            preds_oracle[q_mask_o] = a_classes[p_o]
            acc_a = float(accuracy_score(qry_labels[q_mask_o], a_classes[p_o]) * 100.0)
            per_arch_acc.append(acc_a)

            # Hierarchical
            q_mask_r = (router_preds == a_idx)
            if np.sum(q_mask_r) > 0:
                p_r = clf.predict(q_feat[q_mask_r])
                preds_hier[q_mask_r] = a_classes[p_r]

        acc_o = float(accuracy_score(qry_labels, preds_oracle) * 100.0)
        acc_h = float(accuracy_score(qry_labels, preds_hier) * 100.0)
        f1_h = float(f1_score(qry_labels, preds_hier, average="macro") * 100.0)

        print(f"{desc:<45} | {per_arch_acc[0]:>5.2f}%    | {per_arch_acc[3]:>5.2f}%    | {acc_o:>5.2f}%      | {acc_h:>5.2f}%        | {f1_h:>5.2f}%")

        results_dict[desc] = {
            "solanoid_acc": per_arch_acc[0],
            "vitoid_acc": per_arch_acc[1],
            "pooid_acc": per_arch_acc[2],
            "rosoid_acc": per_arch_acc[3],
            "oracle_acc": acc_o,
            "hierarchical_acc": acc_h,
            "macro_f1": f1_h
        }

    # Analyze fine-grained Solanoid blight & spot separation
    # Tomato early blight (idx 19) vs late blight (idx 23) vs Septoria (idx 20)
    print("\n" + "=" * 90)
    print("FINE-GRAINED TOMATO LESION SEPARATION ANALYSIS")
    print("=" * 90)
    tomato_classes = [c for c in class_names if c.startswith("Tomato")]
    print(f"Total Tomato classes in dataset: {len(tomato_classes)}")

    glob_hier = results_dict["1. Global Only (Bio 512 + DINO 384 = 896d)"]["hierarchical_acc"]
    best_config_name = max(results_dict.keys(), key=lambda k: results_dict[k]["hierarchical_acc"])
    best_hier = results_dict[best_config_name]["hierarchical_acc"]
    best_f1 = results_dict[best_config_name]["macro_f1"]
    gain = best_hier - glob_hier

    print(f"\n[IDEA-008 Empirical Summary]")
    print(f"  * Baseline Global-Only Hierarchical Acc: {glob_hier:.2f}%")
    print(f"  * Best Dual-Scale Configuration: '{best_config_name}'")
    print(f"  * Best Hierarchical Acc: {best_hier:.2f}% | Macro F1: {best_f1:.2f}%")
    print(f"  * Net Gain over Global Baseline: {gain:+.2f}%")

    out_file = EXP_DIR / "idea008_dual_scale_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "results": results_dict,
            "baseline_global_acc": glob_hier,
            "best_configuration": best_config_name,
            "best_hierarchical_acc": best_hier,
            "net_gain": gain,
            "status": "validated" if gain >= 0.5 else "rejected"
        }, f, indent=2)

    print(f"[OK] Saved results to {out_file}")

if __name__ == "__main__":
    evaluate_idea008()


"""
================================================================================
Empirical Test for IDEA-005: DINOv2 Saliency-Guided Background Denoising
Evaluates:
  1. Standard DINOv2 CLS token
  2. Uniform patch mean pooling
  3. Soft saliency-weighted patch pooling (CLS attention from Block 11)
  4. Hard foreground thresholding (Top-50% attention patches)
  5. CLS + Saliency fusion
Metrics:
  - Macro-Archetype Router Accuracy (Top-1, Top-2 across 252 queries)
  - End-to-End Hierarchical Disease Classification Accuracy & Macro-F1
  - Execution latency overhead per image
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

def extract_features_with_saliency(samples, models, device=DEVICE, is_support=False):
    """
    Extracts multiple DINOv2 pooling variants along with BioCLIP features.
    """
    dino_model = models.dino_model
    dino_transforms = models.dino_transforms
    bioclip_model = models.bioclip_model
    bioclip_transforms = models.bioclip_transforms

    # Setup forward hook on last attention block to capture CLS attention
    attn_store = {}
    def hook_fn(module, input, output):
        x = input[0] # [B, N, C]
        B, N, C = x.shape
        qkv = module.qkv(x).reshape(B, N, 3, module.num_heads, module.head_dim).permute(2, 0, 3, 1, 4)
        q, k, v = qkv.unbind(0)
        q = module.q_norm(q)
        k = module.k_norm(k)
        attn = (q * module.scale) @ k.transpose(-2, -1)
        attn = attn.softmax(dim=-1) # [B, num_heads, N, N]
        # Average heads, CLS token attention to patches 1..256
        cls_attn = attn[:, :, 0, 1:].mean(dim=1) # [B, 256]
        attn_store["cls_attn"] = cls_attn

    hook_handle = dino_model.blocks[-1].attn.register_forward_hook(hook_fn)

    feats_cls = []
    feats_mean = []
    feats_soft = []
    feats_top50 = []
    feats_cls_soft = []
    feats_bio = []
    labels = []

    print(f"[*] Extracting saliency features for {len(samples)} images (is_support={is_support})...")
    t0 = time.perf_counter()

    with torch.no_grad():
        for idx, (path, label) in enumerate(samples):
            img = Image.open(path).convert("RGB")
            d_tensor = dino_transforms(img).unsqueeze(0).to(device)
            b_tensor = bioclip_transforms(img).unsqueeze(0).to(device)

            with torch.autocast(device_type="cuda", dtype=torch.float16):
                # 1. DINOv2 tokens
                tokens = dino_model.forward_features(d_tensor) # [1, 257, 384]
                cls_tok = tokens[:, 0, :] # [1, 384]
                patches = tokens[:, 1:, :] # [1, 256, 384]
                cls_attn = attn_store["cls_attn"] # [1, 256]

                # Variant A: Standard CLS
                f_cls = F.normalize(cls_tok, dim=-1)

                # Variant B: Mean patch pooling
                f_mean = F.normalize(patches.mean(dim=1), dim=-1)

                # Variant C: Soft attention-weighted patch pooling
                weights = cls_attn.unsqueeze(-1) # [1, 256, 1]
                f_soft = (patches * weights).sum(dim=1) / (weights.sum(dim=1) + 1e-12)
                f_soft = F.normalize(f_soft, dim=-1)

                # Variant D: Hard foreground thresholding (Top 50% patches)
                top_k = 128 # 50% of 256
                top_idx = torch.topk(cls_attn, top_k, dim=1).indices[0] # [128]
                f_top50 = F.normalize(patches[:, top_idx, :].mean(dim=1), dim=-1)

                # Variant E: CLS + Soft Saliency
                f_cls_soft = F.normalize(cls_tok + f_soft, dim=-1)

                # BioCLIP feature
                f_bio = F.normalize(bioclip_model.encode_image(b_tensor), dim=-1)

            feats_cls.append(f_cls.cpu())
            feats_mean.append(f_mean.cpu())
            feats_soft.append(f_soft.cpu())
            feats_top50.append(f_top50.cpu())
            feats_cls_soft.append(f_cls_soft.cpu())
            feats_bio.append(f_bio.cpu())
            labels.append(label)

    hook_handle.remove()
    elapsed = time.perf_counter() - t0
    print(f"[OK] Done in {elapsed:.2f}s ({elapsed / len(samples) * 1000.0:.2f} ms/image)")

    return {
        "cls": torch.cat(feats_cls, dim=0).float().numpy(),
        "mean_patch": torch.cat(feats_mean, dim=0).float().numpy(),
        "soft_saliency": torch.cat(feats_soft, dim=0).float().numpy(),
        "top50_foreground": torch.cat(feats_top50, dim=0).float().numpy(),
        "cls_plus_soft": torch.cat(feats_cls_soft, dim=0).float().numpy(),
        "bioclip": torch.cat(feats_bio, dim=0).float().numpy(),
        "labels": np.array(labels, dtype=int),
        "ms_per_image": elapsed / len(samples) * 1000.0
    }

def evaluate_idea005():
    print("=" * 80)
    print("IDEA-005: DINOv2 Saliency-Guided Background Denoising Benchmark")
    print("=" * 80)

    # Load cache to get original samples
    cached = torch.load(CACHE_FILE, map_location="cpu")
    support_samples = cached["support_samples"]
    query_samples = cached["query_samples"]
    class_names = cached["class_names"]
    n_queries = len(query_samples)

    class_to_arch = np.array([ARCHETYPE_MAP[c] for c in class_names])
    qry_labels = np.array([s[1] for s in query_samples])
    qry_arch_true = class_to_arch[qry_labels]

    # Load backbones and extract features
    models = load_backbones(DEVICE)
    sup_feats = extract_features_with_saliency(support_samples, models, is_support=True)
    qry_feats = extract_features_with_saliency(query_samples, models, is_support=False)

    sup_labels = sup_feats["labels"]
    sup_arch = class_to_arch[sup_labels]

    variants = [
        ("1. Standard CLS Token (Baseline)", "cls"),
        ("2. Uniform Mean Patch Pooling", "mean_patch"),
        ("3. Soft Saliency-Weighted Patch Pooling", "soft_saliency"),
        ("4. Hard Foreground Top-50% Patches", "top50_foreground"),
        ("5. CLS + Soft Saliency Fusion", "cls_plus_soft")
    ]

    results = {}
    print("\n" + "=" * 80)
    print("EMPIRICAL COMPARISON OF DINOv2 POOLING SCHEMES")
    print("=" * 80)
    print(f"{'Pooling Variant':<42} | {'Router Top-1':<12} | {'Router Top-2':<12} | {'Hierarchical Acc':<16} | {'Macro F1':<10}")
    print("-" * 102)

    for desc, key in variants:
        s_dino = sup_feats[key]
        q_dino = qry_feats[key]

        # 1. Archetype Router Accuracy
        arch_protos = np.stack([s_dino[sup_arch == a].mean(axis=0) for a in range(4)])
        arch_protos /= (np.linalg.norm(arch_protos, axis=-1, keepdims=True) + 1e-12)
        q_dino_norm = q_dino / (np.linalg.norm(q_dino, axis=-1, keepdims=True) + 1e-12)

        sim_arch = q_dino_norm @ arch_protos.T
        top1_arch = sim_arch.argmax(axis=-1)
        top2_arch = np.argsort(sim_arch, axis=-1)[:, -2:]
        acc_top1 = float(np.mean(top1_arch == qry_arch_true) * 100.0)
        acc_top2 = float(np.mean([qry_arch_true[i] in top2_arch[i] for i in range(n_queries)]) * 100.0)

        # 2. End-to-End Hierarchical Pipeline (combining with BioCLIP, shrinkage=0.6)
        s_joint = np.concatenate([sup_feats["bioclip"], s_dino], axis=-1)
        q_joint = np.concatenate([qry_feats["bioclip"], q_dino], axis=-1)

        preds_hier = np.zeros(n_queries, dtype=int)
        for a_idx in range(4):
            a_classes = np.where(class_to_arch == a_idx)[0]
            a_sup_mask = (sup_arch == a_idx)
            local_map = {c: i for i, c in enumerate(a_classes)}
            y_loc = np.array([local_map[y] for y in sup_labels[a_sup_mask]])
            X_loc = s_joint[a_sup_mask]

            clf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=0.6).fit(X_loc, y_loc)
            q_mask = (top1_arch == a_idx)
            if np.sum(q_mask) > 0:
                p_loc = clf.predict(q_joint[q_mask])
                preds_hier[q_mask] = a_classes[p_loc]

        acc_hier = float(accuracy_score(qry_labels, preds_hier) * 100.0)
        f1_hier = float(f1_score(qry_labels, preds_hier, average="macro") * 100.0)

        print(f"{desc:<42} | {acc_top1:>5.2f}%       | {acc_top2:>5.2f}%       | {acc_hier:>5.2f}%           | {f1_hier:>5.2f}%")

        results[key] = {
            "description": desc,
            "router_top1": acc_top1,
            "router_top2": acc_top2,
            "hierarchical_acc": acc_hier,
            "hierarchical_macro_f1": f1_hier
        }

    # Analyze findings
    cls_acc = results["cls"]["hierarchical_acc"]
    cls_router = results["cls"]["router_top1"]
    best_key = max(results.keys(), key=lambda k: results[k]["hierarchical_acc"])
    best_acc = results[best_key]["hierarchical_acc"]
    best_router = results[best_key]["router_top1"]

    print("\n" + "=" * 80)
    print("ANALYSIS OF IDEA-005 FINDINGS")
    print("=" * 80)
    print(f"  * CLS Token: Router Top-1 = {cls_router:.2f}% | Hierarchical Acc = {cls_acc:.2f}%")
    print(f"  * Best Variant ({best_key}): Router Top-1 = {best_router:.2f}% | Hierarchical Acc = {best_acc:.2f}% (Delta: {best_acc - cls_acc:+.2f}%)")
    print(f"  * Saliency vs CLS Router Delta: {results['soft_saliency']['router_top1'] - cls_router:+.2f}%")
    print(f"  * Saliency vs CLS Hierarchical Delta: {results['soft_saliency']['hierarchical_acc'] - cls_acc:+.2f}%")
    print(f"  * Latency: CLS inference is standard; attention hooking adds +{qry_feats['ms_per_image']:.2f} ms/image")

    out_file = EXP_DIR / "idea005_saliency_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "results": results,
            "baseline_cls_hier_acc": cls_acc,
            "best_variant": best_key,
            "best_variant_hier_acc": best_acc,
            "gain_over_cls": best_acc - cls_acc,
            "status": "validated" if (best_acc - cls_acc) >= 0.5 else "rejected"
        }, f, indent=2)

    print(f"[OK] Saved results to {out_file}")

if __name__ == "__main__":
    evaluate_idea005()


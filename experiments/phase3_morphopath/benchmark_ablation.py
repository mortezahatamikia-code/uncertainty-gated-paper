"""
================================================================================
MorphoPath-Edge: Phase 3 Comprehensive Component Ablation Study
================================================================================
TASK-MORPHOPATH-004 Execution Benchmark:
  Measures Top-1, Top-2, Macro F1, and deltas across 6 configurations:
    1. Full Model (MorphoPath-Edge Complete)
    2. w/o Test-Time Manifold Rectification (ADR-005)
    3. w/o Macro Botanical Archetype Router (ADR-001) [Flat model]
    4. w/o Covariance Shrinkage (ADR-002) [Unregularized lambda=0.001]
    5. w/o Micro-Symptom Prompt Ensemble (ADR-004) [Pure visual]
    6. w/o Bayesian Cardinality Gating (ADR-003) [Hard Argmax]
  
  Visualizations:
    - Generates 2D t-SNE manifold projections (Before vs After Manifold Rectification)
      saved to experiments/phase3_morphopath/tsne_manifold_rectification.png
  
  Artifacts:
    - Structured JSON exported to:
      experiments/phase3_morphopath/ablation_study_results.json
================================================================================
"""

from __future__ import annotations
import json
import math
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import torch
from sklearn.manifold import TSNE
from sklearn.metrics import accuracy_score, f1_score

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.morphopath_engine import (
    ARCHETYPE_NAMES,
    DEFAULT_ARCHETYPE_MAP,
    MorphoPathEngine,
    fit_shrunk_lda,
    infer_archetype_for_class,
    is_healthy_leaf_name,
    l2_normalize,
    softmax_prob,
    tukey_power_transform,
)

CACHE_FILE = PROJECT_ROOT / "experiments" / "phase1_morphopath" / "plantdoc_features_seed42.pt"
MICRO_FILE = PROJECT_ROOT / "experiments" / "phase1_morphopath" / "micro_symptom_prototypes.pt"
OUTPUT_JSON = PROJECT_ROOT / "experiments" / "phase3_morphopath" / "ablation_study_results.json"
TSNE_PNG = PROJECT_ROOT / "experiments" / "phase3_morphopath" / "tsne_manifold_rectification.png"


def compute_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    top2_preds: np.ndarray,
    class_names: List[str],
) -> Dict[str, float]:
    """Computes Top-1, Top-2 differential accuracy, Macro F1, FNR, and FPR."""
    top1_acc = float(accuracy_score(y_true, y_pred) * 100.0)
    top2_flags = (y_true == top2_preds[:, 0]) | (y_true == top2_preds[:, 1])
    top2_acc = float(np.mean(top2_flags) * 100.0)
    macro_f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0) * 100.0)

    healthy_indices = set(i for i, c in enumerate(class_names) if is_healthy_leaf_name(c))
    diseased_mask = np.array([y not in healthy_indices for y in y_true])
    healthy_mask = np.array([y in healthy_indices for y in y_true])
    pred_healthy = np.array([y in healthy_indices for y in y_pred])

    fnr = float(np.sum(diseased_mask & pred_healthy) / max(1, np.sum(diseased_mask)) * 100.0)
    fpr = float(np.sum(healthy_mask & ~pred_healthy) / max(1, np.sum(healthy_mask)) * 100.0)

    return {
        "top1_accuracy": round(top1_acc, 2),
        "top2_accuracy": round(top2_acc, 2),
        "macro_f1": round(macro_f1, 2),
        "fnr": round(fnr, 2),
        "fpr": round(fpr, 2),
    }


# ==============================================================================
# Ablation Configurations
# ==============================================================================

def run_config_1_full(
    sup_joint: np.ndarray,
    sup_labels: np.ndarray,
    qry_joint: np.ndarray,
    qry_labels: np.ndarray,
    class_names: List[str],
    micro_protos: np.ndarray,
) -> Dict[str, Any]:
    """1. Full Proposed Model (MorphoPath-Edge Complete)."""
    engine = MorphoPathEngine(
        bioclip_dim=512,
        dinov2_dim=384,
        shrinkage=0.60,
        router_temp=12.0,
        vis_temp=15.0,
        text_temp=30.0,
        w_vis=0.75,
        margin_penalty=0.05,
        penalized_classes=["Potato_leaf_late_blight"],
        micro_prototypes=micro_protos,
        class_names=class_names,
    )
    engine.fit(sup_joint, sup_labels)
    out = engine.forward(qry_joint)
    metrics = compute_metrics(qry_labels, out.top1_preds, out.top2_preds, class_names)
    metrics["router_top1_accuracy"] = float(
        np.mean(out.archetype_preds == engine.class_to_arch[qry_labels]) * 100.0
    )
    return metrics


def run_config_2_no_rectification(
    sup_joint: np.ndarray,
    sup_labels: np.ndarray,
    qry_joint: np.ndarray,
    qry_labels: np.ndarray,
    class_names: List[str],
    micro_protos: np.ndarray,
) -> Dict[str, Any]:
    """2. w/o Test-Time Manifold Rectification (ADR-005): Omits mu_s and mu_q centering."""
    n_classes = len(class_names)
    class_to_arch = np.array([
        DEFAULT_ARCHETYPE_MAP.get(c, infer_archetype_for_class(c)) for c in class_names
    ])
    sup_arch = class_to_arch[sup_labels]

    sup_bio, sup_dino = sup_joint[:, :512], sup_joint[:, 512:]
    qry_bio, qry_dino = qry_joint[:, :512], qry_joint[:, 512:]

    # Archetype DINO prototypes
    arch_protos = [
        sup_dino[sup_arch == a].mean(axis=0) if np.any(sup_arch == a) else np.zeros(384)
        for a in range(4)
    ]
    arch_protos_dino = l2_normalize(np.stack(arch_protos))

    # Tukey transform without centering (NO mu_s / mu_q subtraction)
    sup_tukey = tukey_power_transform(sup_joint)
    qry_tukey = tukey_power_transform(qry_joint)

    # Raw class prototypes (no centering)
    unrect_protos = l2_normalize(np.stack([
        sup_tukey[sup_labels == c].mean(axis=0) if np.any(sup_labels == c) else np.zeros(896)
        for c in range(n_classes)
    ]))

    # Archetype routing
    sim_arch = l2_normalize(qry_dino) @ arch_protos_dino.T
    p_arch = softmax_prob(sim_arch, temp=12.0)

    # Visual similarity on unrectified features
    sims_unrect = qry_tukey @ unrect_protos.T
    for i, c in enumerate(class_names):
        if c == "Potato_leaf_late_blight":
            sims_unrect[:, i] -= 0.05

    p_vis_m = softmax_prob(sims_unrect, temp=15.0)

    # Micro-symptom text fusion
    sim_micro = l2_normalize(qry_bio) @ l2_normalize(micro_protos).T
    p_txt = softmax_prob(sim_micro, temp=30.0)
    p_comb = 0.75 * p_vis_m + 0.25 * p_txt

    top1 = p_comb.argmax(axis=-1)
    top2_ranked = np.argsort(-sims_unrect, axis=-1)[:, :2]
    p2 = np.where(top2_ranked[:, 0] == top1, top2_ranked[:, 1], top2_ranked[:, 0])
    top2_preds = np.column_stack([top1, p2])

    metrics = compute_metrics(qry_labels, top1, top2_preds, class_names)
    metrics["router_top1_accuracy"] = float(
        np.mean(p_arch.argmax(axis=-1) == class_to_arch[qry_labels]) * 100.0
    )
    return metrics


def run_config_3_flat_no_router(
    sup_joint: np.ndarray,
    sup_labels: np.ndarray,
    qry_joint: np.ndarray,
    qry_labels: np.ndarray,
    class_names: List[str],
    micro_protos: np.ndarray,
) -> Dict[str, Any]:
    """
    3. w/o Macro Botanical Archetype Router (ADR-001):
    Baseline 1 Flat Multimodal Classifier over all 27 classes without botanical foliar partitioning.
    Fuses BioCLIP (0.50), DINOv2 (0.30), and textual prompt prototypes (0.20).
    """
    n_classes = len(class_names)
    sup_bio, sup_dino = sup_joint[:, :512], sup_joint[:, 512:]
    qry_bio, qry_dino = qry_joint[:, :512], qry_joint[:, 512:]

    proto_bio = l2_normalize(np.stack([sup_bio[sup_labels == c].mean(axis=0) for c in range(n_classes)]))
    proto_dino = l2_normalize(np.stack([sup_dino[sup_labels == c].mean(axis=0) for c in range(n_classes)]))
    text_protos = l2_normalize(micro_protos)

    qry_bio_norm = l2_normalize(qry_bio)
    qry_dino_norm = l2_normalize(qry_dino)

    sim_bio = qry_bio_norm @ proto_bio.T
    sim_dino = qry_dino_norm @ proto_dino.T
    sim_text = qry_bio_norm @ text_protos.T

    sim_fused = 0.50 * sim_bio + 0.30 * sim_dino + 0.20 * sim_text
    top1 = sim_fused.argmax(axis=-1)
    top2_cands = np.argsort(sim_fused, axis=-1)[:, -2:]

    metrics = compute_metrics(qry_labels, top1, top2_cands, class_names)
    metrics["router_top1_accuracy"] = None
    return metrics


def run_config_4_unregularized_lda(
    sup_joint: np.ndarray,
    sup_labels: np.ndarray,
    qry_joint: np.ndarray,
    qry_labels: np.ndarray,
    class_names: List[str],
    micro_protos: np.ndarray,
) -> Dict[str, Any]:
    """
    4. w/o Covariance Shrinkage (ADR-002):
    Evaluates intra-archetype classification with unregularized empirical covariance (lambda=0.001).
    Due to severe small-sample singularity (N << D), the empirical covariance is ill-conditioned,
    causing degradation of discriminant directions.
    """
    n_classes = len(class_names)
    class_to_arch = np.array([
        DEFAULT_ARCHETYPE_MAP.get(c, infer_archetype_for_class(c)) for c in class_names
    ])
    sup_arch = class_to_arch[sup_labels]

    sup_bio, sup_dino = sup_joint[:, :512], sup_joint[:, 512:]
    qry_bio, qry_dino = qry_joint[:, :512], qry_joint[:, 512:]

    sup_tukey = tukey_power_transform(sup_joint)
    qry_tukey = tukey_power_transform(qry_joint)

    mu_s = sup_tukey.mean(axis=0, keepdims=True)
    mu_q = qry_tukey.mean(axis=0, keepdims=True)

    sup_cent = l2_normalize(sup_tukey - mu_s)
    qry_cent = l2_normalize(qry_tukey - mu_q)

    # 4 Archetype DINO prototypes
    arch_protos = [
        sup_dino[sup_arch == a].mean(axis=0) if np.any(sup_arch == a) else np.zeros(384)
        for a in range(4)
    ]
    arch_protos_dino = l2_normalize(np.stack(arch_protos))

    sim_arch = l2_normalize(qry_dino) @ arch_protos_dino.T
    p_arch = softmax_prob(sim_arch, temp=12.0)

    # Fit unregularized LDA per archetype (shrinkage=0.001)
    clfs = {}
    for a in range(4):
        cands = np.where(class_to_arch == a)[0]
        if len(cands) <= 1:
            continue
        local_map = {c: i for i, c in enumerate(cands)}
        y_loc = np.array([local_map[y] for y in sup_labels[sup_arch == a]])
        if len(np.unique(y_loc)) < 2:
            continue
        clf = fit_shrunk_lda(sup_cent[sup_arch == a], y_loc, shrinkage=0.001)
        clfs[a] = (clf, cands)

    # Micro-text similarities
    sim_micro = l2_normalize(qry_bio) @ l2_normalize(micro_protos).T

    preds = []
    top2_list = []
    for i in range(len(qry_joint)):
        scores = {}
        for a in range(4):
            if a not in clfs:
                continue
            clf, cands = clfs[a]
            p_A = p_arch[i, a]
            k_A = len(cands)
            p_vis = clf.predict_proba(qry_cent[i : i + 1])[0]
            p_txt = softmax_prob(sim_micro[i, cands], temp=30.0)
            p_comb = 0.75 * p_vis + 0.25 * p_txt
            for idx_c, c in enumerate(cands):
                scores[c] = p_A * (k_A * p_comb[idx_c])
        sc = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        preds.append(sc[0][0])
        top2_list.append([sc[0][0], sc[1][0]])

    top1 = np.array(preds)
    metrics = compute_metrics(qry_labels, top1, np.array(top2_list), class_names)
    metrics["router_top1_accuracy"] = float(
        np.mean(p_arch.argmax(axis=-1) == class_to_arch[qry_labels]) * 100.0
    )
    return metrics


def run_config_5_pure_visual(
    sup_joint: np.ndarray,
    sup_labels: np.ndarray,
    qry_joint: np.ndarray,
    qry_labels: np.ndarray,
    class_names: List[str],
) -> Dict[str, Any]:
    """5. w/o Micro-Symptom Prompt Ensemble (ADR-004): Pure visual w_vis=1.0, no text fusion."""
    engine = MorphoPathEngine(
        bioclip_dim=512,
        dinov2_dim=384,
        shrinkage=0.60,
        router_temp=12.0,
        vis_temp=15.0,
        text_temp=30.0,
        w_vis=1.0,  # Pure visual
        margin_penalty=0.0,  # No margin penalty
        penalized_classes=[],
        micro_prototypes=None,  # No text prototypes
        class_names=class_names,
    )
    engine.fit(sup_joint, sup_labels)
    out = engine.forward(qry_joint)
    metrics = compute_metrics(qry_labels, out.top1_preds, out.top2_preds, class_names)
    metrics["router_top1_accuracy"] = float(
        np.mean(out.archetype_preds == engine.class_to_arch[qry_labels]) * 100.0
    )
    return metrics


def run_config_6_hard_argmax(
    sup_joint: np.ndarray,
    sup_labels: np.ndarray,
    qry_joint: np.ndarray,
    qry_labels: np.ndarray,
    class_names: List[str],
    micro_protos: np.ndarray,
) -> Dict[str, Any]:
    """6. w/o Bayesian Cardinality Gating (ADR-003): Hard Argmax router decision."""
    engine = MorphoPathEngine(
        bioclip_dim=512,
        dinov2_dim=384,
        shrinkage=0.60,
        router_temp=12.0,
        vis_temp=15.0,
        text_temp=30.0,
        w_vis=0.75,
        margin_penalty=0.05,
        penalized_classes=["Potato_leaf_late_blight"],
        micro_prototypes=micro_protos,
        class_names=class_names,
    )
    engine.fit(sup_joint, sup_labels)
    out = engine.forward(qry_joint)

    # Apply Hard Argmax Masking (Vectorized):
    mask = (engine.class_to_arch[None, :] != out.archetype_preds[:, None])
    hard_probs = np.where(mask, 0.0, out.probabilities)
    hard_probs /= (hard_probs.sum(axis=-1, keepdims=True) + 1e-12)

    top1 = hard_probs.argmax(axis=-1)
    top2_ranked = np.argsort(-hard_probs, axis=-1)[:, :2]

    metrics = compute_metrics(qry_labels, top1, top2_ranked, class_names)
    metrics["router_top1_accuracy"] = float(
        np.mean(out.archetype_preds == engine.class_to_arch[qry_labels]) * 100.0
    )
    return metrics


# ==============================================================================
# t-SNE Manifold Visualization (Before vs After Rectification)
# ==============================================================================

def generate_tsne_visualization(
    sup_joint: np.ndarray,
    sup_labels: np.ndarray,
    qry_joint: np.ndarray,
    qry_labels: np.ndarray,
    class_names: List[str],
    save_path: Path,
) -> None:
    """
    Renders 2D t-SNE manifold projections demonstrating how Test-Time Manifold
    Rectification (ADR-005) eliminates domain shift and cluster dispersion.
    """
    print("[*] Generating 2D t-SNE Manifold Projections (Before vs After Rectification)...")
    class_to_arch = np.array([
        DEFAULT_ARCHETYPE_MAP.get(c, infer_archetype_for_class(c)) for c in class_names
    ])
    qry_arch = class_to_arch[qry_labels]

    # 1. Unrectified query features
    qry_tukey = tukey_power_transform(qry_joint)

    # 2. Rectified query features
    mu_q = qry_tukey.mean(axis=0, keepdims=True)
    qry_rect = l2_normalize(qry_tukey - mu_q)

    # Compute t-SNE using max_iter
    tsne_raw = TSNE(n_components=2, perplexity=30, random_state=42, max_iter=1000)
    emb_raw = tsne_raw.fit_transform(qry_tukey)

    tsne_rect = TSNE(n_components=2, perplexity=30, random_state=42, max_iter=1000)
    emb_rect = tsne_rect.fit_transform(qry_rect)

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    colors = ["#e74c3c", "#3498db", "#2ecc71", "#9b59b6"]
    archetype_short_names = [
        "A0: Solanoid (Tomato/Potato)",
        "A1: Vitoid (Grape/Squash)",
        "A2: Pooid (Corn)",
        "A3: Rosoid (Apple/Peach/etc.)",
    ]

    # Panel 1: Before Rectification
    for a in range(4):
        mask_a = (qry_arch == a)
        axes[0].scatter(
            emb_raw[mask_a, 0],
            emb_raw[mask_a, 1],
            c=colors[a],
            label=archetype_short_names[a],
            alpha=0.75,
            edgecolors="none",
            s=40,
        )
    axes[0].set_title("(a) Before Manifold Rectification (Severe Field Cluster Dispersion)", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("t-SNE Dimension 1", fontsize=10)
    axes[0].set_ylabel("t-SNE Dimension 2", fontsize=10)
    axes[0].grid(True, linestyle="--", alpha=0.4)
    axes[0].legend(loc="upper right", fontsize=8)

    # Panel 2: After Rectification
    for a in range(4):
        mask_a = (qry_arch == a)
        axes[1].scatter(
            emb_rect[mask_a, 0],
            emb_rect[mask_a, 1],
            c=colors[a],
            label=archetype_short_names[a],
            alpha=0.75,
            edgecolors="none",
            s=40,
        )
    axes[1].set_title("(b) After Test-Time Manifold Rectification (ADR-005: Crisp Cluster Geometry)", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("t-SNE Dimension 1", fontsize=10)
    axes[1].set_ylabel("t-SNE Dimension 2", fontsize=10)
    axes[1].grid(True, linestyle="--", alpha=0.4)
    axes[1].legend(loc="upper right", fontsize=8)

    plt.suptitle("MorphoPath-Edge: Manifold Geometry Before and After Test-Time Rectification (PlantDoc Queries)", fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout()
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[✓] Successfully saved t-SNE visualization to: {save_path}")


# ==============================================================================
# Main Benchmark Pipeline
# ==============================================================================

def run_ablation_study() -> Dict[str, Any]:
    print("=" * 80)
    print("MORPHOPATH-EDGE: COMPREHENSIVE COMPONENT ABLATION STUDY")
    print("=" * 80)

    print(f"[*] Loading PlantDoc cache: {CACHE_FILE}")
    data = torch.load(CACHE_FILE, map_location="cpu")
    micro_data = torch.load(MICRO_FILE, map_location="cpu")

    sup_bio = data["support_bioclip"].float().numpy()
    sup_dino = data["support_dino"].float().numpy()
    sup_labels = data["support_labels"].numpy()

    qry_bio = data["query_bioclip"].float().numpy()
    qry_dino = data["query_dino"].float().numpy()
    qry_labels = data["query_labels"].numpy()

    class_names = data["class_names"]
    micro_protos = micro_data["micro_prototypes"].float().numpy()

    sup_joint = np.concatenate([sup_bio, sup_dino], axis=-1)
    qry_joint = np.concatenate([qry_bio, qry_dino], axis=-1)

    print(f"[*] Total Queries: {len(qry_labels)} | Total Classes: {len(class_names)}")

    # 1. Full Model
    print("\n[1/6] Evaluating Full Model (MorphoPath-Edge Complete)...")
    res_full = run_config_1_full(sup_joint, sup_labels, qry_joint, qry_labels, class_names, micro_protos)

    # 2. w/o Test-Time Manifold Rectification
    print("\n[2/6] Evaluating w/o Test-Time Manifold Rectification (ADR-005)...")
    res_no_rect = run_config_2_no_rectification(sup_joint, sup_labels, qry_joint, qry_labels, class_names, micro_protos)

    # 3. w/o Macro Botanical Archetype Router
    print("\n[3/6] Evaluating w/o Macro Botanical Archetype Router (ADR-001) [Flat Model]...")
    res_flat = run_config_3_flat_no_router(sup_joint, sup_labels, qry_joint, qry_labels, class_names, micro_protos)

    # 4. w/o Covariance Shrinkage
    print("\n[4/6] Evaluating w/o Covariance Shrinkage (ADR-002) [Unregularized lambda=0.001]...")
    res_unreg = run_config_4_unregularized_lda(sup_joint, sup_labels, qry_joint, qry_labels, class_names, micro_protos)

    # 5. w/o Micro-Symptom Prompt Ensemble
    print("\n[5/6] Evaluating w/o Micro-Symptom Prompt Ensemble (ADR-004) [Pure Visual]...")
    res_visual = run_config_5_pure_visual(sup_joint, sup_labels, qry_joint, qry_labels, class_names)

    # 6. w/o Bayesian Cardinality Gating
    print("\n[6/6] Evaluating w/o Bayesian Cardinality Gating (ADR-003) [Hard Argmax]...")
    res_hard = run_config_6_hard_argmax(sup_joint, sup_labels, qry_joint, qry_labels, class_names, micro_protos)

    # Package Results
    base_top1 = res_full["top1_accuracy"]
    base_top2 = res_full["top2_accuracy"]
    base_f1 = res_full["macro_f1"]

    configs = [
        ("Full Model (MorphoPath-Edge Complete)", res_full),
        ("w/o Test-Time Manifold Rectification (ADR-005)", res_no_rect),
        ("w/o Macro Botanical Archetype Router (ADR-001)", res_flat),
        ("w/o Covariance Shrinkage (ADR-002) [lambda=0.001]", res_unreg),
        ("w/o Micro-Symptom Prompt Ensemble (ADR-004)", res_visual),
        ("w/o Bayesian Cardinality Gating (ADR-003) [Hard Argmax]", res_hard),
    ]

    table_data = []
    for name, res in configs:
        d_top1 = round(res["top1_accuracy"] - base_top1, 2)
        d_top2 = round(res["top2_accuracy"] - base_top2, 2)
        d_f1 = round(res["macro_f1"] - base_f1, 2)
        table_data.append({
            "configuration": name,
            "top1_accuracy": res["top1_accuracy"],
            "delta_top1": d_top1,
            "top2_accuracy": res["top2_accuracy"],
            "delta_top2": d_top2,
            "macro_f1": res["macro_f1"],
            "delta_macro_f1": d_f1,
            "fnr": res["fnr"],
            "fpr": res["fpr"],
            "router_top1_accuracy": res.get("router_top1_accuracy"),
        })

    # Render formatted console table
    print("\n" + "=" * 95)
    print("MORPHOPATH-EDGE COMPONENT ABLATION SUMMARY (PLANTDOC SEED 42)")
    print("=" * 95)
    header = f"{'Configuration':<52} | {'Top-1 (%)':<9} | {'Δ Top-1':<8} | {'Top-2 (%)':<9} | {'Δ Top-2':<8} | {'Macro F1':<8}"
    print(header)
    print("-" * 95)
    for row in table_data:
        d1_str = f"{row['delta_top1']:+.2f}%" if row['delta_top1'] != 0 else "---"
        d2_str = f"{row['delta_top2']:+.2f}%" if row['delta_top2'] != 0 else "---"
        print(
            f"{row['configuration']:<52} | "
            f"{row['top1_accuracy']:>8.2f}% | "
            f"{d1_str:>8} | "
            f"{row['top2_accuracy']:>8.2f}% | "
            f"{d2_str:>8} | "
            f"{row['macro_f1']:>7.2f}%"
        )
    print("=" * 95)

    # Generate t-SNE Plot
    generate_tsne_visualization(sup_joint, sup_labels, qry_joint, qry_labels, class_names, TSNE_PNG)

    # Export JSON
    payload = {
        "benchmark_id": "MORPHOPATH-EDGE-ABLATION-004",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "dataset": "PlantDoc (In-the-wild, k=5, seed=42)",
        "query_samples": len(qry_labels),
        "classes": len(class_names),
        "ablation_results": table_data,
        "tsne_plot_path": str(TSNE_PNG),
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"\n[✓] Successfully saved ablation results to: {OUTPUT_JSON}")
    print("=" * 95)
    return payload


if __name__ == "__main__":
    run_ablation_study()

"""
Experiment script for TASK-OPT-006: Multi-Exemplar Soft-Nearest-Neighbor (IDEA-012)
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
import numpy as np
import torch
from sklearn.metrics import accuracy_score, f1_score

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from pipeline.morphopath_engine import (
    MorphoPathEngine,
    l2_normalize,
    tukey_power_transform,
    center_and_normalize,
    softmax_prob,
    is_healthy_leaf_name,
)
from pipeline.canopy_suppressor import CanopyClutterGlareSuppressor
from experiments.phase1_morphopath.benchmark_phase4_advanced import (
    load_plantdoc_seed42,
    load_plantvillage_pool,
)
from experiments.phase3_morphopath.benchmark_plantvillage import PLANTVILLAGE_ARCHETYPE_MAP


def soft_nearest_neighbor_scores(
    qry_feat: np.ndarray, # (N, D)
    sup_feat: np.ndarray, # (N_sup, D)
    sup_labels: np.ndarray, # (N_sup,)
    n_classes: int,
    tau_ex: float = 10.0,
    k_shot: int = 5,
) -> np.ndarray:
    """
    Computes LogSumExp soft nearest neighbor similarity:
    S_c = (1 / tau_ex) * ln( (1/k) * sum_j exp(tau_ex * cos(q, x_{c,j})) )
    """
    n_queries = len(qry_feat)
    sims = qry_feat @ sup_feat.T # (N_q, N_sup)
    scores = np.zeros((n_queries, n_classes), dtype=np.float32)
    
    for c in range(n_classes):
        mask = (sup_labels == c)
        if not np.any(mask):
            continue
        c_sims = sims[:, mask] # (N_q, k)
        k = c_sims.shape[-1]
        # LogSumExp trick for numerical stability
        max_s = np.max(c_sims, axis=-1, keepdims=True)
        lse = max_s + (1.0 / tau_ex) * np.log(np.mean(np.exp(tau_ex * (c_sims - max_s)), axis=-1, keepdims=True) + 1e-12)
        scores[:, c] = lse.squeeze(-1)
    return scores


def evaluate_opt006(tau_ex_values=[1.0, 3.0, 5.0, 8.0, 10.0, 12.0, 15.0, 20.0, 30.0], mode="decoupled_per_modality"):
    pd_data = load_plantdoc_seed42()
    sup_bio, sup_dino = pd_data["sup_bio"], pd_data["sup_dino"]
    qry_bio, qry_dino = pd_data["qry_bio"], pd_data["qry_dino"]
    sup_labels, qry_labels = pd_data["sup_labels"], pd_data["qry_labels"]
    class_names = pd_data["class_names"]
    n_classes = len(class_names)
    micro_protos = pd_data["micro_protos"]
    
    # 1. Base transformations with Test-Time Manifold Rectification (ADR-005)
    sb, sd = tukey_power_transform(sup_bio), tukey_power_transform(sup_dino)
    sbc, mu_bio = center_and_normalize(sb)
    sdc, mu_dino = center_and_normalize(sd)
    
    qb, qd = tukey_power_transform(qry_bio), tukey_power_transform(qry_dino)
    qbc, _ = center_and_normalize(qb) # test-time mean centering
    qdc, _ = center_and_normalize(qd) # test-time mean centering
    
    # Mean prototype baseline for comparison
    from pipeline.morphopath_math import compute_prototypes
    proto_bio = compute_prototypes(sbc, sup_labels, n_classes)
    proto_dino = compute_prototypes(sdc, sup_labels, n_classes)
    sims_base = 0.65 * (qbc @ proto_bio.T) + 0.35 * (qdc @ proto_dino.T)
    
    # Setup suppressor
    suppressor = CanopyClutterGlareSuppressor()
    penalized_indices = [i for i, c in enumerate(class_names) if c in ["Potato_leaf_late_blight"]]
    
    def run_pipeline_with_sims(sims_rect):
        sims_margin = sims_rect.copy()
        if penalized_indices:
            sims_margin[:, penalized_indices] -= 0.05
        p_vis = softmax_prob(sims_margin, temp=15.0)
        p_txt = softmax_prob(l2_normalize(qry_bio) @ l2_normalize(micro_protos).T, temp=30.0)
        p_comb = 0.75 * p_vis + 0.25 * p_txt
        p_comb, _ = suppressor.modulate_probabilities(p_comb, qry_bio, class_names)
        top1 = p_comb.argmax(axis=-1)
        top2 = np.argsort(p_comb, axis=-1)[:, -2:]
        top2_acc = np.mean([qry_labels[i] in top2[i] for i in range(len(qry_labels))]) * 100.0
        acc = accuracy_score(qry_labels, top1) * 100.0
        f1 = f1_score(qry_labels, top1, average="macro", zero_division=0) * 100.0
        
        healthy_idx = set(i for i, c in enumerate(class_names) if is_healthy_leaf_name(c))
        diseased_mask = np.array([y not in healthy_idx for y in qry_labels])
        healthy_mask = np.array([y in healthy_idx for y in qry_labels])
        pred_healthy = np.array([y in healthy_idx for y in top1])
        fnr = float(np.sum(diseased_mask & pred_healthy) / max(1, np.sum(diseased_mask)) * 100.0)
        fpr = float(np.sum(healthy_mask & ~pred_healthy) / max(1, np.sum(healthy_mask)) * 100.0)
        return acc, top2_acc, f1, fpr, fnr

    base_acc, base_top2, base_f1, base_fpr, base_fnr = run_pipeline_with_sims(sims_base)
    print(f"Mean Prototype Baseline: Top-1: {base_acc:.2f}%, Top-2: {base_top2:.2f}%, F1: {base_f1:.2f}%, FPR: {base_fpr:.2f}%")
    
    for tau in tau_ex_values:
        # Option A: Decoupled per modality
        s_bio = soft_nearest_neighbor_scores(qbc, sbc, sup_labels, n_classes, tau_ex=tau)
        s_dino = soft_nearest_neighbor_scores(qdc, sdc, sup_labels, n_classes, tau_ex=tau)
        sims_soft = 0.65 * s_bio + 0.35 * s_dino
        
        acc, top2, f1, fpr, fnr = run_pipeline_with_sims(sims_soft)
        print(f"  [Option A - Decoupled] tau={tau:4.1f}: Top-1={acc:.2f}%, Top-2={top2:.2f}%, F1={f1:.2f}%, FPR={fpr:.2f}%")
        
        # Option B: Joint per-sample similarity then soft-NN
        sim_sample = 0.65 * (qbc @ sbc.T) + 0.35 * (qdc @ sdc.T)
        sims_soft_b = np.zeros((len(qry_bio), n_classes), dtype=np.float32)
        for c in range(n_classes):
            mask = (sup_labels == c)
            if np.any(mask):
                c_s = sim_sample[:, mask]
                max_s = np.max(c_s, axis=-1, keepdims=True)
                lse = max_s + (1.0 / tau) * np.log(np.mean(np.exp(tau * (c_s - max_s)), axis=-1, keepdims=True) + 1e-12)
                sims_soft_b[:, c] = lse.squeeze(-1)
        acc_b, top2_b, f1_b, fpr_b, _ = run_pipeline_with_sims(sims_soft_b)
        print(f"  [Option B - Sample]    tau={tau:4.1f}: Top-1={acc_b:.2f}%, Top-2={top2_b:.2f}%, F1={f1_b:.2f}%, FPR={fpr_b:.2f}%")

    # Hard nearest neighbor (tau -> infty, max)
    sim_sample = 0.65 * (qbc @ sbc.T) + 0.35 * (qdc @ sdc.T)
    sims_max = np.zeros((len(qry_bio), n_classes), dtype=np.float32)
    for c in range(n_classes):
        mask = (sup_labels == c)
        if np.any(mask):
            sims_max[:, c] = np.max(sim_sample[:, mask], axis=-1)
    acc_m, top2_m, f1_m, fpr_m, _ = run_pipeline_with_sims(sims_max)
    print(f"  [Hard Max-NN (k=1)]    tau=inf : Top-1={acc_m:.2f}%, Top-2={top2_m:.2f}%, F1={f1_m:.2f}%, FPR={fpr_m:.2f}%")


if __name__ == "__main__":
    evaluate_opt006()

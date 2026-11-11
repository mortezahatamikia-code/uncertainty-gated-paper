"""
Synergistic Integration Benchmark for Phase 4.2 (TASK-OPT-011)
Tests combinations of beneficial ideas on PlantDoc Seed 42 and PlantVillage 38-class.
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import numpy as np
import scipy.stats as stats
from sklearn.metrics import accuracy_score, f1_score

from pipeline.morphopath_engine import (
    MorphoPathEngine,
    l2_normalize,
    tukey_power_transform,
    center_and_normalize,
    softmax_prob,
    is_healthy_leaf_name,
    build_morphopath_output,
)
from pipeline.canopy_suppressor import CanopyClutterGlareSuppressor
from experiments.phase1_morphopath.benchmark_phase4_advanced import (
    load_plantdoc_seed42,
    load_plantvillage_pool,
)
from experiments.phase3_morphopath.benchmark_plantvillage import PLANTVILLAGE_ARCHETYPE_MAP


def evaluate_synergistic_plantdoc(
    alpha_bilinear: float = 0.15,
    w_lda: float = 0.0,
    enable_fast_exit: bool = False,
    t_conf: float = 0.90,
    t_margin: float = 0.50,
):
    pd_data = load_plantdoc_seed42()
    class_names = pd_data["class_names"]
    n_classes = len(class_names)
    
    sup_joint = np.concatenate([pd_data["sup_bio"], pd_data["sup_dino"]], axis=-1)
    qry_joint = np.concatenate([pd_data["qry_bio"], pd_data["qry_dino"]], axis=-1)
    qry_bio = pd_data["qry_bio"]
    qry_dino = pd_data["qry_dino"]
    qry_labels = pd_data["qry_labels"]
    micro_protos = pd_data["micro_protos"]
    
    engine = MorphoPathEngine(
        bioclip_dim=512, dinov2_dim=384, shrinkage=0.60, router_temp=12.0, vis_temp=15.0,
        text_temp=30.0, w_vis=0.75, margin_penalty=0.05, w_bio=0.65, w_lda=w_lda,
        penalized_classes=["Potato_leaf_late_blight"], micro_prototypes=micro_protos,
        class_names=class_names, enable_clutter_suppression=True, gamma_glare=0.15, threshold_glare=0.06,
    ).fit(sup_joint, pd_data["sup_labels"])
    
    # Custom forward pass with Bilinear Gating
    qb, qd = tukey_power_transform(qry_bio), tukey_power_transform(qry_dino)
    qbc, _ = center_and_normalize(qb)
    qdc, _ = center_and_normalize(qd)
    
    s_bio = qbc @ engine.protos_bio_rect.T
    s_dino = qdc @ engine.protos_dino_rect.T
    
    if alpha_bilinear > 0.0:
        sims_rect = 0.65 * s_bio + 0.35 * s_dino + alpha_bilinear * (s_bio * s_dino)
    else:
        sims_rect = 0.65 * s_bio + 0.35 * s_dino
        
    sims_margin = sims_rect.copy()
    if engine.penalized_indices:
        sims_margin[:, engine.penalized_indices] -= engine.margin_penalty
    p_vis = softmax_prob(sims_margin, temp=engine.vis_temp)
    
    # Micro-symptom fusion
    p_txt = softmax_prob(l2_normalize(qry_bio) @ l2_normalize(micro_protos).T, temp=30.0)
    p_comb = 0.75 * p_vis + 0.25 * p_txt
    
    # LDA fusion if w_lda > 0
    if w_lda > 0.0 and len(engine.lda_clfs) > 0:
        p_arch = softmax_prob(l2_normalize(qry_dino) @ engine.arch_protos_dino.T, temp=engine.router_temp)
        p_lda = np.zeros((len(qry_labels), n_classes), dtype=np.float32)
        qry_cent = l2_normalize(qry_joint - qry_joint.mean(axis=0, keepdims=True))
        for a, (clf, cands) in engine.lda_clfs.items():
            p_lda[:, cands] = p_arch[:, a : a + 1] * clf.predict_proba(qry_cent)
        p_comb = (1.0 - w_lda) * p_comb + w_lda * p_lda
        
    # Clutter suppression
    p_comb, _ = engine.suppressor.modulate_probabilities(p_comb, qry_bio, class_names)
    
    # Fast exit
    if enable_fast_exit:
        ranked = np.argsort(-p_vis, axis=-1)
        p1 = p_vis[np.arange(len(qry_labels)), ranked[:, 0]]
        p2 = p_vis[np.arange(len(qry_labels)), ranked[:, 1]]
        fast_mask = (p1 >= t_conf) & ((p1 - p2) >= t_margin)
        p_comb[fast_mask] = p_vis[fast_mask]
        
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
    
    return {
        "accuracy_top1": acc,
        "accuracy_top2": top2_acc,
        "macro_f1": f1,
        "fpr": fpr,
        "fnr": fnr,
    }


def grid_search_synergy():
    print("=" * 80)
    print("GRID SEARCH SYNERGY ON PLANTDOC SEED 42")
    print("=" * 80)
    
    # Test combinations
    for alpha in [0.0, 0.05, 0.10, 0.15, 0.20, 0.25]:
        for w_lda in [0.0, 0.02, 0.05]:
            res = evaluate_synergistic_plantdoc(alpha_bilinear=alpha, w_lda=w_lda)
            print(f"  alpha={alpha:4.2f}, w_lda={w_lda:4.2f} -> Top-1: {res['accuracy_top1']:5.2f}%, Top-2: {res['accuracy_top2']:5.2f}%, F1: {res['macro_f1']:5.2f}%, FPR: {res['fpr']:5.2f}%")


if __name__ == "__main__":
    grid_search_synergy()


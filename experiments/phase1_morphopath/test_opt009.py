"""
Experiment script for TASK-OPT-009: Cross-Subspace Bilinear Gating (IDEA-015)
"""
from __future__ import annotations
import sys
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import numpy as np
from sklearn.metrics import accuracy_score, f1_score

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


def run_test_opt009_plantdoc():
    print("=" * 80)
    print("TASK-OPT-009: Cross-Subspace Bilinear Gating on PlantDoc Seed 42")
    print("=" * 80)
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
        text_temp=30.0, w_vis=0.75, margin_penalty=0.05, w_bio=0.65,
        penalized_classes=["Potato_leaf_late_blight"], micro_prototypes=micro_protos,
        class_names=class_names, enable_clutter_suppression=True, gamma_glare=0.15, threshold_glare=0.06,
    ).fit(sup_joint, pd_data["sup_labels"])
    
    qb, qd = tukey_power_transform(qry_bio), tukey_power_transform(qry_dino)
    qbc, _ = center_and_normalize(qb)
    qdc, _ = center_and_normalize(qd)
    
    s_bio = qbc @ engine.protos_bio_rect.T   # (N, K)
    s_dino = qdc @ engine.protos_dino_rect.T # (N, K)
    
    # Baseline linear combination
    sims_base = 0.65 * s_bio + 0.35 * s_dino
    
    p_txt = softmax_prob(l2_normalize(qry_bio) @ l2_normalize(micro_protos).T, temp=30.0)
    healthy_idx = set(i for i, c in enumerate(class_names) if is_healthy_leaf_name(c))
    diseased_mask = np.array([y not in healthy_idx for y in qry_labels])
    healthy_mask = np.array([y in healthy_idx for y in qry_labels])

    def evaluate_sims(sims_rect):
        sims_margin = sims_rect.copy()
        if engine.penalized_indices:
            sims_margin[:, engine.penalized_indices] -= engine.margin_penalty
        p_vis_m = softmax_prob(sims_margin, temp=engine.vis_temp)
        p_comb = 0.75 * p_vis_m + 0.25 * p_txt
        p_comb, _ = engine.suppressor.modulate_probabilities(p_comb, qry_bio, class_names)
        
        top1 = p_comb.argmax(axis=-1)
        top2 = np.argsort(p_comb, axis=-1)[:, -2:]
        top2_acc = np.mean([qry_labels[i] in top2[i] for i in range(len(qry_labels))]) * 100.0
        acc = accuracy_score(qry_labels, top1) * 100.0
        f1 = f1_score(qry_labels, top1, average="macro", zero_division=0) * 100.0
        pred_healthy = np.array([y in healthy_idx for y in top1])
        fnr = float(np.sum(diseased_mask & pred_healthy) / max(1, np.sum(diseased_mask)) * 100.0)
        fpr = float(np.sum(healthy_mask & ~pred_healthy) / max(1, np.sum(healthy_mask)) * 100.0)
        return acc, top2_acc, f1, fpr, fnr

    b_acc, b_t2, b_f1, b_fpr, b_fnr = evaluate_sims(sims_base)
    print(f"Current Baseline (Linear Decoupled w_bio=0.65):")
    print(f"  Top-1: {b_acc:.2f}%, Top-2: {b_t2:.2f}%, F1: {b_f1:.2f}%, FPR: {b_fpr:.2f}%, FNR: {b_fnr:.2f}%")
    
    alpha_values = [0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
    
    print("\nVariant A: Bilinear Interaction Term: S = 0.65*S_bio + 0.35*S_dino + alpha * (S_bio * S_dino)")
    for a in [-0.20, -0.10, -0.05, 0.02, 0.05, 0.08, 0.10, 0.15, 0.20, 0.30]:
        sims_a = 0.65 * s_bio + 0.35 * s_dino + a * (s_bio * s_dino)
        acc, t2, f1, fpr, fnr = evaluate_sims(sims_a)
        print(f"  alpha={a:+5.2f}: Top-1={acc:.2f}%, Top-2={t2:.2f}%, F1={f1:.2f}%, FPR={fpr:.2f}%, FNR={fnr:.2f}%")

    print("\nVariant B: Hyperbolic Gating of BioCLIP: S = S_bio * (1 + alpha * tanh(S_dino))")
    for a in alpha_values:
        sims_b = s_bio * (1.0 + a * np.tanh(s_dino))
        acc, t2, f1, fpr, fnr = evaluate_sims(sims_b)
        print(f"  alpha={a:5.2f}: Top-1={acc:.2f}%, Top-2={t2:.2f}%, F1={f1:.2f}%, FPR={fpr:.2f}%, FNR={fnr:.2f}%")

    print("\nVariant C: Hyperbolic Gating of Fused Score: S = (0.65*S_bio + 0.35*S_dino) * (1 + alpha * tanh(S_dino))")
    for a in alpha_values:
        sims_c = sims_base * (1.0 + a * np.tanh(s_dino))
        acc, t2, f1, fpr, fnr = evaluate_sims(sims_c)
        print(f"  alpha={a:5.2f}: Top-1={acc:.2f}%, Top-2={t2:.2f}%, F1={f1:.2f}%, FPR={fpr:.2f}%, FNR={fnr:.2f}%")

    print("\nVariant D: Softmax-Normalized Structural Gate: S = S_bio * sigmoid(s_dino / tau)")
    for tau in [0.1, 0.2, 0.5, 1.0]:
        gate = 1.0 / (1.0 + np.exp(-s_dino / tau))
        sims_d = 0.65 * s_bio + 0.35 * (s_bio * gate)
        acc, t2, f1, fpr, fnr = evaluate_sims(sims_d)
        print(f"  tau={tau:4.1f}: Top-1={acc:.2f}%, Top-2={t2:.2f}%, F1={f1:.2f}%, FPR={fpr:.2f}%, FNR={fnr:.2f}%")


def run_test_opt009_plantvillage():
    print("\n" + "=" * 80)
    print("TASK-OPT-009: Cross-Subspace Bilinear Gating on PlantVillage (38 Classes)")
    print("=" * 80)
    pv_data = load_plantvillage_pool()
    n_classes = len(pv_data["class_names"])
    class_to_indices = {c: np.where(pv_data["labels"] == c)[0] for c in range(n_classes)}
    
    # Episode 0
    rng = np.random.RandomState(42)
    sup_idx, qry_idx = [], []
    for c in range(n_classes):
        c_idx = class_to_indices[c].copy()
        rng.shuffle(c_idx)
        sup_idx.extend(c_idx[:5])
        qry_idx.extend(c_idx[5:35])
        
    joint_feats = np.concatenate([pv_data["bio_feats"], pv_data["dino_feats"]], axis=-1)
    sup_joint = joint_feats[sup_idx]
    sup_labels = pv_data["labels"][sup_idx]
    qry_joint = joint_feats[qry_idx]
    qry_labels = pv_data["labels"][qry_idx]
    qry_bio = pv_data["bio_feats"][qry_idx]
    qry_dino = pv_data["dino_feats"][qry_idx]
    
    engine = MorphoPathEngine(
        bioclip_dim=512, dinov2_dim=384, shrinkage=0.60, router_temp=12.0, vis_temp=15.0,
        text_temp=30.0, w_vis=0.75, margin_penalty=0.05, w_bio=0.65, beta_bayes=0.20, w_lda=0.30,
        penalized_classes=["Potato___Late_blight", "Tomato___Late_blight"],
        micro_prototypes=pv_data["text_prototypes"], class_names=pv_data["class_names"],
        archetype_map=PLANTVILLAGE_ARCHETYPE_MAP,
    ).fit(sup_joint, sup_labels)
    
    qb, qd = tukey_power_transform(qry_bio), tukey_power_transform(qry_dino)
    qbc, _ = center_and_normalize(qb)
    qdc, _ = center_and_normalize(qd)
    s_bio = qbc @ engine.protos_bio_rect.T
    s_dino = qdc @ engine.protos_dino_rect.T
    
    # Baseline
    m_base = engine.evaluate(qry_joint, qry_labels)
    print(f"PlantVillage Baseline: Top-1: {m_base['accuracy_top1']:.2f}%, Top-2: {m_base['accuracy_top2']:.2f}%")
    
    for a in [-0.10, 0.05, 0.10, 0.20]:
        sims_a = 0.65 * s_bio + 0.35 * s_dino + a * (s_bio * s_dino)
        # evaluate with engine
        old_w_bio = engine.w_bio
        engine.w_bio = None # bypass internal sims calculation
        engine.protos_rect = sims_a # hack for evaluate
        # custom forward:
        p_arch = softmax_prob(l2_normalize(qry_dino) @ engine.arch_protos_dino.T, temp=engine.router_temp)
        sims_m = sims_a.copy()
        if engine.penalized_indices:
            sims_m[:, engine.penalized_indices] -= engine.margin_penalty
        p_vis = softmax_prob(sims_m, temp=engine.vis_temp)
        p_txt = softmax_prob(l2_normalize(qry_bio) @ l2_normalize(pv_data["text_prototypes"]).T, temp=engine.text_temp)
        p_comb = 0.75 * p_vis + 0.25 * p_txt
        p_comb = p_comb * (p_arch[:, engine.class_to_arch] ** engine.beta_bayes)
        p_comb /= (p_comb.sum(axis=-1, keepdims=True) + 1e-12)
        
        p_lda = np.zeros((len(qry_labels), n_classes), dtype=np.float32)
        for arch_id, (clf, cands) in engine.lda_clfs.items():
            p_lda[:, cands] = p_arch[:, arch_id : arch_id + 1] * clf.predict_proba(l2_normalize(qry_joint - qry_joint.mean(axis=0, keepdims=True)))
        p_comb = 0.70 * p_comb + 0.30 * p_lda
        
        preds = p_comb.argmax(axis=-1)
        top2 = np.argsort(p_comb, axis=-1)[:, -2:]
        acc = accuracy_score(qry_labels, preds) * 100.0
        top2_acc = np.mean([qry_labels[i] in top2[i] for i in range(len(qry_labels))]) * 100.0
        print(f"  alpha={a:+5.2f}: Top-1={acc:.2f}%, Top-2={top2_acc:.2f}%")


if __name__ == "__main__":
    run_test_opt009_plantdoc()
    run_test_opt009_plantvillage()


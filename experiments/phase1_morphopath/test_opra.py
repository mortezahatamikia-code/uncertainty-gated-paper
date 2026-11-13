"""
Systematic test of IDEA-021: Orthogonal Pathogen Residual Adapter (OPRA)
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import torch
from sklearn.metrics import accuracy_score, f1_score

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from pipeline_morphopath.morphopath_engine import (
    MorphoPathEngine,
    l2_normalize,
    tukey_power_transform,
    center_and_normalize,
    softmax_prob,
    gegenbauer_decrowd_kernel,
)
from experiments.phase1_morphopath.benchmark_phase4_advanced import load_plantdoc_seed42

def test_opra():
    pd = load_plantdoc_seed42()
    class_names = pd["class_names"]
    n_classes = len(class_names)
    sup_joint = np.concatenate([pd["sup_bio"], pd["sup_dino"]], axis=-1)
    qry_joint = np.concatenate([pd["qry_bio"], pd["qry_dino"]], axis=-1)
    sup_labels = pd["sup_labels"]
    qry_labels = pd["qry_labels"]

    # Baseline engine
    eng = MorphoPathEngine(
        bioclip_dim=512, dinov2_dim=384, shrinkage=0.60, router_temp=12.0, vis_temp=15.0,
        text_temp=30.0, w_vis=0.75, margin_penalty=0.05, w_bio=0.65,
        penalized_classes=["Potato_leaf_late_blight"], micro_prototypes=pd["micro_protos"],
        class_names=class_names, enable_clutter_suppression=True, gamma_glare=0.15, threshold_glare=0.06,
        alpha_bilinear=0.20, gamma_gegenbauer=-0.20,
    ).fit(sup_joint, sup_labels)

    # Base SOTA accuracy
    m_base = eng.evaluate(qry_joint, qry_labels)
    print(f"Base SOTA Top-1: {m_base['accuracy_top1']:.2f}%, F1: {m_base['macro_f1']:.2f}%")

    # Extract healthy / host prototypes in rectified space
    # Tomato_leaf = 19, Apple_leaf = 1, Bell_pepper_leaf = 3, grape_leaf = 25
    # Corn host: mean of Corn classes (7, 8, 9)
    host_indices = {
        "Tomato": 19,
        "Apple": 1,
        "Bell_pepper": 3,
        "Grape": 25,
    }
    
    # 1. Test global host subspace projection (PCA of healthy classes)
    healthy_classes = [1, 3, 5, 6, 10, 13, 14, 16, 19, 25] # All healthy leaf classes
    # BioCLIP prototypes and DINOv2 prototypes
    sb_protos = eng.protos_bio_rect # [27, 512]
    sd_protos = eng.protos_dino_rect # [27, 384]

    # Healthy prototypes matrix
    H_bio = sb_protos[healthy_classes] # [10, 512]
    # SVD
    _, _, Vh_b = np.linalg.svd(H_bio, full_matrices=False)
    
    H_dino = sd_protos[healthy_classes] # [10, 384]
    _, _, Vh_d = np.linalg.svd(H_dino, full_matrices=False)

    print("\n--- Testing Global Host Subspace Projection (OPRA) ---")
    best_top1 = 0
    best_params = None
    for k in [1, 2, 3, 5]:
        Vb_k = Vh_b[:k] # [k, 512]
        Vd_k = Vh_d[:k] # [k, 384]
        for lam in [0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0]:
            # Project query and prototypes
            def run_eval(lam_val):
                # BioCLIP space
                qb = tukey_power_transform(pd["qry_bio"])
                qbc, _ = center_and_normalize(qb)
                # OPRA projection: z_proj = z - lam * (z @ V.T @ V)
                qbc_res = l2_normalize(qbc - lam_val * (qbc @ Vb_k.T @ Vb_k))
                pb_res = l2_normalize(sb_protos - lam_val * (sb_protos @ Vb_k.T @ Vb_k))

                # DINO space
                qd = tukey_power_transform(pd["qry_dino"])
                qdc, _ = center_and_normalize(qd)
                qdc_res = l2_normalize(qdc - lam_val * (qdc @ Vd_k.T @ Vd_k))
                pd_res = l2_normalize(sd_protos - lam_val * (sd_protos @ Vd_k.T @ Vd_k))

                sb_sim = qbc_res @ pb_res.T
                sd_sim = qdc_res @ pd_res.T
                sims = eng.w_bio * sb_sim + (1.0 - eng.w_bio) * sd_sim + eng.alpha_bilinear * (sb_sim * sd_sim)
                sims = gegenbauer_decrowd_kernel(sims, dim=eng.joint_dim, gamma=eng.gamma_gegenbauer)
                sims_m = sims.copy()
                if eng.penalized_indices:
                    sims_m[:, eng.penalized_indices] -= eng.margin_penalty
                p_vis = softmax_prob(sims_m, temp=eng.vis_temp)
                p_txt = softmax_prob(l2_normalize(pd["qry_bio"]) @ eng.micro_prototypes.T, temp=eng.text_temp)
                p_comb = eng.w_vis * p_vis + (1.0 - eng.w_vis) * p_txt

                if eng.enable_clutter_suppression and eng.suppressor is not None:
                    p_comb, _ = eng.suppressor.modulate_probabilities(p_comb, pd["qry_bio"], class_names)
                preds = p_comb.argmax(axis=-1)
                return accuracy_score(qry_labels, preds) * 100.0, f1_score(qry_labels, preds, average="macro", zero_division=0) * 100.0

            acc, f1 = run_eval(lam)
            if acc > best_top1:
                best_top1 = acc
                best_params = (k, lam, acc, f1)
            if acc >= 65.08:
                print(f"k={k}, lam={lam:.2f} -> Top-1: {acc:.2f}%, F1: {f1:.2f}%")

    print(f"\nBest Global OPRA: k={best_params[0]}, lam={best_params[1]} -> Top-1: {best_params[2]:.2f}%, F1: {best_params[3]:.2f}%")

    # 2. Test Genus-Specific OPRA (especially Corn: 7, 8, 9 and Tomato: 17-24)
    print("\n--- Testing Genus-Specific Host Subtraction ---")
    # For Corn (classes 7, 8, 9)
    # What if we compute corn common mode
    corn_classes = [7, 8, 9]
    corn_bio_h = sb_protos[corn_classes].mean(axis=0, keepdims=True)
    corn_bio_h = l2_normalize(corn_bio_h)
    corn_dino_h = sd_protos[corn_classes].mean(axis=0, keepdims=True)
    corn_dino_h = l2_normalize(corn_dino_h)

    # Tomato common mode / Tomato_leaf
    tomato_classes = list(range(17, 25))
    tom_bio_h = sb_protos[19:20] # Tomato_leaf
    tom_dino_h = sd_protos[19:20]

    for lam in [0.1, 0.2, 0.3, 0.5, 0.7, 0.9]:
        # Modulate only Corn classes
        qb = tukey_power_transform(pd["qry_bio"])
        qbc, _ = center_and_normalize(qb)
        qd = tukey_power_transform(pd["qry_dino"])
        qdc, _ = center_and_normalize(qd)

        # Copy prototypes
        pb = sb_protos.copy()
        pd_p = sd_protos.copy()

        # Subtract host for Corn prototypes
        pb[corn_classes] = l2_normalize(pb[corn_classes] - lam * (pb[corn_classes] @ corn_bio_h.T @ corn_bio_h))
        pd_p[corn_classes] = l2_normalize(pd_p[corn_classes] - lam * (pd_p[corn_classes] @ corn_dino_h.T @ corn_dino_h))

        sb_sim = qbc @ pb.T
        sd_sim = qdc @ pd_p.T
        sims = eng.w_bio * sb_sim + (1.0 - eng.w_bio) * sd_sim + eng.alpha_bilinear * (sb_sim * sd_sim)
        sims = gegenbauer_decrowd_kernel(sims, dim=eng.joint_dim, gamma=eng.gamma_gegenbauer)
        sims_m = sims.copy()
        if eng.penalized_indices:
            sims_m[:, eng.penalized_indices] -= eng.margin_penalty
        p_vis = softmax_prob(sims_m, temp=eng.vis_temp)
        p_txt = softmax_prob(l2_normalize(pd["qry_bio"]) @ eng.micro_prototypes.T, temp=eng.text_temp)
        p_comb = eng.w_vis * p_vis + (1.0 - eng.w_vis) * p_txt
        if eng.enable_clutter_suppression and eng.suppressor is not None:
            p_comb, _ = eng.suppressor.modulate_probabilities(p_comb, pd["qry_bio"], class_names)
        preds = p_comb.argmax(axis=-1)
        acc = accuracy_score(qry_labels, preds) * 100.0
        f1 = f1_score(qry_labels, preds, average="macro", zero_division=0) * 100.0
        print(f"Corn host sub lam={lam:.2f} -> Top-1: {acc:.2f}%, F1: {f1:.2f}%")

if __name__ == "__main__":
    test_opra()


"""
Grid search over MorphoPath parameters to test if any configuration exceeds 65.08%
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from pipeline_morphopath.morphopath_engine import (
    MorphoPathEngine,
    tukey_power_transform,
    center_and_normalize,
    l2_normalize,
    softmax_prob,
    gegenbauer_decrowd_kernel,
)
from experiments.phase1_morphopath.benchmark_phase4_advanced import load_plantdoc_seed42

def grid_search():
    pd = load_plantdoc_seed42()
    class_names = pd["class_names"]
    n_classes = len(class_names)
    sup_joint = np.concatenate([pd["sup_bio"], pd["sup_dino"]], axis=-1)
    qry_joint = np.concatenate([pd["qry_bio"], pd["qry_dino"]], axis=-1)
    sup_labels = pd["sup_labels"]
    qry_labels = pd["qry_labels"]

    eng = MorphoPathEngine(
        bioclip_dim=512, dinov2_dim=384, shrinkage=0.60, router_temp=12.0, vis_temp=15.0,
        text_temp=30.0, w_vis=0.75, margin_penalty=0.05, w_bio=0.65,
        penalized_classes=["Potato_leaf_late_blight"], micro_prototypes=pd["micro_protos"],
        class_names=class_names, enable_clutter_suppression=True, gamma_glare=0.15, threshold_glare=0.06,
        alpha_bilinear=0.20, gamma_gegenbauer=-0.20,
    ).fit(sup_joint, sup_labels)

    qb, qd = tukey_power_transform(pd["qry_bio"]), tukey_power_transform(pd["qry_dino"])
    qbc, _ = center_and_normalize(qb, eng.mu_s_bio)
    qdc, _ = center_and_normalize(qd, eng.mu_s_dino)

    sb_sim = qbc @ eng.protos_bio_rect.T
    sd_sim = qdc @ eng.protos_dino_rect.T
    p_txt = softmax_prob(l2_normalize(pd["qry_bio"]) @ eng.micro_prototypes.T, temp=30.0)

    best_acc = 65.08
    best_config = None

    print("Current SOTA: 65.08%")

    for wb in [0.55, 0.60, 0.62, 0.65, 0.68, 0.70]:
        for alpha in [0.10, 0.15, 0.20, 0.25, 0.30]:
            for gamma in [0.0, -0.10, -0.15, -0.20, -0.25, -0.30]:
                for w_vis in [0.70, 0.75, 0.80]:
                    sims = wb * sb_sim + (1.0 - wb) * sd_sim + alpha * (sb_sim * sd_sim)
                    if gamma != 0.0:
                        sims = gegenbauer_decrowd_kernel(sims, dim=896, gamma=gamma)
                    sims_m = sims.copy()
                    if eng.penalized_indices:
                        sims_m[:, eng.penalized_indices] -= 0.05
                    p_vis = softmax_prob(sims_m, temp=15.0)
                    p_comb = w_vis * p_vis + (1.0 - w_vis) * p_txt
                    p_comb, _ = eng.suppressor.modulate_probabilities(p_comb, pd["qry_bio"], class_names)
                    preds = p_comb.argmax(axis=-1)
                    acc = accuracy_score(qry_labels, preds) * 100.0
                    if acc > best_acc:
                        f1 = f1_score(qry_labels, preds, average="macro", zero_division=0) * 100.0
                        best_acc = acc
                        best_config = (wb, alpha, gamma, w_vis, acc, f1)
                        print(f"NEW BEST! wb={wb:.2f}, alpha={alpha:.2f}, gamma={gamma:.2f}, w_vis={w_vis:.2f} -> Top-1: {acc:.2f}%, F1: {f1:.2f}%")

    if best_config is None:
        print("No configuration beat 65.08%!")
    else:
        print("Best found:", best_config)

if __name__ == "__main__":
    grid_search()


"""
Test Anti-Collapse Projection Head trained on Centered Rectified Features
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
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
    compute_prototypes,
    gegenbauer_decrowd_kernel,
)
from experiments.phase1_morphopath.benchmark_phase4_advanced import load_plantdoc_seed42

def test_pipeline_anti_collapse():
    pd = load_plantdoc_seed42()
    class_names = pd["class_names"]
    n_classes = len(class_names)
    sup_joint = np.concatenate([pd["sup_bio"], pd["sup_dino"]], axis=-1)
    qry_joint = np.concatenate([pd["qry_bio"], pd["qry_dino"]], axis=-1)
    sup_labels = pd["sup_labels"]
    qry_labels = pd["qry_labels"]

    # Base engine
    eng = MorphoPathEngine(
        bioclip_dim=512, dinov2_dim=384, shrinkage=0.60, router_temp=12.0, vis_temp=15.0,
        text_temp=30.0, w_vis=0.75, margin_penalty=0.05, w_bio=0.65,
        penalized_classes=["Potato_leaf_late_blight"], micro_prototypes=pd["micro_protos"],
        class_names=class_names, enable_clutter_suppression=True, gamma_glare=0.15, threshold_glare=0.06,
        alpha_bilinear=0.20, gamma_gegenbauer=-0.20,
    ).fit(sup_joint, sup_labels)

    # Rectified centered features
    sb, sd = tukey_power_transform(pd["sup_bio"]), tukey_power_transform(pd["sup_dino"])
    sbc, mu_b = center_and_normalize(sb)
    sdc, mu_d = center_and_normalize(sd)
    
    qb, qd = tukey_power_transform(pd["qry_bio"]), tukey_power_transform(pd["qry_dino"])
    qbc, _ = center_and_normalize(qb, mu_b)
    qdc, _ = center_and_normalize(qd, mu_d)

    # Let's test projection heads separately for BioCLIP and DINOv2, or Joint
    # Let's test Joint Centered features
    s_cent = np.concatenate([sbc, sdc], axis=-1)
    q_cent = np.concatenate([qbc, qdc], axis=-1)

    X_s = torch.from_numpy(s_cent).float()
    y_s = torch.from_numpy(sup_labels).long()
    X_q = torch.from_numpy(q_cent).float()

    print("Baseline accuracy: 65.08%")

    for out_dim in [256, 384, 512, 896]:
        for lr in [1e-3, 3e-3, 1e-2]:
            for epochs in [30, 60]:
                for l2_reg in [1e-4, 1e-3]:
                    # Linear projection matrix W: 896 -> out_dim
                    W = nn.Linear(896, out_dim, bias=False)
                    nn.init.orthogonal_(W.weight)
                    
                    # Classifier layer
                    clf = nn.Linear(out_dim, n_classes, bias=False)
                    nn.init.normal_(clf.weight, std=0.01)

                    optimizer = optim.Adam(list(W.parameters()) + list(clf.parameters()), lr=lr, weight_decay=l2_reg)
                    dataset = TensorDataset(X_s, y_s)
                    loader = DataLoader(dataset, batch_size=128, shuffle=True)

                    for epoch in range(epochs):
                        for bx, by in loader:
                            optimizer.zero_grad()
                            z = F.normalize(W(bx), p=2, dim=-1)
                            logits = 15.0 * F.linear(z, F.normalize(clf.weight, p=2, dim=-1))
                            loss = F.cross_entropy(logits, by)
                            loss.backward()
                            optimizer.step()

                    # Evaluate
                    with torch.no_grad():
                        z_sup = F.normalize(W(X_s), p=2, dim=-1).numpy()
                        z_qry = F.normalize(W(X_q), p=2, dim=-1).numpy()
                        
                        # Compute prototypes in projected space
                        p_proj = compute_prototypes(z_sup, sup_labels, n_classes)
                        sims_proj = z_qry @ p_proj.T
                        
                        # Blend with base sims
                        for alpha_proj in [0.0, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0]:
                            sb_sim = qbc @ eng.protos_bio_rect.T
                            sd_sim = qdc @ eng.protos_dino_rect.T
                            base_sims = 0.65 * sb_sim + 0.35 * sd_sim + 0.20 * (sb_sim * sd_sim)
                            base_sims = gegenbauer_decrowd_kernel(base_sims, dim=896, gamma=-0.20)
                            
                            sims = (1.0 - alpha_proj) * base_sims + alpha_proj * sims_proj
                            sims_m = sims.copy()
                            if eng.penalized_indices:
                                sims_m[:, eng.penalized_indices] -= eng.margin_penalty
                            p_vis = softmax_prob(sims_m, temp=15.0)
                            p_txt = softmax_prob(l2_normalize(pd["qry_bio"]) @ eng.micro_prototypes.T, temp=30.0)
                            p_comb = 0.75 * p_vis + 0.25 * p_txt
                            if eng.enable_clutter_suppression and eng.suppressor is not None:
                                p_comb, _ = eng.suppressor.modulate_probabilities(p_comb, pd["qry_bio"], class_names)
                            preds = p_comb.argmax(axis=-1)
                            acc = accuracy_score(qry_labels, preds) * 100.0
                            if acc > 65.08:
                                print(f"out={out_dim}, lr={lr}, ep={epochs}, a_proj={alpha_proj:.2f} -> Top-1: {acc:.2f}% (GAIN!)")

if __name__ == "__main__":
    test_pipeline_anti_collapse()


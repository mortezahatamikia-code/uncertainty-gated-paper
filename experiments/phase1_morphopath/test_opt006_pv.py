"""
Test IDEA-012 on PlantVillage
"""
from __future__ import annotations
import sys
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
from experiments.phase1_morphopath.benchmark_phase4_advanced import load_plantvillage_pool
from pipeline.morphopath_engine import (
    tukey_power_transform,
    center_and_normalize,
    l2_normalize,
    softmax_prob,
    compute_prototypes,
    is_healthy_leaf_name,
)
from experiments.phase1_morphopath.test_opt006 import soft_nearest_neighbor_scores

pv_data = load_plantvillage_pool()
n_classes = len(pv_data["class_names"])
class_to_indices = {c: np.where(pv_data["labels"] == c)[0] for c in range(n_classes)}
rng = np.random.RandomState(42)
sup_idx, qry_idx = [], []
for c in range(n_classes):
    c_idx = class_to_indices[c].copy()
    rng.shuffle(c_idx)
    sup_idx.extend(c_idx[:5])
    qry_idx.extend(c_idx[5:35])

bio_feats, dino_feats, labels = pv_data["bio_feats"], pv_data["dino_feats"], pv_data["labels"]
sup_bio, sup_dino, sup_labels = bio_feats[sup_idx], dino_feats[sup_idx], labels[sup_idx]
qry_bio, qry_dino, qry_labels = bio_feats[qry_idx], dino_feats[qry_idx], labels[qry_idx]

sb, sd = tukey_power_transform(sup_bio), tukey_power_transform(sup_dino)
sbc, mu_b = center_and_normalize(sb)
sdc, mu_d = center_and_normalize(sd)

qb, qd = tukey_power_transform(qry_bio), tukey_power_transform(qry_dino)
qbc, _ = center_and_normalize(qb)
qdc, _ = center_and_normalize(qd)

pb = compute_prototypes(sbc, sup_labels, n_classes)
pd = compute_prototypes(sdc, sup_labels, n_classes)
sims_base = 0.65 * (qbc @ pb.T) + 0.35 * (qdc @ pd.T)

def eval_pv(sims):
    p_vis = softmax_prob(sims, temp=15.0)
    p_txt = softmax_prob(l2_normalize(qry_bio) @ l2_normalize(pv_data["text_prototypes"]).T, temp=30.0)
    p_comb = 0.75 * p_vis + 0.25 * p_txt
    preds = p_comb.argmax(axis=-1)
    return accuracy_score(qry_labels, preds) * 100.0

print(f"PlantVillage Baseline (Mean Proto): {eval_pv(sims_base):.2f}%")
for tau in [1.0, 5.0, 10.0, 20.0]:
    s_b = soft_nearest_neighbor_scores(qbc, sbc, sup_labels, n_classes, tau_ex=tau)
    s_d = soft_nearest_neighbor_scores(qdc, sdc, sup_labels, n_classes, tau_ex=tau)
    sims_soft = 0.65 * s_b + 0.35 * s_d
    print(f"PlantVillage tau={tau:4.1f}: {eval_pv(sims_soft):.2f}%")

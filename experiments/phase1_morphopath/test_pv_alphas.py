"""
Compare 30 episodes on PlantVillage for alpha_bilinear in [0.0, 0.10, 0.15, 0.20]
"""
from __future__ import annotations
import sys
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import numpy as np
import scipy.stats as stats
from sklearn.metrics import accuracy_score

from pipeline_morphopath.morphopath_engine import (
    MorphoPathEngine,
    l2_normalize,
    tukey_power_transform,
    center_and_normalize,
    softmax_prob,
)
from experiments.phase1_morphopath.benchmark_phase4_advanced import load_plantvillage_pool
from experiments.phase3_morphopath.benchmark_plantvillage import PLANTVILLAGE_ARCHETYPE_MAP


def run_pv_comparison(alphas=[0.0, 0.10, 0.15, 0.20], n_episodes=15):
    pv_data = load_plantvillage_pool()
    n_classes = len(pv_data["class_names"])
    class_to_indices = {c: np.where(pv_data["labels"] == c)[0] for c in range(n_classes)}
    joint_feats = np.concatenate([pv_data["bio_feats"], pv_data["dino_feats"]], axis=-1)
    
    results = {a: {"top1": [], "top2": []} for a in alphas}
    
    for ep in range(n_episodes):
        rng = np.random.RandomState(42 + ep * 37)
        sup_idx, qry_idx = [], []
        for c in range(n_classes):
            c_idx = class_to_indices[c].copy()
            rng.shuffle(c_idx)
            sup_idx.extend(c_idx[:5])
            qry_idx.extend(c_idx[5:35])
            
        sup_joint, sup_labels = joint_feats[sup_idx], pv_data["labels"][sup_idx]
        qry_joint, qry_labels = joint_feats[qry_idx], pv_data["labels"][qry_idx]
        qry_bio, qry_dino = pv_data["bio_feats"][qry_idx], pv_data["dino_feats"][qry_idx]
        
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
        
        p_arch = softmax_prob(l2_normalize(qry_dino) @ engine.arch_protos_dino.T, temp=engine.router_temp)
        p_txt = softmax_prob(l2_normalize(qry_bio) @ l2_normalize(pv_data["text_prototypes"]).T, temp=engine.text_temp)
        qry_cent = l2_normalize(qry_joint - qry_joint.mean(axis=0, keepdims=True))
        
        p_lda = np.zeros((len(qry_labels), n_classes), dtype=np.float32)
        for arch_id, (clf, cands) in engine.lda_clfs.items():
            p_lda[:, cands] = p_arch[:, arch_id : arch_id + 1] * clf.predict_proba(qry_cent)
            
        for a in alphas:
            sims = 0.65 * s_bio + 0.35 * s_dino + a * (s_bio * s_dino)
            sims_m = sims.copy()
            if engine.penalized_indices:
                sims_m[:, engine.penalized_indices] -= engine.margin_penalty
            p_vis = softmax_prob(sims_m, temp=engine.vis_temp)
            p_comb = 0.75 * p_vis + 0.25 * p_txt
            p_comb = p_comb * (p_arch[:, engine.class_to_arch] ** engine.beta_bayes)
            p_comb /= (p_comb.sum(axis=-1, keepdims=True) + 1e-12)
            p_comb = 0.70 * p_comb + 0.30 * p_lda
            
            top1_p = p_comb.argmax(axis=-1)
            top2_c = np.argsort(p_comb, axis=-1)[:, -2:]
            t1 = float(accuracy_score(qry_labels, top1_p) * 100.0)
            t2 = float(np.mean([qry_labels[i] in top2_c[i] for i in range(len(qry_labels))]) * 100.0)
            results[a]["top1"].append(t1)
            results[a]["top2"].append(t2)
            
    print(f"Results across {n_episodes} PlantVillage episodes:")
    for a in alphas:
        print(f"  alpha={a:4.2f} -> Top-1: {np.mean(results[a]['top1']):.2f}% ± {np.std(results[a]['top1']):.2f}% | Top-2: {np.mean(results[a]['top2']):.2f}%")


if __name__ == "__main__":
    run_pv_comparison(alphas=[0.0, 0.05, 0.10, 0.15, 0.20], n_episodes=15)


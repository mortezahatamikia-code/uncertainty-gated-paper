"""
Experiment script for TASK-OPT-008: Cardinality-Scaled Ledoit-Wolf Shrinkage (IDEA-014)
"""
from __future__ import annotations
import sys
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import numpy as np
import torch
from sklearn.metrics import accuracy_score, f1_score

from pipeline_morphopath.morphopath_engine import (
    MorphoPathEngine,
    fit_shrunk_lda,
    is_healthy_leaf_name,
)
from experiments.phase1_morphopath.benchmark_phase4_advanced import (
    load_plantdoc_seed42,
    load_plantvillage_pool,
)
from experiments.phase3_morphopath.benchmark_plantvillage import PLANTVILLAGE_ARCHETYPE_MAP


def run_benchmark_opt008_plantvillage():
    print("=" * 75)
    print("TASK-OPT-008: Cardinality-Scaled Shrinkage on PlantVillage (38 Classes)")
    print("=" * 75)
    pv_data = load_plantvillage_pool()
    n_classes = len(pv_data["class_names"])
    class_to_indices = {c: np.where(pv_data["labels"] == c)[0] for c in range(n_classes)}
    
    # Test on multiple episodes (e.g., 5 episodes to get stable statistics)
    n_episodes = 5
    kappa_values = [None, "auto", 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    
    for kappa in kappa_values:
        top1_list = []
        top2_list = []
        for ep in range(n_episodes):
            rng = np.random.RandomState(42 + ep * 37)
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
            
            # Setup engine
            engine = MorphoPathEngine(
                bioclip_dim=512, dinov2_dim=384, shrinkage=0.60, router_temp=12.0, vis_temp=15.0,
                text_temp=30.0, w_vis=0.75, margin_penalty=0.05, w_bio=0.65, beta_bayes=0.20, w_lda=0.30,
                penalized_classes=["Potato___Late_blight", "Tomato___Late_blight"],
                micro_prototypes=pv_data["text_prototypes"], class_names=pv_data["class_names"],
                archetype_map=PLANTVILLAGE_ARCHETYPE_MAP,
            )
            # Fit custom LDA if kappa is set
            engine.fit(sup_joint, sup_labels)
            
            if kappa is not None:
                # Custom refit of LDAs
                sup_arch = engine.class_to_arch[sup_labels]
                engine.lda_clfs = {}
                for a in range(4):
                    cands = np.where(engine.class_to_arch == a)[0]
                    mask_sup_a = (sup_arch == a)
                    if len(cands) <= 1 or not np.any(mask_sup_a):
                        continue
                    local_map = {c: i for i, c in enumerate(cands)}
                    y_loc = np.array([local_map[y] for y in sup_labels[mask_sup_a]])
                    if len(np.unique(y_loc)) >= 2:
                        N_a = int(np.sum(mask_sup_a))
                        if kappa == "auto":
                            shrink = "auto"
                        else:
                            shrink = float(np.clip(kappa / np.sqrt(N_a), 0.25, 0.85))
                        # Centered features
                        clf = fit_shrunk_lda(engine.protos_rect[y_loc] if False else sup_joint[mask_sup_a], y_loc, shrinkage=shrink)
                        engine.lda_clfs[a] = (clf, cands)
                        
            metrics = engine.evaluate(qry_joint, qry_labels)
            top1_list.append(metrics["accuracy_top1"])
            top2_list.append(metrics["accuracy_top2"])
            
        name = f"Fixed lambda=0.60 (Baseline)" if kappa is None else f"kappa={kappa}" if kappa != "auto" else "Ledoit-Wolf auto"
        print(f"  {name:30s}: Top-1: {np.mean(top1_list):.2f}% ± {np.std(top1_list):.2f}% | Top-2: {np.mean(top2_list):.2f}%")


def run_benchmark_opt008_plantdoc():
    print("\n" + "=" * 75)
    print("TASK-OPT-008: Cardinality-Scaled Shrinkage on PlantDoc (Seed 42)")
    print("=" * 75)
    pd_data = load_plantdoc_seed42()
    sup_joint = np.concatenate([pd_data["sup_bio"], pd_data["sup_dino"]], axis=-1)
    qry_joint = np.concatenate([pd_data["qry_bio"], pd_data["qry_dino"]], axis=-1)
    qry_labels = pd_data["qry_labels"]
    sup_labels = pd_data["sup_labels"]
    class_names = pd_data["class_names"]
    
    # In PlantDoc baseline, w_lda is currently 0.0. Let's test if w_lda > 0 with cardinality shrinkage helps!
    for w_lda in [0.0, 0.05, 0.10, 0.15, 0.20, 0.30]:
        for kappa in [None, 2.5, 3.5, 4.5]:
            engine = MorphoPathEngine(
                bioclip_dim=512, dinov2_dim=384, shrinkage=0.60, router_temp=12.0, vis_temp=15.0,
                text_temp=30.0, w_vis=0.75, margin_penalty=0.05, w_bio=0.65, w_lda=w_lda,
                penalized_classes=["Potato_leaf_late_blight"], micro_prototypes=pd_data["micro_protos"],
                class_names=class_names, enable_clutter_suppression=True, gamma_glare=0.15, threshold_glare=0.06,
            ).fit(sup_joint, sup_labels)
            
            if kappa is not None and w_lda > 0:
                sup_arch = engine.class_to_arch[sup_labels]
                engine.lda_clfs = {}
                for a in range(4):
                    cands = np.where(engine.class_to_arch == a)[0]
                    mask_sup_a = (sup_arch == a)
                    if len(cands) <= 1 or not np.any(mask_sup_a):
                        continue
                    local_map = {c: i for i, c in enumerate(cands)}
                    y_loc = np.array([local_map[y] for y in sup_labels[mask_sup_a]])
                    if len(np.unique(y_loc)) >= 2:
                        N_a = int(np.sum(mask_sup_a))
                        shrink = float(np.clip(kappa / np.sqrt(N_a), 0.25, 0.85))
                        sb_c = engine.protos_rect if False else sup_joint[mask_sup_a]
                        engine.lda_clfs[a] = (fit_shrunk_lda(sb_c, y_loc, shrinkage=shrink), cands)
                        
            metrics = engine.evaluate(qry_joint, qry_labels)
            if w_lda == 0.0:
                print(f"  w_lda=0.0 (PlantDoc Baseline): Top-1: {metrics['accuracy_top1']:.2f}%, Top-2: {metrics['accuracy_top2']:.2f}%")
                break
            else:
                k_str = "fixed 0.60" if kappa is None else f"kappa={kappa}"
                print(f"  w_lda={w_lda:.2f}, {k_str:10s}: Top-1: {metrics['accuracy_top1']:.2f}%, Top-2: {metrics['accuracy_top2']:.2f}%, F1: {metrics['macro_f1']:.2f}%")


if __name__ == "__main__":
    run_benchmark_opt008_plantvillage()
    run_benchmark_opt008_plantdoc()


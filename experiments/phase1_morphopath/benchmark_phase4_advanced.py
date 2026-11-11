"""
Phase 4.2 Advanced Zero-Parameter Optimizations Benchmark Runner.
Systematically evaluates IDEA-012, IDEA-013, IDEA-014, IDEA-015, IDEA-016
individually and in combination on PlantDoc Seed 42 and PlantVillage 38-class.
"""

from __future__ import annotations
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
from sklearn.metrics import accuracy_score, f1_score

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from pipeline.morphopath_engine import (
    MorphoPathEngine,
    ARCHETYPE_NAMES,
    DEFAULT_ARCHETYPE_MAP,
    is_healthy_leaf_name,
    l2_normalize,
    tukey_power_transform,
    center_and_normalize,
    softmax_prob,
    fit_shrunk_lda,
    compute_prototypes,
)
from pipeline.canopy_suppressor import CanopyClutterGlareSuppressor
from experiments.phase3_morphopath.benchmark_plantvillage import PLANTVILLAGE_ARCHETYPE_MAP


def load_plantdoc_seed42():
    cache_file = _PROJECT_ROOT / "experiments" / "phase1_morphopath" / "plantdoc_features_seed42.pt"
    micro_file = _PROJECT_ROOT / "experiments" / "phase1_morphopath" / "micro_symptom_prototypes.pt"
    data = torch.load(cache_file, map_location="cpu")
    micro_data = torch.load(micro_file, map_location="cpu")
    return {
        "sup_bio": data["support_bioclip"].float().numpy(),
        "sup_dino": data["support_dino"].float().numpy(),
        "sup_labels": data["support_labels"].numpy(),
        "qry_bio": data["query_bioclip"].float().numpy(),
        "qry_dino": data["query_dino"].float().numpy(),
        "qry_labels": data["query_labels"].numpy(),
        "class_names": data["class_names"],
        "micro_protos": micro_data["micro_prototypes"].float().numpy(),
    }


def load_plantvillage_pool():
    cache_file = _PROJECT_ROOT / "experiments" / "phase3_morphopath" / "plantvillage_features_pool.pt"
    pool = torch.load(cache_file, map_location="cpu")
    return {
        "bio_feats": pool["bio_feats"].numpy(),
        "dino_feats": pool["dino_feats"].numpy(),
        "labels": pool["labels"].numpy(),
        "class_names": pool["class_names"],
        "text_prototypes": pool["text_prototypes"].numpy(),
    }


def evaluate_baseline_plantdoc(pd_data):
    sup_joint = np.concatenate([pd_data["sup_bio"], pd_data["sup_dino"]], axis=-1)
    qry_joint = np.concatenate([pd_data["qry_bio"], pd_data["qry_dino"]], axis=-1)
    engine = MorphoPathEngine(
        bioclip_dim=512, dinov2_dim=384, shrinkage=0.60, router_temp=12.0, vis_temp=15.0,
        text_temp=30.0, w_vis=0.75, margin_penalty=0.05, w_bio=0.65,
        penalized_classes=["Potato_leaf_late_blight"], micro_prototypes=pd_data["micro_protos"],
        class_names=pd_data["class_names"], enable_clutter_suppression=True, gamma_glare=0.15, threshold_glare=0.06,
    ).fit(sup_joint, pd_data["sup_labels"])
    return engine.evaluate(qry_joint, pd_data["qry_labels"]), engine


def evaluate_baseline_plantvillage_ep0(pv_data, k_shot=5, n_queries=30, seed=42):
    n_classes = len(pv_data["class_names"])
    class_to_indices = {c: np.where(pv_data["labels"] == c)[0] for c in range(n_classes)}
    rng = np.random.RandomState(seed)
    sup_idx, qry_idx = [], []
    for c in range(n_classes):
        c_idx = class_to_indices[c].copy()
        rng.shuffle(c_idx)
        sup_idx.extend(c_idx[:k_shot])
        qry_idx.extend(c_idx[k_shot : k_shot + n_queries])

    joint_feats = np.concatenate([pv_data["bio_feats"], pv_data["dino_feats"]], axis=-1)
    sup_joint = joint_feats[sup_idx]
    sup_labels = pv_data["labels"][sup_idx]
    qry_joint = joint_feats[qry_idx]
    qry_labels = pv_data["labels"][qry_idx]

    engine = MorphoPathEngine(
        bioclip_dim=512, dinov2_dim=384, shrinkage=0.60, router_temp=12.0, vis_temp=15.0,
        text_temp=30.0, w_vis=0.75, margin_penalty=0.05, w_bio=0.65, beta_bayes=0.20, w_lda=0.30,
        penalized_classes=["Potato___Late_blight", "Tomato___Late_blight"],
        micro_prototypes=pv_data["text_prototypes"], class_names=pv_data["class_names"],
        archetype_map=PLANTVILLAGE_ARCHETYPE_MAP,
    ).fit(sup_joint, sup_labels)
    return engine.evaluate(qry_joint, qry_labels), engine


if __name__ == "__main__":
    print("Loading data...")
    pd_data = load_plantdoc_seed42()
    metrics_pd, _ = evaluate_baseline_plantdoc(pd_data)
    print("PlantDoc Baseline:")
    print(f"  Top-1: {metrics_pd['accuracy_top1']:.2f}%")
    print(f"  Top-2: {metrics_pd['accuracy_top2']:.2f}%")
    print(f"  F1:    {metrics_pd['macro_f1']:.2f}%")
    print(f"  FPR:   {metrics_pd['fpr']:.2f}%")

    pv_data = load_plantvillage_pool()
    metrics_pv, _ = evaluate_baseline_plantvillage_ep0(pv_data)
    print("PlantVillage Episode 0 Baseline:")
    print(f"  Top-1: {metrics_pv['accuracy_top1']:.2f}%")
    print(f"  Top-2: {metrics_pv['accuracy_top2']:.2f}%")
    print(f"  F1:    {metrics_pv['macro_f1']:.2f}%")
    print(f"  FPR:   {metrics_pv['fpr']:.2f}%")


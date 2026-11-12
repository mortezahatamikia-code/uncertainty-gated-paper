"""
Exploratory empirical evaluation of Phase 4.4 Breakthrough Ideas:
IDEA-021: OPRA
IDEA-022: CBM
IDEA-023: Loupe
IDEA-024: Anti-Collapse Projection Head
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
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
    compute_prototypes,
    build_morphopath_output,
)
from experiments.phase1_morphopath.benchmark_phase4_advanced import (
    load_plantdoc_seed42,
    load_plantvillage_pool,
)

def evaluate_predictions(preds, labels, class_names):
    top1 = accuracy_score(labels, preds) * 100.0
    macro_f1 = f1_score(labels, preds, average="macro", zero_division=0) * 100.0
    # Clinical metrics
    healthy_idx = [i for i, c in enumerate(class_names) if "leaf" in c.lower() and not any(k in c.lower() for k in ["spot", "blight", "scab", "rust", "rot", "mildew", "virus", "mold"])]
    diseased_idx = [i for i in range(len(class_names)) if i not in healthy_idx]
    
    # FPR: healthy predicted as diseased
    h_mask = np.isin(labels, healthy_idx)
    fpr = np.mean(np.isin(preds[h_mask], diseased_idx)) * 100.0 if np.any(h_mask) else 0.0
    # FNR: diseased predicted as healthy
    d_mask = np.isin(labels, diseased_idx)
    fnr = np.mean(np.isin(preds[d_mask], healthy_idx)) * 100.0 if np.any(d_mask) else 0.0
    return {"top1": top1, "macro_f1": macro_f1, "fpr": fpr, "fnr": fnr}

def main():
    pd = load_plantdoc_seed42()
    class_names = pd["class_names"]
    n_classes = len(class_names)
    sup_joint = np.concatenate([pd["sup_bio"], pd["sup_dino"]], axis=-1)
    qry_joint = np.concatenate([pd["qry_bio"], pd["qry_dino"]], axis=-1)
    sup_labels = pd["sup_labels"]
    qry_labels = pd["qry_labels"]

    # Current SOTA baseline
    eng_sota = MorphoPathEngine(
        bioclip_dim=512, dinov2_dim=384, shrinkage=0.60, router_temp=12.0, vis_temp=15.0,
        text_temp=30.0, w_vis=0.75, margin_penalty=0.05, w_bio=0.65,
        penalized_classes=["Potato_leaf_late_blight"], micro_prototypes=pd["micro_protos"],
        class_names=class_names, enable_clutter_suppression=True, gamma_glare=0.15, threshold_glare=0.06,
        alpha_bilinear=0.20, gamma_gegenbauer=-0.20,
    ).fit(sup_joint, sup_labels)
    m_sota = eng_sota.evaluate(qry_joint, qry_labels)
    print(f"Current SOTA: Top-1 = {m_sota['accuracy_top1']:.2f}%, Top-2 = {m_sota['accuracy_top2']:.2f}%, F1 = {m_sota['macro_f1']:.2f}%, FPR = {m_sota['fpr']:.2f}%, FNR = {m_sota['fnr']:.2f}%")

if __name__ == "__main__":
    main()


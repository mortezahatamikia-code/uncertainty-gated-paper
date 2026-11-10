"""
================================================================================
MorphoPath-Edge: Clinical Evaluation & Botanical Metrics (morphopath_eval.py)
================================================================================
Implements diagnostic and clinical evaluation routines for foliar pathology:
  - Top-1 and Top-2 differential diagnostic accuracy
  - Clinical False Negative Rate (FNR) and False Positive Rate (FPR)
  - Botanical foliar archetype routing accuracy and stratified per-archetype metrics
================================================================================
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from sklearn.metrics import accuracy_score, f1_score

from pipeline.morphopath_archetypes import ARCHETYPE_NAMES, is_healthy_leaf_name


def compute_clinical_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: List[str],
) -> Tuple[float, float]:
    """
    Computes clinical False Negative Rate (FNR) and False Positive Rate (FPR).

    FNR measures diseased leaves misdiagnosed as healthy (critical clinical miss).
    FPR measures healthy leaves misdiagnosed as diseased (unnecessary treatment).
    """
    healthy_indices = set(
        i for i, c in enumerate(class_names) if is_healthy_leaf_name(c)
    )
    diseased_mask = np.array([y not in healthy_indices for y in y_true])
    healthy_mask = np.array([y in healthy_indices for y in y_true])
    pred_healthy = np.array([y in healthy_indices for y in y_pred])

    fnr = float(np.sum(diseased_mask & pred_healthy) / max(1, np.sum(diseased_mask)) * 100.0)
    fpr = float(np.sum(healthy_mask & ~pred_healthy) / max(1, np.sum(healthy_mask)) * 100.0)
    return fnr, fpr


def compute_archetype_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_to_arch: np.ndarray,
    archetype_preds: np.ndarray,
) -> Tuple[float, Dict[str, Dict[str, Any]]]:
    """
    Computes macro-botanical router accuracy and per-archetype performance breakdowns.
    """
    qry_arch_true = class_to_arch[y_true]
    router_top1_acc = float(np.mean(archetype_preds == qry_arch_true) * 100.0)

    per_arch: Dict[str, Dict[str, Any]] = {}
    for a in range(4):
        mask_a = (qry_arch_true == a)
        n_a = int(np.sum(mask_a))
        if n_a > 0:
            acc_a = float(accuracy_score(y_true[mask_a], y_pred[mask_a]) * 100.0)
            f1_a = float(f1_score(y_true[mask_a], y_pred[mask_a], average="macro", zero_division=0) * 100.0)
        else:
            acc_a, f1_a = 0.0, 0.0
        per_arch[f"archetype_{a}"] = {
            "name": ARCHETYPE_NAMES[a],
            "n_queries": n_a,
            "accuracy": acc_a,
            "macro_f1": f1_a,
        }
    return router_top1_acc, per_arch


def evaluate_engine(
    engine: Any,
    query_features: np.ndarray,
    query_labels: np.ndarray,
    query_bioclip: Optional[np.ndarray] = None,
    query_dino: Optional[np.ndarray] = None,
) -> Dict[str, Union[float, Dict[str, Any]]]:
    """
    Evaluates MorphoPathEngine on query observations and returns comprehensive metrics.
    Computes Top-1, Top-2 differential accuracy, Macro F1, clinical FNR/FPR,
    and per-archetype performance breakdowns.
    """
    out = engine.forward(query_features, query_bioclip, query_dino)
    y_true = np.asarray(query_labels)
    y_pred = out.top1_preds

    top1_acc = float(accuracy_score(y_true, y_pred) * 100.0)
    top2_flags = (y_true == out.top2_preds[:, 0]) | (y_true == out.top2_preds[:, 1])
    top2_acc = float(np.mean(top2_flags) * 100.0)
    macro_f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0) * 100.0)

    fnr, fpr = compute_clinical_metrics(y_true, y_pred, engine.class_names)
    router_top1_acc, per_arch = compute_archetype_metrics(
        y_true, y_pred, engine.class_to_arch, out.archetype_preds
    )

    return {
        "accuracy_top1": top1_acc,
        "accuracy_top2": top2_acc,
        "macro_f1": macro_f1,
        "fnr": fnr,
        "fpr": fpr,
        "router_top1_accuracy": router_top1_acc,
        "mean_differential_confidence": float(np.mean(out.differential_confidence)),
        "per_archetype": per_arch,
    }


__all__ = [
    "compute_clinical_metrics",
    "compute_archetype_metrics",
    "evaluate_engine",
]

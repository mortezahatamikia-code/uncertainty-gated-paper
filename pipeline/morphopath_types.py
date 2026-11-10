"""
================================================================================
MorphoPath-Edge: Structured Types and Output Definitions (morphopath_types.py)
================================================================================
Defines output container dataclasses and typing contracts for the MorphoPath-Edge
inference pipeline and botanical diagnostic triage system.
================================================================================
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple
import numpy as np


@dataclass
class MorphoPathOutput:
    """Structured container for complete MorphoPath-Edge diagnostic inference results."""
    top1_preds: np.ndarray
    top2_preds: np.ndarray
    top1_names: List[str]
    top2_names: List[Tuple[str, str]]
    top2_probs: np.ndarray
    differential_confidence: np.ndarray
    probabilities: np.ndarray
    archetype_preds: np.ndarray
    archetype_probs: np.ndarray
    clutter_diagnostics: Optional[Any] = None
    glare_score: Optional[np.ndarray] = None


def build_morphopath_output(
    sims_rect: np.ndarray,
    p_comb: np.ndarray,
    pred_arch: np.ndarray,
    p_arch: np.ndarray,
    class_names: List[str],
    n_classes: int,
    clutter_diag: Optional[Any] = None,
    glare_scores: Optional[np.ndarray] = None,
) -> MorphoPathOutput:
    """Vectorized assembly of Top-1/Top-2 triage hypotheses and confidence metrics."""
    from pipeline.morphopath_math import calculate_differential_confidence

    n_queries = len(p_comb)
    top1_preds = p_comb.argmax(axis=-1)
    top2_ranked = np.argsort(-sims_rect, axis=-1)[:, :2]
    p2 = np.where(top2_ranked[:, 0] == top1_preds, top2_ranked[:, 1], top2_ranked[:, 0])
    top2_preds_arr = np.column_stack([top1_preds, p2])

    row_idx = np.arange(n_queries)
    prob_p1, prob_p2 = p_comb[row_idx, top1_preds], p_comb[row_idx, p2]
    sum_prob = prob_p1 + prob_p2 + 1e-12
    top2_probs_arr = np.column_stack([prob_p1 / sum_prob, prob_p2 / sum_prob])

    diff_conf_arr = calculate_differential_confidence(
        probabilities=p_comb, top1_idx=top1_preds, top2_idx=p2, n_classes=n_classes
    )
    return MorphoPathOutput(
        top1_preds=top1_preds,
        top2_preds=top2_preds_arr,
        top1_names=[class_names[p] for p in top1_preds],
        top2_names=[(class_names[p[0]], class_names[p[1]]) for p in top2_preds_arr],
        top2_probs=top2_probs_arr,
        differential_confidence=diff_conf_arr,
        probabilities=p_comb,
        archetype_preds=pred_arch,
        archetype_probs=p_arch,
        clutter_diagnostics=clutter_diag,
        glare_score=glare_scores,
    )


__all__ = ["MorphoPathOutput", "build_morphopath_output"]

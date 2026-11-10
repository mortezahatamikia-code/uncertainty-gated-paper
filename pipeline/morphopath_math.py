"""
================================================================================
MorphoPath-Edge: Manifold & Vectorized Mathematics (morphopath_math.py)
================================================================================
Centralizes core algebraic transforms, hypersphere projections, and statistical
discriminant estimation routines for edge few-shot foliar pathology inference:
  1. Unit L2 Hypersphere Normalization (with zero-copy buffer support).
  2. Tukey Signed Power Transform (z = sign(x) * |x|^0.5).
  3. Zero-Parameter Manifold Centering and Spherical Rectification (ADR-005).
  4. Numerically Stable Zero-Copy NumPy Softmax.
  5. Shannon Margin-Entropy Differential Confidence Estimation (ADR-003).
  6. Closed-Form Ledoit-Wolf Shrunk Fisher LDA (ADR-002).
  7. L2-Normalized Prototype Synthesis via Support Embedding Pooling.
================================================================================
"""

from __future__ import annotations
import math
from typing import Optional, Tuple, Union

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def l2_normalize(x: np.ndarray, eps: float = 1e-12, out: Optional[np.ndarray] = None) -> np.ndarray:
    """
    Projects vectors to the unit hypersphere via L2 normalization.

    Parameters
    ----------
    x : np.ndarray
        Array of shape (..., D).
    eps : float, default=1e-12
        Small epsilon preventing zero division.
    out : Optional[np.ndarray], default=None
        Pre-allocated output buffer for zero-copy in-place operations.

    Returns
    -------
    np.ndarray
        Unit-normalized array of shape (..., D).
    """
    norm = np.linalg.norm(x, axis=-1, keepdims=True)
    norm = np.maximum(norm, eps)
    if out is not None:
        np.divide(x, norm, out=out)
        return out
    return x / norm


def tukey_power_transform(x: np.ndarray, power: float = 0.5, eps: float = 1e-12) -> np.ndarray:
    """
    Applies the Tukey signed power transform followed by L2 normalization.

    Reduces feature kurtosis and aligns sub-Gaussian empirical tail distributions:
        z = sign(x) * |x|^power, normalized to ||z||_2 = 1.

    Parameters
    ----------
    x : np.ndarray
        Feature array of shape (..., D).
    power : float, default=0.5
        Power coefficient (0.5 represents signed square-root).
    eps : float, default=1e-12
        Epsilon constant for numerical stability.

    Returns
    -------
    np.ndarray
        Transformed and L2-normalized feature representation.
    """
    z = np.sign(x) * (np.abs(x) ** power)
    return l2_normalize(z, eps=eps)


def center_and_normalize(
    x: np.ndarray,
    center: Optional[np.ndarray] = None,
    eps: float = 1e-12,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Performs zero-parameter manifold centering and L2 spherical projection (ADR-005).

    Parameters
    ----------
    x : np.ndarray
        Input embeddings of shape (N, D).
    center : Optional[np.ndarray], default=None
        Pre-computed manifold centroid (1, D). If None, estimated as mean(x).
    eps : float, default=1e-12
        Epsilon constant for numerical stability.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        (normalized_centered_features, estimated_centroid).
    """
    mu = x.mean(axis=0, keepdims=True) if center is None else center
    centered = x - mu
    return l2_normalize(centered, eps=eps), mu


def softmax_prob(logits: np.ndarray, temp: float = 1.0, axis: int = -1) -> np.ndarray:
    """
    Computes numerically stable, zero-copy vectorized Softmax probabilities.

    Parameters
    ----------
    logits : np.ndarray
        Raw similarity or unnormalized logit array.
    temp : float, default=1.0
        Inverse temperature scaling multiplier.
    axis : int, default=-1
        Dimension along which softmax is calculated.

    Returns
    -------
    np.ndarray
        Probability simplex distribution summing to 1 along `axis`.
    """
    scaled = logits * temp
    max_val = np.max(scaled, axis=axis, keepdims=True)
    exp_s = np.exp(scaled - max_val)
    return exp_s / np.sum(exp_s, axis=axis, keepdims=True)


def calculate_differential_confidence(
    probabilities: np.ndarray,
    top1_idx: np.ndarray,
    top2_idx: np.ndarray,
    n_classes: int,
) -> np.ndarray:
    """
    Computes Shannon margin-entropy differential triage confidence (ADR-003).

    Formula:
        C(x) = (P(top1) - P(top2)) * (1 - H_norm(P))
        where H_norm(P) = -sum(P * ln(P)) / ln(K).

    Parameters
    ----------
    probabilities : np.ndarray
        Probability distributions array of shape (N, K).
    top1_idx : np.ndarray
        Top-1 predicted class index array of shape (N,).
    top2_idx : np.ndarray
        Top-2 alternative candidate index array of shape (N,).
    n_classes : int
        Total number of classes K.

    Returns
    -------
    np.ndarray
        Confidence scores in range [0, 1] of shape (N,).
    """
    n_queries = len(probabilities)
    row_idx = np.arange(n_queries)
    prob_p1 = probabilities[row_idx, top1_idx]
    prob_p2 = probabilities[row_idx, top2_idx]

    margin = np.maximum(0.0, prob_p1 - prob_p2)
    norm_factor = max(float(math.log(n_classes)), 1e-6)
    entropy = -np.sum(probabilities * np.log(probabilities + 1e-12), axis=-1) / norm_factor
    return np.clip(margin * (1.0 - entropy), 0.0, 1.0).astype(np.float32)


def fit_shrunk_lda(
    features: np.ndarray,
    labels: np.ndarray,
    shrinkage: Union[float, str] = 0.60,
) -> LinearDiscriminantAnalysis:
    """
    Fits regularized Fisher Linear Discriminant Analysis with Ledoit-Wolf shrinkage.

    Parameters
    ----------
    features : np.ndarray
        Centered support features of shape (N, D).
    labels : np.ndarray
        Integer target class labels of shape (N,).
    shrinkage : Union[float, str], default=0.60
        Covariance shrinkage coefficient lambda in [0, 1] or 'auto'.

    Returns
    -------
    LinearDiscriminantAnalysis
        Fitted Scikit-Learn LDA classifier instance.
    """
    clf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=shrinkage)
    clf.fit(features, labels)
    return clf


def compute_prototypes(
    features: np.ndarray,
    labels: np.ndarray,
    n_classes: int,
    eps: float = 1e-12,
) -> np.ndarray:
    """
    Computes L2-normalized mean class prototypes across support observations.

    Parameters
    ----------
    features : np.ndarray
        Support embeddings of shape (N, D).
    labels : np.ndarray
        Class labels array of shape (N,).
    n_classes : int
        Number of classes K.
    eps : float, default=1e-12
        Epsilon for numerical stability during normalization.

    Returns
    -------
    np.ndarray
        Prototype matrix of shape (K, D).
    """
    dim = features.shape[-1]
    protos = np.zeros((n_classes, dim), dtype=np.float32)
    for c in range(n_classes):
        mask = (labels == c)
        if np.any(mask):
            protos[c] = features[mask].mean(axis=0)
    return l2_normalize(protos, eps=eps)


__all__ = [
    "l2_normalize",
    "tukey_power_transform",
    "center_and_normalize",
    "softmax_prob",
    "calculate_differential_confidence",
    "fit_shrunk_lda",
    "compute_prototypes",
]


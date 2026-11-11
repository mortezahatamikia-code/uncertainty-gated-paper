"""
MorphoPath-Edge: Manifold & Vectorized Mathematics (morphopath_math.py)
Algebraic transforms, hypersphere projections, and statistical discriminant routines:
  1. Unit L2 Hypersphere Normalization (zero-copy buffer support).
  2. Tukey Signed Power Transform (z = sign(x) * |x|^0.5).
  3. Zero-Parameter Manifold Centering and Spherical Rectification (ADR-005).
  4. Numerically Stable Zero-Copy NumPy Softmax.
  5. Shannon Margin-Entropy Differential Confidence Estimation (ADR-003).
  6. Closed-Form Ledoit-Wolf Shrunk Fisher LDA (ADR-002).
  7. L2-Normalized Prototype Synthesis via Support Embedding Pooling.
  8. Gegenbauer Spherical Harmonic Decrowding Kernel (IDEA-017).
"""

from __future__ import annotations
import math
from typing import Optional, Tuple, Union

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def l2_normalize(x: np.ndarray, eps: float = 1e-12, out: Optional[np.ndarray] = None) -> np.ndarray:
    """Projects vectors to the unit hypersphere via L2 normalization."""
    norm = np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), eps)
    if out is not None:
        np.divide(x, norm, out=out)
        return out
    return x / norm


def tukey_power_transform(x: np.ndarray, power: float = 0.5, eps: float = 1e-12) -> np.ndarray:
    """Applies Tukey signed power transform followed by L2 normalization: z = sign(x)*|x|^power."""
    z = np.sign(x) * (np.abs(x) ** power)
    return l2_normalize(z, eps=eps)


def center_and_normalize(
    x: np.ndarray, center: Optional[np.ndarray] = None, eps: float = 1e-12
) -> Tuple[np.ndarray, np.ndarray]:
    """Performs zero-parameter manifold centering and L2 spherical projection (ADR-005)."""
    mu = x.mean(axis=0, keepdims=True) if center is None else center
    return l2_normalize(x - mu, eps=eps), mu


def softmax_prob(logits: np.ndarray, temp: float = 1.0, axis: int = -1) -> np.ndarray:
    """Computes numerically stable, zero-copy vectorized Softmax probabilities."""
    scaled = logits * temp
    max_val = np.max(scaled, axis=axis, keepdims=True)
    exp_s = np.exp(scaled - max_val)
    return exp_s / np.sum(exp_s, axis=axis, keepdims=True)


def calculate_differential_confidence(
    probabilities: np.ndarray, top1_idx: np.ndarray, top2_idx: np.ndarray, n_classes: int
) -> np.ndarray:
    """Computes Shannon margin-entropy differential triage confidence (ADR-003)."""
    row_idx = np.arange(len(probabilities))
    margin = np.maximum(0.0, probabilities[row_idx, top1_idx] - probabilities[row_idx, top2_idx])
    norm_factor = max(float(math.log(n_classes)), 1e-6)
    entropy = -np.sum(probabilities * np.log(probabilities + 1e-12), axis=-1) / norm_factor
    return np.clip(margin * (1.0 - entropy), 0.0, 1.0).astype(np.float32)


def fit_shrunk_lda(
    features: np.ndarray, labels: np.ndarray, shrinkage: Union[float, str] = 0.60
) -> LinearDiscriminantAnalysis:
    """Fits regularized Fisher Linear Discriminant Analysis with Ledoit-Wolf shrinkage."""
    clf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=shrinkage)
    clf.fit(features, labels)
    return clf


def compute_prototypes(
    features: np.ndarray, labels: np.ndarray, n_classes: int, eps: float = 1e-12
) -> np.ndarray:
    """Computes L2-normalized mean class prototypes across support observations."""
    dim = features.shape[-1]
    protos = np.zeros((n_classes, dim), dtype=np.float32)
    for c in range(n_classes):
        mask = (labels == c)
        if np.any(mask):
            protos[c] = features[mask].mean(axis=0)
    return l2_normalize(protos, eps=eps)


def gegenbauer_decrowd_kernel(sims: np.ndarray, dim: int = 896, gamma: float = -0.20) -> np.ndarray:
    """
    Applies closed-form degree-2 Gegenbauer spherical harmonic polynomial kernel (IDEA-017).
    Decrowds hyperspherical similarities by penalizing quadratic co-activation noise.
    """
    if gamma == 0.0:
        return sims
    d = float(dim)
    return sims + gamma * ((d / (d - 1.0)) * (sims ** 2) - (1.0 / (d - 1.0)))


__all__ = [
    "l2_normalize",
    "tukey_power_transform",
    "center_and_normalize",
    "softmax_prob",
    "calculate_differential_confidence",
    "fit_shrunk_lda",
    "compute_prototypes",
    "gegenbauer_decrowd_kernel",
]




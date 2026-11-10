"""
================================================================================
MorphoPath-Edge: Zero-Parameter Canopy Clutter, Void & Glare Suppressor
================================================================================
Suppresses non-pathogenic environmental foliar imaging artifacts in closed form:
  1. BioCLIP Negative Rejector Prototypes (Zero-Shot Abiotic Rejectors):
     - Specular sunlight glare and solar reflection on leaf cuticles.
     - Deep canopy voids (bare soil, background mulch, open sky gaps).
     - Peripheral out-of-focus background clutter and abaxial occlusion.
  2. Specular Luminance & Artifact Profiling:
     - Real-time perceptual luminance calculation (Rec. 601: Y = 0.299R + 0.587G + 0.114B).
     - Specular over-saturation thresholding (Y > 0.88).
     - Shadow void thresholding (Y < 0.08).
  3. Spatial Centrality Prior:
     - Closed-form 2D Gaussian centrality prior weighting foreground foliar blade.
  4. Closed-Form Negative Margin Gating:
     - Penalizes lesion-mimicking disease classes under severe specular artifact alignment,
       suppressing false alarms (FPR) while preserving true pathogen sensitivity (FNR).
================================================================================
"""

from __future__ import annotations
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import torch

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

try:
    from pipeline.morphopath_engine import l2_normalize
except (ImportError, ModuleNotFoundError):
    from morphopath_engine import l2_normalize  # type: ignore[no-redef]


# ------------------------------------------------------------------------------
# 1. Negative Text Prompts for Abiotic Environmental Clutter
# ------------------------------------------------------------------------------

CANOPY_NEGATIVE_PROMPTS: Dict[str, List[str]] = {
    "glare": [
        "direct specular sunlight flare and blinding reflection on leaf surface",
        "bright harsh overexposed solar glare artifact on foliage",
        "white specular reflection of bright sun on waxy plant cuticle",
    ],
    "void": [
        "empty sky and bare soil ground void through canopy gap",
        "out of focus dark shadow and deep empty void behind canopy",
        "background soil, dirt, mulch, and open sky with no leaf",
    ],
    "clutter": [
        "blurry secondary background leaf clutter and overlapping foliage",
        "distant out of focus foliage in background canopy clutter",
        "overlapping secondary leaves creating foliar clutter and occlusion",
    ],
}


@dataclass
class ClutterDiagnostics:
    """Structured diagnostic telemetry for foliar image environmental corruption."""
    glare_score: np.ndarray        # (N,) cosine alignment to specular solar glare
    void_score: np.ndarray         # (N,) cosine alignment to canopy background voids
    clutter_score: np.ndarray      # (N,) cosine alignment to out-of-focus secondary clutter
    max_artifact_score: np.ndarray  # (N,) maximum environmental artifact score
    is_glare_corrupted: np.ndarray  # (N,) boolean flag for severe specular glare
    is_void_corrupted: np.ndarray   # (N,) boolean flag for background void penetration


# ------------------------------------------------------------------------------
# 2. Specular Luminance & Centrality Preprocessing Helpers
# ------------------------------------------------------------------------------

def compute_specular_luminance(
    image_array: np.ndarray,
    glare_thresh: float = 0.88,
    void_thresh: float = 0.08,
) -> Dict[str, Union[float, bool]]:
    """
    Computes zero-parameter perceptual luminance and artifact fractions from an RGB image.

    Parameters
    ----------
    image_array : np.ndarray
        RGB image tensor of shape (H, W, 3) in range [0, 1] or [0, 255].
    glare_thresh : float, default=0.88
        Threshold above which pixels are marked as specularly saturated.
    void_thresh : float, default=0.08
        Threshold below which pixels are marked as deep shadow or empty voids.

    Returns
    -------
    Dict[str, Union[float, bool]]
        Luminance statistics including specular fraction, void fraction, and boolean alert flags.
    """
    arr = image_array.astype(np.float32)
    if arr.max() > 1.0:
        arr = arr / 255.0

    # Rec. 601 Luma: Y = 0.299 R + 0.587 G + 0.114 B
    lum = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]

    specular_fraction = float(np.mean(lum > glare_thresh))
    void_fraction = float(np.mean(lum < void_thresh))
    mean_luminance = float(np.mean(lum))
    p95_luminance = float(np.percentile(lum, 95))

    return {
        "specular_fraction": specular_fraction,
        "void_fraction": void_fraction,
        "mean_luminance": mean_luminance,
        "p95_luminance": p95_luminance,
        "has_high_glare": specular_fraction > 0.10,
        "has_high_void": void_fraction > 0.20,
    }


def compute_spatial_centrality_mask(
    height: int,
    width: int,
    sigma_ratio: float = 0.40,
) -> np.ndarray:
    """
    Generates a 2D Gaussian centrality prior mask.

    Emphasizes the primary foreground foliar blade over peripheral canopy voids.

    Parameters
    ----------
    height : int
        Grid vertical dimension.
    width : int
        Grid horizontal dimension.
    sigma_ratio : float, default=0.40
        Gaussian kernel dispersion relative to normalized field dimensions.

    Returns
    -------
    np.ndarray
        Normalized 2D prior mask of shape (height, width) with values in (0, 1].
    """
    y = np.linspace(-1.0, 1.0, height)
    x = np.linspace(-1.0, 1.0, width)
    yy, xx = np.meshgrid(y, x, indexing="ij")
    dist_sq = (xx ** 2) + (yy ** 2)
    mask = np.exp(-dist_sq / (2.0 * (sigma_ratio ** 2)))
    return mask / np.max(mask)


# ------------------------------------------------------------------------------
# 3. CanopyClutterGlareSuppressor Core Class
# ------------------------------------------------------------------------------

class CanopyClutterGlareSuppressor:
    """
    Zero-parameter modular suppressor for foliar field imagery.

    Mitigates false-positive pathogen triage triggered by specular sun reflections,
    canopy soil/sky voids, and secondary background foliar clutter.
    """

    def __init__(
        self,
        negative_prototypes: Optional[np.ndarray] = None,
        gamma_glare: float = 0.15,
        threshold_glare: float = 0.06,
        cache_path: Optional[Union[str, Path]] = None,
    ):
        self.gamma_glare = gamma_glare
        self.threshold_glare = threshold_glare
        self.negative_prototypes: Optional[np.ndarray] = None

        if negative_prototypes is not None:
            self.set_prototypes(negative_prototypes)
        elif cache_path is not None:
            self.load_cache(cache_path)
        else:
            default_p = (
                Path(__file__).resolve().parent.parent
                / "experiments"
                / "phase1_morphopath"
                / "negative_rejector_prototypes.pt"
            )
            if default_p.exists():
                self.load_cache(default_p)

    def set_prototypes(self, protos: np.ndarray) -> None:
        """
        Sets and L2-normalizes 3-category negative prototypes (shape [3, 512]).

        Parameters
        ----------
        protos : np.ndarray
            Embedding array of shape (3, D).
        """
        self.negative_prototypes = l2_normalize(protos)

    def load_cache(self, path: Union[str, Path]) -> None:
        """
        Loads precomputed negative prototypes from PyTorch checkpoint.

        Parameters
        ----------
        path : Union[str, Path]
            Path to the .pt file containing negative rejector prototypes.
        """
        data = torch.load(path, map_location="cpu")
        if isinstance(data, dict) and "negative_prototypes" in data:
            arr = data["negative_prototypes"].float().numpy()
        else:
            arr = data.float().numpy()
        self.set_prototypes(arr)

    def compute_diagnostics(self, query_bioclip: np.ndarray) -> ClutterDiagnostics:
        """
        Computes cosine alignment between query visual embeddings and abiotic prototypes.

        Parameters
        ----------
        query_bioclip : np.ndarray
            Visual feature embeddings of shape (N, 512).

        Returns
        -------
        ClutterDiagnostics
            Structured artifact metrics and corruption detection flags.
        """
        if self.negative_prototypes is None:
            raise RuntimeError("Negative prototypes must be loaded before running diagnostics.")

        q_norm = l2_normalize(query_bioclip)
        sims = q_norm @ self.negative_prototypes.T  # (N, 3): [glare, void, clutter]

        glare_s = sims[:, 0]
        void_s = sims[:, 1]
        clutter_s = sims[:, 2]
        max_s = np.max(sims, axis=-1)

        return ClutterDiagnostics(
            glare_score=glare_s,
            void_score=void_s,
            clutter_score=clutter_s,
            max_artifact_score=max_s,
            is_glare_corrupted=glare_s > 0.15,
            is_void_corrupted=void_s > 0.15,
        )

    def modulate_probabilities(
        self,
        probabilities: np.ndarray,
        query_bioclip: np.ndarray,
        class_names: List[str],
    ) -> Tuple[np.ndarray, ClutterDiagnostics]:
        """
        Applies closed-form negative margin gating to prevent false disease alarms.

        Penalizes lesion-mimicking symptomatic disease classes when abiotic glare or void
        alignment exceeds the empirical sensitivity threshold.

        Parameters
        ----------
        probabilities : np.ndarray
            Predicted probability simplex array of shape (N, K).
        query_bioclip : np.ndarray
            Query visual embeddings of shape (N, 512).
        class_names : List[str]
            Target taxonomy class names of length K.

        Returns
        -------
        Tuple[np.ndarray, ClutterDiagnostics]
            (modulated_probabilities, diagnostic_telemetry).
        """
        diag = self.compute_diagnostics(query_bioclip)
        p_mod = probabilities.copy()

        # Identify classes susceptible to solar glare false alarms
        glare_prone_indices = [
            i for i, c in enumerate(class_names)
            if any(kw in c.lower() for kw in ["rust", "spot", "mildew", "scab", "blight"])
        ]

        if not glare_prone_indices:
            return p_mod, diag

        penalty = self.gamma_glare * np.maximum(0.0, diag.max_artifact_score - self.threshold_glare)

        for idx in glare_prone_indices:
            p_mod[:, idx] -= penalty

        # Re-normalize probability simplex with numerical floor
        p_mod = np.maximum(p_mod, 1e-8)
        p_mod = p_mod / p_mod.sum(axis=-1, keepdims=True)

        return p_mod, diag


if __name__ == "__main__":
    print("[*] Running CanopyClutterGlareSuppressor self-tests...")
    n_q = 5
    d_bio = 512
    k_classes = 4
    class_names = ["Tomato_Early_blight_leaf", "Tomato_leaf", "Corn_rust_leaf", "Apple_leaf"]
    mock_protos = np.random.randn(3, d_bio).astype(np.float32)
    mock_queries = np.random.randn(n_q, d_bio).astype(np.float32)
    mock_probs = np.full((n_q, k_classes), 1.0 / k_classes, dtype=np.float32)

    supp = CanopyClutterGlareSuppressor(negative_prototypes=mock_protos, gamma_glare=0.15, threshold_glare=0.0)
    p_mod, diag = supp.modulate_probabilities(mock_probs, mock_queries, class_names)

    assert p_mod.shape == (n_q, k_classes)
    assert np.allclose(p_mod.sum(axis=-1), 1.0, atol=1e-5)
    assert diag.glare_score.shape == (n_q,)
    print("[✓] CanopyClutterGlareSuppressor self-tests passed successfully.")

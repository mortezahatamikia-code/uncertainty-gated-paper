"""
MorphoPath-Edge: Zero-Parameter Canopy Clutter, Void & Glare Suppressor.
Suppresses non-pathogenic environmental foliar imaging artifacts in closed form:
  1. BioCLIP Negative Rejector Prototypes (glare, void, clutter)
  2. Specular Luminance & Artifact Profiling
  3. Closed-Form Negative Margin Gating
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
    from pipeline_morphopath.morphopath_engine import l2_normalize
except (ImportError, ModuleNotFoundError):
    from morphopath_engine import l2_normalize  # type: ignore[no-redef]


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
    glare_score: np.ndarray
    void_score: np.ndarray
    clutter_score: np.ndarray
    max_artifact_score: np.ndarray
    is_glare_corrupted: np.ndarray
    is_void_corrupted: np.ndarray


class CanopyClutterGlareSuppressor:
    """Zero-parameter foliage artifact suppressor via closed-form negative margin gating."""

    def __init__(
        self,
        negative_prototypes: Optional[np.ndarray] = None,
        gamma_glare: float = 0.15,
        threshold_glare: float = 0.06,
    ):
        self.gamma_glare = gamma_glare
        self.threshold_glare = threshold_glare
        if negative_prototypes is not None:
            self.negative_prototypes = l2_normalize(negative_prototypes)
        else:
            self.negative_prototypes = None
            default_p = _PROJECT_ROOT / "experiments" / "phase1_morphopath" / "negative_rejector_prototypes.pt"
            if default_p.exists():
                self.load_cache(default_p)

    def set_prototypes(self, protos: np.ndarray) -> None:
        self.negative_prototypes = l2_normalize(protos)

    def load_cache(self, path: Union[str, Path]) -> None:
        data = torch.load(path, map_location="cpu")
        arr = data["negative_prototypes"].float().numpy() if isinstance(data, dict) and "negative_prototypes" in data else data.float().numpy()
        self.set_prototypes(arr)

    def compute_diagnostics(self, query_bioclip: np.ndarray) -> ClutterDiagnostics:
        if self.negative_prototypes is None:
            raise RuntimeError("Negative prototypes must be loaded before running diagnostics.")
        sims = l2_normalize(query_bioclip) @ self.negative_prototypes.T
        glare_s, void_s, clutter_s = sims[:, 0], sims[:, 1], sims[:, 2]
        return ClutterDiagnostics(
            glare_score=glare_s, void_score=void_s, clutter_score=clutter_s,
            max_artifact_score=np.max(sims, axis=-1),
            is_glare_corrupted=glare_s > 0.15, is_void_corrupted=void_s > 0.15,
        )

    def modulate_probabilities(
        self, probabilities: np.ndarray, query_bioclip: np.ndarray, class_names: List[str]
    ) -> Tuple[np.ndarray, ClutterDiagnostics]:
        diag = self.compute_diagnostics(query_bioclip)
        p_mod = probabilities.copy()
        glare_prone = [i for i, c in enumerate(class_names) if any(kw in c.lower() for kw in ["rust", "spot", "mildew", "scab", "blight"])]
        if not glare_prone:
            return p_mod, diag

        penalty = self.gamma_glare * np.maximum(0.0, diag.max_artifact_score - self.threshold_glare)
        for idx in glare_prone:
            p_mod[:, idx] -= penalty

        p_mod = np.maximum(p_mod, 1e-8)
        p_mod = p_mod / p_mod.sum(axis=-1, keepdims=True)
        return p_mod, diag


if __name__ == "__main__":
    print("[*] Running CanopyClutterGlareSuppressor self-tests...")
    n_q, d_bio, k_classes = 5, 512, 4
    class_names = ["Tomato_Early_blight_leaf", "Tomato_leaf", "Corn_rust_leaf", "Apple_leaf"]
    mock_protos = np.random.randn(3, d_bio).astype(np.float32)
    mock_queries = np.random.randn(n_q, d_bio).astype(np.float32)
    mock_probs = np.full((n_q, k_classes), 1.0 / k_classes, dtype=np.float32)

    supp = CanopyClutterGlareSuppressor(negative_prototypes=mock_protos, gamma_glare=0.15, threshold_glare=0.0)
    p_mod, diag = supp.modulate_probabilities(mock_probs, mock_queries, class_names)
    assert p_mod.shape == (n_q, k_classes) and np.allclose(p_mod.sum(axis=-1), 1.0, atol=1e-5)
    print("[✓] CanopyClutterGlareSuppressor self-tests passed successfully.")

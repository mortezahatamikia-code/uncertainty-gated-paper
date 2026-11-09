"""
MorphoPath-Edge: Production-Grade Foliar-Pathology Dual Inference Engine.
Integrates foliar routing (ADR-001), Tukey rectification (ADR-005), regularized
LDA (ADR-002), micro-symptom ensemble (ADR-004), and Bayesian gating (ADR-003).
"""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from pipeline.morphopath_types import MorphoPathOutput, build_morphopath_output
from pipeline.morphopath_archetypes import ARCHETYPE_NAMES, DEFAULT_ARCHETYPE_MAP, infer_archetype_for_class, is_healthy_leaf_name
from pipeline.morphopath_math import (
    l2_normalize, tukey_power_transform, center_and_normalize, softmax_prob,
    calculate_differential_confidence, fit_shrunk_lda, compute_prototypes,
)
from pipeline.morphopath_eval import evaluate_engine, compute_clinical_metrics, compute_archetype_metrics


class MorphoPathEngine:
    """Production-grade MorphoPath-Edge dual inference engine."""

    def __init__(
        self, bioclip_dim: int = 512, dinov2_dim: int = 384, shrinkage: Union[float, str] = 0.60,
        router_temp: float = 12.0, vis_temp: float = 15.0, text_temp: float = 30.0, w_vis: float = 0.75,
        margin_penalty: float = 0.05, alpha_bayes: float = 1.0, w_bio: Optional[float] = 0.65,
        beta_bayes: float = 0.0, w_lda: float = 0.0, penalized_classes: Optional[List[str]] = None,
        micro_prototypes: Optional[np.ndarray] = None, class_names: Optional[List[str]] = None,
        archetype_map: Optional[Dict[str, int]] = None, negative_prototypes: Optional[np.ndarray] = None,
        enable_clutter_suppression: bool = False, enable_rectification: bool = True,
        enable_router: bool = True, enable_hard_argmax: bool = False,
        gamma_glare: float = 0.15, threshold_glare: float = 0.06,
    ):
        self.bioclip_dim, self.dinov2_dim = bioclip_dim, dinov2_dim
        self.joint_dim = bioclip_dim + dinov2_dim
        self.shrinkage, self.router_temp, self.vis_temp, self.text_temp = shrinkage, router_temp, vis_temp, text_temp
        self.w_vis, self.margin_penalty, self.alpha_bayes, self.w_bio = w_vis, margin_penalty, alpha_bayes, w_bio
        self.beta_bayes, self.w_lda = beta_bayes, w_lda
        self.penalized_classes = penalized_classes or ["Potato_leaf_late_blight"]
        self.enable_rectification, self.enable_router = enable_rectification, enable_router
        self.enable_hard_argmax, self.enable_clutter_suppression = enable_hard_argmax, enable_clutter_suppression
        self.gamma_glare, self.threshold_glare, self.suppressor = gamma_glare, threshold_glare, None

        if enable_clutter_suppression or negative_prototypes is not None:
            try:
                from pipeline.canopy_suppressor import CanopyClutterGlareSuppressor
            except (ImportError, ModuleNotFoundError):
                from canopy_suppressor import CanopyClutterGlareSuppressor  # type: ignore[no-redef]
            self.suppressor = CanopyClutterGlareSuppressor(
                negative_prototypes=negative_prototypes, gamma_glare=gamma_glare, threshold_glare=threshold_glare
            )

        self.micro_prototypes = l2_normalize(micro_prototypes) if micro_prototypes is not None else None
        self.class_names, self.archetype_map = class_names or [], archetype_map or DEFAULT_ARCHETYPE_MAP
        self.is_fitted = False
        self.class_to_arch = self.arch_protos_dino = self.mu_s = self.protos_rect = None
        self.protos_bio_rect = self.protos_dino_rect = self.mu_s_bio = self.mu_s_dino = None
        self.lda_clfs: Dict[int, Tuple[LinearDiscriminantAnalysis, np.ndarray]] = {}
        self.n_classes, self.penalized_indices = 0, []

    def _split_features(
        self, features: np.ndarray, bioclip_features: Optional[np.ndarray] = None, dinov2_features: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Separates features into BioCLIP (512-d) and DINOv2 (384-d) components."""
        if bioclip_features is not None and dinov2_features is not None:
            return bioclip_features, dinov2_features
        if features.shape[-1] == self.joint_dim:
            return features[:, : self.bioclip_dim], features[:, self.bioclip_dim :]
        raise ValueError(f"Expected joint dimension {self.joint_dim}, got {features.shape[-1]}")

    def fit(
        self,
        support_features: np.ndarray,
        support_labels: np.ndarray,
        support_bioclip: Optional[np.ndarray] = None,
        support_dino: Optional[np.ndarray] = None,
        class_names: Optional[List[str]] = None,
        micro_prototypes: Optional[np.ndarray] = None,
    ) -> MorphoPathEngine:
        """Fits the MorphoPath-Edge engine on few-shot support observations."""
        if class_names is not None: self.class_names = class_names
        if micro_prototypes is not None: self.micro_prototypes = l2_normalize(micro_prototypes)

        self.n_classes = len(self.class_names) if self.class_names else int(np.max(support_labels) + 1)
        if not self.class_names: self.class_names = [f"class_{i}" for i in range(self.n_classes)]

        self.class_to_arch = np.array([self.archetype_map.get(c, infer_archetype_for_class(c)) for c in self.class_names])
        self.penalized_indices = [i for i, c in enumerate(self.class_names) if c in self.penalized_classes]

        sup_bio, sup_dino = self._split_features(support_features, support_bioclip, support_dino)
        sup_arch = self.class_to_arch[support_labels]

        # 1. 4-Archetype DINOv2 Foliar Router Prototypes (ADR-001)
        arch_protos = [
            sup_dino[sup_arch == a].mean(axis=0) if np.any(sup_arch == a) else np.zeros(self.dinov2_dim, dtype=np.float32)
            for a in range(4)
        ]
        self.arch_protos_dino = l2_normalize(np.stack(arch_protos))

        # 2. Tukey Power Transform & Manifold Rectification (ADR-005)
        sup_joint = tukey_power_transform(np.concatenate([sup_bio, sup_dino], axis=-1))
        sup_cent, self.mu_s = center_and_normalize(sup_joint) if self.enable_rectification else (sup_joint, np.zeros((1, self.joint_dim), dtype=np.float32))
        self.protos_rect = compute_prototypes(sup_cent, support_labels, self.n_classes)

        # 3. Decoupled Subspace Rectification Prototypes (w_bio weighting)
        if self.w_bio is not None:
            sb, sd = tukey_power_transform(sup_bio), tukey_power_transform(sup_dino)
            sbc, self.mu_s_bio = center_and_normalize(sb) if self.enable_rectification else (sb, np.zeros((1, self.bioclip_dim), dtype=np.float32))
            sdc, self.mu_s_dino = center_and_normalize(sd) if self.enable_rectification else (sd, np.zeros((1, self.dinov2_dim), dtype=np.float32))
            self.protos_bio_rect = compute_prototypes(sbc, support_labels, self.n_classes)
            self.protos_dino_rect = compute_prototypes(sdc, support_labels, self.n_classes)
        else:
            self.protos_bio_rect = self.protos_dino_rect = None

        # 4. Regularized Shrunk Fisher LDA per Archetype (ADR-002)
        self.lda_clfs = {}
        for a in range(4):
            cands = np.where(self.class_to_arch == a)[0]
            mask_sup_a = (sup_arch == a)
            if len(cands) <= 1 or not np.any(mask_sup_a):
                continue
            local_map = {c: i for i, c in enumerate(cands)}
            y_loc = np.array([local_map[y] for y in support_labels[mask_sup_a]])
            if len(np.unique(y_loc)) >= 2:
                self.lda_clfs[a] = (fit_shrunk_lda(sup_cent[mask_sup_a], y_loc, shrinkage=self.shrinkage), cands)

        self.is_fitted = True
        return self

    def forward(
        self,
        query_features: np.ndarray,
        query_bioclip: Optional[np.ndarray] = None,
        query_dino: Optional[np.ndarray] = None,
        field_running_mean: Optional[np.ndarray] = None,
    ) -> MorphoPathOutput:
        """Executes zero-copy vectorized inference on field query observations."""
        if not self.is_fitted:
            raise RuntimeError("MorphoPathEngine must be fitted via .fit() before inference.")

        qry_bio, qry_dino = self._split_features(query_features, query_bioclip, query_dino)
        n_queries = len(qry_bio)

        # 1. Macro-Botanical Foliar Routing (ADR-001)
        if self.enable_router:
            p_arch = softmax_prob(l2_normalize(qry_dino) @ self.arch_protos_dino.T, temp=self.router_temp)
            pred_arch = p_arch.argmax(axis=-1)
        else:
            p_arch = np.full((n_queries, 4), 0.25, dtype=np.float32)
            pred_arch = np.zeros(n_queries, dtype=np.int64)

        # 2. Tukey Power Transform & Test-Time Manifold Rectification (ADR-005)
        qry_joint = query_features if query_features.shape[-1] == self.joint_dim else np.concatenate([qry_bio, qry_dino], axis=-1)
        qry_jt = tukey_power_transform(qry_joint)
        mu_q = (field_running_mean if field_running_mean is not None else qry_jt.mean(axis=0, keepdims=True)) if self.enable_rectification else None
        qry_cent = l2_normalize(qry_jt - mu_q) if self.enable_rectification else qry_jt

        # 3. Rectified Prototypes Cosine Similarities (ADR-005)
        if self.w_bio is not None and self.protos_bio_rect is not None:
            qb, qd = tukey_power_transform(qry_bio), tukey_power_transform(qry_dino)
            qbc, _ = center_and_normalize(qb) if self.enable_rectification else (qb, None)
            qdc, _ = center_and_normalize(qd) if self.enable_rectification else (qd, None)
            sims_rect = self.w_bio * (qbc @ self.protos_bio_rect.T) + (1.0 - self.w_bio) * (qdc @ self.protos_dino_rect.T)
        else:
            sims_rect = qry_cent @ self.protos_rect.T

        # 4. Micro-Symptom Text Fusion & Margin Penalties (ADR-004)
        sims_rect_margin = sims_rect.copy()
        if self.penalized_indices and self.margin_penalty > 0.0:
            sims_rect_margin[:, self.penalized_indices] -= self.margin_penalty
        p_vis_m = softmax_prob(sims_rect_margin, temp=self.vis_temp)

        p_comb = p_vis_m.copy()
        if self.micro_prototypes is not None and self.w_vis < 1.0:
            p_txt = softmax_prob(l2_normalize(qry_bio) @ self.micro_prototypes.T, temp=self.text_temp)
            p_comb = self.w_vis * p_vis_m + (1.0 - self.w_vis) * p_txt

        # 5. Soft Bayesian Foliar Archetype Prior Gating (ADR-003)
        if self.beta_bayes > 0.0 and self.enable_router:
            p_comb = p_comb * (p_arch[:, self.class_to_arch] ** self.beta_bayes)
            p_comb /= (p_comb.sum(axis=-1, keepdims=True) + 1e-12)

        # 6. Intra-Archetype Shrunk Fisher LDA Posterior Fusion (ADR-002)
        if self.w_lda > 0.0 and len(self.lda_clfs) > 0:
            p_lda = np.zeros((n_queries, self.n_classes), dtype=np.float32)
            for a, (clf, cands) in self.lda_clfs.items():
                p_lda[:, cands] = p_arch[:, a : a + 1] * clf.predict_proba(qry_cent)
            p_comb = (1.0 - self.w_lda) * p_comb + self.w_lda * p_lda

        # 6.5. Hard Archetype Argmax Gating (Ablation Mode)
        if self.enable_hard_argmax and self.enable_router:
            p_comb = np.where(self.class_to_arch[None, :] != pred_arch[:, None], 0.0, p_comb)
            p_comb /= (p_comb.sum(axis=-1, keepdims=True) + 1e-12)

        # 6.6. Zero-Parameter Canopy Clutter & Glare Gating
        clutter_diag, glare_scores = None, None
        if self.enable_clutter_suppression and self.suppressor is not None:
            p_comb, clutter_diag = self.suppressor.modulate_probabilities(
                probabilities=p_comb, query_bioclip=qry_bio, class_names=self.class_names
            )
            glare_scores = clutter_diag.glare_score

        # 7. Zero-Copy Vectorized Top-1 & Top-2 Differential Triage (ADR-003)
        return build_morphopath_output(
            sims_rect=sims_rect, p_comb=p_comb, pred_arch=pred_arch, p_arch=p_arch,
            class_names=self.class_names, n_classes=self.n_classes,
            clutter_diag=clutter_diag, glare_scores=glare_scores,
        )

    def predict(self, query_features: np.ndarray, query_bioclip: Optional[np.ndarray] = None, query_dino: Optional[np.ndarray] = None) -> np.ndarray:
        """Returns top-1 predicted class index array of shape (N,)."""
        return self.forward(query_features, query_bioclip, query_dino).top1_preds

    def predict_proba(self, query_features: np.ndarray, query_bioclip: Optional[np.ndarray] = None, query_dino: Optional[np.ndarray] = None) -> np.ndarray:
        """Returns full calibrated class probability distributions of shape (N, K)."""
        return self.forward(query_features, query_bioclip, query_dino).probabilities

    def evaluate(
        self, query_features: np.ndarray, query_labels: np.ndarray,
        query_bioclip: Optional[np.ndarray] = None, query_dino: Optional[np.ndarray] = None,
    ) -> Dict[str, Union[float, Dict[str, Any]]]:
        """Evaluates the engine on query observations and returns comprehensive metrics."""
        return evaluate_engine(self, query_features, query_labels, query_bioclip, query_dino)


# Backwards-compatibility alias
MorphoPathClassifier = MorphoPathEngine

# Re-export all public symbols for 100% backward compatibility
__all__ = [
    "ARCHETYPE_NAMES", "DEFAULT_ARCHETYPE_MAP", "MorphoPathClassifier", "MorphoPathEngine",
    "MorphoPathOutput", "build_morphopath_output", "calculate_differential_confidence",
    "center_and_normalize", "compute_archetype_metrics", "compute_clinical_metrics",
    "compute_prototypes", "evaluate_engine", "fit_shrunk_lda", "infer_archetype_for_class",
    "is_healthy_leaf_name", "l2_normalize", "softmax_prob", "tukey_power_transform",
]

if __name__ == "__main__":
    from tests.test_morphopath_engine import run_all_tests
    run_all_tests()

"""
MorphoPath-Edge: Production-Grade Foliar-Pathology Dual Inference Engine.
Integrates foliar routing (ADR-001), Tukey rectification (ADR-005), regularized
LDA (ADR-002), micro-symptom fusion (ADR-004), Bayesian triage (ADR-003),
Canopy Clutter & Glare Gating, and Cross-Subspace Bilinear Gating (IDEA-015).
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

from pipeline_morphopath.morphopath_types import MorphoPathOutput, build_morphopath_output
from pipeline_morphopath.morphopath_archetypes import ARCHETYPE_NAMES, DEFAULT_ARCHETYPE_MAP, infer_archetype_for_class, is_healthy_leaf_name
from pipeline_morphopath.morphopath_math import (
    l2_normalize, tukey_power_transform, center_and_normalize, softmax_prob,
    calculate_differential_confidence, fit_shrunk_lda, compute_prototypes,
    gegenbauer_decrowd_kernel,
)
from pipeline_morphopath.morphopath_eval import evaluate_engine, compute_clinical_metrics, compute_archetype_metrics


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
        alpha_bilinear: float = 0.0, gamma_gegenbauer: float = 0.0,
        enable_fast_exit: bool = False, fast_exit_conf: float = 0.95, fast_exit_margin: float = 0.60,
    ):
        self.bioclip_dim, self.dinov2_dim = bioclip_dim, dinov2_dim
        self.joint_dim = bioclip_dim + dinov2_dim
        self.shrinkage, self.router_temp, self.vis_temp, self.text_temp = shrinkage, router_temp, vis_temp, text_temp
        self.w_vis, self.margin_penalty, self.alpha_bayes, self.w_bio = w_vis, margin_penalty, alpha_bayes, w_bio
        self.beta_bayes, self.w_lda, self.alpha_bilinear = beta_bayes, w_lda, alpha_bilinear
        self.gamma_gegenbauer = gamma_gegenbauer
        self.enable_fast_exit, self.fast_exit_conf, self.fast_exit_margin = enable_fast_exit, fast_exit_conf, fast_exit_margin
        self.penalized_classes = penalized_classes or ["Potato_leaf_late_blight"]
        self.enable_rectification, self.enable_router = enable_rectification, enable_router
        self.enable_hard_argmax, self.enable_clutter_suppression = enable_hard_argmax, enable_clutter_suppression
        self.gamma_glare, self.threshold_glare, self.suppressor = gamma_glare, threshold_glare, None

        if enable_clutter_suppression or negative_prototypes is not None:
            try:
                from pipeline_morphopath.canopy_suppressor import CanopyClutterGlareSuppressor
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
        if bioclip_features is not None and dinov2_features is not None:
            return bioclip_features, dinov2_features
        if features.shape[-1] == self.joint_dim:
            return features[:, : self.bioclip_dim], features[:, self.bioclip_dim :]
        raise ValueError(f"Expected joint dimension {self.joint_dim}, got {features.shape[-1]}")

    def fit(
        self, support_features: np.ndarray, support_labels: np.ndarray,
        support_bioclip: Optional[np.ndarray] = None, support_dino: Optional[np.ndarray] = None,
        class_names: Optional[List[str]] = None, micro_prototypes: Optional[np.ndarray] = None,
    ) -> MorphoPathEngine:
        if class_names is not None: self.class_names = class_names
        if micro_prototypes is not None: self.micro_prototypes = l2_normalize(micro_prototypes)
        self.n_classes = len(self.class_names) if self.class_names else int(np.max(support_labels) + 1)
        if not self.class_names: self.class_names = [f"class_{i}" for i in range(self.n_classes)]
        self.class_to_arch = np.array([self.archetype_map.get(c, infer_archetype_for_class(c)) for c in self.class_names])
        self.penalized_indices = [i for i, c in enumerate(self.class_names) if c in self.penalized_classes]

        sup_bio, sup_dino = self._split_features(support_features, support_bioclip, support_dino)
        sup_arch = self.class_to_arch[support_labels]

        # 1. Macro-Botanical Router Prototypes (ADR-001)
        arch_protos = [sup_dino[sup_arch == a].mean(axis=0) if np.any(sup_arch == a) else np.zeros(self.dinov2_dim, dtype=np.float32) for a in range(4)]
        self.arch_protos_dino = l2_normalize(np.stack(arch_protos))

        # 2. Tukey Power Transform & Manifold Rectification (ADR-005)
        sup_joint = tukey_power_transform(np.concatenate([sup_bio, sup_dino], axis=-1))
        sup_cent, self.mu_s = center_and_normalize(sup_joint) if self.enable_rectification else (sup_joint, np.zeros((1, self.joint_dim), dtype=np.float32))
        self.protos_rect = compute_prototypes(sup_cent, support_labels, self.n_classes)

        # 3. Decoupled Subspace Rectification Prototypes
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
            if len(cands) <= 1 or not np.any(mask_sup_a): continue
            local_map = {c: i for i, c in enumerate(cands)}
            y_loc = np.array([local_map[y] for y in support_labels[mask_sup_a]])
            if len(np.unique(y_loc)) >= 2:
                self.lda_clfs[a] = (fit_shrunk_lda(sup_cent[mask_sup_a], y_loc, shrinkage=self.shrinkage), cands)
        self.is_fitted = True
        return self

    def forward(
        self, query_features: np.ndarray, query_bioclip: Optional[np.ndarray] = None,
        query_dino: Optional[np.ndarray] = None, field_running_mean: Optional[np.ndarray] = None,
    ) -> MorphoPathOutput:
        if not self.is_fitted: raise RuntimeError("MorphoPathEngine must be fitted via .fit() before inference.")
        qry_bio, qry_dino = self._split_features(query_features, query_bioclip, query_dino)
        n_queries = len(qry_bio)

        # 1. Foliar Routing (ADR-001)
        if self.enable_router:
            p_arch = softmax_prob(l2_normalize(qry_dino) @ self.arch_protos_dino.T, temp=self.router_temp)
            pred_arch = p_arch.argmax(axis=-1)
        else:
            p_arch, pred_arch = np.full((n_queries, 4), 0.25, dtype=np.float32), np.zeros(n_queries, dtype=np.int64)

        # 2. Tukey & Rectification (ADR-005)
        qry_joint = query_features if query_features.shape[-1] == self.joint_dim else np.concatenate([qry_bio, qry_dino], axis=-1)
        qry_jt = tukey_power_transform(qry_joint)
        mu_q = (field_running_mean if field_running_mean is not None else qry_jt.mean(axis=0, keepdims=True)) if self.enable_rectification else None
        qry_cent = l2_normalize(qry_jt - mu_q) if self.enable_rectification else qry_jt

        # 3. Rectified Prototypes & Cross-Subspace Bilinear Gating (IDEA-015)
        if self.w_bio is not None and self.protos_bio_rect is not None:
            qb, qd = tukey_power_transform(qry_bio), tukey_power_transform(qry_dino)
            qbc, _ = center_and_normalize(qb) if self.enable_rectification else (qb, None)
            qdc, _ = center_and_normalize(qd) if self.enable_rectification else (qd, None)
            sb_sim = qbc @ self.protos_bio_rect.T
            sd_sim = qdc @ self.protos_dino_rect.T
            sims_rect = self.w_bio * sb_sim + (1.0 - self.w_bio) * sd_sim
            if self.alpha_bilinear != 0.0:
                sims_rect = sims_rect + self.alpha_bilinear * (sb_sim * sd_sim)
        else:
            sims_rect = qry_cent @ self.protos_rect.T

        if self.gamma_gegenbauer != 0.0:
            sims_rect = gegenbauer_decrowd_kernel(sims_rect, dim=self.joint_dim, gamma=self.gamma_gegenbauer)

        # 4. Text Fusion & Margin Penalties (ADR-004)
        sims_m = sims_rect.copy()
        if self.penalized_indices and self.margin_penalty > 0.0:
            sims_m[:, self.penalized_indices] -= self.margin_penalty
        p_vis_m = softmax_prob(sims_m, temp=self.vis_temp)

        # 4.5. Fast-Exit Decision Cascade Check (IDEA-016)
        if self.enable_fast_exit:
            ranked = np.argsort(-p_vis_m, axis=-1)
            p1 = p_vis_m[np.arange(n_queries), ranked[:, 0]]
            p2 = p_vis_m[np.arange(n_queries), ranked[:, 1]]
            if np.all((p1 >= self.fast_exit_conf) & ((p1 - p2) >= self.fast_exit_margin)):
                return build_morphopath_output(sims_rect, p_vis_m, pred_arch, p_arch, self.class_names, self.n_classes)

        p_comb = p_vis_m.copy()
        if self.micro_prototypes is not None and self.w_vis < 1.0:
            p_txt = softmax_prob(l2_normalize(qry_bio) @ self.micro_prototypes.T, temp=self.text_temp)
            p_comb = self.w_vis * p_vis_m + (1.0 - self.w_vis) * p_txt

        # 5. Bayesian Foliar Prior Gating (ADR-003)
        if self.beta_bayes > 0.0 and self.enable_router:
            p_comb = p_comb * (p_arch[:, self.class_to_arch] ** self.beta_bayes)
            p_comb /= (p_comb.sum(axis=-1, keepdims=True) + 1e-12)

        # 6. Intra-Archetype Shrunk Fisher LDA (ADR-002)
        if self.w_lda > 0.0 and len(self.lda_clfs) > 0:
            p_lda = np.zeros((n_queries, self.n_classes), dtype=np.float32)
            for a, (clf, cands) in self.lda_clfs.items():
                p_lda[:, cands] = p_arch[:, a : a + 1] * clf.predict_proba(qry_cent)
            p_comb = (1.0 - self.w_lda) * p_comb + self.w_lda * p_lda

        if self.enable_hard_argmax and self.enable_router:
            p_comb = np.where(self.class_to_arch[None, :] != pred_arch[:, None], 0.0, p_comb)
            p_comb /= (p_comb.sum(axis=-1, keepdims=True) + 1e-12)

        # 6.6. Canopy Clutter & Glare Gating
        clutter_diag, glare_scores = None, None
        if self.enable_clutter_suppression and self.suppressor is not None:
            p_comb, clutter_diag = self.suppressor.modulate_probabilities(
                probabilities=p_comb, query_bioclip=qry_bio, class_names=self.class_names
            )
            glare_scores = clutter_diag.glare_score

        # 7. Differential Triage Assembly
        return build_morphopath_output(
            sims_rect=sims_rect, p_comb=p_comb, pred_arch=pred_arch, p_arch=p_arch,
            class_names=self.class_names, n_classes=self.n_classes,
            clutter_diag=clutter_diag, glare_scores=glare_scores,
        )

    def predict(self, query_features: np.ndarray, query_bioclip: Optional[np.ndarray] = None, query_dino: Optional[np.ndarray] = None) -> np.ndarray:
        return self.forward(query_features, query_bioclip, query_dino).top1_preds

    def predict_proba(self, query_features: np.ndarray, query_bioclip: Optional[np.ndarray] = None, query_dino: Optional[np.ndarray] = None) -> np.ndarray:
        return self.forward(query_features, query_bioclip, query_dino).probabilities

    def evaluate(self, query_features: np.ndarray, query_labels: np.ndarray, query_bioclip: Optional[np.ndarray] = None, query_dino: Optional[np.ndarray] = None) -> Dict[str, Any]:
        return evaluate_engine(self, query_features, query_labels, query_bioclip, query_dino)


MorphoPathClassifier = MorphoPathEngine

__all__ = [
    "ARCHETYPE_NAMES", "DEFAULT_ARCHETYPE_MAP", "MorphoPathClassifier", "MorphoPathEngine",
    "MorphoPathOutput", "build_morphopath_output", "calculate_differential_confidence",
    "center_and_normalize", "compute_archetype_metrics", "compute_clinical_metrics",
    "compute_prototypes", "evaluate_engine", "fit_shrunk_lda", "infer_archetype_for_class",
    "is_healthy_leaf_name", "l2_normalize", "softmax_prob", "tukey_power_transform",
]

if __name__ == "__main__":
    from tests_morphopath.test_morphopath_engine import run_all_tests
    run_all_tests()

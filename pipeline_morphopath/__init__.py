"""
MorphoPath-Edge: Production-Grade Foliar-Pathology Dual Inference Engine Package.
Dedicated pipeline for Paper 2 (MorphoPath-Edge).
"""

from pipeline_morphopath.morphopath_types import MorphoPathOutput, build_morphopath_output
from pipeline_morphopath.morphopath_archetypes import (
    ARCHETYPE_NAMES,
    DEFAULT_ARCHETYPE_MAP,
    infer_archetype_for_class,
    is_healthy_leaf_name,
)
from pipeline_morphopath.morphopath_math import (
    l2_normalize,
    tukey_power_transform,
    center_and_normalize,
    softmax_prob,
    calculate_differential_confidence,
    fit_shrunk_lda,
    compute_prototypes,
    gegenbauer_decrowd_kernel,
)
from pipeline_morphopath.morphopath_engine import MorphoPathEngine, MorphoPathClassifier
from pipeline_morphopath.morphopath_eval import evaluate_engine, compute_clinical_metrics, compute_archetype_metrics
from pipeline_morphopath.canopy_suppressor import CanopyClutterGlareSuppressor, ClutterDiagnostics

__all__ = [
    "ARCHETYPE_NAMES",
    "CanopyClutterGlareSuppressor",
    "ClutterDiagnostics",
    "DEFAULT_ARCHETYPE_MAP",
    "MorphoPathClassifier",
    "MorphoPathEngine",
    "MorphoPathOutput",
    "build_morphopath_output",
    "calculate_differential_confidence",
    "center_and_normalize",
    "compute_archetype_metrics",
    "compute_clinical_metrics",
    "compute_prototypes",
    "evaluate_engine",
    "fit_shrunk_lda",
    "gegenbauer_decrowd_kernel",
    "infer_archetype_for_class",
    "is_healthy_leaf_name",
    "l2_normalize",
    "softmax_prob",
    "tukey_power_transform",
]


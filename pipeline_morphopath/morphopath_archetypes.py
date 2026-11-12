"""
================================================================================
MorphoPath-Edge: Botanical Foliar Archetypes & Heuristics (morphopath_archetypes.py)
================================================================================
Implements domain-informed macro-botanical foliar partitioning (ADR-001):
  1. Archetype 0 (Solanoid): Compound serrate leaves (e.g. Tomato, Potato).
  2. Archetype 1 (Vitoid/Cucurbit): Broad palmate-lobed leaves (e.g. Grape, Squash).
  3. Archetype 2 (Pooid): Linear parallel-veined monocots (e.g. Corn, Maize).
  4. Archetype 3 (Rosoid/Deciduous): Simple ovate/serrate foliage (e.g. Apple, Peach).
================================================================================
"""

from __future__ import annotations
from typing import Dict, List


ARCHETYPE_NAMES: List[str] = [
    "A0: Solanoid (Compound serrate - Tomato/Potato)",
    "A1: Vitoid/Cucurbit (Broad palmate - Grape/Squash)",
    "A2: Pooid (Monocot linear parallel - Corn)",
    "A3: Rosoid/Other (Simple ovate/serrate - Apple/Peach/Cherry/etc.)",
]

DEFAULT_ARCHETYPE_MAP: Dict[str, int] = {
    # Archetype 0: Solanoid (Compound serrate) - 10 classes
    "Tomato_Early_blight_leaf": 0, "Tomato_Septoria_leaf_spot": 0, "Tomato_leaf": 0,
    "Tomato_leaf_bacterial_spot": 0, "Tomato_leaf_late_blight": 0, "Tomato_leaf_mosaic_virus": 0,
    "Tomato_leaf_yellow_virus": 0, "Tomato_mold_leaf": 0,
    "Potato_leaf_early_blight": 0, "Potato_leaf_late_blight": 0,
    # Archetype 1: Vitoid/Cucurbit (Broad palmate) - 3 classes
    "grape_leaf": 1, "grape_leaf_black_rot": 1, "Squash_Powdery_mildew_leaf": 1,
    # Archetype 2: Pooid (Monocot linear parallel) - 3 classes
    "Corn_Gray_leaf_spot": 2, "Corn_leaf_blight": 2, "Corn_rust_leaf": 2,
    # Archetype 3: Rosoid/Other (Simple ovate/serrate) - 11 classes
    "Apple_Scab_Leaf": 3, "Apple_leaf": 3, "Apple_rust_leaf": 3,
    "Bell_pepper_leaf": 3, "Bell_pepper_leaf_spot": 3,
    "Blueberry_leaf": 3, "Cherry_leaf": 3, "Peach_leaf": 3,
    "Raspberry_leaf": 3, "Soyabean_leaf": 3, "Strawberry_leaf": 3,
}


def infer_archetype_for_class(class_name: str) -> int:
    """
    Infers the botanical foliar archetype index for novel class strings.

    Parameters
    ----------
    class_name : str
        Foliar disease or healthy class string (e.g. 'Tomato_Early_blight_leaf').

    Returns
    -------
    int
        Archetype index in range [0, 3].
    """
    cn = class_name.lower()
    if any(h in cn for h in ["tomato", "potato", "solan"]):
        return 0
    if any(h in cn for h in ["grape", "squash", "cucumber", "melon", "vitoid", "cucurbit"]):
        return 1
    if any(h in cn for h in ["corn", "maize", "pooid", "wheat", "rice", "grass"]):
        return 2
    return 3


def is_healthy_leaf_name(name: str, legacy_broad: bool = False) -> bool:
    """
    Identifies whether a class name corresponds to an asymptomatic healthy leaf.

    Parameters
    ----------
    name : str
        Foliar class string name.
    legacy_broad : bool, default=False
        If True, reproduces legacy broad matching heuristics.

    Returns
    -------
    bool
        True if the class name denotes an asymptomatic healthy leaf specimen.
    """
    name_lower = name.lower()
    if legacy_broad:
        if "healthy" in name_lower:
            return True
        return ("leaf" in name_lower and not any(kw in name_lower for kw in [
            "blight", "spot", "rot", "mold", "virus", "rust", "mildew", "scab", "scorch", "mite"
        ])) or name_lower.endswith("_leaf")

    if "healthy" in name_lower:
        return True
    diseases = ["scab", "rust", "spot", "blight", "mildew", "virus", "mold", "rot", "mite", "curl", "scorch"]
    if any(d in name_lower for d in diseases):
        return False
    return name_lower.endswith("_leaf") or name_lower.endswith("leaf")


__all__ = [
    "ARCHETYPE_NAMES",
    "DEFAULT_ARCHETYPE_MAP",
    "infer_archetype_for_class",
    "is_healthy_leaf_name",
]


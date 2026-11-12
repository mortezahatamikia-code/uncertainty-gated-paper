"""
Benchmark Intermediate Transformer Layer Fusion (ITLF) on PlantDoc Seed 42.
Evaluates intermediate layers (7, 8, 9, 10, 11) alongside Layer 12 across DINOv2 and BioCLIP.
Tests:
  1. Exact baseline replication (Layer 12 alone -> 65.08%).
  2. Individual intermediate layers (7, 8, 9, 10, 11 alone).
  3. Weighted blend / normalized sum fusion (L_mid + L12) across alpha grid.
  4. Multi-scale hierarchical fusion (L7 + L9 + L12).
  5. Concatenation fusion.
  6. Asymmetric backbone fusion (e.g. DINO multi-layer + BioCLIP L12).
Measures: Top-1, Top-2, Macro F1, FPR, FNR, CPU Latency, and Memory.
"""

import sys
import time
from pathlib import Path
from typing import Dict, Any, Tuple, List

PROJECT_ROOT = Path("E:/work/research-few-shot")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import torch
import torch.nn.functional as F

from pipeline_morphopath.morphopath_engine import MorphoPathEngine
from pipeline_morphopath.morphopath_math import l2_normalize

CACHE_FILE = PROJECT_ROOT / "experiments" / "phase1_morphopath" / "plantdoc_intermediate_features_seed42.pt"
MICRO_FILE = PROJECT_ROOT / "experiments" / "phase1_morphopath" / "micro_symptom_prototypes.pt"


def load_dataset():
    print(f"[*] Loading intermediate features: {CACHE_FILE}")
    data = torch.load(CACHE_FILE, map_location="cpu")
    micro_data = torch.load(MICRO_FILE, map_location="cpu")

    micro_protos = micro_data["micro_prototypes"].float().numpy()
    class_names = data["class_names"]
    sup_labels = data["support_labels"].numpy()
    qry_labels = data["query_labels"].numpy()

    return data, micro_protos, class_names, sup_labels, qry_labels


def evaluate_config(
    sup_bio: np.ndarray,
    sup_dino: np.ndarray,
    qry_bio: np.ndarray,
    qry_dino: np.ndarray,
    sup_labels: np.ndarray,
    qry_labels: np.ndarray,
    class_names: List[str],
    micro_protos: np.ndarray,
    text_bio_slice: bool = False,
) -> Dict[str, Any]:
    """Evaluates features through full Phase 4.3 MorphoPath pipeline."""
    bio_dim = sup_bio.shape[-1]
    dino_dim = sup_dino.shape[-1]
    sup_joint = np.concatenate([sup_bio, sup_dino], axis=-1)
    qry_joint = np.concatenate([qry_bio, qry_dino], axis=-1)

    # If bio_dim != 512, disable micro_prototypes text alignment to prevent dimension mismatch
    effective_micro = micro_protos if bio_dim == 512 else None

    engine = MorphoPathEngine(
        bioclip_dim=bio_dim,
        dinov2_dim=dino_dim,
        shrinkage=0.60,
        router_temp=12.0,
        vis_temp=15.0,
        text_temp=30.0,
        w_vis=0.75 if effective_micro is not None else 1.0,
        margin_penalty=0.05,
        w_bio=0.65,
        penalized_classes=["Potato_leaf_late_blight"],
        micro_prototypes=effective_micro,
        class_names=class_names,
        enable_clutter_suppression=(bio_dim == 512),
        gamma_glare=0.15,
        threshold_glare=0.06,
        alpha_bilinear=0.20,
        gamma_gegenbauer=-0.20,
    )

    engine.fit(
        support_features=sup_joint,
        support_labels=sup_labels,
        support_bioclip=sup_bio,
        support_dino=sup_dino,
    )

    # Benchmark CPU inference latency (5 runs over queries)
    t0 = time.perf_counter()
    for _ in range(5):
        _ = engine.forward(qry_joint, query_bioclip=qry_bio, query_dino=qry_dino)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0 / (5 * len(qry_labels))

    metrics = engine.evaluate(qry_joint, qry_labels, query_bioclip=qry_bio, query_dino=qry_dino)
    metrics["latency_per_sample_ms"] = elapsed_ms
    metrics["total_dim"] = bio_dim + dino_dim
    return metrics


def run_benchmark():
    data, micro_protos, class_names, sup_labels, qry_labels = load_dataset()

    # PyTorch tensors on CPU
    sup_dino_layers = {k: v.numpy() for k, v in data["support_dino_layers"].items()}
    sup_bio_layers = {k: v.numpy() for k, v in data["support_bioclip_proj_layers"].items()}
    qry_dino_layers = {k: v.numpy() for k, v in data["query_dino_layers"].items()}
    qry_bio_layers = {k: v.numpy() for k, v in data["query_bioclip_proj_layers"].items()}

    results = []

    print("\n" + "=" * 90)
    print("STEP 1: REPLICATE CANONICAL PHASE 4.3 SOTA BASELINE (LAYER 12 ALONE)")
    print("=" * 90)

    m12 = evaluate_config(
        sup_bio=sup_bio_layers[12],
        sup_dino=sup_dino_layers[12],
        qry_bio=qry_bio_layers[12],
        qry_dino=qry_dino_layers[12],
        sup_labels=sup_labels,
        qry_labels=qry_labels,
        class_names=class_names,
        micro_protos=micro_protos,
    )
    print(f"Baseline (L12 Alone): Top-1: {m12['accuracy_top1']:.2f}% | Top-2: {m12['accuracy_top2']:.2f}% | "
          f"Macro F1: {m12['macro_f1']:.2f}% | FPR: {m12['fpr']:.2f}% | FNR: {m12['fnr']:.2f}% | "
          f"Latency: {m12['latency_per_sample_ms']:.4f} ms")
    assert abs(m12['accuracy_top1'] - 65.08) < 0.1, f"Expected 65.08%, got {m12['accuracy_top1']}"
    assert abs(m12['accuracy_top2'] - 80.16) < 0.1, f"Expected 80.16%, got {m12['accuracy_top2']}"
    print("[✓] EXACT BASELINE REPLICATION CONFIRMED: 65.08% Top-1, 80.16% Top-2\n")

    results.append({
        "name": "Baseline (L12 Alone)",
        "config": "DINO L12 + BioCLIP L12",
        "top1": m12['accuracy_top1'],
        "top2": m12['accuracy_top2'],
        "macro_f1": m12['macro_f1'],
        "fpr": m12['fpr'],
        "fnr": m12['fnr'],
        "latency_ms": m12['latency_per_sample_ms'],
        "dim": m12['total_dim'],
    })

    print("=" * 90)
    print("STEP 2: INDIVIDUAL INTERMEDIATE LAYERS ALONE (L7, L8, L9, L10, L11)")
    print("=" * 90)
    for l in [11, 10, 9, 8, 7]:
        m = evaluate_config(
            sup_bio=sup_bio_layers[l],
            sup_dino=sup_dino_layers[l],
            qry_bio=qry_bio_layers[l],
            qry_dino=qry_dino_layers[l],
            sup_labels=sup_labels,
            qry_labels=qry_labels,
            class_names=class_names,
            micro_protos=micro_protos,
        )
        print(f"Layer {l:2d} Alone: Top-1: {m['accuracy_top1']:5.2f}% | Top-2: {m['accuracy_top2']:5.2f}% | "
              f"Macro F1: {m['macro_f1']:5.2f}% | FPR: {m['fpr']:5.2f}% | FNR: {m['fnr']:5.2f}%")
        results.append({
            "name": f"Layer {l} Alone",
            "config": f"DINO L{l} + BioCLIP L{l}",
            "top1": m['accuracy_top1'],
            "top2": m['accuracy_top2'],
            "macro_f1": m['macro_f1'],
            "fpr": m['fpr'],
            "fnr": m['fnr'],
            "latency_ms": m['latency_per_sample_ms'],
            "dim": m['total_dim'],
        })

    print("\n" + "=" * 90)
    print("STEP 3: ASYMMETRIC SINGLE LAYER TESTS (DINO L_k + BioCLIP L12 & vice-versa)")
    print("=" * 90)
    for l in [11, 10, 9, 8, 7]:
        # DINO L_k + BioCLIP L12
        m_d = evaluate_config(
            sup_bio=sup_bio_layers[12],
            sup_dino=sup_dino_layers[l],
            qry_bio=qry_bio_layers[12],
            qry_dino=qry_dino_layers[l],
            sup_labels=sup_labels,
            qry_labels=qry_labels,
            class_names=class_names,
            micro_protos=micro_protos,
        )
        print(f"DINO L{l:2d} + BioCLIP L12: Top-1: {m_d['accuracy_top1']:5.2f}% | Top-2: {m_d['accuracy_top2']:5.2f}% | Macro F1: {m_d['macro_f1']:5.2f}%")
        results.append({
            "name": f"DINO L{l} + BioCLIP L12",
            "config": f"DINO L{l} + BioCLIP L12",
            "top1": m_d['accuracy_top1'],
            "top2": m_d['accuracy_top2'],
            "macro_f1": m_d['macro_f1'],
            "fpr": m_d['fpr'],
            "fnr": m_d['fnr'],
            "latency_ms": m_d['latency_per_sample_ms'],
            "dim": m_d['total_dim'],
        })

        # DINO L12 + BioCLIP L_k
        m_b = evaluate_config(
            sup_bio=sup_bio_layers[l],
            sup_dino=sup_dino_layers[12],
            qry_bio=qry_bio_layers[l],
            qry_dino=qry_dino_layers[12],
            sup_labels=sup_labels,
            qry_labels=qry_labels,
            class_names=class_names,
            micro_protos=micro_protos,
        )
        print(f"DINO L12 + BioCLIP L{l:2d}: Top-1: {m_b['accuracy_top1']:5.2f}% | Top-2: {m_b['accuracy_top2']:5.2f}% | Macro F1: {m_b['macro_f1']:5.2f}%")
        results.append({
            "name": f"DINO L12 + BioCLIP L{l}",
            "config": f"DINO L12 + BioCLIP L{l}",
            "top1": m_b['accuracy_top1'],
            "top2": m_b['accuracy_top2'],
            "macro_f1": m_b['macro_f1'],
            "fpr": m_b['fpr'],
            "fnr": m_b['fnr'],
            "latency_ms": m_b['latency_per_sample_ms'],
            "dim": m_b['total_dim'],
        })

    print("\n" + "=" * 90)
    print("STEP 4: WEIGHTED BLEND / NORMALIZED SUM FUSION: L_mid + L12 (ALPHA GRID)")
    print("=" * 90)
    best_blend = None
    best_top1 = 0.0

    alphas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    for mid_l in [9, 8, 7, 10, 11]:
        print(f"\n--- Testing Fusion: Layer {mid_l} + Layer 12 ---")
        for alpha in alphas:
            # Blend DINO
            sup_d = l2_normalize(alpha * sup_dino_layers[mid_l] + (1.0 - alpha) * sup_dino_layers[12])
            qry_d = l2_normalize(alpha * qry_dino_layers[mid_l] + (1.0 - alpha) * qry_dino_layers[12])

            # Blend BioCLIP
            sup_b = l2_normalize(alpha * sup_bio_layers[mid_l] + (1.0 - alpha) * sup_bio_layers[12])
            qry_b = l2_normalize(alpha * qry_bio_layers[mid_l] + (1.0 - alpha) * qry_bio_layers[12])

            m = evaluate_config(
                sup_bio=sup_b, sup_dino=sup_d, qry_bio=qry_b, qry_dino=qry_d,
                sup_labels=sup_labels, qry_labels=qry_labels,
                class_names=class_names, micro_protos=micro_protos,
            )

            if m['accuracy_top1'] > best_top1:
                best_top1 = m['accuracy_top1']
                best_blend = (f"Both L{mid_l}+L12", alpha, m)

            print(f"  Both L{mid_l}+L12 (alpha={alpha:.1f}): Top-1: {m['accuracy_top1']:5.2f}% | Top-2: {m['accuracy_top2']:5.2f}% | Macro F1: {m['macro_f1']:5.2f}%")

        # Also test blending ONLY DINO (leaving BioCLIP at L12)
        for alpha in [0.2, 0.3, 0.5, 0.7]:
            sup_d = l2_normalize(alpha * sup_dino_layers[mid_l] + (1.0 - alpha) * sup_dino_layers[12])
            qry_d = l2_normalize(alpha * qry_dino_layers[mid_l] + (1.0 - alpha) * qry_dino_layers[12])
            m = evaluate_config(
                sup_bio=sup_bio_layers[12], sup_dino=sup_d, qry_bio=qry_bio_layers[12], qry_dino=qry_d,
                sup_labels=sup_labels, qry_labels=qry_labels,
                class_names=class_names, micro_protos=micro_protos,
            )
            if m['accuracy_top1'] > best_top1:
                best_top1 = m['accuracy_top1']
                best_blend = (f"DINO L{mid_l}+L12", alpha, m)
            print(f"  DINO only L{mid_l}+L12 (alpha={alpha:.1f}): Top-1: {m['accuracy_top1']:5.2f}% | Macro F1: {m['macro_f1']:5.2f}%")

        # Also test blending ONLY BioCLIP (leaving DINO at L12)
        for alpha in [0.2, 0.3, 0.5, 0.7]:
            sup_b = l2_normalize(alpha * sup_bio_layers[mid_l] + (1.0 - alpha) * sup_bio_layers[12])
            qry_b = l2_normalize(alpha * qry_bio_layers[mid_l] + (1.0 - alpha) * qry_bio_layers[12])
            m = evaluate_config(
                sup_bio=sup_b, sup_dino=sup_dino_layers[12], qry_bio=qry_b, qry_dino=qry_dino_layers[12],
                sup_labels=sup_labels, qry_labels=qry_labels,
                class_names=class_names, micro_protos=micro_protos,
            )
            if m['accuracy_top1'] > best_top1:
                best_top1 = m['accuracy_top1']
                best_blend = (f"BioCLIP only L{mid_l}+L12", alpha, m)
            print(f"  BioCLIP only L{mid_l}+L12 (alpha={alpha:.1f}): Top-1: {m['accuracy_top1']:5.2f}% | Macro F1: {m['macro_f1']:5.2f}%")

    print("\n" + "=" * 90)
    print("STEP 5: MULTI-SCALE HIERARCHY (L7 + L9 + L12)")
    print("=" * 90)
    # Tri-layer blends: weights (w7, w9, w12)
    tri_weights = [
        (0.2, 0.3, 0.5),
        (0.15, 0.25, 0.60),
        (0.10, 0.20, 0.70),
        (0.33, 0.33, 0.34),
        (0.25, 0.25, 0.50),
    ]
    for w7, w9, w12_wt in tri_weights:
        sup_d = l2_normalize(w7 * sup_dino_layers[7] + w9 * sup_dino_layers[9] + w12_wt * sup_dino_layers[12])
        qry_d = l2_normalize(w7 * qry_dino_layers[7] + w9 * qry_dino_layers[9] + w12_wt * qry_dino_layers[12])
        sup_b = l2_normalize(w7 * sup_bio_layers[7] + w9 * sup_bio_layers[9] + w12_wt * sup_bio_layers[12])
        qry_b = l2_normalize(w7 * qry_bio_layers[7] + w9 * qry_bio_layers[9] + w12_wt * qry_bio_layers[12])

        m = evaluate_config(
            sup_bio=sup_b, sup_dino=sup_d, qry_bio=qry_b, qry_dino=qry_d,
            sup_labels=sup_labels, qry_labels=qry_labels,
            class_names=class_names, micro_protos=micro_protos,
        )
        print(f"Hierarchy L7({w7})+L9({w9})+L12({w12_wt}): Top-1: {m['accuracy_top1']:5.2f}% | Top-2: {m['accuracy_top2']:5.2f}% | Macro F1: {m['macro_f1']:5.2f}%")

    print("\n" + "=" * 90)
    print("STEP 6: CONCATENATION FUSION")
    print("=" * 90)
    # Concat DINO: [L9 || L12] -> 768-d
    # Concat BioCLIP: [L9 || L12] -> 1024-d
    for mid_l in [9, 8, 7]:
        sup_d_cat = l2_normalize(np.concatenate([sup_dino_layers[mid_l], sup_dino_layers[12]], axis=-1))
        qry_d_cat = l2_normalize(np.concatenate([qry_dino_layers[mid_l], qry_dino_layers[12]], axis=-1))

        # DINO concat + BioCLIP L12 alone
        m_dc = evaluate_config(
            sup_bio=sup_bio_layers[12], sup_dino=sup_d_cat,
            qry_bio=qry_bio_layers[12], qry_dino=qry_d_cat,
            sup_labels=sup_labels, qry_labels=qry_labels,
            class_names=class_names, micro_protos=micro_protos,
        )
        print(f"Concat DINO [L{mid_l}||L12] (768-d) + BioCLIP L12: Top-1: {m_dc['accuracy_top1']:5.2f}% | Macro F1: {m_dc['macro_f1']:5.2f}% | Latency: {m_dc['latency_per_sample_ms']:.4f} ms")
        results.append({
            "name": f"Concat DINO [L{mid_l}||L12] + BioCLIP L12",
            "config": f"DINO 768-d + BioCLIP 512-d",
            "top1": m_dc['accuracy_top1'],
            "top2": m_dc['accuracy_top2'],
            "macro_f1": m_dc['macro_f1'],
            "fpr": m_dc['fpr'],
            "fnr": m_dc['fnr'],
            "latency_ms": m_dc['latency_per_sample_ms'],
            "dim": m_dc['total_dim'],
        })

        # Concat BioCLIP: [L_mid || L12] -> 1024-d
        sup_b_cat = l2_normalize(np.concatenate([sup_bio_layers[mid_l], sup_bio_layers[12]], axis=-1))
        qry_b_cat = l2_normalize(np.concatenate([qry_bio_layers[mid_l], qry_bio_layers[12]], axis=-1))
        m_bc = evaluate_config(
            sup_bio=sup_b_cat, sup_dino=sup_dino_layers[12],
            qry_bio=qry_b_cat, qry_dino=qry_dino_layers[12],
            sup_labels=sup_labels, qry_labels=qry_labels,
            class_names=class_names, micro_protos=micro_protos,
            text_bio_slice=True,
        )
        print(f"DINO L12 + Concat BioCLIP [L{mid_l}||L12] (1024-d): Top-1: {m_bc['accuracy_top1']:5.2f}% | Macro F1: {m_bc['macro_f1']:5.2f}% | Latency: {m_bc['latency_per_sample_ms']:.4f} ms")
        results.append({
            "name": f"DINO L12 + Concat BioCLIP [L{mid_l}||L12]",
            "config": f"DINO 384-d + BioCLIP 1024-d",
            "top1": m_bc['accuracy_top1'],
            "top2": m_bc['accuracy_top2'],
            "macro_f1": m_bc['macro_f1'],
            "fpr": m_bc['fpr'],
            "fnr": m_bc['fnr'],
            "latency_ms": m_bc['latency_per_sample_ms'],
            "dim": m_bc['total_dim'],
        })

        # Both concatenated -> 1792-d
        m_both_cat = evaluate_config(
            sup_bio=sup_b_cat, sup_dino=sup_d_cat,
            qry_bio=qry_b_cat, qry_dino=qry_d_cat,
            sup_labels=sup_labels, qry_labels=qry_labels,
            class_names=class_names, micro_protos=micro_protos,
            text_bio_slice=True,
        )
        print(f"Both Concat [L{mid_l}||L12] (1792-d): Top-1: {m_both_cat['accuracy_top1']:5.2f}% | Top-2: {m_both_cat['accuracy_top2']:5.2f}% | Macro F1: {m_both_cat['macro_f1']:5.2f}% | Latency: {m_both_cat['latency_per_sample_ms']:.4f} ms")
        results.append({
            "name": f"Both Concat [L{mid_l}||L12]",
            "config": f"DINO 768-d + BioCLIP 1024-d",
            "top1": m_both_cat['accuracy_top1'],
            "top2": m_both_cat['accuracy_top2'],
            "macro_f1": m_both_cat['macro_f1'],
            "fpr": m_both_cat['fpr'],
            "fnr": m_both_cat['fnr'],
            "latency_ms": m_both_cat['latency_per_sample_ms'],
            "dim": m_both_cat['total_dim'],
        })

    print("\n" + "=" * 90)
    print("STEP 7: RAW CLS TOKEN EVALUATION (UNPROJECTED 768-D BioCLIP & RAW DINO)")
    print("=" * 90)
    sup_dino_raw = {k: v.numpy() for k, v in data["support_dino_raw_layers"].items()}
    qry_dino_raw = {k: v.numpy() for k, v in data["query_dino_raw_layers"].items()}
    sup_bio_raw = {k: v.numpy() for k, v in data["support_bioclip_raw_layers"].items()}
    qry_bio_raw = {k: v.numpy() for k, v in data["query_bioclip_raw_layers"].items()}

    for l in [12, 9, 8]:
        m_raw = evaluate_config(
            sup_bio=sup_bio_raw[l], sup_dino=sup_dino_raw[l],
            qry_bio=qry_bio_raw[l], qry_dino=qry_dino_raw[l],
            sup_labels=sup_labels, qry_labels=qry_labels,
            class_names=class_names, micro_protos=micro_protos,
        )
        print(f"Raw CLS Layer {l} (Bio 768-d + DINO 384-d): Top-1: {m_raw['accuracy_top1']:5.2f}% | Macro F1: {m_raw['macro_f1']:5.2f}%")
        results.append({
            "name": f"Raw CLS Layer {l}",
            "config": f"BioCLIP 768-d L{l} + DINO 384-d L{l}",
            "top1": m_raw['accuracy_top1'],
            "top2": m_raw['accuracy_top2'],
            "macro_f1": m_raw['macro_f1'],
            "fpr": m_raw['fpr'],
            "fnr": m_raw['fnr'],
            "latency_ms": m_raw['latency_per_sample_ms'],
            "dim": m_raw['total_dim'],
        })

    print("\n" + "=" * 90)
    print("SUMMARY OF BENCHMARK FINDINGS")
    print("=" * 90)
    print(f"Baseline Phase 4.3 SOTA: 65.08% Top-1, 80.16% Top-2")
    if best_blend:
        print(f"Best Blended Configuration: {best_blend[0]} (alpha={best_blend[1]:.2f}) -> Top-1: {best_blend[2]['accuracy_top1']:.2f}%, Top-2: {best_blend[2]['accuracy_top2']:.2f}%")
    print("=" * 90)

    import json
    json_path = PROJECT_ROOT / "experiments" / "phase1_morphopath" / "intermediate_layers_benchmark_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"[OK] Saved all benchmark results to {json_path}")

if __name__ == "__main__":
    run_benchmark()

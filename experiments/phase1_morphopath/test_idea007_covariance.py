"""
================================================================================
Empirical Test for IDEA-007: Adaptive Covariance Shrinkage & Archetype Regularization
Evaluates:
  1. Ill-conditioning analysis of within-class covariance matrices across 4 archetypes
  2. Condition number kappa(Sigma) vs shrinkage parameter lambda in [0.0, 1.0]
  3. Analytic Ledoit-Wolf shrinkage lambda* per archetype
  4. Intra-archetype classification accuracy and macro-F1 across shrinkage values
  5. Full hierarchical MorphoPath-Edge accuracy under various shrinkage configurations
================================================================================
"""

import sys
from pathlib import Path
import json
import numpy as np
import torch
import torch.nn.functional as F
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, f1_score

PROJECT_ROOT = Path("E:/work/research-few-shot")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

EXP_DIR = PROJECT_ROOT / "experiments" / "phase1_morphopath"
CACHE_FILE = EXP_DIR / "plantdoc_features_seed42.pt"

ARCHETYPE_MAP = {
    'Tomato_Early_blight_leaf': 0, 'Tomato_Septoria_leaf_spot': 0, 'Tomato_leaf': 0,
    'Tomato_leaf_bacterial_spot': 0, 'Tomato_leaf_late_blight': 0, 'Tomato_leaf_mosaic_virus': 0,
    'Tomato_leaf_yellow_virus': 0, 'Tomato_mold_leaf': 0,
    'Potato_leaf_early_blight': 0, 'Potato_leaf_late_blight': 0,
    'grape_leaf': 1, 'grape_leaf_black_rot': 1, 'Squash_Powdery_mildew_leaf': 1,
    'Corn_Gray_leaf_spot': 2, 'Corn_leaf_blight': 2, 'Corn_rust_leaf': 2,
    'Apple_Scab_Leaf': 3, 'Apple_leaf': 3, 'Apple_rust_leaf': 3,
    'Bell_pepper_leaf': 3, 'Bell_pepper_leaf_spot': 3,
    'Blueberry_leaf': 3, 'Cherry_leaf': 3, 'Peach_leaf': 3,
    'Raspberry_leaf': 3, 'Soyabean_leaf': 3, 'Strawberry_leaf': 3
}

ARCHETYPE_NAMES = [
    "A1: Solanoid (10 classes)",
    "A2: Vitoid/Cucurbit (3 classes)",
    "A3: Pooid (3 classes)",
    "A4: Rosoid/Other (11 classes)"
]

def compute_within_class_cov(X: np.ndarray, y: np.ndarray):
    """Computes pooled within-class covariance matrix and its condition number."""
    classes = np.unique(y)
    N, D = X.shape
    K = len(classes)
    Sw = np.zeros((D, D), dtype=np.float64)
    for c in classes:
        Xc = X[y == c]
        mean_c = Xc.mean(axis=0, keepdims=True)
        diff = Xc - mean_c
        Sw += diff.T @ diff
    Sw /= max(1, N - K)
    return Sw

def condition_number(cov: np.ndarray):
    """Computes condition number of a covariance matrix."""
    s = np.linalg.svd(cov, compute_uv=False)
    s_max = s[0]
    s_min = s[-1]
    if s_min <= 1e-12:
        return float("inf")
    return float(s_max / s_min)

def evaluate_idea007():
    print("=" * 80)
    print("IDEA-007: Adaptive Covariance Shrinkage & Archetype Regularization")
    print("=" * 80)

    data = torch.load(CACHE_FILE, map_location="cpu")
    sup_bio = data["support_bioclip"].float().numpy()
    sup_dino = data["support_dino"].float().numpy()
    sup_labels = data["support_labels"].numpy()

    qry_bio = data["query_bioclip"].float().numpy()
    qry_dino = data["query_dino"].float().numpy()
    qry_labels = data["query_labels"].numpy()

    class_names = data["class_names"]
    n_classes = len(class_names)
    n_queries = len(qry_labels)

    class_to_arch = np.array([ARCHETYPE_MAP[c] for c in class_names])
    sup_arch = class_to_arch[sup_labels]
    qry_arch_true = class_to_arch[qry_labels]

    sup_joint = np.concatenate([sup_bio, sup_dino], axis=-1)
    qry_joint = np.concatenate([qry_bio, qry_dino], axis=-1)
    D = sup_joint.shape[-1] # 896

    # DINOv2 Archetype Router
    arch_protos_dino = np.stack([sup_dino[sup_arch == a].mean(axis=0) for a in range(4)])
    arch_protos_dino /= (np.linalg.norm(arch_protos_dino, axis=-1, keepdims=True) + 1e-12)
    qry_dino_norm = qry_dino / (np.linalg.norm(qry_dino, axis=-1, keepdims=True) + 1e-12)
    pred_arch_router = (qry_dino_norm @ arch_protos_dino.T).argmax(axis=-1)

    # 1. Inspect unregularized covariance condition number
    print(f"\n[1] Within-Class Covariance Ill-Conditioning (D={D}):")
    arch_data = {}
    for a_idx in range(4):
        a_classes = np.where(class_to_arch == a_idx)[0]
        a_sup_mask = (sup_arch == a_idx)
        local_map = {c: i for i, c in enumerate(a_classes)}
        y_loc = np.array([local_map[y] for y in sup_labels[a_sup_mask]])
        X_loc = sup_joint[a_sup_mask]

        Sw = compute_within_class_cov(X_loc, y_loc)
        cond_raw = condition_number(Sw)
        rank_raw = np.linalg.matrix_rank(Sw)
        
        trace_sw = float(np.trace(Sw) / D)
        # Check Ledoit-Wolf shrinkage fitted covariance
        clf_lw = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(X_loc, y_loc)
        cond_lw = condition_number(clf_lw.covariance_)

        # Also calculate the exact ledoit-wolf shrinkage intensity on standardized within-class residuals
        from sklearn.covariance import ledoit_wolf
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_res = np.zeros_like(X_loc)
        for c in np.unique(y_loc):
            c_mask = (y_loc == c)
            X_res[c_mask] = X_loc[c_mask] - X_loc[c_mask].mean(axis=0, keepdims=True)
        _, lambda_lw = ledoit_wolf(sc.fit_transform(X_res))

        arch_data[a_idx] = {
            "name": ARCHETYPE_NAMES[a_idx],
            "n_classes": len(a_classes),
            "n_support": int(len(X_loc)),
            "n_queries": int(np.sum(qry_arch_true == a_idx)),
            "X_loc": X_loc,
            "y_loc": y_loc,
            "Sw": Sw,
            "trace_sw": trace_sw,
            "cond_raw": cond_raw,
            "rank_raw": int(rank_raw),
            "lambda_lw": lambda_lw,
            "cond_lw": cond_lw,
            "classes": a_classes
        }

        print(f"  * {ARCHETYPE_NAMES[a_idx]}:")
        print(f"      Support samples: N={len(X_loc)}, Dim: D={D}, Rank: {rank_raw}/{D}")
        print(f"      Empirical condition number kappa: {cond_raw:.2e} (Strictly Singular!)")
        print(f"      Ledoit-Wolf optimal lambda*: {lambda_lw:.4f} -> Shrunk kappa: {cond_lw:.2f}")

    # 2. Parameter Sweep: Fixed Shrinkage vs Ledoit-Wolf
    shrinkage_grid = [0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]
    results_sweep = {}

    print("\n[2] Shrinkage Sweep (Intra-Archetype Oracle & Full Pipeline):")
    print(f"{'Shrinkage':<12} | {'A1 Solanoid':<14} | {'A2 Vitoid':<14} | {'A3 Pooid':<14} | {'A4 Rosoid':<14} | {'Oracle Mean':<12} | {'Hierarchical':<12}")
    print("-" * 96)

    for shrinkage_val in shrinkage_grid + ["auto", "archetype_adaptive"]:
        intra_accs = []
        preds_oracle = np.zeros(n_queries, dtype=int)
        preds_hier = np.zeros(n_queries, dtype=int)

        for a_idx in range(4):
            info = arch_data[a_idx]
            X_loc, y_loc, a_classes = info["X_loc"], info["y_loc"], info["classes"]
            q_mask_oracle = (qry_arch_true == a_idx)
            q_mask_router = (pred_arch_router == a_idx)

            if shrinkage_val == "auto":
                clf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto").fit(X_loc, y_loc)
            elif shrinkage_val == "archetype_adaptive":
                # Adaptive formula: lambda = D / (D + N_eff)
                # D=896; for N=400 (Solanoid) -> ~0.69; for N=120 (Vitoid/Pooid) -> ~0.88; for N=440 (Rosoid) -> ~0.67
                N_supp = len(X_loc)
                lambda_adapt = float(np.clip(D / (D + 0.5 * N_supp), 0.1, 0.95))
                clf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=lambda_adapt).fit(X_loc, y_loc)
            else:
                clf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=shrinkage_val).fit(X_loc, y_loc)

            # Oracle query prediction
            if np.sum(q_mask_oracle) > 0:
                p_loc = clf.predict(qry_joint[q_mask_oracle])
                preds_oracle[q_mask_oracle] = a_classes[p_loc]
                acc_a = float(accuracy_score(qry_labels[q_mask_oracle], a_classes[p_loc]) * 100.0)
            else:
                acc_a = 0.0
            intra_accs.append(acc_a)

            # Hierarchical router prediction
            if np.sum(q_mask_router) > 0:
                p_hier_loc = clf.predict(qry_joint[q_mask_router])
                preds_hier[q_mask_router] = a_classes[p_hier_loc]

        acc_oracle_mean = float(accuracy_score(qry_labels, preds_oracle) * 100.0)
        acc_hier = float(accuracy_score(qry_labels, preds_hier) * 100.0)
        f1_hier = float(f1_score(qry_labels, preds_hier, average="macro") * 100.0)

        s_label = f"lambda={shrinkage_val}" if isinstance(shrinkage_val, float) else str(shrinkage_val)
        print(f"{s_label:<12} | {intra_accs[0]:>5.2f}%        | {intra_accs[1]:>5.2f}%        | {intra_accs[2]:>5.2f}%        | {intra_accs[3]:>5.2f}%        | {acc_oracle_mean:>5.2f}%       | {acc_hier:>5.2f}%")

        results_sweep[s_label] = {
            "intra_solanoid": intra_accs[0],
            "intra_vitoid": intra_accs[1],
            "intra_pooid": intra_accs[2],
            "intra_rosoid": intra_accs[3],
            "oracle_overall": acc_oracle_mean,
            "hierarchical_acc": acc_hier,
            "hierarchical_macro_f1": f1_hier
        }

    # Summary analysis
    best_fixed = max(
        [(k, v["hierarchical_acc"]) for k, v in results_sweep.items() if k.startswith("lambda=")],
        key=lambda x: x[1]
    )
    print("\n[3] Empirical Summary:")
    print(f"  * Best Fixed Shrinkage: {best_fixed[0]} with Hierarchical Acc = {best_fixed[1]:.2f}%")
    print(f"  * Ledoit-Wolf ('auto'): Hierarchical Acc = {results_sweep['auto']['hierarchical_acc']:.2f}% | Oracle = {results_sweep['auto']['oracle_overall']:.2f}%")
    print(f"  * Archetype-Adaptive:   Hierarchical Acc = {results_sweep['archetype_adaptive']['hierarchical_acc']:.2f}% | Oracle = {results_sweep['archetype_adaptive']['oracle_overall']:.2f}%")

    out_file = EXP_DIR / "idea007_covariance_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "archetype_cov_properties": {
                a: {
                    "name": arch_data[a]["name"],
                    "n_classes": int(arch_data[a]["n_classes"]),
                    "n_support": int(arch_data[a]["n_support"]),
                    "rank": int(arch_data[a]["rank_raw"]),
                    "empirical_cond": "inf" if np.isinf(arch_data[a]["cond_raw"]) else float(arch_data[a]["cond_raw"]),
                    "ledoit_wolf_lambda": float(arch_data[a]["lambda_lw"]),
                    "ledoit_wolf_cond": float(arch_data[a]["cond_lw"])
                } for a in range(4)
            },
            "sweep": results_sweep,
            "best_fixed": best_fixed[0],
            "best_fixed_acc": float(best_fixed[1]),
            "status": "validated" if results_sweep['auto']['hierarchical_acc'] > 46.0 else "rejected"
        }, f, indent=2)
    print(f"[OK] Saved results to {out_file}")

if __name__ == "__main__":
    evaluate_idea007()

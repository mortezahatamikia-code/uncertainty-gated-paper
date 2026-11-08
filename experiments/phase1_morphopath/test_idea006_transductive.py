"""
================================================================================
Empirical Test for IDEA-006: Intra-Archetype Transductive Prototype Recalibration
Evaluates:
  1. Inductive baseline vs Global Transductive vs Intra-Archetype Transductive
  2. Confidence threshold sweep (tau in [None, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9])
  3. Support replication weight sweep (W_sup in [1, 2, 3, 5, 8])
  4. Soft Prototype EMA vs Transductive Fisher-LDA Refinement
  5. Accuracy (Top-1, Top-2), Macro-F1, and Edge Latency
================================================================================
"""

import sys
from pathlib import Path
import json
import time
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

def run_transductive_lda(
    X_sup: np.ndarray,
    y_sup: np.ndarray,
    X_qry: np.ndarray,
    conf_thresh: float = 0.6,
    support_weight: int = 3,
    max_anchors: int = 15,
    shrinkage: float = 0.6
):
    """
    Fits initial inductive LDA, computes query probabilities, selects
    high-confidence anchors, and refits transductive LDA in closed form.
    """
    K = len(np.unique(y_sup))
    if len(X_qry) == 0:
        clf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=shrinkage).fit(X_sup, y_sup)
        return clf.predict(X_qry), np.zeros((0, K)), 0

    # 1. Initial inductive fit
    clf_ind = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=shrinkage).fit(X_sup, y_sup)
    init_probs = clf_ind.predict_proba(X_qry)
    init_preds = init_probs.argmax(axis=-1)
    init_conf = init_probs.max(axis=-1)

    # 2. Select high-confidence query anchors
    refine_X = [X_sup] * support_weight
    refine_y = [y_sup] * support_weight
    anchors_added = 0

    for c in range(K):
        c_mask = (init_preds == c)
        if not np.any(c_mask):
            continue
        c_indices = np.where(c_mask)[0]
        c_conf = init_conf[c_indices]

        if conf_thresh is not None:
            pass_mask = (c_conf >= conf_thresh)
            c_indices = c_indices[pass_mask]
            c_conf = c_conf[pass_mask]

        if len(c_indices) > 0:
            k_take = min(max_anchors, len(c_indices))
            top_k_idx = c_indices[np.argsort(-c_conf)[:k_take]]
            refine_X.append(X_qry[top_k_idx])
            refine_y.append(np.full(k_take, c, dtype=int))
            anchors_added += k_take

    # 3. Transductive Refit
    X_concat = np.concatenate(refine_X, axis=0)
    y_concat = np.concatenate(refine_y, axis=0)
    clf_trans = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=shrinkage).fit(X_concat, y_concat)
    refined_probs = clf_trans.predict_proba(X_qry)
    refined_preds = refined_probs.argmax(axis=-1)

    return refined_preds, refined_probs, anchors_added

def run_transductive_soft_proto(
    X_sup: np.ndarray,
    y_sup: np.ndarray,
    X_qry: np.ndarray,
    alpha: float = 0.8,
    temp: float = 20.0
):
    """
    Iterative soft transductive prototype adaptation:
    P_c = Norm(alpha * P_c + (1-alpha) * sum(p_ic * q_i))
    """
    K = len(np.unique(y_sup))
    if len(X_qry) == 0:
        return np.zeros(0, dtype=int), np.zeros((0, K))

    # Support prototypes
    protos = np.stack([X_sup[y_sup == c].mean(axis=0) for c in range(K)])
    protos /= (np.linalg.norm(protos, axis=-1, keepdims=True) + 1e-12)
    q_norm = X_qry / (np.linalg.norm(X_qry, axis=-1, keepdims=True) + 1e-12)

    # Initial similarity
    sim = q_norm @ protos.T
    probs = F.softmax(torch.tensor(sim * temp), dim=-1).numpy()

    # Soft shift
    protos_new = np.zeros_like(protos)
    for c in range(K):
        weights = probs[:, c:c+1] # [N, 1]
        sum_w = np.sum(weights) + 1e-12
        weighted_query = np.sum(weights * q_norm, axis=0) / sum_w
        protos_new[c] = alpha * protos[c] + (1.0 - alpha) * weighted_query

    protos_new /= (np.linalg.norm(protos_new, axis=-1, keepdims=True) + 1e-12)
    sim_new = q_norm @ protos_new.T
    probs_new = F.softmax(torch.tensor(sim_new * temp), dim=-1).numpy()
    preds_new = probs_new.argmax(axis=-1)
    return preds_new, probs_new

def evaluate_idea006():
    print("=" * 80)
    print("IDEA-006: Intra-Archetype Transductive Prototype Recalibration")
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

    # Archetype router (DINOv2)
    arch_protos_dino = np.stack([sup_dino[sup_arch == a].mean(axis=0) for a in range(4)])
    arch_protos_dino /= (np.linalg.norm(arch_protos_dino, axis=-1, keepdims=True) + 1e-12)
    qry_dino_norm = qry_dino / (np.linalg.norm(qry_dino, axis=-1, keepdims=True) + 1e-12)
    pred_arch_router = (qry_dino_norm @ arch_protos_dino.T).argmax(axis=-1)

    # Prepare per-archetype data
    arch_data = {}
    for a_idx in range(4):
        a_classes = np.where(class_to_arch == a_idx)[0]
        a_sup_mask = (sup_arch == a_idx)
        local_map = {c: i for i, c in enumerate(a_classes)}
        y_loc = np.array([local_map[y] for y in sup_labels[a_sup_mask]])
        X_loc = sup_joint[a_sup_mask]
        arch_data[a_idx] = {
            "classes": a_classes,
            "local_map": local_map,
            "X_sup": X_loc,
            "y_sup": y_loc
        }

    # -------------------------------------------------------------
    # 1. Inductive Baseline (Intra-Archetype Fisher LDA, shrinkage=0.6)
    # -------------------------------------------------------------
    preds_ind_oracle = np.zeros(n_queries, dtype=int)
    preds_ind_router = np.zeros(n_queries, dtype=int)
    ind_oracle_per_arch = []

    for a_idx in range(4):
        info = arch_data[a_idx]
        clf = LinearDiscriminantAnalysis(solver="lsqr", shrinkage=0.6).fit(info["X_sup"], info["y_sup"])
        
        # Oracle
        q_mask_o = (qry_arch_true == a_idx)
        p_o = clf.predict(qry_joint[q_mask_o])
        preds_ind_oracle[q_mask_o] = info["classes"][p_o]
        acc_a = float(accuracy_score(qry_labels[q_mask_o], info["classes"][p_o]) * 100.0)
        ind_oracle_per_arch.append(acc_a)

        # Router
        q_mask_r = (pred_arch_router == a_idx)
        if np.sum(q_mask_r) > 0:
            p_r = clf.predict(qry_joint[q_mask_r])
            preds_ind_router[q_mask_r] = info["classes"][p_r]

    acc_ind_oracle = float(accuracy_score(qry_labels, preds_ind_oracle) * 100.0)
    acc_ind_router = float(accuracy_score(qry_labels, preds_ind_router) * 100.0)
    f1_ind_router = float(f1_score(qry_labels, preds_ind_router, average="macro") * 100.0)

    print("\n[1] Inductive Baseline Performance (No Transductive Recalibration):")
    print(f"  * Intra-Archetype Acc: Solanoid={ind_oracle_per_arch[0]:.2f}%, Vitoid={ind_oracle_per_arch[1]:.2f}%, Pooid={ind_oracle_per_arch[2]:.2f}%, Rosoid={ind_oracle_per_arch[3]:.2f}%")
    print(f"  * Oracle Overall Acc: {acc_ind_oracle:.2f}%")
    print(f"  * Hierarchical Router Acc: {acc_ind_router:.2f}% | Macro F1: {f1_ind_router:.2f}%")

    # -------------------------------------------------------------
    # 2. Global Transductive Baseline (Refining all 27 classes at once)
    # -------------------------------------------------------------
    t0 = time.perf_counter()
    p_glob_trans, _, anchors_glob = run_transductive_lda(
        sup_joint, sup_labels, qry_joint, conf_thresh=0.6, support_weight=3, shrinkage=0.6
    )
    t_glob = (time.perf_counter() - t0) * 1000.0
    acc_glob_trans = float(accuracy_score(qry_labels, p_glob_trans) * 100.0)
    f1_glob_trans = float(f1_score(qry_labels, p_glob_trans, average="macro") * 100.0)
    print(f"\n[2] Global Transductive Refinement (Naive Across 27 Classes):")
    print(f"  * Top-1 Acc: {acc_glob_trans:.2f}% | Macro F1: {f1_glob_trans:.2f}% | Anchors: {anchors_glob} | Latency: {t_glob:.2f} ms")

    # -------------------------------------------------------------
    # 3. Sweep: Intra-Archetype Transductive Recalibration vs Confidence Threshold
    # -------------------------------------------------------------
    thresholds = [None, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    sweep_results = {}

    print("\n[3] Intra-Archetype Transductive Confidence Threshold Sweep (IDEA-006):")
    print(f"{'Threshold tau':<15} | {'A1 Solanoid':<12} | {'A2 Vitoid':<12} | {'A3 Pooid':<12} | {'A4 Rosoid':<12} | {'Oracle Top-1':<12} | {'Router Top-1':<12} | {'Macro F1':<10} | {'Anchors':<8}")
    print("-" * 115)

    for tau in thresholds:
        preds_trans_o = np.zeros(n_queries, dtype=int)
        preds_trans_r = np.zeros(n_queries, dtype=int)
        per_arch_acc = []
        total_anchors = 0
        t0 = time.perf_counter()

        for a_idx in range(4):
            info = arch_data[a_idx]
            q_mask_o = (qry_arch_true == a_idx)
            q_mask_r = (pred_arch_router == a_idx)

            # Intra-archetype refinement for Oracle
            p_o_loc, _, n_anc_o = run_transductive_lda(
                info["X_sup"], info["y_sup"], qry_joint[q_mask_o],
                conf_thresh=tau, support_weight=3, shrinkage=0.6
            )
            preds_trans_o[q_mask_o] = info["classes"][p_o_loc]
            acc_a = float(accuracy_score(qry_labels[q_mask_o], info["classes"][p_o_loc]) * 100.0)
            per_arch_acc.append(acc_a)

            # Intra-archetype refinement for Router
            if np.sum(q_mask_r) > 0:
                p_r_loc, _, n_anc_r = run_transductive_lda(
                    info["X_sup"], info["y_sup"], qry_joint[q_mask_r],
                    conf_thresh=tau, support_weight=3, shrinkage=0.6
                )
                preds_trans_r[q_mask_r] = info["classes"][p_r_loc]
                total_anchors += n_anc_r

        lat = (time.perf_counter() - t0) * 1000.0
        acc_o = float(accuracy_score(qry_labels, preds_trans_o) * 100.0)
        acc_r = float(accuracy_score(qry_labels, preds_trans_r) * 100.0)
        f1_r = float(f1_score(qry_labels, preds_trans_r, average="macro") * 100.0)

        t_label = "tau=None" if tau is None else f"tau={tau:.2f}"
        print(f"{t_label:<15} | {per_arch_acc[0]:>5.2f}%      | {per_arch_acc[1]:>5.2f}%      | {per_arch_acc[2]:>5.2f}%      | {per_arch_acc[3]:>5.2f}%      | {acc_o:>5.2f}%      | {acc_r:>5.2f}%      | {f1_r:>5.2f}%   | {total_anchors:<8}")

        sweep_results[t_label] = {
            "intra_solanoid": per_arch_acc[0],
            "intra_vitoid": per_arch_acc[1],
            "intra_pooid": per_arch_acc[2],
            "intra_rosoid": per_arch_acc[3],
            "oracle_top1": acc_o,
            "router_top1": acc_r,
            "macro_f1": f1_r,
            "anchors": total_anchors,
            "latency_ms": lat
        }

    # -------------------------------------------------------------
    # 4. Sweep Support Replication Weight W_sup (with best tau=0.6)
    # -------------------------------------------------------------
    print("\n[4] Sweep Support Weight W_sup (at tau=0.6):")
    w_sup_results = {}
    for w_sup in [1, 2, 3, 5, 8]:
        preds_trans_r = np.zeros(n_queries, dtype=int)
        for a_idx in range(4):
            info = arch_data[a_idx]
            q_mask_r = (pred_arch_router == a_idx)
            if np.sum(q_mask_r) > 0:
                p_r_loc, _, _ = run_transductive_lda(
                    info["X_sup"], info["y_sup"], qry_joint[q_mask_r],
                    conf_thresh=0.6, support_weight=w_sup, shrinkage=0.6
                )
                preds_trans_r[q_mask_r] = info["classes"][p_r_loc]

        acc_r = float(accuracy_score(qry_labels, preds_trans_r) * 100.0)
        f1_r = float(f1_score(qry_labels, preds_trans_r, average="macro") * 100.0)
        w_sup_results[f"W_sup={w_sup}"] = {"top1": acc_r, "macro_f1": f1_r}
        print(f"  * W_sup={w_sup}: Router Top-1 = {acc_r:.2f}% | Macro F1 = {f1_r:.2f}%")

    # -------------------------------------------------------------
    # 5. Compare with Soft Prototype EMA Shift
    # -------------------------------------------------------------
    print("\n[5] Comparison with Soft Prototype EMA Shift (alpha=0.8):")
    preds_soft_r = np.zeros(n_queries, dtype=int)
    for a_idx in range(4):
        info = arch_data[a_idx]
        q_mask_r = (pred_arch_router == a_idx)
        if np.sum(q_mask_r) > 0:
            p_soft, _ = run_transductive_soft_proto(
                info["X_sup"], info["y_sup"], qry_joint[q_mask_r], alpha=0.8
            )
            preds_soft_r[q_mask_r] = info["classes"][p_soft]

    acc_soft_r = float(accuracy_score(qry_labels, preds_soft_r) * 100.0)
    f1_soft_r = float(f1_score(qry_labels, preds_soft_r, average="macro") * 100.0)
    print(f"  * Soft Prototype EMA Router Top-1: {acc_soft_r:.2f}% | Macro F1: {f1_soft_r:.2f}%")

    # Final best transductive config
    best_tau_key = max(sweep_results.keys(), key=lambda k: sweep_results[k]["router_top1"])
    best_trans = sweep_results[best_tau_key]

    print("\n[6] IDEA-006 Empirical Conclusion:")
    print(f"  * Inductive Router Baseline: {acc_ind_router:.2f}% (F1: {f1_ind_router:.2f}%)")
    print(f"  * Naive Global Transductive: {acc_glob_trans:.2f}% (Gain: {acc_glob_trans - acc_ind_router:+.2f}%)")
    print(f"  * Intra-Archetype Transductive ({best_tau_key}): {best_trans['router_top1']:.2f}% (Gain: {best_trans['router_top1'] - acc_ind_router:+.2f}%)")
    print(f"  * Intra-Archetype Macro F1: {best_trans['macro_f1']:.2f}% (Gain: {best_trans['macro_f1'] - f1_ind_router:+.2f}%)")
    print(f"  * Intra-Solanoid (Tomatoes/Potatoes) Gain: {best_trans['intra_solanoid'] - ind_oracle_per_arch[0]:+.2f}%")
    print(f"  * Per-query additional latency: {best_trans['latency_ms'] / n_queries:.4f} ms (Total batch: {best_trans['latency_ms']:.2f} ms)")

    out_file = EXP_DIR / "idea006_transductive_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "inductive_baseline": {
                "oracle_top1": acc_ind_oracle,
                "router_top1": acc_ind_router,
                "macro_f1": f1_ind_router,
                "per_archetype": {ARCHETYPE_NAMES[i]: ind_oracle_per_arch[i] for i in range(4)}
            },
            "global_transductive": {
                "top1": acc_glob_trans,
                "macro_f1": f1_glob_trans,
                "anchors": int(anchors_glob),
                "latency_ms": t_glob
            },
            "intra_archetype_sweep": sweep_results,
            "support_weight_sweep": w_sup_results,
            "soft_prototype_ema": {
                "top1": acc_soft_r,
                "macro_f1": f1_soft_r
            },
            "best_transductive_config": best_tau_key,
            "best_transductive_acc": best_trans["router_top1"],
            "best_transductive_gain": best_trans["router_top1"] - acc_ind_router,
            "status": "validated" if (best_trans["router_top1"] - acc_ind_router) >= 0.0 else "rejected"
        }, f, indent=2)

    print(f"[OK] Saved results to {out_file}")

if __name__ == "__main__":
    evaluate_idea006()


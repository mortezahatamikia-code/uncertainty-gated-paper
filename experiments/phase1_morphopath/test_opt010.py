"""
Experiment script for TASK-OPT-010: Hierarchical Fast-Exit Decision Cascade (IDEA-016)
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import numpy as np
from sklearn.metrics import accuracy_score, f1_score

from pipeline.morphopath_engine import (
    MorphoPathEngine,
    l2_normalize,
    tukey_power_transform,
    center_and_normalize,
    softmax_prob,
    is_healthy_leaf_name,
    build_morphopath_output,
)
from pipeline.canopy_suppressor import CanopyClutterGlareSuppressor
from experiments.phase1_morphopath.benchmark_phase4_advanced import (
    load_plantdoc_seed42,
    load_plantvillage_pool,
)


def run_fast_exit_experiment():
    print("=" * 80)
    print("TASK-OPT-010: Hierarchical Fast-Exit Decision Cascade")
    print("=" * 80)
    pd_data = load_plantdoc_seed42()
    class_names = pd_data["class_names"]
    n_classes = len(class_names)
    
    sup_joint = np.concatenate([pd_data["sup_bio"], pd_data["sup_dino"]], axis=-1)
    qry_joint = np.concatenate([pd_data["qry_bio"], pd_data["qry_dino"]], axis=-1)
    qry_bio = pd_data["qry_bio"]
    qry_dino = pd_data["qry_dino"]
    qry_labels = pd_data["qry_labels"]
    micro_protos = pd_data["micro_protos"]
    
    engine = MorphoPathEngine(
        bioclip_dim=512, dinov2_dim=384, shrinkage=0.60, router_temp=12.0, vis_temp=15.0,
        text_temp=30.0, w_vis=0.75, margin_penalty=0.05, w_bio=0.65,
        penalized_classes=["Potato_leaf_late_blight"], micro_prototypes=micro_protos,
        class_names=class_names, enable_clutter_suppression=True, gamma_glare=0.15, threshold_glare=0.06,
    ).fit(sup_joint, pd_data["sup_labels"])
    
    # Baseline full forward pass metrics
    m_base = engine.evaluate(qry_joint, qry_labels)
    print(f"Full Deep Path Baseline: Top-1={m_base['accuracy_top1']:.2f}%, Top-2={m_base['accuracy_top2']:.2f}%, F1={m_base['macro_f1']:.2f}%, FPR={m_base['fpr']:.2f}%")
    
    # Fast exit simulation
    # In fast-path, visual softmax alone is computed.
    # If p1 > tau_conf and (p1 - p2) > tau_margin, fast exit!
    # Else, continue to full deep path (micro-symptom fusion + clutter suppression).
    
    n_queries = len(qry_labels)
    healthy_idx = set(i for i, c in enumerate(class_names) if is_healthy_leaf_name(c))
    diseased_mask = np.array([y not in healthy_idx for y in qry_labels])
    healthy_mask = np.array([y in healthy_idx for y in qry_labels])
    
    # Test grid of thresholds
    threshold_pairs = [
        (0.70, 0.30),
        (0.75, 0.35),
        (0.80, 0.40),
        (0.85, 0.45),
        (0.88, 0.45),
        (0.90, 0.50),
        (0.92, 0.55),
        (0.95, 0.60),
    ]
    
    print("\n--- Evaluating Fast-Exit Decision Thresholds on PlantDoc ---")
    for t_conf, t_margin in threshold_pairs:
        # Step 1: Visual similarity
        qb, qd = tukey_power_transform(qry_bio), tukey_power_transform(qry_dino)
        qbc, _ = center_and_normalize(qb)
        qdc, _ = center_and_normalize(qd)
        sims_rect = 0.65 * (qbc @ engine.protos_bio_rect.T) + 0.35 * (qdc @ engine.protos_dino_rect.T)
        
        sims_rect_margin = sims_rect.copy()
        if engine.penalized_indices:
            sims_rect_margin[:, engine.penalized_indices] -= engine.margin_penalty
        p_vis = softmax_prob(sims_rect_margin, temp=engine.vis_temp)
        
        # Rank visual probabilities
        ranked_vis = np.argsort(-p_vis, axis=-1)
        p1 = p_vis[np.arange(n_queries), ranked_vis[:, 0]]
        p2 = p_vis[np.arange(n_queries), ranked_vis[:, 1]]
        margin = p1 - p2
        
        fast_exit_mask = (p1 >= t_conf) & (margin >= t_margin)
        fast_ratio = float(np.mean(fast_exit_mask) * 100.0)
        
        # Deep path for remaining queries
        p_final = p_vis.copy()
        if not np.all(fast_exit_mask):
            ambiguous_idx = np.where(~fast_exit_mask)[0]
            # Execute text fusion and clutter suppression on ambiguous queries
            p_txt = softmax_prob(l2_normalize(qry_bio[ambiguous_idx]) @ l2_normalize(micro_protos).T, temp=30.0)
            p_comb_amb = 0.75 * p_vis[ambiguous_idx] + 0.25 * p_txt
            p_comb_amb, _ = engine.suppressor.modulate_probabilities(
                p_comb_amb, qry_bio[ambiguous_idx], class_names
            )
            p_final[ambiguous_idx] = p_comb_amb
            
        top1 = p_final.argmax(axis=-1)
        top2 = np.argsort(p_final, axis=-1)[:, -2:]
        top2_acc = np.mean([qry_labels[i] in top2[i] for i in range(len(qry_labels))]) * 100.0
        acc = accuracy_score(qry_labels, top1) * 100.0
        f1 = f1_score(qry_labels, top1, average="macro", zero_division=0) * 100.0
        pred_healthy = np.array([y in healthy_idx for y in top1])
        fnr = float(np.sum(diseased_mask & pred_healthy) / max(1, np.sum(diseased_mask)) * 100.0)
        fpr = float(np.sum(healthy_mask & ~pred_healthy) / max(1, np.sum(healthy_mask)) * 100.0)
        
        print(f"  t_conf={t_conf:.2f}, t_margin={t_margin:.2f} | Fast-Exit={fast_ratio:5.1f}% | Top-1={acc:.2f}%, Top-2={top2_acc:.2f}%, F1={f1:.2f}%, FPR={fpr:.2f}%")

    # Now let's profile single-query CPU latency!
    print("\n--- Latency Profiling (1000 single query runs) ---")
    single_q = qry_joint[:1]
    
    # 1. Baseline Full Pass
    latencies_base = []
    for _ in range(100):
        _ = engine.forward(single_q)
    for _ in range(1000):
        t0 = time.perf_counter()
        _ = engine.forward(single_q)
        latencies_base.append((time.perf_counter() - t0) * 1000.0)
        
    mean_base = float(np.mean(latencies_base))
    p50_base = float(np.percentile(latencies_base, 50))
    p95_base = float(np.percentile(latencies_base, 95))
    print(f"  Baseline Full Head Latency: mean={mean_base:.4f} ms, p50={p50_base:.4f} ms, p95={p95_base:.4f} ms (Throughput: {1000.0/mean_base:.1f} FPS)")
    
    # Fast exit function
    def forward_fast_exit(q_joint, t_conf=0.88, t_margin=0.45):
        q_bio, q_dino = q_joint[:, :512], q_joint[:, 512:]
        # Router
        p_arch = softmax_prob(l2_normalize(q_dino) @ engine.arch_protos_dino.T, temp=engine.router_temp)
        pred_arch = p_arch.argmax(axis=-1)
        # Visual
        qb, qd = tukey_power_transform(q_bio), tukey_power_transform(q_dino)
        qbc, _ = center_and_normalize(qb)
        qdc, _ = center_and_normalize(qd)
        sims_rect = 0.65 * (qbc @ engine.protos_bio_rect.T) + 0.35 * (qdc @ engine.protos_dino_rect.T)
        sims_m = sims_rect.copy()
        if engine.penalized_indices:
            sims_m[:, engine.penalized_indices] -= engine.margin_penalty
        p_vis = softmax_prob(sims_m, temp=engine.vis_temp)
        
        # Check fast exit
        ranked = np.argsort(-p_vis, axis=-1)
        p1 = p_vis[0, ranked[0, 0]]
        p2 = p_vis[0, ranked[0, 1]]
        if p1 >= t_conf and (p1 - p2) >= t_margin:
            # Fast exit!
            return build_morphopath_output(sims_rect, p_vis, pred_arch, p_arch, class_names, n_classes)
        # Deep path
        p_txt = softmax_prob(l2_normalize(q_bio) @ l2_normalize(micro_protos).T, temp=30.0)
        p_comb = 0.75 * p_vis + 0.25 * p_txt
        p_comb, diag = engine.suppressor.modulate_probabilities(p_comb, q_bio, class_names)
        return build_morphopath_output(sims_rect, p_comb, pred_arch, p_arch, class_names, n_classes, diag, diag.glare_score)

    latencies_fast = []
    for _ in range(100):
        _ = forward_fast_exit(single_q)
    for _ in range(1000):
        t0 = time.perf_counter()
        _ = forward_fast_exit(single_q)
        latencies_fast.append((time.perf_counter() - t0) * 1000.0)
        
    mean_fast = float(np.mean(latencies_fast))
    p50_fast = float(np.percentile(latencies_fast, 50))
    p95_fast = float(np.percentile(latencies_fast, 95))
    print(f"  Fast-Exit Head Latency:     mean={mean_fast:.4f} ms, p50={p50_fast:.4f} ms, p95={p95_fast:.4f} ms (Throughput: {1000.0/mean_fast:.1f} FPS)")
    print(f"  Speedup on Decision Head:   {(mean_base - mean_fast)/mean_base * 100.0:.1f}% reduction in latency!")


if __name__ == "__main__":
    run_fast_exit_experiment()


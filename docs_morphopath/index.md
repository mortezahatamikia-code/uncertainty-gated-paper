# 🌿 MorphoPath-Edge: Autonomous Zero-Parameter Dual Foliar Inference Documentation

Welcome to the official technical documentation for **MorphoPath-Edge** (Paper 2):  
*“MorphoPath-Edge: Autonomous Foliar Pathology Routing via Decoupled Macro-Archetypes and Zero-Parameter Test-Time Manifold Rectification for Real-Time Edge Diagnostics.”*

---

## 📌 Executive Summary

MorphoPath-Edge is an autonomous, biologically grounded, zero-parameter few-shot foliar diagnostic framework engineered for unconstrained field conditions and extreme resource-constrained mobile hardware. It addresses the catastrophic vulnerability of prior botanical few-shot classifiers—namely, their reliance on error-prone cultigen-level routing or grower species identification, uncalibrated domain shift under field lighting, and intra-host pathological feature collapse.

```
+---------------------------------------------------------------------------------------------------+
|                                 MORPHOPATH-EDGE ARCHITECTURE                                      |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  Live Field Image                                                                                 |
|         │                                                                                         |
|         ├───────────────────────────────┬───────────────────────────────┐                         |
|         ▼                               ▼                               ▼                         |
|  DINOv2 ViT-S/14               BioCLIP ViT-B/16             Canopy Clutter & Glare                |
|  (384-d Geometry)              (512-d Pathology)            Suppressor (Zero-Param)               |
|         │                               │                               │                         |
|         ▼                               ▼                               ▼                         |
|  Tukey Power Rectification     Tukey Power Rectification     Negative Abiotic Protos              |
|  (z = sign(x)*|x|^0.5)         (z = sign(x)*|x|^0.5)         (Solar Flare, Void, Mulch)           |
|         │                               │                               │                         |
|         ▼                               ▼                               │                         |
|  Macro-Archetype Router        Decoupled Weighting ($w=0.65$)           │                         |
|  (Solanoid, Vitoid,            Cross-Subspace Bilinear Gating           │                         |
|   Pooid, Rosoid)               Gegenbauer Spherical Decrowding          │                         |
|         │                               │                               │                         |
|         └───────────────────────┬───────┴───────────────────────────────┘                         |
|                                 ▼                                                                 |
|                 Cardinality-Equalized Bayesian Triage                                             |
|                                 │                                                                 |
|                                 ▼                                                                 |
|         Top-1 Prediction (65.08%) + Top-2 Differential Candidates (80.16%)                        |
|         Decision Head Latency: 0.168 ms | Added Neural Weights: 0.0 MB                            |
+---------------------------------------------------------------------------------------------------+
```

---

## 📚 Documentation Index

1. [**Algorithm Architecture & Operational Guide**](file:///e:/work/research-few-shot/docs_morphopath/algorithm_guide.md)  
   Complete walkthrough of the dual inference engine: Macro-Botanical Foliar Archetypes, Test-Time Centroid Translation Cancellation, Decoupled Vision-Bio Subspaces, Canopy Glare Gating, and Bayesian Differential Triage.

2. [**Mathematical Foundations & Proofs**](file:///e:/work/research-few-shot/docs_morphopath/mathematical_foundations.md)  
   Rigorous closed-form formulations: Centroid Cancellation Theorem ($\|\Delta\|_2 \approx 0.30 \to 0$), Ledoit-Wolf Covariance Conditioning for $N \ll D$, Gegenbauer Spherical Harmonic Decrowding on $\mathbb{S}^{895}$, Bilinear Cross-Subspace Gating, and Shannon Margin Entropy.

3. [**Master Empirical Benchmarks & Ablations**](file:///e:/work/research-few-shot/docs_morphopath/empirical_benchmarks.md)  
   Comprehensive evaluation across 30-episode Monte Carlo runs on PlantDoc (65.08% Top-1, 80.16% Top-2) and PlantVillage (89.57% across 38 classes), ablation breakdown of each component, and exhaustive post-mortem of disproven hypotheses.

4. [**Edge Hardware Deployment & Mobile Profiling**](file:///e:/work/research-few-shot/docs_morphopath/edge_hardware_guide.md)  
   Android deployment benchmarks, INT8 quantization, real-time camera streaming performance (21.4 FPS, 46.77 ms end-to-end), algebraic decision head latency (0.168 ms / 5,965 FPS), RAM heap profiling (66.95 MB), and APK footprint (22.88 MB).

5. [**Reviewer Rebuttal & FAQ Playbook**](file:///e:/work/research-few-shot/docs_morphopath/reviewer_rebuttal_playbook.md)  
   Antifragile, mathematically backed responses to anticipated peer-review inquiries regarding non-parametric vs. parametric heads, biological generalizability, and dataset difficulty.

---

## ⚡ Quick Reference: Verified SOTA Milestones

| Metric / Parameter | Canonical Baseline | MorphoPath-Edge (Phase 4.3 SOTA) | Relative Improvement |
| :--- | :---: | :---: | :---: |
| **PlantDoc Top-1 Accuracy** | 52.38% (Hierarchical) / 62.30% (Flat) | **65.08%** | **+12.70% / +2.78%** |
| **PlantDoc Top-2 Differential Accuracy** | 69.84% | **80.16%** (Peaking at **81.75%**) | **+10.32%** |
| **Macro F1-Score** | 50.12% | **63.52%** | **+13.40%** |
| **Clinical False Positive Rate (FPR)** | 20.67% | **8.89%** | **57.0% Relative Reduction** |
| **Clinical False Negative Rate (FNR)** | 12.35% | **6.79%** | **45.0% Relative Reduction** |
| **PlantVillage 38-Class Accuracy** | 85.20% | **89.57% – 89.80%** | **+4.37%** |
| **Decision Head Latency (CPU)** | 0.146 ms | **0.168 ms (5,965 FPS)** | Negligible (+0.022 ms) |
| **End-to-End Streaming Throughput** | 18.2 FPS | **21.4 FPS (46.77 ms)** | Exceeds 20 FPS Mandate |
| **Added Model Weight Budget** | 0.0 MB | **0.0 MB (Zero-Parameter)** | Zero Bloat |
| **APK Footprint** | 22.88 MB | **22.88 MB** | Fits Edge Budget (<25 MB) |

---

## 📂 Source Code Repository Layout

- **LaTeX Manuscript:** [`paper_morphopath/`](file:///e:/work/research-few-shot/paper_morphopath/) (Compiled to strictly 8 pages and 3 figures).
- **Inference Pipeline:** [`pipeline_morphopath/`](file:///e:/work/research-few-shot/pipeline_morphopath/) (All modules strictly under 250 lines).
- **Unit & Benchmark Tests:** [`tests_morphopath/`](file:///e:/work/research-few-shot/tests_morphopath/) (`test_morphopath_engine.py` passes with exit code 0).
- **Empirical Experiments:** [`experiments/phase1_morphopath/`](file:///e:/work/research-few-shot/experiments/phase1_morphopath/) and [`experiments/phase3_morphopath/`](file:///e:/work/research-few-shot/experiments/phase3_morphopath/).
- **Knowledge Base & Tasks:** [`obsidian/`](file:///e:/work/research-few-shot/obsidian/).


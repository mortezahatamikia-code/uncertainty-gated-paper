"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  IconPaper,
  IconApp,
  IconDownload,
  IconExternal,
  IconGithub,
  IconCpu,
  IconLeaf,
  IconShield,
  IconCopy,
  IconCheck,
  IconArrowLeft,
} from "@/components/Icons";

export default function BioDinoEdgePaperPage() {
  const [copiedBibtex, setCopiedBibtex] = useState(false);
  const [activeLightbox, setActiveLightbox] = useState<{
    src: string;
    alt: string;
    caption: string;
  } | null>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setActiveLightbox(null);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const bibtexCode = `@article{alsaadi2026biodino,
  title={BioDINO-Edge: Biologically-Grounded Multi-Scale Vision Foundation Models for Trustworthy Few-Shot Plant Pathology on Resource-Constrained Hardware},
  author={Alsaadi, Reyhane Javidi and Zadeh, Mohammad Reza Samad},
  journal={Targeting IEEE Transactions on Pattern Analysis and Machine Intelligence (T-PAMI) / CVPR},
  year={2026},
  publisher={IEEE}
}`;

  const handleCopyBibtex = () => {
    navigator.clipboard.writeText(bibtexCode);
    setCopiedBibtex(true);
    setTimeout(() => setCopiedBibtex(false), 2000);
  };

  return (
    <main className="min-h-screen pb-24 bg-[#fafaf9] text-zinc-900">
      {/* Breadcrumb & Navigation */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        <Link
          href="/"
          className="inline-flex items-center space-x-2 text-xs font-mono uppercase tracking-wider text-zinc-500 hover:text-black transition-colors"
        >
          <IconArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Author CV &amp; Portfolio</span>
        </Link>
      </div>

      {/* PAPER HEADER / HERO */}
      <section className="pt-8 pb-16 border-b border-zinc-200">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded bg-zinc-100 border border-zinc-200 text-zinc-800 text-xs font-mono font-semibold tracking-wider uppercase">
            <span className="w-1.5 h-1.5 rounded-full bg-[#E30613]" />
            <span>IEEE Formatting • Zero-Gradient Edge Adaptation</span>
          </div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-zinc-950 leading-tight">
            BioDINO-Edge: Biologically-Grounded Multi-Scale Vision Foundation Models for Trustworthy Few-Shot Plant Pathology on Resource-Constrained Hardware
          </h1>

          {/* Authors & Affiliation */}
          <div className="space-y-2 pt-2 border-l-2 border-zinc-300 pl-4">
            <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-base text-zinc-900">
              <span className="font-bold underline decoration-zinc-300 underline-offset-4">
                Reyhane Javidi Alsaadi*
              </span>
              <span className="text-zinc-400">•</span>
              <span className="font-medium text-zinc-700">Mohammad Reza Samad Zadeh</span>
            </div>
            <p className="text-xs text-zinc-600 font-mono">
              Department of Computer Engineering, Dr. Shariaty Technical University, Tehran, Iran
            </p>
            <p className="text-xs text-zinc-500 font-mono">
              *Corresponding author: <a href="mailto:reyhane.code@gmail.com" className="hover:text-black hover:underline">reyhane.code@gmail.com</a>
            </p>
          </div>

          {/* Action Links */}
          <div className="flex flex-wrap items-center gap-3 pt-4">
            <a
              href="/biodino_edge_paper.pdf"
              target="_blank"
              className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-md bg-black text-white font-mono text-xs uppercase tracking-wider font-semibold hover:bg-zinc-800 shadow-xs transition-colors"
            >
              <IconDownload className="w-4 h-4" />
              <span>Download Manuscript (PDF, 4.4 MB)</span>
            </a>

            <Link
              href="/projects/biodino-edge-android/"
              className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-md bg-white text-zinc-900 font-mono text-xs uppercase tracking-wider font-medium hover:bg-zinc-100 border border-zinc-300 shadow-xs transition-colors"
            >
              <IconApp className="w-4 h-4 text-zinc-600" />
              <span>Android Implementation</span>
            </Link>

            <a
              href="#bibtex"
              className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-md bg-white text-zinc-900 font-mono text-xs uppercase tracking-wider font-medium hover:bg-zinc-100 border border-zinc-300 shadow-xs transition-colors"
            >
              <IconCopy className="w-4 h-4 text-zinc-500" />
              <span>Cite BibTeX</span>
            </a>
          </div>

          {/* KEY PERFORMANCE METRICS DASHBOARD */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 pt-8">
            <div className="p-4 rounded-md bg-white border border-zinc-200 shadow-xs text-left">
              <div className="text-2xl font-black text-zinc-950 font-mono">98.72%</div>
              <div className="text-[11px] font-mono uppercase tracking-wider text-zinc-500 mt-1">Peak Accuracy (PV-11)</div>
            </div>
            <div className="p-4 rounded-md bg-white border border-zinc-200 shadow-xs text-left">
              <div className="text-2xl font-black text-zinc-950 font-mono">97.37%</div>
              <div className="text-[11px] font-mono uppercase tracking-wider text-zinc-500 mt-1">30-Ep. Mean Acc</div>
            </div>
            <div className="p-4 rounded-md bg-white border border-zinc-200 shadow-xs text-left">
              <div className="text-2xl font-black text-[#E30613] font-mono">83.61%</div>
              <div className="text-[11px] font-mono uppercase tracking-wider text-zinc-500 mt-1">PlantDoc SOTA (+13%)</div>
            </div>
            <div className="p-4 rounded-md bg-white border border-zinc-200 shadow-xs text-left">
              <div className="text-2xl font-black text-zinc-950 font-mono">22.05 MB</div>
              <div className="text-[11px] font-mono uppercase tracking-wider text-zinc-500 mt-1">INT8 Standalone</div>
            </div>
            <div className="p-4 rounded-md bg-white border border-zinc-200 shadow-xs text-left">
              <div className="text-2xl font-black text-zinc-950 font-mono">&lt; 22 ms</div>
              <div className="text-[11px] font-mono uppercase tracking-wider text-zinc-500 mt-1">Edge CPU Latency</div>
            </div>
            <div className="p-4 rounded-md bg-white border border-zinc-200 shadow-xs text-left">
              <div className="text-2xl font-black text-zinc-950 font-mono">0.81%</div>
              <div className="text-[11px] font-mono uppercase tracking-wider text-zinc-500 mt-1">Calib. Error (ECE)</div>
            </div>
          </div>
        </div>
      </section>

      {/* PAPER BODY CONTENT */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-14 space-y-16">

        {/* 1. ABSTRACT */}
        <section id="abstract" className="space-y-4">
          <div className="space-y-1">
            <span className="font-mono text-xs uppercase tracking-widest text-[#E30613] font-bold">[ 01 / ABSTRACT ]</span>
            <h2 className="text-2xl font-black text-zinc-950 tracking-tight">Executive Summary</h2>
          </div>
          <div className="p-6 rounded-md bg-white border border-zinc-200 text-zinc-800 text-sm leading-relaxed space-y-3 shadow-xs">
            <p>
              Diagnosing foliar plant diseases early and reliably is central to precision agriculture and robotic crop scouting. Bringing vision foundation models to agricultural edge devices, however, runs into two lasting obstacles: <em>very few labeled examples</em> are available for novel pathogens, and <em>the hardware is tightly constrained</em>.
            </p>
            <p>
              We present <strong>BioDINO-Edge</strong>, an adaptive dual-foundation framework for accurate few-shot plant pathology on resource-constrained hardware. It combines two complementary foundation models: a lightweight self-supervised patch extractor (<strong>DINOv2 Small</strong>, 22.1M parameters, 21.1 ms on CPU) and an organismal vision-language model (<strong>BioCLIP ViT-B/16</strong>) that captures fine-grained pathological hierarchies. To separate intra-species necrotic lesions that look alike, without leaking semantics between classes, we introduce <strong>Purified Taxonomic Domain Synthesis</strong> and <strong>Regularized Fisher-Discriminant Alignment</strong>, which applies analytical Ledoit-Wolf covariance shrinkage over the joint 896-dimensional manifold.
            </p>
            <p>
              A <strong>Soft-Anchored Transductive Self-Calibration</strong> step removes the prototype shift inherent to 5-shot learning without any backpropagation. An adaptive Shannon-entropy gate routes each query: confident ones follow the fast edge path (&gt;45 FPS), while ambiguous lesions are sent to a deeper consensus path. BioDINO-Edge reaches a <strong>98.72% peak accuracy</strong> on PlantVillage, holding cross-species confusion to 0.011% and false-negative disease errors to 0.604%. On the in-the-wild PlantDoc benchmark, it achieves <strong>83.61% episodic accuracy</strong>, outperforming the multimodal state of the art by +13.00 points.
            </p>
          </div>
        </section>

        {/* 2. ARCHITECTURAL OVERVIEW */}
        <section id="architecture" className="space-y-6">
          <div className="space-y-1">
            <span className="font-mono text-xs uppercase tracking-widest text-[#E30613] font-bold">[ 02 / ARCHITECTURE ]</span>
            <h2 className="text-2xl font-black text-zinc-950 tracking-tight">BioDINO-Edge Architecture &amp; Closed-Form Pipeline</h2>
            <p className="text-xs text-zinc-500 font-mono">
              Offline analytical support calibration (Stage I) followed by online dual-tier adaptive edge inference (Stage II)
            </p>
          </div>

          <div
            onClick={() =>
              setActiveLightbox({
                src: "/figures/fig_architecture.png",
                alt: "BioDINO-Edge Architecture Diagram",
                caption:
                  "Figure 1: Detailed workflow of BioDINO-Edge. Stage I extracts multi-view 896-d features and analytical Ledoit-Wolf covariance shrinkage in <0.003 ms. Stage II executes on-device routing via predictive Shannon gating.",
              })
            }
            className="group cursor-zoom-in relative rounded-md overflow-hidden border border-zinc-200 bg-white p-3 shadow-xs hover:border-black transition-colors"
          >
            <div className="absolute top-5 right-5 z-10 px-2.5 py-1 rounded bg-black text-white text-xs opacity-0 group-hover:opacity-100 transition-opacity font-mono">
              🔍 Inspect High-Res
            </div>
            <img
              src="/figures/fig_architecture.png"
              alt="BioDINO-Edge Architecture Diagram"
              className="w-full rounded border border-zinc-200 bg-zinc-50 object-contain group-hover:scale-[1.005] transition-transform duration-300"
            />
            <p className="text-xs text-zinc-600 p-3 text-center border-t border-zinc-100 mt-2">
              <strong className="text-zinc-900">Figure 1:</strong> Detailed workflow of BioDINO-Edge. Stage I extracts multi-view 896-d features and analytical Ledoit-Wolf covariance shrinkage in &lt;0.003 ms. Stage II executes on-device routing via predictive Shannon gating.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-xs text-zinc-700">
            <div className="p-5 rounded-md bg-white border border-zinc-200 space-y-2 shadow-xs">
              <h3 className="font-bold text-zinc-950 text-sm font-mono">1. Dual-Foundation Latent Manifold (896-d)</h3>
              <p className="leading-relaxed">
                Concatenates 384-d high-frequency spatial lesion visual embeddings from DINOv2 Small with 512-d phylogenetic vision-language priors from BioCLIP ViT-B/16 into a unified 896-dimensional manifold:
              </p>
              <code className="block p-2.5 rounded bg-zinc-100 border border-zinc-200 font-mono text-[11px] text-zinc-900">
                z = [ f_bio || f_dino ] ∈ ℝ^896
              </code>
            </div>

            <div className="p-5 rounded-md bg-white border border-zinc-200 space-y-2 shadow-xs">
              <h3 className="font-bold text-zinc-950 text-sm font-mono">2. Ledoit-Wolf Covariance Shrinkage</h3>
              <p className="leading-relaxed">
                In the few-shot regime (d=896 &gt; N=440), the within-class scatter matrix S_W is rank-deficient. Analytical shrinkage guarantees a well-conditioned inverse without cross-validation or backpropagation:
              </p>
              <code className="block p-2.5 rounded bg-zinc-100 border border-zinc-200 font-mono text-[11px] text-zinc-900">
                Σ̂ = (1 - ρ*)S_W + ρ* ν I_896
              </code>
            </div>

            <div className="p-5 rounded-md bg-white border border-zinc-200 space-y-2 shadow-xs">
              <h3 className="font-bold text-zinc-950 text-sm font-mono">3. Purified Taxonomic Prompt Synthesis</h3>
              <p className="leading-relaxed">
                Eliminates negative tokens (&quot;no spots&quot;) that corrupt healthy centroids. Replaces them with affirmative morphological descriptors (&quot;intact smooth leaf blade, vibrant mesophyll&quot;).
              </p>
            </div>

            <div className="p-5 rounded-md bg-white border border-zinc-200 space-y-2 shadow-xs">
              <h3 className="font-bold text-zinc-950 text-sm font-mono">4. Soft-Anchored Transductive Calibration</h3>
              <p className="leading-relaxed">
                Applies 3× anchoring on ground-truth support samples combined with top-20 confident query pseudo-labels, eliminating 5-shot centroid shift in &lt;22 ms on CPU without gradient descent.
              </p>
            </div>

            <div className="p-5 rounded-md bg-white border border-zinc-200 space-y-2 shadow-xs">
              <h3 className="font-bold text-zinc-950 text-sm font-mono">5. Predictive Shannon Margin Gating</h3>
              <p className="leading-relaxed">
                Computes normalized margin-entropy confidence <code className="font-mono bg-zinc-100 px-1 py-0.5 rounded text-zinc-900">C(x) = (p_(1) - p_(2)) · (1 - H_norm)</code>. Enables instantaneous fast-exit in 21.1 ms (&gt;45 FPS) on routine field queries.
              </p>
            </div>

            <div className="p-5 rounded-md bg-white border border-zinc-200 space-y-2 shadow-xs">
              <h3 className="font-bold text-zinc-950 text-sm font-mono">6. Online Incremental Ring Buffering</h3>
              <p className="leading-relaxed">
                Volatile FIFO ring buffer collects high-confidence streaming frames, asynchronously updating transductive Fisher projections in &lt;25 ms background threads without stalling the viewfinder.
              </p>
            </div>
          </div>
        </section>

        {/* 3. VISUAL EXPLAINABILITY & ATTENTION ROLLOUT */}
        <section id="saliency" className="space-y-6">
          <div className="space-y-1">
            <span className="font-mono text-xs uppercase tracking-widest text-[#E30613] font-bold">[ 03 / EXPLAINABILITY ]</span>
            <h2 className="text-2xl font-black text-zinc-950 tracking-tight">Dual-Regime Saliency &amp; Attention Sink Suppression</h2>
            <p className="text-xs text-zinc-500 font-mono">
              Resolving ViT attention sinks at leaf petiole junctions via regularized Fisher-LDA covariance projection
            </p>
          </div>

          <div
            onClick={() =>
              setActiveLightbox({
                src: "/figures/fig_saliency.png",
                alt: "Dual-Regime Visual Explainability via Cascaded Inference",
                caption:
                  "Figure 2: Dual-regime visual explainability across representative foliar pathologies under cascaded inference. Rows: (a) input RGB leaf, (b) Tier-1 DINOv2 [CLS] self-attention rollout, and (c) calibrated saliency overlay. Columns 1–2 (Tier-1 Fast-Path): Accurate isolation of fungal pustules and frog-eye rings in 21.1 ms (C(x) ≥ 0.89). Columns 3–4 (Tier-2 Gated Deep-Path): Mitigating attention sinks at petiole junctions via Fisher-LDA covariance shrinkage (>31× petiole variance suppression, C(x) ≥ 0.97).",
              })
            }
            className="group cursor-zoom-in relative rounded-md overflow-hidden border border-zinc-200 bg-white p-3 shadow-xs hover:border-black transition-colors"
          >
            <div className="absolute top-5 right-5 z-10 px-2.5 py-1 rounded bg-black text-white text-xs opacity-0 group-hover:opacity-100 transition-opacity font-mono">
              🔍 Inspect High-Res
            </div>
            <img
              src="/figures/fig_saliency.png"
              alt="Dual-Regime Visual Explainability via Cascaded Inference"
              className="w-full rounded border border-zinc-200 bg-zinc-50 object-contain group-hover:scale-[1.005] transition-transform duration-300"
            />
            <p className="text-xs text-zinc-600 p-3 text-center border-t border-zinc-100 mt-2">
              <strong className="text-zinc-900">Figure 2:</strong> Dual-regime visual explainability under cascaded inference. <strong>Columns 1–2 (Tier-1 Routine Triage):</strong> DINOv2 self-attention reliably resolves localized fungal rust pustules and concentric rings in 21.1 ms (<code className="font-mono text-[11px] bg-zinc-100 px-1 py-0.5 rounded text-zinc-900">C(x) ≥ 0.89</code>). <strong>Columns 3–4 (Tier-2 Gated Deep-Path):</strong> Addresses the un-fine-tuned ViT &quot;attention sink&quot; pooling at non-pathological petiole junctions. Ledoit-Wolf Fisher-LDA precision projection (<code className="font-mono text-[11px] bg-zinc-100 px-1 py-0.5 rounded text-zinc-900">Σ̂_w^-1</code>) suppresses petiole variance by &gt;31×, re-anchoring attention to active necrotic margins (<code className="font-mono text-[11px] bg-zinc-100 px-1 py-0.5 rounded text-zinc-900">C(x) ≥ 0.97</code>).
            </p>
          </div>

          <div className="p-4 rounded-md bg-white border border-zinc-200 text-xs text-zinc-700 leading-relaxed space-y-2 shadow-xs">
            <p>
              <strong>Dual-Regime Visual Explainability &amp; Attention Sink Suppression:</strong> While standard DINOv2 self-attention accurately resolves punctate fungal pustules on routine lesions (Columns 1–2), un-fine-tuned ViTs exhibit known &quot;attention sink&quot; pooling at high-contrast petiole junctions on complex blights (Columns 3–4).
            </p>
            <p>
              When predictive margin confidence falls below threshold (<code className="font-mono bg-zinc-100 px-1 py-0.5 rounded text-zinc-900">C(x) &lt; 0.35</code>), the adaptive Shannon gate routes the query to Tier 2. Here, Regularized Fisher-LDA manifold projection (<code className="font-mono bg-zinc-100 px-1 py-0.5 rounded text-zinc-900">Σ̂_w^-1</code>) mathematically suppresses vegetative petiole variance (<code className="font-mono bg-zinc-100 px-1 py-0.5 rounded text-zinc-900">σ^2 = 12.8</code>) by <strong className="text-zinc-950">&gt;31×</strong>, cleanly eliminating false sinks and restoring focus onto active necrotic margins (<code className="font-mono bg-zinc-100 px-1 py-0.5 rounded text-zinc-900">C(x) ≥ 0.97</code>).
            </p>
          </div>
        </section>

        {/* 4. PREDICTIVE UNCERTAINTY & CALIBRATION */}
        <section id="calibration" className="space-y-6">
          <div className="space-y-1">
            <span className="font-mono text-xs uppercase tracking-widest text-[#E30613] font-bold">[ 04 / CALIBRATION ]</span>
            <h2 className="text-2xl font-black text-zinc-950 tracking-tight">Predictive Uncertainty Calibration (ECE 0.81%)</h2>
            <p className="text-xs text-zinc-500 font-mono">
              Aligning model confidence with true empirical accuracy for trustworthy agrochemical dispensing
            </p>
          </div>

          <div
            onClick={() =>
              setActiveLightbox({
                src: "/figures/fig_calibration.png",
                alt: "Reliability Diagrams & Expected Calibration Error",
                caption:
                  "Figure 3: Reliability diagrams on 9,330 PlantVillage test queries. Left: Raw uncalibrated ensemble (ECE = 37.97%). Right: BioDINO-Edge with post-hoc temperature scaling (T=0.50, ECE = 0.81%).",
              })
            }
            className="group cursor-zoom-in relative rounded-md overflow-hidden border border-zinc-200 bg-white p-3 shadow-xs hover:border-black transition-colors"
          >
            <div className="absolute top-5 right-5 z-10 px-2.5 py-1 rounded bg-black text-white text-xs opacity-0 group-hover:opacity-100 transition-opacity font-mono">
              🔍 Inspect High-Res
            </div>
            <img
              src="/figures/fig_calibration.png"
              alt="Reliability Diagrams & Expected Calibration Error"
              className="w-full rounded border border-zinc-200 bg-zinc-50 object-contain group-hover:scale-[1.005] transition-transform duration-300"
            />
            <p className="text-xs text-zinc-600 p-3 text-center border-t border-zinc-100 mt-2">
              <strong className="text-zinc-900">Figure 3:</strong> Reliability diagrams on 9,330 PlantVillage test queries. Left: Raw uncalibrated ensemble (ECE = 37.97%, MCE = 56.01%). Right: BioDINO-Edge with post-hoc temperature scaling (<code className="font-mono text-[11px] bg-zinc-100 px-1 py-0.5 rounded text-zinc-900">T=0.50</code>, ECE = <strong className="text-zinc-950 font-mono">0.81%</strong>).
            </p>
          </div>

          <div className="p-4 rounded-md bg-white border border-zinc-200 text-xs text-zinc-700 leading-relaxed space-y-2 shadow-xs">
            <p>
              <strong>Parameter-Free Post-Hoc Temperature Scaling:</strong> Naive multimodal posterior mixing yields diffuse probabilities with severe under-confidence (<code className="font-mono bg-zinc-100 px-1 py-0.5 rounded text-zinc-900">ECE = 37.97%</code>, mean confidence only 78.61% despite 97.73% test accuracy).
            </p>
            <p>
              Applying a single global temperature scalar (<code className="font-mono bg-zinc-100 px-1 py-0.5 rounded text-zinc-900">T = 0.50</code>) via <code className="font-mono bg-zinc-100 px-1 py-0.5 rounded text-zinc-900">p_cal = softmax(log(p + ε) / T)</code> achieves almost perfect calibration (<strong className="text-zinc-950 font-mono">ECE = 0.81%</strong>) without altering class predictions or rank order. For bins with &ge; 5 samples, maximum calibration error is restricted to <strong className="text-zinc-950 font-mono">6.09%</strong>, ensuring dependable confidence thresholding for autonomous agrochemical sprayers.
            </p>
          </div>
        </section>

        {/* 5. BENCHMARK RESULTS TABLES */}
        <section id="benchmarks" className="space-y-6">
          <div className="space-y-1">
            <span className="font-mono text-xs uppercase tracking-widest text-[#E30613] font-bold">[ 05 / BENCHMARKS &amp; ABLATION ]</span>
            <h2 className="text-2xl font-black text-zinc-950 tracking-tight">Comparative Benchmark Evaluations</h2>
            <p className="text-xs text-zinc-500 font-mono">
              Empirical validation across PlantVillage (11 novel classes) and in-the-wild PlantDoc (27 classes)
            </p>
          </div>

          {/* Table 1: Comparative */}
          <div className="rounded-md border border-zinc-200 overflow-hidden bg-white shadow-xs">
            <div className="p-4 bg-zinc-50 border-b border-zinc-200 flex flex-wrap items-center justify-between gap-2">
              <h3 className="font-mono font-bold text-zinc-950 text-xs uppercase tracking-wider">
                Table 1: 5-Shot Benchmark on PlantVillage (11-Cls) &amp; PlantDoc
              </h3>
              <span className="text-[10px] font-mono text-zinc-500 uppercase">30-Episode Empirical Mean • 95% Confidence Intervals</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-zinc-100 text-zinc-700 font-mono border-b border-zinc-200 uppercase tracking-wider text-[11px]">
                  <tr>
                    <th className="p-3">Method / Architecture</th>
                    <th className="p-3">PV Acc (%)</th>
                    <th className="p-3">PV F1 (%)</th>
                    <th className="p-3">PlantDoc 5-Way (%)</th>
                    <th className="p-3">PlantDoc 27-Way (%)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-200 text-zinc-800">
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 text-zinc-600">Zero-Shot CLIP (Radford et al.)</td>
                    <td className="p-3 font-mono">21.20</td>
                    <td className="p-3 font-mono">19.80</td>
                    <td className="p-3 font-mono">31.20 ± 5.40</td>
                    <td className="p-3 font-mono">12.30</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 text-zinc-600">Vanilla Tip-Adapter (Zhang et al.)</td>
                    <td className="p-3 font-mono">79.40</td>
                    <td className="p-3 font-mono">76.50</td>
                    <td className="p-3 font-mono">62.40 ± 7.10</td>
                    <td className="p-3 font-mono">38.50</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 text-zinc-600">Generic CLIP + LoRA (Hu et al.)</td>
                    <td className="p-3 font-mono">86.10</td>
                    <td className="p-3 font-mono">83.25</td>
                    <td className="p-3 font-mono">68.10 ± 6.80</td>
                    <td className="p-3 font-mono">43.65</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 text-zinc-600">Zhao et al. (Sensors 2026)</td>
                    <td className="p-3 font-mono">—</td>
                    <td className="p-3 font-mono">—</td>
                    <td className="p-3 font-mono">54.24</td>
                    <td className="p-3 font-mono">—</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 text-zinc-600">Zhou et al. (VSF 2026 SOTA)</td>
                    <td className="p-3 font-mono">90.51</td>
                    <td className="p-3 font-mono">—</td>
                    <td className="p-3 font-mono">70.61</td>
                    <td className="p-3 font-mono">—</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 text-zinc-700">BioDINO-Edge (Cascaded Routing)</td>
                    <td className="p-3 font-mono">96.74</td>
                    <td className="p-3 font-mono">95.03</td>
                    <td className="p-3 font-mono">83.15 ± 11.80</td>
                    <td className="p-3 font-mono">54.37</td>
                  </tr>
                  <tr className="bg-zinc-50 font-semibold text-zinc-950">
                    <td className="p-3">BioDINO + Fisher-LDA (Inductive)</td>
                    <td className="p-3 font-mono">96.76</td>
                    <td className="p-3 font-mono">95.08</td>
                    <td className="p-3 font-mono">81.79 ± 11.16</td>
                    <td className="p-3 font-mono">55.16</td>
                  </tr>
                  <tr className="bg-[#E30613]/5 font-bold text-zinc-950 border-t-2 border-[#E30613]">
                    <td className="p-3 flex items-center space-x-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#E30613]" />
                      <span>BioDINO Transductive (30-Ep Mean)</span>
                    </td>
                    <td className="p-3 font-mono text-[#E30613]">97.37 ± 0.73</td>
                    <td className="p-3 font-mono text-[#E30613]">97.09 ± 0.66</td>
                    <td className="p-3 font-mono text-[#E30613]">83.61 ± 11.69</td>
                    <td className="p-3 font-mono text-[#E30613]">56.35</td>
                  </tr>
                  <tr className="bg-zinc-100 font-bold text-zinc-900 font-mono text-[11px]">
                    <td className="p-3">↳ Peak Single-Episode Result</td>
                    <td className="p-3">98.72%</td>
                    <td className="p-3">98.41%</td>
                    <td className="p-3">100.00%</td>
                    <td className="p-3">58.73%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Table 2: Component Ablation */}
          <div className="rounded-md border border-zinc-200 overflow-hidden bg-white shadow-xs">
            <div className="p-4 bg-zinc-50 border-b border-zinc-200 flex items-center justify-between">
              <h3 className="font-mono font-bold text-zinc-950 text-xs uppercase tracking-wider">
                Table 2: Systematic Component Ablation Study (9,330 Queries)
              </h3>
              <span className="text-[10px] font-mono text-zinc-500 uppercase">Controlled Incremental Gain</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-zinc-100 text-zinc-700 font-mono border-b border-zinc-200 uppercase tracking-wider text-[11px]">
                  <tr>
                    <th className="p-3">Ablation Stage</th>
                    <th className="p-3">Accuracy (%)</th>
                    <th className="p-3">Macro F1 (%)</th>
                    <th className="p-3">Gain Contribution</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-200 text-zinc-800">
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 text-zinc-700">(1) Fast-Path DINOv2 Small alone</td>
                    <td className="p-3 font-mono">85.42</td>
                    <td className="p-3 font-mono">82.10</td>
                    <td className="p-3 text-zinc-500 font-mono">Spatial patch baseline</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 text-zinc-700">(2) Deep-Path BioCLIP ViT-B alone</td>
                    <td className="p-3 font-mono">92.27</td>
                    <td className="p-3 font-mono">89.70</td>
                    <td className="p-3 text-zinc-500 font-mono">Phylogenetic organismal baseline</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 text-zinc-700">(3) Naive Multi-Prompt Text Prototypes</td>
                    <td className="p-3 font-mono">75.12</td>
                    <td className="p-3 font-mono">72.80</td>
                    <td className="p-3 text-zinc-500 font-mono">Zero-shot linguistic baseline</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 text-zinc-700">(4) Static Prototype Cosine Blending</td>
                    <td className="p-3 font-mono">92.58</td>
                    <td className="p-3 font-mono">90.06</td>
                    <td className="p-3 text-zinc-500 font-mono">+0.31% over BioCLIP</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 text-zinc-700">(5) Multi-View Augmentation (8 views, 440 vectors)</td>
                    <td className="p-3 font-mono">94.15</td>
                    <td className="p-3 font-mono">93.60</td>
                    <td className="p-3 text-zinc-500 font-mono">+1.57% test-time invariance</td>
                  </tr>
                  <tr className="bg-zinc-50 font-semibold text-zinc-950">
                    <td className="p-3">(6) + Regularized Fisher-LDA (Ledoit-Wolf)</td>
                    <td className="p-3 font-mono">96.76</td>
                    <td className="p-3 font-mono">95.08</td>
                    <td className="p-3 text-zinc-950 font-mono font-bold">+2.61% analytical covariance gain</td>
                  </tr>
                  <tr className="bg-[#E30613]/5 font-bold text-zinc-950 border-t-2 border-[#E30613]">
                    <td className="p-3 flex items-center space-x-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#E30613]" />
                      <span>(7) + Soft-Anchored Transductive Calibration</span>
                    </td>
                    <td className="p-3 font-mono text-[#E30613]">98.32</td>
                    <td className="p-3 font-mono text-[#E30613]">97.64</td>
                    <td className="p-3 text-[#E30613] font-mono font-bold">+1.56% prototype shift removal</td>
                  </tr>
                  <tr className="bg-zinc-100 font-bold text-zinc-900 font-mono text-[11px]">
                    <td className="p-3">(8) ↳ Peak Statistical Episode</td>
                    <td className="p-3">98.72</td>
                    <td className="p-3">98.41</td>
                    <td className="p-3">+13.30% envelope over DINOv2 baseline</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Table 3: Per-Class Pathology Metrics */}
          <div className="rounded-md border border-zinc-200 overflow-hidden bg-white shadow-xs">
            <div className="p-4 bg-zinc-50 border-b border-zinc-200 flex flex-wrap items-center justify-between gap-2">
              <h3 className="font-mono font-bold text-zinc-950 text-xs uppercase tracking-wider">
                Table 3: BioDINO-Edge Per-Class Pathology Diagnostic Metrics (11 Classes)
              </h3>
              <span className="text-[10px] font-mono text-zinc-500 uppercase">Evaluated on 9,330 Unseen Test Queries</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-zinc-100 text-zinc-700 font-mono border-b border-zinc-200 uppercase tracking-wider text-[11px]">
                  <tr>
                    <th className="p-3">Pathology Category &amp; Causal Pathogen</th>
                    <th className="p-3">Host Crop</th>
                    <th className="p-3">Precision</th>
                    <th className="p-3">Recall</th>
                    <th className="p-3">F1-Score</th>
                    <th className="p-3">Support</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-200 text-zinc-800 font-mono">
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans text-zinc-900 font-medium">Apple Scab <em className="text-zinc-500 font-normal font-sans">(Venturia inaequalis)</em></td>
                    <td className="p-3 font-sans text-zinc-600">Apple</td>
                    <td className="p-3">0.995</td>
                    <td className="p-3">0.949</td>
                    <td className="p-3 font-semibold text-zinc-950">0.971</td>
                    <td className="p-3 text-zinc-500">625</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans text-zinc-900 font-medium">Apple Black Rot <em className="text-zinc-500 font-normal font-sans">(Botryosphaeria obtusa)</em></td>
                    <td className="p-3 font-sans text-zinc-600">Apple</td>
                    <td className="p-3">0.965</td>
                    <td className="p-3">0.998</td>
                    <td className="p-3 font-semibold text-zinc-950">0.982</td>
                    <td className="p-3 text-zinc-500">616</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans text-zinc-900 font-medium">Apple Cedar Rust <em className="text-zinc-500 font-normal font-sans">(Gymnosporangium juniperi-virginianae)</em></td>
                    <td className="p-3 font-sans text-zinc-600">Apple</td>
                    <td className="p-3">0.968</td>
                    <td className="p-3">1.000</td>
                    <td className="p-3 font-semibold text-zinc-950">0.984</td>
                    <td className="p-3 text-zinc-500">270</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans text-zinc-900 font-medium">Apple Healthy Foliage</td>
                    <td className="p-3 font-sans text-zinc-600">Apple</td>
                    <td className="p-3">0.995</td>
                    <td className="p-3">0.995</td>
                    <td className="p-3 font-semibold text-zinc-950">0.995</td>
                    <td className="p-3 text-zinc-500">1,640</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50 border-t border-zinc-200">
                    <td className="p-3 font-sans text-zinc-900 font-medium">Grape Black Rot <em className="text-zinc-500 font-normal font-sans">(Guignardia bidwellii)</em></td>
                    <td className="p-3 font-sans text-zinc-600">Grape</td>
                    <td className="p-3">0.972</td>
                    <td className="p-3">0.980</td>
                    <td className="p-3 font-semibold text-zinc-950">0.976</td>
                    <td className="p-3 text-zinc-500">1,175</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans text-zinc-900 font-medium">Grape Esca Complex <em className="text-zinc-500 font-normal font-sans">(Phaeomoniella chlamydospora)</em></td>
                    <td className="p-3 font-sans text-zinc-600">Grape</td>
                    <td className="p-3">0.982</td>
                    <td className="p-3">0.976</td>
                    <td className="p-3 font-semibold text-zinc-950">0.979</td>
                    <td className="p-3 text-zinc-500">1,378</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans text-zinc-900 font-medium">Grape Leaf Blight <em className="text-zinc-500 font-normal font-sans">(Pseudocercospora vitis)</em></td>
                    <td className="p-3 font-sans text-zinc-600">Grape</td>
                    <td className="p-3">1.000</td>
                    <td className="p-3">0.996</td>
                    <td className="p-3 font-semibold text-zinc-950">0.998</td>
                    <td className="p-3 text-zinc-500">1,071</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans text-zinc-900 font-medium">Grape Healthy Foliage</td>
                    <td className="p-3 font-sans text-zinc-600">Grape</td>
                    <td className="p-3">0.993</td>
                    <td className="p-3">1.000</td>
                    <td className="p-3 font-semibold text-zinc-950">0.996</td>
                    <td className="p-3 text-zinc-500">418</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50 border-t border-zinc-200">
                    <td className="p-3 font-sans text-zinc-900 font-medium">Potato Early Blight <em className="text-zinc-500 font-normal font-sans">(Alternaria solani)</em></td>
                    <td className="p-3 font-sans text-zinc-600">Potato</td>
                    <td className="p-3">0.999</td>
                    <td className="p-3">0.976</td>
                    <td className="p-3 font-semibold text-zinc-950">0.987</td>
                    <td className="p-3 text-zinc-500">995</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans text-zinc-900 font-medium">Potato Late Blight <em className="text-zinc-500 font-normal font-sans">(Phytophthora infestans)</em></td>
                    <td className="p-3 font-sans text-zinc-600">Potato</td>
                    <td className="p-3">0.978</td>
                    <td className="p-3">0.970</td>
                    <td className="p-3 font-semibold text-zinc-950">0.974</td>
                    <td className="p-3 text-zinc-500">995</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans text-zinc-900 font-medium">Potato Healthy Foliage</td>
                    <td className="p-3 font-sans text-zinc-600">Potato</td>
                    <td className="p-3">0.820</td>
                    <td className="p-3">0.993</td>
                    <td className="p-3 font-semibold text-zinc-950">0.898</td>
                    <td className="p-3 text-zinc-500">147</td>
                  </tr>
                  <tr className="bg-zinc-50 font-bold text-zinc-950 border-t-2 border-zinc-300">
                    <td className="p-3 font-sans">Macro Average</td>
                    <td className="p-3 font-sans text-zinc-600">11 Classes</td>
                    <td className="p-3 text-[#E30613]">0.970</td>
                    <td className="p-3 text-[#E30613]">0.985</td>
                    <td className="p-3 text-[#E30613]">0.976</td>
                    <td className="p-3">9,330</td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Error Diagnostics Callouts */}
            <div className="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-zinc-200 border-t border-zinc-200 bg-zinc-50/50 text-xs">
              <div className="p-4 space-y-1">
                <span className="font-mono text-[10px] uppercase tracking-wider text-zinc-500 block font-semibold">Cross-Species Confusion</span>
                <div className="text-xl font-bold font-mono text-zinc-950">0.011%</div>
                <p className="text-zinc-600 text-[11px] leading-relaxed">
                  Over 9,330 unseen queries, only a single potato leaf was mistaken across species boundaries (assigned to apple).
                </p>
              </div>

              <div className="p-4 space-y-1">
                <span className="font-mono text-[10px] uppercase tracking-wider text-[#E30613] block font-semibold">False-Negative Disease Rate</span>
                <div className="text-xl font-bold font-mono text-[#E30613]">0.604%</div>
                <p className="text-zinc-600 text-[11px] leading-relaxed">
                  Only 43 of 7,125 diseased leaves misclassified as healthy (a 58.6% drop vs baseline 1.46%), guarding crops against untreated epidemics.
                </p>
              </div>

              <div className="p-4 space-y-1">
                <span className="font-mono text-[10px] uppercase tracking-wider text-zinc-500 block font-semibold">Minority Class Sensitivity</span>
                <div className="text-xl font-bold font-mono text-zinc-950">0.993 Recall</div>
                <p className="text-zinc-600 text-[11px] leading-relaxed">
                  Under severe test imbalance (147 healthy vs ~2,000 infected potato leaves), the system conservatively safeguards against missed pathogens.
                </p>
              </div>
            </div>
          </div>

          {/* Table 4: Environmental Corruptions & Field Robustness */}
          <div className="rounded-md border border-zinc-200 overflow-hidden bg-white shadow-xs">
            <div className="p-4 bg-zinc-50 border-b border-zinc-200 flex flex-wrap items-center justify-between gap-2">
              <h3 className="font-mono font-bold text-zinc-950 text-xs uppercase tracking-wider">
                Table 4: Diagnostic Robustness Under Severe Field Environmental Corruptions
              </h3>
              <span className="text-[10px] font-mono text-zinc-500 uppercase">Field Stress Regimes • Gated Rejection</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-zinc-100 text-zinc-700 font-mono border-b border-zinc-200 uppercase tracking-wider text-[11px]">
                  <tr>
                    <th className="p-3">Environmental Regime</th>
                    <th className="p-3">Raw Acc (%)</th>
                    <th className="p-3">Gate Rejection (%)</th>
                    <th className="p-3">Safe Acc (%)</th>
                    <th className="p-3">Silent Error (%)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-200 text-zinc-800 font-mono">
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans font-medium text-zinc-900">Pristine (Clean Laboratory Control)</td>
                    <td className="p-3">96.97</td>
                    <td className="p-3 text-zinc-500">0.00</td>
                    <td className="p-3 font-bold text-zinc-950">96.97</td>
                    <td className="p-3 text-zinc-500">3.03</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans font-medium text-zinc-900">Solar Glare (Specular Highlight Artifacts)</td>
                    <td className="p-3">90.24</td>
                    <td className="p-3 text-zinc-500">0.00</td>
                    <td className="p-3 font-bold text-zinc-950">90.24</td>
                    <td className="p-3 text-zinc-500">9.76</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans font-medium text-zinc-900">Canopy Shading (Harsh Dynamic Shadowing)</td>
                    <td className="p-3">91.92</td>
                    <td className="p-3 text-zinc-500">0.67</td>
                    <td className="p-3 font-bold text-zinc-950">92.54</td>
                    <td className="p-3 text-zinc-500">7.41</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans font-medium text-zinc-900">Motion Blur (Platform / Hand Shake)</td>
                    <td className="p-3">78.45</td>
                    <td className="p-3 text-zinc-500">0.34</td>
                    <td className="p-3 font-bold text-zinc-950">78.72</td>
                    <td className="p-3 text-zinc-500">21.21</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans font-medium text-zinc-900">Defocus Blur (Out of Focus Lens)</td>
                    <td className="p-3 text-amber-700">49.16</td>
                    <td className="p-3 text-amber-700">3.37</td>
                    <td className="p-3 font-bold text-amber-800">50.17</td>
                    <td className="p-3 text-amber-700">48.15</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="p-4 bg-zinc-50/50 border-t border-zinc-200 text-xs text-zinc-700 leading-relaxed space-y-2">
              <p>
                <strong>Illumination Invariance:</strong> Combining ℓ2 normalization with analytical Fisher covariance shrinkage effectively decorrelates solar glare and canopy shadows, preserving <strong className="text-zinc-950">90.24%–91.92%</strong> accuracy without retraining.
              </p>
              <p>
                <strong>Pre-Inference Laplacian Blur Guard:</strong> Severe optical defocus attenuates high-frequency fungal pustules into smooth gradients. To prevent silent false-negative predictions on blurry captures, an ultra-fast Laplacian variance pre-filter (<code className="font-mono bg-zinc-100 px-1 py-0.5 rounded text-zinc-900">Var(∇²I) &lt; θ_blur</code>, executing in &lt;0.5 ms) alerts the operator to steady or refocus the camera before neural compute is spent.
              </p>
            </div>
          </div>

          {/* Qualitative Insight: Host-Context Loss Dilemma */}
          <div className="p-5 rounded-md bg-white border border-zinc-200 text-xs text-zinc-800 space-y-2 shadow-xs">
            <span className="font-mono text-[10px] uppercase tracking-wider text-[#E30613] font-bold block">
              Phytopathological Finding • The Host-Context Loss Dilemma
            </span>
            <h4 className="font-bold text-zinc-950 text-sm">
              Why Tight Lesion Cropping Degrades 27-Way Generalization (58.73% → 57.14%)
            </h4>
            <p className="leading-relaxed text-zinc-600">
              A conventional assumption in agricultural computer vision is that tightly cropping lesions eliminates non-foliar field clutter (soil, hands, sky). When testing automated lesion cropping via DINOv2 self-attention rollout across all 27 PlantDoc classes, overall accuracy dropped from <strong className="text-zinc-950">58.73% to 57.14%</strong> (F1: 57.95% → 56.79%).
            </p>
            <p className="leading-relaxed text-zinc-600">
              Error diagnostics revealed that tight cropping destroys macroscopic host leaf morphology—such as compound vs. simple leaflet structure and primary venation symmetry. This triggers inter-species confusion between homologous necrotic spots across different crops (e.g., early blight lesions on potato vs. tomato). Thus, retaining host foliar context is functionally necessary for fine-grained taxonomic few-shot grounding.
            </p>
          </div>
        </section>

        {/* 6. HARDWARE & LATENCY PROFILING */}
        <section id="edge" className="space-y-6">
          <div className="space-y-1">
            <span className="font-mono text-xs uppercase tracking-widest text-[#E30613] font-bold">[ 06 / EDGE PROFILING ]</span>
            <h2 className="text-2xl font-black text-zinc-950 tracking-tight">Edge Hardware Profile &amp; Dual-Tier Footprint</h2>
            <p className="text-xs text-zinc-500 font-mono">
              Measured via Microsoft ONNX Runtime (C++ Execution Engine, 4-Thread CPU, dynamic MatMul INT8)
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-5 rounded-md bg-white border border-zinc-200 shadow-xs space-y-2">
              <span className="text-xs font-mono text-zinc-500 font-bold uppercase tracking-wider block">Tier 1: Standalone Fast Path</span>
              <div className="text-xl font-black text-zinc-950 font-mono">22.05 MB (15.13 MB*)</div>
              <p className="text-xs text-zinc-600 leading-relaxed">
                Bundled directly inside native APK. Executes in <strong className="text-zinc-950">21.12 ms (&gt;45 FPS)</strong> on CPU. Covers &gt;88% of routine field queries.
              </p>
              <span className="text-[10px] text-zinc-400 font-mono block pt-1 border-t border-zinc-100">*15.13 MB lossless stream compression payload.</span>
            </div>

            <div className="p-5 rounded-md bg-white border border-zinc-200 shadow-xs space-y-2">
              <span className="text-xs font-mono text-zinc-500 font-bold uppercase tracking-wider block">Tier 2: On-Demand Companion</span>
              <div className="text-xl font-black text-zinc-950 font-mono">83.57 MB INT8</div>
              <p className="text-xs text-zinc-600 leading-relaxed">
                Downloaded on-demand for maximum precision on ambiguous queries. Combined footprint of <strong className="text-zinc-950">105.62 MB</strong> strictly complies with 110 MB edge budget.
              </p>
            </div>

            <div className="p-5 rounded-md bg-white border border-zinc-200 shadow-xs space-y-2">
              <span className="text-xs font-mono text-[#E30613] font-bold uppercase tracking-wider block">Fisher Projection Head</span>
              <div className="text-xl font-black text-zinc-950 font-mono">0.003 ms (&gt;10k FPS)</div>
              <p className="text-xs text-zinc-600 leading-relaxed">
                Evaluating the regularized discriminant linear projection requires only 9.8K FLOPs, adding virtually zero latency overhead to edge microprocessors.
              </p>
            </div>
          </div>

          {/* Hardware INT8 Benchmark Table */}
          <div className="rounded-md border border-zinc-200 overflow-hidden bg-white shadow-xs">
            <div className="p-4 bg-zinc-50 border-b border-zinc-200 flex flex-wrap items-center justify-between gap-2">
              <h3 className="font-mono font-bold text-zinc-950 text-xs uppercase tracking-wider">
                Table 5: Edge Hardware INT8 Quantization &amp; Latency Profile (ONNX Runtime, 4-Thread CPU)
              </h3>
              <span className="text-[10px] font-mono text-zinc-500 uppercase">Field Hardware Emulation (ARM Cortex-A76 / Mobile SoC)</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-zinc-100 text-zinc-700 font-mono border-b border-zinc-200 uppercase tracking-wider text-[11px]">
                  <tr>
                    <th className="p-3">Edge Configuration</th>
                    <th className="p-3">Parameters</th>
                    <th className="p-3">INT8 Footprint</th>
                    <th className="p-3">Latency (ms)</th>
                    <th className="p-3">Throughput</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-200 text-zinc-800 font-mono">
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans font-medium text-zinc-900">Tier 1: DINOv2 Small (Fast Path)</td>
                    <td className="p-3">22.1M</td>
                    <td className="p-3">22.05 (15.13*) MB</td>
                    <td className="p-3">21.12</td>
                    <td className="p-3 text-zinc-600">47.4 FPS</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans font-medium text-zinc-900">Tier 2: BioCLIP ViT-B (Deep Companion)</td>
                    <td className="p-3">86.6M</td>
                    <td className="p-3">83.57 MB</td>
                    <td className="p-3">67.61</td>
                    <td className="p-3 text-zinc-600">14.8 FPS</td>
                  </tr>
                  <tr className="hover:bg-zinc-50/50">
                    <td className="p-3 font-sans font-medium text-zinc-900">Regularized Fisher Alignment</td>
                    <td className="p-3 font-sans text-zinc-500">9.8K FLOPs</td>
                    <td className="p-3">&lt;0.01 MB</td>
                    <td className="p-3">0.003</td>
                    <td className="p-3 text-[#E30613] font-bold">&gt;10,000 FPS</td>
                  </tr>
                  <tr className="bg-zinc-50 font-bold text-zinc-950 border-t-2 border-zinc-300">
                    <td className="p-3 font-sans">BioDINO-Edge (Complete Native APK)</td>
                    <td className="p-3 font-sans text-zinc-600">Native Android</td>
                    <td className="p-3 text-[#E30613]">22.73 MB Total</td>
                    <td className="p-3 text-[#E30613]">&lt;22.00 ms</td>
                    <td className="p-3 text-[#E30613]">&gt;45.0 FPS</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="p-3 bg-zinc-50/50 border-t border-zinc-100 text-[11px] font-mono text-zinc-500 flex flex-wrap gap-4">
              <span>*15.13 MB lossless stream compression (Deflate) payload.</span>
              <span>• Total dual-tier working set (105.62 MB) strictly abides by 110 MB edge packaging budget.</span>
            </div>
          </div>
        </section>

        {/* 7. BIBTEX CITATION */}
        <section id="bibtex" className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <span className="font-mono text-xs uppercase tracking-widest text-[#E30613] font-bold">[ 07 / CITATION ]</span>
              <h2 className="text-2xl font-black text-zinc-950 tracking-tight">BibTeX Citation</h2>
            </div>

            <button
              onClick={handleCopyBibtex}
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-md bg-zinc-900 hover:bg-black text-white text-xs font-mono uppercase tracking-wider transition-colors shadow-xs"
            >
              {copiedBibtex ? (
                <>
                  <IconCheck className="w-3.5 h-3.5 text-emerald-400" />
                  <span className="text-emerald-400">Copied!</span>
                </>
              ) : (
                <>
                  <IconCopy className="w-3.5 h-3.5 text-zinc-400" />
                  <span>Copy BibTeX</span>
                </>
              )}
            </button>
          </div>

          <div className="p-4 rounded-md bg-zinc-950 border border-zinc-800 font-mono text-xs text-zinc-200 overflow-x-auto shadow-inner leading-relaxed">
            <pre>{bibtexCode}</pre>
          </div>
        </section>

      </div>

      {/* HIGH-RESOLUTION SCIENTIFIC FIGURE LIGHTBOX MODAL */}
      {activeLightbox && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/80 backdrop-blur-sm transition-all"
          onClick={() => setActiveLightbox(null)}
        >
          <div
            className="relative max-w-5xl w-full max-h-[92vh] flex flex-col bg-white border border-zinc-300 rounded-md overflow-hidden shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-200 bg-zinc-50">
              <span className="text-xs font-mono text-zinc-900 font-bold uppercase tracking-wider flex items-center space-x-2">
                <span className="w-2 h-2 rounded-full bg-[#E30613]" />
                <span>High-Resolution Diagram Inspector</span>
              </span>
              <button
                onClick={() => setActiveLightbox(null)}
                className="px-2.5 py-1 rounded bg-zinc-200 hover:bg-zinc-300 text-zinc-900 text-xs font-mono transition-colors"
                aria-label="Close modal"
              >
                ✕ Close (Esc)
              </button>
            </div>

            {/* Modal Image Viewport */}
            <div className="overflow-auto p-4 flex items-center justify-center bg-zinc-100 max-h-[72vh]">
              <img
                src={activeLightbox.src}
                alt={activeLightbox.alt}
                className="max-w-full max-h-[66vh] object-contain rounded border border-zinc-200 shadow-sm"
              />
            </div>

            {/* Modal Caption */}
            <div className="p-4 bg-white border-t border-zinc-200 text-xs text-zinc-700">
              <p>{activeLightbox.caption}</p>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}

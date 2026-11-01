"use client";

import React, { useState } from "react";
import { IconCpu, IconLeaf, IconShield, IconSparkles, IconCheck } from "./Icons";

interface Scenario {
  id: string;
  name: string;
  crop: string;
  tag: "PATHOLOGY" | "HEALTHY" | "OOD_REJECTED";
  scientificName: string;
  description: string;
  foliageScore: number;
  confidence: number;
  route: "Tier 1: Fast-Path DINOv2 (21ms)" | "Tier 2: Deep 896-d Consensus (68ms)" | "Gate Filtered (0ms)";
  latency: string;
  protocol: string;
  imagePrompt: string;
  probabilities: { name: string; score: number }[];
}

const SCENARIOS: Scenario[] = [
  {
    id: "scab",
    name: "Apple Scab",
    crop: "🍎 Apple (Malus domestica)",
    tag: "PATHOLOGY",
    scientificName: "Venturia inaequalis",
    description: "Dark olive-green velvety lesions expanding on the upper adaxial leaf lamina with chlorotic halos.",
    foliageScore: 0.924,
    confidence: 0.968,
    route: "Tier 1: Fast-Path DINOv2 (21ms)",
    latency: "14.2 ms (>55 FPS)",
    protocol: "Apply protective Captan 50WP (2.5 g/L) or Mancozeb at green-tip phenological stage. PHI: 14 days.",
    imagePrompt: "Olive-green fungal spots on apple leaf blade",
    probabilities: [
      { name: "Apple Scab", score: 98.4 },
      { name: "Apple Black Rot", score: 1.1 },
      { name: "Apple Cedar Rust", score: 0.3 },
      { name: "Apple Healthy", score: 0.2 },
    ],
  },
  {
    id: "esca",
    name: "Grape Esca (Black Measles)",
    crop: "🍇 Grape (Vitis vinifera)",
    tag: "PATHOLOGY",
    scientificName: "Phaeomoniella chlamydospora",
    description: "Acute interveinal necrosis forming characteristic 'tiger-stripe' chlorotic patterns while sparing main veins.",
    foliageScore: 0.891,
    confidence: 0.842,
    route: "Tier 2: Deep 896-d Consensus (68ms)",
    latency: "64.8 ms (Deep-Path)",
    protocol: "Sanitary winter pruning; seal wounds with biological Trichoderma paste; prune dead cordons.",
    imagePrompt: "Tiger-stripe interveinal necrosis on grape leaf",
    probabilities: [
      { name: "Grape Esca", score: 97.2 },
      { name: "Grape Black Rot", score: 2.1 },
      { name: "Grape Isariopsis", score: 0.5 },
      { name: "Grape Healthy", score: 0.2 },
    ],
  },
  {
    id: "late_blight",
    name: "Potato Late Blight",
    crop: "🥔 Potato (Solanum tuberosum)",
    tag: "PATHOLOGY",
    scientificName: "Phytophthora infestans",
    description: "Water-soaked irregular necrotic lesions surrounded by delicate white sporulating downy mildew margins.",
    foliageScore: 0.952,
    confidence: 0.974,
    route: "Tier 1: Fast-Path DINOv2 (21ms)",
    latency: "15.1 ms (>55 FPS)",
    protocol: "High epidemic alert! Systemic Metalaxyl-M (2 ml/L) or Cymoxanil spray within 24h. PHI: 7 days.",
    imagePrompt: "Water-soaked dark lesions on potato leaf",
    probabilities: [
      { name: "Potato Late Blight", score: 98.7 },
      { name: "Potato Early Blight", score: 1.0 },
      { name: "Potato Healthy", score: 0.3 },
    ],
  },
  {
    id: "healthy",
    name: "Apple Healthy Foliage",
    crop: "🌿 Apple (Malus domestica)",
    tag: "HEALTHY",
    scientificName: "Intact Lamina",
    description: "Vibrant emerald mesophyll, intact leaf cuticle, smooth margin, devoid of fungal pustules or chlorosis.",
    foliageScore: 0.961,
    confidence: 0.991,
    route: "Tier 1: Fast-Path DINOv2 (21ms)",
    latency: "13.9 ms (>55 FPS)",
    protocol: "Optimal foliar health detected. Maintain baseline preventive IPM bio-monitoring schedule.",
    imagePrompt: "Healthy smooth green apple leaf lamina",
    probabilities: [
      { name: "Apple Healthy", score: 99.4 },
      { name: "Apple Scab", score: 0.3 },
      { name: "Apple Black Rot", score: 0.3 },
    ],
  },
  {
    id: "ood",
    name: "Non-Foliar Subject (OOD Test)",
    crop: "🚫 Non-Vegetative Object",
    tag: "OOD_REJECTED",
    scientificName: "Manifold Outlier",
    description: "Camera pointed at indoor desktop object / dark background without valid botanical leaf structure.",
    foliageScore: 0.218,
    confidence: 0.0,
    route: "Gate Filtered (0ms)",
    latency: "0.2 ms (Gate Filter)",
    protocol: "Classification aborted! Foliage score (0.22) is below valid threshold (0.40). Align leaf in reticle.",
    imagePrompt: "Non-leaf background test",
    probabilities: [
      { name: "REJECTED (OOD)", score: 100.0 },
    ],
  },
];

export default function InteractiveDemo() {
  const [selectedId, setSelectedId] = useState<string>("scab");
  const [isScanning, setIsScanning] = useState<boolean>(false);
  const [customImage, setCustomImage] = useState<string | null>(null);

  const scenario = SCENARIOS.find((s) => s.id === selectedId) || SCENARIOS[0];

  const handleSelectScenario = (id: string) => {
    setIsScanning(true);
    setSelectedId(id);
    setCustomImage(null);
    setTimeout(() => {
      setIsScanning(false);
    }, 400);
  };

  const handleCustomUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const url = URL.createObjectURL(file);
      setCustomImage(url);
      setIsScanning(true);
      setTimeout(() => {
        setIsScanning(false);
      }, 600);
    }
  };

  return (
    <section id="live-demo" className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <div className="space-y-1">
          <div className="inline-flex items-center space-x-2 text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>Interactive Client-Side Engine Demo</span>
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            Live BioDINO-Edge Foliar Inference Simulator
          </h2>
        </div>
        <p className="text-xs text-slate-400 max-w-sm">
          Simulating real-time DINOv2 feature extraction, analytical Fisher-LDA alignment, and Shannon uncertainty routing.
        </p>
      </div>

      <div className="p-6 sm:p-8 rounded-2xl bg-slate-900/90 border border-emerald-500/30 shadow-2xl space-y-6">
        
        {/* Scenario Selector Pills */}
        <div className="space-y-2">
          <label className="text-xs font-mono text-slate-400 uppercase tracking-wider block">
            Select Test Sample or Diagnostic Regime:
          </label>
          <div className="flex flex-wrap gap-2">
            {SCENARIOS.map((s) => (
              <button
                key={s.id}
                onClick={() => handleSelectScenario(s.id)}
                className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all duration-200 btn-press ${
                  selectedId === s.id && !customImage
                    ? "bg-emerald-500 text-slate-950 font-bold shadow-md shadow-emerald-500/20 scale-105"
                    : "bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700/60"
                }`}
              >
                {s.name}
              </button>
            ))}

            <label className="px-3 py-1.5 rounded-xl text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/60 cursor-pointer flex items-center space-x-1.5">
              <span>📷 Test Custom Image</span>
              <input type="file" accept="image/*" onChange={handleCustomUpload} className="hidden" />
            </label>
          </div>
        </div>

        {/* Live Simulator Viewport */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
          
          {/* Simulated Leaf Scan Viewport */}
          <div className="lg:col-span-5 relative aspect-square rounded-2xl bg-slate-950 border border-slate-800 overflow-hidden flex flex-col items-center justify-center p-4">
            {/* Background Texture / Custom Upload */}
            {customImage ? (
              <img src={customImage} alt="User Foliage" className="absolute inset-0 w-full h-full object-cover opacity-80" />
            ) : (
              <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-tr from-slate-950 via-slate-900 to-emerald-950/30">
                <IconLeaf className="w-32 h-32 text-emerald-500/10" />
              </div>
            )}

            {/* Scanning Laser Line */}
            {isScanning && (
              <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_14px_#10b981] animate-laser z-20" />
            )}

            {/* Target Reticle Overlay */}
            <div className="relative z-10 w-44 h-44 rounded-3xl border-2 border-emerald-500/60 flex flex-col items-center justify-center backdrop-blur-[1px]">
              <div className="w-16 h-16 rounded-full border border-dashed border-emerald-400/80 flex items-center justify-center font-mono text-xs text-emerald-400">
                {isScanning ? "..." : `${Math.round(scenario.confidence * 100)}%`}
              </div>
              <span className="text-[10px] font-mono text-slate-400 mt-2 bg-slate-950/80 px-2 py-0.5 rounded">
                896-d Manifold
              </span>
            </div>

            {/* Real-time Status Capsule */}
            <div className="absolute bottom-3 inset-x-4 flex items-center justify-between text-[11px] font-mono bg-slate-900/90 border border-slate-800 p-2 rounded-xl z-20">
              <span className="text-slate-400">Latency:</span>
              <span className="text-emerald-400 font-bold">{scenario.latency}</span>
            </div>
          </div>

          {/* Diagnostic Analytics Panel */}
          <div className="lg:col-span-7 space-y-4">
            
            {/* Top Result Banner */}
            <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 flex items-center justify-between">
              <div>
                <span className="text-[11px] font-mono text-slate-400 block">{scenario.crop}</span>
                <span className="text-lg font-bold text-white flex items-center space-x-2">
                  <span>{scenario.name}</span>
                </span>
                <span className="text-xs text-slate-400 italic block">Pathogen: {scenario.scientificName}</span>
              </div>

              <div>
                {scenario.tag === "PATHOLOGY" && (
                  <span className="px-3 py-1 rounded-full bg-red-500/20 text-red-400 border border-red-500/30 text-xs font-mono font-bold">
                    PATHOLOGY
                  </span>
                )}
                {scenario.tag === "HEALTHY" && (
                  <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-mono font-bold">
                    HEALTHY
                  </span>
                )}
                {scenario.tag === "OOD_REJECTED" && (
                  <span className="px-3 py-1 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30 text-xs font-mono font-bold">
                    REJECTED (OOD)
                  </span>
                )}
              </div>
            </div>

            {/* Gating Metrics Bars */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-slate-950/50 border border-slate-800 space-y-1.5">
                <div className="flex items-center justify-between text-slate-300 font-mono">
                  <span>Foliage Manifold Gate:</span>
                  <span className={scenario.foliageScore >= 0.40 ? "text-emerald-400 font-bold" : "text-red-400 font-bold"}>
                    {scenario.foliageScore.toFixed(3)} {scenario.foliageScore >= 0.40 ? "✓" : "✗"}
                  </span>
                </div>
                <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${scenario.foliageScore >= 0.40 ? "bg-emerald-400" : "bg-red-400"}`}
                    style={{ width: `${Math.min(100, scenario.foliageScore * 100)}%` }}
                  />
                </div>
                <span className="text-[10px] text-slate-500 block">Threshold: &ge; 0.40 for valid foliage</span>
              </div>

              <div className="p-3 rounded-xl bg-slate-950/50 border border-slate-800 space-y-1.5">
                <div className="flex items-center justify-between text-slate-300 font-mono">
                  <span>Shannon Confidence:</span>
                  <span className="text-cyan-400 font-bold">{(scenario.confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-cyan-400"
                    style={{ width: `${Math.min(100, scenario.confidence * 100)}%` }}
                  />
                </div>
                <span className="text-[10px] text-slate-500 block">Margin-entropy certainty formula</span>
              </div>
            </div>

            {/* Decision Routing Capsule */}
            <div className="p-3 rounded-xl bg-slate-950/50 border border-slate-800 space-y-1">
              <span className="text-[11px] font-mono text-slate-400 block">Executed Architectural Path:</span>
              <span className="text-xs font-semibold text-slate-200 flex items-center space-x-2">
                <IconCpu className="w-4 h-4 text-emerald-400" />
                <span>{scenario.route}</span>
              </span>
            </div>

            {/* Prescribed Agrochemical Protocol */}
            <div className="p-3 rounded-xl bg-emerald-950/30 border border-emerald-500/30 text-xs text-slate-200 space-y-1">
              <span className="font-semibold text-emerald-300 block font-mono text-[11px]">
                Prescribed Agronomic Action Protocol:
              </span>
              <p className="text-slate-300 leading-relaxed text-[11px]">{scenario.protocol}</p>
            </div>

            {/* Class Probability Distribution */}
            <div className="space-y-1.5 pt-1">
              <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
                Calibrated Temperature Scaled Posteriors (T=0.50):
              </span>
              <div className="space-y-1 text-xs">
                {scenario.probabilities.map((p, i) => (
                  <div key={i} className="flex items-center justify-between font-mono text-[11px] text-slate-300">
                    <span>{p.name}</span>
                    <span className="text-emerald-400">{p.score.toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>

      </div>
    </section>
  );
}


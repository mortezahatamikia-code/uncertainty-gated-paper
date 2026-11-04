import React from "react";
import Link from "next/link";
import type { Metadata } from "next";
import { IconPaper, IconDownload, IconChevronRight, IconArrowLeft } from "@/components/Icons";

export const metadata: Metadata = {
  title: "Scientific Publications & Research Monographs | Reyhane Javidi Alsaadi",
  description:
    "Peer-reviewed scientific manuscripts and preprints by Reyhane Javidi Alsaadi in Computer Vision, Vision Foundation Models, and Few-Shot Edge AI.",
  alternates: {
    canonical: "https://reyhane-code.github.io/research/",
  },
  openGraph: {
    title: "Scientific Publications & Research Monographs | Reyhane Javidi Alsaadi",
    description:
      "Peer-reviewed scientific manuscripts and preprints in Vision Foundation Models, Few-Shot Learning, and Edge AI.",
    url: "https://reyhane-code.github.io/research/",
    type: "website",
    images: [
      {
        url: "https://reyhane-code.github.io/figures/fig_architecture.png",
        width: 1200,
        height: 630,
        alt: "Scientific Publications - Reyhane Javidi Alsaadi",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Scientific Publications & Preprints | Reyhane Javidi Alsaadi",
    description: "Vision Foundation Models and Few-Shot Learning for Edge Systems.",
    images: ["https://reyhane-code.github.io/figures/fig_architecture.png"],
  },
};

export default function ResearchCatalogPage() {
  return (
    <main className="min-h-screen bg-[#fafaf9] text-zinc-900 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      <div className="space-y-4 border-b border-zinc-200 pb-6">
        <Link
          href="/"
          className="inline-flex items-center space-x-2 text-xs font-mono text-zinc-500 hover:text-zinc-950 transition-colors"
        >
          <IconArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Author CV &amp; Dossier</span>
        </Link>
        <div className="space-y-1">
          <div className="inline-flex items-center space-x-2 text-xs font-mono text-zinc-700">
            <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
            <span>01 // RESEARCH MONOGRAPHS &amp; PREPRINTS</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold text-zinc-950 tracking-tight">
            Scientific Publications &amp; Preprints
          </h1>
        </div>
        <p className="text-sm text-zinc-600 max-w-2xl leading-relaxed">
          Peer-reviewed scientific manuscripts and preprints by Reyhane Javidi Alsaadi in Computer Vision, Vision Foundation Models, and Edge AI.
        </p>
      </div>

      <div className="space-y-6">
        {/* Featured Paper 1: BioDINO-Edge */}
        <div className="p-6 sm:p-8 border border-zinc-200 bg-white space-y-5 shadow-xs">
          <div className="flex flex-wrap items-center gap-2">
            <span className="px-2.5 py-0.5 rounded bg-zinc-950 text-white text-xs font-mono font-medium">
              Lead / First Author
            </span>
            <span className="px-2.5 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-xs font-mono">
              Target: IEEE T-PAMI / CVPR
            </span>
            <span className="px-2.5 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-xs font-mono">
              Few-Shot Learning
            </span>
          </div>

          <div className="space-y-2 border-b border-zinc-200 pb-4">
            <h2 className="text-2xl font-bold text-zinc-950 leading-snug tracking-tight">
              BioDINO-Edge: Biologically-Grounded Multi-Scale Vision Foundation Models for Trustworthy Few-Shot Plant Pathology on Resource-Constrained Hardware
            </h2>
            <p className="text-sm text-zinc-800 font-medium">
              <strong className="text-zinc-950 underline decoration-zinc-400">Reyhane Javidi Alsaadi</strong> and Mohammad Reza Samad Zadeh
            </p>
            <p className="text-xs text-zinc-500 font-mono">
              Department of Computer Engineering, Dr. Shariaty Technical University, Tehran, Iran
            </p>
          </div>

          <p className="text-xs sm:text-sm text-zinc-600 leading-relaxed">
            Unites self-supervised spatial patch modeling (DINOv2 Small) with organismal vision-language hierarchies (BioCLIP ViT-B). Derives analytical Ledoit-Wolf covariance shrinkage over the joint 896-d manifold, Soft-Anchored Transductive Self-Calibration, and a predictive Shannon uncertainty gate. Reaches 98.72% peak accuracy on PlantVillage and 83.61% on PlantDoc in-the-wild (+13.00% over 2026 SOTA).
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-4 border border-zinc-200 divide-x divide-y sm:divide-y-0 divide-zinc-200 bg-white text-center">
            <div className="p-3.5">
              <div className="text-lg font-bold text-zinc-950 font-mono">98.72%</div>
              <div className="text-[10px] text-zinc-500 font-mono uppercase mt-0.5">Peak Accuracy</div>
            </div>
            <div className="p-3.5">
              <div className="text-lg font-bold text-zinc-950 font-mono">83.61%</div>
              <div className="text-[10px] text-zinc-500 font-mono uppercase mt-0.5">PlantDoc SOTA</div>
            </div>
            <div className="p-3.5">
              <div className="text-lg font-bold text-zinc-950 font-mono">22.05 MB</div>
              <div className="text-[10px] text-zinc-500 font-mono uppercase mt-0.5">INT8 Model</div>
            </div>
            <div className="p-3.5">
              <div className="text-lg font-bold text-zinc-950 font-mono">&lt; 22 ms</div>
              <div className="text-[10px] text-zinc-500 font-mono uppercase mt-0.5">Edge CPU Latency</div>
            </div>
          </div>

          <div className="pt-2 flex flex-wrap gap-2.5">
            <Link
              href="/research/biodino-edge/"
              className="inline-flex items-center space-x-2 px-4 py-2 rounded bg-zinc-950 text-white font-medium text-xs hover:bg-zinc-800 transition-colors"
            >
              <IconPaper className="w-3.5 h-3.5" />
              <span>Explore Interactive Paper Page</span>
              <IconChevronRight className="w-3.5 h-3.5" />
            </Link>
            <a
              href="/biodino_edge_paper.pdf"
              target="_blank"
              className="inline-flex items-center space-x-2 px-4 py-2 rounded bg-white text-zinc-900 border border-zinc-300 hover:border-zinc-950 hover:bg-zinc-50 font-medium text-xs transition-colors"
            >
              <IconDownload className="w-3.5 h-3.5 text-zinc-600" />
              <span>Download PDF (4.4 MB)</span>
            </a>
          </div>
        </div>
      </div>
    </main>
  );
}


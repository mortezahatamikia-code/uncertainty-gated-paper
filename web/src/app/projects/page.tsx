import React from "react";
import Link from "next/link";
import { IconApp, IconChevronRight, IconArrowLeft, IconGithub } from "@/components/Icons";

export default function ProjectsCatalogPage() {
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
            <span>02 // OPEN-SOURCE SOFTWARE &amp; SYSTEMS</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold text-zinc-950 tracking-tight">
            Open-Source Software &amp; Systems
          </h1>
        </div>
        <p className="text-sm text-zinc-600 max-w-2xl leading-relaxed">
          Production-grade engineering software, mobile AI applications, and embedded tools engineered by Reyhane Javidi Alsaadi.
        </p>
      </div>

      <div className="space-y-6">
        {/* Featured Project 1: BioDINO-Edge Android */}
        <div className="p-6 sm:p-8 border border-zinc-200 bg-white space-y-5 shadow-xs">
          <div className="flex flex-wrap items-center gap-2">
            <span className="px-2.5 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-xs font-mono font-medium">
              Kotlin 2.0 &amp; Jetpack Compose
            </span>
            <span className="px-2.5 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-xs font-mono">
              ONNX Runtime Mobile NNAPI
            </span>
            <span className="px-2.5 py-0.5 rounded bg-zinc-950 text-white text-xs font-mono font-medium">
              22.7 MB Standalone APK
            </span>
          </div>

          <div className="space-y-2 border-b border-zinc-200 pb-4">
            <h2 className="text-2xl font-bold text-zinc-950 leading-snug tracking-tight">
              BioDINO-Edge Android: 100% Offline Foliar Disease Scanner
            </h2>
            <p className="text-sm text-zinc-600 font-mono">
              Native Android edge implementation of the BioDINO-Edge few-shot vision foundation model
            </p>
          </div>

          <p className="text-xs sm:text-sm text-zinc-600 leading-relaxed">
            Delivers sustained 55+ FPS on ARM Cortex mobile processors with a zero-allocation <code>PreallocatedTensor</code> buffer pipeline preventing Garbage Collector frame drops. Integrates a 3-layer safety gate (Luminance check &lt;22 lux, Foliage Manifold score &ge;0.40, Shannon Margin-Entropy confidence) to eliminate closed-world false positives on dark frames and non-foliar objects.
          </p>

          <div className="pt-2 flex flex-wrap gap-2.5">
            <Link
              href="/projects/biodino-edge-android/"
              className="inline-flex items-center space-x-2 px-4 py-2 rounded bg-zinc-950 text-white font-medium text-xs hover:bg-zinc-800 transition-colors"
            >
              <IconApp className="w-3.5 h-3.5" />
              <span>Explore Android App Showcase</span>
              <IconChevronRight className="w-3.5 h-3.5" />
            </Link>
            <a
              href="https://github.com/reyhane-code"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center space-x-2 px-4 py-2 rounded bg-white text-zinc-900 border border-zinc-300 hover:border-zinc-950 hover:bg-zinc-50 font-medium text-xs transition-colors"
            >
              <IconGithub className="w-3.5 h-3.5 text-zinc-600" />
              <span>GitHub Repository</span>
            </a>
          </div>
        </div>
      </div>
    </main>
  );
}


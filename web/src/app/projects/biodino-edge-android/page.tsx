"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  IconApp,
  IconPaper,
  IconDownload,
  IconExternal,
  IconGithub,
  IconCpu,
  IconLeaf,
  IconShield,
  IconCheck,
  IconSparkles,
  IconArrowLeft,
  IconCopy,
} from "@/components/Icons";

export default function BioDinoEdgeAndroidPage() {
  const [copiedCmd, setCopiedCmd] = useState<string | null>(null);

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedCmd(id);
    setTimeout(() => setCopiedCmd(null), 2000);
  };

  return (
    <main className="min-h-screen pb-24 bg-[#fafaf9] text-zinc-900">
      {/* Breadcrumb & Navigation */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        <Link
          href="/"
          className="inline-flex items-center space-x-2 text-xs font-mono uppercase tracking-wider text-zinc-500 hover:text-black transition-colors"
        >
          <IconArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Author CV &amp; Portfolio</span>
        </Link>
      </div>

      {/* HERO SECTION */}
      <section className="pt-8 pb-16 border-b border-zinc-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            
            {/* Left Column: Product Info */}
            <div className="lg:col-span-7 space-y-6">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded bg-zinc-100 border border-zinc-200 text-zinc-800 text-xs font-mono font-semibold tracking-wider uppercase">
                <span className="w-1.5 h-1.5 rounded-full bg-[#E30613]" />
                <span>Open-Source Native Android • 100% Offline AI Scanner</span>
              </div>

              <div className="space-y-3">
                <h1 className="text-4xl sm:text-5xl font-black tracking-tight text-zinc-950 leading-tight">
                  BioDINO-Edge{" "}
                  <span className="underline decoration-[#E30613] decoration-4 underline-offset-8">
                    Mobile
                  </span>
                </h1>
                <p className="text-lg text-zinc-700 font-medium">
                  Zero-Latency On-Device Few-Shot Foliar Diagnostics for Precision Agriculture
                </p>
              </div>

              <p className="text-sm text-zinc-700 leading-relaxed max-w-xl">
                A native Android application translating the <strong>BioDINO-Edge foundation model</strong> into the hands of farmers and plant pathologists. Runs 100% offline with zero cloud dependency, featuring a <strong>Zero-GC direct memory pipeline</strong>, <strong>NNAPI hardware acceleration</strong>, and a <strong>3-layer security gate</strong> against dark frames and non-foliar objects.
              </p>

              {/* Action Buttons */}
              <div className="flex flex-wrap gap-3 pt-2">
                <a
                  href="/biodino-edge-v1.0.0.apk"
                  download="biodino-edge-v1.0.0.apk"
                  className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-md bg-black text-white font-mono text-xs uppercase tracking-wider font-semibold hover:bg-zinc-800 shadow-xs transition-colors"
                >
                  <IconDownload className="w-4 h-4" />
                  <span>Download APK v1.0.0 (Release - 22.7 MB)</span>
                </a>

                <Link
                  href="/research/biodino-edge/"
                  className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-md bg-white text-zinc-900 font-mono text-xs uppercase tracking-wider font-medium hover:bg-zinc-100 border border-zinc-300 shadow-xs transition-colors"
                >
                  <IconPaper className="w-4 h-4 text-zinc-600" />
                  <span>Read Scientific Paper (98.7%)</span>
                </Link>

                <a
                  href="https://github.com/reyhane-code"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-md bg-white text-zinc-900 font-mono text-xs uppercase tracking-wider font-medium hover:bg-zinc-100 border border-zinc-300 shadow-xs transition-colors"
                >
                  <IconGithub className="w-4 h-4 text-zinc-600" />
                  <span>GitHub Repository</span>
                </a>
              </div>

              {/* Specs Pills */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-zinc-200 max-w-xl">
                <div className="p-3 rounded-md bg-white border border-zinc-200 shadow-xs">
                  <div className="text-lg font-black text-zinc-950 font-mono">22.73 MB</div>
                  <div className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">Total Release APK</div>
                </div>
                <div className="p-3 rounded-md bg-white border border-zinc-200 shadow-xs">
                  <div className="text-lg font-black text-zinc-950 font-mono">&gt; 55 FPS</div>
                  <div className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">Live Viewfinder</div>
                </div>
                <div className="p-3 rounded-md bg-white border border-zinc-200 shadow-xs">
                  <div className="text-lg font-black text-zinc-950 font-mono">0 MB GC</div>
                  <div className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">Direct Buffer</div>
                </div>
                <div className="p-3 rounded-md bg-white border border-zinc-200 shadow-xs">
                  <div className="text-lg font-black text-[#E30613] font-mono">100% Offline</div>
                  <div className="text-[11px] font-mono uppercase tracking-wider text-zinc-500">Zero Network</div>
                </div>
              </div>
            </div>

            {/* Right Column: Interactive Phone Mockup Frame */}
            <div className="lg:col-span-5 flex justify-center">
              <div className="relative w-72 sm:w-80 rounded-[40px] p-3.5 bg-zinc-950 shadow-xl border border-zinc-300">
                {/* Speaker Grill & Dynamic Island Notch */}
                <div className="absolute top-6 left-1/2 -translate-x-1/2 w-28 h-5 bg-black rounded-full flex items-center justify-center space-x-2 z-20">
                  <div className="w-2.5 h-2.5 rounded-full bg-zinc-900 border border-zinc-800" />
                  <div className="w-10 h-1 rounded-full bg-zinc-900" />
                </div>

                {/* Screen Content Container */}
                <div className="relative w-full aspect-[9/19] rounded-[32px] overflow-hidden bg-zinc-900 border border-zinc-800 flex flex-col justify-between p-4 pt-10 text-white">
                  
                  {/* Top Header Mockup */}
                  <div className="flex items-center justify-between z-10">
                    <div className="flex items-center space-x-1.5">
                      <div className="w-2 h-2 rounded-full bg-[#E30613]" />
                      <span className="text-[11px] font-mono font-bold tracking-wider text-zinc-100 uppercase">BioDINO EDGE</span>
                    </div>
                    <div className="flex items-center space-x-1.5 text-[10px] font-mono text-zinc-300 bg-zinc-800 px-2 py-0.5 rounded border border-zinc-700">
                      <span>NNAPI</span>
                      <span className="text-emerald-400">14ms</span>
                    </div>
                  </div>

                  {/* Camera Reticle & Laser Mockup */}
                  <div className="relative my-auto flex flex-col items-center justify-center">
                    <div className="relative w-44 h-44 rounded-2xl border border-zinc-600 flex items-center justify-center bg-black/40">
                      {/* Scanning Laser Line */}
                      <div className="absolute w-full h-0.5 bg-gradient-to-r from-transparent via-[#E30613] to-transparent shadow-[0_0_8px_#E30613]" />
                      
                      {/* Center Focus Reticle */}
                      <div className="w-12 h-12 rounded-full border border-dashed border-zinc-400 flex items-center justify-center text-[10px] font-mono text-white">
                        98%
                      </div>

                      {/* Corner Brackets */}
                      <div className="absolute top-2 left-2 w-3 h-3 border-t-2 border-l-2 border-white" />
                      <div className="absolute top-2 right-2 w-3 h-3 border-t-2 border-r-2 border-white" />
                      <div className="absolute bottom-2 left-2 w-3 h-3 border-b-2 border-l-2 border-white" />
                      <div className="absolute bottom-2 right-2 w-3 h-3 border-b-2 border-r-2 border-white" />
                    </div>

                    <div className="mt-3 px-3 py-1 rounded bg-black/80 text-white border border-zinc-700 text-[10px] font-mono uppercase tracking-wider">
                      LEAF LOCKED • Apple Scab
                    </div>
                  </div>

                  {/* Bottom Diagnostic Card Mockup */}
                  <div className="p-3.5 rounded-xl bg-zinc-950/95 border border-zinc-800 space-y-2 z-10 shadow-lg">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-white flex items-center space-x-1.5 font-mono">
                        <span>🍎 Apple Scab</span>
                      </span>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#E30613] text-white font-bold">
                        PATHOLOGY
                      </span>
                    </div>
                    <p className="text-[10px] text-zinc-400 line-clamp-2">
                      Fungal lesion caused by <em>Venturia inaequalis</em>. Recommend protective Captan or Mancozeb spray.
                    </p>
                    <div className="pt-1 flex items-center justify-between text-[9px] font-mono text-zinc-400 border-t border-zinc-800">
                      <span>Confidence: 98.4%</span>
                      <span>Latency: 14.2 ms</span>
                    </div>
                  </div>

                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* APP INTERFACE GALLERY PLACEHOLDERS */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-12 border-b border-zinc-200">
        <div className="space-y-1">
          <span className="font-mono text-xs uppercase tracking-widest text-[#E30613] font-bold">[ 01 / MOBILE CAPABILITIES ]</span>
          <h2 className="text-3xl font-black text-zinc-950 tracking-tight">Application Interface &amp; Field Capabilities</h2>
          <p className="text-xs text-zinc-500 font-mono">
            Ergonomic botanical design tested under direct sunlight with progressive disclosure of agronomic insights
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          
          {/* Card 1: Viewfinder */}
          <div className="p-5 rounded-md bg-white border border-zinc-200 space-y-3 shadow-xs">
            <div className="aspect-[9/16] rounded bg-zinc-50 border border-dashed border-zinc-300 flex flex-col items-center justify-center p-4 text-center group hover:border-black transition-colors">
              <IconApp className="w-8 h-8 text-zinc-700 mb-2" />
              <span className="text-xs font-bold text-zinc-900 font-mono">1. Real-Time Viewfinder</span>
              <span className="text-[10px] text-zinc-500 mt-1">Dynamic Laser Reticle &amp; Locking Ring (&gt;55 FPS)</span>
              <span className="mt-4 px-2 py-1 rounded bg-zinc-200 text-[10px] font-mono text-zinc-700">
                Screenshot Frame Ready
              </span>
            </div>
            <h3 className="font-bold text-zinc-950 text-sm font-mono">Real-Time CameraX Stream</h3>
            <p className="text-xs text-zinc-600 leading-relaxed">
              640x640 RGBA_8888 continuous stream with EMA confidence smoothing preventing hand jitter.
            </p>
          </div>

          {/* Card 2: 3-Layer Gate */}
          <div className="p-5 rounded-md bg-white border border-zinc-200 space-y-3 shadow-xs">
            <div className="aspect-[9/16] rounded bg-zinc-50 border border-dashed border-zinc-300 flex flex-col items-center justify-center p-4 text-center group hover:border-black transition-colors">
              <IconShield className="w-8 h-8 text-zinc-700 mb-2" />
              <span className="text-xs font-bold text-zinc-900 font-mono">2. 3-Layer Security Gate</span>
              <span className="text-[10px] text-zinc-500 mt-1">Luminance &amp; Foliage Manifold OOD Rejection</span>
              <span className="mt-4 px-2 py-1 rounded bg-zinc-200 text-[10px] font-mono text-zinc-700">
                Screenshot Frame Ready
              </span>
            </div>
            <h3 className="font-bold text-zinc-950 text-sm font-mono">OOD &amp; Dark Lens Rejection</h3>
            <p className="text-xs text-zinc-600 leading-relaxed">
              Instant rejection if lens is covered (&lt;22 lux) or pointed at non-leaf subjects (cosine score &lt;0.40).
            </p>
          </div>

          {/* Card 3: Diagnostic Card */}
          <div className="p-5 rounded-md bg-white border border-zinc-200 space-y-3 shadow-xs">
            <div className="aspect-[9/16] rounded bg-zinc-50 border border-dashed border-zinc-300 flex flex-col items-center justify-center p-4 text-center group hover:border-black transition-colors">
              <IconLeaf className="w-8 h-8 text-zinc-700 mb-2" />
              <span className="text-xs font-bold text-zinc-900 font-mono">3. Diagnostic Card &amp; Atlas</span>
              <span className="text-[10px] text-zinc-500 mt-1">Progressive Disclosure &amp; Treatment Advice</span>
              <span className="mt-4 px-2 py-1 rounded bg-zinc-200 text-[10px] font-mono text-zinc-700">
                Screenshot Frame Ready
              </span>
            </div>
            <h3 className="font-bold text-zinc-950 text-sm font-mono">Phytopathological Advice</h3>
            <p className="text-xs text-zinc-600 leading-relaxed">
              Provides immediate fungicide protocols alongside expandable scientific pathogen details.
            </p>
          </div>

          {/* Card 4: Field Utilities */}
          <div className="p-5 rounded-md bg-white border border-zinc-200 space-y-3 shadow-xs">
            <div className="aspect-[9/16] rounded bg-zinc-50 border border-dashed border-zinc-300 flex flex-col items-center justify-center p-4 text-center group hover:border-black transition-colors">
              <IconCpu className="w-8 h-8 text-zinc-700 mb-2" />
              <span className="text-xs font-bold text-zinc-900 font-mono">4. Live 5-Shot Enrollment</span>
              <span className="text-[10px] text-zinc-500 mt-1">Dosage Calculator &amp; Weather Window</span>
              <span className="mt-4 px-2 py-1 rounded bg-zinc-200 text-[10px] font-mono text-zinc-700">
                Screenshot Frame Ready
              </span>
            </div>
            <h3 className="font-bold text-zinc-950 text-sm font-mono">In-Field 5-Shot Registration</h3>
            <p className="text-xs text-zinc-600 leading-relaxed">
              Enables farmers to define novel unseen disease classes on the fly with 5 snapshots in the field.
            </p>
          </div>

        </div>
      </section>

      {/* TECHNICAL ARCHITECTURE & PERFORMANCE DETAILS */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-12">
        <div className="space-y-1">
          <span className="font-mono text-xs uppercase tracking-widest text-[#E30613] font-bold">[ 02 / EDGE ARCHITECTURE ]</span>
          <h2 className="text-2xl font-black text-zinc-950 tracking-tight">Mobile Engineering &amp; Edge Optimization Highlights</h2>
          <p className="text-xs text-zinc-500 font-mono">Key architectural decisions powering sustained 55+ FPS on ARM Cortex processors</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 rounded-md bg-white border border-zinc-200 space-y-3 shadow-xs">
            <div className="text-xs font-mono text-zinc-500 uppercase font-bold tracking-wider">1. Zero GC Pipeline</div>
            <h3 className="text-base font-bold text-zinc-950 font-mono">Preallocated Direct Memory</h3>
            <p className="text-xs text-zinc-700 leading-relaxed">
              Allocates a single native <code>ByteBuffer.allocateDirect(1 * 3 * 224 * 224 * 4)</code> at launch. Pixel values are extracted via direct bitwise shifting (<code>shr</code>, <code>and</code>), eliminating Garbage Collector churn and dropped frames entirely.
            </p>
          </div>

          <div className="p-6 rounded-md bg-white border border-zinc-200 space-y-3 shadow-xs">
            <div className="text-xs font-mono text-[#E30613] uppercase font-bold tracking-wider">2. Hardware Acceleration</div>
            <h3 className="text-base font-bold text-zinc-950 font-mono">NNAPI + CPU 4-Thread Fallback</h3>
            <p className="text-xs text-zinc-700 leading-relaxed">
              Initializes Microsoft ONNX Runtime Mobile with the Android Neural Networks API (NNAPI) targeting Qualcomm Hexagon NPU / Adreno GPU. Safely falls back to a 4-thread CPU session if the vendor driver lacks operator support.
            </p>
          </div>

          <div className="p-6 rounded-md bg-white border border-zinc-200 space-y-3 shadow-xs">
            <div className="text-xs font-mono text-zinc-500 uppercase font-bold tracking-wider">3. Model Packaging</div>
            <h3 className="text-base font-bold text-zinc-950 font-mono">22.7 MB APK (73.3% Compression)</h3>
            <p className="text-xs text-zinc-700 leading-relaxed">
              Quantized dynamically with <code>op_types_to_quantize=[&apos;MatMul&apos;]</code>, preserving the initial patch projection as standard FP32 to resolve the Android <code>ConvInteger</code> runtime crash.
            </p>
          </div>
        </div>

        {/* DEVELOPER SETUP & BUILD GUIDE */}
        <div className="rounded-md border border-zinc-200 bg-white p-6 sm:p-8 space-y-6 shadow-xs">
          <div className="space-y-1">
            <span className="font-mono text-xs uppercase tracking-widest text-[#E30613] font-bold">[ 03 / DEVELOPER SETUP &amp; ADB ]</span>
            <h3 className="text-lg font-black text-zinc-950 flex items-center space-x-2">
              <IconGithub className="w-5 h-5 text-zinc-700" />
              <span>Building from Source &amp; ADB Installation</span>
            </h3>
            <p className="text-xs text-zinc-500 font-mono">
              Prerequisites: JDK 17 (Adoptium / OpenJDK) and Android SDK Platform 34
            </p>
          </div>

          <div className="space-y-4">
            <div>
              <div className="flex items-center justify-between text-xs text-zinc-600 font-mono mb-1">
                <span>1. Compile Lightweight Release APK (22.7 MB):</span>
                <button
                  onClick={() => copyToClipboard("cd android_app; .\\gradlew.bat assembleRelease", "cmd1")}
                  className="text-black hover:underline flex items-center space-x-1 font-bold"
                >
                  {copiedCmd === "cmd1" ? <IconCheck className="w-3.5 h-3.5 text-emerald-600" /> : <IconCopy className="w-3.5 h-3.5" />}
                  <span>{copiedCmd === "cmd1" ? "Copied" : "Copy"}</span>
                </button>
              </div>
              <div className="p-3.5 rounded-md bg-zinc-950 font-mono text-xs text-zinc-200 border border-zinc-800 shadow-inner">
                <code>cd android_app; .\gradlew.bat assembleRelease</code>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between text-xs text-zinc-600 font-mono mb-1">
                <span>2. Install via ADB with USB Debugging enabled:</span>
                <button
                  onClick={() => copyToClipboard("adb install -r app/build/outputs/apk/release/app-release.apk", "cmd2")}
                  className="text-black hover:underline flex items-center space-x-1 font-bold"
                >
                  {copiedCmd === "cmd2" ? <IconCheck className="w-3.5 h-3.5 text-emerald-600" /> : <IconCopy className="w-3.5 h-3.5" />}
                  <span>{copiedCmd === "cmd2" ? "Copied" : "Copy"}</span>
                </button>
              </div>
              <div className="p-3.5 rounded-md bg-zinc-950 font-mono text-xs text-zinc-200 border border-zinc-800 shadow-inner">
                <code>adb install -r app/build/outputs/apk/release/app-release.apk</code>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between text-xs text-zinc-600 font-mono mb-1">
                <span>3. Monitor Real-Time Latency &amp; Shannon Gating Logs:</span>
                <button
                  onClick={() => copyToClipboard("adb logcat -s \"BioDINO\"", "cmd3")}
                  className="text-black hover:underline flex items-center space-x-1 font-bold"
                >
                  {copiedCmd === "cmd3" ? <IconCheck className="w-3.5 h-3.5 text-emerald-600" /> : <IconCopy className="w-3.5 h-3.5" />}
                  <span>{copiedCmd === "cmd3" ? "Copied" : "Copy"}</span>
                </button>
              </div>
              <div className="p-3.5 rounded-md bg-zinc-950 font-mono text-xs text-zinc-200 border border-zinc-800 shadow-inner">
                <code>adb logcat -s &quot;BioDINO&quot;</code>
              </div>
            </div>
          </div>
        </div>

      </section>
    </main>
  );
}

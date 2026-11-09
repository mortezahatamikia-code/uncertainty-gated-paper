"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  IconGraduation,
  IconPaper,
  IconApp,
  IconAward,
  IconDownload,
  IconGithub,
  IconLinkedin,
  IconMail,
  IconChevronRight,
  IconCheck,
} from "@/components/Icons";

export default function HomePage() {
  const [copiedEmail, setCopiedEmail] = useState(false);
  const [transcriptTab, setTranscriptTab] = useState<"en" | "fa">("en");
  const [activeDocumentModal, setActiveDocumentModal] = useState<{
    title: string;
    badge?: string;
    details: string;
    src?: string;
    alt?: string;
    downloadUrl?: string;
    downloadLabel?: string;
    hasDualVersion?: boolean;
    englishSrc?: string;
    englishPdf?: string;
    persianSrc?: string;
    persianPdf?: string;
    englishDownloadLabel?: string;
    persianDownloadLabel?: string;
  } | null>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setActiveDocumentModal(null);
      }
      if ((e.ctrlKey || e.metaKey) && (e.key === "p" || e.key === "P")) {
        e.preventDefault();
        window.print();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const handleCopyEmail = () => {
    navigator.clipboard.writeText("reyhane.code@gmail.com");
    setCopiedEmail(true);
    setTimeout(() => setCopiedEmail(false), 2000);
  };

  return (
    <main className="min-h-screen bg-[#fafaf9] text-zinc-900">
      {/* Schema.org Structured Data for Google Search & Academic Crawlers */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Person",
            name: "Reyhane Javidi Alsaadi",
            url: "https://reyhane-code.github.io/",
            image: "https://reyhane-code.github.io/reyhane-javidi.webp",
            email: "reyhane.code@gmail.com",
            jobTitle: "Computer Engineering Scholar & Edge AI Researcher",
            affiliation: {
              "@type": "EducationalOrganization",
              name: "Department of Computer Engineering, Dr. Shariaty Technical University, Tehran",
            },
            alumniOf: {
              "@type": "EducationalOrganization",
              name: "Dr. Shariaty Technical University",
            },
            award: [
              "University Presidential Letter of Commendation (Ref: 5039/202/1615)",
              "Top 5% Cohort Distinction / Dean's Honor Roll",
              "Official Teaching Assistantship in Game Development",
            ],
            sameAs: [
              "https://github.com/reyhane-code",
              "https://www.linkedin.com/in/reyhane-javidi",
            ],
            knowsAbout: [
              "Vision Foundation Models",
              "Few-Shot Learning",
              "Edge AI",
              "Ledoit-Wolf Analytical Covariance Shrinkage",
              "DINOv2",
              "BioCLIP",
              "PyTorch",
              "ONNX Runtime Mobile",
              "INT8 Model Quantization",
              "Next.js",
              "React",
              "TypeScript",
              "LaTeX",
            ],
          }),
        }}
      />

      {/* HERO SECTION — MINIMALIST EDITORIAL */}
      <section className="relative overflow-hidden pt-12 pb-16 border-b border-zinc-200/90 bg-[#fafaf9] text-zinc-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">

            {/* Bio Details */}
            <div className="lg:col-span-8 space-y-6">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded bg-zinc-100 border border-zinc-200 text-zinc-800 text-xs font-mono font-medium tracking-wide">
                <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
                <span>Prospective Graduate Researcher • Seeking M.Sc. / Ph.D. Positions (Spring 2027 / Fall 2027)</span>
              </div>

              <div className="space-y-2">
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-zinc-950 font-sans">
                  Reyhane Javidi Alsaadi
                </h1>
                <p className="text-lg sm:text-xl text-zinc-700 font-medium tracking-tight">
                  Computer Engineering Scholar &amp; Edge AI Researcher
                </p>
                <p className="text-xs text-zinc-500 font-mono flex items-center space-x-2 pt-0.5">
                  <IconGraduation className="w-4 h-4 text-zinc-600" />
                  <span>Department of Computer Engineering, Dr. Shariaty Technical University, Tehran</span>
                </p>
              </div>

              <p className="text-zinc-700 text-base leading-relaxed max-w-2xl">
                Undergraduate researcher working at the intersection of <strong className="text-zinc-950 font-semibold">Vision Foundation Models (DINOv2, BioCLIP)</strong> and <strong className="text-zinc-950 font-semibold">Resource-Constrained Edge AI</strong>. Lead author of the BioDINO-Edge framework (targeting IEEE T-PAMI / CVPR / CompAg), university Teaching Assistant, and recipient of the official university Presidential Letter of Commendation.
              </p>

              {/* Action Buttons — Categorized 3x2 Grid */}
              <div className="space-y-2 pt-1 max-w-2xl">
                {/* Row 1: Academic & Research Outputs */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-2.5">
                  <a
                    href="/Reyhane_Javidi_Alsaadi_CV.pdf"
                    target="_blank"
                    className="flex items-center justify-center space-x-2 px-3 py-2.5 rounded bg-zinc-950 text-white font-medium text-xs hover:bg-zinc-800 transition-colors shadow-xs text-center"
                  >
                    <IconDownload className="w-3.5 h-3.5 shrink-0" />
                    <span className="truncate">Download CV (PDF)</span>
                  </a>

                  <a
                    href="/biodino_edge_paper.pdf"
                    target="_blank"
                    className="flex items-center justify-center space-x-2 px-3 py-2.5 rounded bg-white text-zinc-900 font-medium text-xs hover:bg-zinc-100 border border-zinc-300 hover:border-zinc-950 transition-colors text-center"
                  >
                    <IconPaper className="w-3.5 h-3.5 text-zinc-600 shrink-0" />
                    <span className="truncate">Lead Paper (PDF)</span>
                  </a>

                  <Link
                    href="/projects/biodino-edge-android/"
                    className="flex items-center justify-center space-x-2 px-3 py-2.5 rounded bg-white text-zinc-900 font-medium text-xs hover:bg-zinc-100 border border-zinc-300 hover:border-zinc-950 transition-colors text-center"
                  >
                    <IconApp className="w-3.5 h-3.5 text-zinc-600 shrink-0" />
                    <span className="truncate">Edge AI Showcase</span>
                  </Link>
                </div>

                {/* Row 2: Direct Contact & Research Profiles */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-2.5">
                  <button
                    onClick={handleCopyEmail}
                    className="flex items-center justify-center space-x-1.5 px-2.5 py-2.5 rounded bg-zinc-100 text-zinc-800 font-mono text-xs hover:bg-zinc-200 border border-zinc-200 transition-colors text-center cursor-pointer"
                    title="Click to copy: reyhane.code@gmail.com"
                  >
                    {copiedEmail ? (
                      <>
                        <IconCheck className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                        <span className="text-emerald-700 font-sans font-semibold truncate">Email Copied!</span>
                      </>
                    ) : (
                      <>
                        <IconMail className="w-3.5 h-3.5 text-zinc-600 shrink-0" />
                        <span className="truncate">reyhane.code@gmail.com</span>
                      </>
                    )}
                  </button>

                  <a
                    href="https://github.com/reyhane-code"
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center justify-center space-x-2 px-3 py-2.5 rounded bg-zinc-100 text-zinc-900 font-medium text-xs hover:bg-zinc-200 border border-zinc-200 transition-colors text-center"
                    title="GitHub: reyhane-code"
                  >
                    <IconGithub className="w-3.5 h-3.5 text-zinc-800 shrink-0" />
                    <span className="truncate">GitHub Profile</span>
                  </a>

                  <a
                    href="https://www.linkedin.com/in/reyhane-javidi"
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center justify-center space-x-2 px-3 py-2.5 rounded bg-zinc-100 text-zinc-900 font-medium text-xs hover:bg-zinc-200 border border-zinc-200 transition-colors text-center"
                    title="LinkedIn: reyhane-javidi"
                  >
                    <IconLinkedin className="w-3.5 h-3.5 text-[#0A66C2] shrink-0" />
                    <span className="truncate">LinkedIn Profile</span>
                  </a>
                </div>
              </div>

              {/* 4 Core Pillars at a Glance — Minimalist Metric Matrix */}
              <div className="grid grid-cols-2 sm:grid-cols-4 border border-zinc-200 divide-x divide-y sm:divide-y-0 divide-zinc-200 bg-white max-w-2xl shadow-xs mt-4">
                <div className="p-3.5">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-zinc-500">Cumulative GPA</div>
                  <div className="text-xl font-bold text-zinc-950 font-mono mt-0.5">19.16 <span className="text-xs font-normal text-zinc-500">/ 20</span></div>
                  <div className="text-[11px] text-zinc-600 mt-0.5">Rank 1 • Dean&apos;s List</div>
                </div>
                <div className="p-3.5">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-zinc-500">Peak Accuracy</div>
                  <div className="text-xl font-bold text-zinc-950 font-mono mt-0.5">98.72%</div>
                  <div className="text-[11px] text-zinc-600 mt-0.5">BioDINO-Edge (PV-11)</div>
                </div>
                <div className="p-3.5">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-[#E30613]">In-The-Wild Gain</div>
                  <div className="text-xl font-bold text-[#E30613] font-mono mt-0.5">+13.00%</div>
                  <div className="text-[11px] text-zinc-600 mt-0.5">Over 2026 SOTA (PlantDoc)</div>
                </div>
                <div className="p-3.5">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-zinc-500">Edge CPU Latency</div>
                  <div className="text-xl font-bold text-zinc-950 font-mono mt-0.5">&lt; 22 ms</div>
                  <div className="text-[11px] text-zinc-600 mt-0.5">22 MB INT8 Model</div>
                </div>
              </div>
            </div>

            {/* Profile Picture Card */}
            <div className="lg:col-span-4 flex justify-center">
              <div className="w-64 sm:w-72 border border-zinc-200 bg-white p-2.5 shadow-xs">
                <div className="relative overflow-hidden bg-zinc-100 aspect-[4/5]">
                  <img
                    src="/reyhane-javidi.webp"
                    alt="Reyhane Javidi Alsaadi"
                    className="w-full h-full object-cover object-center grayscale hover:grayscale-0 transition-all duration-300"
                  />
                </div>
                <div className="p-3 bg-white border-t border-zinc-200 mt-2">
                  <div className="font-bold text-zinc-950 text-sm tracking-tight">Reyhane Javidi Alsaadi</div>
                  <div className="text-xs text-zinc-500 font-mono mt-0.5">Edge AI &amp; Vision Researcher</div>
                  <div className="mt-2.5 flex items-center justify-between text-[11px] font-mono text-zinc-600 pt-2 border-t border-zinc-100">
                    <span>Tehran, IR</span>
                    <span className="text-zinc-950 font-medium">Open to M.Sc. / Ph.D.</span>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* MAIN CONTENT CONTAINER */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14 space-y-16">

        {/* 01. FEATURED RESEARCH PUBLICATION (RESEARCH FIRST) */}
        <section id="publications" className="space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
              <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
                01 // Featured Research Publication
              </h2>
            </div>
            <Link
              href="/research/biodino-edge/"
              className="text-xs text-zinc-900 hover:text-zinc-600 flex items-center space-x-1 font-mono font-semibold"
            >
              <span>Interactive Paper Page</span>
              <IconChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="border border-zinc-200 bg-white p-6 sm:p-8 shadow-xs space-y-6">
            <div className="flex flex-wrap items-center gap-2">
              <span className="px-2.5 py-0.5 rounded bg-zinc-950 text-white text-xs font-mono font-medium">
                Lead / First Author
              </span>
              <span className="px-2.5 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-xs font-mono">
                Submitted to CompAg [14-page IEEEtran, 2026]
              </span>
              <span className="px-2.5 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-xs font-mono">
                Analytical Zero-Gradient Alignment
              </span>
            </div>

            <div className="space-y-2 border-b border-zinc-200 pb-5">
              <h3 className="text-xl sm:text-2xl font-bold text-zinc-950 leading-snug tracking-tight">
                BioDINO-Edge: Biologically-Grounded Multi-Scale Vision Foundation Models for Trustworthy Few-Shot Plant Pathology on Resource-Constrained Hardware
              </h3>
              <p className="text-sm text-zinc-800 font-medium">
                <strong className="text-zinc-950 underline decoration-zinc-400">Reyhane Javidi Alsaadi</strong> and Mohammad Reza Samad Zadeh
              </p>
              <p className="text-xs text-zinc-500 font-mono">
                Department of Computer Engineering, Dr. Shariaty Technical University, Tehran, Iran
              </p>
            </div>

            <p className="text-sm text-zinc-700 leading-relaxed">
              We present <strong>BioDINO-Edge</strong>, a dual-foundation framework uniting self-supervised spatial patch modeling (<strong>DINOv2 Small</strong>) with organismal vision-language hierarchies (<strong>BioCLIP ViT-B</strong>). Introduces <em>Purified Taxonomic Domain Synthesis</em> and <em>Regularized Fisher-Discriminant Alignment with analytical Ledoit-Wolf covariance shrinkage</em>, resolving singular covariance matrices without backpropagation in &lt;0.003 ms. A <em>Soft-Anchored Transductive Self-Calibration</em> removes 5-shot prototype shift, yielding a <strong className="text-zinc-950">98.72% peak accuracy</strong> on PlantVillage and <strong className="text-zinc-950">83.61%</strong> on PlantDoc in-the-wild (<strong className="text-[#E30613]">+13.00%</strong> over 2026 SOTA).
            </p>

            {/* Research Problem / Innovation / Impact Grid */}
            <div className="border border-zinc-200 divide-y md:divide-y-0 md:divide-x divide-zinc-200 grid grid-cols-1 md:grid-cols-3 bg-zinc-50/60 text-xs">
              <div className="p-3.5 space-y-1">
                <span className="text-zinc-500 font-mono text-[11px] font-bold block uppercase">• Problem:</span>
                <p className="text-zinc-700 text-[11px] leading-relaxed">
                  Severe data scarcity for novel crop pathogens &amp; memory-compute constraints on agricultural edge microprocessors.
                </p>
              </div>
              <div className="p-3.5 space-y-1">
                <span className="text-zinc-950 font-mono text-[11px] font-bold block uppercase">• Core Innovation:</span>
                <p className="text-zinc-700 text-[11px] leading-relaxed">
                  Joint 896-d DINOv2 + BioCLIP manifold with closed-form Ledoit-Wolf covariance shrinkage in &lt;0.003 ms (zero backprop).
                </p>
              </div>
              <div className="p-3.5 space-y-1">
                <span className="text-zinc-950 font-mono text-[11px] font-bold block uppercase">• Empirical Impact:</span>
                <p className="text-zinc-700 text-[11px] leading-relaxed">
                  <strong>98.72%</strong> peak accuracy, <strong>0.011%</strong> cross-species confusion, and <strong>22.05 MB</strong> INT8 edge model.
                </p>
              </div>
            </div>

            {/* Action Links */}
            <div className="pt-2">
              <Link
                href="/research/biodino-edge/"
                className="inline-flex items-center space-x-2 px-4 py-2 rounded bg-zinc-950 text-white font-medium text-xs hover:bg-zinc-800 transition-colors shadow-2xs"
              >
                <IconPaper className="w-3.5 h-3.5" />
                <span>Read Full Interactive Paper &amp; Saliency Maps</span>
              </Link>
            </div>
          </div>
        </section>

        {/* 02. PROSPECTIVE GRADUATE RESEARCH DIRECTIONS */}
        <section id="research-interests" className="space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
              <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
                02 // Prospective Graduate Research Directions
              </h2>
            </div>
            <span className="text-xs text-zinc-500 font-mono">Future Ph.D. / M.Sc. Thrusts</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {/* Direction 1 */}
            <div className="border border-zinc-200 bg-white p-6 shadow-xs space-y-3">
              <div className="flex items-center space-x-2 border-b border-zinc-100 pb-2">
                <span className="w-2 h-2 rounded-xs bg-zinc-950" />
                <h3 className="font-bold text-zinc-950 text-sm">Host-Agnostic / Cross-Crop Pathogen Disentanglement</h3>
              </div>
              <p className="text-xs text-zinc-600 leading-relaxed">
                Standard vision models erroneously entangle host leaf morphology (venation, leaf outline, chloroplast pigment) with active pathological lesions. My research aims to formulate <strong className="text-zinc-900">domain-disentangled representation learning</strong>, separating query representations into host-tissue and invariant pathogen manifolds for zero-shot diagnosis across novel crops.
              </p>
              <div className="pt-1 flex flex-wrap gap-1.5 font-mono text-[10px] text-zinc-700">
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Cross-Crop Invariance</span>
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Disentangled Manifolds</span>
              </div>
            </div>

            {/* Direction 2 */}
            <div className="border border-zinc-200 bg-white p-6 shadow-xs space-y-3">
              <div className="flex items-center space-x-2 border-b border-zinc-100 pb-2">
                <span className="w-2 h-2 rounded-xs bg-zinc-950" />
                <h3 className="font-bold text-zinc-950 text-sm">Autonomous Support-Buffer Outlier Rejection on Edge Hardware</h3>
              </div>
              <p className="text-xs text-zinc-600 leading-relaxed">
                In robotic scouting and few-shot adaptation, support caches frequently encounter sensor blur or non-foliar occlusions. I plan to research <strong className="text-zinc-900">closed-form statistical filtering</strong> (robust Mahalanobis distance and analytical MCD estimators) directly inside edge support buffers for autonomous purge in &lt;0.01 ms with zero backprop.
              </p>
              <div className="pt-1 flex flex-wrap gap-1.5 font-mono text-[10px] text-zinc-700">
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Robust Mahalanobis Filter</span>
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Zero-Gradient Support</span>
              </div>
            </div>

            {/* Direction 3 */}
            <div className="border border-zinc-200 bg-white p-6 shadow-xs space-y-3">
              <div className="flex items-center space-x-2 border-b border-zinc-100 pb-2">
                <span className="w-2 h-2 rounded-xs bg-zinc-950" />
                <h3 className="font-bold text-zinc-950 text-sm">Resource-Constrained Deep Learning &amp; Zero-Gradient Edge Adaptation</h3>
              </div>
              <p className="text-xs text-zinc-600 leading-relaxed">
                Investigating analytical closed-form linear discriminants, sub-4-bit INT4/INT8 quantization, and transductive calibration on high-throughput microprocessors to deploy multi-scale vision transformers directly onto sub-$20 microcontrollers and drone payloads with deterministic sub-15ms latency.
              </p>
              <div className="pt-1 flex flex-wrap gap-1.5 font-mono text-[10px] text-zinc-700">
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">4-Bit Quantization</span>
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Deterministic Latency</span>
              </div>
            </div>

            {/* Direction 4 */}
            <div className="border border-zinc-200 bg-white p-6 shadow-xs space-y-3">
              <div className="flex items-center space-x-2 border-b border-zinc-100 pb-2">
                <span className="w-2 h-2 rounded-xs bg-zinc-950" />
                <h3 className="font-bold text-zinc-950 text-sm">Trustworthy, Calibrated &amp; Biologically Grounded Multimodal AI</h3>
              </div>
              <p className="text-xs text-zinc-600 leading-relaxed">
                Bridging self-supervised visual patch representations with organismal phylogenetic taxonomies and biological knowledge graphs, emphasizing rigorous uncertainty quantification (ECE &lt; 1%) and conformal prediction bounds to guarantee safe, trustworthy recommendations for automated interventions.
              </p>
              <div className="pt-1 flex flex-wrap gap-1.5 font-mono text-[10px] text-zinc-700">
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Conformal Prediction</span>
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Uncertainty Calibration</span>
              </div>
            </div>
          </div>
        </section>

        {/* 03. ACADEMIC EDUCATION & VERIFIED TRANSCRIPTS */}
        <section id="education" className="space-y-6">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
              <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
                03 // Academic Education &amp; Verified Transcripts
              </h2>
            </div>
            <span className="text-xs text-zinc-500 font-mono">B.Sc. &amp; A.Sc. Official Portals</span>
          </div>

          {/* 1. BACHELOR'S DEGREE */}
          <div className="border border-zinc-200 bg-white p-6 sm:p-7 shadow-xs space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border-b border-zinc-200 pb-4">
              <div>
                <div className="flex items-center space-x-2">
                  <span className="px-2 py-0.5 rounded bg-zinc-950 text-white text-[10px] font-mono uppercase tracking-wider font-semibold">
                    Current Degree Program
                  </span>
                  <span className="text-xs font-mono text-zinc-500">2024 — Expected 2026</span>
                </div>
                <h3 className="text-xl font-bold text-zinc-950 tracking-tight mt-1">
                  Bachelor of Science (B.Sc.) in Computer Engineering — Software
                </h3>
                <p className="text-xs text-zinc-600 font-mono mt-0.5">
                  Department of Computer Engineering, Dr. Shariaty Technical University, Tehran, Iran
                </p>
              </div>
              <div>
                <button
                  onClick={() => {
                    setActiveDocumentModal({
                      title: "B.Sc. Academic Transcript Record",
                      badge: "B.Sc. GPA: 19.16 / 20.00",
                      details: "Official TVU Academic Record • 55 graded credits completed • Rank 1 cohort distinction.",
                      hasDualVersion: true,
                      englishSrc: "/bsc_transcript_en.png",
                      englishPdf: "/Reyhane_Javidi_BSc_Transcript_English.pdf",
                      englishDownloadLabel: "Download English (PDF)",
                      persianSrc: "/bsc_transcript_scan.png",
                      persianPdf: "/bachelorDegreeNumbers.pdf",
                      persianDownloadLabel: "Download Original Scan (PDF)",
                    });
                    setTranscriptTab("en");
                  }}
                  className="inline-flex items-center space-x-2 px-3.5 py-2 rounded bg-zinc-950 hover:bg-zinc-800 text-white font-mono text-xs font-medium transition-colors shadow-2xs cursor-pointer"
                >
                  <IconPaper className="w-3.5 h-3.5" />
                  <span>Inspect B.Sc. Transcript (EN / Scan)</span>
                </button>
              </div>
            </div>

            {/* High-Distinction Coursework Matrix */}
            <div className="space-y-2">
              <span className="text-xs font-bold text-zinc-950 uppercase tracking-wider font-mono">
                Advanced Computer Science &amp; AI Coursework (Official Marks)
              </span>
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 border border-zinc-200 divide-x divide-y divide-zinc-200 bg-white text-xs">
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Algorithm Design</span>
                  <span className="font-mono font-bold text-[#E30613]">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Artificial Intelligence</span>
                  <span className="font-mono font-bold text-[#E30613]">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">AI Laboratory</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Theory of Automata &amp; Lang.</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Probability &amp; Statistics</span>
                  <span className="font-mono font-bold text-zinc-950">19.50 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Discrete Mathematics</span>
                  <span className="font-mono font-bold text-zinc-950">19.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Software Engineering</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Internet of Things (IoT)</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
              </div>
            </div>
          </div>

          {/* 2. ASSOCIATE DEGREE */}
          <div className="border border-zinc-200 bg-white p-6 sm:p-7 shadow-xs space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border-b border-zinc-200 pb-4">
              <div>
                <div className="flex items-center space-x-2">
                  <span className="px-2 py-0.5 rounded bg-zinc-200 text-zinc-900 text-[10px] font-mono uppercase tracking-wider font-semibold">
                    Conferred Degree (70 Credits)
                  </span>
                  <span className="text-xs font-mono text-zinc-500">2022 — 2024</span>
                </div>
                <h3 className="text-xl font-bold text-zinc-950 tracking-tight mt-1">
                  Associate of Science (A.Sc.) in Computer Software Applications
                </h3>
                <p className="text-xs text-zinc-600 font-mono mt-0.5">
                  Department of Computer Engineering, Dr. Shariaty Technical University, Tehran, Iran
                </p>
              </div>
              <div>
                <button
                  onClick={() => {
                    setActiveDocumentModal({
                      title: "Associate Academic Transcript Record",
                      badge: "A.Sc. GPA: 18.96 / 20.00",
                      details: "Official TVU Academic Record • 70 units completed • Conferred Degree (Feb 2024).",
                      hasDualVersion: true,
                      englishSrc: "/asc_transcript_en.png",
                      englishPdf: "/Reyhane_Javidi_Associate_Transcript_English.pdf",
                      englishDownloadLabel: "Download English (PDF)",
                      persianSrc: "/asc_transcript_scan.png",
                      persianPdf: "/associateDegreeNumbers.pdf",
                      persianDownloadLabel: "Download Original Scan (PDF)",
                    });
                    setTranscriptTab("en");
                  }}
                  className="inline-flex items-center space-x-2 px-3.5 py-2 rounded bg-zinc-950 hover:bg-zinc-800 text-white font-mono text-xs font-medium transition-colors shadow-2xs cursor-pointer"
                >
                  <IconPaper className="w-3.5 h-3.5" />
                  <span>Inspect Associate Transcript (EN / Scan)</span>
                </button>
              </div>
            </div>

            {/* Foundational Coursework Matrix */}
            <div className="space-y-2">
              <span className="text-xs font-bold text-zinc-950 uppercase tracking-wider font-mono">
                Foundational CS &amp; Systems Coursework (Official Marks)
              </span>
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 border border-zinc-200 divide-x divide-y divide-zinc-200 bg-white text-xs">
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Data Structures</span>
                  <span className="font-mono font-bold text-[#E30613]">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Advanced Programming</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Database Systems</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Digital Logic Circuits</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Computer Networks</span>
                  <span className="font-mono font-bold text-zinc-950">19.50 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Network Security</span>
                  <span className="font-mono font-bold text-zinc-950">19.25 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Operating Systems Lab</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Final Capstone Project</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 04. UNIVERSITY HONORS & ACADEMIC MENTORSHIP */}
        <section id="honors" className="space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
              <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
                04 // University Honors &amp; Academic Mentorship
              </h2>
            </div>
            <span className="text-xs text-zinc-500 font-mono">Formal Verification Records</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {/* Card 1: Official Presidential Commendation */}
            <div className="border border-zinc-200 bg-white p-6 shadow-xs space-y-4 flex flex-col justify-between">
              <div className="space-y-2.5">
                <div className="flex items-center justify-between border-b border-zinc-100 pb-2">
                  <span className="text-xs font-mono text-zinc-950 font-bold uppercase tracking-wider flex items-center space-x-1.5">
                    <IconAward className="w-3.5 h-3.5 text-[#E30613]" />
                    <span>University Presidential Honor</span>
                  </span>
                  <span className="text-[10px] font-mono text-zinc-600 bg-zinc-100 px-2 py-0.5 rounded border border-zinc-200">
                    Ref: 5039/202/1615
                  </span>
                </div>
                <h3 className="text-base font-bold text-zinc-950">
                  Presidential Letter of Commendation
                </h3>
                <p className="text-xs text-zinc-500 font-mono">
                  Conferred &amp; Sealed by President of Dr. Shariaty Technical University • 2026
                </p>
                <p className="text-xs text-zinc-600 leading-relaxed">
                  Formally awarded by university leadership in recognition of instructional excellence as Teaching Assistant in Game Development, recognizing collaborative academic contribution with faculty member Prof. Toktam Zoghi and dedicated mentorship of peer engineering students.
                </p>
              </div>

              <div className="pt-2 border-t border-zinc-100">
                <button
                  onClick={() => {
                    setActiveDocumentModal({
                      title: "Presidential Letter of Commendation (Ref: 5039/202/1615)",
                      badge: "University President Seal",
                      details: "Official Letter of Commendation conferred by the President of Dr. Shariaty Technical University, recognizing exemplary teaching assistantship and mentorship in Game Development.",
                      hasDualVersion: true,
                      englishSrc: "/commendation_letter_en.png",
                      englishPdf: "/Reyhane_Javidi_Commendation_Letter_English.pdf",
                      englishDownloadLabel: "Download English (PDF)",
                      persianSrc: "/letterOfCommendation.jpg",
                      persianPdf: "/letterOfCommendation.jpg",
                      persianDownloadLabel: "Download Original Parchment (JPG)",
                    });
                    setTranscriptTab("en");
                  }}
                  className="inline-flex items-center space-x-2 px-3.5 py-2 rounded bg-zinc-950 hover:bg-zinc-800 text-white font-mono text-xs font-medium transition-colors shadow-2xs cursor-pointer"
                >
                  <IconPaper className="w-3.5 h-3.5" />
                  <span>Inspect Commendation Letter (EN / Scan)</span>
                </button>
              </div>
            </div>

            {/* Card 2: Official Teaching Assistantship */}
            <div className="border border-zinc-200 bg-white p-6 shadow-xs space-y-4 flex flex-col justify-between">
              <div className="space-y-2.5">
                <div className="flex items-center justify-between border-b border-zinc-100 pb-2">
                  <span className="text-xs font-mono text-zinc-950 font-bold uppercase tracking-wider flex items-center space-x-1.5">
                    <IconGraduation className="w-3.5 h-3.5 text-zinc-700" />
                    <span>Academic Affairs Certificate</span>
                  </span>
                  <span className="text-[10px] font-mono text-zinc-600 bg-zinc-100 px-2 py-0.5 rounded border border-zinc-200">
                    Term: 01/2026 – 07/2026
                  </span>
                </div>
                <h3 className="text-base font-bold text-zinc-950">
                  Teaching Assistant (TA) — Game Development
                </h3>
                <p className="text-xs text-zinc-500 font-mono">
                  Supervised by Prof. Toktam Zoghi • Department of Computer Engineering
                </p>
                <p className="text-xs text-zinc-600 leading-relaxed">
                  Conducted weekly problem-solving labs and code reviews for 40+ engineering students on state machines, interactive graphics rendering, and physics simulations, supported by an official verification letter stamped by the Office of Academic Affairs.
                </p>
              </div>

              <div className="pt-2 border-t border-zinc-100">
                <button
                  onClick={() => {
                    setActiveDocumentModal({
                      title: "Teaching Assistant Verification Certificate",
                      badge: "Office of Academic Affairs Seal",
                      details: "Official certificate of teaching assistantship issued by Prof. Toktam Zoghi and authenticated with the seal of the Office of Academic Affairs, Dr. Shariaty Technical University.",
                      hasDualVersion: true,
                      englishSrc: "/ta_certificate_en.png",
                      englishPdf: "/Reyhane_Javidi_TA_Certificate_English.pdf",
                      englishDownloadLabel: "Download English (PDF)",
                      persianSrc: "/teachingAssistantCertificate.png",
                      persianPdf: "/teachingAssistantCertificate.pdf",
                      persianDownloadLabel: "Download Original Certificate (PDF)",
                    });
                    setTranscriptTab("en");
                  }}
                  className="inline-flex items-center space-x-2 px-3.5 py-2 rounded bg-zinc-950 hover:bg-zinc-800 text-white font-mono text-xs font-medium transition-colors shadow-2xs cursor-pointer"
                >
                  <IconPaper className="w-3.5 h-3.5" />
                  <span>Inspect TA Certificate (EN / Scan)</span>
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* 05. EDGE AI SYSTEMS & ON-DEVICE PROTOTYPING */}
        <section id="engineering" className="space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
              <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
                05 // Edge AI Deployment &amp; Systems Prototyping
              </h2>
            </div>
            <Link
              href="/projects/biodino-edge-android/"
              className="text-xs text-zinc-900 hover:text-zinc-600 flex items-center space-x-1 font-mono font-semibold"
            >
              <span>Explore Mobile Edge Showcase</span>
              <IconChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="border border-zinc-200 bg-white p-6 sm:p-7 shadow-xs space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-b border-zinc-200 pb-4">
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <span className="px-2 py-0.5 rounded bg-zinc-950 text-white text-[10px] font-mono uppercase tracking-wider font-semibold">
                    Edge SysML Prototype
                  </span>
                  <span className="px-2 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-[10px] font-mono">
                    ONNX Runtime Mobile NNAPI
                  </span>
                  <span className="px-2 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-[10px] font-mono">
                    22.05 MB INT8 Model
                  </span>
                </div>
                <h3 className="text-xl font-bold text-zinc-950 tracking-tight mt-1.5">
                  BioDINO-Edge Mobile: 100% Offline Edge Inference Prototyping
                </h3>
                <p className="text-xs text-zinc-600 font-mono mt-0.5">
                  Benchmarked on ARM Cortex Processors • Zero Cloud Dependency
                </p>
              </div>

              <div className="flex items-center space-x-2">
                <Link
                  href="/projects/biodino-edge-android/"
                  className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded bg-zinc-950 text-white font-medium text-xs hover:bg-zinc-800 transition-colors shadow-2xs"
                >
                  <IconApp className="w-3.5 h-3.5" />
                  <span>Interactive App Page</span>
                </Link>
              </div>
            </div>

            {/* 3 Core Systems Pillars */}
            <div className="grid grid-cols-1 sm:grid-cols-3 border border-zinc-200 divide-y sm:divide-y-0 sm:divide-x divide-zinc-200 bg-white text-xs">
              <div className="p-4 space-y-1.5">
                <span className="font-bold text-zinc-950 font-mono text-[11px] block uppercase">1. Zero-GC Direct Memory</span>
                <p className="text-zinc-600 leading-relaxed text-[11px]">
                  Preallocated direct byte buffer pipeline extracting normalized camera pixels via bitwise shifts, eliminating Garbage Collector pauses and sustaining &gt;55 FPS.
                </p>
              </div>

              <div className="p-4 space-y-1.5">
                <span className="font-bold text-zinc-950 font-mono text-[11px] block uppercase">2. Hardware Acceleration</span>
                <p className="text-zinc-600 leading-relaxed text-[11px]">
                  ONNX Runtime Mobile initialized with Android NNAPI targeting Qualcomm Hexagon NPU / Adreno GPU (14.2 ms latency) with seamless 4-thread CPU fallback.
                </p>
              </div>

              <div className="p-4 space-y-1.5">
                <span className="font-bold text-zinc-950 font-mono text-[11px] block uppercase">3. 3-Layer Safety Gate</span>
                <p className="text-zinc-600 leading-relaxed text-[11px]">
                  Rejects dark frames (&lt;22 lux), non-foliar objects (botanical cosine score &lt;0.40), and ambiguous lesions via predictive Shannon margin-entropy confidence gating.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* 06. TECHNICAL COMPETENCIES */}
        <section id="skills" className="space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
              <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
                06 // Technical &amp; Research Competencies
              </h2>
            </div>
            <span className="text-xs text-zinc-500 font-mono">Taxonomy of Capabilities</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 border border-zinc-200 divide-y md:divide-y-0 md:divide-x divide-zinc-200 bg-white shadow-xs">
            {/* Box 1: Machine Learning & Vision */}
            <div className="p-5 space-y-3">
              <h3 className="text-xs font-bold text-zinc-950 uppercase tracking-wider font-mono">Artificial Intelligence &amp; Vision</h3>
              <ul className="space-y-1.5 text-xs text-zinc-600">
                <li>• <strong className="text-zinc-900">PyTorch</strong>, TorchVision, Timm, OpenCLIP</li>
                <li>• <strong className="text-zinc-900">Vision Transformers (ViT)</strong>, DINOv2, BioCLIP</li>
                <li>• <strong className="text-zinc-900">Few-Shot Learning</strong> &amp; Regularized Fisher-LDA</li>
                <li>• Analytical Covariance Shrinkage (<strong className="text-zinc-900">Ledoit-Wolf</strong>)</li>
                <li>• Self-Attention Rollout &amp; Model Calibration</li>
                <li>• Scikit-Learn, <strong className="text-zinc-900">NumPy</strong>, SciPy</li>
              </ul>
            </div>

            {/* Box 2: Edge AI & Optimization */}
            <div className="p-5 space-y-3">
              <h3 className="text-xs font-bold text-zinc-950 uppercase tracking-wider font-mono">Edge AI &amp; Low-Latency Deployment</h3>
              <ul className="space-y-1.5 text-xs text-zinc-600">
                <li>• <strong className="text-zinc-900">ONNX Runtime</strong> &amp; ONNX Runtime Mobile</li>
                <li>• <strong className="text-zinc-900">INT8 Dynamic Quantization</strong> (MatMul)</li>
                <li>• Hardware-Accelerated Inference (NNAPI / CPU)</li>
                <li>• Low-Latency &amp; Zero-Allocation Direct Memory</li>
                <li>• Real-Time Profiling &amp; Edge Hardware Benchmarking</li>
                <li>• Python (Model Export, Pipeline &amp; Tooling)</li>
              </ul>
            </div>

            {/* Box 3: Scientific Writing, Web & Tooling */}
            <div className="p-5 space-y-3">
              <h3 className="text-xs font-bold text-zinc-950 uppercase tracking-wider font-mono">Scientific Writing &amp; Research Tooling</h3>
              <ul className="space-y-1.5 text-xs text-zinc-600">
                <li>• <strong className="text-zinc-900">LaTeX</strong> (IEEEtran &amp; Scientific Typesetting)</li>
                <li>• Linux</li>
                <li>• <strong className="text-zinc-900">Git</strong> (Feature Branching, Rebase, PR Hygiene)</li>
                <li>• TypeScript &amp; JavaScript (ES6+)</li>
                <li>• <strong className="text-zinc-900">Next.js</strong> (App Router, Static Export) &amp; React</li>
                <li>• Tailwind CSS &amp; Modern Web Tooling</li>
              </ul>
            </div>
          </div>
        </section>

        {/* 07. PROSPECTIVE ADVISORS & GRADUATE OUTREACH */}
        <section id="outreach" className="border border-zinc-200 bg-white p-8 sm:p-10 shadow-xs space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-zinc-200 pb-6">
            <div className="space-y-2">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded bg-zinc-100 border border-zinc-200 text-zinc-800 text-xs font-mono font-medium">
                <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
                <span>Graduate Admissions &amp; Lab Outreach</span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-zinc-950 tracking-tight">
                Prospective Faculty &amp; Research Lab Inquiries
              </h2>
              <p className="text-sm text-zinc-600 max-w-2xl leading-relaxed">
                Currently exploring <strong className="text-zinc-950">M.Sc. / Ph.D. research assistantship positions</strong> for Spring 2027 / Fall 2027. Prepared to contribute immediately with first-author manuscript drafting, closed-form mathematical modeling, and optimized edge deployment.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row md:flex-col gap-2.5 min-w-[240px]">
              <a
                href="mailto:reyhane.code@gmail.com?subject=Prospective%20Graduate%20Research%20Inquiry%20-%20Reyhane%20Javidi%20Alsaadi&body=Dear%20Reyhane,%0A%0AWe%20reviewed%20your%20research%20portfolio%20and%20BioDINO-Edge%20work...%0A%0ABest%20regards,"
                className="w-full inline-flex items-center justify-center space-x-2 px-5 py-3 rounded bg-zinc-950 text-white font-medium text-xs hover:bg-zinc-800 transition-colors shadow-xs"
              >
                <IconMail className="w-4 h-4" />
                <span>Initiate Research Inquiry</span>
              </a>

              <a
                href="/Reyhane_Javidi_Alsaadi_CV.pdf"
                target="_blank"
                className="w-full inline-flex items-center justify-center space-x-2 px-4 py-2.5 rounded bg-white text-zinc-900 border border-zinc-300 hover:border-zinc-950 hover:bg-zinc-50 text-xs font-medium transition-colors"
              >
                <IconDownload className="w-4 h-4 text-zinc-600" />
                <span>Download Academic CV (PDF)</span>
              </a>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 border border-zinc-200 divide-y sm:divide-y-0 sm:divide-x divide-zinc-200 bg-white text-xs text-zinc-600">
            <div className="p-4 space-y-1">
              <span className="font-bold text-zinc-950 font-mono text-[11px] block uppercase">Virtual Interview Availability</span>
              <p className="text-zinc-600 leading-relaxed text-[11px]">
                Available for virtual technical and research interviews via Google Meet or Zoom across <strong>European (CET)</strong>, <strong>Eastern (EST)</strong>, and <strong>Pacific (PST)</strong> time zones.
              </p>
            </div>

            <div className="p-4 space-y-1">
              <span className="font-bold text-zinc-950 font-mono text-[11px] block uppercase">Official Verifiable Records</span>
              <p className="text-zinc-600 leading-relaxed text-[11px]">
                Official university transcripts (19.16 B.Sc. GPA), Dean&apos;s commendation letter, and Teaching Assistant verification letter are immediately available upon request.
              </p>
            </div>

            <div className="p-4 space-y-1">
              <span className="font-bold text-zinc-950 font-mono text-[11px] block uppercase">Direct Communication</span>
              <p className="text-zinc-600 leading-relaxed text-[11px]">
                Direct primary contact: <a href="mailto:reyhane.code@gmail.com" className="text-zinc-950 underline font-mono font-medium">reyhane.code@gmail.com</a>. Prompt responses guaranteed within 24 hours.
              </p>
            </div>
          </div>
        </section>

      </div>

      {/* DOCUMENT INSPECTOR MODAL */}
      {activeDocumentModal && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/80 backdrop-blur-sm transition-all"
          onClick={() => setActiveDocumentModal(null)}
        >
          <div
            className="relative max-w-4xl w-full max-h-[92vh] flex flex-col bg-white border border-zinc-300 rounded-md overflow-hidden shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-200 bg-zinc-50">
              <div className="flex items-center space-x-2 overflow-hidden">
                <span className="w-2 h-2 rounded-full bg-[#E30613] shrink-0" />
                <span className="text-xs font-mono text-zinc-950 font-bold uppercase tracking-wider truncate">
                  {activeDocumentModal.title}
                </span>
                {activeDocumentModal.badge && (
                  <span className="text-xs font-mono bg-zinc-200 px-2 py-0.5 rounded text-zinc-800 font-semibold whitespace-nowrap">
                    {activeDocumentModal.badge}
                  </span>
                )}
              </div>
              <button
                onClick={() => setActiveDocumentModal(null)}
                className="px-2.5 py-1 rounded bg-zinc-200 hover:bg-zinc-300 text-zinc-900 text-xs font-mono transition-colors shrink-0 cursor-pointer"
                aria-label="Close modal"
              >
                ✕ Close (Esc)
              </button>
            </div>

            {/* Dual Version Version-Switcher Tabs (English Translation vs. Original Persian Document) */}
            {activeDocumentModal.hasDualVersion && (
              <div className="flex flex-wrap items-center justify-between gap-2 px-4 py-2 bg-zinc-100 border-b border-zinc-200">
                <div className="flex items-center space-x-1.5">
                  <button
                    onClick={() => setTranscriptTab("en")}
                    className={`px-3 py-1.5 rounded text-xs font-mono font-medium transition-colors cursor-pointer ${transcriptTab === "en"
                      ? "bg-zinc-950 text-white shadow-2xs font-semibold"
                      : "bg-white text-zinc-700 hover:bg-zinc-200 border border-zinc-300"
                      }`}
                  >
                    English Academic Translation (Unofficial)
                  </button>
                  <button
                    onClick={() => setTranscriptTab("fa")}
                    className={`px-3 py-1.5 rounded text-xs font-mono font-medium transition-colors cursor-pointer ${transcriptTab === "fa"
                      ? "bg-zinc-950 text-white shadow-2xs font-semibold"
                      : "bg-white text-zinc-700 hover:bg-zinc-200 border border-zinc-300"
                      }`}
                  >
                    Original Persian Document
                  </button>
                </div>
                <div className="text-[11px] font-mono text-zinc-600 hidden sm:block">
                  {transcriptTab === "en"
                    ? "Evaluative Record (Canada / NZ / US Standards)"
                    : "Authentic Official University Record"}
                </div>
              </div>
            )}

            {/* Modal Image Viewport (Pre-reserved dimensions prevent layout shift / jumping on image load) */}
            <div className="overflow-auto p-4 flex items-center justify-center bg-zinc-100/90 h-[68vh] min-h-[380px] sm:min-h-[520px] max-h-[72vh] relative">
              <img
                src={
                  activeDocumentModal.hasDualVersion
                    ? transcriptTab === "en"
                      ? activeDocumentModal.englishSrc
                      : activeDocumentModal.persianSrc
                    : activeDocumentModal.src
                }
                alt={
                  activeDocumentModal.hasDualVersion
                    ? transcriptTab === "en"
                      ? "English Academic Translation"
                      : "Original Persian Document"
                    : activeDocumentModal.alt
                }
                className="max-w-full max-h-full object-contain rounded border border-zinc-200 shadow-sm bg-white"
                loading="eager"
              />
            </div>

            {/* Modal Footer with Active Version Download Button & Disclaimers */}
            <div className="p-4 bg-white border-t border-zinc-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
              <div className="space-y-0.5 text-xs text-zinc-700 max-w-xl">
                {activeDocumentModal.hasDualVersion ? (
                  transcriptTab === "en" ? (
                    <p className="leading-relaxed">
                      <strong className="text-zinc-950 font-semibold">Unofficial English Academic Translation:</strong> Prepared for graduate admissions evaluation. Official certified and sworn translation bearing the seal of the Ministry of Justice and Ministry of Foreign Affairs is available upon institutional request.
                    </p>
                  ) : (
                    <p className="leading-relaxed">
                      <strong className="text-zinc-950 font-semibold">Official University Document:</strong> Authentic original record issued and authenticated by Dr. Shariaty Technical University.
                    </p>
                  )
                ) : (
                  <p className="leading-relaxed">{activeDocumentModal.details}</p>
                )}
              </div>

              {/* Dynamic Download Button (Downloads Currently Selected Version) */}
              <div className="shrink-0">
                {activeDocumentModal.hasDualVersion ? (
                  <a
                    href={transcriptTab === "en" ? activeDocumentModal.englishPdf : activeDocumentModal.persianPdf}
                    download
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center space-x-2 px-4 py-2 rounded bg-zinc-950 hover:bg-zinc-800 text-white font-mono text-xs font-medium transition-colors shadow-2xs cursor-pointer"
                  >
                    <IconDownload className="w-3.5 h-3.5 text-white" />
                    <span>
                      {transcriptTab === "en"
                        ? (activeDocumentModal.englishDownloadLabel || "Download English (PDF)")
                        : (activeDocumentModal.persianDownloadLabel || "Download Original Document")}
                    </span>
                  </a>
                ) : (
                  activeDocumentModal.downloadUrl && (
                    <a
                      href={activeDocumentModal.downloadUrl}
                      download
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center space-x-2 px-4 py-2 rounded bg-zinc-950 hover:bg-zinc-800 text-white font-mono text-xs font-medium transition-colors shadow-2xs cursor-pointer"
                    >
                      <IconDownload className="w-3.5 h-3.5 text-white" />
                      <span>{activeDocumentModal.downloadLabel || "Download Document"}</span>
                    </a>
                  )
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}

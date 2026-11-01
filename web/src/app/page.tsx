"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  IconGraduation,
  IconPaper,
  IconApp,
  IconAward,
  IconSparkles,
  IconDownload,
  IconExternal,
  IconGithub,
  IconLinkedin,
  IconMail,
  IconCpu,
  IconLeaf,
  IconShield,
  IconChevronRight,
  IconCheck,
} from "@/components/Icons";

export default function HomePage() {
  const [copiedEmail, setCopiedEmail] = useState(false);
  const [activeDocumentModal, setActiveDocumentModal] = useState<{
    src: string;
    alt: string;
    title: string;
    badge?: string;
    details: string;
    downloadUrl?: string;
    downloadLabel?: string;
  } | null>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setActiveDocumentModal(null);
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
      {/* Schema.org Structured Data for Google Search & AI Crawlers */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Person",
            name: "Reyhane Javidi Alsaadi",
            url: "https://reyhane-alsaadi.github.io/",
            image: "https://reyhane-alsaadi.github.io/my-img.jpg",
            email: "reyhane.code@gmail.com",
            jobTitle: "Computer Engineering Researcher & Software Engineer",
            worksFor: {
              "@type": "EducationalOrganization",
              name: "Dr. Shariaty Technical University, Tehran",
            },
            affiliation: {
              "@type": "EducationalOrganization",
              name: "Department of Computer Engineering, Dr. Shariaty Technical University, Tehran",
            },
            alumniOf: {
              "@type": "EducationalOrganization",
              name: "Dr. Shariaty Technical University",
            },
            award: [
              "University Official Commendation & Honor Letter for Academic & Technical Accomplishment",
              "Top Academic Distinction / Top 5% Cohort (B.Sc. GPA: 19.16 / 20.00, Associate GPA: 18.96 / 20.00)",
              "Official Teaching Assistant (TA) Distinction in Game Development",
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
              "Full-Stack Software Engineering",
              "NestJS",
              "PostgreSQL",
              "Redis",
              "Next.js",
              "React",
              "Kotlin",
              "Jetpack Compose",
              "ONNX Runtime Mobile",
            ],
          }),
        }}
      />

      {/* HERO SECTION — EDITORIAL SWISS LIGHT */}
      <section className="relative overflow-hidden pt-12 pb-18 border-b border-zinc-200/90 bg-[#fafaf9] text-zinc-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            {/* Bio Details */}
            <div className="lg:col-span-8 space-y-6">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded bg-zinc-100 border border-zinc-200 text-zinc-800 text-xs font-mono font-medium tracking-wide">
                <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
                <span>Prospective Graduate Researcher • Seeking M.Sc. / Ph.D. Opportunities (Fall 2026 / Spring 2027)</span>
              </div>

              <div className="space-y-2">
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-zinc-950 font-sans">
                  Reyhane Javidi Alsaadi
                </h1>
                <p className="text-lg sm:text-xl text-zinc-700 font-medium tracking-tight">
                  Computer Engineering Scholar &amp; Full-Stack AI Engineer
                </p>
                <p className="text-xs text-zinc-500 font-mono flex items-center space-x-2 pt-0.5">
                  <IconGraduation className="w-4 h-4 text-zinc-600" />
                  <span>Department of Computer Engineering, Dr. Shariaty Technical University, Tehran</span>
                </p>
              </div>

              <p className="text-zinc-700 text-base leading-relaxed max-w-2xl">
                Combining <strong className="text-zinc-950 font-semibold">mathematical research rigor</strong> in Vision Foundation Models (DINOv2, BioCLIP) and Few-Shot Learning with <strong className="text-zinc-950 font-semibold">practical software engineering</strong>. Ranked top of my class with a <strong className="text-zinc-950 font-semibold">19.16/20 B.Sc. GPA</strong> (and 18.96/20 Associate GPA), honored with an official university commendation letter, experienced as a <strong className="text-zinc-950 font-semibold">Teaching Assistant</strong>, and lead author of the BioDINO-Edge framework.
              </p>

              {/* Quick Contact & Action Buttons */}
              <div className="flex flex-wrap gap-2.5 pt-1">
                <a
                  href="/Reyhane_Javidi_Alsaadi_CV.pdf"
                  target="_blank"
                  className="inline-flex items-center space-x-2 px-4 py-2.5 rounded bg-zinc-950 text-white font-medium text-xs hover:bg-zinc-800 transition-colors shadow-xs"
                >
                  <IconDownload className="w-3.5 h-3.5" />
                  <span>Download Academic CV (PDF)</span>
                </a>

                <a
                  href="/biodino_edge_paper.pdf"
                  target="_blank"
                  className="inline-flex items-center space-x-2 px-4 py-2.5 rounded bg-white text-zinc-900 font-medium text-xs hover:bg-zinc-100 border border-zinc-300 hover:border-zinc-950 transition-colors"
                >
                  <IconPaper className="w-3.5 h-3.5 text-zinc-600" />
                  <span>Lead Paper (PDF)</span>
                </a>

                <Link
                  href="/projects/biodino-edge-android/"
                  className="inline-flex items-center space-x-2 px-4 py-2.5 rounded bg-white text-zinc-900 font-medium text-xs hover:bg-zinc-100 border border-zinc-300 hover:border-zinc-950 transition-colors"
                >
                  <IconApp className="w-3.5 h-3.5 text-zinc-600" />
                  <span>Android App</span>
                </Link>

                <button
                  onClick={handleCopyEmail}
                  className="inline-flex items-center space-x-2 px-4 py-2.5 rounded bg-zinc-100 text-zinc-800 font-mono text-xs hover:bg-zinc-200 border border-zinc-200 transition-colors"
                >
                  {copiedEmail ? (
                    <>
                      <IconCheck className="w-3.5 h-3.5 text-emerald-600" />
                      <span className="text-emerald-700 font-semibold">Email Copied!</span>
                    </>
                  ) : (
                    <>
                      <IconMail className="w-3.5 h-3.5 text-zinc-600" />
                      <span>reyhane.code@gmail.com</span>
                    </>
                  )}
                </button>

                <a
                  href="https://www.linkedin.com/in/reyhane-javidi"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center space-x-1.5 px-3.5 py-2.5 rounded bg-zinc-100 text-[#0A66C2] font-mono text-xs hover:bg-zinc-200 border border-zinc-200 transition-colors"
                  title="LinkedIn Profile"
                >
                  <IconLinkedin className="w-3.5 h-3.5" />
                  <span className="text-zinc-900 font-sans font-medium">LinkedIn</span>
                </a>

                <a
                  href="https://github.com/reyhane-code"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center space-x-1.5 px-3.5 py-2.5 rounded bg-zinc-100 text-zinc-900 font-mono text-xs hover:bg-zinc-200 border border-zinc-200 transition-colors"
                  title="GitHub Profile"
                >
                  <IconGithub className="w-3.5 h-3.5" />
                  <span className="text-zinc-900 font-sans font-medium">GitHub</span>
                </a>
              </div>

              {/* Key Highlights Snapshot — Swiss Modular Matrix */}
              <div className="grid grid-cols-2 sm:grid-cols-4 border border-zinc-200 divide-x divide-y sm:divide-y-0 divide-zinc-200 bg-white max-w-2xl shadow-xs mt-4">
                <div className="p-3.5">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-zinc-500">B.Sc. GPA (Ongoing)</div>
                  <div className="text-xl font-bold text-zinc-950 font-mono mt-0.5">19.16 <span className="text-xs font-normal text-zinc-500">/ 20</span></div>
                  <div className="text-[11px] text-zinc-600 mt-0.5">Top of Cohort (~3.97/4.0)</div>
                </div>
                <div className="p-3.5">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-zinc-500">Associate GPA</div>
                  <div className="text-xl font-bold text-zinc-950 font-mono mt-0.5">18.96 <span className="text-xs font-normal text-zinc-500">/ 20</span></div>
                  <div className="text-[11px] text-zinc-600 mt-0.5">70 Credits Completed</div>
                </div>
                <div className="p-3.5">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-zinc-500">Class Standing</div>
                  <div className="text-xl font-bold text-zinc-950 font-mono mt-0.5">Top 5%</div>
                  <div className="text-[11px] text-zinc-600 mt-0.5">Dean&apos;s List • Summa Cum Laude</div>
                </div>
                <div className="p-3.5">
                  <div className="text-[10px] font-mono uppercase tracking-wider text-zinc-500">Lead Research</div>
                  <div className="text-xl font-bold text-zinc-950 font-mono mt-0.5">98.72%</div>
                  <div className="text-[11px] text-zinc-600 mt-0.5">BioDINO-Edge Peak Acc</div>
                </div>
              </div>
            </div>

            {/* Profile Picture Card — Editorial Archival Frame */}
            <div className="lg:col-span-4 flex justify-center">
              <div className="w-64 sm:w-72 border border-zinc-200 bg-white p-2.5 shadow-xs">
                <div className="relative overflow-hidden bg-zinc-100 aspect-[4/5]">
                  <img
                    src="/my-img.jpg"
                    alt="Reyhane Javidi Alsaadi"
                    className="w-full h-full object-cover object-center grayscale hover:grayscale-0 transition-all duration-300"
                  />
                </div>
                <div className="p-3 bg-white border-t border-zinc-200 mt-2">
                  <div className="font-bold text-zinc-950 text-sm tracking-tight">Reyhane Javidi Alsaadi</div>
                  <div className="text-xs text-zinc-500 font-mono mt-0.5">Lead Researcher &amp; Software Engineer</div>
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

      {/* MAIN CONTENT CONTAINER — EDITORIAL SWISS LIGHT */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14 space-y-16">

        {/* 01. ACADEMIC TRAJECTORY & GRADUATE AVAILABILITY TIMELINE */}
        <section id="trajectory" className="border border-zinc-200 bg-white p-6 sm:p-7 shadow-xs space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-zinc-200 pb-3">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
              <span className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
                01 // Academic Trajectory &amp; Graduate Applicant Status
              </span>
            </div>
            <span className="text-[11px] font-mono text-zinc-700 bg-zinc-100 px-2.5 py-0.5 rounded border border-zinc-200 w-fit">
              • Target Entry: Fall 2026 / Spring 2027
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-zinc-200 border border-zinc-200 bg-white">
            {/* Step 1 */}
            <div className="p-4 sm:p-5 space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-zinc-950">2022 — Present</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-100 text-zinc-700 border border-zinc-200">Undergraduate</span>
              </div>
              <h3 className="text-sm font-bold text-zinc-950">B.Sc. in Computer Engineering</h3>
              <p className="text-xs text-zinc-600 leading-relaxed">
                Top 5% Distinction (B.Sc. GPA: <strong className="text-zinc-950">19.16 / 20.00</strong>, Associate GPA: <strong className="text-zinc-950">18.96 / 20.00</strong>). University Official Commendation Letter &amp; Teaching Assistant (TA).
              </p>
            </div>

            {/* Step 2 */}
            <div className="p-4 sm:p-5 space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-zinc-950">2025 — 2026</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-100 text-zinc-700 border border-zinc-200">Lead Author</span>
              </div>
              <h3 className="text-sm font-bold text-zinc-950">BioDINO-Edge Research</h3>
              <p className="text-xs text-zinc-600 leading-relaxed">
                Formulation &amp; benchmark of dual-foundation edge framework (<strong className="text-zinc-950">98.72% acc</strong>, 22 ms CPU, INT8 APK). Target: IEEE T-PAMI / CVPR.
              </p>
            </div>

            {/* Step 3 */}
            <div className="p-4 sm:p-5 space-y-1.5 bg-zinc-50/50">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-zinc-950">Fall 2026 / Spring 2027</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#E30613]/10 text-[#E30613] border border-[#E30613]/20 font-semibold">Active Applicant</span>
              </div>
              <h3 className="text-sm font-bold text-zinc-950">M.Sc. / Ph.D. Enrollment</h3>
              <p className="text-xs text-zinc-600 leading-relaxed">
                Seeking graduate research assistantships in <strong className="text-zinc-950">Edge AI &amp; Vision Foundation Models</strong>. Immediate full-time availability.
              </p>
            </div>
          </div>
        </section>

        {/* 02. BALANCED ACADEMIC PILLARS */}
        <section id="pillars" className="space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
              02 // Core Scholastic &amp; Engineering Pillars
            </h2>
            <span className="text-xs text-zinc-500 font-mono">Graduate Research Readiness</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 border border-zinc-200 divide-y sm:divide-y-0 sm:divide-x divide-zinc-200 bg-white shadow-xs">
            {/* Pillar 1: Scholastic */}
            <div className="p-5 space-y-2.5">
              <div className="w-8 h-8 rounded bg-zinc-100 text-zinc-900 flex items-center justify-center font-bold">
                <IconGraduation className="w-4 h-4" />
              </div>
              <h3 className="font-bold text-zinc-950 text-sm tracking-tight">Academic Excellence</h3>
              <p className="text-xs text-zinc-600 leading-relaxed">
                Ranked in the <strong className="text-zinc-900">top 5% of cohort</strong> across both degrees with a B.Sc. GPA of <strong className="text-zinc-900">19.16 / 20.00</strong> (~3.97/4.00) and Associate GPA of <strong className="text-zinc-900">18.96 / 20.00</strong>, with straight 20/20 records in algorithms, AI, and systems.
              </p>
            </div>

            {/* Pillar 2: Research */}
            <div className="p-5 space-y-2.5">
              <div className="w-8 h-8 rounded bg-zinc-100 text-zinc-900 flex items-center justify-center font-bold">
                <IconPaper className="w-4 h-4" />
              </div>
              <h3 className="font-bold text-zinc-950 text-sm tracking-tight">Lead Research Contribution</h3>
              <p className="text-xs text-zinc-600 leading-relaxed">
                First author of BioDINO-Edge, formulating closed-form Ledoit-Wolf covariance shrinkage on DINOv2 + BioCLIP for few-shot edge pathology (98.72% peak accuracy).
              </p>
            </div>

            {/* Pillar 3: Teaching */}
            <div className="p-5 space-y-2.5">
              <div className="w-8 h-8 rounded bg-zinc-100 text-zinc-900 flex items-center justify-center font-bold">
                <IconAward className="w-4 h-4" />
              </div>
              <h3 className="font-bold text-zinc-950 text-sm tracking-tight">Teaching &amp; Mentorship</h3>
              <p className="text-xs text-zinc-600 leading-relaxed">
                Teaching Assistant (TA) for Game Development &amp; Systems, supported by an <strong className="text-zinc-900">official university verification letter</strong> recognizing dedication to student mentorship.
              </p>
            </div>

            {/* Pillar 4: Engineering & Full-Stack */}
            <div className="p-5 space-y-2.5">
              <div className="w-8 h-8 rounded bg-zinc-100 text-zinc-900 flex items-center justify-center font-bold">
                <IconCpu className="w-4 h-4" />
              </div>
              <h3 className="font-bold text-zinc-950 text-sm tracking-tight">Systems Engineering</h3>
              <p className="text-xs text-zinc-600 leading-relaxed">
                Proficient in building end-to-end applications: from mobile native Kotlin/ONNX edge inferencing to modern TypeScript, Next.js, and scalable backend/database architectures.
              </p>
            </div>
          </div>
        </section>

        {/* 03. EDUCATION & ACADEMIC STANDING */}
        <section id="education" className="space-y-6">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
              <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
                03 // Academic Education &amp; Formal Transcripts
              </h2>
            </div>
            <span className="text-xs text-zinc-500 font-mono">B.Sc. &amp; A.Sc. Official Records</span>
          </div>

          {/* 1. BACHELOR'S DEGREE (CURRENT / ONGOING) */}
          <div className="border border-zinc-200 bg-white p-6 sm:p-7 shadow-xs space-y-6">
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
              <button
                onClick={() =>
                  setActiveDocumentModal({
                    src: "/nomerat-2.jpg",
                    alt: "B.Sc. Official University Transcript Scan",
                    title: "B.Sc. Academic Transcript (TVU Portal Scan)",
                    badge: "B.Sc. GPA: 19.16 / 20.00",
                    details:
                      "Official online registry scan from TVU Academic Portal (Bustan). Covers 50 graded core credits with straight 20.00 marks in Algorithms, AI, Automata, and Software Engineering.",
                    downloadUrl: "/nomerat-2.jpg",
                    downloadLabel: "Download Scan (JPG)",
                  })
                }
                className="inline-flex items-center space-x-2 px-3.5 py-2 rounded bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 text-zinc-900 font-mono text-xs font-medium transition-colors w-fit shadow-2xs"
              >
                <IconPaper className="w-3.5 h-3.5 text-zinc-700" />
                <span>Inspect B.Sc. Transcript Scan</span>
              </button>
            </div>

            {/* Metrics Matrix */}
            <div className="grid grid-cols-1 md:grid-cols-3 border border-zinc-200 divide-y md:divide-y-0 md:divide-x divide-zinc-200 bg-white">
              <div className="p-4">
                <span className="text-[11px] text-zinc-500 block font-mono uppercase">Cumulative B.Sc. GPA</span>
                <span className="text-2xl font-bold text-zinc-950 font-mono mt-1 block">19.16 / 20.00</span>
                <span className="text-[11px] text-zinc-600 block mt-0.5">~3.97 / 4.00 (Summa Cum Laude)</span>
              </div>
              <div className="p-4">
                <span className="text-[11px] text-zinc-500 block font-mono uppercase">Class Standing</span>
                <span className="text-2xl font-bold text-zinc-950 font-mono mt-1 block">Top 5% / Dean&apos;s List</span>
                <span className="text-[11px] text-zinc-600 block mt-0.5">Top-ranked student in cohort</span>
              </div>
              <div className="p-4">
                <span className="text-[11px] text-zinc-500 block font-mono uppercase">Curriculum Progress</span>
                <span className="text-base font-bold text-zinc-950 mt-1 block">50 Credits Graded</span>
                <span className="text-[11px] text-zinc-600 block mt-0.5">Senior Year • Final Semester In Progress</span>
              </div>
            </div>

            {/* Selected High-Distinction Coursework */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-zinc-950 uppercase tracking-wider font-mono">
                  Advanced Computer Science, Mathematics &amp; AI Coursework (Exact Marks)
                </span>
                <span className="text-[11px] font-mono text-zinc-600 bg-zinc-100 px-2 py-0.5 rounded border border-zinc-200">
                  Transcripts Verifiable
                </span>
              </div>

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
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Game Development</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Internet Engineering</span>
                  <span className="font-mono font-bold text-zinc-950">19.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Special Topics in CS</span>
                  <span className="font-mono font-bold text-zinc-950">19.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Technical English</span>
                  <span className="font-mono font-bold text-zinc-950">19.00 / 20</span>
                </div>
              </div>
            </div>
          </div>

          {/* 2. ASSOCIATE DEGREE (COMPLETED) */}
          <div className="border border-zinc-200 bg-white p-6 sm:p-7 shadow-xs space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border-b border-zinc-200 pb-4">
              <div>
                <div className="flex items-center space-x-2">
                  <span className="px-2 py-0.5 rounded bg-zinc-200 text-zinc-900 text-[10px] font-mono uppercase tracking-wider font-semibold">
                    Graduated Degree
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
              <button
                onClick={() =>
                  setActiveDocumentModal({
                    src: "/nomerat-1.jpg",
                    alt: "Associate Official University Transcript Scan",
                    title: "Associate Academic Transcript (TVU Registry Scan)",
                    badge: "A.Sc. GPA: 18.96 / 20.00",
                    details:
                      "Official university registry transcript. 70 units completed with perfect 20.00 marks in Data Structures, Advanced Programming, Logic Circuits, Databases, and Capstone Project.",
                    downloadUrl: "/nomerat-1.jpg",
                    downloadLabel: "Download Scan (JPG)",
                  })
                }
                className="inline-flex items-center space-x-2 px-3.5 py-2 rounded bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 text-zinc-900 font-mono text-xs font-medium transition-colors w-fit shadow-2xs"
              >
                <IconPaper className="w-3.5 h-3.5 text-zinc-700" />
                <span>Inspect Associate Transcript Scan</span>
              </button>
            </div>

            {/* Metrics Matrix */}
            <div className="grid grid-cols-1 md:grid-cols-3 border border-zinc-200 divide-y md:divide-y-0 md:divide-x divide-zinc-200 bg-white">
              <div className="p-4">
                <span className="text-[11px] text-zinc-500 block font-mono uppercase">Final Cumulative GPA</span>
                <span className="text-2xl font-bold text-zinc-950 font-mono mt-1 block">18.96 / 20.00</span>
                <span className="text-[11px] text-zinc-600 block mt-0.5">~3.91 / 4.00 (High Honors)</span>
              </div>
              <div className="p-4">
                <span className="text-[11px] text-zinc-500 block font-mono uppercase">Total Credit Units</span>
                <span className="text-2xl font-bold text-zinc-950 font-mono mt-1 block">70 Credits</span>
                <span className="text-[11px] text-zinc-600 block mt-0.5">Fully Conferred &amp; Verified</span>
              </div>
              <div className="p-4">
                <span className="text-[11px] text-zinc-500 block font-mono uppercase">Department Standing</span>
                <span className="text-base font-bold text-zinc-950 mt-1 block">Top 5% Distinction</span>
                <span className="text-[11px] text-zinc-600 block mt-0.5">Highest Graduation Honors</span>
              </div>
            </div>

            {/* Selected High-Distinction Coursework */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-zinc-950 uppercase tracking-wider font-mono">
                  Foundational Software Engineering, Systems &amp; Hardware Coursework
                </span>
                <span className="text-[11px] font-mono text-zinc-600 bg-zinc-100 px-2 py-0.5 rounded border border-zinc-200">
                  Official Records
                </span>
              </div>

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
                  <span className="text-zinc-800 font-medium">Digital Logic Circuits</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Database Systems</span>
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
                  <span className="text-zinc-800 font-medium">Hardware &amp; Embedded Prog.</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Mobile App Development</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Systems Analysis &amp; Design</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Operating Systems Lab</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Web Programming</span>
                  <span className="font-mono font-bold text-zinc-950">19.00 / 20</span>
                </div>
                <div className="p-3 flex items-center justify-between">
                  <span className="text-zinc-800 font-medium">Final Capstone Project</span>
                  <span className="font-mono font-bold text-zinc-950">20.00 / 20</span>
                </div>
              </div>
            </div>
          </div>

          {/* Academic Transparency Note */}
          <div className="p-4 rounded border border-zinc-200 bg-zinc-50 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 text-xs text-zinc-600">
            <div className="flex items-center space-x-2">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-600" />
              <span>
                <strong>Academic Verification:</strong> Official Persian portal records are verifiable via TVU. Unofficial English course-by-course translation and course syllabi descriptions are prepared for admission committees.
              </span>
            </div>
            <div className="flex items-center space-x-2 shrink-0">
              <a
                href="/nomerat-2.jpg"
                target="_blank"
                rel="noreferrer"
                className="text-zinc-900 underline font-mono text-[11px] hover:text-[#E30613]"
              >
                Direct JPG (B.Sc.)
              </a>
              <span className="text-zinc-300">•</span>
              <a
                href="/nomerat-1.jpg"
                target="_blank"
                rel="noreferrer"
                className="text-zinc-900 underline font-mono text-[11px] hover:text-[#E30613]"
              >
                Direct JPG (Associate)
              </a>
            </div>
          </div>
        </section>

        {/* 04. HONORS, AWARDS & OFFICIAL COMMENDATIONS */}
        <section id="honors" className="space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
              <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
                04 // University Honors &amp; Official Commendations
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
                  Conferred &amp; Sealed by President of Dr. Shariaty Technical University • Tehran
                </p>
                <p className="text-xs text-zinc-600 leading-relaxed">
                  Formally awarded by university leadership in recognition of outstanding commitment and instructional excellence as Teaching Assistant in Game Development, recognizing constructive academic collaboration with faculty member Prof. Toktam Zoghi, dedicated mentorship of peer students in coursework projects, and exemplary departmental service.
                </p>
              </div>

              <div className="pt-2 flex flex-wrap gap-2 border-t border-zinc-100">
                <button
                  onClick={() =>
                    setActiveDocumentModal({
                      src: "/letterOfCommendation.jpg",
                      alt: "Official Presidential Letter of Commendation",
                      title: "Presidential Letter of Commendation (Ref: 5039/202/1615)",
                      badge: "University President Seal",
                      details:
                        "Official Letter of Commendation signed and sealed by the President of Dr. Shariaty Technical University, recognizing exemplary academic dedication as Teaching Assistant in Game Development.",
                      downloadUrl: "/letterOfCommendation.jpg",
                      downloadLabel: "Download Original (JPG)",
                    })
                  }
                  className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded bg-zinc-950 hover:bg-zinc-800 text-white font-mono text-xs transition-colors shadow-2xs"
                >
                  <IconPaper className="w-3.5 h-3.5" />
                  <span>Inspect Commendation Scan</span>
                </button>
                <a
                  href="/letterOfCommendation.jpg"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded bg-white hover:bg-zinc-100 border border-zinc-300 text-zinc-800 font-mono text-xs transition-colors"
                >
                  <IconDownload className="w-3.5 h-3.5 text-zinc-600" />
                  <span>JPG</span>
                </a>
              </div>
            </div>

            {/* Card 2: Scholastic Merit */}
            <div className="border border-zinc-200 bg-white p-6 shadow-xs space-y-4 flex flex-col justify-between">
              <div className="space-y-2.5">
                <div className="flex items-center justify-between border-b border-zinc-100 pb-2">
                  <span className="text-xs font-mono text-zinc-950 font-bold uppercase tracking-wider flex items-center space-x-1.5">
                    <IconGraduation className="w-3.5 h-3.5 text-zinc-700" />
                    <span>Scholastic Standing</span>
                  </span>
                  <span className="text-[10px] font-mono text-zinc-600 bg-zinc-100 px-2 py-0.5 rounded border border-zinc-200">
                    Highest Departmental Tier
                  </span>
                </div>
                <h3 className="text-base font-bold text-zinc-950">
                  Top-Tier Academic Distinction (Top 5% • B.Sc. GPA: 19.16 / 20.00)
                </h3>
                <p className="text-xs text-zinc-500 font-mono">Department of Computer Engineering</p>
                <p className="text-xs text-zinc-600 leading-relaxed">
                  Maintained top academic ranking throughout undergraduate tenure, achieving consistent near-perfect scores across core theoretical computer science, algorithms (20/20), artificial intelligence (20/20), automata theory (20/20), and systems engineering courses.
                </p>
              </div>

              <div className="pt-2 border-t border-zinc-100">
                <span className="inline-flex items-center space-x-1.5 text-xs font-mono text-zinc-700 bg-zinc-50 px-2.5 py-1 rounded border border-zinc-200">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-600" />
                  <span>Dean&apos;s List • Summa Cum Laude Equivalent (~3.97 / 4.00)</span>
                </span>
              </div>
            </div>
          </div>
        </section>

        {/* 05. TEACHING & ACADEMIC SERVICE */}
        <section id="teaching" className="space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <div className="flex items-center space-x-2">
              <span className="w-2 h-2 bg-[#E30613] rounded-xs" />
              <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
                05 // Teaching Experience &amp; Academic Mentorship
              </h2>
            </div>
            <span className="text-xs text-zinc-500 font-mono">Departmental Instruction</span>
          </div>

          <div className="border border-zinc-200 bg-white p-6 sm:p-7 shadow-xs space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-b border-zinc-200 pb-4">
              <div>
                <div className="flex items-center space-x-2">
                  <span className="px-2 py-0.5 rounded bg-zinc-950 text-white text-[10px] font-mono uppercase tracking-wider font-semibold">
                    Official Teaching Assistant
                  </span>
                  <span className="text-xs font-mono text-zinc-500">Spring 2026 Semester </span>
                </div>
                <h3 className="text-xl font-bold text-zinc-950 tracking-tight mt-1">
                  Teaching Assistant (TA) — Game Development &amp; Interactive Graphics
                </h3>
                <p className="text-xs text-zinc-600 font-mono mt-0.5">
                  Supervised by Prof. Toktam Zoghi (Assistant Professor, Dept. of Computer Engineering)
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <button
                  onClick={() =>
                    setActiveDocumentModal({
                      src: "/teachingAssistantCertificate.png",
                      alt: "Official Teaching Assistant Certificate",
                      title: "Official Teaching Assistant Verification Certificate",
                      badge: "Office of Academic Affairs Seal",
                      details:
                        "Official certificate of teaching assistantship issued by Prof. Toktam Zoghi and stamped with the official seal of the Office of Academic Affairs (اداره امور آموزش), Dr. Shariaty Technical University.",
                      downloadUrl: "/teachingAssistantCertificate.pdf",
                      downloadLabel: "Download Official PDF",
                    })
                  }
                  className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded bg-zinc-950 hover:bg-zinc-800 text-white font-mono text-xs font-medium transition-colors shadow-2xs"
                >
                  <IconPaper className="w-3.5 h-3.5" />
                  <span>Inspect Official TA Letter</span>
                </button>
                <a
                  href="/teachingAssistantCertificate.pdf"
                  target="_blank"
                  className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded bg-white hover:bg-zinc-100 border border-zinc-300 text-zinc-900 font-mono text-xs font-medium transition-colors shadow-2xs"
                >
                  <IconDownload className="w-3.5 h-3.5 text-zinc-600" />
                  <span>Download PDF</span>
                </a>
              </div>
            </div>

            {/* Instruction Highlights Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 border border-zinc-200 divide-y sm:divide-y-0 sm:divide-x divide-zinc-200 bg-white text-xs">
              <div className="p-4 space-y-1.5">
                <span className="font-bold text-zinc-950 font-mono text-[11px] block uppercase">1. Exercise Formulation &amp; Design</span>
                <p className="text-zinc-600 leading-relaxed text-[11px]">
                  Designed and structured core practical coursework assignments, debugging tasks, and algorithmic game mechanic modules in direct coordination with lead professor.
                </p>
              </div>

              <div className="p-4 space-y-1.5">
                <span className="font-bold text-zinc-950 font-mono text-[11px] block uppercase">2. Student Mentorship &amp; Labs</span>
                <p className="text-zinc-600 leading-relaxed text-[11px]">
                  Conducted weekly office hours and problem-solving labs for 40+ engineering students, addressing technical inquiries and debugging code implementations.
                </p>
              </div>

              <div className="p-4 space-y-1.5">
                <span className="font-bold text-zinc-950 font-mono text-[11px] block uppercase">3. Rigorous Evaluation &amp; Grading</span>
                <p className="text-zinc-600 leading-relaxed text-[11px]">
                  Tested, verified, and graded students&apos; programming submissions and capstone project implementations, with verified dedication commended in writing by university administration.
                </p>
              </div>
            </div>

            <div className="p-3 bg-zinc-50 border border-zinc-200 rounded text-xs text-zinc-600 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
              <span className="flex items-center space-x-2">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-600" />
                <span><strong>Verification Status:</strong> Official verification letter signed by Prof. Toktam Zoghi &amp; stamped by University Office of Academic Affairs (اداره امور آموزش).</span>
              </span>
              <span className="font-mono text-[11px] text-zinc-500 whitespace-nowrap">Official Date: 1405/04/10</span>
            </div>
          </div>
        </section>

        {/* 06. PEER-REVIEWED SCIENTIFIC PUBLICATIONS */}
        <section id="publications" className="space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
              06 // Peer-Reviewed Scientific Publications
            </h2>
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
                Target: IEEE T-PAMI / CVPR / CompAg
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
              We present <strong>BioDINO-Edge</strong>, a dual-foundation framework uniting self-supervised spatial patch modeling (<strong>DINOv2 Small</strong>) with organismal vision-language hierarchies (<strong>BioCLIP ViT-B</strong>). Introduces <em>Purified Taxonomic Domain Synthesis</em> and <em>Regularized Fisher-Discriminant Alignment with analytical Ledoit-Wolf covariance shrinkage</em>, resolving singular covariance matrices without backpropagation in &lt;0.003 ms. A <em>Soft-Anchored Transductive Self-Calibration</em> removes 5-shot centroid shift, yielding a <strong className="text-zinc-950">98.72% peak accuracy</strong> on PlantVillage and <strong className="text-zinc-950">83.61%</strong> on PlantDoc in-the-wild (+13.0% over 2026 SOTA).
            </p>

            {/* Research TL;DR Matrix for Faculty Reviewers */}
            <div className="border border-zinc-200 divide-y md:divide-y-0 md:divide-x divide-zinc-200 grid grid-cols-1 md:grid-cols-3 bg-zinc-50/60 text-xs">
              <div className="p-3.5 space-y-1">
                <span className="text-zinc-500 font-mono text-[11px] font-bold block uppercase">• Problem:</span>
                <p className="text-zinc-700 text-[11px] leading-relaxed">
                  Severe data scarcity for novel foliar pathogens &amp; tightly constrained edge microcontroller hardware.
                </p>
              </div>
              <div className="p-3.5 space-y-1">
                <span className="text-zinc-950 font-mono text-[11px] font-bold block uppercase">• Core Innovation:</span>
                <p className="text-zinc-700 text-[11px] leading-relaxed">
                  Coupling DINOv2 + BioCLIP with analytical Ledoit-Wolf covariance shrinkage in &lt;0.003 ms (zero backprop).
                </p>
              </div>
              <div className="p-3.5 space-y-1">
                <span className="text-zinc-950 font-mono text-[11px] font-bold block uppercase">• Empirical Impact:</span>
                <p className="text-zinc-700 text-[11px] leading-relaxed">
                  <strong>98.72%</strong> peak acc, <strong>83.61%</strong> PlantDoc in-the-wild SOTA (+13.0%), with <strong>22.05 MB</strong> INT8 edge model.
                </p>
              </div>
            </div>

            {/* Metrics Swiss Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 border border-zinc-200 divide-x divide-y sm:divide-y-0 divide-zinc-200 bg-white text-center">
              <div className="p-3.5">
                <div className="text-xl font-bold text-zinc-950 font-mono">98.72%</div>
                <div className="text-[11px] text-zinc-500 font-mono uppercase mt-0.5">Peak Acc (PV-11)</div>
              </div>
              <div className="p-3.5">
                <div className="text-xl font-bold text-zinc-950 font-mono">83.61%</div>
                <div className="text-[11px] text-zinc-500 font-mono uppercase mt-0.5">PlantDoc SOTA (+13.0%)</div>
              </div>
              <div className="p-3.5">
                <div className="text-xl font-bold text-zinc-950 font-mono">22.05 MB</div>
                <div className="text-[11px] text-zinc-500 font-mono uppercase mt-0.5">INT8 Standalone Model</div>
              </div>
              <div className="p-3.5">
                <div className="text-xl font-bold text-zinc-950 font-mono">0.81%</div>
                <div className="text-[11px] text-zinc-500 font-mono uppercase mt-0.5">Calibrated ECE Score</div>
              </div>
            </div>

            <div className="pt-2 flex flex-wrap gap-2.5">
              <Link
                href="/research/biodino-edge/"
                className="inline-flex items-center space-x-2 px-4 py-2 rounded bg-zinc-950 text-white font-medium text-xs hover:bg-zinc-800 transition-colors"
              >
                <IconPaper className="w-3.5 h-3.5" />
                <span>Read Full Interactive Paper &amp; Saliency Maps</span>
              </Link>
              <a
                href="/biodino_edge_paper.pdf"
                target="_blank"
                className="inline-flex items-center space-x-2 px-4 py-2 rounded bg-white text-zinc-900 font-medium text-xs hover:bg-zinc-50 border border-zinc-300 hover:border-zinc-950 transition-colors"
              >
                <IconDownload className="w-3.5 h-3.5 text-zinc-600" />
                <span>Download Manuscript (PDF, 4.4 MB)</span>
              </a>
            </div>
          </div>
        </section>

        {/* 07. RESEARCH INTERESTS & PROSPECTIVE GRADUATE DIRECTIONS */}
        <section id="research-interests" className="space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
              07 // Prospective Graduate Research Directions
            </h2>
            <span className="text-xs text-zinc-500 font-mono">Core Theoretical Topics</span>
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
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Zero-Shot Generalization</span>
              </div>
            </div>

            {/* Direction 2 */}
            <div className="border border-zinc-200 bg-white p-6 shadow-xs space-y-3">
              <div className="flex items-center space-x-2 border-b border-zinc-100 pb-2">
                <span className="w-2 h-2 rounded-xs bg-zinc-950" />
                <h3 className="font-bold text-zinc-950 text-sm">Autonomous Support-Buffer Outlier Rejection on Constrained Edge Hardware</h3>
              </div>
              <p className="text-xs text-zinc-600 leading-relaxed">
                In robotic scouting and few-shot adaptation, support caches frequently encounter sensor blur or non-foliar occlusions. I plan to research <strong className="text-zinc-900">closed-form statistical filtering</strong> (robust Mahalanobis distance and analytical MCD estimators) directly inside edge support buffers for autonomous purge in &lt;0.01 ms with zero backprop.
              </p>
              <div className="pt-1 flex flex-wrap gap-1.5 font-mono text-[10px] text-zinc-700">
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Robust Mahalanobis Filter</span>
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Outlier Rejection</span>
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
                Investigating analytical closed-form linear discriminants, sub-4-bit INT4/INT8 quantization, and transductive calibration on high-throughput microprocessors to deploy multi-scale vision transformers directly onto sub-$20 agricultural microcontrollers and drone payloads with deterministic sub-15ms latency.
              </p>
              <div className="pt-1 flex flex-wrap gap-1.5 font-mono text-[10px] text-zinc-700">
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">4-Bit Quantization</span>
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Low-Power Microcontrollers</span>
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Closed-Form Solvers</span>
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
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Knowledge Graphs</span>
                <span className="px-2 py-0.5 rounded bg-zinc-100 border border-zinc-200">Uncertainty Calibration</span>
              </div>
            </div>
          </div>
        </section>

        {/* 08. SOFTWARE & SYSTEMS ENGINEERING */}
        <section id="engineering" className="space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
              08 // Software Engineering &amp; Systems Architecture
            </h2>
            <Link
              href="/projects/biodino-edge-android/"
              className="text-xs text-zinc-900 hover:text-zinc-600 flex items-center space-x-1 font-mono font-semibold"
            >
              <span>Android App Showcase</span>
              <IconChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
            {/* Card 1: BioDINO-Edge Android */}
            <div className="border border-zinc-200 bg-white p-6 shadow-xs space-y-4 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="px-2 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-[10px] font-mono">
                    Kotlin 2.0 &amp; Compose
                  </span>
                  <span className="px-2 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-[10px] font-mono">
                    ONNX Runtime Mobile NNAPI
                  </span>
                  <span className="px-2 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-[10px] font-mono">
                    22.7 MB APK
                  </span>
                </div>
                <h3 className="text-lg font-bold text-zinc-950">BioDINO-Edge Mobile: 100% Offline Edge Scanner</h3>
                <p className="text-xs text-zinc-600 leading-relaxed">
                  Native Android application running foundation model inference on edge processors at <strong className="text-zinc-900">&gt;55 FPS</strong>. Built with a zero-allocation <code>PreallocatedTensor</code> direct buffer preventing Garbage Collector frame drops, and a 3-layer security gate rejecting dark frames and non-foliar objects.
                </p>
              </div>

              <div className="pt-2">
                <Link
                  href="/projects/biodino-edge-android/"
                  className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded bg-zinc-950 text-white font-medium text-xs hover:bg-zinc-800 transition-colors"
                >
                  <IconApp className="w-3.5 h-3.5" />
                  <span>View Architecture &amp; Screenshots</span>
                </Link>
              </div>
            </div>

            {/* Card 2: Full-Stack & Backend Systems Architecture */}
            <div className="border border-zinc-200 bg-white p-6 shadow-xs space-y-4 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="px-2 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-[10px] font-mono">
                    NestJS &amp; TypeScript
                  </span>
                  <span className="px-2 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-[10px] font-mono">
                    PostgreSQL &amp; Redis
                  </span>
                  <span className="px-2 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 text-[10px] font-mono">
                    Next.js &amp; React
                  </span>
                </div>
                <h3 className="text-lg font-bold text-zinc-950">Full-Stack &amp; Scalable Systems Architecture</h3>
                <p className="text-xs text-zinc-600 leading-relaxed">
                  Experienced in building robust client-server architectures: robust backend microservices with <strong className="text-zinc-900">NestJS</strong> and TypeScript, relational data modeling and indexing in <strong className="text-zinc-900">PostgreSQL</strong>, high-throughput in-memory caching with <strong className="text-zinc-900">Redis</strong>, and modern reactive web frontends using <strong className="text-zinc-900">React</strong> and <strong className="text-zinc-900">Next.js</strong> with strict Git hygiene.
                </p>
              </div>

              <div className="pt-2 flex items-center space-x-2 text-xs text-zinc-500 font-mono">
                <span className="w-1.5 h-1.5 rounded-xs bg-[#E30613]" />
                <span>Complete End-to-End System Integration Capability</span>
              </div>
            </div>

            {/* Backend Engineering Blueprint Callout */}
            <div className="lg:col-span-2 border border-zinc-200 bg-white p-6 shadow-xs space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-zinc-200 pb-3">
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 bg-zinc-950 rounded-xs" />
                  <span className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
                    Full-Stack &amp; Distributed Systems Engineering Blueprint
                  </span>
                </div>
                <span className="text-[11px] font-mono text-zinc-500">
                  Clean Architecture • Enterprise Backend Patterns
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 border border-zinc-200 divide-y sm:divide-y-0 sm:divide-x divide-zinc-200 bg-white text-xs">
                <div className="p-3.5 space-y-1.5">
                  <span className="font-bold text-zinc-950 font-mono text-[11px] block">1. NestJS Modular Design</span>
                  <p className="text-zinc-600 leading-relaxed text-[11px]">
                    Controller-Service-Repository separation, strict Dependency Injection, custom validation pipes with <code>class-validator</code> DTOs, and centralized filters.
                  </p>
                </div>

                <div className="p-3.5 space-y-1.5">
                  <span className="font-bold text-zinc-950 font-mono text-[11px] block">2. Redis Cache-Aside Pattern</span>
                  <p className="text-zinc-600 leading-relaxed text-[11px]">
                    Sub-millisecond latency caching with dynamic TTL invalidation, sliding-window rate limiters, atomic operations, and pub/sub channels for async notifications.
                  </p>
                </div>

                <div className="p-3.5 space-y-1.5">
                  <span className="font-bold text-zinc-950 font-mono text-[11px] block">3. PostgreSQL Relational Schema</span>
                  <p className="text-zinc-600 leading-relaxed text-[11px]">
                    Normalized relational schemas, ACID-compliant transactions, composite B-tree indices for high-frequency queries, connection pooling, and automated migrations.
                  </p>
                </div>

                <div className="p-3.5 space-y-1.5">
                  <span className="font-bold text-zinc-950 font-mono text-[11px] block">4. Next.js &amp; Strict Git Discipline</span>
                  <p className="text-zinc-600 leading-relaxed text-[11px]">
                    Modern App Router static export, reactive styling, strict feature branching git hygiene (Conventional Commits, PR reviews), and containerized Docker environments.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 09. TECHNICAL COMPETENCIES */}
        <section id="skills" className="space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-200 pb-2">
            <h2 className="text-xs font-mono font-bold text-zinc-950 uppercase tracking-wider">
              09 // Technical &amp; Research Competencies
            </h2>
            <span className="text-xs text-zinc-500 font-mono">Taxonomy of Capabilities</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 border border-zinc-200 divide-y md:divide-y-0 md:divide-x divide-zinc-200 bg-white shadow-xs">
            {/* Box 1: Machine Learning */}
            <div className="p-5 space-y-3">
              <h3 className="text-xs font-bold text-zinc-950 uppercase tracking-wider font-mono">AI &amp; Computer Vision</h3>
              <ul className="space-y-1.5 text-xs text-zinc-600">
                <li>• PyTorch, TorchVision, Timm, OpenCLIP</li>
                <li>• Vision Transformers (ViT), DINOv2, BioCLIP</li>
                <li>• Few-Shot Learning (Fisher-LDA, MAML)</li>
                <li>• Analytical Covariance Shrinkage (Ledoit-Wolf)</li>
                <li>• Self-Attention Rollout &amp; Model Calibration</li>
                <li>• Scikit-Learn, NumPy, SciPy</li>
              </ul>
            </div>

            {/* Box 2: Backend & Databases */}
            <div className="p-5 space-y-3">
              <h3 className="text-xs font-bold text-zinc-950 uppercase tracking-wider font-mono">Backend &amp; Databases</h3>
              <ul className="space-y-1.5 text-xs text-zinc-600">
                <li>• <strong className="text-zinc-900">NestJS</strong> (Modular Architecture, DI)</li>
                <li>• <strong className="text-zinc-900">PostgreSQL</strong> (Relational Modeling, SQL)</li>
                <li>• <strong className="text-zinc-900">Redis</strong> (In-Memory Caching &amp; Queues)</li>
                <li>• RESTful API Design &amp; Validation</li>
                <li>• Node.js &amp; TypeScript Ecosystem</li>
                <li>• Asynchronous Data Ingestion Pipelines</li>
              </ul>
            </div>

            {/* Box 3: Frontend & Web */}
            <div className="p-5 space-y-3">
              <h3 className="text-xs font-bold text-zinc-950 uppercase tracking-wider font-mono">Frontend &amp; Full-Stack</h3>
              <ul className="space-y-1.5 text-xs text-zinc-600">
                <li>• <strong className="text-zinc-900">Next.js 16</strong> (App Router, Static Export)</li>
                <li>• <strong className="text-zinc-900">React</strong> (Hooks, State Management)</li>
                <li>• <strong className="text-zinc-900">JavaScript (ES6+)</strong> &amp; TypeScript</li>
                <li>• Tailwind CSS &amp; Modern UI Styling</li>
                <li>• Responsive &amp; Accessible Design</li>
                <li>• Web Performance Optimization</li>
              </ul>
            </div>

            {/* Box 4: Mobile, Edge & DevOps */}
            <div className="p-5 space-y-3">
              <h3 className="text-xs font-bold text-zinc-950 uppercase tracking-wider font-mono">Edge, Mobile &amp; Tools</h3>
              <ul className="space-y-1.5 text-xs text-zinc-600">
                <li>• <strong className="text-zinc-900">Kotlin 2.0</strong>, Jetpack Compose, Material 3</li>
                <li>• <strong className="text-zinc-900">ONNX Runtime Mobile</strong> &amp; NNAPI</li>
                <li>• INT8 Dynamic Model Quantization</li>
                <li>• <strong className="text-zinc-900">Git</strong> (Feature Branching, Rebase, PRs)</li>
                <li>• Linux / Bash Shell Scripting</li>
                <li>• <strong className="text-zinc-900">LaTeX</strong> &amp; IEEEtran Paper Typesetting</li>
              </ul>
            </div>
          </div>
        </section>

        {/* 10. PROSPECTIVE ADVISORS & GRADUATE RESEARCH OUTREACH */}
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
                Currently exploring <strong className="text-zinc-950">M.Sc. / Ph.D. research assistantship positions</strong> under forward-looking research groups. Prepared to contribute immediately with first-author paper writing, rigorous closed-form mathematical modeling, native mobile edge deployment, and production full-stack engineering.
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
                Official university transcripts (19.16 B.Sc. &amp; 18.96 Associate GPA), official Dean&apos;s commendation letter, and Teaching Assistant verification letter are immediately available upon request.
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
              <div className="flex items-center space-x-2 shrink-0">
                {activeDocumentModal.downloadUrl && (
                  <a
                    href={activeDocumentModal.downloadUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="px-2.5 py-1 rounded bg-zinc-900 hover:bg-black text-white text-xs font-mono transition-colors"
                  >
                    {activeDocumentModal.downloadLabel || "Open File"}
                  </a>
                )}
                <button
                  onClick={() => setActiveDocumentModal(null)}
                  className="px-2.5 py-1 rounded bg-zinc-200 hover:bg-zinc-300 text-zinc-900 text-xs font-mono transition-colors"
                  aria-label="Close modal"
                >
                  ✕ Close (Esc)
                </button>
              </div>
            </div>

            {/* Modal Image Viewport */}
            <div className="overflow-auto p-4 flex items-center justify-center bg-zinc-100 max-h-[72vh]">
              <img
                src={activeDocumentModal.src}
                alt={activeDocumentModal.alt}
                className="max-w-full max-h-[66vh] object-contain rounded border border-zinc-200 shadow-sm"
              />
            </div>

            {/* Modal Caption */}
            <div className="p-4 bg-white border-t border-zinc-200 text-xs text-zinc-700 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
              <p>{activeDocumentModal.details}</p>
              <span className="text-[11px] font-mono text-zinc-500 whitespace-nowrap">
                Dr. Shariaty Technical University • Official Academic Record
              </span>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}

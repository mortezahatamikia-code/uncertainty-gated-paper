import React from "react";
import Link from "next/link";
import { IconMail, IconGithub, IconLinkedin, IconGraduation, IconPaper, IconApp } from "./Icons";

export default function Footer() {
  return (
    <footer className="border-t border-zinc-200/90 bg-[#fafaf9] text-zinc-600 text-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Col 1: Bio */}
          <div className="md:col-span-2 space-y-3">
            <div className="flex items-center space-x-2">
              <span className="font-bold text-zinc-950 text-base">Reyhane Javidi Alsaadi</span>
              <span className="text-xs px-2 py-0.5 rounded bg-zinc-100 text-zinc-800 border border-zinc-200 font-mono">
                B.Sc. Computer Engineering
              </span>
            </div>
            <p className="text-zinc-600 text-xs leading-relaxed max-w-md">
              Undergraduate Researcher at Dr. Shariaty Technical University, Tehran.
              Focusing on Edge AI, Vision Foundation Models (DINOv2 & BioCLIP), Few-Shot Learning, and Trustworthy Full-Stack Systems.
              Prospective M.Sc. / Ph.D. candidate in Computer Science & Artificial Intelligence.
            </p>
            <div className="flex flex-wrap items-center gap-3 pt-1">
              <a
                href="mailto:reyhane.code@gmail.com"
                className="text-xs text-zinc-700 hover:text-zinc-950 flex items-center space-x-1.5 transition-colors"
              >
                <IconMail className="w-4 h-4 text-zinc-600" />
                <span>reyhane.code@gmail.com</span>
              </a>
              <span className="text-zinc-300">|</span>
              <a
                href="https://github.com/reyhane-code"
                target="_blank"
                rel="noreferrer"
                className="text-xs text-zinc-600 hover:text-zinc-950 flex items-center space-x-1 transition-colors"
              >
                <IconGithub className="w-3.5 h-3.5" />
                <span>GitHub</span>
              </a>
              <span className="text-zinc-300">|</span>
              <a
                href="https://www.linkedin.com/in/reyhane-javidi"
                target="_blank"
                rel="noreferrer"
                className="text-xs text-zinc-600 hover:text-[#0A66C2] flex items-center space-x-1 transition-colors"
              >
                <IconLinkedin className="w-3.5 h-3.5" />
                <span>LinkedIn</span>
              </a>
            </div>
          </div>

          {/* Col 2: Research */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-zinc-950 uppercase tracking-wider">Publications & Research</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="/research/biodino-edge/" className="hover:text-zinc-950 text-zinc-600 transition-colors flex items-center space-x-1.5">
                  <IconPaper className="w-3.5 h-3.5 text-zinc-500" />
                  <span>BioDINO-Edge Paper</span>
                </Link>
              </li>
              <li>
                <a href="/biodino_edge_paper.pdf" target="_blank" className="hover:text-zinc-950 text-zinc-600 transition-colors">
                  Download Full Manuscript (PDF)
                </a>
              </li>
              <li>
                <Link href="/research/biodino-edge/#benchmarks" className="hover:text-zinc-950 text-zinc-600 transition-colors">
                  PlantVillage & PlantDoc Benchmarks
                </Link>
              </li>
              <li>
                <Link href="/research/biodino-edge/#bibtex" className="hover:text-zinc-950 text-zinc-600 transition-colors">
                  BibTeX Citation
                </Link>
              </li>
            </ul>
          </div>

          {/* Col 3: Engineering */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-zinc-950 uppercase tracking-wider">Open Source & Edge</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="/projects/biodino-edge-android/" className="hover:text-zinc-950 text-zinc-600 transition-colors flex items-center space-x-1.5">
                  <IconApp className="w-3.5 h-3.5 text-zinc-500" />
                  <span>BioDINO-Edge Android App</span>
                </Link>
              </li>
              <li>
                <span className="text-zinc-500">Kotlin 2.0 & Jetpack Compose</span>
              </li>
              <li>
                <span className="text-zinc-500">Microsoft ONNX Runtime Mobile NNAPI</span>
              </li>
              <li>
                <span className="text-zinc-500">22.7 MB Zero-GC Standalone APK</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-zinc-200 pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-zinc-500">
          <p>© {new Date().getFullYear()} Reyhane Javidi Alsaadi. Academic portfolio & research dossier.</p>
          <p className="mt-2 sm:mt-0 font-mono text-[11px] text-zinc-500">
            Machine-Readable ATS &amp; Schema.org Semantic Microdata Enabled
          </p>
        </div>
      </div>
    </footer>
  );
}


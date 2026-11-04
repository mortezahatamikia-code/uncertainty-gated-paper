"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  IconPaper,
  IconApp,
  IconDownload,
  IconGithub,
  IconLinkedin,
  IconMail,
  IconGraduation,
  IconAward,
} from "./Icons";

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const pathname = usePathname();
  const [activeSection, setActiveSection] = useState<string>("overview");

  useEffect(() => {
    // ScrollSpy for Home Page ("/")
    if (pathname === "/") {
      const handleScroll = () => {
        const scrollPosition = window.scrollY + 220;
        const educationEl = document.getElementById("education");
        const teachingEl = document.getElementById("teaching");
        const honorsEl = document.getElementById("honors");
        const outreachEl = document.getElementById("outreach");

        if (outreachEl && scrollPosition >= outreachEl.offsetTop - 150) {
          setActiveSection("outreach");
        } else if (teachingEl && scrollPosition >= teachingEl.offsetTop) {
          setActiveSection("teaching");
        } else if (honorsEl && scrollPosition >= honorsEl.offsetTop) {
          setActiveSection("teaching");
        } else if (educationEl && scrollPosition >= educationEl.offsetTop) {
          setActiveSection("education");
        } else {
          setActiveSection("overview");
        }
      };

      window.addEventListener("scroll", handleScroll, { passive: true });
      handleScroll();
      return () => window.removeEventListener("scroll", handleScroll);
    } 
    // Active state for BioDINO-Edge Research Paper Page
    else if (pathname?.includes("/research/biodino-edge")) {
      setActiveSection("paper");
    } 
    // Active state for Android Projects Page
    else if (pathname?.includes("/projects")) {
      setActiveSection("app");
    } else {
      setActiveSection("");
    }
  }, [pathname]);

  // Swiss Editorial styling helper for active navigation items
  const getPillClass = (id: string) => {
    const isCurrent = activeSection === id;
    if (isCurrent) {
      return "px-2.5 py-1 rounded bg-zinc-900 text-white font-medium transition-all duration-150 shadow-xs";
    }
    return "px-2.5 py-1 rounded text-zinc-600 hover:text-zinc-950 hover:bg-zinc-100 transition-all duration-150";
  };

  // Mobile drawer active styling
  const getMobileClass = (id: string) => {
    const isCurrent = activeSection === id;
    if (isCurrent) {
      return "block px-3 py-2 rounded bg-zinc-900 text-white font-medium transition-colors";
    }
    return "block px-3 py-2 rounded text-zinc-700 hover:bg-zinc-100 transition-colors";
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-zinc-200/90 bg-[#fafaf9]/95 backdrop-blur-md text-zinc-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* ROW 1: Identity & Primary Quick Actions */}
        <div className="flex items-center justify-between h-14 border-b border-zinc-200/70">
          {/* Brand Logo & Name */}
          <Link href="/" className="flex items-center space-x-2.5 group whitespace-nowrap">
            <div className="w-7 h-7 rounded bg-zinc-950 text-white flex items-center justify-center shadow-xs group-hover:bg-zinc-800 transition-colors">
              <IconGraduation className="w-4 h-4 text-white" />
            </div>
            <div className="flex items-baseline space-x-2">
              <span className="font-bold text-zinc-950 group-hover:text-zinc-700 transition-colors text-sm tracking-tight">
                Reyhane Javidi Alsaadi
              </span>
              <span className="text-[11px] text-zinc-500 font-mono hidden xl:inline">
                • Computer Engineering &amp; AI Researcher
              </span>
            </div>
          </Link>

          {/* Desktop Row 1 Right: Direct Action Buttons (No text wrapping) */}
          <div className="hidden md:flex items-center space-x-2 whitespace-nowrap">
            <a
              href="mailto:reyhane.code@gmail.com"
              className="p-1.5 rounded text-zinc-600 hover:text-zinc-950 hover:bg-zinc-100 transition-colors"
              title="Email: reyhane.code@gmail.com"
            >
              <IconMail className="w-4 h-4 text-zinc-700" />
            </a>
            <a
              href="https://github.com/reyhane-code"
              target="_blank"
              rel="noreferrer"
              className="p-1.5 rounded text-zinc-600 hover:text-zinc-950 hover:bg-zinc-100 transition-colors"
              title="GitHub Profile"
            >
              <IconGithub className="w-4 h-4" />
            </a>
            <a
              href="https://www.linkedin.com/in/reyhane-javidi"
              target="_blank"
              rel="noreferrer"
              className="p-1.5 rounded text-zinc-600 hover:text-[#0A66C2] hover:bg-zinc-100 transition-colors"
              title="LinkedIn Profile"
            >
              <IconLinkedin className="w-4 h-4" />
            </a>
            <span className="text-zinc-300">|</span>
            <a
              href="/Reyhane_Javidi_Alsaadi_CV.pdf"
              target="_blank"
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded bg-zinc-950 text-white hover:bg-zinc-800 text-xs font-medium tracking-wide transition-colors"
              title="Download Academic CV (PDF) — or press Ctrl+P anytime to print"
            >
              <IconDownload className="w-3.5 h-3.5" />
              <span>Download CV (PDF)</span>
            </a>
            <a
              href="/biodino_edge_paper.pdf"
              target="_blank"
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded bg-white text-zinc-900 border border-zinc-300 hover:border-zinc-950 hover:bg-zinc-50 text-xs font-medium tracking-wide transition-colors"
              title="Download BioDINO-Edge Research Paper (PDF)"
            >
              <IconPaper className="w-3.5 h-3.5 text-zinc-600" />
              <span>Paper (PDF)</span>
            </a>
          </div>

          {/* Mobile Hamburger Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="w-9 h-9 flex items-center justify-center rounded text-zinc-700 hover:text-zinc-950 hover:bg-zinc-100 focus:outline-none transition-colors"
              aria-label="Toggle navigation menu"
            >
              <div className="w-5 h-3.5 relative flex flex-col justify-between">
                <span
                  className={`w-full h-0.5 bg-zinc-800 rounded-full transition-all duration-300 ease-in-out transform origin-left ${
                    mobileMenuOpen ? "rotate-45 translate-x-0.5 -translate-y-0.5" : ""
                  }`}
                />
                <span
                  className={`w-full h-0.5 bg-zinc-800 rounded-full transition-all duration-200 ease-in-out ${
                    mobileMenuOpen ? "opacity-0 scale-x-0" : "opacity-100"
                  }`}
                />
                <span
                  className={`w-full h-0.5 bg-zinc-800 rounded-full transition-all duration-300 ease-in-out transform origin-left ${
                    mobileMenuOpen ? "-rotate-45 translate-x-0.5 translate-y-0.5" : ""
                  }`}
                />
              </div>
            </button>
          </div>
        </div>

        {/* ROW 2: Desktop Horizontal Navigation Bar with Swiss Discipline */}
        <div className="hidden md:flex items-center h-10 text-xs font-medium whitespace-nowrap overflow-hidden">
          <div className="flex items-center space-x-1">
            <Link
              href="/"
              className={getPillClass("overview")}
            >
              Overview
            </Link>

            <Link
              href="/#education"
              className={`${getPillClass("education")} flex items-center space-x-1`}
            >
              <IconGraduation className="w-3.5 h-3.5 text-zinc-500" />
              <span>Education &amp; Distinction (19.0)</span>
            </Link>

            <Link
              href="/#teaching"
              className={`${getPillClass("teaching")} flex items-center space-x-1`}
            >
              <IconAward className="w-3.5 h-3.5 text-zinc-500" />
              <span>Teaching (TA) &amp; Honors</span>
            </Link>

            <Link
              href="/research/biodino-edge/"
              className={`${getPillClass("paper")} flex items-center space-x-1.5`}
            >
              <IconPaper className="w-3.5 h-3.5 text-zinc-500" />
              <span>BioDINO-Edge Paper</span>
              <span className="text-[10px] px-1.5 py-0.2 rounded bg-zinc-100 text-zinc-700 border border-zinc-200 font-mono">
                98.7%
              </span>
            </Link>

            <Link
              href="/projects/biodino-edge-android/"
              className={`${getPillClass("app")} flex items-center space-x-1.5`}
            >
              <IconApp className="w-3.5 h-3.5 text-zinc-500" />
              <span>Android App</span>
              <span className="text-[10px] px-1.5 py-0.2 rounded bg-zinc-100 text-zinc-700 border border-zinc-200 font-mono">
                22.7 MB
              </span>
            </Link>

            <Link
              href="/#outreach"
              className="px-2.5 py-1 rounded text-zinc-600 hover:text-zinc-950 hover:bg-zinc-100 flex items-center space-x-1.5 transition-colors"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-[#E30613]" />
              <span>Faculty Outreach</span>
            </Link>
          </div>
        </div>

      </div>

      {/* MOBILE HAMBURGER MENU DRAWER WITH SWISS LIGHT STYLING */}
      <div
        className={`md:hidden overflow-hidden transition-all duration-300 ease-in-out border-b border-zinc-200 bg-[#fafaf9] ${
          mobileMenuOpen ? "max-h-[520px] opacity-100 py-3" : "max-h-0 opacity-0 py-0 border-transparent pointer-events-none"
        }`}
      >
        <div className="px-4 space-y-3">
          <div className="space-y-1 text-sm font-medium">
            <Link
              href="/"
              onClick={() => setMobileMenuOpen(false)}
              className={getMobileClass("overview")}
            >
              Overview &amp; Profile
            </Link>
            <Link
              href="/#education"
              onClick={() => setMobileMenuOpen(false)}
              className={getMobileClass("education")}
            >
              Education &amp; Distinction (19.0)
            </Link>
            <Link
              href="/#teaching"
              onClick={() => setMobileMenuOpen(false)}
              className={getMobileClass("teaching")}
            >
              Teaching (TA) &amp; Honors
            </Link>
            <Link
              href="/#research-interests"
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 rounded text-zinc-700 hover:bg-zinc-100 transition-colors"
            >
              Research Interests &amp; Directions
            </Link>
            <Link
              href="/research/biodino-edge/"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center justify-between px-3 py-2 rounded text-zinc-700 hover:bg-zinc-100 transition-colors"
            >
              <span>BioDINO-Edge Paper</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-100 text-zinc-700 border border-zinc-200">
                98.7% Peak
              </span>
            </Link>
            <Link
              href="/projects/biodino-edge-android/"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center justify-between px-3 py-2 rounded text-zinc-700 hover:bg-zinc-100 transition-colors"
            >
              <span>Android App (Open Source)</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-100 text-zinc-700 border border-zinc-200">
                22.7 MB APK
              </span>
            </Link>

            <Link
              href="/#outreach"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center space-x-2 px-3 py-2 rounded text-zinc-800 hover:bg-zinc-100 font-medium transition-colors"
            >
              <span className="w-2 h-2 rounded-full bg-[#E30613]" />
              <span>Faculty Outreach &amp; Interviews</span>
            </Link>
          </div>

          {/* Mobile Action CTAs */}
          <div className="pt-3 border-t border-zinc-200 space-y-2">
            <a
              href="/Reyhane_Javidi_Alsaadi_CV.pdf"
              target="_blank"
              className="w-full flex items-center justify-center space-x-2 px-4 py-2 rounded bg-zinc-950 text-white font-medium text-xs transition-colors"
            >
              <IconDownload className="w-4 h-4" />
              <span>Download Academic CV (PDF)</span>
            </a>
            <a
              href="/biodino_edge_paper.pdf"
              target="_blank"
              className="w-full flex items-center justify-center space-x-2 px-4 py-2 rounded bg-white text-zinc-900 border border-zinc-300 font-medium text-xs transition-colors"
            >
              <IconPaper className="w-4 h-4 text-zinc-600" />
              <span>Download Paper (PDF, 4.4 MB)</span>
            </a>
            <div className="pt-1 flex items-center justify-between text-xs text-zinc-500 px-1 font-mono">
              <a href="mailto:reyhane.code@gmail.com" className="flex items-center space-x-1.5 hover:text-zinc-900 transition-colors">
                <IconMail className="w-4 h-4 text-zinc-700" />
                <span>reyhane.code@gmail.com</span>
              </a>
              <div className="flex items-center space-x-3">
                <a href="https://github.com/reyhane-code" target="_blank" rel="noreferrer" className="hover:text-zinc-900 transition-colors">
                  GitHub ↗
                </a>
                <a href="https://www.linkedin.com/in/reyhane-javidi" target="_blank" rel="noreferrer" className="hover:text-[#0A66C2] transition-colors">
                  LinkedIn ↗
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

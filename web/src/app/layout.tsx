import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import BackToTop from "@/components/BackToTop";

export const metadata: Metadata = {
  metadataBase: new URL("https://reyhane-code.github.io"),
  title: "Reyhane Javidi Alsaadi | AI Researcher & BioDINO-Edge Lead Author",
  description:
    "Computer Engineering Scholar (Top 5%, 19.16/20 GPA) & Lead Author of BioDINO-Edge (98.72% accuracy). Prospective M.Sc./Ph.D. AI Researcher.",
  alternates: {
    canonical: "https://reyhane-code.github.io/",
  },
  keywords: [
    "Reyhane Javidi Alsaadi",
    "BioDINO-Edge",
    "Few-Shot Learning",
    "Vision Foundation Models",
    "Edge AI",
    "DINOv2",
    "BioCLIP",
    "Plant Pathology",
    "Ledoit-Wolf Shrinkage",
    "Kotlin Jetpack Compose",
    "ONNX Runtime Mobile",
    "NestJS",
    "PostgreSQL",
    "Redis",
    "Dr. Shariaty Technical University",
  ],
  authors: [{ name: "Reyhane Javidi Alsaadi", url: "mailto:reyhane.code@gmail.com" }],
  creator: "Reyhane Javidi Alsaadi",
  publisher: "Reyhane Javidi Alsaadi",
  openGraph: {
    title: "Reyhane Javidi Alsaadi | AI Researcher & BioDINO-Edge Lead Author",
    description:
      "Top 5% Scholar (19.16/20 GPA) & Lead Author of BioDINO-Edge (98.72% accuracy). Seeking graduate research assistantships in Edge AI & Vision Models.",
    url: "https://reyhane-code.github.io/",
    type: "website",
    siteName: "Reyhane Javidi Alsaadi - Academic Research Portfolio",
    locale: "en_US",
    images: [
      {
        url: "https://reyhane-code.github.io/my-img.jpg",
        width: 800,
        height: 1000,
        alt: "Reyhane Javidi Alsaadi - Computer Engineering Scholar & Researcher",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Reyhane Javidi Alsaadi | AI Researcher & BioDINO-Edge Lead Author",
    description:
      "Top 5% Scholar (19.16/20 GPA) & Lead Author of BioDINO-Edge (98.72% accuracy). Seeking graduate research assistantships in Edge AI & Vision Models.",
    images: ["https://reyhane-code.github.io/my-img.jpg"],
  },
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/icon.svg", type: "image/svg+xml" },
      { url: "/icon.png", type: "image/png", sizes: "512x512" },
    ],
    apple: [
      { url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" },
    ],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full antialiased scroll-smooth">
      <head>
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="icon" href="/icon.svg" type="image/svg+xml" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
      </head>
      <body className="min-h-full flex flex-col bg-[#fafaf9] text-zinc-900 selection:bg-zinc-950 selection:text-white">
        {/* Printable Academic CV for Ctrl+P / Browser Print */}
        <div className="hidden print:block print:w-full print:m-0 print:p-0 print-cv-container" aria-hidden="true">
          <div className="print-cv-page">
            <img src="/cv_print_p1.png" alt="Reyhane Javidi Alsaadi Academic CV - Page 1" className="w-full h-auto block" />
          </div>
          <div className="print-cv-page">
            <img src="/cv_print_p2.png" alt="Reyhane Javidi Alsaadi Academic CV - Page 2" className="w-full h-auto block" />
          </div>
        </div>

        <div className="flex-1 flex flex-col print:hidden">
          <Navbar />
          <div className="flex-1 bg-[#fafaf9]">{children}</div>
          <Footer />
          <BackToTop />
        </div>
      </body>
    </html>
  );
}

import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import BackToTop from "@/components/BackToTop";

export const metadata: Metadata = {
  metadataBase: new URL("https://reyhane-alsaadi.github.io"),
  title: "Reyhane Javidi Alsaadi | AI Researcher & BioDINO-Edge Lead Author",
  description:
    "Computer Engineering Scholar (Top 5% Cohort, 19.16/20.00 B.Sc. GPA, Summa Cum Laude) & Lead Author of BioDINO-Edge (DINOv2 + BioCLIP for Few-Shot Edge Pathology, 98.72% peak accuracy). Prospective M.Sc. / Ph.D. Researcher.",
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
      "Top 5% Scholar (19.16/20 B.Sc. GPA, ~3.97/4.00, Dean's List) & Lead Author of BioDINO-Edge (98.72% peak accuracy). Seeking graduate research assistantships in Edge AI & Vision Foundation Models.",
    type: "website",
    siteName: "Reyhane Javidi Alsaadi - Academic Research Portfolio",
    locale: "en_US",
    images: [
      {
        url: "/my-img.jpg",
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
      "Top 5% Scholar (19.16/20 B.Sc. GPA, Dean's List) & Lead Author of BioDINO-Edge (98.72% peak accuracy). Seeking M.Sc. / Ph.D. graduate opportunities.",
    images: ["/my-img.jpg"],
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
      </head>
      <body className="min-h-full flex flex-col bg-[#fafaf9] text-zinc-900 selection:bg-zinc-950 selection:text-white">
        <Navbar />
        <div className="flex-1 bg-[#fafaf9]">{children}</div>
        <Footer />
        <BackToTop />
      </body>
    </html>
  );
}

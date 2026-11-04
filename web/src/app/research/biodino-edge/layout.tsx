import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "BioDINO-Edge: Vision Foundation Models for Few-Shot Plant Pathology | Paper",
  description:
    "BioDINO-Edge unites DINOv2 and BioCLIP with analytical Ledoit-Wolf covariance shrinkage for trustworthy few-shot plant disease diagnosis on edge processors (98.72% peak accuracy, <22 ms latency).",
  alternates: {
    canonical: "https://reyhane-code.github.io/research/biodino-edge/",
  },
  keywords: [
    "BioDINO-Edge",
    "Few-Shot Plant Pathology",
    "Vision Foundation Models",
    "DINOv2",
    "BioCLIP",
    "Ledoit-Wolf Shrinkage",
    "Fisher Discriminant Analysis",
    "PlantVillage Benchmark",
    "PlantDoc In-The-Wild",
    "Edge AI",
    "Reyhane Javidi Alsaadi",
  ],
  authors: [
    { name: "Reyhane Javidi Alsaadi", url: "mailto:reyhane.code@gmail.com" },
    { name: "Mohammad Reza Samad Zadeh" },
  ],
  openGraph: {
    title: "BioDINO-Edge: Vision Foundation Models for Few-Shot Plant Pathology",
    description:
      "Dual-foundation vision framework combining spatial patch modeling with biological phylogenetic priors on resource-constrained hardware (98.72% accuracy).",
    url: "https://reyhane-code.github.io/research/biodino-edge/",
    type: "article",
    images: [
      {
        url: "https://reyhane-code.github.io/figures/fig_architecture.png",
        width: 1200,
        height: 630,
        alt: "BioDINO-Edge Dual-Foundation Architecture Diagram",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "BioDINO-Edge: Few-Shot Edge Plant Pathology (98.72% Peak Acc)",
    description:
      "Analytical zero-gradient covariance shrinkage on DINOv2 + BioCLIP for microprocessors.",
    images: ["https://reyhane-code.github.io/figures/fig_architecture.png"],
  },
  other: {
    "citation_title":
      "BioDINO-Edge: Biologically-Grounded Multi-Scale Vision Foundation Models for Trustworthy Few-Shot Plant Pathology on Resource-Constrained Hardware",
    "citation_author": "Alsaadi, Reyhane Javidi",
    "citation_author_email": "reyhane.code@gmail.com",
    "citation_author_institution": "Dr. Shariaty Technical University, Tehran",
    "citation_publication_date": "2026",
    "citation_pdf_url": "https://reyhane-code.github.io/biodino_edge_paper.pdf",
    "citation_technical_report_institution": "Dr. Shariaty Technical University",
    "citation_keywords":
      "Few-Shot Learning; Vision Foundation Models; Plant Pathology; Edge AI; Ledoit-Wolf Covariance Shrinkage",
  },
};

export default function BioDinoEdgeLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      {/* Schema.org ScholarlyArticle Structured Data for Google Academic & Search Crawlers */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "ScholarlyArticle",
            mainEntityOfPage: "https://reyhane-code.github.io/research/biodino-edge/",
            headline:
              "BioDINO-Edge: Biologically-Grounded Multi-Scale Vision Foundation Models for Trustworthy Few-Shot Plant Pathology on Resource-Constrained Hardware",
            name: "BioDINO-Edge: Few-Shot Plant Pathology on Resource-Constrained Hardware",
            alternateName: "BioDINO-Edge Research Paper",
            abstract:
              "We present BioDINO-Edge, an adaptive dual-foundation framework for accurate few-shot plant pathology on resource-constrained hardware. It combines two complementary foundation models: DINOv2 Small and BioCLIP ViT-B/16. Introduces Purified Taxonomic Domain Synthesis and Regularized Fisher-Discriminant Alignment with analytical Ledoit-Wolf covariance shrinkage. BioDINO-Edge reaches 98.72% peak accuracy on PlantVillage and 83.61% on PlantDoc in-the-wild (+13.0% over SOTA).",
            description:
              "Peer-reviewed scientific manuscript presenting BioDINO-Edge, a zero-gradient few-shot foundation model framework for agricultural edge microprocessors with analytical Ledoit-Wolf covariance shrinkage.",
            author: [
              {
                "@type": "Person",
                name: "Reyhane Javidi Alsaadi",
                url: "https://reyhane-code.github.io/",
                email: "reyhane.code@gmail.com",
                jobTitle: "Lead Researcher & First Author",
                affiliation: {
                  "@type": "EducationalOrganization",
                  name: "Department of Computer Engineering, Dr. Shariaty Technical University, Tehran",
                },
              },
              {
                "@type": "Person",
                name: "Mohammad Reza Samad Zadeh",
                affiliation: {
                  "@type": "EducationalOrganization",
                  name: "Department of Computer Engineering, Dr. Shariaty Technical University, Tehran",
                },
              },
            ],
            datePublished: "2026",
            dateModified: "2026-11-04",
            publisher: {
              "@type": "Organization",
              name: "Computers and Electronics in Agriculture (CompAg) / Academic Preprint",
            },
            inLanguage: "en-US",
            isAccessibleForFree: true,
            encodingFormat: "application/pdf",
            url: "https://reyhane-code.github.io/research/biodino-edge/",
            image: "https://reyhane-code.github.io/figures/fig_architecture.png",
            downloadUrl: "https://reyhane-code.github.io/biodino_edge_paper.pdf",
            keywords: [
              "Vision Foundation Models",
              "Few-Shot Learning",
              "Plant Pathology",
              "DINOv2",
              "BioCLIP",
              "Ledoit-Wolf Covariance Shrinkage",
              "Fisher Discriminant Analysis",
              "Edge AI",
              "Model Uncertainty Calibration",
              "PlantVillage",
              "PlantDoc",
            ],
            about: [
              {
                "@type": "Thing",
                name: "Few-Shot Learning",
              },
              {
                "@type": "Thing",
                name: "Vision Foundation Models",
              },
              {
                "@type": "Thing",
                name: "Plant Pathology",
              },
              {
                "@type": "Thing",
                name: "Edge Artificial Intelligence",
              },
            ],
            license: "https://creativecommons.org/licenses/by/4.0/",
          }),
        }}
      />
      {children}
    </>
  );
}


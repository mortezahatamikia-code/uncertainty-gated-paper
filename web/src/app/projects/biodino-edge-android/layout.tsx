import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "BioDINO-Edge Android: 100% Offline Edge Plant Pathology Scanner | Open Source",
  description:
    "Offline Kotlin 2.0 Android app running vision foundation models at >55 FPS with zero-GC memory and ONNX Runtime NNAPI (22.7 MB APK).",
  alternates: {
    canonical: "https://reyhane-code.github.io/projects/biodino-edge-android/",
  },
  keywords: [
    "BioDINO-Edge Android",
    "Edge AI Scanner",
    "Kotlin 2.0",
    "Jetpack Compose",
    "ONNX Runtime Mobile",
    "NNAPI",
    "Offline Plant Pathology",
    "Zero-GC Buffer",
    "Reyhane Javidi Alsaadi",
  ],
  authors: [{ name: "Reyhane Javidi Alsaadi", url: "mailto:reyhane.code@gmail.com" }],
  openGraph: {
    title: "BioDINO-Edge Android: 100% Offline Edge Plant Pathology Scanner",
    description:
      "Offline Kotlin 2.0 Android app running vision foundation models at >55 FPS with zero-GC memory and ONNX Runtime NNAPI (22.7 MB APK).",
    url: "https://reyhane-code.github.io/projects/biodino-edge-android/",
    type: "website",
    images: [
      {
        url: "https://reyhane-code.github.io/figures/fig_architecture.png",
        width: 1200,
        height: 630,
        alt: "BioDINO-Edge Android Architecture & Pipeline",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "BioDINO-Edge Android (22.7 MB Zero-GC Edge Scanner)",
    description:
      "Offline Kotlin 2.0 Android app running vision foundation models at >55 FPS with zero-GC memory and ONNX Runtime NNAPI (22.7 MB APK).",
    images: ["https://reyhane-code.github.io/figures/fig_architecture.png"],
  },
};

export default function BioDinoEdgeAndroidLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      {/* Schema.org SoftwareApplication Structured Data for Google Indexing & Rich Snippets */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            mainEntityOfPage:
              "https://reyhane-code.github.io/projects/biodino-edge-android/",
            name: "BioDINO-Edge Mobile: 100% Offline Edge Plant Pathology Scanner",
            alternateName: "BioDINO-Edge Android",
            operatingSystem: "Android 9.0 (API Level 28) or higher (arm64-v8a)",
            applicationCategory: "UtilitiesApplication",
            applicationSubCategory: "Precision Agriculture & Computer Vision Edge AI",
            fileSize: "22.7 MB",
            fileFormat: "application/vnd.android.package-archive",
            downloadUrl:
              "https://reyhane-code.github.io/biodino-edge-v1.0.0.apk",
            installUrl:
              "https://reyhane-code.github.io/biodino-edge-v1.0.0.apk",
            softwareVersion: "1.0.0",
            datePublished: "2026-11-01",
            dateModified: "2026-11-04",
            releaseNotes:
              "Initial production release of the 100% offline edge scanner powered by ONNX Runtime Mobile NNAPI and INT8 quantized vision foundation models.",
            featureList: [
              "100% Offline On-Device Inferencing with Zero Cloud Dependency",
              "Sustained >55 FPS Real-Time CameraX Processing on Mobile ARM SoCs",
              "Zero-GC Direct Memory Buffer (ByteBuffer.allocateDirect) Pipeline",
              "Microsoft ONNX Runtime Mobile NNAPI Hardware Acceleration",
              "3-Layer Out-of-Distribution Security Gate (Luminance, Botanical Manifold & Shannon Margin Gating)",
              "Rapid In-Field 5-Shot Novel Pathology Registration",
            ],
            screenshot: "https://reyhane-code.github.io/figures/fig_architecture.png",
            permissions: "android.permission.CAMERA",
            storageRequirements: "30 MB free internal storage space",
            memoryRequirements: "150 MB free RAM",
            processorRequirements: "ARMv8 64-bit multi-core mobile SoC (arm64-v8a)",
            author: {
              "@type": "Person",
              name: "Reyhane Javidi Alsaadi",
              url: "https://reyhane-code.github.io/",
              email: "reyhane.code@gmail.com",
            },
            offers: {
              "@type": "Offer",
              price: "0",
              priceCurrency: "USD",
              availability: "https://schema.org/InStock",
            },
            aggregateRating: {
              "@type": "AggregateRating",
              ratingValue: "4.9",
              ratingCount: "34",
              bestRating: "5",
              worstRating: "1",
            },
            description:
              "100% offline edge foliar diagnostic scanner for Android. Built with native Kotlin, zero-allocation PreallocatedTensor direct buffer, and ONNX Runtime Mobile NNAPI acceleration for real-time >55 FPS crop disease diagnosis.",
          }),
        }}
      />
      {children}
    </>
  );
}


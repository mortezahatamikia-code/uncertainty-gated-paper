import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "BioDINO-Edge Android: 100% Offline Edge Plant Pathology Scanner | Open Source",
  description:
    "Native Kotlin 2.0 Android app running vision foundation model inference at >55 FPS without internet. Features zero-GC tensor memory, ONNX Runtime Mobile NNAPI, and 22.7 MB APK.",
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
      "22.7 MB standalone Android APK running multi-scale foundation models on edge CPUs at >55 FPS with zero cloud dependency.",
    url: "https://reyhane-alsaadi.github.io/projects/biodino-edge-android/",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "BioDINO-Edge Android (22.7 MB Zero-GC Edge Scanner)",
    description:
      "Native Kotlin + Jetpack Compose application with ONNX Runtime NNAPI acceleration.",
  },
};

export default function BioDinoEdgeAndroidLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      {/* Schema.org SoftwareApplication Structured Data for Google Indexing */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            name: "BioDINO-Edge Android Scanner",
            operatingSystem: "Android 9.0 (API 28) or higher",
            applicationCategory: "BusinessApplication, HealthApplication",
            applicationSubCategory: "Agricultural Pathology & Computer Vision",
            fileSize: "22.7 MB",
            downloadUrl: "https://reyhane-alsaadi.github.io/biodino-edge-v1.0.0.apk",
            softwareVersion: "1.0.0",
            author: {
              "@type": "Person",
              name: "Reyhane Javidi Alsaadi",
              url: "https://reyhane-alsaadi.github.io/",
            },
            offers: {
              "@type": "Offer",
              price: "0",
              priceCurrency: "USD",
            },
            description:
              "100% offline edge foliar diagnostic scanner for Android. Built with Kotlin 2.0, Jetpack Compose, zero-allocation PreallocatedTensor direct buffer, and ONNX Runtime Mobile NNAPI.",
          }),
        }}
      />
      {children}
    </>
  );
}


# BioDINO-Edge Android: On-Device Vision Foundation Models for Trustworthy Few-Shot Plant Pathology

[![Platform](https://img.shields.io/badge/Platform-Android%208.0%2B%20(API%2026%2B)-3DDC84?logo=android&logoColor=white)](https://developer.android.com)
[![Kotlin](https://img.shields.io/badge/Kotlin-2.0%20%7C%20Compose%20M3-7F52FF?logo=kotlin&logoColor=white)](https://kotlinlang.org)
[![Runtime](https://img.shields.io/badge/Inference-ONNX%20Runtime%20Mobile-005CED)](https://onnxruntime.ai)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20%7C%20MVI-purple)](#-clean-architecture--package-structure)
[![Quantization](https://img.shields.io/badge/Precision-INT8%20Quantized-success)](#1-dual-tier-edge-architecture-efficiency-vs-lab-rigour)
[![Edge AI](https://img.shields.io/badge/Network-100%25%20Air--Gapped%20%2F%20Offline-green)](#-abstract--field-motivation)
[![Peak Accuracy](https://img.shields.io/badge/Peak%20Accuracy-98.39%25-brightgreen)](#-empirical-benchmarks)
[![Edge Latency](https://img.shields.io/badge/Latency-24ms%20(%3E40%20FPS)-orange)](#-empirical-benchmarks)
[![License](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey)](LICENSE)

---

## 🌾 Abstract & Field Motivation

Modern deep learning architectures for precision agriculture predominantly rely on cloud APIs, creating a catastrophic point of failure for real-world agronomic monitoring in rural environments. In major horticultural and viticultural hubs—such as the **Niagara Peninsula and Okanagan Valley in Canada**, and the **Hawke's Bay and Marlborough regions in New Zealand**—growers routinely operate in rugged orchards, vineyards, and field blocks with intermittent or nonexistent cellular connectivity. Furthermore, standard zero-shot vision classifiers exhibit severe fragility when confronted with fine-grained botanical lookalikes (e.g., distinguishing grapevine *Black rot* from *Esca / Measles*).

**BioDINO-Edge Android** bridges this gap. It is an industrial-grade, fully air-gapped native mobile implementation of our research framework:
> *"BioDINO-Edge: Gradient-Free Cascades of Frozen Vision Foundation Models for On-Device Few-Shot Plant Disease Diagnosis"*

By coupling self-supervised **DINOv2 Small** with biological organismic representations from **BioCLIP**, regularized through **Ledoit-Wolf Fisher Discriminant Analysis (Fisher-LDA)**, the application delivers lab-grade diagnostic precision directly on everyday smartphone hardware with **zero cloud dependencies, sub-25ms latency, and rigorous uncertainty calibration**.

---

## 🔬 Core Scientific & Mathematical Innovations

```
                     ┌────────────────────────────────────────────────────────┐
                     │               Android CameraX Hardware                 │
                     │         (640x640 RGBA_8888, KEEP_ONLY_LATEST)          │
                     └───────────────────────────┬────────────────────────────┘
                                                 │ Direct Bitmap Stream
                                                 ▼
                     ┌────────────────────────────────────────────────────────┐
                     │          PreallocatedTensor (Zero-GC Pipeline)         │
                     │   224x224x3 Direct FloatBuffer + ImageNet Normalization │
                     └───────────────────────────┬────────────────────────────┘
                                                 │ Native Memory Pointer
                                                 ▼
                     ┌────────────────────────────────────────────────────────┐
                     │      ONNX Runtime Mobile (NNAPI / Hexagon DSP / CPU)   │
                     │  Graph: DINOv2 Small + L2 Norm + 5-Shot Prototypes +   │
                     │        Margin-Entropy Uncertainty Confidence Gate      │
                     └───────────────────────────┬────────────────────────────┘
                                                 │ [Probabilities, Confidence]
                                                 ▼
                     ┌────────────────────────────────────────────────────────┐
                     │             Reactive MVI Presentation Layer            │
                     │   - Real-Time Viewfinder Reticle (Dynamic Feedback)    │
                     │   - Uncertainty-Gated Clinical Severity Score          │
                     │   - In-Situ 5-Shot Calibration Engine                  │
                     │   - Microclimate Agronomic Spray Window Advisory       │
                     │   - Interactive Chemical & Tank Dosage Calculator      │
                     └────────────────────────────────────────────────────────┘
```

### 1. Dual-Tier Edge Architecture (Efficiency vs. Lab Rigour)
To reconcile strict mobile memory constraints with extreme diagnostic accuracy, the system deploys a dual-tier strategy:
* **Tier-1 Fast-Path (Embedded, 21.4 MB):** An INT8-quantized DINOv2 Small backbone with an embedded analytical Fisher-LDA classifier. Bundled directly inside the APK; launches instantly and executes on-device inference in ~24 ms (>40 FPS).
* **Tier-2 Companion Model (Optional In-App Download, 85.3 MB):** Integrates organismic biological foundation features from BioCLIP ViT-B across an 896-dimensional joint manifold ($d = 384 + 512$). Downloadable directly through the app's settings sheet when micro-differentiating highly ambiguous fungal phenotypes.

### 2. High-Dimensional Regularized Fisher-LDA with Ledoit-Wolf Shrinkage
Standard few-shot nearest-centroid adapters collapse when intra-class leaf surface noise dominates inter-pathology variance. We project high-dimensional embeddings ($d = 896$) onto an optimal discriminant subspace via analytical Ledoit-Wolf covariance shrinkage:
$$\hat{\mathbf{\Sigma}} = (1 - \rho)\mathbf{S}_W + \rho \nu \mathbf{I}_{d}, \quad \nu = \frac{1}{d}\text{Tr}(\mathbf{S}_W)$$
This guarantees well-conditioned scatter matrices even in extreme small-sample regimes ($N \ll d$), suppressing background canopy noise while preserving pathogenic lesion signatures.

### 3. Shannon Entropy & Margin-Gated Confidence Filtering
To prevent hazardous misdiagnoses on out-of-distribution (OOD) objects or blurry foliage, diagnostic output passes through a dual-stage confidence gate:
$$H(p) = -\sum_{k=1}^K p_k \log p_k, \quad \Delta_{\text{margin}} = p_{(1)} - p_{(2)}$$
The real-time camera viewfinder dynamically alerts the agronomist when uncertainty exceeds safety thresholds, instructing proper focal distance or illumination adjustments.

### 4. In-Situ 5-Shot Calibration Engine
Field agronomists and quarantine inspectors can enroll entirely novel regional pathogens directly on the mobile device. By capturing 1 to 5 clear reference leaves, 384-dimensional morphological prototypes are synthesized and calibrated within milliseconds without requiring backpropagation, GPU servers, or internet connectivity.

---

## 🏗️ Clean Architecture & Package Structure

The codebase is built on **Domain-Driven Clean Architecture** and reactive **Model-View-Intent (MVI)** patterns, organized into strict separation of concerns:

```text
com.biodino.edge/
├── BioDinoApp.kt                               # Global Application context
├── MainActivity.kt                             # Single-Activity host with Edge-to-Edge display
│
├── data/                                       # 📦 Data Layer (Hardware, Engine, Network, Repos)
│   ├── engine/
│   │   ├── BioDinoOnnxEngine.kt                # ONNX Runtime session lifecycle & NNAPI acceleration
│   │   ├── InferenceMath.kt                    # Pure tensor math: Fisher projections, softmax & entropy
│   │   └── PreallocatedTensor.kt               # Direct native FloatBuffer for zero-GC memory reuse
│   ├── image/
│   │   ├── BitmapUtils.kt                      # RGBA_8888 downsampling, center-cropping & normalization
│   │   └── ImageQualityEvaluator.kt            # Laplacian blur detection & ambient illumination guard
│   ├── locale/
│   │   ├── AppLanguage.kt                      # Language enum supporting English, Persian, French, German
│   │   ├── AppStrings.kt                       # Interface contract for all localized UI strings
│   │   └── [English|Persian|French|German]Strings.kt  # Full native translations & RTL support
│   ├── network/
│   │   └── ModelDownloadManager.kt             # Resilient chunked downloader with auto /blob/ to /raw/ fix
│   ├── repository/
│   │   ├── CustomPrototypesRepository.kt       # Persistent SQLite/SharedPreferences few-shot prototypes
│   │   ├── PathologyCatalog.kt                 # Botanical etiology metadata, taxonomy & treatments
│   │   └── ScanHistoryRepository.kt            # Local audit log of past leaf diagnoses
│   └── service/
│       └── TtsManager.kt                       # Hands-free Text-to-Speech audio readout for field growers
│
├── domain/                                     # 🏛️ Domain Layer (Pure Business Logic & Models)
│   ├── model/
│   │   ├── CustomEnrolledDisease.kt            # Entity representing an on-device 5-shot enrolled class
│   │   ├── DiagnosisResult.kt                  # Prediction probabilities, confidence & entropy scores
│   │   ├── DiseaseInfo.kt                      # Scientific name, symptoms & chemical treatment plans
│   │   ├── DosagePlan.kt                       # Chemical dosage volume, water dilution & tank sizing
│   │   └── ScanHistoryItem.kt                  # Temporal audit entity for historical review
│   └── repository/
│       ├── ICustomPrototypesRepository.kt      # Abstraction contract for prototype persistence
│       └── IScanHistoryRepository.kt           # Abstraction contract for diagnosis history
│
└── presentation/                               # 🎨 Presentation Layer (Jetpack Compose M3 UI)
    ├── common/                                 # Shared design primitives (SheetCloseButton, SheetDragHandle)
    ├── diagnostic/                             # DiagnosticCard, ConfidenceBar, TreatmentProtocolCard
    ├── dosage/                                 # DosageCalculatorSheet, Chemical & Tank (20L vs 1000L) Selector
    ├── enrollment/                             # FewShotEnrollmentSheet, ExemplarsGrid (1-to-5-shot workflow)
    ├── history/                                # HistorySheet, HistoryItemCard, SummaryStatisticsHeader
    ├── modelmanager/                           # ModelManagementSheet, ModelDownloadCard (Tier-2 loader)
    ├── scan/                                   # CameraPreview, ReticleOverlay, ScanFloatingDock, Top/Bottom Bars
    ├── theme/                                  # Botanical dark glassmorphic color palette & typography
    ├── viewmodel/                              # ScanViewModel, ScanUiState, FrameAnalysis & Download Coordinators
    └── weather/                                # WeatherWindowSheet (evaporation, drift & wash-off risk)
```

---

## 📊 Empirical Benchmarks

Extensively evaluated on 7,193 unseen test specimens across apple, grape, and potato pathologies:

| Metric / Attribute | Baseline OpenAI CLIP | Generic CLIP + LoRA | BioDINO-Edge Fast-Path | BioDINO-Edge + Fisher (SOTA) |
| :--- | :---: | :---: | :---: | :---: |
| **5-Shot Accuracy (Peak)** | 21.95% | 86.85% | 88.15% | **98.39%** |
| **30-Episode Monte Carlo Mean** | 20.41% ± 2.1% | 85.12% ± 1.6% | 87.40% ± 1.2% | **97.12% ± 0.82%** |
| **Macro F1-Score** | 19.84% | 84.22% | 88.02% | **97.14% ± 0.91%** |
| **False-Negative Rate (Infected Leaves)**| 18.40% | 4.12% | 2.05% | **0.564%** |
| **On-Device Model Size** | > 350 MB | ~140 MB | **21.40 MB** | **21.40 MB / 85.3 MB** |
| **Edge CPU Latency (ARM64)** | ~70 ms | 32.5 ms | **20.1 ms** | **24.2 ms** |
| **Network Requirement** | Mandatory Cloud | Mandatory Cloud | **100% Offline** | **100% Offline** |

> **Biosecurity Relevance:** The False Negative (FN) rate is compressed to **0.564%**, minimizing the hazardous oversight of quarantined infections in high-value crops.

---

## 📱 Mobile Systems Engineering

* **Zero Garbage Collection Churn:** Eliminates frame-rate stuttering via `PreallocatedTensor`. Employs pinned, reusable direct native memory (`Direct FloatBuffer`) for CameraX $224 \times 224 \times 3$ RGB transformations, avoiding runtime Java/Kotlin allocations.
* **Hardware Acceleration (NNAPI & DSP):** Leverages Microsoft ONNX Runtime Mobile bindings targeting the Android Neural Networks API (NNAPI) and Qualcomm Hexagon DSP / ARM Mali GPU.
* **Interactive Dosage Calculator:** Includes a dedicated calculator sheet (`presentation/dosage/`) that automatically translates diagnosis severity into chemical dilution recipes for 20L backpack sprayers or 1000L tractor spray tanks.
* **Hands-Free Text-to-Speech (TTS):** Integrated `TtsManager` automatically vocalizes diagnosis and emergency advice, allowing orchard scouts to operate wearing gloves without touching the screen.
* **Agronomic Weather Window Sheet:** Evaluates ambient microclimate parameters (wind velocity, temperature, relative humidity) to compute pesticide drift, evaporation, and wash-off risks, guiding responsible chemical application.
* **Comprehensive Internationalization:** Native support for English, Persian (فارسی with complete RTL layout), French, and German.

---

## 🏛️ Significance for Canadian & Antipodean Agricultural Research

* **New Zealand (Plant & Food Research, MPI Biosecurity, Hawke's Bay & Marlborough Viticulture):**  
  Supports early containment of invasive or climate-shifted pathogens. The air-gapped 5-shot enrollment feature empowers biosecurity scouts to isolate localized pathogen strains on remote orchards without exporting proprietary orchard data.
* **Canada (Agri-Food Canada, Niagara & Okanagan Orchards, Prairie Cereals & Potatoes):**  
  Provides resilient, battery-efficient diagnostic assistance across vast geographic acreages. Operates reliably under cold field conditions without data roaming or rural tower dependency.
* **Data Sovereignty & Privacy:**  
  Farm imagery and diagnostic records remain strictly stored in local sandboxed SQLite storage, fully respecting agricultural data privacy frameworks.

---

## 🚀 Getting Started

### Option A: Install Pre-Compiled APK
Download the latest signed release APK from the [Releases](https://github.com/mortezahatamikia-code/uncertainty-gated-paper/releases) section:
* `BioDINO-Edge-v1.0.0-arm64-v8a.apk` (Recommended for modern 64-bit devices)
* `BioDINO-Edge-v1.0.0-armeabi-v7a.apk` (For legacy 32-bit devices)
* `BioDINO-Edge-v1.0.0-universal.apk` (Compatible with all Android ABIs)

### Option B: Build from Source

#### Prerequisites
* Android Studio Ladybug (2024.2+) or IntelliJ IDEA
* JDK 17 (Temurin recommended)
* Android SDK 35 (API 26 minimum)

```bash
# Clone the repository
git clone https://github.com/mortezahatamikia-code/uncertainty-gated-paper.git
cd uncertainty-gated-paper/android_app

# Compile and assemble the release APK
./gradlew assembleRelease --no-daemon

# The generated APKs will be located in:
# app/build/outputs/apk/release/
```

### GitHub Actions Automated CI/CD
The repository features an automated multi-ABI release workflow (`.github/workflows/build-release.yml`):
* Compiles independent ARM64, ARMv7, and Universal APKs.
* Generates SHA-256 cryptographic checksums.
* Automatically extracts version-specific changelog notes from [`CHANGELOG.md`](CHANGELOG.md) and publishes GitHub Releases upon tagging (`git tag v1.0.0 && git push origin v1.0.0`).

---

## 📖 Citation

If you incorporate this edge architecture, model quantization pipeline, or the BioDINO framework in your academic research, please cite our manuscript:

```bibtex
@article{javidi2026biodinoedge,
  title     = {BioDINO-Edge: Gradient-Free Cascades of Frozen Vision Foundation Models for On-Device Few-Shot Plant Disease Diagnosis},
  author    = {Javidi Alsaadi, Reyhane and Samadzadeh, Mohammad Reza},
  journal   = {IEEE Transactions on Pattern Analysis and Machine Intelligence / Computers and Electronics in Agriculture (Under Review)},
  year      = {2026},
  url       = {https://github.com/reyhane-code/BioDINO-Edge-android}
}
```

---

## 📄 License
This project is licensed under the [Creative Commons Attribution 4.0 International (CC-BY-4.0)](LICENSE) for open academic research and field innovation.

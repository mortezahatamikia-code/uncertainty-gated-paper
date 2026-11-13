---
kind: dependency_management
name: Multi-Tool Dependency Management (pip, Gradle, npm)
category: dependency_management
scope:
    - '**'
source_files:
    - requirements.txt
    - android_app/build.gradle.kts
    - android_app/app/build.gradle.kts
    - android_app/gradle.properties
    - web/package.json
    - web/package-lock.json
---

## Approach

The repository is a multi-language research project and manages third-party dependencies through three independent toolchains, one per language surface:

| Surface | Toolchain | Manifest(s) | Lockfile / Resolution |
|---|---|---|---|
| Python pipeline (`pipeline/`, `experiments/`) | pip / PyPI | `requirements.txt` | No lockfile; versions pinned with `>=` lower bounds |
| Android app (`android_app/`) | Gradle + Kotlin | `build.gradle.kts` (top-level + `app/build.gradle.kts`) | No `.gradle/wrapper/gradle-wrapper.jar` checked in beyond the wrapper JAR itself; no `gradle.lockfile` |
| Web site (`web/`) | npm / Next.js | `package.json` | `package-lock.json` committed under `web/` |

There is no monorepo dependency manager (no `pyproject.toml`, no `Pipfile`, no `poetry.lock`, no `pnpm-lock.yaml`, no `go.mod`). Each sub-project owns its own dependency graph.

## Python — `requirements.txt`

- Single manifest at repo root: `requirements.txt` (33 lines).
- Uses `--extra-index-url https://download.pytorch.org/whl/cu124` to pull CUDA 12.4 wheels from the official PyTorch index rather than the default PyPI index.
- All packages use **lower-bound pinning** (`>=`) rather than exact pins or ranges:
  - `torch>=2.6.0`, `torchvision>=0.21.0`
  - `transformers>=4.40.0`, `peft>=0.10.0`, `accelerate>=0.28.0`, `safetensors>=0.4.0`
  - `numpy>=1.26.0`, `scikit-learn>=1.4.0`, `scipy>=1.12.0`, `pillow>=10.0.0`
  - `onnx>=1.15.0`, `onnxruntime>=1.17.0`
  - `kaggle>=1.6.0`, `ipykernel>=6.29.0`, `tqdm>=4.66.0`
- No `setup.py`, `pyproject.toml`, `Pipfile`, or `poetry.lock` exists at the repo root.
- The header comments document the hardware target (`CUDA 12.4 (NVIDIA RTX Series / Laptop GPUs)`) and the install command (`pip install -r requirements.txt`).
- There is no private PyPI registry configured in this file; only the standard PyPI index plus the extra PyTorch CUDA wheel index are used.

## Android — Gradle (Kotlin DSL)

Two Gradle manifests declare dependencies:

1. Top-level `android_app/build.gradle.kts` declares plugins and their versions via the `plugins {}` block:
   - `com.android.application` version `8.5.2`
   - `org.jetbrains.kotlin.android` version `2.0.21`
   - `org.jetbrains.kotlin.plugin.compose` version `2.0.21`
2. App module `android_app/app/build.gradle.kts` declares runtime dependencies in a single `dependencies { ... }` block:
   - AndroidX core/lifecycle/activity-compose
   - Jetpack Compose BOM pinned at `androidx.compose:compose-bom:2024.06.00` (BOM used for Compose UI, graphics, tooling-preview, material3, material-icons-extended)
   - CameraX grouped under a local `cameraxVersion = "1.3.4"` variable applied to `camera-core`, `camera-camera2`, `camera-lifecycle`, `camera-view`
   - ONNX Runtime Android `com.microsoft.onnxruntime:onnxruntime-android:1.18.0` (matching the exported ONNX model)
   - Kotlin coroutines `org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.1`
   - Testing: `junit:junit:4.13.2`, `androidx.test.ext:junit:1.1.5`, `androidx.test.espresso:espresso-core:3.5.1`

Gradle configuration also sets compile/target SDK to 35, minSdk 24, Java/Kotlin JVM target 17, and enables V1/V2/V3/V4 signing for release builds.

No private Maven/Google repositories are declared in these files; the defaults (Maven Central, Google Maven, Android Repository) are relied upon.

## Web — npm / Next.js

- Manifest: `web/package.json` (27 lines).
- Dependencies pinned with caret ranges (`^`) for devDependencies and exact versions for production deps:
  - Production: `next@16.4.3`, `react@19.3.0`, `react-dom@19.3.0`
  - Dev: `@tailwindcss/turbopack@^4`, `@types/node@^20`, `@types/react@^19`, `@types/react-dom@^19`, `eslint@^9`, `eslint-config-next@16.4.3`, `tailwindcss@^4`, `typescript@^5`
- Lockfile: `web/package-lock.json` is committed alongside `package.json`, so `npm ci` can reproduce an identical tree.
- Scripts: `dev`, `build`, `start`, `lint` (via `eslint`).

## Vendoring & Artifacts

- No vendored Python source trees (no `vendor/`, no `third_party/`).
- Prebuilt binary artifacts are committed directly as data files:
  - `cache_artifacts/biodino_companion_int8.onnx`, `pv_novel_embeddings.pt`, `pv_novel_embeddings_dinov3.pt`
  - Root-level `biodino_companion_int8.onnx`
- These are treated as static assets rather than package-managed dependencies.

## CI / Automation

- GitHub Actions workflows under `.github/workflows/` and `android_app/.github/workflows/` drive builds but do not introduce additional dependency-management tooling beyond invoking the native tools (`pip`, `gradlew`, `npm`).

## Conventions Observed

- Per-subsystem manifests: each language surface has its own manifest; there is no cross-tool resolution layer.
- Python uses `>=` lower-bound constraints without a lockfile, making installs reproducible only up to the latest compatible version on the given platform.
- Android groups related libraries behind local variables (`composeBOM`, `cameraxVersion`) to keep version numbers in one place within the Gradle script.
- Web uses exact versions for runtime dependencies and caret ranges for dev-only tooling, with a committed `package-lock.json`.
- No private registries, proxy settings, or `GOPRIVATE`-style configurations are present in any of the manifests examined.
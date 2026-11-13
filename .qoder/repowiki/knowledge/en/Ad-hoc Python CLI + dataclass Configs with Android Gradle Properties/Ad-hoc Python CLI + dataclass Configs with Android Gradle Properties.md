---
kind: configuration_system
name: Ad-hoc Python CLI + dataclass Configs with Android Gradle Properties
category: configuration_system
scope:
    - '**'
source_files:
    - pipeline/biodino_edge_pipeline.py
    - pipeline/biodino_hierarchical_pipeline.py
    - pipeline/biodino_v3_pipeline.py
    - pipeline/demo_predict.py
    - pipeline_morphopath/morphopath_engine.py
    - android_app/app/keystore.properties
    - android_app/gradle.properties
    - android_app/local.properties
    - DEPLOYMENT_GUIDE.md
---

## Overview

This repository has no centralized configuration framework (no `pydantic-settings`, no `.env` loader, no YAML/TOML config files for the Python pipelines). Runtime configuration is handled in three ad-hoc ways:

1. **Python entry points** use `argparse` to accept dataset paths, `--k_shot`, `--seed`, and flags like `--profile_latency` / `--use_cache`.
2. **Hyperparameters are defined as Python `dataclass`es** with sensible defaults, then passed explicitly into pipeline functions.
3. **Android/Gradle build-time configuration** lives in `android_app/app/keystore.properties` and `android_app/gradle.properties`.

There is no runtime environment-variable loading layer, no feature-flag system, and no secrets manager — secrets (keystore passwords) are committed directly into `keystore.properties`.

---

## Python Pipeline Configuration

### Entry-point CLI (`pipeline/biodino_edge_pipeline.py`)

The main benchmark script defines an `argparse.ArgumentParser` in its `main()` function (line 645):

- `--dataset`: choices `["plantvillage", "plantdoc", "both"]`, default `"plantvillage"`
- `--plantvillage_dir`, `--plantdoc_dir`: override dataset roots
- `--k_shot`: number of support samples per class
- `--seed`: master random seed
- `--profile_latency`: enable latency profiling
- `--use_cache`: load pre-extracted embeddings from `cache_artifacts/pv_novel_embeddings.pt`

These args are parsed once and used to construct a single `EdgeConfig` instance: `cfg = EdgeConfig(seed=args.seed, k_shot=args.k_shot)` (line 657).

### Hyperparameter container (`EdgeConfig`)

`EdgeConfig` is a `@dataclass` (lines 127–152) that centralizes all tunable hyperparameters:

| Field | Default | Meaning |
|---|---:|---|
| `seed` | 42 | Master RNG seed |
| `k_shot` | 5 | Few-shot support size |
| `batch_size` | 128 | Query batch size |
| `scale` | 20.0 | Logit temperature |
| `w_text` | 0.20 | Text prototype fusion weight |
| `w_lda` | 0.75 | Fisher-LDA ensemble weight |
| `w_base` | 0.65 | BioCLIP vs DINOv2 base fusion |
| `tau` | 0.35 | Shannon confidence gating threshold |
| `n_views` | 8 | Multi-view support augmentation count |

All other modules receive `cfg` as an explicit argument; there is no global mutable config object.

### Global constants

At module top-level (lines 109–124), the script sets deterministic seeds, device, project root, dataset roots, cache directory, and results file path as module-level constants:

```python
SEED = 42
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
PROJECT_ROOT = _PROJECT_ROOT
PLANTVILLAGE_ROOT = PROJECT_ROOT / "plantvillage"
PLANTDOC_ROOT = PROJECT_ROOT / "plantdoc"
CACHE_DIR = PROJECT_ROOT / "cache_artifacts"
RESULTS_FILE = PROJECT_ROOT / "biodino_edge_results.json"
```

### MorphoPath engine parameters

`MorphoPathEngine.__init__` (in `pipeline_morphopath/morphopath_engine.py`) takes ~20 keyword arguments covering shrinkage, router temperature, visual/text temperatures, Bayesian priors, micro-prototype weights, archetype maps, clutter suppression toggles, fast-exit thresholds, etc. These are stored directly as instance attributes — again, no schema validation or external config file.

### Other Python scripts

- `pipeline/demo_predict.py` also uses `argparse` for a real-time predictor CLI.
- `experiments/phase1_morphopath/grid_search.py` performs parameter sweeps but writes results to local JSON files rather than reading them back as config.
- No `.env`, `dotenv`, `os.environ` reads (except one `TF_CPP_MIN_LOG_LEVEL` suppressor in `demo_predict.py`).
- No YAML/TOML/JSON config loader exists in the Python codebase.

---

## Android / Gradle Build Configuration

### Keystore secrets (`android_app/app/keystore.properties`)

Contains plaintext keystore credentials:

```
storePassword=rewq4321
keyPassword=rewq4321
keyAlias=biodino
storeFile=biodino-release-key.jks
```

These are referenced by the Gradle build to sign release APKs. The same file is committed to the repo alongside the `.jks` keystore.

### Gradle properties (`android_app/gradle.properties`)

Standard Android/Gradle settings: JVM heap, AndroidX, non-transitive R class, Kotlin style, and `android.suppressUnsupportedCompileSdk=35`.

### Local SDK path (`android_app/local.properties`)

Points to the developer's Android SDK installation on Windows (`sdk.dir=C:\Users\mhata\AppData\Local\Android\Sdk`). This is typically gitignored in normal projects but is present here.

---

## Conventions and Constraints Observed

- **No shared configuration package**: each pipeline script owns its own `argparse` setup and `dataclass` defaults.
- **Defaults-first design**: every tunable parameter has a documented default value inside the code; external overrides come only through CLI flags.
- **Determinism by convention**: `SEED = 42` is set at module scope and propagated to `random`, `numpy`, and `torch` before any model loading.
- **Results-as-config**: benchmark outputs are written to `biodino_edge_results.json`, `biodino_hierarchical_results.json`, `biodino_v3_results.json` at the repo root, and later experiments read these JSON files to reuse prior runs — effectively treating output artifacts as configuration inputs.
- **Hardcoded paths**: dataset roots (`plantvillage`, `plantdoc`), cache dir (`cache_artifacts`), and model names (`vit_small_patch14_dinov2`, `hf-hub:imageomics/bioclip`) are embedded in source rather than loaded from config.
- **Android secrets not externalized**: keystore passwords live in plain text in `keystore.properties` checked into version control.
- **No runtime env-var based configuration**: the Python side does not consult `os.environ` for application settings (only TensorFlow log suppression).
- **No feature flags or environment profiles** (dev/staging/prod): behavior is toggled via CLI flags (`--use_cache`, `--profile_latency`) or constructor booleans (`enable_router`, `enable_rectification`, `enable_clutter_suppression`, `enable_fast_exit`).

---

## Key Files

- `pipeline/biodino_edge_pipeline.py` — `EdgeConfig` dataclass + `argparse` CLI
- `pipeline/biodino_hierarchical_pipeline.py` — another `argparse` entry point
- `pipeline/biodino_v3_pipeline.py` — third variant entry point
- `pipeline/demo_predict.py` — real-time predictor CLI
- `pipeline_morphopath/morphopath_engine.py` — `MorphoPathEngine` constructor parameters
- `android_app/app/keystore.properties` — keystore secrets
- `android_app/gradle.properties` — Gradle/Android build flags
- `android_app/local.properties` — local Android SDK path
- `DEPLOYMENT_GUIDE.md` — deployment instructions (web site & APK distribution)
- `datapackage.json` — dataset metadata manifest (not runtime config, but related artifact descriptor)
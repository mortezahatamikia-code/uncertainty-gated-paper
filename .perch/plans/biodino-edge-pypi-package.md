# BioDINO-Edge → پکیج pip با API داینامیک

## هدف

تبدیل `pipeline/` از مجموعه اسکریپت به یک کتابخانه نصب‌شدنی که:

- با `pip install biodino-edge` نصب شود و بدون torch هم import شود.
- یک کلاس اصلی `BioDINOEdge` با `fit` / `predict` داشته باشد.
- لایه‌ی تابعی مستقل (`biodino_edge.math`) برای کسانی که فقط ریاضیات را می‌خواهند.
- **همه‌ی پارامترها قابل تعیین، همه با دیفالت**، در یک درخت کانفیگ تودرتو با اعتبارسنجی.
- بک‌اند قابل تعویض: torch، onnx، یا فیچرهای از پیش استخراج‌شده.

---

## اصول طراحی

1. **صفر عارضه‌ی جانبی در import.** هیچ seed، هیچ `mkdir`، هیچ تشخیص خودکار GPU در سطح ماژول. همه در سازنده‌ی کلاس.
2. **دیفالت‌ها = اعداد مقاله.** هر پارامتری که در مقاله آمده، دیفالتش همان مقدار منتشرشده است، تا `BioDINOEdge()` خالی همان ۹۷.۴۱٪ را بازتولید کند.
3. **هسته بدون torch.** `math.py` فقط numpy + scikit-learn. torch یک extras است.
4. **بک‌اند به‌عنوان Protocol.** کاربر می‌تواند فیچر خودش را تزریق کند؛ این هم تست‌پذیری را آزاد می‌کند هم کسی را به GPU وابسته نمی‌کند.
5. **کانفیگ immutable و قابل سریال‌سازی.** `frozen=True`، با `from_dict` / `from_yaml` / `merge` / `to_dict`، و اعتبارسنجی در `__post_init__`.

---

## ساختار پکیج

```
biodino-edge/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/biodino_edge/
│   ├── __init__.py          # API عمومی، __version__
│   ├── py.typed
│   ├── config.py            # EdgeConfig و زیرکانفیگ‌ها + اعتبارسنجی
│   ├── math.py              # numpy/sklearn خالص (از core_math.py منتقل)
│   ├── backends/
│   │   ├── base.py          # FeatureBackend Protocol
│   │   ├── torch_backend.py # timm + open_clip (extras: full)
│   │   ├── onnx_backend.py  # onnxruntime (extras: onnx)
│   │   └── precomputed.py   # فیچر آماده، بدون هیچ وابستگی سنگین
│   ├── model.py             # کلاس BioDINOEdge
│   ├── transductive.py      # بازکالیبراسیون فرم بسته
│   ├── calibration.py       # ECE/MCE + temperature scaling
│   ├── results.py           # PredictionResult، BenchmarkResult
│   ├── weights.py           # دانلود و کش ONNX از GitHub Releases
│   └── cli.py               # console_scripts
├── tests/
│   ├── test_math.py         # بدون torch، golden values
│   ├── test_config.py
│   ├── test_model_precomputed.py
│   └── test_reproduce_paper.py   # ۹۷.۴۱٪ روی فیچر کش‌شده
└── examples/
    ├── quickstart.py
    ├── custom_backend.py
    └── streaming.py
```

---

## مدل کانفیگ

یک `EdgeConfig` ریشه که پنج زیرکانفیگ را نگه می‌دارد. هر زیرکانفیگ مستقل قابل ساخت و پاس دادن است.

```python
from biodino_edge import EdgeConfig, EncoderConfig, GateConfig

cfg = EdgeConfig(
    gate=GateConfig(tau=0.30, mode="shannon_margin"),
    encoder=EncoderConfig(batch_size=64),
)
```

### `EncoderConfig`
| پارامتر | دیفالت | توضیح |
|---|---|---|
| `dino_model` | `"vit_small_patch14_dinov2"` | نام timm |
| `bioclip_model` | `"hf-hub:imageomics/bioclip"` | نام open_clip |
| `image_size` | `224` | |
| `dino_dim` | `384` | |
| `bioclip_dim` | `512` | |
| `normalize` | `True` | L2 روی خروجی |
| `batch_size` | `128` | |
| `dtype` | `"float32"` | `float16` برای GPU |

### `AugmentConfig`
| پارامتر | دیفالت |
|---|---|
| `n_views` | `8` |
| `hflip` | `True` |
| `vflip` | `True` |
| `rotation_deg` | `15.0` |
| `jitter` | `0.2` |

### `FisherConfig`
| پارامتر | دیفالت | توضیح |
|---|---|---|
| `solver` | `"lsqr"` | |
| `shrinkage` | `"auto"` | Ledoit–Wolf؛ عدد ثابت هم می‌پذیرد |
| `w_lda` | `0.75` | وزن فیشر در آمیزش نهایی |
| `w_text` | `0.25` | وزن متن در آمیزش نهایی |
| `logit_scale` | `20.0` | همان γ مقاله |

### `GateConfig`
| پارامتر | دیفالت | توضیح |
|---|---|---|
| `mode` | `"shannon_margin"` | `shannon_margin` \| `margin` \| `entropy` \| `max_prob` \| `none` |
| `tau` | `0.35` | آستانه‌ی مقاله |
| `entropy_eps` | `1e-8` | |

### `TransductiveConfig`
| پارامتر | دیفالت |
|---|---|
| `enabled` | `True` |
| `support_weight` | `3` |
| `max_anchors_per_class` | `20` |
| `anchor_threshold` | `0.70` |
| `fifo` | `True` |
| `refit_after` | `20` |

### `CalibrationConfig`
| پارامتر | دیفالت |
|---|---|
| `enabled` | `False` |
| `method` | `"temperature"` |
| `n_bins` | `10` |

### `BackendConfig`
| پارامتر | دیفالت |
|---|---|
| `kind` | `"torch"` |
| `onnx_tier1` | `None` |
| `onnx_tier2` | `None` |
| `weights_dir` | `None` → `~/.cache/biodino` |
| `auto_download` | `True` |
| `num_threads` | `4` |

### `RuntimeConfig`
| پارامتر | دیفالت |
|---|---|
| `device` | `"auto"` |
| `seed` | `42` |
| `deterministic` | `False` |
| `verbose` | `False` |

**اعتبارسنجی:** `tau ∈ [0,1]`، `w_lda + w_text == 1`، `n_views ≥ 1`، `kind` در مجموعه‌ی مجاز، `dino_dim + bioclip_dim == 896` مگر اینکه کاربر صریحاً override کند.

---

## API عمومی — سه لایه

### ۱. سطح بالا
```python
from biodino_edge import BioDINOEdge

model = BioDINOEdge()                       # همه دیفالت
model.fit(
    support_images=support_paths,
    support_labels=labels,
    class_names=class_names,
    prompts=prompts_map,                    # اختیاری
)

res = model.predict(query_paths)
res.top1            # np.ndarray از نام کلاس
res.top2
res.probabilities   # (N, C)
res.confidence      # امتیاز گیت
res.tier            # 1 یا 2
res.latency_ms
```

متدهای دیگر: `predict_proba`، `fit_transform`، `partial_fit` (استریم)، `save` / `load` (joblib، بدون torch)، `from_pretrained`، `evaluate`، `calibration_report`.

### ۲. سطح تابعی
```python
from biodino_edge.math import (
    shannon_confidence, fit_fisher_lda, class_prototypes,
    ensemble_probs, transductive_refit, l2_normalize,
)
```
همه numpy-native، بدون torch، قابل استفاده در هر جای دیگر.

### ۳. سطح بک‌اند
```python
class FeatureBackend(Protocol):
    dino_dim: int
    bioclip_dim: int
    def encode_images(self, images) -> tuple[np.ndarray, np.ndarray]: ...
    def encode_text(self, prompts: list[str]) -> np.ndarray: ...
```

سه پیاده‌سازی آماده: `TorchBackend`، `OnnxBackend`، `PrecomputedBackend`. کاربر می‌تواند کلاس خودش را بنویسد و پاس بدهد.

---

## وزن‌ها

دو فایل ONNX موجود (`biodino_mobile_int8.onnx` ۲۲.۰۵MB، `biodino_companion_int8.onnx` ۸۵.۲۶MB) داخل wheel نمی‌روند. PyPI سقف ۱۰۰MB دارد و آپلود ۸۵MB عذاب است. به‌جایش:

- در GitHub Releases آپلود شوند.
- `weights.py` در اولین اجرا دانلود و در `~/.cache/biodino` با checksum کش کند.
- `biodino download-weights` برای دانلود دستی.
- `BackendConfig.auto_download=False` برای محیط آفلاین.

---

## CLI

```
biodino fit --support ./data --out model.joblib
biodino predict --model model.joblib --images ./queries --json
biodino benchmark --dataset plantvillage --episodes 30
biodino download-weights --tier all
```

`main()` فعلی با argparse حفظ می‌شود اما به `cli.py` منتقل و روی همان API سوار می‌شود.

---

## بسته‌بندی

```toml
[project]
name = "biodino-edge"
requires-python = ">=3.10"
dependencies = ["numpy>=1.24", "scikit-learn>=1.3", "pillow>=10.0"]

[project.optional-dependencies]
full = ["torch>=2.2", "timm>=0.9", "open_clip_torch>=2.24"]
onnx = ["onnxruntime>=1.17"]
dev  = ["pytest", "pytest-cov", "ruff", "mypy"]
```

ساختار `src/` با hatchling، `py.typed` برای type checker، نسخه از `__version__`.

---

## تست و CI

- `test_math.py` — مقادیر golden برای شانون، فیشر، آمیزش. بدون torch.
- `test_config.py` — اعتبارسنجی، merge، سریال‌سازی.
- `test_model_precomputed.py` — کل مسیر fit/predict با فیچر تزریقی.
- `test_reproduce_paper.py` — روی `cache_artifacts/pv_novel_embeddings.pt` همان ۹۷.۴۱٪ ± ۰.۱ بازتولید شود. این تست، قرارداد اصلی است.
- GitHub Actions: ماتریس Python 3.10–3.12 روی ubuntu + windows، نصب فقط `[dev]` (بدون torch) برای سرعت.

---

## ریسک‌ها و تصمیم‌های صریح

**۱. ابهام در دو blend.** `EdgeConfig.w_text=0.20` در کد برای آمیزش پروتوتایپ است، ولی مقاله `0.75 p_fisher + 0.25 p_text` می‌گوید. اینها دو مرحله‌ی متفاوت‌اند و در کد فعلی به هم چسبیده‌اند. در پکیج هر دو صریح می‌شوند: `FisherConfig.w_text` برای آمیزش نهایی، و یک `PrototypeConfig.w_text` جدا برای آمیزش پروتوتایپ. قبل از انتشار باید با اجرای تست بازتولید تثبیت شود کدام کدام است.

**۲. تفاوت دیفالت با مقاله.** اگر تست بازتولید ۹۷.۴۱٪ را نداد، دیفالت‌ها عوض می‌شوند نه تست. عدد مقاله مرجع است.

**۳. `pipeline/` دست‌نخورده می‌ماند.** اسکریپت‌های فعلی برای بازتولید مقاله سر جایشان می‌مانند؛ پکیج از `core_math.py` کپی می‌گیرد و بعد از سبز شدن تست‌ها، اسکریپت‌ها به پکیج delegate می‌کنند.

**۴. لایسنس و نام.** نام `biodino-edge` روی PyPI آزاد است ولی باید قبل از انتشار چک شود. لایسنس پیشنهادی MIT؛ اگر EAAI الزام دیگری دارد، قبل از push مشخص شود.

---

## ترتیب اجرا

1. ساخت اسکلت `src/biodino_edge/` + `pyproject.toml`.
2. انتقال `core_math.py` به `math.py` و حذف وابستگی torch از آن.
3. نوشتن `config.py` با همه‌ی زیرکانفیگ‌ها و اعتبارسنجی.
4. نوشتن `backends/` — اول `PrecomputedBackend` (بدون وابستگی)، بعد torch، بعد onnx.
5. نوشتن `model.py` با `fit` / `predict` / `save` / `load`.
6. `transductive.py` و `calibration.py`.
7. `weights.py` + `cli.py`.
8. تست‌ها، از جمله تست بازتولید ۹۷.۴۱٪.
9. `pip install -e .` و اجرای واقعی روی همین سیستم.
10. README، examples، و آماده‌سازی برای push.
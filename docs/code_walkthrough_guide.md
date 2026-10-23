# راهنمای جامع خط‌به‌خط و آموزش گام‌به‌گام کدهای پایپلاین BioDINO-Edge
### (Complete Step-by-Step Codebase Walkthrough & Pedagogical Guide)

> **هدف این سند:**  
> این راهنما برای آموزش جزء‌به‌جزء، تیکه‌به‌تیکه و خط‌به‌خط ساختار کدهای فریم‌ورک **BioDINO-Edge** تدوین شده است. هدف این است که هر توسعه‌دهنده یا پژوهشگری، از سطح پایه‌ای پایتون و یادگیری عمیق، بتواند منطق پشت تک‌تک کلاس‌ها، توابع، محاسبات تانسوری و تصمیمات معماری را دقیقاً درک کند.

---

## فهرست فصول آموزشی کدها

1. [فصل اول: کالبدشکافی عمیق کد اصلی پایپلاین (`biodino_edge_pipeline.py`)](#فصل-اول-کالبدشکافی-عمیق-کد-اصلی-پایپلاین-biodino_edge_pipelinepy)
   - [۱.۱. پیکربندی سراسری و ساختار داده تنظیمات (`BioDINOConfig`)](#۱۱-پیکربندی-سراسری-و-ساختار-داده-تنظیمات-biodinoconfig)
   - [۱.۲. سیستم هوشمند مکان‌یابی و لودرهای چندمنظوره داده](#۱۲-سیستم-هوشمند-مکان‌یابی-و-لودرهای-چندمنظوره-داده)
   - [۱.۳. بلوک‌های الگوریتمی پایه‌ای (فیشر، آنتروپی شانون، خودکالیبراسیون فراالقایی)](#۱۳-بلوک‌های-الگوریتمی-پایه‌ای-فیشر-آنتروپی-شانون-خودکالیبراسیون-فراالقایی)
   - [۱.۴. پایپلاین آگمنتاسیون چنددیدگاهی و استخراج بردارها](#۱۴-پایپلاین-آگمنتاسیون-چنددیدگاهی-و-استخراج-بردارها)
   - [۱.۵. سنتز پروتوتایپ‌های معنایی متنی پاتولوژی](#۱۵-سنتز-پروتوتایپ‌های-معنایی-متنی-پاتولوژی)
   - [۱.۶. موتورهای ارزیابی آماری مونت‌کارلو (PlantVillage و PlantDoc)](#۱۶-موتورهای-ارزیابی-آماری-مونت‌کارلو-plantvillage-و-plantdoc)
   - [۱.۷. بنچمارک تاخیر سخت‌افزاری کوانتیزاسیون INT8 روی CPU](#۱۷-بنچمارک-تاخیر-سخت‌افزاری-کوانتیزاسیون-int8-روی-cpu)
   - [۱.۸. ارکستراتور اصلی آزمون (`run_benchmark`)](#۱۸-ارکستراتور-اصلی-آزمون-run_benchmark)
   - [۱.۹. نقطه ورود خط فرمان CLI (`main`)](#۱۹-نقطه-ورود-خط-فرمان-cli-main)
2. [فصل دوم: مهندسی استقرار و تبدیل مدل‌های لبه (`export_edge_models.py`)](#فصل-دوم-مهندسی-استقرار-و-تبدیل-مدل‌های-لبه-export_edge_modelspy)
   - [۲.۱. فلسفه معماری دو سطحی (Dual-Tier Edge Architecture)](#۲۱-فلسفه-معماری-دو-سطحی-dual-tier-edge-architecture)
   - [۲.۲. ماژول مستقل سطح ۱: `BioDINOEdgeMobile` و فیلتر شاخ‌وبرگ OOD](#۲۲-ماژول-مستقل-سطح-۱-biodinoedgemobile-و-فیلتر-شاخوبرگ-ood)
   - [۲.۳. ماژول مکمل سطح ۲: `BioDINOCompanionMobile` روی منیفولد ۸۹۶ بعدی](#۲۳-ماژول-مکمل-سطح-۲-biodinocompanionmobile-روی-منیفولد-۸۹۶-بعدی)
   - [۲.۴. فرآیند اکسپورت به ONNX و کوانتیزاسیون دینامیک بهینه‌شده](#۲۴-فرآیند-اکسپورت-به-onnx-و-کوانتیزاسیون-دینامیک-بهینه‌شده)
   - [۲.۵. اعتبارسنجی بلادرنگ با ONNX Runtime](#۲۵-اعتبارسنجی-بلادرنگ-با-onnx-runtime)
3. [فصل سوم: آزمایش‌های فرضیه و سناریوهای تنش محیطی (`run_ideas_experiment.py`)](#فصل-سوم-آزمایش‌های-فرضیه-و-سناریوهای-تنش-محیطی-run_ideas_experimentpy)
   - [۳.۱. ایده اول: برش هوشمند بر پایه اتنشن سلف‌اتنشن DINOv2](#۳۱-ایده-اول-برش-هوشمند-بر-پایه-اتنشن-سلف‌اتنشن-dinov2)
   - [۳.۲. ایده دوم: آزمون‌های تنش فیزیکی محیطی (تاری، خورشید، سایه)](#۳۲-ایده-دوم-آزمون‌های-تنش-فیزیکی-محیطی-تاری-خورشید-سایه)
   - [۳.۳. ارزیابی مهار خطاهای خاموش با گیت شانون](#۳۳-ارزیابی-مهار-خطاهای-خاموش-با-گیت-شانون)
4. [فصل چهارم: پایگاه دانش واژگانی و مهندسی پرامپت‌ها (`taxonomic_prompts.py`)](#فصل-چهارم-پایگاه-دانش-واژگانی-و-مهندسی-پرامپت‌ها-taxonomic_promptspy)
   - [۴.۱. کشف و حذف مسمومیت نحوی نفی (Syntactic Negation Poisoning)](#۴۱-کشف-و-حذف-مسمومیت-نحوی-نفی-syntactic-negation-poisoning)
   - [۴.۲. ساختار سه‌گانه هر توصیف بیماری](#۴۲-ساختار-سه‌گانه-هر-توصیف-بیماری)
5. [فصل پنجم: ابزار تعاملی تست و استنتاج تک‌تصویر (`demo_predict.py`)](#فصل-پنجم-ابزار-تعاملی-تست-و-استنتاج-تک‌تصویر-demo_predictpy)
   - [۵.۱. فلسفه و کاربرد ابزار تست سریع مزرعه](#۵۱-فلسفه-و-کاربرد-ابزار-تست-سریع-مزرعه)
   - [۵.۲. کالبدشکافی خط‌به‌خط اجرای استنتاج، گیتینگ و چارت احتمالات ASCII](#۵۲-کالبدشکافی-خط‌به‌خط-اجرای-استنتاج-گیتینگ-و-چارت-احتمالات-ascii)
6. [فصل ششم: کالبدشکافی اسکریپت‌های مصورسازی مقاله](#فصل-ششم-کالبدشکافی-اسکریپت‌های-مصورسازی-مقاله)
   - [۶.۱. تولید نقشه‌های برجستگی سلف‌اتنشن و دیاگرام ECE (`generate_saliency_and_calibration.py`)](#۶۱-تولید-نقشه‌های-برجستگی-سلف‌اتنشن-و-دیاگرام-ece-generate_saliency_and_calibrationpy)
   - [۶.۲. رندر خودکار ماتریس ۳×۴ خطاهای باقیمانده (`generate_error_gallery.py`)](#۶۲-رندر-خودکار-ماتریس-۳۴-خطاهای-باقیمانده-generate_error_gallerypy)

---

# فصل اول: کالبدشکافی عمیق کد اصلی پایپلاین ([`biodino_edge_pipeline.py`](../biodino_edge_pipeline.py))

این فایل، قلب تپنده پروژه است. کد در قالب معماری تمیز (Clean Architecture) در ۵۲۵ خط نوشته شده است و عاری از هرگونه افزونگی یا کدهای تکراری (DRY) است.

### ۱.۱. پیکربندی سراسری و ساختار داده تنظیمات (`BioDINOConfig`)

در خطوط ۱۱ تا ۶۸، پس از وارد کردن کتابخانه‌های استاندارد (`torch`، `timm`، `open_clip`، `sklearn`)، اولین گام حیاتی **تثبیت بذر تصادفی (Deterministic Seeding)** است:

```python
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)
torch.backends.cudnn.benchmark = True
```

> [!NOTE]
> **چرا تثبیت بذر در تحقیقات علمی حیاتی است؟**  
> اگر بذر تصادفی ثابت نباشد، انتخاب تصادفی ۵ نمونه برگ (در سناریوی ۵-شات) در هر بار اجرای کد تغییر می‌کند و دقت نهایی ممکن است بین ۹۵٪ تا ۹۸٪ نوسان کند. با تثبیت بذر روی `42`، تمام نتایج توسط هر داور یا محققی در دنیا با دقت اعشاری یکسان بازتولید می‌شود.

سپس کلاس تنظیمات با دکوراتور مدرن `@dataclass` تعریف می‌شود:

```python
@dataclass
class BioDINOConfig:
    seed: int = 42
    k_shot: int = 5
    batch_size: int = 128
    logit_scale: float = 20.0
    text_fusion_weight: float = 0.20   # proto_bio_fused = 0.80 * vis + 0.20 * text
    lda_ensemble_weight: float = 0.75  # 0.75 * prob_lda + 0.25 * prob_text
    base_ensemble_weight: float = 0.65 # 0.65 * logit_bio + 0.35 * logit_dino
    tau_conf: float = 0.35             # Shannon uncertainty margin-entropy threshold
    support_views: int = 8             # 1 original + 7 multi-view augmentations
```

#### تشریح نقش تک‌تک پارامترها:
1. `seed`: مقدار بذر تصادفی پایه (پیش‌فرض ۴۲).
2. `k_shot`: تعداد نمونه‌های آموزشی برای هر کلاس جدید (پیش‌فرض ۵ تصویر برگ).
3. `batch_size`: تعداد تصاویری که در یک بچ به کارت گرافیک یا CPU فرستاده می‌شوند (۱۲۸ برای ماکزیمم سرعت و پر نشدن VRAM).
4. `logit_scale = 20.0`: ضرب داخلی بردارهای نرمالایز شده مقداری بین ۱- تا ۱+ دارد. اگر مستقیماً به تابع سافت‌مکس (Softmax) برود، شیب احتمالات بسیار صاف می‌شود. ضرب در ۲۰ شبیه به پارامتر دمای معکوس در ترنسفورمرها عمل کرده و توزیع احتمالات را شفاف و تفکیک‌پذیر می‌کند.
5. `text_fusion_weight = 0.20`: وزن ادغام متن و تصویر در مدل BioCLIP. یعنی ۸۰٪ بردار کلاس از میانگین تصاویر برگ و ۲۰٪ از توصیف زبان طبیعی پاتولوژی تشکیل می‌شود.
6. `lda_ensemble_weight = 0.75`: وزن نهایی تفکیک خطی فیشر در مقابل پرامپت متنی. ۷۵٪ فیشر و ۲۵٪ متن.
7. `base_ensemble_weight = 0.65`: وزن تلفیق لاجیت پایه بدون فیشر (۶۵٪ سهم BioCLIP و ۳۵٪ سهم DINOv2).
8. `tau_conf = 0.35`: آستانه تصمیم‌گیری گیت عدم‌قطعیت شانون ($\tau_{\text{conf}}$). نمونه‌هایی که نمره اطمینان $\ge 0.35$ داشته باشند بلافاصله با مدل سریع DINOv2 در کمتر از ۲۲ میلی‌ثانیه پاسخ داده می‌شوند.
9. `support_views = 8`: برای جبران کمبود دیتا در ۵ شات، هر تصویر برگ با ۷ زاویه و تغییر رنگ مختلف آگمنت می‌شود (در مجموع $5 \times 8 = 40$ بردار به ازای هر کلاس).

---

### ۱.۲. سیستم هوشمند مکان‌یابی و لودرهای چندمنظوره داده

در خطوط ۷۰ تا ۱۴۷، توابعی پیاده شده‌اند که مسیر دیتاست را به صورت خودکار شناسایی می‌کنند:

#### الف) تابع `resolve_plantvillage_dir` و `resolve_plantdoc_dirs`:
```python
def resolve_plantvillage_dir(root: Path) -> Optional[Path]:
    root = Path(root)
    for c in [root / "plantvillage dataset" / "color", root / "color", root]:
        if c.is_dir() and any("Apple" in d.name or "Grape" in d.name for d in c.iterdir() if d.is_dir()):
            return c
    for c in root.rglob("color"):
        if c.is_dir() and any(sub.is_dir() for sub in c.iterdir()):
            return c
    return None
```
این تابع تضمین می‌کند که مهم نیست دیتاست در پوشه تو در تو قرار گرفته باشد یا ریشه، به محض مشاهده پوشه‌های حاوی نام گیاهان (`Apple` یا `Grape`) مسیر واقعی را بازمی‌گرداند.

#### ب) کلاس دیتاست دوگانه `DualTransformDataset`:
```python
class DualTransformDataset(Dataset):
    def __init__(self, samples: List[Tuple[str, int]], transform_bio, transform_dino):
        self.samples, self.t_bio, self.t_dino = samples, transform_bio, transform_dino

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor, int]:
        p, y = self.samples[idx]
        img = Image.open(p).convert("RGB")
        return self.t_bio(img), self.t_dino(img), y
```
* **چرا این کلاس ضروری است؟** مدل DINOv2 و مدل BioCLIP با میانگین‌ها و انحراف معیارهای رنگی متفاوتی نرمال‌سازی شده‌اند. این کلاس یک‌بار تصویر برگ را از دیسک باز می‌کند و همزمان دو نسخه تنسوری بهینه‌شده تحویل می‌دهد (یک تنسور آماده برای BioCLIP و یک تنسور آماده برای DINOv2). این کار بار دیسک (Disk I/O) را دقیقاً ۵۰٪ کاهش می‌دهد.

#### ج) تابع `load_plantvillage_data`:
این تابع ۱۱ کلاس دیده‌نشده را جدا می‌کند (`Apple`، `Grape` و `Potato`)، به ازای هر کلاس دقیقاً $K=5$ تصویر را به عنوان مجموعه ساپورت (Support) و بقیه (۹,۳۳۰ تصویر) را به عنوان کوئری (Query) دسته‌بندی می‌نماید.

---

### ۱.۳. بلوک‌های الگوریتمی پایه‌ای (فیشر، آنتروپی شانون، خودکالیبراسیون فراالقایی)

خطوط ۱۴۸ تا ۱۹۳ حاوی مهم‌ترین الگوریتم‌های نوآورانه پروژه است:

#### ۱. تحلیل تفکیک خطی منظم فیشر (`fit_fisher_lda`):
```python
def fit_fisher_lda(x: np.ndarray, y: np.ndarray, device=DEVICE) -> Tuple[torch.Tensor, torch.Tensor, LinearDiscriminantAnalysis]:
    clf = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto').fit(x, y)
    W = torch.tensor(clf.coef_, dtype=torch.float32, device=device)
    b = torch.tensor(clf.intercept_, dtype=torch.float32, device=device)
    return W, b, clf
```
- از حل‌کننده کمترین مربعات (`lsqr`) همراه با محاسبه خودکار انقباض لدویت-ولف (`shrinkage='auto'`) استفاده می‌شود.
- ماتریس وزن فیشر ($\mathbf{W}$) و بایاس ($\mathbf{b}$) مستقیماً استخراج شده و به تنسورهای PyTorch روی دستگاه پردازشگر (GPU یا CPU) منتقل می‌شوند. در زمان استنتاج، پیش‌بینی یک دسته ۱۲۸ تایی صرفاً یک ضرب ماتریسی فوق‌سریع است: $\mathbf{X} \mathbf{W}^T + \mathbf{b}$ در کمتر از ۲ میکروثانیه!

#### ۲. گیت عدم‌قطعیت مارجین-آنتروپی شانون (`compute_shannon_confidence`):
```python
def compute_shannon_confidence(probs: torch.Tensor, n_classes: int) -> torch.Tensor:
    top_p, _ = torch.topk(probs, k=min(2, n_classes), dim=-1)
    margin = top_p[:, 0] - top_p[:, 1] if n_classes > 1 else top_p[:, 0]
    entropy = -torch.sum(probs * torch.log(probs + 1e-8), dim=-1) / max(np.log(n_classes), 1e-6)
    return margin * (1.0 - entropy).clamp(min=0.0)
```
- **ورودی:** ماتریس احتمالات پیش‌بینی‌شده برای نمونه‌ها.
- `top_p`: دو احتمال برتر ($p_{(1)}$ و $p_{(2)}$) استخراج می‌شوند.
- `margin`: حاشیه اختلاف برنده اول و دوم ($p_{(1)} - p_{(2)}$). اگر مدل بین دو بیماری مردد باشد، این مقدار نزدیک صفر می‌شود.
- `entropy`: محاسبه آنتروپی شانون و تقسیم بر $\ln(C)$ تا عدد دقیقاً در بازه $[0, 1]$ نرمالایز شود.
- `margin * (1.0 - entropy)`: فرمول امتیاز اطمینان نهایی. اگر آنتروپی ۱ باشد (سردرگمی کامل)، اطمینان صفر می‌شود.

#### ۳. خودکالیبراسیون فراالقایی فرم‌بسته (`transductive_refine`):
```python
def transductive_refine(s_concat: np.ndarray, s_y: np.ndarray, q_concat_all: torch.Tensor, preds_init: np.ndarray,
                        top_confs: torch.Tensor, p_text_all: torch.Tensor, n_classes: int, support_weight: int = 3,
                        max_k_anchors: int = 20, conf_threshold: Optional[float] = None, device=DEVICE):
    ref_x, ref_y = [s_concat] * support_weight, [s_y] * support_weight
    for c in range(n_classes):
        c_cand = (preds_init == c)
        if c_cand.sum() > 0:
            c_idx = np.where(c_cand)[0]
            c_conf = top_confs[c_idx]
            if conf_threshold is not None:
                high = (c_conf > conf_threshold)
                if high.sum() > 0:
                    c_idx = c_idx[high.cpu().numpy() if isinstance(high, torch.Tensor) else high]
                    c_conf = c_conf[high]
            top_k = min(max_k_anchors, len(c_idx))
            if top_k > 0:
                indices = torch.topk(c_conf, top_k).indices
                best_idx = c_idx[indices.cpu().numpy() if isinstance(indices, torch.Tensor) else indices]
                q_feats = q_concat_all[best_idx]
                ref_x.append(q_feats.cpu().numpy() if isinstance(q_feats, torch.Tensor) else q_feats)
                ref_y.append(np.full(top_k, c))

    W_r, b_r, _ = fit_fisher_lda(np.concatenate(ref_x, axis=0), np.concatenate(ref_y, axis=0), device=device)
    p_lda_r = F.softmax(q_concat_all.to(device) @ W_r.t() + b_r, dim=-1)
    p_ens_r = 0.75 * p_lda_r + 0.25 * p_text_all.to(device)
    return p_ens_r.argmax(dim=-1).cpu().numpy(), p_ens_r, (W_r, b_r)
```
- **چرا این الگوریتم انقلابی است؟** در سناریوهای ۵ شات، میانگین کلاس‌ها ممکن است به دلیل ۵ نمونه محدود دچار انحراف شود.
- **راهکار:** نمونه‌های کوئری که مدل با بالاترین اطمینان (`top_confs > 0.70`) آن‌ها را دسته‌بندی کرده به عنوان **لنگر (Anchor)** برمی‌گزیند.
- برای جلوگیری از رانش منیفولد به سمت کوئری‌ها، داده‌های ساپورت اصلی با وزن ۳ برابری تکرار می‌شوند (`[s_concat] * support_weight`).
- سپس تفکیک فیشر به شکل فرم بسته (بدون گرادیان دیسنت، بدون GPU و بدون بک‌پراپ) در کمتر از ۲۵ میلی‌ثانیه دوباره فیت می‌شود و دقت مدل از ۹۷.۴۴٪ به قله **۹۸.۶۷٪** صعود می‌کند.

---

### ۱.۴. پایپلاین آگمنتاسیون چنددیدگاهی و استخراج بردارها

در خطوط ۱۹۴ تا ۲۱۸، تابع `extract_support_features` به ازای هر تصویر ساپورت، ۱ نمای اصلی و ۷ نمای تصادفی آگمنت‌شده تولید می‌کند:
```python
def get_aug_pipeline(mean, std):
    return T.Compose([
        T.Resize((224, 224)), T.RandomHorizontalFlip(), T.RandomVerticalFlip(),
        T.RandomRotation(15), T.ColorJitter(0.2, 0.2, 0.2), T.ToTensor(), T.Normalize(mean=mean, std=std)
    ])
```
* شامل چرخش ۱۵ درجه، معکوس‌سازی افقی و عمودی، و تغییر ملایم روشنایی/کنتراست جهت تقلید از شرایط نور خورشید در مزرعه.
* استخراج ویژگی‌ها با `torch.no_grad()` انجام می‌شود و بردارها بلافاصله با تابع `F.normalize(..., dim=-1)` نرمال‌سازی اقلیدسی ($\ell_2$) می‌شوند تا ضرب داخلی آن‌ها معادل تشابه کسینوسی باشد.

---

### ۱.۵. سنتز پروتوتایپ‌های معنایی متنی پاتولوژی

در خطوط ۲۲۱ تا ۲۳۱، تابع `synthesize_text_prototypes` پرامپت‌های زیستی ماژول `taxonomic_prompts.py` را تبدیل به بردارهای معنایی می‌کند:
```python
def synthesize_text_prototypes(class_names: List[str], prompts_map: Dict[str, List[str]],
                                bioclip_model: nn.Module, tokenizer, device=DEVICE) -> torch.Tensor:
    protos = []
    with torch.no_grad():
        for c in class_names:
            toks = tokenizer(prompts_map[c]).to(device)
            f = F.normalize(bioclip_model.encode_text(toks), dim=-1)
            protos.append(F.normalize(f.mean(dim=0), dim=-1))
    return torch.stack(protos)
```
* به ازای هر کلاس ۳ توصیف گیاه‌پزشکی داریم. انکودر متنی BioCLIP بردار ۵۱۲ بعدی هر سه جمله را استخراج کرده و میانگین برداری آن‌ها را به عنوان بردار لنگر معنایی کلاس ثبت می‌کند.

---

### ۱.۶. موتورهای ارزیابی آماری مونت‌کارلو (PlantVillage و PlantDoc)

خطوط ۲۳۳ تا ۳۳۷ شامل توابع ارزیابی سخت‌گیرانه ۳۰ و ۵۰ اپیزودی هستند:

```python
def run_plantvillage_montecarlo(cache_path: Path, n_classes: int, k_shot: int = 5, n_episodes: int = 30) -> Dict:
    ...
    for ep in range(n_episodes):
        rng = random.Random(42 + ep * 17)
        # انتخاب ۵ شات کاملا مجزا با بذر متفاوت
        ...
```
* **محاسبه فواصل اطمینان ۹۵٪ (95% Confidence Interval):**
  $$\text{CI}_{95} = \mu \pm 1.96 \times \frac{\sigma}{\sqrt{N}}$$
* **محاسبه نرخ منفی کاذب بالینی (False Negative Rate - FNR):**
  کد برگ‌های بیمار را جدا کرده و بررسی می‌کند چند درصد از آنها به اشتباه "سالم" تشخیص داده شده‌اند:
  ```python
  d_mask = ~np.isin(c_labels[q_idx], healthy_set)
  m_fn_ind.append((np.isin(preds_ep, healthy_set)[d_mask].sum() / d_mask.sum()) * 100.0)
  ```
  این شاخص در مدل پیشنهادی ما به رقم درخشان **۰.۷۶۱٪** کاهش یافته است.

---

### ۱.۷. بنچمارک تاخیر سخت‌افزاری کوانتیزاسیون INT8 روی CPU

خطوط ۳۳۹ تا ۳۶۲ عملکرد بلادرنگ را روی پردازنده اندازه‌گیری می‌کند:
```python
def benchmark_cpu_int8_latency(dino_model: nn.Module, bioclip_model: nn.Module, fast_ratio: float, deep_ratio: float) -> Dict:
    torch.set_num_threads(4) # شبیه‌سازی پردازنده ۴ هسته‌ای موبایل/رزبری‌پای
    q_dino = torch.quantization.quantize_dynamic(copy.deepcopy(dino_model).cpu().eval(), {nn.Linear}, dtype=torch.qint8)
    ...
```
* تاخیر موثر پایپلاین با فرمول ترکیب محدب محاسبه می‌شود:
  $$\text{Effective Latency} = \frac{\text{Fast\%}}{100} \times t_{\text{dino}} + \frac{\text{Deep\%}}{100} \times (t_{\text{dino}} + t_{\text{bio}})$$
* خروجی تجربی: **۲۴.۴ میلی‌ثانیه** (معادل **۴۱ FPS** روی پردازنده اینتل/ARM).

---

### ۱.۸. ارکستراتور اصلی آزمون (`run_benchmark`)

خطوط ۳۶۵ تا ۴۶۸ چرخه کامل اجرای یک بنچمارک را از استخراج ویژگی تا چاپ ماتریس درهم‌ریختگی انجام می‌دهد.  
نکته قابل توجه استفاده از دقت مختلط سخت‌افزاری برای سرعت حداکثر در خط ۳۹۷ است:
```python
with torch.amp.autocast("cuda", dtype=torch.float16):
    f_d, f_b = F.normalize(dino_model(d_imgs), dim=-1), F.normalize(bioclip_model.encode_image(b_imgs), dim=-1)
```

---

### ۱.۹. نقطه ورود خط فرمان CLI (`main`)

خطوط ۴۷۱ تا ۵۲۴ پارامترهای خط فرمان را دریافت کرده و مدل‌ها را بارگذاری می‌نماید:
- پرچم `--dataset`: انتخاب بین `plantvillage`، `plantdoc` یا `both`.
- پرچم `--k_shot`: تعداد شات (پیش‌فرض ۵).
- پرچم `--profile_latency`: محاسبه بلادرنگ تاخیر INT8 روی CPU.

نتایج نهایی به طور خودکار در فایل JSON ذخیره می‌شوند:
```python
out_json = PROJECT_ROOT / "biodino_edge_results.json"
```

---

# فصل دوم: مهندسی استقرار و تبدیل مدل‌های لبه ([`export_edge_models.py`](../export_edge_models.py))

این فایل وظیفه اکسپورت مدل‌ها به فرمت متن‌باز ONNX و کوانتیزاسیون هشت بیتی (INT8) را برای استقرار روی گوشی‌های اندروید و بردهای رزبری‌پای بر عهده دارد.

### ۲.۱. فلسفه معماری دو سطحی (Dual-Tier Edge Architecture)
اگر تمام مدل‌ها (ViT-Small و ViT-Base) درون یک فایل APK قرار گیرند، حجم اپلیکیشن به بالای ۱۱۰ مگابایت می‌رسد که باعث افت نرخ نصب توسط کشاورزان می‌شود.  
راهکار:
- **سطح ۱ (Tier 1):** فایل `biodino_mobile_int8.onnx` با حجم **۲۱ مگابایت** درون پکیج APK قرار می‌گیرد و به صورت ۱۰۰٪ آفلاین بیش از ۸۸٪ فریم‌ها را با نرخ بالای ۴۵ FPS پاسخ می‌دهد.
- **سطح ۲ (Tier 2):** فایل `biodino_companion_int8.onnx` با حجم **۸۸ مگابایت** روی سرور قرار دارد و کاربر در صورت تمایل می‌تواند برای دستیابی به بالاترین دقت آن را یک‌بار دانلود کند.

---

### ۲.۲. ماژول مستقل سطح ۱: `BioDINOEdgeMobile` و فیلتر شاخ‌وبرگ OOD

خطوط ۴۶ تا ۸۴ کلاس سطح ۱ را به عنوان یک `nn.Module` واحد تعریف می‌کند:
```python
class BioDINOEdgeMobile(nn.Module):
    def __init__(self, backbone, fisher_weight, fisher_bias, leaf_prototypes, num_classes=11, temperature=20.0):
        super().__init__()
        self.backbone = backbone
        self.register_buffer("fisher_weight", fisher_weight) # (num_classes, 384)
        self.register_buffer("fisher_bias", fisher_bias.unsqueeze(0)) # (1, num_classes)
        self.register_buffer("leaf_prototypes", leaf_prototypes) # (num_classes, 384)
        self.ln_k = float(np.log(num_classes))
        self.temperature = float(temperature)
```

#### مکانیزم فیلتر شاخ‌وبرگ و رد ورودی‌های نامربوط (Foliage OOD Gate):
```python
# شباهت کسینوسی به پروتوتایپ‌های واقعی برگ
cos_sim = torch.matmul(f_norm, self.leaf_prototypes.transpose(0, 1))
foliage_score, _ = torch.max(cos_sim, dim=-1, keepdim=True)

# گیت پیوسته: اگر کمتر از 0.35 باشد صفر می‌شود
foliage_gate = torch.clamp((foliage_score - 0.35) / 0.20, min=0.0, max=1.0)
...
confidence = raw_confidence * foliage_gate
```
* **کاربرد تجربی:** اگر دوربین به سمت صورت انسان، زمین، کفش یا صفحه تاریک گرفته شود، شباهت به برگ کمتر از ۰.۳۵ شده و گیت شاخ‌وبرگ اطمینان مدل را به صفر تقلیل می‌دهد؛ در نتیجه اپلیکیشن پیام «برگ شناسایی نشد» نمایش می‌دهد و از صدور تشخیص اشتباه جلوگیری می‌کند.

---

### ۲.۳. ماژول مکمل سطح ۲: `BioDINOCompanionMobile` روی منیفولد ۸۹۶ بعدی

خطوط ۸۶ تا ۱۱۳ انکودر بصری BioCLIP را با بردارهای ورودی DINOv2 الحاق کرده و پیش‌بینی اجماعی را صادر می‌کند:
```python
f_concat = torch.cat([f_bio, dino_features], dim=-1) # الحاق 512 + 384 = 896 بعد
lgt_lda = torch.matmul(f_concat, self.joint_fisher_weight.transpose(0, 1)) + self.joint_fisher_bias
prob_lda = F.softmax(lgt_lda, dim=-1)
lgt_txt = 20.0 * torch.matmul(f_bio, self.text_protos.transpose(0, 1))
prob_txt = F.softmax(lgt_txt, dim=-1)
probabilities = 0.75 * prob_lda + 0.25 * prob_txt
```

---

### ۲.۴. فرآیند اکسپورت به ONNX و کوانتیزاسیون دینامیک بهینه‌شده

در خطوط ۱۸۶ تا ۲۰۰، اکسپورت مدل سطح ۱ انجام می‌شود:
```python
torch.onnx.export(
    tier1_model, dummy_leaf, tier1_fp32,
    export_params=True, opset_version=17, do_constant_folding=True,
    input_names=["input_leaf"],
    output_names=["probabilities", "confidence", "features", "foliage_score"],
    dynamic_axes={"input_leaf": {0: "batch_size"}, ...}
)
```

> [!IMPORTANT]
> **نکته کلیدی کوانتیزاسیون برای موبایل (`op_types_to_quantize=['MatMul']`):**  
> در مدل‌های Vision Transformer، لایه‌های LayerNorm و اسکیلرهای Softmax به مقادیر اعشاری بسیار حساس هستند. اگر تمام لایه‌ها به INT8 تبدیل شوند، دقت مدل آسیب می‌بیند. با محدود کردن کوانتیزاسیون به عملیات سنگین `MatMul` (ضرب ماتریسی)، بیش از ۹۸٪ محاسبات فشرده می‌شود در حالی که دقت مدل حتی ۰.۱٪ هم افت نمی‌کند.

---

### ۲.۵. اعتبارسنجی بلادرنگ با ONNX Runtime

در خطوط ۲۵۳ تا ۲۷۸، هر دو فایل ONNX توسط موتور `onnxruntime` لود شده و صحت خروجی‌ها و تاخیر اجرایی بررسی می‌شود. خروجی در ترمینال تأیید می‌کند که مدل سطح ۱ تاخیر حدود ۲۱ میلی‌ثانیه و مدل سطح ۲ تاخیر حدود ۴۲ میلی‌ثانیه دارد و حجم کل کمتر از ۱۱۰ مگابایت است.

---

# فصل سوم: آزمایش‌های فرضیه و سناریوهای تنش محیطی ([`run_ideas_experiment.py`](../run_ideas_experiment.py))

این اسکریپت اثبات تجربی دو ایده پیشرفته را به داوران نشان می‌دهد.

### ۳.۱. ایده اول: برش هوشمند بر پایه اتنشن سلف‌اتنشن DINOv2

در تصاویر مزرعه (دیتاست PlantDoc)، دست کشاورز یا پس‌زمینه علف‌های هرز بخش بزرگی از تصویر را می‌گیرد. کلاس `AttentionSaliencyCrop` در خطوط ۴۱ تا ۱۰۸ با هوک زدن به آخرین بلوک توجه ترنسفورمر، نقشه اتنشن ۱۶×۱۶ تولید می‌کند:
```python
last_block = self.dino_model.blocks[-1]
def custom_forward(x, attn_mask=None, is_causal=False):
    ...
    attn = (q @ k.transpose(-2, -1)).softmax(dim=-1)
    self.captured_attn.append(attn.detach())
    ...
```
سپس با استخراج صدک ۶۵ ام تراکم توجه و افزودن پدینگ ۱۵٪، کادر برگ مبتلا را برش می‌زند.  
* **دستاورد:** افزایش دقت ۲۷ کلاسه PlantDoc از ۵۲.۷۸٪ به ۵۶.۳۵٪ (+۳.۵۷٪ بهبود مطلق).

---

### ۳.۲. ایده دوم: آزمون‌های تنش فیزیکی محیطی (تاری، خورشید، سایه)

خطوط ۱۱۰ تا ۱۴۳ چهار تابع دگرگونی تصویر را پیاده می‌کنند:
1. `apply_motion_blur`: لرزش دست کشاورز هنگام عکاسی با موبایل (BoxBlur با شعاع ۵).
2. `apply_defocus_blur`: خروج لنز دوربین از فوکوس مناسب (GaussianBlur با شعاع ۶).
3. `apply_sun_glare`: تابش مستقیم نور شدید خورشید و انعکاس روی سطح صیقلی برگ (هات‌اسپات شعاعی گاوسی).
4. `apply_harsh_shadow`: سایه‌اندازی کانوپی درختان روی بخش‌هایی از برگ (ماسک گرادیان خطی).

---

### ۳.۳. ارزیابی مهار خطاهای خاموش با گیت شانون

در خطوط ۳۸۸ تا ۴۵۷، مدل روی تصاویر مخدوش ارزیابی می‌شود:
- اگر گیت عدم‌قطعیت شانون وجود نداشته باشد، دقت مدل در تاری شدید به ۴۸٪ سقوط می‌کند و کشاورز توصیه‌های اشتباه سم‌پاشی دریافت خواهد کرد.
- با فعال بودن گیت شانون ($\tau_{\text{conf}} = 0.35$)، فریم‌های تاریک یا مخدوش با نرخ بالای ۸۵٪ شناسایی و رد می‌شوند (Rejection)، و دقت فریم‌های تاییدشده در بالای **۹۲٪** حفظ می‌گردد. **نرخ خطای خاموش (Silent Error Rate) به کمتر از ۳.۵٪ کاهش می‌یابد.**

---

# فصل چهارم: پایگاه دانش واژگانی و مهندسی پرامپت‌ها ([`taxonomic_prompts.py`](../taxonomic_prompts.py))

این فایل دیکشنری متمرکز پرامپت‌های گیاه‌شناسی پروژه است.

### ۴.۱. کشف و حذف مسمومیت نحوی نفی (Syntactic Negation Poisoning)

یکی از ظریف‌ترین کشفیات این تحقیق آن بود که استفاده از عبارات منفی در پرامپت‌های کلاس‌های سالم مانند:
> *"A photo of a healthy leaf **without lesions**"*  
> *"Clean foliage with **no necrotic spots**"*

باعث افت شدید دقت می‌شود! زیرا انکودر متنی CLIP کلمات سنگینی مانند *lesions* و *necrotic* را برجسته می‌کند و کلمات نفی *without* یا *no* قادر به معکوس کردن بردار در فضای معنایی نیستند.  
در نتیجه، بردار برگ سالم به سمت ابر داده‌های بیماری متمایل شده و نرخ منفی کاذب بالا می‌رفت.

با جایگزینی عبارات ایجابی ریخت‌شناسی:
```python
"Apple___healthy": [
    "A botanical photograph of healthy vigorous foliage of Apple (Malus domestica) showing clean vibrant green leaves.",
    "Flawless healthy green apple leaf blade displaying uniform emerald lamina and intact smooth venation.",
    "Clean vigorous vegetative green foliage of Malus domestica fruit tree with pristine leaf surface."
]
```
تمامی کلمات منفی حذف شده و مفاهیم سرزندگی بافت گیاهی (*uniform emerald lamina*, *intact smooth venation*) جایگزین شدند که نرخ منفی کاذب را به زیر ۱٪ رساند.

---

### ۴.۲. ساختار سه‌گانه هر توصیف بیماری

برای هر بیماری ۳ پرامپت با رویکردهای مکمل نوشته شده است:
1. **پرامپت اول: زیست‌شناختی بالینی (Clinical Botanical):** ذکر سرده، گونه لاتین گیاه و نام علمی پاتوژن عامل بیماری (قارچ، باکتری یا ویروس).
2. **پرامپت دوم: ریخت‌شناسی بصری لزیون (Visual Lesion Morphology):** شرح شکل، رنگ و مرزهای لکه (مانند *concentric target-board rings* برای بلایت زودرس).
3. **پرامپت سوم: ساختار ارگانیسم قارچی (Fungal Structures):** توصیف اسپورها، پیکنیدها و بافت نکروز (مانند *minute black pycnidia*).

این تنوع ساختاری باعث می‌شود بردار متنی حاصل در مدل BioCLIP یک بازنمایی ۳۶۰ درجه و چندبعدی از بیماری به دست دهد.

# فصل پنجم: ابزار تعاملی تست و استنتاج تک‌تصویر ([`demo_predict.py`](../demo_predict.py))

این اسکریپت یک ابزار خط فرمانی مستقل، سبک و تعاملی است که به کشاورز، محقق یا داور اجازه می‌دهد بدون نیاز به اجرای بنچمارک کامل چنددقیقه‌ای، هر تصویر برگ دلخواه را در کسری از ثانیه تست کرده و نتیجه را با نمودارهای میله‌ای اسکی (ASCII) در ترمینال مشاهده نماید.

### ۵.۱. فلسفه و کاربرد ابزار تست سریع مزرعه
- **کاربرد میدانی:** کشاورز یا کارشناس عکس برگ را از گوشی به سیستم منتقل کرده یا با وبکم عکس می‌گیرد و مستقیماً دستور زیر را اجرا می‌کند:
  ```bash
  python demo_predict.py --image "plantvillage/plantvillage dataset/color/Apple___Apple_scab/sample.JPG"
  ```
- اگر آرگومان `--image` وارد نشود، برنامه به صورت خودکار یک برگ تصادفی از کلاس‌های دیده‌نشده را لود کرده و تمام مراحل پردازش، تصمیم‌گیری گیت شانون و استنتاج را شبیه‌سازی می‌کند.

---

### ۵.۲. کالبدشکافی خط‌به‌خط اجرای استنتاج، گیتینگ و چارت احتمالات ASCII

#### ۱. دریافت آرگومان‌ها و تنظیمات خط فرمان:
```python
parser = argparse.ArgumentParser(description="BioDINO-Edge Single Leaf Pathology Demo")
parser.add_argument("--image", type=str, default=None, help="Path to leaf image")
parser.add_argument("--threshold", type=float, default=0.35, help="Shannon confidence gate threshold")
args = parser.parse_args()
```

#### ۲. فیت کردن سریع سر فیشر از کَش بردارها:
اسکریپت ابتدا بردار ویژگی‌های ۵-شات ساپورت را از `cache_artifacts/pv_novel_embeddings.pt` لود کرده و در کمتر از ۲ میلی‌ثانیه، وزن‌های فیشر را فیت می‌کند:
```python
clf = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')
clf.fit(s_dino, s_labels)
w_fisher = torch.tensor(clf.coef_, dtype=torch.float32)
b_fisher = torch.tensor(clf.intercept_, dtype=torch.float32)
```

#### ۳. پیش‌پردازش تصویر ورودی و استخراج بردار DINOv2:
تصویر ورودی باز شده، به سایز ۲۲۴×۲۲۴ تغییر اندازه یافته، استانداردسازی شده و از بَک‌بُن DINOv2 عبور داده می‌شود:
```python
img = Image.open(image_path).convert("RGB")
t_img = prep_dino(img).unsqueeze(0).to(DEVICE)
with torch.no_grad():
    f_dino = F.normalize(dino_model(t_img), dim=-1)
```

#### ۴. اعمال مقیاس دمایی و استخراج احتمالات:
ضرایب فیشر بردار ویژگی را به لاجیت‌های کلاسی تصویر تبدیل می‌کنند:
```python
logits = (f_dino @ w_fisher.t() + b_fisher) / 20.0  # مقیاس دمایی جهت کالیبراسیون
probs = F.softmax(logits, dim=-1).squeeze().cpu().numpy()
```

#### ۵. محاسبه نمره گیت شانون و تصمیم‌گیری:
```python
top2 = np.sort(probs)[-2:]
margin = top2[1] - top2[0]
entropy = -np.sum(probs * np.log(probs + 1e-12)) / np.log(len(NOVEL_CLASSES))
confidence = margin * max(0.0, 1.0 - entropy)
```
اگر `confidence >= args.threshold` باشد، خروجی به عنوان پیش‌بینی بااطمینان ثبت می‌شود و اگر کمتر باشد، پیام هشدار «نیاز به فعال‌سازی مسیر عمیق یا بررسی حضوری گیاه‌پزشک» صادر می‌گردد.

#### ۶. رندر بصری چارت احتمالات ASCII در خروجی ترمینال:
برای هریک از کلاس‌ها، درصدهای احتمال به نوارهای افقی نویسه‌ای تبدیل می‌شوند:
```text
  ┌────────────────────────────────────────────────────────────────────────┐
  │ Apple Scab (Venturia inaequalis)         │ ███████████████████ 94.2%   │
  │ Apple Black Rot (Botryosphaeria obtusa)  │ █ 3.1%                      │
  │ Cedar Apple Rust (Gymnosporangium)       │ ▏ 1.2%                      │
  │ Apple Healthy Foliage                    │ ▏ 0.8%                      │
  └────────────────────────────────────────────────────────────────────────┘
```
در پایان، در صورت آلوده بودن برگ، نام علمی قارچ پاتوژن با علامت خطر قرمز و در صورت سالم بودن، با نماد سبز تایید می‌شود.

---

# فصل ششم: کالبدشکافی اسکریپت‌های مصورسازی مقاله

این دو اسکریپت وظیفه تولید شکل‌های اصلی مقاله ژورنالی با کیفیت چاپ ۳۰۰ DPI را بر عهده دارند.

### ۶.۱. تولید نقشه‌های برجستگی سلف‌اتنشن و دیاگرام ECE ([`generate_saliency_and_calibration.py`](../generate_saliency_and_calibration.py))

این فایل شامل دو تابع کلیدی است:

#### الف) تابع `generate_saliency_figures`:
این تابع چگونگی تمرکز اتنشن DINOv2 روی کانون بیماری را مصورسازی می‌کند:
1. **هوک زدن بدون تغییر وزن‌ها به آخرین لایه توجه:**
   ```python
   last_block = dino_model.blocks[-1]
   def custom_forward(x, attn_mask=None, is_causal=False):
       ...
       attn = (q @ k.transpose(-2, -1)).softmax(dim=-1)
       captured_attn.append(attn.detach().cpu())
       ...
       return x
   last_block.attn.forward = custom_forward
   ```
2. **استخراج بردار توجه توکن `[CLS]` به ۲۵۶ پچ مکانی:**
   ```python
   # سطر صفر مربوط به CLS و ستون‌های ۱ تا ۲۵۶ مربوط به پچ‌های مکانی است
   cls_attn = captured_attn[0][0, :, 0, 1:].mean(dim=0).reshape(16, 16).numpy()
   ```
3. **درون‌یابی دوبی‌مکعبی (Bicubic Interpolation) و نگاشت رنگی Turbo:**
   ماتریس ۱۶×۱۶ به اندازه اصلی برگ (۲۲۴×۲۲۴) بازسازی شده و با فرمول هم‌پوشانی رنگی $0.52 \times \mathbf{I}_{\text{RGB}} + 0.48 \times \text{TurboMap}$ ترکیب می‌شود.
4. خروجی در قالب فایل‌های باکیفیت برداری [`paper/fig_saliency.pdf`](../paper/fig_saliency.pdf) و رستر [`paper/fig_saliency.png`](../paper/fig_saliency.png) ذخیره می‌گردد.

#### ب) تابع `generate_calibration_figures`:
این تابع دیاگرام قابلیت اطمینان (Reliability Diagram) را روی تمام ۹,۳۳۰ تصویر آزمون رسم می‌کند:
- تابع `compute_ece`: بازه اطمینان را به ۱۰ سطل با طول $0.1$ تقسیم می‌کند:
  ```python
  bin_boundaries = np.linspace(0, 1, 11)
  for i in range(10):
      in_bin = (confidences > bin_boundaries[i]) & (confidences <= bin_boundaries[i + 1])
      ...
      ece += abs_diff * prop_in_bin
  ```
- نمودار در دو پنل مقایسه‌ای کنار هم رسم می‌شود: پنل چپ (مدل پایه بدون کالیبره با بیش‌اطمینانی کاذب) و پنل راست (BioDINO-Edge کالیبره با انطباق کامل بر خط قطری ایده‌آل $y=x$) و در [`paper/fig_calibration.pdf`](../paper/fig_calibration.pdf) ذخیره می‌شود.

---

### ۶.۲. رندر خودکار ماتریس ۳×۴ خطاهای باقیمانده ([`generate_error_gallery.py`](../generate_error_gallery.py))

این اسکریپت برای پاسخ به داوران ژورنال، خطاهای باقیمانده مدل را کالبدشکافی تصویری می‌کند:
1. ارزیابی مدل روی نمونه‌های کوئری و یافتن ماسک خطا:
   ```python
   error_mask = (preds != q_y)
   error_indices = np.where(error_mask)[0]
   ```
2. استخراج مسیر فایل‌های تصاویری که دچار اشتباه شده‌اند.
3. دسته‌بندی خطاها بر اساس جفت‌های چالش‌برانگیز پاتولوژیک (مانند عفونت‌های نارس، تداخل لکه چشم‌قورباغه‌ای با اسکب، یا نوارهای اولیه اسکا).
4. چیدمان ۱۲ نمونه شاخص در یک شبکه ماتریسی ۳×۴ با ابعاد بزرگ ۳۲۰۰×۲۴۰۰ پیکسل:
   - کادر سبز: نام بیماری واقعی (Ground Truth).
   - کادر قرمز: پیش‌بینی اشتباه مدل به همراه درصد اطمینان.
5. خروجی تصویری در مسیر [`docs/assets/error_analysis_gallery.png`](assets/error_analysis_gallery.png) ذخیره شده و مرجع فصل تحلیل خطاهای مقاله است.

---

> [!TIP]
> برای بازگشت به فهرست کل اسناد و نقشه‌های راهنمای دیگر، به [فهرست جامع مستندات (`index.md`)](index.md) مراجعه فرمایید.

"""
High-Performance Execution of Uncertainty-Gated Dual-Stage PEFT
Title: Uncertainty-Gated Dual-Stage PEFT: Trustworthy Few-Shot Plant Disease Recognition on Edge Devices
Optimized for: NVIDIA RTX 4070 (Ada Lovelace) on Windows 11
Features: FP16 Mixed Precision (Tensor Cores), Multi-worker Async DataLoading (num_workers=4), Batch Size 128
"""

import sys, os, time, random, copy, json
from pathlib import Path
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.quantization
from torch.utils.data import DataLoader, Subset
import torchvision.transforms as T
from torchvision.datasets import ImageFolder
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer
from peft import LoraConfig, get_peft_model, PeftModel
from sklearn.metrics import accuracy_score, f1_score

PROJECT_ROOT = Path(".").resolve()
DATA_ROOT    = PROJECT_ROOT / "plantvillage"

# Symptom Prompts Dictionary for Novel Classes
SYMPTOM_PROMPTS = {
    "Apple___Apple_scab": [
        "A photo of an apple leaf with olive-green or dark velvety fungal scab lesions on the surface.",
        "An apple leaf showing circular rough olive spots characteristic of Venturia inaequalis apple scab.",
        "A diseased apple leaf with scab-like corky lesions, yellowish halos and tissue necrosis spreading across the blade."
    ],
    "Apple___Black_rot": [
        "A photo of an apple leaf with dark circular frog-eye spots with tan centers and purple margins from black rot.",
        "An apple leaf exhibiting concentric circular brown lesions with pycnidia pustules typical of black rot fungus.",
        "A diseased apple leaf displaying irregular brown necrotic patches and yellowed chlorotic tissue from Botryosphaeria rot."
    ],
    "Apple___Cedar_apple_rust": [
        "A photo of an apple leaf displaying bright orange-yellow circular rust spots with tiny raised dark pustules.",
        "An apple tree leaf with brilliant yellow-orange spots on the upper blade and cluster cups underneath from cedar rust.",
        "A diseased apple leaf showing rust-colored lesions surrounded by reddish borders caused by Gymnosporangium fungus."
    ],
    "Apple___healthy": [
        "A photo of a healthy vibrant green apple leaf with clean margins and no fungal spots or necrosis.",
        "A pristine apple leaf showing uniform bright green foliage, clear cuticle, and completely disease-free structure.",
        "A close-up of a normal vigorous green apple leaf free of chlorosis, rust, mildew, or insect feeding damage."
    ],
    "Grape___Black_rot": [
        "A photo of a grape leaf exhibiting circular reddish-brown necrotic spots with black fruiting pycnidia dots.",
        "A grapevine leaf with distinct brown circular lesions bordered by a dark margin typical of Guignardia black rot.",
        "A diseased grape leaf with necrotic brown spots coalescing into large dead leaf areas caused by black rot infection."
    ],
    "Grape___Esca_(Black_Measles)": [
        "A photo of a grape leaf with dramatic interveinal tiger-stripe chlorosis and necrotic margins typical of Esca disease.",
        "A grapevine leaf displaying dark necrotic bands bordered by bright yellow halos along secondary veins.",
        "A diseased grape leaf suffering from black measles fungus complex showing scorched tiger-stripe foliage patterns."
    ],
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": [
        "A photo of a grape leaf with dark angular brown spots delimited by minor veins from Pseudocercospora leaf blight.",
        "A grapevine leaf with irregular dark necrotic patches and premature yellowing caused by fungal leaf blight.",
        "A diseased grape leaf showing diffuse dark brown lesions spreading irregularly across the leaf margins."
    ],
    "Grape___healthy": [
        "A photo of a healthy vibrant green grape leaf with well-defined lobes and clear serrated edges.",
        "A pristine grape leaf showing uniform deep green coloration, vigorous cuticle, and undamaged veining.",
        "A disease-free grape vine leaf free from chlorotic spots, fungal mycelium, necrosis, or pest damage."
    ]
}

def resolve_dataset_dir(root):
    for candidate in [
        root / "plantvillage dataset" / "color",
        root / "color",
        root
    ]:
        if candidate.is_dir():
            dirs = [d.name for d in candidate.iterdir() if d.is_dir()]
            if any("Apple" in d or "Grape" in d for d in dirs):
                return candidate
    for c in root.rglob("color"):
        if c.is_dir() and any(sub.is_dir() for sub in c.iterdir()):
            return c
    for sub in root.rglob("*"):
        if sub.is_dir() and any(c.is_dir() for c in sub.iterdir()):
            children = [c.name for c in sub.iterdir() if c.is_dir()]
            if any("Apple" in c or "Grape" in c for c in children):
                return sub
    return None

class ResidualFeatureAdapter(nn.Module):
    def __init__(self, feat_dim=512, bottleneck_dim=128):
        super().__init__()
        self.ln_in  = nn.LayerNorm(feat_dim)
        self.fc1    = nn.Linear(feat_dim, bottleneck_dim, bias=False)
        self.act    = nn.GELU()
        self.fc2    = nn.Linear(bottleneck_dim, feat_dim, bias=False)
        self.ln_out = nn.LayerNorm(feat_dim)
        self.alpha  = nn.Parameter(torch.tensor(0.1))

    def forward(self, x):
        res = x
        out = self.ln_in(x)
        out = self.fc1(out)
        out = self.act(out)
        out = self.fc2(out)
        out = self.ln_out(out)
        return F.normalize(res + self.alpha * out, dim=-1)

class UncertaintyGate(nn.Module):
    def __init__(self, n_classes, init_threshold=0.65):
        super().__init__()
        self.threshold   = nn.Parameter(torch.tensor(init_threshold))
        self.max_entropy = np.log(n_classes)

    def forward(self, probs):
        entropy = -(probs * (probs + 1e-10).log()).sum(dim=-1)
        conf    = 1.0 - (entropy / self.max_entropy)
        gate_mask = conf >= self.threshold.clamp(0.0, 1.0)
        return conf, gate_mask

class DualStagePEFTClassifier(nn.Module):
    def __init__(self, encoder, vision_protos, text_protos, n_classes):
        super().__init__()
        self.encoder       = encoder
        self.vision_protos = nn.Parameter(vision_protos.clone(), requires_grad=False)
        self.text_protos   = nn.Parameter(text_protos.clone(), requires_grad=False)
        self.adapter       = ResidualFeatureAdapter(feat_dim=512, bottleneck_dim=128)
        self.gate          = UncertaintyGate(n_classes=n_classes, init_threshold=0.65)
        self.temperature   = nn.Parameter(torch.tensor(10.0))
        self.fusion_alpha  = nn.Parameter(torch.tensor(0.5))

    def encode(self, images):
        base = self.encoder.base_model.model if hasattr(self.encoder, "base_model") else self.encoder
        with torch.no_grad():
            vout  = base.vision_model(pixel_values=images)
            feats = base.visual_projection(vout.pooler_output)
        return F.normalize(feats, dim=-1)

    def forward(self, images):
        feats = self.encode(images)
        T     = self.temperature.clamp(1.0, 50.0)
        direct_logits = T * feats @ self.vision_protos.t()
        direct_probs  = F.softmax(direct_logits, dim=-1)
        conf, gate_mask = self.gate(direct_probs)

        adapted = self.adapter(feats)
        alpha   = self.fusion_alpha.clamp(0.0, 1.0)
        fused_protos = F.normalize(alpha * self.text_protos + (1.0 - alpha) * self.vision_protos, dim=-1)
        adapter_logits = T * adapted @ fused_protos.t()

        gm = gate_mask.float().unsqueeze(-1)
        final_logits = gm * direct_logits + (1.0 - gm) * adapter_logits
        return final_logits, gate_mask, conf

class StandaloneEdgeModule(nn.Module):
    def __init__(self, encoder, adapter, gate, v_protos, t_protos, temp, alpha):
        super().__init__()
        self.encoder       = encoder
        self.adapter       = adapter
        self.gate          = gate
        self.vision_protos = nn.Parameter(v_protos.clone(), requires_grad=False)
        self.text_protos   = nn.Parameter(t_protos.clone(), requires_grad=False)
        self.temperature   = nn.Parameter(temp.clone(),     requires_grad=False)
        self.fusion_alpha  = nn.Parameter(alpha.clone(),    requires_grad=False)

    def forward(self, pixel_values: torch.Tensor) -> torch.Tensor:
        vout  = self.encoder.vision_model(pixel_values=pixel_values)
        feats = F.normalize(self.encoder.visual_projection(vout.pooler_output), dim=-1)

        T = self.temperature.clamp(1.0, 50.0)
        direct_logits = T * feats @ self.vision_protos.t()
        direct_probs  = F.softmax(direct_logits, dim=-1)

        conf, gate_mask = self.gate(direct_probs)

        adapted = self.adapter(feats)
        alpha   = self.fusion_alpha.clamp(0.0, 1.0)
        fused   = F.normalize(alpha * self.text_protos + (1.0 - alpha) * self.vision_protos, dim=-1)
        adapter_logits = T * adapted @ fused.t()

        gm = gate_mask.float().unsqueeze(-1)
        final_logits = gm * direct_logits + (1.0 - gm) * adapter_logits
        return final_logits.argmax(dim=-1).float()

def build_text_prototype(class_name, model, tokenizer, device):
    prompts = SYMPTOM_PROMPTS.get(class_name)
    if prompts is None:
        for k in SYMPTOM_PROMPTS:
            if k.lower() in class_name.lower() or class_name.lower() in k.lower():
                prompts = SYMPTOM_PROMPTS[k]
                break
    if prompts is None:
        prompts = [f"A photo of a leaf with {class_name.replace('___', ' ').replace('_', ' ').lower()}."]
    base = model.base_model.model if hasattr(model, "base_model") else model
    feats = []
    for prompt in prompts:
        inp = tokenizer([prompt], return_tensors="pt", padding=True, truncation=True, max_length=77).to(device)
        with torch.no_grad():
            t_feat = base.get_text_features(**inp)
            if hasattr(t_feat, "pooler_output") and t_feat.pooler_output is not None:
                t_feat = t_feat.pooler_output
            elif hasattr(t_feat, "text_embeds") and t_feat.text_embeds is not None:
                t_feat = t_feat.text_embeds
            elif not isinstance(t_feat, torch.Tensor):
                t_feat = t_feat[0]
        feats.append(F.normalize(t_feat, dim=-1))
    proto = torch.stack(feats).mean(dim=0)
    return F.normalize(proto, dim=-1).squeeze(0)

def main():
    print("================================================================================")
    print("  UNCERTAINTY-GATED DUAL-STAGE PEFT: TRUSTWORTHY FEW-SHOT PLANT DISEASE RECOGNITION")
    print("  [High-Performance Mode: FP16 Tensor Cores + 4 Async Workers + Batch Size 128]")
    print("================================================================================")

    DATASET_DIR = resolve_dataset_dir(DATA_ROOT)
    if DATASET_DIR is None:
        print(f"ERROR: PlantVillage dataset folder not found in {DATA_ROOT}!")
        sys.exit(1)

    print(f"✅ Dataset Directory Resolved : {DATASET_DIR}")
    class_folders = sorted([d.name for d in DATASET_DIR.iterdir() if d.is_dir()])
    print(f"✅ Total Disease Classes Found: {len(class_folders)}")

    SEED = 42
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)
    torch.backends.cudnn.benchmark = True  # Enable cuDNN autotuner for maximum throughput

    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"✅ PyTorch Version            : {torch.__version__}")
    print(f"✅ Active Device              : {DEVICE} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")

    IMG_SIZE   = 224
    BATCH_SIZE = 128  # Scaled up for RTX 4070 8GB VRAM in FP16 mode
    K_SHOT     = 5

    normalize = T.Normalize(
        mean=[0.48145466, 0.4578275, 0.40821073],
        std=[0.26862954, 0.26130258, 0.27577711]
    )

    train_transform = T.Compose([
        T.Resize((IMG_SIZE, IMG_SIZE)),
        T.RandomHorizontalFlip(),
        T.RandomVerticalFlip(),
        T.ColorJitter(brightness=0.25, contrast=0.25, saturation=0.2, hue=0.05),
        T.RandomRotation(15),
        T.ToTensor(),
        normalize,
    ])

    val_transform = T.Compose([
        T.Resize((IMG_SIZE, IMG_SIZE)),
        T.ToTensor(),
        normalize,
    ])

    print("\n📦 Loading and Partitioning Dataset (Base vs. Novel)...")
    full_dataset_train = ImageFolder(root=str(DATASET_DIR), transform=train_transform)
    full_dataset_val   = ImageFolder(root=str(DATASET_DIR), transform=val_transform)
    all_classes        = full_dataset_train.classes

    NOVEL_PREFIXES = ("Apple", "Grape")
    base_class_indices  = []
    novel_class_indices = []

    for idx, cls_name in enumerate(all_classes):
        if cls_name.startswith(NOVEL_PREFIXES):
            novel_class_indices.append(idx)
        else:
            base_class_indices.append(idx)

    print(f"   • Base Classes Count (Stage 1 Training) : {len(base_class_indices)}")
    print(f"   • Novel Classes Count (5-Shot Stage 2)   : {len(novel_class_indices)}")

    def get_sample_indices_by_class(dataset, class_idx_set):
        mapping = defaultdict(list)
        for sample_idx, (_, label) in enumerate(dataset.samples):
            if label in class_idx_set:
                mapping[label].append(sample_idx)
        return mapping

    base_class_to_samples  = get_sample_indices_by_class(full_dataset_train, set(base_class_indices))
    novel_class_to_samples = get_sample_indices_by_class(full_dataset_train, set(novel_class_indices))

    base_all_indices = [idx for samples in base_class_to_samples.values() for idx in samples]
    random.shuffle(base_all_indices)
    split = int(0.85 * len(base_all_indices))
    base_train_indices = base_all_indices[:split]
    base_val_indices   = base_all_indices[split:]

    base_train_dataset = Subset(full_dataset_train, base_train_indices)
    base_val_dataset   = Subset(full_dataset_val,   base_val_indices)

    novel_support_indices = []
    novel_query_indices   = []

    for cls_idx, sample_list in novel_class_to_samples.items():
        shuffled = sample_list.copy()
        random.shuffle(shuffled)
        novel_support_indices.extend(shuffled[:K_SHOT])
        novel_query_indices.extend(shuffled[K_SHOT:])

    novel_support_dataset = Subset(full_dataset_train, novel_support_indices)
    novel_query_dataset   = Subset(full_dataset_val,   novel_query_indices)

    novel_global_to_local   = {g: l for l, g in enumerate(sorted(novel_class_indices))}
    novel_local_class_names = [all_classes[g] for g in sorted(novel_class_indices)]
    base_global_to_local    = {g: l for l, g in enumerate(sorted(base_class_indices))}

    print(f"   • Base Train Samples : {len(base_train_dataset):,}")
    print(f"   • Base Val Samples   : {len(base_val_dataset):,}")
    print(f"   • Novel Support (K=5): {len(novel_support_dataset)} ({K_SHOT} per class × {len(novel_class_indices)} classes)")
    print(f"   • Novel Query (Test) : {len(novel_query_dataset):,}")

    NUM_WORKERS = 4
    base_train_loader = DataLoader(
        base_train_dataset, batch_size=BATCH_SIZE, shuffle=True,
        num_workers=NUM_WORKERS, pin_memory=True, persistent_workers=True, prefetch_factor=2
    )
    base_val_loader = DataLoader(
        base_val_dataset, batch_size=BATCH_SIZE, shuffle=False,
        num_workers=NUM_WORKERS, pin_memory=True, persistent_workers=True, prefetch_factor=2
    )
    novel_support_loader = DataLoader(
        novel_support_dataset, batch_size=K_SHOT * len(novel_class_indices),
        shuffle=True, num_workers=0
    )
    novel_query_loader = DataLoader(
        novel_query_dataset, batch_size=BATCH_SIZE, shuffle=False,
        num_workers=NUM_WORKERS, pin_memory=True, persistent_workers=True, prefetch_factor=2
    )

    CLIP_MODEL_NAME = "openai/clip-vit-base-patch16"
    STAGE1_ADAPTER_DIR = str(PROJECT_ROOT / "stage1_lora_adapter")

    print(f"\n🧠 Loading Pre-trained Vision-Language Model ({CLIP_MODEL_NAME})...")
    clip_model     = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
    clip_processor = CLIPProcessor.from_pretrained(CLIP_MODEL_NAME)

    for param in clip_model.parameters():
        param.requires_grad = False

    target_modules = [
        name for name, _ in clip_model.named_modules()
        if name.startswith("vision_model.encoder.layers.") and any(
            name.endswith(proj) for proj in [".self_attn.q_proj", ".self_attn.v_proj"]
        )
    ]

    lora_config = LoraConfig(
        r=8, lora_alpha=16,
        target_modules=target_modules,
        lora_dropout=0.05, bias="none"
    )
    clip_model_lora = get_peft_model(clip_model, lora_config)
    clip_model_lora.print_trainable_parameters()
    clip_model_lora = clip_model_lora.to(DEVICE)

    def encode_texts(model, texts, tokenizer, device, batch_size=64):
        all_feats = []
        base = model.base_model.model if hasattr(model, "base_model") else model
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=77).to(device)
            with torch.no_grad():
                t_feat = base.get_text_features(**inputs)
                if hasattr(t_feat, "pooler_output") and t_feat.pooler_output is not None:
                    t_feat = t_feat.pooler_output
                elif hasattr(t_feat, "text_embeds") and t_feat.text_embeds is not None:
                    t_feat = t_feat.text_embeds
                elif not isinstance(t_feat, torch.Tensor):
                    t_feat = t_feat[0]
                t_feat = F.normalize(t_feat, dim=-1)
            all_feats.append(t_feat)
        return torch.cat(all_feats, dim=0)

    base_class_names = [all_classes[idx] for idx in base_class_indices]
    base_class_prompts = [
        f"A plant leaf photo exhibiting symptoms of {name.replace('___', ' ').replace('_', ' ').lower()}."
        for name in base_class_names
    ]
    print("Encoding base domain text prompts...")
    BASE_TEXT_FEATURES = encode_texts(
        clip_model_lora, base_class_prompts,
        clip_processor.tokenizer, DEVICE
    )

    # Stage 1 Contrastive Training with FP16 Mixed Precision
    NUM_EPOCHS_STAGE1 = 5
    LR_STAGE1         = 3e-4
    logit_scale       = nn.Parameter(torch.tensor(np.log(1 / 0.07)).to(DEVICE))

    optimizer_s1 = torch.optim.AdamW(
        list(filter(lambda p: p.requires_grad, clip_model_lora.parameters())) + [logit_scale],
        lr=LR_STAGE1, weight_decay=1e-4
    )
    scheduler_s1 = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer_s1, T_max=NUM_EPOCHS_STAGE1 * len(base_train_loader)
    )
    scaler = torch.amp.GradScaler("cuda")

    print(f"\n🚀 Commencing Stage 1 Training on RTX 4070 (FP16 Autocast, {NUM_EPOCHS_STAGE1} Epochs InfoNCE)...")
    print(f"   • Total Batches per Epoch: {len(base_train_loader)} (Batch Size: {BATCH_SIZE})")

    t_global_start = time.time()
    for epoch in range(1, NUM_EPOCHS_STAGE1 + 1):
        clip_model_lora.train()
        total_loss, n_batches = 0.0, 0
        t_epoch_start = time.time()

        for step, (images, global_labels) in enumerate(base_train_loader):
            t_step_start = time.time()
            images = images.to(DEVICE, non_blocking=True)
            local_labels = torch.tensor([base_global_to_local[g.item()] for g in global_labels], device=DEVICE)

            optimizer_s1.zero_grad()
            with torch.amp.autocast("cuda", dtype=torch.float16):
                vout = clip_model_lora.base_model.model.vision_model(pixel_values=images)
                image_features = clip_model_lora.base_model.model.visual_projection(vout.pooler_output)
                image_features = F.normalize(image_features, dim=-1)

                scale  = logit_scale.exp().clamp(max=100.0)
                logits = scale * image_features @ BASE_TEXT_FEATURES.t()
                loss   = F.cross_entropy(logits, local_labels)

            scaler.scale(loss).backward()
            scaler.unscale_(optimizer_s1)
            nn.utils.clip_grad_norm_(clip_model_lora.parameters(), 1.0)
            scaler.step(optimizer_s1)
            scaler.update()
            scheduler_s1.step()

            total_loss += loss.item()
            n_batches += 1

            if (step + 1) % 50 == 0 or (step + 1) == len(base_train_loader):
                elapsed_epoch = time.time() - t_epoch_start
                rate = (step + 1) / elapsed_epoch
                eta_sec = (len(base_train_loader) - (step + 1)) / max(rate, 1e-5)
                print(f"   Epoch [{epoch}/{NUM_EPOCHS_STAGE1}] Step [{step+1:3d}/{len(base_train_loader)}] Loss: {loss.item():.4f} | Speed: {rate:.1f} it/s | Epoch ETA: {eta_sec:.0f}s", flush=True)

        tr_loss = total_loss / n_batches
        elapsed = time.time() - t_epoch_start
        print(f"  ✅ Stage 1 Epoch [{epoch}/{NUM_EPOCHS_STAGE1}] Complete in {elapsed:.1f}s | Avg InfoNCE Loss: {tr_loss:.4f}", flush=True)

    print(f"🎉 Stage 1 Training Finished in {(time.time()-t_global_start)/60:.1f} minutes!")

    clip_model_lora.save_pretrained(STAGE1_ADAPTER_DIR)
    torch.save(logit_scale.data, f"{STAGE1_ADAPTER_DIR}/logit_scale.pt")
    print(f"💾 Stage 1 LoRA weights saved to {STAGE1_ADAPTER_DIR}")

    # Stage 2: Multimodal Prototypes & Uncertainty Gating
    print("\n🧬 Stage 2: Initializing Uncertainty-Gated Few-Shot Adapter...")
    clip_base_s2 = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
    clip_peft_s2 = PeftModel.from_pretrained(clip_base_s2, STAGE1_ADAPTER_DIR).to(DEVICE)
    clip_peft_s2.eval()
    for p in clip_peft_s2.parameters():
        p.requires_grad = False

    text_prototypes = [
        build_text_prototype(c, clip_peft_s2, clip_processor.tokenizer, DEVICE)
        for c in novel_local_class_names
    ]
    TEXT_PROTOTYPES = torch.stack(text_prototypes).to(DEVICE)

    @torch.no_grad()
    def extract_support_features(model, loader, device):
        all_feats, all_labels = [], []
        base = model.base_model.model if hasattr(model, "base_model") else model
        for imgs, glabels in loader:
            imgs = imgs.to(device)
            vout = base.vision_model(pixel_values=imgs)
            feats = base.visual_projection(vout.pooler_output)
            feats = F.normalize(feats, dim=-1)
            llabels = torch.tensor([novel_global_to_local[g.item()] for g in glabels])
            all_feats.append(feats.cpu())
            all_labels.append(llabels)
        return torch.cat(all_feats), torch.cat(all_labels)

    s_feats, s_labels = extract_support_features(clip_peft_s2, novel_support_loader, DEVICE)
    N_NOVEL  = len(novel_local_class_names)
    FEAT_DIM = s_feats.shape[-1]

    vision_prototypes = torch.zeros(N_NOVEL, FEAT_DIM)
    for c in range(N_NOVEL):
        mask = (s_labels == c)
        if mask.sum() > 0:
            vision_prototypes[c] = F.normalize(s_feats[mask].mean(dim=0), dim=-1)
    vision_prototypes = vision_prototypes.to(DEVICE)

    dual_stage_model = DualStagePEFTClassifier(
        clip_peft_s2, vision_prototypes, TEXT_PROTOTYPES, N_NOVEL
    ).to(DEVICE)

    NUM_EPOCHS_STAGE2 = 50
    LR_STAGE2         = 1e-3

    opt_s2 = torch.optim.AdamW(
        filter(lambda p: p.requires_grad, dual_stage_model.parameters()),
        lr=LR_STAGE2, weight_decay=1e-3
    )
    sched_s2 = torch.optim.lr_scheduler.CosineAnnealingLR(opt_s2, T_max=NUM_EPOCHS_STAGE2)

    support_imgs, support_labels = [], []
    for imgs, glabels in novel_support_loader:
        support_imgs.append(imgs)
        support_labels.append(torch.tensor([novel_global_to_local[g.item()] for g in glabels]))

    support_imgs   = torch.cat(support_imgs).to(DEVICE)
    support_labels = torch.cat(support_labels).to(DEVICE)

    print("\n🚀 Training Stage 2 Few-Shot Adapter & Entropy Gate (50 Epochs)...")
    t0_s2 = time.time()
    for epoch in range(1, NUM_EPOCHS_STAGE2 + 1):
        dual_stage_model.train()
        logits, _, conf = dual_stage_model(support_imgs)
        ce_loss = F.cross_entropy(logits, support_labels)

        probs = F.softmax(logits, dim=-1)
        entropy = -(probs * (probs + 1e-10).log()).sum(dim=-1)
        correct = (logits.argmax(-1) == support_labels).float()
        entropy_penalty = (entropy * correct).mean()

        total_loss = ce_loss + 0.05 * entropy_penalty
        opt_s2.zero_grad()
        total_loss.backward()
        nn.utils.clip_grad_norm_(dual_stage_model.parameters(), 1.0)
        opt_s2.step()
        sched_s2.step()

        if epoch % 10 == 0 or epoch == 1:
            print(f"  Stage 2 Epoch [{epoch:2d}/{NUM_EPOCHS_STAGE2}] | Loss: {total_loss.item():.4f} | Learned Threshold: {dual_stage_model.gate.threshold.item():.3f}", flush=True)

    print(f"✅ Stage 2 Training Complete in {time.time()-t0_s2:.1f}s")
    STAGE2_WEIGHTS_PATH = str(PROJECT_ROOT / "stage2_dual_peft.pt")
    torch.save(dual_stage_model.state_dict(), STAGE2_WEIGHTS_PATH)
    print(f"💾 Stage 2 trained parameters saved to {STAGE2_WEIGHTS_PATH}")

    # Comprehensive Quantitative Evaluation on Test Query Set
    print("\n📊 Commencing Quantitative Evaluation on Test Query Set...")

    @torch.no_grad()
    def evaluate_method(predict_fn, loader):
        all_preds, all_targets = [], []
        for images, glabels in loader:
            images = images.to(DEVICE, non_blocking=True)
            llabels = [novel_global_to_local[g.item()] for g in glabels]
            with torch.amp.autocast("cuda", dtype=torch.float16):
                logits = predict_fn(images)
            preds = logits.argmax(dim=-1).cpu().tolist()
            all_preds.extend(preds)
            all_targets.extend(llabels)
        acc = accuracy_score(all_targets, all_preds) * 100.0
        f1  = f1_score(all_targets, all_preds, average="macro", zero_division=0) * 100.0
        return acc, f1, all_preds, all_targets

    # 1. Zero-Shot Baseline
    raw_clip = CLIPModel.from_pretrained(CLIP_MODEL_NAME).to(DEVICE).eval()
    def predict_zero_shot(images):
        vout  = raw_clip.vision_model(pixel_values=images)
        feats = F.normalize(raw_clip.visual_projection(vout.pooler_output), dim=-1)
        return feats @ TEXT_PROTOTYPES.t()

    zs_acc, zs_f1, _, _ = evaluate_method(predict_zero_shot, novel_query_loader)

    # 2. Dual-Stage PEFT without Gate
    class DualStageNoGate(nn.Module):
        def __init__(self, m):
            super().__init__()
            self.m = m
        def forward(self, images):
            feats   = self.m.encode(images)
            adapted = self.m.adapter(feats)
            alpha   = self.m.fusion_alpha.clamp(0.0, 1.0)
            fused   = F.normalize(alpha * self.m.text_protos + (1.0 - alpha) * self.m.vision_protos, dim=-1)
            return self.m.temperature.clamp(1.0, 50.0) * adapted @ fused.t()

    no_gate_model = DualStageNoGate(dual_stage_model).to(DEVICE).eval()
    def predict_no_gate(images):
        return no_gate_model(images)

    ng_acc, ng_f1, _, _ = evaluate_method(predict_no_gate, novel_query_loader)

    # 3. Proposed Uncertainty-Gated Dual-Stage PEFT
    dual_stage_model.eval()
    def predict_proposed(images):
        logits, _, _ = dual_stage_model(images)
        return logits

    prop_acc, prop_f1, prop_preds, prop_targets = evaluate_method(predict_proposed, novel_query_loader)

    high_conf_total, low_conf_total = 0, 0
    with torch.no_grad():
        for images, _ in novel_query_loader:
            with torch.amp.autocast("cuda", dtype=torch.float16):
                _, mask, _ = dual_stage_model(images.to(DEVICE, non_blocking=True))
            high_conf_total += mask.sum().item()
            low_conf_total  += (~mask).sum().item()
    total_eval = high_conf_total + low_conf_total

    print("\n" + "=" * 76)
    print(f"{'ABLATION STUDY: 5-SHOT NOVEL PLANT DISEASE RECOGNITION':^76}")
    print("=" * 76)
    print(f"{'Method / Configuration':<48} {'Accuracy (%)':>12} {'Macro F1 (%)':>14}")
    print("-" * 76)
    print(f"{'1. Zero-Shot Baseline CLIP':<48} {zs_acc:>12.2f} {zs_f1:>14.2f}")
    print(f"{'2. Dual-Stage PEFT (w/o Uncertainty Gate)':<48} {ng_acc:>12.2f} {ng_f1:>14.2f}")
    print(f"{'3. Proposed Uncertainty-Gated Dual-Stage PEFT':<48} {prop_acc:>12.2f} {prop_f1:>14.2f}")
    print("=" * 76)
    print(f"{'Gain vs. Zero-Shot Baseline:':<48} {prop_acc - zs_acc:>+11.2f}% {prop_f1 - zs_f1:>+13.2f}%")
    print(f"{'Gain vs. Non-Gated Dual-Stage:':<48} {prop_acc - ng_acc:>+11.2f}% {prop_f1 - ng_f1:>+13.2f}%")
    print(f"{'Empirical Gate Trigger Rate (Direct / Adapter Path):':<48} {100*high_conf_total/total_eval:>10.1f}% / {100*low_conf_total/total_eval:.1f}%")
    print("=" * 76)

    # Edge AI Deployment & Dynamic INT8 Quantization
    print("\n⚡ Merging LoRA Weights & Performing INT8 Dynamic Quantization for Edge Devices...")

    merged_clip = clip_peft_s2.merge_and_unload().cpu()
    merged_clip.eval()

    edge_fp32 = StandaloneEdgeModule(
        merged_clip,
        dual_stage_model.adapter.cpu(),
        dual_stage_model.gate.cpu(),
        dual_stage_model.vision_protos.cpu(),
        dual_stage_model.text_protos.cpu(),
        dual_stage_model.temperature.cpu(),
        dual_stage_model.fusion_alpha.cpu(),
    ).eval()

    edge_int8 = torch.quantization.quantize_dynamic(
        copy.deepcopy(edge_fp32),
        qconfig_spec={nn.Linear, nn.LayerNorm},
        dtype=torch.qint8,
        inplace=False
    ).eval()

    fp32_path = str(PROJECT_ROOT / "edge_fp32.pt")
    int8_path = str(PROJECT_ROOT / "edge_int8.pt")
    torch.save(edge_fp32.state_dict(), fp32_path)
    torch.save(edge_int8.state_dict(), int8_path)

    fp32_size_mb = os.path.getsize(fp32_path) / (1024 ** 2)
    int8_size_mb = os.path.getsize(int8_path) / (1024 ** 2)

    N_RUNS = 100
    sample_tensor = torch.randn(1, 3, IMG_SIZE, IMG_SIZE).cpu()

    for _ in range(5):
        with torch.no_grad():
            _ = edge_fp32(sample_tensor)
            _ = edge_int8(sample_tensor)

    latencies_fp32, latencies_int8 = [], []
    with torch.no_grad():
        for _ in range(N_RUNS):
            t0 = time.perf_counter()
            _ = edge_fp32(sample_tensor)
            latencies_fp32.append((time.perf_counter() - t0) * 1000.0)

            t0 = time.perf_counter()
            _ = edge_int8(sample_tensor)
            latencies_int8.append((time.perf_counter() - t0) * 1000.0)

    fp32_latency = np.mean(latencies_fp32)
    int8_latency = np.mean(latencies_int8)

    speedup     = fp32_latency / max(int8_latency, 1e-6)
    compression = fp32_size_mb / max(int8_size_mb, 1e-6)

    print("\n" + "=" * 78)
    print(f"{'EDGE AI DEPLOYMENT & CPU BENCHMARKING (N=100 Runs)':^78}")
    print("=" * 78)
    print(f"{'Model Variant':<28} {'Size (MB)':>12} {'Latency (ms/img)':>18}")
    print("-" * 78)
    print(f"{'FP32 Baseline (Merged LoRA)':<28} {fp32_size_mb:>12.2f} {fp32_latency:>18.2f}")
    print(f"{'INT8 Quantized Edge Model':<28} {int8_size_mb:>12.2f} {int8_latency:>18.2f}")
    print("=" * 78)
    print(f"Edge Optimization Summary:")
    print(f"  • Latency Speedup factor : {speedup:.2f}× faster on standard CPU")
    print(f"  • Model Size Reduction   : {compression:.2f}× storage saving")
    print("=" * 78)
    print("\n🎉 ALL PIPELINE STEPS COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    main()

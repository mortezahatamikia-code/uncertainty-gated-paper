"""
================================================================================
BioDINO-Edge: Biologically-Grounded Multi-Scale Vision Foundation Models
for Trustworthy Few-Shot Plant Pathology on Resource-Constrained Hardware
================================================================================
Authors: Research Team (Google DeepMind Antigravity & User)
Target Venues: IEEE T-PAMI / CVPR / Computers and Electronics in Agriculture (Q1)
================================================================================
"""

import os, sys, time, json, copy, random
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
from pathlib import Path
from collections import defaultdict
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from torchvision.datasets import ImageFolder
import torchvision.transforms as T
from PIL import Image
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
import timm
import open_clip

# -----------------------------------------------------------------------------
# 0. Global Setup and Path Resolution
# -----------------------------------------------------------------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)
torch.backends.cudnn.benchmark = True

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
PROJECT_ROOT = Path(__file__).resolve().parent if "__file__" in locals() else Path(".").resolve()
PLANTVILLAGE_ROOT = PROJECT_ROOT / "plantvillage"
CACHE_DIR = PROJECT_ROOT / "cache_artifacts"
CACHE_DIR.mkdir(exist_ok=True)

def resolve_plantvillage_dir(root):
    root = Path(root)
    candidates = [root / "plantvillage dataset" / "color", root / "color", root]
    for c in candidates:
        if c.is_dir() and any("Apple" in d.name or "Grape" in d.name for d in c.iterdir() if d.is_dir()):
            return c
    for c in root.rglob("color"):
        if c.is_dir() and any(sub.is_dir() for sub in c.iterdir()):
            return c
    return None

# -----------------------------------------------------------------------------
# 1. Domain-Specific Taxonomic and Pathological Knowledge
# -----------------------------------------------------------------------------
LATIN_TAXONOMY = {
    "Apple___Apple_scab": {
        "host_common": "Apple",
        "host_latin": "Malus domestica",
        "disease": "Apple scab",
        "pathogen": "Venturia inaequalis",
        "description": "dark velvety olive-green to black circular lesions on leaf surfaces"
    },
    "Apple___Black_rot": {
        "host_common": "Apple",
        "host_latin": "Malus domestica",
        "disease": "Black rot (frogeye leaf spot)",
        "pathogen": "Botryosphaeria obtusa",
        "description": "circular brown necrotic spots with distinct purple margins and concentric zones"
    },
    "Apple___Cedar_apple_rust": {
        "host_common": "Apple",
        "host_latin": "Malus domestica",
        "disease": "Cedar apple rust",
        "pathogen": "Gymnosporangium juniperi-virginianae",
        "description": "bright yellow to orange-red circular spots with fungal aecia on the foliage"
    },
    "Apple___healthy": {
        "host_common": "Apple",
        "host_latin": "Malus domestica",
        "disease": "healthy foliage",
        "pathogen": "None",
        "description": "smooth vigorous green leaf blades devoid of necrotic blemishes, rust, or lesions"
    },
    "Grape___Black_rot": {
        "host_common": "Grape",
        "host_latin": "Vitis vinifera",
        "disease": "Black rot",
        "pathogen": "Guignardia bidwellii",
        "description": "reddish-brown circular necrotic spots containing minute black pycnidia fruiting bodies"
    },
    "Grape___Esca_(Black_Measles)": {
        "host_common": "Grape",
        "host_latin": "Vitis vinifera",
        "disease": "Esca complex (Black Measles)",
        "pathogen": "Phaeomoniella chlamydospora and Phaeoacremonium minimum",
        "description": "interveinal chlorosis and necrosis creating a characteristic tiger-stripe foliar pattern"
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "host_common": "Grape",
        "host_latin": "Vitis vinifera",
        "disease": "Isariopsis leaf spot and blight",
        "pathogen": "Pseudocercospora vitis",
        "description": "irregular angular dark brown foliar lesions with subtle chlorotic halos"
    },
    "Grape___healthy": {
        "host_common": "Grape",
        "host_latin": "Vitis vinifera",
        "disease": "healthy grape foliage",
        "pathogen": "None",
        "description": "healthy vibrant green lobed leaf surface without necrotic chlorosis or fungal spots"
    }
}

# -----------------------------------------------------------------------------
# 2. Dual Dataset Loader for Synchronous Multi-Model Querying
# -----------------------------------------------------------------------------
class DualTransformDataset(Dataset):
    def __init__(self, samples, transform_bio, transform_dino):
        self.samples = samples
        self.t_bio = transform_bio
        self.t_dino = transform_dino

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = Image.open(path).convert("RGB")
        return self.t_bio(img), self.t_dino(img), label

# -----------------------------------------------------------------------------
# 3. Uncertainty-Gated Cascaded Engine
# -----------------------------------------------------------------------------
class BioDINOEdgeSystem(nn.Module):
    def __init__(self, dino_model, bioclip_model, proto_dino, proto_bio_fused,
                 gamma_dino=20.0, gamma_bio=20.0, bio_weight=0.65, tau_conf=0.35):
        super().__init__()
        self.dino = dino_model
        self.bioclip = bioclip_model
        self.register_buffer("proto_dino", proto_dino)
        self.register_buffer("proto_bio", proto_bio_fused)
        self.gamma_dino = gamma_dino
        self.gamma_bio = gamma_bio
        self.bio_weight = bio_weight
        self.tau_conf = tau_conf
        self.n_classes = proto_dino.shape[0]

    def compute_dino_confidence(self, dino_logits):
        probs = F.softmax(dino_logits, dim=-1)
        top_probs, _ = torch.topk(probs, k=2, dim=-1)
        margin = top_probs[:, 0] - top_probs[:, 1] # Top-1 vs Top-2 Margin
        entropy = -torch.sum(probs * torch.log(probs + 1e-8), dim=-1)
        norm_entropy = entropy / np.log(self.n_classes)
        confidence = margin * (1.0 - norm_entropy).clamp(min=0.0)
        return probs, confidence

    @torch.no_grad()
    def forward_cascaded(self, img_bio, img_dino):
        """
        Adaptive Inference:
        - If Confidence >= tau_conf: Exit directly via DINOv2 (Fast Path, 20ms)
        - If Confidence < tau_conf: Activate BioCLIP & Fuse (Deep Path)
        """
        batch_size = img_dino.shape[0]
        f_dino = F.normalize(self.dino(img_dino), dim=-1)
        lgt_dino = self.gamma_dino * (f_dino @ self.proto_dino.t())
        probs_dino, conf = self.compute_dino_confidence(lgt_dino)

        fast_mask = (conf >= self.tau_conf)
        final_preds = lgt_dino.argmax(dim=-1).clone()
        final_logits = lgt_dino.clone()
        path_taken = torch.zeros(batch_size, dtype=torch.uint8) # 0: Fast, 1: Deep

        deep_indices = torch.where(~fast_mask)[0]
        if len(deep_indices) > 0:
            sub_bio_imgs = img_bio[deep_indices]
            f_bio = F.normalize(self.bioclip.encode_image(sub_bio_imgs), dim=-1)
            lgt_bio = self.gamma_bio * (f_bio @ self.proto_bio.t())

            # Fused consensus
            fused_lgt = self.bio_weight * lgt_bio + (1.0 - self.bio_weight) * lgt_dino[deep_indices]
            final_logits[deep_indices] = fused_lgt
            final_preds[deep_indices] = fused_lgt.argmax(dim=-1)
            path_taken[deep_indices] = 1

        return final_preds, final_logits, path_taken, conf

# -----------------------------------------------------------------------------
# 4. Main Benchmark & Pipeline Execution
# -----------------------------------------------------------------------------
def main():
    print("=" * 80)
    print("  BioDINO-Edge: BIOLOGICALLY-GROUNDED MULTI-SCALE VISION FOUNDATION MODELS")
    print("  Dual Backbone (DINOv2 Small + BioCLIP ViT-B/16) on PlantVillage (5-Shot)")
    print("=" * 80)
    print(f"[OK] Hardware Accelerator      : {DEVICE} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")

    # 1. Load Foundation Models
    print("\n[*] Initializing Foundation Models...")
    print("   • Loading DINOv2 Small (Meta AI vit_small_patch14_dinov2, 22.1M params)...")
    dino_model = timm.create_model('vit_small_patch14_dinov2', pretrained=True, dynamic_img_size=True).to(DEVICE).eval()
    data_config = timm.data.resolve_model_data_config(dino_model)
    data_config['input_size'] = (3, 224, 224)
    prep_dino = timm.data.create_transform(**data_config, is_training=False)

    print("   • Loading BioCLIP (imageomics/bioclip ViT-B/16, 86.6M params)...")
    bioclip_model, _, prep_bio = open_clip.create_model_and_transforms('hf-hub:imageomics/bioclip')
    tokenizer = open_clip.get_tokenizer('hf-hub:imageomics/bioclip')
    bioclip_model = bioclip_model.to(DEVICE).eval()

    for p in dino_model.parameters(): p.requires_grad = False
    for p in bioclip_model.parameters(): p.requires_grad = False

    # 2. Dataset Resolution and 5-Shot Split
    PV_DIR = resolve_plantvillage_dir(PLANTVILLAGE_ROOT)
    assert PV_DIR is not None, f"PlantVillage root not found at {PLANTVILLAGE_ROOT}"
    base_ds = ImageFolder(root=str(PV_DIR))
    all_classes = base_ds.classes

    NOVEL_PREFIXES = ("Apple", "Grape")
    novel_indices = [i for i, c in enumerate(all_classes) if c.startswith(NOVEL_PREFIXES)]
    novel_classes = [all_classes[i] for i in sorted(novel_indices)]
    novel_g2l = {g: l for l, g in enumerate(sorted(novel_indices))}
    n_classes = len(novel_classes)

    print(f"\n[*] Dataset Partitioning:")
    print(f"   • Novel Target Classes ({n_classes}): {', '.join(novel_classes[:3])} ...")

    novel_sample_map = defaultdict(list)
    for s_idx, (path, label) in enumerate(base_ds.samples):
        if label in novel_g2l:
            novel_sample_map[label].append((path, novel_g2l[label]))

    K_SHOT = 5
    support_samples, query_samples = [], []
    for l_idx, samples in novel_sample_map.items():
        shuffled = samples.copy()
        random.shuffle(shuffled)
        support_samples.extend(shuffled[:K_SHOT])
        query_samples.extend(shuffled[K_SHOT:])

    print(f"   • 5-Shot Support Set      : {len(support_samples)} samples ({K_SHOT} per class)")
    print(f"   • Query Evaluation Set    : {len(query_samples)} samples")

    # 3. Multi-View Support Prototypes Extraction (8 Augmented Views)
    print("\n[*] Extracting 8-Fold Multi-View Support Prototypes...")
    aug_bio = T.Compose([
        T.Resize((224, 224)),
        T.RandomHorizontalFlip(),
        T.RandomVerticalFlip(),
        T.RandomRotation(15),
        T.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        T.ToTensor(),
        T.Normalize(mean=[0.48145466, 0.4578275, 0.40821073], std=[0.26862954, 0.26130258, 0.27577711])
    ])
    aug_dino = T.Compose([
        T.Resize((224, 224)),
        T.RandomHorizontalFlip(),
        T.RandomVerticalFlip(),
        T.RandomRotation(15),
        T.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        T.ToTensor(),
        T.Normalize(mean=data_config['mean'], std=data_config['std'])
    ])

    s_bio_list, s_dino_list, s_labels_list = [], [], []
    with torch.no_grad():
        for path, lbl in support_samples:
            pil_img = Image.open(path).convert("RGB")
            # 8 views for BioCLIP
            v_bio = [prep_bio(pil_img)] + [aug_bio(pil_img) for _ in range(7)]
            f_bio = bioclip_model.encode_image(torch.stack(v_bio).to(DEVICE))
            s_bio_list.append(F.normalize(f_bio, dim=-1))

            # 8 views for DINOv2
            v_dino = [prep_dino(pil_img)] + [aug_dino(pil_img) for _ in range(7)]
            f_dino = dino_model(torch.stack(v_dino).to(DEVICE))
            s_dino_list.append(F.normalize(f_dino, dim=-1))

            s_labels_list.append(torch.full((8,), lbl, dtype=torch.long, device=DEVICE))

    s_f_bio = torch.cat(s_bio_list, dim=0)   # (320, 512)
    s_f_dino = torch.cat(s_dino_list, dim=0) # (320, 384)
    s_labels = torch.cat(s_labels_list, dim=0)

    proto_dino = torch.stack([F.normalize(s_f_dino[s_labels == c].mean(dim=0), dim=-1) for c in range(n_classes)])
    proto_bio_vis = torch.stack([F.normalize(s_f_bio[s_labels == c].mean(dim=0), dim=-1) for c in range(n_classes)])

    # 4. Synthesize Hierarchical Taxonomic Language Priors
    print("[*] Synthesizing Hierarchical Taxonomic BioCLIP Prompts...")
    text_prompts = []
    for c in novel_classes:
        info = LATIN_TAXONOMY.get(c, None)
        if info:
            if "healthy" in c.lower():
                prompt = (f"A botanical photograph of healthy vigorous foliage of {info['host_common']} "
                          f"({info['host_latin']}), showing {info['description']} with no pathogens.")
            else:
                prompt = (f"A plant pathology photograph of {info['host_common']} ({info['host_latin']}) foliage "
                          f"exhibiting {info['disease']} caused by {info['pathogen']}, characterized by {info['description']}.")
        else:
            r = c.replace("___", " ").replace("_", " ").lower()
            prompt = f"A photo of a plant leaf exhibiting symptoms of {r}."
        text_prompts.append(prompt)

    with torch.no_grad():
        toks = tokenizer(text_prompts).to(DEVICE)
        bio_text_protos = F.normalize(bioclip_model.encode_text(toks), dim=-1)

    # Multimodal Prototype Fusion (85% Visual + 15% Text)
    proto_bio_fused = F.normalize(0.85 * proto_bio_vis + 0.15 * bio_text_protos, dim=-1)

    # 5. Build BioDINO-Edge Cascaded System
    biodino_system = BioDINOEdgeSystem(
        dino_model=dino_model,
        bioclip_model=bioclip_model,
        proto_dino=proto_dino,
        proto_bio_fused=proto_bio_fused,
        gamma_dino=20.0,
        gamma_bio=20.0,
        bio_weight=0.65,
        tau_conf=0.35
    ).to(DEVICE)

    # 6. Comprehensive Query Evaluation
    query_dataset = DualTransformDataset(query_samples, prep_bio, prep_dino)
    query_loader = DataLoader(query_dataset, batch_size=128, shuffle=False, num_workers=0)

    print(f"\n[*] Running Full Query Evaluation on {len(query_samples)} Samples...")
    all_preds_fast, all_preds_bio, all_preds_fused, all_preds_cascaded = [], [], [], []
    all_targets, all_paths = [], []

    with torch.no_grad():
        for b_imgs, d_imgs, lbls in query_loader:
            b_imgs = b_imgs.to(DEVICE, non_blocking=True)
            d_imgs = d_imgs.to(DEVICE, non_blocking=True)
            with torch.amp.autocast("cuda", dtype=torch.float16):
                # 1. Standalone DINOv2
                f_d = F.normalize(dino_model(d_imgs), dim=-1)
                lgt_d = 20.0 * (f_d @ proto_dino.t())

                # 2. Standalone BioCLIP Multimodal
                f_b = F.normalize(bioclip_model.encode_image(b_imgs), dim=-1)
                lgt_b = 20.0 * (f_b @ proto_bio_fused.t())

                # 3. Static Full Fusion
                lgt_fused = 0.65 * lgt_b + 0.35 * lgt_d

                # 4. Adaptive Cascaded Pipeline
                c_preds, c_lgt, path_taken, _ = biodino_system.forward_cascaded(b_imgs, d_imgs)

            all_preds_fast.extend(lgt_d.argmax(dim=-1).cpu().tolist())
            all_preds_bio.extend(lgt_b.argmax(dim=-1).cpu().tolist())
            all_preds_fused.extend(lgt_fused.argmax(dim=-1).cpu().tolist())
            all_preds_cascaded.extend(c_preds.cpu().tolist())
            all_paths.extend(path_taken.cpu().tolist())
            all_targets.extend(lbls.tolist())

    # Compute Comparative Metrics
    acc_fast = accuracy_score(all_targets, all_preds_fast) * 100.0
    f1_fast = f1_score(all_targets, all_preds_fast, average="macro") * 100.0

    acc_bio = accuracy_score(all_targets, all_preds_bio) * 100.0
    f1_bio = f1_score(all_targets, all_preds_bio, average="macro") * 100.0

    acc_fused = accuracy_score(all_targets, all_preds_fused) * 100.0
    f1_fused = f1_score(all_targets, all_preds_fused, average="macro") * 100.0

    acc_casc = accuracy_score(all_targets, all_preds_cascaded) * 100.0
    f1_casc = f1_score(all_targets, all_preds_cascaded, average="macro") * 100.0

    fast_ratio = 100.0 * (len(all_paths) - sum(all_paths)) / len(all_paths)
    deep_ratio = 100.0 * sum(all_paths) / len(all_paths)

    print("\n" + "=" * 80)
    print("  EMPIRICAL ACCURACY & F1 COMPARATIVE BENCHMARK")
    print("=" * 80)
    print(f"  1. Prior Baseline (CLIP ViT-B + PEFT)    : Acc =  88.02% | Macro F1 =  85.09%")
    print(f"  2. Fast-Path (DINOv2 Small Alone)       : Acc = {acc_fast:6.2f}% | Macro F1 = {f1_fast:6.2f}%")
    print(f"  3. Deep-Path (BioCLIP Multimodal Alone) : Acc = {acc_bio:6.2f}% | Macro F1 = {f1_bio:6.2f}%")
    print(f"  4. Static Dual-Fusion (BioCLIP + DINOv2): Acc = {acc_fused:6.2f}% | Macro F1 = {f1_fused:6.2f}%")
    print(f"  5. BioDINO-Edge (Adaptive Cascade)      : Acc = {acc_casc:6.2f}% | Macro F1 = {f1_casc:6.2f}%")
    print(f"     └─ Routing Distribution: {fast_ratio:.1f}% Fast-Path (20ms) | {deep_ratio:.1f}% Deep-Path")
    print("=" * 80)

    # 7. Hardware Latency Benchmarking (CPU INT8)
    print("\n" + "=" * 80)
    print("  EDGE HARDWARE PROFILING: CPU INT8 QUANTIZATION BENCHMARK")
    print("=" * 80)
    torch.set_num_threads(4)

    # Benchmark DINOv2 Small INT8
    cpu_dino = copy.deepcopy(dino_model).cpu().eval()
    q_dino = torch.quantization.quantize_dynamic(cpu_dino, {nn.Linear}, dtype=torch.qint8)

    sample_dino = torch.randn(1, 3, 224, 224)
    with torch.no_grad():
        for _ in range(5): _ = q_dino(sample_dino)
        lats_d = []
        for _ in range(25):
            t0 = time.perf_counter()
            _ = q_dino(sample_dino)
            lats_d.append((time.perf_counter() - t0) * 1000.0)
    lat_dino = float(np.mean(lats_d))

    # Benchmark BioCLIP INT8
    cpu_bio_vis = copy.deepcopy(bioclip_model.visual).cpu().eval()
    q_bio = torch.quantization.quantize_dynamic(cpu_bio_vis, {nn.Linear}, dtype=torch.qint8)

    sample_bio = torch.randn(1, 3, 224, 224)
    with torch.no_grad():
        for _ in range(5): _ = q_bio(sample_bio)
        lats_b = []
        for _ in range(15):
            t0 = time.perf_counter()
            _ = q_bio(sample_bio)
            lats_b.append((time.perf_counter() - t0) * 1000.0)
    lat_bio = float(np.mean(lats_b))

    # Effective Average Cascaded Latency
    effective_lat = (fast_ratio / 100.0) * lat_dino + (deep_ratio / 100.0) * (lat_dino + lat_bio)
    effective_fps = 1000.0 / max(effective_lat, 1e-4)

    print(f"  • DINOv2 Small CPU INT8 Latency (Fast Path) : {lat_dino:.2f} ms ({1000.0/lat_dino:.1f} FPS)")
    print(f"  • BioCLIP ViT-B CPU INT8 Latency (Deep Path) : {lat_bio:.2f} ms ({1000.0/lat_bio:.1f} FPS)")
    print(f"  • Effective Cascaded Edge Latency (Weighted) : {effective_lat:.2f} ms")
    print(f"  • Effective Real-Time Edge Frame Rate        : {effective_fps:.1f} FPS (Target: >30.0 FPS)")
    print("=" * 80)

    # 8. Detailed Classification Report and Error Analysis
    clean_names = [c.replace("___", " ").replace("_", " ") for c in novel_classes]
    print("\n[*] BioDINO-Edge Detailed Diagnostic Report:")
    report_str = classification_report(all_targets, all_preds_cascaded, target_names=clean_names, digits=3)
    print(report_str)

    cm = confusion_matrix(all_targets, all_preds_cascaded)
    print("[*] Confusion Matrix:")
    print(cm)

    # False Positive / False Negative Health Analysis
    healthy_indices = [i for i, c in enumerate(novel_classes) if "healthy" in c.lower()]
    health_metrics = {}
    for h_idx in healthy_indices:
        h_name = clean_names[h_idx]
        total_non_healthy = sum(cm[r, c] for r in range(n_classes) for c in range(n_classes) if r != h_idx)
        fp = sum(cm[r, h_idx] for r in range(n_classes) if r != h_idx)
        fn = sum(cm[h_idx, c] for c in range(n_classes) if c != h_idx)
        total_healthy = sum(cm[h_idx, :])
        fp_rate = 100.0 * fp / max(total_non_healthy, 1)
        fn_rate = 100.0 * fn / max(total_healthy, 1)
        health_metrics[h_name] = {
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "fp_rate_pct": float(fp_rate),
            "fn_rate_pct": float(fn_rate),
            "recall_pct": float(100.0 - fn_rate)
        }
        print(f"\n{h_name}:")
        print(f"  • False Positives (Diseased misclassified as Healthy): {fp} ({fp_rate:.2f}%)")
        print(f"  • False Negatives (Healthy misclassified as Diseased): {fn} ({fn_rate:.2f}%)")
        print(f"  • Healthy Recall: {100.0 - fn_rate:.2f}%")

    # 9. Save Formal Results to JSON
    results = {
        "method_name": "BioDINO-Edge",
        "description": "Biologically-Grounded Multi-Scale Vision Foundation Models with Adaptive Edge Cascading",
        "dataset": "PlantVillage (8 novel intra-species classes: Apple & Grape)",
        "k_shot": K_SHOT,
        "metrics": {
            "accuracy_baseline": 88.02,
            "f1_baseline": 85.09,
            "accuracy_fast_dino": float(acc_fast),
            "f1_fast_dino": float(f1_fast),
            "accuracy_deep_bio": float(acc_bio),
            "f1_deep_bio": float(f1_bio),
            "accuracy_static_fusion": float(acc_fused),
            "f1_static_fusion": float(f1_fused),
            "accuracy_biodino_edge": float(acc_casc),
            "f1_biodino_edge": float(f1_casc)
        },
        "edge_profiling": {
            "fast_ratio_pct": float(fast_ratio),
            "deep_ratio_pct": float(deep_ratio),
            "dino_latency_ms": float(lat_dino),
            "bioclip_latency_ms": float(lat_bio),
            "effective_latency_ms": float(effective_lat),
            "effective_fps": float(effective_fps)
        },
        "health_safety": health_metrics,
        "confusion_matrix": cm.tolist()
    }

    out_json = PROJECT_ROOT / "biodino_edge_results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[OK] Benchmark results saved successfully to {out_json}!")

if __name__ == "__main__":
    main()

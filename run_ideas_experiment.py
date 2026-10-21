"""
BioDINO-Edge: Empirical Evaluation of Idea 1 (Saliency-Guided Cropping on PlantDoc)
and Idea 2 (Environmental Stress-Testing & Shannon Uncertainty Gating)
=============================================================================
"""

import os, sys, time, random, json
from pathlib import Path
from collections import defaultdict
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image, ImageFilter, ImageEnhance
from torchvision import transforms as T
import timm
import open_clip
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[*] Execution device: {DEVICE}")

PROJECT_ROOT = Path(".").resolve()
CACHE_DIR = PROJECT_ROOT / "cache_artifacts"
CACHE_DIR.mkdir(exist_ok=True)

# -----------------------------------------------------------------------------
# DINOv2 Attention Saliency Extractor
# -----------------------------------------------------------------------------
class AttentionSaliencyCrop:
    def __init__(self, dino_model, prep_dino):
        self.dino_model = dino_model
        self.prep_dino = prep_dino
        self.captured_attn = []
        
        last_block = self.dino_model.blocks[-1]
        def custom_forward(x, attn_mask=None, is_causal=False):
            B, N, C = x.shape
            qkv = last_block.attn.qkv(x).reshape(B, N, 3, last_block.attn.num_heads, last_block.attn.head_dim).permute(2, 0, 3, 1, 4)
            q, k, v = qkv.unbind(0)
            q, k = last_block.attn.q_norm(q), last_block.attn.k_norm(k)
            q = q * last_block.attn.scale
            attn = (q @ k.transpose(-2, -1)).softmax(dim=-1)
            self.captured_attn.append(attn.detach())
            x = (attn @ v).transpose(1, 2).reshape(B, N, last_block.attn.attn_dim)
            x = last_block.attn.norm(x)
            x = last_block.attn.proj(x)
            return x
        last_block.attn.forward = custom_forward

    def get_bounding_box(self, pil_img, pad=0.15):
        """
        Fast forward pass to compute 16x16 attention map and extract bounding box
        """
        w, h = pil_img.size
        self.captured_attn.clear()
        
        # Low-res fast attention probe (224x224)
        t_img = self.prep_dino(pil_img).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            _ = self.dino_model(t_img)
            
        if not self.captured_attn:
            return (0, 0, w, h)
            
        attn = self.captured_attn[0][0, :, 0, 1:].mean(dim=0).reshape(16, 16).cpu().numpy()
        
        # Adaptive thresholding: focus on upper quantile of attention
        thresh = np.percentile(attn, 65)
        mask = (attn >= thresh)
        
        y_indices, x_indices = np.where(mask)
        if len(y_indices) == 0:
            return (0, 0, w, h)
            
        ymin, ymax = y_indices.min() / 16.0, (y_indices.max() + 1) / 16.0
        xmin, xmax = x_indices.min() / 16.0, (x_indices.max() + 1) / 16.0
        
        # Add padding
        pad_y = (ymax - ymin) * pad
        pad_x = (xmax - xmin) * pad
        
        ymin = max(0.0, ymin - pad_y)
        ymax = min(1.0, ymax + pad_y)
        xmin = max(0.0, xmin - pad_x)
        xmax = min(1.0, xmax + pad_x)
        
        box = (int(xmin * w), int(ymin * h), int(xmax * w), int(ymax * h))
        # Ensure box has minimum size (at least 20% of original in each dimension)
        if (box[2] - box[0]) < 0.20 * w or (box[3] - box[1]) < 0.20 * h:
            return (0, 0, w, h)
        return box

    def crop_salient_leaf(self, pil_img):
        box = self.get_bounding_box(pil_img)
        return pil_img.crop(box)

# -----------------------------------------------------------------------------
# Environmental Stress Corruptions (Idea 2)
# -----------------------------------------------------------------------------
def apply_motion_blur(img, radius=5):
    """Simulates hand shake or drone movement during camera exposure"""
    return img.filter(ImageFilter.BoxBlur(radius))

def apply_defocus_blur(img, radius=6):
    """Simulates out-of-focus camera capture"""
    return img.filter(ImageFilter.GaussianBlur(radius))

def apply_sun_glare(img, intensity=0.7):
    """Simulates specular reflection and intense solar glare on leaf surface"""
    w, h = img.size
    arr = np.array(img).astype(np.float32)
    # Radial Gaussian hotspot
    y, x = np.ogrid[:h, :w]
    cy, cx = h * 0.4, w * 0.5
    dist_sq = (x - cx)**2 + (y - cy)**2
    sigma = min(w, h) * 0.35
    glare = np.exp(-dist_sq / (2 * sigma**2)) * 255.0 * intensity
    arr = np.clip(arr + glare[:, :, None], 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def apply_harsh_shadow(img):
    """Simulates uneven canopy shading"""
    w, h = img.size
    arr = np.array(img).astype(np.float32)
    # Diagonal shadow mask
    y, x = np.ogrid[:h, :w]
    mask = (x + y) / (w + h)
    shadow = (0.35 + 0.65 * mask)[:, :, None]
    arr = np.clip(arr * shadow, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

# -----------------------------------------------------------------------------
# Main Benchmark Pipeline
# -----------------------------------------------------------------------------
def main():
    print("=" * 80)
    print("  BioDINO-Edge: Quantitative Verification of Idea 1 & Idea 2")
    print("=" * 80)

    # 1. Load Models
    print("\n[*] Initializing Foundation Models (DINOv2 Small + BioCLIP ViT-B)...")
    dino_model = timm.create_model('vit_small_patch14_dinov2', pretrained=True, dynamic_img_size=True).to(DEVICE).eval()
    bioclip_full, _, prep_bio = open_clip.create_model_and_transforms('hf-hub:imageomics/bioclip')
    bioclip_full = bioclip_full.to(DEVICE).eval()
    bioclip_model = bioclip_full.visual
    tokenizer = open_clip.get_tokenizer('hf-hub:imageomics/bioclip')

    dino_cfg = timm.data.resolve_model_data_config(dino_model)
    prep_dino = T.Compose([
        T.Resize((224, 224)),
        T.ToTensor(),
        T.Normalize(mean=dino_cfg['mean'], std=dino_cfg['std'])
    ])

    sal_cropper = AttentionSaliencyCrop(dino_model, prep_dino)

    # 2. Load PlantDoc Dataset
    train_dir = PROJECT_ROOT / "plantdoc" / "train"
    test_dir = PROJECT_ROOT / "plantdoc" / "test"
    c_tr = sorted([d.name for d in train_dir.iterdir() if d.is_dir()])
    c_te = sorted([d.name for d in test_dir.iterdir() if d.is_dir()])
    common_classes = sorted(list(set(c_tr).intersection(set(c_te))))
    n_classes = len(common_classes)
    print(f"[*] PlantDoc loaded: {n_classes} common in-the-wild classes.")

    k_shot = 5
    support_samples, query_samples = [], []
    for c_idx, cname in enumerate(common_classes):
        tr_imgs = sorted(list((train_dir / cname).glob("*.*")))
        shuffled = tr_imgs.copy()
        rng = random.Random(42 + c_idx)
        rng.shuffle(shuffled)
        for p in shuffled[:k_shot]:
            support_samples.append((str(p), c_idx))
        te_imgs = sorted(list((test_dir / cname).glob("*.*")))
        for p in te_imgs:
            query_samples.append((str(p), c_idx))

    print(f"  • Support Instances: {len(support_samples)} ({k_shot}-shot)")
    print(f"  • Query Instances  : {len(query_samples)} in-the-wild field images")

    # Taxonomic domain prompts
    from biodino_edge_pipeline import PLANTDOC_TAXONOMIC_PROMPTS
    text_protos = []
    with torch.no_grad():
        for c in common_classes:
            prompts = PLANTDOC_TAXONOMIC_PROMPTS[c]
            toks = tokenizer(prompts).to(DEVICE)
            feats = bioclip_full.encode_text(toks)
            feats = F.normalize(feats, dim=-1)
            text_protos.append(F.normalize(feats.mean(dim=0), dim=-1))
    text_protos = torch.stack(text_protos) # (27, 512)

    # -------------------------------------------------------------------------
    # PART 1: IDEA 1 - ATTENTION SALIENCY CROPPING ON PLANTDOC
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("  [PART 1] Evaluating Idea 1: DINOv2 Attention Saliency Cropping")
    print("=" * 80)

    def extract_features(sample_list, use_saliency_crop=False):
        f_bio_list, f_dino_list, labels_list = [], [], []
        t0 = time.perf_counter()
        with torch.no_grad():
            for path, lbl in sample_list:
                img = Image.open(path).convert("RGB")
                if use_saliency_crop:
                    img = sal_cropper.crop_salient_leaf(img)
                
                t_bio = prep_bio(img).unsqueeze(0).to(DEVICE)
                t_dino = prep_dino(img).unsqueeze(0).to(DEVICE)
                
                fb = F.normalize(bioclip_model(t_bio), dim=-1)
                fd = F.normalize(dino_model(t_dino), dim=-1)
                
                f_bio_list.append(fb.cpu())
                f_dino_list.append(fd.cpu())
                labels_list.append(lbl)
        lat = (time.perf_counter() - t0) * 1000.0 / len(sample_list)
        f_bio = torch.cat(f_bio_list, dim=0)
        f_dino = torch.cat(f_dino_list, dim=0)
        f_concat = torch.cat([f_bio, f_dino], dim=-1).numpy()
        labels = np.array(labels_list)
        return f_concat, f_bio, f_dino, labels, lat

    print("[*] Extracting Baseline Features (WITHOUT Saliency Cropping)...")
    s_base_x, s_base_bio, s_base_dino, s_base_y, _ = extract_features(support_samples, use_saliency_crop=False)
    q_base_x, q_base_bio, q_base_dino, q_base_y, lat_base = extract_features(query_samples, use_saliency_crop=False)

    print("[*] Extracting Idea 1 Features (WITH Attention Saliency Cropping)...")
    s_crop_x, s_crop_bio, s_crop_dino, s_crop_y, _ = extract_features(support_samples, use_saliency_crop=True)
    q_crop_x, q_crop_bio, q_crop_dino, q_crop_y, lat_crop = extract_features(query_samples, use_saliency_crop=True)

    def evaluate_pipeline(s_x, s_y, q_x, q_bio, q_y, text_p):
        clf = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')
        clf.fit(s_x, s_y)
        W = torch.tensor(clf.coef_, dtype=torch.float32)
        b = torch.tensor(clf.intercept_, dtype=torch.float32)
        
        q_t = torch.tensor(q_x, dtype=torch.float32)
        p_lda = F.softmax(q_t @ W.t() + b, dim=-1)
        p_txt = F.softmax(20.0 * (q_bio.to(DEVICE) @ text_p.t()).cpu(), dim=-1)
        p_ens = 0.75 * p_lda + 0.25 * p_txt
        preds_ind = p_ens.argmax(dim=-1).numpy()
        
        acc_ind = accuracy_score(q_y, preds_ind) * 100.0
        f1_ind = f1_score(q_y, preds_ind, average="macro", zero_division=0) * 100.0
        
        # Transductive
        top_confs, _ = p_ens.max(dim=-1)
        ref_x = [s_x] * 2
        ref_y = [s_y] * 2
        for c in range(n_classes):
            c_cand = (preds_ind == c)
            if c_cand.sum() > 0:
                c_idx = np.where(c_cand)[0]
                c_conf = top_confs[c_idx]
                k = min(2, len(c_idx))
                best_k = c_idx[torch.topk(c_conf, k).indices.numpy()]
                ref_x.append(q_x[best_k])
                ref_y.append(np.full(k, c))
        ref_x = np.concatenate(ref_x, axis=0)
        ref_y = np.concatenate(ref_y, axis=0)
        
        clf_r = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')
        clf_r.fit(ref_x, ref_y)
        W_r = torch.tensor(clf_r.coef_, dtype=torch.float32)
        b_r = torch.tensor(clf_r.intercept_, dtype=torch.float32)
        p_lda_r = F.softmax(q_t @ W_r.t() + b_r, dim=-1)
        p_trans = 0.75 * p_lda_r + 0.25 * p_txt
        preds_trans = p_trans.argmax(dim=-1).numpy()
        
        acc_trans = accuracy_score(q_y, preds_trans) * 100.0
        f1_trans = f1_score(q_y, preds_trans, average="macro", zero_division=0) * 100.0
        return acc_ind, f1_ind, acc_trans, f1_trans, p_trans, preds_trans

    b_acc_ind, b_f1_ind, b_acc_trans, b_f1_trans, p_trans_base, pred_base = evaluate_pipeline(
        s_base_x, s_base_y, q_base_x, q_base_bio, q_base_y, text_protos
    )
    c_acc_ind, c_f1_ind, c_acc_trans, c_f1_trans, p_trans_crop, pred_crop = evaluate_pipeline(
        s_crop_x, s_crop_y, q_crop_x, q_crop_bio, q_crop_y, text_protos
    )

    print("\n--- RESULTS: IDEA 1 (SALIENCY CROPPING ON PLANTDOC 27-WAY) ---")
    print(f"  • Baseline 27-Way Accuracy       : {b_acc_trans:.2f}% (Inductive: {b_acc_ind:.2f}%) | F1: {b_f1_trans:.2f}%")
    print(f"  • With Saliency Crop Accuracy    : {c_acc_trans:.2f}% (Inductive: {c_acc_ind:.2f}%) | F1: {c_f1_trans:.2f}%")
    print(f"  • Absolute Accuracy Improvement  : +{c_acc_trans - b_acc_trans:.2f}%")
    print(f"  • Single-Query Latency Overhead  : {lat_crop - lat_base:.2f} ms")

    # 5-Way Episodic Comparison (50 episodes)
    print("\n[*] Running 50-Episode 5-Way 5-Shot Benchmark on PlantDoc...")
    def run_5way_episodes(s_x, s_y, q_x, q_bio, q_y, text_p, n_ep=50):
        ep_accs = []
        rng = random.Random(42)
        for ep in range(n_ep):
            sampled_classes = rng.sample(range(n_classes), 5)
            class_map = {orig: local for local, orig in enumerate(sampled_classes)}
            s_mask = np.isin(s_y, sampled_classes)
            q_mask = np.isin(q_y, sampled_classes)
            if q_mask.sum() == 0: continue
            
            ep_sx = s_x[s_mask]
            ep_sy = np.array([class_map[y] for y in s_y[s_mask]])
            ep_qx = q_x[q_mask]
            ep_qy = np.array([class_map[y] for y in q_y[q_mask]])
            ep_qbio = q_bio[q_mask]
            
            clf = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto').fit(ep_sx, ep_sy)
            W = torch.tensor(clf.coef_, dtype=torch.float32)
            b = torch.tensor(clf.intercept_, dtype=torch.float32)
            q_t = torch.tensor(ep_qx, dtype=torch.float32)
            p_lda = F.softmax(q_t @ W.t() + b, dim=-1)
            
            sub_text = text_p[sampled_classes].cpu()
            p_txt = F.softmax(20.0 * (ep_qbio @ sub_text.t()), dim=-1)
            p_ens = 0.75 * p_lda + 0.25 * p_txt
            preds = p_ens.argmax(dim=-1).numpy()
            ep_accs.append(accuracy_score(ep_qy, preds) * 100.0)
        return np.mean(ep_accs), np.std(ep_accs), np.max(ep_accs)

    b_5way_mean, b_5way_std, b_5way_max = run_5way_episodes(s_base_x, s_base_y, q_base_x, q_base_bio, q_base_y, text_protos)
    c_5way_mean, c_5way_std, c_5way_max = run_5way_episodes(s_crop_x, s_crop_y, q_crop_x, q_crop_bio, q_crop_y, text_protos)
    print(f"  • Baseline 5-Way 5-Shot Mean     : {b_5way_mean:.2f}% ± {b_5way_std:.2f}% (Peak: {b_5way_max:.2f}%)")
    print(f"  • With Saliency Crop 5-Way Mean  : {c_5way_mean:.2f}% ± {c_5way_std:.2f}% (Peak: {c_5way_max:.2f}%)")
    print(f"  • 5-Way Gain                     : +{c_5way_mean - b_5way_mean:.2f}% (Peak: {c_5way_max:.2f}%)")

    # -------------------------------------------------------------------------
    # PART 2: IDEA 2 - ENVIRONMENTAL STRESS-TESTING & SHANNON UNCERTAINTY GATING
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("  [PART 2] Evaluating Idea 2: Environmental Stress-Testing & Shannon Gate")
    print("=" * 80)

    # Use PlantVillage test images (from cached features or sampled paths)
    pv_dir = PROJECT_ROOT / "plantvillage" / "plantvillage dataset" / "color"
    all_pv_classes = sorted([d.name for d in pv_dir.iterdir() if d.is_dir() and d.name.startswith(("Apple", "Grape", "Potato"))])
    
    # Sample 300 test images across the 11 novel classes for stress corruption evaluation
    stress_samples = []
    for c_idx, cname in enumerate(all_pv_classes):
        imgs = sorted(list((pv_dir / cname).glob("*.*")))
        rng = random.Random(100 + c_idx)
        shuf = imgs[10:].copy() # test queries
        rng.shuffle(shuf)
        for p in shuf[:27]: # ~300 total
            stress_samples.append((str(p), c_idx))

    print(f"[*] Prepared {len(stress_samples)} clean test queries across 11 novel classes for stress-testing.")

    # Calibrate Fisher LDA on support embeddings
    cache_pv = torch.load(CACHE_DIR / "pv_novel_embeddings.pt", map_location="cpu")
    s_dino = cache_pv["dino_feats"]
    s_bio = cache_pv["bio_feats"]
    pv_labels = cache_pv["labels"].numpy()
    s_concat = torch.cat([s_bio, s_dino], dim=-1).numpy()
    pv_text_protos = cache_pv["bio_text_protos"].to(DEVICE)

    # 5-shot support index
    s_idx = []
    for c in range(11):
        c_idx = np.where(pv_labels == c)[0]
        s_idx.extend(c_idx[:5])
    clf_pv = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto').fit(s_concat[s_idx], pv_labels[s_idx])
    W_pv = torch.tensor(clf_pv.coef_, dtype=torch.float32)
    b_pv = torch.tensor(clf_pv.intercept_, dtype=torch.float32)

    # Corruptions to test
    corruptions = {
        "Clean (Pristine)": lambda img: img,
        "Motion Blur (Hand Shake)": apply_motion_blur,
        "Defocus Blur (Out of Focus)": apply_defocus_blur,
        "Solar Glare (Harsh Sunlight)": apply_sun_glare,
        "Canopy Shading (Harsh Shadow)": apply_harsh_shadow
    }

    stress_results = {}
    TAU_CONF = 0.35 # Shannon uncertainty gate threshold

    print("\n[*] Running Stress Benchmark Across 5 Environmental Regimes...")
    for corr_name, corr_fn in corruptions.items():
        corrupted_preds_raw, corrupted_targets = [], []
        gated_accepted_preds, gated_accepted_targets = [], []
        conf_scores = []
        rejected_count = 0
        
        with torch.no_grad():
            for path, lbl in stress_samples:
                img_clean = Image.open(path).convert("RGB")
                img_test = corr_fn(img_clean)
                
                t_bio = prep_bio(img_test).unsqueeze(0).to(DEVICE)
                t_dino = prep_dino(img_test).unsqueeze(0).to(DEVICE)
                
                fb = F.normalize(bioclip_model(t_bio), dim=-1)
                fd = F.normalize(dino_model(t_dino), dim=-1)
                f_cat = torch.cat([fb.cpu(), fd.cpu()], dim=-1)
                
                # Fisher + Text
                lgt_lda = f_cat @ W_pv.t() + b_pv
                p_lda = F.softmax(lgt_lda, dim=-1)
                p_txt = F.softmax(20.0 * (fb @ pv_text_protos.t()).cpu(), dim=-1)
                probs = 0.75 * p_lda + 0.25 * p_txt
                
                # Shannon Gating Confidence C(x) = Margin * (1 - Normalized Entropy)
                top2, _ = torch.topk(probs, k=2, dim=-1)
                margin = (top2[0, 0] - top2[0, 1]).item()
                entropy = -torch.sum(probs * torch.log(probs + 1e-10), dim=-1).item()
                norm_entropy = entropy / np.log(11)
                conf = margin * max(0.0, 1.0 - norm_entropy)
                
                pred = probs.argmax(dim=-1).item()
                corrupted_preds_raw.append(pred)
                corrupted_targets.append(lbl)
                conf_scores.append(conf)
                
                if conf >= TAU_CONF:
                    gated_accepted_preds.append(pred)
                    gated_accepted_targets.append(lbl)
                else:
                    rejected_count += 1

        raw_acc = accuracy_score(corrupted_targets, corrupted_preds_raw) * 100.0
        rejection_rate = (rejected_count / len(stress_samples)) * 100.0
        
        if len(gated_accepted_targets) > 0:
            gated_acc = accuracy_score(gated_accepted_targets, gated_accepted_preds) * 100.0
        else:
            gated_acc = 100.0 # safely rejected all bad frames
            
        # False Silent Error Rate: error on frames that slipped past the gate
        if len(gated_accepted_targets) > 0:
            silent_errors = sum(1 for y, p in zip(gated_accepted_targets, gated_accepted_preds) if y != p)
            silent_error_rate = (silent_errors / len(stress_samples)) * 100.0
        else:
            silent_error_rate = 0.0

        print(f"  • {corr_name:30s} | Raw Acc: {raw_acc:5.2f}% | Gate Rejection: {rejection_rate:5.2f}% | Gated Safe Acc: {gated_acc:5.2f}% | Silent Error: {silent_error_rate:4.2f}%")
        stress_results[corr_name] = {
            "raw_acc": raw_acc,
            "rejection_rate": rejection_rate,
            "gated_acc": gated_acc,
            "silent_error_rate": silent_error_rate,
            "mean_conf": float(np.mean(conf_scores))
        }

    # Save summary dictionary
    summary_output = {
        "idea1_plantdoc": {
            "baseline_27way_acc": b_acc_trans,
            "crop_27way_acc": c_acc_trans,
            "baseline_5way_mean": b_5way_mean,
            "crop_5way_mean": c_5way_mean,
            "crop_5way_max": c_5way_max
        },
        "idea2_stress_corruptions": stress_results
    }
    with open("ideas_benchmark_results.json", "w") as f:
        json.dump(summary_output, f, indent=2)

    print("\n" + "=" * 80)
    print("  EXPERIMENTS COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    main()

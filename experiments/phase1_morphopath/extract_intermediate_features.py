"""
Extract and cache intermediate and final layer representations for DINOv2 and BioCLIP on PlantDoc (5-shot, seed 42).
Captures transformer blocks 7, 8, 9, 10, 11, and 12 (final) via PyTorch forward hooks.
Preserves exact support and query splits and baseline feature alignment.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path("E:/work/research-few-shot")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from PIL import Image

from pipeline.biodino_hierarchical_pipeline import load_backbones, DEVICE
from pipeline.data_engine import load_plantdoc, PairDataset, extract_norm_stats, build_augmentation_pipeline

OUTPUT_DIR = PROJECT_ROOT / "experiments" / "phase1_morphopath"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = OUTPUT_DIR / "plantdoc_intermediate_features_seed42.pt"

LAYERS = [7, 8, 9, 10, 11, 12]  # 1-indexed layer numbers (blocks 6..11)

def build_hook_handlers(models):
    dino_cache = {}
    bio_cache = {}
    handles = []

    for l in LAYERS:
        blk_idx = l - 1  # 0-indexed block

        # DINOv2 hook
        def make_dino_hook(layer_num):
            def hook(module, inp, out):
                # out is [B, 257, 384]
                dino_cache[f"raw_{layer_num}"] = out[:, 0].detach()
                if layer_num == 12:
                    dino_cache[f"norm_{layer_num}"] = models.dino_model.norm(out)[:, 0].detach()
                else:
                    dino_cache[f"norm_{layer_num}"] = models.dino_model.norm(out)[:, 0].detach()
            return hook

        h_d = models.dino_model.blocks[blk_idx].register_forward_hook(make_dino_hook(l))
        handles.append(h_d)

        # BioCLIP hook
        def make_bio_hook(layer_num):
            def hook(module, inp, out):
                # out is [B, 197, 768]
                bio_cache[f"raw_{layer_num}"] = out[:, 0].detach()
                # ln_post + projection
                post_ln = models.bioclip_model.visual.ln_post(out)[:, 0]
                proj_feat = post_ln @ models.bioclip_model.visual.proj
                bio_cache[f"proj_{layer_num}"] = proj_feat.detach()
            return hook

        h_b = models.bioclip_model.visual.transformer.resblocks[blk_idx].register_forward_hook(make_bio_hook(l))
        handles.append(h_b)

    return dino_cache, bio_cache, handles


def extract_and_cache(force: bool = False):
    if CACHE_FILE.exists() and not force:
        print(f"[*] Cache already exists at {CACHE_FILE}. Loading...")
        data = torch.load(CACHE_FILE, map_location="cpu")
        print(f"[*] Loaded keys: {list(data.keys())}")
        return data

    print("[*] Loading PlantDoc (k_shot=5, seed=42)...")
    plantdoc_dir = PROJECT_ROOT / "plantdoc"
    support_samples, query_samples, class_names, prompts = load_plantdoc(plantdoc_dir, k_shot=5, seed=42)
    print(f"[*] Support samples: {len(support_samples)}, Query samples: {len(query_samples)}, Classes: {len(class_names)}")

    print(f"[*] Loading foundation models on {DEVICE}...")
    models = load_backbones(DEVICE)

    dino_cache, bio_cache, handles = build_hook_handlers(models)

    # 1. Extract Support Set Features (8 views per sample: 1 canonical + 7 augmented)
    bioclip_mean, bioclip_std = extract_norm_stats(models.bioclip_transforms)
    aug_bioclip = build_augmentation_pipeline(bioclip_mean, bioclip_std)
    aug_dino = build_augmentation_pipeline(models.dino_config["mean"], models.dino_config["std"])

    print(f"[*] Extracting support features across layers {LAYERS} ({len(support_samples) * 8} total views)...")
    sup_dino_layers = {l: [] for l in LAYERS}
    sup_dino_raw_layers = {l: [] for l in LAYERS}
    sup_bio_proj_layers = {l: [] for l in LAYERS}
    sup_bio_raw_layers = {l: [] for l in LAYERS}
    sup_labels_list = []

    with torch.no_grad():
        for img_idx, (image_path, class_label) in enumerate(support_samples):
            image = Image.open(image_path).convert("RGB")
            bioclip_views = [models.bioclip_transforms(image)] + [aug_bioclip(image) for _ in range(7)]
            dino_views = [models.dino_transforms(image)] + [aug_dino(image) for _ in range(7)]

            bio_batch = torch.stack(bioclip_views).to(DEVICE)
            dino_batch = torch.stack(dino_views).to(DEVICE)

            # Trigger forward pass (hooks populate dino_cache and bio_cache)
            _ = models.bioclip_model.encode_image(bio_batch)
            _ = models.dino_model(dino_batch)

            for l in LAYERS:
                # DINO: layer 12 normed matches official dino_model output
                d_norm = F.normalize(dino_cache[f"norm_{l}"], dim=-1).cpu()
                d_raw = F.normalize(dino_cache[f"raw_{l}"], dim=-1).cpu()
                sup_dino_layers[l].append(d_norm)
                sup_dino_raw_layers[l].append(d_raw)

                # BioCLIP: layer 12 proj matches official encode_image output
                b_proj = F.normalize(bio_cache[f"proj_{l}"], dim=-1).cpu()
                b_raw = F.normalize(bio_cache[f"raw_{l}"], dim=-1).cpu()
                sup_bio_proj_layers[l].append(b_proj)
                sup_bio_raw_layers[l].append(b_raw)

            sup_labels_list.append(torch.full((8,), class_label, dtype=torch.long))

            if (img_idx + 1) % 25 == 0 or (img_idx + 1) == len(support_samples):
                print(f"    Support processed: {img_idx + 1}/{len(support_samples)}")

    sup_dino = {l: torch.cat(sup_dino_layers[l], dim=0) for l in LAYERS}
    sup_dino_raw = {l: torch.cat(sup_dino_raw_layers[l], dim=0) for l in LAYERS}
    sup_bio_proj = {l: torch.cat(sup_bio_proj_layers[l], dim=0) for l in LAYERS}
    sup_bio_raw = {l: torch.cat(sup_bio_raw_layers[l], dim=0) for l in LAYERS}
    sup_labels = torch.cat(sup_labels_list, dim=0)

    # 2. Extract Query Set Features
    print(f"[*] Extracting query features across layers {LAYERS} ({len(query_samples)} queries)...")
    query_dataset = PairDataset(query_samples, models.bioclip_transforms, models.dino_transforms)
    query_loader = DataLoader(query_dataset, batch_size=32, shuffle=False, num_workers=0)

    qry_dino_layers = {l: [] for l in LAYERS}
    qry_dino_raw_layers = {l: [] for l in LAYERS}
    qry_bio_proj_layers = {l: [] for l in LAYERS}
    qry_bio_raw_layers = {l: [] for l in LAYERS}
    qry_labels_list = []

    with torch.no_grad():
        for bio_imgs, dino_imgs, labels in query_loader:
            bio_imgs = bio_imgs.to(DEVICE)
            dino_imgs = dino_imgs.to(DEVICE)

            with torch.autocast(device_type="cuda", dtype=torch.float16):
                _ = models.bioclip_model.encode_image(bio_imgs)
                _ = models.dino_model(dino_imgs)

            for l in LAYERS:
                d_norm = F.normalize(dino_cache[f"norm_{l}"], dim=-1).cpu().float()
                d_raw = F.normalize(dino_cache[f"raw_{l}"], dim=-1).cpu().float()
                qry_dino_layers[l].append(d_norm)
                qry_dino_raw_layers[l].append(d_raw)

                b_proj = F.normalize(bio_cache[f"proj_{l}"], dim=-1).cpu().float()
                b_raw = F.normalize(bio_cache[f"raw_{l}"], dim=-1).cpu().float()
                qry_bio_proj_layers[l].append(b_proj)
                qry_bio_raw_layers[l].append(b_raw)

            qry_labels_list.append(labels)

    qry_dino = {l: torch.cat(qry_dino_layers[l], dim=0) for l in LAYERS}
    qry_dino_raw = {l: torch.cat(qry_dino_raw_layers[l], dim=0) for l in LAYERS}
    qry_bio_proj = {l: torch.cat(qry_bio_proj_layers[l], dim=0) for l in LAYERS}
    qry_bio_raw = {l: torch.cat(qry_bio_raw_layers[l], dim=0) for l in LAYERS}
    qry_labels = torch.cat(qry_labels_list, dim=0)

    # 3. Text Prototypes (BioCLIP text encoder)
    tokens = [models.tokenizer(prompts[c]).to(DEVICE) for c in class_names]
    text_prototypes = []
    with torch.no_grad():
        for tok in tokens:
            tf = F.normalize(models.bioclip_model.encode_text(tok), dim=-1)
            text_prototypes.append(F.normalize(tf.mean(dim=0), dim=-1))
    text_prototypes = torch.stack(text_prototypes).cpu()

    # Remove hooks
    for h in handles:
        h.remove()

    # 4. Verify exact match with baseline Layer 12
    base_file = OUTPUT_DIR / "plantdoc_features_seed42.pt"
    if base_file.exists():
        base_data = torch.load(base_file, map_location="cpu")
        dino_match = torch.allclose(sup_dino[12], base_data["support_dino"], atol=1e-4)
        bio_match = torch.allclose(sup_bio_proj[12], base_data["support_bioclip"], atol=1e-4)
        print(f"[*] Layer 12 Verification vs plantdoc_features_seed42.pt:")
        print(f"    Support DINOv2 L12 match:   {dino_match} (max diff: {(sup_dino[12] - base_data['support_dino']).abs().max():.2e})")
        print(f"    Support BioCLIP L12 match:  {bio_match} (max diff: {(sup_bio_proj[12] - base_data['support_bioclip']).abs().max():.2e})")
        qry_d_match = torch.allclose(qry_dino[12], base_data["query_dino"], atol=1e-3)
        qry_b_match = torch.allclose(qry_bio_proj[12], base_data["query_bioclip"], atol=1e-3)
        print(f"    Query DINOv2 L12 match:     {qry_d_match} (max diff: {(qry_dino[12] - base_data['query_dino']).abs().max():.2e})")
        print(f"    Query BioCLIP L12 match:    {qry_b_match} (max diff: {(qry_bio_proj[12] - base_data['query_bioclip']).abs().max():.2e})")

    payload = {
        # Drop-in baseline keys (Layer 12)
        "support_bioclip": sup_bio_proj[12],
        "support_dino": sup_dino[12],
        "support_labels": sup_labels,
        "query_bioclip": qry_bio_proj[12],
        "query_dino": qry_dino[12],
        "query_labels": qry_labels,
        "class_names": class_names,
        "text_prototypes": text_prototypes,
        "support_samples": support_samples,
        "query_samples": query_samples,
        # Multi-layer features
        "support_dino_layers": sup_dino,
        "support_dino_raw_layers": sup_dino_raw,
        "support_bioclip_proj_layers": sup_bio_proj,
        "support_bioclip_raw_layers": sup_bio_raw,
        "query_dino_layers": qry_dino,
        "query_dino_raw_layers": qry_dino_raw,
        "query_bioclip_proj_layers": qry_bio_proj,
        "query_bioclip_raw_layers": qry_bio_raw,
        "layers": LAYERS,
    }

    torch.save(payload, CACHE_FILE)
    print(f"[OK] Saved intermediate features cache to {CACHE_FILE} (Size: {CACHE_FILE.stat().st_size / 1e6:.2f} MB)")
    return payload

if __name__ == "__main__":
    extract_and_cache(force=True)


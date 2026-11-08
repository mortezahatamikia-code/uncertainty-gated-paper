"""
Extract and cache DINOv2 (384-d) and BioCLIP (512-d) embeddings for PlantDoc (5-shot, seed 42)
Saved strictly inside experiments/phase1_morphopath/ to keep new work completely isolated.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path("E:/work/research-few-shot")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
import numpy as np
from PIL import Image

from pipeline.biodino_hierarchical_pipeline import load_backbones, extract_support_features, DEVICE
from pipeline.data_engine import load_plantdoc, PairDataset

OUTPUT_DIR = PROJECT_ROOT / "experiments" / "phase1_morphopath"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = OUTPUT_DIR / "plantdoc_features_seed42.pt"

def extract_and_cache():
    if CACHE_FILE.exists():
        print(f"[*] Cache already exists at {CACHE_FILE}. Skipping extraction.")
        data = torch.load(CACHE_FILE, map_location="cpu")
        print(f"[*] Loaded keys: {list(data.keys())}")
        return data

    print(f"[*] Loading PlantDoc (k_shot=5, seed=42)...")
    plantdoc_dir = PROJECT_ROOT / "plantdoc"
    support_samples, query_samples, class_names, prompts = load_plantdoc(plantdoc_dir, k_shot=5, seed=42)
    print(f"[*] Support: {len(support_samples)}, Query: {len(query_samples)}, Classes: {len(class_names)}")

    print(f"[*] Loading backbones on {DEVICE}...")
    models = load_backbones(DEVICE)

    # 1. Support features (8 views)
    sup_bio, sup_dino, sup_labels = extract_support_features(support_samples, models, DEVICE)

    # 2. Query features
    query_dataset = PairDataset(query_samples, models.bioclip_transforms, models.dino_transforms)
    query_loader = DataLoader(query_dataset, batch_size=32, shuffle=False, num_workers=0)

    qry_bio_list, qry_dino_list, qry_labels_list = [], [], []
    with torch.no_grad():
        for bio_imgs, dino_imgs, labels in query_loader:
            bio_imgs = bio_imgs.to(DEVICE)
            dino_imgs = dino_imgs.to(DEVICE)
            with torch.autocast(device_type="cuda", dtype=torch.float16):
                bio_feat = F.normalize(models.bioclip_model.encode_image(bio_imgs), dim=-1)
                dino_feat = F.normalize(models.dino_model(dino_imgs), dim=-1)
            qry_bio_list.append(bio_feat.cpu())
            qry_dino_list.append(dino_feat.cpu())
            qry_labels_list.append(labels)

    qry_bio = torch.cat(qry_bio_list, dim=0)
    qry_dino = torch.cat(qry_dino_list, dim=0)
    qry_labels = torch.cat(qry_labels_list, dim=0)

    # 3. Standard text prototypes
    tokens = [models.tokenizer(prompts[c]).to(DEVICE) for c in class_names]
    text_prototypes = []
    with torch.no_grad():
        for tok in tokens:
            tf = F.normalize(models.bioclip_model.encode_text(tok), dim=-1)
            text_prototypes.append(F.normalize(tf.mean(dim=0), dim=-1))
    text_prototypes = torch.stack(text_prototypes).cpu()

    payload = {
        "support_bioclip": sup_bio.cpu(),
        "support_dino": sup_dino.cpu(),
        "support_labels": sup_labels.cpu(),
        "query_bioclip": qry_bio.cpu(),
        "query_dino": qry_dino.cpu(),
        "query_labels": qry_labels.cpu(),
        "class_names": class_names,
        "text_prototypes": text_prototypes,
        "support_samples": support_samples,
        "query_samples": query_samples,
    }

    torch.save(payload, CACHE_FILE)
    print(f"[OK] Saved features cache to {CACHE_FILE} (Size: {CACHE_FILE.stat().st_size / 1e6:.2f} MB)")
    return payload

if __name__ == "__main__":
    extract_and_cache()


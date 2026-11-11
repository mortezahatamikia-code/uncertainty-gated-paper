"""
Experiment script for TASK-OPT-007: Asymmetric Contrastive Symptom Prompts with Dual Negative Margin (IDEA-013)
"""
from __future__ import annotations
import sys
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import numpy as np
import torch
import torch.nn.functional as F
import open_clip
from sklearn.metrics import accuracy_score, f1_score

from pipeline.morphopath_engine import (
    MorphoPathEngine,
    l2_normalize,
    tukey_power_transform,
    center_and_normalize,
    softmax_prob,
    is_healthy_leaf_name,
)
from pipeline.canopy_suppressor import CanopyClutterGlareSuppressor
from experiments.phase1_morphopath.benchmark_phase4_advanced import load_plantdoc_seed42

# 1. Define Negative Symptom Prompts
NEGATIVE_SYMPTOM_PROMPTS = {
    # Generic non-pathological healthy foliage baseline
    "generic_healthy": [
        "Pristine vibrant emerald green leaf blade showing intact continuous cuticle with zero spots or necrosis.",
        "Flawless healthy green foliar lamina with uniform cellular mesophyll and clear smooth veins.",
        "Clean intact vegetative foliage free of lesions, chlorosis, discoloration or blight.",
        "Healthy intact foliage, absence of chlorotic yellow halo, absence of necrotic spots, uniform cellular chlorophyll."
    ],
    # Specific per-disease negative contrast: absence of specific symptoms
    "Apple_Scab_Leaf": [
        "Smooth green apple leaf surface free of dark velvety fungal crusts, scab lesions, or foliar distortion.",
        "Clean apple leaf lamina without diffuse olive-green fungal patches."
    ],
    "Apple_rust_leaf": [
        "Uniform green apple leaf without yellow-orange rust pustules, aecial cups, or chlorotic rings.",
        "Clean apple foliage free of sulfur-yellow spermogonia spots."
    ],
    "Bell_pepper_leaf_spot": [
        "Clean pepper leaf with intact smooth lamina, absence of water-soaked spots, and no dark necrotic specks.",
        "Uniform green capsicum foliage free of bacterial leaf spots."
    ],
    "Corn_Gray_leaf_spot": [
        "Uniform maize leaf blade without rectangular tan blights, absence of vein-bounded gray necrotic streaks.",
        "Clean linear corn leaf free of rectangular foliar blights."
    ],
    "Corn_leaf_blight": [
        "Clean corn foliage without large cigar-shaped elliptical lesions, absence of sprawling tan blights.",
        "Uniform green maize leaf blade free of elongated fungal blights."
    ],
    "Corn_rust_leaf": [
        "Smooth maize leaf surface without reddish-brown powdery rust pustules, absence of ruptured epidermal blisters.",
        "Clean linear corn foliage free of golden-brown urediniospores."
    ],
    "Potato_leaf_early_blight": [
        "Clean potato foliage without concentric target-board rings, absence of zoned dark brown Alternaria spots.",
        "Uniform green potato leaf blade without chlorotic yellow halos or target spots."
    ],
    "Potato_leaf_late_blight": [
        "Clean dry potato leaf without water-soaked greasy necrotic blotches, absence of decaying brown rot or white mold.",
        "Firm intact potato foliage free of Phytophthora late blight rot."
    ],
    "Squash_Powdery_mildew_leaf": [
        "Clean green cucurbit leaf surface without white powdery talc-like patches, absence of fungal mildew carpets.",
        "Vibrant green squash foliage free of powdery fungal colonies."
    ],
    "Tomato_Early_blight_leaf": [
        "Clean tomato foliage without concentric ring target lesions, absence of brown Alternaria target spots.",
        "Uniform green tomato leaflets free of zoned necrotic lesions and yellow halos."
    ],
    "Tomato_Septoria_leaf_spot": [
        "Clean tomato foliage without numerous circular gray spots, absence of dark-rimmed pycnidial flecks.",
        "Uniform green tomato leaflets free of dense punctate Septoria spots."
    ],
    "Tomato_leaf_bacterial_spot": [
        "Clean tomato leaflet surface without water-soaked greasy black angular spots, absence of yellow greasy halos.",
        "Intact tomato foliar lamina free of bacterial specks and coalescing ragged holes."
    ],
    "Tomato_leaf_late_blight": [
        "Firm clean tomato foliage without rapidly expanding greasy purplish-black water-soaked rot or cottony mold.",
        "Intact healthy green tomato leaf tissue free of destructive late blight foliar decay."
    ],
    "Tomato_leaf_mosaic_virus": [
        "Uniformly green flat tomato leaflet without mottled light and dark mosaic patches, absence of blistered foliar distortion.",
        "Smooth non-rugose tomato foliage free of viral mosaic chlorosis."
    ],
    "Tomato_leaf_yellow_virus": [
        "Flat expanded green tomato foliage without upward spoon-like curling or cupping, absence of marginal yellow chlorosis.",
        "Healthy non-stunted tomato leaflets free of upward rolled margins."
    ],
    "Tomato_mold_leaf": [
        "Clean abaxial and adaxial tomato leaf surfaces without velvety olive-brown mold carpets or yellow chlorotic blotches.",
        "Pristine green tomato leaflets free of Passalora fulva fungal mold."
    ],
    "grape_leaf_black_rot": [
        "Clean grape leaf blade without circular reddish-brown necrotic spots, absence of dark margins with black pycnidia.",
        "Uniform lobed grape foliage free of Guignardia black rot leaf spots."
    ],
}


def encode_negative_prompts(class_names):
    cache_path = _PROJECT_ROOT / "experiments" / "phase1_morphopath" / "negative_symptom_prototypes.pt"
    if cache_path.exists():
        print(f"[*] Loading cached negative symptom prototypes from {cache_path}...")
        data = torch.load(cache_path, map_location="cpu")
        return data["proto_gen"], data["neg_protos_class"]

    print("[*] Loading BioCLIP for negative prompt encoding...")
    bioclip_model, _, _ = open_clip.create_model_and_transforms("hf-hub:imageomics/bioclip")
    tokenizer = open_clip.get_tokenizer("hf-hub:imageomics/bioclip")
    bioclip_model = bioclip_model.to("cuda").eval()
    
    # Generic healthy embedding
    tok_gen = tokenizer(NEGATIVE_SYMPTOM_PROMPTS["generic_healthy"]).to("cuda")
    with torch.no_grad():
        emb_gen = F.normalize(bioclip_model.encode_text(tok_gen), dim=-1)
        proto_gen = F.normalize(emb_gen.mean(dim=0), dim=-1).cpu().numpy()
        
    # Class-specific negative embeddings
    neg_protos = []
    with torch.no_grad():
        for c in class_names:
            if c in NEGATIVE_SYMPTOM_PROMPTS:
                prompts = NEGATIVE_SYMPTOM_PROMPTS[c]
                tok = tokenizer(prompts).to("cuda")
                emb = F.normalize(bioclip_model.encode_text(tok), dim=-1)
                proto = F.normalize(emb.mean(dim=0), dim=-1).cpu().numpy()
            else:
                proto = proto_gen
            neg_protos.append(proto)
    neg_protos_class = np.stack(neg_protos)
    torch.save({"proto_gen": proto_gen, "neg_protos_class": neg_protos_class}, cache_path)
    print(f"[*] Saved negative symptom prototypes to {cache_path}")
    return proto_gen, neg_protos_class


def run_benchmark_opt007():
    pd_data = load_plantdoc_seed42()
    class_names = pd_data["class_names"]
    proto_gen, neg_protos_class = encode_negative_prompts(class_names)
    
    sup_joint = np.concatenate([pd_data["sup_bio"], pd_data["sup_dino"]], axis=-1)
    qry_joint = np.concatenate([pd_data["qry_bio"], pd_data["qry_dino"]], axis=-1)
    qry_bio = pd_data["qry_bio"]
    qry_dino = pd_data["qry_dino"]
    qry_labels = pd_data["qry_labels"]
    micro_protos = pd_data["micro_protos"]
    
    # Baseline engine
    engine = MorphoPathEngine(
        bioclip_dim=512, dinov2_dim=384, shrinkage=0.60, router_temp=12.0, vis_temp=15.0,
        text_temp=30.0, w_vis=0.75, margin_penalty=0.05, w_bio=0.65,
        penalized_classes=["Potato_leaf_late_blight"], micro_prototypes=micro_protos,
        class_names=class_names, enable_clutter_suppression=True, gamma_glare=0.15, threshold_glare=0.06,
    ).fit(sup_joint, pd_data["sup_labels"])
    
    m_base = engine.evaluate(qry_joint, qry_labels)
    print("\n" + "=" * 70)
    print(f"Current Baseline (without negative prompts):")
    print(f"  Top-1: {m_base['accuracy_top1']:.2f}%, Top-2: {m_base['accuracy_top2']:.2f}%, F1: {m_base['macro_f1']:.2f}%, FPR: {m_base['fpr']:.2f}%, FNR: {m_base['fnr']:.2f}%")
    print("=" * 70)
    
    healthy_idx = set(i for i, c in enumerate(class_names) if is_healthy_leaf_name(c))
    diseased_idx = set(range(len(class_names))) - healthy_idx
    q_bio_norm = l2_normalize(qry_bio)
    pos_protos_norm = l2_normalize(micro_protos)
    pos_sim = q_bio_norm @ pos_protos_norm.T # (N, K)
    
    # Compute visual similarities exactly as engine does
    qb, qd = tukey_power_transform(qry_bio), tukey_power_transform(qry_dino)
    qbc, _ = center_and_normalize(qb)
    qdc, _ = center_and_normalize(qd)
    sims_rect = engine.w_bio * (qbc @ engine.protos_bio_rect.T) + (1.0 - engine.w_bio) * (qdc @ engine.protos_dino_rect.T)
    sims_rect_margin = sims_rect.copy()
    if engine.penalized_indices:
        sims_rect_margin[:, engine.penalized_indices] -= engine.margin_penalty
    p_vis_m = softmax_prob(sims_rect_margin, temp=engine.vis_temp)

    # Test different eta values and strategies
    eta_values = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]
    
    print("\nStrategy 1: Class-Specific Negative Prompts on Disease Classes Only")
    for eta in eta_values:
        neg_sim = q_bio_norm @ neg_protos_class.T # (N, K)
        mod_sim = pos_sim.copy()
        for c in diseased_idx:
            mod_sim[:, c] -= eta * neg_sim[:, c]
        for c in healthy_idx:
            mod_sim[:, c] += eta * neg_sim[:, c]
                
        p_txt = softmax_prob(mod_sim, temp=30.0)
        p_comb = 0.75 * p_vis_m + 0.25 * p_txt
        p_comb, _ = engine.suppressor.modulate_probabilities(p_comb, qry_bio, class_names)
        
        top1 = p_comb.argmax(axis=-1)
        top2 = np.argsort(p_comb, axis=-1)[:, -2:]
        top2_acc = np.mean([qry_labels[i] in top2[i] for i in range(len(qry_labels))]) * 100.0
        acc = accuracy_score(qry_labels, top1) * 100.0
        f1 = f1_score(qry_labels, top1, average="macro", zero_division=0) * 100.0
        
        diseased_mask = np.array([y not in healthy_idx for y in qry_labels])
        healthy_mask = np.array([y in healthy_idx for y in qry_labels])
        pred_healthy = np.array([y in healthy_idx for y in top1])
        fnr = float(np.sum(diseased_mask & pred_healthy) / max(1, np.sum(diseased_mask)) * 100.0)
        fpr = float(np.sum(healthy_mask & ~pred_healthy) / max(1, np.sum(healthy_mask)) * 100.0)
        print(f"  eta={eta:.2f}: Top-1={acc:.2f}%, Top-2={top2_acc:.2f}%, F1={f1:.2f}%, FPR={fpr:.2f}%, FNR={fnr:.2f}%")

    print("\nStrategy 2: Generic Healthy Negative Prompt Subtracted from Diseases Only")
    for eta in eta_values:
        neg_gen_sim = q_bio_norm @ proto_gen # (N,)
        mod_sim = pos_sim.copy()
        for c in diseased_idx:
            mod_sim[:, c] -= eta * neg_gen_sim
        for c in healthy_idx:
            mod_sim[:, c] += eta * neg_gen_sim
            
        p_txt = softmax_prob(mod_sim, temp=30.0)
        p_comb = 0.75 * p_vis_m + 0.25 * p_txt
        p_comb, _ = engine.suppressor.modulate_probabilities(p_comb, qry_bio, class_names)
        
        top1 = p_comb.argmax(axis=-1)
        top2 = np.argsort(p_comb, axis=-1)[:, -2:]
        top2_acc = np.mean([qry_labels[i] in top2[i] for i in range(len(qry_labels))]) * 100.0
        acc = accuracy_score(qry_labels, top1) * 100.0
        f1 = f1_score(qry_labels, top1, average="macro", zero_division=0) * 100.0
        
        pred_healthy = np.array([y in healthy_idx for y in top1])
        fnr = float(np.sum(diseased_mask & pred_healthy) / max(1, np.sum(diseased_mask)) * 100.0)
        fpr = float(np.sum(healthy_mask & ~pred_healthy) / max(1, np.sum(healthy_mask)) * 100.0)
        print(f"  eta={eta:.2f}: Top-1={acc:.2f}%, Top-2={top2_acc:.2f}%, F1={f1:.2f}%, FPR={fpr:.2f}%, FNR={fnr:.2f}%")


if __name__ == "__main__":
    run_benchmark_opt007()

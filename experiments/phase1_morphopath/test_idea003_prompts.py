"""
Test IDEA-003: Micro-Symptom Textual Prompt Engineering for BioCLIP
Compares standard generic taxonomic prompts vs pathological micro-symptom descriptors
(e.g., pycnidia specks, target-board concentric rings, water-soaked angular halos, olive-green velvety sporulation).
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path("E:/work/research-few-shot")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import torch
import torch.nn.functional as F
from sklearn.metrics import accuracy_score
import open_clip

CACHE_FILE = PROJECT_ROOT / "experiments" / "phase1_morphopath" / "plantdoc_features_seed42.pt"

# Domain-specific micro-symptom descriptors based on cellular necrosis and fungal/bacterial/viral etiology
MICRO_SYMPTOM_PROMPTS = {
    "Apple_Scab_Leaf": [
        "Olive-green to dull dark brown velvety fungal lesions with irregular diffuse borders on leaf blade.",
        "Scabby dark olive necrotic fungal crusts causing foliar distortion and leaf puckering.",
        "Velvety superficial dark olive patches with dendritic branched fungal mycelium on apple leaf."
    ],
    "Apple_leaf": [
        "Pristine vibrant emerald green leaf blade showing intact continuous cuticle with zero spots or necrosis.",
        "Flawless healthy green foliar lamina with uniform cellular mesophyll and clear smooth veins.",
        "Clean intact vegetative foliage free of lesions, chlorosis, discoloration or blight."
    ],
    "Apple_rust_leaf": [
        "Bright sulfur-yellow to vivid orange-red circular chlorotic spots with minute raised fungal spermogonia pustules.",
        "Orange circular rust lesions with tubular fungal aecial cups protruding on lower leaf surface.",
        "Vibrant yellow-orange necrotic rings with small dark fructification centers on leaf blade."
    ],
    "Bell_pepper_leaf": [
        "Pristine glossy deep green foliage with uniform flat lamina and healthy vein architecture.",
        "Flawless emerald pepper leaf with intact smooth leaf margins and no chlorotic or necrotic spots.",
        "Clean healthy vegetative capsicum foliage displaying vibrant cellular pigmentation."
    ],
    "Bell_pepper_leaf_spot": [
        "Small circular to irregular dark brown necrotic lesions with distinct translucent water-soaked halos.",
        "Bacterial leaf spot lesions with sunken necrotic brown centers and prominent chlorotic margins.",
        "Punctate dark brown foliar necrotic specks with yellowish water-soaked margins."
    ],
    "Blueberry_leaf": [
        "Pristine elliptic healthy green leaf blade with smooth margin and vibrant cellular chlorophyll.",
        "Flawless intact vegetative green foliage of blueberry shrub with uniform leaf color.",
        "Clean shiny healthy emerald leaf blade free from foliar decay or lesions."
    ],
    "Cherry_leaf": [
        "Vibrant smooth glossy dark green foliar lamina with finely serrate healthy leaf margins.",
        "Intact flawless cherry leaf blade displaying uniform cellular pigmentation and clear veins.",
        "Clean emerald green vegetative foliage without any lesions, spotting, or viral mottling."
    ],
    "Corn_Gray_leaf_spot": [
        "Narrow rectangular elongated tan to grayish-brown necrotic lesions strictly delimited by leaf veins.",
        "Blocky parallel-sided rectangular gray blight spots bordered by longitudinal venation.",
        "Vein-bounded rectangular lesions with grayish necrotic center and straight linear margins on monocot blade."
    ],
    "Corn_leaf_blight": [
        "Large elliptical to cigar-shaped grayish-green to tan foliar necrotic blights with rounded ends.",
        "Elongated spindle-shaped dry tan blight lesions spreading across multiple leaf veins.",
        "Broad elliptical foliar blight lesions with dark concentric fungal sporulation zones."
    ],
    "Corn_rust_leaf": [
        "Numerous small oval to elongated raised reddish-brown to cinnamon powdery fungal rust pustules.",
        "Ruptured epidermal blisters extruding reddish-golden powdery fungal urediniospores on leaf surface.",
        "Dense scattered orange-brown powdery rust lesions covering linear monocot foliage."
    ],
    "Peach_leaf": [
        "Elongated lanceolate vibrant light green leaf blade with intact smooth lamina and clear midrib.",
        "Flawless vegetative peach foliage with vibrant continuous cuticle and zero discoloration.",
        "Pristine clean green leaf blade with uniform healthy mesophyll and no fungal distortion."
    ],
    "Potato_leaf_early_blight": [
        "Dark brown to black necrotic spots exhibiting conspicuous concentric target-board rings.",
        "Concentric target-like rings within dark circular lesions surrounded by chlorotic yellow halo.",
        "Alternaria target-spot necrosis showing dark zoned ridges like an archery target on leaf blade."
    ],
    "Potato_leaf_late_blight": [
        "Large irregular dark water-soaked grayish-brown necrotic blotches with greasy translucent texture.",
        "Rapidly expanding dark greasy foliar necrosis surrounded by pale chlorotic border with delicate white fungal down.",
        "Water-soaked decaying leaf tissue turning rapidly blackish-brown and papery under humid necrosis."
    ],
    "Raspberry_leaf": [
        "Vibrant green pinnate leaf blade with sharply serrated leaflet margins and uniform chlorophyll.",
        "Clean healthy compound foliage with intact green leaflets and pristine venation.",
        "Flawless vegetative green foliage free from chlorosis, mosaic or anthracnose spots."
    ],
    "Soyabean_leaf": [
        "Healthy trifoliate emerald leaf blade with intact broad ovate leaflets and uniform green pigmentation.",
        "Clean flawless vegetative foliage of soybean with smooth intact cellular cuticle.",
        "Pristine green soybean leaf blade displaying clear reticulate venation with no necrotic lesions."
    ],
    "Squash_Powdery_mildew_leaf": [
        "Superficial white powdery talcum-powder-like fungal patches and mats spreading over the adaxial lamina.",
        "Dense white dusty circular colonies of powdery fungal mycelium covering cucurbit foliage.",
        "Chalky white effuse fungal coating colonizing the entire upper leaf surface."
    ],
    "Strawberry_leaf": [
        "Intact dark green trifoliate foliage with sharp coarse serrations and vigorous glossy lamina.",
        "Flawless healthy green strawberry leaflet with uniform mesophyll and clear branching veins.",
        "Clean vibrant vegetative foliage without leaf spots, scorch or powdery mildew."
    ],
    "Tomato_Early_blight_leaf": [
        "Conspicuous dark brown circular lesions featuring sharp concentric target-board ridges and wide chlorotic halo.",
        "Target-board concentric ring lesions with concentric zoned bands of dead necrotic tissue on tomato leaflets.",
        "Dry brown target-like circular necrotic spots surrounded by bright yellow senescent halo."
    ],
    "Tomato_Septoria_leaf_spot": [
        "Hundreds of tiny circular necrotic spots (1-3mm) with pale grayish-white centers and conspicuous black speck pycnidia.",
        "Small circular lesions with parchment-like gray centers studded with tiny black fungal fruiting bodies (pycnidia).",
        "Dense pinhead-sized circular grayish foliar spots with dark brown margins and micro-pycnidial specks."
    ],
    "Tomato_leaf": [
        "Pristine deeply lobed compound foliage with rich vibrant emerald pigmentation and intact leaf edges.",
        "Flawless healthy tomato leaflets displaying clean cellular cuticle and prominent green veins.",
        "Vigorous clean vegetative tomato foliage free from lesions, spots, yellowing or viral distortion."
    ],
    "Tomato_leaf_bacterial_spot": [
        "Small angular dark brown to black water-soaked lesions delimited by minor veinlets, surrounded by greasy yellow halos.",
        "Angular punctate greasy blackish spots with conspicuous yellow halos on lower and upper leaflet surfaces.",
        "Punctate water-soaked necrotic specks with greasy appearance coalescing into ragged foliar holes."
    ],
    "Tomato_leaf_late_blight": [
        "Extensive rapidly expanding dark water-soaked purplish-black greasy necrotic lesions collapsing leaflet tissue.",
        "Greasy translucent dark foliar rot with pale yellow-green borders and white cottony mildew under moist conditions.",
        "Destructive water-soaked grayish-black foliar blights turning leaves limp, brown and desiccated."
    ],
    "Tomato_leaf_mosaic_virus": [
        "Striking systemic mottled pattern of alternating light green, yellow and dark green blistered patches.",
        "Puckered deformed leaf lamina showing viral mosaic blotches, blistering and distorted fern-like narrow leaflets.",
        "Chlorotic green and yellow mosaic discoloration with uneven surface rugosity and stunted leaf growth."
    ],
    "Tomato_leaf_yellow_virus": [
        "Severe upward leaf curling and cupping into spoon-like shapes with intense bright golden-yellow marginal chlorosis.",
        "Stunted foliage exhibiting severe cup-shaped inward rolling of leaf margins and bright interveinal yellowing.",
        "Pronounced upward curling of leaflet margins with vivid golden chlorosis and thick leathery texture."
    ],
    "Tomato_mold_leaf": [
        "Diffuse pale yellow to greenish chlorotic spots on upper leaf surface corresponding to velvety olive-brown mold beneath.",
        "Fluffy olive-green to yellowish velvety fungal sporulation mats thriving on the lower abaxial leaflet surface.",
        "Conspicuous velvety brownish-green fungal carpet on underside of foliage beneath chlorotic upper patches."
    ],
    "grape_leaf": [
        "Pristine broad palmate-lobed green leaf blade with sharp dentate margin and uniform chlorophyll.",
        "Clean vigorous vitis foliage displaying healthy continuous cuticle and intact palmate venation.",
        "Flawless emerald grape leaf with smooth lamina and zero lesions, measles or blight."
    ],
    "grape_leaf_black_rot": [
        "Small circular to oval reddish-brown to tan necrotic lesions ringed by dark brown borders studded with tiny black pycnidia.",
        "Circular tan spots with distinct dark margin and numerous minute black pepper-like fungal fruiting specks.",
        "Reddish-brown necrotic foliar spots with distinct darker borders and concentric rings of black pycnidial dots."
    ]
}

def main():
    print("=" * 80)
    print("  IDEA-003: Micro-Symptom Textual Prompt Engineering Evaluation")
    print("=" * 80)
    data = torch.load(CACHE_FILE, map_location="cpu")
    qry_bio = data["query_bioclip"].float()
    qry_labels = data["query_labels"]
    class_names = data["class_names"]
    base_text_protos = data["text_prototypes"].float()

    print(f"[*] Loading BioCLIP text tokenizer and encoder on CUDA...")
    bioclip_model, _, _ = open_clip.create_model_and_transforms("hf-hub:imageomics/bioclip")
    tokenizer = open_clip.get_tokenizer("hf-hub:imageomics/bioclip")
    bioclip_model = bioclip_model.to("cuda").eval()

    # Synthesize new micro-symptom prototypes
    print("[*] Synthesizing micro-symptom domain prototypes...")
    micro_prototypes = []
    with torch.no_grad():
        for c in class_names:
            tok = tokenizer(MICRO_SYMPTOM_PROMPTS[c]).to("cuda")
            tf = F.normalize(bioclip_model.encode_text(tok), dim=-1)
            micro_prototypes.append(F.normalize(tf.mean(dim=0), dim=-1).cpu())
    micro_prototypes = torch.stack(micro_prototypes)

    # 1. Zero-shot overall comparison
    base_sim = qry_bio @ base_text_protos.t()
    micro_sim = qry_bio @ micro_prototypes.t()

    acc_base_zs = float(accuracy_score(qry_labels, base_sim.argmax(dim=-1)) * 100.0)
    acc_micro_zs = float(accuracy_score(qry_labels, micro_sim.argmax(dim=-1)) * 100.0)

    print(f"\n[Overall Zero-Shot Accuracy on 252 Field Queries (27 Classes)]")
    print(f"  Baseline Taxonomic Prompts:   {acc_base_zs:.2f}%")
    print(f"  Micro-Symptom Prompts (IDEA-003): {acc_micro_zs:.2f}%")
    print(f"  Gain: +{acc_micro_zs - acc_base_zs:.2f}%")

    # 2. Solanoid / Tomato Multi-Disease Cluster (8 diseases)
    tomato_idx = [i for i, c in enumerate(class_names) if "Tomato" in c]
    tomato_mask = torch.tensor([qry_labels[i].item() in tomato_idx for i in range(len(qry_labels))])
    tomato_targets = qry_labels[tomato_mask].numpy()

    t_base_sim = base_sim[tomato_mask][:, tomato_idx]
    t_micro_sim = micro_sim[tomato_mask][:, tomato_idx]

    t_base_preds = [tomato_idx[p] for p in t_base_sim.argmax(dim=-1)]
    t_micro_preds = [tomato_idx[p] for p in t_micro_sim.argmax(dim=-1)]

    t_acc_base = float(accuracy_score(tomato_targets, t_base_preds) * 100.0)
    t_acc_micro = float(accuracy_score(tomato_targets, t_micro_preds) * 100.0)

    print(f"\n[Fine-Grained Tomato Complex (8 Necrotic Foliar Diseases, {len(tomato_targets)} Images)]")
    print(f"  Baseline Prompts:             {t_acc_base:.2f}%")
    print(f"  Micro-Symptom Prompts (IDEA-003): {t_acc_micro:.2f}%")
    print(f"  Gain on Complex Cluster:      +{t_acc_micro - t_acc_base:.2f}%")

    # 3. Solanoid (Tomato + Potato) Combined (10 classes)
    sol_idx = [i for i, c in enumerate(class_names) if "Tomato" in c or "Potato" in c]
    sol_mask = torch.tensor([qry_labels[i].item() in sol_idx for i in range(len(qry_labels))])
    sol_targets = qry_labels[sol_mask].numpy()

    s_base_preds = [sol_idx[p] for p in base_sim[sol_mask][:, sol_idx].argmax(dim=-1)]
    s_micro_preds = [sol_idx[p] for p in micro_sim[sol_mask][:, sol_idx].argmax(dim=-1)]

    s_acc_base = float(accuracy_score(sol_targets, s_base_preds) * 100.0)
    s_acc_micro = float(accuracy_score(sol_targets, s_micro_preds) * 100.0)

    print(f"\n[Solanoid Archetype Intra-Cluster Zero-Shot (10 Classes, {len(sol_targets)} Images)]")
    print(f"  Baseline Prompts:             {s_acc_base:.2f}%")
    print(f"  Micro-Symptom Prompts (IDEA-003): {s_acc_micro:.2f}%")
    print(f"  Gain on Solanoid Archetype:   +{s_acc_micro - s_acc_base:.2f}%")

    # 4. Impact on Few-Shot Visual-Text Fused Ensemble
    sup_bio = data["support_bioclip"].float()
    sup_dino = data["support_dino"].float()
    sup_labels = data["support_labels"]
    qry_dino = data["query_dino"].float()

    proto_bio = torch.stack([F.normalize(sup_bio[sup_labels == c].mean(dim=0), dim=-1) for c in range(27)])
    proto_dino = torch.stack([F.normalize(sup_dino[sup_labels == c].mean(dim=0), dim=-1) for c in range(27)])

    sim_v_bio = qry_bio @ proto_bio.t()
    sim_v_dino = qry_dino @ proto_dino.t()

    # Base fusion with base text
    fused_base = 0.50 * sim_v_bio + 0.30 * sim_v_dino + 0.20 * base_sim
    fused_micro = 0.50 * sim_v_bio + 0.30 * sim_v_dino + 0.20 * micro_sim

    acc_fused_base = float(accuracy_score(qry_labels, fused_base.argmax(dim=-1)) * 100.0)
    acc_fused_micro = float(accuracy_score(qry_labels, fused_micro.argmax(dim=-1)) * 100.0)

    print(f"\n[Few-Shot Multimodal Ensemble (5-Shot Visual + Text Prototype)]")
    print(f"  Base Multimodal Ensemble:     {acc_fused_base:.2f}%")
    print(f"  Micro-Symptom Ensemble (IDEA-003): {acc_fused_micro:.2f}%")
    print(f"  Overall Few-Shot Gain:        +{acc_fused_micro - acc_fused_base:.2f}%")

    # Save micro prototypes to cache
    out_path = PROJECT_ROOT / "experiments" / "phase1_morphopath" / "micro_symptom_prototypes.pt"
    torch.save({"micro_prototypes": micro_prototypes, "prompts": MICRO_SYMPTOM_PROMPTS}, out_path)
    print(f"\n[OK] Saved micro-symptom prototypes to {out_path}")

if __name__ == "__main__":
    main()


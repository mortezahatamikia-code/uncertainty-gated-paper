"""
BioDINO-Edge: Automated Error Analysis Gallery Generator
=========================================================
Extracts the remaining ~91 misclassified leaf samples across 7,193 test images,
categorizes them by biological failure pattern, and renders a publication-grade
side-by-side visual diagnostic gallery image.
"""

import os
import sys
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# Configure UTF-8 for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

NOVEL_CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight",
    "Grape___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy"
]

SHORT_NAMES = {
    "Apple___Apple_scab": "Apple Scab",
    "Apple___Black_rot": "Apple Black Rot",
    "Apple___Cedar_apple_rust": "Cedar Apple Rust",
    "Apple___healthy": "Apple Healthy",
    "Grape___Black_rot": "Grape Black Rot",
    "Grape___Esca_(Black_Measles)": "Grape Esca",
    "Grape___Leaf_blight": "Grape Leaf Blight",
    "Grape___healthy": "Grape Healthy",
    "Potato___Early_blight": "Potato Early Blight",
    "Potato___Late_blight": "Potato Late Blight",
    "Potato___healthy": "Potato Healthy"
}

def main():
    print("[*] Generating Error Analysis Gallery for BioDINO-Edge...")
    cache_path = os.path.join("cache_artifacts", "pv_novel_embeddings.pt")
    if not os.path.exists(cache_path):
        print("[-] Error: Cache not found.")
        sys.exit(1)

    data = torch.load(cache_path, map_location="cpu", weights_only=False)
    dino_feats = data["dino_feats"]
    bio_feats = data["bio_feats"]
    labels = data["labels"]
    bio_text_protos = data["bio_text_protos"]
    paths = data.get("paths", None)

    if paths is None:
        print("[-] Paths not saved in cache.")
        sys.exit(1)

    # 1. Calibrate 5-shot support set
    support_idx = []
    query_idx = []
    for c in range(len(NOVEL_CLASSES)):
        c_idx = (labels == c).nonzero().squeeze()
        support_idx.extend(c_idx[:5].tolist())
        query_idx.extend(c_idx[5:].tolist())

    s_b = bio_feats[support_idx]
    s_d = dino_feats[support_idx]
    s_concat = torch.cat([s_b, s_d], dim=-1).numpy()
    s_y = labels[support_idx].numpy()

    lda_clf = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')
    lda_clf.fit(s_concat, s_y)

    # 2. Evaluate query set
    q_b = bio_feats[query_idx]
    q_d = dino_feats[query_idx]
    q_y = labels[query_idx].numpy()
    q_paths = [paths[i] for i in query_idx]

    # Fisher-LDA prediction
    q_concat = torch.cat([q_b, q_d], dim=-1).numpy()
    prob_lda = torch.tensor(lda_clf.predict_proba(q_concat))
    lgt_t = 20.0 * (q_b @ bio_text_protos.t())
    prob_t = F.softmax(lgt_t, dim=-1)
    final_probs = 0.75 * prob_lda + 0.25 * prob_t
    preds = final_probs.argmax(dim=-1).numpy()

    # Find errors
    error_mask = (preds != q_y)
    error_indices = np.where(error_mask)[0]
    total_errors = len(error_indices)
    total_queries = len(q_y)
    acc = (1.0 - total_errors / total_queries) * 100.0

    print(f"[*] Total Test Queries: {total_queries}")
    print(f"[*] Total Correct:      {total_queries - total_errors}")
    print(f"[*] Total Errors:       {total_errors} (Accuracy: {acc:.2f}%)")

    # 3. Select 12 Diverse Representative Error Cases
    # Categorize errors
    error_groups = {}
    for idx in error_indices:
        true_c = q_y[idx]
        pred_c = preds[idx]
        pair = (true_c, pred_c)
        if pair not in error_groups:
            error_groups[pair] = []
        error_groups[pair].append(idx)

    selected_indices = []
    # Prioritize top error pairs (Black rot vs Esca, Scab vs Black rot, etc.)
    sorted_pairs = sorted(error_groups.keys(), key=lambda p: len(error_groups[p]), reverse=True)
    for pair in sorted_pairs:
        # take up to 2-3 per pair
        samples = error_groups[pair][:2]
        selected_indices.extend(samples)
        if len(selected_indices) >= 12:
            break
    selected_indices = selected_indices[:12]

    # 4. Render 3x4 Matplotlib Grid
    fig, axes = plt.subplots(3, 4, figsize=(16, 12))
    fig.suptitle(f"BioDINO-Edge: Visual Dissection of Representative Error Cases ({total_errors} errors / {total_queries} test leaves)",
                 fontsize=16, fontweight='bold', y=0.98)

    os.makedirs(os.path.join("docs", "assets"), exist_ok=True)

    for i, ax in enumerate(axes.flat):
        if i < len(selected_indices):
            err_idx = selected_indices[i]
            img_path = q_paths[err_idx]
            true_label = SHORT_NAMES[NOVEL_CLASSES[q_y[err_idx]]]
            pred_label = SHORT_NAMES[NOVEL_CLASSES[preds[err_idx]]]
            conf = final_probs[err_idx, preds[err_idx]].item() * 100.0

            try:
                img = Image.open(img_path).convert("RGB")
                ax.imshow(img)
            except Exception:
                ax.text(0.5, 0.5, "Image Missing", ha='center')

            title_text = f"True: {true_label}\nPred: {pred_label} ({conf:.1f}%)"
            ax.set_title(title_text, fontsize=11, fontweight='bold',
                         color='darkred' if 'Healthy' in true_label else 'navy')
            ax.axis('off')
            
            # Draw decorative border
            for spine in ax.spines.values():
                spine.set_edgecolor('red')
                spine.set_linewidth(2)
        else:
            ax.axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    output_path = os.path.join("docs", "assets", "error_analysis_gallery.png")
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"\n[+] High-Resolution Gallery successfully rendered and saved to:\n    -> {output_path}")

if __name__ == "__main__":
    main()

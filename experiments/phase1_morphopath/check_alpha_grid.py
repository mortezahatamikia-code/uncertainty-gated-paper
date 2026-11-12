import sys
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import torch
import numpy as np
from pipeline_morphopath.morphopath_engine import MorphoPathEngine

data = torch.load(_PROJECT_ROOT / "experiments" / "phase1_morphopath" / "plantdoc_features_seed42.pt", map_location="cpu")
micro = torch.load(_PROJECT_ROOT / "experiments" / "phase1_morphopath" / "micro_symptom_prototypes.pt", map_location="cpu")

sj = np.concatenate([data["support_bioclip"].float().numpy(), data["support_dino"].float().numpy()], axis=-1)
qj = np.concatenate([data["query_bioclip"].float().numpy(), data["query_dino"].float().numpy()], axis=-1)
sy = data["support_labels"].numpy()
qy = data["query_labels"].numpy()
classes = data["class_names"]
micro_p = micro["micro_prototypes"].float().numpy()

for a in [0.0, 0.02, 0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20]:
    eng = MorphoPathEngine(
        w_bio=0.65, enable_clutter_suppression=True, alpha_bilinear=a,
        micro_prototypes=micro_p, class_names=classes,
    ).fit(sj, sy)
    m = eng.evaluate(qj, qy)
    print(f"alpha={a:4.2f}: Top-1={m['accuracy_top1']:.2f}%, Top-2={m['accuracy_top2']:.2f}%, F1={m['macro_f1']:.2f}%, FPR={m['fpr']:.2f}%")

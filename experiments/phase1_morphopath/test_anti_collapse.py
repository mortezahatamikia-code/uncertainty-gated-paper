"""
Test IDEA-024: Intra-Genus Contrastive Anti-Collapse Projection Head
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import accuracy_score, f1_score

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from experiments.phase1_morphopath.benchmark_phase4_advanced import load_plantdoc_seed42

# Define CosFace / ArcFace margin loss
class CosFaceLoss(nn.Module):
    def __init__(self, in_features: int, num_classes: int, s: float = 20.0, m: float = 0.25):
        super().__init__()
        self.in_features = in_features
        self.num_classes = num_classes
        self.s = s
        self.m = m
        self.weight = nn.Parameter(torch.FloatTensor(num_classes, in_features))
        nn.init.xavier_uniform_(self.weight)

    def forward(self, input: torch.Tensor, label: torch.Tensor) -> torch.Tensor:
        cosine = F.linear(F.normalize(input), F.normalize(self.weight))
        one_hot = torch.zeros_like(cosine)
        one_hot.scatter_(1, label.view(-1, 1), 1.0)
        output = self.s * (cosine - one_hot * self.m)
        return F.cross_entropy(output, label)

class AntiCollapseHead(nn.Module):
    def __init__(self, in_dim: int = 896, hidden_dim: int = 512, out_dim: int = 256):
        super().__init__()
        self.fc1 = nn.Linear(in_dim, hidden_dim, bias=False)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.relu = nn.ReLU(inplace=True)
        self.fc2 = nn.Linear(hidden_dim, out_dim, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.relu(self.bn1(self.fc1(x)))
        out = self.fc2(h)
        return F.normalize(out, p=2, dim=-1)

class LinearAntiCollapseHead(nn.Module):
    def __init__(self, in_dim: int = 896, out_dim: int = 512):
        super().__init__()
        self.fc = nn.Linear(in_dim, out_dim, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.normalize(self.fc(x), p=2, dim=-1)

def test_anti_collapse():
    pd = load_plantdoc_seed42()
    class_names = pd["class_names"]
    n_classes = len(class_names)
    
    # Joint support and query
    sup_joint = torch.from_numpy(np.concatenate([pd["sup_bio"], pd["sup_dino"]], axis=-1)).float()
    qry_joint = torch.from_numpy(np.concatenate([pd["qry_bio"], pd["qry_dino"]], axis=-1)).float()
    sup_y = torch.from_numpy(pd["sup_labels"]).long()
    qry_y = pd["qry_labels"]

    print(f"Support set: {sup_joint.shape}, Query set: {qry_joint.shape}")

    # Test different setups
    device = torch.device("cpu") # Must train and run on CPU for edge benchmark verification
    torch.manual_seed(42)

    for arch in ["linear", "mlp"]:
        for out_dim in [256, 384, 512]:
            for margin in [0.15, 0.25, 0.35]:
                for lr in [1e-3, 3e-3]:
                    if arch == "linear":
                        model = LinearAntiCollapseHead(in_dim=896, out_dim=out_dim).to(device)
                    else:
                        model = AntiCollapseHead(in_dim=896, hidden_dim=512, out_dim=out_dim).to(device)
                    
                    criterion = CosFaceLoss(in_features=out_dim, num_classes=n_classes, s=20.0, m=margin).to(device)
                    optimizer = optim.Adam(list(model.parameters()) + list(criterion.parameters()), lr=lr, weight_decay=1e-4)

                    # Quick train loop (50 epochs)
                    dataset = TensorDataset(sup_joint, sup_y)
                    loader = DataLoader(dataset, batch_size=128, shuffle=True)
                    
                    t0 = time.perf_counter()
                    model.train()
                    for epoch in range(40):
                        for bx, by in loader:
                            bx, by = bx.to(device), by.to(device)
                            optimizer.zero_grad()
                            z = model(bx)
                            loss = criterion(z, by)
                            loss.backward()
                            optimizer.step()
                    train_time = time.perf_counter() - t0

                    # Evaluate
                    model.eval()
                    with torch.no_grad():
                        z_sup = model(sup_joint)
                        # Compute class prototypes
                        protos = torch.zeros(n_classes, out_dim)
                        for c in range(n_classes):
                            mask = (sup_y == c)
                            if mask.any():
                                protos[c] = z_sup[mask].mean(dim=0)
                        protos = F.normalize(protos, p=2, dim=-1)

                        # Inference timing
                        t_inf0 = time.perf_counter()
                        z_qry = model(qry_joint)
                        sims = torch.mm(z_qry, protos.t())
                        preds = sims.argmax(dim=-1).cpu().numpy()
                        t_inf1 = time.perf_counter()
                        inf_latency_per_sample = (t_inf1 - t_inf0) / len(qry_y) * 1000.0

                    acc = accuracy_score(qry_y, preds) * 100.0
                    f1 = f1_score(qry_y, preds, average="macro", zero_division=0) * 100.0
                    if acc >= 64.0:
                        print(f"[{arch.upper()}] out={out_dim}, m={margin:.2f}, lr={lr:.3f} | Train: {train_time:.2f}s | Latency: {inf_latency_per_sample:.4f} ms | Top-1: {acc:.2f}%, F1: {f1:.2f}%")

if __name__ == "__main__":
    test_anti_collapse()

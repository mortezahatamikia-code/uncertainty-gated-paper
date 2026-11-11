"""
Test Bilinear Gating across PlantDoc seeds if other seeds exist or inspect available PlantDoc caches.
"""
from __future__ import annotations
import sys
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# Check what other PlantDoc cache files exist
for p in (_PROJECT_ROOT / "experiments" / "phase1_morphopath").glob("*.pt"):
    print(p.name)
for p in (_PROJECT_ROOT / "experiments" / "phase3_morphopath").glob("*.pt"):
    print(p.name)


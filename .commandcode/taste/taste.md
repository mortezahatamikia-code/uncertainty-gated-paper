# Taste

- Prefers artifact/footprint sizes (APK, model binaries) reported as approximate values (`≈`, one decimal) with an explicit unit definition (e.g. MiB = 2^20 bytes), while accuracy/F1/FNR/latency stay exact with ± and CIs. Confidence: 0.7
- Wants reported numbers regenerated from real builds (re-export models, rebuild the APK) and verified before they are written into documents, rather than reusing existing figures. Confidence: 0.6
- Wants deliverable folders to be self-documenting: a README.md inside the folder that explains what each file is for, which stage it belongs to, where/when each is used, with citations to the official, current source (with access date). Confidence: 0.6
- Treats reproducibility as a binding contract: library defaults should equal the published paper's values so a no-argument call reproduces the headline result, and if a reproduction test disagrees the defaults are corrected rather than the test loosened ("the paper number is the reference"). Confidence: 0.55
- Expects claims in deliverables to be verified against primary sources rather than trusted from memory — e.g. asking for every newly added bibliography entry to be checked as real (with correct authors/pages/year) and for duplicates/no-citation entries to be swept before submission. Confidence: 0.6

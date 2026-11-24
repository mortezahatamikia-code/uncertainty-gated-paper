import re
import glob

files = [
    "paper/sections/00_frontmatter.tex",
    "paper/sections/01_introduction.tex",
    "paper/sections/02_related_work.tex",
    "paper/sections/03_problem_formulation.tex",
    "paper/sections/03_methodology.tex",
    "paper/sections/04_experimental_setup.tex",
    "paper/sections/05_results.tex",
    "paper/sections/08_discussion.tex",
    "paper/sections/09_conclusion.tex",
    "paper/sections/10_appendix.tex"
]

# Pattern for Definition: "Full Name (ACRONYM)" or "Full Name [ACRONYM]"
def_pattern = re.compile(r'([A-Za-z0-9\s\-]{3,40})\s*[\(\[]([A-Z][A-Z0-9]{1,8})[\)\]]')

# Also search for standalone acronyms
acr_pattern = re.compile(r'\b([A-Z]{2,8})\b')

print("--- DEFINITIONS FOUND ---")
definitions = {}
for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    matches = def_pattern.findall(content)
    for full, acr in matches:
        full_clean = " ".join(full.strip().split())
        if len(full_clean.split()) <= 6 and not any(w in full_clean.lower() for w in ["see", "table", "fig", "eq", "section", "ref"]):
            definitions.setdefault(acr, []).append((fpath, full_clean))

for acr, locs in sorted(definitions.items()):
    print(f"{acr}: {locs}")

print("\n--- FIRST USE vs DEFINITIONS ---")
first_uses = {}
for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines, 1):
        for acr in acr_pattern.findall(line):
            if acr not in first_uses:
                first_uses[acr] = (fpath, idx, line.strip())

# Ignore standard LaTeX commands or bib words
ignore = {"AND", "THE", "FOR", "NOT", "WITH", "ALL", "NEW", "OR", "IN", "ON", "TO", "OF", "BY", "AN", "AS", "AT", "IS", "IT", "NO", "SO", "DO", "IF", "UP", "MY", "US", "AM", "PM", "OK", "TV"}

for acr, (fpath, line_no, line_text) in sorted(first_uses.items()):
    if acr in ignore:
        continue
    is_def = acr in definitions
    print(f"{acr:8s} | First use: {fpath}:{line_no} | Defined: {is_def}")
    if is_def:
        for def_file, def_name in definitions[acr]:
            print(f"         Def in {def_file}: '{def_name}'")

# -*- coding: utf-8 -*-
"""Verify final PDF numbers: new canonical values present, stale values absent."""
import re
from pathlib import Path

PDF = Path(__file__).resolve().parent.parent.parent / "paper" / "main_eaai_elsarticle.pdf"

from pypdf import PdfReader
text = " ".join(page.extract_text() or "" for page in PdfReader(str(PDF)).pages)

text = re.sub(r"\s+", " ", text)
new = ["97.41", "98.67", "98.06", "0.702", "96.05", "94.83", "97.45",
       "2.33", "87.26", "92.60", "0.021", "51.9", "0.839", "98.15",
       "0.968", "0.982", "0.974", "11.57", "2.11"]
stale = ["97.37", "98.72", "0.604", "96.76", "98.32", "97.64",
         "85.42", "92.27", "0.011", "58.6", "97.368"]
print("NEW present:")
for n in new:
    print(f"  {n}: {'OK' if n in text else 'MISSING!'}")
print("STALE absent:")
for s in stale:
    print(f"  {s}: {'OK' if s not in text else 'STILL PRESENT!'}")
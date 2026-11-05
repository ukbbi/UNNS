#!/usr/bin/env python3
"""Generate all 15 figures of Paper I v0.2 and results/FIGURE_DATA.json (exact input records)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib, figs_a, figs_b, figs_c
figs_a.run(); figs_b.run(); figs_c.run()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "FIGURE_DATA.json")
json.dump(figlib.DATA, open(out, "w"), indent=1, default=str)
print("figures:", len([f for f in os.listdir(figlib.OUT) if f.endswith(".pdf")]), "records:", len(figlib.DATA))

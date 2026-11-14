#!/usr/bin/env python3
"""Recompute every sha256 listed in MANIFEST.json (run from the package root or anywhere)."""
import hashlib, json, os, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = json.load(open(os.path.join(root, "MANIFEST.json")))
bad = [p for p, h in m.items() if not os.path.exists(os.path.join(root, p)) or hashlib.sha256(open(os.path.join(root, p), "rb").read()).hexdigest() != h]
print(len(m), "entries;", "ALL MATCH" if not bad else "MISMATCH: " + ", ".join(bad))
sys.exit(1 if bad else 0)

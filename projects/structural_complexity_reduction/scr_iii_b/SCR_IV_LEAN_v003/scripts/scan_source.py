#!/usr/bin/env python3
"""Fail if any Lean source (outside comments) uses sorry, admit, axiom, native_decide, opaque/implemented_by. usage: scan_source.py ROOT"""
import re, sys, pathlib
bad = []
for f in sorted(pathlib.Path(sys.argv[1]).glob("SCR_IV_*.lean")) + sorted(pathlib.Path(sys.argv[1]).glob("tests/*.lean")):
    s = f.read_text(); s = re.sub(r"/-.*?-/", "", s, flags=re.S); s = re.sub(r"--[^\n]*", "", s)
    for m in re.finditer(r"\b(sorry|admit|axiom|native_decide|implemented_by|extern|unsafe|opaque)\b", s):
        bad.append((f.name, m.group(1)))
print("forbidden tokens outside comments:", bad if bad else "none")
sys.exit(1 if bad else 0)

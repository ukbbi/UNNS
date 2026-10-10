#!/usr/bin/env python3
"""Write one Lean file per frontier prefix: theorem  subOK Rreal 40 U leaf D0 b cert = true := by decide +kernel  (untrusted certificate data).
usage: mk_lean.py ROOT CERTDIR OBJ D0 OUTDIR b1 b2 ...   (OBJ: ground|nong|nongT)"""
import sys, pathlib
sys.set_int_max_str_digits(0)
ROOT, CD, OBJ, D0, OUT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3], int(sys.argv[4]), pathlib.Path(sys.argv[5]); OUT.mkdir(parents=True, exist_ok=True)
cs = (CD/f"cert_{OBJ}_D{D0}.txt").read_text().split()
U, leaf = {"ground": ("claimedGroundNum", "(fun _ => false)"), "nong": ("claimedNonGNum", "leafGrammar"), "nongT": ("claimedNonGTrue", "leafGrammar")}[OBJ]
for b in map(int, sys.argv[6:]):
    (OUT/f"{OBJ}_{b}.lean").write_text(f"import SCR_IV_V4\nopen SCR_IV\ntheorem p_{OBJ}_{b} : subOK Rreal 40 {U} {leaf} {D0} {b} {cs[b]} = true := by decide +kernel\n")

#!/usr/bin/env python3
"""
Verify the reproduced C003 result against the historical one-shot quantitative lock
using the ACTUAL project layout.

The script auto-detects the project root from its own file location.
"""
from pathlib import Path
import hashlib, re, sys

def find_project_root():
    """
    Script lives at:
      <root>/06_VALIDATION/C003_FINAL_v001/<script>.py
    Therefore parents[2] is the actual UNNS_MULTI_CLOCK_RECURRENCE root.
    """
    here = Path(__file__).resolve()
    root = here.parents[2]
    required = [
        root / "05_METHODS" / "rep_study_v002.py",
        root / "05_METHODS" / "grammar_dev_v001.py",
        root / "05_METHODS" / "mc_grammar_v001.py",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise SystemExit(
            "Could not resolve UNNS_MULTI_CLOCK_RECURRENCE root from script location.\n"
            "Missing:\n  " + "\n  ".join(missing)
        )
    return root


ROOT=find_project_root()
HIST=ROOT/"08_OUTPUTS"/"C003_FINAL_v001"/"C003_FINAL_QUANT_SHA256.txt"
REPRO=ROOT/"08_OUTPUTS"/"C003_FINAL_v001"/"REPRO"

if not HIST.exists():
    raise SystemExit(f"Missing historical quantitative lock: {HIST}")

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):
            h.update(chunk)
    return h.hexdigest()

expected={}
for line in HIST.read_text(encoding="utf-8").splitlines():
    m=re.match(r"^([0-9a-f]{64})\s+(.+)$",line.strip())
    if m:
        expected[Path(m.group(2)).name]=m.group(1)

checks={
    "C003_FINAL_RESULTS.csv":REPRO/"C003_FINAL_RESULTS.csv",
    "C003_FINAL_RESULTS.json":REPRO/"C003_FINAL_RESULTS.json",
    "TC_P01_C003_DETAIL.json":REPRO/"TC_P01_C003_DETAIL.json",
    "TC_P01_C003_CTRL_DETAIL.json":REPRO/"TC_P01_C003_CTRL_DETAIL.json",
}

ok=True
for name,p in checks.items():
    if not p.exists():
        print(name, "MISSING")
        ok=False
        continue
    got=sha256(p)
    exp=expected.get(name)
    match=(got==exp)
    ok &= match
    print(name, "MATCH" if match else "MISMATCH")
    print("  expected:",exp)
    print("  got:     ",got)

if not ok:
    sys.exit(1)

print("PASS: regenerated C003 artifacts match the historical one-shot quantitative lock.")

#!/usr/bin/env python3
"""
Compare regenerated P001 artifacts with the historical locked artifacts.

Run after generate_P001.py and run_P001_blind.py:

    python 06_VALIDATION/PROSPECTIVE_P01/verify_P001.py

The script compares the canonical numerical CSVs against historical hashes
recorded in the project.
"""
from pathlib import Path
import hashlib, re, sys

ROOT = Path(".").resolve()

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

historical_receipt = (
    ROOT / "08_OUTPUTS" / "PROSPECTIVE_P01" / "BLIND_QUANT_LOCK_SHA256.txt"
)
if not historical_receipt.exists():
    raise SystemExit("Historical BLIND_QUANT_LOCK_SHA256.txt is missing.")

expected = {}
for line in historical_receipt.read_text().splitlines():
    m = re.match(r"^([0-9a-f]{64})\s+(.+)$", line.strip())
    if m:
        expected[Path(m.group(2)).name] = m.group(1)

checks = {
    "P001_A.csv":
        ROOT / "06_VALIDATION" / "PROSPECTIVE_P01" / "INGEST" / "P001_A.csv",
    "P001_B.csv":
        ROOT / "06_VALIDATION" / "PROSPECTIVE_P01" / "INGEST" / "P001_B.csv",
    "BLIND_RESULTS.csv":
        ROOT / "08_OUTPUTS" / "PROSPECTIVE_P01" / "REPRO_BLIND" / "BLIND_RESULTS.csv",
    "BLIND_ROBUSTNESS.csv":
        ROOT / "08_OUTPUTS" / "PROSPECTIVE_P01" / "REPRO_BLIND" / "BLIND_ROBUSTNESS.csv",
    "P001_A_DETAIL.json":
        ROOT / "08_OUTPUTS" / "PROSPECTIVE_P01" / "REPRO_BLIND" / "P001_A_DETAIL.json",
    "P001_B_DETAIL.json":
        ROOT / "08_OUTPUTS" / "PROSPECTIVE_P01" / "REPRO_BLIND" / "P001_B_DETAIL.json",
}

ok = True
for name, p in checks.items():
    got = sha256(p)
    exp = expected.get(name)
    match = got == exp
    ok &= match
    print(f"{name}: {'MATCH' if match else 'MISMATCH'}")
    print("  expected:", exp)
    print("  got:     ", got)

if not ok:
    sys.exit(1)
print("PASS: regenerated artifacts match the historical blind quantitative lock.")

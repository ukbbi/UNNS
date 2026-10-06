#!/usr/bin/env python3
"""YM-3B frozen batch entry point.

This stage uses the frozen CORR-I v0.1.2 numerical mirror already stored at:
    scripts/ym3/run_corr_i.py

Inputs:
    data/derived/corr_i/ym3b/ss23/common/
    data/derived/corr_i/ym3b/ss23/common_pchip/
    data/derived/corr_i/ym3b/ss23/digitized/
    data/derived/corr_i/ym3b/matched_gamma/

The canonical frozen run outputs are already recorded under output/ym3b/ and docs/YM3B_RESULT.*.
Use this file as the project entry-point record; do not change CORR-I mathematics.
"""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[2]
CH=ROOT/"chambers"/"corr_i"/"corr_i_v012.html"
EXPECTED="f972c9d460cebc19ef165e66c03f971411062eba093876406ed2efe614e2deb2"
got=hashlib.sha256(CH.read_bytes()).hexdigest()
if got != EXPECTED:
    raise SystemExit(f"CORR-I hash mismatch: {got}")
print("CORR-I v0.1.2 hash: PASS")
print("Frozen YM-3B result record:", ROOT/"docs"/"YM3B_RESULT.md")
print("Machine-readable summary:", ROOT/"output"/"ym3b"/"YM3B_SUMMARY.csv")

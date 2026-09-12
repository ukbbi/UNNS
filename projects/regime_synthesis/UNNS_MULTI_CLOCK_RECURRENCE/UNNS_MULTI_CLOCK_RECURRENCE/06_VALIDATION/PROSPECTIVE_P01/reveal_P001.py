#!/usr/bin/env python3
"""
Verify the original P001 A/B commitment and bind reproduced blind results
to the post-reveal identities.

Run from project root:

    python 06_VALIDATION/PROSPECTIVE_P01/reveal_P001.py

Reads:
    06_VALIDATION/PROSPECTIVE_P01/P001_PAIR_LOCK.json
    08_OUTPUTS/PROSPECTIVE_P01/REVEAL/P001_REVEAL_KEY.json
    08_OUTPUTS/PROSPECTIVE_P01/REPRO_BLIND/BLIND_RESULTS.csv
"""
from pathlib import Path
import json, hashlib
import pandas as pd

ROOT = Path(".").resolve()
VAL = ROOT / "06_VALIDATION" / "PROSPECTIVE_P01"
REV = ROOT / "08_OUTPUTS" / "PROSPECTIVE_P01" / "REVEAL"
REPRO = ROOT / "08_OUTPUTS" / "PROSPECTIVE_P01" / "REPRO_BLIND"
OUT = ROOT / "08_OUTPUTS" / "PROSPECTIVE_P01" / "REPRO_REVEAL"
OUT.mkdir(parents=True, exist_ok=True)

lock = json.loads((VAL / "P001_PAIR_LOCK.json").read_text())
key = json.loads((REV / "P001_REVEAL_KEY.json").read_text())

payload = json.dumps(
    {"salt": key["salt"], "mapping": key["mapping"]},
    sort_keys=True, separators=(",", ":")
)
recomputed = hashlib.sha256(payload.encode()).hexdigest()
expected = lock["blind_assignment"]["mapping_commitment_sha256"]
if recomputed != expected:
    raise RuntimeError("Commitment verification failed.")

blind = pd.read_csv(REPRO / "BLIND_RESULTS.csv")
blind["revealed_identity"] = blind["id"].map(key["mapping"])

def expectation(identity):
    if identity == "HIGH_FREQ_CANDIDATE_HYPOTHESIS":
        return "EXPECTED_TEMPORAL_CORE_SUPPORTED"
    return "EXPECTED_NOT_TEMPORAL_CORE_SUPPORTED"

blind["predeclared_expectation"] = blind["revealed_identity"].map(expectation)
blind["expectation_met"] = [
    state == "TEMPORAL_CORE_SUPPORTED"
    if exp == "EXPECTED_TEMPORAL_CORE_SUPPORTED"
    else state != "TEMPORAL_CORE_SUPPORTED"
    for state, exp in zip(blind["temporal_state"], blind["predeclared_expectation"])
]

blind.to_csv(OUT / "P001_REVEALED_RESULTS.csv", index=False)
(OUT / "P001_REVEAL_VERIFICATION.json").write_text(json.dumps({
    "commitment_expected": expected,
    "commitment_recomputed": recomputed,
    "commitment_verified": True,
    "mapping": key["mapping"],
}, indent=2))

print("Commitment verified:", True)
print(blind.to_string(index=False))

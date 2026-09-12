from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys

EXPECTED_SOURCE_SHA256 = "977e6ab3c437252395dc7f7185af1829619fe1eec754f59f5f3ceae2ca0b969f"
EXPECTED_SELECTION_SHA256 = "385cca0a0b28ac3b17f757ef3b7fcfe2c1954423ceb5376b927b67633a40875e"

def sha256_file(path: Path, block=16*1024*1024):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(block), b""):
            h.update(b)
    return h.hexdigest()

def find_root(start: Path):
    for p in [start.resolve()] + list(start.resolve().parents):
        if (p/"MANIFEST.json").exists() and (p/"outputs").exists():
            return p
    raise RuntimeError("Project root not found.")

def main():
    root = find_root(Path(__file__).resolve().parent)
    print("PILOT B ADAPTER RESULT - FINAL VERIFICATION")
    print("project root :", root)

    rec_path = root/"outputs/records/pilot_b/PILOT_B_ADAPTER_RUN.json"
    if not rec_path.exists():
        raise RuntimeError(f"Missing canonical run record: {rec_path}")
    rec = json.loads(rec_path.read_text(encoding="utf-8-sig"))

    if rec.get("status") != "COMPLETE_READY_FOR_STRUC_ROUTE_I":
        raise RuntimeError(f"Unexpected run status: {rec.get('status')}")
    print("[PASS] run status: COMPLETE_READY_FOR_STRUC_ROUTE_I")

    src = rec.get("source", {})
    if src.get("sha256") != EXPECTED_SOURCE_SHA256:
        raise RuntimeError("Pilot-B source SHA-256 mismatch in run record.")
    if src.get("selection_sha256") != EXPECTED_SELECTION_SHA256:
        raise RuntimeError("Pilot-B selection SHA-256 mismatch in run record.")
    print("[PASS] source and frozen-selection identities match")

    expected_paths = {
        "objects": root/rec["outputs"]["derived_objects"],
        "relations": root/rec["outputs"]["derived_relations"],
        "manifest": root/rec["outputs"]["route_project"]/"manifest.json",
        "route_bundle": root/rec["outputs"]["route_bundle"],
        "phys_stats": root/rec["outputs"]["phys_stats"],
        "raw_adapter_report": root/rec["outputs"]["raw_adapter_report"],
        "canonical_adapter_report": root/rec["outputs"]["canonical_adapter_report"],
    }

    for key, p in expected_paths.items():
        if not p.exists():
            raise RuntimeError(f"Missing {key}: {p}")
        print(f"[PASS] exists: {key}")

    hashes = rec.get("hashes", {})
    for key in ("objects","relations","manifest","route_bundle","phys_stats"):
        got = sha256_file(expected_paths[key])
        exp = hashes.get(key)
        if got != exp:
            raise RuntimeError(f"Hash mismatch for {key}: expected {exp}, got {got}")
        print(f"[PASS] SHA-256: {key}")

    raw_report = json.loads(expected_paths["raw_adapter_report"].read_text(encoding="utf-8-sig"))
    if raw_report.get("status") != "COMPLETE":
        raise RuntimeError("Raw frozen-adapter report is not COMPLETE.")
    result = raw_report.get("result", {})
    print(f"[PASS] raw adapter report: COMPLETE")
    if result:
        print("        objects             :", result.get("objects"))
        print("        relation candidates :", result.get("relation_candidates"))

    print()
    print("[VERIFIED] Pilot-B adapter result is complete and canonical.")
    print("The prior WinError 5 occurred only while deleting temporary PB_STAGE after")
    print("canonicalization. Do NOT rerun the adapter. Proceed to STRUC-ROUTE-I v0.1.2.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print()
        print("[FAIL]", e)
        raise SystemExit(1)

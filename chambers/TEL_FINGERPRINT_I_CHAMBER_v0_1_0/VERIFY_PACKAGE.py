#!/usr/bin/env python3
"""Verify the bounded TEL-FINGERPRINT-I v0.1.0 chamber package."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "README.md",
    "ENGINE_LOCK.json",
    "INPUT_SCHEMA.md",
    "PROTOCOL_TEL_FINGERPRINT_I_v0_1.md",
    "TEL_FINGERPRINT_I_CHAMBER_v0_1_0.html",
    "RUN_TEL_FINGERPRINT_I_CHAMBER.bat",
    "RUN_TEL_FINGERPRINT_I_CHAMBER.sh",
    "CHANGELOG.md",
    "STATUS.md",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    errors: list[str] = []
    files = {}
    for name in REQUIRED:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"missing file: {name}")
            continue
        files[name] = {"size_bytes": path.stat().st_size, "sha256": sha256(path)}

    lock_path = ROOT / "ENGINE_LOCK.json"
    lock = None
    if lock_path.exists():
        try:
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"ENGINE_LOCK.json invalid: {exc}")

    if lock:
        if lock.get("chamber") != "TEL-FINGERPRINT-I":
            errors.append("wrong chamber identifier")
        if lock.get("version") != "0.1.0":
            errors.append("wrong chamber version")
        if len(lock.get("route_ids", [])) != 4:
            errors.append("route lock must contain four routes")
        if len(lock.get("defect_coordinates", {})) != 10:
            errors.append("engine lock must contain ten defect coordinates")

    html_path = ROOT / "TEL_FINGERPRINT_I_CHAMBER_v0_1_0.html"
    if html_path.exists():
        html = html_path.read_text(encoding="utf-8")
        markers = [
            "TEL-FINGERPRINT-I",
            "PHI_PLUS",
            "PHI_MINUS",
            "PSI_PLUS",
            "PSI_MINUS",
            "ROUTE_CLASS_BIFURCATED",
            "route-label permutation",
            "NO MATRIX FLATTENING",
            "TEL_FINGERPRINT_I_RESULT_RECORD.json",
        ]
        for marker in markers:
            if marker not in html:
                errors.append(f"HTML marker missing: {marker}")
        if "http://" in html or "https://" in html:
            errors.append("standalone chamber must not require external URLs")

    result = {
        "package": "TEL_FINGERPRINT_I_CHAMBER_v0_1_0",
        "verdict": "PASS" if not errors else "FAIL",
        "errors": errors,
        "files": files,
    }
    output = ROOT / "LOCAL_PACKAGE_VERIFICATION.json"
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

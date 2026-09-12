from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import zipfile

PKG = "ROUTE_EXTRACT_PB"
VERSION = "0.1.3-pb"
FROZEN_EXTRACTOR_SHA256 = "dfa24fa5c3f11de038e00d160324a47674e17f29a59cb30bc9cd0d5d03bd1203"
PRIMARY_ARCHIVE_SHA256 = "405bc1acd99bec9c48b3aef47ed375991cf4ee4e83807e54ea491f2d55b6bd87"
PRIMARY_RUN_ID = "jhtdb_pilot_b_20260907_145640"
EXPECTED_COUNTS = {"D_STITCH": 3962, "P_TIME": 8806, "P_SCALE": 4830}

# File-level SHA-256 identities from the already verified primary Pilot-B export.
# These hashes are invariant under ordinary ZIP recompression, unlike the ZIP
# container checksum (which changes with timestamps/compression metadata).
PRIMARY_FILES = {
    "EDGES.parquet": "5fffe762df5dd160b3551c8df6c6a2e2a23af73e2ef0f5439c8a798cc7d9f6fd",
    "LADDERS.zip": "5388f227e11b857c1f0c3e02483c5b6d521a893b8b4f7e3b11d8156986bca615",
    "NODES.parquet": "2751b0e9c5b9ff26862e73419ae18fba25cb73c58f1b53fc0ee54df2d6608dac",
    "NULLS.csv": "be6ddc5af8b1696392ccdce8e2f6f8fa7b57cce2815eeb05f7860f70e8f147a4",
    "RESULT.json": "31e3c20aa24471d78b2de3eada282fc65503de74486adef8dd3eed663a1ac567",
    "RUN.json": "2efd26cf8d76d010a04dae1773aadf99ea7dbd3a2d8ff453ce2823cf89ca135d",
    "SQUARES.parquet": "b4f0b762454842207ec49841db6eb7473ca3ec386c62fce10fa51a4b52d03f1e",
    "STITCH_BY_SCALE.csv": "09ee3a4be03210e745e3c019bc0149ea214b38b7c5895f777383603b1ab3b904",
    "STITCH_BY_TIME.csv": "18f4ea1bd7474b29aa33111c951c3f4867ab5882c165483ee70368eae18a14b9",
    "STITCH_PHYSICS.json": "71665fb233ea20b4ccdf4f79aa19d583ca12c138de49470d1823659947242911",
    "STITCH_TAIL.csv": "cfe63b54e59f7773ffebd06a91445f1ffe283fecba744fec9bc72c315e71b3a0",
    "SUMMARY.csv": "ae590b062f1a6155735e6ee0992e4c55c96ad28dda4bad9d0675d10323a27a3c",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def project_root(script_dir: Path) -> Path:
    # tools/derive/ROUTE_EXTRACT_PB_v011 -> project root
    return script_dir.parents[2]


def find_primary_dir(root: Path) -> Path:
    d = root / "outputs" / "route_i" / "pilot_b" / PRIMARY_RUN_ID
    if not d.is_dir():
        raise FileNotFoundError(
            "Primary Pilot-B ROUTE-I run directory not found:\n"
            f"  {d}"
        )
    return d


def verify_primary_dir(run_dir: Path):
    print("[CHECK] primary Pilot-B scientific payload")
    for name, expected in PRIMARY_FILES.items():
        p = run_dir / name
        if not p.is_file():
            raise FileNotFoundError(f"Missing primary run file: {p}")
        got = sha256_file(p)
        if got.lower() != expected.lower():
            raise RuntimeError(
                f"{name}: content checksum mismatch.\n"
                f"Expected: {expected}\nFound:    {got}"
            )
        print(f"  [PASS] {name}")

    result = json.loads((run_dir / "RESULT.json").read_text(encoding="utf-8-sig"))
    runrec = json.loads((run_dir / "RUN.json").read_text(encoding="utf-8-sig"))
    if result.get("meta", {}).get("run_id") != PRIMARY_RUN_ID:
        raise RuntimeError("RESULT.json run_id mismatch.")
    if result.get("meta", {}).get("version") != "0.1.2":
        raise RuntimeError("RESULT.json STRUC-ROUTE-I version mismatch.")
    verdict_obj = result.get("verdict")
    verdict_class = verdict_obj.get("class") if isinstance(verdict_obj, dict) else verdict_obj
    if verdict_class != "CONSTRAINED_ROUTING":
        raise RuntimeError(f"Unexpected primary verdict: {verdict_obj!r}")
    print("  [PASS] run identity/version/verdict")


def make_temp_zip(run_dir: Path) -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "UNNS"
    base.mkdir(parents=True, exist_ok=True)
    zpath = base / "PBX_PRIMARY.zip"
    if zpath.exists():
        zpath.unlink()

    # Repack only after file-level identity has been verified. ZIP-container
    # bytes are not treated as the scientific identity.
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in PRIMARY_FILES:
            zf.write(run_dir / name, f"{PRIMARY_RUN_ID}/{name}")
    return zpath


def load_frozen_extractor(root: Path):
    p = root / "tools" / "derive" / "ROUTE_LADDER_EXTRACT_v0_1_1" / "extract_ladders.py"
    if not p.exists():
        raise FileNotFoundError(p)
    got = sha256_file(p)
    if got != FROZEN_EXTRACTOR_SHA256:
        raise RuntimeError(
            "Frozen ROUTE_LADDER_EXTRACT_v0_1_1 checksum mismatch.\n"
            f"Expected: {FROZEN_EXTRACTOR_SHA256}\nFound:    {got}"
        )
    spec = importlib.util.spec_from_file_location("frozen_route_extract", p)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not import frozen extractor.")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, p


def copy_tree_files(src: Path, dst: Path):
    dst.mkdir(parents=True, exist_ok=True)
    for p in src.iterdir():
        if p.is_file():
            shutil.copy2(p, dst / p.name)


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    root = project_root(script_dir)
    run_dir = find_primary_dir(root)

    print(f"{PKG} v{VERSION}")
    print(f"Project root : {root}")
    print(f"Primary run  : {run_dir}")

    verify_primary_dir(run_dir)
    run_zip = make_temp_zip(run_dir)
    run_sha = sha256_file(run_zip)
    print(f"[PASS] temporary transport ZIP created: {run_zip}")

    mod, frozen_path = load_frozen_extractor(root)
    print("[PASS] frozen extractor SHA-256")

    # Patch identity-validation constants only. The frozen extraction function,
    # selection rules, sorting, numeric rendering, range checks, and cross-checks
    # are executed unchanged.
    mod.DEFAULT_RUN_NAME = run_zip.name
    mod.EXPECTED_RUN_SHA256 = run_sha
    mod.EXPECTED = {
        "run_id": PRIMARY_RUN_ID,
        "route_i_version": "0.1.2",
        **EXPECTED_COUNTS,
    }

    stage = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "UNNS" / "PBX_STAGE"
    if stage.exists():
        shutil.rmtree(stage, ignore_errors=True)
    stage.mkdir(parents=True, exist_ok=True)

    print("[RUN] frozen extraction logic on Pilot-B primary run")
    report = mod.extract_ladders(run_zip, stage)

    raw_can = stage / "ladders" / "route_i" / "jhtdb_pilot_a" / "primary"
    raw_i = stage / "ladders" / "struc_i" / "jhtdb_pilot_a"
    raw_p = stage / "ladders" / "struc_perc_i" / "jhtdb_pilot_a"

    can = root / "ladders" / "route_i" / "pilot_b" / "primary"
    dst_i = root / "ladders" / "struc_i" / "pilot_b"
    dst_p = root / "ladders" / "struc_perc_i" / "pilot_b"
    rec_dir = root / "outputs" / "records" / "pilot_b"

    for d in (can, dst_i, dst_p, rec_dir):
        d.mkdir(parents=True, exist_ok=True)

    for d in (can, dst_i, dst_p):
        for old in d.glob("*"):
            if old.is_file():
                old.unlink()

    # Copy byte-identical ladder CSVs from the frozen extractor stage.
    for name in ("D_STITCH.csv", "P_TIME.csv", "P_SCALE.csv"):
        shutil.copy2(raw_can / name, can / name)
        shutil.copy2(raw_can / name, dst_i / name)
        shutil.copy2(raw_can / name, dst_p / name)

    # Canonical Pilot-B manifest: identity metadata only; ladder bytes untouched.
    m = json.loads((raw_can / "MANIFEST.json").read_text(encoding="utf-8-sig"))
    m["pilot"] = "jhtdb_pilot_b"
    m["purpose"] = (
        "Deterministic extraction of Pilot-B primary STRUC-ROUTE-I scalar descendants "
        "for independent canonical STRUC-I and STRUC-PERC-I interrogation."
    )
    m["wrapper"] = {
        "name": PKG,
        "version": VERSION,
        "frozen_extractor_path": str(frozen_path.relative_to(root)).replace("\\", "/"),
        "frozen_extractor_sha256": FROZEN_EXTRACTOR_SHA256,
        "scientific_extraction_logic_modified": False,
        "identity_validation_substitution_only": True,
    }
    manifest_text = json.dumps(m, indent=2, ensure_ascii=False) + "\n"
    for d in (can, dst_i, dst_p):
        (d / "MANIFEST.json").write_text(manifest_text, encoding="utf-8")

    readme = (
        "JHTDB PILOT B — PRIMARY ROUTE-DERIVED LADDERS\n"
        "===============================================\n\n"
        "D_STITCH.csv  finite source-object stitch_defect values.\n"
        "P_TIME.csv    time_persistence on actual sources of eligible time edges.\n"
        "P_SCALE.csv   scale_persistence on actual sources of eligible scale edges.\n\n"
        "Frozen extraction rules preserved exactly: duplicates retained; no deduplication,\n"
        "jitter, smoothing, normalization or rescaling; binary64 rendered with 17\n"
        "significant digits; ascending stable sort only.\n"
    )
    (can / "README.txt").write_text(readme, encoding="utf-8")

    ledger = []
    for p in sorted(can.iterdir()):
        if p.is_file() and p.name != "SHA256SUMS.txt":
            ledger.append(f"{sha256_file(p)}  {p.name}")
    (can / "SHA256SUMS.txt").write_text("\n".join(ledger) + "\n", encoding="utf-8")

    # Verify chamber-facing CSV copies are byte-identical.
    hashes = {}
    for name in ("D_STITCH.csv", "P_TIME.csv", "P_SCALE.csv"):
        h = sha256_file(can / name)
        if sha256_file(dst_i / name) != h or sha256_file(dst_p / name) != h:
            raise RuntimeError(f"{name}: chamber-facing copies are not byte-identical.")
        hashes[name] = h

    run_record = {
        "record": "PILOT_B_ROUTE_EXTRACT",
        "version": VERSION,
        "status": "PASS_READY_FOR_STRUC_I_AND_STRUC_PERC_I",
        "source_run": {
            "directory": str(run_dir.relative_to(root)).replace("\\", "/"),
            "verified_original_archive_sha256": PRIMARY_ARCHIVE_SHA256,
            "identity_basis": "file-level SHA-256 of all primary scientific payload files",
            "temporary_transport_zip_sha256": run_sha,
            "run_id": PRIMARY_RUN_ID,
            "route_i_version": "0.1.2",
            "verdict": "CONSTRAINED_ROUTING",
        },
        "frozen_extractor": {
            "path": str(frozen_path.relative_to(root)).replace("\\", "/"),
            "sha256": FROZEN_EXTRACTOR_SHA256,
            "scientific_logic_modified": False,
        },
        "counts": EXPECTED_COUNTS,
        "ladder_sha256": hashes,
        "canonical_dir": "ladders/route_i/pilot_b/primary",
        "struc_i_dir": "ladders/struc_i/pilot_b",
        "struc_perc_i_dir": "ladders/struc_perc_i/pilot_b",
    }
    rec_path = rec_dir / "ROUTE_EXTRACT.json"
    rec_path.write_text(json.dumps(run_record, indent=2) + "\n", encoding="utf-8")

    archive = rec_dir / "ROUTE_LADDERS.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(can.iterdir()):
            if p.is_file():
                zf.write(p, p.name)

    print()
    print("[READY] Pilot-B route ladders extracted and verified.")
    print(f"D_STITCH : {EXPECTED_COUNTS['D_STITCH']}")
    print(f"P_TIME   : {EXPECTED_COUNTS['P_TIME']}")
    print(f"P_SCALE  : {EXPECTED_COUNTS['P_SCALE']}")
    print("STRUC-I inputs     : ladders\\struc_i\\pilot_b")
    print("STRUC-PERC-I inputs: ladders\\struc_perc_i\\pilot_b")
    print("Record             : outputs\\records\\pilot_b\\ROUTE_EXTRACT.json")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print()
        print("[FAIL]", e)
        raise SystemExit(1)

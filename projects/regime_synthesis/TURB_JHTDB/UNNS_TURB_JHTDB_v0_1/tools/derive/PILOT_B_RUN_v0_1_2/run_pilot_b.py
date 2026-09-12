from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone
import zipfile

TOOL_NAME = "JHTDB_PILOT_B_RUN"
TOOL_VERSION = "0.1.2"

SOURCE_REL = Path("data/raw/jhtdb/pilot_b/isotropic1024-coarse-pilot-b-velocity.h5")
SOURCE_RECORD_REL = Path("data/raw/jhtdb/pilot_b/SOURCE_RECORD.json")
FREEZE_REL = Path("analysis/replication/jhtdb_pilot_b/FREEZE_SHA256.txt")
ADAPTER_REL = Path("tools/derive/JHTDB_ROUTE_ADAPTER_v0_1_0")
PILOT_A_CONFIG_REL = ADAPTER_REL / "config/pilot_a.json"

EXPECTED_SELECTION_SHA256 = "385cca0a0b28ac3b17f757ef3b7fcfe2c1954423ceb5376b927b67633a40875e"
EXPECTED_SOURCE_SHA256 = "977e6ab3c437252395dc7f7185af1829619fe1eec754f59f5f3ceae2ca0b969f"
EXPECTED_SOURCE_BYTES = 2015302728

ALLOWED_CONFIG_DIFFS = {
    ("adapter", "pilot"),
    ("source", "relative_path"),
    ("source", "expected_sha256"),
}

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def sha256_file(path: Path, block_size=16 * 1024 * 1024):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()

def find_project_root(start: Path):
    for p in [start.resolve()] + list(start.resolve().parents):
        if (p / "MANIFEST.json").exists() and (p / ADAPTER_REL).exists():
            return p
    raise FileNotFoundError("Could not locate UNNS_TURB_JHTDB_v0_1 project root.")

def parse_freeze(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    rows = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        digest, rel = line.split(None, 1)
        rows.append((digest.lower(), Path(rel.strip().replace("\\", "/"))))
    return rows

def verify_freeze(root: Path):
    rows = parse_freeze(root / FREEZE_REL)
    bad = []
    missing = []
    for expected, rel in rows:
        p = root / rel
        if not p.exists():
            missing.append(str(rel))
            continue
        got = sha256_file(p)
        if got.lower() != expected:
            bad.append({"path": str(rel), "expected": expected, "found": got})
    if missing or bad:
        raise RuntimeError(
            "FROZEN PROTOCOL/INSTRUMENT VERIFICATION FAILED\n"
            f"missing={len(missing)} mismatched={len(bad)}\n"
            f"missing_examples={missing[:5]}\n"
            f"mismatch_examples={bad[:3]}"
        )
    return len(rows)

def flatten(obj, prefix=()):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            out.update(flatten(v, prefix + (str(k),)))
        return out
    return {prefix: obj}

def verify_config_equivalence(pilot_a: dict, pilot_b: dict):
    a = flatten(pilot_a)
    b = flatten(pilot_b)
    keys = set(a) | set(b)
    diffs = []
    for key in sorted(keys):
        av = a.get(key, "<MISSING>")
        bv = b.get(key, "<MISSING>")
        if av != bv:
            diffs.append((key, av, bv))
    illegal = [d for d in diffs if d[0] not in ALLOWED_CONFIG_DIFFS]
    if illegal:
        raise RuntimeError(
            "Pilot-B config changes frozen scientific settings.\n"
            + "\n".join(f"{'.'.join(k)}: {a!r} -> {b!r}" for k, a, b in illegal)
        )
    required = {d[0] for d in diffs}
    if required != ALLOWED_CONFIG_DIFFS:
        raise RuntimeError(
            "Pilot-B config difference set is not exactly the preregistered identity/source substitution.\n"
            f"found={sorted('.'.join(x) for x in required)}"
        )
    return [
        {"field": ".".join(k), "pilot_a": av, "pilot_b": bv}
        for k, av, bv in diffs
    ]

def verify_source_record(root: Path):
    p = root / SOURCE_RECORD_REL
    if not p.exists():
        raise FileNotFoundError(p)
    rec = json.loads(p.read_text(encoding="utf-8-sig"))
    if rec.get("status") != "ACQUIRED_HASHED_READY_FOR_ADAPTER":
        raise RuntimeError(f"SOURCE_RECORD status is {rec.get('status')!r}, not ready.")
    if rec.get("readiness", {}).get("adapter_may_run") is not True:
        raise RuntimeError("SOURCE_RECORD readiness.adapter_may_run is not true.")
    if rec.get("selection_lock", {}).get("sha256") != EXPECTED_SELECTION_SHA256:
        raise RuntimeError("Pilot-B selection lock SHA-256 mismatch.")
    acq = rec.get("acquisition", {})
    if acq.get("sha256") != EXPECTED_SOURCE_SHA256:
        raise RuntimeError("SOURCE_RECORD source SHA-256 mismatch.")
    if int(acq.get("bytes", -1)) != EXPECTED_SOURCE_BYTES:
        raise RuntimeError("SOURCE_RECORD source byte-size mismatch.")
    if acq.get("hdf5_validation", {}).get("status") != "PASS":
        raise RuntimeError("SOURCE_RECORD HDF5 validation is not PASS.")
    return rec

def verify_targets_absent(root: Path):
    targets = [
        root / "data/derived/objects/jhtdb_pilot_b/objects.parquet",
        root / "data/derived/objects/jhtdb_pilot_b/objects.csv",
        root / "ladders/native/jhtdb_pilot_b/route_project/manifest.json",
        root / "outputs/records/pilot_b/JHTDB_PILOT_B_ROUTE.zip",
        root / "outputs/records/pilot_b/PILOT_B_ADAPTER_RUN.json",
        root / "outputs/tables/pilot_b/JHTDB_PHYS_STATS.csv",
    ]
    existing = [str(p) for p in targets if p.exists()]
    if existing:
        raise RuntimeError(
            "Pilot-B adapter outputs already exist. The preregistered stopping rule "
            "forbids silently replacing a seen Pilot-B run.\nExisting:\n  "
            + "\n  ".join(existing)
        )

def prepare_stage(root: Path, source: Path):
    # v0.1.1: keep the staging path deliberately short for Windows MAX_PATH
    # compatibility. The v0.1.0 staging destination exceeded 260 characters
    # in the user's project location, causing os.link() to fail before any
    # Pilot-B derived data were generated.
    # Do not touch the abandoned v0.1.0 deep staging tree here.
    # On this Windows path it can itself be difficult to remove because of
    # path-length/access semantics. It contains no completed Pilot-B result
    # and is irrelevant to the v0.1.2 run.
    stage = root / "PB_STAGE"
    marker = stage / "STAGE_MARKER.json"
    if stage.exists():
        if marker.exists():
            shutil.rmtree(stage)
        else:
            raise RuntimeError(
                f"Refusing to delete unrecognized staging directory: {stage}"
            )
    stage.mkdir(parents=True)
    marker.write_text(
        json.dumps({"tool": TOOL_NAME, "version": TOOL_VERSION, "created_utc": utc_now()}, indent=2) + "\n",
        encoding="utf-8",
    )

    stage_source = stage / SOURCE_REL
    stage_source.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(source, stage_source)
    except Exception as e:
        raise RuntimeError(
            "Could not create a zero-copy hard link to the 2-GB Pilot-B HDF5. "
            "No full copy was made. The staging path is already shortened in v0.1.1; "
            "if this still fails, verify that the project is on NTFS and hard links are permitted. "
            f"Original error: {e}"
        )

    energy = root / "data/source/ener_Re_time.txt"
    if energy.exists():
        dst = stage / "data/source/ener_Re_time.txt"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(energy, dst)
    return stage

def stream_subprocess(cmd, cwd: Path, env: dict, log_path: Path):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8", newline="\n") as log:
        log.write("COMMAND: " + " ".join(str(x) for x in cmd) + "\n\n")
        log.flush()
        p = subprocess.Popen(
            [str(x) for x in cmd],
            cwd=str(cwd),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        assert p.stdout is not None
        for line in p.stdout:
            print(line, end="")
            log.write(line)
            log.flush()
        return p.wait()

def copy_table(src_dir: Path, dst_dir: Path, stem: str):
    dst_dir.mkdir(parents=True, exist_ok=True)
    for ext in (".parquet", ".csv"):
        src = src_dir / f"{stem}{ext}"
        if src.exists():
            dst = dst_dir / src.name
            shutil.copy2(src, dst)
            return dst
    raise FileNotFoundError(f"No {stem}.parquet or {stem}.csv in {src_dir}")

def canonicalize_outputs(root: Path, stage: Path, raw_report: dict, config_diffs: list, freeze_count: int):
    stage_derived = stage / "data/derived/objects/jhtdb_pilot_b"
    stage_route = stage / "ladders/native/jhtdb_pilot_b/route_project"
    stage_phys = stage / "outputs/tables/JHTDB_PHYS_STATS.csv"
    stage_raw_report = stage / "outputs/records/JHTDB_ADAPTER_REPORT.json"

    if not stage_raw_report.exists() or not stage_route.exists() or not stage_derived.exists():
        raise RuntimeError("Frozen adapter did not produce the expected staging outputs.")

    target_derived = root / "data/derived/objects/jhtdb_pilot_b"
    target_route = root / "ladders/native/jhtdb_pilot_b/route_project"
    records = root / "outputs/records/pilot_b"
    tables = root / "outputs/tables/pilot_b"
    records.mkdir(parents=True, exist_ok=True)
    tables.mkdir(parents=True, exist_ok=True)
    target_derived.mkdir(parents=True, exist_ok=True)
    target_route.mkdir(parents=True, exist_ok=True)

    obj_path = copy_table(stage_derived, target_derived, "objects")
    rel_path = copy_table(stage_derived, target_derived, "relations")

    for p in stage_route.iterdir():
        if p.is_file():
            shutil.copy2(p, target_route / p.name)

    manifest_path = target_route / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    raw_labels = {
        "project_name": manifest.get("project_name"),
        "run_id": manifest.get("run_id"),
    }
    manifest["project_name"] = "JHTDB isotropic1024coarse — UNNS Turbulence Pilot B"
    manifest["run_id"] = "jhtdb_pilot_b"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    phys_target = tables / "JHTDB_PHYS_STATS.csv"
    shutil.copy2(stage_phys, phys_target)
    shutil.copy2(stage_phys, target_route / "PHYS_STATS.csv")

    raw_report_copy = records / "JHTDB_ADAPTER_REPORT_RAW.json"
    shutil.copy2(stage_raw_report, raw_report_copy)

    canonical_report = json.loads(stage_raw_report.read_text(encoding="utf-8"))
    canonical_report["outputs"] = {
        "derived_objects": str(obj_path),
        "derived_relations": str(rel_path),
        "route_project": str(target_route),
        "phys_stats": str(phys_target),
        "route_zip": str(records / "JHTDB_PILOT_B_ROUTE.zip"),
    }
    canonical_report["output_hashes"] = {
        obj_path.name: sha256_file(obj_path),
        rel_path.name: sha256_file(rel_path),
        "manifest.json": sha256_file(manifest_path),
    }
    canonical_report["postprocess"] = {
        "type": "metadata_only_relabel_and_output_relocation",
        "scientific_arrays_modified": False,
        "raw_manifest_labels": raw_labels,
        "canonical_manifest_labels": {
            "project_name": manifest["project_name"],
            "run_id": manifest["run_id"],
        },
        "reason": (
            "Frozen adapter v0.1.0 hardcodes Pilot-A project_name/run_id and three "
            "top-level output filenames. The adapter itself was not modified. "
            "Pilot-B execution therefore occurred in an isolated staging root; only "
            "identity metadata and output locations were canonicalized afterward."
        ),
    }
    canonical_report_path = records / "JHTDB_ADAPTER_REPORT.json"
    canonical_report_path.write_text(json.dumps(canonical_report, indent=2) + "\n", encoding="utf-8")
    (target_route / "ADAPTER_REPORT.json").write_text(
        json.dumps(canonical_report, indent=2) + "\n", encoding="utf-8"
    )

    route_zip = records / "JHTDB_PILOT_B_ROUTE.zip"
    with zipfile.ZipFile(route_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in ("manifest.json", obj_path.name, rel_path.name, "ADAPTER_REPORT.json", "PHYS_STATS.csv"):
            if name == obj_path.name:
                p = obj_path
            elif name == rel_path.name:
                p = rel_path
            else:
                p = target_route / name
            zf.write(p, name)

    run_record = {
        "record": "JHTDB_PILOT_B_ADAPTER_RUN",
        "version": TOOL_VERSION,
        "status": "COMPLETE_READY_FOR_STRUC_ROUTE_I",
        "created_utc": utc_now(),
        "frozen_adapter": {
            "path": str(ADAPTER_REL).replace("\\", "/"),
            "version": "0.1.0",
            "frozen_files_verified": freeze_count,
            "modified": False,
        },
        "config_equivalence": {
            "scientific_settings_changed": False,
            "allowed_identity_source_differences": config_diffs,
        },
        "source": {
            "path": str(SOURCE_REL).replace("\\", "/"),
            "sha256": raw_report.get("source", {}).get("sha256"),
            "bytes": EXPECTED_SOURCE_BYTES,
            "selection_sha256": EXPECTED_SELECTION_SHA256,
        },
        "adapter_result": raw_report.get("result"),
        "metadata_canonicalization": canonical_report["postprocess"],
        "outputs": {
            "derived_objects": str(obj_path.relative_to(root)).replace("\\", "/"),
            "derived_relations": str(rel_path.relative_to(root)).replace("\\", "/"),
            "route_project": str(target_route.relative_to(root)).replace("\\", "/"),
            "route_bundle": str(route_zip.relative_to(root)).replace("\\", "/"),
            "phys_stats": str(phys_target.relative_to(root)).replace("\\", "/"),
            "raw_adapter_report": str(raw_report_copy.relative_to(root)).replace("\\", "/"),
            "canonical_adapter_report": str(canonical_report_path.relative_to(root)).replace("\\", "/"),
        },
        "hashes": {
            "objects": sha256_file(obj_path),
            "relations": sha256_file(rel_path),
            "manifest": sha256_file(manifest_path),
            "route_bundle": sha256_file(route_zip),
            "phys_stats": sha256_file(phys_target),
        },
    }
    run_record_path = records / "PILOT_B_ADAPTER_RUN.json"
    run_record_path.write_text(json.dumps(run_record, indent=2) + "\n", encoding="utf-8")
    return run_record

def preflight(root: Path, config_path: Path):
    print("JHTDB PILOT B — FROZEN ADAPTER PREFLIGHT")
    print(f"project root : {root}")

    freeze_count = verify_freeze(root)
    print(f"[PASS] frozen replication set: {freeze_count}/{freeze_count} SHA-256 matches")

    source_record = verify_source_record(root)
    print("[PASS] SOURCE_RECORD: ACQUIRED_HASHED_READY_FOR_ADAPTER")
    print(f"[PASS] HDF5 validation: {source_record['acquisition']['hdf5_validation']['status']}")

    source = root / SOURCE_REL
    if not source.exists():
        raise FileNotFoundError(source)
    if source.stat().st_size != EXPECTED_SOURCE_BYTES:
        raise RuntimeError(
            f"Pilot-B HDF5 byte size mismatch: expected {EXPECTED_SOURCE_BYTES}, "
            f"found {source.stat().st_size}"
        )
    print(f"[PASS] Pilot-B HDF5 present: {source.stat().st_size} bytes")

    pilot_a = json.loads((root / PILOT_A_CONFIG_REL).read_text(encoding="utf-8"))
    pilot_b = json.loads(config_path.read_text(encoding="utf-8"))
    diffs = verify_config_equivalence(pilot_a, pilot_b)
    print("[PASS] Pilot-B config preserves all frozen scientific settings")
    for d in diffs:
        print(f"       identity/source substitution: {d['field']}")

    verify_targets_absent(root)
    print("[PASS] no prior canonical Pilot-B adapter result will be overwritten")
    return freeze_count, source_record, source, diffs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preflight-only", action="store_true")
    args = ap.parse_args()

    script_dir = Path(__file__).resolve().parent
    root = find_project_root(script_dir)
    config_path = script_dir / "PILOT_B_CONFIG.json"

    freeze_count, source_record, source, diffs = preflight(root, config_path)
    if args.preflight_only:
        print("\n[PREFLIGHT PASS] No Pilot-B derived data were generated.")
        return 0

    stage = prepare_stage(root, source)
    adapter_dir = root / ADAPTER_REL
    adapter_script = adapter_dir / "run_adapter.py"
    log_path = root / "outputs/records/pilot_b/ADAPTER_RUN_LOG.txt"

    print("\n[RUN] frozen JHTDB_ROUTE_ADAPTER_v0_1_0 in isolated Pilot-B staging root")
    print("      The original adapter files are not modified.")
    print(f"      Stage: {stage}")

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    cmd = [
        sys.executable,
        str(adapter_script),
        "--config", str(config_path),
        "--project-root", str(stage),
    ]
    rc = stream_subprocess(cmd, adapter_dir, env, log_path)
    if rc != 0:
        print(f"\n[FAILED] Frozen adapter returned exit code {rc}.")
        print(f"Stage preserved for diagnosis: {stage}")
        return rc

    raw_report_path = stage / "outputs/records/JHTDB_ADAPTER_REPORT.json"
    raw_report = json.loads(raw_report_path.read_text(encoding="utf-8"))
    if raw_report.get("source", {}).get("sha256") != EXPECTED_SOURCE_SHA256:
        raise RuntimeError("Frozen adapter did not report the expected Pilot-B source SHA-256.")
    if raw_report.get("status") != "COMPLETE":
        raise RuntimeError("Frozen adapter report is not COMPLETE.")

    run_record = canonicalize_outputs(root, stage, raw_report, diffs, freeze_count)

    # Remove only our recognized stage after successful canonicalization.
    shutil.rmtree(stage)

    print("\n[READY] Pilot-B adapter completed with frozen scientific logic.")
    print("Canonical route bundle:")
    print("  outputs\\records\\pilot_b\\JHTDB_PILOT_B_ROUTE.zip")
    print("Run record:")
    print("  outputs\\records\\pilot_b\\PILOT_B_ADAPTER_RUN.json")
    print("Next preregistered step: STRUC-ROUTE-I v0.1.2.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

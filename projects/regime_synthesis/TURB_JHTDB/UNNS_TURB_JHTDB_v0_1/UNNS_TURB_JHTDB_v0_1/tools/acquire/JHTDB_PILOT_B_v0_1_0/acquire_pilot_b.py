from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import h5py
import numpy as np

TOOL_VERSION = "0.1.0"
TESTING_TOKEN = "edu.jhu.pha.turbulence.testing-201406"
EXPECTED_DATASET = "isotropic1024coarse"
EXPECTED_FIELD = "velocity"
DEFAULT_SLAB_DEPTH = 30


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    total = path.stat().st_size
    done = 0
    with path.open("rb") as f:
        for block in iter(lambda: f.read(16 * 1024 * 1024), b""):
            h.update(block)
            done += len(block)
            pct = (100.0 * done / total) if total else 100.0
            print(f"\r[SHA256] {pct:6.2f}%", end="", flush=True)
    print()
    return h.hexdigest()


def canonical_selection_hash(selection: dict) -> str:
    payload = json.dumps(
        selection, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def atomic_write_json(path: Path, obj: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def project_root_from_script() -> Path:
    # <project>/tools/acquire/JHTDB_PILOT_B_v0_1_0/acquire_pilot_b.py
    return Path(__file__).resolve().parents[3]


def read_and_verify_record(project_root: Path) -> tuple[Path, dict]:
    record_path = project_root / "data/raw/jhtdb/pilot_b/SOURCE_RECORD.json"
    if not record_path.exists():
        raise FileNotFoundError(record_path)
    record = json.loads(record_path.read_text(encoding="utf-8"))
    if record.get("record") != "JHTDB_PILOT_B_SOURCE":
        raise ValueError("Unexpected source record type.")
    selection = record["selection"]
    expected = record["selection_lock"]["sha256"]
    found = canonical_selection_hash(selection)
    if found.lower() != expected.lower():
        raise RuntimeError(
            "PILOT-B SOURCE SELECTION LOCK FAILED.\n"
            f"expected: {expected}\nfound:    {found}\n"
            "Do not acquire data until the provenance discrepancy is resolved."
        )
    if selection["dataset"] != EXPECTED_DATASET or selection["field"] != EXPECTED_FIELD:
        raise ValueError("Unexpected dataset/field in frozen source selection.")
    return record_path, record


def plan_from_record(record: dict, slab_depth: int) -> dict:
    s = record["selection"]
    c = s["cutout"]
    t = s["time"]
    xs, xe = c["x_1based_inclusive"]
    ys, ye = c["y_1based_inclusive"]
    zs, ze = c["z_1based_inclusive"]
    ts, te = t["stored_frame_indices_1based_inclusive"]
    nx, ny, nz = c["shape_xyz"]
    nframes = t["stored_frame_count"]
    slabs_per_frame = math.ceil(nz / slab_depth)
    raw_bytes = nx * ny * nz * 3 * 4 * nframes
    max_points_per_query = nx * ny * min(slab_depth, nz)
    return {
        "xs": xs, "xe": xe, "ys": ys, "ye": ye, "zs": zs, "ze": ze,
        "ts": ts, "te": te, "nx": nx, "ny": ny, "nz": nz,
        "nframes": nframes,
        "slab_depth": slab_depth,
        "slabs_per_frame": slabs_per_frame,
        "query_count": slabs_per_frame * nframes,
        "raw_bytes": raw_bytes,
        "max_points_per_query": max_points_per_query,
    }


def print_plan(record: dict, plan: dict) -> None:
    s = record["selection"]
    print("JHTDB PILOT B — FROZEN ACQUISITION PLAN")
    print(f"  selection SHA-256 : {record['selection_lock']['sha256']}")
    print(f"  dataset           : {s['dataset']}")
    print(f"  spatial           : x={plan['xs']}:{plan['xe']} y={plan['ys']}:{plan['ye']} z={plan['zs']}:{plan['ze']}")
    print(f"  frames            : {plan['ts']}:{plan['te']}")
    print(f"  physical window   : {s['time']['physical_window'][0]:.3f}..{s['time']['physical_window'][1]:.3f}")
    print(f"  z slab depth      : {plan['slab_depth']}")
    print(f"  points/query max  : {plan['max_points_per_query']:,}")
    print(f"  serial queries    : {plan['query_count']}")
    print(f"  raw float payload : {plan['raw_bytes'] / 1024**3:.6f} GiB")
    print("  Pilot-A overlap   : spatial=0, time=0")


def import_giverny():
    try:
        from givernylocal.turbulence_dataset import turb_dataset
        from givernylocal.turbulence_toolkit import getCutout
    except Exception as exc:
        raise RuntimeError(
            "givernylocal is not available. Run SETUP_ACQUIRE.bat first."
        ) from exc
    return turb_dataset, getCutout


def find_velocity_array(ds) -> np.ndarray:
    names = list(ds.data_vars)
    if not names:
        raise RuntimeError("JHTDB response contained no data variables.")
    # A one-time, one-variable getCutout request should return one data variable.
    # Prefer a velocity-like name if the service returns additional metadata variables.
    preferred = [n for n in names if "vel" in n.lower()]
    name = preferred[0] if preferred else names[0]
    arr = np.asarray(ds[name].values, dtype=np.float32)
    return arr


def expected_frame_names(ts: int, te: int) -> list[str]:
    return [f"Velocity_{i:04d}" for i in range(ts, te + 1)]


def initialize_partial(path: Path, record: dict, plan: dict) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    s = record["selection"]
    dx = float(s["space"]["dx_decimal"])
    xs0 = s["cutout"]["x_0based_inclusive"][0]
    ys0 = s["cutout"]["y_0based_inclusive"][0]
    zs0 = s["cutout"]["z_0based_inclusive"][0]
    nx, ny, nz = plan["nx"], plan["ny"], plan["nz"]
    with h5py.File(path, "w") as f:
        f.attrs.update({
            "dataset": EXPECTED_DATASET,
            "filterWidth": 1,
            "t_start": plan["ts"],
            "t_end": plan["te"],
            "t_step": 1,
            "x_start": plan["xs"],
            "x_end": plan["xe"],
            "x_step": 1,
            "y_start": plan["ys"],
            "y_end": plan["ye"],
            "y_step": 1,
            "z_start": plan["zs"],
            "z_end": plan["ze"],
            "z_step": 1,
            "pilot_b_selection_sha256": record["selection_lock"]["sha256"],
            "acquisition_tool": f"JHTDB_PILOT_B_v{TOOL_VERSION}",
        })
        f.create_dataset("xcoor", data=((xs0 + np.arange(nx)) * dx).astype(np.float32), chunks=(nx,))
        f.create_dataset("ycoor", data=((ys0 + np.arange(ny)) * dx).astype(np.float32), chunks=(ny,))
        f.create_dataset("zcoor", data=((zs0 + np.arange(nz)) * dx).astype(np.float32), chunks=(nz,))
        for frame in range(plan["ts"], plan["te"] + 1):
            d = f.create_dataset(
                f"Velocity_{frame:04d}",
                shape=(nz, ny, nx, 3),
                dtype=np.float32,
                chunks=(16, 32, 32, 1),
                fillvalue=0.0,
            )
            d.attrs["_acq_written_z"] = 0
            d.attrs["_acq_complete"] = 0
        f.flush()


def validate_h5(path: Path, record: dict, plan: dict, allow_resume_attrs: bool = False) -> dict:
    expected = expected_frame_names(plan["ts"], plan["te"])
    with h5py.File(path, "r") as f:
        for cname in ("xcoor", "ycoor", "zcoor"):
            if cname not in f or f[cname].shape != (256,):
                raise RuntimeError(f"HDF5 coordinate validation failed: {cname}")
        for name in expected:
            if name not in f:
                raise RuntimeError(f"Missing velocity dataset: {name}")
            d = f[name]
            if d.shape != (256, 256, 256, 3) or d.dtype != np.dtype("float32"):
                raise RuntimeError(f"Unexpected {name} layout: shape={d.shape} dtype={d.dtype}")
            if not allow_resume_attrs and int(d.attrs.get("_acq_complete", 1)) != 1:
                raise RuntimeError(f"Incomplete velocity dataset: {name}")
        root_expected = {
            "dataset": EXPECTED_DATASET,
            "t_start": plan["ts"], "t_end": plan["te"], "t_step": 1,
            "x_start": plan["xs"], "x_end": plan["xe"],
            "y_start": plan["ys"], "y_end": plan["ye"],
            "z_start": plan["zs"], "z_end": plan["ze"],
        }
        for k, v in root_expected.items():
            found = f.attrs.get(k)
            if isinstance(found, bytes):
                found = found.decode("utf-8", errors="replace")
            if found != v:
                raise RuntimeError(f"Root attribute mismatch {k}: expected={v!r} found={found!r}")
        sel = f.attrs.get("pilot_b_selection_sha256")
        if isinstance(sel, bytes):
            sel = sel.decode("utf-8", errors="replace")
        if sel != record["selection_lock"]["sha256"]:
            raise RuntimeError("HDF5 selection-lock attribute mismatch.")
    return {
        "status": "PASS",
        "velocity_datasets": expected,
        "velocity_dataset_shape_zyxc": [256, 256, 256, 3],
        "coordinate_lengths_xyz": [256, 256, 256],
        "root_attrs_checked": list(root_expected.keys()) + ["pilot_b_selection_sha256"],
    }


def remove_resume_attrs(path: Path, plan: dict) -> None:
    with h5py.File(path, "r+") as f:
        for name in expected_frame_names(plan["ts"], plan["te"]):
            d = f[name]
            for attr in ("_acq_written_z", "_acq_complete"):
                if attr in d.attrs:
                    del d.attrs[attr]
        f.flush()


def acquire(project_root: Path, record_path: Path, record: dict, plan: dict, *, force_restart: bool) -> None:
    token = os.environ.get("JHTDB_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "JHTDB_TOKEN is not set. Use a registered JHTDB token in this command window.\n"
            "Do not put the token into SOURCE_RECORD.json or commit it to the project."
        )
    if token == TESTING_TOKEN or ".testing-" in token:
        raise RuntimeError(
            "The public JHTDB testing token is intentionally rejected for Pilot B. "
            "It is limited to 4096 points per query and cannot acquire this frozen 256^3 source efficiently."
        )

    turb_dataset, getCutout = import_giverny()
    raw_dir = project_root / "data/raw/jhtdb/pilot_b"
    final_path = project_root / record["acquisition"]["local_file"]
    partial_path = final_path.with_suffix(".partial.h5")
    log_path = raw_dir / "ACQUIRE_LOG.txt"

    if final_path.exists():
        print(f"[FOUND] final source already exists: {final_path}")
        validation = validate_h5(final_path, record, plan)
        digest = sha256_file(final_path)
        finalize_record(record_path, record, final_path, digest, validation)
        print("[READY] Existing source verified and SOURCE_RECORD.json finalized.")
        return

    if force_restart and partial_path.exists():
        partial_path.unlink()
    initialize_partial(partial_path, record, plan)
    validate_h5(partial_path, record, plan, allow_resume_attrs=True)

    cube = turb_dataset(
        dataset_title=EXPECTED_DATASET,
        output_path=str(raw_dir),
        auth_token=token,
    )

    def log(message: str) -> None:
        stamp = utc_now()
        line = f"{stamp}  {message}"
        print(line)
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    log(f"START tool={TOOL_VERSION} selection_sha256={record['selection_lock']['sha256']}")
    log(f"PLAN x={plan['xs']}:{plan['xe']} y={plan['ys']}:{plan['ye']} z={plan['zs']}:{plan['ze']} t={plan['ts']}:{plan['te']} slab_depth={plan['slab_depth']}")

    for frame in range(plan["ts"], plan["te"] + 1):
        dname = f"Velocity_{frame:04d}"
        with h5py.File(partial_path, "r+") as f:
            d = f[dname]
            written = int(d.attrs.get("_acq_written_z", 0))
            complete = int(d.attrs.get("_acq_complete", 0))
        if complete:
            log(f"SKIP frame={frame} complete=1")
            continue

        z_local = written
        while z_local < plan["nz"]:
            count = min(plan["slab_depth"], plan["nz"] - z_local)
            z1 = plan["zs"] + z_local
            z2 = z1 + count - 1
            axes = np.array([
                [plan["xs"], plan["xe"]],
                [plan["ys"], plan["ye"]],
                [z1, z2],
                [frame, frame],
            ], dtype=np.int64)
            strides = np.array([1, 1, 1, 1], dtype=np.int64)

            last_exc = None
            for attempt in range(1, 6):
                try:
                    log(f"QUERY frame={frame} z={z1}:{z2} attempt={attempt}")
                    ds = getCutout(cube, EXPECTED_FIELD, axes, strides, verbose=True)
                    arr = find_velocity_array(ds)
                    expected_shape = (count, plan["ny"], plan["nx"], 3)
                    if arr.shape != expected_shape:
                        raise RuntimeError(
                            f"Unexpected JHTDB slab shape for frame={frame}, z={z1}:{z2}: "
                            f"expected={expected_shape} found={arr.shape}"
                        )
                    if not np.isfinite(arr).all():
                        raise RuntimeError(f"Non-finite velocity value in frame={frame}, z={z1}:{z2}")
                    with h5py.File(partial_path, "r+") as f:
                        d = f[dname]
                        d[z_local:z_local + count, :, :, :] = arr
                        d.attrs["_acq_written_z"] = z_local + count
                        if z_local + count == plan["nz"]:
                            d.attrs["_acq_complete"] = 1
                        f.flush()
                    log(f"WRITE frame={frame} local_z={z_local}:{z_local + count - 1} source_z={z1}:{z2} PASS")
                    del arr, ds
                    gc.collect()
                    last_exc = None
                    break
                except Exception as exc:
                    last_exc = exc
                    log(f"RETRY frame={frame} z={z1}:{z2} attempt={attempt} error={type(exc).__name__}: {exc}")
                    if attempt < 5:
                        time.sleep([5, 15, 30, 60][attempt - 1])
            if last_exc is not None:
                raise RuntimeError(
                    f"Acquisition failed after retries for frame={frame}, z={z1}:{z2}. "
                    f"Partial file is preserved for resume: {partial_path}"
                ) from last_exc
            z_local += count

    validation = validate_h5(partial_path, record, plan)
    remove_resume_attrs(partial_path, plan)
    # Validate again after removing acquisition-only resume metadata.
    validation = validate_h5(partial_path, record, plan)
    partial_path.replace(final_path)
    digest = sha256_file(final_path)
    finalize_record(record_path, record, final_path, digest, validation)
    log(f"COMPLETE file={final_path.name} bytes={final_path.stat().st_size} sha256={digest}")
    print("\n[READY] Pilot-B source acquired, validated, hashed, and recorded.")
    print(f"  {final_path}")
    print(f"  SHA-256: {digest}")


def finalize_record(record_path: Path, record: dict, final_path: Path, digest: str, validation: dict) -> None:
    # Re-verify the immutable selection before recording readiness.
    found = canonical_selection_hash(record["selection"])
    expected = record["selection_lock"]["sha256"]
    if found.lower() != expected.lower():
        raise RuntimeError("Selection lock changed during acquisition; refusing to finalize.")
    size = final_path.stat().st_size
    record["status"] = "ACQUIRED_HASHED_READY_FOR_ADAPTER"
    record["acquisition"]["sha256"] = digest
    record["acquisition"]["bytes"] = size
    record["acquisition"]["gib"] = size / (1024**3)
    record["acquisition"]["acquired_utc"] = utc_now()
    record["acquisition"]["hdf5_validation"] = validation
    record["readiness"]["adapter_may_run"] = True
    record["readiness"]["condition"] = "Satisfied: source exists, selection lock verified, HDF5 validation passed, SHA-256 recorded."
    atomic_write_json(record_path, record)
    checksum_path = final_path.parent / "SOURCE_SHA256.txt"
    checksum_path.write_text(f"{digest}  {final_path.name}\n", encoding="utf-8")


def verify_only(project_root: Path, record_path: Path, record: dict, plan: dict) -> None:
    final_path = project_root / record["acquisition"]["local_file"]
    if not final_path.exists():
        raise FileNotFoundError(final_path)
    validation = validate_h5(final_path, record, plan)
    digest = sha256_file(final_path)
    finalize_record(record_path, record, final_path, digest, validation)
    print("[PASS] Existing source validated, hashed, and SOURCE_RECORD.json finalized.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Acquire the frozen JHTDB Pilot-B velocity source.")
    parser.add_argument("--dry-run", action="store_true", help="Verify the frozen selection and print the acquisition plan only.")
    parser.add_argument("--verify-only", action="store_true", help="Validate/hash an already acquired final HDF5 and update SOURCE_RECORD.json.")
    parser.add_argument("--force-restart", action="store_true", help="Delete an existing .partial.h5 and restart acquisition from the first slab.")
    parser.add_argument("--slab-depth", type=int, default=DEFAULT_SLAB_DEPTH, help="Serial z-slab depth. Default 30 keeps each request below 2 million grid points.")
    args = parser.parse_args()

    if args.slab_depth < 1 or args.slab_depth > 30:
        raise ValueError("--slab-depth must be between 1 and 30 for this frozen acquisition tool.")

    root = project_root_from_script()
    record_path, record = read_and_verify_record(root)
    plan = plan_from_record(record, args.slab_depth)
    print_plan(record, plan)

    if args.dry_run:
        print("\n[PASS] Frozen selection verified. No network access or source data inspection occurred.")
        return 0
    if args.verify_only:
        verify_only(root, record_path, record, plan)
        return 0
    acquire(root, record_path, record, plan, force_restart=args.force_restart)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\n[STOPPED] Acquisition interrupted. Partial HDF5 is preserved for resume.", file=sys.stderr)
        raise SystemExit(130)
    except Exception as exc:
        print(f"\n[ERROR] {exc}", file=sys.stderr)
        raise SystemExit(1)

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

try:
    import h5py
    import numpy as np
except ImportError as e:
    print("Missing dependency:", e)
    print("Install with:  py -m pip install h5py numpy")
    sys.exit(2)


CANDIDATE_NAMES = [
    "isotropic1024-coarse-velocity.h5",
    "isotropic1024_coarse_velocity.h5",
    "isotropic1024coarse-velocity.h5",
    "isotropic1024coarse_velocity.h5",
]


def jsonable(value):
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, np.ndarray):
        if value.size <= 256:
            return value.tolist()
        return {
            "shape": list(value.shape),
            "dtype": str(value.dtype),
            "preview": value.reshape(-1)[:16].tolist(),
        }
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    try:
        return value.tolist()
    except Exception:
        return repr(value)


def attr_dict(obj):
    return {str(k): jsonable(v) for k, v in obj.attrs.items()}


def sha256_file(path: Path, block_size=16 * 1024 * 1024):
    h = hashlib.sha256()
    total = path.stat().st_size
    read = 0
    with path.open("rb") as f:
        while True:
            block = f.read(block_size)
            if not block:
                break
            h.update(block)
            read += len(block)
            pct = 100.0 * read / total if total else 100.0
            print(f"\rSHA-256: {pct:6.2f}%", end="", flush=True)
    print()
    return h.hexdigest()


def find_input(root: Path):
    for name in CANDIDATE_NAMES:
        hits = list(root.rglob(name))
        if hits:
            return hits[0]
    h5s = [p for p in root.rglob("*.h5") if "velocity" in p.name.lower()]
    if len(h5s) == 1:
        return h5s[0]
    if not h5s:
        raise FileNotFoundError(
            "No velocity HDF5 found. Pass the file explicitly:\n"
            '  py tools\\validate\\inspect_velocity_h5.py "FULL\\PATH\\TO\\FILE.h5"'
        )
    raise RuntimeError(
        "More than one candidate velocity HDF5 found. Pass the intended file explicitly."
    )


def sparse_numeric_sample(ds, max_points=4096):
    """
    Read a small deterministic sample without loading the full dataset.
    Works for arbitrary dimensional numeric datasets.
    """
    if not np.issubdtype(ds.dtype, np.number) or ds.size == 0:
        return None

    # Build a strided hyperslab with at most ~4096 values.
    shape = ds.shape
    if not shape:
        arr = np.asarray(ds[()])
    else:
        target_per_axis = max(1, int(round(max_points ** (1 / max(1, len(shape))))))
        slices = []
        for n in shape:
            if n <= target_per_axis:
                slices.append(slice(None))
            else:
                step = max(1, n // target_per_axis)
                slices.append(slice(0, n, step))
        arr = np.asarray(ds[tuple(slices)])

        # Hard cap after reading the strided slab.
        if arr.size > max_points:
            flat = arr.reshape(-1)
            idx = np.linspace(0, flat.size - 1, max_points, dtype=int)
            arr = flat[idx]

    flat = np.asarray(arr).reshape(-1)
    finite = flat[np.isfinite(flat)]
    if finite.size == 0:
        return {
            "sample_count": int(flat.size),
            "finite_count": 0,
        }

    return {
        "sample_count": int(flat.size),
        "finite_count": int(finite.size),
        "min": float(np.min(finite)),
        "max": float(np.max(finite)),
        "mean": float(np.mean(finite)),
        "std": float(np.std(finite)),
    }


def dataset_edge_preview(ds):
    if ds.size == 0:
        return None
    # Only preview very small or 1-D coordinate-like datasets.
    if len(ds.shape) == 1 and ds.shape[0] <= 4096 and np.issubdtype(ds.dtype, np.number):
        arr = np.asarray(ds[:])
        return {
            "first": jsonable(arr[:8]),
            "last": jsonable(arr[-8:]),
            "min": float(np.nanmin(arr)),
            "max": float(np.nanmax(arr)),
        }
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Inspect the JHTDB-derived HuggingFace velocity HDF5 without modifying it."
    )
    parser.add_argument(
        "h5",
        nargs="?",
        help="Path to isotropic1024-coarse-velocity.h5. If omitted, search project tree.",
    )
    parser.add_argument(
        "--no-hash",
        action="store_true",
        help="Skip full-file SHA-256 if you want a faster metadata-only pass.",
    )
    args = parser.parse_args()

    script = Path(__file__).resolve()
    project_root = script.parents[2] if len(script.parents) >= 3 else Path.cwd()

    h5_path = Path(args.h5).expanduser().resolve() if args.h5 else find_input(project_root)
    if not h5_path.exists():
        raise FileNotFoundError(h5_path)

    print("Inspecting:", h5_path)
    print("Size:", f"{h5_path.stat().st_size / (1024**3):.3f} GiB")

    report = {
        "report_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "UNNS turbulence pilot - immutable source HDF5 inspection",
        "input": {
            "path": str(h5_path),
            "filename": h5_path.name,
            "bytes": h5_path.stat().st_size,
            "gib": h5_path.stat().st_size / (1024**3),
        },
        "sha256": None,
        "hdf5": {},
        "observations": [],
    }

    if not args.no_hash:
        report["sha256"] = sha256_file(h5_path)

    tree_lines = []

    with h5py.File(h5_path, "r") as f:
        report["hdf5"]["root_attrs"] = attr_dict(f)
        report["hdf5"]["datasets"] = {}
        report["hdf5"]["groups"] = {}

        def visit(name, obj):
            indent = "  " * name.count("/")
            if isinstance(obj, h5py.Group):
                tree_lines.append(f"{indent}[GROUP] /{name}")
                report["hdf5"]["groups"][name] = {
                    "attrs": attr_dict(obj),
                }
            elif isinstance(obj, h5py.Dataset):
                tree_lines.append(
                    f"{indent}[DATASET] /{name} shape={obj.shape} dtype={obj.dtype} "
                    f"chunks={obj.chunks} compression={obj.compression}"
                )
                info = {
                    "shape": list(obj.shape),
                    "ndim": int(obj.ndim),
                    "size": int(obj.size),
                    "dtype": str(obj.dtype),
                    "chunks": list(obj.chunks) if obj.chunks else None,
                    "compression": obj.compression,
                    "compression_opts": jsonable(obj.compression_opts),
                    "shuffle": bool(obj.shuffle),
                    "fletcher32": bool(obj.fletcher32),
                    "scaleoffset": jsonable(obj.scaleoffset),
                    "fillvalue": jsonable(obj.fillvalue),
                    "attrs": attr_dict(obj),
                    "sparse_sample_stats": sparse_numeric_sample(obj),
                    "edge_preview": dataset_edge_preview(obj),
                }
                report["hdf5"]["datasets"][name] = info

        f.visititems(visit)

    # Structural observations only; no scientific claim is made here.
    ds_names = list(report["hdf5"]["datasets"])
    velocity_like = [
        n for n in ds_names
        if "vel" in n.lower() or n.lower().startswith("u") or "velocity_" in n.lower()
    ]
    if velocity_like:
        report["observations"].append(
            f"Velocity-like datasets found: {len(velocity_like)}."
        )

    root_attrs = report["hdf5"]["root_attrs"]
    keys_lower = {k.lower(): k for k in root_attrs}
    for key in ("dataset", "t_start", "t_end", "t_step", "x_start", "x_end",
                "y_start", "y_end", "z_start", "z_end", "filterwidth"):
        if key in keys_lower:
            report["observations"].append(
                f"Root attribute {keys_lower[key]}={root_attrs[keys_lower[key]]!r}"
            )

    output_dir = project_root / "outputs" / "records"
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "H5_REPORT.json"
    tree_path = output_dir / "H5_TREE.txt"

    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tree_path.write_text("\n".join(tree_lines) + "\n", encoding="utf-8")

    print()
    print("Wrote:")
    print(" ", report_path)
    print(" ", tree_path)
    print()
    print("The source HDF5 was opened READ-ONLY and was not modified.")


if __name__ == "__main__":
    main()

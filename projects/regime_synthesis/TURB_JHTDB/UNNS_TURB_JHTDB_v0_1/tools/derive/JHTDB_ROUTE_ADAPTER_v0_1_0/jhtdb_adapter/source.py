from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re

import h5py
import numpy as np


VELOCITY_RE = re.compile(r"^Velocity_(\d+)$")


def sha256_file(path: Path, progress=None):
    h = hashlib.sha256()
    total = path.stat().st_size
    read = 0
    with path.open("rb") as f:
        for block in iter(lambda: f.read(16 * 1024 * 1024), b""):
            h.update(block)
            read += len(block)
            if progress:
                progress(read / total if total else 1.0)
    return h.hexdigest()


def inspect_source(path: Path):
    with h5py.File(path, "r") as f:
        vsets = []
        for name in f.keys():
            m = VELOCITY_RE.match(name)
            if m:
                vsets.append((int(m.group(1)), name))
        vsets.sort()
        if not vsets:
            raise ValueError("No Velocity_#### datasets found.")

        first = f[vsets[0][1]]
        if first.ndim != 4 or first.shape[-1] != 3:
            raise ValueError(f"Unexpected velocity shape: {first.shape}")

        for _, name in vsets:
            if f[name].shape != first.shape:
                raise ValueError("Velocity frame shapes are inconsistent.")

        coords = {}
        for cname in ("xcoor", "ycoor", "zcoor"):
            if cname not in f:
                raise ValueError(f"Missing coordinate dataset: {cname}")
            coords[cname] = np.asarray(f[cname][:], dtype=float)

        # HDF5 GetCutout order is [z,y,x,component].
        nz, ny, nx, _ = first.shape
        if len(coords["xcoor"]) != nx or len(coords["ycoor"]) != ny or len(coords["zcoor"]) != nz:
            raise ValueError("Coordinate lengths do not match [z,y,x] velocity dimensions.")

        dx = float(np.median(np.diff(coords["xcoor"])))
        dy = float(np.median(np.diff(coords["ycoor"])))
        dz = float(np.median(np.diff(coords["zcoor"])))
        if not (np.isclose(dx, dy, rtol=1e-8, atol=1e-12) and np.isclose(dx, dz, rtol=1e-8, atol=1e-12)):
            raise ValueError(f"Non-isotropic grid spacing: dx={dx},dy={dy},dz={dz}")

        attrs = {str(k): _jsonable(v) for k, v in f.attrs.items()}
        return {
            "velocity_datasets": [name for _, name in vsets],
            "velocity_indices": [i for i, _ in vsets],
            "shape": list(first.shape),
            "dtype": str(first.dtype),
            "dx": dx,
            "origin_xyz": [
                float(coords["xcoor"][0]),
                float(coords["ycoor"][0]),
                float(coords["zcoor"][0]),
            ],
            "coordinate_ranges": {
                "x": [float(coords["xcoor"][0]), float(coords["xcoor"][-1])],
                "y": [float(coords["ycoor"][0]), float(coords["ycoor"][-1])],
                "z": [float(coords["zcoor"][0]), float(coords["zcoor"][-1])],
            },
            "root_attrs": attrs,
        }


def _jsonable(v):
    if isinstance(v, bytes):
        return v.decode("utf-8", errors="replace")
    if isinstance(v, np.ndarray):
        return v.tolist()
    if isinstance(v, np.generic):
        return v.item()
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    return repr(v)


def read_velocity_frame(path: Path, dataset_name: str):
    with h5py.File(path, "r") as f:
        return np.asarray(f[dataset_name][:], dtype=np.float32)


def parse_energy_history(path: Path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.split()
        if len(parts) != 3:
            continue
        try:
            t, e, re = map(float, parts)
        except Exception:
            continue
        rows.append((t, e, re))
    return rows


def nearest_energy_reference(rows, time_value: float):
    if not rows:
        return None
    return min(rows, key=lambda r: abs(r[0] - time_value))

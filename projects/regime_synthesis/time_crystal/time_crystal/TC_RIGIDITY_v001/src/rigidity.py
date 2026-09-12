from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path
import numpy as np


EXPECTED_METRIC_SHA256 = "06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553"


def sha256_bytes(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


class Artifact:
    """Read files from either an extracted package directory or its ZIP."""
    def __init__(self, path: str | Path):
        self.path = Path(path).resolve()
        if not self.path.exists():
            raise FileNotFoundError(self.path)
        self.is_zip = self.path.is_file() and self.path.suffix.lower() == ".zip"

    def _member(self, suffix: str) -> str:
        with zipfile.ZipFile(self.path, "r") as zf:
            names = [n for n in zf.namelist() if n.endswith(suffix)]
        if len(names) != 1:
            raise FileNotFoundError(f"{self.path}: expected one member ending {suffix}, found {len(names)}")
        return names[0]

    def read_bytes(self, suffix: str) -> bytes:
        if self.is_zip:
            with zipfile.ZipFile(self.path, "r") as zf:
                return zf.read(self._member(suffix))
        p = self.path / suffix
        if not p.exists():
            # Allow caller to pass suffix relative to package root even when
            # the package directory itself contains an additional same-name root.
            matches = list(self.path.rglob(Path(suffix).name))
            matches = [m for m in matches if str(m).replace("\\","/").endswith(suffix)]
            if len(matches) != 1:
                raise FileNotFoundError(p)
            p = matches[0]
        return p.read_bytes()

    def read_json(self, suffix: str) -> dict:
        return json.loads(self.read_bytes(suffix).decode("utf-8"))

    def read_csv(self, suffix: str) -> list[dict]:
        text = self.read_bytes(suffix).decode("utf-8")
        return list(csv.DictReader(io.StringIO(text)))


def verify_lock(lock_art: Artifact) -> tuple[dict, bytes]:
    lock = lock_art.read_json("LOCK.json")
    metric = lock_art.read_bytes("src/tc_closure.py")
    observed = sha256_bytes(metric)
    expected = lock["frozen_files"]["src/tc_closure.py"]
    if observed != expected or observed != EXPECTED_METRIC_SHA256:
        raise RuntimeError(
            "Frozen metric verification failed.\n"
            f"LOCK expected: {expected}\n"
            f"Package expected: {EXPECTED_METRIC_SHA256}\n"
            f"Observed: {observed}"
        )
    return lock, metric


def normalized_profile(vec: np.ndarray) -> np.ndarray:
    vec = np.asarray(vec, dtype=float)
    m = np.nanmax(np.abs(vec))
    return vec / m if np.isfinite(m) and m > 0 else vec.copy()


def geometry_similarity(a: np.ndarray, b: np.ndarray) -> dict:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    cosine = float(np.dot(a, b) / (na * nb + 1e-15))
    aa = normalized_profile(a)
    bb = normalized_profile(b)
    rms = float(np.sqrt(np.mean((aa - bb) ** 2)))
    return {
        "cosine_similarity": cosine,
        "normalized_RMS_distance": rms,
    }


def universality_score(values: list[float]) -> dict:
    x = np.asarray(values, dtype=float)
    mean = float(np.mean(x))
    sd = float(np.std(x, ddof=1)) if len(x) > 1 else 0.0
    cv = sd / abs(mean) if abs(mean) > 1e-15 else np.inf
    score = float(np.clip(1.0 - cv, 0.0, 1.0))
    return {
        "mean": mean,
        "sd": sd,
        "CV": float(cv),
        "U": score,
        "n": int(len(x)),
    }


def basin_area(rows: list[dict], xkey: str, ykey: str, boundary: float,
               seed_n: int = 5) -> dict:
    x = np.asarray([float(r[xkey]) for r in rows], dtype=float)
    y = np.asarray([float(r[ykey]) for r in rows], dtype=float)
    order = np.argsort(x)
    x, y = x[order], y[order]
    mask = x <= float(boundary) + 1e-12
    x, y = x[mask], y[mask]
    if len(x) < 2:
        return {"normalized_area": np.nan, "n_points": len(x)}

    x0 = float(x[0])
    width = float(boundary) - x0
    xn = (x - x0) / width if width > 0 else np.zeros_like(x)
    baseline = float(np.median(y[:min(seed_n, len(y))]))
    yn = y / baseline if abs(baseline) > 1e-15 else y * np.nan
    area = float(np.trapezoid(yn, xn))
    return {
        "normalized_area": area,
        "n_points": int(len(x)),
        "baseline": baseline,
        "boundary": float(boundary),
        "x_start": x0,
    }


def pareto_dominates(control: dict, target: dict, axes: list[str],
                     tol: float = 1e-12) -> dict:
    comparisons = {}
    all_ge = True
    any_gt = False
    for axis in axes:
        c = float(control[axis])
        t = float(target[axis])
        ge = c >= t - tol
        gt = c > t + tol
        comparisons[axis] = {
            "control": c,
            "target": t,
            "control_ge_target": bool(ge),
        }
        all_ge &= ge
        any_gt |= gt
    return {
        "axes": axes,
        "dominates_or_equals": bool(all_ge),
        "strictly_better_on_at_least_one_axis": bool(any_gt),
        "comparisons": comparisons,
    }


def spectrum_vector(rows: list[dict], label: str) -> np.ndarray:
    subset = sorted(
        [r for r in rows if r["label"] == label],
        key=lambda r: int(r["q"])
    )
    if len(subset) != 10:
        raise ValueError(f"{label}: expected 10 q values, found {len(subset)}")
    return np.asarray([float(r["closure"]) for r in subset], dtype=float)

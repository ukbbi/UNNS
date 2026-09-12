from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd


EXPECTED_METRIC_SHA256 = "06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553"


class Artifact:
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
            matches = [m for m in self.path.rglob(Path(suffix).name)
                       if str(m).replace("\\","/").endswith(suffix)]
            if len(matches) != 1:
                raise FileNotFoundError(p)
            p = matches[0]
        return p.read_bytes()

    def read_json(self, suffix: str) -> dict:
        return json.loads(self.read_bytes(suffix).decode("utf-8"))

    def read_csv(self, suffix: str) -> list[dict]:
        return list(csv.DictReader(io.StringIO(self.read_bytes(suffix).decode("utf-8"))))


class MiData:
    def __init__(self, path: str | Path):
        self.path = Path(path).resolve()
        if not self.path.exists():
            raise FileNotFoundError(self.path)

    def read(self, member: str) -> pd.DataFrame:
        with zipfile.ZipFile(self.path, "r") as zf:
            raw = zf.read(member).decode("utf-8-sig")
        return pd.read_csv(io.StringIO(raw))


def verify_provenance(lock: Artifact, mi: Artifact, ctrl: Artifact) -> dict:
    lock_json = lock.read_json("LOCK.json")
    metric = lock.read_bytes("src/tc_closure.py")
    import hashlib
    observed = hashlib.sha256(metric).hexdigest()
    expected = lock_json["frozen_files"]["src/tc_closure.py"]
    if observed != expected or observed != EXPECTED_METRIC_SHA256:
        raise RuntimeError("Frozen metric lock verification failed")

    mi_json = mi.read_json("outputs/external_validation.json")
    ctrl_json = ctrl.read_json("outputs/control_validation.json")
    if mi_json["frozen_metric_sha256"] != observed:
        raise RuntimeError("Mi external validation does not match frozen metric")
    if ctrl_json["metric_sha256"] != observed:
        raise RuntimeError("Control validation does not match frozen metric")
    return {
        "lock_id": lock_json["lock_id"],
        "metric_sha256": observed,
        "mi_validation_status": mi_json["status"],
        "control_validation_status": ctrl_json["status"],
    }


def spin_glass_scaling(df: pd.DataFrame) -> list[dict]:
    L = np.asarray([8.0, 12.0, 16.0, 20.0])
    rows = []
    for _, r in df.iterrows():
        y = np.asarray([r["s_8"], r["s_12"], r["s_16"], r["s_20"]], dtype=float)
        alpha = float(np.polyfit(np.log(L), np.log(y), 1)[0])
        slope = float(np.polyfit(L, y, 1)[0])
        rows.append({
            "g": float(r["g"]),
            "chi_8": float(y[0]),
            "chi_12": float(y[1]),
            "chi_16": float(y[2]),
            "chi_20": float(y[3]),
            "alpha_logL": alpha,
            "linear_slope": slope,
            "ratio_20_to_8": float(y[-1] / y[0]),
            "size_growth": bool(alpha > 0.0),
        })
    return rows


def crossing_interval(rows: list[dict]) -> dict:
    """
    Locate the first sign change of the empirical finite-size exponent alpha.
    No interpolation is used for the primary interval.
    """
    ordered = sorted(rows, key=lambda r: r["g"])
    for a, b in zip(ordered[:-1], ordered[1:]):
        if a["alpha_logL"] <= 0.0 < b["alpha_logL"]:
            return {
                "lower_g": a["g"],
                "upper_g": b["g"],
                "alpha_lower": a["alpha_logL"],
                "alpha_upper": b["alpha_logL"],
            }
    return {
        "lower_g": None, "upper_g": None,
        "alpha_lower": None, "alpha_upper": None,
    }


def spatial_localization(arr: np.ndarray) -> dict:
    """
    Fig. 3d matrix rows are qubit locations; columns are successive 10-cycle
    averaged windows. The final column corresponds to the late-time profile.

    Use absolute relative-response amplitudes and report:
      IPR = sum p_i^2
      N_eff = 1/IPR
      RMS radius around the maximal-response site.
    """
    v = np.abs(np.asarray(arr[:, -1], dtype=float))
    p = v / (np.sum(v) + 1e-15)
    ipr = float(np.sum(p * p))
    center = int(np.argmax(v))
    radius = float(np.sqrt(np.sum(p * (np.arange(len(v)) - center) ** 2)))
    return {
        "IPR": ipr,
        "N_eff": float(1.0 / ipr),
        "peak_site_zero_based": center,
        "RMS_radius_sites": radius,
        "total_relative_response": float(np.sum(v)),
    }


def distribution_stats(x: np.ndarray) -> dict:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    ax = np.abs(x)
    mu = float(np.mean(ax))
    sd = float(np.std(ax, ddof=1))
    return {
        "mean_abs": mu,
        "sd_abs": sd,
        "CV_abs": float(sd / mu) if mu > 0 else np.inf,
        "q05_abs": float(np.quantile(ax, 0.05)),
        "median_abs": float(np.quantile(ax, 0.50)),
        "q95_abs": float(np.quantile(ax, 0.95)),
        "n": int(len(ax)),
    }


def typicality_stats(df: pd.DataFrame, mapping: dict[int, str]) -> list[dict]:
    rows = []
    for K, col in sorted(mapping.items()):
        st = distribution_stats(df[col].to_numpy(dtype=float))
        rows.append({"K": int(K), "column": col, **st})
    return rows


def typicality_summary(rows: list[dict]) -> dict:
    ordered = sorted(rows, key=lambda r: r["K"])
    a, b = ordered[0], ordered[-1]
    return {
        "K_min": a["K"],
        "K_max": b["K"],
        "mean_abs_initial": a["mean_abs"],
        "mean_abs_final": b["mean_abs"],
        "mean_retention": float(b["mean_abs"] / a["mean_abs"]) if a["mean_abs"] > 0 else np.nan,
        "sd_initial": a["sd_abs"],
        "sd_final": b["sd_abs"],
        "sd_contraction_factor": float(a["sd_abs"] / b["sd_abs"]) if b["sd_abs"] > 0 else np.inf,
        "final_CV": b["CV_abs"],
    }


def classical_spin_glass_analogue(L_values=(8,12,16,20)) -> list[dict]:
    """
    Same mathematical Edwards-Anderson pair-order form for a deterministic
    classical sign-flip two-cycle with fixed site values z_i=±1.

    Excluding the two edge sites and summing ordered i != j interior pairs:
      chi_cl = [(L-2)(L-3)]/(L-2) = L-3.

    This is intentionally a counterexample showing that extensive pair order
    alone is not uniquely quantum or DTC-specific.
    """
    return [{"L": int(L), "chi_classical": float(L - 3)} for L in L_values]


def classical_localization_analogue(L=20, perturb_site=9) -> dict:
    """
    For an uncoupled exact sign-flip map X_(t+1)=-X_t, changing one coordinate
    remains confined to that coordinate forever.
    """
    p = np.zeros(L, dtype=float)
    p[perturb_site] = 1.0
    ipr = float(np.sum(p*p))
    return {
        "IPR": ipr,
        "N_eff": float(1/ipr),
        "RMS_radius_sites": 0.0,
        "interpretation": "perfectly localized classical perturbation",
    }

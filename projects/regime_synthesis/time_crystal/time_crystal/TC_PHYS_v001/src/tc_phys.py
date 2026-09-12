from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import io
import re
import zipfile
import numpy as np

N_ITER = 5
N_TIME = 51
N_QUBIT = 57
DTYPE = np.float32
EXPECTED_VALUES = N_ITER * N_TIME * N_QUBIT
EXPECTED_BYTES = EXPECTED_VALUES * np.dtype(DTYPE).itemsize
PARITY = (-1.0) ** np.arange(N_TIME)

EPS_RE = re.compile(r"_Eps(\d+)_")
SPECIAL_MARKERS = ("POL", "NEEL", "NoDIS", "RND_RefDis", "PolND_RefDis", "epsref1")


def parse_epsilon(name: str) -> float:
    m = EPS_RE.search(name)
    if not m:
        raise ValueError(f"Cannot parse epsilon from {name}")
    code = m.group(1)
    return int(code) / (10 ** (len(code) - 1))


def is_regular_file(name: str) -> bool:
    return not any(tag in name for tag in SPECIAL_MARKERS)


def classify_file(name: str) -> dict:
    if "_NEEL" in name:
        initial = "neel"
    elif "_POL" in name or "_PolND_" in name:
        initial = "polarized"
    elif "_RND_" in name:
        initial = "random"
    else:
        initial = "standard_untagged"

    if "NoDIS" in name or "PolND" in name:
        disorder = "no_disorder_tagged"
    elif "RefDis" in name:
        disorder = "reference_disorder_tagged"
    else:
        disorder = "standard_or_unspecified"

    device = "Brooklyn" if "_Bro57_" in name else "Manhattan" if "_Man57_" in name else "unknown"
    return {"initial_state": initial, "disorder": disorder, "device": device}


class DataSource:
    """Read the supplied .dat corpus either from Data.zip or an extracted directory."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._zip = None
        if self.path.is_file() and self.path.suffix.lower() == ".zip":
            self._zip = zipfile.ZipFile(self.path, "r")
            self._names = sorted(
                n for n in self._zip.namelist()
                if n.lower().endswith(".dat") and "/._" not in n and not Path(n).name.startswith("._")
            )
        elif self.path.is_dir():
            self._names = [str(p) for p in sorted(self.path.rglob("*.dat")) if not p.name.startswith("._")]
        else:
            raise FileNotFoundError(f"Input not found: {self.path}")

    def names(self) -> list[str]:
        return [Path(n).name for n in self._names]

    def iter_arrays(self):
        for n in self._names:
            name = Path(n).name
            if self._zip:
                raw = self._zip.read(n)
                if len(raw) != EXPECTED_BYTES:
                    raise ValueError(f"{name}: {len(raw)} bytes, expected {EXPECTED_BYTES}")
                arr = np.frombuffer(raw, dtype=DTYPE).copy()
            else:
                p = Path(n)
                if p.stat().st_size != EXPECTED_BYTES:
                    raise ValueError(f"{name}: {p.stat().st_size} bytes, expected {EXPECTED_BYTES}")
                arr = np.fromfile(p, dtype=DTYPE)
            if arr.size != EXPECTED_VALUES:
                raise ValueError(f"{name}: {arr.size} float32 values, expected {EXPECTED_VALUES}")
            yield name, arr.reshape(N_ITER, N_TIME, N_QUBIT).astype(np.float64)


def measurement_correct(raw_tq: np.ndarray, final_points: int = 5) -> np.ndarray:
    """
    Operational reconstruction of Eq. (4):
      m_corr(t) = [m_meas(t) - m_final] / |m_meas(0) - m_final|
    with m_final taken as the mean of the last `final_points` samples.
    """
    final = np.nanmean(raw_tq[-final_points:], axis=0)
    denom = np.abs(raw_tq[0] - final)
    denom = np.where(denom > 1e-8, denom, np.nan)
    return (raw_tq - final) / denom


def align_period2(corrected_tq: np.ndarray) -> np.ndarray:
    """
    Remove the known ideal 2T sign alternation and the initial-state sign.
    This is used only to fit the depolarization envelope and to represent
    half-frequency order as a slowly varying positive/negative amplitude.
    """
    s0 = np.sign(corrected_tq[0]).astype(float)
    s0[s0 == 0] = 1.0
    return corrected_tq * s0[None, :] * PARITY[:, None]


def fit_reference_eq7(aligned_ref_tq: np.ndarray, fit_start: int = 13) -> dict:
    """
    Fit the stated Eq. (7) structural form
        1/2 [m(t) + sign(m(t))] = a exp(-b t) + c
    after removing the known 2T sign alternation.

    b is searched on a fixed grid; for each b, a and c are solved exactly
    by linear least squares. This avoids a nonlinear optimizer dependency.
    """
    t = np.arange(fit_start, N_TIME, dtype=float)
    y = 0.5 * (aligned_ref_tq[fit_start:] + np.sign(aligned_ref_tq[fit_start:]))

    # The supplied data are finite for essentially all usable qubits.
    # Fill any rare non-finite entry columnwise to keep the vectorized fit stable.
    y2 = y.copy()
    for q in range(N_QUBIT):
        col = y2[:, q]
        good = np.isfinite(col)
        if not good.any():
            col[:] = 0.0
        elif not good.all():
            col[~good] = np.nanmedian(col[good])

    b_grid = np.linspace(0.0, 0.35, 351)
    e = np.exp(-b_grid[:, None] * t[None, :])           # [B,T]
    ec = e - e.mean(axis=1, keepdims=True)
    var_e = np.sum(ec * ec, axis=1)                    # [B]

    yc = y2 - y2.mean(axis=0, keepdims=True)           # [T,Q]
    cov = ec @ yc                                      # [B,Q]
    a_all = cov / np.where(var_e[:, None] > 1e-12, var_e[:, None], np.nan)
    c_all = y2.mean(axis=0)[None, :] - a_all * e.mean(axis=1)[:, None]

    ssy = np.sum(yc * yc, axis=0)[None, :]
    sse = ssy - (cov * cov) / np.where(var_e[:, None] > 1e-12, var_e[:, None], np.nan)
    sse = np.maximum(sse, 0.0)

    idx = np.nanargmin(sse, axis=0)
    q = np.arange(N_QUBIT)
    a = a_all[idx, q]
    b = b_grid[idx]
    c = c_all[idx, q]
    best_sse = sse[idx, q]
    rmse = np.sqrt(best_sse / len(t))

    # R^2 in the transformed fit space.
    total = np.sum((y2 - y2.mean(axis=0, keepdims=True)) ** 2, axis=0)
    r2 = 1.0 - best_sse / np.where(total > 1e-12, total, np.nan)

    return {"a": a, "b": b, "c": c, "rmse": rmse, "r2": r2}


@dataclass
class PreparedRecord:
    name: str
    epsilon: float
    meta: dict
    ref: np.ndarray
    target: np.ndarray
    bar_ref: np.ndarray
    bar_target: np.ndarray
    fit_a: np.ndarray
    fit_b: np.ndarray
    fit_c: np.ndarray
    fit_rmse: np.ndarray
    fit_r2: np.ndarray


def prepare_record(name: str, arr: np.ndarray, final_points: int = 5, fit_start: int = 13) -> PreparedRecord:
    ref = align_period2(measurement_correct(arr[0], final_points=final_points))
    targets = np.stack(
        [align_period2(measurement_correct(arr[k], final_points=final_points)) for k in range(1, N_ITER)],
        axis=0,
    )
    target = np.nanmean(targets, axis=0)

    # The paper states that the bar denotes an average over five timesteps
    # after the initial 13 timesteps: operationally t = 13..17.
    bar_ref = np.nanmean(ref[13:18], axis=0)
    bar_target = np.nanmean(target[13:18], axis=0)

    fit = fit_reference_eq7(ref, fit_start=fit_start)
    return PreparedRecord(
        name=name,
        epsilon=parse_epsilon(name),
        meta=classify_file(name),
        ref=ref,
        target=target,
        bar_ref=bar_ref,
        bar_target=bar_target,
        fit_a=fit["a"],
        fit_b=fit["b"],
        fit_c=fit["c"],
        fit_rmse=fit["rmse"],
        fit_r2=fit["r2"],
    )


def mitigate_record(
    rec: PreparedRecord,
    W0: float = 0.15,
    Wf_ratio: float = 2.0 / 3.0,
    rescale_start: int = 13,
) -> dict:
    Wf = W0 * Wf_ratio
    accepted = (
        np.isfinite(rec.bar_ref)
        & np.isfinite(rec.bar_target)
        & np.isfinite(rec.fit_a)
        & np.isfinite(rec.fit_b)
        & np.isfinite(rec.fit_c)
        & (rec.bar_ref >= W0)
    )
    thermal = np.abs(rec.bar_target) <= Wf

    out = rec.target.copy()
    t = np.arange(N_TIME, dtype=float)
    invalid_fit = np.zeros(N_QUBIT, dtype=bool)

    for q in np.flatnonzero(accepted & ~thermal):
        denom = rec.fit_a[q] * np.exp(-rec.fit_b[q] * t) + rec.fit_c[q]
        # Only reject numerically unusable fitted denominators.
        if (not np.all(np.isfinite(denom[rescale_start:]))) or np.any(np.abs(denom[rescale_start:]) < 0.05):
            invalid_fit[q] = True
            continue

        ratio = rec.bar_target[q] / rec.bar_ref[q]
        m = rec.target[:, q]
        # Eq. (8), applied after the initial transient window.
        M = ratio * (m + np.sign(m)) / denom - np.sign(m)
        out[rescale_start:, q] = M[rescale_start:]

    accepted &= ~invalid_fit
    return {
        "aligned_mitigated": out,
        "accepted": accepted,
        "thermal": thermal,
        "W0": W0,
        "Wf": Wf,
    }


def half_frequency_amplitude(aligned_tq: np.ndarray) -> np.ndarray:
    """
    In the aligned representation, the exact omega_D/2 component of the
    original alternating signal is the zero-frequency sum of aligned data.
    Normalize by N_TIME so a perfect 2T signal has amplitude about 1.
    """
    return np.abs(np.nansum(aligned_tq, axis=0)) / aligned_tq.shape[0]


def decay_constants(aligned_tq: np.ndarray, start: int = 13, stop: int = 31) -> np.ndarray:
    """
    Reconstruct delta_i from |Z_i| ~ exp(-delta_i t) after initial transients.
    Uses log-linear least squares on usable points in t=[start, stop).
    """
    t = np.arange(start, stop, dtype=float)
    out = np.full(aligned_tq.shape[1], np.nan)
    for q in range(aligned_tq.shape[1]):
        y = np.abs(aligned_tq[start:stop, q])
        good = np.isfinite(y) & (y > 0.03)
        if good.sum() < 6:
            continue
        coeff = np.polyfit(t[good], np.log(y[good]), 1)
        out[q] = max(0.0, -float(coeff[0]))
    return out


def record_metrics(rec: PreparedRecord, W0: float = 0.15, Wf_ratio: float = 2.0 / 3.0) -> tuple[dict, list[dict]]:
    mit = mitigate_record(rec, W0=W0, Wf_ratio=Wf_ratio)
    ok = mit["accepted"]
    z = mit["aligned_mitigated"][:, ok]

    if ok.any():
        h = half_frequency_amplitude(z)
        delta = decay_constants(z)
        metrics = {
            "filename": rec.name,
            "epsilon": rec.epsilon,
            "device": rec.meta["device"],
            "initial_state": rec.meta["initial_state"],
            "disorder": rec.meta["disorder"],
            "n_qubits_total": N_QUBIT,
            "n_qubits_accepted": int(ok.sum()),
            "n_qubits_rejected": int(N_QUBIT - ok.sum()),
            "thermal_fraction_accepted": float(np.mean(mit["thermal"][ok])),
            "half_frequency_mean": float(np.nanmean(h)),
            "half_frequency_variance": float(np.nanvar(h)),
            "delta_mean": float(np.nanmean(delta)) if np.isfinite(delta).any() else np.nan,
            "late_aligned_mean_20_40": float(np.nanmean(z[20:41])),
            "fit_r2_median_accepted": float(np.nanmedian(rec.fit_r2[ok])),
        }
    else:
        metrics = {
            "filename": rec.name,
            "epsilon": rec.epsilon,
            "device": rec.meta["device"],
            "initial_state": rec.meta["initial_state"],
            "disorder": rec.meta["disorder"],
            "n_qubits_total": N_QUBIT,
            "n_qubits_accepted": 0,
            "n_qubits_rejected": N_QUBIT,
            "thermal_fraction_accepted": np.nan,
            "half_frequency_mean": np.nan,
            "half_frequency_variance": np.nan,
            "delta_mean": np.nan,
            "late_aligned_mean_20_40": np.nan,
            "fit_r2_median_accepted": np.nan,
        }

    qrows = []
    Wf = W0 * Wf_ratio
    for q in range(N_QUBIT):
        reason = "accepted"
        if not np.isfinite(rec.bar_ref[q]) or not np.isfinite(rec.bar_target[q]):
            reason = "nonfinite"
        elif rec.bar_ref[q] < W0:
            reason = "reference_below_W0"
        elif not np.isfinite(rec.fit_a[q] + rec.fit_b[q] + rec.fit_c[q]):
            reason = "fit_invalid"
        elif not ok[q]:
            reason = "fit_denominator_invalid"
        qrows.append({
            "filename": rec.name,
            "epsilon": rec.epsilon,
            "qubit": q,
            "accepted": bool(ok[q]),
            "reason": reason,
            "bar_ref_13_17": float(rec.bar_ref[q]) if np.isfinite(rec.bar_ref[q]) else np.nan,
            "bar_target_13_17": float(rec.bar_target[q]) if np.isfinite(rec.bar_target[q]) else np.nan,
            "thermal_no_rescale": bool(mit["thermal"][q]),
            "W0": W0,
            "Wf": Wf,
            "fit_a": float(rec.fit_a[q]) if np.isfinite(rec.fit_a[q]) else np.nan,
            "fit_b": float(rec.fit_b[q]) if np.isfinite(rec.fit_b[q]) else np.nan,
            "fit_c": float(rec.fit_c[q]) if np.isfinite(rec.fit_c[q]) else np.nan,
            "fit_rmse": float(rec.fit_rmse[q]) if np.isfinite(rec.fit_rmse[q]) else np.nan,
            "fit_r2": float(rec.fit_r2[q]) if np.isfinite(rec.fit_r2[q]) else np.nan,
        })
    return metrics, qrows


def aggregate_regular(file_rows: list[dict]) -> list[dict]:
    regular = [r for r in file_rows if is_regular_file(r["filename"]) and np.isfinite(r["half_frequency_variance"])]
    eps_values = sorted(set(r["epsilon"] for r in regular))
    out = []
    for e in eps_values:
        g = [r for r in regular if r["epsilon"] == e]
        def med(key):
            vals = np.asarray([r[key] for r in g], dtype=float)
            return float(np.nanmedian(vals)) if np.isfinite(vals).any() else np.nan
        out.append({
            "epsilon": e,
            "n_files": len(g),
            "accepted_qubits_median": med("n_qubits_accepted"),
            "half_frequency_mean_median": med("half_frequency_mean"),
            "half_frequency_variance_median": med("half_frequency_variance"),
            "delta_mean_median": med("delta_mean"),
            "late_aligned_mean_median": med("late_aligned_mean_20_40"),
            "thermal_fraction_median": med("thermal_fraction_accepted"),
        })
    return out


def gaussian_smooth_peak(scan_rows: list[dict], key: str, max_epsilon: float = 0.20) -> dict:
    rows = [r for r in scan_rows if r["epsilon"] <= max_epsilon and np.isfinite(r[key])]
    x = np.asarray([r["epsilon"] for r in rows], dtype=float)
    y = np.asarray([r[key] for r in rows], dtype=float)
    order = np.argsort(x)
    x, y = x[order], y[order]
    if len(x) < 5:
        return {"peak_epsilon": np.nan, "bandwidth": np.nan, "raw_peak_epsilon": np.nan}

    gaps = np.diff(np.unique(x))
    positive = gaps[gaps > 0]
    grid_step = float(np.median(positive)) if len(positive) else 0.01
    bandwidth = 2.5 * grid_step

    grid = np.linspace(float(x.min()), float(x.max()), 2001)
    sm = np.empty_like(grid)
    for i, z in enumerate(grid):
        w = np.exp(-0.5 * ((x - z) / bandwidth) ** 2)
        sm[i] = np.sum(w * y) / np.sum(w)
    j = int(np.argmax(sm))
    return {
        "peak_epsilon": float(grid[j]),
        "bandwidth": float(bandwidth),
        "raw_peak_epsilon": float(x[int(np.argmax(y))]),
        "grid": grid,
        "smooth": sm,
        "x": x,
        "y": y,
    }


def segmented_decay_break(scan_rows: list[dict], max_epsilon: float = 0.20) -> dict:
    rows = [r for r in scan_rows if r["epsilon"] <= max_epsilon and np.isfinite(r["delta_mean_median"])]
    x = np.asarray([r["epsilon"] for r in rows], dtype=float)
    y = np.asarray([r["delta_mean_median"] for r in rows], dtype=float)
    order = np.argsort(x)
    x, y = x[order], y[order]

    best = None
    # At least five points on each side; break point belongs to both segments.
    for k in range(4, len(x) - 4):
        x1, y1 = x[:k+1], y[:k+1]
        x2, y2 = x[k:], y[k:]
        c1 = np.polyfit(x1, y1, 1)
        c2 = np.polyfit(x2, y2, 1)
        sse = float(np.sum((y1 - np.polyval(c1, x1)) ** 2) + np.sum((y2 - np.polyval(c2, x2)) ** 2))
        if best is None or sse < best["sse"]:
            best = {
                "break_epsilon": float(x[k]),
                "sse": sse,
                "left_slope": float(c1[0]),
                "right_slope": float(c2[0]),
                "x": x,
                "y": y,
            }
    return best or {"break_epsilon": np.nan, "sse": np.nan, "left_slope": np.nan, "right_slope": np.nan, "x": x, "y": y}

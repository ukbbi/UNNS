#!/usr/bin/env python3
"""
VREF-I/A — Vacuum-Referenced Profile Representation, refinement calibration.

Frozen source:
  Baker et al. 2022, pure SU(3), E_x^NP(x_t), x_l=d/4≈0.128 fm.

This chamber is calibration-only. It cannot emit a Structural Vacuum
Continuity or Isolation verdict.

Dependencies: numpy, matplotlib
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception as exc:
    plt = None
    _MATPLOTLIB_ERROR = repr(exc)
else:
    _MATPLOTLIB_ERROR = None


EPS = np.finfo(float).eps


class VREFError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_config(script_dir: Path) -> dict:
    path = script_dir / "VREF_A_CONFIG.json"
    if not path.exists():
        raise VREFError(f"Missing frozen config: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_table(path: Path):
    if not path.exists():
        raise VREFError(f"Missing admitted source table: {path}")
    try:
        arr = np.loadtxt(path, comments="#", dtype=float)
    except Exception as exc:
        raise VREFError(f"Could not parse {path}: {exc}") from exc
    if arr.ndim != 2 or arr.shape[1] != 3:
        raise VREFError(f"{path.name}: expected exactly 3 numerical columns, got shape {arr.shape}")
    x, y, e = arr[:, 0], arr[:, 1], arr[:, 2]
    if not (np.all(np.isfinite(x)) and np.all(np.isfinite(y)) and np.all(np.isfinite(e))):
        raise VREFError(f"{path.name}: non-finite value detected")
    if np.any(e < 0):
        raise VREFError(f"{path.name}: negative published error detected")
    return x, y, e


def positive_branch_with_symmetry_check(x, y, e, name: str, tol=1e-12):
    neg = np.where(x < -tol)[0]
    pos = np.where(x > tol)[0]
    zero = np.where(np.abs(x) <= tol)[0]
    if len(zero) != 1:
        raise VREFError(f"{name}: expected exactly one x_t=0 row; found {len(zero)}")

    xneg = -x[neg][::-1]
    yneg = y[neg][::-1]
    eneg = e[neg][::-1]
    xpos = x[pos]
    ypos = y[pos]
    epos = e[pos]

    if len(neg) != len(pos):
        raise VREFError(f"{name}: positive/negative branch lengths differ ({len(pos)} vs {len(neg)})")
    if not np.allclose(xneg, xpos, rtol=0.0, atol=tol):
        raise VREFError(f"{name}: mirrored transverse coordinates are not exact within {tol:g}")
    if not np.allclose(yneg, ypos, rtol=0.0, atol=tol):
        raise VREFError(f"{name}: mirrored central values are not exact within {tol:g}")
    if not np.allclose(eneg, epos, rtol=0.0, atol=tol):
        raise VREFError(f"{name}: mirrored error values are not exact within {tol:g}")

    ids = np.concatenate([zero, pos])
    ids = ids[np.argsort(x[ids])]
    xp, yp, ep = x[ids], y[ids], e[ids]
    if not np.all(np.diff(xp) > 0):
        raise VREFError(f"{name}: non-negative branch is not strictly ordered")
    return xp, yp, ep


def linear_interp_no_extrap(x, y, xq):
    xq = np.asarray(xq, dtype=float)
    tol = 1e-12
    if np.min(xq) < np.min(x) - tol or np.max(xq) > np.max(x) + tol:
        raise VREFError(
            f"Common-grid request [{np.min(xq):.9g}, {np.max(xq):.9g}] "
            f"exceeds native support [{np.min(x):.9g}, {np.max(x):.9g}]"
        )
    return np.interp(xq, x, y)


def _pchip_slopes(x, y):
    """Fritsch-Butland / PCHIP derivative construction."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    if n < 2:
        raise VREFError("PCHIP needs at least two points")
    h = np.diff(x)
    delta = np.diff(y) / h
    d = np.zeros(n, dtype=float)

    if n == 2:
        d[:] = delta[0]
        return d

    # Interior derivatives
    for k in range(1, n - 1):
        if delta[k - 1] == 0.0 or delta[k] == 0.0 or np.sign(delta[k - 1]) != np.sign(delta[k]):
            d[k] = 0.0
        else:
            w1 = 2.0 * h[k] + h[k - 1]
            w2 = h[k] + 2.0 * h[k - 1]
            d[k] = (w1 + w2) / (w1 / delta[k - 1] + w2 / delta[k])

    # Endpoints, matching the standard PCHIP endpoint rule
    d0 = ((2.0 * h[0] + h[1]) * delta[0] - h[0] * delta[1]) / (h[0] + h[1])
    if np.sign(d0) != np.sign(delta[0]):
        d0 = 0.0
    elif np.sign(delta[0]) != np.sign(delta[1]) and abs(d0) > abs(3.0 * delta[0]):
        d0 = 3.0 * delta[0]
    d[0] = d0

    dn = ((2.0 * h[-1] + h[-2]) * delta[-1] - h[-1] * delta[-2]) / (h[-1] + h[-2])
    if np.sign(dn) != np.sign(delta[-1]):
        dn = 0.0
    elif np.sign(delta[-1]) != np.sign(delta[-2]) and abs(dn) > abs(3.0 * delta[-1]):
        dn = 3.0 * delta[-1]
    d[-1] = dn
    return d


def pchip_interp_no_extrap(x, y, xq):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xq = np.asarray(xq, dtype=float)
    tol = 1e-12
    if np.min(xq) < np.min(x) - tol or np.max(xq) > np.max(x) + tol:
        raise VREFError("PCHIP extrapolation is prohibited")
    d = _pchip_slopes(x, y)
    out = np.empty_like(xq, dtype=float)

    for qi, q in enumerate(xq):
        if abs(q - x[-1]) <= tol:
            i = len(x) - 2
        else:
            i = int(np.searchsorted(x, q, side="right") - 1)
            i = max(0, min(i, len(x) - 2))
        h = x[i + 1] - x[i]
        t = (q - x[i]) / h
        h00 = 2*t**3 - 3*t**2 + 1
        h10 = t**3 - 2*t**2 + t
        h01 = -2*t**3 + 3*t**2
        h11 = t**3 - t**2
        out[qi] = h00*y[i] + h10*h*d[i] + h01*y[i+1] + h11*h*d[i+1]
    return out


def rms(v):
    v = np.asarray(v, dtype=float)
    return float(np.sqrt(np.mean(v * v)))


def linf(v):
    return float(np.max(np.abs(v)))


def rms_error_envelope(z, eps):
    """
    Exact extrema of RMS over independent box intervals z_j±eps_j.
    Min chooses the point in each interval nearest zero; max chooses farthest.
    """
    z = np.asarray(z, dtype=float)
    eps = np.asarray(eps, dtype=float)
    absz = np.abs(z)
    min_abs = np.maximum(absz - eps, 0.0)
    max_abs = absz + eps
    return rms(min_abs), rms(max_abs)


def sign_class(x, tol=1e-12):
    if x > tol:
        return 1
    if x < -tol:
        return -1
    return 0


def sequence_direction_signature(values):
    values = list(map(float, values))
    scale = max(1.0, *(abs(v) for v in values))
    tol = 1e-12 * scale
    return tuple(sign_class(values[i+1] - values[i], tol) for i in range(len(values)-1))


def ordering_signature(values):
    # Stable ordinal ranking; ties are represented by equal rounded bins only at numerical tolerance.
    vals = list(map(float, values))
    scale = max(1.0, *(abs(v) for v in vals))
    tol = 1e-12 * scale
    pairs = []
    for i in range(len(vals)):
        row = []
        for j in range(len(vals)):
            row.append(sign_class(vals[i] - vals[j], tol))
        pairs.append(tuple(row))
    return tuple(pairs)


def c_class(c):
    if not np.isfinite(c):
        return None
    tol = 1e-12 * max(1.0, abs(c))
    return sign_class(c - 1.0, tol)


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def format_float(x):
    if x is None:
        return ""
    if isinstance(x, (float, np.floating)):
        if math.isnan(float(x)):
            return "nan"
        return f"{float(x):.12g}"
    return x


def self_test():
    # Linear interpolation
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0, 2.0])
    q = np.array([0.5, 1.5])
    assert np.allclose(linear_interp_no_extrap(x, y, q), [0.5, 1.5])

    # PCHIP exactly reproduces a straight line
    assert np.allclose(pchip_interp_no_extrap(x, y, q), [0.5, 1.5])

    # RMS box envelope
    lo, hi = rms_error_envelope(np.array([2.0, -1.0]), np.array([0.5, 2.0]))
    assert abs(lo - math.sqrt((1.5**2 + 0.0**2)/2.0)) < 1e-12
    assert abs(hi - math.sqrt((2.5**2 + 3.0**2)/2.0)) < 1e-12

    # Signatures
    assert sequence_direction_signature([3, 2, 1]) == (-1, -1)
    assert c_class(0.8) == -1 and c_class(1.2) == 1
    print("VREF-I/A self-test: PASS")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", type=Path, default=None)
    ap.add_argument("--validate-only", action="store_true",
                    help="Run source/hash/support integrity checks and stop before metric computation.")
    ap.add_argument("--self-test", action="store_true",
                    help="Run synthetic implementation tests and exit.")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        return 0

    script_dir = Path(__file__).resolve().parent
    cfg = load_config(script_dir)
    project_root = args.project_root.resolve() if args.project_root else script_dir.parent.parent.resolve()

    # Paths
    source_base = project_root / cfg["source_base"]
    source_records = []
    native = {}

    # Mandatory source/hash/ingestion/symmetry checks
    for spec in cfg["sources"]:
        path = source_base / spec["file"]
        actual_hash = sha256_file(path)
        if actual_hash.lower() != spec["sha256"].lower():
            raise VREFError(
                f"{spec['file']}: SHA-256 mismatch\n"
                f"expected {spec['sha256']}\nactual   {actual_hash}"
            )
        x, y, e = load_table(path)
        xp, yp, ep = positive_branch_with_symmetry_check(x, y, e, spec["file"])
        native[spec["level"]] = {
            "spec": spec, "path": path, "x": xp, "y": yp, "e": ep,
            "rows_total": len(x), "rows_nonnegative": len(xp),
            "support_min": float(np.min(x)), "support_max": float(np.max(x))
        }
        source_records.append({
            "level": spec["level"],
            "beta": spec["beta"],
            "file": str(path.relative_to(project_root)),
            "sha256": actual_hash,
            "rows_total": len(x),
            "rows_nonnegative": len(xp),
            "support_min_fm": float(np.min(x)),
            "support_max_fm": float(np.max(x)),
        })

    xgrid = np.array(cfg["grid"]["x_fm"], dtype=float)
    ugrid = np.array(cfg["grid"]["u"], dtype=float)
    for level, rec in native.items():
        if xgrid[0] < rec["x"][0] - 1e-12 or xgrid[-1] > rec["x"][-1] + 1e-12:
            raise VREFError(f"{level}: frozen common grid exceeds native non-negative support")

    if args.validate_only:
        print("VREF-I/A source validation: PASS")
        for r in source_records:
            print(
                f"{r['level']} beta={r['beta']:.3f}: "
                f"rows={r['rows_total']}, nonnegative={r['rows_nonnegative']}, "
                f"support=[{r['support_min_fm']:.6f},{r['support_max_fm']:.6f}] fm"
            )
        print("No VREF-I/A metrics were computed (--validate-only).")
        return 0

    if plt is None:
        raise VREFError(
            "matplotlib is required for the frozen figure outputs. "
            f"Import error: {_MATPLOTLIB_ERROR}"
        )

    l2 = float(cfg["constants"]["l_ref_squared_GeV_inv2"])
    offsets = np.array(cfg["windows"]["offsets_u"], dtype=float)
    starts = np.array(cfg["windows"]["starts_u"], dtype=float)

    profiles = {}
    loo_rows = []

    for level, rec in native.items():
        x, y, e = rec["x"], rec["y"], rec["e"]
        y_lin = linear_interp_no_extrap(x, y, xgrid)
        e_lin = linear_interp_no_extrap(x, e, xgrid)
        y_pchip = pchip_interp_no_extrap(x, y, xgrid)

        profiles[level] = {
            "spec": rec["spec"],
            "y_linear": y_lin,
            "e_linear": e_lin,
            "y_pchip": y_pchip,
            "z_linear": l2 * y_lin,
            "eps_z": l2 * e_lin,
            "z_pchip": l2 * y_pchip,
        }

        # Leave-one-out linear interpolation diagnostic on native positive branch
        for i in range(1, len(x)-1):
            pred = np.interp(x[i], [x[i-1], x[i+1]], [y[i-1], y[i+1]])
            resid = pred - y[i]
            err = e[i]
            loo_rows.append({
                "level": level,
                "beta": rec["spec"]["beta"],
                "x_fm": x[i],
                "observed_GeV2": y[i],
                "predicted_GeV2": pred,
                "residual_GeV2": resid,
                "abs_residual_GeV2": abs(resid),
                "published_error_GeV2": err,
                "abs_residual_over_error": abs(resid)/err if err > 0 else float("nan"),
                "abs_residual_over_abs_value": abs(resid)/abs(y[i]) if y[i] != 0 else float("nan")
            })

    # Grid output
    grid_rows = [{"j": j, "u": u, "x_fm": x} for j, (u, x) in enumerate(zip(ugrid, xgrid))]
    write_csv(
        project_root / cfg["outputs"]["grid_csv"],
        ["j", "u", "x_fm"],
        [{k: format_float(v) for k, v in r.items()} for r in grid_rows]
    )

    # Profile output
    profile_rows = []
    for level in ["R1", "R2", "R3"]:
        p = profiles[level]
        spec = p["spec"]
        for j, (u, x) in enumerate(zip(ugrid, xgrid)):
            profile_rows.append({
                "level": level,
                "beta": spec["beta"],
                "j": j,
                "u": u,
                "x_fm": x,
                "EX_NP_linear_GeV2": p["y_linear"][j],
                "EX_NP_error_linear_GeV2": p["e_linear"][j],
                "EX_NP_pchip_GeV2": p["y_pchip"][j],
                "z_linear": p["z_linear"][j],
                "eps_z": p["eps_z"][j],
                "z_pchip": p["z_pchip"][j],
                "pchip_minus_linear_z": p["z_pchip"][j] - p["z_linear"][j],
            })
    write_csv(
        project_root / cfg["outputs"]["profile_csv"],
        list(profile_rows[0].keys()),
        [{k: format_float(v) for k, v in r.items()} for r in profile_rows]
    )

    # LOO output
    write_csv(
        project_root / cfg["outputs"]["loo_csv"],
        list(loo_rows[0].keys()),
        [{k: format_float(v) for k, v in r.items()} for r in loo_rows]
    )

    # Window metrics for linear and PCHIP
    window_rows = []
    distance_series = {"linear": {k: [] for k in profiles}, "pchip": {k: [] for k in profiles}}
    for interp in ["linear", "pchip"]:
        for level in ["R1", "R2", "R3"]:
            p = profiles[level]
            z_all = p["z_linear"] if interp == "linear" else p["z_pchip"]
            eps_all = p["eps_z"]
            for wi, s in enumerate(starts):
                idx0 = int(round(s / 0.125))
                idx = np.arange(idx0, idx0 + 5)
                z = z_all[idx]
                eps = eps_all[idx]
                d = rms(z)
                di = linf(z)
                dmin, dmax = rms_error_envelope(z, eps)
                distance_series[interp][level].append(d)
                window_rows.append({
                    "interpolation": interp,
                    "level": level,
                    "beta": p["spec"]["beta"],
                    "window": wi,
                    "start_u": s,
                    "end_u": s + 0.5,
                    "D_RMS": d,
                    "D_RMS_env_min": dmin,
                    "D_RMS_env_max": dmax,
                    "D_Linf": di,
                })
    write_csv(
        project_root / cfg["outputs"]["windows_csv"],
        list(window_rows[0].keys()),
        [{k: format_float(v) for k, v in r.items()} for r in window_rows]
    )

    # Refinement metrics
    refinement_rows = []
    c_series = {"linear": [], "pchip": []}
    r_order_sigs = {"linear": [], "pchip": []}
    for interp in ["linear", "pchip"]:
        key = "z_linear" if interp == "linear" else "z_pchip"
        for wi, s in enumerate(starts):
            idx0 = int(round(s / 0.125))
            idx = np.arange(idx0, idx0 + 5)
            z1 = profiles["R1"][key][idx]
            z2 = profiles["R2"][key][idx]
            z3 = profiles["R3"][key][idx]
            r12 = rms(z1-z2)
            r23 = rms(z2-z3)
            r13 = rms(z1-z3)
            c = r23/r12 if r12 > 0 else float("nan")
            c_series[interp].append(c)
            r_order_sigs[interp].append(ordering_signature([r12, r23, r13]))
            refinement_rows.append({
                "interpolation": interp,
                "window": wi,
                "start_u": s,
                "end_u": s + 0.5,
                "R12": r12,
                "R23": r23,
                "R13": r13,
                "C_R23_over_R12": c,
                "C_class": {-1: "<1", 0: "=1", 1: ">1"}.get(c_class(c), "NA"),
            })
    write_csv(
        project_root / cfg["outputs"]["refinement_csv"],
        list(refinement_rows[0].keys()),
        [{k: format_float(v) for k, v in r.items()} for r in refinement_rows]
    )

    # Frozen qualitative interpolation-sensitivity logic
    sensitivity_reasons = []

    # 1) profile sign changes
    for level in ["R1", "R2", "R3"]:
        zl = profiles[level]["z_linear"]
        zp = profiles[level]["z_pchip"]
        for j in range(len(zl)):
            if sign_class(zl[j]) != sign_class(zp[j]):
                sensitivity_reasons.append(
                    f"{level}: linear/PCHIP sign classification differs at u={ugrid[j]:.3f}"
                )

    # 2) D(s) direction-pattern changes
    for level in ["R1", "R2", "R3"]:
        sig_l = sequence_direction_signature(distance_series["linear"][level])
        sig_p = sequence_direction_signature(distance_series["pchip"][level])
        if sig_l != sig_p:
            sensitivity_reasons.append(
                f"{level}: linear/PCHIP D_RMS path direction signature differs "
                f"({sig_l} vs {sig_p})"
            )

    # 3) C(s) <1/=1/>1 classification changes
    for wi, s in enumerate(starts):
        cl = c_class(c_series["linear"][wi])
        cp = c_class(c_series["pchip"][wi])
        if cl != cp:
            sensitivity_reasons.append(
                f"window {wi} start_u={s:.3f}: linear/PCHIP contraction classification differs"
            )

    # 4) ordering of R12/R23/R13 changes
    for wi, s in enumerate(starts):
        if r_order_sigs["linear"][wi] != r_order_sigs["pchip"][wi]:
            sensitivity_reasons.append(
                f"window {wi} start_u={s:.3f}: linear/PCHIP refinement-distance ordering differs"
            )

    outcome = "CALIBRATION-SENSITIVE" if sensitivity_reasons else "CALIBRATION-VALID"

    # Figures
    profile_png = project_root / cfg["outputs"]["profile_png"]
    profile_png.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(8.0, 5.2))
    ax = fig.add_subplot(111)
    for level in ["R1", "R2", "R3"]:
        p = profiles[level]
        label = f"{level}  β={p['spec']['beta']:.3f}"
        ax.errorbar(ugrid, p["z_linear"], yerr=p["eps_z"], marker="o", capsize=2, label=label)
    ax.set_xlabel(r"$u=x_t/d$")
    ax.set_ylabel(r"$z=d^2 E_x^{NP}$")
    ax.set_title("VREF-I/A common-grid profiles")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(profile_png, dpi=180)
    plt.close(fig)

    distance_png = project_root / cfg["outputs"]["distance_png"]
    distance_png.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(8.0, 5.2))
    ax = fig.add_subplot(111)
    for level in ["R1", "R2", "R3"]:
        vals = np.array(distance_series["linear"][level], dtype=float)
        lows = []
        highs = []
        p = profiles[level]
        for s in starts:
            idx0 = int(round(s / 0.125))
            idx = np.arange(idx0, idx0 + 5)
            lo, hi = rms_error_envelope(p["z_linear"][idx], p["eps_z"][idx])
            lows.append(lo); highs.append(hi)
        yerr = np.vstack([vals - np.array(lows), np.array(highs) - vals])
        ax.errorbar(starts, vals, yerr=yerr, marker="o", capsize=2,
                    label=f"{level}  β={p['spec']['beta']:.3f}")
    ax.set_xlabel("window start s")
    ax.set_ylabel(r"$D_{\rm VREF}$")
    ax.set_title("VREF-I/A fixed-window vacuum-referenced distance")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(distance_png, dpi=180)
    plt.close(fig)

    # Build report
    report_path = project_root / cfg["outputs"]["report_md"]
    report_path.parent.mkdir(parents=True, exist_ok=True)

    source_table_md = "\n".join(
        f"| {r['level']} | {r['beta']:.3f} | {r['rows_total']} | "
        f"{r['rows_nonnegative']} | [{r['support_min_fm']:.6f}, {r['support_max_fm']:.6f}] |"
        for r in source_records
    )

    primary_ref_rows = [r for r in refinement_rows if r["interpolation"] == "linear"]
    refine_table_md = "\n".join(
        f"| {r['window']} | {r['start_u']:.3f} | {r['R12']:.8g} | "
        f"{r['R23']:.8g} | {r['R13']:.8g} | {r['C_R23_over_R12']:.8g} | {r['C_class']} |"
        for r in primary_ref_rows
    )

    sensitivity_md = "\n".join(f"- {x}" for x in sensitivity_reasons) if sensitivity_reasons else "- None."

    report = f"""# VREF-I/A Calibration Report

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Branch:** VREF-I/A — refinement validation  
**Source:** `BAKER_2022_SU3`  
**Outcome:** **{outcome}**

> This is a representation-calibration result only. It is prohibited from being interpreted as `CONTINUITY-SUPPORTED` or `ISOLATION-SUPPORTED`.

## Source integrity

| Level | beta | rows | x_t>=0 rows | native support [fm] |
|---|---:|---:|---:|---|
{source_table_md}

All three admitted files passed the frozen SHA-256, finite-value, three-column, non-negative-error, mirror-symmetry, ordering, and common-support checks.

## Frozen executable geometry

- Reference length: d = {cfg['constants']['d_fm']} fm
- Dimensionless coordinate: u = x_t/d
- Common grid: u = {cfg['grid']['u']}
- Window width: W = {cfg['windows']['width_u']}
- Window size: m = {cfg['windows']['m']}
- Primary interpolation: piecewise linear
- Sensitivity interpolation: PCHIP (Fritsch-Butland)
- Extrapolation: prohibited

## Primary cross-refinement metrics

| window | start u | R12 | R23 | R13 | C=R23/R12 | C class |
|---:|---:|---:|---:|---:|---:|:---:|
{refine_table_md}

## Linear/PCHIP qualitative-sensitivity audit

{sensitivity_md}

## Leave-one-out diagnostic

The full deterministic leave-one-out table is written to:

`{cfg['outputs']['loo_csv']}`

This diagnostic is descriptive only and does not alter the frozen interpolation rule or the calibration outcome by itself.

## Outcome rule

`CALIBRATION-SENSITIVE` is assigned only if the frozen PCHIP sensitivity changes at least one qualitative representation property: profile sign classification, the direction signature of the D_RMS path, the C(s) classification relative to 1, or the ordering of R12/R23/R13 for any window.

Otherwise, after all mandatory integrity checks pass, the outcome is `CALIBRATION-VALID`.

## Scope restriction

VREF-I/A does not test whether D_struct approaches zero in an asymptotic vacuum-compatible region. The common three-resolution support ends at x_t≈0.511 fm. A separate preregistered VREF-I/B source is required for Structural Vacuum Accessibility.
"""
    report_path.write_text(report, encoding="utf-8")

    # Run record
    run_path = project_root / cfg["outputs"]["run_json"]
    run_path.parent.mkdir(parents=True, exist_ok=True)
    script_hash = sha256_file(Path(__file__).resolve())
    config_hash = sha256_file(script_dir / "VREF_A_CONFIG.json")
    prereg = project_root / "stage2" / "PREREG_VREF_I.md"
    admission = project_root / "stage2" / "SOURCE_ADMISSION.md"

    run_record = {
        "schema": "UNNS_VREF_I_A_RUN_v1",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "outcome": outcome,
        "scope": "calibration-only",
        "prohibited_interpretations": cfg["prohibited_outcomes"],
        "software": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "matplotlib": getattr(sys.modules.get("matplotlib"), "__version__", None),
        },
        "hashes": {
            "vref_a_py": script_hash,
            "config_json": config_hash,
            "prereg_md": sha256_file(prereg) if prereg.exists() else None,
            "source_admission_md": sha256_file(admission) if admission.exists() else None,
        },
        "sources": source_records,
        "frozen_constants": cfg["constants"],
        "grid": cfg["grid"],
        "windows": cfg["windows"],
        "interpolation": cfg["interpolation"],
        "sensitivity_reasons": sensitivity_reasons,
        "outputs": cfg["outputs"],
    }
    run_path.write_text(json.dumps(run_record, indent=2) + "\n", encoding="utf-8")

    print(f"VREF-I/A complete: {outcome}")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VREFError as exc:
        print(f"VREF-I/A ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)

#!/usr/bin/env python3
import argparse
import io
import json
import math
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

PHI = (1.0 + math.sqrt(5.0)) / 2.0
F1_KHZ = 88.0
F2_KHZ = 54.387
CV_FOLDS = 5
RIDGE_ALPHA = 1e-9
SEED = 20260826

ZHU_RECORDS = {
    "ZHU_FIG1_C1": "数据/fig1/fig1(c1).xlsx",
    "ZHU_FIG1_C3": "数据/fig1/fig1(c3).xlsx",
}
ZHU_SPECTRA = {
    "ZHU_FIG1_C1": "数据/fig1/fig1(c2).xlsx",
    "ZHU_FIG1_C3": "数据/fig1/fig1(c4).xlsx",
}
LUO_IDS = [
    "LUO_EE_LOW_N12", "LUO_EE_LOW_N32",
    "LUO_EE_DTQC_N12", "LUO_EE_DTQC_N32",
    "LUO_EE_HIGH_N12", "LUO_EE_HIGH_N32",
]

def make_features(x, freqs):
    cols = [np.ones_like(x, dtype=float)]
    for f in freqs:
        ph = 2.0 * np.pi * f * x
        cols.append(np.cos(ph))
        cols.append(np.sin(ph))
    return np.column_stack(cols)

def ridge_fit(X, y, alpha=RIDGE_ALPHA):
    A = X.T @ X
    reg = np.eye(A.shape[0]) * alpha
    reg[0, 0] = 0.0
    return np.linalg.solve(A + reg, X.T @ y)

def blocked_cv_r2(x, y, freqs, k=CV_FOLDS, alpha=RIDGE_ALPHA):
    n = len(x)
    bounds = np.linspace(0, n, k + 1, dtype=int)
    values = []
    for i in range(k):
        test = np.zeros(n, dtype=bool)
        test[bounds[i]:bounds[i + 1]] = True
        train = ~test
        beta = ridge_fit(make_features(x[train], freqs), y[train], alpha)
        pred = make_features(x[test], freqs) @ beta
        ss = float(np.sum((y[test] - np.mean(y[test])) ** 2))
        values.append(float(
            1.0 - np.sum((y[test] - pred) ** 2) / (ss + 1e-30)
        ))
    return float(np.mean(values))

def basis(depth):
    axis = [1.0 / depth, PHI / depth]
    mixed = [abs(PHI - 1.0) / depth, (PHI + 1.0) / depth]
    return axis, mixed

def nested_fractional_scan(x, y):
    base = basis(1)[0] + basis(1)[1]
    base_r2 = blocked_cv_r2(x, y, base)
    rows = []
    for d in (2, 3, 4):
        frac = basis(d)[0] + basis(d)[1]
        frac_r2 = blocked_cv_r2(x, y, frac)
        nested_r2 = blocked_cv_r2(x, y, base + frac)
        rows.append({
            "depth": d,
            "integer_parent_r2_cv": base_r2,
            "fractional_only_r2_cv": frac_r2,
            "integer_plus_fractional_r2_cv": nested_r2,
            "fractional_cover_gain": nested_r2 - base_r2,
        })
    return rows

def perturb_cases(x, y):
    yield "BASE", x, y
    yield "DOWNSAMPLE_5", x[::5], y[::5]
    yield "DOWNSAMPLE_10", x[::10], y[::10]
    n = max(100, int(round(0.75 * len(x))))
    yield "PREFIX_0.75", x[:n], y[:n]
    rng = np.random.default_rng(SEED)
    yield "NOISE_0.020SD", x, y + rng.normal(
        0.0, 0.02 * (np.std(y) + 1e-30), size=len(y)
    )

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="UNNS_MULTI_CLOCK_RECURRENCE root")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    zhu_raw = root / "02_RAW" / "ZHU_2026" / "data.zip"
    luo_dir = root / "03_INGEST" / "LUO"
    out = root / "06_VALIDATION" / "ZHU_2026" / "INVESTIGATION_v001"
    out.mkdir(parents=True, exist_ok=True)

    if not zhu_raw.exists():
        raise FileNotFoundError(zhu_raw)
    for rid in LUO_IDS:
        p = luo_dir / f"{rid}.csv"
        if not p.exists():
            raise FileNotFoundError(p)

    depth_rows = []
    mode_rows = []
    spectrum_rows = []
    robust_rows = []

    with zipfile.ZipFile(zhu_raw, "r") as zhu:
        for rid, member in ZHU_RECORDS.items():
            df = pd.read_excel(
                io.BytesIO(zhu.read(member)),
                header=None,
                names=["time_ms", "response"],
            )
            x = F2_KHZ * df["time_ms"].to_numpy(float)
            y = df["response"].to_numpy(float)

            for row in nested_fractional_scan(x, y):
                depth_rows.append({"id": rid, "platform": "ZHU_2026", **row})

            for d in (1, 2):
                axis, mixed = basis(d)
                labels = [
                    ("axis_f2", axis[0]),
                    ("axis_f1", axis[1]),
                    ("mixed_difference", mixed[0]),
                    ("mixed_sum", mixed[1]),
                ]
                for label, f in labels:
                    mode_rows.append({
                        "id": rid,
                        "depth": d,
                        "mode": label,
                        "frequency_cycles_per_f2_cycle": f,
                        "physical_frequency_khz": f * F2_KHZ,
                        "single_mode_r2_cv": blocked_cv_r2(x, y, [f]),
                    })
                for label, freqs in (
                    ("axis_pair", axis),
                    ("mixed_pair", mixed),
                    ("full_basis", axis + mixed),
                ):
                    mode_rows.append({
                        "id": rid,
                        "depth": d,
                        "mode": label,
                        "frequency_cycles_per_f2_cycle": None,
                        "physical_frequency_khz": None,
                        "single_mode_r2_cv": blocked_cv_r2(x, y, freqs),
                    })

            b1 = basis(1)[0] + basis(1)[1]
            b2 = basis(2)[0] + basis(2)[1]
            for case, xp, yp in perturb_cases(x, y):
                parent = blocked_cv_r2(xp, yp, b1)
                nested = blocked_cv_r2(xp, yp, b1 + b2)
                robust_rows.append({
                    "id": rid,
                    "case": case,
                    "n": len(yp),
                    "integer_parent_r2_cv": parent,
                    "integer_plus_d2_r2_cv": nested,
                    "fractional_cover_gain_d2": nested - parent,
                })

        expected = {
            "integer_difference": abs(F1_KHZ - F2_KHZ),
            "half_difference": abs(F1_KHZ - F2_KHZ) / 2.0,
            "f1": F1_KHZ,
            "f2": F2_KHZ,
            "half_sum": (F1_KHZ + F2_KHZ) / 2.0,
        }
        for rid, member in ZHU_SPECTRA.items():
            sdf = pd.read_excel(
                io.BytesIO(zhu.read(member)),
                header=None,
                names=["frequency_khz", "amplitude"],
            )
            for label, target in expected.items():
                win = sdf[
                    (sdf["frequency_khz"] >= target - 0.5)
                    & (sdf["frequency_khz"] <= target + 0.5)
                ]
                if len(win):
                    idx = win["amplitude"].idxmax()
                    spectrum_rows.append({
                        "id": rid,
                        "source_spectrum_member": member,
                        "component": label,
                        "target_frequency_khz": target,
                        "observed_peak_frequency_khz": float(
                            sdf.loc[idx, "frequency_khz"]
                        ),
                        "peak_amplitude": float(sdf.loc[idx, "amplitude"]),
                    })

    for rid in LUO_IDS:
        df = pd.read_csv(luo_dir / f"{rid}.csv")
        x = df["time"].to_numpy(float)
        y = df["S"].to_numpy(float)
        for row in nested_fractional_scan(x, y):
            depth_rows.append({"id": rid, "platform": "LUO_2026", **row})

    depth_df = pd.DataFrame(depth_rows)
    mode_df = pd.DataFrame(mode_rows)
    spectrum_df = pd.DataFrame(spectrum_rows)
    robust_df = pd.DataFrame(robust_rows)

    depth_df.to_csv(out / "FRACTIONAL_COVER_SCAN.csv", index=False)
    mode_df.to_csv(out / "ZHU_MODE_DECOMPOSITION.csv", index=False)
    spectrum_df.to_csv(out / "ZHU_SOURCE_SPECTRUM_AUDIT.csv", index=False)
    robust_df.to_csv(out / "ZHU_FRACTIONAL_COVER_ROBUSTNESS.csv", index=False)

    write_json(out / "FRACTIONAL_COVER_SCAN.json", depth_rows)
    write_json(out / "ZHU_MODE_DECOMPOSITION.json", mode_rows)
    write_json(out / "ZHU_SOURCE_SPECTRUM_AUDIT.json", spectrum_rows)
    write_json(out / "ZHU_FRACTIONAL_COVER_ROBUSTNESS.json", robust_rows)

    audit = {
        "status": "POST_VALIDATION_DIAGNOSTIC",
        "method_changed": False,
        "locked_zhu_validation_changed": False,
        "c003_loaded": False,
        "new_thresholds_defined": 0,
        "new_verdicts_defined": 0,
        "zhu_d2_gain_positive_all_robustness_cases": bool(
            (robust_df["fractional_cover_gain_d2"] > 0).all()
        ),
    }
    write_json(out / "INVESTIGATION_AUDIT.json", audit)

    print(json.dumps(audit, indent=2))
    print()
    print(depth_df[depth_df["depth"] == 2].to_string(index=False))

if __name__ == "__main__":
    main()

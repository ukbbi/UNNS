#!/usr/bin/env python3
import argparse
import io
import json
import math
import hashlib
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def make_features(x, freqs):
    cols = [np.ones_like(x, dtype=float)]
    for f in freqs:
        phase = 2.0 * np.pi * f * x
        cols.append(np.cos(phase))
        cols.append(np.sin(phase))
    return np.column_stack(cols)


def ridge_fit(X, y, alpha):
    A = X.T @ X
    reg = np.eye(A.shape[0]) * alpha
    reg[0, 0] = 0.0
    return np.linalg.solve(A + reg, X.T @ y)


def blocked_cv_r2(x, y, freqs, k, alpha):
    n = len(x)
    bounds = np.linspace(0, n, k + 1, dtype=int)
    vals = []
    for i in range(k):
        test = np.zeros(n, dtype=bool)
        test[bounds[i]:bounds[i + 1]] = True
        train = ~test
        beta = ridge_fit(make_features(x[train], freqs), y[train], alpha)
        pred = make_features(x[test], freqs) @ beta
        ss = float(np.sum((y[test] - np.mean(y[test])) ** 2))
        vals.append(float(
            1.0 - np.sum((y[test] - pred) ** 2) / (ss + 1e-30)
        ))
    return float(np.mean(vals)), float(np.std(vals, ddof=0)), vals


def basis(depth, ratio):
    axis = [1.0 / depth, ratio / depth]
    mixed = [abs(ratio - 1.0) / depth, (ratio + 1.0) / depth]
    return axis, mixed


def eval_parent_and_depth(x, y, depth, cfg, ratio=None):
    ratio = float(cfg["source_ratio"] if ratio is None else ratio)
    parent_axis, parent_mixed = basis(cfg["parent_depth"], ratio)
    frac_axis, frac_mixed = basis(depth, ratio)

    pa, pa_sd, pa_folds = blocked_cv_r2(
        x, y, parent_axis, cfg["cv_folds"], cfg["ridge_alpha"]
    )
    pf, pf_sd, pf_folds = blocked_cv_r2(
        x, y, parent_axis + parent_mixed, cfg["cv_folds"], cfg["ridge_alpha"]
    )
    na, na_sd, na_folds = blocked_cv_r2(
        x, y, parent_axis + parent_mixed + frac_axis,
        cfg["cv_folds"], cfg["ridge_alpha"]
    )
    nf, nf_sd, nf_folds = blocked_cv_r2(
        x, y, parent_axis + parent_mixed + frac_axis + frac_mixed,
        cfg["cv_folds"], cfg["ridge_alpha"]
    )

    return {
        "depth": int(depth),
        "parent_axis_r2_cv": pa,
        "parent_full_r2_cv": pf,
        "parent_mixed_gain": pf - pa,
        "nested_axis_r2_cv": na,
        "nested_full_r2_cv": nf,
        "frac_axis_gain": na - pf,
        "frac_mixed_gain": nf - na,
        "frac_total_gain": nf - pf,
        "parent_axis_r2_cv_sd": pa_sd,
        "parent_full_r2_cv_sd": pf_sd,
        "nested_axis_r2_cv_sd": na_sd,
        "nested_full_r2_cv_sd": nf_sd,
        "parent_axis_fold_r2": [float(v) for v in pa_folds],
        "parent_full_fold_r2": [float(v) for v in pf_folds],
        "nested_axis_fold_r2": [float(v) for v in na_folds],
        "nested_full_fold_r2": [float(v) for v in nf_folds],
    }


def perturb_cases(x, y, cfg):
    yield "BASE", x, y
    for f in cfg["robustness"]["downsample_factors"]:
        yield f"DOWNSAMPLE_{f}", x[::int(f)], y[::int(f)]
    for frac in cfg["robustness"]["prefix_fractions"]:
        n = max(100, int(round(len(x) * float(frac))))
        yield f"PREFIX_{frac:.2f}", x[:n], y[:n]
    for sig in cfg["robustness"]["noise_sigma_fractions"]:
        rng = np.random.default_rng(cfg["seed"])
        yn = y + rng.normal(0, float(sig) * (np.std(y) + 1e-30), size=len(y))
        yield f"NOISE_{sig:.3f}SD", x, yn


def load_cfg(root):
    return json.loads((root / "05_METHODS/FC_CONFIG_v003.json").read_text())


def run_development(root, cfg):
    corpus = pd.read_csv(root / "04_CORPUS/CORPUS_v001.csv").set_index("id", drop=False)
    out = root / "08_OUTPUTS/FC_v003"
    det = out / "RECORD_DETAILS"
    det.mkdir(parents=True, exist_ok=True)

    results, scans, robustness = [], [], []

    for rid in cfg["development_scope_ids"]:
        row = corpus.loc[rid]
        df = pd.read_csv(root / row["file"])
        x = df["time"].to_numpy(float)
        y = df["S"].to_numpy(float)
        ok = np.isfinite(x) & np.isfinite(y)
        x, y = x[ok], y[ok]

        evs = [
            eval_parent_and_depth(x, y, d, cfg)
            for d in cfg["fractional_depths"]
        ]
        best = max(evs, key=lambda z: z["frac_total_gain"])
        second = sorted(evs, key=lambda z: z["frac_total_gain"], reverse=True)[1]

        for ev in evs:
            scans.append({
                "id": rid,
                "role": row["role"],
                "regime": row["regime"],
                **{k: v for k, v in ev.items() if not isinstance(v, list)},
            })

        summary = {
            "id": rid,
            "role": row["role"],
            "regime": row["regime"],
            "n": int(len(y)),
            "source_ratio": float(cfg["source_ratio"]),
            "parent_full_r2_cv": float(best["parent_full_r2_cv"]),
            "parent_mixed_gain": float(best["parent_mixed_gain"]),
            "best_fractional_depth": int(best["depth"]),
            "frac_axis_gain": float(best["frac_axis_gain"]),
            "frac_mixed_gain": float(best["frac_mixed_gain"]),
            "frac_total_gain": float(best["frac_total_gain"]),
            "fractional_depth_margin": float(
                best["frac_total_gain"] - second["frac_total_gain"]
            ),
            "coupling_mean_S": float(np.mean(y)),
            "coupling_median_S": float(np.median(y)),
            "coupling_std_S": float(np.std(y)),
            "coupling_final_S": float(y[-1]),
        }
        results.append(summary)

        dstar = best["depth"]
        for label, xp, yp in perturb_cases(x, y, cfg):
            ev = eval_parent_and_depth(xp, yp, dstar, cfg)
            robustness.append({
                "id": rid,
                "role": row["role"],
                "case": label,
                "fixed_fractional_depth": int(dstar),
                "n": int(len(yp)),
                "parent_full_r2_cv": ev["parent_full_r2_cv"],
                "frac_axis_gain": ev["frac_axis_gain"],
                "frac_mixed_gain": ev["frac_mixed_gain"],
                "frac_total_gain": ev["frac_total_gain"],
                "mean_S": float(np.mean(yp)),
            })

        (det / f"{rid}.json").write_text(
            json.dumps({"summary": summary, "fractional_scan": evs}, indent=2)
        )

    rdf = pd.DataFrame(results)
    sdf = pd.DataFrame(scans)
    bdf = pd.DataFrame(robustness)
    rdf.to_csv(out / "FC_RESULTS.csv", index=False)
    sdf.to_csv(out / "FC_SCAN.csv", index=False)
    bdf.to_csv(out / "ROBUSTNESS.csv", index=False)
    (out / "FC_RESULTS.json").write_text(json.dumps(results, indent=2))
    (out / "FC_SCAN.json").write_text(json.dumps(scans, indent=2))
    (out / "ROBUSTNESS.json").write_text(json.dumps(robustness, indent=2))

    audit = {
        "version": cfg["version"],
        "status": "PASS_DIAGNOSTIC_DEVELOPMENT",
        "records": len(results),
        "classification_thresholds": 0,
        "verdicts_emitted": 0,
        "c003_loaded": False,
        "zhu_used_for_development_run": False,
        "huang_loaded": False,
        "moon_loaded": False,
        "results_sha256": sha256(out / "FC_RESULTS.csv"),
        "scan_sha256": sha256(out / "FC_SCAN.csv"),
        "robustness_sha256": sha256(out / "ROBUSTNESS.csv"),
    }
    (out / "AUDIT.json").write_text(json.dumps(audit, indent=2))
    return audit


def run_zhu_retro(root, cfg):
    raw = root / "02_RAW/ZHU_2026/data.zip"
    out = root / "06_VALIDATION/ZHU_2026/RETRO_v003"
    out.mkdir(parents=True, exist_ok=True)
    results, scans, robustness = [], [], []

    f2 = float(cfg["zhu_adapter"]["f2_khz"])
    ratio = float(cfg["source_ratio"])

    with zipfile.ZipFile(raw, "r") as z:
        for rid, member in cfg["zhu_retrospective_records"].items():
            df = pd.read_excel(io.BytesIO(z.read(member)), header=None)
            t = pd.to_numeric(df.iloc[:, 0], errors="coerce").to_numpy(float)
            y = pd.to_numeric(df.iloc[:, 1], errors="coerce").to_numpy(float)
            ok = np.isfinite(t) & np.isfinite(y)
            x, y = f2 * t[ok], y[ok]

            evs = [
                eval_parent_and_depth(x, y, d, cfg, ratio=ratio)
                for d in cfg["fractional_depths"]
            ]
            best = max(evs, key=lambda z: z["frac_total_gain"])
            second = sorted(evs, key=lambda z: z["frac_total_gain"], reverse=True)[1]
            for ev in evs:
                scans.append({
                    "id": rid,
                    **{k: v for k, v in ev.items() if not isinstance(v, list)},
                })

            summary = {
                "id": rid,
                "status": "RETROSPECTIVE_ONLY_NOT_VALIDATION",
                "n": int(len(y)),
                "parent_full_r2_cv": float(best["parent_full_r2_cv"]),
                "parent_mixed_gain": float(best["parent_mixed_gain"]),
                "best_fractional_depth": int(best["depth"]),
                "frac_axis_gain": float(best["frac_axis_gain"]),
                "frac_mixed_gain": float(best["frac_mixed_gain"]),
                "frac_total_gain": float(best["frac_total_gain"]),
                "fractional_depth_margin": float(
                    best["frac_total_gain"] - second["frac_total_gain"]
                ),
                "coupling_sector": None,
            }
            results.append(summary)

            dstar = best["depth"]
            for label, xp, yp in perturb_cases(x, y, cfg):
                ev = eval_parent_and_depth(xp, yp, dstar, cfg, ratio=ratio)
                robustness.append({
                    "id": rid,
                    "case": label,
                    "fixed_fractional_depth": int(dstar),
                    "n": int(len(yp)),
                    "parent_full_r2_cv": ev["parent_full_r2_cv"],
                    "frac_axis_gain": ev["frac_axis_gain"],
                    "frac_mixed_gain": ev["frac_mixed_gain"],
                    "frac_total_gain": ev["frac_total_gain"],
                })

    pd.DataFrame(results).to_csv(out / "ZHU_RETRO_RESULTS.csv", index=False)
    pd.DataFrame(scans).to_csv(out / "ZHU_RETRO_SCAN.csv", index=False)
    pd.DataFrame(robustness).to_csv(out / "ZHU_RETRO_ROBUSTNESS.csv", index=False)
    (out / "ZHU_RETRO_RESULTS.json").write_text(json.dumps(results, indent=2))
    audit = {
        "version": cfg["version"],
        "status": "RETROSPECTIVE_ONLY_NOT_VALIDATION",
        "records": len(results),
        "classification_thresholds": 0,
        "verdicts_emitted": 0,
        "c003_loaded": False,
        "reason_not_validation": (
            "The v003 architecture was motivated by the locked Zhu v002 depth-selection failure."
        ),
        "results_sha256": sha256(out / "ZHU_RETRO_RESULTS.csv"),
    }
    (out / "ZHU_RETRO_AUDIT.json").write_text(json.dumps(audit, indent=2))
    return audit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument(
        "--mode",
        choices=["development", "zhu-retro", "all"],
        default="development",
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()
    cfg = load_cfg(root)
    reports = {}
    if args.mode in ("development", "all"):
        reports["development"] = run_development(root, cfg)
    if args.mode in ("zhu-retro", "all"):
        reports["zhu_retro"] = run_zhu_retro(root, cfg)
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path
import io
import json
import math
import zipfile

import numpy as np
import pandas as pd


def _rank_average(x: np.ndarray) -> np.ndarray:
    """Average ranks, 1-based, without scipy."""
    s = pd.Series(x)
    return s.rank(method="average").to_numpy(float)


def spearman_rho(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    x = x[m]
    y = y[m]
    if len(x) < 3:
        return None
    rx = _rank_average(x)
    ry = _rank_average(y)
    sx = np.std(rx)
    sy = np.std(ry)
    if sx == 0 or sy == 0:
        return 0.0
    return float(np.corrcoef(rx, ry)[0, 1])


def _safe_ratio(a, b):
    if b is None or not np.isfinite(b) or b == 0:
        return None
    return float(a / b)


def _summary(v):
    a = np.asarray(v, dtype=float)
    a = a[np.isfinite(a)]
    if not len(a):
        return {"n": 0, "mean": None, "median": None, "p90": None, "max": None}
    return {
        "n": int(len(a)),
        "mean": float(np.mean(a)),
        "median": float(np.median(a)),
        "p90": float(np.quantile(a, .90)),
        "max": float(np.max(a)),
    }


def stitch_physics_analysis(
    nodes: pd.DataFrame,
    *,
    viscosity: float | None = None,
    seed: int = 20260905,
    permutations: int = 2000,
):
    """
    Test whether large scale-time stitching defects coincide with high
    enstrophy / strain-dissipation intensity.

    The analysis is descriptive + deterministic permutation enrichment.
    It does not change the STRUC-ROUTE-I verdict.
    """
    if "stitch_defect" not in nodes.columns:
        raise ValueError("NODES table has no stitch_defect column.")
    required = ["enstrophy_mean", "q_mean"]
    missing = [c for c in required if c not in nodes.columns]
    if missing:
        raise ValueError(f"NODES table missing physical columns: {missing}")

    d = nodes.copy()
    d["stitch_defect"] = pd.to_numeric(d["stitch_defect"], errors="coerce")
    d["enstrophy_mean"] = pd.to_numeric(d["enstrophy_mean"], errors="coerce")
    d["q_mean"] = pd.to_numeric(d["q_mean"], errors="coerce")
    d = d.loc[np.isfinite(d["stitch_defect"])].copy()

    # From Q = 1/2(enstrophy - strain_sq), hence strain_sq=enstrophy-2Q.
    d["strain_sq_mean_proxy"] = np.maximum(
        d["enstrophy_mean"].to_numpy(float) - 2.0 * d["q_mean"].to_numpy(float),
        0.0,
    )
    if viscosity is not None:
        d["dissipation_mean_proxy"] = (
            2.0 * float(viscosity) * d["strain_sq_mean_proxy"]
        )
        diss_col = "dissipation_mean_proxy"
    else:
        diss_col = "strain_sq_mean_proxy"

    n = len(d)
    if n < 20:
        raise ValueError(f"Only {n} stitching-eligible nodes; insufficient tail sample.")

    q90 = float(d["stitch_defect"].quantile(.90))
    q95 = float(d["stitch_defect"].quantile(.95))
    q99 = float(d["stitch_defect"].quantile(.99))

    masks = {
        "top10pct": d["stitch_defect"] >= q90,
        "top5pct": d["stitch_defect"] >= q95,
        "top1pct": d["stitch_defect"] >= q99,
        "D_ge_0p1": d["stitch_defect"] >= 0.1,
        "D_ge_0p5": d["stitch_defect"] >= 0.5,
    }

    correlations = {
        "spearman_D_vs_enstrophy_mean": spearman_rho(
            d["stitch_defect"], d["enstrophy_mean"]
        ),
        "spearman_D_vs_dissipation_proxy": spearman_rho(
            d["stitch_defect"], d[diss_col]
        ),
    }

    # Top-decile coincidence test. Expected overlap under random association = 10%.
    rng = np.random.default_rng(seed)
    topD = masks["top10pct"].to_numpy(bool)
    ens_thresh = float(d["enstrophy_mean"].quantile(.90))
    diss_thresh = float(d[diss_col].quantile(.90))
    topE = (d["enstrophy_mean"].to_numpy(float) >= ens_thresh)
    topX = (d[diss_col].to_numpy(float) >= diss_thresh)

    def overlap_test(target):
        observed = int(np.sum(topD & target))
        denom = int(np.sum(topD))
        frac = observed / denom if denom else None
        perm = np.empty(permutations, dtype=int)
        for i in range(permutations):
            perm[i] = int(np.sum(topD & rng.permutation(target)))
        p = (1 + int(np.sum(perm >= observed))) / (permutations + 1)
        expected = float(np.mean(target)) if len(target) else None
        return {
            "topD_n": denom,
            "observed_overlap_n": observed,
            "observed_overlap_fraction": frac,
            "random_expected_fraction": expected,
            "enrichment": _safe_ratio(frac, expected) if frac is not None else None,
            "permutation_p_enrichment": float(p),
            "permutations": int(permutations),
        }

    overlap = {
        "top10_D_with_top10_enstrophy": overlap_test(topE),
        "top10_D_with_top10_dissipation_proxy": overlap_test(topX),
    }

    tail_rows = []
    for name, mask in masks.items():
        tail = d.loc[mask]
        rest = d.loc[~mask]
        if not len(tail):
            continue
        e_tail = float(tail["enstrophy_mean"].median())
        e_rest = float(rest["enstrophy_mean"].median()) if len(rest) else None
        x_tail = float(tail[diss_col].median())
        x_rest = float(rest[diss_col].median()) if len(rest) else None
        tail_rows.append({
            "tail_definition": name,
            "tail_n": int(len(tail)),
            "tail_fraction": float(len(tail) / len(d)),
            "D_min": float(tail["stitch_defect"].min()),
            "D_median": float(tail["stitch_defect"].median()),
            "D_max": float(tail["stitch_defect"].max()),
            "enstrophy_median_tail": e_tail,
            "enstrophy_median_rest": e_rest,
            "enstrophy_median_ratio": _safe_ratio(e_tail, e_rest),
            "dissipation_proxy_median_tail": x_tail,
            "dissipation_proxy_median_rest": x_rest,
            "dissipation_proxy_median_ratio": _safe_ratio(x_tail, x_rest),
        })

    # Keep the top 10% node records as a directly inspectable event table.
    event_cols = [
        c for c in [
            "node_id", "time_idx", "time_value", "scale_idx", "scale_value",
            "object_id", "stitch_defect", "enstrophy_mean", "enstrophy_integral",
            "q_mean", "q_max", "strain_sq_mean_proxy", "dissipation_mean_proxy",
            "cx", "cy", "cz", "physical_volume", "equiv_radius"
        ] if c in d.columns
    ]
    events = d.loc[masks["top10pct"], event_cols].copy()
    events = events.sort_values("stitch_defect", ascending=False).reset_index(drop=True)

    by_time = (
        d.assign(high_D=masks["top10pct"].to_numpy(bool))
        .groupby("time_idx", dropna=False)
        .agg(
            eligible=("stitch_defect", "size"),
            high_D=("high_D", "sum"),
            mean_D=("stitch_defect", "mean"),
            mean_enstrophy=("enstrophy_mean", "mean"),
            mean_dissipation_proxy=(diss_col, "mean"),
        )
        .reset_index()
    )
    by_time["high_D_fraction"] = by_time["high_D"] / by_time["eligible"]

    by_scale = (
        d.assign(high_D=masks["top10pct"].to_numpy(bool))
        .groupby("scale_idx", dropna=False)
        .agg(
            eligible=("stitch_defect", "size"),
            high_D=("high_D", "sum"),
            mean_D=("stitch_defect", "mean"),
            mean_enstrophy=("enstrophy_mean", "mean"),
            mean_dissipation_proxy=(diss_col, "mean"),
        )
        .reset_index()
    )
    by_scale["high_D_fraction"] = by_scale["high_D"] / by_scale["eligible"]

    report = {
        "analysis": "STITCH_DEFECT_PHYSICS_TAIL",
        "eligible_nodes": int(len(d)),
        "viscosity": viscosity,
        "dissipation_quantity": (
            "2*nu*(enstrophy_mean-2*q_mean)"
            if viscosity is not None
            else "strain_sq_mean_proxy=enstrophy_mean-2*q_mean"
        ),
        "stitch_defect": _summary(d["stitch_defect"]),
        "tail_thresholds": {"q90": q90, "q95": q95, "q99": q99},
        "correlations": correlations,
        "top_decile_overlap": overlap,
        "tail_comparisons": tail_rows,
        "interpretation_rule": (
            "Association is supported when high-D tails show repeatable enrichment "
            "in enstrophy/dissipation proxy and/or positive rank correlation. "
            "This post-run analysis is exploratory and does not alter the chamber verdict."
        ),
    }
    return report, events, by_time, by_scale


def analyze_run_zip(
    run_zip: str | Path,
    out_dir: str | Path,
    *,
    viscosity: float | None = None,
    permutations: int = 2000,
):
    run_zip = Path(run_zip)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(run_zip, "r") as zf:
        node_names = [n for n in zf.namelist() if n.endswith("/NODES.parquet") or n == "NODES.parquet"]
        if len(node_names) != 1:
            raise ValueError("Run ZIP must contain exactly one NODES.parquet.")
        raw = zf.read(node_names[0])
        nodes = pd.read_parquet(io.BytesIO(raw))

    report, events, by_time, by_scale = stitch_physics_analysis(
        nodes, viscosity=viscosity, permutations=permutations
    )
    report["source_run_zip"] = str(run_zip.resolve())

    (out_dir / "STITCH_PHYSICS.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    events.to_csv(out_dir / "STITCH_TAIL.csv", index=False)
    by_time.to_csv(out_dir / "STITCH_BY_TIME.csv", index=False)
    by_scale.to_csv(out_dir / "STITCH_BY_SCALE.csv", index=False)

    return report

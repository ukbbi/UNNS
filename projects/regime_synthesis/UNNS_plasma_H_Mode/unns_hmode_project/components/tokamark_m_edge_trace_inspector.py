#!/usr/bin/env python3
"""
tokamark_m_edge_trace_inspector.py

UNNS-H Mode Project
Trace-level inspection for the first TokaMark/MAST m_edge(t) probe.

Reads:
  outputs/reports/tokamark_shot_12063_m_edge_t_probe.csv

Writes:
  outputs/reports/tokamark_shot_12063_m_edge_trace_inspection_windows.csv
  outputs/reports/tokamark_shot_12063_m_edge_trace_inspection_summary.json
  outputs/reports/tokamark_shot_12063_m_edge_trace_inspection.md

Run:
  python components\\tokamark_m_edge_trace_inspector.py --input outputs\\reports\\tokamark_shot_12063_m_edge_t_probe.csv --out-dir outputs\\reports
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


PRIMARY_COLUMNS = [
    "m_edge",
    "C_edge_capacity",
    "F_route_fragmentation",
    "S_edge_response",
    "S_power_balance",
    "S_transport",
    "density_support",
    "geometry_stability",
    "missingness_pressure",
    "nbi_proxy",
    "density_proxy",
    "dalpha_proxy",
    "softx_lower_proxy",
    "softx_upper_proxy",
    "te_profile_gradient_proxy",
    "ne_profile_gradient_proxy",
    "te_edge_median_proxy",
    "te_core_median_proxy",
    "ne_edge_median_proxy",
    "ne_core_median_proxy",
]

REPORT_COLUMNS = [
    "m_edge",
    "C_edge_capacity",
    "F_route_fragmentation",
    "S_edge_response",
    "S_power_balance",
    "S_transport",
    "dalpha_proxy",
    "softx_lower_proxy",
    "softx_upper_proxy",
    "te_profile_gradient_proxy",
    "ne_profile_gradient_proxy",
    "density_proxy",
    "nbi_proxy",
    "missingness_pressure",
]


@dataclass
class Window:
    label: str
    state: str
    start_time: float
    end_time: float
    start_index: int
    end_index: int
    duration: float


def to_float(x: Any) -> Optional[float]:
    try:
        y = float(x)
        return y if np.isfinite(y) else None
    except Exception:
        return None


def finite_stats(values: Iterable[Any]) -> Dict[str, Any]:
    arr = pd.to_numeric(pd.Series(list(values)), errors="coerce").to_numpy(dtype=float)
    finite = arr[np.isfinite(arr)]
    out: Dict[str, Any] = {
        "finite_count": int(finite.size),
        "total_count": int(arr.size),
        "finite_fraction": float(finite.size / max(arr.size, 1)),
    }
    if finite.size == 0:
        out.update({k: None for k in ["min", "p05", "median", "mean", "p95", "max", "std"]})
        return out
    out.update({
        "min": float(np.nanmin(finite)),
        "p05": float(np.nanpercentile(finite, 5)),
        "median": float(np.nanmedian(finite)),
        "mean": float(np.nanmean(finite)),
        "p95": float(np.nanpercentile(finite, 95)),
        "max": float(np.nanmax(finite)),
        "std": float(np.nanstd(finite)),
    })
    return out


def slope_label(first: Optional[float], last: Optional[float], tol: float = 1e-9) -> str:
    if first is None or last is None:
        return "na"
    delta = last - first
    if delta > tol:
        return "increase"
    if delta < -tol:
        return "decrease"
    return "flat"


def first_last_slope(df: pd.DataFrame, col: str) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    if col not in df.columns or "time_s" not in df.columns or df.empty:
        return None, None, None
    sub = df[["time_s", col]].copy()
    sub["time_s"] = pd.to_numeric(sub["time_s"], errors="coerce")
    sub[col] = pd.to_numeric(sub[col], errors="coerce")
    sub = sub[np.isfinite(sub["time_s"]) & np.isfinite(sub[col])]
    if len(sub) == 0:
        return None, None, None
    first = float(sub[col].iloc[0])
    last = float(sub[col].iloc[-1])
    if len(sub) < 2:
        return first, last, None
    dt = float(sub["time_s"].iloc[-1] - sub["time_s"].iloc[0])
    slope = None if abs(dt) < 1e-12 else float((last - first) / dt)
    return first, last, slope


def contiguous_windows(df: pd.DataFrame, state: str, min_duration: float, prefix: str) -> List[Window]:
    windows: List[Window] = []
    t = pd.to_numeric(df["time_s"], errors="coerce").to_numpy(dtype=float)
    mask = df["m_edge_state"].astype(str).eq(state).to_numpy()
    start: Optional[int] = None
    n = 0
    for i, flag in enumerate(mask):
        if flag and start is None:
            start = i
        is_last = i == len(mask) - 1
        if start is not None and ((not flag) or is_last):
            end = i if flag and is_last else i - 1
            t0 = to_float(t[start])
            t1 = to_float(t[end])
            if t0 is not None and t1 is not None:
                duration = t1 - t0
                if duration >= min_duration:
                    n += 1
                    windows.append(Window(f"{prefix}_{n:03d}", state, t0, t1, int(start), int(end), float(duration)))
            start = None
    return windows


def peak_window(df: pd.DataFrame, col: str, mode: str, half_width: float, state: str, label: str) -> Optional[Window]:
    if col not in df.columns:
        return None
    s = pd.to_numeric(df[col], errors="coerce")
    if not s.notna().any():
        return None
    idx = int(s.idxmax() if mode == "max" else s.idxmin())
    t0 = float(df.loc[idx, "time_s"])
    sub = df[(df["time_s"] >= t0 - half_width) & (df["time_s"] <= t0 + half_width)]
    if sub.empty:
        return None
    return Window(
        label=label,
        state=state,
        start_time=float(sub["time_s"].iloc[0]),
        end_time=float(sub["time_s"].iloc[-1]),
        start_index=int(sub.index[0]),
        end_index=int(sub.index[-1]),
        duration=float(sub["time_s"].iloc[-1] - sub["time_s"].iloc[0]),
    )


def slice_time(df: pd.DataFrame, t0: float, t1: float) -> pd.DataFrame:
    return df[(df["time_s"] >= t0) & (df["time_s"] <= t1)].copy()


def med(stats: Dict[str, Dict[str, Any]], col: str) -> Optional[float]:
    return stats.get(col, {}).get("median")


def classify(state: str, during: Dict[str, Dict[str, Any]], d_before: Dict[str, Optional[float]]) -> Tuple[str, List[str]]:
    notes: List[str] = []
    c = med(during, "C_edge_capacity")
    f = med(during, "F_route_fragmentation")
    edge = med(during, "S_edge_response")
    power = med(during, "S_power_balance")
    transport = med(during, "S_transport")
    missing = med(during, "missingness_pressure")

    if missing is not None and missing >= 0.55:
        notes.append("high_missingness_pressure")

    if state == "positive_boundary_margin":
        if c is not None and f is not None and c > f:
            notes.append("capacity_exceeds_fragmentation")
        if edge is not None and edge >= 0.55:
            notes.append("edge_response_high")
        if power is not None and power <= 0.35:
            notes.append("low_power_balance_pressure")
        if transport is not None and transport >= 0.55:
            notes.append("transport_pressure_present")
        if d_before.get("m_edge") is not None and d_before["m_edge"] > 0:
            notes.append("m_edge_higher_than_before")

        if "capacity_exceeds_fragmentation" in notes and "high_missingness_pressure" not in notes:
            if "edge_response_high" in notes or "low_power_balance_pressure" in notes:
                return "interpretable_positive_candidate", notes
            return "weak_positive_candidate", notes
        return "fragile_positive_candidate", notes

    if state == "negative_leakage_margin":
        if c is not None and f is not None and f > c:
            notes.append("fragmentation_exceeds_capacity")
        if power is not None and power >= 0.55:
            notes.append("power_balance_pressure_high")
        if edge is not None and edge <= 0.35:
            notes.append("edge_response_low")
        if d_before.get("m_edge") is not None and d_before["m_edge"] < 0:
            notes.append("m_edge_lower_than_before")

        if "fragmentation_exceeds_capacity" in notes and "high_missingness_pressure" not in notes:
            if "power_balance_pressure_high" in notes or "edge_response_low" in notes:
                return "interpretable_negative_candidate", notes
            return "weak_negative_candidate", notes
        return "fragile_negative_candidate", notes

    if "peak_positive" in state:
        return classify("positive_boundary_margin", during, d_before)
    if "peak_negative" in state:
        return classify("negative_leakage_margin", during, d_before)
    return "boundary_or_other_window", notes


def inspect_window(df: pd.DataFrame, window: Window, columns: List[str], context_width: float) -> Dict[str, Any]:
    during_df = slice_time(df, window.start_time, window.end_time)
    before_df = slice_time(df, window.start_time - context_width, window.start_time)
    after_df = slice_time(df, window.end_time, window.end_time + context_width)

    during = {c: finite_stats(during_df[c]) for c in columns if c in during_df.columns}
    before = {c: finite_stats(before_df[c]) for c in columns if c in before_df.columns}
    after = {c: finite_stats(after_df[c]) for c in columns if c in after_df.columns}

    d_before: Dict[str, Optional[float]] = {}
    d_after: Dict[str, Optional[float]] = {}
    trend: Dict[str, Dict[str, Any]] = {}

    for c in columns:
        dm = med(during, c)
        bm = med(before, c)
        am = med(after, c)
        d_before[c] = None if dm is None or bm is None else float(dm - bm)
        d_after[c] = None if dm is None or am is None else float(dm - am)
        first, last, slope = first_last_slope(during_df, c)
        trend[c] = {"first": first, "last": last, "slope_per_s": slope, "trend": slope_label(first, last)}

    flag, notes = classify(window.state, during, d_before)

    flat: Dict[str, Any] = {
        "window_label": window.label,
        "state": window.state,
        "start_time": window.start_time,
        "end_time": window.end_time,
        "duration": window.duration,
        "start_index": window.start_index,
        "end_index": window.end_index,
        "point_count": int(len(during_df)),
        "interpretability_flag": flag,
        "interpretability_notes": ";".join(notes),
    }

    for c in columns:
        flat[f"{c}__during_median"] = med(during, c)
        flat[f"{c}__before_median"] = med(before, c)
        flat[f"{c}__after_median"] = med(after, c)
        flat[f"{c}__delta_vs_before"] = d_before.get(c)
        flat[f"{c}__delta_vs_after"] = d_after.get(c)
        flat[f"{c}__trend"] = trend.get(c, {}).get("trend")
        flat[f"{c}__slope_per_s"] = trend.get(c, {}).get("slope_per_s")

    return {"flat": flat, "during": during, "before": before, "after": after, "delta_vs_before": d_before, "delta_vs_after": d_after, "trend": trend}


def global_summary(df: pd.DataFrame) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "rows": int(len(df)),
        "time_min": to_float(df["time_s"].min()),
        "time_max": to_float(df["time_s"].max()),
        "state_counts": df["m_edge_state"].astype(str).value_counts(dropna=False).to_dict(),
    }
    for c in [c for c in PRIMARY_COLUMNS if c in df.columns]:
        out[f"{c}_stats"] = finite_stats(df[c])
    return out


def make_report(input_path: Path, summary: Dict[str, Any], rows: List[Dict[str, Any]], details: List[Dict[str, Any]], min_duration: float, context_width: float) -> str:
    rows_df = pd.DataFrame(rows)
    lines: List[str] = []
    lines.append("# TokaMark m_edge(t) Trace Inspection")
    lines.append("")
    lines.append("## 1. Purpose")
    lines.append("")
    lines.append("This report inspects the first `m_edge(t)` trace for a public MAST/TokaMark shot and asks whether detected positive and negative windows have interpretable diagnostic structure.")
    lines.append("")
    lines.append("This is trace-level triage. It is not formula revision and not physical validation.")
    lines.append("")
    lines.append("## 2. Input")
    lines.append("")
    lines.append(f"```text\n{input_path}\n```")
    lines.append("")
    lines.append("## 3. Settings")
    lines.append("")
    lines.append("```text")
    lines.append(f"minimum interval duration: {min_duration} s")
    lines.append(f"context width before/after: {context_width} s")
    lines.append("```")
    lines.append("")
    lines.append("## 4. Global trace summary")
    lines.append("")
    lines.append("```text")
    lines.append(f"rows:     {summary.get('rows')}")
    lines.append(f"time_min: {summary.get('time_min')}")
    lines.append(f"time_max: {summary.get('time_max')}")
    lines.append("```")
    lines.append("")
    lines.append("State counts:")
    lines.append("")
    lines.append("```text")
    for k, v in summary.get("state_counts", {}).items():
        lines.append(f"{k}: {v}")
    lines.append("```")
    lines.append("")
    lines.append("## 5. Inspected windows")
    lines.append("")
    if rows_df.empty:
        lines.append("_No windows met the inspection criteria._")
    else:
        show = [
            "window_label", "state", "start_time", "end_time", "duration", "point_count",
            "interpretability_flag", "interpretability_notes",
            "m_edge__during_median", "C_edge_capacity__during_median",
            "F_route_fragmentation__during_median", "S_edge_response__during_median",
            "S_power_balance__during_median", "S_transport__during_median",
            "missingness_pressure__during_median",
        ]
        show = [c for c in show if c in rows_df.columns]
        lines.append(rows_df[show].to_markdown(index=False, floatfmt=".6g"))
    lines.append("")
    lines.append("## 6. Interpretability flags")
    lines.append("")
    if rows_df.empty:
        lines.append("_No flags._")
    else:
        counts = rows_df["interpretability_flag"].value_counts().to_dict()
        lines.append("```text")
        for k, v in counts.items():
            lines.append(f"{k}: {v}")
        lines.append("```")
    lines.append("")
    lines.append("## 7. Detailed window notes")
    lines.append("")
    detail_by_label = {d["flat"]["window_label"]: d for d in details}
    for row in rows[:12]:
        d = detail_by_label[row["window_label"]]["flat"]
        lines.append(f"### {d['window_label']} — {d['state']}")
        lines.append("")
        lines.append("```text")
        lines.append(f"time: {d['start_time']} → {d['end_time']} s")
        lines.append(f"duration: {d['duration']} s")
        lines.append(f"flag: {d['interpretability_flag']}")
        lines.append(f"notes: {d['interpretability_notes']}")
        lines.append("")
        for c in REPORT_COLUMNS:
            lines.append(
                f"{c}: during={d.get(c + '__during_median')} "
                f"delta_before={d.get(c + '__delta_vs_before')} "
                f"trend={d.get(c + '__trend')}"
            )
        lines.append("```")
        lines.append("")
    lines.append("## 8. Main conclusion")
    lines.append("")
    lines.append("The inspected windows should be used to decide whether the v0.1 `m_edge(t)` trace has interpretable diagnostic behavior. Positive intervals are stronger when capacity exceeds fragmentation, edge response is high, and missingness is not dominant. Negative intervals are stronger when fragmentation exceeds capacity with coherent route-stress proxies.")
    lines.append("")
    lines.append("If the positive intervals are interpretable, the next step is cross-shot comparison with a weaker or negative TokaMark candidate. If they are fragile or missingness-dominated, revise the v0.1 formula before using it further.")
    lines.append("")
    lines.append("## 9. Next document")
    lines.append("")
    lines.append("```text")
    lines.append("docs/")
    lines.append("  20_TOKAMARK_M_EDGE_T_TRACE_INSPECTION.md")
    lines.append("```")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect TokaMark m_edge(t) trace windows.")
    parser.add_argument("--input", default="outputs/reports/tokamark_shot_12063_m_edge_t_probe.csv")
    parser.add_argument("--out-dir", default="outputs/reports")
    parser.add_argument("--shot-id", type=int, default=12063)
    parser.add_argument("--min-duration", type=float, default=0.003)
    parser.add_argument("--context-width", type=float, default=0.010)
    parser.add_argument("--peak-half-width", type=float, default=0.004)
    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    if "time_s" not in df.columns or "m_edge_state" not in df.columns:
        raise ValueError("Input must contain time_s and m_edge_state columns.")
    df["time_s"] = pd.to_numeric(df["time_s"], errors="coerce")
    df = df.sort_values("time_s").reset_index(drop=True)

    cols = [c for c in PRIMARY_COLUMNS if c in df.columns]

    windows: List[Window] = []
    windows += contiguous_windows(df, "positive_boundary_margin", args.min_duration, "positive")
    windows += contiguous_windows(df, "negative_leakage_margin", args.min_duration, "negative")

    ppos = peak_window(df, "m_edge", "max", args.peak_half_width, "peak_positive_window", "peak_positive")
    pneg = peak_window(df, "m_edge", "min", args.peak_half_width, "peak_negative_window", "peak_negative")
    if ppos:
        windows.append(ppos)
    if pneg:
        windows.append(pneg)

    # Keep deterministic order.
    windows = sorted(windows, key=lambda w: (w.start_time, w.label))

    details = [inspect_window(df, w, cols, args.context_width) for w in windows]
    rows = [d["flat"] for d in details]

    summary = global_summary(df)
    summary.update({
        "component": "tokamark_m_edge_trace_inspector.py",
        "input": str(input_path),
        "shot_id": args.shot_id,
        "min_duration": args.min_duration,
        "context_width": args.context_width,
        "peak_half_width": args.peak_half_width,
        "window_count": len(rows),
        "interpretability_counts": pd.Series([r["interpretability_flag"] for r in rows]).value_counts().to_dict() if rows else {},
    })

    prefix = f"tokamark_shot_{args.shot_id}_m_edge_trace_inspection"
    windows_csv = out_dir / f"{prefix}_windows.csv"
    summary_json = out_dir / f"{prefix}_summary.json"
    report_md = out_dir / f"{prefix}.md"

    pd.DataFrame(rows).to_csv(windows_csv, index=False)
    summary_json.write_text(json.dumps({"summary": summary, "windows": rows}, indent=2, default=str), encoding="utf-8")
    report_md.write_text(make_report(input_path, summary, rows, details, args.min_duration, args.context_width), encoding="utf-8")

    print("Trace inspection complete.")
    print(f"Windows CSV: {windows_csv}")
    print(f"Summary:     {summary_json}")
    print(f"Report:      {report_md}")
    print("Interpretability counts:")
    for k, v in summary["interpretability_counts"].items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()

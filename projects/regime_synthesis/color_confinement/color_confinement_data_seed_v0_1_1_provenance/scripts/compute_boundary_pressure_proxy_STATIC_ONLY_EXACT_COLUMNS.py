#!/usr/bin/env python3
"""
compute_boundary_pressure_proxy.py

UNNS Color Confinement / Boundary-Pressure Proxy v0.3.0
STATIC-ONLY, exact-column aligned version

Reads:
  reports/repair_threshold_window_static_gaps.csv

Expected static table columns:
  r_fm
  gap01_GeV
  gap12_GeV
  d_gap01_GeV_d_r_GeV_per_fm
  d_gap12_GeV_d_r_GeV_per_fm

Writes:
  reports/boundary_pressure_proxy_table.csv
  reports/boundary_pressure_proxy_metrics.json
  reports/boundary_pressure_proxy_summary.md
  chamber_inputs/boundary_pressure_proxy_ladder.csv
  chamber_inputs/boundary_pressure_proxy_ladder_SCHEMA.csv

Purpose:
  Compute the first explicit UNNS boundary-pressure proxy:

      Pi_boundary_available(r)

  from static repair-window gap compression, threshold proximity, and
  repair-window sharpening. This version deliberately removes the stale
  flux path and does not read Baker flux tables.

Boundary:
  This is a structural diagnostic proxy. It is not a QCD potential and not
  a fitted confinement law.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


VERSION = "0.3.0_STATIC_ONLY_EXACT_COLUMNS"

DEFAULT_R_C_FM = 1.224
DEFAULT_R_CS_FM = 1.293

# We keep the same relative emphasis from the definition note, but with flux removed.
# These are renormalized before use.
DEFAULT_WEIGHTS_UNNORMALIZED = {
    "gap": 0.35,
    "threshold": 0.30,
    "slope": 0.20,
}

# Exact columns used by repair_threshold_window_static_gaps.csv.
REQUIRED_COLUMNS = [
    "r_fm",
    "gap01_GeV",
    "gap12_GeV",
]

OPTIONAL_SLOPE_COLUMNS = [
    "d_gap01_GeV_d_r_GeV_per_fm",
    "d_gap12_GeV_d_r_GeV_per_fm",
]


# ---------------------------------------------------------------------------
# CSV and numeric utilities
# ---------------------------------------------------------------------------

def safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    s = str(value).strip().replace("−", "-")
    if not s or s.lower() in {"nan", "none", "null", "na", "n/a", "--", "—"}:
        return None
    try:
        x = float(s)
    except ValueError:
        return None
    if math.isnan(x) or math.isinf(x):
        return None
    return x


def read_csv_dicts(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = [dict(r) for r in reader]
    if not rows:
        raise ValueError(f"No rows found in {path}")
    return rows


def format_csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return f"{value:.10g}"
    return value


def write_csv_dicts(path: Path, rows: List[Dict[str, Any]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: format_csv_value(row.get(k)) for k in fieldnames})


def normalize_weights(raw: Dict[str, float]) -> Dict[str, float]:
    total = sum(v for v in raw.values() if v > 0)
    if total <= 0:
        raise ValueError("Weight sum must be positive.")
    return {k: max(v, 0.0) / total for k, v in raw.items()}


def minmax_norm(values: Sequence[Optional[float]], neutral: float = 0.5) -> List[Optional[float]]:
    valid = [v for v in values if v is not None and not math.isnan(v)]
    if not valid:
        return [None for _ in values]
    lo, hi = min(valid), max(valid)
    if abs(hi - lo) <= 1e-15:
        return [neutral if v is not None else None for v in values]
    return [None if v is None else (v - lo) / (hi - lo) for v in values]


def mean_available(values: Iterable[Optional[float]]) -> Optional[float]:
    valid = [v for v in values if v is not None and not math.isnan(v)]
    if not valid:
        return None
    return sum(valid) / len(valid)


def weighted_available(components: Dict[str, Optional[float]], weights: Dict[str, float]) -> Optional[float]:
    numerator = 0.0
    denominator = 0.0
    for key, value in components.items():
        if value is None or math.isnan(value):
            continue
        w = weights.get(key, 0.0)
        numerator += w * value
        denominator += w
    if denominator <= 0:
        return None
    return numerator / denominator


def clip01(x: float) -> float:
    return max(0.0, min(1.0, x))


def pressure_band(pi_value: Optional[float]) -> str:
    if pi_value is None:
        return "UNAVAILABLE"
    if pi_value < 0.25:
        return "RELAXED_ROUTE_EXTENSION"
    if pi_value < 0.50:
        return "MILD_BOUNDARY_TENSION"
    if pi_value < 0.75:
        return "ACTIVE_REPAIR_WINDOW_PRESSURE"
    return "HIGH_BOUNDARY_PRESSURE_NEAR_REPAIR"


def median_positive_spacing(xs: Sequence[float]) -> float:
    diffs = [b - a for a, b in zip(xs[:-1], xs[1:]) if b > a]
    if not diffs:
        return 1e-6
    return statistics.median(diffs)


# ---------------------------------------------------------------------------
# Exact-column input loading
# ---------------------------------------------------------------------------

def validate_static_columns(rows: List[Dict[str, str]]) -> None:
    columns = set(rows[0].keys())
    missing = [c for c in REQUIRED_COLUMNS if c not in columns]
    if missing:
        raise ValueError(
            "Input table is not the expected repair-window table. "
            f"Missing required columns: {missing}. Available columns: {list(rows[0].keys())}"
        )


def finite_difference(xs: Sequence[float], ys: Sequence[Optional[float]]) -> List[Optional[float]]:
    """Fallback derivative if source derivative columns are missing."""
    n = len(xs)
    slopes: List[Optional[float]] = [None] * n
    for i in range(n):
        if ys[i] is None:
            continue
        if n == 1:
            continue
        if i == 0 and ys[1] is not None and xs[1] != xs[0]:
            slopes[i] = abs((ys[1] - ys[0]) / (xs[1] - xs[0]))
        elif i == n - 1 and ys[n - 2] is not None and xs[n - 1] != xs[n - 2]:
            slopes[i] = abs((ys[n - 1] - ys[n - 2]) / (xs[n - 1] - xs[n - 2]))
        elif 0 < i < n - 1 and ys[i - 1] is not None and ys[i + 1] is not None and xs[i + 1] != xs[i - 1]:
            slopes[i] = abs((ys[i + 1] - ys[i - 1]) / (xs[i + 1] - xs[i - 1]))
    return slopes


def load_static_table(path: Path) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    rows = read_csv_dicts(path)
    validate_static_columns(rows)

    have_source_slopes = all(c in rows[0] for c in OPTIONAL_SLOPE_COLUMNS)

    out: List[Dict[str, Any]] = []
    for idx, row in enumerate(rows):
        r_fm = safe_float(row.get("r_fm"))
        gap01 = safe_float(row.get("gap01_GeV"))
        gap12 = safe_float(row.get("gap12_GeV"))
        if r_fm is None:
            continue

        item = {
            "source_row": idx + 1,
            "r_fm": r_fm,
            "gap01_GeV": gap01,
            "gap12_GeV": gap12,
            "data_status_source": row.get("data_status", ""),
            "source_id": row.get("source_id", ""),
        }

        if have_source_slopes:
            item["d_gap01_GeV_d_r_GeV_per_fm"] = safe_float(row.get("d_gap01_GeV_d_r_GeV_per_fm"))
            item["d_gap12_GeV_d_r_GeV_per_fm"] = safe_float(row.get("d_gap12_GeV_d_r_GeV_per_fm"))
        else:
            item["d_gap01_GeV_d_r_GeV_per_fm"] = None
            item["d_gap12_GeV_d_r_GeV_per_fm"] = None

        out.append(item)

    if not out:
        raise ValueError(f"No usable rows found in {path}")

    out.sort(key=lambda row: row["r_fm"])

    # Fallback slopes if exact source derivative columns are absent.
    if not have_source_slopes:
        xs = [r["r_fm"] for r in out]
        d01 = [r["gap01_GeV"] for r in out]
        d12 = [r["gap12_GeV"] for r in out]
        fd01 = finite_difference(xs, d01)
        fd12 = finite_difference(xs, d12)
        for row, s01, s12 in zip(out, fd01, fd12):
            row["d_gap01_GeV_d_r_GeV_per_fm"] = s01
            row["d_gap12_GeV_d_r_GeV_per_fm"] = s12

    metadata = {
        "columns_used": {
            "r": "r_fm",
            "gap01": "gap01_GeV",
            "gap12": "gap12_GeV",
            "slope01": "d_gap01_GeV_d_r_GeV_per_fm" if have_source_slopes else "finite_difference_fallback",
            "slope12": "d_gap12_GeV_d_r_GeV_per_fm" if have_source_slopes else "finite_difference_fallback",
        },
        "source_slope_columns_present": have_source_slopes,
        "input_columns": list(rows[0].keys()),
    }
    return out, metadata


# ---------------------------------------------------------------------------
# Proxy computation
# ---------------------------------------------------------------------------

def compute_proxy_table(
    static_rows: List[Dict[str, Any]],
    *,
    r_c_fm: float,
    r_cs_fm: float,
    weights: Dict[str, float],
) -> List[Dict[str, Any]]:
    r_values = [row["r_fm"] for row in static_rows]
    gap01 = [row["gap01_GeV"] for row in static_rows]
    gap12 = [row["gap12_GeV"] for row in static_rows]

    slope01_abs = [None if row["d_gap01_GeV_d_r_GeV_per_fm"] is None else abs(row["d_gap01_GeV_d_r_GeV_per_fm"]) for row in static_rows]
    slope12_abs = [None if row["d_gap12_GeV_d_r_GeV_per_fm"] is None else abs(row["d_gap12_GeV_d_r_GeV_per_fm"]) for row in static_rows]

    # Gap compression: smaller normalized gap means stronger compression.
    gap01_norm = minmax_norm(gap01)
    gap12_norm = minmax_norm(gap12)
    g01_compression = [None if v is None else 1.0 - v for v in gap01_norm]
    g12_compression = [None if v is None else 1.0 - v for v in gap12_norm]
    c_gap = [mean_available([a, b]) for a, b in zip(g01_compression, g12_compression)]

    # Threshold proximity: nearest distance to r_c or r_cs.
    threshold_width = max(abs(r_cs_fm - r_c_fm), median_positive_spacing(r_values), 1e-9)
    c_threshold = []
    for r in r_values:
        d_thr = min(abs(r - r_c_fm), abs(r - r_cs_fm))
        c_threshold.append(clip01(1.0 - d_thr / threshold_width))

    # Sharpening: normalize absolute source derivatives.
    slope01_norm = minmax_norm(slope01_abs)
    slope12_norm = minmax_norm(slope12_abs)
    c_slope = [mean_available([a, b]) for a, b in zip(slope01_norm, slope12_norm)]

    out: List[Dict[str, Any]] = []
    for i, base in enumerate(static_rows):
        components = {
            "gap": c_gap[i],
            "threshold": c_threshold[i],
            "slope": c_slope[i],
        }
        pi_value = weighted_available(components, weights)
        available_components = [k for k, v in components.items() if v is not None]
        missing_components = [k for k, v in components.items() if v is None]

        notes = []
        notes.append("STATIC_ONLY")
        notes.append("FLUX_PATH_REMOVED")
        if missing_components:
            notes.append("missing_components=" + "|".join(missing_components))

        out.append({
            "r_fm": base["r_fm"],
            "gap01_GeV": base["gap01_GeV"],
            "gap12_GeV": base["gap12_GeV"],
            "G01_compression": g01_compression[i],
            "G12_compression": g12_compression[i],
            "C_gap": c_gap[i],
            "C_threshold": c_threshold[i],
            "S01_abs_GeV_per_fm": slope01_abs[i],
            "S12_abs_GeV_per_fm": slope12_abs[i],
            "C_slope": c_slope[i],
            "C_flux": None,
            "Pi_boundary_available": pi_value,
            "pressure_band": pressure_band(pi_value),
            "available_components": "|".join(available_components),
            "data_status": "STATIC_ONLY",
            "source_data_status": base.get("data_status_source", ""),
            "notes": "; ".join(notes),
        })

    return out


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def write_ladder(path: Path, table: List[Dict[str, Any]], *, sort_values: bool = True) -> None:
    values = [row["Pi_boundary_available"] for row in table if row["Pi_boundary_available"] is not None]
    if sort_values:
        values = sorted(values)

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["value"])
        for value in values:
            writer.writerow([f"{value:.10g}"])


def write_schema(path: Path) -> None:
    rows = [
        {
            "field": "value",
            "meaning": "Pi_boundary_available(r), static-only boundary-pressure proxy ladder",
            "units": "dimensionless",
            "status": "derived_UNNS_boundary_pressure_proxy_STATIC_ONLY",
        }
    ]
    write_csv_dicts(path, rows, ["field", "meaning", "units", "status"])


def build_metrics(
    table: List[Dict[str, Any]],
    *,
    static_path: Path,
    input_metadata: Dict[str, Any],
    r_c_fm: float,
    r_cs_fm: float,
    weights: Dict[str, float],
) -> Dict[str, Any]:
    values = [row["Pi_boundary_available"] for row in table if row["Pi_boundary_available"] is not None]
    band_counts: Dict[str, int] = {}
    for row in table:
        band_counts[row["pressure_band"]] = band_counts.get(row["pressure_band"], 0) + 1

    if values:
        max_row = max(table, key=lambda r: -1.0 if r["Pi_boundary_available"] is None else r["Pi_boundary_available"])
        min_row = min(table, key=lambda r: 2.0 if r["Pi_boundary_available"] is None else r["Pi_boundary_available"])
    else:
        max_row = {}
        min_row = {}

    return {
        "script": "compute_boundary_pressure_proxy.py",
        "version": VERSION,
        "mode": "STATIC_ONLY_EXACT_COLUMNS",
        "status": "computed_proxy_not_physical_law",
        "inputs": {
            "static": str(static_path),
            "flux": "REMOVED_NOT_READ",
            "input_metadata": input_metadata,
        },
        "threshold_markers": {
            "r_c_fm": r_c_fm,
            "r_cs_fm": r_cs_fm,
        },
        "weights_effective_normalized": weights,
        "rows": len(table),
        "pi_boundary": {
            "min": min(values) if values else None,
            "max": max(values) if values else None,
            "mean": sum(values) / len(values) if values else None,
            "min_at_r_fm": min_row.get("r_fm"),
            "max_at_r_fm": max_row.get("r_fm"),
            "max_band": max_row.get("pressure_band"),
        },
        "pressure_band_counts": band_counts,
        "boundary": (
            "STATIC_ONLY structural diagnostic proxy derived from repair-window static gaps. "
            "It is not a QCD potential and not a fitted universal confinement law."
        ),
    }


def write_summary(path: Path, metrics: Dict[str, Any], table_path: Path, ladder_path: Path) -> None:
    pi = metrics["pi_boundary"]
    md = f"""# Boundary-Pressure Proxy Computation Summary

**Script:** compute_boundary_pressure_proxy.py  
**Version:** {VERSION}  
**Mode:** STATIC_ONLY_EXACT_COLUMNS  
**Status:** computed structural diagnostic proxy, not a fitted physical law

## Inputs

```text
static: {metrics['inputs']['static']}
flux:   REMOVED_NOT_READ
```

## Exact columns used

```json
{json.dumps(metrics['inputs']['input_metadata']['columns_used'], indent=2)}
```

## Outputs

```text
{table_path}
{ladder_path}
```

## Threshold markers

```text
r_c  = {metrics['threshold_markers']['r_c_fm']} fm
r_cs = {metrics['threshold_markers']['r_cs_fm']} fm
```

## Effective normalized weights

```json
{json.dumps(metrics['weights_effective_normalized'], indent=2)}
```

## Proxy range

```text
rows: {metrics['rows']}
min Pi_boundary_available: {pi['min']}
max Pi_boundary_available: {pi['max']}
mean Pi_boundary_available: {pi['mean']}
min at r_fm: {pi['min_at_r_fm']}
max at r_fm: {pi['max_at_r_fm']}
max band: {pi['max_band']}
```

## Band counts

```json
{json.dumps(metrics['pressure_band_counts'], indent=2)}
```

## Boundary

This table is a structural UNNS diagnostic. It is not a QCD potential, not a
derivation of confinement, and not a universal fitted law.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(md, encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Compute static-only UNNS boundary-pressure proxy.")
    parser.add_argument("--root", default=".", help="Project root. Default: current directory.")
    parser.add_argument("--static", default="reports/repair_threshold_window_static_gaps.csv")
    parser.add_argument("--output-table", default="reports/boundary_pressure_proxy_table.csv")
    parser.add_argument("--output-ladder", default="chamber_inputs/boundary_pressure_proxy_ladder.csv")
    parser.add_argument("--output-schema", default="chamber_inputs/boundary_pressure_proxy_ladder_SCHEMA.csv")
    parser.add_argument("--output-metrics", default="reports/boundary_pressure_proxy_metrics.json")
    parser.add_argument("--output-summary", default="reports/boundary_pressure_proxy_summary.md")
    parser.add_argument("--r-c", type=float, default=DEFAULT_R_C_FM)
    parser.add_argument("--r-cs", type=float, default=DEFAULT_R_CS_FM)
    parser.add_argument("--w-gap", type=float, default=DEFAULT_WEIGHTS_UNNORMALIZED["gap"])
    parser.add_argument("--w-threshold", type=float, default=DEFAULT_WEIGHTS_UNNORMALIZED["threshold"])
    parser.add_argument("--w-slope", type=float, default=DEFAULT_WEIGHTS_UNNORMALIZED["slope"])
    parser.add_argument("--preserve-r-order-ladder", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    static_path = (root / args.static).resolve()
    output_table = (root / args.output_table).resolve()
    output_ladder = (root / args.output_ladder).resolve()
    output_schema = (root / args.output_schema).resolve()
    output_metrics = (root / args.output_metrics).resolve()
    output_summary = (root / args.output_summary).resolve()

    weights = normalize_weights({
        "gap": args.w_gap,
        "threshold": args.w_threshold,
        "slope": args.w_slope,
    })

    static_rows, input_metadata = load_static_table(static_path)
    table = compute_proxy_table(static_rows, r_c_fm=args.r_c, r_cs_fm=args.r_cs, weights=weights)

    fieldnames = [
        "r_fm",
        "gap01_GeV",
        "gap12_GeV",
        "G01_compression",
        "G12_compression",
        "C_gap",
        "C_threshold",
        "S01_abs_GeV_per_fm",
        "S12_abs_GeV_per_fm",
        "C_slope",
        "C_flux",
        "Pi_boundary_available",
        "pressure_band",
        "available_components",
        "data_status",
        "source_data_status",
        "notes",
    ]
    write_csv_dicts(output_table, table, fieldnames)
    write_ladder(output_ladder, table, sort_values=not args.preserve_r_order_ladder)
    write_schema(output_schema)

    metrics = build_metrics(
        table,
        static_path=static_path,
        input_metadata=input_metadata,
        r_c_fm=args.r_c,
        r_cs_fm=args.r_cs,
        weights=weights,
    )
    output_metrics.parent.mkdir(parents=True, exist_ok=True)
    output_metrics.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    write_summary(output_summary, metrics, output_table, output_ladder)

    print("BOUNDARY-PRESSURE PROXY COMPLETE")
    print(f"version: {VERSION}")
    print("mode: STATIC_ONLY_EXACT_COLUMNS")
    print(f"rows: {metrics['rows']}")
    print("flux: REMOVED_NOT_READ")
    print(f"table:   {output_table}")
    print(f"ladder:  {output_ladder}")
    print(f"schema:  {output_schema}")
    print(f"metrics: {output_metrics}")
    print(f"summary: {output_summary}")
    print("boundary: structural diagnostic proxy; not a QCD potential or fitted law")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

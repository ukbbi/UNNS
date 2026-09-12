#!/usr/bin/env python3
"""
compute_boundary_pressure_proxy.py

UNNS Color Confinement / Boundary-Pressure Proxy v0.1.0

Reads:
  reports/repair_threshold_window_static_gaps.csv
  reports/baker_flux_profile_trusted_summary.csv          [optional]

Writes:
  reports/boundary_pressure_proxy_table.csv
  reports/boundary_pressure_proxy_metrics.json
  reports/boundary_pressure_proxy_summary.md
  chamber_inputs/boundary_pressure_proxy_ladder.csv
  chamber_inputs/boundary_pressure_proxy_ladder_SCHEMA.csv

Purpose:
  Compute the first explicit UNNS boundary-pressure proxy:

      Pi_boundary_available(r)

  from static repair-window gap compression, threshold proximity,
  finite-difference sharpening, and optional flux-tube localization.

Important boundary:
  This script computes a structural diagnostic proxy. It does not claim to
  derive QCD confinement and does not fit a universal physical law.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# Defaults from the current color-confinement diagnostic chain
# ---------------------------------------------------------------------------

DEFAULT_R_C = 1.224
DEFAULT_R_CS = 1.293

DEFAULT_WEIGHTS = {
    "gap": 0.35,
    "threshold": 0.30,
    "slope": 0.20,
    "flux": 0.15,
}


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def read_csv_dicts(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = [dict(r) for r in reader]
    if not rows:
        raise ValueError(f"No rows found in {path}")
    return rows


def write_csv_dicts(path: Path, rows: List[Dict[str, Any]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: format_csv_value(row.get(k)) for k in fieldnames})


def format_csv_value(v: Any) -> Any:
    if v is None:
        return ""
    if isinstance(v, float):
        if math.isnan(v):
            return ""
        return f"{v:.10g}"
    return v


def safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    s = str(value).strip()
    if not s or s.lower() in {"nan", "none", "null", "na", "n/a", "--", "—"}:
        return None
    # allow accidental unicode minus
    s = s.replace("−", "-")
    try:
        x = float(s)
    except ValueError:
        return None
    if math.isnan(x) or math.isinf(x):
        return None
    return x


def lower_key_map(row: Dict[str, Any]) -> Dict[str, str]:
    return {k.strip().lower(): k for k in row.keys()}


def find_column(rows: Sequence[Dict[str, Any]], aliases: Sequence[str]) -> Optional[str]:
    if not rows:
        return None
    keymap = lower_key_map(rows[0])
    normalized_aliases = [a.strip().lower() for a in aliases]

    # exact case-insensitive match
    for a in normalized_aliases:
        if a in keymap:
            return keymap[a]

    # relaxed matching: remove punctuation and separators
    def squash(s: str) -> str:
        return "".join(ch for ch in s.lower() if ch.isalnum())

    squashed = {squash(k): v for k, v in keymap.items()}
    for a in normalized_aliases:
        sa = squash(a)
        if sa in squashed:
            return squashed[sa]

    return None


def first_number(row: Dict[str, Any], col: Optional[str]) -> Optional[float]:
    if col is None:
        return None
    return safe_float(row.get(col))


def minmax_norm(values: Sequence[Optional[float]], *, neutral: float = 0.5) -> List[Optional[float]]:
    valid = [v for v in values if v is not None and not math.isnan(v)]
    if not valid:
        return [None for _ in values]
    lo, hi = min(valid), max(valid)
    if abs(hi - lo) <= 1e-15:
        return [neutral if v is not None else None for v in values]
    return [None if v is None else (v - lo) / (hi - lo) for v in values]


def clip01(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return max(0.0, min(1.0, x))


def mean_available(values: Iterable[Optional[float]]) -> Optional[float]:
    valid = [v for v in values if v is not None and not math.isnan(v)]
    if not valid:
        return None
    return sum(valid) / len(valid)


def weighted_available(components: Dict[str, Optional[float]], weights: Dict[str, float]) -> Optional[float]:
    num = 0.0
    den = 0.0
    for k, v in components.items():
        if v is None or math.isnan(v):
            continue
        w = weights.get(k, 0.0)
        num += w * v
        den += w
    if den <= 0:
        return None
    return num / den


def finite_difference(xs: Sequence[float], ys: Sequence[Optional[float]]) -> Tuple[List[Optional[float]], List[str]]:
    """
    Finite-difference |dy/dx|.
    Uses centered differences in the interior and one-sided differences at endpoints.
    """
    n = len(xs)
    slopes: List[Optional[float]] = [None] * n
    notes: List[str] = [""] * n

    for i in range(n):
        if ys[i] is None:
            continue

        if n == 1:
            notes[i] = "NO_SLOPE_SINGLE_ROW"
            continue

        if i == 0:
            j = 1
            if ys[j] is not None and xs[j] != xs[i]:
                slopes[i] = abs((ys[j] - ys[i]) / (xs[j] - xs[i]))
                notes[i] = "ENDPOINT_ONE_SIDED"
        elif i == n - 1:
            j = n - 2
            if ys[j] is not None and xs[i] != xs[j]:
                slopes[i] = abs((ys[i] - ys[j]) / (xs[i] - xs[j]))
                notes[i] = "ENDPOINT_ONE_SIDED"
        else:
            j0, j1 = i - 1, i + 1
            if ys[j0] is not None and ys[j1] is not None and xs[j1] != xs[j0]:
                slopes[i] = abs((ys[j1] - ys[j0]) / (xs[j1] - xs[j0]))
                notes[i] = "CENTERED"
            else:
                # fallback to any available one-sided neighbor
                candidates = []
                for j in (j0, j1):
                    if ys[j] is not None and xs[j] != xs[i]:
                        candidates.append(abs((ys[j] - ys[i]) / (xs[j] - xs[i])))
                if candidates:
                    slopes[i] = sum(candidates) / len(candidates)
                    notes[i] = "LOCAL_ONE_SIDED_FALLBACK"

    return slopes, notes


def pressure_band(pi: Optional[float]) -> str:
    if pi is None:
        return "UNAVAILABLE"
    if pi < 0.25:
        return "RELAXED_ROUTE_EXTENSION"
    if pi < 0.50:
        return "MILD_BOUNDARY_TENSION"
    if pi < 0.75:
        return "ACTIVE_REPAIR_WINDOW_PRESSURE"
    return "HIGH_BOUNDARY_PRESSURE_NEAR_REPAIR"


def median_positive_spacing(xs: Sequence[float]) -> float:
    diffs = [b - a for a, b in zip(xs[:-1], xs[1:]) if b > a]
    if not diffs:
        return 1e-6
    return statistics.median(diffs)


# ---------------------------------------------------------------------------
# Static table normalization
# ---------------------------------------------------------------------------

@dataclass
class StaticColumns:
    r: str
    delta01: Optional[str]
    delta12: Optional[str]
    v0: Optional[str]
    v1: Optional[str]
    v2: Optional[str]


def detect_static_columns(rows: Sequence[Dict[str, Any]]) -> StaticColumns:
    r_col = find_column(rows, [
        "r_fm", "r", "separation_fm", "source_separation_fm", "distance_fm",
        "static_source_separation_fm", "r_nearest_fm"
    ])
    if r_col is None:
        raise ValueError("Could not detect source-separation column. Expected r_fm or similar.")

    d01_col = find_column(rows, [
        "delta01_GeV", "delta01", "gap01_GeV", "gap01", "V1_minus_V0_GeV",
        "V1-V0", "gap_V1_V0_GeV", "gap_v1_v0", "gap01_nearest_GeV"
    ])
    d12_col = find_column(rows, [
        "delta12_GeV", "delta12", "gap12_GeV", "gap12", "V2_minus_V1_GeV",
        "V2-V1", "gap_V2_V1_GeV", "gap_v2_v1", "gap12_nearest_GeV"
    ])

    v0_col = find_column(rows, ["V0_GeV", "V0", "E0_GeV", "E0"])
    v1_col = find_column(rows, ["V1_GeV", "V1", "E1_GeV", "E1"])
    v2_col = find_column(rows, ["V2_GeV", "V2", "E2_GeV", "E2"])

    if d01_col is None and not (v0_col and v1_col):
        raise ValueError("Could not detect delta01/gap01 or V0,V1 columns.")
    if d12_col is None and not (v1_col and v2_col):
        raise ValueError("Could not detect delta12/gap12 or V1,V2 columns.")

    return StaticColumns(
        r=r_col, delta01=d01_col, delta12=d12_col, v0=v0_col, v1=v1_col, v2=v2_col
    )


def build_static_rows(path: Path) -> Tuple[List[Dict[str, Any]], StaticColumns]:
    rows = read_csv_dicts(path)
    cols = detect_static_columns(rows)

    out: List[Dict[str, Any]] = []
    for idx, row in enumerate(rows):
        r = first_number(row, cols.r)
        if r is None:
            continue

        d01 = first_number(row, cols.delta01)
        d12 = first_number(row, cols.delta12)

        if d01 is None and cols.v0 and cols.v1:
            v0 = first_number(row, cols.v0)
            v1 = first_number(row, cols.v1)
            if v0 is not None and v1 is not None:
                d01 = v1 - v0

        if d12 is None and cols.v1 and cols.v2:
            v1 = first_number(row, cols.v1)
            v2 = first_number(row, cols.v2)
            if v1 is not None and v2 is not None:
                d12 = v2 - v1

        out.append({
            "source_row": idx + 1,
            "r_fm": r,
            "delta01_GeV": d01,
            "delta12_GeV": d12,
        })

    if not out:
        raise ValueError(f"No usable static rows found in {path}")

    out.sort(key=lambda x: x["r_fm"])
    return out, cols


# ---------------------------------------------------------------------------
# Flux table support
# ---------------------------------------------------------------------------

@dataclass
class FluxColumns:
    r: str
    peak: Optional[str]
    width: Optional[str]
    area: Optional[str]
    component: Optional[str]


def detect_flux_columns(rows: Sequence[Dict[str, Any]]) -> FluxColumns:
    r_col = find_column(rows, [
        "r_fm", "d_fm", "separation_fm", "source_separation_fm", "distance_fm",
        "profile_separation_fm", "static_source_separation_fm"
    ])
    if r_col is None:
        raise ValueError("Could not detect flux separation column.")

    peak_col = find_column(rows, [
        "peak", "peak_Ex", "peak_ex", "peak_field", "peak_GeV2", "peak_Ex_GeV2",
        "max_Ex", "Ex_peak", "profile_peak"
    ])
    width_col = find_column(rows, [
        "width", "width_fm", "fwhm", "fwhm_fm", "FWHM_fm",
        "profile_width", "estimated_fwhm_fm"
    ])
    area_col = find_column(rows, [
        "area", "profile_area", "integral", "trapz_area", "area_GeV2_fm",
        "Ex_area", "field_area"
    ])
    component_col = find_column(rows, [
        "component", "profile_component", "field_component", "type"
    ])

    if peak_col is None and width_col is None and area_col is None:
        raise ValueError("Flux table found, but no peak/width/area columns were detected.")

    return FluxColumns(r=r_col, peak=peak_col, width=width_col, area=area_col, component=component_col)


def build_flux_lookup(path: Path, *, allow_extrapolation: bool = False) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if not path.exists():
        return None, f"Optional flux file not found: {path}"

    rows = read_csv_dicts(path)
    cols = detect_flux_columns(rows)

    raw: List[Dict[str, Any]] = []
    for row in rows:
        r = first_number(row, cols.r)
        if r is None:
            continue
        comp = str(row.get(cols.component, "")).strip().upper() if cols.component else ""
        # Keep only conventional trusted FULL/NP components if component field exists.
        if comp and comp not in {"FULL", "NP", "FULL/NP", "FULL_NP"}:
            continue

        raw.append({
            "r_fm": r,
            "component": comp or "UNSPECIFIED",
            "peak": first_number(row, cols.peak),
            "width": first_number(row, cols.width),
            "area": first_number(row, cols.area),
        })

    if not raw:
        return None, f"No usable flux rows found in {path}"

    # Normalize each observable over the raw trusted flux rows.
    for key in ("peak", "width", "area"):
        vals = [r[key] for r in raw]
        norms = minmax_norm(vals)
        for row, nval in zip(raw, norms):
            row[f"{key}_norm"] = nval

    for row in raw:
        row["C_flux_row"] = weighted_available(
            {
                "area": row.get("area_norm"),
                "peak": row.get("peak_norm"),
                "width": row.get("width_norm"),
            },
            {"area": 0.40, "peak": 0.30, "width": 0.30},
        )

    # Average rows that share the same separation after normalization.
    by_r: Dict[float, List[Dict[str, Any]]] = {}
    for row in raw:
        by_r.setdefault(row["r_fm"], []).append(row)

    points = []
    for r, group in sorted(by_r.items()):
        points.append({
            "r_fm": r,
            "C_flux": mean_available([g.get("C_flux_row") for g in group]),
            "n_flux_rows": len(group),
        })

    return {
        "points": points,
        "allow_extrapolation": allow_extrapolation,
        "columns": cols.__dict__,
    }, None


def interpolate_flux(flux_lookup: Optional[Dict[str, Any]], r: float) -> Tuple[Optional[float], str]:
    if not flux_lookup:
        return None, "NO_FLUX_TABLE"

    points = flux_lookup["points"]
    if not points:
        return None, "NO_FLUX_POINTS"

    xs = [p["r_fm"] for p in points]
    ys = [p["C_flux"] for p in points]

    # exact or near-exact match
    for x, y in zip(xs, ys):
        if abs(x - r) <= 1e-9:
            return y, "STATIC_PLUS_FLUX_MATCHED"

    # outside range
    if r < xs[0] or r > xs[-1]:
        if not flux_lookup.get("allow_extrapolation", False):
            return None, "STATIC_ONLY_FLUX_RANGE_MISMATCH"
        # linear extrapolation using nearest two points
        if len(xs) < 2:
            return None, "STATIC_ONLY_FLUX_SINGLE_POINT"
        if r < xs[0]:
            x0, x1, y0, y1 = xs[0], xs[1], ys[0], ys[1]
        else:
            x0, x1, y0, y1 = xs[-2], xs[-1], ys[-2], ys[-1]
        if y0 is None or y1 is None or x1 == x0:
            return None, "STATIC_ONLY_FLUX_EXTRAPOLATION_FAILED"
        return y0 + (r - x0) * (y1 - y0) / (x1 - x0), "STATIC_PLUS_FLUX_EXTRAPOLATED"

    # interpolation inside range
    for i in range(len(xs) - 1):
        if xs[i] <= r <= xs[i + 1]:
            x0, x1, y0, y1 = xs[i], xs[i + 1], ys[i], ys[i + 1]
            if y0 is None or y1 is None or x1 == x0:
                return None, "STATIC_ONLY_FLUX_INTERPOLATION_FAILED"
            return y0 + (r - x0) * (y1 - y0) / (x1 - x0), "STATIC_PLUS_FLUX_INTERPOLATED"

    return None, "STATIC_ONLY_FLUX_UNMATCHED"


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------

def compute_proxy(
    static_rows: List[Dict[str, Any]],
    *,
    flux_lookup: Optional[Dict[str, Any]],
    r_c: float,
    r_cs: float,
    weights: Dict[str, float],
) -> List[Dict[str, Any]]:
    xs = [r["r_fm"] for r in static_rows]
    d01 = [r["delta01_GeV"] for r in static_rows]
    d12 = [r["delta12_GeV"] for r in static_rows]

    # Gap compression: lower normalized gap = stronger compression.
    d01_norm = minmax_norm(d01)
    d12_norm = minmax_norm(d12)
    G01 = [None if v is None else 1.0 - v for v in d01_norm]
    G12 = [None if v is None else 1.0 - v for v in d12_norm]

    C_gap = [mean_available([a, b]) for a, b in zip(G01, G12)]

    # Threshold proximity.
    w_thr = max(abs(r_cs - r_c), median_positive_spacing(xs), 1e-9)
    C_threshold = []
    for r in xs:
        d_thr = min(abs(r - r_c), abs(r - r_cs))
        C_threshold.append(clip01(1.0 - d_thr / w_thr))

    # Slope / sharpening.
    s01, s01_notes = finite_difference(xs, d01)
    s12, s12_notes = finite_difference(xs, d12)
    s01_norm = minmax_norm(s01)
    s12_norm = minmax_norm(s12)
    C_slope = [mean_available([a, b]) for a, b in zip(s01_norm, s12_norm)]

    # Flux optional.
    C_flux = []
    flux_status = []
    for r in xs:
        fv, status = interpolate_flux(flux_lookup, r)
        C_flux.append(fv)
        flux_status.append(status)

    out: List[Dict[str, Any]] = []
    for i, base in enumerate(static_rows):
        components = {
            "gap": C_gap[i],
            "threshold": C_threshold[i],
            "slope": C_slope[i],
            "flux": C_flux[i],
        }
        pi = weighted_available(components, weights)

        available = [k for k, v in components.items() if v is not None and not math.isnan(v)]
        missing = [k for k, v in components.items() if v is None or (isinstance(v, float) and math.isnan(v))]

        notes = []
        if s01_notes[i]:
            notes.append(f"S01:{s01_notes[i]}")
        if s12_notes[i]:
            notes.append(f"S12:{s12_notes[i]}")
        if missing:
            notes.append("missing_components=" + "|".join(missing))

        out.append({
            "r_fm": base["r_fm"],
            "delta01_GeV": base["delta01_GeV"],
            "delta12_GeV": base["delta12_GeV"],
            "G01_compression": G01[i],
            "G12_compression": G12[i],
            "C_gap": C_gap[i],
            "C_threshold": C_threshold[i],
            "S01_abs_GeV_per_fm": s01[i],
            "S12_abs_GeV_per_fm": s12[i],
            "C_slope": C_slope[i],
            "C_flux": C_flux[i],
            "Pi_boundary_available": pi,
            "pressure_band": pressure_band(pi),
            "available_components": "|".join(available),
            "data_status": flux_status[i],
            "notes": "; ".join(notes),
        })

    return out


def build_metrics(
    table: List[Dict[str, Any]],
    *,
    static_path: Path,
    flux_path: Path,
    static_columns: StaticColumns,
    flux_warning: Optional[str],
    r_c: float,
    r_cs: float,
    weights: Dict[str, float],
) -> Dict[str, Any]:
    vals = [r["Pi_boundary_available"] for r in table if r["Pi_boundary_available"] is not None]
    max_row = max(table, key=lambda r: -1 if r["Pi_boundary_available"] is None else r["Pi_boundary_available"])

    band_counts: Dict[str, int] = {}
    for row in table:
        band_counts[row["pressure_band"]] = band_counts.get(row["pressure_band"], 0) + 1

    return {
        "script": "compute_boundary_pressure_proxy.py",
        "version": "0.1.0",
        "status": "computed_proxy_not_physical_law",
        "inputs": {
            "static": str(static_path),
            "flux": str(flux_path),
            "flux_warning": flux_warning,
            "static_columns": static_columns.__dict__,
        },
        "threshold_markers": {
            "r_c_fm": r_c,
            "r_cs_fm": r_cs,
        },
        "weights": weights,
        "rows": len(table),
        "pi_boundary": {
            "min": min(vals) if vals else None,
            "max": max(vals) if vals else None,
            "mean": sum(vals) / len(vals) if vals else None,
            "max_at_r_fm": max_row.get("r_fm"),
            "max_band": max_row.get("pressure_band"),
        },
        "pressure_band_counts": band_counts,
        "boundary": (
            "This is a structural diagnostic proxy derived from curated static gaps "
            "and optional trusted flux summaries. It is not a QCD potential and not "
            "a fitted universal confinement law."
        ),
    }


def write_ladder(path: Path, table: List[Dict[str, Any]], *, sort_values: bool = True) -> None:
    vals = [r["Pi_boundary_available"] for r in table if r["Pi_boundary_available"] is not None]
    if sort_values:
        vals = sorted(vals)

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["value"])
        for v in vals:
            writer.writerow([f"{v:.10g}"])


def write_schema(path: Path) -> None:
    rows = [
        {
            "field": "value",
            "meaning": "Pi_boundary_available(r), sorted as a single-column chamber ladder",
            "units": "dimensionless",
            "status": "derived_UNNS_boundary_pressure_proxy",
        }
    ]
    write_csv_dicts(path, rows, ["field", "meaning", "units", "status"])


def write_summary(path: Path, metrics: Dict[str, Any], table_path: Path, ladder_path: Path) -> None:
    pi = metrics["pi_boundary"]
    md = f"""# Boundary-Pressure Proxy Computation Summary

**Script:** compute_boundary_pressure_proxy.py  
**Version:** v0.1.0  
**Status:** computed structural diagnostic proxy, not a fitted physical law

## Inputs

```text
static: {metrics["inputs"]["static"]}
flux:   {metrics["inputs"]["flux"]}
```

Flux warning/status:

```text
{metrics["inputs"].get("flux_warning") or "none"}
```

## Outputs

```text
{table_path}
{ladder_path}
```

## Threshold markers

```text
r_c  = {metrics["threshold_markers"]["r_c_fm"]} fm
r_cs = {metrics["threshold_markers"]["r_cs_fm"]} fm
```

## Weights

```json
{json.dumps(metrics["weights"], indent=2)}
```

## Proxy range

```text
rows: {metrics["rows"]}
min Π_boundary_available: {pi["min"]}
max Π_boundary_available: {pi["max"]}
mean Π_boundary_available: {pi["mean"]}
max at r_fm: {pi["max_at_r_fm"]}
max band: {pi["max_band"]}
```

## Band counts

```json
{json.dumps(metrics["pressure_band_counts"], indent=2)}
```

## Boundary

This table is a structural UNNS diagnostic. It is not a QCD potential, not a
derivation of confinement, and not a universal fitted law.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(md, encoding="utf-8")


def parse_weights(args: argparse.Namespace) -> Dict[str, float]:
    weights = {
        "gap": args.w_gap,
        "threshold": args.w_threshold,
        "slope": args.w_slope,
        "flux": args.w_flux,
    }
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("Weight sum must be positive.")
    # Normalize so CLI overrides can be any positive scale.
    return {k: v / total for k, v in weights.items()}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compute UNNS color-confinement boundary-pressure proxy."
    )
    parser.add_argument("--root", default=".", help="Project root. Default: current directory.")
    parser.add_argument(
        "--static",
        default="reports/repair_threshold_window_static_gaps.csv",
        help="Static repair-window gap table.",
    )
    parser.add_argument(
        "--flux",
        default="reports/baker_flux_profile_trusted_summary.csv",
        help="Optional trusted flux summary table.",
    )
    parser.add_argument(
        "--output-table",
        default="reports/boundary_pressure_proxy_table.csv",
        help="Output proxy table CSV.",
    )
    parser.add_argument(
        "--output-ladder",
        default="chamber_inputs/boundary_pressure_proxy_ladder.csv",
        help="Output single-column chamber ladder CSV.",
    )
    parser.add_argument(
        "--output-schema",
        default="chamber_inputs/boundary_pressure_proxy_ladder_SCHEMA.csv",
        help="Output chamber ladder schema CSV.",
    )
    parser.add_argument(
        "--output-metrics",
        default="reports/boundary_pressure_proxy_metrics.json",
        help="Output metrics JSON.",
    )
    parser.add_argument(
        "--output-summary",
        default="reports/boundary_pressure_proxy_summary.md",
        help="Output short Markdown summary.",
    )
    parser.add_argument("--r-c", type=float, default=DEFAULT_R_C, help="Repair threshold r_c in fm.")
    parser.add_argument("--r-cs", type=float, default=DEFAULT_R_CS, help="Repair threshold r_cs in fm.")
    parser.add_argument("--w-gap", type=float, default=DEFAULT_WEIGHTS["gap"])
    parser.add_argument("--w-threshold", type=float, default=DEFAULT_WEIGHTS["threshold"])
    parser.add_argument("--w-slope", type=float, default=DEFAULT_WEIGHTS["slope"])
    parser.add_argument("--w-flux", type=float, default=DEFAULT_WEIGHTS["flux"])
    parser.add_argument(
        "--allow-flux-extrapolation",
        action="store_true",
        help="Allow flux C_flux extrapolation outside trusted flux separation range. Default: off.",
    )
    parser.add_argument(
        "--preserve-r-order-ladder",
        action="store_true",
        help="Write ladder in r order instead of sorted value order.",
    )

    args = parser.parse_args()

    root = Path(args.root).resolve()
    static_path = (root / args.static).resolve()
    flux_path = (root / args.flux).resolve()

    output_table = (root / args.output_table).resolve()
    output_ladder = (root / args.output_ladder).resolve()
    output_schema = (root / args.output_schema).resolve()
    output_metrics = (root / args.output_metrics).resolve()
    output_summary = (root / args.output_summary).resolve()

    weights = parse_weights(args)

    static_rows, static_cols = build_static_rows(static_path)
    flux_lookup, flux_warning = build_flux_lookup(
        flux_path,
        allow_extrapolation=args.allow_flux_extrapolation,
    )

    table = compute_proxy(
        static_rows,
        flux_lookup=flux_lookup,
        r_c=args.r_c,
        r_cs=args.r_cs,
        weights=weights,
    )

    fieldnames = [
        "r_fm",
        "delta01_GeV",
        "delta12_GeV",
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
        "notes",
    ]
    write_csv_dicts(output_table, table, fieldnames)
    write_ladder(output_ladder, table, sort_values=not args.preserve_r_order_ladder)
    write_schema(output_schema)

    metrics = build_metrics(
        table,
        static_path=static_path,
        flux_path=flux_path,
        static_columns=static_cols,
        flux_warning=flux_warning,
        r_c=args.r_c,
        r_cs=args.r_cs,
        weights=weights,
    )

    output_metrics.parent.mkdir(parents=True, exist_ok=True)
    output_metrics.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    write_summary(output_summary, metrics, output_table, output_ladder)

    print("BOUNDARY-PRESSURE PROXY COMPLETE")
    print(f"rows: {metrics['rows']}")
    print(f"table:   {output_table}")
    print(f"ladder:  {output_ladder}")
    print(f"schema:  {output_schema}")
    print(f"metrics: {output_metrics}")
    print(f"summary: {output_summary}")
    if flux_warning:
        print(f"flux: {flux_warning}")
    print("boundary: structural diagnostic proxy; not a QCD potential or fitted law")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

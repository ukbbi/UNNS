#!/usr/bin/env python3
"""
b_ladder_to_struc_perc_i.py

Compress a Phase B supernova light-curve ladder CSV into a compact
STRUC_PERC_I-ready canonical input.

Input:
  ladders/B_SN1987A_light_curve_ladder.csv

Output:
  struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv

Compression rule:
  one row per object × band × phase_name

Usage from B_supernova_light_curves/:
  python tools/b_ladder_to_struc_perc_i.py ladders/B_SN1987A_light_curve_ladder.csv struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv

Usage from B_supernova_light_curves/tools/:
  python b_ladder_to_struc_perc_i.py ../ladders/B_SN1987A_light_curve_ladder.csv ../struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv

Batch example from B_supernova_light_curves/:
  python tools/b_ladder_to_struc_perc_i.py --batch ladders struc_perc_i/canonical_inputs struc_perc_i/summaries/B_STRUC_PERC_I_SUMMARY.csv
"""

import csv
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path


PHASE_ORDER = {
    "pre_discovery_or_baseline": 0,
    "rise": 1,
    "peak": 2,
    "early_decline": 3,
    "plateau_or_shoulder": 4,
    "break": 5,
    "tail_decay": 6,
    "late_relaxation": 7,
    "unclassified": 8,
}


OUTPUT_COLUMNS = [
    "struc_perc_id",
    "source_ladder_id",
    "object_name",
    "supernova_type",
    "band",
    "phase_name",
    "stage_index",
    "n_points",
    "time_start_mjd",
    "time_end_mjd",
    "duration_days",
    "time_mid_mjd",
    "mag_start",
    "mag_end",
    "mag_min",
    "mag_max",
    "mag_mean",
    "mag_median",
    "mag_range",
    "mean_slope",
    "median_slope",
    "mean_curvature",
    "median_curvature",
    "transition_marker",
    "boundary_role",
    "support_regime_proxy",
    "struc_perc_role",
    "gap",
    "gap_source",
    "alpha_ready",
    "unns_interpretation",
    "raw_reference",
]


SUMMARY_COLUMNS = [
    "input_file",
    "output_file",
    "object_name",
    "rows_in",
    "rows_out",
    "bands",
    "phases",
    "time_min_mjd",
    "time_max_mjd",
    "status",
]


def to_float(value):
    if value is None:
        return None
    text = str(value).strip()
    if text == "":
        return None
    try:
        x = float(text)
    except ValueError:
        return None
    if math.isnan(x) or math.isinf(x):
        return None
    return x


def fmt(value):
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10g}"
    return str(value)


def mean(values):
    values = [v for v in values if v is not None]
    return statistics.fmean(values) if values else None


def median(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


def read_ladder(input_csv):
    with Path(input_csv).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def compress_ladder(input_csv, output_csv):
    input_csv = Path(input_csv)
    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    rows = read_ladder(input_csv)
    if not rows:
        raise ValueError(f"No rows found in {input_csv}")

    groups = defaultdict(list)
    for row in rows:
        key = (
            row.get("object_name", "").strip(),
            row.get("band", "").strip(),
            row.get("phase_name", "").strip(),
        )
        groups[key].append(row)

    compressed = []
    for (object_name, band, phase_name), items in groups.items():
        items = sorted(items, key=lambda r: to_float(r.get("time_mjd")) or 0.0)

        times = [to_float(r.get("time_mjd")) for r in items]
        mags = [to_float(r.get("brightness_value")) for r in items]
        slopes = [to_float(r.get("slope_local")) for r in items]
        curvs = [to_float(r.get("curvature_local")) for r in items]

        valid_times = [t for t in times if t is not None]
        valid_mags = [m for m in mags if m is not None]

        t0 = min(valid_times) if valid_times else None
        t1 = max(valid_times) if valid_times else None
        duration = (t1 - t0) if t0 is not None and t1 is not None else None
        tmid = ((t0 + t1) / 2.0) if t0 is not None and t1 is not None else None

        first = items[0]
        last = items[-1]

        mag_start = to_float(first.get("brightness_value"))
        mag_end = to_float(last.get("brightness_value"))
        mag_min = min(valid_mags) if valid_mags else None
        mag_max = max(valid_mags) if valid_mags else None
        mag_range = (mag_max - mag_min) if mag_min is not None and mag_max is not None else None

        # In magnitude units, lower magnitude means brighter. Use magnitude range as
        # the first STRUC_PERC_I gap proxy because it captures phase-local excursion.
        gap = mag_range
        gap_source = "phase_local_magnitude_range"

        stage_index = first.get("stage_index", "")
        if not stage_index:
            stage_index = PHASE_ORDER.get(phase_name, 8)

        source_ladder_id = first.get("ladder_id", "")
        struc_perc_id = f"{source_ladder_id}_{phase_name}".replace(" ", "")

        compressed.append({
            "struc_perc_id": struc_perc_id,
            "source_ladder_id": source_ladder_id,
            "object_name": object_name,
            "supernova_type": first.get("supernova_type", ""),
            "band": band,
            "phase_name": phase_name,
            "stage_index": stage_index,
            "n_points": len(items),
            "time_start_mjd": fmt(t0),
            "time_end_mjd": fmt(t1),
            "duration_days": fmt(duration),
            "time_mid_mjd": fmt(tmid),
            "mag_start": fmt(mag_start),
            "mag_end": fmt(mag_end),
            "mag_min": fmt(mag_min),
            "mag_max": fmt(mag_max),
            "mag_mean": fmt(mean(mags)),
            "mag_median": fmt(median(mags)),
            "mag_range": fmt(mag_range),
            "mean_slope": fmt(mean(slopes)),
            "median_slope": fmt(median(slopes)),
            "mean_curvature": fmt(mean(curvs)),
            "median_curvature": fmt(median(curvs)),
            "transition_marker": first.get("transition_marker", ""),
            "boundary_role": first.get("boundary_role", ""),
            "support_regime_proxy": first.get("support_regime_proxy", ""),
            "struc_perc_role": first.get("struc_perc_role", ""),
            "gap": fmt(gap),
            "gap_source": gap_source,
            "alpha_ready": "yes" if len(items) >= 2 and gap is not None else "partial",
            "unns_interpretation": (
                "compact object-band-phase observable boundary-response state "
                "derived from Phase B light-curve ladder"
            ),
            "raw_reference": first.get("raw_reference", ""),
        })

    compressed.sort(
        key=lambda r: (
            r["object_name"],
            r["band"],
            int(r["stage_index"]) if str(r["stage_index"]).isdigit() else PHASE_ORDER.get(r["phase_name"], 8),
            r["phase_name"],
        )
    )

    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(compressed)

    all_times = [to_float(r.get("time_mjd")) for r in rows]
    all_times = [t for t in all_times if t is not None]
    object_names = sorted({r.get("object_name", "") for r in rows if r.get("object_name")})
    bands = sorted({r.get("band", "") for r in rows if r.get("band")})
    phases = sorted({r.get("phase_name", "") for r in rows if r.get("phase_name")}, key=lambda p: PHASE_ORDER.get(p, 99))

    summary = {
        "input_file": str(input_csv),
        "output_file": str(output_csv),
        "object_name": ";".join(object_names),
        "rows_in": len(rows),
        "rows_out": len(compressed),
        "bands": ";".join(bands),
        "phases": ";".join(phases),
        "time_min_mjd": fmt(min(all_times) if all_times else None),
        "time_max_mjd": fmt(max(all_times) if all_times else None),
        "status": "converted",
    }

    return summary


def output_name_for(input_path):
    name = Path(input_path).name
    if name.endswith("_light_curve_ladder.csv"):
        return name.replace("_light_curve_ladder.csv", "_struc_perc_input.csv")
    return Path(input_path).stem + "_struc_perc_input.csv"


def batch_convert(ladders_dir, output_dir, summary_csv):
    ladders_dir = Path(ladders_dir)
    output_dir = Path(output_dir)
    summary_csv = Path(summary_csv)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_csv.parent.mkdir(parents=True, exist_ok=True)

    input_files = sorted(ladders_dir.glob("B_*_light_curve_ladder.csv"))
    if not input_files:
        raise FileNotFoundError(f"No B_*_light_curve_ladder.csv files found in {ladders_dir}")

    summaries = []
    for input_file in input_files:
        output_file = output_dir / output_name_for(input_file)
        summary = compress_ladder(input_file, output_file)
        summaries.append(summary)
        print(f"Converted: {input_file} -> {output_file}")
        print(f"  rows_in={summary['rows_in']} rows_out={summary['rows_out']} bands={summary['bands']}")

    with summary_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        writer.writerows(summaries)

    print(f"Summary written: {summary_csv}")


def main(argv):
    if len(argv) == 5 and argv[1] == "--batch":
        _, _, ladders_dir, output_dir, summary_csv = argv
        batch_convert(ladders_dir, output_dir, summary_csv)
        return 0

    if len(argv) != 3:
        print(__doc__)
        return 1

    input_csv, output_csv = argv[1], argv[2]
    summary = compress_ladder(input_csv, output_csv)
    print(f"Object: {summary['object_name']}")
    print(f"Rows in: {summary['rows_in']}")
    print(f"Rows out: {summary['rows_out']}")
    print(f"Bands: {summary['bands']}")
    print(f"Phases: {summary['phases']}")
    print(f"Output: {summary['output_file']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

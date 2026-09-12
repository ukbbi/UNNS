#!/usr/bin/env python3
"""
b_struc_input_to_numeric_ladders.py

Convert Phase B STRUC_PERC_I canonical-input CSV files into plain numeric
ladder .txt files suitable for STRUC-PERC-I v2.5.0 batch mode.

Input:
  struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv

Output:
  struc_perc_i/numeric_ladders/B_SN1987A_numeric_ladder.txt

Core rule:
  Use the canonical input "gap" column as the phase-local structural gap.
  Convert gaps into a monotone cumulative ladder:

    x0 = 0
    x1 = gap1
    x2 = gap1 + gap2
    ...

Why:
  STRUC-PERC-I expects a plain ordered numeric ladder x1 <= x2 <= ... <= xn.
  It does not understand the multi-column Phase B schema directly.

Usage from B_supernova_light_curves/:
  python tools/b_struc_input_to_numeric_ladders.py struc_perc_i/canonical_inputs/B_SN1987A_struc_perc_input.csv struc_perc_i/numeric_ladders/B_SN1987A_numeric_ladder.txt

Batch usage from B_supernova_light_curves/:
  python tools/b_struc_input_to_numeric_ladders.py --batch struc_perc_i/canonical_inputs struc_perc_i/numeric_ladders struc_perc_i/summaries/B_NUMERIC_LADDER_SUMMARY.csv
"""

import csv
import math
import sys
from pathlib import Path


SUMMARY_COLUMNS = [
    "input_file",
    "output_file",
    "object_name",
    "rows_in",
    "numeric_points_out",
    "gap_source",
    "gap_min",
    "gap_max",
    "gap_sum",
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


def read_csv(path):
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def sort_key(row):
    object_name = row.get("object_name", "")
    band = row.get("band", "")
    try:
        stage_index = int(float(row.get("stage_index", 999)))
    except ValueError:
        stage_index = 999
    phase = row.get("phase_name", "")
    try:
        tmid = float(row.get("time_mid_mjd", 0))
    except ValueError:
        tmid = 0
    return (object_name, band, stage_index, phase, tmid)


def extract_gaps(rows):
    """
    Use the canonical 'gap' column first.
    Fallback to 'mag_range' only if gap is missing.

    Zero or negative values are not useful as ladder increments for this first
    STRUC-PERC-I run, so they are skipped.
    """
    gaps = []
    gap_source = "gap"
    for row in sorted(rows, key=sort_key):
        value = to_float(row.get("gap"))
        if value is None:
            value = to_float(row.get("mag_range"))
            gap_source = "mag_range_fallback"
        if value is None:
            continue
        value = abs(value)
        if value <= 0:
            continue
        gaps.append(value)
    return gaps, gap_source


def gaps_to_cumulative_ladder(gaps):
    ladder = [0.0]
    total = 0.0
    for g in gaps:
        total += g
        ladder.append(total)

    # STRUC-PERC-I requires at least 3 numeric values.
    # If there are fewer than two valid gaps, return whatever exists and flag later.
    return ladder


def object_name_from_rows(rows, input_file):
    for row in rows:
        name = row.get("object_name", "").strip()
        if name:
            return name.replace(" ", "")
    stem = Path(input_file).stem
    return stem.replace("_struc_perc_input", "")


def write_ladder_txt(ladder, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for x in ladder:
            f.write(f"{x:.10g}\n")


def convert_one(input_csv, output_txt):
    input_csv = Path(input_csv)
    output_txt = Path(output_txt)

    rows = read_csv(input_csv)
    if not rows:
        raise ValueError(f"No rows found in {input_csv}")

    gaps, gap_source = extract_gaps(rows)
    ladder = gaps_to_cumulative_ladder(gaps)

    status = "converted" if len(ladder) >= 3 else "too_few_points"
    write_ladder_txt(ladder, output_txt)

    object_name = object_name_from_rows(rows, input_csv)

    return {
        "input_file": str(input_csv),
        "output_file": str(output_txt),
        "object_name": object_name,
        "rows_in": len(rows),
        "numeric_points_out": len(ladder),
        "gap_source": gap_source,
        "gap_min": min(gaps) if gaps else "",
        "gap_max": max(gaps) if gaps else "",
        "gap_sum": sum(gaps) if gaps else "",
        "status": status,
    }


def output_name_for(input_path):
    name = Path(input_path).name
    if name.endswith("_struc_perc_input.csv"):
        return name.replace("_struc_perc_input.csv", "_numeric_ladder.txt")
    return Path(input_path).stem + "_numeric_ladder.txt"


def batch_convert(input_dir, output_dir, summary_csv):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    summary_csv = Path(summary_csv)

    output_dir.mkdir(parents=True, exist_ok=True)
    summary_csv.parent.mkdir(parents=True, exist_ok=True)

    input_files = sorted(input_dir.glob("B_*_struc_perc_input.csv"))
    if not input_files:
        raise FileNotFoundError(f"No B_*_struc_perc_input.csv files found in {input_dir}")

    summaries = []
    for input_file in input_files:
        output_file = output_dir / output_name_for(input_file)
        summary = convert_one(input_file, output_file)
        summaries.append(summary)
        print(f"Converted: {input_file} -> {output_file}")
        print(f"  rows_in={summary['rows_in']} numeric_points_out={summary['numeric_points_out']} status={summary['status']}")

    with summary_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        writer.writerows(summaries)

    print(f"Summary written: {summary_csv}")


def main(argv):
    if len(argv) == 5 and argv[1] == "--batch":
        _, _, input_dir, output_dir, summary_csv = argv
        batch_convert(input_dir, output_dir, summary_csv)
        return 0

    if len(argv) != 3:
        print(__doc__)
        return 1

    input_csv, output_txt = argv[1], argv[2]
    summary = convert_one(input_csv, output_txt)
    print(f"Object: {summary['object_name']}")
    print(f"Rows in: {summary['rows_in']}")
    print(f"Numeric points out: {summary['numeric_points_out']}")
    print(f"Gap source: {summary['gap_source']}")
    print(f"Output: {summary['output_file']}")
    print(f"Status: {summary['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

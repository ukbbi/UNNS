#!/usr/bin/env python3
"""
c_spectra_to_line_ladder.py

STELLAR_BOUNDARY_DYNAMICS_I
Phase C — WISeREP spectra to spectral line ladders.

Reads raw WISeREP spectra folders plus wiserep_spectra.csv metadata and writes:

  ladders/C1_SN1993J_spectral_line_ladder.csv
  ladders/C2_SN2012aw_spectral_line_ladder.csv
  summaries/C_SPECTRAL_LINE_LADDER_SUMMARY.csv

Expected input layout:

  raw/
    C1_SN1993J/
      wiserep_spectra.csv
      SOURCE_SN1993J_WISeREP.txt
      *.dat / *.flm / *.txt / *.ascii

    C2_SN2012aw/
      wiserep_spectra.csv
      SOURCE_SN2012aw_WISeREP.txt
      *.dat / *.flm / *.txt / *.ascii

Usage from C_spectral_time_series/:

  python tools/c_spectra_to_line_ladder.py --batch raw ladders summaries/C_SPECTRAL_LINE_LADDER_SUMMARY.csv

Single object:

  python tools/c_spectra_to_line_ladder.py raw/C1_SN1993J ladders/C1_SN1993J_spectral_line_ladder.csv

Notes:
  - This script extracts structural line-window proxies, not elemental abundances.
  - It accepts ASCII-like spectra with at least two numeric columns:
      wavelength flux
  - It skips source notes, metadata CSVs, and non-spectrum text files.
"""

import argparse
import csv
import math
import statistics
import sys
from pathlib import Path


SPECTRUM_EXTENSIONS = {".dat", ".flm", ".txt", ".ascii", ".asc"}

# Rest-frame line windows. Widths are intentionally broad because WISeREP data
# are heterogeneous and early SN lines are broad/velocity-shifted.
LINE_DEFINITIONS = [
    {
        "line_id": "H_alpha",
        "line_name": "H alpha",
        "element_group": "H",
        "rest_wavelength": 6562.8,
        "window_half_width": 180.0,
        "continuum_inner": 220.0,
        "continuum_outer": 420.0,
    },
    {
        "line_id": "H_beta",
        "line_name": "H beta",
        "element_group": "H",
        "rest_wavelength": 4861.3,
        "window_half_width": 140.0,
        "continuum_inner": 180.0,
        "continuum_outer": 360.0,
    },
    {
        "line_id": "He_I_5876",
        "line_name": "He I 5876",
        "element_group": "He",
        "rest_wavelength": 5875.6,
        "window_half_width": 160.0,
        "continuum_inner": 200.0,
        "continuum_outer": 400.0,
    },
    {
        "line_id": "O_I_7774",
        "line_name": "O I 7774",
        "element_group": "O",
        "rest_wavelength": 7774.0,
        "window_half_width": 180.0,
        "continuum_inner": 220.0,
        "continuum_outer": 450.0,
    },
    {
        "line_id": "Ca_II_NIR",
        "line_name": "Ca II near-infrared triplet",
        "element_group": "Ca",
        "rest_wavelength": 8579.0,
        "window_half_width": 360.0,
        "continuum_inner": 420.0,
        "continuum_outer": 760.0,
    },
    {
        "line_id": "Si_II_6355",
        "line_name": "Si II 6355",
        "element_group": "Si",
        "rest_wavelength": 6355.0,
        "window_half_width": 160.0,
        "continuum_inner": 200.0,
        "continuum_outer": 420.0,
    },
    {
        "line_id": "Fe_II_5169",
        "line_name": "Fe II 5169",
        "element_group": "Fe",
        "rest_wavelength": 5169.0,
        "window_half_width": 180.0,
        "continuum_inner": 220.0,
        "continuum_outer": 440.0,
    },
    {
        "line_id": "Ni_Co_decay_proxy",
        "line_name": "Ni/Co decay proxy blend",
        "element_group": "NiCo",
        "rest_wavelength": 5890.0,
        "window_half_width": 260.0,
        "continuum_inner": 320.0,
        "continuum_outer": 650.0,
    },
]

OUTPUT_COLUMNS = [
    "object_id",
    "object_name",
    "spectrum_id",
    "spectrum_file",
    "spectrum_date",
    "phase_days",
    "redshift",
    "instrument",
    "source_archive",
    "line_id",
    "line_name",
    "element_group",
    "rest_wavelength",
    "observed_center_wavelength",
    "window_min",
    "window_max",
    "n_points_total",
    "n_points_window",
    "wavelength_min",
    "wavelength_max",
    "continuum_level",
    "line_flux_proxy",
    "line_depth_proxy",
    "equivalent_width_proxy",
    "velocity_proxy_km_s",
    "width_proxy_angstrom",
    "signal_quality_proxy",
    "spectral_phase_role",
    "alpha_ready",
    "raw_reference",
]

SUMMARY_COLUMNS = [
    "object_id",
    "object_name",
    "raw_folder",
    "output_file",
    "metadata_rows",
    "spectrum_files_found",
    "spectrum_files_parsed",
    "spectra_with_metadata",
    "ladder_rows_written",
    "date_min",
    "date_max",
    "phase_min",
    "phase_max",
    "status",
]


def to_float(value, default=0.0):
    try:
        if value is None or str(value).strip() == "":
            return default
        x = float(str(value).strip())
        if math.isnan(x) or math.isinf(x):
            return default
        return x
    except Exception:
        return default


def fmt(value):
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def clean_key(key):
    return (key or "").strip().lower().replace(" ", "_").replace("-", "_")


def read_metadata(folder):
    """
    Reads WISeREP metadata CSV when present and builds lookup by filename-like
    fields plus a row list for fallback matching.

    WISeREP metadata column names vary; this function keeps original row fields
    and also creates normalized lookup helpers.
    """
    meta_path = Path(folder) / "wiserep_spectra.csv"
    if not meta_path.exists():
        return [], {}

    with meta_path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        rows = list(csv.DictReader(f))

    lookup = {}
    for row in rows:
        values = list(row.values())
        for value in values:
            if not value:
                continue
            value = str(value).strip()
            if value:
                lookup[value] = row
                lookup[Path(value).name] = row

    return rows, lookup


def metadata_value(row, candidates, default=""):
    if not row:
        return default

    # exact original key
    for c in candidates:
        if c in row and row[c] not in (None, ""):
            return row[c]

    # normalized key comparison
    normalized = {clean_key(k): v for k, v in row.items()}
    for c in candidates:
        key = clean_key(c)
        if key in normalized and normalized[key] not in (None, ""):
            return normalized[key]

    return default


def parse_date_like(value):
    text = str(value or "").strip()
    return text


def parse_phase(value):
    # Supports numeric, +12.3, -4.1, "12.3 d", etc.
    text = str(value or "").strip()
    if not text:
        return ""
    token = ""
    for ch in text:
        if ch.isdigit() or ch in ".-+eE":
            token += ch
        elif token:
            break
    try:
        return fmt(float(token))
    except Exception:
        return ""


def parse_ascii_spectrum(path):
    """
    Parse ASCII-like spectra with at least two numeric columns.
    Lines may contain comments or headers; non-numeric rows are skipped.
    """
    wl = []
    flux = []
    with Path(path).open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(("#", "%", ";", "@", "\\")):
                continue
            parts = stripped.replace(",", " ").split()
            if len(parts) < 2:
                continue
            try:
                w = float(parts[0])
                y = float(parts[1])
            except Exception:
                continue
            if math.isfinite(w) and math.isfinite(y):
                wl.append(w)
                flux.append(y)

    if len(wl) < 10:
        raise ValueError(f"Too few numeric wavelength/flux rows: {path}")

    # Sort by wavelength in case file is unordered.
    pairs = sorted(zip(wl, flux), key=lambda p: p[0])
    return [p[0] for p in pairs], [p[1] for p in pairs]


def median(values):
    values = [v for v in values if math.isfinite(v)]
    if not values:
        return 0.0
    return statistics.median(values)


def mean(values):
    values = [v for v in values if math.isfinite(v)]
    if not values:
        return 0.0
    return statistics.fmean(values)


def robust_std(values):
    values = [v for v in values if math.isfinite(v)]
    if len(values) < 2:
        return 0.0
    return statistics.pstdev(values)


def line_window_proxy(wavelengths, fluxes, line_def, redshift):
    rest = line_def["rest_wavelength"]
    center = rest * (1.0 + redshift)
    hw = line_def["window_half_width"]
    inner = line_def["continuum_inner"]
    outer = line_def["continuum_outer"]

    wmin = center - hw
    wmax = center + hw

    line_pairs = [(w, f) for w, f in zip(wavelengths, fluxes) if wmin <= w <= wmax]
    cont_pairs = [
        (w, f)
        for w, f in zip(wavelengths, fluxes)
        if (center - outer <= w <= center - inner) or (center + inner <= w <= center + outer)
    ]

    if not line_pairs:
        return None

    line_w = [p[0] for p in line_pairs]
    line_f = [p[1] for p in line_pairs]
    cont_f = [p[1] for p in cont_pairs]

    continuum = median(cont_f) if cont_f else median(fluxes)

    # Emission/absorption agnostic proxies.
    mean_line = mean(line_f)
    min_line = min(line_f)
    max_line = max(line_f)

    line_flux_proxy = sum((f - continuum) for f in line_f) / max(1, len(line_f))
    line_depth_proxy = (continuum - min_line) / (abs(continuum) + 1e-12)

    # Equivalent width proxy using median spacing.
    if len(line_w) > 1:
        spacing = median([abs(b - a) for a, b in zip(line_w, line_w[1:])])
    else:
        spacing = 0.0
    ew_proxy = sum((1.0 - (f / (continuum + 1e-12))) for f in line_f) * spacing

    # Peak/depth location: whichever deviates more from continuum.
    min_dev = abs(min_line - continuum)
    max_dev = abs(max_line - continuum)
    if max_dev > min_dev:
        feature_flux = max_line
        feature_w = line_w[line_f.index(max_line)]
    else:
        feature_flux = min_line
        feature_w = line_w[line_f.index(min_line)]

    c_km_s = 299792.458
    velocity_proxy = ((feature_w / center) - 1.0) * c_km_s

    # Width proxy: weighted RMS around feature center by absolute deviation.
    weights = [abs(f - continuum) for f in line_f]
    sw = sum(weights)
    if sw > 0:
        mu = sum(w * weight for w, weight in zip(line_w, weights)) / sw
        width = math.sqrt(sum(weight * (w - mu) ** 2 for w, weight in zip(line_w, weights)) / sw)
    else:
        width = max(line_w) - min(line_w)

    signal_quality = abs(line_flux_proxy) / (robust_std(cont_f) + 1e-12) if cont_f else 0.0

    return {
        "observed_center_wavelength": center,
        "window_min": wmin,
        "window_max": wmax,
        "n_points_window": len(line_pairs),
        "continuum_level": continuum,
        "line_flux_proxy": line_flux_proxy,
        "line_depth_proxy": line_depth_proxy,
        "equivalent_width_proxy": ew_proxy,
        "velocity_proxy_km_s": velocity_proxy,
        "width_proxy_angstrom": width,
        "signal_quality_proxy": signal_quality,
    }


def spectral_phase_role(phase_days):
    p = to_float(phase_days, default=None)
    if p is None:
        return "unknown_phase"
    if p < -5:
        return "early_pre_peak"
    if p <= 10:
        return "near_peak"
    if p <= 60:
        return "early_decline"
    if p <= 180:
        return "late_decline"
    return "nebular_late"


def object_from_folder(folder):
    name = Path(folder).name
    if "SN1993J" in name:
        return "C1_SN1993J", "SN1993J"
    if "SN2012aw" in name:
        return "C2_SN2012aw", "SN2012aw"
    return name, name.replace("C_", "")


def spectrum_files(folder):
    files = []
    for path in Path(folder).iterdir():
        if not path.is_file():
            continue
        name_upper = path.name.upper()
        if name_upper.startswith("SOURCE_"):
            continue
        if path.name == "wiserep_spectra.csv":
            continue
        if path.suffix.lower() in SPECTRUM_EXTENSIONS:
            files.append(path)
    return sorted(files)


def find_metadata_for_file(path, meta_rows, lookup):
    name = Path(path).name

    if name in lookup:
        return lookup[name]

    # Try substring match against any metadata field.
    for row in meta_rows:
        row_text = " ".join(str(v) for v in row.values() if v)
        if name in row_text:
            return row

        stem = Path(name).stem
        if stem and stem in row_text:
            return row

    return {}


def convert_object(raw_folder, output_csv):
    raw_folder = Path(raw_folder)
    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    object_id, object_name = object_from_folder(raw_folder)

    meta_rows, meta_lookup = read_metadata(raw_folder)
    files = spectrum_files(raw_folder)

    ladder_rows = []
    parsed_count = 0
    with_meta_count = 0
    dates = []
    phases = []

    for spec_path in files:
        try:
            wavelengths, fluxes = parse_ascii_spectrum(spec_path)
        except Exception:
            continue

        parsed_count += 1
        meta = find_metadata_for_file(spec_path, meta_rows, meta_lookup)
        if meta:
            with_meta_count += 1

        date = parse_date_like(metadata_value(meta, ["Obs-date", "Obs Date", "Date", "obsdate", "time"], ""))
        phase = parse_phase(metadata_value(meta, ["Phase", "phase", "Rest-frame phase", "Phase (days)"], ""))
        redshift = to_float(metadata_value(meta, ["Redshift", "z", "redshift"], "0"), 0.0)
        instrument = metadata_value(meta, ["Instrument", "Telescope/Instrument", "Instr", "Source"], "")
        source_archive = "WISeREP"

        if date:
            dates.append(date)
        if phase != "":
            phases.append(to_float(phase))

        w_min = min(wavelengths)
        w_max = max(wavelengths)
        spec_id = Path(spec_path).stem

        for line_def in LINE_DEFINITIONS:
            proxy = line_window_proxy(wavelengths, fluxes, line_def, redshift)
            if proxy is None:
                continue

            ladder_rows.append({
                "object_id": object_id,
                "object_name": object_name,
                "spectrum_id": spec_id,
                "spectrum_file": spec_path.name,
                "spectrum_date": date,
                "phase_days": phase,
                "redshift": fmt(redshift),
                "instrument": instrument,
                "source_archive": source_archive,
                "line_id": line_def["line_id"],
                "line_name": line_def["line_name"],
                "element_group": line_def["element_group"],
                "rest_wavelength": fmt(line_def["rest_wavelength"]),
                "observed_center_wavelength": fmt(proxy["observed_center_wavelength"]),
                "window_min": fmt(proxy["window_min"]),
                "window_max": fmt(proxy["window_max"]),
                "n_points_total": len(wavelengths),
                "n_points_window": proxy["n_points_window"],
                "wavelength_min": fmt(w_min),
                "wavelength_max": fmt(w_max),
                "continuum_level": fmt(proxy["continuum_level"]),
                "line_flux_proxy": fmt(proxy["line_flux_proxy"]),
                "line_depth_proxy": fmt(proxy["line_depth_proxy"]),
                "equivalent_width_proxy": fmt(proxy["equivalent_width_proxy"]),
                "velocity_proxy_km_s": fmt(proxy["velocity_proxy_km_s"]),
                "width_proxy_angstrom": fmt(proxy["width_proxy_angstrom"]),
                "signal_quality_proxy": fmt(proxy["signal_quality_proxy"]),
                "spectral_phase_role": spectral_phase_role(phase),
                "alpha_ready": "yes" if proxy["n_points_window"] >= 3 else "partial",
                "raw_reference": f"{raw_folder.name}/{spec_path.name}::{line_def['line_id']}",
            })

    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(ladder_rows)

    summary = {
        "object_id": object_id,
        "object_name": object_name,
        "raw_folder": str(raw_folder),
        "output_file": str(output_csv),
        "metadata_rows": len(meta_rows),
        "spectrum_files_found": len(files),
        "spectrum_files_parsed": parsed_count,
        "spectra_with_metadata": with_meta_count,
        "ladder_rows_written": len(ladder_rows),
        "date_min": min(dates) if dates else "",
        "date_max": max(dates) if dates else "",
        "phase_min": fmt(min(phases)) if phases else "",
        "phase_max": fmt(max(phases)) if phases else "",
        "status": "converted" if ladder_rows else "no_ladder_rows",
    }

    print(f"Converted: {raw_folder}")
    print(f"  spectra found: {len(files)}")
    print(f"  spectra parsed: {parsed_count}")
    print(f"  ladder rows: {len(ladder_rows)}")
    print(f"  output: {output_csv}")

    return summary


def write_csv(path, rows, columns):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def output_name(raw_folder):
    object_id, _ = object_from_folder(raw_folder)
    return f"{object_id}_spectral_line_ladder.csv"


def batch_convert(raw_root, ladders_dir, summary_csv):
    raw_root = Path(raw_root)
    ladders_dir = Path(ladders_dir)

    targets = []
    for folder in sorted(raw_root.iterdir()):
        if folder.is_dir() and folder.name.startswith("C"):
            targets.append(folder)

    if not targets:
        raise FileNotFoundError(f"No C* raw object folders found in {raw_root}")

    summaries = []
    for folder in targets:
        out = ladders_dir / output_name(folder)
        summaries.append(convert_object(folder, out))

    write_csv(summary_csv, summaries, SUMMARY_COLUMNS)
    print(f"Summary written: {summary_csv}")


def main():
    parser = argparse.ArgumentParser(description="Convert WISeREP raw spectra into Phase C spectral line ladders.")
    parser.add_argument("paths", nargs="*", help="Batch: raw_root ladders_dir summary_csv. Single: raw_folder output_csv.")
    parser.add_argument("--batch", action="store_true")
    args = parser.parse_args()

    if args.batch:
        if len(args.paths) != 3:
            raise SystemExit("Batch usage: python tools/c_spectra_to_line_ladder.py --batch raw ladders summaries/C_SPECTRAL_LINE_LADDER_SUMMARY.csv")
        batch_convert(args.paths[0], args.paths[1], args.paths[2])
        return

    if len(args.paths) != 2:
        raise SystemExit(__doc__)

    convert_object(args.paths[0], args.paths[1])


if __name__ == "__main__":
    main()

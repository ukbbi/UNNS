#!/usr/bin/env python3
"""
osc_to_b_ladder.py

Convert an Open Supernova Catalog / AstroCats object JSON file into the
Phase B STRUC_PERC_I-compatible light-curve ladder schema.

Usage:
  python osc_to_b_ladder.py SN1987A_OSC_raw.json B_SN1987A_light_curve_ladder.csv
  python osc_to_b_ladder.py SN1993J_OSC_raw.json B_SN1993J_light_curve_ladder.csv
"""

import json
import csv
import sys
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

SCHEMA_COLUMNS = [
    "ladder_id", "source_id", "source_name", "object_name", "alias_names",
    "supernova_type", "classification_source", "ra_deg", "dec_deg",
    "redshift", "host_galaxy", "band", "stage_index", "phase_name",
    "time_mjd", "time_since_discovery_days", "time_since_peak_days",
    "brightness_value", "brightness_unit", "brightness_error", "detection_flag",
    "quality_flag", "slope_local", "curvature_local", "transition_marker",
    "boundary_role", "support_regime_proxy", "struc_perc_role",
    "unns_interpretation", "raw_reference"
]

def date_to_mjd(date_text):
    if not date_text:
        return None
    date_text = date_text.replace("-", "/")
    dt = datetime.strptime(date_text, "%Y/%m/%d").replace(tzinfo=timezone.utc)
    return dt.timestamp() / 86400.0 + 40587.0

def safe_first(records, key="value", default=""):
    if isinstance(records, list) and records:
        return str(records[0].get(key, default))
    return default

def phase_from_time_since_peak(dt):
    if dt is None:
        return (8, "unclassified", "unknown", "observable_ladder_state")
    if dt < -5:
        return (1, "rise", "boundary_response_rise", "observable_ladder_state")
    if -5 <= dt <= 5:
        return (2, "peak", "maximum_observable_response", "transition_state")
    if 5 < dt <= 40:
        return (3, "early_decline", "post_boundary_relaxation", "relaxation_state")
    if 40 < dt <= 120:
        return (4, "plateau_or_shoulder", "plateau_or_buffer_regime", "relaxation_state")
    if 120 < dt <= 220:
        return (5, "break", "transition_break", "transition_state")
    if 220 < dt <= 600:
        return (6, "tail_decay", "tail_decay", "relaxation_state")
    return (7, "late_relaxation", "late_basin_relaxation", "relaxation_state")

def transition_marker_from_phase(phase):
    return {
        "rise": "rise_onset",
        "peak": "peak",
        "early_decline": "decline_onset",
        "plateau_or_shoulder": "plateau_onset",
        "break": "break",
        "tail_decay": "tail_onset",
        "late_relaxation": "late_relaxation",
        "unclassified": "ambiguous",
    }.get(phase, "none")

def support_proxy_from_phase(phase):
    return {
        "rise": "shock_cooling",
        "peak": "ejecta_cooling",
        "early_decline": "ejecta_cooling",
        "plateau_or_shoulder": "recombination_plateau",
        "break": "ambiguous",
        "tail_decay": "radioactive_tail",
        "late_relaxation": "late_remnant_relaxation",
    }.get(phase, "unknown")

def load_osc_object(json_path):
    with Path(json_path).open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or not data:
        raise ValueError("OSC JSON must be a non-empty object keyed by supernova name.")
    object_key = next(iter(data.keys()))
    return object_key, data[object_key]

def convert(json_path, output_csv):
    json_path = Path(json_path)
    object_key, obj = load_osc_object(json_path)

    object_name = obj.get("name", object_key)
    aliases = "; ".join(a.get("value", "") for a in obj.get("alias", []) if a.get("value"))
    supernova_type = safe_first(obj.get("claimedtype"), "value", "unknown")
    ra = safe_first(obj.get("ra"), "value", "")
    dec = safe_first(obj.get("dec"), "value", "")
    redshift = safe_first(obj.get("redshift"), "value", "")
    host = safe_first(obj.get("host"), "value", "")
    discovery_date = safe_first(obj.get("discoverdate"), "value", "")
    discovery_mjd = date_to_mjd(discovery_date) if discovery_date else None

    mag_phot = []
    skipped_nonmag = 0
    for p in obj.get("photometry", []):
        if "magnitude" not in p or "time" not in p:
            skipped_nonmag += 1
            continue
        try:
            t = float(p["time"])
            mag = float(p["magnitude"])
        except (TypeError, ValueError):
            continue
        band = str(p.get("band", "unknown"))
        mag_phot.append((band, t, mag, p))

    by_band = defaultdict(list)
    for band, t, mag, p in mag_phot:
        by_band[band].append((t, mag, p))
    for band in by_band:
        by_band[band].sort(key=lambda x: x[0])

    peak_by_band = {}
    for band, entries in by_band.items():
        peak_by_band[band] = min(((t, mag) for t, mag, _ in entries), key=lambda x: x[1])

    rows = []
    for band, entries in sorted(by_band.items()):
        peak_time, peak_mag = peak_by_band[band]
        n = len(entries)
        for i, (t, mag, p) in enumerate(entries):
            prev = entries[i - 1] if i > 0 else None
            nxt = entries[i + 1] if i + 1 < n else None

            slope = ""
            curvature = ""
            if prev:
                dt = t - prev[0]
                if dt:
                    slope = (mag - prev[1]) / dt
            if prev and nxt:
                dt1 = t - prev[0]
                dt2 = nxt[0] - t
                if dt1 and dt2:
                    slope_prev = (mag - prev[1]) / dt1
                    slope_next = (nxt[1] - mag) / dt2
                    curvature = (slope_next - slope_prev) / ((dt1 + dt2) / 2.0)

            time_since_peak = t - peak_time
            stage_index, phase, boundary_role, struc_role = phase_from_time_since_peak(time_since_peak)
            time_since_discovery = t - discovery_mjd if discovery_mjd is not None else ""

            rows.append({
                "ladder_id": f"B_{object_name}_{band}".replace(" ", ""),
                "source_id": "B1",
                "source_name": "Open Supernova Catalog / AstroCats",
                "object_name": object_name,
                "alias_names": aliases,
                "supernova_type": supernova_type,
                "classification_source": "Open Supernova Catalog / AstroCats",
                "ra_deg": ra,
                "dec_deg": dec,
                "redshift": redshift,
                "host_galaxy": host,
                "band": band,
                "stage_index": stage_index,
                "phase_name": phase,
                "time_mjd": t,
                "time_since_discovery_days": time_since_discovery,
                "time_since_peak_days": time_since_peak,
                "brightness_value": mag,
                "brightness_unit": "mag",
                "brightness_error": "",
                "detection_flag": "detection",
                "quality_flag": "usable",
                "slope_local": slope,
                "curvature_local": curvature,
                "transition_marker": transition_marker_from_phase(phase),
                "boundary_role": boundary_role,
                "support_regime_proxy": support_proxy_from_phase(phase),
                "struc_perc_role": struc_role,
                "unns_interpretation": "observed post-collapse brightness-time ladder state",
                "raw_reference": f"{json_path.name}::{object_key}::photometry",
            })

    with Path(output_csv).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Object: {object_name}")
    print(f"Rows written: {len(rows)}")
    print(f"Skipped non-magnitude photometry records: {skipped_nonmag}")
    print(f"Output: {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python osc_to_b_ladder.py INPUT_OSC_JSON OUTPUT_LADDER_CSV")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])

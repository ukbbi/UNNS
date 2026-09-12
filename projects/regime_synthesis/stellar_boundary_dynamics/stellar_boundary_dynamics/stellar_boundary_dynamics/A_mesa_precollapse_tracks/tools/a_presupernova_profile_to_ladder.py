#!/usr/bin/env python3
"""
a_presupernova_profile_to_ladder.py

Real Phase A converter for STELLAR_BOUNDARY_DYNAMICS_I.

Converts Zenodo 5556959 pre-supernova MESA profile .data files into
Phase A numerical pre-supernova profile ladders.

Input examples:
  precomputed_tracks/selected_tracks/ZENODO_5556959/profile_single_M12.09_128net.data
  precomputed_tracks/selected_tracks/ZENODO_5556959/profile_single_M19.98_128net.data

Output examples:
  ladders/A1_12M_presupernova_profile_ladder.csv
  ladders/A2_20M_presupernova_profile_ladder.csv

This converter operates on real processed pre-supernova profile/model data,
not on scaffold inlists.

Usage from A_mesa_precollapse_tracks/:

  python tools/a_presupernova_profile_to_ladder.py --batch precomputed_tracks/selected_tracks/ZENODO_5556959 ladders summaries/A_PRESUPERNOVA_PROFILE_LADDER_SUMMARY.csv

Single file:

  python tools/a_presupernova_profile_to_ladder.py precomputed_tracks/selected_tracks/ZENODO_5556959/profile_single_M12.09_128net.data ladders/A1_12M_presupernova_profile_ladder.csv
"""

import argparse
import csv
import math
import re
from pathlib import Path


OUTPUT_COLUMNS = [
    "ladder_id",
    "source_id",
    "source_name",
    "object_name",
    "progenitor_type",
    "target_mass_class",
    "selected_model_mass",
    "network",
    "model_number",
    "num_zones",
    "star_age",
    "time_seconds",
    "star_mass",
    "he_core_mass",
    "c_core_mass",
    "o_core_mass",
    "si_core_mass",
    "fe_core_mass",
    "zone_index",
    "radial_order",
    "q",
    "mass_coordinate",
    "radius",
    "logR",
    "logT",
    "logRho",
    "logP",
    "luminosity",
    "entropy",
    "ye",
    "abar",
    "mu",
    "h1",
    "he4",
    "c12",
    "o16",
    "ne20",
    "mg24",
    "si28",
    "fe56",
    "eps_nuc",
    "non_nuc_neu",
    "support_margin_proxy",
    "energy_loss_proxy",
    "dominant_species",
    "composition_stage",
    "boundary_role",
    "struc_perc_role",
    "unns_interpretation",
    "raw_reference",
]


SUMMARY_COLUMNS = [
    "input_file",
    "output_file",
    "ladder_id",
    "object_name",
    "progenitor_type",
    "target_mass_class",
    "selected_model_mass",
    "network",
    "model_number",
    "num_zones_header",
    "rows_written",
    "center_logT",
    "center_logRho",
    "center_ye",
    "center_dominant_species",
    "surface_logT",
    "surface_logRho",
    "surface_dominant_species",
    "status",
]


SPECIES = ["h1", "he4", "c12", "o16", "ne20", "mg24", "si28", "fe56"]


def to_float(value, default=0.0):
    try:
        if value is None:
            return default
        text = str(value).strip()
        if text == "":
            return default
        x = float(text)
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


def make_unique(names):
    counts = {}
    unique = []
    for name in names:
        counts[name] = counts.get(name, 0) + 1
        if counts[name] == 1:
            unique.append(name)
        else:
            unique.append(f"{name}__{counts[name]}")
    return unique


def parse_filename(path):
    """
    Expected names:
      profile_single_M12.09_128net.data
      profile_single_M19.98_128net.data
    """
    name = Path(path).name
    m = re.match(r"profile_(?P<kind>single|binary)_M(?P<mass>[0-9.]+)_(?P<network>[^.]+)\.data$", name)
    if not m:
        return {
            "progenitor_type": "unknown",
            "selected_model_mass": "",
            "network": "",
            "target_mass_class": "unknown",
            "ladder_id": Path(path).stem,
            "source_id": "A_PRECOMP_ZENODO_5556959",
            "object_name": Path(path).stem,
        }

    kind = m.group("kind")
    mass = float(m.group("mass"))
    network = m.group("network")

    if abs(mass - 12.0) <= abs(mass - 20.0):
        target = "12M"
        ladder_id = "A1_12M"
        source_id = "A1"
        object_name = "12M_pre_supernova_single_profile"
    else:
        target = "20M"
        ladder_id = "A2_20M"
        source_id = "A2"
        object_name = "20M_pre_supernova_single_profile"

    return {
        "progenitor_type": kind,
        "selected_model_mass": mass,
        "network": network,
        "target_mass_class": target,
        "ladder_id": ladder_id,
        "source_id": source_id,
        "object_name": object_name,
    }


def read_mesa_profile(path):
    """
    MESA profile-style structure observed in Zenodo 5556959 files:

      line 1: global column numbers
      line 2: global column names
      line 3: global values
      line 4: blank
      line 5: profile column numbers
      line 6: profile column names
      line 7+: profile zone rows

    Duplicate profile column names are made unique internally. For abundance
    columns, the first occurrence is used unless otherwise specified.
    """
    path = Path(path)
    with path.open("r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    if len(lines) < 7:
        raise ValueError(f"File too short to be a MESA profile: {path}")

    global_names = lines[1].split()
    global_values = lines[2].split()
    profile_names_raw = lines[5].split()
    profile_names = make_unique(profile_names_raw)

    if len(global_names) != len(global_values):
        raise ValueError(f"Global header name/value mismatch in {path}")

    meta = dict(zip(global_names, global_values))

    rows = []
    for line in lines[6:]:
        parts = line.split()
        if not parts:
            continue
        if len(parts) != len(profile_names):
            # Skip malformed footer/header fragments if any.
            continue
        rows.append(dict(zip(profile_names, parts)))

    if not rows:
        raise ValueError(f"No profile data rows found in {path}")

    return meta, profile_names, rows


def get(row, key, default=0.0):
    return to_float(row.get(key), default)


def dominant_species(row):
    values = {sp: get(row, sp, 0.0) for sp in SPECIES if sp in row}
    if not values:
        return "unknown", 0.0
    sp, val = max(values.items(), key=lambda kv: kv[1])
    return sp, val


def composition_stage(row):
    sp, val = dominant_species(row)
    logT = get(row, "logT")
    q = get(row, "q")

    if q > 0.80 and sp in ("h1", "he4"):
        return "outer_envelope"
    if sp == "h1":
        return "hydrogen_rich"
    if sp == "he4":
        return "helium_rich"
    if sp in ("c12", "o16"):
        return "carbon_oxygen_layer"
    if sp in ("ne20", "mg24"):
        return "neon_magnesium_layer"
    if sp == "si28":
        return "silicon_rich_layer"
    if sp == "fe56":
        return "iron_group_layer"
    if logT >= 9.5:
        return "advanced_burning_core"
    return "mixed_composition_layer"


def boundary_role(row):
    q = get(row, "q")
    if q <= 1e-4:
        return "central_core"
    if q <= 1e-2:
        return "inner_core"
    if q <= 5e-2:
        return "core_boundary_region"
    if q <= 0.5:
        return "intermediate_shell"
    if q <= 0.95:
        return "outer_shell"
    return "surface_envelope"


def struc_perc_role(row):
    role = boundary_role(row)
    if role in ("central_core", "inner_core", "core_boundary_region"):
        return "precollapse_boundary_state"
    if role in ("intermediate_shell", "outer_shell"):
        return "support_shell_state"
    return "envelope_state"


def support_margin_proxy(row):
    """
    First structural support proxy from profile-local thermodynamic state.
    It is not a physical pressure-support theorem. It provides a monotone-ready
    scalar combining pressure and density scale:
        support_margin_proxy = logP - logRho
    """
    return get(row, "logP") - get(row, "logRho")


def energy_loss_proxy(row):
    """
    Positive values indicate neutrino-loss scale relative to nuclear energy scale.
    Uses log10(1 + non_nuc_neu) - log10(1 + abs(eps_nuc)).
    """
    eps = abs(get(row, "eps_nuc"))
    neu = abs(get(row, "non_nuc_neu"))
    return math.log10(1.0 + neu) - math.log10(1.0 + eps)


def convert_one(input_file, output_csv):
    input_file = Path(input_file)
    output_csv = Path(output_csv)
    meta_file = parse_filename(input_file)
    meta, profile_names, rows = read_mesa_profile(input_file)

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    model_number = meta.get("model_number", "")
    num_zones = meta.get("num_zones", "")
    star_age = meta.get("star_age", "")
    time_seconds = meta.get("time_seconds", "")
    star_mass = meta.get("star_mass", "")
    he_core_mass = meta.get("he_core_mass", "")
    c_core_mass = meta.get("c_core_mass", "")
    o_core_mass = meta.get("o_core_mass", "")
    si_core_mass = meta.get("si_core_mass", "")
    fe_core_mass = meta.get("fe_core_mass", "")

    out_rows = []
    total = len(rows)

    for i, row in enumerate(rows, start=1):
        sp, _ = dominant_species(row)
        out_rows.append({
            "ladder_id": meta_file["ladder_id"],
            "source_id": meta_file["source_id"],
            "source_name": "Zenodo 5556959 pre-supernova processed MESA profile",
            "object_name": meta_file["object_name"],
            "progenitor_type": meta_file["progenitor_type"],
            "target_mass_class": meta_file["target_mass_class"],
            "selected_model_mass": fmt(meta_file["selected_model_mass"]),
            "network": meta_file["network"],
            "model_number": model_number,
            "num_zones": num_zones,
            "star_age": star_age,
            "time_seconds": time_seconds,
            "star_mass": star_mass,
            "he_core_mass": he_core_mass,
            "c_core_mass": c_core_mass,
            "o_core_mass": o_core_mass,
            "si_core_mass": si_core_mass,
            "fe_core_mass": fe_core_mass,
            "zone_index": int(get(row, "zone")),
            "radial_order": i,
            "q": fmt(get(row, "q")),
            "mass_coordinate": fmt(get(row, "mass")),
            "radius": fmt(get(row, "radius")),
            "logR": fmt(get(row, "logR")),
            "logT": fmt(get(row, "logT")),
            "logRho": fmt(get(row, "logRho")),
            "logP": fmt(get(row, "logP")),
            "luminosity": fmt(get(row, "luminosity")),
            "entropy": fmt(get(row, "entropy")),
            "ye": fmt(get(row, "ye")),
            "abar": fmt(get(row, "abar")),
            "mu": fmt(get(row, "mu")),
            "h1": fmt(get(row, "h1")),
            "he4": fmt(get(row, "he4")),
            "c12": fmt(get(row, "c12")),
            "o16": fmt(get(row, "o16")),
            "ne20": fmt(get(row, "ne20")),
            "mg24": fmt(get(row, "mg24")),
            "si28": fmt(get(row, "si28")),
            "fe56": fmt(get(row, "fe56")),
            "eps_nuc": fmt(get(row, "eps_nuc")),
            "non_nuc_neu": fmt(get(row, "non_nuc_neu")),
            "support_margin_proxy": fmt(support_margin_proxy(row)),
            "energy_loss_proxy": fmt(energy_loss_proxy(row)),
            "dominant_species": sp,
            "composition_stage": composition_stage(row),
            "boundary_role": boundary_role(row),
            "struc_perc_role": struc_perc_role(row),
            "unns_interpretation": "real pre-supernova radial structure ladder state",
            "raw_reference": f"{input_file.name}::zone={int(get(row, 'zone'))}",
        })

    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(out_rows)

    # Center is last row in these profiles: q near 0, highest logT/logRho.
    surface = out_rows[0]
    center = out_rows[-1]

    summary = {
        "input_file": str(input_file),
        "output_file": str(output_csv),
        "ladder_id": meta_file["ladder_id"],
        "object_name": meta_file["object_name"],
        "progenitor_type": meta_file["progenitor_type"],
        "target_mass_class": meta_file["target_mass_class"],
        "selected_model_mass": fmt(meta_file["selected_model_mass"]),
        "network": meta_file["network"],
        "model_number": model_number,
        "num_zones_header": num_zones,
        "rows_written": len(out_rows),
        "center_logT": center["logT"],
        "center_logRho": center["logRho"],
        "center_ye": center["ye"],
        "center_dominant_species": center["dominant_species"],
        "surface_logT": surface["logT"],
        "surface_logRho": surface["logRho"],
        "surface_dominant_species": surface["dominant_species"],
        "status": "converted",
    }

    print(f"Converted: {input_file}")
    print(f"Output: {output_csv}")
    print(f"Rows written: {len(out_rows)}")
    print(f"Center: logT={summary['center_logT']} logRho={summary['center_logRho']} Ye={summary['center_ye']} dominant={summary['center_dominant_species']}")
    return summary


def output_name_for(input_file):
    name = Path(input_file).name
    if "M12.09" in name:
        return "A1_12M_presupernova_profile_ladder.csv"
    if "M19.98" in name:
        return "A2_20M_presupernova_profile_ladder.csv"
    stem = Path(input_file).stem
    return f"{stem}_presupernova_profile_ladder.csv"


def batch_convert(input_dir, output_dir, summary_csv):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    summary_csv = Path(summary_csv)

    files = sorted(input_dir.glob("profile_single_M*_128net.data"))
    # Prefer only the selected baseline pair if present.
    selected = [p for p in files if ("M12.09" in p.name or "M19.98" in p.name)]
    if selected:
        files = selected

    if not files:
        raise FileNotFoundError(f"No selected profile_single_M*_128net.data files found in {input_dir}")

    summaries = []
    for file in files:
        out = output_dir / output_name_for(file)
        summaries.append(convert_one(file, out))

    summary_csv.parent.mkdir(parents=True, exist_ok=True)
    with summary_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        writer.writerows(summaries)

    print(f"Summary written: {summary_csv}")


def main():
    parser = argparse.ArgumentParser(description="Convert Zenodo pre-supernova profile .data files to Phase A ladders.")
    parser.add_argument("paths", nargs="*", help="Single mode: input_file output_csv. Batch mode: input_dir output_dir summary_csv.")
    parser.add_argument("--batch", action="store_true")
    args = parser.parse_args()

    if args.batch:
        if len(args.paths) != 3:
            raise SystemExit("Batch usage: python tools/a_presupernova_profile_to_ladder.py --batch INPUT_DIR OUTPUT_DIR SUMMARY_CSV")
        batch_convert(args.paths[0], args.paths[1], args.paths[2])
        return

    if len(args.paths) != 2:
        raise SystemExit(__doc__)

    convert_one(args.paths[0], args.paths[1])


if __name__ == "__main__":
    main()

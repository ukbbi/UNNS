from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import shutil
import sys
import zipfile

import pandas as pd


TOOL = "ROUTE_LADDER_EXTRACT"
VERSION = "0.1.1"
DEFAULT_RUN_NAME = "jhtdb_pilot_a_20260904_235409.zip"
EXPECTED_RUN_SHA256 = "cc2c2caadca37d8f9cea7415bad37929da4e3a11d069a1414d18fba42126b788"
UNIT_INTERVAL_TOL = 1e-12

EXPECTED = {
    "run_id": "jhtdb_pilot_a_20260904_235409",
    "route_i_version": "0.1.2",
    "D_STITCH": 4957,
    "P_TIME": 10507,
    "P_SCALE": 6009,
}

LADDERS = {
    "D_STITCH": {
        "column": "stitch_defect",
        "selection": "finite stitch_defect on stitching-eligible source nodes",
        "axis": None,
    },
    "P_TIME": {
        "column": "time_persistence",
        "selection": "node_id is a source of at least one eligible time relation",
        "axis": "time",
    },
    "P_SCALE": {
        "column": "scale_persistence",
        "selection": "node_id is a source of at least one eligible scale relation",
        "axis": "scale",
    },
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def find_project_root(start: Path) -> Path:
    rel = Path("outputs") / "exports" / "struc_route_i" / "jhtdb_pilot_a" / DEFAULT_RUN_NAME
    cur = start.resolve()
    for p in [cur] + list(cur.parents):
        if (p / rel).exists():
            return p
    raise FileNotFoundError(
        "Could not locate the turbulence project root. Expected to find:\n"
        f"  outputs\\exports\\struc_route_i\\jhtdb_pilot_a\\{DEFAULT_RUN_NAME}\n"
        "above this tool folder."
    )


def chamber_parser_compatibility(csv_path: Path) -> dict:
    """
    Simulate the relevant ingestion assumptions of canonical STRUC-I v1.0.4
    and STRUC-PERC-I v2.5.0.

    STRUC-I: one header row + one numeric 'value' column.
    STRUC-PERC-I: split CSV tokens, parseFloat-compatible numbers; header ignored.
    """
    lines = csv_path.read_text(encoding="utf-8").replace("\r", "").strip().split("\n")
    if not lines or lines[0].strip().lower() != "value":
        raise ValueError(f"{csv_path.name}: expected single header 'value'.")

    vals = []
    for line in lines[1:]:
        s = line.strip()
        if not s:
            continue
        vals.append(float(s))

    if len(vals) < 3:
        raise ValueError(f"{csv_path.name}: fewer than 3 numeric values.")
    if not all(math.isfinite(v) for v in vals):
        raise ValueError(f"{csv_path.name}: non-finite value detected.")

    # STRUC-I sorts after reading; STRUC-PERC-I also sorts after reading.
    return {
        "struc_i_v1_0_4": "PASS",
        "struc_perc_i_v2_5_0": "PASS",
        "parsed_numeric_count": len(vals),
        "sorted_ascending": all(vals[i] <= vals[i+1] for i in range(len(vals)-1)),
    }


def write_value_csv(path: Path, series: pd.Series):
    path.parent.mkdir(parents=True, exist_ok=True)
    values = pd.to_numeric(series, errors="raise").astype(float)
    if not values.map(math.isfinite).all():
        raise ValueError(f"{path.name}: non-finite value encountered.")

    # 17 significant digits preserves binary64 round-trip values.
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("value\n")
        for v in values:
            f.write(format(float(v), ".17g") + "\n")


def locate_member(names: list[str], basename: str) -> str:
    hits = [n for n in names if n.endswith("/" + basename) or n == basename]
    if len(hits) != 1:
        raise ValueError(
            f"Expected exactly one {basename} in run ZIP, found {len(hits)}: {hits}"
        )
    return hits[0]


def extract_ladders(run_zip: Path, project_root: Path):
    run_zip = run_zip.resolve()
    project_root = project_root.resolve()

    print(f"{TOOL} v{VERSION}")
    print(f"Project root: {project_root}")
    print(f"Frozen run:   {run_zip}")
    print()

    run_sha = sha256_file(run_zip)
    print("Frozen run SHA-256:")
    print(f"  {run_sha}")
    if run_sha.lower() != EXPECTED_RUN_SHA256.lower():
        raise ValueError(
            "Frozen run ZIP checksum mismatch.\n"
            f"Expected: {EXPECTED_RUN_SHA256}\n"
            f"Found:    {run_sha}\n"
            "Refusing extraction from a different or modified chamber export."
        )
    print("  PASS — frozen source identity locked.")

    with zipfile.ZipFile(run_zip, "r") as zf:
        names = zf.namelist()
        node_member = locate_member(names, "NODES.parquet")
        edge_member = locate_member(names, "EDGES.parquet")
        result_member = locate_member(names, "RESULT.json")
        run_member = locate_member(names, "RUN.json")
        squares_member = locate_member(names, "SQUARES.parquet")
        ladders_member = locate_member(names, "LADDERS.zip")

        nodes_raw = zf.read(node_member)
        edges_raw = zf.read(edge_member)
        squares_raw = zf.read(squares_member)
        ladders_raw = zf.read(ladders_member)
        result_raw = zf.read(result_member)
        run_raw = zf.read(run_member)

    result = json.loads(result_raw)
    run_record = json.loads(run_raw)

    run_id = result.get("meta", {}).get("run_id")
    route_version = result.get("meta", {}).get("version")
    if run_id != EXPECTED["run_id"]:
        raise ValueError(f"Unexpected run_id: {run_id!r}; expected {EXPECTED['run_id']!r}")
    if route_version != EXPECTED["route_i_version"]:
        raise ValueError(
            f"Unexpected STRUC-ROUTE-I version: {route_version!r}; "
            f"expected {EXPECTED['route_i_version']!r}"
        )

    # Production extraction requires pyarrow because the frozen chamber output is Parquet.
    # pandas raises a clear ImportError if the environment lacks a Parquet engine.
    nodes = pd.read_parquet(io.BytesIO(nodes_raw))
    edges = pd.read_parquet(io.BytesIO(edges_raw))
    squares = pd.read_parquet(io.BytesIO(squares_raw))

    required_node_cols = {
        "node_id", "scale_persistence", "time_persistence", "stitch_defect"
    }
    required_edge_cols = {"src_id", "dst_id", "axis"}
    miss_n = sorted(required_node_cols - set(nodes.columns))
    miss_e = sorted(required_edge_cols - set(edges.columns))
    if miss_n:
        raise ValueError(f"NODES.parquet missing columns: {miss_n}")
    if miss_e:
        raise ValueError(f"EDGES.parquet missing columns: {miss_e}")

    nodes = nodes.copy()
    edges = edges.copy()
    nodes["node_id"] = nodes["node_id"].astype(str)
    edges["src_id"] = edges["src_id"].astype(str)
    edges["axis"] = edges["axis"].astype(str).str.lower().str.strip()

    if nodes["node_id"].duplicated().any():
        raise ValueError("NODES.parquet contains duplicate node_id values.")

    # Exact route-derived populations.
    finite_stitch = pd.to_numeric(nodes["stitch_defect"], errors="coerce")
    d_stitch = finite_stitch[finite_stitch.map(math.isfinite)]

    time_src = set(edges.loc[edges["axis"] == "time", "src_id"])
    scale_src = set(edges.loc[edges["axis"] == "scale", "src_id"])

    p_time = pd.to_numeric(
        nodes.loc[nodes["node_id"].isin(time_src), "time_persistence"],
        errors="raise",
    )
    p_scale = pd.to_numeric(
        nodes.loc[nodes["node_id"].isin(scale_src), "scale_persistence"],
        errors="raise",
    )

    populations = {
        "D_STITCH": d_stitch.sort_values(kind="mergesort").reset_index(drop=True),
        "P_TIME": p_time.sort_values(kind="mergesort").reset_index(drop=True),
        "P_SCALE": p_scale.sort_values(kind="mergesort").reset_index(drop=True),
    }

    # Independent cross-check 1:
    # ROUTE-I generic LADDERS.zip contains persistence for all nodes.
    # For a source node, persistence must be >0; terminal/non-source nodes are 0.
    # Therefore the positive subset must exactly equal our edge-source selection.
    with zipfile.ZipFile(io.BytesIO(ladders_raw), "r") as lz:
        def generic_values(name):
            text = lz.read(name).decode("utf-8").replace("\r", "")
            vals = []
            for line in text.strip().split("\n")[1:]:
                if line.strip():
                    vals.append(float(line.strip()))
            return pd.Series(vals, dtype=float)

        generic_scale = generic_values("scale_persistence.csv")
        generic_time = generic_values("time_persistence.csv")

    generic_scale_pos = generic_scale[generic_scale > 0].sort_values(
        kind="mergesort"
    ).reset_index(drop=True)
    generic_time_pos = generic_time[generic_time > 0].sort_values(
        kind="mergesort"
    ).reset_index(drop=True)

    if len(generic_scale_pos) != len(populations["P_SCALE"]) or not (
        generic_scale_pos.to_numpy() == populations["P_SCALE"].to_numpy()
    ).all():
        raise ValueError(
            "P_SCALE source-edge selection does not match the independent "
            "positive-persistence population in embedded LADDERS.zip."
        )
    if len(generic_time_pos) != len(populations["P_TIME"]) or not (
        generic_time_pos.to_numpy() == populations["P_TIME"].to_numpy()
    ).all():
        raise ValueError(
            "P_TIME source-edge selection does not match the independent "
            "positive-persistence population in embedded LADDERS.zip."
        )

    # Independent cross-check 2:
    # Re-aggregate node-level stitch defects by scale×time cell and require
    # agreement with ROUTE-I's exported SQUARES.parquet cell means.
    finite_nodes = nodes.loc[
        pd.to_numeric(nodes["stitch_defect"], errors="coerce").map(math.isfinite),
        ["scale_idx", "time_idx", "stitch_defect"]
    ].copy()
    agg = (
        finite_nodes.groupby(["scale_idx", "time_idx"], as_index=False)
        .agg(
            n_sources=("stitch_defect", "size"),
            mean_defect=("stitch_defect", "mean"),
        )
        .sort_values(["scale_idx", "time_idx"])
        .reset_index(drop=True)
    )
    sq = (
        squares[["scale_idx", "time_idx", "n_sources", "mean_defect"]]
        .sort_values(["scale_idx", "time_idx"])
        .reset_index(drop=True)
    )
    if len(agg) != len(sq):
        raise ValueError(
            f"D_STITCH cell aggregation mismatch: {len(agg)} vs {len(sq)} cells."
        )
    if not (
        (agg["scale_idx"].to_numpy() == sq["scale_idx"].to_numpy()).all()
        and (agg["time_idx"].to_numpy() == sq["time_idx"].to_numpy()).all()
        and (agg["n_sources"].to_numpy() == sq["n_sources"].to_numpy()).all()
    ):
        raise ValueError("D_STITCH scale×time cell identity/count mismatch.")
    max_cell_err = float(
        abs(agg["mean_defect"].to_numpy() - sq["mean_defect"].to_numpy()).max()
    )
    if max_cell_err > 1e-12:
        raise ValueError(
            f"D_STITCH cell-mean cross-check failed; max error={max_cell_err:.3e}"
        )

    # Cross-check against chamber's own summary counts.
    expected_from_result = {
        "D_STITCH": int(result["structure"]["stitch"]["eligible_sources"]),
        "P_TIME": int(result["structure"]["time"]["source_nodes"]),
        "P_SCALE": int(result["structure"]["scale"]["source_nodes"]),
    }

    for name, s in populations.items():
        n = len(s)
        print(f"{name:10s} n={n:,}")
        if n != EXPECTED[name]:
            raise ValueError(f"{name}: n={n}, expected frozen count {EXPECTED[name]}")
        if n != expected_from_result[name]:
            raise ValueError(
                f"{name}: n={n}, but RESULT.json reports {expected_from_result[name]}"
            )
        if not all(math.isfinite(float(v)) for v in s):
            raise ValueError(f"{name}: non-finite values present.")

    # Structural ranges are [0,1] mathematically. Numerical JSD evaluation can
    # produce machine-roundoff excursions such as 1.0000000000000002.
    # We therefore VALIDATE with a tight tolerance but DO NOT CLIP or modify
    # the extracted values.
    range_diagnostics = {}
    for name in ("D_STITCH", "P_TIME", "P_SCALE"):
        s = populations[name]
        vmin = float(s.min())
        vmax = float(s.max())
        low_excursion = max(0.0, -vmin)
        high_excursion = max(0.0, vmax - 1.0)
        range_diagnostics[name] = {
            "min": vmin,
            "max": vmax,
            "low_excursion": low_excursion,
            "high_excursion": high_excursion,
            "tolerance": UNIT_INTERVAL_TOL,
            "values_modified": False,
        }
        print(
            f"{name:10s} range=[{vmin:.17g}, {vmax:.17g}] "
            f"excursion_low={low_excursion:.3e} "
            f"excursion_high={high_excursion:.3e}"
        )
        if vmin < -UNIT_INTERVAL_TOL or vmax > 1.0 + UNIT_INTERVAL_TOL:
            raise ValueError(
                f"{name} exceeds the mathematical [0,1] range by more than "
                f"the numerical tolerance {UNIT_INTERVAL_TOL:.1e}: "
                f"min={vmin:.17g}, max={vmax:.17g}"
            )

    canonical_dir = (
        project_root / "ladders" / "route_i" / "jhtdb_pilot_a" / "primary"
    )
    struc_i_dir = project_root / "ladders" / "struc_i" / "jhtdb_pilot_a"
    struc_perc_dir = project_root / "ladders" / "struc_perc_i" / "jhtdb_pilot_a"
    record_dir = project_root / "outputs" / "records"

    for d in (canonical_dir, struc_i_dir, struc_perc_dir, record_dir):
        d.mkdir(parents=True, exist_ok=True)

    ladder_records = {}
    compatibility = {}

    for name, series in populations.items():
        canonical = canonical_dir / f"{name}.csv"
        write_value_csv(canonical, series)

        # Chamber-facing copies are byte-identical to the canonical derived ladder.
        dst_i = struc_i_dir / canonical.name
        dst_p = struc_perc_dir / canonical.name
        shutil.copy2(canonical, dst_i)
        shutil.copy2(canonical, dst_p)

        sha = sha256_file(canonical)
        if sha256_file(dst_i) != sha or sha256_file(dst_p) != sha:
            raise RuntimeError(f"{name}: chamber-facing copy checksum mismatch.")

        comp = chamber_parser_compatibility(canonical)
        if comp["parsed_numeric_count"] != len(series):
            raise RuntimeError(f"{name}: parser compatibility count mismatch.")
        compatibility[name] = comp

        vals = [float(v) for v in series]
        distinct = len(set(vals))
        ladder_records[name] = {
            "file": f"{name}.csv",
            "count": int(len(vals)),
            "distinct_values": int(distinct),
            "duplicate_count": int(len(vals) - distinct),
            "min": float(min(vals)),
            "max": float(max(vals)),
            "sha256": sha,
            "source_column": LADDERS[name]["column"],
            "selection_rule": LADDERS[name]["selection"],
            "ordering": "ascending stable sort; duplicates preserved",
            "numeric_format": "binary64 rendered with .17g",
        }

    manifest = {
        "tool": {
            "name": TOOL,
            "version": VERSION,
        },
        "project": "UNNS_TURB_JHTDB_v0_1",
        "pilot": "jhtdb_pilot_a",
        "purpose": (
            "Deterministic extraction of primary STRUC-ROUTE-I scalar descendants "
            "for independent canonical STRUC-I and STRUC-PERC-I interrogation."
        ),
        "source": {
            "run_zip_filename": run_zip.name,
            "run_zip_sha256": run_sha,
            "run_id": run_id,
            "struc_route_i_version": route_version,
            "result_json_sha256": sha256_bytes(result_raw),
            "run_json_sha256": sha256_bytes(run_raw),
            "nodes_parquet_sha256": sha256_bytes(nodes_raw),
            "edges_parquet_sha256": sha256_bytes(edges_raw),
            "squares_parquet_sha256": sha256_bytes(squares_raw),
            "embedded_ladders_zip_sha256": sha256_bytes(ladders_raw),
            "route_verdict": result.get("verdict", {}).get("class"),
        },
        "rules": {
            "duplicates": "PRESERVED",
            "deduplication": False,
            "jitter": False,
            "smoothing": False,
            "normalization": False,
            "rescaling": False,
            "manual_editing": False,
            "sort": "ascending stable",
            "chamber_flow": (
                "Each ladder is fed independently to STRUC-I v1.0.4 and "
                "STRUC-PERC-I v2.5.0. STRUC-I output is NOT input to STRUC-PERC-I."
            ),
        },
        "ladders": ladder_records,
        "parser_compatibility": compatibility,
        "target_chambers": {
            "STRUC-I": "v1.0.4",
            "STRUC-PERC-I": "v2.5.0",
        },
    }

    manifest_path = canonical_dir / "MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    readme = (
        "JHTDB PILOT A — PRIMARY ROUTE-DERIVED LADDERS\n"
        "================================================\n\n"
        "D_STITCH.csv\n"
        "  Full source-object scale-time stitching-defect population.\n"
        "  Selection: finite NODES.stitch_defect.\n\n"
        "P_TIME.csv\n"
        "  Temporal persistence on actual sources of eligible time relations.\n\n"
        "P_SCALE.csv\n"
        "  Scale persistence on actual sources of eligible scale relations.\n\n"
        "All duplicates and full binary64 numerical content are preserved.\n"
        "No normalization, rescaling, smoothing, jitter or deduplication is applied.\n\n"
        "Run order:\n"
        "  1. D_STITCH -> STRUC-I\n"
        "  2. D_STITCH -> STRUC-PERC-I\n"
        "  3. P_TIME   -> STRUC-I\n"
        "  4. P_TIME   -> STRUC-PERC-I\n"
        "  5. P_SCALE  -> STRUC-I\n"
        "  6. P_SCALE  -> STRUC-PERC-I\n"
    )
    (canonical_dir / "README.txt").write_text(readme, encoding="utf-8")

    # Identical manifest copy beside each chamber-facing set.
    shutil.copy2(manifest_path, struc_i_dir / "MANIFEST.json")
    shutil.copy2(manifest_path, struc_perc_dir / "MANIFEST.json")

    # Hash ledger.
    ledger_lines = []
    for p in sorted(canonical_dir.iterdir()):
        if p.is_file():
            ledger_lines.append(f"{sha256_file(p)}  {p.name}")
    (canonical_dir / "SHA256SUMS.txt").write_text(
        "\n".join(ledger_lines) + "\n", encoding="utf-8"
    )

    report = {
        "status": "PASS",
        "tool": f"{TOOL} v{VERSION}",
        "source_run": str(run_zip),
        "source_run_sha256": run_sha,
        "canonical_output": str(canonical_dir),
        "struc_i_output": str(struc_i_dir),
        "struc_perc_i_output": str(struc_perc_dir),
        "counts": {k: int(len(v)) for k, v in populations.items()},
        "checks": {
            "frozen_counts_match": True,
            "result_summary_counts_match": True,
            "persistence_crosscheck_embedded_ladders": True,
            "stitch_cell_mean_crosscheck_squares": True,
            "stitch_cell_mean_max_abs_error": max_cell_err,
            "all_finite": True,
            "quantity_ranges_valid_with_tolerance": True,
            "unit_interval_tolerance": UNIT_INTERVAL_TOL,
            "range_diagnostics": range_diagnostics,
            "values_clipped_or_modified": False,
            "duplicates_preserved": True,
            "copies_byte_identical": True,
            "struc_i_parser_compatible": True,
            "struc_perc_i_parser_compatible": True,
        },
        "ladder_sha256": {k: v["sha256"] for k, v in ladder_records.items()},
    }

    report_path = record_dir / "ROUTE_LADDER_EXTRACT_REPORT.json"
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    archive = record_dir / "ROUTE_LADDERS_PRIMARY.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(canonical_dir.iterdir()):
            if p.is_file():
                zf.write(p, p.name)

    print()
    print("PASS — deterministic ladder extraction complete.")
    print(f"Canonical:   {canonical_dir}")
    print(f"STRUC-I:     {struc_i_dir}")
    print(f"STRUC-PERC-I:{struc_perc_dir}")
    print(f"Report:      {report_path}")
    print(f"Archive:     {archive}")
    return report


def main():
    ap = argparse.ArgumentParser(
        description="Extract primary chamber ladders from frozen STRUC-ROUTE-I run."
    )
    ap.add_argument("--project-root", default=None)
    ap.add_argument("--run-zip", default=None)
    args = ap.parse_args()

    tool_dir = Path(__file__).resolve().parent
    if args.project_root:
        project_root = Path(args.project_root).resolve()
    else:
        project_root = find_project_root(tool_dir)

    if args.run_zip:
        run_zip = Path(args.run_zip).resolve()
    else:
        run_zip = (
            project_root
            / "outputs"
            / "exports"
            / "struc_route_i"
            / "jhtdb_pilot_a"
            / DEFAULT_RUN_NAME
        )

    if not run_zip.exists():
        raise FileNotFoundError(run_zip)

    extract_ladders(run_zip, project_root)


if __name__ == "__main__":
    main()

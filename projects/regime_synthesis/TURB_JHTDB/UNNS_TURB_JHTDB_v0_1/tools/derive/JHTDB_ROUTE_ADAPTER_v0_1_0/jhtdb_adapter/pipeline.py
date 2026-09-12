from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import gc
import hashlib
import json
import math
import shutil
import time
import zipfile

import h5py
import numpy as np
import pandas as pd

from .source import (
    inspect_source, sha256_file, read_velocity_frame,
    parse_energy_history, nearest_energy_reference,
)
from .physics import block_average_velocity, physical_fields, physical_stats
from .objects import segment_q_objects, object_table
from .relations import overlap_relations


def _hash(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _find_project_root(start: Path, relative_source: str):
    cur = start.resolve()
    for p in [cur] + list(cur.parents):
        if (p / relative_source).exists():
            return p
    raise FileNotFoundError(
        f"Could not locate project root containing {relative_source} "
        f"above {start}"
    )


def _margin_cells(native_margin: int, factor: int):
    return max(1, int(math.ceil(native_margin / factor)))


def _min_voxels(min_native: int, min_coarse: int, factor: int):
    return max(int(min_coarse), int(math.ceil(min_native / (factor ** 3))))


def _time_value(frame_cutout_index: int, stored_dt: float, origin: int):
    return float((frame_cutout_index - origin) * stored_dt)


def _write_table(df: pd.DataFrame, preferred_path: Path):
    """
    Prefer Parquet for normal chamber use. Fall back to CSV only when the
    current Python environment lacks a Parquet engine. The Windows launcher
    installs pyarrow, so production runs remain Parquet by default.
    """
    try:
        df.to_parquet(preferred_path, index=False)
        return preferred_path
    except ImportError:
        fallback = preferred_path.with_suffix(".csv")
        df.to_csv(fallback, index=False)
        return fallback


def build_route_manifest(cfg, source_report, source_sha, object_rows, relation_rows):
    return {
        "project_name": "JHTDB isotropic1024coarse — UNNS Turbulence Pilot A",
        "run_id": "jhtdb_pilot_a",
        "domain": "TURBULENCE_JHTDB",
        "strict_adjacent": True,
        "relation_rule": cfg["relations"]["eligibility"],
        "edge_weight_column": cfg["route_i"]["edge_weight_column"],
        "object_weight_column": cfg["route_i"]["object_weight_column"],
        "nulls": cfg["route_i"]["nulls"],
        "inference": cfg["route_i"]["inference"],
        "adapter": {
            "name": cfg["adapter"]["name"],
            "version": cfg["adapter"]["version"],
            "pilot": cfg["adapter"]["pilot"],
            "source_dataset": cfg["source"]["dataset"],
            "source_sha256": source_sha,
            "source_shape": source_report["shape"],
            "axis_order": cfg["source"]["axis_order"],
            "multiscale_method": cfg["scales"]["method"],
            "block_factors": cfg["scales"]["block_factors"],
            "boundary_policy": cfg["boundary"],
            "segmentation": cfg["segmentation"],
            "relation_candidate_rule": cfg["relations"]["candidate_rule"],
            "confidence_definition": cfg["relations"]["confidence"],
            "weight_note": (
                "weight=enstrophy_integral is a positive extensive routing weight; "
                "no physical conservation law is asserted."
            ),
            "n_objects": int(object_rows),
            "n_relation_candidates": int(relation_rows),
        }
    }


def run_adapter(
    config_path: Path,
    *,
    project_root: Path | None = None,
    skip_hash: bool = False,
    frame_limit: int | None = None,
    factors_override: list[int] | None = None,
    progress=print,
):
    started = time.time()
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    rel_source = cfg["source"]["relative_path"]

    if project_root is None:
        project_root = _find_project_root(config_path.parent, rel_source)
    project_root = Path(project_root).resolve()
    source_path = project_root / rel_source
    if not source_path.exists():
        raise FileNotFoundError(source_path)

    progress(f"[SOURCE] {source_path}")
    source_report = inspect_source(source_path)

    source_sha = None
    do_hash = bool(cfg["source"].get("validate_sha256", True)) and not skip_hash
    if do_hash:
        progress("[SOURCE] Computing canonical SHA-256...")
        source_sha = sha256_file(
            source_path,
            progress=lambda f: progress(f"  SHA-256 {100*f:6.2f}%")
        )
        expected = cfg["source"].get("expected_sha256")
        if expected and source_sha.lower() != expected.lower():
            raise ValueError(
                "SOURCE SHA-256 MISMATCH\n"
                f"expected: {expected}\n"
                f"found:    {source_sha}"
            )
        progress("[SOURCE] SHA-256 PASS")
    else:
        progress("[SOURCE] SHA-256 skipped by request.")

    velocity_names = source_report["velocity_datasets"]
    velocity_indices = source_report["velocity_indices"]
    if frame_limit is not None:
        velocity_names = velocity_names[:frame_limit]
        velocity_indices = velocity_indices[:frame_limit]

    factors = factors_override or list(cfg["scales"]["block_factors"])
    if sorted(factors) != factors or factors[0] != 1:
        raise ValueError("Scale block_factors must be ascending and begin with 1.")
    for a, b in zip(factors[:-1], factors[1:]):
        if b % a:
            raise ValueError("Adjacent block factors must be integer nested.")

    base_shape = tuple(source_report["shape"][:3])
    for f in factors:
        if any(n % f for n in base_shape):
            raise ValueError(f"Source shape {base_shape} not divisible by factor {f}")

    dx = float(source_report["dx"])
    origin_xyz = tuple(source_report["origin_xyz"])
    nu = float(cfg["source"]["viscosity"])
    stored_dt = float(cfg["source"]["stored_dt"])
    time_origin = int(cfg["source"]["cutout_time_index_origin"])

    ref_path = project_root / cfg.get("reference", {}).get(
        "energy_history_relative_path", "__missing__"
    )
    energy_ref = parse_energy_history(ref_path)

    object_frames = []
    relation_frames = []
    phys_rows = []
    warnings = []

    prev_frame_labels = {}
    prev_frame_objects = {}

    for ti, (cutout_index, dset) in enumerate(zip(velocity_indices, velocity_names)):
        time_value = _time_value(cutout_index, stored_dt, time_origin)
        progress(
            f"[FRAME {ti+1}/{len(velocity_names)}] {dset} "
            f"cutout_index={cutout_index} t={time_value:.6f}"
        )
        velocity_native = read_velocity_frame(source_path, dset)
        if tuple(velocity_native.shape) != tuple(source_report["shape"]):
            raise ValueError(f"Frame shape changed: {velocity_native.shape}")

        current_labels = {}
        current_objects = {}
        previous_scale_labels = None
        previous_scale_objects = None
        previous_factor = None

        for si, factor in enumerate(factors):
            progress(f"  [SCALE {si+1}/{len(factors)}] block factor={factor}")
            velocity = block_average_velocity(velocity_native, factor)
            spacing = dx * factor
            margin = _margin_cells(
                int(cfg["boundary"]["margin_native_cells"]), factor
            )
            fields = physical_fields(velocity, spacing, nu)
            stats = physical_stats(velocity, fields, margin)

            minvox = _min_voxels(
                int(cfg["segmentation"]["min_native_voxels"]),
                int(cfg["segmentation"]["min_coarse_voxels"]),
                factor,
            )
            labels, seg = segment_q_objects(
                fields["Q"],
                fields["enstrophy"],
                fields["helicity"],
                q_rms_multiplier=float(cfg["segmentation"]["q_rms_multiplier"]),
                margin_cells=margin,
                min_voxels=minvox,
                discard_touching=bool(
                    cfg["boundary"].get("discard_touching_objects", True)
                ),
            )

            objs = object_table(
                labels,
                fields["Q"],
                fields["enstrophy"],
                fields["helicity"],
                time_idx=ti,
                time_value=time_value,
                scale_idx=si,
                factor=factor,
                spacing_native=dx,
                origin_xyz=origin_xyz,
            )

            if len(objs) == 0:
                warnings.append(
                    f"No objects at frame={ti}, scale={si}, factor={factor}"
                )

            ref = nearest_energy_reference(energy_ref, time_value)
            ref_t = ref_e = ref_re = None
            if ref:
                ref_t, ref_e, ref_re = ref

            phys_rows.append({
                "time_idx": ti,
                "time_value": time_value,
                "source_dataset": dset,
                "scale_idx": si,
                "block_factor": factor,
                "grid_nz": velocity.shape[0],
                "grid_ny": velocity.shape[1],
                "grid_nx": velocity.shape[2],
                "spacing": spacing,
                "boundary_margin_cells": margin,
                "min_object_voxels": minvox,
                **stats,
                **seg,
                "object_count": int(len(objs)),
                "global_ref_time": ref_t,
                "global_ref_energy": ref_e,
                "global_ref_Re_lambda": ref_re,
                "local_to_global_energy_ratio": (
                    stats["kinetic_energy_local"] / ref_e
                    if ref_e not in (None, 0) else None
                ),
            })

            object_frames.append(objs)
            current_labels[si] = labels
            current_objects[si] = objs

            # Adjacent scale relation: previous finer -> current coarser.
            if previous_scale_labels is not None:
                rel = overlap_relations(
                    previous_scale_labels,
                    labels,
                    previous_scale_objects,
                    objs,
                    axis="scale",
                    src_factor=previous_factor,
                    dst_factor=factor,
                    spacing_native=dx,
                )
                if len(rel):
                    relation_frames.append(rel)

            # Adjacent time relation: previous frame -> current frame, same scale.
            if si in prev_frame_labels:
                rel = overlap_relations(
                    prev_frame_labels[si],
                    labels,
                    prev_frame_objects[si],
                    objs,
                    axis="time",
                    src_factor=factor,
                    dst_factor=factor,
                    spacing_native=dx,
                )
                if len(rel):
                    relation_frames.append(rel)

            previous_scale_labels = labels
            previous_scale_objects = objs
            previous_factor = factor

            # Release heavy physical arrays; retain compact labels + tables.
            del fields, velocity
            gc.collect()

        del velocity_native
        prev_frame_labels = current_labels
        prev_frame_objects = current_objects
        gc.collect()

    objects = (
        pd.concat(object_frames, ignore_index=True)
        if object_frames else pd.DataFrame()
    )
    relations = (
        pd.concat(relation_frames, ignore_index=True)
        if relation_frames else pd.DataFrame(columns=[
            "src_id","dst_id","axis","overlap_src","overlap_dst","iou",
            "distance_norm","feature_similarity","transfer_weight","confidence"
        ])
    )
    phys = pd.DataFrame(phys_rows)

    # Derived canonical paths.
    derived_dir = project_root / "data" / "derived" / "objects" / cfg["adapter"]["pilot"]
    route_dir = project_root / "ladders" / "native" / cfg["adapter"]["pilot"] / "route_project"
    records_dir = project_root / "outputs" / "records"
    tables_dir = project_root / "outputs" / "tables"
    for p in (derived_dir, route_dir, records_dir, tables_dir):
        p.mkdir(parents=True, exist_ok=True)

    obj_path = _write_table(objects, derived_dir / "objects.parquet")
    rel_path = _write_table(relations, derived_dir / "relations.parquet")

    route_manifest = build_route_manifest(
        cfg, source_report, source_sha, len(objects), len(relations)
    )
    route_manifest_path = route_dir / "manifest.json"
    route_manifest_path.write_text(
        json.dumps(route_manifest, indent=2) + "\n", encoding="utf-8"
    )
    route_obj_path = _write_table(objects, route_dir / "objects.parquet")
    route_rel_path = _write_table(relations, route_dir / "relations.parquet")

    phys_path = tables_dir / "JHTDB_PHYS_STATS.csv"
    phys.to_csv(phys_path, index=False)
    phys.to_csv(route_dir / "PHYS_STATS.csv", index=False)

    zip_path = records_dir / "JHTDB_PILOT_A_ROUTE.zip"

    report = {
        "adapter": cfg["adapter"],
        "status": "COMPLETE",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": time.time() - started,
        "project_root": str(project_root),
        "source": {
            "path": str(source_path),
            "sha256": source_sha,
            "inspection": source_report,
        },
        "configuration": cfg,
        "result": {
            "frames": len(velocity_names),
            "scale_factors": factors,
            "objects": int(len(objects)),
            "relation_candidates": int(len(relations)),
            "scale_relations": int((relations["axis"] == "scale").sum()) if len(relations) else 0,
            "time_relations": int((relations["axis"] == "time").sum()) if len(relations) else 0,
        },
        "warnings": warnings,
        "outputs": {
            "derived_objects": str(obj_path),
            "derived_relations": str(rel_path),
            "route_project": str(route_dir),
            "phys_stats": str(phys_path),
            "route_zip": str(zip_path),
        },
    }

    report_path = records_dir / "JHTDB_ADAPTER_REPORT.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (route_dir / "ADAPTER_REPORT.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )

    report["output_hashes"] = {
        obj_path.name: _hash(obj_path),
        rel_path.name: _hash(rel_path),
        "manifest.json": _hash(route_manifest_path),
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (route_dir / "ADAPTER_REPORT.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path, arcname in (
            (route_manifest_path, "manifest.json"),
            (route_obj_path, route_obj_path.name),
            (route_rel_path, route_rel_path.name),
            (route_dir / "ADAPTER_REPORT.json", "ADAPTER_REPORT.json"),
            (route_dir / "PHYS_STATS.csv", "PHYS_STATS.csv"),
        ):
            zf.write(file_path, arcname)

    progress("")
    progress("[COMPLETE]")
    progress(f"  objects:            {len(objects):,}")
    progress(f"  relation candidates:{len(relations):,}")
    progress(f"  route project ZIP:  {zip_path}")

    return report

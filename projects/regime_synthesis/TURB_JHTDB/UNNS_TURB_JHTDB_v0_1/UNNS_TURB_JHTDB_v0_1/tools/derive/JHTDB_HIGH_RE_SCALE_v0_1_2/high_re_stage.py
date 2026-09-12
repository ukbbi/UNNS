from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import sys
import time
import zipfile

import h5py
import numpy as np
import pandas as pd

TOOL = "JHTDB_HIGH_RE_SCALE"
VERSION = "0.1.2"
CONFIG_NAME = "high_re.json"
SOURCE_VERIFY_RECORD = "HIGH_RE_SOURCE_VERIFY.json"
ADAPTER_REPORT = "HIGH_RE_ADAPTER_REPORT.json"
STAGE_REPORT = "HIGH_RE_SCALE_STAGE_REPORT.json"


def sha256_file(path: Path, progress=False) -> str:
    h = hashlib.sha256()
    total = path.stat().st_size
    done = 0
    with path.open("rb") as f:
        for block in iter(lambda: f.read(16 * 1024 * 1024), b""):
            h.update(block)
            if progress:
                done += len(block)
                pct = 100.0 * done / total if total else 100.0
                print(f"    SHA-256 {pct:6.2f}%", end="\r", flush=True)
    if progress:
        print(" " * 30, end="\r")
    return h.hexdigest()


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def json_write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def find_project_root(start: Path, cfg: dict) -> Path:
    rel = Path(cfg["export_manifest_relative"])
    for p in [start.resolve()] + list(start.resolve().parents):
        if (p / rel).exists() and (p / cfg["canonical_pilot_a_adapter"]).exists():
            return p
    raise FileNotFoundError(
        "Could not locate UNNS_TURB_JHTDB_v0_1 with the verified HIGH_RE_EXPORT.\n"
        f"Expected: {rel}"
    )


def load_cfg() -> tuple[dict, Path, Path]:
    tool_dir = Path(__file__).resolve().parent
    cfg = json_load(tool_dir / "config" / CONFIG_NAME)
    root = find_project_root(tool_dir, cfg)
    return cfg, tool_dir, root


def import_canonical(root: Path, cfg: dict):
    # Scientific identity gate: refuse to run if the canonical Pilot-A adapter
    # or ROUTE-I core files have been modified since this stage was frozen.
    for rel, expected in (cfg.get("canonical_code_sha256") or {}).items():
        p = root / rel
        if not p.exists():
            raise FileNotFoundError(p)
        found = sha256_file(p)
        if found.lower() != str(expected).lower():
            raise ValueError(
                f"Canonical code identity mismatch: {rel}\n"
                f"Expected: {expected}\nFound:    {found}"
            )

    adapter_dir = root / cfg["canonical_pilot_a_adapter"]
    chamber_dir = root / cfg["canonical_route_chamber"]
    for p in (str(adapter_dir), str(chamber_dir)):
        if p not in sys.path:
            sys.path.insert(0, p)

    from jhtdb_adapter.source import inspect_source, read_velocity_frame
    from jhtdb_adapter.physics import block_average_velocity, physical_fields, physical_stats
    from jhtdb_adapter.objects import segment_q_objects, object_table
    from jhtdb_adapter.relations import overlap_relations
    from struc_route.engine import analyze_project

    return {
        "inspect_source": inspect_source,
        "read_velocity_frame": read_velocity_frame,
        "block_average_velocity": block_average_velocity,
        "physical_fields": physical_fields,
        "physical_stats": physical_stats,
        "segment_q_objects": segment_q_objects,
        "object_table": object_table,
        "overlap_relations": overlap_relations,
        "analyze_project": analyze_project,
    }


def _source_state(path: Path):
    st = path.stat()
    return {"bytes": int(st.st_size), "mtime_ns": int(st.st_mtime_ns)}


def _cache_valid(cache: dict, cfg: dict, root: Path) -> bool:
    try:
        if cache.get("status") != "PASS":
            return False
        arc = root / cfg["source_archive_relative"]
        c_arc = cache["archive"]
        if _source_state(arc) != {"bytes": c_arc["bytes"], "mtime_ns": c_arc["mtime_ns"]}:
            return False
        export_root = root / cfg["source_root_relative"]
        for s in cfg["samples"]:
            p = export_root / s["relative_h5"]
            c = cache["samples"][s["sample_id"]]
            if _source_state(p) != {"bytes": c["bytes"], "mtime_ns": c["mtime_ns"]}:
                return False
            if c["sha256"].lower() != s["expected_sha256"].lower():
                return False
        return True
    except Exception:
        return False


def verify_sources(cfg: dict, root: Path, *, allow_cache=True) -> dict:
    records_dir = root / "outputs" / "records"
    records_dir.mkdir(parents=True, exist_ok=True)
    cache_path = records_dir / SOURCE_VERIFY_RECORD
    if allow_cache and cache_path.exists():
        cache = json_load(cache_path)
        if _cache_valid(cache, cfg, root):
            print("[SOURCE VERIFY] PASS — cached hashes are valid and source file state is unchanged.")
            return cache

    print("UNNS JHTDB HIGH-RE — SOURCE INTEGRITY GATE")
    archive = root / cfg["source_archive_relative"]
    archive_sha_file = archive.with_suffix(archive.suffix + ".sha256")
    export_root = root / cfg["source_root_relative"]
    manifest_path = root / cfg["export_manifest_relative"]
    source_plan = root / "analysis" / "generalization" / "jhtdb_high_re" / "SOURCE_PLAN.json"

    for p in (archive, export_root, manifest_path, source_plan):
        if not p.exists():
            raise FileNotFoundError(p)

    plan_sha = sha256_file(source_plan)
    if plan_sha.lower() != cfg["frozen_source_plan_sha256"].lower():
        raise ValueError(
            "Frozen SOURCE_PLAN.json checksum mismatch.\n"
            f"Expected: {cfg['frozen_source_plan_sha256']}\nFound:    {plan_sha}"
        )
    print("  frozen SOURCE_PLAN.json: PASS")

    print("  hashing HIGH_RE_EXPORT.tar (~1.4 GiB)...")
    archive_sha = sha256_file(archive, progress=True)
    if archive_sha.lower() != cfg["source_archive_sha256"].lower():
        raise ValueError(
            "HIGH_RE_EXPORT.tar checksum mismatch.\n"
            f"Expected: {cfg['source_archive_sha256']}\nFound:    {archive_sha}"
        )
    print(f"  archive SHA-256: {archive_sha}  PASS")

    if archive_sha_file.exists():
        txt = archive_sha_file.read_text(encoding="utf-8", errors="replace").strip().split()
        if not txt or txt[0].lower() != archive_sha.lower():
            raise ValueError("HIGH_RE_EXPORT.tar.sha256 does not match the verified archive.")
        print("  archive .sha256 sidecar: PASS")

    export_manifest = json_load(manifest_path)
    records = export_manifest.get("records", [])
    if len(records) != 7:
        raise ValueError(f"Expected exactly 7 export records, found {len(records)}")
    by_key = {(r.get("dataset"), int(r.get("source_snapshot_label"))): r for r in records}

    mods = import_canonical(root, cfg)
    inspect_source = mods["inspect_source"]
    verified_samples = {}

    for i, s in enumerate(cfg["samples"], 1):
        sid = s["sample_id"]
        h5 = export_root / s["relative_h5"]
        if not h5.exists():
            raise FileNotFoundError(h5)
        key = (s["dataset"], int(s["snapshot"]))
        rec = by_key.get(key)
        if rec is None:
            raise ValueError(f"EXPORT_MANIFEST missing {key}")
        manifest_sha = str(rec.get("sha256", "")).strip().lower()
        if len(manifest_sha) != 64 or any(c not in "0123456789abcdef" for c in manifest_sha):
            raise ValueError(f"EXPORT_MANIFEST has an invalid SHA-256 for {sid}: {manifest_sha!r}")
        if rec.get("sample_role") != s["role"]:
            raise ValueError(f"EXPORT_MANIFEST role mismatch for {sid}")

        # v0.1.1 integrity rule: HIGH_RE_EXPORT.tar is the primary frozen source
        # identity. Once that exact archive hash passes, the per-file hashes in
        # its own EXPORT_MANIFEST are authoritative. The duplicated hashes in
        # config/high_re.json are audit notes only; rejecting the source on a
        # transcription mismatch in that duplicate list is incorrect.
        cfg_sha = str(s.get("expected_sha256", "")).strip().lower()
        if cfg_sha and cfg_sha != manifest_sha:
            print(f"      NOTE: duplicate config hash differs from locked archive manifest for {sid};")
            print("            using archive + EXPORT_MANIFEST identity (v0.1.1 bugfix policy).")

        print(f"  [{i}/7] {sid}: hashing 192 MiB HDF5...")
        digest = sha256_file(h5, progress=True)
        if digest.lower() != manifest_sha:
            raise ValueError(
                f"Source HDF5 checksum mismatch for {sid}.\n"
                f"EXPORT_MANIFEST: {manifest_sha}\nFound:           {digest}"
            )
        ins = inspect_source(h5)
        if ins["shape"] != [256, 256, 256, 3]:
            raise ValueError(f"{sid}: expected [256,256,256,3], found {ins['shape']}")
        if ins["velocity_datasets"] != ["Velocity_0001"]:
            raise ValueError(f"{sid}: expected exactly Velocity_0001")
        with h5py.File(h5, "r") as f:
            if str(f.attrs.get("dataset")) != s["dataset"]:
                raise ValueError(f"{sid}: dataset attribute mismatch")
            if int(f.attrs.get("source_snapshot_label")) != int(s["snapshot"]):
                raise ValueError(f"{sid}: snapshot attribute mismatch")
            if bool(f.attrs.get("temporal_sequence")) is not False:
                raise ValueError(f"{sid}: temporal_sequence must be false")
        state = _source_state(h5)
        verified_samples[sid] = {
            **state,
            "path": str(h5),
            "sha256": digest,
            "inspection": ins,
        }
        print(f"      {digest}  PASS")

    arc_state = _source_state(archive)
    out = {
        "tool": {"name": TOOL, "version": VERSION},
        "status": "PASS",
        "archive": {**arc_state, "path": str(archive), "sha256": archive_sha},
        "frozen_source_plan_sha256": plan_sha,
        "export_manifest_sha256": sha256_file(manifest_path),
        "samples": verified_samples,
    }
    json_write(cache_path, out)
    print("\n[PASS] Seven frozen high-Re source HDF5 files verified.")
    print(f"Record: {cache_path}")
    return out


def _margin_cells(native_margin: int, factor: int):
    return max(1, int(math.ceil(native_margin / factor)))


def _min_voxels(min_native: int, min_coarse: int, factor: int):
    return max(int(min_coarse), int(math.ceil(min_native / (factor ** 3))))


def _write_table(df: pd.DataFrame, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)


def _route_manifest(cfg: dict, s: dict, source_sha: str, source_report: dict, nobj: int, nrel: int):
    g = cfg["grammar"]
    return {
        "project_name": f"JHTDB high-Re {s['dataset']} snapshot {s['snapshot']} — scale-only",
        "run_id": f"jhtdb_high_re_{s['sample_id']}",
        "domain": "TURBULENCE_JHTDB_HIGH_RE_SCALE",
        "strict_adjacent": True,
        "relation_rule": g["relation_eligibility"],
        "edge_weight_column": cfg["route_i"]["edge_weight_column"],
        "object_weight_column": cfg["route_i"]["object_weight_column"],
        "nulls": cfg["route_i"]["nulls"],
        "inference": cfg["route_i"]["inference"],
        "adapter": {
            "name": TOOL,
            "version": VERSION,
            "branch": cfg["branch"],
            "analysis_scope": "SCALE_ONLY_INDEPENDENT_SNAPSHOT",
            "dataset": s["dataset"],
            "snapshot": int(s["snapshot"]),
            "sample_id": s["sample_id"],
            "sample_role": s["role"],
            "source_sha256": source_sha,
            "source_shape": source_report["shape"],
            "axis_order": "zyxc",
            "block_factors": g["block_factors"],
            "multiscale_method": g["multiscale_method"],
            "boundary_margin_native_cells": g["boundary_margin_native_cells"],
            "segmentation": {
                "field": g["segmentation_field"],
                "mode": "q_rms",
                "q_rms_multiplier": g["q_rms_multiplier"],
                "connectivity": g["connectivity"],
                "min_native_voxels": g["min_native_voxels"],
                "min_coarse_voxels": g["min_coarse_voxels"],
            },
            "relation_candidate_rule": g["relation_candidate_rule"],
            "confidence_definition": g["relation_confidence"],
            "time_edges_constructed": False,
            "snapshot_sequence_interpretation": False,
            "n_objects": int(nobj),
            "n_relation_candidates": int(nrel),
            "weight_note": "weight=enstrophy_integral; no conservation law is asserted."
        }
    }


def build_one_adapter(cfg: dict, root: Path, mods: dict, s: dict, verify_record: dict) -> dict:
    sid = s["sample_id"]
    export_root = root / cfg["source_root_relative"]
    h5 = export_root / s["relative_h5"]
    source_sha = verify_record["samples"][sid]["sha256"]
    source_report = mods["inspect_source"](h5)
    dset = source_report["velocity_datasets"][0]
    velocity_native = mods["read_velocity_frame"](h5, dset)
    if velocity_native.shape != (256, 256, 256, 3):
        raise ValueError(f"{sid}: source shape changed: {velocity_native.shape}")

    g = cfg["grammar"]
    dx = float(source_report["dx"])
    origin_xyz = tuple(source_report["origin_xyz"])
    factors = list(g["block_factors"])

    obj_frames = []
    rel_frames = []
    phys_rows = []
    previous_labels = None
    previous_objects = None
    previous_factor = None

    print(f"\n[ADAPTER] {sid} · {s['dataset']} snapshot {s['snapshot']} · role={s['role']}")
    for si, factor in enumerate(factors):
        t0 = time.time()
        print(f"  scale {si+1}/5 · factor={factor}")
        velocity = mods["block_average_velocity"](velocity_native, factor)
        spacing = dx * factor
        margin = _margin_cells(int(g["boundary_margin_native_cells"]), factor)
        # Viscosity is irrelevant to Q/enstrophy/helicity and the current object grammar.
        fields = mods["physical_fields"](velocity, spacing, 0.0)
        stats = mods["physical_stats"](velocity, fields, margin)
        minvox = _min_voxels(int(g["min_native_voxels"]), int(g["min_coarse_voxels"]), factor)
        labels, seg = mods["segment_q_objects"](
            fields["Q"], fields["enstrophy"], fields["helicity"],
            q_rms_multiplier=float(g["q_rms_multiplier"]),
            margin_cells=margin,
            min_voxels=minvox,
            discard_touching=bool(g["discard_touching_objects"]),
        )
        objs = mods["object_table"](
            labels, fields["Q"], fields["enstrophy"], fields["helicity"],
            time_idx=0, time_value=0.0,
            scale_idx=si, factor=factor,
            spacing_native=dx, origin_xyz=origin_xyz,
        )
        obj_frames.append(objs)
        phys_rows.append({
            "sample_id": sid,
            "dataset": s["dataset"],
            "snapshot": int(s["snapshot"]),
            "role": s["role"],
            "scale_idx": si,
            "block_factor": factor,
            "grid_nz": velocity.shape[0],
            "grid_ny": velocity.shape[1],
            "grid_nx": velocity.shape[2],
            "spacing": spacing,
            "boundary_margin_cells": margin,
            "min_object_voxels": minvox,
            **stats, **seg,
            "object_count": int(len(objs)),
            "elapsed_seconds": time.time() - t0,
        })
        print(f"    objects={len(objs):,} q_rms={seg['q_rms']:.6g} threshold={seg['q_threshold']:.6g}")

        if previous_labels is not None:
            rel = mods["overlap_relations"](
                previous_labels, labels, previous_objects, objs,
                axis="scale", src_factor=previous_factor, dst_factor=factor,
                spacing_native=dx,
            )
            if len(rel):
                rel_frames.append(rel)
            print(f"    scale relation candidates={len(rel):,}")

        previous_labels = labels
        previous_objects = objs
        previous_factor = factor
        del fields, velocity
        gc.collect()

    del velocity_native
    gc.collect()

    objects = pd.concat(obj_frames, ignore_index=True) if obj_frames else pd.DataFrame()
    relations = pd.concat(rel_frames, ignore_index=True) if rel_frames else pd.DataFrame(columns=[
        "src_id", "dst_id", "axis", "overlap_src", "overlap_dst", "iou",
        "distance_norm", "feature_similarity", "transfer_weight", "confidence"
    ])
    if len(objects) == 0:
        raise ValueError(f"{sid}: no structural objects found at any scale")
    if set(relations.get("axis", pd.Series(dtype=str)).astype(str)) - {"scale"}:
        raise ValueError(f"{sid}: non-scale relation appeared in scale-only branch")

    route_dir = root / "ladders" / "native" / "jhtdb_high_re" / sid / "route_project"
    derived_dir = root / "data" / "derived" / "objects" / "jhtdb_high_re" / sid
    for d in (route_dir, derived_dir):
        d.mkdir(parents=True, exist_ok=True)

    _write_table(objects, derived_dir / "objects.parquet")
    _write_table(relations, derived_dir / "relations.parquet")
    _write_table(objects, route_dir / "objects.parquet")
    _write_table(relations, route_dir / "relations.parquet")
    phys = pd.DataFrame(phys_rows)
    phys.to_csv(route_dir / "PHYS_STATS.csv", index=False)

    manifest = _route_manifest(cfg, s, source_sha, source_report, len(objects), len(relations))
    json_write(route_dir / "manifest.json", manifest)

    report = {
        "tool": {"name": TOOL, "version": VERSION},
        "status": "ROUTE_INPUT_READY",
        "sample": s,
        "source": {"path": str(h5), "sha256": source_sha, "inspection": source_report},
        "grammar": g,
        "result": {
            "objects": int(len(objects)),
            "scale_relation_candidates": int(len(relations)),
            "time_relations": 0,
            "per_scale": phys_rows,
        },
        "outputs": {"route_project": str(route_dir), "derived_dir": str(derived_dir)},
    }
    json_write(route_dir / "ADAPTER_REPORT.json", report)

    bundle_dir = root / "outputs" / "records" / "high_re_route_inputs"
    bundle_dir.mkdir(parents=True, exist_ok=True)
    bundle = bundle_dir / f"{sid}_ROUTE_INPUT.zip"
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in ("manifest.json", "objects.parquet", "relations.parquet", "ADAPTER_REPORT.json", "PHYS_STATS.csv"):
            zf.write(route_dir / name, name)
    report["outputs"]["route_input_zip"] = str(bundle)
    report["outputs"]["route_input_zip_sha256"] = sha256_file(bundle)
    json_write(route_dir / "ADAPTER_REPORT.json", report)
    return report


def run_adapter_stage(cfg: dict, root: Path) -> dict:
    verify_record = verify_sources(cfg, root, allow_cache=True)
    mods = import_canonical(root, cfg)
    reports = []
    for s in cfg["samples"]:
        reports.append(build_one_adapter(cfg, root, mods, s, verify_record))

    agg = {
        "tool": {"name": TOOL, "version": VERSION},
        "status": "ALL_ROUTE_INPUTS_READY",
        "branch": cfg["branch"],
        "source_archive_sha256": verify_record["archive"]["sha256"],
        "samples": reports,
    }
    out = root / "outputs" / "records" / ADAPTER_REPORT
    json_write(out, agg)
    print(f"\n[PASS] 7 scale-only route projects created.\nRecord: {out}")
    return agg


def _write_value_csv(path: Path, values: pd.Series):
    path.parent.mkdir(parents=True, exist_ok=True)
    vals = pd.to_numeric(values, errors="raise").astype(float)
    if not np.isfinite(vals.to_numpy()).all():
        raise ValueError(f"{path}: non-finite P_SCALE value")
    vals = vals.sort_values(kind="mergesort")
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("value\n")
        for v in vals:
            f.write(format(float(v), ".17g") + "\n")
    return vals


def _read_run_table(run_dir: Path, stem: str):
    p = run_dir / f"{stem}.parquet"
    if p.exists():
        return pd.read_parquet(p)
    p = run_dir / f"{stem}.csv"
    if p.exists():
        return pd.read_csv(p)
    raise FileNotFoundError(f"No {stem}.parquet/csv in {run_dir}")


def extract_one_pscale(cfg: dict, root: Path, s: dict, result: dict, run_dir: Path) -> dict:
    sid = s["sample_id"]
    nodes = _read_run_table(run_dir, "NODES")
    edges = _read_run_table(run_dir, "EDGES")
    scale_edges = edges.loc[edges["axis"].astype(str).str.lower() == "scale"].copy()
    src_ids = set(scale_edges["src_id"].astype(str))
    if not src_ids:
        raise ValueError(f"{sid}: no eligible scale edges after frozen relation rule")
    sel = nodes.loc[nodes["node_id"].astype(str).isin(src_ids), "scale_persistence"]
    if len(sel) != int(result["structure"]["scale"]["source_nodes"]):
        raise ValueError(
            f"{sid}: P_SCALE count {len(sel)} != chamber source_nodes "
            f"{result['structure']['scale']['source_nodes']}"
        )

    dirs = {
        "route": root / "ladders" / "route_i" / "jhtdb_high_re" / sid,
        "struc_i": root / "ladders" / "struc_i" / "jhtdb_high_re" / sid,
        "struc_perc": root / "ladders" / "struc_perc_i" / "jhtdb_high_re" / sid,
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    canonical = dirs["route"] / "P_SCALE.csv"
    vals = _write_value_csv(canonical, sel)
    sha = sha256_file(canonical)
    for k in ("struc_i", "struc_perc"):
        dst = dirs[k] / "P_SCALE.csv"
        shutil.copy2(canonical, dst)
        if sha256_file(dst) != sha:
            raise RuntimeError(f"{sid}: byte-identical chamber copy check failed")

    scale_test = result.get("evidence", {}).get("tests", {}).get("scale_persistence")
    null_quality = result.get("null_quality", {})
    analyzable = bool(
        len(scale_edges) > 0
        and scale_test is not None
        and null_quality.get("usable_for_inference") is True
        and len(vals) > 0
    )
    record = {
        "schema": "UNNS_JHTDB_HIGH_RE_P_SCALE_v0.1",
        "sample": s,
        "status": "ANALYZABLE" if analyzable else "UNDERRESOLVED",
        "route_run_dir": str(run_dir),
        "route_i_version": result.get("meta", {}).get("version"),
        "route_global_verdict": result.get("verdict", {}).get("class"),
        "note_global_verdict": (
            "Scale-only branch intentionally supplies one inferential axis; the global ROUTE-I verdict "
            "may be UNDERRESOLVED and is not the high-Re branch endpoint."
        ),
        "scale_structure": result.get("structure", {}).get("scale"),
        "scale_test": scale_test,
        "null_quality": null_quality,
        "eligible_scale_edges": int(len(scale_edges)),
        "P_SCALE": {
            "count": int(len(vals)),
            "distinct_values": int(vals.nunique()),
            "min": float(vals.min()),
            "max": float(vals.max()),
            "mean": float(vals.mean()),
            "sha256": sha,
            "ordering": "ascending stable sort; duplicates preserved",
            "numeric_format": "binary64 rendered with .17g",
            "normalization": False
        },
    }
    # Avoid Python spelling issue in source provenance: rewrite boolean field explicitly.
    record["P_SCALE"]["normalization"] = False
    json_write(dirs["route"] / "P_SCALE_RECORD.json", record)
    shutil.copy2(dirs["route"] / "P_SCALE_RECORD.json", dirs["struc_i"] / "P_SCALE_RECORD.json")
    shutil.copy2(dirs["route"] / "P_SCALE_RECORD.json", dirs["struc_perc"] / "P_SCALE_RECORD.json")
    return record


def _existing_pscale_record(root: Path, s: dict):
    p = root / "ladders" / "route_i" / "jhtdb_high_re" / s["sample_id"] / "P_SCALE_RECORD.json"
    csv = p.parent / "P_SCALE.csv"
    if not p.exists() or not csv.exists():
        return None
    rec = json_load(p)
    expected = rec.get("P_SCALE", {}).get("sha256")
    if expected and sha256_file(csv) == expected:
        return rec
    return None


def run_route_stage(cfg: dict, root: Path) -> dict:
    # Require source integrity and route inputs.
    verify_record = verify_sources(cfg, root, allow_cache=True)
    mods = import_canonical(root, cfg)
    analyze_project = mods["analyze_project"]
    sample_records = []

    for i, s in enumerate(cfg["samples"], 1):
        sid = s["sample_id"]
        existing = _existing_pscale_record(root, s)
        if existing is not None:
            print(f"[{i}/7] {sid}: existing P_SCALE record verified; skipping deterministic rerun.")
            sample_records.append(existing)
            continue

        route_project = root / "ladders" / "native" / "jhtdb_high_re" / sid / "route_project"
        for name in ("manifest.json", "objects.parquet", "relations.parquet"):
            if not (route_project / name).exists():
                raise FileNotFoundError(
                    f"{route_project / name}\nRun RUN_ADAPTER_WINDOWS.bat first."
                )
        # v0.1.2 transport-only fix: keep the ROUTE-I run directory short enough
        # for legacy Windows MAX_PATH handling. The previous path reached exactly
        # 260 characters at NODES.parquet on the user's project location.
        # No scientific input, threshold, null, or chamber code is changed.
        output_root = root / "outputs" / "r" / "hr" / sid
        output_root.mkdir(parents=True, exist_ok=True)

        # Guard against silently reintroducing a MAX_PATH failure on Windows.
        probe = output_root / f"jhtdb_high_re_{sid}_20991231_235959" / "NODES.parquet"
        if os.name == "nt" and len(str(probe)) >= 248:
            raise OSError(
                f"ROUTE-I output path remains too long for safe Windows operation ({len(str(probe))} chars):\n{probe}"
            )

        print(f"\n[{i}/7] STRUC-ROUTE-I v0.1.2 · {sid}")
        print(f"  route output root: {output_root}")
        def progress(frac, phase, msg):
            print(f"  [{frac*100:6.2f}%] {phase:16s} {msg}")
        try:
            result, run_dir = analyze_project(route_project, output_root, progress)
            if str(result.get("meta", {}).get("version")) != str(cfg["route_i"]["version"]):
                raise ValueError(f"{sid}: unexpected ROUTE-I version")
            rec = extract_one_pscale(cfg, root, s, result, Path(run_dir))
            sample_records.append(rec)
            print(
                f"  P_SCALE n={rec['P_SCALE']['count']:,} mean={rec['P_SCALE']['mean']:.6f} "
                f"status={rec['status']}"
            )
        except ValueError as exc:
            rec = {
                "schema": "UNNS_JHTDB_HIGH_RE_P_SCALE_v0.1",
                "sample": s,
                "status": "UNDERRESOLVED",
                "reason": str(exc),
                "P_SCALE": None,
                "scale_test": None,
                "null_quality": None,
                "scale_structure": None,
            }
            sample_records.append(rec)
            d = root / "ladders" / "route_i" / "jhtdb_high_re" / sid
            d.mkdir(parents=True, exist_ok=True)
            json_write(d / "P_SCALE_RECORD.json", rec)
            print(f"  [UNDERRESOLVED] {exc}")

    rows = []
    for r in sample_records:
        test = r.get("scale_test") or {}
        nq = r.get("null_quality") or {}
        ss = r.get("scale_structure") or {}
        ps = r.get("P_SCALE") or {}
        rows.append({
            "sample_id": r["sample"]["sample_id"],
            "dataset": r["sample"]["dataset"],
            "snapshot": r["sample"]["snapshot"],
            "role": r["sample"]["role"],
            "status": r["status"],
            "reason": r.get("reason"),
            "P_SCALE_n": ps.get("count"),
            "P_SCALE_mean": ps.get("mean"),
            "P_SCALE_min": ps.get("min"),
            "P_SCALE_max": ps.get("max"),
            "scale_edges": ss.get("edges"),
            "scale_source_nodes": ss.get("source_nodes"),
            "branch_fraction_all": ss.get("branch_fraction_all"),
            "merge_fraction_all": ss.get("merge_fraction_all"),
            "null_mean": test.get("null_mean"),
            "null_std": test.get("null_std"),
            "favorable_z": test.get("favorable_z"),
            "p_favorable": test.get("p_favorable"),
            "p_opposing": test.get("p_opposing"),
            "null_mean_mobility": nq.get("mean_mobility_fraction"),
            "null_unique_graph_fraction": nq.get("unique_graph_fraction"),
            "null_real_match_fraction": nq.get("real_graph_match_fraction"),
            "P_SCALE_sha256": ps.get("sha256"),
        })
    summary = pd.DataFrame(rows)
    table_dir = root / "outputs" / "tables" / "high_re_scale"
    table_dir.mkdir(parents=True, exist_ok=True)
    summary_path = table_dir / "HIGH_RE_SCALE_SUMMARY.csv"
    summary.to_csv(summary_path, index=False)

    all_ready = all(r.get("status") == "ANALYZABLE" and r.get("P_SCALE") for r in sample_records)
    stage = {
        "tool": {"name": TOOL, "version": VERSION},
        "status": "SCALE_LADDERS_READY_FOR_STRUC_CHAMBERS" if all_ready else "UNDERRESOLVED",
        "branch": cfg["branch"],
        "source_archive_sha256": verify_record["archive"]["sha256"],
        "samples": sample_records,
        "summary_csv": str(summary_path),
        "next_stage": "Run each P_SCALE.csv independently through STRUC-I v1.0.4 and STRUC-PERC-I v2.5.0 under frozen protocol.",
    }
    record_path = root / "outputs" / "records" / STAGE_REPORT
    json_write(record_path, stage)

    status_path = root / "analysis" / "generalization" / "jhtdb_high_re" / "STAGE_STATUS.json"
    json_write(status_path, {
        "status": stage["status"],
        "stage_report": str(record_path),
        "sample_count": len(sample_records),
    })

    bundle = root / "outputs" / "records" / "HIGH_RE_SCALE_LADDERS.zip"
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as zf:
        for r in sample_records:
            sid = r["sample"]["sample_id"]
            d = root / "ladders" / "route_i" / "jhtdb_high_re" / sid
            if (d / "P_SCALE.csv").exists():
                zf.write(d / "P_SCALE.csv", f"{sid}/P_SCALE.csv")
            if (d / "P_SCALE_RECORD.json").exists():
                zf.write(d / "P_SCALE_RECORD.json", f"{sid}/P_SCALE_RECORD.json")
        zf.write(summary_path, "HIGH_RE_SCALE_SUMMARY.csv")
        zf.write(record_path, STAGE_REPORT)
    stage["ladder_bundle"] = str(bundle)
    stage["ladder_bundle_sha256"] = sha256_file(bundle)
    json_write(record_path, stage)

    if all_ready:
        print("\n[COMPLETE] Seven frozen high-Re P_SCALE ladders are ready.")
        print("Next: STRUC-I v1.0.4 + STRUC-PERC-I v2.5.0, independently per ladder.")
    else:
        print("\n[UNDERRESOLVED] One or more samples did not produce an analyzable P_SCALE ladder.")
        print("Do not reinterpret or retune; inspect the stage report first.")
    print(f"Summary: {summary_path}")
    print(f"Bundle:  {bundle}")
    return stage


def main():
    ap = argparse.ArgumentParser(description="UNNS JHTDB high-Re scale-only stage")
    ap.add_argument("command", choices=["verify", "adapter", "route", "all"])
    args = ap.parse_args()
    cfg, tool_dir, root = load_cfg()
    print(f"{TOOL} v{VERSION}")
    print(f"Project root: {root}")
    print(f"Command: {args.command}\n")
    if args.command == "verify":
        verify_sources(cfg, root, allow_cache=False)
    elif args.command == "adapter":
        run_adapter_stage(cfg, root)
    elif args.command == "route":
        stage = run_route_stage(cfg, root)
        if stage.get("status") != "SCALE_LADDERS_READY_FOR_STRUC_CHAMBERS":
            raise SystemExit(2)
    else:
        verify_sources(cfg, root, allow_cache=False)
        run_adapter_stage(cfg, root)
        stage = run_route_stage(cfg, root)
        if stage.get("status") != "SCALE_LADDERS_READY_FOR_STRUC_CHAMBERS":
            raise SystemExit(2)


if __name__ == "__main__":
    main()

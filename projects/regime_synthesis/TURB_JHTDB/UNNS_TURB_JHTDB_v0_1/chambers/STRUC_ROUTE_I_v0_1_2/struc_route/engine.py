from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import os
import shutil
import time
import numpy as np
import pandas as pd

from .io import load_project, normalize_and_validate
from .rules import apply_relation_rule
from .metrics import axis_metrics, stitching_metrics, family_transitions
from .nulls import rewire_degree_preserving, graph_signature
from .export import write_json, export_ladders
from .postrun import stitch_physics_analysis

VERSION = "0.1.2"
INSTRUMENT = "STRUC-ROUTE-I"

EVIDENCE_SPECS = {
    "scale_persistence": ("scale.persistence_mean_sources", "high"),
    "time_persistence": ("time.persistence_mean_sources", "high"),
    "stitch_defect": ("stitch.mean_defect", "low"),
}

DESCRIPTIVE_ONLY_SPECS = {
    "scale_entropy": (
        "scale.entropy_mean_sources",
        "Current endpoint-rewiring null preserves each source's outgoing edge "
        "weight multiset, so source route entropy is invariant by construction."
    ),
    "time_entropy": (
        "time.entropy_mean_sources",
        "Current endpoint-rewiring null preserves each source's outgoing edge "
        "weight multiset, so source route entropy is invariant by construction."
    ),
}

def _sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def _get_nested(d, path):
    cur = d
    for p in path.split("."):
        if cur is None or p not in cur:
            return None
        cur = cur[p]
    return cur

def _run_metrics(manifest, objects, edges):
    weight_col = manifest.get("edge_weight_column", "confidence")
    object_weight = manifest.get("object_weight_column")
    scale_sum, scale_nodes, scale_trans = axis_metrics(
        objects, edges, "scale", weight_col, object_weight
    )
    time_sum, time_nodes, time_trans = axis_metrics(
        objects, edges, "time", weight_col, object_weight
    )
    stitch_sum, stitch_nodes, squares = stitching_metrics(
        objects, scale_trans, time_trans
    )
    nodes = objects.copy()
    for part in (scale_nodes, time_nodes, stitch_nodes[["node_id", "stitch_defect"]] if len(stitch_nodes) else None):
        if part is not None and len(part):
            nodes = nodes.merge(part, on="node_id", how="left")
    summary = {"scale": scale_sum, "time": time_sum, "stitch": stitch_sum}
    return summary, nodes, squares

def _empirical_test(real, null_vals, direction):
    arr = np.array([x for x in null_vals if x is not None and np.isfinite(x)], dtype=float)
    if real is None or not np.isfinite(real) or len(arr) == 0:
        return None
    mu = float(np.mean(arr))
    sd = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
    if direction == "high":
        z = (real - mu) / sd if sd > 0 else (math.inf if real > mu else 0.0)
        fav = (1 + int(np.sum(arr >= real))) / (len(arr) + 1)
        opp = (1 + int(np.sum(arr <= real))) / (len(arr) + 1)
    else:
        z = (mu - real) / sd if sd > 0 else (math.inf if real < mu else 0.0)
        fav = (1 + int(np.sum(arr <= real))) / (len(arr) + 1)
        opp = (1 + int(np.sum(arr >= real))) / (len(arr) + 1)
    return {
        "real": float(real),
        "null_mean": mu,
        "null_std": sd,
        "favorable_z": float(z),
        "p_favorable": float(fav),
        "p_opposing": float(opp),
        "n_null": int(len(arr)),
        "direction": direction,
    }

def _apply_analysis_filter(manifest, objects, relations):
    """
    Optional analysis-only structural filter.

    Used for sensitivity tests without re-running the physical adapter.
    The source object/edge tables remain unchanged; the operative graph is
    explicitly filtered and the filter is exported in RESULT/RUN.
    """
    cfg = manifest.get("analysis_filter") or {}
    if not cfg:
        return objects, relations, {
            "applied": False,
            "config": None,
            "objects_before": int(len(objects)),
            "objects_after": int(len(objects)),
            "relations_before": int(len(relations)),
            "relations_after": int(len(relations)),
        }

    keep = pd.Series(True, index=objects.index)
    if "max_scale_idx" in cfg:
        keep &= objects["scale_idx"] <= int(cfg["max_scale_idx"])
    if "min_scale_idx" in cfg:
        keep &= objects["scale_idx"] >= int(cfg["min_scale_idx"])
    if "max_time_idx" in cfg:
        keep &= objects["time_idx"] <= int(cfg["max_time_idx"])
    if "min_time_idx" in cfg:
        keep &= objects["time_idx"] >= int(cfg["min_time_idx"])

    filtered_objects = objects.loc[keep].copy().reset_index(drop=True)
    ids = set(filtered_objects["node_id"].astype(str))
    filtered_relations = relations.loc[
        relations["src_id"].astype(str).isin(ids)
        & relations["dst_id"].astype(str).isin(ids)
    ].copy().reset_index(drop=True)

    if len(filtered_objects) == 0:
        raise ValueError("analysis_filter removed all objects.")
    if len(filtered_relations) == 0:
        raise ValueError("analysis_filter removed all relations.")

    return filtered_objects, filtered_relations, {
        "applied": True,
        "config": cfg,
        "objects_before": int(len(objects)),
        "objects_after": int(len(filtered_objects)),
        "relations_before": int(len(relations)),
        "relations_after": int(len(filtered_relations)),
    }


def _publish(publish, payload):
    if publish is not None:
        publish(payload)


def analyze_project(project_dir: str | Path, output_root: str | Path,
                    progress=None, publish=None):
    project_dir = Path(project_dir)
    output_root = Path(output_root)
    manifest, objects, relations, families, source_paths = load_project(project_dir)
    objects, relations, families = normalize_and_validate(
        manifest, objects, relations, families
    )
    objects, relations, filter_record = _apply_analysis_filter(
        manifest, objects, relations
    )

    if progress:
        progress(0.05, "VALIDATION", f"{len(objects):,} objects · {len(relations):,} supplied relations")

    eligible = apply_relation_rule(relations, manifest.get("relation_rule"))
    if len(eligible) == 0:
        raise ValueError("Relation rule rejected all relations.")

    if progress:
        progress(0.10, "ELIGIBILITY", f"{len(eligible):,} eligible relations")

    real_summary, node_metrics, squares = _run_metrics(manifest, objects, eligible)

    real_payload = {
        "stage": "REAL_GRAPH_COMPLETE",
        "provisional": True,
        "input": {
            "n_objects": int(len(objects)),
            "n_relations_supplied": int(len(relations)),
            "n_relations_eligible": int(len(eligible)),
            "scale_layers": int(objects["scale_idx"].nunique()),
            "time_layers": int(objects["time_idx"].nunique()),
            "analysis_filter": filter_record,
        },
        "structure": real_summary,
        "evidence_status": "PENDING_NULL_ENSEMBLE",
    }
    _publish(publish, real_payload)

    if progress:
        progress(0.22, "REAL GRAPH", "Persistence · branching · entropy · stitching complete")

    null_cfg = manifest.get("nulls", {}) or {}
    null_count = int(null_cfg.get("count", 100))
    seed = int(null_cfg.get("seed", 20260904))
    swaps = float(null_cfg.get("swaps_per_edge", 5.0))
    null_rows = []
    real_signature = graph_signature(eligible)
    null_started = time.time()

    for i in range(null_count):
        rew, mobility = rewire_degree_preserving(
            objects, eligible, seed + i + 1, swaps
        )
        s, _, _ = _run_metrics(manifest, objects, rew)
        row = {
            "null_index": i + 1,
            "seed": seed + i + 1,
            "swap_attempts": mobility["attempts"],
            "swap_accepted": mobility["accepted"],
            "mobility_fraction": mobility["mobility_fraction"],
            "mobile_groups": mobility["mobile_groups"],
            "transition_groups": mobility["transition_groups"],
            "graph_signature": mobility["graph_signature"],
            "matches_real_graph": mobility["graph_signature"] == real_signature,
        }
        for key, (path, _) in EVIDENCE_SPECS.items():
            row[key] = _get_nested(s, path)
        null_rows.append(row)

        elapsed = time.time() - null_started
        done = i + 1
        rate = elapsed / done if done else None
        eta = rate * (null_count - done) if rate is not None else None
        mean_mobility_so_far = float(np.mean(
            [r["mobility_fraction"] for r in null_rows]
        ))
        _publish(publish, {
            "stage": "NULL_PROGRESS",
            "null_index": done,
            "null_count": null_count,
            "accepted_swaps_current": int(mobility["accepted"]),
            "mobility_current": float(mobility["mobility_fraction"]),
            "mean_mobility_so_far": mean_mobility_so_far,
            "elapsed_seconds": float(elapsed),
            "eta_seconds": float(eta) if eta is not None else None,
        })

        if progress and (i == 0 or (i + 1) % max(1, null_count // 20) == 0):
            progress(
                0.22 + 0.58 * (i + 1) / max(1, null_count),
                "NULL ENSEMBLE",
                f"{i+1}/{null_count} · accepted swaps={mobility['accepted']}"
            )

    null_df = pd.DataFrame(null_rows)

    # Null-mobility diagnostics.
    mobility_cfg = null_cfg.get("mobility", {}) or {}
    min_mean_mobility = float(mobility_cfg.get("min_mean_fraction", 0.01))
    min_unique_fraction = float(mobility_cfg.get("min_unique_graph_fraction", 0.10))
    max_real_match_fraction = float(mobility_cfg.get("max_real_match_fraction", 0.90))

    if len(null_df):
        total_attempts = int(null_df["swap_attempts"].sum())
        total_accepted = int(null_df["swap_accepted"].sum())
        mean_mobility = float(null_df["mobility_fraction"].mean())
        median_mobility = float(null_df["mobility_fraction"].median())
        zero_mobility_fraction = float((null_df["swap_accepted"] == 0).mean())
        unique_graphs = int(null_df["graph_signature"].nunique())
        unique_graph_fraction = float(unique_graphs / len(null_df))
        real_match_fraction = float(null_df["matches_real_graph"].mean())
    else:
        total_attempts = total_accepted = unique_graphs = 0
        mean_mobility = median_mobility = zero_mobility_fraction = 0.0
        unique_graph_fraction = real_match_fraction = 0.0

    null_flags = []
    if total_accepted == 0:
        null_flags.append("NULL_ENSEMBLE_IMMOBILE")
    if mean_mobility < min_mean_mobility:
        if "NULL_ENSEMBLE_IMMOBILE" not in null_flags:
            null_flags.append("NULL_ENSEMBLE_IMMOBILE")
    if unique_graph_fraction < min_unique_fraction:
        null_flags.append("NULL_ENSEMBLE_LOW_DIVERSITY")
    if real_match_fraction > max_real_match_fraction:
        null_flags.append("NULL_ENSEMBLE_REAL_CLONE_DOMINATED")

    null_quality = {
        "model": "DIRECTED_LAYER_DEGREE_PRESERVING_ENDPOINT_SWAPS",
        "requested_nulls": null_count,
        "swap_attempts_total": total_attempts,
        "swap_accepted_total": total_accepted,
        "mean_mobility_fraction": mean_mobility,
        "median_mobility_fraction": median_mobility,
        "zero_mobility_null_fraction": zero_mobility_fraction,
        "unique_graphs": unique_graphs,
        "unique_graph_fraction": unique_graph_fraction,
        "real_graph_match_fraction": real_match_fraction,
        "thresholds": {
            "min_mean_mobility_fraction": min_mean_mobility,
            "min_unique_graph_fraction": min_unique_fraction,
            "max_real_match_fraction": max_real_match_fraction,
        },
        "flags": null_flags,
        "usable_for_inference": len(null_flags) == 0,
    }

    inference = manifest.get("inference", {}) or {}
    alpha = float(inference.get("alpha", 0.05))
    min_nulls = int(inference.get("min_nulls", 20))

    tests = {}
    supportive = 0
    opposing = 0
    eligible_tests = 0
    for key, (path, direction) in EVIDENCE_SPECS.items():
        real = _get_nested(real_summary, path)
        vals = null_df[key].tolist() if key in null_df.columns else []
        t = _empirical_test(real, vals, direction)
        tests[key] = t
        if t and t["n_null"] >= min_nulls:
            eligible_tests += 1
            supportive += int(t["p_favorable"] <= alpha)
            opposing += int(t["p_opposing"] <= alpha)

    descriptive_only = {}
    for key, (path, reason) in DESCRIPTIVE_ONLY_SPECS.items():
        descriptive_only[key] = {
            "real": _get_nested(real_summary, path),
            "role": "DESCRIPTIVE_ONLY",
            "reason": reason,
        }

    if eligible_tests < 2 or null_count < min_nulls or not null_quality["usable_for_inference"]:
        verdict = "UNDERRESOLVED"
    elif supportive >= 2 and opposing == 0:
        verdict = "CONSTRAINED_ROUTING"
    elif supportive == 0 and opposing == 0:
        verdict = "NULL_LIKE_ROUTING"
    else:
        verdict = "MIXED_ROUTING"

    tags = list(null_quality["flags"])
    for key, t in tests.items():
        if t and t["p_favorable"] <= alpha:
            tags.append({
                "scale_persistence": "PERSISTENT_SCALE",
                "time_persistence": "PERSISTENT_TIME",
                "scale_entropy": "CONSTRAINED_SCALE_ENTROPY",
                "time_entropy": "CONSTRAINED_TIME_ENTROPY",
                "stitch_defect": "LOW_STITCH_DEFECT",
            }[key])

    fam_rows = family_transitions(objects, eligible)

    run_seed = manifest.get("run_id")
    if run_seed:
        safe = "".join(c if c.isalnum() or c in "_-" else "_" for c in str(run_seed))
    else:
        safe = "route"
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_id = f"{safe}_{ts}"
    run_dir = output_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    # Input hashes.
    hashes = {}
    for k, p in source_paths.items():
        if p and Path(p).exists():
            hashes[k] = {"path": p, "sha256": _sha256(Path(p))}

    result = {
        "meta": {
            "instrument": INSTRUMENT,
            "version": VERSION,
            "run_id": run_id,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "project_name": manifest.get("project_name"),
            "domain": manifest.get("domain", "GENERIC"),
        },
        "model": {
            "graph": "DIRECTED_LAYERED_SCALE_TIME",
            "strict_adjacent": bool(manifest.get("strict_adjacent", True)),
            "relation_rule": manifest.get("relation_rule", {"mode":"all","conditions":[]}),
            "edge_weight_column": manifest.get("edge_weight_column", "confidence"),
            "object_weight_column": manifest.get("object_weight_column"),
            "stitching": "JSD(ST,TS)/ln(2)",
            "null_model": "DIRECTED_LAYER_DEGREE_PRESERVING_ENDPOINT_SWAPS",
            "composite_score": None,
            "entropy_inference_role": (
                "DESCRIPTIVE_ONLY under the current endpoint-rewiring null; "
                "outgoing source edge-weight multisets are preserved."
            ),
        },
        "input": {
            "n_objects": int(len(objects)),
            "n_relations_supplied": int(len(relations)),
            "n_relations_eligible": int(len(eligible)),
            "scale_layers": int(objects["scale_idx"].nunique()),
            "time_layers": int(objects["time_idx"].nunique()),
            "hashes": hashes,
            "analysis_filter": filter_record,
        },
        "structure": real_summary,
        "null_quality": null_quality,
        "evidence": {
            "alpha": alpha,
            "min_nulls": min_nulls,
            "null_count": null_count,
            "eligible_tests": eligible_tests,
            "supportive_tests": supportive,
            "opposing_tests": opposing,
            "tests": tests,
            "descriptive_only": descriptive_only,
        },
        "verdict": {
            "class": verdict,
            "tags": tags,
            "rule": (
                "UNDERRESOLVED if <2 inferential metrics, <min_nulls, or null ensemble fails mobility/diversity checks; "
                "CONSTRAINED_ROUTING if >=2 favorable tests and 0 opposing; "
                "NULL_LIKE_ROUTING if 0 favorable and 0 opposing; otherwise MIXED_ROUTING."
            ),
        },
        "family_transitions": fam_rows,
    }

    run_record = {
        "instrument": INSTRUMENT,
        "version": VERSION,
        "run_id": run_id,
        "manifest": manifest,
        "source_hashes": hashes,
        "run_status": "COMPLETE",
    }

    # Compact human-readable summary.
    summary_rows = []
    for axis in ("scale", "time"):
        s = real_summary[axis]
        for k in (
            "edges", "layers", "source_nodes", "persistence_mean_sources",
            "persistence_p90_sources", "branch_fraction_all", "merge_fraction_all",
            "entropy_mean_sources", "conservation_mean"
        ):
            summary_rows.append({"section": axis, "metric": k, "value": s.get(k)})
    for k, v in real_summary["stitch"].items():
        summary_rows.append({"section": "stitch", "metric": k, "value": v})
    for k in (
        "swap_attempts_total", "swap_accepted_total", "mean_mobility_fraction",
        "median_mobility_fraction", "zero_mobility_null_fraction",
        "unique_graphs", "unique_graph_fraction", "real_graph_match_fraction"
    ):
        summary_rows.append({"section": "null_quality", "metric": k, "value": null_quality.get(k)})
    summary_rows.append({"section": "null_quality", "metric": "flags", "value": "|".join(null_quality["flags"])})
    summary_rows.append({"section": "verdict", "metric": "class", "value": verdict})
    summary_df = pd.DataFrame(summary_rows)

    # Exploratory physical association of the high-D_square tail.
    # It does not alter the chamber verdict.
    stitch_physics = None
    stitch_events = pd.DataFrame()
    stitch_by_time = pd.DataFrame()
    stitch_by_scale = pd.DataFrame()
    try:
        viscosity = None
        adapter_meta = manifest.get("adapter") or {}
        if adapter_meta.get("viscosity") is not None:
            viscosity = float(adapter_meta["viscosity"])
        stitch_physics, stitch_events, stitch_by_time, stitch_by_scale = (
            stitch_physics_analysis(
                node_metrics,
                viscosity=viscosity,
                permutations=1000,
            )
        )
    except Exception as exc:
        stitch_physics = {
            "status": "NOT_AVAILABLE",
            "reason": str(exc),
        }

    result["stitch_physics"] = stitch_physics

    # Persist exact eligible graph and node metrics.
    # RUN_WINDOWS requires pyarrow, so normal chamber runs are Parquet.
    # CSV fallback keeps the scientific engine testable in restricted Python
    # environments where an optional Parquet engine is unavailable.
    def write_analysis_table(df, parquet_name, csv_name):
        try:
            df.to_parquet(run_dir / parquet_name, index=False)
            return parquet_name
        except ImportError:
            df.to_csv(run_dir / csv_name, index=False)
            return csv_name

    node_table_file = write_analysis_table(node_metrics, "NODES.parquet", "NODES.csv")
    edge_table_file = write_analysis_table(eligible, "EDGES.parquet", "EDGES.csv")
    square_table_file = write_analysis_table(squares, "SQUARES.parquet", "SQUARES.csv")
    result["meta"]["table_files"] = {
        "nodes": node_table_file,
        "edges": edge_table_file,
        "squares": square_table_file,
    }
    null_df.to_csv(run_dir / "NULLS.csv", index=False)
    summary_df.to_csv(run_dir / "SUMMARY.csv", index=False)
    if len(stitch_events):
        stitch_events.to_csv(run_dir / "STITCH_TAIL.csv", index=False)
    if len(stitch_by_time):
        stitch_by_time.to_csv(run_dir / "STITCH_BY_TIME.csv", index=False)
    if len(stitch_by_scale):
        stitch_by_scale.to_csv(run_dir / "STITCH_BY_SCALE.csv", index=False)
    if stitch_physics is not None:
        write_json(run_dir / "STITCH_PHYSICS.json", stitch_physics)
    write_json(run_dir / "RESULT.json", result)
    write_json(run_dir / "RUN.json", run_record)
    export_ladders(run_dir, node_metrics, squares)

    if progress:
        progress(1.0, "COMPLETE", f"{verdict} · {run_id}")

    return result, run_dir

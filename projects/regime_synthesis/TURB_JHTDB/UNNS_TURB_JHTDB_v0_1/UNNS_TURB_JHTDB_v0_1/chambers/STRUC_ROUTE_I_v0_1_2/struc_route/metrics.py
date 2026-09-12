from __future__ import annotations
from collections import defaultdict
import math
import numpy as np
import pandas as pd

LN2 = math.log(2.0)

def _weights(edges: pd.DataFrame, weight_col: str | None):
    if weight_col and weight_col in edges.columns:
        w = pd.to_numeric(edges[weight_col], errors="coerce").fillna(1.0).to_numpy(float)
        w = np.where(w > 0, w, 0.0)
        return w
    return np.ones(len(edges), dtype=float)

def _axis_adjacency(objects, edges, axis, weight_col=None):
    ed = edges.loc[edges["axis"] == axis].copy()
    w = _weights(ed, weight_col)
    adj = defaultdict(list)
    rev = defaultdict(list)
    for (src, dst), ww in zip(ed[["src_id", "dst_id"]].itertuples(index=False, name=None), w):
        adj[str(src)].append((str(dst), float(ww)))
        rev[str(dst)].append((str(src), float(ww)))
    return ed, adj, rev

def _normalized_out(adj):
    out = {}
    for src, pairs in adj.items():
        total = sum(max(w, 0.0) for _, w in pairs)
        if total <= 0:
            p = 1.0 / len(pairs) if pairs else 0
            out[src] = [(d, p) for d, _ in pairs]
        else:
            out[src] = [(d, max(w, 0.0) / total) for d, w in pairs]
    return out

def axis_metrics(objects: pd.DataFrame, edges: pd.DataFrame, axis: str,
                 weight_col: str | None = None,
                 object_weight_col: str | None = None):
    ed, adj, rev = _axis_adjacency(objects, edges, axis, weight_col)
    idx_col = "scale_idx" if axis == "scale" else "time_idx"
    n_layers = int(objects[idx_col].nunique())
    layer_span = max(1, n_layers - 1)

    # Layered DAG: process nodes in descending layer index.
    node_layer = objects.set_index("node_id")[idx_col].to_dict()
    ordered = sorted(objects["node_id"].astype(str), key=lambda n: node_layer[n], reverse=True)
    reach = {}
    for n in ordered:
        children = [d for d, _ in adj.get(n, [])]
        reach[n] = max([1 + reach.get(d, 0) for d in children], default=0)

    persistence = {n: reach[n] / layer_span for n in ordered}
    source_nodes = [n for n in ordered if n in adj]
    p_all = np.array(list(persistence.values()), dtype=float) if persistence else np.array([])
    p_src = np.array([persistence[n] for n in source_nodes], dtype=float) if source_nodes else np.array([])

    outdeg = {n: len(adj.get(n, [])) for n in ordered}
    indeg = {n: len(rev.get(n, [])) for n in ordered}
    branch = {n: max(outdeg[n] - 1, 0) for n in ordered}
    merge = {n: max(indeg[n] - 1, 0) for n in ordered}

    nout = _normalized_out(adj)
    entropy = {}
    for n, pairs in nout.items():
        d = len(pairs)
        if d <= 1:
            entropy[n] = 0.0
            continue
        ps = np.array([p for _, p in pairs if p > 0], dtype=float)
        h = -float(np.sum(ps * np.log(ps))) / math.log(d)
        entropy[n] = h

    conservation = {}
    if object_weight_col and object_weight_col in objects.columns:
        obj_w = pd.to_numeric(objects.set_index("node_id")[object_weight_col], errors="coerce").to_dict()
        # Attribute each child weight across incoming parents in proportion to incoming edge weights.
        incoming_sum = {}
        for dst, pairs in rev.items():
            incoming_sum[dst] = sum(max(w, 0.0) for _, w in pairs)
        for src, pairs in adj.items():
            parent_w = obj_w.get(src)
            if parent_w is None or not np.isfinite(parent_w) or parent_w <= 0:
                continue
            routed = 0.0
            for dst, ew in pairs:
                child_w = obj_w.get(dst)
                if child_w is None or not np.isfinite(child_w):
                    continue
                denom = incoming_sum.get(dst, 0.0)
                share = (max(ew, 0.0) / denom) if denom > 0 else 0.0
                routed += child_w * share
            conservation[src] = routed / parent_w

    def q(arr, x):
        return float(np.quantile(arr, x)) if arr.size else None

    summary = {
        "axis": axis,
        "nodes": int(len(objects)),
        "edges": int(len(ed)),
        "layers": n_layers,
        "source_nodes": int(len(source_nodes)),
        "persistence_mean_all": float(np.mean(p_all)) if p_all.size else None,
        "persistence_mean_sources": float(np.mean(p_src)) if p_src.size else None,
        "persistence_p50_sources": q(p_src, .50),
        "persistence_p90_sources": q(p_src, .90),
        "persistence_max": float(np.max(p_all)) if p_all.size else None,
        "branch_fraction_all": float(np.mean([v > 0 for v in branch.values()])) if branch else None,
        "merge_fraction_all": float(np.mean([v > 0 for v in merge.values()])) if merge else None,
        "mean_out_degree_sources": float(np.mean([outdeg[n] for n in source_nodes])) if source_nodes else None,
        "entropy_mean_sources": float(np.mean(list(entropy.values()))) if entropy else None,
        "entropy_p90_sources": q(np.array(list(entropy.values()), dtype=float), .90) if entropy else None,
        "conservation_mean": float(np.mean(list(conservation.values()))) if conservation else None,
    }

    node_df = pd.DataFrame({
        "node_id": ordered,
        f"{axis}_persistence": [persistence[n] for n in ordered],
        f"{axis}_out_degree": [outdeg[n] for n in ordered],
        f"{axis}_in_degree": [indeg[n] for n in ordered],
        f"{axis}_branching": [branch[n] for n in ordered],
        f"{axis}_merging": [merge[n] for n in ordered],
        f"{axis}_entropy": [entropy.get(n, np.nan) for n in ordered],
        f"{axis}_conservation": [conservation.get(n, np.nan) for n in ordered],
    })
    return summary, node_df, nout

def _dist_after_two(start, first, second):
    result = defaultdict(float)
    for mid, p1 in first.get(start, []):
        for dst, p2 in second.get(mid, []):
            result[dst] += p1 * p2
    total = sum(result.values())
    if total > 0:
        for k in list(result):
            result[k] /= total
    return dict(result)

def jsd_norm(p: dict, q: dict):
    keys = set(p) | set(q)
    if not keys:
        return None
    pv = np.array([p.get(k, 0.0) for k in keys], dtype=float)
    qv = np.array([q.get(k, 0.0) for k in keys], dtype=float)
    if pv.sum() <= 0 or qv.sum() <= 0:
        return None
    pv /= pv.sum()
    qv /= qv.sum()
    m = 0.5 * (pv + qv)
    def kl(a, b):
        mask = a > 0
        return float(np.sum(a[mask] * np.log(a[mask] / b[mask])))
    return (0.5 * kl(pv, m) + 0.5 * kl(qv, m)) / LN2

def stitching_metrics(objects: pd.DataFrame, scale_trans: dict, time_trans: dict):
    loc = objects.set_index("node_id")[["scale_idx", "time_idx"]].to_dict("index")
    by_cell = defaultdict(list)
    node_rows = []

    for src in objects["node_id"].astype(str):
        if src not in scale_trans or src not in time_trans:
            continue
        pst = _dist_after_two(src, scale_trans, time_trans)
        pts = _dist_after_two(src, time_trans, scale_trans)
        d = jsd_norm(pst, pts)
        if d is None:
            continue
        s = int(loc[src]["scale_idx"])
        t = int(loc[src]["time_idx"])
        by_cell[(s, t)].append(d)
        node_rows.append({
            "node_id": src, "scale_idx": s, "time_idx": t,
            "stitch_defect": d
        })

    cell_rows = []
    for (s, t), vals in sorted(by_cell.items()):
        cell_rows.append({
            "scale_idx": s,
            "time_idx": t,
            "n_sources": len(vals),
            "mean_defect": float(np.mean(vals)),
            "p90_defect": float(np.quantile(vals, .90)),
            "max_defect": float(np.max(vals)),
        })
    node_df = pd.DataFrame(node_rows)
    cell_df = pd.DataFrame(cell_rows)
    vals = node_df["stitch_defect"].to_numpy(float) if len(node_df) else np.array([])
    summary = {
        "eligible_sources": int(len(node_df)),
        "cells": int(len(cell_df)),
        "mean_defect": float(np.mean(vals)) if vals.size else None,
        "p90_defect": float(np.quantile(vals, .90)) if vals.size else None,
        "max_defect": float(np.max(vals)) if vals.size else None,
    }
    return summary, node_df, cell_df

def family_transitions(objects: pd.DataFrame, edges: pd.DataFrame):
    if "family_id" not in objects.columns:
        return []
    fam = objects.set_index("node_id")["family_id"].to_dict()
    counts = defaultdict(int)
    totals = defaultdict(int)
    for src, dst, axis in edges[["src_id", "dst_id", "axis"]].itertuples(index=False, name=None):
        a, b = fam.get(str(src)), fam.get(str(dst))
        if pd.isna(a) or pd.isna(b):
            continue
        key = (str(axis), str(a), str(b))
        counts[key] += 1
        totals[(str(axis), str(a))] += 1
    rows = []
    for (axis, a, b), c in sorted(counts.items()):
        rows.append({
            "axis": axis,
            "src_family": a,
            "dst_family": b,
            "count": c,
            "probability": c / totals[(axis, a)]
        })
    return rows

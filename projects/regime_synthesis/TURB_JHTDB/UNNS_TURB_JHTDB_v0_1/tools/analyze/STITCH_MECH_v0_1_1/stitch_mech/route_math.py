from __future__ import annotations
from collections import defaultdict
import math
import numpy as np
import pandas as pd

LN2 = math.log(2.0)


def _weights(edges: pd.DataFrame, weight_col: str | None):
    if weight_col and weight_col in edges.columns:
        w = pd.to_numeric(edges[weight_col], errors="coerce").fillna(1.0).to_numpy(float)
        return np.where(w > 0, w, 0.0)
    return np.ones(len(edges), dtype=float)


def _axis_adjacency(objects, edges, axis, weight_col=None):
    ed = edges.loc[edges["axis"] == axis].copy()
    w = _weights(ed, weight_col)
    adj = defaultdict(list)
    rev = defaultdict(list)
    for (src, dst), ww in zip(
        ed[["src_id", "dst_id"]].itertuples(index=False, name=None), w
    ):
        adj[str(src)].append((str(dst), float(ww)))
        rev[str(dst)].append((str(src), float(ww)))
    return ed, adj, rev


def _normalized_out(adj):
    out = {}
    for src, pairs in adj.items():
        total = sum(max(w, 0.0) for _, w in pairs)
        if total <= 0:
            p = 1.0 / len(pairs) if pairs else 0.0
            out[src] = [(d, p) for d, _ in pairs]
        else:
            out[src] = [(d, max(w, 0.0) / total) for d, w in pairs]
    return out


def axis_metrics(objects, edges, axis, weight_col="confidence", object_weight_col="weight"):
    ed, adj, rev = _axis_adjacency(objects, edges, axis, weight_col)
    idx_col = "scale_idx" if axis == "scale" else "time_idx"
    n_layers = int(objects[idx_col].nunique())
    layer_span = max(1, n_layers - 1)

    node_layer = objects.set_index("node_id")[idx_col].to_dict()
    ordered = sorted(
        objects["node_id"].astype(str),
        key=lambda n: node_layer[n],
        reverse=True
    )
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

    nout = _normalized_out(adj)

    def q(arr, x):
        return float(np.quantile(arr, x)) if arr.size else None

    summary = {
        "axis": axis,
        "nodes": int(len(objects)),
        "edges": int(len(ed)),
        "layers": n_layers,
        "source_nodes": int(len(source_nodes)),
        "persistence_mean_sources": float(np.mean(p_src)) if p_src.size else None,
        "persistence_p90_sources": q(p_src, .90),
        "persistence_max": float(np.max(p_all)) if p_all.size else None,
        "branch_fraction_all": float(np.mean([outdeg[n] > 1 for n in ordered])) if ordered else None,
        "merge_fraction_all": float(np.mean([indeg[n] > 1 for n in ordered])) if ordered else None,
    }

    node_df = pd.DataFrame({
        "node_id": ordered,
        f"{axis}_persistence": [persistence[n] for n in ordered],
        f"{axis}_out_degree": [outdeg[n] for n in ordered],
        f"{axis}_in_degree": [indeg[n] for n in ordered],
        f"{axis}_branching": [max(outdeg[n] - 1, 0) for n in ordered],
        f"{axis}_merging": [max(indeg[n] - 1, 0) for n in ordered],
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


def stitching_metrics(objects, scale_trans, time_trans):
    loc = objects.set_index("node_id")[["scale_idx", "time_idx"]].to_dict("index")
    node_rows = []
    for src in objects["node_id"].astype(str):
        if src not in scale_trans or src not in time_trans:
            continue
        pst = _dist_after_two(src, scale_trans, time_trans)
        pts = _dist_after_two(src, time_trans, scale_trans)
        d = jsd_norm(pst, pts)
        if d is None:
            continue
        node_rows.append({
            "node_id": src,
            "scale_idx": int(loc[src]["scale_idx"]),
            "time_idx": int(loc[src]["time_idx"]),
            "stitch_defect": float(d),
        })
    node_df = pd.DataFrame(node_rows)
    vals = node_df["stitch_defect"].to_numpy(float) if len(node_df) else np.array([])
    return {
        "eligible_sources": int(len(node_df)),
        "mean_defect": float(np.mean(vals)) if vals.size else None,
        "p90_defect": float(np.quantile(vals, .90)) if vals.size else None,
        "max_defect": float(np.max(vals)) if vals.size else None,
    }, node_df


def run_metrics(objects, edges, edge_weight_col="confidence", object_weight_col="weight"):
    ss, sn, st = axis_metrics(objects, edges, "scale", edge_weight_col, object_weight_col)
    ts, tn, tt = axis_metrics(objects, edges, "time", edge_weight_col, object_weight_col)
    ds, dn = stitching_metrics(objects, st, tt)
    return {
        "scale_persistence": ss["persistence_mean_sources"],
        "time_persistence": ts["persistence_mean_sources"],
        "stitch_defect": ds["mean_defect"],
        "stitch_p90": ds["p90_defect"],
        "stitch_max": ds["max_defect"],
        "stitch_n": ds["eligible_sources"],
    }, sn, tn, dn

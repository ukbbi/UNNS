from __future__ import annotations

import hashlib
import random
import pandas as pd


def graph_signature(edges: pd.DataFrame) -> str:
    """
    Stable signature of the operative directed layered graph.

    Only structural edge identity is hashed:
        axis | src_id | dst_id

    Relation weights/features are deliberately excluded because the null model
    rewires ancestry while preserving the supplied per-edge metadata rows.
    """
    triples = sorted(
        (str(a), str(s), str(d))
        for s, d, a in edges[["src_id", "dst_id", "axis"]].itertuples(
            index=False, name=None
        )
    )
    payload = "\n".join(f"{a}|{s}|{d}" for a, s, d in triples).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def rewire_degree_preserving(
    objects: pd.DataFrame,
    edges: pd.DataFrame,
    seed: int,
    swaps_per_edge: float = 5.0,
):
    """
    Directed endpoint swaps within each physical transition layer.

        a -> x, b -> y   =>   a -> y, b -> x

    This preserves:
    - axis;
    - physical transition layer;
    - source out-degree;
    - destination in-degree;
    - total edge count.

    Returns:
        rewired_edges, diagnostics

    diagnostics contains the number of attempted and accepted swaps so the
    caller can determine whether the null ensemble was actually mobile.
    """
    rng = random.Random(seed)
    out = edges.copy().reset_index(drop=True)
    loc = objects.set_index("node_id")[["scale_idx", "time_idx"]].to_dict("index")

    groups = {}
    for i, e in out.iterrows():
        src = str(e["src_id"])
        axis = str(e["axis"])
        L = loc[src]
        key = (axis, int(L["scale_idx"]), int(L["time_idx"]))
        groups.setdefault(key, []).append(i)

    attempts_total = 0
    accepted_total = 0
    group_rows = []

    for key, inds in groups.items():
        if len(inds) < 2:
            group_rows.append({
                "group": key,
                "edges": len(inds),
                "attempts": 0,
                "accepted": 0,
                "mobility_fraction": 0.0,
            })
            continue

        pairs = {
            (str(out.at[i, "src_id"]), str(out.at[i, "dst_id"]))
            for i in inds
        }
        attempts = max(10, int(swaps_per_edge * len(inds)))
        accepted = 0

        for _ in range(attempts):
            attempts_total += 1
            i, j = rng.sample(inds, 2)
            a, x = str(out.at[i, "src_id"]), str(out.at[i, "dst_id"])
            b, y = str(out.at[j, "src_id"]), str(out.at[j, "dst_id"])

            # A swap with the same source or same destination changes nothing.
            if a == b or x == y:
                continue

            p1, p2 = (a, y), (b, x)

            # Avoid duplicate edges.
            if p1 in pairs or p2 in pairs:
                continue

            pairs.discard((a, x))
            pairs.discard((b, y))
            pairs.add(p1)
            pairs.add(p2)

            out.at[i, "dst_id"] = y
            out.at[j, "dst_id"] = x
            accepted += 1
            accepted_total += 1

        group_rows.append({
            "group": key,
            "edges": len(inds),
            "attempts": attempts,
            "accepted": accepted,
            "mobility_fraction": accepted / attempts if attempts else 0.0,
        })

    diagnostics = {
        "attempts": int(attempts_total),
        "accepted": int(accepted_total),
        "mobility_fraction": (
            float(accepted_total / attempts_total) if attempts_total else 0.0
        ),
        "transition_groups": int(len(groups)),
        "mobile_groups": int(sum(1 for g in group_rows if g["accepted"] > 0)),
        "group_diagnostics": group_rows,
        "graph_signature": graph_signature(out),
    }
    return out, diagnostics

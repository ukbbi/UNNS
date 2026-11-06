"""E11 -- source-divisibility filtration of the two anchor contents (T18): all regimes, all Hasse covers, the exact event record of each cover
(faces born by dimension/type, delta f, delta rank, delta beta, accounting identity, inclusion), classification into genuine
homology transitions and cell-structure-only events, and the fate of the anchor's 2-cycle z in every regime containing it (T21 data)."""
import json
import os
import time
from collections import Counter
import _path
import threshold_closure as tc
import cell_boundary as cb
import history_complex as hc
import face_threshold as ft
import source_filtration as sf
import E10_h2


def classify(ev):
    db = ev["delta_betti"]
    if any(db):
        return "homology_transition"
    if ev["born"]:
        dr3 = ev["delta_rank"][2] if len(ev["delta_rank"]) > 2 else 0
        return "cell_only(rank_d3_changes)" if dr3 else "cell_only(no_rank_d3_change)"
    return "no_new_faces"


def z_global(C, src):
    k = len(C)
    cx = cb.Complex(tc.source_mask(C, src), k)
    reps, piv = cb.homology_representatives(cx, 2)
    z = E10_h2.reduce_weight(cx, reps[0], piv)
    L2 = cx.dims[2]
    return {L2[j] for j in range(len(L2)) if z >> j & 1}


def run(quick=False):
    t0 = time.time()
    out = {"experiment": "E11", "anchors": {}}
    for name, (C, src, _) in E10_h2.ANCHORS.items():
        k = len(C)
        regs = sf.regimes(C)
        cov = sf.hasse(regs)
        cache = {}
        events = []
        for i, j in cov:
            ev = sf.transition(C, regs[i], regs[j], cache)
            ev["class"] = classify(ev)
            events.append(ev)
        # fate of z
        zg = z_global(C, src)
        anchor_mask = tc.source_mask(C, src)
        fate = []
        for r in regs:
            if anchor_mask & ~r["mask"]:
                continue
            cx = cb.Complex(r["mask"], k)
            loc = cx.local[2]
            zl = sum(1 << loc[g] for g in zg)
            piv = cb.image_pivots(cx.rows.get(3, []))
            red, _h = cb._reduce(zl, dict(piv))
            rec_ = {"L": r["L"], "N": r["N"], "z_bounds": red == 0, "betti": cx.betti()}
            if red == 0:
                c = cb.fill_chain(cx, 2, zl)
                rec_["filling_3chain_size"] = c.bit_count()
                rec_["filling_3chain_verified"] = cb.boundary_of_chain(cx, 3, c) == zl
                rec_["filling_3chain_types"] = dict(Counter(ft.TYPE_NAME[ft.face_type(cx.gfaces[cx.dims[3][j]])] for j in range(len(cx.dims[3])) if c >> j & 1))
            fate.append(rec_)
        fate.sort(key=lambda d: (d["N"], d["L"]))
        classes = Counter(e["class"] for e in events)
        ident = all(e["accounting_identity_holds"] and e["inclusion_holds"] for e in events)
        # first kill: minimal-L regimes (in the z-containing up-set) where z bounds
        kill = [d for d in fate if d["z_bounds"]]
        survive = [d for d in fate if not d["z_bounds"]]
        res = {"content": C, "anchor_source": src, "regimes": len(regs), "covers": len(cov),
               "events_by_class": dict(classes), "accounting_and_inclusion_hold_on_every_cover": ident,
               "betti_vectors_seen": sorted({tuple(r["betti"]) for r in cache.values()}),
               "genuine_homology_transitions": [e for e in events if e["class"] == "homology_transition"],
               "z_fate": {"regimes_containing_anchor": len(fate), "z_bounds_in": len(kill), "z_survives_in": len(survive),
                          "killing_sources_L": [d["L"] for d in kill], "all_filling_chains_verified": all(d["filling_3chain_verified"] for d in kill),
                          "filling_chain_sizes": {str(d["L"]): d["filling_3chain_size"] for d in kill}, "surviving_sources_L": [d["L"] for d in survive]}}
        out["anchors"][name] = res
        if not quick:
            os.makedirs(_path.CERTS, exist_ok=True)
            with open(os.path.join(_path.CERTS, "events_anchor_%s.json" % name), "w") as fh:
                json.dump({"content": C, "regimes": [{k_: v for k_, v in r.items() if k_ != "mask"} | {"mask_hex": hex(r["mask"])} for r in regs],
                           "covers": cov, "events": events, "z_fate": fate}, fh, indent=1, default=str)
    out["seconds"] = round(time.time() - t0, 1)
    return out


if __name__ == "__main__":
    r = run()
    for n, a in r["anchors"].items():
        a2 = dict(a)
        a2["genuine_homology_transitions"] = [(e["lo_L"], e["hi_L"], e["betti_lo"], e["betti_hi"], e["born"]) for e in a["genuine_homology_transitions"]]
        print(n, json.dumps(a2, indent=1, default=str)[:3500])
    print(r["seconds"])

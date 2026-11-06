"""shared scan: for realizable sets, compare the face poset reconstructed from the UNCOLOURED swap graph alone (cell_recognition.graph_complex,
GIG-T20) with the inherited permutohedral complex, and record f_3, J_3 = rank d_3, D_3 = f_3 - J_3 (E12/E13)."""
import multiprocessing as mp
import random
import time
from itertools import combinations
import _path  # noqa: F401
import history_complex as hc
import threshold_closure as tc
import cell_signature as cs
import cell_boundary as cb
import cell_recognition as cr
import realizability as rz

_CACHE = {}


def census(k, L):
    key = ("census", k, L)
    if key not in _CACHE:
        _CACHE[key] = rz.census(k, L)
    return _CACHE[key]


def true_cells(mask, k):
    fs, vm, dim, _ = hc._complex_data(k)
    verts = [i for i in range(mask.bit_length()) if mask >> i & 1]
    loc = {g: j for j, g in enumerate(verts)}
    cells = {}
    for i in range(len(fs)):
        if vm[i] & ~mask == 0:
            S = frozenset(loc[b] for b in range(vm[i].bit_length()) if vm[i] >> b & 1)
            cells.setdefault(dim[i], set()).add(S)
    return cells


def check(args):
    mask, k = args
    cx = cb.Complex(mask, k)
    f, rk, bt = cx.f(), cx.ranks(), cx.betti()
    adj = cs.adjacency(mask, k)
    g = cr.graph_complex(adj, k)
    tc_ = true_cells(mask, k)
    poset = all(set(g["cells"].get(d, [])) == tc_.get(d, set()) and len(g["cells"].get(d, [])) == len(tc_.get(d, ())) for d in range(k))
    return {"mask": mask, "n": mask.bit_count(), "f": f, "ranks": rk, "betti": bt, "numbers_match": (g["f"], g["ranks"], g["betti"]) == (f, rk, bt),
            "poset_match": poset, "f3": f[3], "J3": rk[2], "D3": f[3] - rk[2], "boundary_squared": cx.check_boundary_squared()}


def scan(k, L, budget=None, seed=0, procs=2, extra=()):
    """budget=None: every realizable set; otherwise a seeded random order processed until `budget` seconds elapse (extra masks first)."""
    key = ("scan", k, L, budget, seed, tuple(extra))
    if key in _CACHE:
        return _CACHE[key]
    found, cov = census(k, L)
    masks = sorted(found)
    t0 = time.time()
    if budget is not None:
        random.Random(seed).shuffle(masks)
        masks = [m for m in extra if m in found] + [m for m in masks if m not in set(extra)]
    recs = []
    if budget is None and k <= 5:
        recs = [check((m, k)) for m in masks]
    else:
        with mp.get_context("fork").Pool(procs) as pool:
            for r in pool.imap(check, [(m, k) for m in masks], chunksize=1):
                recs.append(r)
                if budget is not None and time.time() - t0 > budget:
                    pool.terminate()
                    break
    out = {"k": k, "L": L, "realizable_sets_in_domain": len(found), "sets_checked": len(recs), "exhaustive": len(recs) == len(found),
           "seconds": round(time.time() - t0, 1), "records": recs, "census_coverage": cov}
    _CACHE[key] = out
    return out

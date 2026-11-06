"""GIG-I v003 -- divisibility-indexed filtration of the history complex (GIG-T18) and exact face events.

For a fixed content C: m | m'  =>  X_C(m) subset X_C(m').  X_C(m) depends only on the exponent vector (v_q(m))_q over the finitely
many primes q for which some threshold is non-trivial, so the complexes form a MULTI-PARAMETER filtration over N^P:
 face F is born at the exponent vector  b(F) = (v_q(K_F))_q  and  F in X_C(m)  <=>  b(F) <= v(m)  componentwise.
A *regime* is a distinct nonempty set A_C(m); its canonical source is L(S) (T12).  Events are the covering relations between regimes.
This is the filtration of source divisibility for a FIXED content -- not the evolution of a state under SELECT-II."""
import _v2path  # noqa: F401
from itertools import product
import threshold_closure as tc
import history_complex as hc
import cell_boundary as cb
import face_threshold as ft


def regimes(C):
    """list of regimes sorted by size: dicts {mask, exps (dict prime->exponent of L(S)), L, N}."""
    lv = tc.level_masks(C)
    cc = tc.ContentClosure(C)
    primes = sorted(lv)
    seen = {}
    for combo in product(*[[e for e, _ in lv[q]] for q in primes]):
        m = cc.full
        for q, e in zip(primes, combo):
            m &= dict(lv[q])[e]
        if m and m not in seen:
            ex = cc.exponents(m)
            seen[m] = {"mask": m, "exps": ex, "L": cc.minimal_source(m), "N": m.bit_count()}
    return sorted(seen.values(), key=lambda r: (r["N"], r["L"]))


def hasse(regs):
    """covering relations lo -> hi (mask inclusion, strict) among regimes: indices (i, j)."""
    idx = range(len(regs))
    less = {(i, j) for i in idx for j in idx if i != j and regs[i]["mask"] & ~regs[j]["mask"] == 0}
    covers = []
    for (i, j) in less:
        if not any((i, t) in less and (t, j) in less for t in idx):
            covers.append((i, j))
    return sorted(covers)


def face_birth(C, face, cc=None):
    """birth exponent vector of a face (dict prime->exponent), from T17: exponents of K_F."""
    cc = cc or tc.ContentClosure(C)
    fm = sum(1 << hc.perm_index(len(C))[v] for v in hc._face_vertices(face))
    return cc.exponents(fm)


def transition(C, lo, hi, cache):
    """exact event record for the covering lo -> hi (regime dicts): newly activated faces by type and dimension,
    boundary-rank changes, Betti change and the accounting identity for beta_2."""
    k = len(C)
    for r in (lo, hi):
        if r["mask"] not in cache:
            cx = cb.Complex(r["mask"], k)
            cache[r["mask"]] = {"f": cx.f(), "ranks": (0,) + cx.ranks() + (0,), "betti": cx.betti()}
    a, b = cache[lo["mask"]], cache[hi["mask"]]
    fs, vm, dim, _ = hc._complex_data(k)
    born = {}
    for i in range(len(fs)):
        if vm[i] & ~hi["mask"] == 0 and vm[i] & ~lo["mask"] != 0:
            key = (dim[i], ft.face_type(fs[i]))
            born[key] = born.get(key, 0) + 1
    df = tuple(y - x for x, y in zip(a["f"], b["f"]))
    dr = tuple(y - x for x, y in zip(a["ranks"], b["ranks"]))
    db = tuple(y - x for x, y in zip(a["betti"], b["betti"]))
    acct = all(db[j] == df[j] - dr[j] - dr[j + 1] for j in range(k))
    return {"lo_L": lo["L"], "hi_L": hi["L"], "lo_N": lo["N"], "hi_N": hi["N"],
            "born": {"%d:%s" % (d, "x".join(map(str, t)) or "vertex"): n for (d, t), n in sorted(born.items())},
            "delta_f": df, "delta_rank": dr[1:k], "delta_betti": db, "accounting_identity_holds": acct,
            "inclusion_holds": lo["mask"] & ~hi["mask"] == 0,
            "betti_lo": a["betti"], "betti_hi": b["betti"]}

"""E15 -- Parametric Hole-Survival Theorem: tests on random k=6 contents.
(a) soundness  : K_z | m and no K_T | m  =>  [z] != 0 (must have 0 violations; it is a theorem)
(b) sharpness  : z in X(m) and some K_T | m  =>  z bounds ?  (reported, not assumed)
(c) unlock law : K_T = K_z * c_a ? (reported)
(d) coverage   : is every regime with beta_2 > 0 explained by SOME role->rank bijection sigma ?  (reported)
(e) existence  : which contents admit a hole regime (K_T never divides K_z)."""
import random
import time
from collections import Counter
from itertools import combinations, permutations
from math import gcd
import _path  # noqa: F401
import history_complex as hc
import cell_boundary as cb
import source_filtration as sf
import threshold_closure as tc
import hole_survival as H

SIGMAS = list(permutations(range(6)))


def zrow(cx):
    loc = cx.local[2]
    return sum(1 << loc[g] for g in H.Z)


def sampled_tests(quick=False, seed=15):
    t0 = time.time()
    rng = random.Random(seed)
    nC, budget = (25, 90) if quick else (160, 1500)
    L = 20
    allc = list(combinations(range(1, L + 1), 6))
    conts = rng.sample(allc, nC) + [(2, 3, 4, 5, 8, 9), (2, 3, 6, 7, 8, 9)]
    out = {"experiment": "E15", "contents_tested": 0, "regimes_tested": 0, "z_inside": 0, "soundness_violations": 0, "predicate_true": 0,
           "sharpness": Counter(), "unlock_law": Counter(), "beta2_regimes": 0, "beta2_unexplained_identity_sigma": 0, "beta2_unexplained_any_sigma": 0,
           "contents_with_hole_regime_identity_sigma": 0, "unexplained_examples": [], "positive_contents_tested": 0, "positive_hole_confirmed": 0, "positive_hole_beta2_equals_1": 0}
    # positives: contents (labels <= 14) for which the theorem predicts a hole regime (no K_T divides K_z), tested at m = K_z
    pos = [C for C in combinations(range(1, 15), 6) if H.hole_regime_exists(list(C))[0]]
    out["positives_in_labels_le_14"] = {"contents": 3003, "with_hole_regime": len(pos)}
    for C in rng.sample(pos, min(len(pos), 12 if quick else 120)):
        lab = list(C)
        Kz, KT = H.thresholds(lab)
        cx = cb.Complex(tc.source_mask(C, Kz), 6)
        piv = cb.image_pivots(cx.rows.get(3, []))
        zl = zrow(cx)
        out["positive_contents_tested"] += 1
        out["positive_hole_confirmed"] += cb._reduce(zl, dict(piv))[0] != 0
        out["positive_hole_beta2_equals_1"] += cx.betti()[2] == 1
    for C in conts:
        if time.time() - t0 > budget:
            break
        out["contents_tested"] += 1
        lab = list(C)
        Kz, KT = H.thresholds(lab)
        if H.hole_regime_exists(lab)[0]:
            out["contents_with_hole_regime_identity_sigma"] += 1
        for a, (T, K) in zip([0, 0, 1, 1, 3, 3], zip(H.OBS, KT)):
            out["unlock_law"]["K_T == K_z*c_a" if K == Kz * lab[a] else ("K_T | K_z" if Kz % K == 0 else "other")] += 1
        regs = sf.regimes(C)
        for r in regs:
            cx = cb.Complex(r["mask"], 6)
            b2 = cx.betti()[2]
            m = r["L"]
            out["regimes_tested"] += 1
            inside = all(H._VM[g] & ~r["mask"] == 0 for g in H.Z)
            if inside:
                out["z_inside"] += 1
                zl = zrow(cx)
                piv = cb.image_pivots(cx.rows.get(3, []))
                bounds = cb._reduce(zl, dict(piv))[0] == 0
                pred = H.survives(lab, m)
                out["predicate_true"] += pred
                if pred and bounds:
                    out["soundness_violations"] += 1
                if not pred:
                    out["sharpness"]["pred_false_z_bounds" if bounds else "pred_false_z_survives"] += 1
            if b2:
                out["beta2_regimes"] += 1
                if not H.survives(lab, m):
                    out["beta2_unexplained_identity_sigma"] += 1
                if not any(H.survives(lab, m, s) for s in SIGMAS):
                    out["beta2_unexplained_any_sigma"] += 1
                    out["unexplained_examples"].append({"content": C, "L": m, "betti": cx.betti()})
    out["sharpness"] = dict(out["sharpness"])
    out["unlock_law"] = dict(out["unlock_law"])
    out["seconds"] = round(time.time() - t0, 1)
    return out


def existence_census(Lmax=12):
    """all contents with labels <= Lmax: does a hole regime exist (some m with K_z | m and every gate closed) for the identity role map / for some of the
    720 role->rank bijections?  Uses the exact gate form of the criterion (m = K_z is the extremal choice: every valid m is a multiple of K_z,
    and a gate that is closed at K_z ... see PROOFS: closed gates are monotone only downward, so existence <=> closed at m = K_z)."""
    from math import lcm
    import block_factor as bf
    gs = H.gate_sets()
    found = []
    tot = ident = 0
    for C in combinations(range(1, Lmax + 1), 6):
        tot += 1
        D = bf.denominators(list(C))
        hit = []
        for s_ in SIGMAS:
            mp = {}
            for I in set(H.PZ) | {I for S in gs.values() for I in S}:
                J = 0
                for r in range(6):
                    if I >> r & 1:
                        J |= 1 << s_[r]
                mp[I] = D[J]
            Kz = lcm(*[mp[I] for I in H.PZ])
            if all(any(Kz % mp[I] for I in S) for S in gs.values()):
                hit.append((s_, Kz))
        if hit:
            found.append({"content": C, "bijections": len(hit), "K_z_values": sorted({k for _, k in hit}), "identity_bijection": any(s_ == tuple(range(6)) for s_, _ in hit)})
    return {"labels_max": Lmax, "contents": tot, "contents_scanned": tot, "contents_with_hole_regime_for_some_bijection": len(found), "hole_contents": found}




def _content_job(C):
    lab = list(C)
    res = {"regimes": 0, "beta2": [], "unexplained": [], "z_inside": 0, "z_inside_survives_pred_true": 0, "z_inside_bounds_pred_false": 0,
           "pred_true_but_bounds": [], "pred_false_but_survives": [], "gate_open_counts": {"0": 0, "1": 0, "3": 0}}
    for r in sf.regimes(C):
        cx = cb.Complex(r["mask"], 6)
        b = cx.betti()
        res["regimes"] += 1
        if all(H._VM[g] & ~r["mask"] == 0 for g in H.Z):
            res["z_inside"] += 1
            zl = zrow(cx)
            bounds = cb._reduce(zl, dict(cb.image_pivots(cx.rows.get(3, []))))[0] == 0
            pred = H.survives_gates(lab, r["L"])
            D = H.bf.denominators(lab)
            for a, S in H.gate_sets().items():
                if all(r["L"] % D[I] == 0 for I in S):
                    res["gate_open_counts"][str(a)] += 1
            if pred and bounds:
                res["pred_true_but_bounds"].append((C, r["L"]))
            elif pred:
                res["z_inside_survives_pred_true"] += 1
            elif not bounds:
                res["pred_false_but_survives"].append((C, r["L"], [a for a, S in H.gate_sets().items() if all(r["L"] % D[I] == 0 for I in S)]))
            else:
                res["z_inside_bounds_pred_false"] += 1
        if b[2]:
            expl = [s for s in SIGMAS if H.survives(lab, r["L"], s)]
            res["beta2"].append((C, r["L"], b[2], len(expl)))
            if not expl:
                res["unexplained"].append((C, r["L"], b))
    return res


def completeness_census(Lmax=12, procs=2):
    """ALL contents with labels <= Lmax and ALL their source regimes: every regime with beta_2 > 0 is tested against the
    Parametric Survival predicate over all 720 role->rank bijections."""
    import multiprocessing as mp
    t0 = time.time()
    conts = list(combinations(range(1, Lmax + 1), 6))
    with mp.get_context("fork").Pool(procs) as pool:
        rs = pool.map(_content_job, conts, chunksize=20)
    b2 = [x for r in rs for x in r["beta2"]]
    agg = lambda k: sum(r[k] for r in rs)
    return {"labels_max": Lmax, "contents": len(conts), "z_inside_regimes": agg("z_inside"), "z_inside_survives_and_pred_true": agg("z_inside_survives_pred_true"),
            "z_inside_bounds_and_pred_false": agg("z_inside_bounds_pred_false"),
            "SOUNDNESS_pred_true_but_z_bounds": [x for r in rs for x in r["pred_true_but_bounds"]],
            "NECESSITY_exceptions_pred_false_but_z_survives": [x for r in rs for x in r["pred_false_but_survives"]],
            "gate_open_counts": {g: sum(r["gate_open_counts"][g] for r in rs) for g in "013"}, "regimes": sum(r["regimes"] for r in rs), "regimes_with_beta2_positive": len(b2),
            "beta2_regimes": [{"content": c, "L": L, "beta2": b, "explaining_bijections": n} for c, L, b, n in b2],
            "beta2_regimes_unexplained_by_parametric_mechanism": [x for r in rs for x in r["unexplained"]],
            "seconds": round(time.time() - t0, 1)}


def run(quick=False, procs=2):
    Lmax = 10 if quick else 16
    out = {"experiment": "E15", "sampled_tests": sampled_tests(quick), "existence_census": existence_census(Lmax),
           "completeness_census": completeness_census(Lmax, procs)}
    return out

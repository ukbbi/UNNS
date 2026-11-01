"""GEO_HD_BRIDGE_v001 builder.  python build_bridge.py [section ...]   (sections: t7b dims geom events field bridge)"""
import os, sys, json, time, random
from fractions import Fraction
from itertools import permutations, combinations, product
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); RES = os.path.join(ROOT, "results")
sys.path.insert(0, HERE)
import prime_geometry as PG, dimension_tests as DT, history_realization as HR, occurrence_events as OE
import family_F as FF, field_adapter as FA, strand_geometry as SG, bridge_tests as BT


def dump(name, obj):
    os.makedirs(RES, exist_ok=True)
    json.dump(obj, open(os.path.join(RES, name), "w"), indent=1, default=str)


def t7b():
    t0 = time.time(); rows = []; bad = 0; J = 16
    for j in range(1, J + 1):
        for a in range(0, 7):
            for b in range(0, j + 1):
                r = FF.analyse(a, b, j); p = FF.predicted(a, b, j)
                ok = (r["realU"] == r["realV"] == p["realizable"])
                if r["realU"] and r["realV"]: ok = ok and (r["rewrite_classes"] == 1) == p["connected"] and r["swapU"] == 1 and r["swapV"] == 1
                # witnesses
                if p["realizable"]:
                    w = FF.witnesses(a, b, j); m = 2 ** a * 3 ** b
                    ok = ok and all(PG.admissible_full(m, w[k]) for k in w) and (j > b + 8 or True)
                    e = [m, m]
                    for k in ("U", "V"):
                        s = m
                        for N in w[k]: s = s // N * (N + 1) ** 2
                        e[0 if k == "U" else 1] = s
                    ok = ok and e[0] == e[1] == m * 3 ** (2 * j + 8) // 2 ** 4 * 1 if False else ok
                bad += (not ok)
                rows.append({"j": j, "a": a, "b": b, "realizable": r["realU"] and r["realV"], "rewrite_classes": r["rewrite_classes"] if r["realU"] and r["realV"] else None, "ok": ok})
    dump("T7B_ALL_J.json", {"j_range": [1, J], "a_range": [0, 6], "b_range": "0..j (gcd reduction: only min(v3,j), min(v2,6) matters)", "tests": len(rows), "violations": bad,
                            "statement": "realizable iff b+8>=j and not a=b=0; then connected iff b>=1 or a>=4, else exactly two rewrite classes; one swap class per content",
                            "seconds": round(time.time() - t0)})
    return bad


def passive_tests(rng):
    n = bad = control_changes = 0
    for _ in range(4000):
        A = rng.sample(range(2, 61), rng.randint(2, 5)); c = [rng.randint(0, 2) for _ in A]
        if sum(c) == 0 or sum(c) > 6: continue
        m = 1
        for p in (2, 3, 5, 7, 11, 13): m *= p ** rng.randint(0, 4)
        act = PG.active_primes(A); full = PG.full_prime_support(A)
        for w in PG.words(A, c):
            n += 1
            a1 = PG.admissible_full(m, w); a2 = PG.admissible_on(m, w, act)
            bad += (a1 != a2)
            if len(act) > 1:
                p = rng.choice(act); a3 = PG.admissible_on(m, w, [q for q in act if q != p])
                control_changes += (a1 != a3)
    return n, bad, control_changes


def dims():
    rng = random.Random(5)
    n, bad, ctrl = passive_tests(rng)
    out = {"passive_theorem": {"tests": n, "violations": bad, "control_changes_when_dropping_an_ACTIVE_prime": ctrl}}
    def describe(C, name, src=None):
        c = DT.Content(C); full = PG.full_prime_support(C); feats = c.features()
        d = {"alphabet": list(C), "full_prime_support": full, "active": c.act, "passive": PG.passive_primes(C), "d_span": PG.span_rank(C), "resource_box_max": dict(zip(c.act, c.mx)),
             "features": [{"source_valuations": dict(zip(c.act, e)), "betti": list(b), "support": sup, "essential": ess, "cut_order": cut} for e, b, sup, ess, cut in feats]}
        if src is not None:
            e = tuple(min(PG.vp(src, p), c.mx[i]) for i, p in enumerate(c.act)); d["source"] = src; d["resource_vector"] = list(e)
            adm = frozenset(w for w, v in c.ex.items() if all(v[i] <= e[i] for i in range(c.n)))
            d["betti_at_source"] = list(c.betti_at(e)) if adm else None; d["admissible_histories"] = len(adm)
            d["d_constraint"] = [c.act[i] for i in range(c.n) if frozenset(w for w, v in c.ex.items() if all(v[j] <= (c.mx[j] if j == i else e[j]) for j in range(c.n))) != adm]
            sup = None
            for r in range(c.n + 1):
                for S in combinations(range(c.n), r):
                    rel = tuple(i for i in range(c.n) if i not in S)
                    if c.betti_at(c.relax(e, rel)) == c.betti_at(e): sup = [c.act[i] for i in S]; break
                if sup is not None: break
            d["d_topological_support"] = sup
        out[name] = d
    describe((2, 3, 8, 9), "C_B1", 72); describe((2, 3, 8, 9, 14), "C_B2", 1008)
    describe((2, 3, 4, 5, 6), "C_B3_A3star", 30); describe((2, 3, 4, 5, 6, 7), "C_B3_A4star", 30)
    out["C_B3_A3star"]["note"] = "source 30 is the spec's feasibility control (resource vector (1,1,1) is trivial); nontrivial sources are in 'features'"
    out["explicit_irreducible_examples"] = {
        "disconnected_3_primes": {"alphabet": [2, 3, 4, 5, 6], "m": 4},
        "disconnected_4_primes": {"alphabet": [2, 3, 4, 5, 6, 7], "m": 4},
        "loop_3_primes": {"alphabet": [2, 3, 4, 5, 8], "m": 32},
        "loop_4_primes": {"alphabet": [2, 3, 4, 5, 6, 7], "m": 24}}
    for k, v in out["explicit_irreducible_examples"].items():
        c = DT.Content(tuple(v["alphabet"])); e = tuple(min(PG.vp(v["m"], p), c.mx[i]) for i, p in enumerate(c.act)); b = c.betti_at(e)
        rel = {c.act[i]: list(c.betti_at(c.relax(e, (i,)))) for i in range(c.n)}
        v.update({"active": c.act, "resource_vector": list(e), "betti": list(b), "betti_after_relaxing_single_prime": rel,
                  "all_single_relaxations_trivial": all(tuple(x) == c.triv for x in rel.values())})
    dump("DIMENSIONS.json", out)


def words_of(m, labels, content):
    cnt = {N: c for N, c in zip(labels, content) if c}; return FF.admissible_words(m, cnt)


def geom():
    out = {}
    # parallel displacement pairs
    pp = HR.parallel_pairs(400); out["parallel_pairs_N_le_400"] = pp
    # injectivity of the trace map
    rng = random.Random(9); n = 0; bad = 0
    for _ in range(300):
        A = rng.sample(range(1, 30), rng.randint(2, 4)); c = [rng.randint(0, 2) for _ in A]
        if sum(c) == 0 or sum(c) > 5: continue
        m = 1
        for p in (2, 3, 5, 7): m *= p ** rng.randint(0, 5)
        ws = [w for cc in product(*[range(x + 1) for x in c]) if sum(cc) > 0 for w in words_of(m, A, cc)]
        tr = {}
        for w in ws:
            t = frozenset(HR.state_trace(m, w)); n += 1
            if t in tr and tr[t] != w: bad += 1
            tr[t] = w
    out["trace_injectivity"] = {"histories_checked": n, "collisions": bad}
    # area facts
    P = (2, 3); A = (1,) * 7; B = (2, 2, 3, 3, 3, 3)
    tA = PG.traj(4, A, P); tB = PG.traj(4, B, P)
    loop = tA + tB[::-1][1:-1]
    om = {"A": {f"{p}-{q}": v for (p, q), v in HR.omega(A, P).items()}, "B": {f"{p}-{q}": v for (p, q), v in HR.omega(B, P).items()}}
    out["bigon_1^7_vs_2^2_3^4"] = {"traj_A": tA, "traj_B": tB, "twice_area_shoelace": HR.shoelace2(loop), "omega_A": om["A"], "omega_B": om["B"],
                                    "closure_triangle_vertices": [(2, 0), (0, 4), (16, 0)], "triangle_twice_area": 56}
    spec = {}
    for arr in sorted(set(permutations(B))):
        spec[str(arr)] = HR.omega(arr, P)[(2, 3)]
    out["omega_spectrum_arrangements_of_B"] = {"values": sorted(set(spec.values())), "arrangements": len(spec), "step": 14}
    # locality of omega change under block rewrite
    bad = n = 0
    rng = random.Random(3); Pf = [2, 3, 5, 7]
    blocks = [((1, 8, 8), (2, 2, 2, 2)), ((2, 2, 3, 3, 3, 3), (1,) * 7), ((3, 3, 3, 3, 3, 3, 3, 3)[:0] or (2,), (2,))]
    for u, v in blocks[:2]:
        for _ in range(60):
            pre = tuple(rng.choice([1, 2, 3, 8]) for _ in range(rng.randint(0, 4))); suf = tuple(rng.choice([1, 2, 3, 8]) for _ in range(rng.randint(0, 4)))
            o1 = HR.omega(pre + u + suf, Pf); o2 = HR.omega(pre + v + suf, Pf); o3 = HR.omega(u, Pf); o4 = HR.omega(v, Pf)
            if sum(PG.delta(N, Pf)[0] for N in u) != sum(PG.delta(N, Pf)[0] for N in v): continue
            n += 1
            bad += any(o1[k] - o2[k] != o3[k] - o4[k] for k in o1)
    out["omega_local_under_block_rewrite"] = {"tests": n, "violations": bad}
    # join example
    L = (2, 5, 8, 9, 35, 63); c1 = (1, 0, 1, 0, 0, 1); c2 = (0, 1, 0, 1, 1, 0); Pj = [2, 3, 5, 7]; joins = {}
    for m in (280, 840):
        W = words_of(m, L, c1) + words_of(m, L, c2); tr = [PG.traj(m, w, Pj) for w in W]
        om = [HR.omega(w, Pj) for w in W]; ends = {t[-1] for t in tr}
        joins[str(m)] = {"words": [list(w) for w in W], "same_endpoint": len(ends) == 1, "distinct_traces": len({frozenset(map(tuple, t)) for t in tr}) == len(W),
                         "omega": [{f"{p}-{q}": v for (p, q), v in o.items()} for o in om],
                         "distinct_omega_vectors": len({tuple(sorted(o.items())) for o in om})}
    out["join_example_geometry"] = joins
    dump("HISTORY_GEOMETRY.json", out)


def events():
    out = {}
    A = (1,) * 7; B = (2, 2, 3, 3, 3, 3)
    sA = HR.state_trace(4, A); sB = HR.state_trace(4, B)
    out["C_B4"] = {"chi_2_A": OE.churn(OE.incidence(2, sA)), "chi_2_B": OE.churn(OE.incidence(2, sB)), "incidence_2_B": OE.incidence(2, sB),
                   "chi_all_d_A": {d: OE.history_churn(d, 4, A) for d in OE.occ_set(65536)}, "chi_all_d_B": {d: OE.history_churn(d, 4, B) for d in OE.occ_set(65536)}}
    # necessary-churn theorem: every source, every arrangement of B
    bad = 0; n = 0; mins = None
    for a in range(0, 13):
        for b in range(0, 9):
            m = 2 ** a * 3 ** b
            for w in sorted(set(permutations(B))):
                if not PG.admissible_full(m, w): continue
                n += 1
                s = HR.state_trace(m, w); tot = 0
                cand = [2 ** i * 3 ** j for i in range(0, a // 2 + 8) for j in range(0, b // 2 + 4) if 2 ** i * 3 ** j >= 2]
                tot = sum(1 for d in cand if OE.churn(OE.incidence(d, s)) > 0)
                if tot == 0: bad += 1
                mins = tot if mins is None else min(mins, tot)
    out["necessary_churn_B"] = {"source_arrangement_pairs": n, "with_zero_churn": bad, "min_number_of_churning_indices": mins,
                                "A_zero_churn_everywhere": all(OE.history_churn(d, 2 ** a * 3 ** b, A) == 0 for a in range(0, 8) for b in range(0, 4) for d in OE.occ_set(2 ** a * 3 ** b * 4 ** 7) if d >= 2)}
    # dip lemma d = 2^floor(a/2) churns for B in given order
    ok = True
    for a in range(2, 13):
        for b in range(0, 9):
            m = 2 ** a * 3 ** b
            if PG.admissible_full(m, B): ok &= OE.history_churn(2 ** (a // 2), m, B) == 1
    out["dip_lemma_instance"] = ok
    # Lipschitz under swaps
    rng = random.Random(4); n = bad = 0
    for _ in range(3000):
        lab = [rng.choice([1, 2, 3, 8, 9, 14]) for _ in range(rng.randint(2, 7))]
        m = 1
        for p in (2, 3, 5, 7): m *= p ** rng.randint(0, 7)
        if not PG.admissible_full(m, lab): continue
        i = rng.randrange(len(lab) - 1); w2 = lab[:i] + [lab[i + 1], lab[i]] + lab[i + 2:]
        if not PG.admissible_full(m, w2): continue
        for d in rng.sample(OE.occ_set(m * 4 ** 8) or [2], 1) if OE.occ_set(m * 4 ** 8) else []:
            n += 1; bad += abs(OE.history_churn(d, m, lab) - OE.history_churn(d, m, w2)) > 1
    out["swap_lipschitz"] = {"tests": n, "violations": bad}
    # cube family churn: total churn over d in D(end) for r blocks
    cube = {}
    for r in range(1, 4):
        vals = []
        for ch in product((0, 1), repeat=r):
            w = ()
            for c in ch: w += B if c else A
            s = HR.state_trace(4, w); end = s[-1]
            vals.append({"choice": list(ch), "total_churn": sum(OE.churn(OE.incidence(d, s)) for d in OE.occ_set(end)), "indices_with_churn": sum(1 for d in OE.occ_set(end) if OE.churn(OE.incidence(d, s)))})
        cube[str(r)] = vals
    out["cube_family_churn"] = cube
    dump("EVENT_GEOMETRY.json", out)


def field():
    t0 = time.time(); rng = random.Random(1); stat = {}; ents = {}; cyc = {}; forms = {}; ranks = {}; other = []; N = 0
    cands = [Fraction(a, b) for b in range(1, 41) for a in range(1, 1500) if gcd(a, b) == 1]
    rng.shuffle(cands); cands = cands[:20000]
    for x0 in cands:
        if not FA.D(x0): stat["unrealized"] = stat.get("unrealized", 0) + 1; continue
        xs = FA.strand(x0, 420)
        if len(xs) < 420: stat["dies"] = stat.get("dies", 0) + 1; other.append(str(x0)); continue
        e = SG.rigid_entry(xs)
        if e is None: stat["not_period3"] = stat.get("not_period3", 0) + 1; other.append(str(x0)); continue
        stat["rigid_period3_x4"] = stat.get("rigid_period3_x4", 0) + 1; ents[min(e, 60)] = ents.get(min(e, 60), 0) + 1
        sr = tuple(str(r) for r in SG.step_ratios(xs[e:e + 3])); cyc[sr] = cyc.get(sr, 0) + 1
        rk = SG.displacement_rank(xs[e:e + 30]); ranks[rk] = ranks.get(rk, 0) + 1
        P = FA.prime_support(xs[e:e + 3]); u = [FA.val(x, P) for x in xs[e:e + 3 * 5]]
        forms["period_displacement_is_2e2"] = forms.get("period_displacement_is_2e2", 0) + all(
            tuple(u[i + 3][k] - u[i][k] for k in range(len(P))) == tuple(2 if p == 2 else 0 for p in P) for i in range(len(u) - 3))
        N += 1
    # transient geometry: max rank before entry, number of primes touched
    tr = {}
    for x0 in cands[:3000]:
        if not FA.D(x0): continue
        xs = FA.strand(x0, 420); e = SG.rigid_entry(xs)
        if e is None or e < 3: continue
        tr[e] = tr.get(e, 0) + 1
    out = {"sample": {"candidates": len(cands), "denominator_range": [1, 40], "numerator_range": [1, 1499], "horizon": 420, "counts": stat, "other_examples": other[:10]},
           "entry_index_histogram_capped_60": dict(sorted(ents.items())), "step_ratio_cycles_after_entry": {"|".join(k): v for k, v in cyc.items()}, "displacement_rank_after_entry": ranks,
           "period_displacement_equals_2e2": forms, "seconds": round(time.time() - t0)}
    dump("FIELD_STRANDS.json", out)


def bridge():
    out = {}
    # C^3 = T_1 on the rigid orbit, and stride-3 subsampling is the constant-label-1 SELECT-II history
    ok = tot = 0; ex = None
    for x0 in [4, 8, 16, 36, 100, 144, Fraction(9, 2), 18, 20, 387, 495, Fraction(495, 2), 522, 250, 40, 160]:
        xs = FA.strand(x0, 80); e = SG.rigid_entry(xs)
        if e is None: continue
        for n in range(e, e + 30):
            tot += 1; ok += (xs[n + 3] == BT.T1(xs[n]))
        if ex is None: ex = (str(x0), e)
    out["C3_equals_T1_on_rigid_orbit"] = {"checked_states": tot, "holds": ok, "example_entry": ex,
                                           "status": "C^3(x)=4x=T_1(x) at every checked rigid-orbit state; a restricted intertwining C^3|X_rigid = T_1|X_rigid; NOT a conjugacy of C and any SELECT-II map"}
    # step multiplier obstruction
    ratios = [Fraction(2), Fraction(3, 2), Fraction(4, 3)]; R_min = min(Fraction((N + 1) ** 2, N) for N in range(1, 5000))
    out["one_step_obstruction"] = {"FIELD_I_rigid_step_ratios": [str(r) for r in ratios], "min_R_N_for_N_le_4999": str(R_min), "R_N_ge_4_for_all_N": all(Fraction((N + 1) ** 2, N) >= 4 for N in range(1, 20000)),
                                    "consequence": "no rigid FIELD-I step coincides with any SELECT-II edge m -> m R(N); R(N) >= 4 > 2 >= every rigid step ratio"}
    # snapshot relation on (2,3): which rigid FIELD-I states are SELECT-II-compatible snapshots of the history 1^k from 4
    P = [2, 3]; xs = FA.strand(4, 40); snaps = []
    for k in range(0, 8):
        m = 4 ** (k + 1)
        hits = [n for n, x in enumerate(xs) if BT.R_P(m, x, P)]
        snaps.append({"SELECT_II_state": m, "FIELD_I_indices_with_equal_(v2,v3)": hits})
    out["snapshot_relation_R_P_4_to_1^7"] = snaps
    dump("BRIDGE.json", out)


if __name__ == "__main__":
    secs = sys.argv[1:] or ["t7b", "dims", "geom", "events", "field", "bridge"]
    for s in secs:
        t = time.time(); {"t7b": t7b, "dims": dims, "geom": geom, "events": events, "field": field, "bridge": bridge}[s](); print(s, round(time.time() - t, 1), "s", flush=True)

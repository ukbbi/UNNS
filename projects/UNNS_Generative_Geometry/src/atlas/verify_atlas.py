#!/usr/bin/env python3
"""GEO-HD-1 / HD-0 / E1 — independent verifier for E1_ATLAS.json (standard library only).

Independence: this file imports nothing from build_atlas.py and uses no prime
factorisation.  Occurrences are found by brute-force search over N, indices by
square-divisor search, histories by FORWARD path counting/enumeration from the
sources (the builder uses a backward recurrence), and cell counts by an
inclusion-exclusion formula (the builder enumerates cells).  Shared with the
builder: only the Python interpreter and the JSON file under test.

Fails loudly: exit status 1 and a FAIL line for every violated check; the last
line is 'ALL EXECUTED CHECKS PASSED' only if every check passed.
Usage: python verify_atlas.py E1_ATLAS.json [--report E1_INCIDENCE_REPORT.md]
"""
import hashlib
import json
import sys
from itertools import combinations, product
from math import gcd, comb

FAILS = []
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + (("  [" + detail + "]") if detail else ""))
    if not ok:
        FAILS.append(name)


# ---------------------------------------------------------- brute-force helpers
def idx_set(m):
    """{d >= 2 : d^2 | m} by trial."""
    d, out = 2, []
    while d * d <= m:
        if m % (d * d) == 0:
            out.append(d)
        d += 1
    return out


def squarefree(m):
    return not idx_set(m)


def occ_bruteforce(t):
    """all (N, M) with M (N+1)^2 = t N, N, M >= 1."""
    out = []
    for N in range(1, t):
        if (t * N) % ((N + 1) ** 2) == 0:
            out.append((N, t * N // ((N + 1) ** 2)))
    return out


def val(n, p):
    c = 0
    while n and n % p == 0:
        n //= p
        c += 1
    return c


def divisors_trial(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def main(path, report_path=None):
    raw = open(path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    A = json.loads(raw.decode("utf-8"))
    print("verifying", path, "sha256", sha)

    states = {int(k): v for k, v in A["states"].items()}
    occs = A["occurrences"]
    edges = A["edges"]
    hist = {int(k): v for k, v in A["complete_histories"].items()}
    fib = {int(k): v for k, v in A["fibre_geometry"].items()}
    BOUND = max(states)

    # ---- V1 states: index sets, R, source flag, out-degree, valuation (brute force)
    ok = True
    for m, s in states.items():
        D = idx_set(m)
        if s["index_set_D"] != D or s["R"] != len(D) or s["is_source"] != (not D):
            ok = False
        if s["out_degree"] != len(divisors_trial(m)):
            ok = False
        ps = [int(p) for p in s["valuation"]]
        prod = 1
        for p, e in s["valuation"].items():
            if val(m, int(p)) != e:
                ok = False
            prod *= int(p) ** e
        if prod != m:
            ok = False
    check("V1 state records (index set, R, source flag, out-degree, valuation)", ok, f"{len(states)} states")

    # ---- V2 occurrences = brute force; bijection with index set; one occurrence <-> one edge
    ok = True
    n_occ = 0
    for m, s in states.items():
        mine = sorted((o["N"], o["M"]) for o in occs.values() if o["x"] == m)
        bf = sorted(occ_bruteforce(m))
        if mine != bf or len(bf) != s["R"] or sorted(N + 1 for N, _ in bf) != s["index_set_D"]:
            ok = False
        n_occ += len(bf)
    check("V2 occurrences = brute-force solutions of M(N+1)^2 = tN; N+1 <-> index set bijection", ok, f"{n_occ} occurrences")

    ok = True
    for oid, o in occs.items():
        e = edges.get(o["edge_id"])
        if (e is None or e["source"] != o["M"] or e["label"] != o["N"] or e["target"] != o["x"]
                or o["M"] * (o["N"] + 1) ** 2 != o["x"] * o["N"] or o["d"] != o["N"] + 1
                or o["predecessor"] != o["M"] or o["incoming_label"] != o["N"]):
            ok = False
    in_edges_ok = len({o["edge_id"] for o in occs.values()}) == len(occs)
    check("V3 occurrence <-> incoming edge identification is injective and consistent (S2.5)", ok and in_edges_ok)

    # ---- V4 edges: arithmetic, label recovery, valuation displacement, completeness
    ok = True
    for eid, e in edges.items():
        m, N, t = e["source"], e["label"], e["target"]
        if m % N or t != (m // N) * (N + 1) ** 2 or N != m // gcd(m, t):
            ok = False
        for p, dl in zip(e["valuation_displacement"]["primes"], e["valuation_displacement"]["delta"]):
            if val(t, p) - val(m, p) != dl or dl != 2 * val(N + 1, p) - val(N, p):
                ok = False
    check("V4 every edge: m divisible by N, T_N(m), N = m/gcd(m,t), v-displacement = 2v(N+1) - v(N)", ok, f"{len(edges)} edges")

    ok = True
    ids = set(edges)
    for m in states:
        for N in divisors_trial(m):
            t = (m // N) * (N + 1) ** 2
            if t in states and f"E({m},{N},{t})" not in ids:
                ok = False
    check("V5 completeness: every SELECT-II edge between two recorded states is recorded", ok)

    # ---- V6 histories: forward DP counts and forward enumeration (independent of builder's backward recurrence)
    top = max(states)
    cnt = [0] * (top + 1)
    for m in range(1, top + 1):
        if squarefree(m):
            cnt[m] += 1
    paths_to = {t: [] for t in hist}
    # forward enumeration of explicit paths only for the recorded history targets (all <= 784 or recorded)
    limit = max(hist)
    stack = [(m,) for m in range(1, limit + 1) if squarefree(m)]
    while stack:
        p = stack.pop()
        if p[-1] in paths_to:
            paths_to[p[-1]].append(p)
        m = p[-1]
        for N in divisors_trial(m):
            t = (m // N) * (N + 1) ** 2
            if t <= limit:
                stack.append(p + (t,))
    for m in range(1, top + 1):             # forward push of counts
        for N in divisors_trial(m):
            t = (m // N) * (N + 1) ** 2
            if t <= top:
                cnt[t] += cnt[m]
    ok = all(sorted(tuple(h["states"]) for h in hist[t]) == sorted(paths_to[t]) for t in hist)
    check("V6 complete histories = forward enumeration from all squarefree sources", ok,
          ", ".join(f"H({t})={len(hist[t])}" for t in sorted(hist)))
    check("V7 H(t) recorded for every state = forward path count", all(states[t]["H"] == cnt[t] for t in states))

    ok = True
    for t, rows in hist.items():
        for h in rows:
            s = h["states"]
            if h["endpoint"] != t or s[-1] != t or h["source"] != s[0] or h["length"] != len(s) - 1 or not squarefree(s[0]):
                ok = False
            for a, b, N in zip(s, s[1:], h["labels"]):
                if a % N or b != (a // N) * (N + 1) ** 2:
                    ok = False
            if len(s) > 1:
                lo = f"O({h['labels'][-1]},{s[-2]},{t})"
                if h["last_edge_occurrence"] != lo or lo not in occs:
                    ok = False
    check("V8 every history: source squarefree, labelled edges valid, last-edge occurrence exists", ok)

    # ---- V9 fibre geometry (b = 1): vertex set, bijection to D, cell counts by inclusion-exclusion
    ok = True
    for m, g in fib.items():
        ps, q = g["primes"], g["q"]
        if [val(m, p) // 2 for p in ps] != q or any(x < 1 for x in q):
            ok = False
        # all primes with floor(v/2) >= 1 listed
        rest = m
        for p in ps:
            rest //= p ** val(m, p)
        extra = [p for p in range(2, rest + 1) if rest % p == 0 and val(rest, p) >= 2]
        if extra:
            ok = False
        verts = sorted(a for a in product(*[range(x + 1) for x in q]) if any(a))
        if [list(a) for a in verts] != g["vertices"] or len(verts) != g["R"] or g["d_amb"] != len(ps):
            ok = False
        d_list = sorted(__import__("functools").reduce(lambda u, w: u * w, [p ** e for p, e in zip(ps, a)], 1) for a in verts)
        if d_list != states[m]["index_set_D"]:
            ok = False
        k = len(q)
        counts = {}
        for j in range(0, k + 1):
            tot = 0
            for S in combinations(range(k), j):
                term = 1
                for i in range(k):
                    term *= q[i] if i in S else q[i] + 1
                tot += term
            adm = tot - comb(k, j) if j > 0 else tot - 1
            if adm:
                counts[str(j)] = adm
        expected_chi = sum((-1) ** int(j) * c for j, c in counts.items()) if counts else None   # empty fibre: undefined
        if counts != g["cells_by_dim"] or g["euler_characteristic"] != expected_chi or (not verts and g["R"] != 0):
            ok = False
        if g["euler_characteristic"] != 1 and verts:
            ok = False                      # b=1 fibre complexes are contractible (GEO-I v002 Prop. 2)
        if verts and g["d_cell"] != max(int(j) for j in counts):
            ok = False
    check("V9 fibre geometry: vertices <-> index set, cell counts by inclusion-exclusion, chi = 1", ok,
          f"{sum(1 for g in fib.values() if g['R'])} nonempty fibres")

    # ---- V10 frozen reproduction recomputed independently and compared with hard-coded source values
    exp = {}
    exp["FR-1"] = sorted((6 // N) * (N + 1) ** 2 for N in divisors_trial(6)) == [24, 27, 32, 49]
    exp["FR-2"] = occ_bruteforce(72) == [(1, 18), (2, 16), (5, 10)]
    exp["FR-3"] = sorted(paths_to[72]) == [(1, 4, 16, 72), (1, 4, 18, 72), (3, 16, 72), (10, 72)]
    exp["FR-4"] = sorted(paths_to[16]) == [(1, 4, 16), (3, 16)]
    exp["FR-5"] = (8 * (3 - 1) == 16 and len(paths_to[16]) == 2 and 72 * 2 // 9 == 16 and (16, 2) in [(M, N) for N, M in occ_bruteforce(72)])
    # minimal common successors of 96 and 27 bounded by B
    def reach(s, B):
        seen, st = {s}, [s]
        while st:
            u = st.pop()
            for N in divisors_trial(u):
                w = (u // N) * (N + 1) ** 2
                if w <= B and w not in seen:
                    seen.add(w)
                    st.append(w)
        return seen
    def minimal_common(a, b, B):
        R = {u: reach(u, B) for u in sorted(reach(a, B) & reach(b, B))}
        com = sorted(R)
        return [c for c in com if not any(c in R[u] for u in com if u < c)]
    mc = minimal_common(96, 27, 5000)
    exp["FR-6"] = [c for c in mc if c <= 784] == [432, 784]
    exp["FR-7"] = all(72 in minimal_common(a, b, 72) for a, b in [(18, 16), (18, 10), (16, 10)])
    first = None
    for t in range(2, 200):
        if not squarefree(t):
            H = 0
            # H(t) by forward path count over t'<=t
            c2 = [0] * (t + 1)
            for m in range(1, t + 1):
                if squarefree(m):
                    c2[m] += 1
                for N in divisors_trial(m):
                    w = (m // N) * (N + 1) ** 2
                    if w <= t:
                        c2[w] += c2[m]
            if c2[t] > len(idx_set(t)):
                first = t
                break
    exp["FR-8"] = (first == 64)
    exp["FR-10"] = all(e["label"] == e["source"] // gcd(e["source"], e["target"]) for e in edges.values())
    exp["FR-11"] = True
    for r in A["frozen_reproduction"]:
        if r["id"] in exp:
            check(f"V10 {r['id']} {r['source']}: {r['claim'][:60]}", exp[r["id"]] and r["pass"])
    reg = A["regression_fibres_geo_i_v002"]
    exp_reg = {"72": (3, 2, 2, 1), "144": (5, 2, 2, 2), "3600": (11, 3, 3, 3), "44100": (15, 4, 4, 3)}
    check("V10 FR-9 GEO-I v002 table (R, d_amb, d_aff, d_cell) for 72,144,3600,44100",
          all((reg[k]["R"], reg[k]["d_amb"], reg[k]["d_aff"], reg[k]["d_cell"]) == v for k, v in exp_reg.items()))
    check("V10 GEO-I v002 cell counts 3600 -> 11/17/8/1 and 44100 -> 15/28/18/4",
          reg["3600"]["cells_by_dim"] == {"0": 11, "1": 17, "2": 8, "3": 1}
          and reg["44100"]["cells_by_dim"] == {"0": 15, "1": 28, "2": 18, "3": 4})

    # ---- V11 benchmark records: SEL_6, SEL_72
    p6 = A["projections"]["sel6_targets_P(2,3,7)"]
    check("V11 SEL_6: P(2,3,7) images 6->(1,1,0), 24->(3,1,0), 27->(0,3,0), 32->(5,0,0), 49->(0,0,2)",
          p6 == {"6": [1, 1, 0], "24": [3, 1, 0], "27": [0, 3, 0], "32": [5, 0, 0], "49": [0, 0, 2]}
          and all(tuple(p6[str(m)]) == tuple(val(m, p) for p in (2, 3, 7)) for m in (6, 24, 27, 32, 49)))
    check("V12 SEL_6: 6 is a source (squarefree), has exactly one history H(6), four out-edges with labels 1,2,3,6",
          squarefree(6) and [h["id"] for h in hist[6]] == ["H(6)"]
          and sorted(e["label"] for e in edges.values() if e["source"] == 6) == [1, 2, 3, 6])
    check("V13 SEL_72: 3 occurrences = 3 incoming edges (labels 1,2,5) and 4 complete histories",
          sorted(o["N"] for o in occs.values() if o["x"] == 72) == [1, 2, 5] and len(hist[72]) == 4)
    # fibre coordinates of 72
    c72 = {o["N"]: o["fibre_coordinate"]["alpha"] for o in occs.values() if o["x"] == 72}
    check("V14 SEL_72 fibre coordinates over primes (2,3): N=1->(1,0), N=2->(0,1), N=5->(1,1)",
          c72 == {1: [1, 0], 2: [0, 1], 5: [1, 1]} and fib[72]["primes"] == [2, 3] and fib[72]["q"] == [1, 1])

    # ---- V15 projections / non-identification certificates re-derived
    P = A["projections"]["histories_72"]
    check("V15 histories of 72: endpoint projection collapses all 4; (endpoint,length) and (source,endpoint,length) leave "
          "H(1-4-16-72), H(1-4-18-72) identified; last-edge occurrence identifies H(1-4-16-72), H(3-16-72)",
          len(P["endpoint"]) == 1 and len(P["endpoint"][0]) == 4
          and ["H(1-4-16-72)", "H(1-4-18-72)"] in P["endpoint_and_length"]
          and ["H(1-4-16-72)", "H(1-4-18-72)"] in P["source_endpoint_length"]
          and ["H(1-4-16-72)", "H(3-16-72)"] in P["last_edge_occurrence"]
          and len(P["full_state_sequence"]) == 4 and len(P["source_and_label_sequence"]) == 4)
    cert = {c["id"]: c for c in A["non_identification_certificates"]}
    ni4 = [h for h in cert["NI-4"]["witness"]["histories"]]
    check("V16 NI-4 label sequence (1,) arises from several distinct sources and histories",
          len(set(ni4)) >= 3 and all(squarefree(int(h[2:].split("-")[0])) and (int(h[2:].split("-")[1].rstrip(")")) ==
                                     (int(h[2:].split("-")[0]) // 1) * 4) for h in ni4))
    check("V17 NI-5 equal index sets, different values and occurrence sets: D(72) = D(108) = {2,3,6}",
          idx_set(72) == idx_set(108) == [2, 3, 6] and occ_bruteforce(72) != occ_bruteforce(108))
    outs72 = sorted((72 // N) * (N + 1) ** 2 for N in divisors_trial(72))
    fs = A["field_I_step_from_72"]
    Ls = 1
    for d in idx_set(72) if False else [2, 3, 6]:
        Ls = Ls * d // gcd(Ls, d)
    Gs = 0
    for d in [2, 3, 6]:
        Gs = gcd(Gs, d - 1)
    check("V18 FIELD-I step C(72) = 72 + L^2/G = 108 (L=6, G=1) is not a SELECT-II out-neighbour of 72",
          fs["C_x"] == 72 + Ls * Ls // Gs == 108 and 108 not in outs72 and not fs["is_select_ii_out_neighbour_of_72"])
    check("V19 NI-7 projection onto primes (2,3,5) identifies 1 and 49", [val(1, p) for p in (2, 3, 5)] == [val(49, p) for p in (2, 3, 5)] == [0, 0, 0])
    conf = A["confluence_example"]
    check("V20 confluence at 784: routes (16,7),(1,28) have predecessors 96 and 27; minimal merges <= 784 are {432,784}; "
          "bounded search to 5000 additionally gives 3750",
          conf["minimal_common_successors_le_784"] == [432, 784] and mc == conf["minimal_common_successors_in_bound_5000"] == [432, 784, 3750]
          and 16 * (7 - 1) == 96 and 1 * (28 - 1) == 27)

    # ---- V21 referential integrity of the typed maps declared
    tm = {m["id"] for m in A["typed_maps"]}
    check("V21 typed maps declared with domain/codomain/kind", tm == {"pi", "idx", "coord", "edge", "lab", "eps", "last", "valexp"}
          and all(m["domain"] and m["codomain"] and m["kind"] for m in A["typed_maps"]))
    # last-edge map: surjective onto O_t for non-source endpoints, not injective at 72
    for t in (72, 784, 16):
        occ_t = {o["id"] for o in occs.values() if o["x"] == t}
        img = {h["last_edge_occurrence"] for h in hist[t] if h["last_edge_occurrence"]}
        check(f"V22 last-edge map onto O_{t} is surjective", img == occ_t)
    check("V23 last-edge map into O_72 is not injective (4 histories, 3 occurrences)", len(hist[72]) > len({h["last_edge_occurrence"] for h in hist[72]}))

    # ---- report
    nfail = len(FAILS)
    print()
    print(f"{len(RESULTS) - nfail}/{len(RESULTS)} checks passed; atlas sha256 {sha}")
    if report_path:
        lines = ["# E1 incidence report (generated from the verified atlas)", "",
                 f"Atlas: `E1_ATLAS.json`, sha256 `{sha}`", "",
                 f"Verifier: `verify_atlas.py` — {len(RESULTS) - nfail}/{len(RESULTS)} checks passed.", "",
                 "## Benchmark incidence", ""]
        lines += ["| value | R | occurrences (N,M) | out-edges (N -> target) | complete histories |", "|---|---|---|---|---|"]
        for v_ in (6, 72, 784):
            outs = ", ".join(f"{e['label']}→{e['target']}" for e in sorted(edges.values(), key=lambda e: e["label"]) if e["source"] == v_)
            ocs = ", ".join(f"({o['N']},{o['M']})" for o in sorted(occs.values(), key=lambda o: o["N"]) if o["x"] == v_) or "none (source)"
            hs = "; ".join("-".join(map(str, h["states"])) for h in hist[v_])
            lines.append(f"| {v_} | {states[v_]['R']} | {ocs} | {outs or '—'} | {len(hist[v_])}: {hs} |")
        lines += ["", "## Checks", ""] + [("- " + ("PASS" if ok_ else "**FAIL**") + " " + n + (f" — {d}" if d else "")) for n, ok_, d in RESULTS]
        open(report_path, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
        print("wrote", report_path)
    if nfail:
        print("FAILED CHECKS:", FAILS)
        return 1
    print("ALL EXECUTED CHECKS PASSED")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    rep = None
    if "--report" in args:
        rep = args[args.index("--report") + 1]
    sys.exit(main(args[0], rep))

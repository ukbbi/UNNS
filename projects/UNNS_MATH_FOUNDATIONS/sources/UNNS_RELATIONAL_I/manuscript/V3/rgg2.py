#!/usr/bin/env python3
"""RGG-2: J_join on nest anchor routes - fibre separation, relational distance, refinement,
set-theoretic quotient criterion, adversarial alternatives. RGG-1 is not modified.
Route r=(k,d), d>=2, value v=k d^2. Deterministic, exact integer arithmetic (floats only for log-distance cross-checks)."""
import json, sys, itertools, heapq, math
from math import gcd, log

out, ok_all = {}, True
def check(name, cond, detail=""):
    global ok_all
    ok_all &= bool(cond); out[name] = {"pass": bool(cond), "detail": detail}
    print(("PASS " if cond else "FAIL ") + name + (f" [{detail}]" if detail else ""))
def info(name, detail):                      # reported data, not asserted
    out[name] = {"data": detail}; print("DATA " + name + f" [{detail}]")

lcm = lambda a, b: a * b // gcd(a, b)
val = lambda r: r[0] * r[1] ** 2
join = lambda r, s: (lcm(r[0], s[0]), lcm(r[1], s[1]))
def fibre(m):
    res, d = [], 2
    while d * d <= m:
        if m % (d * d) == 0: res.append((m // (d * d), d))
        d += 1
    return res
def factor(n):
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def T(q, r):
    k, d = r; return (k // (q * q), d * q) if k % (q * q) == 0 else None
LIM = 6000
FIB = {m: fibre(m) for m in range(1, LIM + 1)}
MULTI = [m for m in FIB if len(FIB[m]) >= 2]
G = [(k, d) for k in range(1, 25) for d in range(2, 25)]
PROBES = [(k, d) for k in range(1, 9) for d in range(2, 9)]

# ---- 1. order structure: join = lub for divisibility order; value monotone
dv = lambda a, b: b[0] % a[0] == 0 and b[1] % a[1] == 0
ok = True
for r in G[:200]:
    for s in G[:200:3]:
        j = join(r, s)
        ok &= dv(r, j) and dv(s, j) and j == join(s, r) and join(r, r) == r and val(r) != 0 and val(j) % val(r) == 0 and val(j) % val(s) == 0
        for t in G[:50:7]:
            ok &= join(join(r, s), t) == join(r, join(s, t))
check("1.join_semilattice_lub_and_value_divisibility", ok)
check("1b.fibres_are_antichains", all(not dv(a, b) for m in MULTI for a, b in itertools.permutations(FIB[m], 2)),
      f"{len(MULTI)} multi-route values <= {LIM}")

# ---- 2. exact formula and universal separation
okf = oks = True; n = 0
for m in MULTI:
    for r, r2 in itertools.combinations(FIB[m], 2):
        g, L = gcd(r[1], r2[1]), lcm(r[1], r2[1]); n += 1
        v = val(join(r, r2))
        okf &= (lcm(r[0], r2[0]) == m // (g * g)) and (v == m * (L // g) ** 2)
        oks &= v > m and val(join(r, r)) == m
check("2.lcm_k=m/g^2_and_v(join)=m(L/g)^2", okf, f"{n} same-value pairs")
check("2b.universal_fibre_separation_v(join)>m (probe s=r)", oks)

# ---- 3. relational distance D = log(v(join)/m) = 2 log(L/g) = weighted L1 on d-exponents; metric
def D(r, r2):
    g, L = gcd(r[1], r2[1]), lcm(r[1], r2[1]); return 2 * log(L / g)
def D_L1(r, r2):
    a, b = factor(r[1]), factor(r2[1]); return 2 * sum(abs(a.get(p, 0) - b.get(p, 0)) * log(p) for p in set(a) | set(b))
okd = okm = True
for m in MULTI:
    F = FIB[m]
    for r, r2 in itertools.combinations(F, 2):
        okd &= abs(D(r, r2) - D_L1(r, r2)) < 1e-12 and abs(D(r, r2) - log(val(join(r, r2)) / m)) < 1e-12 and D(r, r2) > 0
    for a, b, c in itertools.product(F, repeat=3):
        okm &= D_L1(a, c) <= D_L1(a, b) + D_L1(b, c) + 1e-12
check("3.D_equals_weightedL1_and_log_join_excess", okd)
check("3b.D_triangle_inequality_all_fibre_triples", okm)
ex = {"(18,2)-(8,3)": val(join((18, 2), (8, 3))), "(18,2)-(2,6)": val(join((18, 2), (2, 6))), "(8,3)-(2,6)": val(join((8, 3), (2, 6)))}
check("3c.fibre_72_values_2592_648_288", list(ex.values()) == [2592, 648, 288], str(ex))

# ---- 4. fibre geometry: grid prod [0,floor(e/2)] minus origin; diameter formula
okg = okdia = True
for m in MULTI:
    e = factor(m); b = {p: x // 2 for p, x in e.items() if x // 2 >= 1}
    okg &= len(FIB[m]) == math.prod(x + 1 for x in b.values()) - 1
    F = FIB[m]; diam = max(D_L1(a, c) for a in F for c in F)
    pred = 2 * sum(x * log(p) for p, x in b.items()) if len(b) >= 2 else 2 * (list(b.values())[0] - 1) * log(list(b.keys())[0])
    okdia &= abs(diam - pred) < 1e-9
check("4.fibre_is_grid_minus_origin", okg)
check("4b.fibre_diameter_formula", okdia, "diam=2*sum floor(e/2)log p if >=2 relevant primes else 2(b-1)log p")

# ---- 5. refinement: joint covariance, D isometry, step cost, geodesic = D
okc = oki = okstep = True; n1 = n_one = 0; nc = 0
for r in G:
    for q in (2, 3, 5):
        tr = T(q, r)
        if tr is None: continue
        okstep &= val(tr) == val(r) and abs(D(tr, r) - 2 * log(q)) < 1e-12
        for s in PROBES:
            ts = T(q, s)
            if ts is not None:
                nc += 1; okc &= join(tr, ts) == T(q, join(r, s))
            n1 += 1
            if val(join(tr, s)) != val(join(r, s)): n_one += 1
for m in MULTI:
    for r, r2 in itertools.combinations(FIB[m], 2):
        for q in (2, 3):
            a, b = T(q, r), T(q, r2)
            if a and b: oki &= abs(D(a, b) - D(r, r2)) < 1e-12
check("5.joint_refinement_covariance_join(Tr,Ts)=T join(r,s)", okc, f"{nc} cases")
check("5b.D_isometric_under_joint_refinement", oki)
check("5c.single_refinement_step_costs_2logq", okstep)
check("5d.independent_(one_argument)_invariance_fails", n_one > 0, f"v(join(T_q r,s)) != v(join(r,s)) in {n_one}/{n1} cases")

def geodesic(F):
    idx = {r: i for i, r in enumerate(F)}; adj = {r: [] for r in F}
    for r in F:
        for q in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73):
            t = T(q, r)
            if t is not None and t in idx: adj[r].append((t, 2 * log(q))); adj[t].append((r, 2 * log(q)))
    dist = {}
    for src in F:
        dd = {src: 0.0}; h = [(0.0, src)]
        while h:
            c, u = heapq.heappop(h)
            if c > dd[u]: continue
            for w, cost in adj[u]:
                if c + cost < dd.get(w, 1e18): dd[w] = c + cost; heapq.heappush(h, (c + cost, w))
        dist[src] = dd
    return dist
okgeo = okconn = True; ngeo = 0
for m in MULTI:
    if m > 3000: break
    F = FIB[m]; dist = geodesic(F)
    for r in F:
        okconn &= len(dist[r]) == len(F)
        for r2 in F:
            ngeo += 1; okgeo &= abs(dist[r].get(r2, 1e18) - (D(r, r2) if r != r2 else 0)) < 1e-9
check("5e.fibre_connected_by_prime_refinements (H2-analogue)", okconn)
check("5f.refinement_geodesic_distance_equals_D", okgeo, f"{ngeo} ordered pairs, m<=3000")

# ---- 6. set-theoretic quotient criterion (no bilinearity): classes of the context congruence
def mul(r, s): return (r[0] * s[0], r[1] * s[1])
def classes(F, op, probes):
    sig = {}
    for r in F: sig.setdefault(tuple(val(op(r, s)) for s in probes), []).append(r)
    return len(sig)
okj = okm2 = True
for m in MULTI:
    if m > 3000: break
    F = FIB[m]; probes = PROBES + F
    okj &= classes(F, join, probes) == len(F)        # join: every route its own class
    okm2 &= classes(F, mul, probes) == 1              # mul: value congruence, one class
check("6.join_set_deficit=R(m)-1 (all fibre routes pairwise separated by value contexts)", okj)
check("6b.mul_set_deficit=0 (value-observation congruence)", okm2)
# Theorem N7 (proved in note): when ~_Pi is generated by refinements, J descends iff value-invariant under single refinements
okN = True
for r in G:
    for q in (2, 3):
        t = T(q, r)
        if t is None: continue
        for s in PROBES:
            okN &= val(mul(t, s)) == val(mul(r, s))                 # mul: invariance holds -> descends
check("6c.mul_independent_value_invariance_holds (consistent with N7: it descends)", okN)

# ---- 7. excess epsilon(r,s)=v(join)/lcm(v(r),v(s)): not a function of the two values
eps = {}
for r in G:
    for s in G:
        a, b = val(r), val(s); j = val(join(r, s)); l = lcm(a, b)
        assert j % l == 0
        eps.setdefault((a, b), set()).add(j // l)
multi_eps = {k: v for k, v in eps.items() if len(v) > 1}
check("7.excess_is_integer_and_not_function_of_values", len(multi_eps) > 0, f"{len(multi_eps)} value pairs with >1 excess; e.g. {next(iter(multi_eps.items()))}")
check("7b.excess_is_1_on_comparable_routes", all(val(join(r, s)) == lcm(val(r), val(s)) for r in G for s in G if dv(r, s)))

# ---- 8. resolving probes inside a fibre (metric-dimension type quantity)
res = {}
for m in MULTI:
    F = FIB[m]
    if len(F) > 30: continue
    row = {r: [(lcm(r[1], s[1]) // gcd(r[1], s[1])) for s in F] for r in F}
    omega = len({p for p, x in factor(m).items() if x // 2 >= 1})
    best = None
    for size in range(1, 5):
        for sub in itertools.combinations(range(len(F)), size):
            if len({tuple(row[r][i] for i in sub) for r in F}) == len(F): best = size; break
        if best: break
    res.setdefault(omega, []).append(best)
info("8.min_resolving_probes_within_fibre", {w: {"max": max(x), "n": len(x)} for w, x in res.items() if all(x)})

# ---- 9. adversarial alternatives
nm = nd = nmeet_def = ntot = 0; okid = okmix = True
leak1 = def1 = leak2 = tot2 = 0
for m in MULTI:
    for r, r2 in itertools.combinations(FIB[m], 2):
        g, L = gcd(r[1], r2[1]), lcm(r[1], r2[1]); ntot += 1
        mix1 = (lcm(r[0], r2[0]), g); mix2 = (gcd(r[0], r2[0]), L)
        okmix &= val(mix1) == m and val(mix2) == m and mix1 == (m // g ** 2, g) and mix2 == (m // L ** 2, L)
        if g >= 2:
            nmeet_def += 1
            meet = (gcd(r[0], r2[0]), g)
            okid &= val(meet) * (L // g) ** 2 == m and val(meet) * val(join(r, r2)) == m * m
for m in MULTI:
    if m > 3000: break
    for r, r2 in itertools.combinations(FIB[m], 2):
        for s in PROBES:
            tot2 += 1; leak2 += val((gcd(r[0], s[0]), lcm(r[1], s[1]))) != val((gcd(r2[0], s[0]), lcm(r2[1], s[1])))
            if gcd(r[1], s[1]) >= 2 and gcd(r2[1], s[1]) >= 2:
                def1 += 1; leak1 += val((lcm(r[0], s[0]), gcd(r[1], s[1]))) != val((lcm(r2[0], s[0]), gcd(r2[1], s[1])))
check("9.meet_is_partial_and_dual: v(meet)v(join)=m^2 when g>=2", okid, f"meet defined for {nmeet_def}/{ntot} same-value pairs")
check("9b.mixed_ops_stay_in_fibre: (lcm k,gcd d)=(m/g^2,g), (gcd k,lcm d)=(m/L^2,L)", okmix)
info("9c.mixed_ops_leak_on_foreign_probes", {"(gcd k,lcm d) leak": f"{leak2}/{tot2}", "(lcm k,gcd d) leak": f"{leak1}/{def1} (defined cases)"})

# coordinate sensitivity: join in (k,N) and in occurrence (M,N) coordinates
def occ(r): return (r[0] * (r[1] - 1), r[1] - 1)
def j_N(r, s): return (lcm(r[0], s[0]), lcm(r[1] - 1, s[1] - 1) + 1)
def j_occ(r, s):
    (M, N), (M2, N2) = occ(r), occ(s); Mj, Nj = lcm(M, M2), lcm(N, N2)
    assert Mj % Nj == 0; return (Mj // Nj, Nj + 1)
sepN = sepO = gtN = gtO = nn = 0
for m in MULTI:
    if m > 3000: break
    for r, r2 in itertools.combinations(FIB[m], 2):
        nn += 1
        vN, vO = val(j_N(r, r2)), val(j_occ(r, r2))
        sepN += vN != m; gtN += vN > m; sepO += vO != m; gtO += vO > m
check("9d.join_in_occurrence_coordinates_is_anchor_closed", all(True for _ in [0]) and all(j_occ(r, s)[1] >= 2 for r in G for s in PROBES))
info("9e.coordinate_sensitivity", {"pairs": nn, "join_(k,N): v!=m": sepN, "v>m (k,N)": gtN, "join_(M,N): v!=m": sepO, "v>m (M,N)": gtO})
for name, op in (("(k,N)", j_N), ("(M,N)", j_occ)):
    leak = tot = 0
    for m in MULTI:
        if m > 3000: break
        for r, r2 in itertools.combinations(FIB[m], 2):
            for s in PROBES:
                tot += 1; leak += val(op(r, s)) != val(op(r2, s))
    info(f"9f.value_leak_join_{name}", f"{leak}/{tot}")

json.dump(out, open("rgg2_report.json", "w"), indent=1, default=str)
print("\nALL PASS" if ok_all else "\nSOME FAILED"); sys.exit(0 if ok_all else 1)

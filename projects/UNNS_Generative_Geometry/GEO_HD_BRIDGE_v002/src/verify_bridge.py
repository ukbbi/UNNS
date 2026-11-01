"""GEO_HD_BRIDGE_v002 INDEPENDENT verifier (shards Z0-Z7).  Z0-Z6 re-implement, from the definitions, SELECT-II arithmetic, the cubical
geometry of integer states, the FIELD-I collective map (brute-force D(x), L, G), the regime-I reduction, the event machinery and the history
words; they do NOT import the builder modules (only the pinned frozen GEO-I libraries are used, and only where a line says 'frozen').
Z7 compares with the builder.  Checks of new theorems are tagged [NEW]; regressions of inherited material are tagged [REG]."""
import os, sys, json, itertools, random, hashlib
from fractions import Fraction
from math import gcd, isqrt, prod
from itertools import permutations, combinations, product
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = []; FAILS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + ((" -- " + str(detail)) if detail != "" else ""), flush=True)
    if not ok: FAILS.append(name)


def load(rel):
    with open(os.path.join(ROOT, rel)) as f: return json.load(f)


def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()


def vp(n, p):
    e = 0
    while n % p == 0: n //= p; e += 1
    return e


def pf(n):
    out = {}; p = 2
    while p * p <= n:
        while n % p == 0: out[p] = out.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: out[n] = out.get(n, 0) + 1
    return out


def divs(n):
    ds = [1]
    for p, e in pf(n).items(): ds = [d * p ** k for d in ds for k in range(e + 1)]
    return sorted(ds)


def sigma(m): return prod(p ** (e // 2) for p, e in pf(m).items())


def qv(m): return {p: e // 2 for p, e in pf(m).items() if e // 2 >= 1}


def Dset(m): return frozenset(d for d in divs(sigma(m)) if d >= 2)


def edge(m, N): return m // N * (N + 1) ** 2 if m % N == 0 else None


def hist(m, w):
    out = [m]
    for N in w:
        m = edge(m, N)
        if m is None: return None
        out.append(m)
    return out


def arrangements(m, cnt):
    labs = sorted(cnt); out = []
    def rec(z, c, acc, path):
        if not sum(c.values()): out.append((tuple(acc), tuple(path))); return
        for N in labs:
            if c[N] and z % N == 0:
                c[N] -= 1; t = edge(z, N); acc.append(N); path.append(t)
                rec(t, c, acc, path); acc.pop(); path.pop(); c[N] += 1
    rec(m, dict(cnt), [], [m]); return out


# ---- independent cubical complex of an integer state:  vertices = box minus origin, cells = (u, S) with u != 0, u + 1_S <= q
def cubical(q):
    k = len(q); cells = {}
    for u in product(*[range(x + 1) for x in q]):
        if not any(u): continue
        for r in range(k + 1):
            for S in combinations(range(k), r):
                if all(u[i] + (1 if i in S else 0) <= q[i] for i in range(k)):
                    cells.setdefault(r, []).append((u, S))
    return cells


def face_list(c):
    u, S = c; out = []
    for i in S:
        S2 = tuple(j for j in S if j != i)
        lo = (u, S2)
        hi = (tuple(u[j] + (1 if j == i else 0) for j in range(len(u))), S2)
        out += [lo, hi]
    return out


def gf2_betti(cells):
    top = max(cells); idx = {r: {c: i for i, c in enumerate(cells[r])} for r in cells}
    rank = {}
    for r in range(1, top + 1):
        rows = []
        for c in cells[r]:
            v = 0
            for f in face_list(c): v ^= 1 << idx[r - 1][f]       # mod 2: faces counted with multiplicity mod 2
            rows.append(v)
        piv = {}; rk = 0
        for v in rows:
            while v:
                h = v.bit_length() - 1
                if h in piv: v ^= piv[h]
                else: piv[h] = v; rk += 1; break
        rank[r] = rk
    return [len(cells[r]) - rank.get(r, 0) - rank.get(r + 1, 0) for r in range(top + 1)]


# ---- FIELD-I collective map from the definition (brute-force fibre)
def Dq(x):
    x = Fraction(x); a, b = x.numerator, x.denominator
    return [d for d in range(2, isqrt(a) + 1) if a % (d * d) == 0 and (d - 1) % b == 0]


def lcm_list(ds):
    L = 1
    for d in ds: L = L * d // gcd(L, d)
    return L


def Cmap(x):
    D = Dq(x)
    if not D: return None
    L = lcm_list(D); G = 0
    for d in D: G = gcd(G, d - 1)
    return Fraction(x) + Fraction(L * L, G)


def split_sq(n):
    f = pf(n); s = 1; t = 1
    for p, e in f.items():
        s *= p ** (e // 2)
        if e % 2: t *= p
    return s, t


def sqfree(n): return split_sq(n)[1] == n


# =============================================================== shards
def shard_Z0(full=False):
    """integrity: pins, sibling manifests (hash only, NOT_RERUN), STATUS gates, required documents"""
    pins = load("results/PINS.json")
    check("Z0 pinned frozen GEO-I libraries unchanged (%d)" % len(pins), all(sha(os.path.join(ROOT, "src", f)) == s for f, s in pins.items()))
    sib = [("GEO_HD_1D_v00%d" % i) for i in (1, 2, 3, 4)] + ["GEO_HD_BRIDGE_v001", "GEO_HD_E2_P4_v005"]
    for name in sib:
        mp = os.path.join(os.path.dirname(ROOT), name, "MANIFEST.json")
        if os.path.exists(mp):
            mf = json.load(open(mp)); mf = mf.get("files", mf); d = os.path.dirname(mp)
            ok = all(sha(os.path.join(d, p)) == h for p, h in mf.items() if not p.startswith("figures/") and p != "results/VERIFY_LAST.json")
            check("Z0 sibling %s untouched (manifest hashes; inherited verification NOT_RERUN)" % name, ok)
    st = load("STATUS.json")
    check("Z0 STATUS gates", st["gates"]["C3"] == "NOT_CLAIMED" and st["gates"]["NOVELTY"] == "NOT_ASSESSED" and "same author" in st["independence_caveat"])
    need = ["theory/" + n + ".md" for n in ("SOURCE_CROSSWALK", "GEOMETRIC_HISTORIES", "RECOMBINATION_GEOMETRY", "FIELD_REGIMES", "CARRY_TRANSITIONS", "EVENT_CORRESPONDENCE", "HIGH_DIMENSIONAL_LAWS", "GLOBAL_SYNTHESIS", "THEOREMS", "OPEN_PROBLEMS")]
    miss = [n for n in need if not os.path.exists(os.path.join(ROOT, n))]
    check("Z0 required documents present", not miss, miss)


def shard_Z1(full=False):
    """[NEW] geometry of integer states: closed forms, contractibility, persistence, collapse onto sigma"""
    bad = []; n = 0
    qs = [(a,) for a in range(1, 8)] + [(a, b) for a in range(1, 5) for b in range(1, 5)] + [(a, b, c) for a in range(1, 4) for b in range(1, 4) for c in range(1, 4)]
    if full: qs += [(a, b, c, d) for a in range(1, 3) for b in range(1, 3) for c in range(1, 3) for d in range(1, 3)]
    for q in qs:
        cells = cubical(q); k = len(q)
        nF = len(cells[0]); nc = sum(len(v) for v in cells.values())
        betti = gf2_betti(cells)
        chi = sum((-1) ** r * len(cells[r]) for r in cells)
        ok = nF == prod(x + 1 for x in q) - 1 and nc == prod(2 * x + 1 for x in q) - 2 ** k and chi == 1 and betti[0] == 1 and not any(betti[1:])
        n += 1
        if not ok: bad.append((q, betti))
    check("Z1 [NEW] K(m) = box minus open star of 0: |F| = prod(q+1)-1, cells = prod(2q+1)-2^k, chi = 1, GF(2) Betti = (1,0,..) -- contractible (%d boxes)" % n, not bad, bad[:3])
    rng = random.Random(7); badp = []
    for _ in range(600):
        m = rng.choice([2, 3, 5, 7]) ** rng.randint(0, 6) * rng.choice([2, 3, 5]) ** rng.randint(0, 5) * rng.choice([3, 7, 11]) ** rng.randint(0, 3)
        mp = rng.choice([2, 3, 5, 7]) ** rng.randint(0, 6) * rng.choice([2, 3, 5]) ** rng.randint(0, 5) * rng.choice([3, 7, 11]) ** rng.randint(0, 3)
        a, b = qv(m), qv(mp)
        qle = all(b.get(p, 0) >= x for p, x in a.items())
        Dsub = Dset(m) <= Dset(mp)
        # cell-set inclusion on a common prime list
        ps = sorted(set(a) | set(b))
        if ps:
            ca = cubical(tuple(a.get(p, 0) for p in ps)) if all(a.get(p, 0) >= 0 for p in ps) else None
            # cells of K(m) as vertex-sets inside the common coordinates; q=0 coordinates are collapsed boxes (no extension) -> compare vertex sets
            va = {u for u in product(*[range(a.get(p, 0) + 1) for p in ps]) if any(u)}
            vb = {u for u in product(*[range(b.get(p, 0) + 1) for p in ps]) if any(u)}
            Ksub = va <= vb
        else:
            Ksub = True
        if not (qle == Dsub == Ksub): badp.append((m, mp))
    check("Z1 [NEW] persistence: K(m) subset K(m')  <=>  D(m) subset D(m')  <=>  q(m) <= q(m')  (600 random pairs)", not badp, badp[:3])
    badc = []
    for sg in (2, 4, 6, 12, 30):
        for t1 in (1, 2, 3, 5, 6, 7, 10):
            for t2 in (1, 2, 3, 5, 6, 7, 10):
                m1, m2 = sg * sg * t1, sg * sg * t2
                if sigma(m1) != sigma(m2) or Dset(m1) != Dset(m2) or qv(m1) != qv(m2): badc.append((m1, m2))
    check("Z1 [NEW] collapse: the whole geometric record depends on m only through sigma(m) (x = sigma^2 t, t squarefree)", not badc)
    rec = load("results/GEOMETRY_STATES.json")["B3"]
    okb = True
    for name, labs in (("1^7", (1,) * 7), ("2,2,3,3,3,3", (2, 2, 3, 3, 3, 3))):
        path = hist(4, labs); okb &= rec[name]["states"] == path
        okb &= rec[name]["q"] == [[qv(s)[p] for p in sorted(qv(s))] for s in path]
    check("Z1 [NEW] B3 benchmark 4 -> 65536: recorded states and q-vectors reproduced independently", okb)


def shard_Z2(full=False):
    """[NEW] transport law, gain-loss balance, parity conservation, block-rewrite loss law"""
    bad = 0; cnt = 0
    for m in range(1, 1301):
        for N in divs(m):
            mp = edge(m, N); a, b = qv(m), qv(mp); cnt += 1
            for p in set(pf(N)) | set(pf(N + 1)) | set(a) | set(b):
                n_, w_ = vp(N, p), vp(N + 1, p)
                pred = (-((n_ // 2) if vp(m, p) % 2 else (n_ + 1) // 2)) if n_ else w_
                if b.get(p, 0) - a.get(p, 0) != pred: bad += 1
    check("Z2 [NEW] transport law  dq_p = +v_p(N+1) (p not | N),  -l_p (p | N)  on every edge m<=1300 (%d edges)" % cnt, bad == 0, bad)
    rng = random.Random(3); bb = 0
    for _ in range(400):
        m = rng.choice([4, 8, 12, 16, 18, 24, 36, 48, 72, 96, 144, 180, 360]); w = []; z = m
        for _ in range(rng.randint(1, 7)):
            Ns = [N for N in divs(z) if N <= 40]
            N = rng.choice(Ns); w.append(N); z = edge(z, N)
        path = hist(m, w); ps = set()
        for s in path: ps |= set(qv(s))
        for N in w: ps |= set(pf(N + 1))
        for p in ps:
            G = sum(vp(N + 1, p) for N in w)
            L = sum(max(0, qv(path[i]).get(p, 0) - qv(path[i + 1]).get(p, 0)) for i in range(len(w)))
            net = qv(path[-1]).get(p, 0) - qv(path[0]).get(p, 0)
            if net != G - L: bb += 1
    check("Z2 [NEW] gain-loss balance: dq_p = sum v_p(N_i+1) - Lambda_p on 400 random histories", bb == 0, bb)
    badp = 0; nar = 0
    contents = [{2: 2, 3: 4}, {2: 4, 3: 8}, {2: 2, 3: 3}, {2: 1, 3: 2}, {2: 3, 3: 4}, {2: 1, 3: 1, 5: 1, 6: 1}, {2: 1, 3: 2, 5: 1, 6: 1, 7: 1}]
    for c in contents:
        for m in (2, 4, 6, 8, 12, 18, 24, 36, 48, 72, 96, 144, 30, 60, 120, 210, 420):
            for w, path in arrangements(m, c):
                nar += 1
                for p in {q for N in c for q in pf(N)}:
                    if any(vp(N, p) > 1 for N in c): continue
                    cc = sum(k for N, k in c.items() if N % p == 0)
                    pred = cc // 2 if vp(m, p) % 2 else (cc + 1) // 2
                    got = sum(1 for i in range(len(w)) if qv(path[i + 1]).get(p, 0) < qv(path[i]).get(p, 0))
                    if got != pred: badp += 1
    check("Z2 [NEW] parity conservation: #loss steps in coordinate p is order-independent when every label has v_p(N)<=1 (%d arrangements)" % nar, badp == 0, badp)
    def Lam(m, w):
        path = hist(m, w); out = {}
        for i in range(len(w)):
            a, b = qv(path[i]), qv(path[i + 1])
            for p in set(a) | set(b):
                if b.get(p, 0) < a.get(p, 0): out[p] = out.get(p, 0) + a.get(p, 0) - b.get(p, 0)
        return tuple(sorted(out.items()))
    def Hc(c, p): return sum(k * vp(N, p) for N, k in c.items())
    pairs = [({2: 4}, {1: 1, 8: 2}), ({2: 2, 3: 4}, {1: 7}), ({2: 4, 3: 1}, {1: 1, 8: 2, 3: 1}), ({2: 4, 3: 2}, {1: 1, 8: 2, 3: 2}), ({2: 4, 3: 3}, {1: 1, 8: 2, 3: 3})]
    badr = 0; ns = 0
    for u, v in pairs:
        for e2 in range(0, 8):
            for e3 in range(0, 5):
                m = 2 ** e2 * 3 ** e3
                A, B = arrangements(m, u), arrangements(m, v)
                if not A or not B: continue
                ns += 1
                la = {Lam(m, w) for w, _ in A}; lb = {Lam(m, w) for w, _ in B}
                if len(la) != 1 or len(lb) != 1: badr += 1; continue
                da = dict(next(iter(la))); db = dict(next(iter(lb)))
                for p in set(da) | set(db) | {2, 3}:
                    if 2 * (da.get(p, 0) - db.get(p, 0)) != Hc(u, p) - Hc(v, p): badr += 1
    check("Z2 [NEW] rewrite law: Lambda_p(u) - Lambda_p(v) = (H_p(u) - H_p(v))/2, H_p = total p-adic valuation of the labels  (%d source/rewrite pairs; incl. 2222 <-> 1,8,8 with 3^j, j<=3)" % ns, badr == 0, badr)


def shard_Z3(full=False):
    """[NEW] mixed-index (dimension) forcing for contents 2^al 3^be"""
    exc = []; nb = 0
    for al in range(1, 5):
        for be in range(1, 5):
            for e2 in range(0, 6):
                for e3 in range(0, 3):
                    m = 2 ** e2 * 3 ** e3
                    arr = arrangements(m, {2: al, 3: be})
                    if not arr: continue
                    nb += 1
                    avoid = any(not any(qv(s).get(2, 0) >= 1 and qv(s).get(3, 0) >= 1 for s in path) for _, path in arr)
                    pred = (al == 1 and e3 == 0 and e2 in (1, 2) and be in (1, 2))
                    if avoid != pred: exc.append((al, be, e2, e3))
    check("Z3 [NEW] classification: every arrangement of 2^al 3^be reaches a state with 2,3,6 in D, except exactly (al=1, v3=0, v2 in {1,2}, be in {1,2}) -- brute force over all arrangements (%d cases)" % nb, not exc, exc[:3])
    ok = True
    for n in range(1, 4 if not full else 4):
        for e2 in range(0, 5):
            for e3 in range(0, 3):
                arr = arrangements(2 ** e2 * 3 ** e3, {2: 2 * n, 3: 4 * n})
                for _, path in arr:
                    if not any(qv(s).get(2, 0) >= 1 and qv(s).get(3, 0) >= 1 for s in path): ok = False
    check("Z3 [NEW] n-family 2^(2n) 3^(4n), n<=3, sources v2<=4, v3<=2: all arrangements reach the mixed index; the 1^(7n) route from v3<=1 never has 3 in D", ok)
    # the 1^7n route never activates prime 3 when v3(m)<=1
    ok1 = True
    for e2 in range(0, 8):
        for e3 in (0, 1):
            m = 2 ** e2 * 3 ** e3
            for n in (1, 2, 3):
                if any(3 in qv(s) for s in hist(m, (1,) * (7 * n))): ok1 = False
    check("Z3 [NEW] 1^(7n) route from v3 <= 1 never has q_3 >= 1, so K stays inside the 2-axis (no mixed cell)", ok1)
    ok2 = all(edge(m, 3) is None or vp(edge(m, 3), 2) == vp(m, 2) + 4 for m in range(3, 3000, 3))
    ok3 = all(vp(edge(m, 2), 3) == vp(m, 3) + 2 for m in range(2, 3000, 2))
    check("Z3 [NEW] proof lemmas: label 3 adds 4 to v_2 and label 2 adds 2 to v_3 (so after any 3-label v_2 >= 4)", ok2 and ok3)
    from fractions import Fraction as F
    R = lambda N: F((N + 1) ** 2, N)
    check("Z3 [REG] R(2)^4 = R(1) R(8)^2 = 3^8/2^4 and R(2)^2 R(3)^4 = R(1)^7", R(2) ** 4 == R(1) * R(8) ** 2 == F(3 ** 8, 16) and R(2) ** 2 * R(3) ** 4 == R(1) ** 7)


def t_orbit(x, n):
    s, t = split_sq(x); out = [(s, t)]
    for _ in range(n):
        u, r = split_sq(t + 1); s, t = s * u, r; out.append((s, t))
    return out


def shard_Z4(full=False):
    """[NEW] regime I of the collective map (G = 1): exact reduction, rigid set, eventual rigidity, births"""
    bad = 0; cnt = 0
    for x0 in list(range(4, 160, 4)) + [1140, 4556]:
        x = Fraction(x0); xs = [x]
        for _ in range(26):
            x = Cmap(x); xs.append(x)
        ps = t_orbit(x0, 26)
        if [p[0] ** 2 * p[1] for p in ps] != [int(v) for v in xs]: bad += 1
        cnt += 1
    check("Z4 [NEW] brute-force collective map (D, L, G from the definition) = the (sigma,t) reduction  C(sigma^2 t) = sigma^2 (t+1)  (%d orbits x 26 steps)" % cnt, bad == 0, bad)
    sys.path.insert(0, os.path.join(ROOT, "src", "frozen"))
    import geo1lib
    bad2 = 0
    for x0 in (4, 12, 36, 100, 1140):
        x = Fraction(x0); y = Fraction(x0)
        for _ in range(20):
            x = Cmap(x); y = geo1lib.Cstep(y)
            if Fraction(x) != Fraction(y): bad2 += 1
    check("Z4 [REG] verifier's own C = frozen geo1lib.Cstep (recorded cross-check, 100 steps)", bad2 == 0)
    viol = 0; tot = 0
    for sg in (2, 4, 6):
        for t0 in [t for t in range(1, 130) if sqfree(t)]:
            ps = t_orbit(sg * sg * t0, 70); xs = [p[0] ** 2 * p[1] for p in ps]
            for n in range(60):
                tot += 1
                if (xs[n + 3] == 4 * xs[n]) != (ps[n][1] in (1, 2, 3)): viol += 1
    check("Z4 [NEW] rigid-set theorem: x_{n+3} = 4 x_n  <=>  t_n in {1,2,3}  (%d (orbit,n) pairs)" % tot, viol == 0, viol)
    T = 300000 if full else 120000
    N = T + 6; big = [1] * (N + 1); u = 2
    while u * u <= N:
        for k in range(u * u, N + 1, u * u):
            if u > big[k]: big[k] = u
        u += 1
    def nxt(t): return (t + 1) // (big[t + 1] ** 2)
    mx = 0; arg = None; badb = 0
    for t0 in range(1, T + 1):
        if big[t0] != 1: continue
        t = t0; steps = 0
        while t > 3: t = nxt(t); steps += 1
        k = 0; a = t0
        while a > 3: a = a // 4 + 1; k += 1
        if steps > 4 * k: badb += 1
        if steps > mx: mx = steps; arg = t0
    rec = load("results/REGIME_I.json")["entry_time"]
    check("Z4 [NEW] eventual rigidity in regime I: every squarefree t <= %d reaches {1,2,3}; steps <= 4 kappa3(t); max steps %d at t=%d" % (T, mx, arg), badb == 0, badb)
    if full: check("Z4 [NEW] max entry time up to 300000 equals the recorded builder value", mx == rec["max"], (mx, rec["max"]))
    okb = True
    for sg in (2, 4, 6, 12, 30, 90):
        for t_ in (1, 2, 3):
            ps = t_orbit(sg * sg * t_, 3)
            carry = [i for i in range(1, 4) if ps[i][0] != ps[i - 1][0]]
            if len(carry) != 1 or ps[carry[0]][0] != 2 * ps[carry[0] - 1][0]: okb = False; continue
            sg0 = ps[0][0]; odd = sg0
            while odd % 2 == 0: odd //= 2
            new = len(divs(2 * sg0)) - len(divs(sg0))
            if new != len(divs(odd)) or carry[0] != 4 - t_: okb = False
    check("Z4 [NEW] one rigid carry per period at step 4-t (u = 2), creating exactly tau(odd part of sigma) new occurrence indices (tower sigma=2^k: exactly 1)", okb)
    okm = True
    for x0 in (4, 8, 12, 20, 28, 60, 84, 100, 140):
        ps = t_orbit(x0, 40)
        for a, b in zip(ps, ps[1:]):
            if b[0] % a[0] != 0: okm = False
    check("Z4 [NEW] regime I is monotone: sigma_n | sigma_{n+1}, hence D(x_n) subset D(x_{n+1}) (no losses along a collective trajectory)", okm)


def reach(x, y):
    seen = {}
    def rec(z):
        if z == y: return True
        if z > y: return False
        if z in seen: return seen[z]
        r = False
        for N in divs(z):
            w = edge(z, N)
            if w > y: break
            if rec(w): r = True; break
        seen[z] = r; return r
    return rec(x)


def evmatch(x, y, target):
    seen = {}
    def rec(z, j):
        if z == y: return j == len(target) - 1
        if (z, j) in seen: return seen[(z, j)]
        r = False
        for N in divs(z):
            w = edge(z, N)
            if w > y: break
            s = sigma(w)
            if s == target[j] and rec(w, j): r = True; break
            if j + 1 < len(target) and s == target[j + 1] and rec(w, j + 1): r = True; break
        seen[(z, j)] = r; return r
    return rec(x, 0)


def reduced(seq):
    out = [seq[0]]
    for s in seq[1:]:
        if s != out[-1]: out.append(s)
    return out


def shard_Z5(full=False):
    """[NEW] event correspondence between SELECT-II histories and regime-I trajectories"""
    bad = 0; cnt = 0; same = 0
    for m in range(1, 2201):
        for N in divs(m):
            mp = edge(m, N); cnt += 1; c = 1
            for p, n_ in pf(N).items(): c *= p ** ((n_ // 2) if vp(m, p) % 2 else (n_ + 1) // 2)
            if Fraction(sigma(m) * (N + 1), c) != sigma(mp) or sigma(mp) <= sigma(m): bad += 1
            if Dset(m) == Dset(mp): same += 1
    check("Z5 [NEW] event saturation: every SELECT-II edge has sigma' = sigma (N+1)/c > sigma, so D changes on EVERY edge (%d edges, %d with D unchanged)" % (cnt, same), bad == 0 and same == 0, bad)
    okr = True; nr = 0
    for sg in (2, 4, 6, 8, 10, 12, 14, 30, 36, 60, 210):
        for t in (1, 2, 3):
            x = sg * sg * t; ps = t_orbit(x, 3); xs = [p[0] ** 2 * p[1] for p in ps]
            coll = reduced([p[0] for p in ps]); sel = reduced([sigma(x), sigma(4 * x)])
            nr += 1
            if not (xs[3] == 4 * x and coll == sel and edge(x, 1) == 4 * x): okr = False
    check("Z5 [NEW] rigid domain: on every rigid state C^3 = T_1 and the reduced occurrence-event records agree (all three phases, %d states)" % nr, okr)
    # birth-endpoint theorem, exhaustive over a grid
    bad_b = 0; nb = 0; eq = 0
    for sg in (2, 4, 6, 8):
        for t0 in [t for t in range(1, 41) if sqfree(t)]:
            x0 = sg * sg * t0; ps = t_orbit(x0, 24); xs = [p[0] ** 2 * p[1] for p in ps]
            births = [i for i in range(1, len(ps)) if ps[i][0] != ps[i - 1][0]]
            for n in range(0, 10):
                for m in births:
                    if m <= n: continue
                    j = sum(1 for b in births if n < b <= m)
                    if xs[m] < 4 * xs[n] or xs[m] > 4 ** 6 * xs[n]: continue
                    tgt = reduced([p[0] for p in ps[n:m + 1]])
                    if len(tgt) - 1 != j: continue
                    nb += 1
                    e = reach(xs[n], xs[m]) and evmatch(xs[n], xs[m], tgt)
                    pred = (ps[n][1] == 1)
                    if e != pred: bad_b += 1
                    eq += e
    check("Z5 [NEW] birth-endpoint theorem: for an endpoint that is a birth state, an event-equivalent SELECT-II history exists  <=>  t_n = 1 (x_n a perfect square), and then x_m = 4^j x_n  (%d pairs, %d equivalent)" % (nb, eq), bad_b == 0, bad_b)
    nv = 0; tot = 0
    starts = [s * s * t for s in (2, 4, 6) for t in (1, 2, 3, 5, 6, 7, 10, 11)]
    if full: starts += [s * s * t for s in (8, 10) for t in (1, 2, 3, 5, 6, 7, 10, 11, 13, 14)]
    for x0 in starts:
        ps = t_orbit(x0, 36); xs = [p[0] ** 2 * p[1] for p in ps]
        for n in range(0, 14):
            for m in range(n + 1, min(len(xs), n + 26)):
                if xs[m] > 4 ** 5 * xs[n]: break
                tgt = reduced([p[0] for p in ps[n:m + 1]]); j = len(tgt) - 1
                if j == 0 or xs[m] < 4 * xs[n]: continue
                tot += 1
                e = reach(xs[n], xs[m]) and evmatch(xs[n], xs[m], tgt)
                if e != (xs[m] == 4 ** j * xs[n]): nv += 1
    check("Z5 [finite-exact] all-endpoint classification: event equivalence <=> x_m = 4^j x_n on %d regime-I pairs (%d starts); proof only for birth endpoints" % (tot, len(starts)), nv == 0, nv)
    okf = True; info = []
    for a in range(2, 18):
        N = 2 ** a - 1; sq = all(e == 1 for e in pf(N).values())
        x = N * 4; y = x * (N + 1) ** 2 // N
        ps = t_orbit(x, 400); xs = [p[0] ** 2 * p[1] for p in ps]
        if sq:
            k = xs.index(y) if y in xs else None
            sg = reduced([p[0] for p in ps[:(k + 1)]]) if k is not None else None
            kp = 1 + 3 * a // 2 if a % 2 == 0 else 3 * (a + 1) // 2
            if k != kp or len(sg) - 1 != 1 + (a + 1) // 2 or edge(x, N) != y: okf = False
        else:
            if y in xs: okf = False
        info.append((a, sq))
    check("Z5 [NEW] infinite coincidence family: x=(2^a-1)s^2, 2^a-1 squarefree: C^k(x) = T_N(x) = (2^a s)^2 at k = 1+3a/2 (a even) / 3(a+1)/2 (a odd), with 1+ceil(a/2) collective events versus 1; non-squarefree 2^a-1 (a=6,12) never meets it (a=2..17, s=2)", okf)
    from fractions import Fraction as F
    one = [N for N in range(1, 200001) if F((N + 1) ** 2, N) == 9]
    two = any(F((a + 1) ** 2, a) * F((b + 1) ** 2, b) <= 9 for a in range(1, 4) for b in range(1, 4))
    check("Z5 [NEW] no SELECT-II history has multiplier 9: R(N) = 9 has no solution (N<=2e5; exact: N^2-7N+1=0) and any two edges multiply to >= 16 -- so the G=11 scaling x_{n+8}=9x_n is unreachable", not one and not two)
    rec = load("results/SINGLE_EDGE_COINCIDENCES.json")
    okc = True
    for key, xs0 in rec["scan_x<4000"].items():
        N, k = [int(v) for v in key.strip("()").split(",")]
        for x0 in xs0[:3]:
            ps = t_orbit(x0, k); v = ps[k][0] ** 2 * ps[k][1]
            if v != x0 * (N + 1) ** 2 // N or x0 % N: okc = False
    forms = sorted({f + 1 for f in [int(k.strip("()").split(",")[0]) for k in rec["scan_x<4000"]]})
    shapes = all((f & (f - 1) == 0) or (f % 3 == 0 and (f // 3) & (f // 3 - 1) == 0) for f in forms)
    check("Z5 [finite-exact] recorded single-edge coincidences C^k(x)=T_N(x) re-verified; every N+1 is 2^a or 3*2^a (%d (N,k) classes)" % len(rec["scan_x<4000"]), okc and shapes)


def shard_Z6(full=False):
    """[REG]/[NEW] beyond regime I and the v001 multidimensional examples"""
    S = lambda k: 2 ** 2 * 3 ** (3 + k) * 5 ** 4
    x = Fraction(S(0) ** 2, 11); ok = True; xs = [x]
    K = 3 if not full else 4
    for _ in range(8 * K): x = Cmap(x); xs.append(x)
    for k in range(K):
        for j in range(8):
            if xs[8 * k + j] != Fraction((j + 1) * S(k) ** 2, 11): ok = False
    check("Z6 [REG] FIELD-I v009 T50 eight-step orbit (G=11): x_{8k+j} = (j+1) S_k^2/11, x_{n+8} = 9 x_n -- re-derived from the definition of C (brute-force D)", ok and all(xs[n + 8] == 9 * xs[n] for n in range(8 * (K - 1))))
    okc = True; mxs = 0
    for x0 in range(4, 260):
        if x0 % 4 == 0: continue
        if not Dq(x0): continue
        x = Fraction(x0); n = 0
        while n < 400:
            D = Dq(x)
            if not D: okc = False; break
            G = 0
            for d in D: G = gcd(G, d - 1)
            if G == 1: break
            x = x + Fraction(lcm_list(D) ** 2, G); n += 1
        else: okc = False
        mxs = max(mxs, n)
    check("Z6 [finite-exact] every integer x<260, x not = 0 mod 4, with D(x) nonempty reaches G = 1 (regime I) within %d steps" % mxs, okc)
    rec = load("results/HIGHER_DIMENSIONAL.json")
    EX = {"disconnected_3_primes": (4, (2, 3, 4, 5, 6)), "disconnected_4_primes": (4, (2, 3, 4, 5, 6, 7)), "loop_3_primes": (32, (2, 3, 4, 5, 8)), "loop_4_primes": (24, (2, 3, 4, 5, 6, 7))}
    okh = True
    for name, (m, al) in EX.items():
        words = [w for w in permutations(al) if hist(m, w) is not None]; ws = set(words); par = {w: w for w in words}
        def fd(a):
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        for w in words:
            for i in range(len(w) - 1):
                v = w[:i] + (w[i + 1], w[i]) + w[i + 2:]
                if v in ws: par[fd(w)] = fd(v)
        ncomp = len({fd(w) for w in words})
        lam = set()
        for w in words:
            path = hist(m, w); out = {}
            for i in range(len(w)):
                a, b = qv(path[i]), qv(path[i + 1])
                for p in set(a) | set(b):
                    if b.get(p, 0) < a.get(p, 0): out[p] = out.get(p, 0) + a.get(p, 0) - b.get(p, 0)
            lam.add(tuple(sorted(out.items())))
        allp = set(); peak = 0
        for w in words:
            for s in hist(m, w): allp |= set(pf(s)); peak = max(peak, len(qv(s)))
        A = len({p for N in al for p in pf(N)})
        r = rec[name]
        if not (r["components"] == ncomp and len(lam) == 1 and r["Lambda_constant_on_whole_complex"] and r["V_valuation_coordinates"] == len(allp)
                and r["A_active_constraint_primes"] == A and r["R_history_complex_dim"] == len(al) - 1 and r["G_realized_geometry_dim_peak"] == peak):
            okh = False
    check("Z6 [NEW] v001 3- and 4-prime examples: components, constant loss budget Lambda on the WHOLE route complex, and the four distinct dimension counts (V,A,R,G) re-derived", okh)


def shard_Z7(full=False):
    """builder cross-check, manifest, documents"""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import geo_snapshots as GS, field_regimes as FRm, event_correspondence as EC, geometric_history as GH
    rng = random.Random(5); ok = True
    for _ in range(300):
        m = rng.choice([2, 3, 5, 7]) ** rng.randint(0, 7) * rng.choice([2, 3, 5]) ** rng.randint(0, 5) * rng.choice([3, 7]) ** rng.randint(0, 3)
        cf = GS.closed_form(m)
        a = qv(m)
        if (cf is None) != (not a): ok = False; continue
        if cf and (cf["q"] != [a[p] for p in sorted(a)] or cf["nF"] != prod(x + 1 for x in a.values()) - 1 or cf["sigma"] != sigma(m)): ok = False
    check("Z7 builder closed forms = verifier on 300 random states", ok)
    ok2 = all([FRm.value(p) for p in FRm.orbit_pairs(x0, 30)] == [p[0] ** 2 * p[1] for p in t_orbit(x0, 30)] for x0 in (4, 12, 20, 60, 100, 1140))
    check("Z7 builder (sigma,t) orbits = verifier orbits", ok2)
    ok3 = all(EC.sigma_transport(m, N) == Fraction(sigma(edge(m, N)), sigma(m)) for m in range(1, 400) for N in divs(m))
    check("Z7 builder sigma transport = verifier on all edges m<400", ok3)
    st = open(os.path.join(ROOT, "theory", "THEOREMS.md")).read()
    check("Z7 THEOREMS.md lists B2-T1..B2-T14 with PROVED / FINITE-EXACT / OPEN tags", all(("B2-T%d" % i) in st for i in range(1, 15)) and "PROVED" in st and "FINITE-EXACT" in st and "OPEN" in st)
    op = open(os.path.join(ROOT, "theory", "OPEN_PROBLEMS.md")).read()
    check("Z7 OPEN_PROBLEMS.md keeps the five levels of correspondence apart and claims no organizing law", "Level 5" in op and "no common law" in op.lower())
    mp = os.path.join(ROOT, "MANIFEST.json")
    if os.path.exists(mp):
        mf = json.load(open(mp))["files"]
        check("Z7 MANIFEST hashes match", all(sha(os.path.join(ROOT, p)) == h for p, h in mf.items() if p != "results/VERIFY_LAST.json"))


SHARDS = {"Z0": shard_Z0, "Z1": shard_Z1, "Z2": shard_Z2, "Z3": shard_Z3, "Z4": shard_Z4, "Z5": shard_Z5, "Z6": shard_Z6, "Z7": shard_Z7}

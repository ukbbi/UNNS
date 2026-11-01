"""v005 INDEPENDENT planar audit of P4-P1 (CP3-A).  From-scratch code: shares nothing with the pinned engine or geo3.py.
For random nested rank-2 lattices Lambda <= Lambda' of Z^2 (row HNF) and boxes Q, every 2-cell C of U(Lambda,Q) is tested EXACTLY (Fractions) for
C <= U(Lambda',Q) by convex-polygon subtraction (C is contained iff area(C minus union of closed 2-cells of Lambda') = 0; lower-dimensional target cells have
measure zero and U is closed).  Hard cells (P4-Z2 robust form) are additionally checked against the structure (1)-(7) of the proof of P4-P1."""
import sys, os, random, json, time
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mini


def hnf2_all(n):
    out = []
    for a in range(1, n + 1):
        if n % a == 0:
            b = n // a
            for x in range(b):
                out.append(((a, x), (0, b)))
    return out


def member2(B):
    (a, x), (_, b) = B
    def f(v):
        i, r = divmod(v[0], a)
        return r == 0 and (v[1] - i * x) % b == 0
    return f


def axis_order(member, axis, cap=10 ** 4):
    for t in range(1, cap):
        v = [0, 0]; v[axis] = t
        if member(tuple(v)): return t


def sub_of(Bp, M):
    """lattice with basis rows M.Bp, returned as HNF2"""
    rows = [[sum(M[i][k] * Bp[k][c] for k in range(2)) for c in range(2)] for i in range(2)]
    # row-style HNF
    r = [list(x) for x in rows]
    while r[1][0] != 0:
        q = r[0][0] // r[1][0] if r[1][0] else 0
        r[0] = [r[0][c] - q * r[1][c] for c in range(2)]
        r[0], r[1] = r[1], r[0]
    if r[0][0] < 0: r[0] = [-x for x in r[0]]
    if r[1][1] < 0: r[1] = [-x for x in r[1]]
    r[0][1] %= r[1][1]
    return ((r[0][0], r[0][1]), (r[1][0], r[1][1]))


# ------------------------------------------------------------ exact convex polygon arithmetic
def clip(poly, a, c, le=True):
    out = []; n = len(poly)
    def val(p): return a[0] * p[0] + a[1] * p[1] - c
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        vp, vq = val(p), val(q)
        ip = vp <= 0 if le else vp >= 0
        iq = vq <= 0 if le else vq >= 0
        if ip: out.append(p)
        if (vp < 0 < vq) or (vq < 0 < vp):
            t = vp / (vp - vq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    ded = []
    for p in out:
        if not ded or ded[-1] != p: ded.append(p)
    if len(ded) > 1 and ded[0] == ded[-1]: ded.pop()
    return ded


def area2(poly):
    s = 0
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        s += p[0] * q[1] - p[1] * q[0]
    return s / 2


def parallelogram(base, g, h):
    pts = [tuple(map(Fr, base)), (Fr(base[0] + g[0]), Fr(base[1] + g[1])), (Fr(base[0] + g[0] + h[0]), Fr(base[1] + g[1] + h[1])), (Fr(base[0] + h[0]), Fr(base[1] + h[1]))]
    if g[0] * h[1] - g[1] * h[0] < 0: pts.reverse()
    return pts


def halfplanes(poly):
    hs = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        a = (q[1] - p[1], -(q[0] - p[0]))
        hs.append((a, a[0] * p[0] + a[1] * p[1]))
    return hs


def subtract(pieces, target):
    hs = halfplanes(target)
    out = []
    for P in pieces:
        rest = P
        for a, c in hs:
            outside = clip(rest, a, c, le=False)
            if len(outside) >= 3 and area2(outside) > 0: out.append(outside)
            rest = clip(rest, a, c, le=True)
            if len(rest) < 3 or area2(rest) == 0: break
    return out


def bbox_poly(poly):
    return (min(p[0] for p in poly), min(p[1] for p in poly), max(p[0] for p in poly), max(p[1] for p in poly))


def contained_2cell(base, gens, target_polys):
    src = parallelogram(base, gens[0], gens[1])
    sb = bbox_poly(src); pieces = [src]
    for tb, tp in target_polys:
        if tb[0] > sb[2] or tb[2] < sb[0] or tb[1] > sb[3] or tb[3] < sb[1]: continue
        pieces = subtract(pieces, tp)
        if not pieces: return True, None
    P = pieces[0]
    cx = sum(p[0] for p in P) / len(P); cy = sum(p[1] for p in P) / len(P)
    return False, (cx, cy)


def hard_structure_ok(base, gens, kp, lp):
    """steps (1)-(6) of the proof of P4-P1 for a hard cell: returns (ok, detail)"""
    V = mini.corners(tuple(base), [tuple(g) for g in gens])
    A = [v for v in V if v[0] == 0]; B = [v for v in V if v[1] == 0]
    if not A or not B: return False, "no axis corners"
    A, B = A[0], B[0]
    others = [v for v in V if v not in (A, B)]
    if len(others) != 2 or (A[0] + B[0], A[1] + B[1]) != (others[0][0] + others[1][0], others[0][1] + others[1][1]): return False, "A,B not opposite"
    if not all(v[0] >= kp and v[1] >= lp for v in others): return False, "D,E not >= (k',l')"
    if not all(Fr(v[0], kp) + Fr(v[1], lp) >= 2 for v in V): return False, "half-plane bound"
    if not (A[1] % lp == 0 and B[0] % kp == 0 and A[1] >= 2 * lp and B[0] >= 2 * kp): return False, "x0,y0 divisibility"
    return True, "ok"


def audit(seed, n_lattices, qmax, nmax_src=6, nmax_tgt=6, max_cells_per=400, time_budget=None):
    rng = random.Random(seed)
    stats = dict(pairs=0, runs=0, cells2=0, hard=0, structure_violations=0, failures=0, boxes=0)
    fails = []
    t0 = time.time()
    tgts = [(n, Bp) for n in range(1, nmax_tgt + 1) for Bp in hnf2_all(n)]
    for _ in range(n_lattices):
        if time_budget and time.time() - t0 > time_budget: break
        n, Bp = rng.choice(tgts)
        m = rng.randint(1, nmax_src)
        Ms = hnf2_all(m)
        M = rng.choice(Ms)
        B = sub_of(Bp, [list(M[0]), list(M[1])])
        mB, mBp = member2(B), member2(Bp)
        assert all(mBp(r) for r in B)
        kp, lp = axis_order(mBp, 0), axis_order(mBp, 1)
        stats['pairs'] += 1
        for _ in range(2):
            Q = (rng.randint(1, qmax), rng.randint(1, qmax))
            sc, _, _ = mini.cells(mB, Q, maxdim=2)
            tc, _, _ = mini.cells(mBp, Q, maxdim=2)
            tpolys = [(bbox_poly(p), p) for p in (parallelogram(b, g[0], g[1]) for b, g in tc if len(g) == 2)]
            stats['boxes'] += 1
            for b, g in sc:
                if len(g) != 2: continue
                stats['cells2'] += 1
                ok, wit = contained_2cell(b, g, tpolys)
                if not ok:
                    stats['failures'] += 1; fails.append(dict(B=B, Bp=Bp, Q=Q, base=b, gens=g, witness=[str(x) for x in wit]))
                # hardness (P4-Z2 robust)
                mc = tuple(b[c] + sum(min(x[c], 0) for x in g) for c in range(2))
                if mc == (0, 0) and all(mBp(tuple(max(v, 0) for v in x)) and mBp(tuple(min(v, 0) for v in x)) for x in g):
                    stats['hard'] += 1
                    sok, why = hard_structure_ok(b, g, kp, lp)
                    if not sok: stats['structure_violations'] += 1; fails.append(dict(kind='structure', why=why, B=B, Bp=Bp, Q=Q, base=b, gens=g))
            stats['runs'] += 1
    stats['seconds'] = round(time.time() - t0, 1)
    return stats, fails


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    qm = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    st, fl = audit(seed, n, qm)
    print(json.dumps(st)); print(len(fl), "failures")


def hard_driven_audit(seed, n_pairs, time_budget=None, nmax_src=4, nmax_tgt=4, cap=14):
    """enumerate ALL hard cells (P4-Z2 robust form; base forced = -sum g_i^-) of random nested pairs inside Qmax=(3k'+2,3l'+2) and test each EXACTLY
    against U(Lambda', Q_C), Q_C = bounding box of the cell (the worst box); check the proof structure on every one."""
    rng = random.Random(seed)
    tgts = [(n, Bp) for n in range(1, nmax_tgt + 1) for Bp in hnf2_all(n)]
    stats = dict(pairs=0, hard=0, structure_violations=0, failures=0, distinct_boxes=0); fails = []
    t0 = time.time()
    for _ in range(n_pairs):
        if time_budget and time.time() - t0 > time_budget: break
        n, Bp = rng.choice(tgts)
        M = rng.choice(hnf2_all(rng.randint(2, nmax_src)))
        B = sub_of(Bp, [list(M[0]), list(M[1])])
        mB, mBp = member2(B), member2(Bp)
        kp, lp = axis_order(mBp, 0), axis_order(mBp, 1)
        Qm = (min(4 * kp + 3, cap), min(4 * lp + 3, cap))
        G = [g for g in mini.graver_region(mB, Qm) if mini.lexpos(g)]
        H = [g for g in G if mBp((max(g[0], 0), max(g[1], 0))) and mBp((min(g[0], 0), min(g[1], 0)))]
        stats['pairs'] += 1
        cache = {}
        for i in range(len(H)):
            for j in range(i + 1, len(H)):
                g, h = H[i], H[j]
                if g[0] * h[1] - g[1] * h[0] == 0: continue
                u = (-(min(g[0], 0) + min(h[0], 0)), -(min(g[1], 0) + min(h[1], 0)))
                cs = mini.corners(u, [g, h])
                if not mB(u) or any(not any(c) for c in cs) or any(c[0] > Qm[0] or c[1] > Qm[1] for c in cs): continue
                QC = (max(c[0] for c in cs), max(c[1] for c in cs))
                if QC not in cache:
                    tc, _, _ = mini.cells(mBp, QC, maxdim=2)
                    cache[QC] = [(bbox_poly(p), p) for p in (parallelogram(b, x[0], x[1]) for b, x in tc if len(x) == 2)]
                    stats['distinct_boxes'] += 1
                stats['hard'] += 1
                sok, why = hard_structure_ok(u, [g, h], kp, lp)
                if not sok: stats['structure_violations'] += 1; fails.append(dict(kind='structure', why=why, B=B, Bp=Bp, base=u, gens=[g, h]))
                ok, wit = contained_2cell(u, [g, h], cache[QC])
                if not ok: stats['failures'] += 1; fails.append(dict(kind='noncontained', B=B, Bp=Bp, Q=QC, base=u, gens=[g, h], witness=[str(x) for x in wit]))
    stats['seconds'] = round(time.time() - t0, 1)
    return stats, fails

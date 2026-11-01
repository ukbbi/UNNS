"""v005 3D hard-cell scan.  For every pair Lambda <= Lambda' of Z^3 (Lambda' without a free coordinate unless --free) enumerate ALL hard cells
(P4-Z2 robust form) with bounding box <= Qmax, and test each against U(Lambda', Q_C), Q_C = its own bounding box (the worst box).
Screening: exact-rational sample points (lambda in {1/3,1/2,2/3}^j); an uncovered sample point is re-checked EXACTLY with the engine's in_cell."""
import sys, time, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'engine'))
import numpy as np, geo3
import exact_containment as ec
from fractions import Fraction

def sample_pts(u, gens, vals):
    pts = []
    import itertools
    for lam in itertools.product(vals, repeat=len(gens)):
        pts.append([float(u[c]) + sum(l * float(g[c]) for l, g in zip(lam, gens)) for c in range(3)])
    return np.array(pts)

def cover_all(C, P, Qc, eps=1e-9):
    """boolean array: which sample points are covered by a cell with bbox <= Qc"""
    cov = np.zeros(len(P), dtype=bool)
    lo = P.min(0) - eps; hi = P.max(0) + eps
    for j in (3, 2, 1, 0):
        A = C.arr[j]
        if A is None: continue
        base, Minv, l, h = A
        m = (l <= hi).all(1) & (h >= lo).all(1) & (h <= Qc).all(1)
        if not m.any(): continue
        b, Mi = base[m], Minv[m]
        lam = np.einsum('nij,pnj->pni', Mi, P[:, None, :] - b[None])
        ok = (lam[..., :j] >= -eps).all(2) & (lam[..., :j] <= 1 + eps).all(2)
        if j < 3: ok &= (np.abs(lam[..., j:]) <= eps).all(2)
        cov |= ok.any(1)
        if cov.all(): break
    return cov

def exact_uncovered(C, p, Qc):
    pl = [int(np.floor(float(x))) for x in p]; ph = [int(np.ceil(float(x))) for x in p]
    for base, gs in C.targets_for(pl, ph, Qc):
        if ec.in_cell(base, gs, p): return False
    return True

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--nmax', type=int, default=6); ap.add_argument('--mmax', type=int, default=6)
    ap.add_argument('--cap', type=int, default=12); ap.add_argument('--mult', type=int, default=3)
    ap.add_argument('--shard', type=int, default=0); ap.add_argument('--nshards', type=int, default=1)
    ap.add_argument('--free', action='store_true'); ap.add_argument('--out', default='scan.json')
    ap.add_argument('--nmin', type=int, default=2)
    ap.add_argument('--targets-json', default=None, help='explicit list of target HNF bases to scan instead of the enumeration')
    ap.add_argument('--mmin', type=int, default=2)
    a = ap.parse_args()
    vals2 = [Fraction(1, 6), Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(5, 6)]
    vals3 = [Fraction(1, 6), Fraction(1, 2), Fraction(5, 6)]
    targets = []
    if a.targets_json:
        for Bp in json.load(open(a.targets_json)):
            Bp = tuple(tuple(r) for r in Bp)
            targets.append((geo3.index_of(Bp), Bp, geo3.axis_orders(Bp)))
    for n in (range(a.nmin, a.nmax + 1) if not a.targets_json else []):
        for Bp in geo3.hnf3_enum(n):
            k = geo3.axis_orders(Bp)
            nofree = min(k) >= 2
            if nofree != (not a.free): continue
            targets.append((n, Bp, k))
    targets = targets[a.shard::a.nshards]
    res = dict(args=vars(a), per_target=[], violations=[], stats=dict(pairs=0, hard=0, hard2=0, hard3=0, noncontained=0, float_alarm=0, covered=0))
    t0 = time.time()
    for n, Bp, k in targets:
        Qmax = tuple(min(a.mult * ki, a.cap) for ki in k)
        C = geo3.Complex(Bp, Qmax)
        th = 0; tn = 0
        for m in range(a.mmin, a.mmax + 1):
            for M in geo3.hnf3_enum(m):
                B = geo3.sublattice(Bp, M)
                G = geo3.lexpos(geo3.graver(B, Qmax))
                hc = geo3.hard_cells(G, B, Bp, Qmax)
                res['stats']['pairs'] += 1
                for u, gens in hc:
                    Qc = np.array(u) + sum((np.maximum(g, 0) for g in gens), np.zeros(3, dtype=np.int64))
                    vals = vals2 if len(gens) == 2 else vals3
                    P = sample_pts(u, gens, [float(v) for v in vals])
                    cov = cover_all(C, P, Qc)
                    res['stats']['hard'] += 1; th += 1
                    res['stats']['hard%d' % len(gens)] += 1
                    if cov.all():
                        res['stats']['covered'] += 1
                    else:
                        idx = int(np.argmin(cov))
                        lam_pts = []
                        import itertools
                        lam = list(itertools.product(vals, repeat=len(gens)))[idx]
                        p = tuple(Fraction(int(u[c])) + sum(l * int(g[c]) for l, g in zip(lam, gens)) for c in range(3))
                        if exact_uncovered(C, p, Qc):
                            res['stats']['noncontained'] += 1; tn += 1
                            res['violations'].append(dict(Bp=Bp, B=B, k=k, u=[int(x) for x in u], gens=[[int(x) for x in g] for g in gens],
                                                          Qc=[int(x) for x in Qc], witness=[str(x) for x in p]))
                        else:
                            res['stats']['float_alarm'] += 1
        res['per_target'].append(dict(n=n, Bp=Bp, k=k, Qmax=Qmax, hard=th, noncontained=tn))
        print(n, Bp, k, Qmax, 'hard', th, 'viol', tn, round(time.time() - t0), flush=True)
        json.dump(res, open(a.out, 'w'))
    print(res['stats'])

if __name__ == '__main__':
    main()

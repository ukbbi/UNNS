"""Radius-two ball intersection census (v006).  B_2(x) with typed words (+ forward, - backward); meeting pairs (word_x, word_y) for d(x,y) <= 4.
Exact: complete neighbourhoods from exact_lib (Pollard rho, deterministic Miller-Rabin below 3.18e23)."""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import factor, _divisors
def moves(n, fn):
    """typed neighbours: list of (letter, label, y, f_y)"""
    out = []
    for N in _divisors(fn):
        y = n // N * (N + 1) ** 2; fy = dict(fn)
        for p, e in factor(N).items():
            fy[p] = fy.get(p, 0) - e
            if fy[p] == 0: del fy[p]
        for p, e in factor(N + 1).items(): fy[p] = fy.get(p, 0) + 2 * e
        out.append(("+", N, y, fy))
    for q in _divisors(fn, cap=lambda e: e // 2):
        if q >= 2:
            N = q - 1; y = n // (q * q) * N; fy = dict(fn)
            for p, e in factor(q).items():
                fy[p] = fy.get(p, 0) - 2 * e
                if fy[p] == 0: del fy[p]
            for p, e in factor(N).items(): fy[p] = fy.get(p, 0) + e
            out.append(("-", N, y, fy))
    return out
def ball2(x):
    """dict vertex -> {word: labels}  for words of length 0,1,2 (labels = tuple of N's)"""
    fx = factor(x); res = {x: {"": ()}}
    for l1, N1, y1, f1 in moves(x, fx):
        res.setdefault(y1, {}).setdefault(l1, (N1,))
        for l2, N2, y2, f2 in moves(y1, f1):
            res.setdefault(y2, {}).setdefault(l1 + l2, (N1, N2))
    return res
def meetings(x, y):
    """minimal total length and the set of (wx, wy) meeting word pairs of that length (<=4), or None"""
    bx, by = ball2(x), ball2(y); best = None; pairs = set()
    small, large = (bx, by) if len(bx) < len(by) else (by, bx)
    for z in small:
        if z in large:
            for wa in bx.get(z, {}):
                for wb in by.get(z, {}):
                    s = len(wa) + len(wb)
                    if best is None or s < best: best = s; pairs = set()
                    if s == best: pairs.add((wa, wb))
    return best, pairs
if __name__ == "__main__":
    for n in (11, 13, 3239, 5039):
        print(n, meetings(10**6 * n, 10**6 * (n + 1)))

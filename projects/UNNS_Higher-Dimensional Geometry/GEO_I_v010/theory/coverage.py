"""Exact test of  U = conv(F)  for k = 2 by convex-piece subtraction (no arrangement needed).
conv(F) minus the union of the 2-cells is computed exactly as a list of convex pieces (rational vertices); empty <=> U = conv(F).
Used for the finite base-window certificates of the stabilization theorem."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fractions import Fraction as Fr
try:
    from gmpy2 import mpq
except Exception:
    mpq = Fr
from lattice_model import *
from realization import maximal_cells


def hull(P):
    P = sorted(set(P))
    if len(P) <= 2: return P
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo = []
    for p in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(P):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]            # counter-clockwise


def area2(poly):
    s = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return s


def clip(poly, a, b, c):
    """part of convex polygon poly with a x + b y <= c (closed).  returns vertex list (maybe degenerate)."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if fp <= 0: out.append(p)
        if (fp < 0 and fq > 0) or (fp > 0 and fq < 0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def cell_halfplanes(u, g, h):
    """parallelogram u + [0,1]g + [0,1]h  as 4 halfplanes a x + b y <= c (integers)."""
    hp = []
    # sides parallel to g: normal n = (g_y, -g_x) up to sign; the cell lies between the line through u and the line through u+h
    for (v, w) in ((g, h), (h, g)):
        nx, ny = v[1], -v[0]
        c0 = nx * u[0] + ny * u[1]; c1 = c0 + nx * w[0] + ny * w[1]
        lo, hi = (c0, c1) if c0 <= c1 else (c1, c0)
        hp.append((nx, ny, hi)); hp.append((-nx, -ny, -lo))
    return hp


def uncovered(L, Q):
    """list of convex pieces of conv(F) not covered by 2-cells; None if F is empty / degenerate."""
    cd = complex_data(L, Q)
    if cd is None: return None
    F = cd['F']; H = hull(F)
    if len(H) < 3: return []
    pieces = [[(mpq(x), mpq(y)) for x, y in H]]
    cells2 = [c for c in cd['cells'][2]] if len(cd['cells']) > 2 else []
    cells2.sort(key=lambda c: -abs(c[1][0][0] * c[1][1][1] - c[1][0][1] * c[1][1][0]))
    for (u, (g, h)) in cells2:
        bb = (min(u[0], u[0] + g[0], u[0] + h[0], u[0] + g[0] + h[0]), max(u[0], u[0] + g[0], u[0] + h[0], u[0] + g[0] + h[0]),
              min(u[1], u[1] + g[1], u[1] + h[1], u[1] + g[1] + h[1]), max(u[1], u[1] + g[1], u[1] + h[1], u[1] + g[1] + h[1]))
        hp = cell_halfplanes(u, g, h); new = []
        for pc in pieces:
            xs = [p[0] for p in pc]; ys = [p[1] for p in pc]
            if max(xs) < bb[0] or min(xs) > bb[1] or max(ys) < bb[2] or min(ys) > bb[3]: new.append(pc); continue
            rem = pc
            for (a, b, c) in hp:
                outp = clip(rem, -a, -b, -c)           # a x + b y >= c  (outside of that halfplane)
                if len(outp) >= 3 and area2(outp) > 0: new.append(outp)
                rem = clip(rem, a, b, c)
                if len(rem) < 3 or area2(rem) <= 0: rem = None; break
        pieces = new
        if not pieces: return []
    return pieces


def is_hull_covered(L, Q):
    r = uncovered(L, Q)
    return None if r is None else (len(r) == 0)

"""GEO-I v005, Programme A.  Uniform proof of G5-C1 for s = +1 and s = -1 (all d >= 2) by the LAYER CONSTRUCTION, with a machine check
of every cell the proof uses.

SETTING.  Gamma = Gamma_(d,s), s = +-1, box Q=(Q1,Q2) >= (d,d), Q != (d,d), F = Gamma cap [0,Q] \\ {0}, H = conv(F).
Layers (level sets of the integer functional D):
   s = -1 : D = (i+j)/d  = m ,  1 <= m <= M = floor((Q1+Q2)/d) ;  layer m = { (p, md-p) : alpha_m <= p <= beta_m }
            alpha_m = max(0, md-Q2), beta_m = min(Q1, md) ;  in-layer step e = (1,-1) ;  bridges h(a) = (a, d-a), a = q-p in [0,d].
   s = +1 : D = (j-i)/d  = m ,  -floor(Q1/d) <= m <= floor(Q2/d) ;  layer m = { (p, p+md) } , p in [alpha_m, beta_m],
            alpha_m = max(0,-md) (+1 if m = 0: the origin is missing), beta_m = min(Q1, Q2-md) ;  e = (1,1) ; bridges h(a) = (a, a+d), a in [-d,0].
All in-layer steps e and all bridges h(a) are Graver vectors (explicit Graver sets, pure_lattice).
PROOF (see STABILIZATION.md).  (1) H cap {D = m} = conv(layer m) and the lower/upper boundary of H is linear between consecutive integer D,
hence H = union of trapezoids T_m = conv(L_m u L_{m+1}).  (2) If both layers have >= 2 points, a monotone lattice path in the band a in [alo,ahi]
from (alpha_m,alpha_{m+1}) to (beta_m-1,beta_{m+1}-1) exists; consecutive parallelograms P(point(m,p); e, h(q-p)) overlap on every slice, so their union
is T_m.  (3) If the extreme layer is a single point p, the whole triangle conv(p u L_nbr) is half of ONE parallelogram with corners p, v_alpha, v_beta,
v_alpha+v_beta-p.  This module builds exactly these cells and checks them (corners in F, generators Graver, independent; exact coverage of H)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pure_lattice import fibre, graver_s_plus, graver_s_minus
import coverage as C
from coverage import mpq


def layers(d, s, Q):
    """returns dict m -> (alpha, beta, point(p)), plus e and band."""
    Q1, Q2 = Q
    if s == -1:
        L = {m: (max(0, m * d - Q2), min(Q1, m * d)) for m in range(1, (Q1 + Q2) // d + 1)}
        pt = lambda m, p: (p, m * d - p); e = (1, -1); band = (0, d)
    elif s == 1:
        L = {}
        for m in range(-(Q1 // d), Q2 // d + 1):
            a, b = max(0, -m * d), min(Q1, Q2 - m * d)
            if m == 0: a = 1
            L[m] = (a, b)
        pt = lambda m, p: (p, p + m * d); e = (1, 1); band = (-d, 0)
    else: raise ValueError('s must be +1 or -1')
    return L, pt, e, band


def proof_cells(d, s, Q):
    """the cells used by the proof, as (corner-set, base, g, h)."""
    L, pt, e, band = layers(d, s, Q)
    ms = sorted(L); cells = []; notes = []
    def add(base, g, h): cells.append((base, g, h))
    def sub(a, b): return (a[0] - b[0], a[1] - b[1])
    for m in ms[:-1]:
        a0, b0 = L[m]; a1, b1 = L[m + 1]
        n0, n1 = b0 - a0 + 1, b1 - a1 + 1
        if n0 >= 2 and n1 >= 2:                                                   # monotone path (step 2 of the proof)
            p, q = a0, a1; pe, qe = b0 - 1, b1 - 1
            alo, ahi = band
            while True:
                add(pt(m, p), e, sub(pt(m + 1, q), pt(m, p)))
                if (p, q) == (pe, qe): break
                a = q - p
                if p < pe and a - 1 >= alo: p += 1                                 # step p: a decreases by 1
                elif q < qe and a + 1 <= ahi: q += 1                               # step q: a increases by 1
                else: raise RuntimeError('no monotone path (proof step 2 violated) at %s' % ((m, p, q),))
        elif n0 == 1 or n1 == 1:                                                  # extreme single-point layer (step 3)
            if n1 == 1 and n0 >= 2:                                               # apex on the top
                apex = pt(m + 1, a1); va, vb = pt(m, a0), pt(m, b0)
            elif n0 == 1 and n1 >= 2:                                             # apex at the bottom
                apex = pt(m, a0); va, vb = pt(m + 1, a1), pt(m + 1, b1)
            else:
                notes.append('both layers single'); continue
            add(apex, sub(va, apex), sub(vb, apex))
    return cells, notes


def verify_box(d, s, Q):
    """machine check of the proof's cell list for one box.  returns dict(ok, ...)."""
    F = set(fibre(d, s, Q)); G = graver_s_plus(d) if s == 1 else graver_s_minus(d)
    cells, notes = proof_cells(d, s, Q)
    ok_cells = True; bad = None; polys = []
    for (u, g, h) in cells:
        corners = [u, (u[0] + g[0], u[1] + g[1]), (u[0] + h[0], u[1] + h[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1])]
        legit = all(c in F for c in corners) and (g in G) and (h in G) and (g[0] * h[1] - g[1] * h[0] != 0)
        if not legit: ok_cells = False; bad = (u, g, h); break
    if not ok_cells: return {'Q': Q, 'ok': False, 'why': 'illegal cell', 'cell': bad}
    H = C.hull(sorted(F))
    pieces = [[(mpq(x), mpq(y)) for x, y in H]]
    for (u, g, h) in sorted(cells, key=lambda c: -abs(c[1][0] * c[2][1] - c[1][1] * c[2][0])):
        hp = C.cell_halfplanes(u, g, h); new = []
        for pc in pieces:
            rem = pc
            for (a, b, c) in hp:
                outp = C.clip(rem, -a, -b, -c)
                if len(outp) >= 3 and C.area2(outp) > 0: new.append(outp)
                rem = C.clip(rem, a, b, c)
                if len(rem) < 3 or C.area2(rem) <= 0: rem = None; break
        pieces = new
        if not pieces: break
    return {'Q': Q, 'ok': not pieces, 'n_cells': len(cells), 'uncovered_pieces': len(pieces), 'notes': notes}

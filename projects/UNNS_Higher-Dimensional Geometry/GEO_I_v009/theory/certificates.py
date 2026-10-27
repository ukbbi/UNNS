"""GEO-I v005, G5-T6.  Effective, independently checkable witness certificates.

A CERTIFICATE of non-embeddedness of K_abs(Lambda,q) is  (res, b, q, u, A, v, B, t, l)  where
   Lambda = { alpha : prod r_i^alpha_i = 1 mod b },  A=(g_1..g_r), B=(h_1..h_s) lex-positive Graver vectors,
   u,v in Lambda, the 2^r corners of P(u;A) and the 2^s corners of P(v;B) lie in [0,q] \\ {0},
   (u,A) != (v,B) as cells, and rationals t_i, l_j in (0,1) with   u + sum t_i g_i = v + sum l_j h_j .
It proves (T-REL) that two distinct cells of K_abs share a relative-interior point, hence K_abs is not embedded.  Verification uses only
integer/rational arithmetic and a brute-force Graver test; it shares no code with the search.  `witness_d_span` etc. are then read off
(rank over Q) from the same data.  Minimality of a box (all predecessors embedded) is certified separately by the exact LP audit."""
import os, sys, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'geometry'))


def _in_lambda(res, b, a):
    x = 1
    for r, e in zip(res, a):
        x = x * (pow(r, e, b) if e >= 0 else pow(pow(r, -1, b), -e, b)) % b
    return x == 1 % b


def _rank(vs):
    M = [[Fr(x) for x in v] for v in vs]; r = 0
    for c in range(len(M[0]) if M else 0):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * bb for a, bb in zip(M[i], M[r])]
        r += 1
    return r


def _is_graver(res, b, g):
    ranges = [range(0, x + 1) if x >= 0 else range(x, 1) for x in g]
    for w in itertools.product(*ranges):
        if any(w) and tuple(w) != tuple(g) and _in_lambda(res, b, w): return False
    return _in_lambda(res, b, g)


def _lexpos(g):
    for c in g:
        if c: return c > 0
    return False


def _corners(u, A):
    pts = [tuple(u)]
    for g in A: pts = pts + [tuple(a + c for a, c in zip(p, g)) for p in pts]
    return pts


def relint_coefficients(W, delta):
    """rationals c_j in (0,1) with sum c_j W_j = delta (exact), via the exact LP of the template criterion; None if delta not in the open zonotope."""
    from exactlp import lp_box
    from obstruction_templates import _solve_unique, rank
    m, n = len(W), len(delta)
    if rank(W) == m:
        t = _solve_unique(W, delta)
        return t if t is not None and all(0 < x < 1 for x in t) else None
    c0 = [Fr(sum(w[i] for w in W), 2) for i in range(n)]
    dc = [Fr(delta[i]) - c0[i] for i in range(n)]
    A = [[Fr(W[j][i]) for j in range(m)] + [-dc[i]] for i in range(n)]
    st, val, z = lp_box(A, [Fr(x) for x in delta], [0] * m + [1], m + 1)
    if st != 'optimal' or val <= 0: return None
    lam = Fr(z[m]); return [(Fr(z[j]) + lam / 2) / (1 + lam) for j in range(m)]


def make_certificate(res, b, q, witness):
    """witness: dict from witness_dimension (A,B,delta,base=[u,v])."""
    u, v = witness['base']; A = [tuple(a) for a in witness['A']]; B = [tuple(x) for x in witness['B']]
    W = [tuple(g) for g in A] + [tuple(-c for c in h) for h in B]
    delta = tuple(vi - ui for ui, vi in zip(u, v))
    co = relint_coefficients(W, delta)
    assert co is not None
    return {'res': list(res), 'b': b, 'q': list(q), 'u': list(u), 'v': list(v), 'A': [list(a) for a in A], 'B': [list(x) for x in B],
            't': [str(x) for x in co[:len(A)]], 'l': [str(x) for x in co[len(A):]]}


def verify_certificate(c):
    """independent verification; returns (ok, info)."""
    res, b, q = tuple(c['res']), c['b'], tuple(c['q']); k = len(res)
    u, v = tuple(c['u']), tuple(c['v']); A = [tuple(a) for a in c['A']]; B = [tuple(x) for x in c['B']]
    t = [Fr(x) for x in c['t']]; l = [Fr(x) for x in c['l']]
    why = []
    if not (_in_lambda(res, b, u) and _in_lambda(res, b, v)): why.append('base not in Lambda')
    for g in A + B:
        if not _lexpos(g): why.append('not lex-positive %s' % (g,))
        if not _is_graver(res, b, g): why.append('not Graver %s' % (g,))
    if A and _rank(A) != len(A): why.append('A dependent')
    if B and _rank(B) != len(B): why.append('B dependent')
    CA, CB = _corners(u, A), _corners(v, B)
    for p in CA + CB:
        if not all(0 <= x <= qq for x, qq in zip(p, q)) or not any(p): why.append('corner out of box/origin %s' % (p,))
        if not _in_lambda(res, b, p): why.append('corner not in Lambda %s' % (p,))
    if sorted(CA) == sorted(CB): why.append('same cell')
    if not (all(0 < x < 1 for x in t) and all(0 < x < 1 for x in l)) or len(t) != len(A) or len(l) != len(B): why.append('coefficients not in (0,1)')
    lhs = [Fr(u[i]) + sum(t[j] * A[j][i] for j in range(len(A))) for i in range(k)]
    rhs = [Fr(v[i]) + sum(l[j] * B[j][i] for j in range(len(B))) for i in range(k)]
    if lhs != rhs: why.append('no common relative-interior point')
    gens = A + B
    delta = tuple(vi - ui for ui, vi in zip(u, v))
    span = _rank(gens + [delta]) if gens else 0
    support = len({i for w in gens + [delta] for i in range(k) if w[i]})
    return (not why), {'why': why, 'd_span': span, 'd_support': support, 'd_intersection': len(A) + len(B) - span}

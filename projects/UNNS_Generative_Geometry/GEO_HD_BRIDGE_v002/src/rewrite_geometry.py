"""G2-B: geometric effect of an arithmetic rewrite u <-> v (blocks with equal multiplier).
Laws (theory/RECOMBINATION_GEOMETRY.md):
 B2-T3  loss budget Lambda_p of any history = G_p(content) - dq_p(endpoints); so it depends on the CONTENT only.
 B2-T3' for a rewrite u<->v:  Lambda_p(u) - Lambda_p(v) = G_p(u) - G_p(v) = (H_p(u) - H_p(v))/2,  H_p = sum v_p(N).
 B2-T4  parity conservation of loss steps when all labels have v_p(N) <= 1.
 B2-T5  dimension forcing for 2^(2n) 3^(4n)."""
import _paths  # noqa
from collections import Counter
from geometric_history import (step, states, gain_loss, arrangements, predicted_loss_steps, avoids_square, feasible, both_active)
from geo_snapshots import vp
from geo1lib import factor


def content_G(content):
    """G_p = sum over labels of v_p(N+1) -- the arrangement-independent gain content"""
    g = Counter()
    for N in content:
        for p in factor(N + 1):
            g[p] += vp(N + 1, p)
    return dict(g)


def content_H(content):
    h = Counter()
    for N in content:
        for p in factor(N):
            h[p] += vp(N, p)
    return dict(h)


def multiplier(content):
    from fractions import Fraction as Fr
    r = Fr(1)
    for N in content:
        r *= Fr((N + 1) ** 2, N)
    return r


def loss_vector_diff(u, v):
    """predicted Lambda_p(u) - Lambda_p(v) for every prime (requires multiplier(u) == multiplier(v))"""
    assert multiplier(u) == multiplier(v)
    Gu, Gv = content_G(u), content_G(v)
    return {p: Gu.get(p, 0) - Gv.get(p, 0) for p in set(Gu) | set(Gv) if Gu.get(p, 0) != Gv.get(p, 0)}


def check_rewrite_law(m, u, v):
    """for a source m at which both contents are executable: Lambda(u-arrangements) is a single vector, Lambda(v-arrangements) too, and
    their difference equals the predicted one.  Returns a dict (ok flag, vectors, counts)."""
    A, B = arrangements(m, u), arrangements(m, v)
    if not A or not B:
        return None
    la = {tuple(sorted(gain_loss(m, w)['Lambda'].items())) for w, _ in A}
    lb = {tuple(sorted(gain_loss(m, w)['Lambda'].items())) for w, _ in B}
    if len(la) != 1 or len(lb) != 1:
        return {'ok': False, 'reason': 'loss budget not constant on arrangements'}
    la, lb = dict(next(iter(la))), dict(next(iter(lb)))
    diff = {p: la.get(p, 0) - lb.get(p, 0) for p in set(la) | set(lb) if la.get(p, 0) != lb.get(p, 0)}
    return {'ok': diff == loss_vector_diff(u, v), 'Lambda_u': la, 'Lambda_v': lb, 'diff': diff, 'n_u': len(A), 'n_v': len(B)}


def forced_square(n, e2, e3):
    """True iff every arrangement of 2^(2n) 3^(4n) from valuations (e2,e3) has a state with v2>=2 and v3>=2 (so 6 in D(m));
    None if no arrangement is admissible."""
    if not feasible(e2, e3, 2 * n, 4 * n):
        return None
    return not avoids_square(e2, e3, 2 * n, 4 * n)

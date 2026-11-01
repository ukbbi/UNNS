"""G2-G: the v001 multidimensional route-topology examples (3 and 4 active primes) viewed through the geometry of their histories.
Four DIFFERENT quantities are kept apart:  (V) valuation coordinates involved, (A) active constraint primes (primes dividing a label),
(R) dimension of the combinatorial history complex (labels - 1), (G) dimension of the realized occurrence geometry along the history
(ambient dimension k(m) = #{p: v_p(m) >= 2}; for integers d_aff = k)."""
import _paths  # noqa
from itertools import permutations
from collections import Counter
from math import prod
from geo1lib import factor
from geo_snapshots import qvec
from geometric_history import states, gain_loss, ambient_profile

EXAMPLES = {
    'disconnected_3_primes': (4, (2, 3, 4, 5, 6)),
    'disconnected_4_primes': (4, (2, 3, 4, 5, 6, 7)),
    'loop_3_primes': (32, (2, 3, 4, 5, 8)),
    'loop_4_primes': (24, (2, 3, 4, 5, 6, 7)),
}


def admissible_words(m, alpha):
    return [w for w in permutations(alpha) if states(m, w) is not None]


def swap_classes(m, alpha):
    words = admissible_words(m, alpha); ws = set(words); par = {w: w for w in words}
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for w in words:
        for i in range(len(w) - 1):
            v = w[:i] + (w[i + 1], w[i]) + w[i + 2:]
            if v in ws:
                par[find(w)] = find(v)
    cl = {}
    for w in words:
        cl.setdefault(find(w), []).append(w)
    return sorted(cl.values(), key=lambda c: (len(c), c))


def active_constraint_primes(alpha):
    return sorted({p for N in alpha for p in factor(N)})


def invariants(m, w):
    path = states(m, w)
    prof = ambient_profile(path)
    sup = sorted({p for s in path for p in qvec(s)})
    sizes = [prod(x + 1 for x in qvec(s).values()) - 1 for s in path]
    gl = gain_loss(m, w)
    nloss = sum(1 for i in range(len(w)) if any(i in v for v in gl['loss_steps'].values()))
    return {'peak_k': max(prof), 'support': sup, 'peak_D': max(sizes), 'loss_steps': nloss,
            'Lambda': tuple(sorted(gl['Lambda'].items())), 'prof': prof}


def example_table(name):
    m, alpha = EXAMPLES[name]
    cl = swap_classes(m, alpha)
    allp = set()
    for w in admissible_words(m, alpha):
        for s in states(m, w):
            allp |= set(factor(s))
    rows = []
    for c in cl:
        inv = [invariants(m, w) for w in c]
        rows.append({'n_words': len(c), 'first_labels': sorted({w[0] for w in c}),
                     'peak_k': sorted({i['peak_k'] for i in inv}), 'peak_D': sorted({i['peak_D'] for i in inv}),
                     'support': sorted({tuple(i['support']) for i in inv}), 'loss_steps': sorted({i['loss_steps'] for i in inv}),
                     'Lambda': sorted({i['Lambda'] for i in inv}), 'activation_orders': len({tuple(i['prof']) for i in inv})})
    return {'name': name, 'source': m, 'labels': list(alpha), 'components': len(cl),
            'V_valuation_coordinates': len(allp), 'A_active_constraint_primes': len(active_constraint_primes(alpha)),
            'R_history_complex_dim': len(alpha) - 1,
            'G_realized_geometry_dim_peak': max(max(ambient_profile(states(m, w))) for w in admissible_words(m, alpha)),
            'classes': rows,
            'Lambda_constant_on_whole_complex': len({tuple(sorted(gain_loss(m, w)['Lambda'].items())) for w in admissible_words(m, alpha)}) == 1}

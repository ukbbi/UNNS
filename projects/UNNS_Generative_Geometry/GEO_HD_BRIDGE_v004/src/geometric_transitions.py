"""R3-G: rational geometric records along a collective trajectory (frozen GEO-I engine) + F-only reconstruction."""
import _paths
from fractions import Fraction as Fr
from geo2lib import analyse
from rational_geometry import record, split_graver

def geo_row(x):
    x = Fr(x); r = record(x); s = split_graver(r); a = analyse(x)
    return {'x': str(x), 'q': r['q'], 'nF': len(r['F']), 'graver': len(r['G']), 'dormant': len(s['dormant']),
            'cells_move': a['move']['cells_per_dim'], 'components': a['move']['components'], 'betti': a['move']['betti']['2'],
            'betti_p': a['move']['betti']['2147483647'], 'cells_axis': a['axis']['cells_per_dim'], 'D': sorted(r['D']),
            'chi': sum((-1) ** i * c for i, c in enumerate(a['move']['cells_per_dim']))}

def tower_period_starts(S0fun, l, K):
    return [geo_row(Fr(S0fun(k) ** 2, l)) for k in range(K)]

def within_period(S, l, P):
    return [geo_row(Fr(t * S * S, l)) for t in range(1, P + 2)]

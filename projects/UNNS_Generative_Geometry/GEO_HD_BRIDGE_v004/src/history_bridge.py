"""A4-T7: relation between the move complex K_move of a state and the SELECT-II history-recombination complex.
SELECT-II (frozen integer rule) only produces INTEGER states.  For an integer m the modulus is b=1, Lambda_1=Z^k, F=B\\{0}, and
K_move(m) = union of cubes of the box grid not containing the origin = contractible (PROVED, nerve lemma).  Hence K_move(endpoint)
carries no information on the history complex of that endpoint."""
import _paths
from fractions import Fraction as Fr
from geometric_transitions import geo_row
from history_invariants import extension_chain, analyse_content

def integer_kmove_rows(ms):
    out = []
    for m in ms:
        r = geo_row(Fr(m)); out.append({'m': m, 'q': r['q'], 'nF': r['nF'], 'betti': r['betti'], 'cells': r['cells_move'], 'axis_equal': r['cells_move'][:1] == r['cells_axis'][:1]})
    return out

def bridge_rows(steps=3):
    rows = []
    for A, E in extension_chain(steps=steps):
        if E is None: continue
        h = analyse_content(A); r = geo_row(Fr(E))
        rows.append({'A': list(A), 'E': E, 'history_components': h['components'], 'history_sizes': h['sizes'], 'n_words': h['n_words'],
                     'bit_constant_on_components': h['bit_constant_on_components'], 'both_orders_present': h['both_orders_present'],
                     'K_move_betti': r['betti'], 'K_move_q': r['q'], 'K_move_nF': r['nF']})
    return rows

"""HD-1D v001: occurrence events along histories.  D(m) = {d>=2 : d | s(m)}, s(m) = prod p^floor(v_p(m)/2).

Facts used (proved in theory/THEOREMS.md, D-T4):  D(m) <-> e(m) = floor(v(m)/2) is a bijection onto exponent vectors; a history's
fibre sequence determines the history; distinct labels from one state always give distinct fibres."""
from select_history import run, fibre, half_valuation, s_of


def fibre_sequence(h):
    return tuple(fibre(m) for m in run(*h))


def rho(h, d):
    return tuple(int(d in set(D)) for D in fibre_sequence(h))


def birth_loss(h):
    seq = fibre_sequence(h); out = []
    for j in range(1, len(seq)):
        a, b = set(seq[j - 1]), set(seq[j])
        out.append(dict(step=j, label=h[1][j - 1], state=run(*h)[j], births=sorted(b - a), losses=sorted(a - b)))
    return out


def signature_table(h):
    """rho_d for every d that ever occurs"""
    seq = fibre_sequence(h)
    ds = sorted({d for D in seq for d in D})
    return {d: tuple(int(d in set(D)) for D in seq) for d in ds}


def swap_signature_difference(h, i):
    """positions at which the fibre sequences of h and its swap at i differ (theory: exactly {i+1})"""
    from route_complex import do_swap
    a, b = fibre_sequence(h), fibre_sequence(do_swap(h, i))
    return [j for j in range(len(a)) if a[j] != b[j]]

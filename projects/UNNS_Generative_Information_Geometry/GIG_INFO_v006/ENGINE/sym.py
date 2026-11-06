"""GIG-INFO v004 -- symbolic (non-integer) history grammar.
Alphabet Sigma = {S,R,N} (Sunny, Rainy, Snowy).  A system is a list of six distinguishable events with categories cats (e.g. S,S,S,R,R,N) and a rule set G subset Sigma x Sigma (9 bits).
A history = ordering of the six events; admissible iff every consecutive pair of categories is in G.  Histories are vertices of the permutohedron P_6 (p = tuple of event indices);
legal swaps = adjacent-position swaps between admissible histories; K = full subcomplex of P_6 on the admissible histories (v001 definition).  No integer divisibility is used anywhere."""
import itertools
import _vpath  # noqa: F401
import history_complex as hc

SIGMA = "SRN"
PAIRS = [(a, b) for a in SIGMA for b in SIGMA]  # bit i of a rule code <-> PAIRS[i]
PERMS = hc.perms(6)


def rules(code):
    return {PAIRS[i] for i in range(9) if code >> i & 1}


def admissible_mask(cats, code):
    G = rules(code)
    m = 0
    for i, p in enumerate(PERMS):
        if all((cats[p[j]], cats[p[j + 1]]) in G for j in range(5)):
            m |= 1 << i
    return m


def all_systems(cats):
    """dict mask -> list of rule codes producing it (non-empty systems only)."""
    out = {}
    for code in range(512):
        m = admissible_mask(cats, code)
        if m:
            out.setdefault(m, []).append(code)
    return out


def multisets():
    return [tuple(c) for c in itertools.combinations_with_replacement(SIGMA, 6)]

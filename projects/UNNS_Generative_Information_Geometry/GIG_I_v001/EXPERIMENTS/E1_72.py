"""E1 -- complete histories of 72: classification and exact information decomposition (GIG-T4)."""
import json, os
from decimal import Decimal
from fractions import Fraction
import _path
from history_fibres import complete_histories, classify, content, count_fixed_source, endpoint
from swap_graph import swap_graph, components
import information as inf


def run():
    H = sorted(complete_histories(72))
    adj = swap_graph(H)
    comps = components(adj)
    sizes = sorted(len(c) for c in comps)
    pieces = classify(H)
    # class sizes per piece (swap graph never leaves a piece)
    piece_classes = {}
    for key, hs in pieces.items():
        sub = swap_graph(hs)
        piece_classes[key] = sorted(len(c) for c in components(sub))
    chain = inf.uniform_chain(piece_classes)
    # four-level chain M, Q|M, C|M,Q, W|M,Q,C  (uniform model)
    N = len(H)
    by_source = {}
    for (m0, q), hs in pieces.items():
        by_source.setdefault(m0, {})[q] = piece_classes[(m0, q)]
    HM = inf.shannon([Fraction(sum(sum(s) for s in qs.values()), N) for qs in by_source.values()])
    HQ = sum(Decimal_w(sum(sum(s) for s in qs.values()), N) * inf.shannon([Fraction(sum(s), sum(sum(x) for x in qs.values())) for s in qs.values()]) for qs in by_source.values())
    out = {
        "source_convention": "complete-history fibre F_72 (all squarefree sources)",
        "probability_model": "uniform on F_72",
        "precision_digits": inf.PREC,
        "histories": [[h[0], list(h[1])] for h in H],
        "N": N,
        "A_bits": inf.fmt(inf.hartley(N), 12),
        "swap_class_sizes": sizes,
        "pieces": {"%d|%s" % (k[0], list(k[1])): v for k, v in piece_classes.items()},
        "H(M|T)": inf.fmt(HM, 12),
        "H(Q|M,T)": inf.fmt(HQ, 12),
        "H(P|T)": inf.fmt(chain["H(P|T)"], 12),
        "H(C|P,T)": inf.fmt(chain["H(C|P,T)"], 12),
        "H(C|T)": inf.fmt(inf.class_entropy(sizes), 12),
        "H(W|C,T)": inf.fmt(chain["H(W|C,T)"], 12),
        "H(W|T)": inf.fmt(chain["H(W|T)"], 12),
        "fixed_source_counts": {str(m0): count_fixed_source(m0, 72) for m0 in sorted({h[0] for h in H})},
        "nonuniform_example": nonuniform_example(H),
    }
    return out


def Decimal_w(a, b):
    return Decimal(a) / Decimal(b)


def nonuniform_example(H):
    """a nonuniform ensemble on F_72 with entropy strictly below A(72)=2 bits (GIG-T3)."""
    probs = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 8)]
    return {"probs": [str(p) for p in probs], "H": inf.fmt(inf.shannon(probs), 12), "A": inf.fmt(inf.hartley(len(H)), 12)}


if __name__ == "__main__":
    r = run()
    print(json.dumps(r, indent=1))

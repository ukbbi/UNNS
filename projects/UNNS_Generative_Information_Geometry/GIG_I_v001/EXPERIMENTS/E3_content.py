"""E3 -- different generating contents with a common source and endpoint: source 4, endpoint 65536 = 4^8."""
import json
from fractions import Fraction
from decimal import Decimal
import _path
from history_fibres import fixed_source_histories, classify, R, is_admissible, endpoint, content, count_fixed_source
from swap_graph import swap_graph, components
import information as inf


def run():
    m0, t = 4, 65536
    H = sorted(fixed_source_histories(m0, t))
    assert all(is_admissible(*h) and endpoint(*h) == t for h in H)
    N = len(H)
    pieces = classify(H)
    pc = {}
    for key, hs in pieces.items():
        pc[key] = sorted(len(c) for c in components(swap_graph(hs)))
    # uniform model on the fixed-source fibre F_t(m0): source is deterministic, so H(M|T)=0
    ch = inf.uniform_chain(pc)
    contents = {"|".join(map(str, key[1])): {"n_histories": sum(v), "class_sizes": v} for key, v in sorted(pc.items(), key=lambda kv: kv[0][1])}
    # the stated multiplier identity
    ident = R(1) ** 7 == R(2) ** 2 * R(3) ** 4
    # admissibility of the two contents of the identity from source 4 and from source 1
    from itertools import permutations
    def adm(src, cont):
        return sum(1 for w in set(permutations(cont)) if is_admissible(src, w))
    c1, c2 = (1,) * 7, (2, 2, 3, 3, 3, 3)
    return {
        "source_convention": "fixed-source fibre F_65536(4)", "probability_model": "uniform on F_65536(4)", "precision_digits": inf.PREC,
        "multiplier_identity_R1^7=R2^2*R3^4": ident,
        "N": N, "A_bits": inf.fmt(inf.hartley(N), 12),
        "pieces_by_content": contents,
        "content_entropy_H(Q|T)": inf.fmt(ch["H(P|T)"], 12),
        "class_entropy_given_content_H(C|Q,T)": inf.fmt(ch["H(C|P,T)"], 12),
        "ordering_entropy_H(W|C,T)": inf.fmt(ch["H(W|C,T)"], 12),
        "total": inf.fmt(ch["H(W|T)"], 12),
        "admissible_orderings_from_4": {"1^7": adm(4, c1), "2^2 3^4": adm(4, c2)},
        "admissible_orderings_from_1": {"1^7": adm(1, c1), "2^2 3^4": adm(1, c2)},
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=1))

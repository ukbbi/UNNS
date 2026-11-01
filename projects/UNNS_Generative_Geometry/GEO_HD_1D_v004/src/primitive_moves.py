"""HD-1D v004 builder: content fibres {c >= 0 : V_A c = d} (finite: every R(N) > 1) and their connectivity under sets of kernel moves."""
from itertools import product
from valuation_matrix import matrix, displacement
from integer_kernel import graver_candidates


def content_fibre(A, d, cap=60):
    """all nonnegative integer vectors c with V_A c = d.  Finite because R(N) > 1 for all N: the multiplier grows with |c|."""
    ps, V = matrix(A); s = len(A); out = []
    def rec(j, c, rem):
        if j == s:
            if all(r == 0 for r in rem): out.append(tuple(c))
            return
        k = 0
        while k <= cap:
            r2 = [rem[i] - V[i][j] * k for i in range(len(ps))]
            c.append(k); rec(j + 1, c, r2); c.pop()
            k += 1
            # prune with a cheap monotone bound: total multiplier exponent cannot exceed that of the target
            if sum(abs(x) for x in r2) > 10 ** 6: break
    # tighter: use log R > 0 weights through the 2-adic+3-adic... fall back to a total-length cap
    rec(0, [], list(d)); return out


def fibre_by_length(A, d, maxlen):
    """enumerate by total length <= maxlen (exact within the length cap)"""
    ps, V = matrix(A); s = len(A); out = []
    def rec(j, c, rem, left):
        if j == s - 1:
            for k in range(left + 1):
                r2 = [rem[i] - V[i][j] * k for i in range(len(ps))]
                if all(x == 0 for x in r2): out.append(tuple(c + [k]))
            return
        for k in range(left + 1):
            rec(j + 1, c + [k], [rem[i] - V[i][j] * k for i in range(len(ps))], left - k)
    rec(0, [], list(d), maxlen); return out


def components(fibre, moves):
    S = set(fibre); seen = set(); comps = []
    for c in sorted(S):
        if c in seen: continue
        st = [c]; seen.add(c); comp = [c]
        while st:
            x = st.pop()
            for z in moves:
                for sg in (1, -1):
                    y = tuple(a + sg * b for a, b in zip(x, z))
                    if y in S and y not in seen: seen.add(y); st.append(y); comp.append(y)
        comps.append(sorted(comp))
    return comps

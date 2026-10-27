"""GEO-I v008 Programme C: test of the B-COMMON mechanism on all minimal boxes of the complete censuses (n<=NMAX).
B-COMMON (proved, MINIMAL_RANK.md): if S != T are partitions of [n] into circuits and x in C lies outside span(S) and span(T), then cells (S,x),(T,x) collide and their witness has rank <= r+t-1
(g_1+..+g_r = 1-2x = h_1+..+h_t).  Here r=t=2 gives rank 3.  The script records, for every minimal box, whether such a triple (S,T,x) exists (it is NOT claimed for all minimal boxes).
usage: common_base.py NMAX OUT.json"""
import os, sys, json, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'theory')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import binary_01 as B
from rank_attack import basis_sets


def two_partitions(C, n):
    full = (1 << n) - 1; circ = B.circuits_of([c for c in C if c]); cs = set(circ); out = []
    for a in circ:
        b = full ^ a
        if a < b and b in cs: out.append((a, b))
    return out


def has_common_base(cols):
    n = len(cols); C = [0] + B.codewords(cols); Cs = set(C); parts = two_partitions(C, n)
    spans = [{0, a, b, a ^ b} for a, b in parts]
    for i, j in itertools.combinations(range(len(parts)), 2):
        if any(x not in spans[i] and x not in spans[j] for x in C): return True
    return False


if __name__ == '__main__':
    nmax = int(sys.argv[1]); res = {}
    for n in range(int(sys.argv[3]) if len(sys.argv) > 3 else 4, nmax + 1):
        tot = yes = 0
        for m in range(1, n - 2):
            for cols in basis_sets(n, m):
                if B.is_embedded(cols) or not B.minimal_nonembedded(cols): continue
                tot += 1; yes += has_common_base(cols)
        res[n] = {'minimal_representatives': tot, 'with_common_base_2circuit_partitions': yes}; print(n, res[n], flush=True)
    json.dump(res, open(sys.argv[2], 'w'), indent=1)

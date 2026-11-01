"""R3-B/T2: complete classification of the two-prime, box (1,1) rational states, and the general split Graver = realized(D) + dormant.
For x = (p r)^2 / b, p<r primes, gcd(pr, b)=1:  A: p=1, B: r=1, C: pr=1, E: p=r  (all mod b).  Lambda cap {-1,0,1}^2 contains
(1,0) iff A, (0,1) iff B, (1,1) iff C, (1,-1) iff E.  D = {p if A} + {r if B} + {pr if C}."""
import _paths
from fractions import Fraction as Fr
from math import gcd
from rational_geometry import record, split_graver
from graver_relations import isprime

ALLOWED = {frozenset(), frozenset('A'), frozenset('B'), frozenset('C'), frozenset('E'), frozenset('CE'), frozenset('ABCE')}

def type_of(p, r, b):
    t = set()
    if p % b == 1 % b: t.add('A')
    if r % b == 1 % b: t.add('B')
    if p * r % b == 1 % b: t.add('C')
    if (p - r) % b == 0: t.add('E')
    return frozenset(t)

def D_of_type(p, r, t):
    return frozenset(({p} if 'A' in t else set()) | ({r} if 'B' in t else set()) | ({p * r} if 'C' in t else set()))

def graver_of_type(t):
    G = set()
    if 'A' in t: G |= {(1, 0), (-1, 0)}
    if 'B' in t: G |= {(0, 1), (0, -1)}
    if 'C' in t: G |= {(1, 1), (-1, -1)}
    if 'E' in t: G |= {(1, -1), (-1, 1)}
    # conformal minimality inside the box (1,1): (1,1) is dominated by (1,0) or (0,1); (1,-1) likewise
    if 'A' in t:
        G -= {(1, 1), (-1, -1), (1, -1), (-1, 1)}
    if 'B' in t:
        G -= {(1, 1), (-1, -1), (1, -1), (-1, 1)}
    return G

def scan(pmax=40, bmax=300):
    ps = [p for p in range(2, pmax) if isprime(p)]
    stats = {'states': 0, 'type_violations': 0, 'graver_violations': 0, 'D_violations': 0, 'by_D_E': {}}
    for i, p in enumerate(ps):
        for r in ps[i + 1:]:
            for b in range(2, bmax):
                if gcd(p * r, b) != 1: continue
                rec = record(Fr(p * p * r * r, b))
                if rec['q'] != [1, 1]: continue
                t = type_of(p, r, b)
                stats['states'] += 1
                if t not in ALLOWED: stats['type_violations'] += 1
                if set(rec['G']) != graver_of_type(t): stats['graver_violations'] += 1
                if rec['D'] != D_of_type(p, r, t): stats['D_violations'] += 1
                Dk = str(sorted(rec['D']) if len(rec['D']) < 2 else 'multi') if not rec['D'] else ('pr' if rec['D'] == {p * r} else 'other')
                key = (Dk, 'E' in t)
                stats['by_D_E'][str(key)] = stats['by_D_E'].get(str(key), 0) + 1
    return stats

"""A5-T1 extended family scan: for activation-family instances (k, l, ps, q) apply the proper-divisor obstruction (O(1) closed forms) and the exact resolver.
usage: python scan_family.py out.json k l pmax Pmax qmax"""
import _paths, sys, json, time, itertools
from fractions import Fraction as Fr
from graver_relations import isprime, primitive_root_of_order
from stage_sieve import proper_divisor_block
from reachability import resolve_family

def run(k, l, pmax, Pmax, qmax, budget=1500):
    c = primitive_root_of_order(l, k); cinv = pow(c, -1, l); t0 = time.time()
    pr = [p for p in range(3, pmax) if isprime(p) and p % l == c]
    qs = [q for q in range(2, qmax) if isprime(q) and q % l == cinv]
    rows = []; skipped = 0
    for ps in itertools.combinations(pr, k):
        P = 1
        for p in ps: P *= p
        if P > Pmax: continue
        for q in qs:
            if q in ps: continue
            b, uf, ua = proper_divisor_block(list(ps), l, q)
            if b: rows.append({'k': k, 'l': l, 'ps': list(ps), 'q': q, 'class': 'BLOCKED_BY_PROPER_DIVISOR'}); continue
            if time.time() - t0 > budget: skipped += 1; continue
            r = resolve_family(k, l, list(ps), q); rows.append({'k': k, 'l': l, 'ps': list(ps), 'q': q, **r})
    return rows, skipped

if __name__ == '__main__':
    out = sys.argv[1]; k, l, pmax, Pmax, qmax = map(int, sys.argv[2:7])
    rows, sk = run(k, l, pmax, Pmax, qmax)
    json.dump({'rows': rows, 'skipped_budget': sk}, open(out, 'w'))
    import collections
    print(collections.Counter(r['class'] for r in rows), 'skipped', sk)
    print(sorted({r['q'] for r in rows if r['class'] == 'REACHED'}))

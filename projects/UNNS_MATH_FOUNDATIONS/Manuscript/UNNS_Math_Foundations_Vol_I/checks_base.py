#!/usr/bin/env python3
"""Volume I auxiliary exact-integer checks; never alters archived research files.

Scope: finite consistency checks of selected mathematical statements in the
working manuscript; not an independent verification of every theorem/proof.
"""
from __future__ import annotations
from collections import deque
from functools import lru_cache
from itertools import combinations
from math import gcd, isqrt, lcm
from fractions import Fraction
import json
from pathlib import Path


def divisors(n: int) -> list[int]:
    low, high = [], []
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            low.append(i)
            if i * i != n:
                high.append(n // i)
    return low + high[::-1]


def indices(a: int, b: int = 1) -> list[int]:
    assert a > 0 and b > 0 and gcd(a, b) == 1
    return [d for d in range(2, isqrt(a)+1) if a % (d*d) == 0 and (d - 1) % b == 0]


def occurrences_bruteforce(a: int, b: int) -> list[tuple[int,int]]:
    val = Fraction(a, b)
    return [(m, n) for n in range(1, a + 1) for m in range(1, a + 1)
            if Fraction(m * (n+1)**2, n) == val]


def successors(m: int, cap: int | None = None) -> list[int]:
    ss = sorted({(m//n)*(n+1)**2 for n in divisors(m)})
    return ss if cap is None else [t for t in ss if t <= cap]


def pred(t: int) -> list[int]:
    return sorted({(t//(d*d))*(d-1) for d in indices(t)})


@lru_cache(None)
def anc(t: int) -> frozenset[int]:
    out = {t}
    for p in pred(t):
        out.update(anc(p))
    return frozenset(out)


@lru_cache(None)
def histories(t: int) -> int:
    pp = pred(t)
    return sum(histories(p) for p in pp) if pp else 1


def reachable_upto(m: int, cap: int) -> frozenset[int]:
    seen = {m}
    q = deque([m])
    while q:
        v = q.popleft()
        for w in successors(v, cap):
            if w not in seen:
                seen.add(w)
                q.append(w)
    return frozenset(seen)


def check(label, test, record):
    record.append({'id':label, 'pass':bool(test)})
    if not test:
        raise AssertionError(label)


def main() -> None:
    out = []
    tested = 0
    for a in range(1, 80):
        for b in range(1, 13):
            if gcd(a, b) != 1:
                continue
            actual = occurrences_bruteforce(a, b)
            from_formula = [((a//(d*d))*((d-1)//b), d-1) for d in indices(a,b)]
            if set(actual) != set(from_formula):
                raise AssertionError(f'fibre mismatch at {a}/{b}')
            tested += 1
    check('T1_rational_fibres', tested > 450, out)
    check('R72_equals_3', len(indices(72)) == 3, out)
    check('R72_indices', indices(72) == [2,3,6], out)
    check('D_400_over_3', indices(400,3) == [4,10], out)
    check('D_20736_over_5', indices(20736,5) == [6,16,36], out)
    check('distinct_successor_count', all(len(successors(n)) == len(divisors(n)) for n in range(1,801)), out)
    check('edge_growth', all(t>=4*m for m in range(1,301) for t in successors(m)), out)
    check('indegree_R', all(len(pred(t)) == len(indices(t)) for t in range(1,1501)), out)
    check('edge_gcd_label', all((lambda k, n:(gcd(m,t)==k and m//gcd(m,t)==n))(m//n,n)
                                  for m in range(1,301) for n in divisors(m)
                                  for t in [(m//n)*(n+1)**2]), out)
    # Bounded traversal is logically exhaustive because every edge strictly increases.
    common = sorted(reachable_upto(1,100) & reachable_upto(2,100))
    check('common_1_2_at_most_100', common == [81,100], out)
    check('81_not_reaches_100', 100 not in reachable_upto(81,100), out)
    common_anc = anc(32) & anc(300)
    maximal = sorted(x for x in common_anc if not any(x!=y and y in reachable_upto(x,300)
                                                       for y in common_anc))
    check('32_300_maximal_common_ancestors', maximal==[2,6],out)
    check('H72_equals_4', histories(72) == 4, out)
    check('squarefree_sources', all((len(pred(t))==0)==(len(indices(t))==0)
                                    for t in range(1,3001)), out)
    # Each direct edge is a cover in tested region. For p->t, an alternative
    # length >=2 path would have an intermediate strictly between p and t.
    no_shortcut = True
    for m in range(1,151):
        for t in successors(m,1500):
            for q in successors(m,t-1):
                if t in reachable_upto(q,t):
                    no_shortcut = False
                    break
    check('no_shortcuts_finite_sample', no_shortcut, out)
    report = {
        'scope':'auxiliary finite verification, not an independent theorem proof',
        'rational_fibre_samples':tested,
        'checks':out,
        'pass_count':sum(x['pass'] for x in out),
        'fail_count':sum(not x['pass'] for x in out),
        'computed_witnesses': {'common_futures_1_2_at_most_100':common,
                               'maximal_common_ancestors_32_300':maximal,
                               'history_count_72':histories(72)}
    }
    output=Path(__file__).with_name('volume_i_verification.json')
    output.write_text(json.dumps(report,indent=2),encoding='utf8')
    print(f"Volume I finite checks: {report['pass_count']} PASS; {report['fail_count']} FAIL; rational samples: {tested}")
    print('Witnesses:',report['computed_witnesses'])

if __name__ == '__main__':
    main()

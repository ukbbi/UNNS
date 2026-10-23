#!/usr/bin/env python3
"""SELECT-II v001: exact positive-integer self-nest iteration graph.

Declared interpretation: replace the first nest argument M by its prior integer
output m; choose any N >= 1. Retain only integer successors (equiv. N | m).
An edge m -> t has label N and value t = (m//N)*(N+1)^2.
This interpretation is NOT asserted to exhaust UNNS recursive grammar.
Standard library only; deterministic tests and finite data.
"""
from __future__ import annotations
import collections
import itertools
import json
import math
import sys
from functools import lru_cache
from fractions import Fraction
from pathlib import Path

RESULTS = {}
GOOD = True

def check(label, ok, detail=None):
    global GOOD
    ok = bool(ok)
    GOOD &= ok
    RESULTS[label] = {"pass": ok, "detail": detail}
    print(("PASS " if ok else "FAIL ") + label + (f" [{detail}]" if detail is not None else ""))

def data(label, detail):
    RESULTS[label] = {"data": detail}
    print("DATA " + label + " " + json.dumps(detail, sort_keys=True))

def divisors(m: int):
    """All positive divisors, increasing."""
    a, b = [], []
    for d in range(1, math.isqrt(m)+1):
        if m % d == 0:
            a.append(d)
            if d*d < m: b.append(m//d)
    return a + b[::-1]

def nest_value(m: int, n: int):
    return Fraction(m*(n+1)**2, n)

def successors(m: int):
    """Ordered triples (target, label N) for each N | m."""
    return tuple(((m//n)*(n+1)**2, n) for n in divisors(m))

@lru_cache(None)
def predecessors(t: int):
    """Ordered triples (source, label N) for each squared divisor (N+1)^2 | t."""
    return tuple((t//(d*d)*(d-1), d-1) for d in range(2,math.isqrt(t)+1) if t%(d*d)==0)

def is_squarefree(t: int):
    return not predecessors(t)

def R(t: int):
    """Prime-factor formula for count of distinct integer nest occurrences."""
    m, p, result = t, 2, 1
    while p*p <= m:
        e = 0
        while m % p == 0:
            m//=p; e+=1
        if e: result *= (e//2+1)
        p += 1
    return result-1  # remaining prime has exponent 1 => multiplier 1

@lru_cache(None)
def root_ancestors(t: int):
    pr=predecessors(t)
    if not pr: return (t,)
    return tuple(sorted({root for m,n in pr for root in root_ancestors(m)}))

def is_edge(m: int, t: int):
    """Exact arithmetic membership; returns N or None."""
    if m <= 0 or t <= 0: return None
    g=math.gcd(m,t)
    n=m//g
    if t == g*(n+1)**2: return n
    return None

def bounded_paths(start: int, ceiling: int):
    """Exact reachable values and shortest-by-steps witness path up to ceiling.
    All edges increase, so exploring only states <= ceiling is exhaustive for that horizon.
    """
    seen={start: ((start, None),)} if start<=ceiling else {}
    q=collections.deque([start] if start<=ceiling else [])
    while q:
        m=q.popleft()
        for t,n in successors(m):
            if t > ceiling: break
            if t not in seen:
                seen[t]=seen[m]+((t,n),)
                q.append(t)
    return seen

def show_path(path):
    return " -> ".join(str(x) if n is None else f"{x} (N={n})" for x,n in path)

# --- A: the explicitly declared one-step rule ---
ok_int = all((nest_value(m,n).denominator==1) == (m % n == 0)
             for m in range(1,301) for n in range(1,101))
check("A1.integrality_iff_N_divides_m", ok_int, "m<=300, N<=100; proved by gcd(N,(N+1)^2)=1")
check("A2.immediate_successor_formula", all(nest_value(m,n)==t for m in range(1,501) for t,n in successors(m)))
check("A3.successors_distinct_strictly_ordered_by_N", all(all(a[0]<b[0] for a,b in itertools.pairwise(successors(m))) for m in range(1,2001)))
check("A4.all_edges_grow_by_factor_at_least_four", all(t>=4*m and (t==4*m)==(n==1) for m in range(1,2001) for t,n in successors(m)))
check("A5.source_value_divides_successor_iff_N_equals_one", all((t%m==0)==(n==1) for m in range(1,2001) for t,n in successors(m)))

# --- B: target multiplicity, rooted acyclic structure ---
check("B1.indegree_equals_nest_multiplicity_R", all(len(predecessors(t))==R(t) for t in range(1,20001)), "t<=20000; proof by d=N+1")
check("B2.outdegree_equals_number_of_divisors", all(len(successors(m))==len(divisors(m)) for m in range(1,5001)), "m<=5000; injective N->t")
check("B3.squarefree_iff_no_predecessor", all(is_squarefree(t)==(R(t)==0) for t in range(1,20001)))
check("B4.predecessors_strictly_smaller_and_labels_exact", all(0<m<t and is_edge(m,t)==n for t in range(1,10001) for m,n in predecessors(t)))
check("B5.gcd_identifies_unique_edge_label", all(is_edge(m,t)==n for m in range(1,400) for t,n in successors(m)), "N=m/gcd(m,t)")
check("B6.converse_edge_membership", all((is_edge(m,t) is not None)==(t in dict(successors(m))) for m in range(1,130) for t in range(1,1001)), "checked independently of target factorization")
check("B7.all_nodes_descend_from_squarefree_sources", all(all(is_squarefree(r) and r<=t for r in root_ancestors(t)) for t in range(1,6001)))
check("B8.predecessors_and_distinct_roots_of_72", predecessors(72)==((18,1),(16,2),(10,5)) and root_ancestors(72)==(1,3,10), f"pred={predecessors(72)}; roots={root_ancestors(72)}")
check("B9.one_target_can_have_multiple_squarefree_roots", root_ancestors(16)==(1,3))

# --- C: common futures and failure of least common future ---
R1=bounded_paths(1,100)
R2=bounded_paths(2,100)
common=set(R1).intersection(R2)
check("C1.common_futures_1_and_2_through_100_exact", common=={81,100}, f"{sorted(common)}")
check("C2.two_distinct_common_futures_exhibited", all(t in R1 and t in R2 for t in (81,100)))
check("C3.paths_exact_under_nest_rule", all(all(is_edge(path[i-1][0],path[i][0])==path[i][1] for i in range(1,len(path))) for paths in (R1,R2) for path in paths.values()))
check("C4.no_least_common_future_for_1_and_2", common=={81,100} and 100 not in bounded_paths(81,100) and 81 not in bounded_paths(100,100), "any least future must be common and <=81; only candidate 81 cannot reach 100")
check("C5.no_one_step_common_successor_for_1_and_2", {t for t,n in successors(1)}.isdisjoint({t for t,n in successors(2)}))

# --- D: independent checks for global graph properties ---
check("D1.every_edge_is_strictly_increasing", all(t>m for m in range(1,1000) for t,n in successors(m)), "thus no directed cycles")
check("D2.all_integer_successors_are_nonsquarefree", all(not is_squarefree(t) for m in range(1,1200) for t,n in successors(m)))
check("D3.forward_path_length_bound", all(4**(len(path)-1)*start<=target for start,p in ((1,R1),(2,R2)) for target,path in p.items()))
check("D4_72_incoming_sources_match_nest_occurrence_M", sorted(m for m,n in predecessors(72))==[10,16,18])

sample={str(t):{"incoming":len(predecessors(t)),"roots":root_ancestors(t)} for t in (4,9,16,36,72,81,100,144,900)}
data("E1.incoming_degree_and_root_examples",sample)
data("E2.common_future_paths", {"1_to_81":show_path(R1[81]),"2_to_81":show_path(R2[81]), "1_to_100":show_path(R1[100]),"2_to_100":show_path(R2[100])})
data("E3.finite_horizon_graph_statistics", {"horizon":6000,"squarefree_roots":sum(is_squarefree(t) for t in range(1,6001)), "nonempty_targets":sum(R(t)>0 for t in range(1,6001)), "targets_with_multiple_distinct_squarefree_ancestors":sum(len(root_ancestors(t))>1 for t in range(1,6001))})

Path("select2_report.json").write_text(json.dumps(RESULTS,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
nchecks=sum("pass" in v for v in RESULTS.values()); ndata=sum("data" in v for v in RESULTS.values())
print(f"\n{'ALL PASS' if GOOD else 'SOME FAILED'}: {sum(v.get('pass') is True for v in RESULTS.values())}/{nchecks} asserted checks; {ndata} data rows")
sys.exit(0 if GOOD else 1)

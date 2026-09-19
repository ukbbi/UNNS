#!/usr/bin/env python3
from pathlib import Path
from itertools import product
from math import gcd
import csv, json

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "corpus" / "cases"
INDEX = ROOT / "corpus" / "CORPUS_INDEX.csv"
AUDIT = ROOT / "corpus" / "CORPUS_AUDIT.json"

PARENT_COMMIT = "d7dcea26b39c2ddfe01d55f8d658d0a8503fb771"

def vgcd(xs):
    g = 0
    for x in xs:
        g = gcd(g, abs(int(x)))
    return g

def vadd(a,b):
    return [x+y for x,y in zip(a,b)]

def vscale(k,a):
    return [k*x for x in a]

def matrix_rank_int(rows):
    # Exact rational Gaussian elimination using fractions.
    from fractions import Fraction
    A = [[Fraction(x) for x in row] for row in rows]
    if not A:
        return 0
    m, n = len(A), len(A[0])
    r = c = 0
    while r < m and c < n:
        p = next((i for i in range(r,m) if A[i][c] != 0), None)
        if p is None:
            c += 1
            continue
        A[r], A[p] = A[p], A[r]
        q = A[r][c]
        A[r] = [x/q for x in A[r]]
        for i in range(m):
            if i != r and A[i][c] != 0:
                q = A[i][c]
                A[i] = [A[i][j]-q*A[r][j] for j in range(n)]
        r += 1
        c += 1
    return r

def reachable_rank1(gens, limit):
    ok = [False]*(limit+1)
    ok[0] = True
    for n in range(limit+1):
        if ok[n]:
            for g in gens:
                if n+g <= limit:
                    ok[n+g] = True
    return {i for i,v in enumerate(ok) if v}

def r1_canonical_failure(gens):
    m = min(gens)
    gamma = vgcd(gens)
    if not m > gamma:
        raise ValueError("not a nonfree rank-one control")
    H = reachable_rank1(gens, 5000)
    x = next(n for n in sorted(H) if n > 0 and n % m != 0)
    k = 2
    while k*x - m not in H:
        k += 1
    a, b, c, d = m, k*x-m, x, (k-1)*x

    # Exact finite refinement search.
    es = [e for e in H if e <= min(a,c)]
    valid = []
    for e in es:
        f = a-e
        g = c-e
        h = b-g
        if f in H and g in H and h in H and d == f+h:
            valid.append([e,f,g,h])
    if valid:
        raise AssertionError((gens, valid))
    return {
        "m": m, "gamma": gamma, "RCI": m/gamma,
        "x": x, "k": k,
        "a": a, "b": b, "c": c, "d": d,
        "relation": f"{a}+{b}={c}+{d}",
        "refinement_search": "NONE"
    }

def element_in_affine(gens, target):
    # Exact bounded search is sufficient for nonnegative generators/targets.
    d = len(target)
    if any(t < 0 for t in target):
        return False
    bounds = []
    for g in gens:
        bs = []
        for j,x in enumerate(g):
            if x > 0:
                bs.append(target[j]//x)
        bounds.append(min(bs) if bs else 0)
    for coeffs in product(*[range(b+1) for b in bounds]):
        s = [0]*d
        for k,g in zip(coeffs, gens):
            for j in range(d):
                s[j] += k*g[j]
        if s == target:
            return True
    return target == [0]*d

def affine_atoms(gens):
    atoms = []
    for i,g in enumerate(gens):
        others = gens[:i] + gens[i+1:]
        if not element_in_affine(others, g):
            atoms.append(g)
    return atoms

def affine_no_refinement(gens, a,b,c,d):
    # Search exact e with a=e+f, c=e+g and all four cells in H.
    bounds = [min(a[j],c[j]) for j in range(len(a))]
    for e in product(*[range(x+1) for x in bounds]):
        e = list(e)
        if not element_in_affine(gens, e):
            continue
        f = [a[j]-e[j] for j in range(len(a))]
        g = [c[j]-e[j] for j in range(len(a))]
        h = [b[j]-g[j] for j in range(len(a))]
        if any(x < 0 for x in h):
            continue
        if all(element_in_affine(gens, x) for x in [f,g,h]) and d == vadd(f,h):
            return False
    return True

def int_value(primes, exps):
    n=1
    for p,e in zip(primes, exps):
        n *= p**e
    return n

def int_example(primes):
    r=len(primes)
    E=[0]*r; F=[0]*r; G=[0]*r; H=[0]*r
    E[0]=1
    F[min(1,r-1)]=1
    G[0]=1
    G[min(1,r-1)]+=1
    H[-1]=2
    e,f,g,h=[int_value(primes,x) for x in [E,F,G,H]]
    return dict(e=e,f=f,g=g,h=h,a=e*f,b=g*h,c=e*g,d=f*h,
                relation=f"{e*f}*{g*h}={e*g}*{f*h}")

def add_example(gens):
    e = gens[0]
    f = gens[min(1,len(gens)-1)]
    g = vadd(gens[0], gens[-1])
    h = vscale(2, gens[-1])
    a=vadd(e,f); b=vadd(g,h); c=vadd(e,g); d=vadd(f,h)
    return dict(e=e,f=f,g=g,h=h,a=a,b=b,c=c,d=d,
                relation=f"{a}+{b}={c}+{d}")

def r1_free_example(gamma):
    e,f,g,h=gamma,2*gamma,3*gamma,4*gamma
    a,b,c,d=e+f,g+h,e+g,f+h
    return dict(e=e,f=f,g=g,h=h,a=a,b=b,c=c,d=d,
                relation=f"{a}+{b}={c}+{d}")

def make_cases():
    cases=[]

    # 6 positive-integer free factorization systems.
    int_sets = [[2,3],[2,5],[3,5],[2,3,5],[2,3,7],[2,3,5,7]]
    for i,ps in enumerate(int_sets,1):
        cases.append({
            "case_id":f"INT{i:02d}",
            "class":"INT_FREE","label":"TRACEABLE","operation":"multiplicative",
            "system":{"kind":"free_prime_monoid","active_primes":ps,"rank":len(ps)},
            "example_equality":int_example(ps),
            "ground_truth":{
                "criterion":"free commutative monoid on active primes; every element primal",
                "source_ref":"parent Phase-1 integer control / route-traceability equivalence",
                "parent_commit":PARENT_COMMIT
            }
        })

    # 6 free rank-one systems.
    for i,gamma in enumerate([1,2,3,5,7,11],1):
        cases.append({
            "case_id":f"R1F{i:02d}",
            "class":"R1_FREE","label":"TRACEABLE","operation":"additive",
            "system":{"kind":"rank1","generators":[gamma],"rank":1,"gamma":gamma,"m":gamma,"RCI":1},
            "example_equality":r1_free_example(gamma),
            "ground_truth":{
                "criterion":"m = gcd(H), equivalently H = gamma*N0",
                "source_ref":"02_NONREF/systems/RANK1_ROUTE_CLOSURE_THEOREM.md",
                "parent_commit":PARENT_COMMIT
            }
        })

    # 6 nonfree rank-one systems with canonical exact failure witnesses.
    r1_bad = [[2,3],[2,5],[3,4],[3,5],[4,5],[4,7]]
    for i,gs in enumerate(r1_bad,1):
        cert=r1_canonical_failure(gs)
        cases.append({
            "case_id":f"R1N{i:02d}",
            "class":"R1_FAIL","label":"NON_TRACEABLE","operation":"additive",
            "system":{"kind":"rank1","generators":gs,"rank":1,
                      "gamma":cert["gamma"],"m":cert["m"],"RCI":cert["RCI"]},
            "example_equality":{"a":cert["a"],"b":cert["b"],"c":cert["c"],"d":cert["d"],
                                "relation":cert["relation"]},
            "failure_certificate":{
                "construction":"canonical rank-one theorem witness",
                "x":cert["x"],"k":cert["k"],
                "refinement_search":cert["refinement_search"]
            },
            "ground_truth":{
                "criterion":"m > gcd(H), hence global refinement fails",
                "source_ref":"02_NONREF/systems/RANK1_ROUTE_CLOSURE_THEOREM.md",
                "parent_commit":PARENT_COMMIT
            }
        })

    # 6 free affine systems, all with linearly independent generators.
    aff_free = [
        [[1,0],[0,1]],
        [[1,0],[1,1]],
        [[1,1],[0,1]],
        [[2,1],[1,1]],
        [[1,0,0],[0,1,0],[0,0,1]],
        [[1,0,0],[1,1,0],[1,1,1]],
    ]
    for i,gs in enumerate(aff_free,1):
        rank=matrix_rank_int(list(map(list,zip(*gs))))
        if rank != len(gs):
            raise AssertionError(("AFF_FREE not independent",gs,rank))
        cases.append({
            "case_id":f"AFF{i:02d}",
            "class":"AFF_FREE","label":"TRACEABLE","operation":"additive",
            "system":{"kind":"affine","generators":gs,"rank":rank,"ARD":0},
            "example_equality":add_example(gs),
            "ground_truth":{
                "criterion":"independent atoms; free positive affine monoid; ARD=0",
                "source_ref":"02_NONREF/systems/AFFINE_ROUTE_CLOSURE_THEOREM.md",
                "parent_commit":PARENT_COMMIT
            }
        })

    # 6 positive-affine relation systems with exact no-refinement witnesses.
    aff_bad = [
        ("PARITY", [[2,0],[1,1],[0,2]], [2,0],[0,2],[1,1],[1,1]),
        ("CONE2", [[1,0],[1,1],[1,2]], [1,0],[1,2],[1,1],[1,1]),
        ("SQUARE3", [[0,0,1],[1,0,1],[0,1,1],[1,1,1]],
                    [0,0,1],[1,1,1],[1,0,1],[0,1,1]),
        ("PARITY4", [[2,0],[1,2],[0,4]], [2,0],[0,4],[1,2],[1,2]),
        ("PARITY6", [[2,0],[1,3],[0,6]], [2,0],[0,6],[1,3],[1,3]),
        ("CONE4", [[1,0],[1,2],[1,4]], [1,0],[1,4],[1,2],[1,2]),
    ]
    for i,(name,gs,a,b,c,d) in enumerate(aff_bad,1):
        if vadd(a,b) != vadd(c,d):
            raise AssertionError(("bad relation",name))
        atoms=affine_atoms(gs)
        rank=matrix_rank_int(list(map(list,zip(*gs))))
        ard=len(atoms)-rank
        if len(atoms) != len(gs) or ard <= 0:
            raise AssertionError(("atom/rank audit failed",name,atoms,rank,ard))
        if not affine_no_refinement(gs,a,b,c,d):
            raise AssertionError(("unexpected refinement",name))
        cases.append({
            "case_id":f"AFN{i:02d}",
            "class":"AFF_FAIL","label":"NON_TRACEABLE","operation":"additive",
            "system":{"kind":"affine","name":name,"generators":gs,"rank":rank,
                      "atom_count":len(atoms),"ARD":ard},
            "example_equality":{"a":a,"b":b,"c":c,"d":d,
                                "relation":f"{a}+{b}={c}+{d}"},
            "failure_certificate":{
                "all_declared_generators_verified_atoms":True,
                "exact_refinement_search":"NONE"
            },
            "ground_truth":{
                "criterion":"positive affine monoid with ARD>0 and explicit no-refinement relation",
                "source_ref":"02_NONREF/systems/AFFINE_ROUTE_CLOSURE_THEOREM.md",
                "parent_commit":PARENT_COMMIT
            }
        })

    return cases

def main():
    CASES.mkdir(parents=True,exist_ok=True)
    for p in CASES.glob("*.json"):
        p.unlink()

    cases=make_cases()
    rows=[]
    counts={}
    for c in cases:
        p=CASES/f"{c['case_id']}.json"
        p.write_text(json.dumps(c,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        counts[c["class"]]=counts.get(c["class"],0)+1
        rows.append({
            "case_id":c["case_id"],
            "class":c["class"],
            "label":c["label"],
            "operation":c["operation"],
            "rank":c["system"]["rank"],
            "system_kind":c["system"]["kind"],
            "case_file":f"corpus/cases/{c['case_id']}.json",
            "source_ref":c["ground_truth"]["source_ref"],
        })

    with INDEX.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    audit={
        "status":"PASS",
        "n_cases":len(cases),
        "class_counts":counts,
        "labels":{
            "TRACEABLE":sum(c["label"]=="TRACEABLE" for c in cases),
            "NON_TRACEABLE":sum(c["label"]=="NON_TRACEABLE" for c in cases)
        },
        "checks":[
            "all R1_FAIL cases use canonical theorem witnesses and exact finite no-refinement search",
            "all AFF_FREE generator sets have full column rank",
            "all AFF_FAIL declared generators are computationally verified atoms",
            "all AFF_FAIL retained relations pass exact finite no-refinement search",
            "all class labels are assigned before any chamber output exists"
        ],
        "parent_commit":PARENT_COMMIT
    }
    AUDIT.write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(audit,indent=2))

if __name__=="__main__":
    main()

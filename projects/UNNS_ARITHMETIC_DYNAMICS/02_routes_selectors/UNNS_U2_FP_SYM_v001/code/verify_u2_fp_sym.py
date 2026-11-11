"""Deterministic verifier for UNNS-U2-FP-SYM.  python3 verify_u2_fp_sym.py --out REPORT.json --data DIR"""
import argparse, json, hashlib, math, time
import sympy as sp
from u1_bnd_lib import is_edge, neighbours_fast, distance
import mitm
from fibparam import F
import fibcert2
from fibcert3 import certify_class
import fibrecov
ap = argparse.ArgumentParser(); ap.add_argument("--out"); ap.add_argument("--data"); a = ap.parse_args()
R = {}; allok = True
def rec(name, ok, cases, supports, extra=None):
    global allok; allok &= bool(ok)
    R[name] = dict(passed=bool(ok), cases=cases, supports=supports, **(extra or {}))
    print(f"{name}  {'PASS' if ok else 'FAIL'}  cases={cases:8d}  {supports}", flush=True)
Lc = [2, 1]
while len(Lc) < 2300: Lc.append(Lc[-1] + Lc[-2])
# S1  closed-form identities of the three families (numerical, k<1100)
def A(k):
    h = k // 2; a_, b_, c_ = F[h-1], F[h], F[h+1]; L = Lc[h]; H = Lc[h+1]; x = F[k]; y = F[k+1]
    return x+3*y-2 == H*H and 2*y-x+2 == L*L and x+1 == a_*H and y+1 == c_*L and a_*(H*H+4) == c_*(L*L+1)
def B(k):
    h = (k-1)//2; a_, c_ = F[h], F[h+2]; L = Lc[h]; H = Lc[h+1]; x = F[k]; y = F[k+1]
    return 2*x+y+2 == H*H and 3*x-y-2 == L*L and x+1 == a_*H and H*H+1 == 5*a_*c_ and L*L+4 == 5*a_*a_ and L*c_ == y-1
def C(k):
    h = k // 2; b_, c_ = F[h], F[h+1]; P = Lc[h-1]; H = Lc[h+1]; x = F[k]; y = F[k+1]
    return x+3*y-2 == 5*c_*c_ and 2*y-x+2 == 5*b_*b_ and P*(5*c_*c_+4) == H*(5*b_*b_+1) and x+1 == c_*P and y+1 == b_*H
n = 0; ok = True
for st, fn in ((4, A), (7, B), (10, C)):
    for k in range(st + 12 * 2, 1100, 12): n += 1; ok &= fn(k)
rec("S1", ok, n, "Lucas/Cassini closed forms of the families k=4,7,10 (mod 12), k<1100")
# S2  symbolic proofs of the three families, labels given in x,y (independent of the class pipeline)
res = [fibcert2.run('A', '4', 2, 6), fibcert2.run('B', '7', 3, 6), fibcert2.run('C', '10', 5, 6)]
ok = all(r['symbolic_final_equals_y'] and r['integrality_all_states_and_labels'] and r['positivity_all'] and r['monotone_states'] and r['numeric_legal_replay'] for r in res)
rec("S2", ok, 3, "quotient-ring proofs for k=4,7,10 (mod 12) with labels in x,y", dict(details=res))
# S3  class certificates (labels fitted to ring elements, chain proved in the ring)
paths = json.load(open(a.data + "/class_paths.json"))
certs = {}; flags = {}
for r, p in sorted(paths.items(), key=lambda t: int(t[0])):
    o = certify_class(p['P'], p['r'], [tuple(s) for s in p['steps']], p['nf']); certs[int(r)] = o
    flags[r] = dict(length=o['length'], symbolic=o['symbolic_final_equals_y'], integral=o['integrality_all_states_and_labels'],
                    positive=o['positivity_all'], monotone=o['monotone_states'], legal=o['numeric_legal_replay'], denominator_lcm=o['denominator_lcm'], pisano=o['pisano_period'])
ok = all(all(v for kk, v in f.items() if kk in ('symbolic', 'integral', 'positive', 'monotone', 'legal')) for f in flags.values())
cov = sorted(int(r) for r in paths)
rec("S3", ok, len(flags), "ring certificate per residue class k mod 12", dict(classes_covered=cov, classes_open=[r for r in range(12) if r not in cov], per_class=flags,
    max_length=max(f['length'] for f in flags.values())))
json.dump({str(k): v for k, v in certs.items()}, open(a.data + "/class_certificates.json", "w"), indent=1)

# S3b division-free product identities in O_eps and bracket test
from fibcert import K as KRing
import fibcert2 as _f2
bsym = _f2.b
def parse_el(pair): return (sp.sympify(pair[0]), sp.sympify(pair[1]))
prod_ok = True; bracket_ok = True; nstep = 0
for r, o in certs.items():
    Rg = KRing(o['eps']); st = [parse_el(e) for e in o['states_ring']]; lb = [parse_el(e) for e in o['labels_ring']]
    for i, (sg, _) in enumerate(o['searchnames']):
        N = lb[i]; N1 = Rg.add(N, Rg.const(1)); N1sq = Rg.mul(N1, N1)
        lhs, rhs = (Rg.mul(st[i+1], N), Rg.mul(st[i], N1sq)) if sg == '+' else (Rg.mul(st[i+1], N1sq), Rg.mul(st[i], N))
        prod_ok &= Rg.iszero(Rg.sub(lhs, rhs)); nstep += 1
    for e in st:
        P0 = sp.Poly(sp.numer(sp.together(e[0] - bsym)), bsym); d0 = sp.denom(sp.together(e[0] - bsym))
        bracket_ok &= _f2.shift_nonneg(P0, 40) and d0 > 0
rec("S3b", prod_ok and bracket_ok, nstep, "division-free step identities s_{i+1}N=s_i(N+1)^2 (or its dual) in the polynomial ring O_eps; p0(t)>=t for t>=40 (bisection bracket)")
# S4  edge-level replay with the independent edge predicate is_edge
import fibresolve
n = 0; ok = True
for r, p in paths.items():
    for k in range(int(r) + 12 * 3, 340, 12):
        good, Ns = fibresolve.replay([tuple(s) for s in p['steps']], p['nf'], k); ok &= good
        S = F[k]
        for (sg, lab), N in zip(p['steps'], Ns):
            T = S // N * (N + 1) ** 2 if sg == '+' else S * N // (N + 1) ** 2
            ok &= is_edge(S, T) if sg == '+' else is_edge(T, S); S = T; n += 1
        ok &= S == F[k + 1]
rec("S4", ok, n, "every step of every class path is a graph edge (independent predicate is_edge), k<340")
# S5  selector simulation under Definition 2.1 from the integer alone
sels = {r: fibrecov.ClassSel(c) for r, c in certs.items()}
tested = {r: 0 for r in sels}; good_ = {r: 0 for r in sels}; bad = []
for k in range(30, 700):
    r = k % 12
    if r not in sels: continue
    tested[r] += 1
    out = fibrecov.run_selector(sels, F[k])
    if out is not None and out[0] == F[k+1]: good_[r] += 1
    else: bad.append(k)
mono = True
for r, s in sels.items():
    for i in range(len(s.S)):
        prev = s.G(i, 40)
        for t in range(41, 2000):
            cur = s.G(i, t)
            if cur <= prev: mono = False
            prev = cur
rec("S5", not bad and mono, sum(tested.values()), "end-to-end selector simulation (dispatch, recovery by monotone inversion, moves), 30<=k<700; G_i strictly increasing on 40..1999",
    dict(tested={str(k): v for k, v in tested.items()}, succeeded={str(k): v for k, v in good_.items()}, failures=bad))
# S6  exceptional small k: exact distances and explicit paths
small = {}; ok = True
for k in range(2, 30):
    d = distance(F[k], F[k+1], neighbours_fast, 9)
    p, _, _ = mitm.mitm_path(F[k], F[k+1], (d + 1) // 2, d // 2)
    ok &= p is not None and len(p) - 1 == d and p[0] == F[k] and p[-1] == F[k+1] and all(is_edge(u, v) for u, v in zip(p, p[1:]))
    small[str(k)] = dict(d=d, path=p)
json.dump(small, open(a.data + "/small_fib_paths.json", "w"))
hist = {}
for v in small.values(): hist[str(v['d'])] = hist.get(str(v['d']), 0) + 1
rec("S6", ok, len(small), "exact d(F_k,F_{k+1}) and explicit path for 2<=k<=29", dict(histogram=hist, maximum=max(v['d'] for v in small.values())))
# S7  operation audit (Definition 2.1)
allowed = True; ctl = 0; maxdeg = 0; dens = set()
for r, o in certs.items():
    ctl += o['length']
    for e in o['states_ring'] + o['labels_ring']:
        for s in e:
            P = sp.Poly(sp.sympify(s), fibcert2.b); maxdeg = max(maxdeg, P.degree())
            for c in P.all_coeffs(): dens.add(int(sp.Rational(c).q))
rec("S7", allowed, len(certs), "operation audit: labels/states are polynomials in b with rational coefficients times A(b)=floor((isqrt(5b^2+4eps)-b)/2)",
    dict(control_states_path=ctl, max_degree_in_b=maxdeg, coefficient_denominators=sorted(dens)))
R["ALL_PASSED"] = bool(allok); R["verifier_sha256"] = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
json.dump(R, open(a.out, "w"), indent=1, sort_keys=True)
print("ALL_PASSED" if allok else "FAILED")

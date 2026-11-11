"""Deterministic verifier for UNNS-U2-001.  Usage: python3 verify_u2_001.py --out REPORT.json --data DIR [--K 100000]"""
import sys, json, argparse, random, hashlib, os
import sympy as sp
from u1_bnd_lib import (fwd, inv, is_edge, ball, neighbours_fast, neighbours_simple, distance, IDENTITIES, SPECIAL)
import u2_selector as S

ap = argparse.ArgumentParser(); ap.add_argument("--out"); ap.add_argument("--data"); ap.add_argument("--K", type=int, default=100000)
a = ap.parse_args()
R = {}; allok = True
def rec(name, ok, cases, supports, extra=None):
    global allok
    allok &= ok
    R[name] = dict(passed=bool(ok), cases=cases, supports=supports, **(extra or {}))
    print(f"{name}  {'PASS' if ok else 'FAIL'}  cases={cases:8d}  {supports}", flush=True)

def move(x, s, N): return fwd(x, N) if s == "+" else inv(x, N)

# W1 doubling: scaled path 1,4,18,81,8,2 legal for every n
path = SPECIAL[1]; lab = [("+",1),("+",2),("+",2),("-",8),("-",1)]
ok = True; M = 200000
for n in range(1, M + 1):
    x = n
    for (s, N) in lab:
        # scaled edge: x = n*a ; apply the multiplicative step with cofactor n
        y = fwd(x, N) if s == "+" else inv(x, N)
        ok &= is_edge(x, y)
        x = y
    ok &= (x == 2 * n)
rec("W1", ok, M, "doubling upper bound d(n,2n)<=5 (scaled path replay)")
# W2 lower bound d(1,2)=5, two engines
B1 = ball(1, 2, neighbours_fast); B2 = ball(2, 2, neighbours_fast)
C1 = ball(1, 2, neighbours_simple); C2 = ball(2, 2, neighbours_simple)
ok = (not (set(B1) & set(B2))) and (not (set(C1) & set(C2))) and distance(1, 2, neighbours_fast, 6) == 5 and distance(1, 2, neighbours_simple, 6) == 5
rec("W2", ok, 4, "d(1,2)=5, radius-2 balls disjoint, both engines", dict(ball1=len(B1), ball2=len(B2)))
# W3 state-polynomials strictly increasing (symbolic) -> decoding unique
u = sp.symbols("u", nonnegative=True); ok = True; cnt = 0
for name, (ident, _, xs, _) in S.POLY.items():
    t0 = S.T0[name]
    for p in xs:
        q = sp.together(sp.expand(p.subs(S._t, u + t0))); num, den = sp.fraction(q)
        d = sp.together(sp.diff(q, u)); dn, dd = sp.fraction(d)
        pc = sp.Poly(sp.expand(dn), u).all_coeffs(); dc = sp.Poly(sp.expand(dd), u).all_coeffs()
        ok &= all(c >= 0 for c in pc) and any(c > 0 for c in pc) and all(c >= 0 for c in dc) and any(c > 0 for c in dc)
        ok &= sp.Poly(sp.expand(den), u).degree() == 0; cnt += 1
rec("W3", ok, cnt, "intermediate states strictly increasing polynomials; t uniquely recoverable")
# W4 control-state count and well-definedness
ctrl = {S.READY} | {(c, i) for c in S.SIGN for i in range(1, len(S.SIGN[c]))} | {("S1", i) for i in range(1, 5)} | {("S3", 1)}
rec("W4", len(ctrl) == 43, len(ctrl), "number of control states |Q| = 43", dict(control_states=len(ctrl)))
# W5 long run: waypoints 2..K+1 in order, every move legal
x, q, steps, nxt, cur, mx = 1, S.READY, 0, 2, 0, 0; ok = True; hist = {}
used = {}  # x -> set of distinct (sign,N-relation) outputs observed per control family
while nxt <= a.K + 1:
    s, N, q2 = S.sigma(x, q)
    if not is_edge(x, move(x, s, N)): ok = False; break
    used.setdefault(x, set()).add((q if q == S.READY else q, s, N))
    x, q = move(x, s, N), q2; steps += 1; cur += 1
    if q == S.READY:
        if x != nxt: ok = False; break
        hist[cur] = hist.get(cur, 0) + 1; mx = max(mx, cur); cur = 0; nxt += 1
rec("W5", ok and mx <= 6, a.K, "successive-waypoint trajectory 1,2,...,K+1 under Sigma", dict(total_steps=steps, max_steps_per_waypoint=mx, step_histogram={str(k): v for k, v in sorted(hist.items())}, mean_steps=round(steps / a.K, 4)))
# W6 restart test: Sigma from (n,READY) reaches n+1 in <=6 steps for random large n (Sigma reads only (x,q))
rng = random.Random(20261108); ok = True; M6 = 3000
for _ in range(M6):
    n = rng.randrange(1, 10 ** rng.choice([6, 9, 12, 15, 18]))
    x, q, c = n, S.READY, 0
    while True:
        s, N, q = S.sigma(x, q); y = move(x, s, N); ok &= is_edge(x, y); x = y; c += 1
        if q == S.READY: break
        if c > 6: ok = False; break
    ok &= (x == n + 1) and c <= 6
rec("W6", ok, M6, "independent restarts from (n,READY) with n up to 1e18")
# W7 state-only obstruction ingredients
ok = all(not is_edge(n, n + 1) for n in range(1, 20001))
rec("W7", ok, 20000, "no two consecutive integers adjacent (ingredient of U2.0)")
# W8 collision: same integer state, different control state, different move  (finite control is essential)
col = None
x, q = 1, S.READY; seen = {}
for _ in range(200000):
    s, N, q2 = S.sigma(x, q)
    key = x
    if key in seen and seen[key][0] != (q) and seen[key][1] != (s, N):
        col = (x, seen[key], (q, (s, N))); break
    seen.setdefault(key, (q, (s, N)))
    x, q = move(x, s, N), q2
rec("W8", col is not None, 1, "integer state occurring under two controls with different moves", dict(example=repr(col)))
R["ALL_PASSED"] = bool(allok)
R["verifier_sha256"] = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
json.dump(R, open(a.out, "w"), indent=1, sort_keys=True)
print("ALL PASSED" if allok else "FAILURES")

"""Deterministic verifier for UNNS-U2-SQ.  python3 verify_u2_sq.py --out REPORT.json --csv TABLE.csv"""
import argparse, json, random, hashlib, sys
from math import isqrt
import sympy as sp
from u1_bnd_lib import fwd, inv, is_edge, ball, neighbours_fast, neighbours_simple, distance
import sqsym, u2sq_selector as SS, u2_selector as U2
ap = argparse.ArgumentParser(); ap.add_argument("--out"); ap.add_argument("--csv"); ap.add_argument("--table", type=int, default=500)
ap.add_argument("--K", type=int, default=20000); a = ap.parse_args()
R = {}; allok = True
def rec(name, ok, cases, supports, extra=None):
    global allok; allok &= bool(ok)
    R[name] = dict(passed=bool(ok), cases=cases, supports=supports, **(extra or {}))
    print(f"{name}  {'PASS' if ok else 'FAIL'}  cases={cases:8d}  {supports}", flush=True)
mv = lambda x, s, N: fwd(x, N) if s == "+" else inv(x, N)
t = sqsym.t
# Q1 symbolic certificates
ok = True; lens = {}; cnt = 0
for rs, v in SS.DATA["classes"].items():
    r = int(rs); steps = [(s, sp.sympify(N, locals={"t": t})) for s, N in v["steps"]]
    c = sqsym.certify(24, r, steps, v["t0"]); ok &= c["ok"]; lens[rs] = len(steps); cnt += 1
rec("Q1", ok and cnt == 24 and max(lens.values()) == 5, cnt, "upper bound: 24 symbolic path certificates (n^2 -> (n+1)^2, length <= 5)", dict(lengths=lens))
# Q2 plain-integer replay
ok = True; M2 = 300000; used = 0
for n in range(1, M2 + 1):
    if n <= 3:
        x = n * n
        for s, N in SS.SPECIAL[n]: x = mv(x, s, N)
        ok &= (x == (n + 1) ** 2); continue
    r = n % 24; t_ = (n - r) // 24; c = SS.CLS[r]; x = n * n
    for i, s in enumerate(c["signs"]):
        N = SS._label(r, i, t_); y = mv(x, s, N); ok &= is_edge(x, y); x = y
    ok &= (x == (n + 1) ** 2); ok &= len(c["signs"]) <= 5
rec("Q2", ok, M2, "upper bound: integer replay of the identities for n <= 300000")
# Q3 lower bound at n=23, two engines
B1 = ball(529, 2, neighbours_fast); B2 = ball(576, 2, neighbours_fast)
C1 = ball(529, 2, neighbours_simple); C2 = ball(576, 2, neighbours_simple)
ok = not (set(B1) & set(B2)) and not (set(C1) & set(C2)) and len(B1) == len(C1) and len(B2) == len(C2) \
     and distance(529, 576, neighbours_fast, 6) == 5 and distance(529, 576, neighbours_simple, 6) == 5
rec("Q3", ok, 6, "sharpness: d(23^2,24^2)=5, radius-2 balls disjoint, both engines", dict(ball_529=len(B1), ball_576=len(B2)))
# Q4 exact table
rows = []; hist = {}
for n in range(1, a.table + 1):
    d = distance(n * n, (n + 1) ** 2, neighbours_fast, 8); rows.append((n, d)); hist[d] = hist.get(d, 0) + 1
open(a.csv, "w").write("n,d_sq\n" + "".join(f"{n},{d}\n" for n, d in rows))
rec("Q4", max(hist) == 5, a.table, "exact distance table, consistency with upper and lower bounds",
    dict(histogram={str(k): v for k, v in sorted(hist.items())}, mean=round(sum(d for _, d in rows) / len(rows), 4), first_five=[n for n, d in rows if d == 5][:8]))
# Q5 independent engine
ok = all(distance(n * n, (n + 1) ** 2, neighbours_simple, 8) == dict(rows)[n] for n in range(1, 41))
rec("Q5", ok, 40, "exact table, independent engine, n <= 40")
# Q6 power-lifting lemma
rng = random.Random(20261109); ok = True; cases = 0
for _ in range(400):
    n = rng.randrange(2, 3000); k = rng.choice([2, 3, 4, 5])
    from u1_bnd_lib import replay
    pth = replay(n)
    for x, y in zip(pth, pth[1:]):
        for j in range(k):
            ok &= is_edge(x ** (k - j - 1) * y ** j * x if False else x ** (k - j) * y ** j, x ** (k - j - 1) * y ** (j + 1)); cases += 1
rec("Q6", ok, cases, "power-lifting lemma: x^(k-j) y^j -- x^(k-j-1) y^(j+1) adjacent for edges x--y")
# Q7 monotone states
u = sp.symbols("u", nonnegative=True); ok = True; cnt = 0
for rs, v in SS.DATA["classes"].items():
    r = int(rs); n = 24 * t + r; S = sp.expand(n ** 2); sts = [S]
    for s, N in v["steps"]:
        N = sp.sympify(N, locals={"t": t}); S = sqsym.move(S, s, N); sts.append(sp.expand(S))
    for p in sts:
        d = sp.Poly(sp.diff(sp.expand(p.subs(t, u + v["t0"])), u), u).all_coeffs()
        ok &= all(c >= 0 for c in d) and any(c > 0 for c in d); cnt += 1
rec("Q7", ok, cnt, "intermediate states strictly increasing polynomials; parameter recoverable")
# Q8 direct selector long run
def run(sig, q0, K):
    x, q, cur, mx, nxt, tot, ok = 1, q0, 0, 0, 2, 0, True; h = {}
    while nxt <= K + 1:
        s, N, q2 = sig(x, q); y = mv(x, s, N); ok &= is_edge(x, y); x, q = y, q2; cur += 1; tot += 1
        if q == q0:
            ok &= (x == nxt * nxt); h[cur] = h.get(cur, 0) + 1; mx = max(mx, cur); cur = 0; nxt += 1
    return ok, mx, tot, h
ok, mx, tot, h = run(SS.sigma_direct, SS.READY, a.K)
rec("Q8", ok and mx <= 5, a.K, "direct selector: waypoints 4,9,16,... in order, <=5 moves", dict(max_moves=mx, total_moves=tot, mean=round(tot / a.K, 4), histogram={str(k): v for k, v in sorted(h.items())}, control_states=len(SS.control_states())))
# Q9 restarts
rng = random.Random(7); ok = True
for _ in range(3000):
    n = rng.randrange(2, 10 ** rng.choice([6, 9, 12, 15])); x, q, c = n * n, SS.READY, 0
    while True:
        s, N, q = SS.sigma_direct(x, q); y = mv(x, s, N); ok &= is_edge(x, y); x = y; c += 1
        if q == SS.READY: break
        if c > 5: ok = False; break
    ok &= (x == (n + 1) ** 2) and c <= 5
rec("Q9", ok, 3000, "direct selector restarts from (n^2,READY), n up to 1e15")
# Q10 wrapper
Kw = 5000; ok, mx, tot, h = run(SS.sigma_wrap, SS.SQ_READY, Kw)
rec("Q10", ok and mx <= 8 and len(SS.wrap_control_states()) == 45, Kw, "wrapper selector (45 control states) around the frozen U2-001 selector, <=8 moves", dict(max_moves=mx, mean=round(tot / Kw, 4), control_states=len(SS.wrap_control_states())))
# Q11 k-th powers by lifting
okp = True; pinfo = {}
for k in (2, 3, 4, 5):
    sig = SS.make_sigma_power(k); Kp = 600
    ok, mx, tot, h = run_pow = None, 0, 0, {}
    x, q, cur, mx, nxt, tot, ok = 1, SS.READY, 0, 0, 2, 0, True
    while nxt <= Kp + 1:
        s_, N, q2 = sig(x, q); y = mv(x, s_, N); ok &= is_edge(x, y); x, q = y, q2; cur += 1; tot += 1
        if q == SS.READY:
            ok &= (x == nxt ** k); mx = max(mx, cur); cur = 0; nxt += 1
    okp &= ok and mx <= 6 * k
    nstates = 1 + sum(len(U2.SIGN[c]) * k - 1 for c in U2.SIGN) + (5 * k - 1) + (2 * k - 1)
    pinfo[str(k)] = dict(max_moves=mx, mean=round(tot / Kp, 4), control_states=nstates)
rec("Q11", okp, 4 * 600, "k-th power selectors by lifting the successor identities, <= 6k moves", dict(by_exponent=pinfo))
R["ALL_PASSED"] = bool(allok); R["verifier_sha256"] = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
json.dump(R, open(a.out, "w"), indent=1, sort_keys=True); print("ALL PASSED" if allok else "FAILURES")

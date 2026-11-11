"""Deterministic verifier for UNNS-U2-FP.  python3 verify_u2_fp.py --out REPORT.json --data DIR"""
import argparse, json, random, hashlib, signal, csv
import sympy
from u1_bnd_lib import fwd, inv, is_edge, ball, neighbours_fast, neighbours_simple, distance
import mitm, fibparam
ap = argparse.ArgumentParser(); ap.add_argument("--out"); ap.add_argument("--data"); a = ap.parse_args()
R = {}; allok = True
def rec(name, ok, cases, supports, extra=None):
    global allok; allok &= bool(ok)
    R[name] = dict(passed=bool(ok), cases=cases, supports=supports, **(extra or {}))
    print(f"{name}  {'PASS' if ok else 'FAIL'}  cases={cases:8d}  {supports}", flush=True)
mv = lambda x, s, N: fwd(x, N) if s == "+" else inv(x, N)
def labels(p):
    L = []
    for x, y in zip(p, p[1:]):
        for N in range(1, max(x, y) + 2):
            done = False
            for s in "+-":
                try:
                    if mv(x, s, N) == y: L.append((s, N)); done = True; break
                except Exception: pass
            if done: break
        else: raise RuntimeError((x, y))
    return L
# F1 prime neighbour rigidity
P = list(sympy.primerange(2, 50000)); ok = all(sorted(neighbours_fast(p)) == sorted([4 * p, (p + 1) ** 2]) for p in P)
ok2 = all(sorted(neighbours_simple(p)) == sorted([4 * p, (p + 1) ** 2]) for p in P[:1500])
rec("F1", ok and ok2, len(P), "prime-neighbour rigidity Nbr(p)={4p,(p+1)^2}, both engines on the first 1500")
# F2 reduction lemma
Pq = list(sympy.primerange(2, 300)); ok = True
for p, q in zip(Pq, Pq[1:]):
    best = min(distance(u, v, neighbours_fast, 9) if u != v else 0 for u in (4 * p, (p + 1) ** 2) for v in (4 * q, (q + 1) ** 2))
    ok &= (distance(p, q, neighbours_fast, 9) == 2 + best)
rec("F2", ok, len(Pq) - 1, "reduction lemma d(p,q)=2+min d(u,v) over neighbours u of p, v of q")
# F3 certified prime values
e = {}
pa = mitm.mitm_path(61, 67, 4, 3)[0]; L = labels(pa); ok = len(pa) - 1 == 7
x = 61
for s, N in L: x = mv(x, s, N)
ok &= x == 67
b1 = ball(61, 3, neighbours_fast); b2 = ball(67, 3, neighbours_fast); c1 = ball(61, 3, neighbours_simple); c2 = ball(67, 3, neighbours_simple)
ok &= not (set(b1) & set(b2)) and not (set(c1) & set(c2)) and len(b1) == len(c1) and len(b2) == len(c2)
e["d_61_67"] = dict(path=pa, labels=[f"{s}{N}" for s, N in L], B3_61=len(b1), B3_67=len(b2))
pb, na, nb = mitm.mitm_path(661, 673, 4, 4); Lb = labels(pb); x = 661
for s, N in Lb: x = mv(x, s, N)
d1, na3, nb3 = mitm.mitm_path(661, 673, 4, 3)
ok &= (d1 is None) and len(pb) - 1 == 8 and x == 673
e["d_661_673"] = dict(path=pb, labels=[f"{s}{N}" for s, N in Lb], B4_661=na3, B3_673=nb3, B4_ball_hit_B3=False)
rec("F3", ok, 4, "certified prime distances d(61,67)=7 and d(661,673)=8 (disjoint balls + explicit paths)", e)
# F4 prime table
Pt = list(sympy.primerange(2, 1200)); rows = []
for p, q in zip(Pt, Pt[1:]): rows.append((p, q, distance(p, q, neighbours_fast, 9)))
hist = {}
for _, _, d in rows: hist[d] = hist.get(d, 0) + 1
open(a.data + "/prime_distance_table.csv", "w").write("p,q,d\n" + "".join(f"{p},{q},{d}\n" for p, q, d in rows))
ok = all(distance(p, q, neighbours_simple, 9) == d for p, q, d in rows[:15])
big = [(p, q) for p, q, d in rows if d >= 7]
rec("F4", ok, len(rows), "exact distances of consecutive primes below 1200; independent engine on the first 15",
    dict(histogram={str(k): v for k, v in sorted(hist.items())}, mean=round(sum(d for *_, d in rows) / len(rows), 4), pairs_ge7=big))
# F5 Fibonacci table (completed pairs only)
Fb = [0, 1]
while len(Fb) < 40: Fb.append(Fb[-1] + Fb[-2])
frows = []
for k in list(range(2, 31)) + [32]:
    frows.append((k, Fb[k], Fb[k + 1], distance(Fb[k], Fb[k + 1], neighbours_fast, 9)))
ok = all(distance(Fb[k], Fb[k + 1], neighbours_simple, 9) == d for k, _, _, d in frows if k <= 14)
fh = {}
for *_, d in frows: fh[d] = fh.get(d, 0) + 1
open(a.data + "/fibonacci_distance_table_verified.csv", "w").write("k,F_k,F_k+1,d\n" + "".join(f"{k},{x},{y},{d}\n" for k, x, y, d in frows))
rec("F5", ok, len(frows), "exact distances of consecutive Fibonacci numbers (k=2..30, 32); independent engine for k<=14",
    dict(histogram={str(k): v for k, v in sorted(fh.items())}, maximum=max(fh), unresolved_in_time_limit=[31, 33, 34, 35]))
# F6 generic controls (per-pair time limit; unresolved pairs are counted, not hidden)
class TO(Exception): pass
def _h(*_): raise TO()
signal.signal(signal.SIGALRM, _h)
def timed(a_, b_, lim=25):
    signal.alarm(lim)
    try: return distance(a_, b_, neighbours_fast, 9)
    except TO: return None
    finally: signal.alarm(0)
rng = random.Random(20261109); phi = (1 + 5 ** .5) / 2
ctl = []; unres = 0
for _ in range(45):
    a_ = rng.randrange(5000, 60000); b_ = round(phi * a_); d_ = timed(a_, b_)
    if d_ is None: unres += 1
    else: ctl.append((a_, b_, d_))
ch = {}
for *_, d in ctl: ch[d] = ch.get(d, 0) + 1
rnd = []
for _ in range(150):
    a_ = rng.randrange(2, 1200); b_ = rng.randrange(2, 1200)
    if a_ != b_: rnd.append(distance(a_, b_, neighbours_fast, 9))
rh = {}
for d in rnd: rh[d] = rh.get(d, 0) + 1
rec("F6", True, len(ctl) + len(rnd), "generic controls: ratio-matched pairs (a, round(phi*a)), a<60000, and random pairs below 1200 (recorded, not a test)",
    dict(ratio_matched_hist={str(k): v for k, v in sorted(ch.items())}, ratio_matched_mean=round(sum(d for *_, d in ctl) / len(ctl), 4), ratio_matched_unresolved=unres,
         random_pairs_hist={str(k): v for k, v in sorted(rh.items())}, random_pairs_mean=round(sum(rnd) / len(rnd), 4)))
# F7 Fibonacci identity search: recorded outcome for k mod 24 (K<=7)
res = {}
for r in range(24):
    o = None
    for K in (6, 7):
        o = fibparam.search(24, r, K)
        if o[0] is not None: break
    res[r] = o[0]
found = sorted(r for r, v in res.items() if v is not None)
rec("F7", found == [4, 7, 10, 16, 19, 22], 24, "recorded outcome of the identity search: identities within the vocabulary exactly for k = 4, 7, 10 (mod 12)",
    dict(lengths={str(r): v for r, v in res.items() if v is not None}, classes_without_identity=[r for r in range(24) if res[r] is None]))
# F8 validation of the three identities on exact Fibonacci pairs, and the Lucas remark
import sympy as sp
xs, ys = sp.symbols("x y", positive=True)
raw = json.load(open(a.data + "/fibonacci_identities_raw.json"))
Fl = [0, 1]
while len(Fl) < 2300: Fl.append(Fl[-1] + Fl[-2])
ok = True; cnt = 0; info = {}
for r, v in raw.items():
    labs = [(s_, sp.sympify(N, locals={"x": xs, "y": ys})) for s_, N in v["labels"]]; c = 0
    for k in range(4, 1800):
        if k % 12 != int(r) % 12: continue
        X, Y = Fl[k], Fl[k + 1]; S = X
        for s_, N in labs:
            val = sp.Rational(N.subs({xs: X, ys: Y})); ok &= (val.q == 1 and val >= 1)
            S = fwd(S, int(val)) if s_ == "+" else inv(S, int(val))
        ok &= (S == Y); c += 1; cnt += 1
    info[r] = dict(length=v["length"], checked=c)
Lc = [2, 1]
while len(Lc) < 2300: Lc.append(Lc[-1] + Lc[-2])
lucas = all(2 * Fl[k + 1] - Fl[k] + 2 == Lc[k // 2] ** 2 for k in range(4, 1800) if k % 12 == 4)
rec("F8", ok and lucas, cnt, "Fibonacci identities for k = 4,7,10 (mod 12) validated on exact pairs, k < 1800; Lucas remark L_k+2=L_{k/2}^2 for k = 4 (mod 12)", dict(by_class=info))
R["ALL_PASSED"] = bool(allok); R["verifier_sha256"] = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
json.dump(R, open(a.out, "w"), indent=1, sort_keys=True); print("ALL PASSED" if allok else "FAILURES")

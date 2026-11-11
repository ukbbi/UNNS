import json, sys, sympy as sp
from fractions import Fraction
from u1_bnd_lib import fwd, inv, is_edge
x, y = sp.symbols("x y", positive=True)
raw = json.load(open("../data/fibonacci_identities_raw.json"))
F = [0, 1]
while len(F) < 2300: F.append(F[-1] + F[-2])
res = {}
for r, v in raw.items():
    labs = [(s, sp.sympify(N, locals={"x": x, "y": y})) for s, N in v["labels"]]
    fn = [sp.lambdify((x, y), N, "math") for _, N in labs]
    # exact evaluation with Fractions: use sympy Rational substitution
    bad = []; cnt = 0
    for k in range(4, 1800):
        if k % 12 != int(r) % 12: continue
        X, Y = F[k], F[k + 1]; S = X; ok = True
        for (s, N) in labs:
            val = sp.Rational(N.subs({x: X, y: Y}))
            if val.q != 1 or val < 1: ok = False; break
            Nn = int(val)
            try: S2 = fwd(S, Nn) if s == "+" else inv(S, Nn)
            except Exception: ok = False; break
            S = S2
        ok = ok and S == Y; cnt += 1
        if not ok: bad.append(k)
    res[r] = dict(length=v["length"], checked=cnt, failures=bad[:10], nfail=len(bad)); print(r, res[r], flush=True)
json.dump(res, open("/tmp/fibvalidate.json", "w"))

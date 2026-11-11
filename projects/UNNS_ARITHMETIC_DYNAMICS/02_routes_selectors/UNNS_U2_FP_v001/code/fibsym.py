import re, sys, json, sympy as sp
from fractions import Fraction
import fibparam as fp
x, y = sp.symbols("x y", positive=True)
SMALL = {"x": x, "y": y, "x+y": x + y, "y-x": y - x, "2x": 2 * x, "2y": 2 * y}
def parse(e):
    e = e.strip()
    if e.startswith("["):
        a, b = e[1:-1].split("*"); return SMALL[a] * SMALL[b]
    if e.isdigit(): return sp.Integer(int(e))
    m = re.fullmatch(r"\((-?\d+)x([+-]\d+)y([+-]\d+)\)/(\d+)", e)
    a, b, c, d = map(int, m.groups()); return (a * x + b * y + c) / sp.Integer(d)
def Nexpr(sign, lab, S):
    if sign == "+": return sp.cancel(S / parse(lab[2:])) if lab.startswith("S/") else parse(lab)
    if lab.startswith("q=sqrt(S/"): return sp.cancel(sp.sqrt(sp.factor(sp.cancel(S / parse(lab[len("q=sqrt(S/"):-1])))) - 1)
    return sp.cancel(parse(lab[2:]) - 1)
def mv(S, s, N): return sp.cancel(S * (N + 1) ** 2 / N) if s == "+" else sp.cancel(S * N / (N + 1) ** 2)
def resolve(steps, nf):
    S = x; out = []
    for s, l in steps[:nf]: N = Nexpr(s, l, S); out.append((s, N)); S = mv(S, s, N)
    mid = S; S = y; g = []
    for s, l in reversed(steps[nf:]):
        o = "-" if s == "+" else "+"; N = Nexpr(o, l, S); g.append((s, N)); S = mv(S, o, N)
    return out + g[::-1], sp.simplify(S - mid)
if __name__ == "__main__":
    cov = json.load(open("/tmp/fibcover.json"))["24"]; out = {}
    for r in ("4", "7", "10"):
        P, r_ = 24, int(r)
        res = fp.search(24, r_, 7, J=3)
        L, steps, nf = res[0], res[1], res[2]
        ids, resid = resolve(steps, nf)
        out[r] = dict(length=L, nf=nf, raw=steps, labels=[(s, str(sp.factor(N))) for s, N in ids], mid_residual=str(resid))
        print(r, L, nf, out[r]["labels"], "resid", resid, flush=True)
    json.dump(out, open("../data/fibonacci_identities_raw.json", "w"), indent=1)

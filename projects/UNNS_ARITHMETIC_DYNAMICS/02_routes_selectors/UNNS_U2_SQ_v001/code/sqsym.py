"""Resolve found 5-step square paths into symbolic identities and certify them exactly."""
import sys, json, re, sympy as sp
t = sp.symbols("t", positive=True)
nsym = sp.symbols("n", positive=True)

def parse_form(e):
    e = e.strip("[]")
    e = re.sub(r"(\d+)n", r"\1*n", e)
    return sp.sympify(e, locals={"n": nsym})

def Nexpr(sign, lab, S, n_of_t):
    """N expression for a move of given sign and label string, evaluated at current symbolic state S."""
    if sign == "+":
        if lab.startswith("S/"):
            return sp.cancel(S / parse_form(lab[2:]).subs(nsym, n_of_t))
        return sp.cancel(parse_form(lab).subs(nsym, n_of_t))
    if lab.startswith("q=sqrt(S/"):
        e = parse_form(lab[len("q=sqrt(S/"):-1]).subs(nsym, n_of_t)
        r = sp.sqrt(sp.factor(sp.cancel(S / e)))
        return sp.cancel(r - 1)
    return sp.cancel(parse_form(lab[2:]).subs(nsym, n_of_t) - 1)

def move(S, sign, N):
    return sp.cancel(S * (N + 1) ** 2 / N) if sign == "+" else sp.cancel(S * N / (N + 1) ** 2)

def resolve(M, r, steps, nf):
    n = M * t + r
    A = n ** 2; B = (n + 1) ** 2
    S = A; out = []
    for sgn, lab in steps[:nf]:
        N = Nexpr(sgn, lab, S, n); out.append((sgn, N)); S = move(S, sgn, N)
    Smid = S
    S = B; gl = []
    for sgn, lab in reversed(steps[nf:]):
        o = "-" if sgn == "+" else "+"
        N = Nexpr(o, lab, S, n)
        gl.append((sgn, N)); S = move(S, o, N)
    ok = sp.simplify(S - Smid) == 0
    return out + gl[::-1], ok

def is_poly(e):
    try: sp.Poly(sp.expand(e), t); return True
    except Exception: return False

def integer_valued(p):
    p = sp.Poly(sp.expand(p), t); deg = max(p.degree(), 0)
    return all(sp.Rational(p.eval(k)).q == 1 for k in range(deg + 1))

def positive_from(p, t0):
    u = sp.symbols("u", nonnegative=True)
    q = sp.Poly(sp.expand(p.subs(t, t0 + u)), u)
    return all(c >= 0 for c in q.all_coeffs()) and q.eval(0) >= 1

def certify(M, r, steps, t0):
    n = M * t + r; s = sp.expand(n ** 2); rows = []; ok = True; notes = []
    for i, (d, N) in enumerate(steps):
        N = sp.expand(N)
        if not is_poly(N): return dict(ok=False, notes=[f"step {i+1}: label not polynomial"], rows=rows)
        if not (integer_valued(N) and positive_from(N, t0)): ok = False; notes.append(f"step {i+1}: label")
        den = N if d == "+" else (N + 1) ** 2
        q, rem = sp.div(sp.Poly(s, t), sp.Poly(sp.expand(den), t))
        if rem.as_expr() != 0:
            return dict(ok=False, notes=notes + [f"step {i+1}: cofactor not polynomial"], rows=rows)
        k = sp.expand(q.as_expr())
        if not (integer_valued(k) and positive_from(k, t0)): ok = False; notes.append(f"step {i+1}: cofactor")
        nxt = sp.expand(k * (N + 1) ** 2) if d == "+" else sp.expand(k * N)
        rows.append(dict(step=i + 1, dir=d, N=N, k=k, before=s, after=nxt)); s = nxt
    if sp.expand(s - (n + 1) ** 2) != 0: ok = False; notes.append("endpoint")
    return dict(ok=ok, notes=notes, rows=rows)

if __name__ == "__main__":
    res = {}
    for line in open(sys.argv[1]):
        if not line.startswith("["): continue
        M, r, (d, steps, nf), dt = json.loads(line)
        ids, ok = resolve(M, r, steps, nf)
        best = None
        for t0 in range(0, 4):
            if M * t0 + r < 1: continue
            c = certify(M, r, ids, t0)
            if c["ok"]: best = (t0, c); break
        res[r] = dict(length=d, resolved_ok=bool(ok), t0=None if best is None else best[0],
                      steps=[(s, str(sp.factor(N))) for s, N in ids],
                      cert=bool(best), notes=[] if best else certify(M, r, ids, 3).get("notes"))
        print(r, d, ok, res[r]["t0"], res[r]["cert"], res[r]["notes"][:2] if not best else "", flush=True)
    json.dump(res, open(sys.argv[2], "w"), indent=1)

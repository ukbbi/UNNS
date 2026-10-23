#!/usr/bin/env python3
"""FIELD-I v010: class-closure certificate (T51) for the q = 11 carry, g = 6689, seed {80279: 208, 11: 1, 2: 4}.
Not part of field10.py: the class-closure needs about 50 000 machine steps (a transient of ~207 carries x 120 steps plus the class period 120 x 209 = 25 080), i.e. 30-40 minutes.  Run:  python q11_certificate.py > output/q11_certificate.txt
Exact claim certified: the persistent orbit of x0 = L0^2/6689 (L0 = 80279^208 * 11 * 2^4, G(x0) = 6689 exactly) is eventually periodic in the T51 class sense with
gamma-period 120 = 11^2 - 1 and L_(n+120) = 11 L_n, hence x_(n+120) = 121 x_n forever."""
import os, sys, time
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'field10.py')).read()
exec(compile(src[:src.index('# v010 additions.')], 'field10_base', 'exec'), globals())
g = 6689; Es = {80279: 208, 11: 1, 2: 4}; t0 = time.time()
print("seed", Es, "g", g, "exact G(x0) =", Gexact(g, 1, Es), flush=True)
cyc = run_cycle(g, Es, 1, maxn=60000)
print("run_cycle:", cyc[:4] if cyc[0] == 'cycle' else cyc, f"elapsed {time.time() - t0:.1f}s", flush=True)
if cyc[0] == 'cycle':
    pp, rp, ev, uni = reduce_cycle(cyc)
    ok = (pp, rp, uni) == (120, 11, True)
    print(f"{'PASS' if ok else 'FAIL'}: class transient {cyc[1]}, class period {cyc[2]}, gamma-period {pp}, rho = {rp}, uniform {uni}, events (w, r^2) = {ev}: x_(n+{pp}) = {rp}^2 x_n forever")
    sys.exit(0 if ok else 1)
sys.exit(1)

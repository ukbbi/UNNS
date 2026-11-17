"""v008: bounded-forward-label degeneracy test (Theorem S).
Coordinates (proved): B n = Q^2 a N, B (n+1) = Q'^2 a' M,  P | N+1, P' | M+1,
  midpoint law  <=>  a P (Q(N+1)-P) = a' P' (Q'(M+1)-P')   and   Q'^2 a' M - Q^2 a N = B.
Eliminating a:  a' * Num / D1 = B,  D1 = P (X(N+1)-P),  Num = X Y lam - M P^2 Y^2 + N P'^2 X^2,  (X,Y)=(Q,Q'),
  lam = Y M P (N+1) - X N P'(M+1).   Along lam = const, Num is a quadratic in X.  An infinite family with N,M bounded
  needs the X^2-coefficient to vanish AND  c0 + (P/(N+1)) c1 = 0  (then a' c1 = B P (N+1))."""
import sys, os, json
sys.dont_write_bytecode = True
from fractions import Fraction as F
def divisors(m): return [d for d in range(1, m + 1) if m % d == 0]
def analyse(N, M, P, Pp):
    gam = M * P * (N + 1); dl = N * Pp * (M + 1); kap = F(dl, gam)
    # c2 = kap*lam + N Pp^2 - M P^2 kap^2 = 0  -> lam*
    lam = F(M * P * P * kap * kap - N * Pp * Pp) / kap
    # Num(X) with Y = (dl X + lam)/gam :  XY lam - M P^2 Y^2 + N Pp^2 X^2
    a1 = F(dl, gam); b1 = lam / gam                        # Y = a1 X + b1
    c2 = a1 * lam - M * P * P * a1 * a1 + N * Pp * Pp
    c1 = b1 * lam - 2 * M * P * P * a1 * b1
    c0 = -M * P * P * b1 * b1
    return lam, c2, c1, c0
if __name__ == "__main__":
    K = int(sys.argv[1]); rows = []; tested = 0
    for N in range(1, K + 1):
        for M in range(1, K + 1):
            for P in divisors(N + 1):
                for Pp in divisors(M + 1):
                    tested += 1
                    lam, c2, c1, c0 = analyse(N, M, P, Pp)
                    assert c2 == 0
                    ident = (c1 != 0) and (c0 + F(P, N + 1) * c1 == 0)
                    if ident and lam.denominator == 1: rows.append((N, M, P, Pp, str(lam), str(c1), str(c0)))
    print("tested", tested, "tuples; degenerate identity holds with integer lam*:", len(rows)); print(rows[:20])
    json.dump({"K": K, "tested": tested, "degenerate": rows}, open('../results/S2_degenerate.json', 'w'))

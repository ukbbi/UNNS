"""v008 E2: bounded forward labels N,M<=K with q=rho*q0, r=sigma*r0 (rho^2 | n, sigma^2 | n+1, q0,r0 bounded): 'square-root routes'.
Midpoint equation  m A r0^2 (rho q0 - 1) = m' C q0^2 (sigma r0 - 1),  A=M(N+1)^2, C=N(M+1)^2, with n = m rho^2, n+1 = m' sigma^2.
Since gcd(m,m')=1 after cancelling, solve  b sigma^2 - a rho^2 = 1  with a/b = C q0^2 (sigma r0-1) / (A r0^2 (rho q0-1)) in lowest terms. Exact integer search; each hit re-verified with the legal-route definition at B=10^6."""
import sys, os, math, json, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from midpoint_lib import check_witness
B = 10**6
def search(K, Q0, R):
    rho = np.arange(1, R + 1, dtype=object)[:, None]; hits = []
    rr = np.arange(1, R + 1, dtype=np.int64)
    for N in range(1, K + 1):
        for M in range(1, K + 1):
            A = M * (N + 1) ** 2; C = N * (M + 1) ** 2
            for q0 in range(1, Q0 + 1):
                for r0 in range(1, Q0 + 1):
                    # a/b = C q0^2 (s r0 -1) / (A r0^2 (rho q0 -1)); need b s^2 - a rho^2 = 1.  cross-multiply:  A r0^2 (rho q0-1) * (s^2) * ?  -> use exact ints below
                    for r_ in range(1, R + 1):
                        den = A * r0 * r0 * (r_ * q0 - 1)
                        if den <= 0: continue
                        s = rr
                        num = C * q0 * q0 * (s * r0 - 1)
                        g = np.gcd(num, den)
                        a = num // g; b = den // g
                        ok = np.nonzero(b * s * s - a * r_ * r_ == 1)[0]
                        for i in ok:
                            sg = int(s[i]); aa = int(a[i]); bb = int(b[i]); n = aa * r_ * r_
                            if n >= 2: hits.append((n, N, M, q0 * r_, r0 * sg, q0, r0, r_, sg))
    return hits
if __name__ == "__main__":
    K, Q0, R = map(int, sys.argv[1:4]); t = time.time(); h = search(K, Q0, R)
    legal = []
    for (n, N, M, q, r, q0, r0, rho, sg) in h:
        ok = check_witness(B, n, N, q, M, r)
        if all(ok.values()): legal.append((n, N, M, q, r))
    print("candidate solutions", len(h), "fully legal at B=10^6:", len(legal), round(time.time() - t))
    for x in sorted(legal)[:40]: print(x)
    json.dump({"K": K, "Q0": Q0, "R": R, "candidates": len(h), "legal": legal}, open('../results/S1_sqrt_routes.json', 'w'))

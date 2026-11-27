"""Engine A: backward ancestry enumeration (standard library only; independent of Engine B).

H_{k+1}(n) = sum over labels b with p_b | n of H_k(n*q_b/p_b)           (nesting: n(m-1)/m^2)
H[n] is a packed integer: field k (WIDTH bits) = H_k(n).
Because every predecessor is at most n/lam (lam = least multiplier > 1), n is processed in blocks
[L, ceil(lam*L)) whose predecessors all lie below L.
"""
import argparse
from math import ceil

WIDTH = 40
MASK = (1 << WIDTH) - 1


def nesting_pairs(X, degree=2):
    out, m = [], 2
    while m ** degree <= X:
        out.append((m ** degree, m - 1))      # (p, q): x = n*q/p
        m += 1
    return out


def ancestry_census(X, pairs=None):
    """Return list H with H[n] packed H_k(n), 1 <= n <= X (H[0] unused)."""
    if pairs is None:
        pairs = nesting_pairs(X)
    pairs = sorted(pairs)                       # by p
    H = [1] * (X + 1)
    H[0] = 0
    if not pairs:
        return H
    lam = min(p / q for p, q in pairs)
    L = 1
    while L <= X:
        R = min(X + 1, max(L + 1, int(ceil(L * lam - 1e-9))))
        for p, q in pairs:
            if p >= R:
                break
            first = ((L + p - 1) // p) * p
            j = first // p
            for n in range(first, R, p):
                H[n] += H[j * q] << WIDTH
                j += 1
        L = R
    return H


def unpack(v):
    out = []
    while v:
        out.append(v & MASK)
        v >>= WIDTH
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="ancestry census")
    ap.add_argument("X", type=int)
    args = ap.parse_args()
    H = ancestry_census(args.X)
    print("H(n) for n = 4, 9, 36:", [sum(unpack(H[n])) for n in (4, 9, 36) if n <= args.X])
    print("sum H(n), n <= X:", sum(sum(unpack(v)) for v in H))

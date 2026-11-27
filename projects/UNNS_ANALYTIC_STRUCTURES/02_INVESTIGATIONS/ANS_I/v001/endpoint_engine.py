"""Engine B: forward enumeration of minimal history endpoints (standard library only).

A grammar is a list of labels (b, p, q): T_b(x) = p*x/q, legal iff q | x, gcd(p,q)=1, p > q.
Recurrence (ANS-T03):  E(empty)=1,  E(wb) = p*E(w)/gcd(E(w), q).
Depth-resolved multiplicities are packed into one integer: field k (WIDTH bits) = a_k(n).
"""
from math import gcd, isqrt
import argparse, csv

WIDTH = 40
MASK = (1 << WIDTH) - 1


def nesting_labels(X, degree=2):
    """All labels of the grammar x -> x(N+1)^degree/N whose endpoint factor fits under X."""
    out, N = [], 1
    while (N + 1) ** degree <= X:
        out.append((N, (N + 1) ** degree, N))
        N += 1
    return out


def endpoint_census(X, labels=None):
    """Return {n: packed a_k(n)} for all minimal endpoints n <= X."""
    if labels is None:
        labels = nesting_labels(X)
    labs = sorted(labels, key=lambda l: l[1] / l[2])          # ascending multiplier
    pq = [(p, q) for _, p, q in labs if p <= X]
    a = {1: 1}
    stack = [(1, 0)]
    while stack:
        E, k = stack.pop()
        unit = 1 << (WIDTH * (k + 1))
        for p, q in pq:
            if E * p > X * q:          # E(wb) >= (p/q) E(w): no later label can fit
                break
            F = p * (E // gcd(E, q))
            if F <= X:
                a[F] = a.get(F, 0) + unit
                stack.append((F, k + 1))
    return a


def unpack(v):
    out = []
    while v:
        out.append(v & MASK)
        v >>= WIDTH
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="minimal-endpoint census")
    ap.add_argument("X", type=int)
    ap.add_argument("--csv")
    args = ap.parse_args()
    a = endpoint_census(args.X)
    print("distinct minimal endpoints", len(a), "words", sum(sum(unpack(v)) for v in a.values()))
    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["n", "depth", "a_k"])
            for n in sorted(a):
                for k, c in enumerate(unpack(a[n])):
                    if c:
                        w.writerow([n, k, c])

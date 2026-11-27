"""Independent Moebius inversion a_k = mu * H_k and comparison of the two engines (ANS-T02)."""
import argparse
from ancestry_engine import ancestry_census
from endpoint_engine import endpoint_census


def primes_upto(X):
    s = bytearray([1]) * (X + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, int(X ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(range(i * i, X + 1, i)))
    return [i for i in range(X + 1) if s[i]]


def mobius_transform(H):
    """Apply product over primes of (1 - p^{-s}) to the coefficient list (exact, linear in H)."""
    a = list(H)
    X = len(a) - 1
    for p in primes_upto(X):
        for j in range(X // p, 0, -1):
            a[j * p] -= a[j]
    return a


def mu(n):
    r, d = 1, 2
    while d * d <= n:
        if n % d == 0:
            n //= d
            if n % d == 0:
                return 0
            r = -r
        d += 1
    return -r if n > 1 else r


def direct_inversion(H, n):
    """a(n) = sum_{d|n} mu(d) H(n/d), evaluated from the definition (small n)."""
    return sum(mu(d) * H[n // d] for d in range(1, n + 1) if n % d == 0)


def compare(X, H=None, a=None):
    H = H if H is not None else ancestry_census(X)
    a = a if a is not None else endpoint_census(X)
    inv = mobius_transform(H)
    bad = [n for n in range(1, X + 1) if inv[n] != a.get(n, 0)]
    return bad


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("X", type=int, nargs="?", default=100000)
    args = ap.parse_args()
    bad = compare(args.X)
    print("X =", args.X, "mismatches between mu*H and forward a_k:", len(bad), bad[:10])
    raise SystemExit(1 if bad else 0)

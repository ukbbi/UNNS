"""Exact, standard-library operators for Maxwell/UNNS induction comparison.

All integer Fourier supports are finite computational witnesses. The accompanying
proofs in theory/THEOREMS.md cover the infinite exact eigenmode case separately.
"""
from fractions import Fraction
from functools import reduce
from math import gcd


def content(x):
    """GCD of nonzero integer Fourier indices with nonzero coefficients."""
    if not x:
        return 0
    return reduce(gcd, (abs(m) for m, c in x.items() if c != 0), 0)


def multiplier(N):
    if not isinstance(N, int) or N < 1:
        raise ValueError('N must be positive integer')
    return Fraction((N+1)**2, N)


def strict_step(x, N):
    """Partial whole-field map: undefined (None) if any occupied index fails."""
    multiplier(N)
    if not x:
        return None
    if any((m % N) != 0 for m, c in x.items() if c != 0):
        return None
    a = (N+1)**2
    return {(m//N)*a: c for m, c in x.items() if c != 0}


def component_step(x, N):
    """Declared lossy componentwise map Q_N followed by D_N."""
    multiplier(N)
    a = (N+1)**2
    return {(m//N)*a: c for m, c in x.items() if c != 0 and m % N == 0}


def E_step(x, N, q):
    """Exactly v007 rule E: Bloch-class projector followed by D_N."""
    if not isinstance(q, int) or q < 1:
        raise ValueError('q positive integer')
    multiplier(N)
    if q % N:
        return {}
    a = (N+1)**2
    return {(m//N)*a: c for m, c in x.items()
            if c != 0 and gcd(m % q, q) % N == 0}


def walk(x, word, mode, q=6):
    x = dict(x)
    path = [content(x)]
    for N in word:
        if mode == 'strict':
            x = strict_step(x, N)
        elif mode == 'component':
            x = component_step(x, N)
        elif mode == 'E':
            x = E_step(x, N, q)
        else:
            raise ValueError(mode)
        if x is None:
            return None, path
        path.append(content(x))
        if not x:
            return {}, path
    return x, path


def sample_fourier():
    """Finite exact support witness from Bloch class kappa=0 modulo q=6.
    Coefficients are arbitrary nonzero rational probes, not an exact eigenstate.
    The spectral test reconstructs a numerical eigenstate of the SAME medium.
    """
    return {
        -18: Fraction(1, 37), -12: Fraction(1, 13), -6: Fraction(1, 2),
          6: Fraction(1, 2),  12: Fraction(1, 13), 18: Fraction(1, 37),
    }


def exact_curvature_mismatch(delta, q, N):
    """epsilon(rz)''(0)-epsilon(z)''(0); exact no-go certificate."""
    r = multiplier(N)
    return -2 * Fraction(delta) * q * q * (r*r-1)

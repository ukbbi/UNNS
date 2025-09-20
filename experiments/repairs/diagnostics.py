import numpy as np

def residues(u, coeffs):
    """
    Compute local echo residues for UNNS sequence.
    r[i] = predicted value - actual value
    """
    r_len = len(coeffs)
    r = np.zeros_like(u, dtype=float)
    for i in range(r_len, len(u)):
        pred = sum(coeffs[j] * u[i-j-1] for j in range(r_len))
        r[i] = pred - u[i]
    return r

def growth_factor(u):
    """Compute local growth factor |u[n+1]|/|u[n]|."""
    return np.array([abs(u[i+1]/u[i]) if u[i] != 0 else 0 for i in range(len(u)-1)])

def upi(D, R, M, S):
    """Compute UNNS Paradox Index (UPI)."""
    return (D * R) / (M + S + 1e-9)

def ring_violation_score(coeffs, ring="gaussian"):
    """
    Check how far coefficients are from desired ring.
    Currently supports 'gaussian' (nearest Z[i]).
    """
    if ring == "gaussian":
        return [abs(c - (round(c.real) + 1j*round(c.imag))) for c in coeffs]
    return [0.0 for _ in coeffs]

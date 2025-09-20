import numpy as np

def proofreading(u, coeffs, i, eta=0.5):
    """Proofread single index i using recurrence prediction."""
    r_len = len(coeffs)
    if i < r_len: return u
    pred = sum(coeffs[j] * u[i-j-1] for j in range(r_len))
    u[i] = (1-eta) * u[i] + eta * pred
    return u

def excision_refit(u, coeffs, a, b):
    """
    Excision + refit for indices [a,b].
    Replace corrupted region using local recurrence.
    """
    r_len = len(coeffs)
    for i in range(a, b+1):
        if i >= r_len:
            pred = sum(coeffs[j] * u[i-j-1] for j in range(r_len))
            u[i] = pred
    return u

def project_gaussian(z):
    """Project scalar to nearest Gaussian integer."""
    return round(z.real) + 1j*round(z.imag)

def mismatch_projection(coeffs):
    """Project coefficients to Gaussian integers."""
    return [project_gaussian(c) for c in coeffs]

def global_renormalization(u):
    """Normalize sequence amplitude."""
    norm = np.sqrt(np.mean(np.abs(u)**2))
    if norm == 0: return u
    return u / norm

def homologous_replacement(u, template, a, b):
    """
    Replace segment [a,b] with scaled template segment.
    """
    seg = template[a:b+1]
    if len(seg) == 0: return u
    scale = np.mean(u[a:b+1]) / (np.mean(seg)+1e-9)
    u[a:b+1] = scale * seg
    return u

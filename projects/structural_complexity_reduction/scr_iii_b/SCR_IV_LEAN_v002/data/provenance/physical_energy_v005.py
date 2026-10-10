#!/usr/bin/env python3
"""SCR-III-B PREFLIGHT_v005 -- independent physical energy evaluator (pure Python, no dependencies).

Selected reference model: Dryad SPMMC-SSI-Unix-v1.00 (all-pair dumbbell interaction), template parameters.
Evidence level of this file: SOURCE-DERIVED INDEPENDENT PYTHON CALCULATION. It is not the original code.

Conventions (each tested in validate_v005.py against verbatim original-source functions):
  * state s_i = +1 means the moment points along the island unit vector u_i (README, Dipole_Unit_Vector).
  * dumbbell: charges +-q s_i at r_i +- (l/3) u_i, q = (pi/4) M(T) w h   (derived; tested by test E3)
  * pair energy  U_ij = (mu0/4pi) q^2 sum_{a,c=+-1} a c / |r_i + a(l/3)u_i - r_j - c(l/3)u_j| * s_i s_j
  * H(s) = sum_{i<j} U_ij  = A(T) * sum_{i<j} K_ij s_i s_j,  A(T) = kappa*mu0*M(T)^2*V/2,  V=(pi/6) l w h
  * K_ij = (3/16)(w h)/(l d) * [1/r++ + 1/r-- - 1/r+- - 1/r-+]  (source formula, transcribed)
  * single flip:  dE_i = -2 A(T) s_i h_i,  h_i = sum_j K_ij s_j   (= source reversal-exponent update)
  * M(T) = M0 (1 - T/Tc)^beta, valid 0 <= T < Tc only (no extrapolation above Tc).
Energies: joules ('_J'), normalized ('_norm' = H/A, dimensionless), and kT units on request.
H has a natural zero (non-interacting islands); no arbitrary additive offset is introduced (B(T)=0).
"""
from math import sqrt, pi
from itertools import combinations

MU0 = 1.25663706212e-6      # H/m  (CODATA 2018)
KB = 1.380649e-23           # J/K  (exact, SI 2019)
SOURCE_MU0_OVER_KB_CONST = 0.910179   # K, as hard-coded (rounded) in original source line ~1527

TEMPLATE = dict(a=260.0, l=160.0, w=60.0, h=15.0,             # nm  (SPMMC v1.00 template defaults)
                M0=7.9e5, beta=0.5, Tc=820.0, kappa=1.0)       # A/m, -, K, -


class Island:
    __slots__ = ("x", "y", "ux", "uy")

    def __init__(self, x, y, ux, uy):
        self.x, self.y, self.ux, self.uy = x, y, ux, uy


def source_geometry(L, a=TEMPLATE["a"], y_down=True):
    """Finite free-boundary patch exactly as SPMMC initialize_dipole_system builds it.
    Order: for row,col: horizontal then vertical; then left-dangling horizontals; then top-dangling verticals.
    y_down=True : source convention (vertical unit vector (0,-1), rows go to -y).
    y_down=False: mirror image (y -> -y incl. unit vectors), physically equivalent."""
    sg = 1.0 if y_down else -1.0
    isl = []
    for row in range(L):
        for col in range(L):
            isl.append(Island(a * (col + 0.5), sg * a * (-row), 1.0, 0.0))
            isl.append(Island(a * col, sg * a * (-row - 0.5), 0.0, sg * -1.0))
    for row in range(L):
        isl.append(Island(a * (-1 + 0.5), sg * a * (-row), 1.0, 0.0))
    for col in range(L):
        isl.append(Island(a * col, sg * a * (-(-1) - 0.5), 0.0, sg * -1.0))
    return isl


def vertex_positions(L, a=TEMPLATE["a"], y_down=True):
    sg = 1.0 if y_down else -1.0
    return [(a * col, sg * a * (-row)) for row in range(L) for col in range(L)]


def incident_islands(isl, vpos, a=TEMPLATE["a"]):
    """Indices of the four islands at each vertex (geometric: centre within a/2 of the vertex)."""
    out = []
    for vx, vy in vpos:
        idx = [i for i, p in enumerate(isl)
               if 1e-9 < sqrt((p.x - vx) ** 2 + (p.y - vy) ** 2) < 0.5 * a + 1e-9]
        out.append(idx)
    return out


def ice_ok_geometric(state, isl, vpos, a=TEMPLATE["a"]):
    """2-in/2-out at every vertex by geometry: arrow s*u points toward the vertex => 'in'.
    Independent of the source's ENWS bit table."""
    for v, idx in zip(vpos, incident_islands(isl, vpos, a)):
        n_in = 0
        for i in idx:
            p = isl[i]
            toward = (v[0] - p.x) * (state[i] * p.ux) + (v[1] - p.y) * (state[i] * p.uy)
            n_in += 1 if toward > 0 else 0
        if len(idx) != 4 or n_in != 2:
            return False
    return True


def vertex_charges_geometric(state, isl, vpos, a=TEMPLATE["a"]):
    """Net 'in minus out' per vertex (0 for 2-in/2-out)."""
    res = []
    for v, idx in zip(vpos, incident_islands(isl, vpos, a)):
        q = 0
        for i in idx:
            p = isl[i]
            toward = (v[0] - p.x) * (state[i] * p.ux) + (v[1] - p.y) * (state[i] * p.uy)
            q += 1 if toward > 0 else -1
        res.append(q)
    return res


def K_pair(ei, ej, l=TEMPLATE["l"], w=TEMPLATE["w"], h=TEMPLATE["h"]):
    """Normalized coupling, transcribed from the source formula (reference = ei, neighbour = ej)."""
    rx, ry = ej.x - ei.x, ej.y - ei.y
    d = sqrt(rx * rx + ry * ry)
    if d == 0.0:
        raise ValueError("coincident centres")

    def inv(a_, c_):
        sq = (1.0 + (l / (3 * d)) ** 2 + (l / (3 * d)) ** 2
              + (2.0 / 3.0) * c_ * l * (rx * ej.ux + ry * ej.uy) / d ** 2
              - (2.0 / 3.0) * a_ * l * (rx * ei.ux + ry * ei.uy) / d ** 2
              - (2.0 / 9.0) * a_ * c_ * l * l * (ei.ux * ej.ux + ei.uy * ej.uy) / d ** 2)
        return 1.0 / sqrt(sq)
    return (3.0 / 16.0) * (w * h) / (l * d) * (inv(1, 1) + inv(-1, -1) - inv(1, -1) - inv(-1, 1))


def K_pairs(isl, **kw):
    """Upper-triangle list [(i,j,K_ij)], all pairs (no cutoff) -- SPMMC production setting."""
    return [(i, j, K_pair(isl[i], isl[j], **kw)) for i, j in combinations(range(len(isl)), 2)]


# ---------- physical (charge-based) pair energy, independent of the K normalisation ----------
def moment_M(T, M0=TEMPLATE["M0"], beta=TEMPLATE["beta"], Tc=TEMPLATE["Tc"]):
    if not (0.0 <= T < Tc):
        raise ValueError("T=%r outside the supported domain 0 <= T < Tc=%r (no extrapolation)" % (T, Tc))
    return M0 * (1.0 - T / Tc) ** beta


def island_volume_m3(l=TEMPLATE["l"], w=TEMPLATE["w"], h=TEMPLATE["h"]):
    return (pi / 6.0) * l * w * h * 1e-27


def A_joule(T, kappa=TEMPLATE["kappa"], **kw):
    """Energy scale A(T) = kappa * mu0 * M(T)^2 * V / 2  [J]  (= t0 * kB * Tc * (1-t)^(2 beta))."""
    p = {k: kw.get(k, TEMPLATE[k]) for k in ("l", "w", "h", "M0", "beta", "Tc")}
    return kappa * MU0 * moment_M(T, p["M0"], p["beta"], p["Tc"]) ** 2 * island_volume_m3(p["l"], p["w"], p["h"]) / 2.0


def pair_energy_charge_model_J(ei, ej, T, l=TEMPLATE["l"], w=TEMPLATE["w"], h=TEMPLATE["h"],
                               M0=TEMPLATE["M0"], beta=TEMPLATE["beta"], Tc=TEMPLATE["Tc"]):
    """Coulomb energy (s_i = s_j = +1) of two dumbbells, computed from explicit charge positions in metres."""
    q = (pi / 4.0) * moment_M(T, M0, beta, Tc) * (w * 1e-9) * (h * 1e-9)
    total = 0.0
    for a_ in (1, -1):
        for c_ in (1, -1):
            px = (ei.x + a_ * (l / 3.0) * ei.ux) - (ej.x + c_ * (l / 3.0) * ej.ux)
            py = (ei.y + a_ * (l / 3.0) * ei.uy) - (ej.y + c_ * (l / 3.0) * ej.uy)
            r = sqrt(px * px + py * py) * 1e-9
            total += a_ * c_ / r
    return (MU0 / (4.0 * pi)) * q * q * total


# ---------- state encoding and energies ----------
def decode(sid, n):
    """Deterministic encoding: bit i of integer sid = 1 <-> s_i = +1."""
    return [1 if (sid >> i) & 1 else -1 for i in range(n)]


def encode(state):
    return sum(1 << i for i, s in enumerate(state) if s > 0)


def energy_norm(state, pairs):
    """H/A = sum_{i<j} K_ij s_i s_j   (SOURCE-DERIVED SIGN: +)."""
    return sum(k * state[i] * state[j] for i, j, k in pairs)


def energy_norm_legacy_v004(state, pairs):
    """v001-v004 sign convention (-sum K s s). Kept ONLY for regression comparison; contradicts the source."""
    return -energy_norm(state, pairs)


def energy_J(state, pairs, T, **kw):
    return A_joule(T, **kw) * energy_norm(state, pairs)


def pair_contributions_J(state, pairs, T, **kw):
    A = A_joule(T, **kw)
    return [(i, j, A * k * state[i] * state[j]) for i, j, k in pairs]


def local_fields(state, pairs, n):
    h = [0.0] * n
    for i, j, k in pairs:
        h[i] += k * state[j]
        h[j] += k * state[i]
    return h


def flip_delta_norm(state, k_idx, h):
    """H/A change when spin k flips: -2 s_k h_k (single-counted energy)."""
    return -2.0 * state[k_idx] * h[k_idx]


def flip_delta_J(state, k_idx, h, T, **kw):
    return A_joule(T, **kw) * flip_delta_norm(state, k_idx, h)


def spearman(x, y):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for t in range(i, j + 1):
                r[order[t]] = (i + j) / 2.0
            i = j + 1
        return r
    rx, ry = ranks(x), ranks(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else float("nan")


def rel_err(a, b, atol):
    return abs(a - b) / max(abs(a), abs(b), atol)

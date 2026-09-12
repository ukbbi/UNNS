from __future__ import annotations

import math
import numpy as np


def block_average_velocity(velocity: np.ndarray, factor: int) -> np.ndarray:
    """
    Exact non-overlapping box coarse-graining.

    Input shape: [z, y, x, 3]
    Output shape: [z/f, y/f, x/f, 3]
    """
    v = np.asarray(velocity)
    if v.ndim != 4 or v.shape[-1] != 3:
        raise ValueError(f"Expected velocity [z,y,x,3], got {v.shape}")
    if factor < 1:
        raise ValueError("factor must be >=1")
    if factor == 1:
        return v
    nz, ny, nx, nc = v.shape
    if nz % factor or ny % factor or nx % factor:
        raise ValueError(f"Grid {v.shape[:3]} not divisible by factor={factor}")
    out = v.reshape(
        nz // factor, factor,
        ny // factor, factor,
        nx // factor, factor,
        nc
    ).mean(axis=(1, 3, 5), dtype=np.float32)
    return np.asarray(out, dtype=np.float32)


def _grad(a: np.ndarray, spacing: float, axis: int) -> np.ndarray:
    return np.asarray(
        np.gradient(a, spacing, axis=axis, edge_order=2),
        dtype=np.float32
    )


def physical_fields(velocity: np.ndarray, spacing: float, viscosity: float):
    """
    Boundary-safe Cartesian derivatives for HDF5 order [z,y,x,component].

    Components are interpreted as [u_x,u_y,u_z].

    Computes:
      divergence
      Q = 1/2[(tr A)^2 - tr(A^2)]
      enstrophy = |omega|^2 / 2
      strain_sq = sum_ij S_ij^2 = |omega|^2/2 - 2Q
      dissipation_proxy = 2 nu strain_sq
      helicity = u dot omega

    No periodic wrap-around is used.
    """
    v = np.asarray(velocity, dtype=np.float32)
    if v.ndim != 4 or v.shape[-1] != 3:
        raise ValueError(f"Expected [z,y,x,3], got {v.shape}")
    if min(v.shape[:3]) < 3:
        raise ValueError("Need >=3 cells per spatial dimension for edge_order=2")

    u = v[..., 0]
    vv = v[..., 1]
    w = v[..., 2]

    # Diagonal gradients.
    du_dx = _grad(u, spacing, axis=2)
    dv_dy = _grad(vv, spacing, axis=1)
    dw_dz = _grad(w, spacing, axis=0)

    divergence = du_dx + dv_dy + dw_dz
    tr_a2 = du_dx * du_dx + dv_dy * dv_dy + dw_dz * dw_dz

    enstrophy = np.zeros(u.shape, dtype=np.float32)
    helicity = np.zeros(u.shape, dtype=np.float32)

    # xy pair -> omega_z
    du_dy = _grad(u, spacing, axis=1)
    dv_dx = _grad(vv, spacing, axis=2)
    tr_a2 += 2.0 * du_dy * dv_dx
    omega_z = dv_dx - du_dy
    enstrophy += 0.5 * omega_z * omega_z
    helicity += w * omega_z
    del du_dy, dv_dx, omega_z

    # xz pair -> omega_y
    du_dz = _grad(u, spacing, axis=0)
    dw_dx = _grad(w, spacing, axis=2)
    tr_a2 += 2.0 * du_dz * dw_dx
    omega_y = du_dz - dw_dx
    enstrophy += 0.5 * omega_y * omega_y
    helicity += vv * omega_y
    del du_dz, dw_dx, omega_y

    # yz pair -> omega_x
    dv_dz = _grad(vv, spacing, axis=0)
    dw_dy = _grad(w, spacing, axis=1)
    tr_a2 += 2.0 * dv_dz * dw_dy
    omega_x = dw_dy - dv_dz
    enstrophy += 0.5 * omega_x * omega_x
    helicity += u * omega_x
    del dv_dz, dw_dy, omega_x

    q = 0.5 * (divergence * divergence - tr_a2)

    # Because ||Omega||^2 = |omega|^2/2 = enstrophy:
    # Q = 1/2(||Omega||^2 - ||S||^2)
    strain_sq = enstrophy - 2.0 * q
    # Numerical noise may produce tiny negative values.
    strain_sq = np.maximum(strain_sq, 0.0).astype(np.float32, copy=False)
    dissipation_proxy = (2.0 * viscosity * strain_sq).astype(np.float32, copy=False)

    return {
        "divergence": np.asarray(divergence, dtype=np.float32),
        "Q": np.asarray(q, dtype=np.float32),
        "enstrophy": np.asarray(enstrophy, dtype=np.float32),
        "strain_sq": strain_sq,
        "dissipation_proxy": dissipation_proxy,
        "helicity": np.asarray(helicity, dtype=np.float32),
    }


def interior_slices(shape, margin_cells: int):
    if margin_cells < 0:
        raise ValueError("margin_cells must be >=0")
    if margin_cells == 0:
        return tuple(slice(None) for _ in shape)
    if any(n <= 2 * margin_cells + 2 for n in shape):
        raise ValueError(
            f"Margin {margin_cells} too large for shape {shape}; "
            "need a nontrivial retained interior."
        )
    return tuple(slice(margin_cells, n - margin_cells) for n in shape)


def physical_stats(velocity, fields, margin_cells: int):
    sl = interior_slices(velocity.shape[:3], margin_cells)
    vint = velocity[sl + (slice(None),)]
    q = fields["Q"][sl]
    ens = fields["enstrophy"][sl]
    div = fields["divergence"][sl]
    strain_sq = fields["strain_sq"][sl]
    hel = fields["helicity"][sl]

    speed2 = np.sum(vint * vint, axis=-1, dtype=np.float64)
    return {
        "kinetic_energy_local": float(0.5 * np.mean(speed2)),
        "divergence_mean": float(np.mean(div, dtype=np.float64)),
        "divergence_rms": float(np.sqrt(np.mean(div.astype(np.float64) ** 2))),
        "q_mean": float(np.mean(q, dtype=np.float64)),
        "q_rms": float(np.sqrt(np.mean(q.astype(np.float64) ** 2))),
        "q_positive_fraction": float(np.mean(q > 0)),
        "enstrophy_mean": float(np.mean(ens, dtype=np.float64)),
        "strain_sq_mean": float(np.mean(strain_sq, dtype=np.float64)),
        "helicity_mean": float(np.mean(hel, dtype=np.float64)),
    }

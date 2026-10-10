# Frozen G1→G4 Filter

No gate definition changes from v002.

- G1: `curvature_method == "turning_angle"`
- G2: `delta_kappa > 0.05`
- G3: bifurcation-capable with pinned soft band `s_lo=0.08`, `s_hi=0.10`, `T_min=0.70`
- G4: `locality_score < 0.10`

Order is frozen: `G1 → G2 → G3 → G4` with early termination for cost accounting.

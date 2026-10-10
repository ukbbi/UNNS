# Frozen structural gates

The v002 filter is unchanged from v001 and from the pinned P4 baseline profile.

- **G1 — Geometric curvature consistency:** `curvature_method == "turning_angle"`.
- **G2 — Baseline separability:** `delta_kappa > 0.05`.
- **G3 — Bifurcation capability:** bifurcation required; sharpness ≥0.10 requires valid temporal signature; sharpness <0.08 fails; the 0.08–0.10 band passes only with temporal quality ≥0.70.
- **G4 — Locality consistency:** `locality_score < 0.10`.

Execution order is permanently G1→G2→G3→G4. Early termination is allowed only after a gate fails. Rejected candidates are retained in the negative-space export.

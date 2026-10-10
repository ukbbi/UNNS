# SCR-I v003 Design Rationale

v003 keeps the generator, independent viability oracle and G1→G4 filter frozen. It changes only the target-preservation unit from candidate identity to target-basin/class geometry.

The basin geometry is taken from the pinned LIII clustering rule: normalized `(gamma0, beta, d, kmax, locality)` coordinates, radius 0.25, minimum 20 neighbors.

Design-only audit requires complete basin representation, ≥20 target survivors per basin, ≥95% within-basin radius coverage, centroid drift ≤0.125, and full adequately-populated phenotype-stratum coverage.

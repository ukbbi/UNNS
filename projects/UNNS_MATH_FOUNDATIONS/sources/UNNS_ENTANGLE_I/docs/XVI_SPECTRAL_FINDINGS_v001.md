# XVI Source-Locked Spectral Conditioning — Findings v001

## Verified technical result

1. The user-uploaded `XVI_INVARIANTS_AUDIT_v001.json` is frozen byte-for-byte (SHA-256 `a0653783748355b06a96c86eb3b12fd07845c5976273a6bc8c7fcd0a40f8651e`). The earlier verdict remains **INVARIANT_FIDELITY_NOT_CERTIFIED**.
2. The original Chamber XVI source was executed directly on new random-initialized τ-fields in an isolated Node VM; no canonical HTML edits were made. Four raw field snapshots are included (N=64 and 128, seed 41, steps 0 and 24, zero evolution noise). Original-JS per-shell powers, p, and R² are stored along with the arrays.
3. On precisely those new raw fields the source all-bin p values are **−3.8416, −3.8477, −3.8305, −3.8289**, and the independently calculated NumPy values agree to ~10⁻¹³ or better. This is **a source-parity result on new fields**, not a reproduction of the older exported p≈−3.0 from different fields and parameters.
4. Separate fixed-policy conditioned fits on the same new fields give **−3.7551, −3.8395, −3.7744, −3.8725**. Their R² exceed 0.99 and are reproducible between the two implementations. This establishes numerical support/fit consistency for these snapshots only, not uniqueness or physical significance of that negative slope.
5. **The source +2.28 target fails.** We have not changed its sign, threshold, or the earlier certification verdict.

## Adversarial interpretation controls

The original diagnostic fits the FFT of the Laplacian of τ. Therefore white-noise τ, with approximately flat τ Fourier power, produces κ Fourier power ∝k⁴ and an expected fitted p≈−4. On deliberately independent white-noise null fields the conditioned p is approximately −3.78 (64²) and −3.83 (128²), with high R². Thus a precise negative slope near −4 can arise from the **known differential operator and trivial broadband input**, not necessarily a UNNS spectral invariant.

A generated control with an **imposed** κ power law p=+2.28 is recovered as approximately +2.267 (64²) and +2.201 (128²) with R² above 0.97. The narrowband control is correctly rejected for insufficient supported bins. These positives validate the sensitivity of the conditioned diagnostic in its tested scope, **not** the physical source hypothesis.

## Limitations and open gates

- The four historic `LPB-Closure` reports still lack raw τ arrays. The exact original p and R² in those files cannot be recomputed; P6 is BLOCKED.
- The original JS engine's `captureSpectrum` source fit is unchanged and included; the conditioned bin selection is a different metric, labeled diagnostic-only.
- A fine log fit has no physical meaning unless the power spectrum has independently identified source physics and survives null controls, grid/seed robustness and fidelity checks. A white-noise null also yields a high R² negative slope.
- Source runs include only one original-engine seed, two grids and two snapshots; no claim of general convergence or invariant preservation.
- No quantum event measure or Born rule is derived.

**Research verdict:** `SPECTRAL_CONDITIONING_AUDIT_ONLY`. The source computations are now reproducible on new raw fields, but **the original structural invariant remains uncertified**. A subsequent experiment should source-export raw fields for the historical parameter combinations, collect many seeds, and test whether any residual spectral feature survives the explicit derivative/white-noise null.

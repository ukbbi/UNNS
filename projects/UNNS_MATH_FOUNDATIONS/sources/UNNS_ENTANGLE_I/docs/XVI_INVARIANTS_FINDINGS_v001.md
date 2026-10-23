# XVI Invariant Fidelity — Executed findings v001

**Verdict: `INVARIANT_FIDELITY_NOT_CERTIFIED`.** All baseline hashes pass. The original Chamber XVI is unmodified; the previous negative τ certification remains frozen, and the grid-scaled candidate is still a `LIMITED_PHYSICAL_GEOMETRY_WITNESS` only.

## Original source and exports

The original browser UI searches μ only in the narrow interval `[1.600,1.640]`. Source validation aims at `p=+2.28`, `R²≥0.95`, `μ≈1.618`. Yet its four exported post-run spectra have **negative slopes p**: −3.3469 (64), −2.9578 (128), −2.9478 (128) and −2.9893 (256). All four source exports mark `C_invariants=false`. These are different parameter settings and not a controlled grid series. **No raw τ arrays are exported**, so individual export metrics cannot be independently replayed from their JSON files.

## Direct original-JS fidelity witness

On the same 64² arrays, running the original HTML class directly reproduces the Python source-formula port's μ★ and H_r to ~1e−15; the p/R² values differ measurably due to the combination of different FFT roundoff and a log fit including bins of nearly zero power. For the seeded smooth initial field, original JS p=8.037277 vs NumPy p=7.987854, a difference of ~0.049424; R² differs by ~0.002418. The candidate final field also shows nonzero p/R² differences. These mismatches are explicitly **FAILS**, not a source fidelity certificate.

## New candidate versus ablations

- Original candidate's final standard deviation retains ~89.2–89.5% of initial level across seeds 41/137 and three grids.
- No-closure advection/diffusion typically retains ~93% and diffusion-only also ~93%. Retention by itself does not demonstrate uniquely UNNS structure.
- Removing closure changes the final field by ~1.7–1.8% relative L² across the tested seeds/grids: a reproducible nonzero *numerical effect*.
- Candidate source-formula p is ~25.4–25.6 on 64², ~20.4 on 128², ~12.9 on 256²; the original source fit R² is typically 0.63–0.82, below 0.95. These values vary strongly with grid and fail p=+2.28. Most fitted radial bins contain less than 10^-12 of the peak bin power, so the slope is not physically reliable.
- μ★ often reaches the search window's upper endpoint for seed 137. It does not independently demonstrate a φ attractor; it also shifts with pixel-grid sampling.
- New candidate's tail histogram entropy changes are less than 10^-3 relative, but both controls exhibit comparable stationarity. The source's histogram choice is self-normalizing to the field's varying support; stationary H_r under this convention is not sufficient for meaningful structural preservation.

## Decision

I0/I1 and finite observation/ablation gates pass. Source-export replay I2 is BLOCKED; strict JS spectral parity I12 FAILS; I6/7/8 FAIL; invariant distinctness I11 is NOT DEMONSTRATED. The original non-convergent τ evolution remains uncertified. No observable-event rule or quantum Born probability was derived.

**Recommended next investigation (not performed):** a preregistered spectral estimator conditioning audit using raw original-engine field exports, plus a broad scale search and physically normalized coordinate mapping. These would be new definitions and must never replace or rename original v001 outputs.

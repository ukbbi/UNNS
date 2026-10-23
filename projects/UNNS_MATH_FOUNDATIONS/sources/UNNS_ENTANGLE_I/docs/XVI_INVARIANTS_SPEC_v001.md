# XVI Structural Invariant Fidelity — Source-locked preregistration v001

## Input and scope

Authoritative source is **user-provided** `UNNS-Chamber_XVI_v0.8.4_STABLE.html`, preserved in the current project's `docs/sources/XVI_ENGINE_v084.html`. User-supplied JSON exports and `XVI_GRID_SCALING_v001.json` are frozen, separately hash-checked inputs. No source rewrite and no retuning the original validation thresholds.

The auditable experiment uses the grid candidate previously labeled `LIMITED_PHYSICAL_GEOMETRY_WITNESS`: fixed physical domain `L = 2π`, `T=0.4`, grids 64²/128²/256², deterministic seeds 41 and 137. The prior parameters and initialization are imported from the frozen grid-phase module. This is **not** the canonical Chamber XVI's unmodified nonlinear evolution.

The experiment has three branches using identical initial fields and time grids: (a) the prior finite-volume closure candidate, (b) same advection/diffusion but `α=0`, (c) diffusion only. Initial, 80%-time and final snapshots are inspected. These tail snapshots and the new 80%-time stationarity statistic are **new diagnostics**, not the source's cached `C⨂₄` history.

## Original definitions as implemented

1. **μ★:** source `sampleScaledBilinear`: sample periodic τ at `((xμ)%W,(yμ)%W)` by bilinear interpolation; `Delta_scale` = mean squared difference against original pixel τ. Source `estimateMuStar` chooses the minimum over the *restricted* iterated-addition grid `μ=1.600, 1.601, ..., <=1.640`. This places the golden ratio inside the search window by construction and uses grid-pixel, not fixed physical coordinates.
2. **p and R²:** source `captureSpectrum`: compute κ as *FFT Laplacian* of τ with wave numbers `(2π/W)k`; FFT κ, radial bin by `floor(sqrt(kx_index² + ky_index²))`, average squared complex FFT amplitudes within each nonempty integer bin `1 <= bin < W/2`. Perform straight log–log least-squares fit using **all bins**, without a minimum-power cutoff. Returns `p = -slope`, R² = 1 − SSE/SST. Source has no guard for zero or tiny powers. In Python, nonfinite fits are labeled undefined; numerical finite fits are preserved verbatim, even when meaningless. Separate reliable-support checks NEVER modify the original p fit.
3. **Entropy H_r:** 50-bin histogram between each field's *own* min and max, with bin index `floor(((τ-min)/(max-min))*49)` clamped `[0,49]`, `H_r=-Σ p_i log₂ p_i`. For an exactly uniform field the formula divides by zero; this audit reports undefined instead of inventing a value. Entropy here is **histogram Shannon entropy of τ amplitudes**, not entanglement entropy.

Original source monitors update spectral/entropy state on a discrete step schedule and cache entropy. A final-time diagnostic from the new branch therefore is not an exact replay of source UI timing. Original JSON exports do not carry raw τ arrays, hence the source reports cannot be independently recalculated from the archived JSON alone.

## Gates — thresholds frozen before scientific verdict

- **I0** all frozen inputs byte-integrity PASS.
- **I1** original source formulas recovered without relabeling physical units or sign.
- **I2** exact export replay requires raw τ from original exports; BLOCKED otherwise.
- **I3/I12** shared-array direct original JavaScript vs Python formula port: μ, Δ, H within 1e-10; p/R² within 1e-8 for strict fidelity; record failures, never hide them.
- **I4** candidate final std / initial std ≥ 0.65 on every grid and seed; finite-window condition only.
- **I5** candidate differs from no-closure control by relative L² ≥ 0.01; this certifies a nonzero *effect*, not invariant preservation.
- **I6** physical reliability of **the original all-bin p fit**: ≥8 supported radial bins, ≥1 octave, dominant power fraction ≤0.90, **at least 80% of fitted bins** above 10^-12 of peak bin power. Support flags are diagnostic only and cannot change p/R² values.
- **I7** μ within ±0.010 of 1.618 and not at a search endpoint at all grids/seeds; success would still be limited by the restricted scan.
- **I8** source's strict p target `p≈+2.28` within ±0.05, R²≥0.95, reliable I6 across all runs. (Original exported p≈−3 is disclosed as a source-target inconsistency, not silently corrected.)
- **I9** new 80%-time → final-time relative |ΔH|/|Hfinal| <1e-3 at all runs; if diffusion controls also satisfy it, report **non-specific** stationarity, not a preservation mechanism.
- **I11** nontrivial invariant distinct from controls requires independently reliable source diagnostics, beyond the observed field difference; otherwise OPEN/NOT DEMONSTRATED.
- **I10** Born rule remains NOT DERIVED; this phase makes no quantum measurement interpretation.

## Strict interpretation

**No primary pass can follow from passing unit tests alone.** A failed spectral reproducibility gate, failure against the original source target, or unavailable field-based original reproduction prevents a canonical-invariant certificate. The failure cannot be removed by changing spectral fit bounds, shifting the p sign, enlarging μ scan post hoc, or changing the 50-bin entropy rule. All proposed fixes require a separate preregistered study.

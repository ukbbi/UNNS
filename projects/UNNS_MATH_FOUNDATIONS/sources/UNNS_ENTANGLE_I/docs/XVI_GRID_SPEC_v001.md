# XVI Grid Geometry and τ Update — Phase v001 Specification

## 1. Problem and source boundary

The frozen Phase τ report `XVI_TAU_EVOLUTION_v001.json` concludes `FULL_TAU_CERTIFICATION_NOT_ESTABLISHED`. Gate T2 fails for at least the source-compatible centered candidate (relative idempotence near vanishing flux), and T4 fails for source-origin nonlinear trajectories under refinement. The original Chamber XVI source is intact, and this phase does **not** modify it. The mathematical objective here is to **separate physical-unit consistency from finite-difference projection consistency**.

## 2. Dimensional discrepancy in original HTML conventions

On an N×N grid, the original source model uses a spatial gradient `0.5*(roll(-1)−roll(1))` in the τ proto-flux, and Laplacian spectral `k=2πm/N`. Meanwhile its projection combines derivative operators with inconsistent symbols. The repaired finite-volume projection uses `h=2π/N`, divergence `D` as an h-scaled forward difference, and `G=-D*` as the h-scaled backward gradient.

For a fixed periodic physical domain `[0,2π]²`, a centered gradient coefficient is `1/(2h)=N/(4π)` rather than `1/2`. Consequently the source gradient is smaller than the fixed-domain physical gradient by `h=2π/N`. The source spectral m=1 Laplacian symbol is `-(2π/N)²` rather than the continuum `-1`. Keeping original λ, β and α constant across N therefore has no automatically established fixed-physical-domain interpretation. This is a **geometric provenance audit, not a proof that only one coordinate interpretation is possible**.

## 3. Distinct numerical candidate C — declared model

Physical domain `[0,2π]²`, periodic, `h=2π/N`; grid N ∈ {64,128,256}, seeds 41 and 137, analytic smooth initial arrays matched across grids from `init_tau` in the frozen Phase τ source. Define h-compatible second-difference Laplacian Δ_h, centered physical ∂_x,h, finite-volume backward G_h and matched forward D_h with the sign convention `G_h=-D_h*`. At every step:

```
κ = Δ_h τ
J = τ (G_h τ) − γ (G_h κ)
ψ = (D_h G_h)^† D_h J       [zero mode fixed by pseudoinverse]
J* = J − G_h ψ
τ_next = τ + Δt [−c ∂_x,h τ + ν Δ_h τ − α ψ]
```

Parameters: `c=0.45`, `ν=0.03`, `γ=1e-5`, `α=0.08`, **T=0.4**. For each N, choose `n_steps=ceil(T/min(0.25h/|c|, 0.20h²/ν))`, `Δt=T/n_steps`. The optional independent time-refinement comparator halves Δt for fixed N=128 and both seeds. Noise is **disabled**. This is an independent *physical-unit illustrative evolution* with diffusive sign and matched operators. **It is not the source's `τ←τ + λ sin(roll τ−τ)−β Δ_source τ; τ←τ−α_c ψ` model**, and it cannot validate that model by substitution.

## 4. Fixed finite checks / interpretation

* **S0**: byte-exact uploaded τ baseline, authentic HTML and repair source checksums match. The frozen negative T2/T4 verdicts must be retained. A failing lock aborts all new results.
* **S1**: report physical dimension ratios at 64,128,256 without silently declaring a corrected canonical length scale.
* **S2**: numerical idempotence reporting includes absolute residuals, relative residuals, and an interpretability indicator for projected-flux norm less than `1e-12` of reference norm. No relative success verdict is assigned below that floor.
* **S3**: for each seed, at **T=0.4** the relative field grid differences must decrease 64→128→256 and the 128→256 error must be <0.10. This is a *coupled space-time Cauchy* check, not pure spatial order of convergence.
* **S3b**: at the same fixed Δt=0.004 for all three N (100 steps at T=0.4), mesh-only differences decrease and the 128→256 error is <0.10 for both seeds. This isolates the mesh comparison from variation in time step.
* **S4**: every candidate closure in the tested finite run has compatible post-projection divergence RMS relative to pre-projection <1e-10, scaled idempotence <1e-10, and relative quadratic energy-decomposition residual <1e-10.
* **S5**: each finite run completes with finite τ, max |τ| <100 and final spatial standard deviation at least 0.65 of its own initial value (guards against uniformization as a false success). Also report the fraction of non-mean spectral power in modes |k|≤4.
* **S5a**: fixed-grid N=128 tests with Δt/2 must have relative final τ error <0.01 for both seeds; this diagnoses time discretization error but does not establish a continuum theorem.
* **S5b**: at N=64, seed 41, switching off the closure forcing (α=0, all else identical) must change the final τ field by relative L2 >0.001; prevents an inert closure term being credited.
* **S6**: XIV/XV chamber μ*, p, R² and chamber entropy remain OPEN and unimplemented.
* **S7**: exclusive observable events and quantum probability representation remain NOT DERIVED.

Numerical tolerances concern this finite model only; they are not stochastic confidence intervals or analytic guarantees. The source audit T0–T7 verdicts remain immutable regardless of outcomes. If any S3/S3b/S4/S5/S5a/S5b fails, the *new candidate* receives `CANDIDATE_NOT_CERTIFIED`. Even if all pass, `LIMITED_PHYSICAL_GEOMETRY_WITNESS` is the highest allowed candidate status. Full canonical τ dynamics and a Born derivation cannot be claimed in either case.

## 5. Counterexamples and next theorem obligations

A projection can be orthogonal while its nonlinear τ evolution lacks refinement convergence. A near-zero τ gradient can inflate relative idempotence errors while absolute residuals vanish. Preservation of a small band of Fourier modes is not equivalent to invariance of chamber Φ-lock, spectral slope p or entropy. A classical finite-volume flux projection can coexist with arbitrary assignments of q-outcome weights. The last point continues to block quantum measure selection until independent event-algebra and measurement-composition principles are derived.

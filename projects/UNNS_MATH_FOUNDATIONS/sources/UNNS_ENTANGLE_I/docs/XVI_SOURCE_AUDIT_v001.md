# Canonical XVI source reconciliation

## Recovered materials
- `XVI_ENGINE_v084.html`: intact v0.8.4 TauFieldEngineN JavaScript engine.
- Four exports: 64 α=0.020 interval=5; 128 α=0.015 interval=6;
  128 α=0.010 interval=6; 256 α=0.010 interval=6. All seed 41.
- Phase 3 frozen measure-representation report kept as source-locked baseline.

## Important source observations
1. `initializeFFTCache()` constructs k components as `(2π/W)*k_idx`.
2. `projectFlux()` computes `divJ` by periodic central differences with
   `grid_scale=(2π)/(2*W)`; the gradient is spectral `i*k*ψ̂`.
3. `psi_hat=-FFT(divJ)/k²` gives a hybrid operator with an inconsistent symbol.
4. The `divJ` diagnostics are never updated from `J*` after projection.
5. `computeIdempotence()` compares τ before/after another Closure step; its name
   is not a direct check of flux-projection algebraic idempotence.
6. C3 validates `abs(mean_divJ)/rms_divJ` under periodic conditions.
7. Export JSON identifies v0.8.0; engine itself declares v0.8.4.

`tools/xvi_original_engine_probe_v001.cjs` extracts *unchanged* engine class
from frozen HTML at runtime, invokes actual `projectFlux()` on longitudinal
Fourier modes, and prints directly measured residual/energy/idempotence. Node
is OPTIONAL: run Python tests and report without Node installed.

## Interpretation
The ideal L² Helmholtz projector is quadratic by definition of its inner-product
geometry. It cannot be used as evidence that UNNS derived quantum Born weights.
The immediate actionable next phase is a **separate controlled repair candidate**,
not a silent rewrite of canonical Operator XVI. Source-locked regression cases
should reject mean-only flux neutrality and test actual post-projection RMS.

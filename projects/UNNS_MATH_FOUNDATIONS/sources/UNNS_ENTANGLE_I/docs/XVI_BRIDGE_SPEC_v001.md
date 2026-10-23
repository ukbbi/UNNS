# XVI Canonical Bridge v001 — frozen specification

## Scope
Source-locked, *negative-control-first* audit of the **original, unmodified**
`UNNS-Chamber_XVI_v0.8.4_STABLE.html`, plus four 2026-10-20 seed-41 exports.
Phase 3's `MEASURE_REP_PHASE3_v001.json` is snapshotted and locked.
All historical UNNS_ENTANGLE_I phases and canonical Chamber XVI remain unchanged.

## Mathematics: exactly what the implementation does
On a periodic N×N grid the source computes divergence with
`grid_scale = (2π)/(2N) = π/N` times the centered-neighbor **difference**,
while its FFT grid uses `kx=(2π/N)k_index` and the spectral gradient uses `i*kx`.
The Poisson solver divides by `-(kx²+ky²)`.
These three symbols do not form a matched discrete gradient/divergence/Laplacian triple.

Let J=(sin(2πmx/N),0), m=1 and y independent. The implemented divergence
symbol is `d = (2π/N) sin(2πm/N)` and the implemented spectral wave number is
`k = (2πm/N)`. The computed gradient subtracts a **fraction** `d/k` of the
longitudinal flux, leaving

    R_N(m) = 1 - sin(2πm/N)/m.

The divergence measured with the same periodic stencil, after the source's
projectFlux(), retains exactly `R_N(m)` of its initial RMS (for this test mode).
For m=1, N=64/128/256: R=0.901982859670..., 0.950932325672...,
0.975458771477...; so correction degrades under grid refinement.
The projection also violates P²=P. With C=(1-R), `||J*||²+||∇ψ||²` misses
`||J||²` by `2*R*C*||J||²`, an L² orthogonality defect for this mode.

A *separate ideal comparator* with matched spectral symbols (on the periodic
2π domain) projects a pure longitudinal mode exactly. It **does not modify**
or repair the canonical source. It shows the issue is numerical-symbol mismatch,
not a mathematical failure of Helmholtz decomposition.

## Source/metric caveats
- The `divJ` buffer is computed **before** subtracting `∇ψ` and never recomputed
  afterward in `projectFlux()`. Timeline `mean_divJ`/`rms_divJ` therefore refer
  to the unprojected, current proto-flux J, not the projected field's divergence.
- For a periodic centered-difference divergence, spatial mean is exactly zero
  in exact arithmetic by telescoping, independent of whether the field is sealed.
  The chamber's C3 mean/RMS ratio does not certify divergence-free projection.
- The chamber's `computeIdempotence()` measures `||τ - Closure(τ)||²/||τ||²` for
  a scalar τ update, **not** the algebraic operator identity P²=P on flux.
- Source constructor says v0.8.4; JSON export hardcodes `version: '0.8.0'`.
- None of four exported JSON files supplies raw τ or J arrays: reproducing the
  original full stochastic run from the exports alone is impossible.
- The four grid cases alter more than grid size (α_c, interval, and duration),
  thus are **not** a controlled convergence series.

## Prespecified gates

| Gate | Required for PASS | v001 result |
|---|---|---|
| B0 | All input SHA-256 locks match | PASS |
| B1 | Audit faithful to original source | PASS |
| B2 | Projected longitudinal divergence ≤1e-10 relative RMS on 64/128/256 | FAIL |
| B3 | P²=P, J* ⟂ ∇ψ and L² identity to 1e-10 | FAIL |
| B4 | Matched-operator ideal comparator behaves correctly | REFERENCE ONLY |
| B5 | Independently derive observable exclusive-event measure from canonical flux closure | BLOCKED |
| B6 | Derive Born rule, full quantum entanglement and no-signalling from UNNS | NOT DERIVED |

A failed B2 or B3 is an **implementation** result, not a no-go theorem against
all possible corrected UNNS formulations. Passing B2/B3 with a corrected
operator would still not imply B5 or B6.

## Acceptance policy
No retrospective threshold changes. No fitting of quantum target correlations.
No conflation of classical field energy with probabilities. Original HTML and
JSON exports are immutable reference inputs. New code and output are separate.

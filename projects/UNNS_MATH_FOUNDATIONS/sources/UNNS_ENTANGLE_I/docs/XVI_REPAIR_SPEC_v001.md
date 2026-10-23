# XVI Projection Repair v001 — Source-locked mathematical certificate

**Scope:** an independent, numerical flux-projection candidate. **No changes to the v0.8.4 HTML, previous Chamber runs, Phase 3, or previous Bridge verdict.** This is *not* certification of the full time-evolution/τ-update and *not* a quantum probability result.

## Original discrepancy and baseline

The frozen `XVI_ENGINE_v084.html` computes a periodic *centered* finite-difference divergence with coefficient `grid_scale = (2*pi)/(2*N)` and subsequently inverts a Poisson operator with a *spectral* wave number `k = 2*pi*mode/N`. It reconstructs a correction gradient with that spectral wave number. Those two derivative symbols do not match. The frozen `XVI_CANONICAL_BRIDGE_v001.json` reports remaining divergence ratios 0.9019828597, 0.9509323257 and 0.9754587715 for longitudinal mode one on grids 64, 128, 256. Mean divergence alone is always nearly zero under periodic central differences; it is not a flux closure certificate.

## Precise discrete theorem (independent of probability)

On a finite **even** N×N periodic grid let `H` be the real vector-flux space with inner product `⟨J,K⟩ = mean(Jx*Kx+Jy*Ky)`. Let `D:H→S` be a real linear discrete divergence and define `G=-D*`. Let `L=DG=-DD*` and `L†` be its Moore–Penrose pseudoinverse, *including the nonconstant nullspace*. Define

`P = I - G L† D = I - D* (DD*)† D`.

Then **exactly in finite-dimensional arithmetic**: `DP=0`, `P²=P`, `P*=P`, and `⟨PJ,(I-P)J⟩=0`; hence `||J||² = ||PJ||² + ||(I-P)J||²`. These follow from elementary pseudoinverse identities, since `range(D)=range(DD*)`, and **the quadratic norm is already given in the premise**. The theorem does not prove a Born rule or establish a physical probability measure.

### Candidate C — closest source-compatible choice

Retain the original divergence's literal coefficient `h=π/N`:

`D(J)[y,x] = h*(Jx[y,x+1]-Jx[y,x-1]+Jy[y+1,x]-Jy[y-1,x])`.

The Fourier symbol is `d(k)=2i*h*sin(2πk/N)`; both the correction gradient `G` and Laplacian `L=DG` now use this **same** discrete symbol. For each mode with `|dx|²+|dy|² > 0`, solve

`ψ_hat = -(dx*Jx_hat+dy*Jy_hat) / (|dx|²+|dy|²)`, `P(J)_hat=(Jx_hat,Jy_hat) - (gx,gy)*ψ_hat`, `gx=-conj(dx)`, `gy=-conj(dy)`.

Null modes of `D` use `ψ_hat=0`, leaving the corresponding components unchanged. On even grids, the centered stencil has checkerboard/Nyquist nullspace beyond the constant mode. **A vanishing central-difference divergence does not imply continuum divergence vanishes at Nyquist.** The initial chamber coefficient has nonphysical derivative scaling; matching it repairs the projection algebra but does not itself fix physical discretization of τ evolution.

### Candidate F — independent finite-volume comparator

On a physical 2π-periodic domain with `Δx=2π/N`, use forward `D_x f=(f[x+1]-f[x])/Δx`, `D_y` similarly, and backward `G=-D*`. These have `d(k)=(exp(2πik/N)-1)/Δx`, with no checkerboard divergence nullspace except the constant scalar mode. Solve with the same pseudoinverse formula. This is an **alternative discrete operator**, not a source-preserving repair. Do not mix the two definitions of divergence when reporting closure.

## Preregistered executable gates

| Gate | Acceptance rule | Meaning |
|---|---|---|
| L0 | all frozen SHA-256 inputs match | source provenance preserved |
| L1 | candidate C: relative post-divergence, idempotence, energy defect, orthogonality, adjoint defect each < 1e-10; N=64/128/256, seeds 41/137 | candidate C algebra verified |
| L2 | same for candidate F | comparator consistent |
| L3 | for sampled smooth low-frequency fields, relative error vs matched continuum spectral projection strictly decreases 64→128→256 | finite-grid refinement consistency on this test corpus |
| L4 | checkerboard retained by C and eliminated by F | nullspace disclosed, not hidden |
| L5 | one closed field admits distinct normalized q=1/q=2 weights | flux projection alone does **not** select probability |
| L6 | independent UNNS observable-event structure and noncontextuality proof | **OPEN**; not a numerical gate |
| L7 | original τ evolution/invariants/grid-stable physical closure | **NOT TESTED**, requires separate work |

The numerical error thresholds are absolute predeclared constraints for the particular testing scope. They are not universal rigorous floating-point error bounds. Results use standard NumPy FFT and float64.

## Scope-limiting cautions

1. `P` acts on classical flux, not directly on physical quantum states or measurement events.
2. The repaired `ψ` can have a different scale from the source `ψ`; copying it into `τ←τ−α_c ψ` without reassessing units and dynamics would be unjustified. Do not patch the original HTML blindly.
3. The source-aligned operator has Nyquist modes which are invisible to its divergence; the separate finite-volume comparator addresses this deficiency, but has different flux semantics.
4. Convergence demonstrated for a smooth low-mode test family does not certify general nonsmooth fields, arbitrary boundary conditions, or physical invariants (μ,p,R²,entropy).
5. An exact quadratic energy decomposition is not a derivation of the Born rule because the Hilbert/L² inner product is an input assumption.
6. Prior `C⨂` (idempotence/invariants/flux-neutral/entropy/reversibility) badges of the original chamber are *not* upgraded by these tests; the patched flux requires new postprojection logs and independent end-to-end tests.

**Primary possible verdict:** `CANDIDATE_FLUX_PROJECTION_CERTIFIED_IN_TESTED_SCOPE`; never `CANONICAL_XVI_CERTIFIED` or `BORN_RULE_DERIVED`.

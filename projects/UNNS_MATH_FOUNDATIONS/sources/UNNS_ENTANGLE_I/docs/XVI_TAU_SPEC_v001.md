# XVI Tau Evolution v001 — Preregistered nonlinear closure certification

## Source scope and provenance

The prior, uploaded `XVI_PROJECTION_REPAIR_v001.json` is frozen **byte-for-byte** at `docs/frozen/XVI_PROJECTION_REPAIR_v001.json`. Its SHA-256 appears in `config/XVI_TAU_LOCK_v001.json`. The original Chamber XVI v0.8.4 HTML is **not altered** and is verified against its previous frozen SHA-256 under `docs/sources/XVI_ENGINE_v084.html` (installed by the earlier Canonical Bridge). Other Phases 0–3 and the prior repaired flux projector remain untouched. This is an **incremental overlay**.

This phase tests the **full deterministic nonlinear evolution chain** of a candidate Python translation of the HTML's mathematical update. The tested operation is classical numerical field dynamics, **not** an observable quantum event or a quantum probability measure.

## Three locked comparator arms

* `original_emulation`: translated original mismatched source Helmholtz/Poisson correction; uses the original source's literal central-difference divergence and original FFT coefficient symbols.
* `central_source`: preserves source divergence but solves Poisson with its *matching* adjoint finite-grid gradient and Laplacian, including nullspace disclosure.
* `forward_volume`: independent matched forward-difference divergence/backward-adjoint gradient in a physical 2π-periodic domain, with a unique zero-mode nullspace.

**Only the projection method differs across arms.** Each receives exactly the same deterministic initial τ array, base update and proto-flux. This does NOT imply the physical units of candidate corrections are equivalent. This mismatch is a deliberate audit target.

## Nonlinear iteration: source-derived ordering

For τ on an even N×N periodic grid, set `β=0.000002`, `λ=0.1`, `γ=0.00001`, `αc=0.01`, closure interval 6, steps 180 and **σ=anneal_sigma=0**. Define source FFT Laplacian with `k=2π*integer/N`, and source spatial gradient with immediate neighbors divided by 2.

Every step `s` (s begins at zero):

```
κ_s = source_FFT_laplacian(τ_s)
τ_evolved = τ_s + λ sin(roll_x(τ_s,-1) - τ_s) - β κ_s
if s>0 and s mod 6 == 0:
    Jx,Jy = τ_evolved × grad_center(τ_evolved)
            - γ grad_center(source_FFT_laplacian(τ_evolved))
    J*, ψ = P_method(J)
    τ_{s+1} = τ_evolved - αc ψ
else:
    τ_{s+1} = τ_evolved
```

Note: the actual HTML constructor uses `config.sigma || 0.02`, so explicitly setting `sigma=0` is not honored via configuration. The optional direct JavaScript witness explicitly assigns `eng.sigma=0` after construction to create a controlled deterministic comparator. Production UI default noise is **not** certified by this run.

Source HTML and exported runs use a 0.8.4/0.8.0 version mismatch, preserved as previously audited. The pseudo-Poisson correction and source-laplacian conventions are reproduced, not silently repaired.

## Frozen comparator protocol

Full run: smooth periodic band-limited initial fields, grids N=64,128,256 and seeds 41/137; 180 steps; three projector arms. Additional independent random-phase stress corpus on grids 64 and 128, seeds 41/137, 72 steps, all three arms. Randomness is NumPy PCG64 and is **not** the chamber's own JavaScript PRNG. Evolution has no added stochastic noise. Same smooth analytic seed and physical spatial coordinates at each grid; co-located grid samples are compared to assess resolution consistency.

A direct original-JavaScript witness uses the byte-locked HTML engine for N=64, seeds 41/137 and 24 steps, with the exact same initial array and explicit zero noise; acceptance is relative τ RMS error <1e-10. It does **not** certify all 180 steps, source random initialization, nonzero noise, the UI or 256² direct JavaScript execution.

## Scientific acceptance/falsification gates — fixed before inspecting outputs

| Gate | Pass condition | Qualification |
|---|---|---|
| T0 | prior repair and original HTML SHA-256 match active/frozen source | preserve baseline |
| T1 | all four source-derived nonlinear stages executed, specified source order | source translation only |
| T2 | at **every** candidate closure: post-projection compatible divergence RMS <1e-10, projector idempotence relative <1e-10, quadratic energy defect relative <1e-10 | FAIL if any grid/seed/corpus violates |
| T3 | all candidate runs remain finite over their complete windows, max |τ| <1e6, final τ RMS <5× initial τ RMS | finite-horizon, not asymptotic stability |
| T4 | on the common smooth corpus, τ-grid Cauchy relative error strictly decreases 64→128→256 and final 128-vs-256 error <0.10 in every repaired arm/seed | separate from flux projection accuracy |
| T5 | Chamber XIV μ*, XV spectral slope p/R² and entropy are independently translated, validated, and meet frozen invariance tolerance | **OPEN**, not certified merely by finite τ |
| T6 | original unmodified JS source 24-step zero-noise τ matches Python translation to <1e-10 for both locked seeds | short scope only; optional Node rerun |
| T7 | independent exclusive observable-event structure plus probability representation bridge | **NOT DERIVED**, no Born-rule claim |

All numerical magnitudes use float64/NumPy FFT. Gates are **finite test conditions, not error-bound theorems**. There is no general guarantee of physical closure from passing them.

## Required outcomes

Primary verdict can only be `FINITE_WINDOW_TAU_CANDIDATE_PASS_LIMITED` if T2/T3/T4 all pass, otherwise `FULL_TAU_CERTIFICATION_NOT_ESTABLISHED`. Even a pass does **not** elevate T5/T7. Unit tests confirm correct algorithms and honest reporting; they do **not** constitute primary physical validation.

## Predetermined negative controls

* The original projection must remain imperfect on a low longitudinal mode, not be quietly replaced.
* Smooth τ trajectories from the different discretizations can diverge despite individually accurate flux projection; track grid Cauchy errors.
* Centered stencils have checkerboard/Nyquist nullspaces, and the corresponding scalar potential can be ill-conditioned.
* Different q-weight rules can still be imposed on the same closed field; measure-selection remains independent.

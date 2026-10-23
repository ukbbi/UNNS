# XVI Tau Evolution v001 — Findings (source-bound, numerical)

## Outcome

**Primary verdict:** `FULL_TAU_CERTIFICATION_NOT_ESTABLISHED`.

The original and two candidate projectors were integrated into the **same source-grounded nonlinear τ update**, without modifying canonical Chamber XVI. After a controlled 180-step smooth run, plus a 72-step seeded random-phase stress run, the candidate projectors were not jointly certified across all grids and both input families by the preregistered gates.

The full report is `output/XVI_TAU_EVOLUTION_v001.json`; do not mistake unit-test success for a physical-theorem pass. The report contains every seed/method/grid pairing, the last three closure diagnostics, and sparse field summaries.

## What the experiment established

**T0 PASS:** Original Chamber HTML SHA and the user-uploaded repair baseline are unchanged and checked. The previous report's favorable flux-projection conclusion is preserved without amendment.

**T1 PASS_SOURCE_TRANSLATION_ONLY:** Python implements the HTML's `evolveField → computeFlux → projectFlux → τ ← τ−αψ` sequence with the original source's periodic gradient, source FFT Laplacian, original closure schedule, and common initial data.

**T6 PASS_24_STEP_ZERO_NOISE_WITNESS_ONLY:** Running the unmodified original HTML engine JavaScript directly for 24 steps at grid 64 against precisely identical seeded smooth initial fields and explicitly disabled noise yields relative τ RMS errors 1.205e−17 (seed 41), 1.132e−17 (seed 137). The witness validates the short-run translation, **not** all long runs nor UI noise settings.

**T2 FAIL:** the matched-central repaired flux does retain almost-zero compatible divergence and energy defect, but the idempotence *relative metric* degrades at 256² in the full smooth evolution: approximately 0.001779 (seed 41) and 0.001989 (seed 137) compared with 1e−10 threshold. This is a conditioning/nullspace and cancellation warning, not evidence of altered canonical physics. Finite-volume candidate remains around machine-precision for the tested compatible discrete projector; full suite is conjunctive and therefore fails T2.

**T3 PASS_FINITE_WINDOW:** each candidate run remained finite and under the declared τ magnitude and growth limits for the finite deterministic windows. This does **not** assert asymptotic stability, physical energy conservation, or stability under random noise.

**T4 FAIL_OR_NONCONVERGENT:** smooth τ-field Cauchy errors between 128² and 256² were about 0.2403 (seed 41) and 0.2208 (seed 137) with the finite-volume candidate, above the preregistered threshold of 0.10. The central-source repair did show small grid discrepancies (~3.24e−5 and ~3.03e−5) on this corpus; that arm's potential is extremely scale-sensitive and the T2 numerical-idempotence gate fails. Different discretizations are not interchangeable merely because both are exact projectors on their own flux space.

**T5 OPEN:** we have not reproduced Chamber's XIV μ*, XV spectral power slope p / R² and entropy monitor for full source runs with frozen comparator criteria. Final τ RMS and mean cannot substitute for these diagnostics. Additionally the published original 64–256 JSON exports did not include raw fields or post-projection divergence time series. Thus **no physical invariant certification is claimed**.

**T7 NOT_DERIVED:** a matched orthogonal field projector does not imply observable-event identification, probability noncontextuality, a measure-representation theorem, or quantum Born weights. The earlier measure-nonuniqueness counterexample remains intact.

## Important confounding convention

The canonical HTML's default `sigma` is 0.02 if the constructor receives a falsy value due to `config.sigma || 0.02`. To isolate numerical projection differences, the deterministic direct JS witness manually sets `sigma = 0`; Python likewise rejects nonzero noise. This deliberately deviates from the original UI's stochastic default behavior. Matching true noisy source runs is a **new separate experiment**, and a source-preserving random-stream comparison would require reproducing the exact JavaScript PRNG and its sampling order.

## Recommended research continuation (do not auto-claim completion)

1. Perform a strict grid-geometry and τ potential-scale dimensional audit before modifying a full chamber or calling any method physically valid.
2. Test source-compatible center projector under conditioning-aware absolute and relative idempotence residuals, including near-zero flux and Nyquist components, without retroactively changing this phase's predeclared gate.
3. Develop a truly physically consistent evolution discretization (flux, Laplacian, τ dynamics and time-step scaling together) as a **new independently named candidate**; compare to source baseline with fixed physical time and spatial domain.
4. Translate and preregister the μ*, p, R², entropy and post-correction divergence metrics, with transparent noise controls, before seeking strong full-chamber certification.
5. Only after independent dynamics certification reconsider the measure-representation project; no finite classical field computation by itself derives Born's rule.

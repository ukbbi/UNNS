# Method reconstruction

## 1. Measurement correction

For each qubit and each run, the package implements the paper's Eq. (4):

`m_corr(t) = [m_meas(t) - m_final] / |m_meas(0) - m_final|`

The paper calls `m_final` an average over "a few" latest points. Because the exact count is not specified, this reconstruction uses the last **5** samples and records that choice in `physics_validation.json`.

## 2. 2T envelope alignment

The ideal epsilon=0 reference alternates sign every Floquet period. A single exponential envelope cannot be fitted directly to a sign-alternating trace.

For the error-envelope fit only, the code removes:
- the initial-state sign, and
- the known ideal `(-1)^t` alternation.

This does not create a DTC criterion; it only places the measured 2T reference envelope into one branch so the published depolarization fit can be operationalized.

## 3. Post-transient average and W0/Wf

The paper states that the bar in Eq. (8) is an average over five timesteps after the initial 13 timesteps.

This reconstruction therefore uses:

`t = 13,14,15,16,17`

Default thresholds:

`W0 = 0.15`

`Wf/W0 = 2/3`, hence `Wf = 0.10`.

A qubit with reference average below `W0` is rejected.

For finite epsilon, a qubit whose post-transient average lies inside `[-Wf, Wf]` is treated as thermal and is not depolarization-rescaled.

## 4. Reference fit: Eq. (7)

After the 2T alignment, the stated form

`1/2 [m_i^(0)(t) + sign(m_i^(0)(t))] = a_i exp(-b_i t) + c_i`

is fitted from timestep 13 onward.

The implementation searches `b` on a fixed reproducible grid and solves `a,c` exactly by linear least squares for each `b`.

No arbitrary fit-quality threshold is imposed because the paper does not publish its numerical convergence cutoff. Numerically invalid fitted denominators are rejected and all fit diagnostics are exported.

## 5. Depolarization rescaling: Eq. (8)

For accepted, nonthermal qubits, the package applies the stated Eq. (8) form after timestep 13:

`M_i(t) = (bar_m_eps / bar_m_0) * [m_i_eps(t) + sign(m_i_eps(t))] / fit_i(t) - sign(m_i_eps(t))`

Thermal qubits remain measurement-corrected but are not rescaled.

## 6. Critical fluctuations

For every accepted qubit:

`h_i = |F{Z_i(t)}(omega_D/2)|`

The implementation normalizes by the number of time samples, so a perfect 2T oscillation has amplitude approximately 1. The normalization changes the vertical scale of `Var(h_i)` but not its epsilon location.

Repeated supplied files at the same epsilon are aggregated by the median. File-level results remain in `file_metrics.csv`.

Two peak locations are reported:
- the raw discrete epsilon with the largest median variance;
- a lightly smoothed peak.

The smoothing bandwidth is **not** set to 0.075 or any physical target. It is generated from the epsilon grid as `2.5 x median grid spacing` for epsilon <= 0.20.

## 7. Depolarization transition

For each accepted qubit, the package estimates

`|Z_i(t)| ~ exp(-delta_i t)`

from the post-transient window `t=13..30`.

The median epsilon curve is then fit by two linear segments; the shared grid point minimizing total squared error is reported as the decay transition.

## 8. Physics gate

The package tests:

- persistent 2T response for the supplied epsilon=0.05 standard run;
- rapid depolarization for the epsilon=0.50 thermal run;
- critical-fluctuation transition near the published epsilon_c;
- independent decay-rate transition in the same region.

This is the final firewall before any UNNS temporal-closure construction.

# TC_CTRL_v001 — Result Summary

## Status

**PASS_CONTROL_CHALLENGE**

The exact frozen metric from `TC_CLOSURE_LOCK_v001` was verified before the
control suite ran.

Metric SHA-256:

`06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553`

## Exact synthetic period-2

- detected q0: **2**
- C(2): **1.000000**
- recurrence-family contrast: **1.000000**
- shuffle p_ge: **0.004975**

As required, the frozen metric recognizes exact temporal recurrence.

## Classical nonlinear period-2 — logistic map r=3.20

- detected q0: **2**
- C(2): **1.000000**
- recurrence-family contrast: **0.213201**
- shuffle p_ge: **0.004975**

This is the decisive control: an ordinary classical nonlinear period-2
attractor produces strong, temporally significant frozen closure.

## Classical period-4 sanity test — logistic map r=3.50

- detected q0: **4**
- C(q0): **0.987293**
- shuffle p_ge: **0.004975**

The frozen recurrence-depth detector generalizes beyond q=2 and independently
selects q=4 in this classical control.

## Chaotic negative control — logistic map r=4.00

- detected q0: **8**
- local spectral contrast: **0.015997**
- detected-family contrast: **0.019559**
- shuffle p_ge: **0.393035**

Although the q detector must return some interior q, the closure contrast is
tiny and the trajectory is not distinguishable from its time-shuffled null.

## IID random negative control

- local spectral contrast: **0.009812**
- detected-family contrast: **0.008827**
- shuffle p_ge: **0.497512**

Again there is no meaningful ordered recurrence.

## Damped/transient period doubling

At gamma=0.10:

- detected q0: **2**
- C(2): **0.191644**
- q=2 family contrast: **0.117976**
- shuffle p_ge: **0.054726**

The sign alternation remains period-2, but supported closure collapses as the
trajectory amplitude dies away.

## Preserved limitation: harmonic ambiguity

For the noisy period-2 control at sigma=0.20 the frozen detector reports:

- detected q0: **8**
- C(2): **0.825999**
- q=2 family contrast: **0.815937**

Because all even recurrence depths are close to degenerate in a nearly exact
period-2 sequence, small noise can make the frozen local-contrast rule promote
a higher harmonic. This is now an explicit limitation of the q0 detector and
has not been repaired after inspection.

## Main scientific result

The control challenge gives a clear answer:

**Temporal closure is not unique to a discrete time crystal.**

A completely classical logistic-map period-2 attractor produces strong q=2
closure and survives the same time-shuffle test.

Therefore the correct interpretation is:

**C(q) detects temporal recurrence structure.**

The DTC-specific distinction must occur at a higher structural level:
perturbation rigidity, collective persistence, and universality across
initial states / disorder realizations.

This is exactly the reason to proceed next to `TC_RIGIDITY_v001`.

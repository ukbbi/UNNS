# TC_RIGIDITY_v001 — Result Summary

## Status

**RIGIDITY_TEST_COMPLETE**

## Specificity verdict

**DTC_SPECIFICITY_NOT_ESTABLISHED**

This is a scientifically informative negative result, not a failed run.

The frozen temporal-closure metric remained unchanged.

Metric SHA-256:

`06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553`

## Closure-family geometry

The site-resolved Mi MBL-DTC closure spectrum and the exact ordinary classical
2T spectrum are almost the same geometric object:

- cosine similarity: **0.999988952**
- normalized RMS distance: **0.005819179**

The Mi spectrum is essentially an experimentally attenuated version of the
ideal alternating closure ladder.

Therefore closure-family geometry by itself is not DTC-specific.

## Initial-state universality

The dimensionless universality score is:

- Mi MBL-DTC: **0.986036**
- Mi prethermal: **0.844370**

The exact values are exported in `rigidity_vectors.csv`.

Most importantly, the deliberately ordinary classical map:

`X_(t+1) = -X_t`

has **U = 1.000000** across three
very different initial states.

Thus high initial-state universality is also not unique to a DTC.

## Perturbation-basin geometry

Dimensionless normalized basin-retention areas:

- Frey_MBL_DTC: **0.982069**
- classical_exact2T_plus_noise: **0.923071**
- classical_exact2T_plus_damping: **0.669981**

The Frey MBL-DTC has the strongest retention among these particular
perturbations, but the ordinary 2T + noise control also sustains a broad
closure basin. This is quantitative evidence for stronger DTC rigidity in
that comparison, not a categorical separator.

## Pareto result

Exact ordinary classical 2T is greater than or equal to the Mi MBL-DTC on all
three core monotone recurrence-rigidity axes `(C,F,S)`:

**True**

The ordinary classical sign-flip family is also greater than or equal to the
Mi MBL initial-state result on `(C,F,S,U)`:

**True**

This has an important consequence:

> No monotone scalar reweighting of C, F, S, and U can now be justified as a
> DTC-specific order parameter.

At the same time, the same rigidity vector **does** preserve the experimentally
useful separation:

- Mi MBL-DTC over thermal control: **True**
- Mi MBL-DTC over prethermal control: **True**

## Main finding

The research has now isolated the boundary of what temporal closure can claim.

**UNNS temporal closure and recurrence rigidity are genuine structural
observables, but trajectory-level recurrence alone does not encode the
many-body nature of a time crystal.**

The next stage should therefore not retune these metrics. It must introduce an
independent collective/many-body structural coordinate and ask whether:

`temporal closure + collective order`

separates DTCs from ordinary classical periodic attractors.

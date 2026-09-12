# TC_CLOSURE_v001 — Result Summary

## Status

**TC_CLOSURE_V001_COMPLETE**

The frozen physics layer passed its firewall gate before this analysis began.

## First structural result

The generic closure spectrum searched recurrence depths q=1..10 without supplying q=2.

It detected:

**q0 = 2**

with low-perturbation local spectral contrast:

**0.765595**

The spectrum therefore independently selects the expected 2-step recurrence as its strongest primitive temporal closure.

## Exploratory closure basin

Using the predeclared v001 robust plateau-exit rule, the recurrence-family contrast leaves its low-perturbation basin at:

**epsilon = 0.070**

Only after that closure result was written was it compared with the frozen physical transition reference:

**epsilon_c ≈ 0.075**

Absolute grid-level difference:

**0.005**

No interpolation toward the physical reference is used.

## Temporal-order null

For the representative epsilon=0.05 standard run:

- observed C(q0): **0.681821**
- shuffled-time null mean: **0.284335**
- null 99th percentile: **0.393027**
- empirical p( shuffled >= observed ): **0.004975**

The high closure therefore depends on temporal ordering, not merely on the set of observed state amplitudes.

## Controls

All supplied epsilon=0.05 special/control records are exported individually in `outputs/control_comparison.csv`.

The no-disorder-tagged records show substantially weaker recurrence-family closure than the strongest standard/disordered low-epsilon records, while the standard polarized and Neel records remain strongly closed. This is consistent with the closure metric responding to more than simple signal amplitude.

## Interpretation status

This is a positive **exploratory structural result**, not yet the final time-crystal claim.

The important new observations are:

1. q=2 emerges from a q=1..10 recurrence search rather than being inserted.
2. Its higher multiples form a coherent recurrence family.
3. The recurrence-family basin loses stability at epsilon=0.07 on the observed grid.
4. That structural edge lies close to the independently frozen physical transition near epsilon=0.075.
5. A time-shuffle surrogate destroys most of the closure signal.

The next decisive test is to freeze this exact metric and apply it unchanged to an independent DTC dataset and to ordinary period-doubled controls.

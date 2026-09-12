# TC_EXT_MI_v001 — Method

## Purpose

Apply the exact frozen temporal-closure metric from `TC_CLOSURE_LOCK_v001`
to the independent Mi et al. dataset without changing the closure formula,
q search, recurrence-family definition, or shuffle-null protocol.

## Frozen metric

The runner imports:

`..\TC_CLOSURE_LOCK_v001\src\tc_closure.py`

and verifies its SHA-256 against the lock before analysis.

Expected metric SHA-256:

`06344c8641aa14e6663cc3cba65d86fcdb9e37857909e85da6bc0d689e5b2553`

No copy of the metric is edited inside this validation package.

## Dataset-specific adapter A — Fig. 2d

Files:

- `DTC_Data/fig_2d_right.csv`
- `DTC_Data/fig_2d_left.csv`

The CSV matrices are stored as qubit location × time.

The adapter performs only:

`qubit × time -> transpose -> X_t vector across qubits`

No smoothing, sign alignment, rescaling, or closure-specific tuning is applied.

The public paper identifies the right panel as g=0.97 MBL-DTC and the left
panel as g=0.60 thermal. Those labels are used only for interpretation after
the frozen metric has been calculated.

## Dataset-specific adapter B — Fig. 3a

File:

`DTC_Data/fig_3a.csv`

The file contains six experimental traces:
- three MBL-DTC initial-state autocorrelators;
- three prethermal initial-state autocorrelators.

For each regime, all three traces are used as coordinates of one X_t vector.
This provides a recurrence test that simultaneously carries information about
the three initial-state classes.

The adapter also evaluates all 3 choose 2 pairs. No pair is selected or
discarded.

## Frozen quantities calculated

For every trajectory:

- `C(q)` for q=1..10
- automatic q0 from maximum local spectral contrast
- recurrence-family contrast
- 200 time-order shuffle surrogates with frozen seed 20260819

## What is not tested here

The Mi CSV release does not provide a full site-resolved trajectory sweep over
the phase-transition parameter g in the same form as Fig. 2d. Therefore the
original `plateau_exit_boundary` rule is not applied to manufacture a basin
location from summary observables.

That limitation is preserved rather than replacing the frozen basin rule with
a dataset-specific alternative.

## Interpretation status

This is an independent-dataset test of a frozen metric.

It is not a fully preregistered end-to-end experiment because the Mi-specific
adapter was designed after inspecting the CSV layout. The core closure metric,
however, was frozen before this dataset was ingested.

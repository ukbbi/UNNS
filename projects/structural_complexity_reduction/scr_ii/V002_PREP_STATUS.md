# SCR-II v002 Prep Status

This package closes v001 before primary execution and introduces the multiplicity-controlled v002 benchmark.

## Important

There is deliberately **no v002 primary runner in this package**.

First reproduce on the local Windows machine:

1. v002 preregistration validation;
2. v002 multiplicity calibration;
3. v002 implementation/design audit.

Only after those records are reviewed should a separate primary runner be built.

## Expected calibration multiplicity

Using the frozen calibration seeds:

- d=8: 6–10 exact solutions;
- d=10: 21–39 exact solutions;
- d=12: 86–141 exact solutions.

This removes the v001 single-solution degeneracy.

## Design-preservation diagnostic

The design audit records, but does not tune on, whether the frozen structural filter preserves the entire independently generated exact solution set.

A negative preservation diagnostic is scientifically meaningful and must not be repaired by retuning the benchmark after freeze.

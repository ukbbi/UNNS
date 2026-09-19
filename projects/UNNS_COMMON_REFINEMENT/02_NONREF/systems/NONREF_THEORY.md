# Phase 2 — Exact Non-Refinement Controls

## 1. Construction

Let `H ⊆ N` be an additive commutative cancellative monoid. Define the multiplicative monomial monoid

`M_H = { X^n : n ∈ H }`

with

`X^r · X^s = X^(r+s)`.

Then a multiplicative endpoint equality

`X^a X^b = X^c X^d`

is exactly the additive equality

`a+b = c+d`.

A common multiplicative refinement exists in `M_H` exactly when there are `e,f,g,h ∈ H` such that

`a=e+f,  b=g+h,  c=e+g,  d=f+h`.

So refinement can be tested by exact integer arithmetic.

## 2. Flagship counterexample

Take

`H=<2,3>={0,2,3,4,5,...}`.

Then

`2+4=3+3=6`

and therefore

`X^2 X^4 = X^3 X^3 = X^6`.

All ambient nonnegative-integer refinement witnesses are obtained by choosing `e=0,1,2`:

- `(e,f,g,h)=(0,2,3,1)`
- `(1,1,2,2)`
- `(2,0,1,3)`

Every ambient witness uses exponent `1`, but `1∉H`.

Therefore no refinement witness exists in `H`:

`D_R = 1`.

This is an exact failure, not a search-time failure.

## 3. Repair

Adjoin the missing exponent `1`.

Then `<1,2,3>=N`, and the same equality immediately has valid refinements, for example

`(e,f,g,h)=(0,2,3,1)`.

Thus the obstruction is removed by restoring the missing splitting element.

## 4. Structural interpretation

The control demonstrates:

`endpoint equality ≠ route closure`.

The failure is caused by a **splitting hole**: the ambient free monoid contains refinement witnesses, but every such witness requires at least one element omitted by the submonoid.

For the flagship case the common blocking hole is exactly `1`.

The current Phase-2 hypothesis is therefore:

> Common refinement requires not merely endpoint closure, but sufficient closure under the residual/splitting elements demanded by route reconciliation.

This is narrower and more testable than saying "holes cause failure." Scaled free monoids such as `2N=<2,4,6>` have gaps in ambient `N` but no corresponding defect relative to their own group `2Z`.

## 5. Status

The scripts establish explicit `D_R=1` controls and compare them with scaled-free and repaired controls.

They do **not** claim that saturation is sufficient for refinement in arbitrary commutative monoids. Phase 2 identifies it as a candidate structural ingredient to test.

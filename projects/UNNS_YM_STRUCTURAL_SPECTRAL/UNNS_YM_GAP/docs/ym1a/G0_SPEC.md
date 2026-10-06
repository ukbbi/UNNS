# YM1A-G0 — Adversarial Gapless Continuation

**Status:** frozen construction protocol v1.0  
**Input:** `ladders/ym1a_refinement.csv`  
**Canonical chamber:** unchanged `STRUC-I`

## 1. Purpose

YM1A-G0 creates a controlled synthetic route from the measured positive-gap
Yang–Mills spectrum toward a formal zero-gap boundary.

This stage does **not** claim that the synthetic route is a physically realized
Yang–Mills deformation. Its purpose is adversarial: preserve as much of the
measured internal spectral organization as possible while removing the absolute
separation from the vacuum.

## 2. Primary adversary — common-offset compression

Let the five-coordinate physical ladder at refinement level `i` be

\[
L_i=(x_1,x_2,x_3,x_4,x_5),
\]

where `x1` is the `A1++` ground state, the mass-gap coordinate.

For

\[
\epsilon = 2^{-k},\qquad k=0,1,\ldots,10,
\]

define

\[
L_i^{\mathrm{offset}}(\epsilon)
=
L_i-(1-\epsilon)x_1(1,1,1,1,1).
\]

Therefore

\[
x_1(\epsilon)=\epsilon x_1\to0^+
\]

while every pairwise spectral spacing is exactly preserved:

\[
x_j(\epsilon)-x_m(\epsilon)=x_j-x_m.
\]

This is the primary adversary because it changes the vacuum separation while
leaving the internal additive spectral geometry untouched.

The formal `epsilon=0` endpoint is stored for reference only. The primary
chamber sweep uses strictly positive epsilon.

## 3. Matched massive control — upward translation

Use the same deformation magnitude in the opposite direction:

\[
L_i^{\mathrm{up}}(\epsilon)
=
L_i+(1-\epsilon)x_1(1,1,1,1,1).
\]

This family also preserves all pairwise spacings exactly but moves the spectrum
away from the vacuum.

A structural failure present in both directions cannot be interpreted as
vacuum-specific non-crossability.

## 4. Null N1 — ratio-preserving scale collapse

\[
L_i^{\mathrm{scale}}(\epsilon)=\epsilon L_i.
\]

All mass ratios inside the five-coordinate vector are preserved while both the
gap and all internal spacings collapse toward zero.

This distinguishes a vacuum-offset obstruction from generic sensitivity to
small absolute scale.

## 5. Null N2 — gap-only deformation

\[
L_i^{\mathrm{gaponly}}(\epsilon)
=
(\epsilon x_1,x_2,x_3,x_4,x_5).
\]

Only the mass-gap coordinate moves. This tests whether any chamber transition
is caused solely by `c1` rather than by the collective translated branch.

## 6. Frozen epsilon grid

The primary sweep is:

\[
1,\frac12,\frac14,\frac18,\ldots,\frac1{1024}.
\]

No intermediate epsilon values are to be inserted after viewing the first
STRUC-I outcomes. A later refinement of the boundary is allowed only as a new,
explicitly versioned phase after the coarse boundary result has been recorded.

## 7. Candidate boundary event

At each lattice refinement level `i`, begin at `epsilon=1` and move down the
frozen grid.

The per-level candidate boundary index `k_i*` is the **first** grid point at
which the canonical `STRUC-I` verdict differs from its own `epsilon=1`
physical-baseline verdict, or the canonical chamber emits its existing
non-admissibility/failure state.

No new threshold is introduced for G0. Continuous chamber metrics are
descriptive unless a threshold already belongs to frozen `STRUC-I`.

If no categorical event occurs by `epsilon=1/1024`, that level is recorded as
**no boundary observed on the preregistered G0 grid**.

## 8. Refinement-stable G0 criterion

A G0 vacuum-boundary candidate requires all of the following:

1. a primary-family boundary event at at least **6 of 8** lattice refinement levels;
2. the event is present at **all four finest** lattice levels;
3. the observed `k_i*` values span no more than **two dyadic grid steps** across
   the qualifying levels;
4. the matched upward control does not show the same event at equal or smaller
   deformation depth in at least **6 of 8** levels.

Interpretation is then qualified by the nulls:

- if the scale null reproduces the same boundary, the result is not specific to
  vacuum-offset removal;
- if the gap-only null reproduces it while the offset branch does not, the
  effect is coordinate-local rather than collective;
- if the offset branch shows the stable event while both null interpretations
  differ, the evidence for a structural vacuum-boundary mechanism strengthens.

These are preregistered decision rules, not post-hoc scoring.

## 9. Files

`nulls/ym1a_g0/`

- `g0_offset.csv` — primary adversarial family
- `g0_upctrl.csv` — matched massive control
- `g0_scale.csv` — ratio-preserving scale-collapse null
- `g0_gaponly.csv` — gap-only null
- `g0_long.csv` — all families in long form
- `g0_invariants.csv` — construction checks
- `g0_endpoint.csv` — formal epsilon=0 endpoint, not primary chamber input

`scripts/ym1a_g0/`

- `build.py`
- `verify.py`
- `RUN_BUILD.bat`
- `RUN_VERIFY.bat`

`output/ym1a_g0_build.json` records the frozen build checks.

## 10. Interpretation boundary

YM1A-G0 only constructs the adversarial route.

The next phase, **YM1A-G1**, will adapt the frozen families to canonical
`STRUC-I` input and run the chamber without changing its rules.

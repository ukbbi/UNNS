# Rank-One Route Closure — Result Report

## Result

The distinction requested in `02_NONREF` is now exact.

For every nonzero additive submonoid

`H ⊆ N0`

let

- `m = min(H \ {0})`
- `g = gcd(H)`

Then:

`H has common 2x2 refinement for every endpoint equality`

**if and only if**

`m = g`.

Equivalently:

`H = g N0`.

Equivalently, `H` already equals the nonnegative part of its generated rank-one lattice.

## Exact classifier

`RCI(H) = m/g`

- `RCI = 1` → global route closure.
- `RCI > 1` → an exact `D_R = 1` equality necessarily exists.

## Why the original controls separate

| System | m | gcd | RCI | Global refinement |
|---|---:|---:|---:|---|
| `N0` | 1 | 1 | 1 | YES |
| `2N0` | 2 | 2 | 1 | YES |
| `3N0` | 3 | 3 | 1 | YES |
| `<2,3>` | 2 | 1 | 2 | NO |
| `<2,5>` | 2 | 1 | 2 | NO |
| `<3,4>` | 3 | 1 | 3 | NO |
| `<3,5>` | 3 | 1 | 3 | NO |
| `<4,5>` | 4 | 1 | 4 | NO |

## Constructive failure

If `RCI>1`, the project now constructs a counterexample rather than merely searching for one.

Choose:
- `m` = least positive element,
- `x` = least element of H not divisible by m,
- `k` = least integer ≥2 with `kx-m ∈ H`.

Then

`m + (kx-m) = x + (k-1)x`

has no common refinement in H.

For `<2,3>` this gives exactly

`2+4=3+3`.

For `<3,4>` it gives

`3+9=4+8`.

## Computational adversarial check

Generator families tested: **793**

Range: generators chosen from `1..12`, set sizes `1..4`.

- theorem-classified refinement families: **280**
- theorem-classified non-refinement families: **513**
- constructive `D_R=1` counterexamples verified: **513**
- false counterexamples found: **0**

The computation is a validation of the implementation; the criterion itself is established by proof, not inferred from the scan.

## UNNS significance

This is the first theorem-level version of structural route closure in the project:

`same endpoint + full rank-one lattice closure -> common structural ancestry`

while

`same endpoint + lattice splitting defect -> possible exact route-closure failure`.

The earlier "blocking hole" language is therefore sharpened: in rank one the exact obstruction is failure to occupy all nonnegative points permitted by the generated lattice.

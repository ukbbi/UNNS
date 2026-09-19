# PHASE 2 FROZEN PROTOCOL

## Aim
Produce exact systems with endpoint equality but no common refinement.

## Domain family
Additive submonoids `H` of `N`, represented multiplicatively by `M_H={X^n:n∈H}`.

## Endpoint condition
`a+b=c+d`, equivalently `X^a X^b = X^c X^d`.

## Exact witness condition
`a=e+f`, `b=g+h`, `c=e+g`, `d=f+h`, with all `e,f,g,h∈H`.

## Exact search
For a fixed endpoint equality, every ambient `N` witness is parameterized by `e`:

- `f=a-e`
- `g=c-e`
- `h=b-g`

with `max(0,c-b) ≤ e ≤ min(a,c)`.

This is a finite exhaustive enumeration. A `D_R=1` verdict is issued only when this complete witness list contains no all-in-H witness.

## Controls
- `N=<1>`: free control.
- `2N=<2,4,6>`: scaled-free control.
- `3N=<3,6,9>`: scaled-free control.
- `<2,3>` repaired by adjoining `1`.

## Primary diagnostic
`D_R=0/1` from exact witness existence.

## Secondary structural diagnostic
For each failure:
- ambient witness count
- minimum number of out-of-H witness entries
- common blocking holes
- conductor / hole profile relative to the generated group

## Freeze rule
Do not alter system generators or witness equations after inspecting results. New systems must be appended as a separately versioned extension.

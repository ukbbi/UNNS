# Benchmark protocol — ROUTE_CSP_I

## Nominal search space

Each instance is a binary route of depth `d`, giving `2^d` complete candidates.

Calibration depths: `8, 10, 12`.  
Primary transfer depths: `14, 16, 18`.

## Instance construction order

For each seed:

1. Generate structural route metadata and one Γ_route-compatible backbone.
2. Generate the alternate/decoy branch metadata independently.
3. Generate branch costs and checksum weights.
4. Compute the backbone checksum and cost.
5. Freeze the arithmetic target from the backbone.
6. Emit the instance.
7. Exact baseline enumeration determines the full solution set; accidental additional solutions are retained.

The structural filter must never inspect steps 4–7 as gate inputs.

## Solution predicate

A full route is a solution iff:

- checksum modulo 31 equals the instance checksum target;
- total cost is within `[C_min,C_max]`;
- terminal seal condition is satisfied.

## Cost-window construction

The backbone cost defines the center. The half-width is frozen as:

\[
W(d)=\max(2,\lfloor 0.04d floor).
\]

Thus:

\[
C_{min}=C_{backbone}-W(d),\qquad C_{max}=C_{backbone}+W(d).
\]

## Terminal seal

The seal is one parity bit derived from the backbone terminal branch ID. The exact solver checks it; the structural filter may not.

## Ground truth

The baseline arm exhaustively enumerates all `2^d` complete routes for every primary instance.

Because `d≤18`, the largest nominal leaf count is 262,144, allowing exact solution-set comparison for every primary instance.

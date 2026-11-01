# GEO-HD-1B experiment preregistration (initial)

## Locked starting cases

- `B6`: all four labels N=1,2,3,6 and valuation projections `(2,3,7)`.
- `B72`: all twelve outgoing labels and two distinct equal-length histories.
- `B900`: 7-point three-dimensional trivial-lattice control.
- `B1296`: 2×2 enlarged trivial-lattice control, detecting the false d=1 remark.
- `P3`: parity-congruence `k=3`, primes `[2,5,11]`, 13 vertices.
- `P4`: parity-congruence `k=4`, primes `[2,5,11,17]`, 40 vertices.

## Independent checks

1. Derive each exponent vertex via actual `D(x)` and via congruence coordinates; assert equality.
2. Derive Graver vectors via conformal indecomposability and independently compare with the closed form.
3. Fix a **precise** admissible cell grammar (independent Graver direction subsets, full corner admissibility, translations). It is a new higher-dimensional extension, not automatically Paper A's.
4. Enumerate candidate cells, canonicalize by their exact vertex sets, and audit face intersections. No rounding in rank, incidence or geometry.
5. Compare exact polytope hull to union. A rational witness disproves coverage; a covering proof requires an exact certificate (e.g., exact subdivision), not sampling.
6. Homology requires actual chain complex boundary maps and verification `∂²=0`; pending that, report `not assessed`.
7. Repeat the cell study with at least one justified competing grammar to isolate grammar dependence.

## Success and falsification criteria

- PASS requires a rigorous theorem/counterexample about genuine nontrivial 3D/4D coupling or arithmetic histories, with explicit hypotheses.
- Any observed gap or collision in a provisional grammar is labelled as a grammar-relative computation until proved.
- If no nontrivial phenomenon survives, record the negative result and move to a more discriminating lattice; do not manufacture a universal theorem.

## Reproducibility

Run `RUN_WINDOWS.bat`, which calls `RUN_CHECKS.py`. The new baseline uses only Python standard libraries. `Scripts/geo_hd_1_check*.py` are preserved original checks requiring `sympy`. Version/manifest and exact generated JSON data are included.

# FIELD-I v007 — Persistent-G Growth and Collapse (SPEC)

Frozen predecessors v002–v006 and the G1–G3 memo are unchanged (byte-identical copies are inside the zip). v007 adds only `field7.py` (standalone: helpers copied from v005).

## Objects
x = a/b (lowest terms), D = D(x) = {d>=2 : d^2|a, d = 1 mod b} nonempty, g = gcd{d-1}, L = lcm D, y = g x (integer), Y = y + L^2, x' = C(x) = Y/g. Event classes: none (D' = D), preserving (D' strictly larger, every new d = 1 mod g, so G' = g), reducing (some new d != 1 mod g, so G' < g).

## Tracks
- **K8 Growth classification.** Exact membership criterion for D(x'), transition identity, event classes with reproducible witnesses.
- **K9 Arithmetic obstruction.** Congruence and prime-power anatomy of a preserving event (fresh primes, carried prime powers, divisor closure).
- **K10 Persistent regimes.** G = 4, 5, 12 first: proof or exact counterexample.
- **K11 Global collapse.** G_n > 1 ==> exists k > n with G_k < G_n ?

## Verification design
Exact Fraction/integer arithmetic. Three independent constructions of D(x'): (i) the criterion d^2|Y and g/gcd(g,d-1) | Y/d^2, (ii) occurrence integrality M = x'(d-1)/d^2 in Z>0, (iii) brute force Dset(a',b'); plus a factorisation-based Dx. K10 uses direct forward iteration of the collective map, never the (s,t) recursion, to test the closed form. Tags PASS / FAIL / DATA / OPEN; OPEN rows are never asserted.

## Run
`RUN_TESTS.bat` runs field2, g_checks, field3, field4, field5, field6, field7. `FIELD7_QUICK=1` shrinks field7 ranges.

# SPEC — FIELD-I v011
Question (O10.1): which prime carries forever, decided from finite arithmetic data rather than from the observed orbit?
Method: (1) exact carry-level predictor next_M (T67 = T53+T54 as a formula, validated against the gamma-level residue machine); (2) minimax selection for fixed odometers (T64) and its windowed persistence criterion;
(3) quotient-residue formula for Abs_p and the worst-case carry (T65); (4) static survivor certificate from ONE reset state (T66, with unsaturated extension): sufficient, and necessary for saturated survivors with prime g.
Tests: soundness against the machine, completeness on exact eventual cycles, uniqueness, negatives, coverage, end-to-end scaling-law prediction, controls (incl. the exact g = 31, L0 = 2^5*101^2 example).
Files: field11.py, THEOREMS.md, RESULTS.md, CONTEXT.md, RUN_TESTS.bat, output/.

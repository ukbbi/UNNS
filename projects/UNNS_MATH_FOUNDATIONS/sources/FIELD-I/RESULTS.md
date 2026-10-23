# FIELD-I v001 — initial results

**Release phase:** arithmetic F1–F3 complete as proofs and implemented; F4 leakage control and F5 conditional nonselection witness complete. **Intrinsic binary interaction selection remains open.** The 58-page relational manuscript, RGG packages and SELECT-I/II are unchanged.

## Reproducible outcomes

`python field1.py` (Python 3.13.5 in packaging environment): **46 tests, 46 pass, zero errors and zero failures**. Tests are enumerated in `output/reports/test_report.json`. All files in `output/` are actual generated deterministic outputs. Run without network or external Python packages.

- Nest 18: the first three integer terms are 361, 722, 1083, matching the 2017 original's example.
- Integer fibre 72: occurrences `(18,1)`, `(16,2)`, `(10,5)`.
- Non-anchor rational fibre `225/2`: `(25,2)`, `(18,4)`, `(7,14)`; three exact collisions.
- For `1<=N<=11` and `1<=M<=199`, **30 distinct noninteger values** occur at least twice within the sampled rectangular domain. This counts **distinct values with at least two in-bound occurrences**; it is not the number of collision pairs, and not a complete bound on rational fibres outside the rectangle. Sample witnesses are in `output/witnesses/rational_collisions.json`.
- Intersection of entire rational sequences of nests 2 and 4 begins at `225/2`, at moduli 25 and 18; the integer-only intersection starts at 225. Results for further pairs appear in `output/tables/cross_nest.csv`.
- Fixed-nest `U(M,N)=(M+1,N)` separates equal-value occurrences through next-value differences, but this is precisely the index number `(N+1)^2/N`, which re-encodes the nest label.
- Deliberately introduced `J_low` and `J_high` are distinct CAI operations sharing simultaneous unary-successor covariance and same-nest agreement. For `(25,2)` and `(18,4)`, their resulting nest outputs are `225/2` and `625/4`. These constructions prove *nonselection by the tested constraints*, not an independently selected interaction.

## Established vs conditional vs open

| Item | Status | Where |
|---|---|---|
| Rational-fibre characterization | PROVED | THEOREMS.md F1 |
| Entire rational cross-nest intersections | PROVED | THEOREMS.md F2 |
| Non-anchor collisions | PROVED possible; tested bounded population | THEOREMS.md F1 and output/witnesses |
| Two consecutive observations reconstruct `(M,N)` | PROVED, label chart | THEOREMS.md F4 |
| Unary fixed-nest dynamics determines unique binary operation | **FALSE** under CAI + covariance + same-nest agreement | THEOREMS.md F5 witness |
| Any UNNS-intrinsic binary interaction, physical significance | OPEN | synthesis/LIMITS.md |

### Scientific interpretation

The arithmetic extension is a valid completion of the rational occurrence domain, not an automatically novel theorem. No quotient obstruction is claimed on the basis of next-value identification alone, and the old RGG-2 join is not extended by fiat.

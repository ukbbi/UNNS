# MODEL_COMPATIBILITY — PAPER_IV_SYNTHESIS v0.5

Where a result is transferred between the two generating rules, the domain on which it is proved is stated here. A transfer is made only where listed; everything else is marked open or obstructed in the manuscript.

| Rule | Map | Domain | Notes |
|---|---|---|---|
| Individual (SELECT-II) | T_N(m) = m(N+1)^2/N | positive integers m with N dividing m (rational variants noted separately) | R(N) = (N+1)^2/N >= 4 |
| Collective (FIELD-I) | C(x) = x + L^2/G | pairs x = (a,b) with D(x) non-empty | C(x)/x <= 2 |
| Comparison | C is not T_N | all x with D(x) non-empty | ratio bound 2 < 4 (Section 11, SIV-P9) |

## Transfers argued

1. Factorization lemma (f factors through a surjection pi iff f is constant on fibres): purely set-theoretic; used for both rules.
2. Predecessor bijection (SIV-P2a): integer states only. D(t) <-> incoming steps, d -> (N = d-1, m = t(d-1)/d^2). Not claimed for rational states (open O8).
3. Translation formula for predecessors under C: integer x with integer C(x) only.
4. Monotone minimality (S4): transfers to any family of sets that grows by inclusion (Lemma M gives D(x) inside D(Cx)); no claim about lattice-level comparison (open O7).
5. Component rule and edge window for K(D): hold for every finite divisor set D; recomputed over the recorded range (results/c5_checks.json) as well as proved.
6. Cross-system statements are limited to levels L1-L2 of SIV-P9; L3 is open, L4 and L5 are obstructed. No commuting square between the two rules is claimed.

## Not transferred

- Finite-exact censuses (SIV-P5, SIV-P8 towers) are stated for the checked ranges only and are not extrapolated.
- Betti changes beyond graph level (O4), reachability of activation families (O6) and effective onset laws (O5) are open.
- Errata B2-T7 and B2-T9 are not used.

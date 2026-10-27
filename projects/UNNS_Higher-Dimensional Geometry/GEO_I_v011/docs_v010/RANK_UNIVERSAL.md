# GEO-I v010 — Programme C: universal rank three? (G10-C1, G10-C2, G10-T5, G10-T6)

**Question.** Is `r_min = 3` for every minimal non-embedded 0/1 box, at every nullity?

**Established.**
* G10-T5 (= G10-L5, PROVED): a double two-circuit decomposition of one word yields a collision of generator rank exactly 3 (B-COMMON + B-LOW).
* G10-C1′ (PROVED): *if* every minimal box has W2 (two distinct two-circuit partitions of the all-ones word), then `r_min = 3` universally.
* G10-T4 (PROVED+CHECKED): W2 and rank 3 hold for every minimal box of nullity ≤ 6 (215 classes at nullity 6). So **a rank-4 minimal box needs nullity ≥ 7.**
* G10-T6 (PROVED): the structural reduction of §1 of `MATHEMATICS.md`: E1, F1, A1, rigidity, counting identity.

**Open.** G10-C1 (W2 in general) and G10-C2 (a rank-4 minimal box). Adversarial searches found no counterexample: 2 × 1500 random supports at nullity 7 (≈ 1200 minimal each, W2 always, minimum 48 / 54 two-blocks), hill-climbing (best 45), random graphic cut spaces (nullity ≤ 5 only), and the `K_{2,t}` family (`t ≤ 10`). The consequence is a *uniform bound on the dimension needed to detect a defect, if W2 holds*; the evidence is consistent with it but is not a proof, and a rank-4 counterexample would be equally informative.

**Why W2 may be provable.** By rigidity (G10-R) the only non-unique word is `1`, and the counting identity expresses the number of disjoint circuit families through the number `β` of partitions of `1`; W2 asks `β` to contain two *two*-block partitions. A proof would need to show that a partition of `1` into more than two circuits can be merged, which was not obtained.

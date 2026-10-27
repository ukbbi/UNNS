# GEO-I v010 — Report

**Question asked:** what would make v010 a breakthrough — complete planar stabilization, or universal rank-three obstructions (or a rank-4 counterexample)?

**What happened.**
1. *Planar, hollow part — closed.* The hollow-box complement `conv F ∖ U0 = int T1 ⊔ int T2` (v009: OPEN, CHECKED only) is now a theorem for all `d ≥ 5`, all units `2 ≤ s ≤ d−2`. The proof is short: the steps of the lower-left hull chain are Graver (reflection argument), their zonogon is tiled by cells, and the remainder above the upper path is `T1 ∪ T2` plus one cell. It rests on the hull chain, not on Euclid's algorithm; the Euclid-style transfer rules R-MIR, R-EUC, R-LAT were tested against the true cells and are **false**. Consequences: `β1 = 2`, and G8-R1 becomes unconditional (the enlarged square hull is covered).
2. *Planar, cap — not closed.* A bounded attempt using the same chain idea on the enlarged hull did not give a uniform cover. G10-T2 stays OPEN, so G10-T3 stays OPEN. The conditional chain is now one step: G10-T2 ⇒ `U = H`.
3. *Binary — structure, not yet universality.* A partition criterion (non-embedded ⇔ a set with two circuit partitions) is proved; the full-support property of minimal boxes (previously a conjecture) follows; minimal boxes live in affine hyperplanes; non-unique words are only `1`. With these, nullity six was classified: 215 minimal boxes, every one of rank 3, every one with ≥ 16 two-circuit partitions of `1`. Universal `r_min = 3` is reduced to W2 and remains open; a rank-4 box needs nullity ≥ 7 and was not found.
4. *Certification.* New BOUNDARY and RANK6 certificate kinds with a standalone checker; 675 certificates accepted; tampering rejected.

**Not a breakthrough claim.** The planar hollow-box theorem is a genuine closure of an open v004–v009 problem; the two other possible breakthroughs (cap, universal rank three) did not close. No priority claim is made (see `PRIOR_ART.md`).

**Corrections.** Legacy certificate count is 19 (not 20). v009's shipped `verify_full.json` was stale; v010 regenerates its own reports.

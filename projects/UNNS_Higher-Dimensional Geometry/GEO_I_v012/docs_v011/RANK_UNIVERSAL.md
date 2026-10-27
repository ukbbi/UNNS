# GEO-I v011 — Programme C: universal minimum rank three (G11-T4)

**Question (v010).** Is `r_min = 3` for every minimal non-embedded 0/1 box, at every nullity?
**Answer: yes (G11-T4, PROVED).**

* G11-T3 (PROVED+CHECKED): W2 holds for every minimal box (`CIRCUIT_PARTITIONS.md`).
* G10-L5 (inherited, PROVED): two distinct two-circuit decompositions of one word give a collision of generator rank exactly 3; B-LOW (inherited): rank ≥ 3.
* G10-C1′ (inherited, PROVED conditional on W2): hence `r_min = 3` for every minimal box and, deleting to a minimal sub-box (G9-T5), for every non-embedded box of the frozen binary 0/1 geometric model.

**Consequences.** (i) G10-C2 "a rank-4 minimal box exists" is **FALSE** in this model; the v010 implication `r_min ≥ 4 ⇒ ν ≥ 7` is vacuous. (ii) The dimension needed to detect a defect (rank of the witness) is uniformly bounded by 3 independently of the nullity: the high-dimensional complexity of the binary model is controlled by a small number of general mechanisms (rigidity ⇒ vector-space partition ⇒ Parseval). **Scope.** The frozen binary 0/1 geometric model only; the statement concerns the *minimum* witness rank, not individual higher-rank witnesses, and says nothing about other occurrence models.

**Not needed:** nullity-7 classification, the `K_{2,t}` induction (G10-K stays CHECKED).

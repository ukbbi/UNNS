# E2-P3 — Counterexamples and negative results (preserved)

## Genuine containment failures (all certificates verify independently)

* **Control C / E2-P1 family:** 77 S1 rows with target lattice Z³ (b′ ∈ {1,2}; primes {2,5,11}-type parity lattice b = 3). Witness (2/3,2/3,2/3) from the cell P((0,0,2);(0,1,−1),(1,0,−1)) and its coordinate permutations. Each is **essential** (full coordinate support, 2-dimensional cell, and CONTAINED in all three coordinate-face restrictions) — but the target lattice is trivial, so it is **not** a both-nontrivial specimen.
* **Pure-lattice failures** (target Z³, not claimed FIELD-I realizable): 22 (Λ̃,Q̃) pairs in the scan, e.g. x₃ ≡ x₁+x₂ (mod 3) in box (2,2,1) with witness (2/3,2/3,5/6).  See results/P3_3D.json.

## Negative / limiting results

* No planar containment failure in 9788 rows: CP3-A is **not refuted** but also **not proved** outside rectangular and inherited targets.
* Abstract invariants do not decide geometry: P2-A loses 8 of 11 old Graver edges yet U ⊆ U′; E2-P1 keeps all vertices yet U ⊄ U′ (three coordinates).
* E2-P2's planar window defect (ERRATA/E2_P2_ADDENDUM_003): the argument was incomplete for q₁ < q₂; no verdict changed.
* 337 pure-lattice and FIELD-I rows are UNAVAILABLE by explicit limit, never silently dropped (data/P3_SEARCH_LIMITS.json).

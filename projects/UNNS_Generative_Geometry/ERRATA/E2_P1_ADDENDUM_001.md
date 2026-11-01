# E2-P1 — Addendum 001 (append-only; the E2-P1 package is unchanged)
**Correction A — fibre/vertex inclusion does not imply lattice inclusion.**
E2-P1 report §4 ("vertices persist iff lattices are ordered") is stated too strongly. What E2-P1 proves (E2-6.1) is the forward implication, for a common box:
  Λ ⊆ Λ′  ⟹  F ⊆ F′.
The converse is false. Exact witness (checked by `src/lattice_transport.py`, three independent decision procedures, and by brute force on [−12,12]²):
  x = 484/3 and x′ = 484/7, primes (2,11), box [0,1]²: both fibres are {(1,1)} (D = {22}), but Λ₃ = {a+b even} and Λ₇ = {a ≡ b mod 3} are INCOMPARABLE.
The reverse direction (F ⊆ F′ ⇒ ordered lattices) holds only under an extra hypothesis such as E2-4's "F spans Λ_b". That hypothesis must accompany every use. The 13 → 13 → 26 specimen, its counts and its counterexamples are unaffected.
Further, E2-P2 found genuine FIELD-I transitions (same primes and box) with F ⊆ F′ whose lattices SHRINK or are INCOMPARABLE (e.g. 1296/7 → 7776/35); see E2-P2 `results/P2_COUNTEREXAMPLES.json`.

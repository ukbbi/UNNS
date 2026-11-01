# E2-P1 — Addendum 002 (append-only)
**Correction B — abstract-cell survival needs target vertices as well as target generators.**
E2-P1 Theorem E2-6.2 ("a j-cell of K is a cell of K′ iff all its generators lie in G ∩ G′") holds as stated only when its vertices are already in F′, e.g. when Λ ⊆ Λ′ on a common box. The general statement is
  c ∈ K′  ⇔  V(c) ⊆ F′  ∧  Gen(c) ⊆ G′,
where Gen(c) are the generators of c at its lexicographically minimal vertex. For Λ ⊆ Λ′ the vertex condition is automatic and the criterion reduces to the Graver-generator condition, so the E2-P1 specimen and all its counts are unchanged. E2-P2 uses the general form (and tests it on every corpus row: `cell_prediction_exact`).

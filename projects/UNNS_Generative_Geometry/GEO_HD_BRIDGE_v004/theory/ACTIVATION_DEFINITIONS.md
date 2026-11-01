# Definitions (A4)

**Common coordinate embedding.** A relation is a vector in universal sparse exponent coordinates `g ∈ ⊕_p Z` (prime ↦ exponent). For `d∈D` put `e(d)=` its exponent vector. Vectors at different states are comparable without any box or lattice reference.

**Realised pairs.** `E_g(x) = {(u,v)∈D(x)² : e(v)−e(u)=g}`. A relation `g` is *active* at `x` if `E_g(x)≠∅`, *dormant* if `E_g(x)=∅`.

**Existing primitive relation.** `g ∈ Gr(x)` = region-Graver set of `x` (conformally minimal non-zero vectors of `Λ_b` inside `[−q,q]`), written in universal coordinates. v003 split: positive-primitive / edge-realised / dormant (`Gr∖` realised).

**Activation event (arithmetic).** `E_g(x)=∅`, `E_g(y)≠∅`. Without more it is an **arithmetic activation comparison** — a statement about two numbers.

**Dynamical activation.** The same event with `x→y` an *admissible transformation*: either a finite chain of actual FIELD-I steps `y=C^n(x)`, or a frozen SELECT-II integer edge. Only these two are admitted. Two levels:
* **step activation**: `y=C(x)`, `g∈Gr(x)`, `E_g(x)=∅≠E_g(y)`;
* **trajectory activation**: `y=C^n(x)`, `g∈Gr(x_m)` dormant at some `m<n`, `E_g(x_n)≠∅`; intermediate states may have left the lattice of `g` (excursion).

**Creation vs activation.** `g` is *created-and-realised* when `E_g(x_n)=∅≠E_g(x_{n+1})` but `g∉Gr(x_n)` (new coordinate, box growth or modulus change). Only `g∈Gr(x_n)` counts as activation of a previously existing primitive relation.

**Complexes.** `K_move(x)` = cubical complex of `F(x)` with the region-Graver moves = the frozen GEO-I "move" complex (cells `P(u;g_1..g_j)`, all vertices in `F`). `K_axis(x)` = same with axis moves. We do **not** identify `K_move` with the full realised GEO-I complex `K_real` of earlier work, nor with any history-recombination complex (A4-T7).

**Statuses.** PROVED, PROVED-SCOPED (proved under the stated hypotheses), FINITE-EXACT (exact on the listed finite range, no extrapolation), COUNTEREXAMPLE, OPEN, NOT-TESTED.

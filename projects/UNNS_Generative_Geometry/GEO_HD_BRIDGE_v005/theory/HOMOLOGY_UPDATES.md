# A5-T4 / A5-T7 — Predictive homology update and event types

Input: a D-event `D→D′` (D⊂D′, from Lemma M) with `N=D′∖D`. Complexes `K=K(D)`, `K′=K(D′)`, survivors `K°=K∩K′` (MOVE_TRANSITIONS A5-T3.2), `Dead_j=cells(K)∖cells(K′)`, `New_j=cells(K′)∖cells(K)`. Field F fixed (GF(2) and GF(2³¹−1) agree on all tested data).

## Theorem A5-T4.1 (zig-zag identity) — PROVED
Let `r_i=rank(H_i(K°)→H_i(K))`, `r′_i=rank(H_i(K°)→H_i(K′))`, `h_i=dim H_i(K,K°)`, `h′_i=dim H_i(K′,K°)`. Then
  `β_i(K) = r_i + h_i − β_{i−1}(K°) + r_{i−1}` and the same for K′, hence

  **Δβ_i = (h′_i − h_i) + (r′_i − r_i) + (r′_{i−1} − r_{i−1}).**

*Proof.* Long exact sequence of (K,K°): `β_i(K)=dim im(ι_i)+dim im(j_i)`, `dim im(j_i)=dim ker(∂: H_i(K,K°)→H_{i−1}(K°)) = h_i − (β_{i−1}(K°)−r_{i−1})`. Subtract the same identity for K′; `β_{i−1}(K°)` cancels. ∎
By excision `h_i=dim H_i(Dead-part rel survivors)` and `h′_i=dim H_i(New-part rel survivors)` are **local**: they involve only dead cells, new cells and their attaching faces. The terms `r,r′` are the only global ones (they see H(K°)). Euler characteristic needs no global term: **Δχ = Σ_j (−1)^j (|New_j|−|Dead_j|)**.
*Audit (FINITE-EXACT).* On all 2,576 events the identity and the reconstruction of β(K), β(K′) from (r,h,β(K°)) hold with 0 exceptions (Z4).

## Theorem A5-T4.2 (a topology change always has a cause) — PROVED
* `Δβ_i<0 ⇒ Dead_i≠∅ or New_{i+1}≠∅`  (a cycle can only vanish by losing an i-cell, or by acquiring a new (i+1)-cell that bounds it);
* `Δβ_i>0 ⇒ New_i≠∅ or Dead_{i+1}≠∅`.
*Proof.* If `Dead_i=New_{i+1}=∅` then `Z_i(K)⊆Z_i(K′)` and `B_i(K′)=B_i(K)`. ∎
In arithmetic terms: **destruction of i-dimensional homology needs either an old i-cell pierced by a new occurrence (A5-T3.2.2) or a new occurrence closing a new (i+1)-cell.** (Z4: holds for every β₁ drop of the census: 176 drops, each has a dead edge or a new 2-cell; none has neither.)

## Corollary A5-T4.3 (nested events) — PROVED
If `Dead=∅` (K⊂K′): `Δβ_i = h_i(K′,K) − k_i − k_{i−1}`, `k_i=dim ker(H_i(K)→H_i(K′))`: classes created relative to K minus classes killed. The G=5/G=11 tower transitions are of this kind (TOWERS.md).

## Theorem A5-T4.4 (exact predictive update at graph level) — PROVED + FINITE-EXACT
If neither K nor K′ has 2-cells: `Δβ₁ = ΔE − ΔV + Δβ₀` with `ΔV=|N|`, `ΔE=|NewEdges|−|Pierced|`, where `Pierced` and `NewEdges` are computed from the old edge set and N by the interval rule, and `Δβ₀` by union–find on `E(K)∖Pierced ∪ NewEdges`. `predict_graph_update` does this **without building K(D′)**. Exact on 175/175 graph-level census events and on random divisor sets (Z5).
*Control (the proved A4 family):* `D={P}→D(y)`, `N={p_iq}`, `Pierced=∅`, `NewEdges=C(k+1,2)`, `ΔV=k`, `Δβ₀=0` ⇒ `Δβ₁=C(k+1,2)−k = k(k−1)/2` — the v004 value, now obtained from the transition law.
*Limit.* For complexes with 2-, 3-cells only the local terms `h,h′` and the cause criteria are arithmetic; `r,r′` require H(K°). This release does **not** claim a rebuild-free Betti prediction in higher dimension.

## A5-T7 — event types (FINITE-EXACT census + PROVED structure)
Types as in the spec: I (nothing changes), II (some β up, none down), III (down), IV (mixed), V (Betti unchanged, complex changed).
* **PROVED:** a D-event adds a vertex, so **Type I never occurs among D-events**; every “activation without topological change” is Type V (the complex changes, Betti does not).
* **Census (ℓ=5,7,11,13; S<1500; 24 steps; 382 orbits; 2,576 D-events):** Type V 1,787 · II 603 · III 172 · IV 14. Edge deaths in 251 events (max 16 in one event); 2,325 events are nested (Dead=∅). β₂ changes in 246 events, β₃ in 1.
* **Mechanism table for β₁** (dead edge?, new 2-cell?) → (up/same/down): (no,no)→ 178 up / 27 same / 0 down · (no,yes)→ 210 / 1,865 / 45 · (yes,no)→ 0 / 2 / 0 · (yes,yes)→ 0 / 118 / 131. The empty “down” cell of (no,no) is the proved theorem A5-T4.2 (the (yes,no) row has only 2 events); the **zero “up” in both dead-edge rows is a census regularity, not a theorem**: in the abstract calculus a pierced edge with β₁ *increase* exists (`D={56,21,32,45}`, `N={51,15,11}`: β=(1,0)→(2,1), one dead edge) — COUNTEREXAMPLE to promoting the regularity to a law of the calculus; whether it can occur dynamically is OPEN.
* v004 cross-check (Z8): all 474 step-activation events reproduced (Betti before/after) by this independent engine; of the 57 β₁ drops all 57 contain a dead edge and 57/57 a new 2-cell.
* No arithmetic predicate `𝒜(x)` ⇒ Type is claimed (A5-T7 target). What is proved is the *form* of the answer: Type is determined by (K(D), N); N is arithmetic (stage sieve); the dependency of Type on the arithmetic of N beyond that is OPEN.

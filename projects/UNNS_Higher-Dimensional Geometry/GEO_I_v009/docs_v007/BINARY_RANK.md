# GEO-I v007 — Programme B: binary 0/1 boxes and obstruction rank

## 0. Result

`r_min ≤ 3` for every minimal non-embedded binary 0/1 box (**G7-C2**) is **still OPEN**: no proof, no counterexample. What v007 adds is an exact structural theory of the collisions that reduces the question to a small combinatorial problem and a larger exhaustive evidence base:

| ID | Statement | Status |
|---|---|---|
| G7-B1 (B-DELTA) | witness rank = rank of the generators of the two cells (`δ` is automatically in their span); ≤ r+t | PROVED+CHECKED |
| G7-B2 (B-COSET) | the cells with union `U` are exactly `(partition S of U into circuits, nonzero coset of span(S) in the code)` | PROVED+CHECKED |
| F1 | every collision is between cells with ≥ 2 circuits each (no segment collisions) | PROVED+CHECKED |
| F2 (B-MIN) | in a minimal box every collision has `x ≡ 1` outside `U` | PROVED |
| G7-B3 (B-NULL) | a full-support collision (`U = [n]`) forces nullity `n − rank M ≥ 3`; two cells with union `[n]` always collide | PROVED+CHECKED |
| B-ATOM | for `r = t = 2`, full support: generator rank ≤ 3 iff some connected component of the atom graph is `z`-constant with consistent signs | PROVED+CHECKED |
| G7-C2 | `r_min ≤ 3` | **OPEN** (CHECKED: n ≤ 6 complete; n = 7 complete under FS; n = 8 restricted) |

Acceptance label for Programme B: **B-PARTIAL** (reduction theorems proved; the rank bound is not).

## 1. Setting (v006, unchanged)

Columns `c₁..c_n ∈ F₂^m` (nonzero), code `C = ker M ⊆ F₂ⁿ`, box `1ⁿ`, `F` = nonzero codewords as 0/1 vectors. Circuits = minimal nonempty supports of codewords. By v006 Lemma B1 the cells of dimension ≥ 1 are `P(x; S₁..S_r)`: `x ∈ C`, `S_j` pairwise disjoint circuits, generator `g_j = (1−2x_i)_{i ∈ S_j}`, corners `x ⊕ f`, `f ∈ span(S) := {⊕_{j∈J} S_j}`, all nonzero. v006 Theorem B2: two cells `P(x;S)`, `P(y;T)` have intersecting relative interiors iff `U := ∪S_j = ∪T_l` and `x = y` outside `U` (common point `z = (½ on U, x outside U)`). A *minimal box* is non-embedded with every coordinate deletion embedded (deletion of `i` = restriction to codewords supported off `i`). A *witness* of a collision is `(A,B,δ)`, `δ = y − x`; its **rank** is `rank{generators of A, of B, δ}`.

**Four rank notions, kept separate.** For a box: `r_max` = max rank over all witnesses (parity 6: 6); `r_irr` = rank restricted to v005-irreducible witnesses (inherited definition; parity 5 has irreducible rank 4); `r_min` = min rank over all witnesses of that box; `r_min^{minimal}` = `r_min` for **minimal** boxes — the quantity G7-C2 bounds. `r_min ≤ r_max` always; `r_irr` is a different restriction and is not ordered against `r_min` by definition. Parity 5 (`1⁵`): witnesses of rank 3 (75) and 4 (15), so `r_min = 3`, `r_max = 4`; it is **not** minimal (its deletion `1⁴` is non-embedded).

## 2. Theorems with proofs

**B-COSET.** *The cells with union `U` are in bijection with pairs `(S, x + span(S))` where `S` is a set of pairwise disjoint circuits with union `U` and `x + span(S)` is a coset of `span(S)` in `C` different from `span(S)`.* Proof. A cell is determined by its corner set `x + span(S)` (corners `x⊕f` are distinct because the `S_j` are disjoint, so `|span S| = 2^r`). The corners are nonzero iff `x ∉ span(S)`. `S` is recovered from `span(S)`: its minimal nonempty supports are exactly the `S_j` (a nonempty XOR of a subfamily has support equal to the union of that subfamily). Different `x` in one coset give the same cell. ∎ (`theory/binary_circuits.py`; cross-checked against `binary_01.cells_01` on every tested box; independent re-implementation in `certificates/checker.py`.)

**Collision criterion restated.** Two distinct cells `(S,x)`, `(T,y)` collide iff `∪S = ∪T = U` and `x|_{[n]∖U} = y|_{[n]∖U}` (the restriction is constant on a coset since flips lie in `U`). In particular, **two distinct cells with union `[n]` always collide**.

**F1.** *If `A`, `B` collide then `r,t ≥ 2`.* If `r = 1`, `S₁ = U` is a circuit; every codeword supported inside `U` is `0` or has support exactly `U` (circuit minimality), so `t = 1`, and `x ⊕ y` (a codeword supported in `U`) is `0` or `U`, i.e. `y ∈ x + span(S)`: the cells coincide. ∎

**F2 (B-MIN).** *In a minimal box every collision has `x_i = 1` for all `i ∉ U`.* If `x_i = 0` for some `i ∉ U`, every corner of both cells has `i`-th coordinate `0` (flips lie in `U`), the circuits avoid `i`, so both cells exist in the deletion of `i` and still collide: that deletion is non-embedded, contradicting minimality. ∎

**B-DELTA.** *The witness rank equals `rank{g_1..g_r, h_1..h_t}` and is `≤ r+t`.* On `U`: `δ = y − x = (s_x − s_y)/2` with `s_x = 1−2x = Σ_j g_j` and `s_y = Σ_l h_l`; outside `U`, `δ = 0`. So `δ ∈ span(g,h)`. (Replacing the base corners by other corners changes `δ` by an element of the span.) ∎ This turns witness rank into the rank of a sign-pattern matrix.

**B-NULL.** *If the box has a collision with `U = [n]` then `dim C = n − rank(M) ≥ 3`.* Let the cells be `(S,x) ≠ (T,y)`, `r,t ≥ 2` (F1). If `S = T`: `x, y` lie in different cosets of `span S` in `C`, with `span S` itself a third coset: `|C| ≥ 3·2^r`, so `dim C ≥ r+2 ≥ 4`. If `S ≠ T`: `span S ≠ span T` are both subspaces of `C` of dimension `r, t ≥ 2`, so `dim(span S + span T) ≥ max(r,t)+1 ≥ 3`. ∎ Hence a complete census of boxes with a full-support collision on `n` coordinates needs only `m = rank M ≤ n−3`.

**B-ATOM (r = t = 2, `U = [n]`).** Write `S = {S₁,S₂}`, `T = {T₁,T₂}`, atoms `S_i ∩ T_j`, `z = x ⊕ y`, `ε_k = 1 − 2z_k`. A linear dependency `α g₁ + β g₂ = γ h₁ + δ' h₂` reads, in coordinate `k` of atom `(i,j)`, `α_i = ε_k γ_j` (writing `(α₁,α₂) = (α,β)`, `(γ₁,γ₂) = (γ,δ')`). Form the bipartite graph on `{S₁,S₂,T₁,T₂}` with one edge per nonempty atom. If `z` is not constant on an atom, both endpoints are forced to `0`, and zero propagates along every incident edge; if `z` is constant the edge says `α_i = ε γ_j`. So a nonzero solution exists iff some connected component has only constant atoms and consistent signs around its (at most one, a 4-cycle) cycle; for the 4-cycle the sign condition is `ε₁₁ε₂₂ = ε₁₂ε₂₁`. ∎ `rank_reduction.atom_criterion` implements this; it agrees with the directly computed rank on **all 57,219** `(2,2)` full-support collisions of all non-embedded boxes with `n ≤ 7`, `m ≤ n−3` (including 8,496 same-partition collisions).

## 3. Why the open question is hard

For a minimal box, `U = [n]` in every collision found; so the box has two cells with union `[n]`, i.e. two circuit partitions `S ≠ T` of `[n]` (or one partition with two cosets) and `r,t ≥ 2`. `r_min ≤ 3` then amounts to: *some* colliding pair of such cells has a dependency among its `r + t` generators. By B-ATOM this is a statement about how the partitions `S,T` and the codeword `z = x ⊕ y ∈ C` interact: for `r = t = 2` one needs a component of the atom graph on which `z` is constant. No argument that this must happen in a *minimal* box was found; deletion-minimality is a global condition on all coordinate deletions and is only used through F2. The `(r,t) = (2,3)` collisions (e.g. columns `1,1,2,2,3,3`) show that collisions with a 3-circuit cell occur in minimal boxes (alongside `(2,2)` collisions); a rank-3 witness existed in every minimal box found.

## 4. Computation

`experiments/rank_counterexamples.py N MMAX OUT` enumerates all multisets of `N` nonzero columns of rank `m ≤ MMAX` in `F₂^m`, tests minimality (`binary_01.minimal_nonembedded`), and records the minimum witness rank, the nullity and the collision types.

| n | columns searched | minimal boxes | by min rank | nullity | label |
|---|---|---|---|---|---|
| 4 | rank ≤ 1 | 1 | {3:1} | {3:1} | complete |
| 5 | rank ≤ 2 | 3 | {3:3} | {3:3} | complete |
| 6 | rank ≤ 3 (v006: ≤ 5) | 50 | {3:50} | {3:49, 4:1} | complete (v006 data: all ranks) |
| 7 | rank ≤ 4 | 2983 | {3:2983} | {3:2940, 4:43} | complete among nullity ≥ 3; complete under FS |
| 8 | rank ≤ 4 only | 5902 | {3:5902} | {4:5895, 5:7} | **restricted — not complete** |
| 9 | rank ≤ 3 only | 0 (4687 sets) | — | — | restricted (no minimal box exists at rank ≤ 3 for n = 9) |

**FS** = "every minimal box has a full-support collision". It is *observed* in every minimal box found (all collisions of all of them have `U = [n]`) but not proved; F2 only shows that a counter-example to FS would have `x ≡ 1` off `U`. Consequently the `n = 7` row is complete only for boxes of nullity ≥ 3 (equivalently for boxes with a full-support collision, B-NULL) and the `n ≥ 8` rows are restricted. Collision types seen: `(2,2)`, `(2,3)`, `(2,4)`; no minimal box with only non-`(2,*)` collisions. **No minimal box with `r_min ≥ 4` was found.** (A counterexample would need the six-point certificate: exact `M` and box, non-embedded, coordinatewise minimal, every lower-rank witness excluded, a rank ≥ 4 witness, the exact intersection point; `certificates/D2_rank.json` is the format, checked by `certificates/checker.py`.)

Regressions (unchanged, re-run by `verify.py`): parity 4 (3 witnesses, rank 3, minimal), parity 5 (90 witnesses, spans `{3:75, 4:15}`, not minimal), parity 6 (1440 witnesses, spans `{3:360,4:315,5:585,6:180}`; v006 complete census n = 6), the mod-24 example `b = 24` residues `(5,7,13,23)` (first obstructions `(4,1,1,1)`, `(3,2,1,1)`, planar span 2), all inherited from v005/v006 and not relabelled as new.

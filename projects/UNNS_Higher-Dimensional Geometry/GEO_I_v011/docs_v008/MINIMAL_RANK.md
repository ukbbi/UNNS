# GEO-I v008 — Programme C: minimal binary obstructions and the rank bound

Setting (v006/v007, unchanged): columns `c_1..c_n ∈ F_2^m` (nonzero), code `C = ker M`, box `1^n`, cells = (partition `S` of `U` into pairwise disjoint circuits, nonzero coset `x+span(S)` in `C`), collision of `(S,x) ≠ (T,y)` iff `∪S = ∪T = U` and `x = y` outside `U` (B-COSET, centre criterion), witness rank = rank of the generators of the two cells (B-DELTA). A box is *minimal* if non-embedded with every coordinate deletion embedded. `r_min` = minimum witness rank over all witnesses of the box.

## 0. Registry

| ID | Statement | Status |
|---|---|---|
| **B-NULL′** | *any* collision (not only full-support) forces nullity `n − rank M ≥ 3` | **PROVED** |
| **B-BASIS** | a box of rank `m` is `GL_m(F_2)`-equivalent to `(e_1..e_m) + (n−m)` extra columns; so basis + extra-multiset enumeration is exhaustive | **PROVED** |
| **B-LOW (G8-T3a)** | every collision witness has rank ≥ 3; hence `r_min ≥ 3` for every non-embedded box | **PROVED** |
| **B-COMMON** | if `S ≠ T` are circuit partitions of `[n]` and `x ∈ C ∖ (span S ∪ span T)`, cells `(S,x),(T,x)` collide with witness rank `≤ r+t−1` (`= 3` for `r=t=2`) | **PROVED** |
| **B-SERIES** | parallel (series) classes: circuits, cells, collisions, ranks and minimality of a box are those of its reduced box; minimal boxes are exactly blow-ups of reduced minimal boxes with all coordinates in some circuit | **PROVED+CHECKED** (404 blow-ups, 0 discrepancies) |
| **G8-T3b** | every minimal box of nullity 3 or 4 (all `n`) has `r_min = 3`; classification: nullity 3 = blow-ups of the parity-4 code; nullity 4 = blow-ups of three reduced codes with `p = 6, 7, 8` | **PROVED+CHECKED** (finite classification + B-SERIES; two independent paths agree for `n ≤ 8`) |
| **G8-T3c (RM family)** | for every `k ≥ 3` the box of `RM(1,k−1)` (`n = 2^{k−1}`, nullity `k`) is minimal non-embedded, and `r_min = 3` | **PROVED** (+CHECKED `k = 3,4,5`) |
| G8-C3′ (common base) | every minimal box has two partitions of `[n]` into two circuits and a common base `x` | **OPEN**; CHECKED all minimal boxes `n ≤ 8` (complete); n = 9 also (1,757 of 1,757) |
| G8-C3 | every minimal box has a full-support collision (FS) | **OPEN**; CHECKED `n ≤ 9` complete (all collisions of all minimal boxes are full-support) |
| G8-T3 | `r_min ≤ 3` for every minimal box | **OPEN** (proved for nullity `≤ 4` and for the RM family; complete census `n ≤ 9` finds no rank ≥ 4) |

Benchmarks preserved (not recounted as v008 results): parity 4 (minimal, 3 witnesses, rank 3), parity 5 (90 witnesses, ranks `{3:75, 4:15}`, not minimal), parity 6 (1440 witnesses), the 7D conditional and 8D restricted qualifications of v007 as stated historically.

## 1. Proofs

**B-NULL′.** Let `(S,x) ≠ (T,y)` collide, `r,t ≥ 2` (v007 F1). If `S ≠ T`: `span S ≠ span T` are subspaces of `C` of dimensions `r,t ≥ 2`, so `dim(span S + span T) ≥ max(r,t) + 1 ≥ 3`. If `S = T`: `span S`, `x+span S`, `y+span S` are three distinct cosets of `span S` in `C` (`x,y ∉ span S` because corners are nonzero, and `x⊕y ∉ span S` because the cells differ), so `|C| ≥ 3·2^r`, `dim C ≥ r+2 ≥ 4`. The argument uses only the subspaces `span S, span T ⊂ C`, never `U = [n]`. ∎

**B-BASIS.** The box depends only on `C = ker M`. If `rank M = m`, choose `m` independent columns; a change of basis of `F_2^m` sends them to `e_1..e_m`; `ker M` is unchanged; permuting coordinates puts them first. Remaining `n−m` columns are an arbitrary multiset of nonzero vectors. By B-NULL′, `m ≤ n−3` suffices. ∎ (`experiments/rank_attack.py`)

**B-LOW.** Let `(S,x) ≠ (T,y)` collide, generators `g_1..g_r` (disjoint supports, independent), `h_1..h_t`, `r,t≥2`. Suppose the rank is 2. Then `r = 2` and each `h_l ∈ span(g_1,g_2)`, `h_l = α g_1 + β g_2` with entries in `{0,±1}`. If `α,β ≠ 0` then `supp h_l = S_1 ∪ S_2 = U`, so `T_l = U`, contradicting `t ≥ 2`. So `h_l = ±g_{j(l)}`, `T_l = S_{j(l)}`, hence `T = S` and `y|_{S_j} ∈ {x|_{S_j}, 1−x|_{S_j}}` for each `j`, i.e. `y ∈ x + span S`: the two cells coincide. Contradiction. ∎

**B-COMMON.** For `(S,x), (T,x)` with common `x` and `∪S = ∪T = [n]`: `Σ g_j = 1 − 2x = Σ h_l` on `[n]` (for a union `U` the same identity holds on `U`), a nontrivial linear dependency among the `r+t` generators; so rank `≤ r+t−1`. Cells exist iff `x ∉ span S`, `x ∉ span T`; they are distinct as `S ≠ T` and collide by the centre criterion. ∎

**B-SERIES.** Call `i ~ j` *parallel* if `c_i = c_j` for every codeword `c ∈ C` (equal columns of a generator matrix of `C`). Every codeword is constant on classes, so `C` is the pull-back of a code `C_red ⊂ F_2^p` on the `p` classes. Supports are unions of classes, so circuits of `C` are the blow-ups of circuits of `C_red`; cells `(S,x)` correspond bijectively (corner sets are blown up); the collision condition "same `U`, `x` equal outside `U`" is invariant (constant on classes). Generators are blown-up vectors, i.e. have duplicated coordinates, so ranks are unchanged. Deleting coordinate `i` restricts to codewords vanishing on the whole class of `i`; the other class members become identically-zero coordinates, which do not influence cells or collisions; so the deletion equals the class deletion of `C_red`. Hence embeddedness, minimality and the multiset of witness ranks agree. A coordinate that is zero on all codewords can be deleted without changing the box, so it cannot occur in a minimal box. ∎ (`theory/binary_min.py`, `theory/rank_reduce.py:check_series_invariance`)

**G8-T3b (nullity ≤ 4).** By B-NULL′ every non-embedded box has nullity `≥ 3`. A minimal box of nullity `k` is the blow-up of a reduced minimal box (B-SERIES) whose code has dimension `k` and whose coordinates are `p` *distinct nonzero* generator columns spanning `F_2^k`: a spanning subset `Σ ⊂ F_2^k ∖ {0}`. Up to `GL(k,2)` (orbit enumeration by union-find on the generating transvections; `theory/binary_min.py:support_orbits`) and exact tests of non-embeddedness, minimality and witness ranks:
* `k = 3`: **one** orbit (`p = 4`, the affine-plane complement; = the parity-4 code), min rank 3;
* `k = 4`: **three** orbits, `p = 6, 7, 8` (orbit sizes 420, 120, 15), min rank 3; the `p = 8` orbit is `RM(1,3)`.
Therefore every minimal box of nullity 3 (resp. 4) is a blow-up of the 1 (resp. 3) reduced codes and has `r_min = 3` (B-SERIES + B-LOW). The count `7·C(n−1,3)` of labelled nullity-3 minimal boxes found in exploration is the number of (orbit member, composition of `n` into 4 positive parts). *Independent validation:* `tests/check_nullity_classification.py` compares, for `n ≤ 8`, the set of code invariants produced by blow-ups of the classification with the set found by the unrelated basis+extras enumeration of rank `n−k`: equal in every case (`ALL EQUAL`). ∎ (finite computations: `output/data/v8_nullity34.json`).

**G8-T3c (RM family).** Let `Σ_k = {x ∈ F_2^k: x_k = 1}` (`2^{k−1}` points), `C = {(u·x)_{x∈Σ_k}: u ∈ F_2^k}` (dimension `k`, contains `1`, weights `0, n/2, n`). *Circuits:* the codewords of weight `n/2` (`u ∉ {0, e_k}`), minimal because every nonzero codeword has weight `≥ n/2`. For `u ∉ {0,e_k}`, `supp(u)` and `supp(u+e_k)` are complementary circuits: a partition of `[n]` into two circuits. *Non-embedded* (`k ≥ 3`): two partitions from `u,u'` with `e_k,u,u'` independent are distinct, cells exist because `dim C ≥ 3`, and two distinct cells with union `[n]` always collide (v007). *Minimal:* deleting a coordinate `x_0` leaves the code `{u : u·x_0 = 0}` whose reduced box is the simplex code (all `2^{k−1}−1` nonzero points of `F_2^k/⟨x_0⟩`; no two points are parallel since `x+y = x_0` is impossible for `x,y ∈ Σ_k`). In the simplex code any two distinct codewords have intersecting supports (all weights `2^{k−2}`, pairwise intersections of size `2^{k−3} > 0` for `k ≥ 3`), hence no cell has `r ≥ 2`; by F1 (collisions need `r,t ≥ 2`) the box is embedded. *Rank:* for `k ≥ 4` choose `u,u'` with `e_k,u,u'` independent and `x ∈ C ∖ span(e_k,u,u')`; B-COMMON gives rank 3, and B-LOW gives `≥ 3`. For `k = 3` the box is the parity-4 code (class orbit above). ∎ (`theory/binary_min.py:rm_support, common_base_witness`; exact checks `k = 3,4,5`).

## 2. Computation (exact; two labels kept apart)

`experiments/rank_attack.py N [MMAX] OUT` enumerates basis+extras (B-BASIS) with `MMAX = N−3` (complete). Counts are **representatives of the basis+extras enumeration**, not comparable with v007's raw column-multiset counts (1, 3, 50, 2983, 5902) or with v006.

| n | representatives tested | non-embedded | minimal | min-rank histogram | distinct code-invariant classes | label |
|---|---|---|---|---|---|---|
| 4 | 1 | 1 | 1 | `{3:1}` | 1 | complete |
| 5 | 11 | 6 | 3 | `{3:3}` | 1 | complete |
| 6 | 100 | 37 | 11 | `{3:11}` | 3 | complete |
| 7 | 912 | 279 | 50 | `{3:50}` | 5 | complete |
| 8 | 9,007 | 2,712 | 273 | `{3:273}` | 11 | complete |
| 9 | 102,645 | 33,983 | 1,757 | `{3:1757}` | 16 | complete |

(see `output/data/v8_rank_n*.json` for all counts). In all of them: every collision of every minimal box is full-support, and every minimal box has a `(2,2)` collision of rank 3. Because the census is now complete through `n = 9` (B-NULL′ makes `m ≤ n−3` exhaustive), the v007 qualifications "7D conditional on FS" and "8D restricted" are **superseded for `n ≤ 9`**: complete lists exist; they stay recorded as historically stated in v007.

## 3. What remains

G8-T3 in general. The mechanism found (`B-COMMON`) reduces it to a structural statement (G8-C3′): *every minimal box contains two circuit partitions of `[n]` into two circuits sharing a base `x`*; it holds in every minimal box with `n ≤ 8` and is proved for the nullity-3, nullity-4 and RM families. A counterexample to G8-T3 would need a minimal box with *every* witness of rank ≥ 4, i.e. an exhaustive exclusion of all rank-3 witnesses (RANK certificate); none has been found.

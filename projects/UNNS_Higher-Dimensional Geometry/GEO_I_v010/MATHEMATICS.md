# GEO-I v010 — Mathematics: registry and proofs

Statuses: **PROVED**, **PROVED+CHECKED**, **CHECKED**, **FALSE**, **CORRECTED**, **OPEN**, **UNAVAILABLE**. A failed proof is never recorded as a falsification; a numerical pattern is never recorded as a theorem. Definitions of GEO-I v001–v009 are used unchanged (the v009 mathematics, which contains the v008 mathematics as its Section A, is kept verbatim in `docs_v009/MATHEMATICS.md`).

## 0. Registry (v010)

| ID | Statement | Status |
|---|---|---|
| **G10-Z** | zonogon theorem: for `d ≥ 5`, units `2 ≤ s ≤ d−2`, `H0 = conv F ⊆ Z ∪ T1 ∪ T2 ∪ K`, with `Z` the zonogon on the hull steps (tiled by Graver cells) and `K` one Graver cell | **PROVED+CHECKED** (§2; exact check all 6560 unit pairs `d ≤ 150`) |
| **G10-T1 = G9-C1** | `H0 ∖ U0 = int T1 ⊔ int T2` for `d ≥ 5`, `2 ≤ s ≤ d−2` (and `d = 3, 4`: only `s ≡ ±1`) | **PROVED+CHECKED** |
| **G10-T1H = G9-T1H** | `β1(U0) = 2` for the same `(d,s)` | **PROVED+CHECKED** (Alexander duality, §2.5) |
| **G10-R1** | `H0 ⊆ U_Q` for every `Q ≥ (d,d)`, `Q ≠ (d,d)`, `d ≥ 5`, `s ≢ ±1` (G8-R1 made unconditional) | **PROVED+CHECKED** |
| G10-S1, G10-S2 | explicit closed-form covers for `d ≡ 1 (mod s)` and `d ≡ −1 (mod s)` (direct or transposed) | **PROVED+CHECKED** (corollaries of G10-Z; 1276 pairs `d ≤ 150`) |
| G10-L1 | modular sail theorem (hull steps are Graver; zonogon tiling) | **PROVED** (§2.1–2.3) |
| G10-L2 | candidate Euclidean cell-transfer rules | R-SYM holds (100 pairs `d ≤ 18`); **R-MIR, R-EUC, R-LAT FALSE** (counterexamples stored) |
| **G10-T2** | cap: `C_Q = H_Q ∖ H_0 ⊆ U_Q` for nonexceptional small boxes | **OPEN** (CHECKED: 26,636 boxes `d ≤ 20` (v008) plus 10,110 boxes `d = 21..22` (v009)) |
| G10-L3, G10-L4 | cap lemmas (cell extension, corner compatibility) | **OPEN** — not proved (§3) |
| **G10-T3** | consolidated planar stabilization `U = H` | **OPEN** — valid only if T1 and T2 are both proved; T1 now is, T2 is not |
| **G10-E1** | exact criterion: a binary box is non-embedded iff one set `U` has two distinct partitions into circuits | **PROVED** (§1.1) + CHECKED against the cell engine |
| **G10-F1** | in a minimal non-embedded box every such pair has `U = [n]`; the all-ones word lies in `C` (this proves G8-C3 / FS) | **PROVED** (§1.2) |
| **G10-A1** | affine reduction: reduced support of a minimal box lies in a hyperplane `u0·σ = 1` of `F_2^k`; classes = `AGL(k−1,2)` orbits of spanning subsets of `AG(k−1,2)` | **PROVED** (§1.3) |
| **G10-R** | rigidity: in a minimal box every codeword other than `0, 1` has a unique decomposition into disjoint circuits; counting identity `#families = 2^k − 2 + #(partitions of 1)` | **PROVED** (§1.4) + CHECKED (215 classes) |
| **G10-L5 (= G10-T5)** | local rank-three extraction: a double two-circuit decomposition `a⊔b = c⊔d` of one word gives a collision of generator rank exactly 3 whenever nullity `≥ 3` | **PROVED** (§1.5) |
| **G10-C1′** | W2 (every minimal box has `≥ 2` two-circuit partitions of the all-ones word) ⇒ `r_min = 3` for all minimal boxes | **PROVED** (conditional statement, §1.5) |
| **G10-C1** | universal `r_min = 3` | **OPEN** |
| **G10-T4** | nullity six: 381 affine orbits, 350 spanning, 349 non-embedded, **215 minimal**, all rank 3, all W2 (minimum `16 = 2^{k−2}` two-blocks); hence every non-embedded box of nullity `≤ 6` has `r_min = 3` | **PROVED+CHECKED** (two independent paths, 0 disagreements) |
| G10-K | cut space of `K_{2,t}`: minimal non-embedded, nullity `t+1`, rank 3, `2^{t−1}` two-blocks (`t ≥ 3`) | **CHECKED** `t = 2..10`; general `t` not proved |
| **G10-C2** | rank-4 minimal box (would need nullity `≥ 7`) | **OPEN** — no counterexample in the adversarial searches (§4) |
| G10-T6 | general structural reduction (E1, F1, A1, rigidity) | **PROVED** — this is §1 |
| G10-B | BOUNDARY certificate kind + standalone checker | **PROVED+CHECKED** (453 certificates, tamper tests) |

Corrections to inherited statements (v010): **G8-C3 (FS) and G9-T5's reduction need no longer be conjectural: FS is the theorem G10-F1.** G9-C1 and G9-T1/T1H (OPEN in v009) are closed by G10-Z. Legacy certificate files: the v007 certificate files `D1`–`D3` contain **19** certificates (6 + 5 + 8; the v008 documents said 20); this correction is kept.

## 1. Binary boxes

Conventions (frozen, GEO-I v006–v009): a binary 0/1 box is the code `C = ker M ⊆ F_2^n`; a *circuit* is a minimal support of a nonzero codeword; every nonzero codeword is a disjoint union of circuits. A *cell* is `(S, x)`: `S` a set of pairwise disjoint circuits, `x ∈ C`, `x ∉ span S`, with `x` taken modulo `span S`; its *union* is `U = ∪S`. A *collision* is two distinct cells `(S,x)`, `(T,y)` with the same `U` and `x = y` off `U`. The box is *non-embedded* iff it has a collision. Deleting coordinate `i` means shortening (words vanishing at `i`, coordinate dropped). A box is *minimal* if it is non-embedded and every single deletion is embedded.

### 1.1 Theorem G10-E1 (partition criterion)
*A binary box is non-embedded iff some set `U` is a disjoint union of circuits in two distinct ways.*

*Proof.* (⇐) Let `S ≠ T` be partitions of `U` into circuits. If `span S = C`, every circuit `t ∈ T` is a sum of members of `S`; the members involved have supports inside `supp t`, so by minimality of `supp t` there is exactly one member and `t ∈ S`; hence `T ⊆ S`, and as both partition `U`, `T = S`, a contradiction. So `span S` and likewise `span T` are proper subspaces of `C`. A vector space over `F_2` is not a union of two proper subspaces, so there is `x ∈ C ∖ (span S ∪ span T)`. Then `(S,x)` and `(T,x)` are cells with the same union and the same `x` off `U`, and they are distinct because `S ≠ T` (a cell determines its circuit set). A partition by a single circuit `{U}` is the only partition of `U`, so only families of `≥ 2` circuits matter.
(⇒) Let `(S,x) ≠ (T,y)` be a collision with union `U`. If `S ≠ T` we are done. If `S = T`, the cosets `x + span S`, `y + span S` differ, but `c = x ⊕ y ∈ C` has support in `U`, and `c ∉ span S`. Decompose `c` and `1_U ⊕ c` (both codewords supported in `U`, with disjoint supports) into disjoint circuits; together they form a partition `S'` of `U`. If `S' = S`, then `c` is a sum of members of `S`, contradicting `c ∉ span S`. So `S' ≠ S`. ∎

Implemented independently of the cell engine in `theory/binary6.py` (`non_embedded`); `tests/test_geo10.py` and the cross-check records compare it with the cell engine on every spanning affine class of nullity 3, 4 and 5 (and a random sample), and on all 350 classes of nullity 6: **0 disagreements**.

### 1.2 Theorem G10-F1 (full support) — proves G8-C3
*In a minimal non-embedded box every pair of distinct partitions of one set has `U = [n]`; hence `1 = (1,…,1) ∈ C`.*

*Proof.* Let `S ≠ T` partition `U ≠ [n]` and let `i ∉ U`. Circuits avoiding `i` remain circuits of the shortened code `C_i = {c ∈ C : c_i = 0}`, so `S,T` are two distinct partitions of `U` in `C_i`; by G10-E1 the box `C_i` is non-embedded, contradicting minimality. So `U = [n]` and `1 = Σ S ∈ C`. ∎
(Previously G8-C3 was OPEN, CHECKED for `n ≤ 9`; this proof makes it a theorem for all `n`.)

### 1.3 Corollary G10-A1 (affine reduction)
Let `k = dim C`, `G` a generator matrix and `Σ ⊂ F_2^k ∖ 0` the set of its distinct nonzero columns (reduced support, by B-SERIES the box is a blow-up of the reduced one). Because `1 ∈ C` (G10-F1), there is `u0 ∈ F_2^k` with `u0·σ = 1` for all `σ ∈ Σ`; it is unique since `Σ` spans. So `Σ ⊂ {σ : u0·σ = 1} ≅ AG(k−1,2)`, `|Σ| ≤ 2^{k−1}`, and two minimal boxes are isomorphic iff the subsets are `AGL(k−1,2)`-equivalent. This is the route used for the classification (orbit counts 5, 10, 32, 382 for `m = 2..5`, Burnside, `tools/burnside_affine.c`; 381 non-empty orbits for `m = 5`, nullity 6). ∎

### 1.4 Rigidity and counting identity (G10-R)
*In a minimal box every codeword `w ∉ {0, 1}` has exactly one decomposition into disjoint circuits; the number of non-empty families of pairwise disjoint circuits is `2^k − 2 + β`, where `β` is the number of partitions of the all-ones word into circuits (the "blocks").*
*Proof.* Two distinct decompositions of `w ≠ 1` are two partitions of `U = supp w ≠ [n]`, contradicting G10-F1. Every nonzero codeword has at least one. A family of disjoint circuits is a decomposition of its union. ∎ Checked on all 215 minimal classes of nullity 6 (`tests/test_geo10.py`).

### 1.5 Local rank-three extraction (G10-L5/T5) and G10-C1′
**W2:** the all-ones word has at least two two-circuit partitions `a⊔b ≠ c⊔d`.
*Claim.* If the code has a word `U = a⊔b = c⊔d` (two distinct 2-circuit partitions) and `dim C ≥ 3`, there is `x ∈ C ∖ (span{a,b} ∪ span{c,d})` and the collision `(S=(a,b),x)`, `(T=(c,d),x)` has generator rank exactly 3.
*Proof.* Existence of `x`: as in 1.1 (both spans are proper: `span S = C` is impossible for `S ≠ T`). Both cells have `r = t = 2` circuits and a common base `x`, so B-COMMON (v008) gives witness rank `≤ r + t − 1 = 3`; B-LOW gives `≥ 3`. (`rank3_witness` computes the exact rank; it equals 3 on every case tested.) ∎
**G10-C1′.** If every minimal box satisfies W2, then `r_min = 3` for all minimal boxes (hence, by deleting down to a minimal sub-box as in G9-T5, for every non-embedded box). The only missing input is W2 (G10-C1).

### 1.6 Theorem G10-T4 (nullity six)
Spanning `AGL(5,2)`-orbits of subsets of `AG(5,2)` (nullity 6): **381 non-empty orbits** (Burnside: 382 including `∅`), **350 spanning**, **349 non-embedded**, **215 minimal non-embedded**, sizes `p = 10..32`; every one has W2 (minimum number of two-circuit partitions of 1 is `16 = 2^{k−2}`) and minimum witness rank **3**. Hence, with G9-T5: every non-embedded box of nullity `≤ 6` has `r_min = 3`. Orbit completeness: python generator vs. Burnside program (`tools/burnside_affine.c`); classification: `theory/binary6.py` partition criterion vs. cell engine `theory/binary5.py` (350 classes, 0 disagreements, `output/data/v10_binary6_crosscheck.json`); certificates `C6_rank6.json` (215), accepted by the standalone `certificates/checker10.py`.

### 1.7 Infinite family K_{2,t} (G10-K, CHECKED)
The cut space of the complete bipartite graph `K_{2,t}` (`n = 2t`, nullity `t+1`) is minimal non-embedded with rank 3 for `t = 2..10`, with `2^{t−1}` two-circuit partitions of 1 for `t ≥ 3` (3 for `t = 2`). This gives minimal boxes of unbounded nullity and rank 3; a proof for all `t` is not claimed.

## 2. The hollow box `Q = (d,d)` — proof of G10-Z, G9-C1, G9-T1H

Notation (frozen, v007–v009). `Γ = {(i,j) : j ≡ s i (mod d)}`, `t = s⁻¹ mod d`, `2 ≤ s ≤ d−2` (so `d ≥ 5`). `F = Γ ∩ [0,d]² ∖ 0 = {P_i = (i, s i mod d) : 1 ≤ i ≤ d−1} ∪ {A=(0,d), B=(d,0), C=(d,d)}`. A Graver vector is a conformally minimal nonzero vector of `Γ`. A cell `P(u; g, h)` has `g,h` Graver, independent, with `u, u+g, u+h, u+g+h ∈ F`. `U0` = union of all cells and Graver segments with endpoints in `F`; `H0 = conv F`. `T1 = conv(A, P_{d−t}, C)`, `T2 = conv(B, P_{d−1}, C)`; G7-T3 (proved for all `d ≥ 3`): `int Ti ∩ U0 = ∅`, `∂Ti ⊂ U0`. Put `u* = P_{d−t} − A = (d−t, −1)` and `g* = P_1 − A = (1, s−d)`.

### 2.1 Lemma 1 (the chain)
Let `A = c_0, c_1, …, c_N = B` be the points of `F` on the lower-left boundary of `H0` (consecutive F-points), `v_i = c_i − c_{i−1} = (a_i, −b_i)`, `a_i, b_i > 0`. Slopes `b_i/a_i` are non-increasing in `i` (convexity). **Then `v_1 = g*` and `v_N = u*`.**
*Proof.* Every `p ∈ F ∖ {B}` has `B − p = (a, −b)`, `b ≥ 1`, `a ≡ −b t (mod d)`. Writing `b t = q d + r` with `0 ≤ r < d`, `a = d − r ≤ b(d−t)` iff `(b−q) d ≥ d` iff `q ≤ b−1`, true because `t < d`. So `b/a ≥ 1/(d−t)` with equality for `b = 1`, `p = P_t = B − u*`. Hence the supporting direction of the hull at `B` is `u*`, `u*` is primitive in `Γ` (the triangle `T1` is empty: `a` takes integer values on `F`), so consecutive F-points on that edge differ by exactly `u*`; thus `v_N = u*`. Transposition `(x,y) ↦ (y,x)` maps `Γ_{d,s}` to `Γ_{d,t}`, `u*` to `−g*`, and reverses the chain, so `v_1 = g*`. ∎ (Verified for all 1808 unit pairs `d ≤ 80`.)

### 2.2 Lemma 2 (hull steps are Graver)
Each `v_i` is a Graver vector of `Γ`.
*Proof.* Let `w ∈ Γ` be conformally `≤ v_i`, `w ∉ {0, v_i}`. The point `p = c_{i−1} + w` lies in the closed rectangle with diagonal `c_{i−1}c_i`, hence in `[0,d]²`, and in `Γ`; so `p ∈ F` (it is nonzero). It is not on the line `c_{i−1}c_i` (the points are consecutive), and `H0` lies on one side of that line, so `p` is strictly on the hull side. The reflected point `c_{i−1} + c_i − p = c_{i−1} + (v_i − w)` is also in `F`, but lies strictly on the other side of the line, outside `H0`: a contradiction. ∎

### 2.3 Lemma 3 (zonogon)
Order the steps by slope, steepest first; this is the chain order. `Z = A + Σ_i [0,1] v_i`. Every vertex of every parallelogram below is a partial sum `A + Σ_{i∈I} v_i`, whose coordinates lie in `[0,d]` (monotone steps), is in `Γ` and is non-zero: so it lies in `F`. By induction on the number of steps, `Z_n = Z_{n−1} ∪ (strip swept by the upper path of Z_{n−1} along v_n)`, and the strip is the union of the parallelograms `P(u; w, v_n)` with `w` running over the upper path `v_{n−1}, …, v_1` (parallel pairs omitted). Each such parallelogram is a Graver cell by Lemma 2. Hence `Z` is a union of cells of `U0`. (`zonogon_cells` in `theory/modular_sail.py`.)

### 2.4 Lemma 4 and the proof of G10-Z
The upper boundary of `Z` is the reversed chain: `A, A+v_N = A+u* = P_{d−t}, …, B − g* = P_{d−1}, B`, a concave path from `A` to `B`. Let `Δ = conv(P_{d−t}, C, P_{d−1})`. `H0` is bounded by the lower chain, `AC` and `CB`; so `H0 ∖ Z` is the region above the upper path, which splits into `T1` (above the first step), `T2` (above the last step) and the region `R` between the middle of the path and `C`. **Claim: every vertex `q` of the upper path between `P_{d−t}` and `P_{d−1}` lies in `Δ`.** It is above the chord `P_{d−t}P_{d−1}` by concavity. If it were on the `A`-side of the line `C P_{d−t}` (equation `y = d − 1 + (x−d+t)/t`) with `x > d−t`, then `d−1 < y ≤ d`, forcing `y = d` and `q ∈ {A,C}`, i.e. `q = C ∈ Δ`; the symmetric statement for the line `C P_{d−1}` follows by transposition. Therefore `R ⊆ Δ`. Finally `Δ` is contained in the cell `K = P((d−t−1, d−s−1); (1,s), (t,1))`: its corners are `(d−t−1, d−s−1)`, `P_{d−t} = (d−t, d−1)`, `P_{d−1} = (d−1, d−s)` and `C = (d,d)`, all in `F`, and `(1,s)`, `(t,1)` are Graver (they are `P_1 − 0` and `P_t − 0`, and the triangle argument of Lemma 1). So

> **G10-Z.** `H0 ⊆ Z ∪ T1 ∪ T2 ∪ K`, where `Z` and `K` are unions of cells. ∎

Machine check: `experiments/sail_families.py` (exact rational arithmetic) verifies, for **every** unit pair `5 ≤ d ≤ 150`, `2 ≤ s ≤ d−2` (**6560 pairs**), that the cells are valid (Graver generators by exact box scan, corners in `F`) and that `conv F ∖ (T1 ∪ T2 ∪ cells)` has area exactly 0; for `d ≤ 32` (262 pairs) the v005/v009 cell engine independently confirms `H0 ∖ U0 = int T1 ∪ int T2` and that every cover cell is an engine cell. 453 BOUNDARY certificates (all pairs `d ≤ 40`, samples to `d = 199`) are accepted by the standalone `checker10.py`.

### 2.5 Consequences
* **G10-T1 / G9-C1.** The cells lie in `U0` and `∂Ti ⊂ U0`, so `H0 ∖ U0 ⊆ int T1 ∪ int T2`; the reverse inclusion is G7-T3. For `d = 3, 4` the only units are `s ≡ ±1`, the separate cases (`s ≡ −1`: `β1 = d`).
* **G10-T1H / G9-T1H.** `U0 ⊆ H0` and `R² ∖ H0` is connected and unbounded, so the bounded components of `R² ∖ U0` are exactly `int T1` and `int T2`; by Alexander duality `β1(U0) = 2` (and `β2 = 0`).
* **G10-R1.** With G9-C1, the proved conditional theorem G8-R1 applies: `H0 ⊆ U_Q` for all `Q ≥ (d,d)`, `Q ≠ (d,d)`.
* **G10-S1/S2.** For `d = sm+1` the zonogon is the parallelogram `U1` of `s` cells with steps `(1,s−d)`, `(m,−1)` and `K` covers `R2`; for `d = sM−1` the zonogon is the hexagon of three faces (`g + h4 + h = (d,−d)`) plus `K`. These are the closed forms of v010 `MODULAR_SAIL.md`.

### 2.6 What this does not give
The cap `C_Q = H_Q ∖ H0` for small boxes (G10-T2) is still not proved; therefore the consolidated G10-T3 stays OPEN (§3).

## 3. The cap (G10-T2/T3): honest status
A bounded attempt reused Lemma 2 (hull steps are Graver) for the hull `H_Q` of an enlarged box: the lower-left chain of `H_Q` is that of `H0` (unchanged), but new top and right chains appear, and their steps are Graver for the same reason; however the covering cells needed for `C_Q` are not those of a zonogon on one chain (the region is between two chains), and the corner compatibility of horizontal and vertical enlargement (v009 B3–B5) is not obtained. **G10-T2 remains OPEN.** Evidence is unchanged (CHECKED, v009: no counterexample). The conditional chain is now short: **G10-T2 ⇒ G10-T3** (`U = H` for all `d`, units `s`, `Q ≥ (d,d)`, `Q ≠ (d,d)`), because G10-R1 supplies the square hull and G7-T1 / `s = ±1` the rest.

## 4. Adversarial results (G10-C2, negative record)
* Random minimal boxes of nullity 7 (two runs, 1500 supports each, 1174 / 1203 minimal): all satisfy W2 (minimum number of two-blocks 48 and 54); hill-climbing to minimise the number of two-blocks stops at 45 (never 0).
* Cut spaces of random graphs on 6, 7, 8, 9 vertices (725 samples, 399 non-embedded, each shortened to a minimal box): all W2, all rank 3. These minimal boxes have nullity 3, 4 or 5 only, so this search does **not** reach nullity `≥ 6` beyond the K_{2,t} family; it is weak evidence only.
* **FALSE rules** (G10-L2): R-MIR (`|cells(d,s)| = |cells(d,d−s)|`: 58 counterexamples, first `(d,s) = (7,2)`), R-EUC (one-step Euclid transfer of cell counts depends only on the first quotient: false), R-LAT (cell generator sets correspond under the Euclid map: 76 counterexamples, first `(4,3)`). R-SYM (transposition) holds on 100 pairs `d ≤ 18`. All counterexamples are stored in `output/data/v10_sail_attack.json`.

## 5. Independent validation paths

| Claim | Path 1 | Path 2 |
|---|---|---|
| G10-Z / G10-T1 | `theory/modular_sail.py`: exact Fraction polygon subtraction, own Graver scan | v005/v009 engine (`hollow_check`, `coverage.complex_data`) for `d ≤ 32`; standalone `checker10.py` BOUNDARY (own `F`, Graver, cells) |
| nullity-6 classification | `binary6.py` partition criterion | cell engine `binary5.py` (0 disagreements) + Burnside orbit count |
| rank 3 | `rank3_witness` (exact) | `checker10.py` RANK6 (own implementation) |
| E1 | proof (§1.1) | equality with the cell engine on all classes of nullity ≤ 6 |

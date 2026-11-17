# UNNS-SCALE-I v002 — Boundary Arithmetic and Hierarchical Composition

Builds on the frozen local baseline `UNNS-SCALE-I` v001 (unchanged). Status vocabulary as in v001: **PROVED**, **CERTIFIED**, **EXPERIMENTAL**, **OPEN**. Every PROVED statement below also carries an independent computational cross-check, named in brackets.

## 0. Inherited from v001 (used without change)

- **Lemma 0.** `deg_G(u) = τ(u) + s(u)`, `s(u) = #{q ≥ 2 : q² | u}`.
- **Theorem 2.** `{Bu,Bv} ∈ E ⇔ {u,v} ∈ E`, labels preserved; so the neighbours of `Bx` that lie in `Bℕ` are exactly the `B`-multiples of the neighbours of `x`.
- **Theorem 3(iii).** `deg(Bx) = deg(x) + ε_B(x)`, where `ε_B(x)` is the number of neighbours of `Bx` outside `Bℕ` (the *exits*).

Write `B = ∏ p^{b_p}`, `x = ∏ p^{a_p}` (zero exponents allowed). Put `s₁(u) = s(u) + 1 = #{q ≥ 1 : q² | u}`.

## 1. The boundary law

**Theorem A1 (prime-factor boundary law) — PROVED.**

    ε_B(x) = ∏_p (a_p + b_p + 1) − ∏_p (a_p + 1) + ∏_p (⌊(a_p+b_p)/2⌋ + 1) − ∏_p (⌊a_p/2⌋ + 1).

*Proof.* `ε_B(x) = deg(Bx) − deg(x) = [τ(Bx) − τ(x)] + [s₁(Bx) − s₁(x)]` by Theorem 3(iii) and Lemma 0 (the constants `−1` in `s = s₁ − 1` cancel). Both `τ` and `s₁` are products over primes of `(e+1)` and `(⌊e/2⌋+1)`. ∎
*[Cross-check A1: 13 values of B up to 3·10⁶ (including 10⁶, 30030, 7³·11, 2¹⁰); 2,000 values of x each (1..1500 and 500 random below 10⁶); closed form compared with a direct count of non-lattice neighbours from complete neighbourhood enumeration: 0 mismatches.]*

**Corollary A2 (coprime case) — PROVED.** If `gcd(x,B)=1`: `ε_B(x) = (τ(B) − 1) τ(x) + s(B)(s(x) + 1)`. For a prime `x = p ∤ B`: `ε_B(p) = 2(τ(B) − 1) + s(B)`.
*[Cross-check: all coprime x < 4000 for B ∈ {10, 12, 360, 10⁶, 30030}: 0 mismatches.]*

**Corollary A3 — PROVED.** For `B > 1`, `ε_B(x) ≥ 1` for every `x`: some `b_p ≥ 1` gives `∏(a+b+1) > ∏(a+1)`, and the `s₁` difference is non-negative.

## 2. Average number of exits

Define, for `B` with prime-power exponents `b_p`:

- `c_B = ∏_{p|B} (b_p + 1 − b_p/p)`,
- `h(m) = ∏_{p|m} (−b_p/(b_p+1))` for squarefree `m | rad(B)`, and `d_B = τ(B) Σ_{m | rad B} h(m) (log m)/m`,
- `K_B = ζ(2) ( ∏_{p|B} (1 − p⁻²) L_p − 1 )`, `L_p = (⌊b/2⌋ + 1) + p^{b − 2(⌊b/2⌋+1)} / (1 − p⁻²)`,
- `γ` Euler's constant.

**Theorem A4 (mean number of exits) — PROVED.** For fixed `B`,

    (1/X) Σ_{x ≤ X} ε_B(x) = (c_B − 1)(log X + 2γ − 1) − d_B + K_B + O_B(X^{−1/2}).

In particular the mean grows like `(c_B − 1) log X`; for `B = 10⁶ = 2⁶5⁶`, `c_B − 1 = (7 − 3)(7 − 6/5) − 1 = 22.2`.

*Proof.* (i) *τ-part.* `f(n) = τ(Bn)/τ(B) = ∏_p (a_p + b_p + 1)/(b_p + 1)` is multiplicative, and `f = 1 * 1 * h` with `h = f * μ * μ` multiplicative. At a prime `p ∤ B`, `f(p^a) = a + 1`, so `h(p^a) = 0` for `a ≥ 1`. At `p | B`, `f(p^a) = (a+b+1)/(b+1)` is linear in `a`, so `h(p⁰) = 1`, `h(p) = f(p) − 2f(1) = −b/(b+1)`, and `h(p^a) = f(p^a) − 2f(p^{a−1}) + f(p^{a−2}) = 0` for `a ≥ 2`. Hence `h` is supported on the divisors `m` of `rad(B)` and
`Σ_{n ≤ X} τ(Bn) = τ(B) Σ_m h(m) D(X/m)`, with `D(Y) = Σ_{k ≤ Y} τ(k) = Y log Y + (2γ−1)Y + O(√Y)` (Dirichlet). Dividing by `X`,
`(1/X) Σ τ(Bn) = c_B (log X + 2γ − 1) − d_B + O_B(X^{−1/2})`, where `c_B = τ(B) Σ_m h(m)/m = τ(B) ∏_p (1 − b_p/((b_p+1)p)) = ∏_p (b_p + 1 − b_p/p)`. The case `B = 1` gives `c = 1`, `d = 0`.
(ii) *s-part.* `q² | Bx ⇔ (q²/g_q) | x` with `g_q = gcd(q², B)`, hence the exact identity
`Σ_{x ≤ X} (s₁(Bx) − s₁(x)) = Σ_{q ≥ 1} ( ⌊X g_q/q²⌋ − ⌊X/q²⌋ )`.
Replacing floors by their real values gives `X Σ_q (g_q − 1)/q²` with error at most `O(√(XB))` (floor errors for `q ≤ √(XB)`, tail of the series beyond). The series `Σ_q gcd(q²,B)/q²` is multiplicative in `q`; its Euler factor at `p | B` is `Σ_{a ≥ 0} p^{min(2a,b) − 2a} = L_p`, and at `p ∤ B` it is `(1−p⁻²)⁻¹`. Subtracting `ζ(2)` gives `K_B`.
(iii) Add (i) and (ii). ∎

*[Cross-check A2 — mean computed by exact sieve (not by the formula), X up to 4·10⁶:]*

| B | c_B − 1 | observed slope (X = 10⁶ → 4·10⁶) | exact mean at X = 4·10⁶ | prediction | error |
|---|---|---|---|---|---|
| 10 | 1.7000 | 1.7002 | 27.9522 | 27.9525 | −0.0003 |
| 12 | 2.3333 | 2.3337 | 39.5917 | 39.5923 | −0.0006 |
| 360 | 9.5000 | 9.5011 | 160.9865 | 160.9881 | −0.0016 |
| 1000 | 7.5000 | 7.5009 | 126.4490 | 126.4506 | −0.0016 |
| 10⁶ | 22.2000 | 22.2027 | 379.7874 | 379.7922 | −0.0048 |

The error shrinks with `X` at the rate `X^{−1/2}` predicted by the proof (for `B = 10⁶`: −0.0935, −0.0338, −0.0086, −0.0048 at `X = 10⁴, 10⁵, 10⁶, 4·10⁶`). The s-part identity itself was checked against direct factor-based enumeration at `X = 3000` for `B ∈ {12, 360, 1000}`.

**Remark.** The statement in the assessment that the mean has the form `(c_B − 1) log X + O_B(1)` is correct; Theorem A4 identifies the `O(1)` term exactly.

## 3. Hierarchical composition

**Theorem B1 (additivity) — PROVED.** For all `A, B ≥ 1` and `x`:

    ε_{AB}(x) = ε_A(x) + ε_B(Ax) = ε_B(x) + ε_A(Bx).

*Proof.* `ε_{AB}(x) = deg(ABx) − deg(x) = [deg(ABx) − deg(Ax)] + [deg(Ax) − deg(x)] = ε_B(Ax) + ε_A(x)`; swap `A` and `B`. ∎
*[Cross-check: 9 pairs of scale factors (including 10⁶×10⁶, 10⁴×10⁴, 12×18, 7×49), 1,499 values of x each; left side computed from enumeration of non-lattice neighbours of `ABx`; all four quantities agree: 0 mismatches.]*
Exit counts of nested scales therefore **add**; they do not multiply.

**Theorem B2 (level stratification) — PROVED.** Let `B₁,…,B_d ≥ 1`, `P_j = B₁⋯B_j`, `A_j = P_j ℕ` (`A₀ = ℕ ⊃ A₁ ⊃ … ⊃ A_d`), and `u = P_d x`. The number of neighbours of `u` lying in `A_j` is `deg(u/P_j) = deg(B_{j+1}⋯B_d x)`. Hence the number `n_j` of neighbours of `u` in `A_j ∖ A_{j+1}` is

    n_j = deg(B_{j+1}⋯B_d x) − deg(B_{j+2}⋯B_d x)   (0 ≤ j < d),   n_d = deg(x),

and `Σ_{j<d} n_j = ε_{P_d}(x)`.

*Proof.* Theorem 2 applied with scale `P_j` to the vertex `u ∈ A_j`: its neighbours in `A_j` are the `P_j`-multiples of the neighbours of `u/P_j`. The lattices are nested, so strata are differences. ∎
*[Cross-check: 9 chains (10⁶×10⁶; 10⁴×10⁴×10⁴; 10³×4; 10²×6; 10×12; 10⁴×10⁸; 2×3×5×7; and two orderings of 10⁶, 10³, 10³), 519 vertices each; each neighbour of `u` classified by the deepest lattice containing it; 0 mismatches.]*

**Example (infinite graph, `x = 1`, vertex `10¹²`).** `deg(10¹²) = 217`, so `ε_{10¹²}(1) = 216` for every factorisation, but the level profile `(n₀, n₁, …)` depends on the nesting:

| nesting | strata `(n₀, …, n_d)` | exits | note |
|---|---|---|---|
| 10⁶ × 10⁶ | 153, 63, 1 | 153 + 63 = 216 | `ε₁₀⁶(10⁶) + ε₁₀⁶(1)` |
| 10⁴ × 10⁴ × 10⁴ | 112, 72, 32, 1 | 112 + 72 + 32 = 216 | |
| 10³ × 10³ × 10³ × 10³ | 93, 60, 45, 18, 1 | 216 | |
| 10² × 6 | 61, 51, 41, 31, 21, 11, 1 | 216 | |
| 10 × 12 | 38, 23, 32, 19, 26, 15, 20, 11, 14, 7, 8, 3, 1 | 216 | parity oscillation from the `⌊e/2⌋` terms |

The total is invariant under refinement; the distribution of exits across scales is a property of the chosen nesting. The comparison of `10⁶×10⁶` with `10⁴×10⁴×10⁴` asked for in the research plan is therefore exact: 216 = 63 + 153 = 32 + 72 + 112.

## 4. Information preserved by the inner coordinate

Let `n = Bq + r`, `0 ≤ r < B`, and let `T₁ : n ↦ 4n` be the label-1 move (admissible at every vertex).

**Lemma C1 — PROVED.** `⌊4^t n / B⌋ = 4^t q + ⌊4^t r / B⌋` (since `4^t Bq / B` is an integer).

**Definition.** A *faithful outer-coordinate model for `T₁`* is a quadruple `(S, Φ, o, e)`: a set `S`, a deterministic map `Φ : S → S`, an observation `o : S → ℤ≥0` and an encoding `e : ℕ → S`, such that `o(Φ^t e(n)) = ⌊4^t n / B⌋` for all `t ≥ 0` and `n ≥ 0`. (`t` ranges over all steps, or over `t ≤ T` for a *horizon-`T`* model.)

**Theorem C2 (resolution by horizon) — PROVED.** For every `B ≥ 1`, `T ≥ 0` and `q`: the number of distinct outer trajectories `(⌊4^t n/B⌋)_{t ≤ T}` produced by the `B` numbers `n = Bq + r` equals `min(4^T, B)`.

*Proof.* By Lemma C1 the trajectory of `n` is determined by the numbers `⌊4^t r/B⌋ + 4^t q`, and `⌊4^j r/B⌋ = ⌊⌊4^T r/B⌋ / 4^{T−j}⌋` for `j ≤ T`, so the trajectory is determined by `⌊4^T r/B⌋`. The map `r ↦ ⌊c r/B⌋` with `c = 4^T` takes `r = 0,…,B−1` to values in `[0, ⌊c(B−1)/B⌋]`. If `c ≥ B` consecutive `r` give distinct values (increment `c/B ≥ 1`), so there are `B` of them. If `c < B` the increments are `< 1`, every integer from 0 to `c − 1` is attained, and the largest value is `⌊c − c/B⌋ = c − 1`, so there are exactly `c` values. ∎

**Theorem C3 (minimal inner information) — PROVED.** In any faithful horizon-`T` outer-coordinate model, the encoding `e` takes at least `min(4^T, B)` distinct values on each block `{Bq,…,Bq+B−1}`. In a faithful all-horizon model `e` is injective on every block, so at least `B` internal states per outer block, i.e. `log₂ B` bits per block, are unavoidable; and `B` suffice (take `S = ℕ`, `Φ = T₁`, `o = ⌊·/B⌋`, `e = id`). The threshold horizon at which all of `r` is resolved is `T = ⌈log₄ B⌉`; before that, each additional step reveals exactly two bits (the number of classes is `4^T`).

*Proof.* Two numbers with the same `e`-value have the same observation sequence under `Φ`; by C2 the number of different observation sequences on a block is `min(4^T, B)`. ∎
*[Cross-check: class counts computed by brute force for `B ∈ {12, 1000, 4⁵, 10⁶, 3·10⁶+1}` and every horizon up to threshold + 1: equal to `min(4^t, B)` in every case; injectivity holds exactly when `4^t ≥ B`; block independence checked for `B = 360`; Lemma C1 checked on 112,504 combinations of (B, q, r, t).]*

**Consequences.**
- For `B = 10⁶` the threshold is `T = 10`: `4⁹ = 262,144 < 10⁶ ≤ 4¹⁰ = 1,048,576`; nine steps leave collisions, ten steps resolve all one million remainders. [verified]
- v001 Theorem 4 is the single-step case: after one step an outer-only model can distinguish at most `min(4, B)` of the `B` remainders in a block.
- For the original scaling hypothesis: a faithful deterministic model of even the single universal move on `[0, 10¹²)` cannot be built on the `10⁶` outer coordinates alone; it carries `log₂ 10⁶ ≈ 19.93` bits per block, `39.86` bits in total, exactly as the unreduced domain. A reduction must come from restricting which dynamics are required (for example the scale-preserving moves of Theorem 3), not from discarding `r`.

*Scope.* The theorem concerns deterministic exact reproduction of the observation sequence of one move. It says nothing about approximate, stochastic, or restricted-observable models, and it uses one label only; additional labels can only add distinctions.

## 5. Infinite-graph versus finite-window boundary counts

v001 counted exits in the infinite graph (`10⁶` has `deg = 64`, one in-lattice edge, **63 exits**). Inside the window `[1, L]`, `L = 10¹²`, the forward move `N = 10⁶` from `10⁶` lands at `10⁶(10⁶+1)² / 10⁶ = 1,000,002,000,001 > L`, so only **62 exits** remain. [verified by enumeration] The top vertex `10¹²` has infinite degree 217 but only 48 neighbours in the window (all forward neighbours exceed `L`).

**Theorem W (edge classes in a window) — PROVED.** Let `s = (N+1)²`, `K_N = ⌊L/s⌋`, `g_N = gcd(B,N)`, `g'_N = gcd(B,s)`. Among the edges of `G[1..L]`, the numbers with both / exactly one / no endpoint in `Bℕ` are

    both      = Σ_N ⌊K_N / B⌋ = e(⌊L/B⌋),
    exactly one = Σ_N ⌊K_N g_N / B⌋ + Σ_N ⌊K_N g'_N / B⌋ − 2 · both,
    none      = e(L) − (n_u + n_v − both),

where `n_u = Σ_N ⌊K_N g_N/B⌋`, `n_v = Σ_N ⌊K_N g'_N/B⌋`, `e(L) = Σ_{m ≥ 2} ⌊L/m²⌋`, and the sums run over `N ≥ 1` with `(N+1)² ≤ L`. (Here `⌊K/(B/g)⌋ = ⌊Kg/B⌋` since `g | B`.)

*Proof.* An edge is `{kN, ks}` with `1 ≤ k ≤ K_N`. Its smaller endpoint is in `Bℕ` iff `B | kN`, i.e. `(B/g_N) | k`; its larger endpoint iff `B | ks`, i.e. `(B/g'_N) | k`; both iff `B | k` (v001 Theorem 2). Count multiples. ∎
*[Cross-check: closed form equals brute-force classification of every edge for 8 pairs `(L,B)` including `(3·10⁷, 1000)` and `(10⁶, 10⁶)`: equal in all; bookkeeping at `(10⁶,10)`, `(10⁶,100)`, `(2·10⁶, 1000)`: per-vertex enumeration gives infinite exits = window exits + exits beyond the window, and window exits = the closed-form "exactly one" count.]*

**The trillion window `[1, 10¹²]`** (exact):

| B | lattice vertices | edges inside copy | edges with exactly one lattice endpoint | mean window exits per lattice vertex |
|---|---|---|---|---|
| 10³ | 10⁹ | 644,887,919 | 6,193,421,292 | 6.19 |
| 10⁴ | 10⁸ | 64,478,820 | 1,128,650,367 | 11.29 |
| 10⁶ | 10⁶ | 643,494 | 20,054,629 | 20.05 |

(total edges `e(10¹²) = 644,932,606,630`.)
For `B = 10⁶` the infinite-graph exit total over the `10⁶` lattice vertices is `Σ_{x ≤ 10⁶} ε_{10⁶}(x) = 349,007,877` (mean 349.0, from the exact sieve of Section 2). Only 20,054,629 of these lie inside the window; **328,953,248 (94.3%)** are forward moves landing beyond `10¹²`. The window average (≈ 20) and the infinite-graph average (≈ 349, growing as `22.2 log X`) therefore describe different objects, and v001's sample mean of 260 exits belongs to the infinite graph.

## 6. Register

| Result | Status |
|---|---|
| A1 prime-factor boundary law; A2 coprime form; A3 `ε ≥ 1` | PROVED, enumeration-checked |
| A4 mean number of exits with explicit constants and `O(X^{−1/2})` error | PROVED, sieve-checked to X = 4·10⁶ |
| B1 additivity; B2 level stratification; 10¹² decompositions | PROVED, enumeration-checked |
| C1–C3 resolution by horizon; minimal inner information; threshold `⌈log₄ B⌉` | PROVED, brute-force checked |
| W edge-class counts in `[1, L]`; trillion-window table | PROVED, brute-force checked at 8 (L, B) pairs; trillion values by the proved formula |
| `sup_n d(Bn, B(n+1))` | OPEN (next) |
| Gate 4 (computational benefit) | NOT STARTED (deferred) |

## 7. Not shown here

The exact distance supremum `D_B = sup_n d_G(Bn, B(n+1))`; behaviour of the *window* mean exit count as `L → ∞` with `B` fixed; scale compatibility of grammars other than SELECT-II; any statement about computational cost. Originality against the literature has not been reviewed.

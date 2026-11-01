# R3-F  Exact arithmetic of collective transitions with G > 1

## 1. The class G(x) = b
Let `x = a/b` be reduced with `D(x) ≠ ∅` and `G(x) = b` (the gcd of `d-1` over `D(x)` equals the denominator; always `b | G` because `d ≡ 1 mod b`). For `b=1` this is exactly regime I (`G=1`, `4|x`). Put `L = lcm D(x)` and `t = a / L²`.

**Theorem R3-T5a (exact reduction) — PROVED.**
(i) `t` is a positive integer (each `d ∈ D` has `d² | a` and `d | L`, so `L² = lcm(d²)` divides `a`).
(ii) `C(x) = x + L²/b = (t+1) L² / b`.
(iii) If `gcd(t+1, b) = 1`, then `C(x)` is reduced with denominator `b`, `D(x) ⊆ D(C(x))`, `L | L'`, and `G(C(x)) = b`: the class is invariant, `D` never loses an element and `G` stays `b`.
(iv) If `gcd(t+1,b) > 1` the orbit leaves the class (denominator drops).
*Proof.* (ii) `G=b`. (iii) `d² | a = tL²` ⇒ `d² | (t+1)L²`; same denominator ⇒ the congruence is unchanged ⇒ `D ⊆ D'`. `G' | G = b` (more terms) and `b | G'` ⇒ `G' = b`. ∎  
So inside the class the dynamics is `(L,t) -> (L,t+1)` until `D` changes, then `L -> L'`, `t -> t(L/L')²`. For `b=1` this is the v002 regime-I reduction `(σ,t)`.

## 2. Event times and dichotomy
Let `D_b(S) = {d | S, d >= 2, d ≡ 1 mod b}`. For `t = u_t² τ'` (`τ'` squarefree) one has `D(tL²/b) = D_b(u_t L)` (`d² | τ'(uL)²` iff `d | uL`).

**Theorem R3-T5b (first event of a fresh stage is a perfect square; dichotomy, `b = ℓ` prime) — PROVED.**
(a) Let `x = L²/ℓ` in the class with `D = D_ℓ(L)`. Put `u* = min{u >= 2 : D_ℓ(uL) ≠ D_ℓ(L)}`. Then `D` is unchanged for `1 <= t < u*²` and changes at `t = u*²`, as long as `u*² < ℓ`; the stage length is `u*² - 1`. If `u*² > ℓ` the orbit reaches the integer `L²` first and leaves.  
*Proof.* `D_ℓ(uL)` is monotone in `u` under divisibility, `D(x_t)=D_ℓ(u_tL)`, `u_t² <= t`; at `t=u*²`, `u_t=u*`. ∎
(b) Dichotomy: a class orbit either leaves the class (to an integer) in finitely many steps or has infinitely many events. *Proof.* Between events `t` increases by 1 and stays `< ℓ` (it only shrinks at events); when `t+1 = ℓ` the next state is an integer. ∎  
So persistent `G>1` orbits in the class are exactly those with infinitely many occurrence events, and every event lands at a square time on fresh stages.

## 3. Explicit infinite towers — PROVED for every k
**R3-T5b' (ℓ=11, period 8, ρ²=9).** `S_k = 2²·3^{3+k}·5⁴`, `x = S_k²/11`. Discrete logs mod 11 base 2: `3 = 2^8`, `5 = 2^4`; `d = 2^a 3^c 5^e ≡ 2^{a+8c+4e}`, so `d ≡ 1` iff `a+8c+4e ≡ 0 (10)`: `a ∈ {0,2}` and `e ≡ -2c` (a=0) resp. `e ≡ 2-2c` (a=2) mod 5. Hence `|D| = 2k+7`; `12 ∈ D` gives `G=11`; the maximal exponents of 2, 3, 5 all occur, so `L = S_k`. For `t=1..8`, `u_t ∈ {1,2}` and `D_11(2S_k)=D_11(S_k)` (exponent `a=3` is odd, never a solution), so `D` is unchanged; at `t=9`, `u=3` adds exactly the two elements with `c = 4+k` (one `e` for each `a ∈ {0,2}`), `L' = 3S_k = S_{k+1}`, `x_8 = S_{k+1}²/11`. By induction `x_{8k+j} = (j+1) S_k²/11` for all `k`, `x_{n+8} = 9 x_n`, `G ≡ 11`, one event per period creating exactly 2 indices. (Re-derivation of FIELD-I T50 for all `k`; verified for k<12 with the frozen map and k<6 by the independent verifier.)  
**R3-T5c (ℓ=5, period 3, ρ²=4) — counterexample to "rigid ⇔ G∞=1".** `S_k = 126·2^k = 2^{k+1}·3²·7`. `3 = 2^3`, `7 ≡ 2` mod 5: `d ≡ 1` iff `a+3c+f ≡ 0 (4)`. `6 ∈ D` ⇒ `G=5`; all maximal exponents occur ⇒ `L = S_k`; `t=2,3` squarefree ⇒ no change; `t=4` (`u=2`) adds elements with `a=k+2` (1 or 2 of them according to `-(k+2) mod 4`) ⇒ `L' = 2S_k`. So `x_{3k+j}=(j+1)S_k²/5`, `x_{n+3}=4x_n` with `G=5` forever. **Hence B2-T7's "iff G∞=1" is false** (`GEO_HD_BRIDGE_v002_ERRATUM_B2-T7.md`); only `G∞=1 ⇒ eventually rigid` stands.

## 4. Stage law (conditional / finite-exact)
Suppose a persistent orbit is a concatenation of fresh stages with first-event times `τ_i = u_i²` and `L_{i+1} = u_i L_i`. Then the orbit advances `τ_i - 1` steps per stage, multiplying `x` by `τ_i`. If the stage sequence is periodic with period `r`, then `x_{n+P} = ρ² x_n` with `P = Σ_{i<r}(τ_i - 1)`, `ρ² = Π τ_i`. Instances: ℓ=11: `τ=(9)` ⇒ `(8,9)`; ℓ=5: `(4)` ⇒ `(3,4)`; **ℓ=29, S=1890: `τ=(25,4,9)` ⇒ `P=24+3+8=35`, `ρ²=900`** (events at steps 24, 27, 35, 59, 62, 70, … and `x_{35}=900x_0`, `x_{70}=900x_{35}`; `G ≡ 29`; checked by the verifier). The periodicity hypothesis is verified, not proved, for ℓ=29; for the towers it is proved (§3).

## 5. Census (finite-exact; `results/G_CENSUS.json`, `data/G_CENSUS_ROWS.json`)
1 920 orbits `x_0 = S²/ℓ`, `ℓ ∈ {5,7,11,13,17,19,23,29}`, 70–90 steps: 1 801 detected as exactly periodic, 119 unresolved in the window. Of the periodic ones 968 keep `G>1` forever (944 with `G = ℓ`, 24 with another value) and 833 fall to `G=1` (all with `(P,ρ²)=(3,4)`, the regime-I rigid orbit). Persistent `(P,ρ²)` found: `(3,4)`, `(8,9)`, `(35,900)` only. No other value appeared; this is **not** a theorem (O3-5).

## 6. Not shown
Classification of `G > b`-states and their approach to the class (24 persistent orbits have `G ∉ {1,ℓ}`); proof that every persistent orbit is eventually periodic (FIELD-I T51 is cited, not re-proved); the `(35,900)` periodicity for all `k`.

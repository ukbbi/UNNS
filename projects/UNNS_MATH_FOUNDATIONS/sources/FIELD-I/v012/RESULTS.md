# RESULTS — FIELD-I v012: Effective Predictability, Bounds on the Transient

Full run of `field12.py`: **0 FAIL, 352 s** (`output/field12_output.txt`). Proofs: THEOREMS.md (T69–T73). v002–v011, the G1–G3 memo and the relational manuscript are unchanged (byte-identical to the v011 package). v011 was rerun in full (0 FAIL, 379 s). (v011's *quick* mode reports one FAIL in S2b: a coverage threshold — at least 5 non-constant gap patterns — that the reduced quick sample misses, with 0 mismatches; it is not a soundness failure.)

## Answer to the v012 question (what is decided, what is not)
| Claim | Status |
|---|---|
| **Reset-descent bound** (T69): from a segment start with γ₀, the first reset needs at most κ(γ₀) carries, κ = iterations of f(a)=⌊a/4⌋+1 (≈ log₄ γ₀); the bound is **attained** for every κ = 1…11 | **PROVED** (from T54); sharpness DATA, 6 witnesses re-run by exact iteration of C |
| **Certificate-entry bound by class counting** (T70): after the first reset the class cycle is entered at index ≤ H(g)−1; for prime g the entry state is statically certified for the active prime | **PROVED** |
| **Polynomial certificate-entry bound** (T71): index ≤ K_poly(g) = (Φ+1)(Σ+(Σ+1)(ω+1)+1), cubic in the orders, via the epoch structure of the scheduler | **PROVED** for prime g (or whenever T67 applies) |
| **Dynamic-G effective bound** (T72): chain of reducing events g₀⊋g₁⊋…, ≤ Ω(g₀) segments with G>1, γ recursion, per-segment carries ≤ κ(γ_i)+H(g_i)−1, G=1 tail ≤ 4κ₃(t), explicit total R(g₀,γ₀) | **PROVED** |
| The **exact** transient time, or a bound near the observed entry indices (≲ 210 vs. bounds ≥ 10⁸) | **OPEN** (O12.1) |
| Static certification for composite/even g | **OPEN** (O12.2; scope erratum for v011 T68(a) registered, T73) |

## Review of the proposal
* T69 is **correct but not sharp**. Its chain b′ ≤ ⌊(b+1)/4⌋ ≤ ⌊b/2⌋ discards a factor 2 per carry. The sharp bound is κ(γ₀) ≈ log₄ γ₀ and it is attained: g = 79, γ₀ = 1 444 161 needs exactly 11 carries (proposal: 21); g = 11, γ₀ = 173 715 needs exactly 9 (proposal: 18).
* T70 is **correct** (the pigeonhole argument and the saturation argument for the recurring prime hold as outlined). The index is sharpened to H − 1 (repeat ≤ H), and the proposal's table H(11) = 171, H(31) = 2 655, H(59) = 21 297 195 is reproduced exactly (E1).
* New: T71 replaces the product H(g) by a polynomial; T72 answers the proposal's "bound from arbitrary seed before G stabilizes" as an explicit bound.
* **Scope correction (accepted):** v011 T68(a) is worded for every persistent orbit, but its justification (necessity half of T66) is proved for prime g only. In all six exact composite/even cycles tested (g = 15, 39, 51, 57, 68, 87) **every** reset state fails S5 while the orbit is persistent (E5). v011 is preserved; the erratum is T73.

## Numbers
| Test | Result |
|---|---|
| A1 arithmetic | κ(a) = closed form (least k with 4ᵏ > (3a−4)/2) and κ(a) ≤ ⌈log₂ a⌉, ≤ ⌈log₄ a⌉+1: exhaustive a ≤ 300 000 and 4 000 random a up to 2²²⁰, 0 violations. κ(2,10,100,1000,10⁶,10¹²,10³⁰) = 1,2,4,6,11,21,51 vs ⌈log₂⌉ = 1,4,7,10,20,40,100 |
| A2 machine, γ₀>1 | 13 204 prime-g starts (γ₀ up to 10⁹), 12 302 reach a reset: T54 inequality γ′ ≤ γ_s/4+1 violated 0 times at carries; K_reset > κ(γ₀) in 0 cases |
| A2 sharpness | κ attained for every κ = 0…11 by an exact machine orbit: g=29 (γ₀=2,5), 157 (17), 97 (67), 23 (293), 113 (1 061), 79 (4 169), 19 (20 902), 11 (173 715), 101 (352 837), 79 (1 444 161) |
| A3 exact check | 6/6 sharp witnesses (κ=1…6) confirmed by direct iteration of C on Fractions (independent of the machine): carries to the first reset = κ, G constant |
| E2 class entry | 1 092 prime-g reset seeds (half adversarial: two saturated primes compete, run exactly to their first reset); 2 leave persistence; j ≤ H(g), i ≤ H(g)−1, i ≤ K_poly(g) always; **1 090 cycle-entry states each statically certified for exactly the active prime**; 0 violations |
| E3 epoch lemmas | 22 670 epochs in 1 092 orbits: L1 (every carry is a pure saturated prime power or has unsaturated support), L2 (saturated-power carries leave the frozen competitor unchanged), Φ rises at every epoch-ending carry, saturation monotone, per-epoch size ≤ N_o+(N_o+1)(\|Abs\|+1): 0 violations |
| D1 stepper | exact general step `gstep` (reducing events included) = independent direct iteration of C: (G, γ, L) agree on 300/300 orbits × 10 steps |
| D2 chains | 14 074 orbits from composite/even g₀ (59 skipped: γ₀ > 2⁶⁰ or time cap), 21 796 segments, chain lengths {1: 7 928, 2: 4 645, 3: 1 426, 4: 75}: chain ≤ Ω(g₀); strict divisibility; carries per segment ≤ κ+H−1; carries to reset ≤ κ(γ_i); T54 at every carry; γ_{i+1} ≤ g_{i+1}(γ_before+1)/g_i and γ_before ≤ γ_i+4g_i; plateau steps ≤ 4g per carry; G=1 tail ≤ 4κ₃(t); total carries ≤ R(g₀,γ₀): **0 violations** |
| D3 end-to-end | 122 orbits whose chain of G-reductions (length 2: 64, 3: 57, 4: 1) ends in a persistent prime g: every reset state of the exact final class cycle is statically certified for the single active prime (T66); 0 failures |
| C1/C2 controls | g=31, L₀=2⁵·101² (v011 example): class cycle entered at carry 0, closed at 3 (carries 4,4,2); sharpest descent g=79, γ₀=1 444 161: 11 carries = κ |

## DATA (not claims)
* Observed entry index of the class cycle (carries after the first reset): maximum **208** (g = 211), median 0 (most random reset states are already in the cycle); the first reset state is already certified in 1 016 of 1 090 cycles. Active primes {2: 990, 3: 100} — the adversarial seeds produce survivor 3, never yet 5 or 7 in this sample.
* Against these, the proved bounds are H(211) ≈ 2.4·10¹³ and K_poly(211) ≈ 1.1·10⁸: they are **worst-case guarantees with large slack, not predictions**. In the dynamic-G sample the largest total number of carries before the final cycle was 43, while R(g₀,γ₀) has 14 digits.
* Dynamic-G sample (D2): final regimes G=1 (13 792 orbits), and persistent G = 17 (74), 23 (52), 37 (39), 5 (39), 19 (24), 43 (17), 31 (13), 7 (7), 68 (6), 13 (4), 11 (3), 85 (2), 25 (2) — including composite final g = 68, 85, 25.
* Which D2 checks are informative: the T54/κ checks, the γ recursion, the divisibility chain and the G=1 tail are tight; the carry bounds κ+H−1 and R(g₀,γ₀) hold with enormous slack (H is exponential in the orders), so they are consequences of the proofs, not measurements.
* The D-sample is built from composite/even g₀ with two primes q ≡ 1 (mod g₀) plus small primes (`gen_dyn_seed`); it is not exhaustive over initial fibres. The theorems are statements about every x₀.
* E5 (composite/even scope): status of `cert_sat` at all reset states of six exact composite cycles — g=15 (4 states), 39 (12), 51 (8), 57 (18), 68 (16), 87 (28): all 'window' (S5 fails). The survivor is nevertheless unique (T60) and the class cycle is entered within H(g) carries (T70(a)).
* Engineering note: v011's exact-G check enumerated every divisor of L and exhausted memory (exit 137) on adversarial seeds; field12.py uses a lazy, early-exit version (same value; None above 3·10⁶ divisors).

## OPEN (not claimed)
* **O12.1** Exact transient time / a bound near the observed indices. **O12.2** Static certificate for composite/even g (replace S5 by a condition on plateau steps with gcd(g,w) > 1). **O12.3** T71 where T67 does not apply. **O12.4** closed-form m_p and survivor for the q-carry families. **O12.5** infinitely many carry sizes. The q = 11 (g = 6689) class-closure certificate remains incomplete.
* Everything here is a consequence of the chosen collective map C(x) = x + L²/G (nonselection theorem, v002); no claim is made about other UNNS grammars.

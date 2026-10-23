# FIELD-I v012 — THEOREMS (T69–T73): Effective Predictability, Bounds on the Transient

Status tags: **PROVED** (hand proof from earlier theorems; the tests are consistency checks, not the proof), **DATA**, **OPEN**.
Notation as in v009–v011: a state x = γL²/g with g = G(x), L = lcm D(x), exponent state E = (e_p), o_p = ord_g(p), w = γ+1, w = γ+1 at a plateau step.
A *carry* (= preserving growth event) is a step with L′ ≠ L; a *reducing event* is a step with G′ < G (T35a); a *segment* is a maximal run of constant G; a *reset state* has γ = 1.
Throughout, "carry events" are counted, not collective-map steps (a plateau has at most 4g steps, v007 T37).

Question of v012 (O11.1): **how far can the transient continue before the rigid regime is certified?** The bounds below depend on the finite data (g₀, γ₀) only — not on the size of the exponents.

Definitions. f(a) = ⌊a/4⌋ + 1.  κ(a) = least k with fᵏ(a) = 1 (κ(1) = 0).  P_g = {primes p ∤ g : p² < g} (g odd), {p ∤ g : p² ≤ 4g} (g even): the only primes that can carry after the first reset (T52(c)).
H(g) = ∏_{p∈P_g}(2·o_p − 1).  Σ = Σ_{P_g} o_p, ω = max o_p, Φ = Σ_{P_g}(o_p − 1), K_poly(g) = (Φ+1)·(Σ + (Σ+1)(ω+1) + 1).

---------------------------------------------------------------------------------------------------------------------------------

## T69 — The reset-descent bound (PROVED; sharp)

**Statement.** In a segment of constant G = g (any g, composite and even included), started at a state with γ = γ₀, the first reset state is reached after at most **κ(γ₀)** carries, unless a reducing event ends the segment first. Moreover
 κ(a) = least k with 4ᵏ > (3a−4)/2  (a ≥ 2)   [upper bound proved; equality exhaustively checked for a ≤ 300 000],
hence κ(a) ≤ ⌈log₂ a⌉ (the form in the proposal) and κ(a) ≤ ⌈log₄ a⌉ + 1. Examples: κ(2) = 1, κ(10) = 2, κ(100) = 4, κ(1000) = 6, κ(10⁶) = 11 (proposal: 1, 4, 7, 10, 20).
**The bound is attained**: for every κ ∈ {1,…,11} (recorded run; witnesses listed in RESULTS) an exact residue-machine orbit needs exactly κ(γ₀) carries, e.g. g = 11, γ₀ = 173 715: 9 carries; g = 79, γ₀ = 1 444 161: 11 carries (proposal: 21). So no better function of γ₀ alone exists.
*Proof.* T54: a carry from a plateau that started at γ_s ≥ 1 gives γ′ ≤ γ_s/4 + 1; γ′ is an integer, so γ′ ≤ f(γ_s). f is nondecreasing, hence after k carries γ ≤ fᵏ(γ₀), and γ is 1 as soon as fᵏ(γ₀) = 1. Between carries γ only grows (T44(c)), so γ = 1 can only occur directly after a carry (or at the start).
Closed form: from a_{k+1} ≤ a_k/4 + 1 one gets a_k − 4/3 ≤ (a₀ − 4/3)/4ᵏ, so a_k < 2, i.e. a_k = 1, once 4ᵏ > (3a₀−4)/2. The log₂ form: 2ᵏ ≥ a gives 4ᵏ ≥ a² > (3a−4)/2. QED
*Tests A1 (arithmetic, exhaustive), A2 (T54 inequality at every carry of 13 204 machine starts with γ₀ up to 10⁹, 12 302 reaching a reset; K_reset ≤ κ(γ₀) always), A3 (sharp witnesses re-run by exact iteration of C on Fractions, independent of the machine).*
Scope: counts carries, not steps; the first plateau and every later one has at most 4g steps (T37), so the reset is reached in at most (κ(γ₀)+1)·4g collective steps.

---------------------------------------------------------------------------------------------------------------------------------

## T70 — The class-counting entry bound (PROVED)

**Statement.** Let a segment have constant G = g and let s₀ be its first reset state. Then
 (a) if G stays g forever, the reset-state class sequence s₀, s₁, … repeats within H(g) steps: the first repeated class occurs at index j ≤ H(g), the cycle is entered at an index **i ≤ H(g) − 1**, and from s_i on the orbit is purely periodic (x_{n+P} = ρ²x_n, T51);
 (b) if the segment ends with a reducing event, it ends before the carry number H(g) after s₀;
 (c) for **prime g** (more generally whenever T66 applies) the entry state s_i is **statically certified** (S3–S5) for the unique active prime r.
So the number of carries from the start of the segment to a certified state is at most κ(γ₀) + H(g) − 1, independent of the exponents.
*Proof.* After the first reset every carry is complete with M² < g (g even: ≤ 4g) (T54, T52(c)), so only primes of P_g change their exponent; the other exponents are constant along the orbit. By T67 the next reset state is a function of the class vector (c_p(e_p))_{p∈P_g} (T51 class lemma), and a class has at most 2o_p − 1 values (exact below saturation, then o_p residues), so there are at most H(g) class vectors.
Among s₀,…,s_H two share a class; the first repeat j ≤ H gives the entry i < j ≤ H, so i ≤ H−1, and the closure principle (T51) makes the orbit periodic from s_i. (b) If the segment lasted H carries after s₀ the same pigeonhole argument would make it periodic, so no reducing event could occur (persistence of the next step is a function of the class, T51).
(c) In the cycle every carry recurs infinitely often, hence is a prime power (T55), and by T60 only one prime r carries. r is saturated: its exponent rises in every period while its class returns, impossible for an unsaturated class (exact). The orbit from s_i carries only r and stays persistent, which is the hypothesis of the necessity half of T66; so S3, S4 hold and S5 is automatic for prime g. The availability of coprime M does not depend on r's phase (r saturated), so S4 holds at s_i as well as at the worst-case phase. QED
Review check: the proposal's table H(11) = 171, H(31) = 2 655, H(59) = 21 297 195 is reproduced (test E1). Its index is sharpened to H − 1, and ⌈log₂γ₀⌉ replaced by κ(γ₀).
*Tests E2: 1 092 prime-g reset seeds incl. adversarial competing seeds run exactly to their first reset; j ≤ H, i ≤ H−1, every cycle-entry state certified for exactly the active prime, 0 violations.*

---------------------------------------------------------------------------------------------------------------------------------

## T71 — The polynomial entry bound (PROVED for g prime, or whenever T67 applies)

**Statement.** In the setting of T70 (G = g from s₀ on; g prime, or every prime factor of g larger than the squares of all carries), the entry index (and the exit index) satisfies
 **i ≤ K_poly(g) = (Φ+1)·(Σ + (Σ+1)(ω+1) + 1)** — a cubic polynomial in the multiplicative orders instead of the product H(g).
For g = 11, 31, 59, 101, 197: K_poly = 2 688, 44 928, 1 243 920, 10 707 144, 229 237 866 (H = 171, 2 655, 21 297 195, ≈10⁸, 1.8·10¹⁵). So K_poly improves on H from g ≈ 59 on; the minimum of the two is the bound.
*Proof.* Call p ∈ P_g saturated if e_p ≥ o_p − 1. Saturation is monotone (exponents never decrease).
 **L1 (reduction).** The next carry M* = smallest available M (T67) is either a pure power r^a of a saturated prime r, or its prime support lies entirely among unsaturated primes. Indeed if M = r^a·s (a ≥ 1, s > 1 coprime to r, r saturated) is available through d, then d′ = d·r^{i−e_r−a} with i ≡ e_r + a (mod o_r), 0 ≤ i ≤ e_r, is a smaller divisor ≡ 1 (mod g) with new part s < M (the T55 argument), so M is not minimal.
 **L2 (frozen competitor).** Availability of M with unsaturated support depends on the residues of the saturated primes only through the full subgroups ⟨q⟩, and on the exact exponents of the unsaturated primes. Hence c_U := min{available M with unsaturated support} is *constant* as long as no unsaturated exponent changes.
 **Epochs.** An epoch is a maximal run of carries that are pure powers of saturated primes; it ends with a carry of unsaturated support (an *epoch-ending* carry), or never. Such a carry raises Φ_cur = Σ_{P_g} min(e_p, o_p−1) by at least 1 (each prime of its support has e_p < o_p − 1), so there are at most Φ epoch-ending carries, hence at most Φ+1 epochs.
 **Inside an epoch** the saturated primes are independent odometers Z/o_p with fixed tables Abs_p (T56/T65: the tables depend on the saturated set and on the frozen exact exponents), plus the frozen competitor c_U (if c_U ever wins, the epoch ends). Let p* = argmin m_p over the saturated primes, m_p = p^{maxgap(Abs_p)} (T64).
 *Claim A.* Every saturated r ≠ p* fires at most |Abs_r| ≤ o_r times in the epoch. After its first firing r's phase lies in Abs_r and each further firing moves it to the next element cyclically; within |Abs_r| landings it lands on the element a* before the largest gap, where its pending carry is m_r. There c_{p*} ≤ m_{p*} < m_r (T64(i)), so r never fires again.
 *Claim B.* If p* fires |Abs_{p*}| + 1 times in a row (no other prime, no c_U), the system returns to the state it had after the first of these firings, hence repeats forever: the class cycle has been entered. So in an epoch that is not the final periodic one, runs of consecutive p*-firings have length ≤ |Abs_{p*}|, and there are at most N_o + 1 such runs, N_o ≤ Σ_{r≠p*}|Abs_r| the number of non-survivor firings.
 So an epoch contains at most N_o + (N_o+1)·|Abs_{p*}| ≤ Σ + (Σ+1)ω saturated carries before it ends or its cycle begins, plus the ending carry. Summing over at most Φ+1 epochs gives the bound. The exit index obeys the same bound (the carry sequence is deterministic until the window is violated). QED
*Tests E3 (L1, L2, Φ-increase, monotone saturation, per-epoch size ≤ N_o+(N_o+1)(|Abs_{p*}|+1)) on 1 092 exact carry-level orbits (22 670 epochs); 0 violations. DATA E2: the largest observed entry index is 208 (g = 211), against H ≈ 10¹⁵ and K_poly ≈ 2·10⁸: the bounds are worst-case guarantees, not predictions.*

---------------------------------------------------------------------------------------------------------------------------------

## T72 — The dynamic-G effective bound (PROVED)

**Statement.** Let x₀ be any state (D(x₀) ≠ ∅) with G(x₀) = g₀ and γ₀. The orbit is a chain of segments g₀ ⊋ g₁ ⊋ … ⊋ g_k ≥ 1, each g_{i+1} | g_i, and
 (i) the number of segments with G > 1 is at most Ω(g₀) (counted with multiplicity);
 (ii) at a reducing event g_i → g_{i+1}: γ_{i+1} = (g_{i+1}/g_i)·(γ_before + 1)/r², r = L′/L ≥ 1, and γ_before ≤ γ_i + 4g_i; hence **γ_{i+1} ≤ g_{i+1}(γ_i + 4g_i + 1)/g_i** (a function of the finite data only);
 (iii) segment i contains at most **κ(γ_i) + H(g_i) − 1** carries (before its reducing event, or before the final class cycle is entered) and at most (carries+1)·4g_i + 1 steps;
 (iv) if the chain ends at G = 1 (regime I) the tail to the cycle 1 → 2 → 3 takes at most **4·κ₃(t)** steps, κ₃(t) = least k with fᵏ(t) ≤ 3, t = γ_k;
 (v) hence the total number of carries before the orbit is in its final class cycle is at most R(g₀, γ₀), where R(1, ·) = 0 and R(g, Γ) = κ(Γ) + H(g) − 1 + max_{g′ | g, 1 < g′ < g} R(g′, ⌊g′(Γ+4g+1)/g⌋). This is explicit and computable from (g₀, γ₀) alone.
*Proof.* (i) D(x) ⊂ D(x′) and G(x′) | G(x) (v005 T31); a strictly decreasing divisibility chain g₀ > g₁ > … > g_k ≥ 2 has Ω(g₀) ≥ Ω(g_k) + k ≥ k + 1.
(ii) x′ = (γ+1)L²/g. At a reducing event G′ = g′, y′ = g′x′ = g′(γ+1)L²/g, so γ′ = y′/L′² = (g′/g)(γ+1)(L/L′)² (T44(a), L | L′ because D ⊂ D′). Within a segment the plateau-start γ never rises (f(a) ≤ a), and each plateau adds at most 4g to γ (T37), so γ_before ≤ γ_i + 4g_i.
(iii) T69 gives the carries to the first reset, T70 the carries after it (the segment is a constant-G run, so T51/T52/T54/T67 apply to it verbatim; persistence of every step is a function of the class, so a segment that outlives H carries after its reset is periodic and never reduces). The step count: ≤ 4g per plateau (T37).
(iv) At G = 1 the state is x = s²t, γ = t squarefree (T30, T32), and t → sqf(t+1). Among t+1,…,t+4 one is divisible by 4, so within 4 steps t drops to at most (t+4)/4, i.e. to ≤ f(t) (and values ≤ 3 lie in the cycle).
(v) Combine (ii)–(iv), maximising over the possible chains. QED
This closes the dynamic-G part of O11.1 as an *existence of an explicit bound*; the bound is astronomically loose (it is dominated by H(g_i)). It does not give the exact transient time.
*Tests D1 (exact stepper `gstep` = independent direct iteration of C, 300 orbits × 10 steps), D2 (14 074 orbits from composite/even g₀, 21 796 segments: all of (i)–(v) as inequalities, 0 violations; chain lengths up to 4), D3 (122 orbits whose chain of G-reductions ends in a persistent prime g: every reset state of the final exact class cycle is certified for the single active prime).*

---------------------------------------------------------------------------------------------------------------------------------

## T73 — Registered corrections and scope notes

(E12.1) **v011 T68(a) scope.** v011 T68(a) is worded for "every persistent orbit". Its justification (necessity half of T66) is proved for **prime g** (S5 automatic) only. For composite or even g the hypothesis S5 (no prime factor of g ≤ m²) can fail while the orbit is persistent — in all six exact composite cycles tested (g = 15, 39, 51, 57, 68, 87) *every* reset state fails S5 (status 'window', test E5). So for composite/even g the survivor exists (T60) and the class cycle is entered within H(g) carries (T70(a)), but **static certification as formulated in T66 is not available** (OPEN O11.2). v011 is preserved unchanged; this entry is the erratum.
(E12.2) The proposal's T69 is correct but loses a factor 2 per carry: its step b′ ≤ ⌊(b+1)/4⌋ ≤ ⌊b/2⌋ discards the factor 4; the sharp statement is κ(γ₀) (≈ log₄ γ₀) and it is attained.
(E12.3) The proposal's T70 is correct; the entry index is ≤ H − 1 (repeat ≤ H), and T71 supplies a bound that does not grow like a product over primes.
(E12.4) "Bound from arbitrary seed before G stabilizes — open" in the proposal is answered by T72 as an explicit bound; the *exact* transient time is still open.

---------------------------------------------------------------------------------------------------------------------------------

## Status after v012

PROVED: T69 (sharp reset-descent), T70 (class-counting entry bound; certified entry for prime g), T71 (polynomial entry bound), T72 (dynamic-G effective bound), T73 (registered corrections).
OPEN: **O12.1** the exact transient time / a bound that is within a small factor of the observed entry index (observed ≲ 200 vs. bounds ≥ 10⁸); **O12.2** static certification for composite/even g (= O11.2; S5 must be replaced by a condition on the gcd(g,w) steps); **O12.3** T71 for composite g where T67 does not apply; **O12.4** closed-form m_p and survivor for the q-carry families (= O11.3); **O12.5** infinitely many distinct carry sizes (= O11.4); the q = 11 class-closure certificate (g = 6689) is still not completed.
All bounds are consequences of the deliberately chosen collective map C(x) = x + L²/G (nonselection theorem, v002); they say nothing about other UNNS grammars.

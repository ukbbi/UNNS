# RGG-1 — first relational grammar candidate (note, 2026-10-21)

Status labels: **[proved]** exact argument, **[checked]** finite test only, **[proposed]** definition/choice, **[untested]**.
Baseline manuscript v2 (43 pp, 61/61) is untouched. Verifier: `rgg1.py` (15 checks, ALL PASS, exact integer arithmetic + one rank computation).

## 1. Setting
Anchor occurrence (M,N)=(kN,N), d=N+1 ≥ 2 ⇒ route r=(k,d), value v(r)=k·d². [proved; Cor. 10.2]
Field occurrences (N∤M) are outside this first grammar.

## 2. Candidates [proposed]
- **J_mul(r,s) = {(k_r k_s, d_r d_s)}**, single-valued, "joint continuation = compose parameters".
- **J_join(r,s) = {(lcm k, lcm d)}**, adversarial alternative.
- **J_blind(r,s) = {t : v(t)=v(r)v(s)}**, value-only baseline.

## 3. Results
1. **[proved]** v(J_mul(r,s)) = v(r)v(s). So v is a monoid homomorphism and "same value" is a congruence for J_mul: value-level interaction never leaks. [checked on 106k triples]
2. **[proved, rule-imposed]** (ℕ×ℕ≥2, ·) is cancellative, so J_mul is faithful: same-value, different routes always have different continuations with every probe. This is a consequence of the definition, not a discovery; do not present it as evidence.
3. **[proved]** J_mul(r,s) ∈ J_blind(r,s). **Correction to a naive claim:** J_blind is never a singleton (it always contains (k_r k_s d_r², d_s) and (k_r k_s d_s², d_r) besides the product route), so "J_mul refines J_blind exactly when R(v_r v_s)>1" is vacuous. Check 3b printing 17424/17424 reflects this.
4. **[proved/checked]** Refinement T_q(k,d)=(k/q², dq) preserves value and is *covariant*: T_q(r)·s = T_q(r·s). Independent invariance fails (route changes, value does not); joint refinement gives T_q(r)T_q(s)=T_{q²}(rs). This is the hidden-sector pattern (joint ≠ independent) arising from a rule rather than an assumed B.
5. **[proved]** Exponent-lattice linearization: route ↦ (x,y)=(v_p(k),v_p(d))_p ∈ ℤ^{2P}; composition = addition; Π(x,y)=x+2y; refinements are translations by κ_p=(−2e_p,e_p), which span ker Π. So (V,Π,K,𝒯) with (H1),(H2) are now **derived from the nest rule + J_mul**, not postulated. (Over ℤ; real span is the manuscript's V.)
6. **Still open (honest):** J_mul does not determine B. Taking polarization B_Q(r,s)=Q(rs)−Q(r)−Q(s) of a quadratic Q: Q=|y|² gives δ=P (sees d separately), Q=|x|² gives δ=P, Q=|Π|² gives δ=0. Which Q is "natural" is a **[proposed]** choice; the grammar only supplies the criterion: independent refinement invariance ⇔ Q depends on exponents only via x+2y (Thm 7.1 applies to the lattice).
7. **[checked]** J_join is value-leaky: 56678/106320 same-value triples give different values (e.g. r=(4,2), r'=(1,4), s=(1,4): 64 vs 16). It realizes a genuine quotient obstruction with a *rule-derived* continuation, but it is tropical (max of exponents), not bilinear — the manuscript's theorems do not apply and need an order-theoretic analogue. **[untested]** whether this is more than a curiosity.
8. **[checked data, not theorem]** For field-involving pairs, a d-multiplicative, value-multiplicative continuation exists as an integer occurrence in only 4.6% of the sampled pairs; for anchor pairs always. Suggests an exclusion zone, but the rule for field routes is unchosen.

## 4. Critical assessment
- J_mul is essentially the multiplicative monoid on (k,d). Its content is that v is a homomorphism while d is not recoverable from v — real but modest. Do not oversell.
- Strongest new fact: refinements and K arise from the nest rule (item 5), closing part of the "bridge" for (V,Π,𝒯). B and F remain unconstructed.
- Most interesting next candidate: J_join-type (value-leaky) rules, since they produce interaction information invisible to the value without importing B.

## 5. Suggested next steps (not started)
(a) characterize all J that are value-congruences vs value-leaky among natural lattice operations (gcd, lcm, mixed); (b) order-theoretic deficit for non-additive J; (c) decide a justified rule for field occurrences; (d) only then consider Q for a B.

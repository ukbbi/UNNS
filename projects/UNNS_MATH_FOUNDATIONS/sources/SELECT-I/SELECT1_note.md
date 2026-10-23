# SELECT-I — Generative Operation Selection (2026-10-21)

Scope: integer-anchor routes r=(k,d), v(r)=kd². Manuscript v3, RGG-1/2/2.1 are untouched.
Verifier: `select1.py` (stdlib only, deterministic, a few minutes): 26 checks pass, 0 fail, 4 data rows; output in `select1_output.txt`; SHA-256 at the end.
Labels: **proved** / **checked** (finite, exact) / **hypothesis** / **open**.

## Verdict (S5)
Factor-preserving least continuation is **not** an intrinsic consequence of nesting and refinement. It is an additional rule, and the evidence says more precisely what that rule is:
1. The selection of J is exactly the selection of a *reachability order* (proved, standard: a commutative-associative-idempotent J is the lub of the order J(r,s)=s, and conversely).
2. The amplification moves E_{p,k}, E_{p,d} yield the divisibility order, and its lub is J_join (proved, checked). But E is a hypothesis: it is generated neither by the nest rule nor by T_q.
3. **Fork (new, proved, checked).** If the refinement T_q is *also* a generative step, the least common continuation is no longer J_join but J_ref(r,s)=(lcm(v_r,v_s)/L², L), L=lcm(d_r,d_s). Its value is lcm(v_r,v_s): it separates **no** fibre (v(J_ref(r,r'))=m on all 1277 same-value pairs, m≤3000). With inverse refinements as steps, no single route is selected at all: the minimal continuations are the whole fibre F(lcm(v_r,v_s)) (122/144 test pairs have more than one).
   So the separation theorem of §11 holds exactly when T_q is treated as a symmetry/equivalence and not as a continuation step. That choice is a further obstruction, not a free detail.
4. Iterating the nest rule on its own value m (N|m) gives m'=(m/N)(N+1)²: m | m' only for N=1 (m'=4m). Natural nest iteration consumes the factor N; it does not retain factors (proved; checked for m≤2000). Whether this is the right reading of UNNS continuation is not established by the material available; I flag it as a reading, not a finding about canonical UNNS.

## S1 — Coordinate rigidity [proved; your proof is correct]
If f(q(N+1)−1)=q f(N) for all primes q (hence all q by iteration) then g(d)=f(d−1) satisfies g(qd)=q g(d); with L=lcm(d₁,d₂), g(d₁)/d₁=g(L)/L=g(d₂)/d₂, so f=c(N+1). Checked: c(N+1) passes; N, N², 2N+1, N+2, ⌊1.5(N+1)⌋ fail; finite-range linkage on d≤240.
Consequence: J_N and the occurrence join J_occ are not covariant (failures 10088/11737 and 10306/11737 on tested pairs; worked example (4,2),(4,3),q=2: (1,16) vs (1,6), while J_join gives (1,12)=(1,12)). This ties to Lemma 11.14: separation is robust across charts, covariance is not.
Caveat: rigidity says *which chart is homogeneous under T_q*, which is close to the definition of T_q; it does not say why UNNS must require covariance.

## S2/S3 — Reachability and minimal continuation
- E only: r⪯s iff k|k', d|d' [proved, checked exactly]; lub = J_join [proved, brute force 144 pairs]. Your "Conditional Selection Theorem" is true but definitional: J_join is the lub of that order. What is not definitional: (a) minimality need not be an extra axiom (below); (b) the order itself is the real assumption.
- E + forward T_q: r⪯s iff d|d' and v|v' [checked]; lub J_ref.
- E + T_q and inverses: r⪯s iff v|v' (equal-value routes mutually reachable) [checked, sources k≤3].
- **Minimality from absorption (proved).** For a semilattice J: retention (J(r,s) is E-above both) ⇔ ≤_J ⊆ ⪯_E; absorption (r⪯_E s ⇒ J(r,s)=s) ⇔ ⪯_E ⊆ ≤_J. Together ≤_J=⪯_E, hence J=J_join. So "least" is derived, from absorption.

## S4 — Discrimination matrix [checked; box k≤10,d≤10, fibres m≤1500, grid 24×24]
Columns: closed, commutative, idempotent, associative, T-covariant, retention, absorption, separates fibres (probe r), value-descends.
| op | clo | com | idem | assoc | cov | ret | abs | sep | val |
|---|---|---|---|---|---|---|---|---|---|
| J_join | 1|1|1|1|1|1|1|1|0 |
| J_max | 1|1|1|1|1|0|1|0|1 |
| J_min | 1|1|1|1|1|0|0|0|1 |
| J_lexmax | 1|1|1|1|1|0|1|0|0 |
| J_mul | 1|1|0|1|0|1|0|0|1 |
| J_N | 1|1|1|1|0|0|0|1|0 |
| J_occ | 1|1|1|1|0|0|0|1|0 |
| J_ref | 1|1|1|1|1|0|1|0|1 |
| J_mixB (gcd k, lcm d) | 1|1|1|1|1|0|0|0|0 |
| J_mixA, J_meet | partial: not closed |
Algebra + covariance admit six operations: J_join, J_max, J_min, J_lexmax, J_ref, J_mixB. Adding retention leaves only J_join. Notes: J_N and J_occ *are* associative (lcm in a chart) — an expectation I had wrong; J_mul separates nothing because it is not idempotent (v(r×r)=v(r×r')=m²). J_max is confirmed as covariant and not separating, as in your note; it also satisfies absorption, so absorption alone does not select J_join.

## What remains open
- Independent justification of E (amplification as a generative step) and of treating T_q as a symmetry rather than a step; retention as a requirement (nest iteration consumes factors).
- A regime-dependent family is now concrete rather than speculative: factor-preserving continuation gives J_join (relationally rich); a refinement-absorbing continuation gives J_ref (value-level, no fibre separation).
- Nothing here bears on physics or entanglement.

Test bugs corrected during development (not mathematical errors): box/prime-list limits in the reachability BFS, a separation test that mis-scored non-idempotent J_mul, five wrong expected-profile entries (J_lexmax absorption, J_N/J_occ associativity, J_ref absorption, J_mul separation).
cd2f3510dbf28f00b2958a0d69d94c95fe93f2638eb01e8622f9c4aabaa72095  select1.py

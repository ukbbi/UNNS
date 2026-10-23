# Phase 2C — Generative-to-Observable Projection: Constructive Theorem Search

Status: **SPECIFICATION + COUNTEREXAMPLES; PRIMARY THEOREM OPEN**. Does not change the canonical Operator XVI or any earlier files.

## Source-locked foundations
The uploaded *Mechanisms, Structural Closure, and Proto-Closure in the UNNS Substrate* defines a mechanism M=(Σ,R,C,O); a refinement sequence S₀→S₁→…; structural closure as a nontrivial recurrent orbit (Definitions 3, 6, 7), with the refined approximate recurrence d(Sₙ,Sₙ₊ₖ)<ε for all sufficiently large n and >1 structural equivalence class (Definition 12). Proto-closure precedes numerical evaluation (Definition 9). None of those definitions specifies a Hilbert space, a probability measure, an observable projection or additivity.

## Primary target, with types
Define a specified mechanism domain 𝓜_pc, observable vector space V, and projection Π:𝓜_pc→V, plus a representation Π_ref of admissible refinements. Prove *from independent generative properties* that for Π-generated orthogonal refinements v=u+w,

W(v)=W(u)+W(w), u⊥w.

The proof must not assume norm-square, orthogonal additivity, setting-independent unnormalized totals, or the Born rule in the hypotheses under a renamed form. In finite-dimensional real V, if radial W(v)=f(‖v‖), continuity and orthogonal additivity hold and W(v)=‖v‖^q for q>0, then q=2 (take u=e₁,w=e₂). This is a **conditional standard identity**, not an UNNS theorem.

## Candidate constructive bridge (explicitly exploratory)
Take Σ={A,B}, deterministic alternating rewrite A↔B, discrete metric, and admissible refinement as iteration. Π₀(A)=e₁, Π₀(B)=e₂. Its orbit is a nontrivial 2-cycle. Π₀ can be extended to a *formal split* relation e₁+e₂, but the mechanism does not mandate that relation. A competing Πθ rotates the output vectors by θ and preserves recurrence; an amplitude-scaled Πs changes norms. The projection and its weight are additional choices. For fixed Π₀, the family Wq(v)=‖v‖^q admits every q>0. The counterexample destroys any claim that proto-closure alone selects q.

## Required proof obligations / gates (frozen)
- C0 BASELINE: byte-for-byte SHA-256 match of user-provided Phase 2B report; stop with nonzero exit on mismatch.
- C1 SOURCE: finite recurrence witness agrees with source definitions (PASS possible); no identification with XVI.
- C2 PROJECTION: provide a mathematically specified Π and induced refinement action (CONSTRUCTED_TOY, not unique/canonical).
- C3 NATURALITY: show compatibility of Π with *all admissible refinement morphisms* from independently defined rules; a chosen map alone is INSUFFICIENT.
- C4 CONSERVATION: derive orthogonal additivity from C1–C3 without postulating it. Must exclude q=1 and q=3 witnesses before PASS.
- C5 QUANTUM: only if C4 passes, extend to complex phases, contexts and multipartite networks; not attempted here.

Primary PASS requires C0–C4 all PASS with a checked proof. Failure to specify the independently fixed refinement-to-observation map -> OPEN; counterexample to an unconditional implication -> FAIL_UNCONDITIONAL. Tests passing are not proof gates passing.

## Adversarial controls and falsification
1. Period-two orbit with weights q in {1,1.5,2,3,6}: all preserve recurrence, only q=2 additive at e₁,e₂.
2. Rotation Πθ: state recurrence survives all θ; does not select q.
3. Scaling Πs: state recurrence survives all positive s; no canonical observable normalization follows.
4. An explicit artificially additive rule gives q=2, but is classified as AXIOM_INSERTED rather than DERIVED.

## Relation to locality
No Bell locality claim is made. A later entanglement bridge must explicitly examine factorization P(x,y|a,b,λ)=P(x|a,λ)P(y|b,λ) and measurement independence ρ(λ|a,b)=ρ(λ), and identify which assumption a proposed model relaxes.

## Verdict policy
C0 baseline verification is a software/integrity result. C1 finite orbit checks a toy mechanism. C2 is candidate construction only. C3–C4 remain OPEN/NOT_DERIVED. Phase 2B remains unchanged.

# XVI Closure Theorem — Phase 1 v001 (attempt and counterexample audit)

**Status: NOT PROVED.** This is a theorem investigation, not a demonstration that canonical Operator XVI entails quantum probabilities. Existing Phase 0 and canonical XVI are unchanged.

## Scope and dependencies

Phase 0 defines a two-branch antisymmetric tensor and the family of normalized measurement probabilities proportional to |amplitude|^q. Phase 1 asks whether an *independently specified* recursion entails rotation-independent **unnormalized** structural weight, and thus selects q=2. No quantum amplitudes, Born rule, or Bell targets are used in the recursion below. The word “closure” in the toy model refers only to its mathematically defined rotational averaging; it must not be equated with canonical Operator XVI without a separately proved correspondence.

## Definitions

Let V=R^2 with its standard Euclidean rotations R_t (the Euclidean metric is provided as geometry, not derived). Let w:V→[0,∞) be bounded on each circle, measurable on circles. Define Haar rotational averaging A[w](v)=(1/2π)∫_0^{2π} w(R_t v)dt. The candidate recursion is G[w]=(w+A[w])/2 and w_(n+1)=G[w_n]. A is a positive, linear idempotent projection on functions for which these integrals exist. Its output is rotation invariant and G^n[w]=A[w]+2^(-n)(w-A[w]). This is a concrete recursion, defined without probabilities.

Define *weak closure* as G[w]=w. Define *basis-weight closure* for a pair of orthonormal measurement coordinates as Z_q(θ)=|cos θ|^q+|sin θ|^q being independent of θ. Define *orthogonal refinement conservation* as M(v)=M(P_e v)+M(P_{e⊥}v) for every unit e and every v, with M(v)≥0, M(0)=0. These three notions MUST NOT be conflated.

## Proposition 1 (proved): weak closure is insufficient

The fixed points of G are exactly rotation-invariant weights. For any q>0, w_q(v)=||v||^q is a fixed point. Thus G's weak closure does not select q=2. Counterexamples q=1 and q=3 are constructive, nonnegative, and admit recursive refinement without changing the fact of G-fixedness. **G1 partial, G2 weak form passed; G3 and G4 fail for this toy recursion.**

Proof: Haar invariance gives A^2=A and A[w_q]=w_q. Subtract A[w] from the recurrence to get w_n-A[w]=2^-n(w_0-A[w]); therefore the limit is radial. Every radial weight is fixed. QED.

## Proposition 2 (proved): additional orthogonal refinement conservation selects quadratic radial weights

Assume M(v)=f(||v||)≥0 is radial and finite for each v, and that M(v)=M(P_e v)+M(P_{e⊥}v) for **all** e and v. For s,t≥0, take v=(s,t) and the coordinate basis to obtain f(sqrt(s²+t²))=f(s)+f(t). Put h(u)=f(sqrt u). Then h(u+v)=h(u)+h(v) for u,v≥0. Nonnegativity makes h monotone; the monotone additive solutions are h(u)=c u, c≥0. Hence M(v)=c||v||². If the normalization M(e_1)=1 is imposed, c=1. QED.

**Dependency audit:** Radiality follows from the toy Haar recursion only in the limit; orthogonal refinement conservation is EXTRA, not derived from G and not proven for canonical XVI. The result is conditional and is not a UNNS derivation of the Born rule. Full real/complex Born rules and multipartite consistency also remain open.

## Proposition 3 (proved): fixed unnormalized projection total selects q=2

For finite q>0, Z_q(0)=1 and Z_q(π/4)=2^(1-q/2). If Z_q is constant then q=2. Conversely Z_2(θ)=1 for all θ by the Pythagorean identity. The tensor amplitude common factor (1/sqrt2)^q multiplies Z_q and cannot change uniqueness. This is a known consequence of Euclidean orthogonality; it is NOT a novel substrate theorem.

## Bell-locality and probabilities

For q>0, the normalized q-family is P(++ )=P(-- )=sin^q(Δ)/(2[sin^q(Δ)+cos^q(Δ)]), and P(+-)=P(-+)=cos^q(Δ)/(2[sin^q(Δ)+cos^q(Δ)]), using absolute values. Marginals are 1/2, hence no-signalling for all q. A *Bell-local* model requires a setting-independent λ distribution ρ(λ) and factorization P(x,y|a,b)=∫ρ(λ)P_A(x|a,λ)P_B(y|b,λ)dλ, together with measurement independence ρ(λ|a,b)=ρ(λ). Violation of CHSH excludes this package of assumptions; specifying a joint tensor is not a physical explanation of which assumption fails. The q-family is a contextual joint-probability model; no underlying causal dynamics or loophole-free implementation is supplied.

## Preregistered gates and verdicts (v001)

| Gate | Requirement | v001 verdict |
|---|---|---|
| G1 | Explicit recursion not relying on quantum probabilities; demonstrably identified with independent UNNS canonical rules | **PARTIAL**: explicit toy recursion; UNNS mapping not derived |
| G2 | Prove relevant closure invariance follows from recursion | **PARTIAL**: rotational fixed-point closure proved; basis-weight/refinement conservation not implied |
| G3 | Quadratic measure without assuming equivalent additivity | **FAIL / OPEN**: obtained only with an additional axiom |
| G4 | Exclude q≠2 from the derived assumptions alone | **FAIL**: q=1,3 are radial fixed points |
| G5 | Reproduce Bell/NS at q=2, with fixed settings | **PASS as reference calculation only**, not a new substrate prediction |

Acceptance of a future TRUE SUBSTRATE theorem requires ALL of G1–G4 proved without importing orthogonal additivity, quadratic normalization, or the quantum correlation target under other names. Falsification: exhibit any q≠2 satisfying all *actually derived* closure axioms; or demonstrate failure of an asserted invariant under refinement. G5 must be run without parameter fitting and cannot rescue failures of G1–G4.

## Counterexample matrix

- w_1(v)=||v||: G-fixed; orthogonal refinement sum at (1,1) equals 2 but unsplit sqrt2, so conservation fails.
- w_2(v)=||v||²: G-fixed and conserves orthogonal refinement.
- w_3(v)=||v||³: G-fixed; refinement sum at (1,1) equals 2 but unsplit 2sqrt2.
- w(v)=||v||²(1+ε cos(2arg v)), |ε|≤1: nonnegative but anisotropic; G contracts anisotropy by 1/2 at each step and tends to ||v||². This shows convergence to radiality, not power selection.
- Normalized q probabilities obey no-signalling even for q>2 and can exceed Tsirelson; operational conditions beyond no-signalling are necessary.

## Phase 2 requirement

Supply a frozen, source-cited definition of **canonical XVI** and an independently defined UNNS structural generator; prove or refute an operator-to-refinement-conservation lemma before using language such as “derived Born rule.” Do not rewrite XVI to engineer success. Extend beyond the restricted real plane (complex phases, multipartite, composition/network locality).

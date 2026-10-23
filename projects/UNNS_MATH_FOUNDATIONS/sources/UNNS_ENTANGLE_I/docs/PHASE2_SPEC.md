# Phase 2 — Orthogonal Refinement Conservation (v001)

## Status
**SOURCE-GATED / NOT PROVED.** The Phase 1 JSON is frozen, byte-identical, by SHA-256 in `config/PHASE2_LOCK.json`. This increment is a preregistered test program, **not** a claim that canonical Operator XVI has been analysed.

## Question
Does **canonical Operator XVI**, without modification or an inserted additivity assumption, entail for every admissible orthogonal decomposition v=u+w (u·w=0): M(v)=M(u)+M(w)? Distinguish recursively induced closure, rotation invariance and orthogonal refinement conservation.

## Frozen claims and nonclaims
- Phase 1 shows toy Haar averaging fixes radial powers ||v||^q for any q>0.
- Non-signalling does not distinguish q in the normalized family.
- For radial nonnegative weights, orthogonal refinement additivity implies M(v)=c||v||²; this is a **conditional** standard theorem.
- The canonical Operator XVI source (definition or executable with frozen version) is **not included** in the supplied baseline; the operator correspondence and primary theorem cannot be tested yet.

## Preregistered procedure (do not adapt after observing primary results)
1. Acquire canonical XVI source, version, equations, admissible state space, domain, update rule, limits, tolerances, and relevant UNNS structural-generator source. Record exact SHA-256 hashes; do not rewrite canonical code.
2. Define an independent adapter mapping the canonical state to a nonnegative scalar M and explain its operational meaning before testing; show that the mapping is not simply an L2/Born-norm definition. If unavailable, mark `MAPPING_UNDEFINED`.
3. Prove or disprove that the actual canonical map entails orthogonal additivity for all admissible refinements. Produce a symbolic statement with all assumptions and a numeric sweep only as a supporting check.
4. Test countermodels (radial q=1, q=3; anisotropic nonnegative measure) and nonorthogonal splits, and check their status under the *actual* canonical conditions.
5. Only if canonical additivity is derived independently, apply the nonnegative Cauchy-functional-equation theorem to select q=2. Never report the conditional theorem as an independent UNNS derivation.

## Fixed gates
- P2-G0 SOURCE_LOCK: authentic canonical source and version/hash recorded. **BLOCKED until provided.**
- P2-G1 OPERATOR_MAPPING: precise mapping from canonical dynamics to candidate M without quantum/Born postulate. **BLOCKED.**
- P2-G2 REFINE_LEMMA: derivation of orthogonal refinement conservation, with no equivalent hypothesis inserted. **OPEN.**
- P2-G3 ADVERSARIAL: either falsify by admissible counterexample or exclude q≠2 under *derived* axioms, not by assumption. **OPEN.**
- P2-G4 COMPOSITION: compatibility with separate branches, probability normalization, and locality assumptions independently audited. **OPEN.**
- P2-G5 BASELINE_INTEGRITY: frozen Phase 1 checksum matches. **Executable PASS/FAIL.**

## Acceptance and falsification
Accept a substrate-level q=2 selection claim only if P2-G0..G3 all pass, written proof covers full declared domain, and there is no imported orthogonal additivity, L2 metric as measure, or setting-dependent postselection. G4 must pass before claiming a physical theory of entanglement. Failure to prove is `OPEN`; a valid q≠2 counterexample respecting all canonical premises is `FALSIFIED`. No numeric tolerance can establish a universal theorem.

## First executed control
The attached independent script verifies hash integrity and computes refinement defects for radial power countermodels. These are logical controls, **not experiments on canonical XVI**.

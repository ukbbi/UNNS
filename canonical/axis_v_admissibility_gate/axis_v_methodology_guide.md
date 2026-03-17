# Axis V Methodology: Best Practices for Admissibility Gate Design

**Version**: 1.0.0  
**Date**: February 2026  
**Status**: Production Methodological Framework  
**UNNS Research Collective**

---

## Executive Summary

This document codifies the methodological principles underlying Axis V chamber design, validation, and certification. It serves as both a retrospective analysis of successful chamber development (V-2 through V-5) and a prescriptive guide for future mechanism discovery.

The core principle is **surgical precision over adversarial stress-testing**: each chamber enforces a single orthogonal invariant with brutal falsification discipline, rather than maximizing difficulty or parameter complexity.

---

## Part I: Foundational Principles

### 1.1 The Surgical vs Adversarial Distinction

**Surgical Chamber Design**:
- Enforces **one irreducible invariant** F(H)
- Uses **minimal computational complexity**
- Provides **binary admissibility oracle** (or well-defined continuous degradation)
- Operates **deterministically** (no solver timeouts, heuristics)
- Maintains **falsification discipline** (hard kill condition)

**Adversarial Design** (AVOID):
- Maximizes hardness or parameter-tuning difficulty
- Entangles feasibility with search/optimization complexity
- Introduces ambiguity (what counts as "violation"?)
- Optimizes for "breaking" the system
- Conflates mechanism testing with stress limits

**Key insight**: Axis V exists to **discriminate mechanisms**, not to find breaking points. A chamber that is "too hard" obscures whether utility failure is due to the invariant or computational intractability.

---

### 1.2 The Invariant-Falsifier-Signature Triad

Every chamber must specify three components before implementation:

**Invariant F(H)**:
- Mathematical definition: F: 𝓗 → {0,1} or [0,1]
- Computable from history H at step t
- Independent of utility realization (prevents circularity)

**Falsifier 𝓕(H)**:
- Maps histories to {PASS, FAIL}
- Brutal, non-negotiable: FAIL → chamber invalid
- Preregistered (no post-hoc adjustment)
- Statistically decisive (p < 0.001 or deterministic)

**Signature S**:
- Predicted temporal pattern of utility emergence
- Coupling mode: B_u (cliff) vs C_u (gradual)
- Predicted correlation: P(utility | F=TRUE) vs P(utility | F=FALSE)

**Example (V-5)**:
- Invariant: F_5(H) = 1 if XOR-SAT(H) = SAT, else 0
- Falsifier: 𝓕_5 = FAIL if utility realized while UNSAT
- Signature: Discrete cliff; P(U|SAT) >> P(U|UNSAT) = 0

---

### 1.3 Logic Container Selection

**L-B (Instantaneous Feasibility)**:
- Evaluates F(H_t) at each step t
- Violation → immediate collapse
- Use when: invariant is structural/instantaneous property
- Examples: V-3 (topology), V-4 (spectrum), V-5 (SAT)

**L-C (Accumulated Feasibility)**:
- Evaluates ∫_0^t F(H_s) ds over history
- Gradual degradation or threshold crossing
- Use when: invariant depends on historical accumulation
- Examples: V-1 (ancestral correlation), V-2 (ensemble structure)

**Decision criteria**:
- Does invariant depend on "how we got here"? → L-C
- Is invariant a property of current state only? → L-B
- Does violation have memory? → L-C
- Is violation binary and immediate? → L-B

---

### 1.4 Coupling Mode Selection

**B_u (Brittle Cliff)**:
- Binary collapse: F violation → utility impossible
- Extreme sensitivity at boundary
- Use when: feasibility is boolean (yes/no)
- Examples: V-3, V-4, V-5

**C_u (Stress-Gated)**:
- Continuous stress accumulation
- Gradual resistance increase
- Use when: feasibility degrades smoothly
- Examples: V-1, V-2

**Decision criteria**:
- Is there a sharp boundary between admissible/inadmissible? → B_u
- Does admissibility degrade continuously? → C_u
- Can you identify a discrete "violation point"? → B_u
- Is there a stress integral that accumulates? → C_u

---

## Part II: Chamber Design Protocol

### 2.1 Pre-Implementation Phase

**Step 1: Invariant Identification**

Ask:
1. What global property might gate utility?
2. Is it computable from history H?
3. Is it independent of utility itself? (avoid circularity)
4. Does it map to known mathematical structures? (graphs, matrices, constraint systems)

**Red flags**:
- Invariant requires utility knowledge (circular)
- Invariant is composite (combine V-3 AND V-4) → split into separate chambers
- Invariant is parametric (depends on free tuning) → surgical design broken

**Step 2: Non-Overlap Analysis**

Before implementing, prove non-overlap with existing chambers:

| Chamber | Depends On | Orthogonality Test |
|---------|------------|-------------------|
| V-3 | Edge topology | Edge rewiring changes V-3? |
| V-4 | Adjacency spectrum | Spectral perturbation changes V-4? |
| V-5 | Node-local bits | Bit flip changes V-5? |

New chamber must be:
1. Invariant under perturbations that change existing chambers, OR
2. Sensitive to perturbations that leave existing chambers unchanged

**Step 3: Falsifier Specification**

Preregister the falsifier:

```
𝓕(H) = FAIL if:
  [Specific, deterministic condition]
  
Example (V-5):
  Utility realized (U_t > U_crit for k consecutive steps)
  AND
  XOR-SAT constraints unsatisfiable (unsat_count > 0)
```

**Falsifier requirements**:
- Deterministic (no probabilistic thresholds unless p < 0.001)
- Observable (can be checked from chamber data)
- Brutal (no "close enough" - FAIL is chamber death)
- Independent of parameters (not tunable post-hoc)

**Step 4: Signature Prediction**

Predict temporal pattern **before running**:

- **Cliff behavior**: Utility snaps at feasibility boundary?
- **Hysteresis**: Once violated, can feasibility recover?
- **Accumulation**: Does violation history matter?
- **Correlation**: What's P(utility | F=TRUE) vs P(utility | F=FALSE)?

Write predictions in lab notebook / preregistration document.

---

### 2.2 Implementation Phase

**Architecture**:

```javascript
class FeasibilityPredicate {
  constructor(config) { /* parameters */ }
  
  evaluate(history, config) {
    // Returns: {feasible: boolean, metrics: {...}}
    // Must be deterministic for given (history, config)
  }
}

class Chamber {
  constructor(predicate, coupling_mode) {
    this.predicate = predicate;
    this.coupling = coupling_mode; // 'B_u' or 'C_u'
  }
  
  run(maxSteps) {
    for (t = 0; t < maxSteps; t++) {
      let F = this.predicate.evaluate(this.history, this.config);
      
      if (this.coupling === 'B_u' && !F.feasible) {
        this.collapsed = true;
        break; // Immediate termination
      }
      
      if (this.coupling === 'C_u') {
        this.stress += (1 - F.feasible); // Accumulation
      }
      
      // Generate next event...
      // Evaluate utility...
    }
  }
  
  testFalsifier() {
    // Checks if utility appeared during inadmissible state
    // Returns: 'PASS' or 'FAIL'
  }
}
```

**Key implementation principles**:
- **Determinism**: Same seed → same result
- **No hidden parameters**: All config explicit
- **Separation of concerns**: Feasibility check independent of utility evaluation
- **Comprehensive logging**: Record F(H_t), utility timelines, violation points
- **JSON export**: Full state for reproducibility

---

### 2.3 Diagnostic Development

Every chamber must implement **non-overlap diagnostics**:

**Test 1: Perturbation Invariance**

Goal: Prove new chamber invariant under perturbations that affect existing chambers

```javascript
function testInvariance(chamber, history, perturbationType) {
  let F_before = chamber.predicate.evaluate(history);
  
  let history_perturbed = applyPerturbation(history, perturbationType);
  // perturbationType: 'edge_rewire', 'spectral_nudge', 'bit_flip', etc.
  
  let F_after = chamber.predicate.evaluate(history_perturbed);
  
  assert(F_before === F_after, "Chamber not invariant under expected perturbation");
}
```

**Test 2: Sensitivity to Orthogonal Changes**

Goal: Prove new chamber sensitive to changes that leave existing chambers unchanged

```javascript
function testSensitivity(chamber, history) {
  let F_before = chamber.predicate.evaluate(history);
  
  let history_modified = applyOrthogonalChange(history);
  // Change that should affect this chamber but not others
  
  let F_after = chamber.predicate.evaluate(history_modified);
  
  assert(F_before !== F_after, "Chamber not sensitive to orthogonal changes");
}
```

**Test 3: Cross-Chamber Comparison**

Goal: Same seed produces different feasibility outcomes

```javascript
function testOrthogonality(chamber_A, chamber_B, seed) {
  let results_A = chamber_A.run(seed);
  let results_B = chamber_B.run(seed);
  
  // Expect: different feasibility outcomes
  assert(results_A.feasible !== results_B.feasible, 
         "Chambers showing correlated behavior - possible overlap");
}
```

---

### 2.4 Validation Phase

**Step 1: Falsifier Compliance**

Run N seeds (N ≥ 50), check:
- Falsifier triggers: 0 (must be zero)
- If falsifier triggers even once → chamber invalid

```
Falsifier Compliance Rate = (Seeds with 𝓕=PASS) / (Total Seeds)
Required: 100%
```

**Step 2: Utility Gating**

Compute conditional probabilities:
- P(utility | F=TRUE)
- P(utility | F=FALSE)

Expected patterns:
- **B_u chambers**: P(U|F=FALSE) ≈ 0 (strict gating)
- **C_u chambers**: P(U|F=FALSE) < P(U|F=TRUE) (stress effect)

If P(U|F=FALSE) ≈ P(U|F=TRUE) → invariant irrelevant to utility

**Step 3: Signature Validation**

Compare predicted vs observed temporal patterns:
- Cliff behavior: Check for abrupt collapse at violation point
- Hysteresis: Test recovery after violation
- Accumulation: Verify stress integral matches prediction

**Step 4: Cross-Chamber Validation**

Run all chambers on same seeds, verify:
- Different feasibility outcomes (orthogonality)
- Non-correlated failures (independence)
- Consistent statistical patterns across chambers

**Correlation matrix** (should show low correlation):
```
        V-3    V-4    V-5
V-3    1.00   0.15   0.08
V-4    0.15   1.00   0.05
V-5    0.08   0.05   1.00
```

High correlation (> 0.5) suggests overlap.

---

## Part III: Common Pitfalls & Solutions

### 3.1 Circular Validation

**Problem**: Invariant depends on utility, creating self-fulfilling prophecy

**Example (WRONG)**:
```javascript
F(H) = (utility_realized(H) AND some_other_condition)
```

This guarantees P(U|F=TRUE) = 1 by construction (circular).

**Solution**: Invariant must be computable **without** knowing utility status

**Test**: Can you evaluate F(H) on histories where utility is undefined?

---

### 3.2 Parameter Drift

**Problem**: Adjusting parameters post-hoc to "make chamber work"

**Example (WRONG)**:
```
Run chamber with α = 0.5 → doesn't show utility gating
Try α = 0.6 → still doesn't work
Try α = 0.8 → works! (use this)
```

**Solution**: Preregister parameter values or use parameter-free design

**Acceptable**: Calibration to achieve 50/50 SAT/UNSAT mix (statistical balance)  
**Unacceptable**: Tuning to maximize utility gating (outcome-targeted)

---

### 3.3 Disguised Overlap

**Problem**: New chamber secretly tests same mechanism as existing chamber

**Example**: V-3 tests acyclicity, V-X tests "tree-width < 5"
- Both depend on graph topology
- Tree-width ≤ 1 ↔ tree (special case of DAG)
- Not truly orthogonal

**Solution**: Operational diagnostics
- Edge rewiring test: If both change together → overlap
- Bit flip test: If both unchanged → overlap
- Require: one changes while other stays constant

---

### 3.4 Falsifier Leakage

**Problem**: Chamber allows utility in inadmissible states

**Example**:
```
Seed 12345: F=FALSE at t=500, utility appears at t=600
Falsifier doesn't trigger because utility appeared "after" violation
```

**Solution**: Prefix-monotonicity enforcement
- Once F violated, must remain violated (no recovery)
- Utility appearing at t=600 after violation at t=500 → FAIL

**Implementation**:
```javascript
testFalsifier() {
  let first_violation = this.timeline.findIndex(t => !t.feasible);
  let utility_time = this.timeline.findIndex(t => t.utility_realized);
  
  if (utility_time > first_violation) {
    return 'FAIL'; // Utility after violation
  }
  return 'PASS';
}
```

---

### 3.5 Soft Boundaries

**Problem**: Feasibility "boundary" is fuzzy, making falsifier ambiguous

**Example (WRONG)**:
```javascript
F(H) = (λ_max < 2.0 + ε)  // What is ε?
```

**Solution**: Hard boundaries
```javascript
F(H) = (λ_max ≤ 2.0)  // Binary, deterministic
```

For continuous degradation, use explicit stress function:
```javascript
stress(H) = max(0, λ_max - 2.0)  // Non-negative penalty
```

---

## Part IV: Certification & Production Readiness

### 4.1 Certification Checklist

Before declaring chamber "locked":

- [ ] **Invariant defined mathematically**
- [ ] **Falsifier preregistered** (deterministic condition)
- [ ] **Signature predicted** (written before validation)
- [ ] **N ≥ 50 seeds validated**
- [ ] **Falsifier compliance: 100%** (zero triggers)
- [ ] **Utility gating confirmed** (P(U|F=TRUE) >> P(U|F=FALSE))
- [ ] **Non-overlap diagnostics passed** (edge rewiring, bit flip, etc.)
- [ ] **Cross-chamber comparison** (low correlation with existing)
- [ ] **Code reviewed & documented** (comments, README)
- [ ] **JSON export tested** (reproducibility confirmed)
- [ ] **Known issues documented** (if any)

**Status levels**:
- **PENDING**: Exploratory, not yet validated
- **VALIDATED**: Passed checklist, but not production-certified
- **LOCKED**: Production-certified, no further mechanism changes allowed

---

### 4.2 Lock Conditions

A chamber is locked when:
1. All certification checklist items passed
2. Results published or preregistered
3. Mechanism accepted by research collective
4. No falsifier violations across extended validation (N ≥ 100)

**Once locked**:
- ✅ Allowed: Bug fixes (implementation errors)
- ✅ Allowed: Performance optimization
- ✅ Allowed: Visualization improvements
- ❌ Forbidden: Invariant changes
- ❌ Forbidden: Falsifier relaxation
- ❌ Forbidden: Parameter adjustments

**Rationale**: Lock prevents conceptual drift and ensures long-term reproducibility.

---

### 4.3 Production Standards

**Code quality**:
- Deterministic (no `Math.random()` without seeded RNG)
- Commented (explain non-obvious algorithms)
- Modular (separate feasibility logic from utility evaluation)
- Tested (unit tests for core functions)

**Documentation**:
- Invariant definition (mathematical)
- Falsifier specification (precise condition)
- Diagnostic protocols (how to test non-overlap)
- Parameter meanings (if any)
- Known limitations

**Reproducibility**:
- JSON export with full state
- Seed-level granularity
- Version tagging (v1.0.0, v1.1.0, etc.)
- Changelog maintained

---

## Part V: Advanced Topics

### 5.1 Continuous Feasibility

For chambers with F(H) ∈ [0,1] instead of {0,1}:

**Stress function**:
```javascript
stress(H) = 1 - F(H)
```

**Coupling**:
```javascript
if (coupling === 'C_u') {
  accumulated_stress += stress(H_t) * dt;
  U_crit_effective = U_crit * (1 + β * accumulated_stress);
}
```

**Falsifier** (modified for continuous):
```javascript
testFalsifier() {
  // Utility while stress > threshold?
  if (utility_realized && stress > stress_threshold) {
    return 'FAIL';
  }
  return 'PASS';
}
```

---

### 5.2 Hybrid Chambers

Combining multiple invariants (use sparingly):

**When justified**:
- Invariants are tightly coupled (e.g., spectral + Laplacian)
- Testing joint hypothesis (V-3 AND V-4)
- Interaction effects under investigation

**When NOT justified**:
- Just "combining existing chambers" without new insight
- Trying to "strengthen" weak chamber
- Adding complexity to improve statistics

**Rule**: If hybrid chamber, must show it's irreducible (cannot be decomposed).

---

### 5.3 Mechanism Interactions

Testing whether V-i and V-j interact:

**Protocol**:
1. Run V-i alone on seed S → result A
2. Run V-j alone on seed S → result B
3. Run V-i AND V-j jointly → result C

**Interaction detected if**:
- C.feasible ≠ (A.feasible AND B.feasible)
- C.utility ≠ f(A.utility, B.utility) for any simple f

**Implications**:
- If strong interaction → mechanisms not independent
- If no interaction → factorization holds

---

### 5.4 Scalability Considerations

**Computational complexity**:
- V-3 (DAG check): O(n) with DFS
- V-4 (spectral): O(n²) to O(n³) depending on method
- V-5 (XOR-SAT): O(n³) for Gaussian elimination

**Memory usage**:
- V-3: O(n) for recursion stack
- V-4: O(n²) for adjacency matrix
- V-5: O(mn) for constraint matrix

**Optimization strategies**:
- Sparse representations (V-4, V-5)
- Incremental updates (don't recompute from scratch)
- Early termination (collapse detection)

**Scalability limits**:
- n = 1000: All chambers fast (< 1 second per step)
- n = 10,000: V-4 and V-5 become slow (seconds per step)
- n = 100,000: Need specialized implementations

---

## Part VI: Future Directions

### 6.1 Discovering New Mechanisms (V-6, V-7, ...)

**Heuristics**:
1. Look for utility failures unexplained by V-1 through V-5
2. Identify mathematical structures not yet tested (e.g., homology, entropy)
3. Consider temporal dimensions (past, future, counterfactual)
4. Explore multi-scale feasibility (micro vs macro)

**Candidate V-6 classes**:
- **Informational**: Shannon entropy, mutual information constraints
- **Topological**: Homology classes, Betti numbers
- **Temporal**: Consistency with possible futures, counterfactual stability
- **Multi-scale**: Micro-macro alignment, scale separation

**Validation requirements** (same as V-1 through V-5):
- Define F(H) mathematically
- Specify brutal falsifier
- Predict signature
- Prove non-overlap with existing chambers

---

### 6.2 Completeness Question

**Open problem**: Are V-1 through V-5 sufficient, or do more classes exist?

**Approaches**:
1. **Exhaustive search**: Systematically test all mathematical invariants
2. **Dimension counting**: Algebraic topology of admissibility space
3. **Empirical gap**: Find utility patterns unexplained by current chambers

**Completeness theorem** (conjectured):
```
∃ finite N such that admissibility factors into N ≤ 10 irreducible classes
```

Proving or disproving this is major open problem.

---

## Conclusion

This methodology transforms chamber development from ad-hoc exploration into systematic science:

**Key principles**:
1. **Surgical precision**: One invariant, minimal complexity
2. **Falsification discipline**: Brutal falsifiers, no leakage
3. **Operational non-overlap**: Proven by diagnostics, not assumed
4. **Preregistration**: Invariant, falsifier, signature before validation
5. **Production standards**: Reproducibility, documentation, certification

**Impact**: Any future V-chamber must follow this protocol. Chambers that violate these principles will not be accepted into Axis V canon.

This document serves as both retrospective (explaining V-2 through V-5 success) and prescriptive (guiding future mechanism discovery). It ensures Axis V remains a rigorous, falsifiable framework rather than an informal collection of observations.

---

**Version History**:
- v1.0.0 (Feb 2026): Initial methodology based on V-2 through V-5 development

**Authors**: UNNS Research Collective  
**License**: CC BY 4.0  
**Repository**: github.com/unns-research/axis-v-methodology

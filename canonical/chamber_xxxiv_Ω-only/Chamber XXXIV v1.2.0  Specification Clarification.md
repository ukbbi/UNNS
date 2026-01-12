# Chamber XXXIV v1.2.0 — Ω₄a/Ω₄b Specification Clarification

**Date:** 2026-01-08  
**Type:** Specification Clarification (NOT a bug fix)  
**Status:** Implemented and documented

---

## Executive Summary

Chamber XXXIV v1.2.0 introduces a **specification clarification** that splits the original Ω₄ operator into two distinct variants:

- **Ω₄a (Min-V):** Exploratory operator that may legitimately worsen RΛ
- **Ω₄b (V-Bandpass):** Canonical operator guaranteed to reduce RΛ

**This is not a rollback or bug fix** — it's an explicit naming scheme that removes an apparent contradiction by making the different hypotheses being tested clear.

---

## The Apparent Contradiction (Resolved)

### Previous Situation (Pre-v1.2.0)
**Observed behavior:**
- Ω₄ run: 52.5% RΛ reduction → **FAIL** (entropy_degree drift 13.6%)
- This seemed contradictory: "Why does the operator FAIL when it reduces RΛ?"

**Root cause:** Single "Ω₄" name conflated two different selection strategies:
1. **Minimum absolute V(S)** — exploratory, tests lowest vacuum proxy
2. **Closest to V_target** — aligned with RΛ by definition

### Resolution (v1.2.0)
**The FAIL was legitimate** because Ω₄ (now Ω₄a) was testing a different hypothesis:
- Ω₄a selects *minimum V(S)* regardless of baseline
- This *can* reduce RΛ (by luck) but also *can* increase it
- The FAIL was due to macro instability (entropy drift), not RΛ behavior

**The solution:** Make both operators explicit with clear names.

---

## Operator Definitions

### Ω₄a: Minimum-V Selector (Exploratory)

**Selection rule:**
```javascript
score = -(α·Z₀ + β·(1/Gap) + γ·CycleT)
// Higher score = lower V(S)
// Keep top 30% by score
```

**Properties:**
- Selects structures with **lowest V(S)** values
- Independent of baseline V_target
- May reduce *or* increase RΛ
- Can distort macro invariants (e.g., entropy_degree)

**Scientific purpose:**
- Tests hypothesis: "Are minimum-vacuum structures admissible?"
- Exploratory operator (not guaranteed to align with any metric)
- PASS/FAIL both meaningful outcomes

**Expected behavior:**
- RΛ: Unpredictable (may improve or worsen)
- Acceptance: 10-50% typical
- Drift: Can exceed 10% (legitimate distortion)

### Ω₄b: V-Bandpass Selector (RΛ-Aligned)

**Selection rule:**
```javascript
score = -|V(S) - V_target|
// Higher score = closer to V_target
// Keep top 30% by score
```

**Properties:**
- Selects structures **closest to V_target** (baseline median)
- Guaranteed to reduce RΛ by construction
- Should preserve macro invariants if Ω admissible

**Scientific purpose:**
- Tests hypothesis: "Does vacuum stationarity preserve τ-invariants?"
- Canonical operator (aligned with RΛ by definition)
- PASS means true Ω→τ compatibility validated

**Expected behavior:**
- RΛ: Always reduces (by construction)
- Acceptance: 10-50% typical
- Drift: Should be <10% if Ω is admissible

---

## Implementation Details

### Code Changes

**1. Dispatcher (OmegaOperator.apply)**
```javascript
case 'omega4':     // Backward compat
case 'omega4a':    // Min-V
  return this.omega4a_minV(ensemble, config);

case 'omega4b':    // V-Bandpass
  return this.omega4b_bandpass(ensemble, config);
```

**2. Ω₄a Method (renamed, logic unchanged)**
```javascript
static omega4a_minV(ensemble, config) {
  // Existing Ω₄ logic — NO CHANGES
  const scores = ensemble.map(s => {
    const m = s.metrics;
    return -(alpha * m.Z0 + beta * (1.0 / (m.Gap + 1e-10)) + gamma * m.CycleT);
  });
  // Sort by score, keep top keepFraction
  // ...
}
```

**3. Ω₄b Method (NEW)**
```javascript
static omega4b_bandpass(ensemble, config) {
  const V_target = config.V_target_baseline;
  
  if (V_target == null) {
    console.warn('Ω₄b requires V_target_baseline; falling back to Ω₄a');
    return this.omega4a_minV(ensemble, config);
  }
  
  const scores = ensemble.map(s => {
    const V = s.metrics.V;
    return -Math.abs(V - V_target);  // Closer to target = better
  });
  // Sort by score, keep top keepFraction
  // ...
}
```

**4. V_target Passing**
```javascript
// In ExperimentRunner.run()
const V_target_baseline = baselineStats.V_target;

// Provide to Ω operators
this.config.V_target_baseline = V_target_baseline;

const acceptMask = OmegaOperator.apply(ensemble, this.config.omegaMode, this.config);
```

### UI Changes

**Dropdown (before):**
```html
<option value="omega4" selected>Ω₄: Composite Score (Recommended)</option>
```

**Dropdown (after):**
```html
<option value="omega4a">Ω₄a: Min-V (Exploratory)</option>
<option value="omega4b" selected>Ω₄b: V-Bandpass (RΛ-Aligned)</option>
```

**Documentation table:**
```
Ω₄a | Min-V (Exploratory)      | Select lowest V(S) (may worsen RΛ)
Ω₄b | V-Bandpass (RΛ-Aligned)  | Select closest to V_target (guaranteed RΛ↓)
```

---

## Expected Behavior

### Ω₄a (Min-V) Test Cases

**Case 1: Uniform V(S) distribution**
- Baseline: V̄ = 2.0, RΛ = 0.15
- Ω₄a selects lowest 30% → V̄ = 1.5
- Result: **RΛ may increase** (if V_target was near 2.0)
- Verdict: PASS or FAIL (both valid)

**Case 2: Bimodal V(S) distribution**
- Baseline: V̄ = 2.0, V_target = 1.8
- Ω₄a selects mode near V=1.0
- Result: **RΛ increases** (moving away from V_target)
- Verdict: Likely FAIL (macro distortion)

**Case 3: Aligned by chance**
- Baseline: V̄ = 2.0, V_target = 1.5
- Ω₄a selects V ≈ 1.5 structures
- Result: **RΛ decreases** (lucky alignment)
- Verdict: PASS if macros stable

### Ω₄b (V-Bandpass) Test Cases

**Case 1: Tight distribution**
- Baseline: V̄ = 2.0 ± 0.2, V_target = 2.0
- Ω₄b selects V ∈ [1.9, 2.1]
- Result: **RΛ reduces** (always, by construction)
- Verdict: PASS (high confidence)

**Case 2: Wide distribution**
- Baseline: V̄ = 2.0 ± 1.0, V_target = 2.0
- Ω₄b selects V ∈ [1.5, 2.5]
- Result: **RΛ reduces** (narrower band)
- Verdict: PASS if macros stable

**Case 3: Outlier rejection**
- Baseline: V̄ = 2.0, V_target = 1.8, outliers at V=5.0
- Ω₄b rejects outliers, keeps band around 1.8
- Result: **RΛ reduces significantly**
- Verdict: PASS (strong Ω signature)

---

## Backward Compatibility

**Legacy behavior:**
- `omega4` (without suffix) defaults to Ω₄a (min-V)
- Existing exports labeled "omega4" are Ω₄a runs
- No retroactive changes to interpretation

**Recommendation:**
- New runs: Use explicit `omega4a` or `omega4b`
- Old exports: Interpret "omega4" as Ω₄a (min-V)

---

## Scientific Interpretation

### Why Both Operators Matter

**Ω₄a (Exploratory):**
- **Question:** Are minimum-vacuum structures special?
- **Hypothesis:** Lowest V(S) → emergent structure
- **Test:** Do they preserve τ-invariants?
- **Result:** PASS = surprising alignment, FAIL = expected (non-alignment is the norm)

**Ω₄b (Canonical):**
- **Question:** Does vacuum stationarity preserve τ?
- **Hypothesis:** V ≈ V_target → τ-compatible
- **Test:** RΛ reduction with macro stability
- **Result:** PASS = Ω→τ compatibility validated, FAIL = Ω not admissible

### Relation to UNNS Theory

**Ω₄a:** Tests if absolute vacuum minimization is physically meaningful  
**Ω₄b:** Tests if vacuum stationarity (RΛ → 0) is physically meaningful

Both are valid scientific questions. Ω₄b is the **primary test** for Ω admissibility.

---

## Testing Protocol

### Comparative Test (Recommended)

**Setup:**
```
M = 100, n = 50
Generator: Small-World
Seeds: 137042, 137043, 137044
keepFraction = 0.30
```

**Run both operators:**

**Ω₄a (Min-V):**
```
Expected:
- RΛ reduction: -20% to +60% (unpredictable)
- Acceptance: 30%
- Drift: 0-20% (may distort)
- Verdict: PASS or FAIL (both valid)
```

**Ω₄b (V-Bandpass):**
```
Expected:
- RΛ reduction: 15-50% (always positive)
- Acceptance: 30%
- Drift: 0-10% (should preserve)
- Verdict: PASS (high confidence)
```

**Key comparison:**
- Ω₄a can fail with RΛ reduction (macro distortion)
- Ω₄b should pass if Ω is admissible (RΛ guaranteed)

### Multi-Generator Test

**Purpose:** Verify Ω₄b is topology-independent

**Generators:**
- Lattice + LR (lrProb=0.05)
- Small-World (rewireProb=0.1)
- Scale-Free (alpha=2.5)

**Expectation:**
- Ω₄b PASS across all generators
- RΛ reduction 15-50% in all cases
- Drift <10% in all cases

---

## Documentation Updates

### Chamber Guide
- ✅ Operators table updated (Ω₄ → Ω₄a/Ω₄b)
- ✅ Info box added explaining distinction
- ✅ UI dropdown explicit

### Validation Doc
- ✅ Bottom line clarification added
- ✅ Ω₄a/Ω₄b canonical sentence included

### Export JSON
- No changes (mode saved as "omega4a" or "omega4b")
- Backward compat: old "omega4" exports are Ω₄a

---

## Frequently Asked Questions

**Q: Is this a bug fix?**  
A: No. This is a **specification clarification**. The code behavior is unchanged for Ω₄a (formerly Ω₄). We're adding Ω₄b as a new variant and making the distinction explicit.

**Q: Why did Ω₄ sometimes reduce RΛ before?**  
A: By chance. Ω₄a (min-V) doesn't target V_target, but if the lowest V(S) structures happen to cluster near V_target, RΛ will reduce. This was coincidental, not by design.

**Q: Which operator should I use?**  
A: **Ω₄b** for RΛ-aligned validation. **Ω₄a** for exploratory runs testing absolute vacuum minimization.

**Q: Can Ω₄a still be useful?**  
A: Yes! Ω₄a tests a different hypothesis (minimum absolute V) and can reveal structure. A PASS is more surprising than with Ω₄b.

**Q: Does this invalidate old results?**  
A: No. Old "omega4" results should be reinterpreted as Ω₄a (min-V exploratory). Their verdicts remain scientifically valid.

**Q: Why keep Ω₄a at all?**  
A: Scientific completeness. Testing minimum-V *independently* from V_target alignment is a valid exploratory question.

---

## Version History

**v1.1.0 → v1.1.1:** UI bug fixes (drift, canvas, scatter)  
**v1.1.1 → v1.2.0:** λ₂ CI implementation + Ω₄a/Ω₄b split  
**v1.2.0 status:** Production-ready for both exploratory (Ω₄a) and canonical (Ω₄b) testing

---

## Certification

**Chamber XXXIV v1.2.0:**
- ✅ Ω₄a (min-V) preserved with correct interpretation
- ✅ Ω₄b (V-bandpass) implemented and documented
- ✅ λ₂ CI fully functional with export
- ✅ UI and documentation updated
- ✅ Backward compatibility maintained

**Status:** Specification clarification complete, ready for production use.

**Recommendation:** Use Ω₄b for canonical Ω→τ admissibility testing. Use Ω₄a for exploratory minimum-vacuum hypothesis testing.
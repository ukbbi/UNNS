# Chamber XXX — Conservation Violation Detector

> **A computational instrument for detecting conservation law violations in proto-closed refinement systems**

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)]()
[![Tests](https://img.shields.io/badge/tests-6%2F6%20passed-brightgreen)]()
[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()

---

## Overview

Chamber XXX is a diagnostic computational environment designed to test conservation claims in discrete refinement systems. It distinguishes between three critical regimes:

| Regime | Closure | Conservation | Diagnostic Signature |
|--------|---------|--------------|---------------------|
| **Pure Cycle** | Proto-closed | Holds | Zero divergence everywhere |
| **Structural Collapse** | None | N/A | Boundary divergence (+1/-1) |
| **Cycle + Leak** | Proto-closed | **Falsified** | Witness generated |

**Key capability:** Detects conservation-violating leaks from proto-closed cycles via witness generation.

---

## Validation Results

### ✅ ALL TESTS PASSED (6/6)

| Mechanism | Type | Verdict | Status |
|-----------|------|---------|--------|
| `A_pure_cycle` | Positive control | Proto-closed, Conservative | ✅ |
| `B_expansion` | Negative control | Structural collapse | ✅ |
| `C_balanced_leak` | False-positive guard | Proto-closed, Conservative | ✅ |
| `M_conservative` | Compensated branches | Proto-closed, Conservative | ✅ |
| **`M_leak`** | **Cycle + leak** | **Proto-closed, FALSIFIED** | ✅ |
| `M_collapse` | Unbounded expansion | Structural collapse | ✅ |

---

## Critical Test: M_leak

**Configuration:**
```
Σ = {a, b}
Rules:
  r1: a → b  (cycle)
  r2: b → a  (cycle)
  r3: a → aa (leak, initially blocked)
  
Schedule:
  Steps 0-9:  Constraint level 0 (leak blocked)
  Step 10:    Constraint level 1 (leak enabled)
```

**Result:**
```json
{
  "closure": "proto-closed",
  "conservation": "FALSIFIED",
  "witness": {
    "type": "cycle-with-leak",
    "cycle": ["a", "b"],
    "leak": "a → aa",
    "falsifies_conservation": true
  }
}
```

**Interpretation:**

The system maintains a proto-closed cycle {a ↔ b} for 10 steps, then executes a **closure-relevant leak** to external state 'aa'. The chamber:

1. ✅ Detected the proto-closed cycle
2. ✅ Identified the leak edge
3. ✅ Generated a witness proving conservation violation
4. ✅ Computed divergence flux: +1 at source, -1 at target

**This is genuine falsification** — not curve-fitting, not narrative adjustment.

---

## Divergence Carrier: Z[O,R,P]

Chamber XXX uses a three-component divergence carrier to track structural changes:

- **O**: Orbit-preserving transformations
- **R**: Reductions/contractions
- **P**: Projections/expansions

### Divergence Patterns

**Perfect closure (A, C, M_conservative):**
```
All vertices: O=0, R=0, P=0
```

**Structural collapse (B, M_collapse):**
```
Source:  O=0, R=0, P=+1
Sink:    O=0, R=0, P=-1
```

**Cycle + leak (M_leak):**
```
Cycle:        O=0, R=0, P=0
Leak source:  O=0, R=0, P=+1
Leak target:  O=0, R=0, P=-1
```

---

## Witness System

### Witness Generation

For mechanism `M_leak`, the chamber generated:

```json
{
  "type": "cycle-with-leak",
  "cycle_size": 2,
  "cycle_nodes": ["a", "b"],
  "leak_source": "a",
  "leak_target": "aa",
  "leak_edge": {
    "action": "r3: a => aa",
    "rule_type": "P",
    "is_leak": true,
    "closure_relevant": true
  },
  "leak_flux": {"O": 0, "R": 0, "P": 1},
  "falsifies_conservation": true,
  "pattern_signature": "cycle:a,b|leak:a->aa"
}
```

### Witness Metadata

- **Cycle identification:** Correctly identified 2-state cycle
- **Leak detection:** Flagged closure-relevant escape edge
- **Flux computation:** Matched divergence at source (+1 in P component)
- **Conservation verdict:** Correctly flagged falsification

---

## False-Positive Protection

### C_balanced_leak Test

**Configuration:** Leak rule `a → c` available but never executed

**Result:** ✅ NO FALSE POSITIVE

The chamber correctly:
- Did NOT flag the available leak as a violation
- Maintained zero divergence (stayed in cycle)
- Generated NO witnesses
- Classified as proto-closed + conservative

**Conclusion:** Chamber only flags **executed** closure-relevant leaks, not merely available paths.

---

## Production Readiness

### Code Quality: ✅ EXCELLENT

- Clean JSON output format
- Complete metadata tracking
- Comprehensive witness generation
- Robust edge classification

### Diagnostic Capability: ✅ COMPLETE

All three critical regimes validated:
1. Proto-closure detection
2. Structural collapse detection
3. Conservation violation detection

### Reproducibility: ✅ DETERMINISTIC

All runs used seed 137042. Results fully reproducible.

---

## Usage

### Running a Test

```javascript
// Load mechanism configuration
const mechanism = {
  name: "M_leak",
  sigma: ["a", "b"],
  rules: [
    {id: "r1", repr: "a => b", type: "O"},
    {id: "r2", repr: "b => a", type: "O"},
    {id: "r3", repr: "a => aa", type: "P"}
  ],
  constraints: [...],
  refinement_schedule: [...]
};

// Execute
const result = chamber.execute(mechanism);

// Check witnesses
if (result.witnesses.summary.falsifies) {
  console.log("Conservation FALSIFIED");
  console.log(result.witnesses.witnesses);
} else {
  console.log("Conservation holds");
}
```

### Output Bundle

Each test produces a complete evidence bundle:

```json
{
  "meta": {...},
  "trace": {
    "states": [...],
    "steps": [...]
  },
  "graph": {
    "vertices": [...],
    "edges": [...],
    "metrics": {...}
  },
  "divergence": {
    "divergence_map": {...},
    "summary": {...}
  },
  "witnesses": {
    "witnesses": [...],
    "summary": {...}
  }
}
```

---

## Scientific Significance

### Falsification Capability

Chamber XXX provides **empirical falsification** of conservation claims:

1. **Theory claims:** "Proto-closed systems conserve divergence flux"
2. **Chamber tests:** Execute M_leak mechanism
3. **Result:** Witness generated, conservation falsified
4. **Conclusion:** Theory claim requires refinement or scoping

### Diagnostic Precision

The chamber distinguishes three structurally distinct regimes with high precision:

- **Zero divergence** → Proto-closed, conservative
- **Boundary divergence** → Structural collapse
- **Witness generated** → Proto-closed, conservation falsified

This enables rigorous testing of theoretical predictions.

---

## Comparison with Other Chambers

### Chamber XXXI (Ordering Noise)
- **Focus:** Robustness of least-divergence selection
- **Method:** σ-sweeps, statistical validation
- **Result:** Universal behavior, phase transitions

### Chamber XXX (Conservation Violation)
- **Focus:** Conservation law falsification
- **Method:** Witness generation, divergence analysis
- **Result:** Successful falsification via cycle-with-leak

**Complementary roles:** XXXI validates selection robustness; XXX validates (or falsifies) conservation.

---

## Limitations

### Scope

Chamber XXX is designed for:
✅ Finite proto-closed systems  
✅ Discrete state spaces  
✅ Deterministic refinement  
✅ Z[O,R,P] divergence carrier  

It is NOT designed for:
❌ Infinite-depth refinement  
❌ Stochastic rule selection  
❌ Continuous state spaces  
❌ Multi-component interactions beyond Z[O,R,P]  

---

## Files

### Validation Data

All test results available in complete evidence bundles:

- `A_pure_cycle_complete_bundle.json` — Positive control
- `B_expansion_complete_bundle.json` — Structural collapse
- `C_balanced_leak_complete_bundle.json` — False-positive guard
- `M_conservative_complete_bundle.json` — Compensated branches
- **`M_leak_complete_bundle.json`** — **Critical conservation test**
- `M_collapse_complete_bundle.json` — Unbounded expansion

### Documentation

- `CHAMBER_XXX_VALIDATION.md` — Complete validation report
- `README.md` — This file

---

## Installation

Chamber XXX is a single self-contained HTML file:

```bash
# No installation required
open chamber_xxx_mvp.html
```

**Requirements:**
- Modern web browser (Chrome, Firefox, Edge, Safari)
- JavaScript enabled

**No dependencies, no build process, no server.**

---

## Quick Start

1. Open `chamber_xxx_mvp.html` in browser
2. Select mechanism from dropdown
3. Click "Run Mechanism"
4. View results in real-time
5. Download evidence bundle

**Example output:**

```
Mechanism: M_leak
Closure: proto-closed
Conservation: FALSIFIED ✗

Witness detected:
  Type: cycle-with-leak
  Cycle: {a, b}
  Leak: a → aa
  Verdict: Conservation violation confirmed
```

---

## Citation

If you use Chamber XXX in research, please cite:

```bibtex
@software{chamber_xxx,
  title = {Chamber XXX: Conservation Violation Detector},
  author = {UNNS Research Collective},
  year = {2025},
  version = {1.0.0},
  url = {https://unns.tech/chamber_xxx}
}
```

---

## License

Research use: Free and open  
Commercial use: Contact UNNS Research Collective  

---

## Contact

**UNNS Research Collective**  
Email: contact@unns.tech  
Web: https://unns.tech  

---

## Acknowledgments

Chamber XXX builds on theoretical foundations from:
- UNNS Substrate framework
- Divergence carrier formalism (Z[O,R,P])
- Proto-closure theory

Special thanks to contributors who tested early versions and provided feedback.

---

## Changelog

### v1.0.0 (2025-12-29)
- ✅ Initial production release
- ✅ All 6 validation tests passed
- ✅ Witness system complete
- ✅ Divergence carrier validated
- ✅ False-positive protection verified

---

**Status:** ✅ PRODUCTION READY  
**Validation:** 6/6 tests passed  
**Confidence:** High — All critical capabilities validated  

**Chamber XXX is ready for scientific use in conservation falsification testing.**

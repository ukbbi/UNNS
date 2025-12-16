# Comparison Result Card  
## τ-Filtered Observability — Multi-Run Structural Comparison

**Chamber:** τ-Filtered Observability — Foundations Chamber  
**Context:** Canonical comparison (validated imports)  
**Comparison Type:** Multi-run τ-filtered structural analysis  
**Runs Compared:** 4  
**Operator Alphabet:** Φ, Ψ, τ, XII  

---



## How to Read This Card

This card summarizes what remains **structurally consistent** when several runs of the same system are compared under different parameters.

You do **not** need to understand the internal mathematics to read it correctly:

- **Runs** are separate executions of the same process with different settings.
- **Survival ratio** shows how much of each run remains admissible under τ-filtering.
- **Stability** indicates whether these survival rates behave consistently across runs.
- **Paths** are sequences of operations; persistence means the same sequence appears in multiple runs.
- **Collapse** marks where the system exceeds admissibility limits and is filtered out.
- **Operators (Φ, Ψ, τ, XII)** label types of behavior, not physical objects.

The card answers three practical questions:

1. *Does the system behave consistently across variations?*  
2. *Which structures persist, and which depend on initial conditions?*  
3. *Where do admissibility limits (collapse) appear?*

All values shown here are computed directly by the Chamber and can be reproduced
by re-importing the same data files.

---

## Compared Datasets

This comparison aggregates the following validated runs:

- `test_run_comparison.json`
- `test_run_high_lambda.json`
- `test_run_low_lambda.json`
- `test_run_mixed_operators.json`
- `test_run_varied_params.json`

Each run differs in seed and/or parameter regime (Λ, δ, ε),
but conforms to the same UNNS execution and schema contract.

---

## Structural Alignment Summary

| Metric | Value |
|------|------|
| Aligned Runs | **4 / 4** |
| Common State Bins (B) | **20** |
| Maximum Path Length | **10** |
| Operator Alphabet | **Φ, Ψ, τ, XII** |

All runs are structurally alignable under the Chamber’s binning
and path normalization rules, enabling meaningful comparison.

---

## τ-Survival Stability

### Survival Ratio per Run

- **Run 1:** ~72%
- **Run 2:** ~70%
- **Run 3:** ~88%
- **Run 4:** ~78%

**Mean Survival Ratio:** **79.2%**  
**Variance (σ²):** **0.0191**

**Stability Verdict:** **Stable**

Interpretation:  
Despite parameter variation, the system exhibits a consistent
τ-admissible survival rate across runs.

---

## Path Persistence Analysis

| Measure | Result |
|------|------|
| Paths in All Runs | **0** |
| Paths in ≥50% of Runs | **1** |

Interpretation:  
No single operator path is globally invariant across all runs.
However, at least one path persists in a majority of runs,
indicating partial structural robustness with seed dependence.

---

## Operator Dominance Drift

Observed operator frequency trends across runs:

- **Φ (Generation):** Peaks in mid-range Λ regimes
- **Ψ (Structural mediation):** Increases under parameter variation
- **τ (Admissible continuation):** Tracks survival ratio
- **XII (Collapse):** Present in **75% of runs**

This confirms that collapse is **selective**, not exceptional.

---

## Collapse Onset Detection

| Measure | Result |
|------|------|
| Runs with Collapse | **3 / 4** |
| Collapse Classification | **τ-Critical** |
| Seed Sensitivity | **High** |

Interpretation:  
Collapse is not universal but appears consistently under
certain admissibility regimes, marking a τ-critical boundary
rather than random instability.

---

## κ-Envelope Summary

The κ-envelope (min / median / max) across runs shows:

- bounded median curvature
- controlled divergence near collapse transitions
- consistent envelope shape across parameter variation

This supports the interpretation of κ as a **stability observable**,
not a numerical artifact.

---

## Structural Verdicts

| Metric | Classification | Justification |
|------|------|------|
| Survival Ratio Stability | **Stable** | Low variance across runs |
| Path Persistence | **Seed-Dependent** | No global invariant paths |
| Collapse Presence | **τ-Critical** | Collapse in 75% of runs |

---

## Interpretation (Public-Facing)

This comparison demonstrates that:

- τ-filtered observability produces **stable aggregate behavior**
  across varied parameters
- collapse (Operator XII) functions as a **selection mechanism**
  rather than a failure state
- structural invariants emerge statistically, not axiomatically

The result aligns with the UNNS framework in which
existence is determined operationally by survival
under recursive and observability constraints.

---

## Reproducibility

This card is reproducible by:

1. Opening `tau_filtered_observability_lab.html`
2. Importing the listed JSON files via **Compare → Import Run to Queue**
3. Executing comparison with default alignment settings

Any deviation from these results indicates a change
in Chamber logic or schema and must be versioned explicitly.

---

## Status

**Comparison Status:** Validated  
**Canonical Role:** Reference comparison for τ-filtered observability  
**Intended Use:** Documentation, citation, regression baseline

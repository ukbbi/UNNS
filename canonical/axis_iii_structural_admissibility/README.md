# axis_iii_structural_admissibility

Structural admissibility program for **UNNS (Unbounded Nested Number Sequences)**  
Axis II → Axis III transition and formalization of the **Structural Irreversibility Criterion**.

---

## 1. Scope

This folder contains the complete experimental and theoretical closure of:

- **Axis II** — Operator Control Hypothesis (falsified)
- **Axis III** — Structural Admissibility Hypothesis (confirmed)

Primary result:

> Worldline-local utility is admissible **iff** the underlying grammar–topology structure enforces irreversible convergence of histories.

---

## 2. Folder Contents

| File | Role |
|------|------|
| `axis_ii_iii_laboratory_v1_0_0.html` | Integrated laboratory dashboard (Axis II + Axis III) |
| `chamber_xlv_v1_3_0_temporal_injection.html` | Chamber XLV — ε–κ–t sweep |
| `chamber_xlvi_v1_0_0_temporal_generative.html` | Chamber XLVI — Temporal–Generative Alignment |
| `chamber_xlvii_v1_0_0_structural_admissibility.html` | Chamber XLVII — Structural Admissibility Test |
| `structural_irreversibility_unns_article_v1_0_0.html` | Public-facing research article |
| `Structural Irreversibility and the Admissibility of Worldline-Local Utility.pdf` | Technical monograph (PDF) |


---

## 3. Research Architecture

### 3.1 Axis II — Operator Control (Falsified)

Tested whether utility can be induced or stabilized via:

- ε — static asymmetry
- κ — coherence regulation
- γ — generative bias
- temporal injection timing

**Total runs:** 160 (pre-registered)  
**Result:** No admissibility transitions observed.

Formal closure:


G° ≠ f(ε)
G° ≠ f(κ)
G° ≠ f(γ)
G° ≠ f(timing)


Operator-level control of worldline-local utility is insufficient.

---

### 3.2 Axis III — Structural Admissibility (Confirmed)

Operators disabled:


ε = 0
κ = 0
γ = 0


Independent variables:

- Grammar ∈ {G1, G2, G3}
- Topology ∈ {Balanced Tree, Asymmetric Tree, DAG}

Total simulations:


3 grammars × 3 topologies × 50 seeds = 450 runs


Observed correlation:

- All DAG structures admit utility
- No tree structures admit utility
- Grammar modulates frequency but not admissibility

---

## 4. Structural Irreversibility Criterion

### Definition

A grammar–topology structure is **structurally irreversible** if:

There exist histories h₁, h₂ and time t such that:

- h₁(t) ≠ h₂(t)
- ∃ t' > t where h₁(t') = h₂(t')
- No inverse operation recovers the prior distinction

### Theorem

Worldline-local utility is admissible **iff** the structure is structurally irreversible.

Implications:

- DAG structures → admissible
- Tree structures → inadmissible
- Cyclic structures → inadmissible (merge reversibility reintroduced)

---

## 5. Structural Distinction

### Trees

- Single parent per node
- Histories diverge but never merge
- Structural separability preserved
- Process-irreversible but structurally reversible

Result: No worldline commitment.

### Directed Acyclic Graphs (DAGs)

- Multiple parents allowed
- Independent histories can merge
- Separability destroyed after merge
- Structurally irreversible

Result: Worldline commitment enforced.

---

## 6. Methodological Status

This folder represents a **closed research arc**:

1. Hypothesis generation (operator control)
2. Pre-registered falsification
3. Exhaustion of explanatory class
4. Structural reframing
5. Law-level consolidation

Axis II is permanently closed under current substrate assumptions.

Future research must operate at the structural taxonomy level, not operator tuning.

---

## 7. Reproducibility

All simulations:

- Fixed depth = 400
- No early stopping
- 50 independent seeds per structure
- Operators disabled in Axis III

Dashboard (`axis_ii_iii_laboratory_v1_0_0.html`) provides:

- Frequency summaries
- Seed-level inspection
- Structure-level comparisons

---

## 8. Integration within UNNS

This result:

- Strengthens Chamber XLIV existence proof
- Clarifies limits of operator-driven models
- Formalizes worldline commitment as topology-level fact
- Elevates admissibility from dynamic emergence to structural permission

The Structural Irreversibility Criterion becomes part of the UNNS admissibility framework.

---

## 9. Status

- Axis II: Falsified
- Axis III: Confirmed
- Structural law: Extracted
- Operator tuning: Scientifically closed

---

**Terminal statement**

Worldline-local utility is not something a system can be made to do.  
It is something a structure either permits or forbids.